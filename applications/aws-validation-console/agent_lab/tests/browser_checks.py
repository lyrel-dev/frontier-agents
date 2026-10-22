#!/usr/bin/env python3
"""UI checks. --native requires native navigation; --bridge is explicitly limited.
Only this test harness supplies provider fixtures. Product files contain no demo data.
"""
import argparse,asyncio,json,os,socket,sys,tempfile,threading,time,urllib.request,urllib.error
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
import uvicorn
from lab.api import create_app
from lab.models import Configuration
from lab.store import Store
from lab.service import Service

ROOT=Path(__file__).resolve().parents[1]
OP='test-only-operator-credential-123456789';AP='test-only-approval-credential-123456789'


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--native',action='store_true');parser.add_argument('--bridge',action='store_true');a=parser.parse_args()
 if not (a.native or a.bridge):parser.error('Choose --native or the explicitly limited --bridge harness')
 output=ROOT/'validation';output.mkdir(exist_ok=True);checks=[]
 def check(label,value):
  assert value,label
  checks.append(label);print('PASS',label)
 with tempfile.TemporaryDirectory() as d:
  config=Configuration();store=Store(d);app=create_app(config,store,OP,AP)
  @app.middleware('http')
  async def delayed_workspace(request,call_next):
   # Exercise the unlock/loading race with actual HTTP latency, not a sleep in the test.
   if request.url.path=='/api/workspace':await asyncio.sleep(.2)
   return await call_next(request)
  sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
  server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=port,log_level='error',access_log=False))
  thread=threading.Thread(target=server.run,daemon=True);thread.start()
  for _ in range(100):
   if server.started:break
   time.sleep(.02)
  base=f'http://127.0.0.1:{port}'
  try:
   with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
    page=b.new_page(viewport={'width':1440,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    if a.native:
     page.goto(base,wait_until='networkidle')
    else:
     def bridge(source,path,options):
      assert path.startswith('/api/') and not path.startswith('//')
      req=urllib.request.Request(base+path,data=options.get('body','').encode() if 'body' in options else None,headers=options.get('headers',{}),method=options.get('method','GET'))
      try:
       with urllib.request.urlopen(req) as r:return {'status':r.status,'body':r.read().decode(),'headers':dict(r.headers)}
      except urllib.error.HTTPError as e:return {'status':e.code,'body':e.read().decode(),'headers':dict(e.headers)}
     page.expose_binding('__testHTTPBridge',bridge)
     html=(ROOT/'static/index.html').read_text().replace('<link rel="stylesheet" href="/static/style.css">','<style>'+ (ROOT/'static/style.css').read_text()+'</style>')
     html=html.replace('<script defer src="/static/charts.js"></script>','').replace('<script defer src="/static/app.js"></script>','')
     page.set_content(html)
     page.evaluate("()=>{window.fetch=async(path,options={})=>{const r=await window.__testHTTPBridge(path,options);return new Response(r.body,{status:r.status,headers:r.headers})}}")
     page.add_script_tag(content=(ROOT/'static/charts.js').read_text());page.add_script_tag(content=(ROOT/'static/app.js').read_text())
    check('empty install has no fabricated observations','No measured trials yet' in page.locator('body').inner_text())
    check('execution starts locked',page.locator('#write-state').text_content()=='Execution locked')
    check('trial registration disabled without binding',page.get_by_role('button',name='Register experiment',exact=True).is_disabled())
    page.screenshot(path=str(output/'empty-desktop.png'),full_page=True)
    page.get_by_role('button',name='Unlock workspace').click();page.get_by_label('Operator token',exact=True).fill(OP);page.get_by_role('button',name='Unlock',exact=True).click()
    deadline=time.monotonic()+10
    while time.monotonic()<deadline:
     if page.evaluate('Boolean(state.token && state.workspace && state.config)'):break
     time.sleep(.05)
    check('operator token unlocks a real local HTTP backend',page.get_by_role('button',name='Lock workspace').count()==1)
    check('workspace response completed despite delayed HTTP',page.evaluate('Boolean(state.workspace && state.config)'))
    check('unlocked workspace still has zero experiments',page.evaluate('state.workspace.entities.length')==0)
    for view in ['trials','prevention','evidence','connections','overview']:
     page.locator('[data-view="'+view+'"]').click()
     check('navigation '+view,page.evaluate('state.view')==view)
    page.set_viewport_size({'width':390,'height':844})
    for view in ['overview','trials','prevention','evidence','connections']:
     page.locator('[data-view="'+view+'"]').click()
     check('mobile layout '+view,page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
    page.locator('[data-view="overview"]').click();page.screenshot(path=str(output/'empty-mobile.png'),full_page=True)
    check('no token in browser persistent storage',page.evaluate('(()=>{try{return localStorage.length===0&&sessionStorage.length===0}catch{return true}})()'))
    page.get_by_role('button',name='Lock workspace').click()
    check('lock removes credential and data',page.evaluate("state.token==='' && state.workspace===null && state.detail===null"))
    # Explicit test-only graphs; not inserted in product assets or preview.
    page.set_viewport_size({'width':1440,'height':1000})
    page.evaluate("""()=>{document.querySelector('#view').replaceChildren();let h=document.createElement('div');h.id='test-graph';document.querySelector('#view').append(h);LabCharts.draw(h,{title:'Test fixture only',unit:'ms',series:[{name:'Fixture',interval_ms:1000,points:[{t:'2026-01-01T00:00:00Z',value:1},{t:'2026-01-01T00:00:01Z',value:null},{t:'2026-01-01T00:00:02Z',value:3}]}]})}""")
    check('metric has interactive SVG',page.locator('#test-graph svg').count()==1)
    check('metric graph keyboard focusable',page.locator('#test-graph svg').get_attribute('tabindex')=='0')
    check('CSV and table controls exist','CSV' in page.locator('#test-graph').inner_text() and 'Source samples' in page.locator('#test-graph').inner_text())
    check('graph has zoom controls',page.locator('#test-graph button').count()>=4)
    svg=page.locator('#test-graph svg');svg.focus();svg.press('Home');svg.press('ArrowRight')
    check('keyboard inspection reports an explicit gap rather than zero','No sample' in page.locator('#test-graph .chart-readout').inner_text())
    check('null gap is not connected by a polyline',page.locator('#test-graph polyline').count()==0)
    original_labels=svg.locator('text').all_text_contents()
    page.locator('#test-graph').get_by_role('button',name='Zoom +',exact=True).click()
    check('zoom changes the visible time interval',svg.locator('text').all_text_contents()!=original_labels)
    page.locator('#test-graph').get_by_role('button',name='Reset',exact=True).click()
    check('reset restores the full interval',svg.locator('text').all_text_contents()==original_labels)
    toggle=page.locator('#test-graph .chart-legend button');toggle.click()
    check('series can be hidden',toggle.get_attribute('aria-pressed')=='false' and page.locator('#test-graph circle').count()==0)
    toggle.click();check('series can be restored',toggle.get_attribute('aria-pressed')=='true' and page.locator('#test-graph circle').count()==2)
    page.locator('#test-graph summary').click()
    page.locator('#test-graph .sample-table').get_by_role('cell',name='No sample',exact=True).wait_for()
    check('source table preserves the null sample','No sample' in page.locator('#test-graph .sample-table').inner_text())
    with page.expect_download() as dl:
     page.locator('#test-graph').get_by_role('button',name='CSV',exact=True).click()
    import csv,io
    rows=list(csv.reader(io.StringIO(Path(dl.value.path()).read_text())))
    check('CSV exports every original point including its empty gap',len(rows)==4 and rows[2][2]=='')
    check('no JavaScript errors',not errors)
    b.close()
  finally:server.should_exit=True;thread.join(10)
 report={'passed':len(checks),'checks':checks,'native_navigation':a.native,'provider_access':'none','browser_bridge':a.bridge,
         'not_verified':[] if a.native else ['Native browser navigation, fetch/CORS, and served CSP enforcement; harness injects DOM and bridges API calls to a real loopback HTTP server.']}
 (output/'browser-review.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
