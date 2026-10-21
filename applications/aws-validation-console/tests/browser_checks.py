"""Browser behavior checks. Uses set_content because this environment blocks navigation.
The live-service checks bridge fetch to a real FastAPI TestClient; they do not test TCP/CSP.
Run: python tests/browser_checks.py
"""
import json,sys,tempfile,base64,shutil,os
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from playwright.sync_api import sync_playwright
from fastapi.testclient import TestClient
from app.server import create_app
TOKEN='browser-test-only-token-0123456789abcdef'
results=[]
def check(name,value):
    assert value,name
    results.append({'name':name,'result':'pass'})
def route(page,name):
    page.evaluate('(x)=>location.hash=x',name)
    page.wait_for_timeout(80)
def close(page):
    page.evaluate("document.querySelectorAll('dialog[open]').forEach(d=>d.close())")
def inject(page,html,mode):
    page.set_content(html.replace("const MODE = location.protocol === 'file:' ? 'preview' : 'service';",f"const MODE = '{mode}';"))
    page.wait_for_selector('h1')

html=(ROOT/'static/console.html').read_text()
out=ROOT/'validation';out.mkdir(exist_ok=True)
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'),headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1050},device_scale_factor=1)
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    inject(page,html,'preview')
    check('preview starts with 38 scenario revisions',page.locator('.metric-number').nth(1).inner_text()=='38')
    check('synthetic mode explicitly labelled','preview' in page.locator('#mode-bar').inner_text().lower())
    check('preview has no authenticated service',page.evaluate('state.unlocked===false && state.token===""'))
    page.screenshot(path=str(out/'desktop.png'),full_page=True)
    for r in ['connections','inventory','scenarios','runs','validations','reports','roadmap','data','overview']:
        route(page,r)
        check('desktop route '+r,page.locator('h1').count()==1 and page.locator('h1').inner_text()!='')
    route(page,'scenarios')
    for model in ['ec2','eks-ec2','eks-fargate','ecs-ec2','ecs-fargate','lambda']:
        page.select_option('#model-filter',model)
        check('scenario filter '+model,page.locator('tbody tr').count()>0)
    page.select_option('#model-filter','all')
    page.fill('#search-scenarios','nothing-matches-zzz')
    check('search empty state',page.locator('.filter-count').inner_text()=='0 records')
    page.fill('#search-scenarios','')
    page.evaluate("showDetail('execution_run:example-run-1@1')")
    page.locator('#drawer [data-action="evaluate"]').click()
    page.wait_for_timeout(150)
    check('preview evaluates known failure',page.evaluate("records('validation_run').at(-1).record.data.outcome==='fail'"))
    check('failure retains missing evidence check',page.evaluate("records('validation_run').at(-1).record.data.checks.some(x=>x.outcome==='inconclusive')"))
    page.screenshot(path=str(out/'validation-details.png'),full_page=True)
    page.locator('#drawer [data-action="report"]').click();page.wait_for_timeout(100)
    check('report is linked to new validation',page.evaluate("records('report').at(-1).record.data.validation_ref===records('validation_run').at(-1).meta.ref"))
    with page.expect_download() as d:
        page.locator('#drawer [data-action="download-report"]').click()
    downloaded=Path(d.value.path()).read_text()
    check('HTML report carries synthetic warning','SYNTHETIC EXAMPLE' in downloaded)
    close(page)
    # Immutable references cannot be silently overwritten.
    page.evaluate("openImport({schema_version:'1.0',kind:'validation_bundle',records:[{...clone(records('scenario')[0].record),title:'Changed title'}]})")
    page.locator('[data-action="review-import"]').click()
    check('immutable revision conflict visible','conflicts' in page.locator('#import-review').inner_text())
    check('conflicting import cannot commit',page.locator('#commit-import').is_disabled())
    close(page)
    page.evaluate('newScenario()')
    page.locator('[data-action="review-import"]').click()
    check('new definition can be reviewed',page.locator('#commit-import').is_enabled())
    text=page.locator('#import-json').input_value();page.fill('#import-json',text+' ')
    check('editing invalidates import preview',page.locator('#commit-import').is_disabled())
    page.locator('[data-action="review-import"]').click();page.locator('#commit-import').click()
    page.wait_for_timeout(80)
    check('new definition committed to preview memory',page.evaluate("records('scenario').length===39"))
    # Escaping and protocol restrictions apply to imported text.
    page.evaluate("openImport({schema_version:'1.0',kind:'validation_bundle',records:[{...clone(records('scenario')[0].record),id:'xss-test',title:'<img src=x onerror=alert(1)>',data:{...clone(records('scenario')[0].record.data),source_urls:['javascript:alert(1)']}}]})")
    page.locator('[data-action="review-import"]').click();page.locator('#commit-import').click();page.wait_for_timeout(80)
    page.evaluate("showDetail('scenario:xss-test@1')")
    check('imported title rendered as text',page.locator('#drawer img').count()==0 and '<img' in page.locator('#drawer h2').inner_text())
    check('unsafe source protocol not linked',page.locator('#drawer a[href^="javascript:"]').count()==0)
    close(page)
    with page.expect_download() as d:
        page.evaluate('exportWorkspace()')
    exported=json.loads(Path(d.value.path()).read_text())
    check('workspace export has imported revision',any(r['id']=='xss-test' for r in exported['records']))
    page.set_viewport_size({'width':390,'height':844});route(page,'overview');page.wait_for_timeout(400)
    clean=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    inject(clean,html,'preview');clean.wait_for_timeout(400)
    clean.screenshot(path=str(out/'mobile.png'),full_page=True);clean.close()
    check('mobile navigation initially hidden',not page.locator('#sidebar').is_visible())
    page.locator('[data-action="menu"]').click();page.wait_for_timeout(300)
    check('mobile menu opens',page.locator('#sidebar').is_visible())
    page.keyboard.press('Escape');page.wait_for_timeout(300)
    check('Escape closes mobile menu',not page.locator('#sidebar').is_visible())
    for r in ['connections','inventory','scenarios','runs','validations','reports','roadmap','data','overview']:
        route(page,r)
        check('mobile no page overflow '+r,page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'))
    check('preview no JavaScript errors',not errors)
    page.close()
    # Live-mode UI with real backend requests through a test bridge.
    with tempfile.TemporaryDirectory() as td:
        app=create_app(Path(td)/'data',token=TOKEN,testing=True)
        with TestClient(app) as client:
            page=browser.new_page(viewport={'width':1440,'height':1050})
            errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
            def bridge(path,opts):
                resp=client.request(opts.get('method','GET'),path,headers=opts.get('headers',{}),content=opts.get('body'))
                return {'status':resp.status_code,'contentType':resp.headers.get('content-type',''),'body':base64.b64encode(resp.content).decode()}
            page.expose_function('backendBridge',bridge)
            patch="""<script>window.fetch=async (path,opts={})=>{const r=await window.backendBridge(path,opts);return new Response(Uint8Array.from(atob(r.body),c=>c.charCodeAt(0)),{status:r.status,headers:{'Content-Type':r.contentType}});};</script>"""
            inject(page,html.replace('<script>const APP_DATA',patch+'<script>const APP_DATA'),'service')
            check('service begins locked without synthetic records',page.evaluate('!state.unlocked && state.entries.length===0'))
            page.locator('#unlock-button').click();page.fill('#console-token',TOKEN);page.locator('#unlock-form button[type="submit"]').click()
            page.wait_for_function('state.unlocked===true')
            check('unlock loads actual catalogue only',page.evaluate("records('scenario').length===37 && records('snapshot').length===0"))
            route(page,'connections')
            check('empty configuration remains empty',page.evaluate('state.connections.length===0'))
            page.evaluate('openImport(APP_DATA.examples)')
            page.locator('[data-action="review-import"]').click();page.wait_for_function("!document.querySelector('#commit-import').disabled")
            page.locator('#commit-import').click();page.wait_for_function("records('execution_run').length===2")
            check('live import origin assigned by backend',page.evaluate("get('execution_run:example-run-1@1').meta.origin==='imported'"))
            page.evaluate("showDetail('execution_run:example-run-1@1')")
            page.locator('#drawer [data-action="evaluate"]').click()
            page.wait_for_function("records('validation_run').length===3")
            check('live evaluation computed by Python evaluator',page.evaluate("records('validation_run').at(-1).record.data.evaluator_version==='scalar-1.0'"))
            page.locator('#drawer [data-action="report"]').click();page.wait_for_function("records('report').length===2")
            check('live report persisted',len(client.get('/api/workspace',headers={'Authorization':'Bearer '+TOKEN}).json()['records'])>37)
            close(page);page.locator('#unlock-button').click()
            check('locking removes token and displayed records',page.evaluate('state.token==="" && state.entries.length===0 && !state.unlocked'))
            check('live UI no JavaScript errors',not errors)
            page.close()
    browser.close()
(out/'browser-checks.json').write_text(json.dumps({'checks':len(results),'passed':len(results),'harness':'Chromium set_content; explicit mode override. Service fetch bridged to FastAPI TestClient. No real navigation/TCP/CSP enforcement or external connections tested.','results':results},indent=2))
print(f'{len(results)} browser checks passed')
