"""Exercise DOM-injected previews/reports and bridged loopback HTTP with CSP.
Browser navigation is blocked in the execution environment; this is not a file-navigation test.
No AWS, engine, Kubernetes or Grafana service is contacted.
"""
import csv, io, json, os, socket, sys, tempfile, threading, time, urllib.request, urllib.error, base64, hashlib, html
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from playwright.sync_api import sync_playwright
import uvicorn
from app.server import create_app
from build_ui import build_ui
build_ui()
OUT=Path(os.environ.get('METRICS_TEST_OUTPUT',ROOT/'validation-output'));OUT.mkdir(parents=True,exist_ok=True)
results=[]
def check(name,value):
    assert value,name
    results.append({'name':name,'result':'pass'});print('PASS',name,flush=True)
def wait_js(page,expr):
    for _ in range(100):
        if page.evaluate(expr):return
        page.wait_for_timeout(20)
    raise AssertionError(expr)
def route(page,name):
    page.evaluate('(x)=>location.hash=x',name);page.wait_for_timeout(90)
def close(page):page.evaluate("document.querySelectorAll('dialog[open]').forEach(d=>d.close())")
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1000});errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content((ROOT/'static/console.html').read_text().replace("const MODE = location.protocol === 'file:' ? 'preview' : 'service';", "const MODE = 'preview';"));page.wait_for_selector('h1')
    # about:blank lacks SubtleCrypto here. Supply real SHA-256 only in the test harness.
    page.expose_function('testHash',lambda text:hashlib.sha256(text.encode()).hexdigest())
    page.evaluate("async()=>{hash=async value=>window.testHash(stable(value));for(const e of state.entries)e.meta.sha256=await hash(e.record);}")
    check('preview DOM loads',page.evaluate("state.mode==='preview'"))
    check('every overview count has a graph',page.locator('.metric-card .mc-card').count()==page.locator('.metric-card').count()==4)
    check('overview incident metrics have graphs',page.locator('.mc-card:not(.mc-mini)').count()==4)
    page.locator('[data-mc="expand"]').first.click()
    check('workspace count expands to interactive graph',page.locator('#drawer [data-mc="csv"]').count()==1)
    close(page);route(page,'metrics')
    check('all 32 catalogue metrics have graphs',page.locator('.mc-card').count()==32)
    check('all 32 graphs have CSV controls',page.locator('[data-mc="csv"]').count()==32)
    check('all 32 graphs keyboard accessible',page.locator('.mc-svg[tabindex="0"]').count()==32)
    check('synthetic demonstration clearly identified','SYNTHETIC GRAPH EXAMPLE' in page.locator('.metrics-intro').inner_text())
    check('synthetic demo not silently imported',page.evaluate("!get('scenario:EXAMPLE-METRICS@1')"))
    page.locator('[data-metrics-field="query"]').fill('latency · p95')
    check('metric search filters graph cards',page.locator('.mc-card').count()==1)
    card=page.locator('.mc-card').first;svg=card.locator('.mc-svg')
    check('explicit missing interval breaks line',card.locator('path.mc-series').count()==2)
    check('incident markers rendered',card.locator('.mc-event').count()==6)
    card.locator('summary').filter(has_text='Incident markers').click()
    check('incident marker list contains timestamps','10:05:42 UTC' in card.inner_text())
    svg.focus();page.keyboard.press('Home');page.keyboard.press('ArrowRight')
    check('keyboard inspects next actual sample','10:00:10 UTC' in card.locator('.mc-tooltip').inner_text())
    page.keyboard.press('Home')
    for _ in range(45):page.keyboard.press('ArrowRight')
    check('missing sample not shown as zero','No sample' in card.locator('.mc-tooltip').inner_text())
    card.locator('[data-mc="in"]').click()
    check('zoom narrows range',page.evaluate("[...MetricCharts.registry.values()].find(x=>document.querySelector(`[data-chart=\"${x.id}\"]`)).range!==null"))
    card.locator('[data-mc="reset"]').click()
    check('reset restores complete extent',page.evaluate("[...MetricCharts.registry.values()].find(x=>document.querySelector(`[data-chart=\"${x.id}\"]`)).range===null"))
    svg.focus();page.keyboard.press('+');page.keyboard.press('+')
    check('keyboard zoom retains focus',page.evaluate("document.activeElement.classList.contains('mc-svg')"))
    card.locator('[data-mc="reset"]').click();box=svg.bounding_box()
    page.mouse.move(box['x']+box['width']*.25,box['y']+box['height']*.55)
    page.mouse.down();page.mouse.move(box['x']+box['width']*.75,box['y']+box['height']*.55,steps=8);page.mouse.up()
    check('drag selects time range',page.evaluate("[...MetricCharts.registry.values()].find(x=>document.querySelector(`[data-chart=\"${x.id}\"]`)).range!==null"))
    card.locator('[data-mc="reset"]').click();card.locator('[data-mc="toggle"]').click()
    check('legend can hide series',card.locator('path.mc-series').count()==0)
    card.locator('[data-mc="toggle"]').click()
    check('legend can restore series',card.locator('path.mc-series').count()==2)
    with page.expect_download() as result:card.locator('[data-mc="csv"]').click()
    csv_text=Path(result.value.path()).read_text();rows=list(csv.reader(io.StringIO(csv_text)))
    check('CSV retains all 90 actual samples',len(rows)==91)
    check('CSV preserves explicit null as empty',any(row[1]=='' for row in rows[1:]))
    check('CSV includes source and immutable reference','source,evidence_ref' in rows[0][-2]+','+rows[0][-1])
    page.locator('[data-metrics-field="from"]').fill('2026-10-21T10:10');page.locator('[data-metrics-field="from"]').dispatch_event('change')
    check('global UTC range filters samples',page.evaluate("[...MetricCharts.registry.values()].filter(x=>document.querySelector(`[data-chart=\"${x.id}\"]`)).every(x=>x.spec.traces.every(t=>t.points.every(p=>p.t>=Date.parse('2026-10-21T10:10:00Z'))))"))
    page.locator('[data-metrics-action="reset"]').click()
    page.locator('[data-metrics-field="source"]').select_option('workspace')
    check('workspace does not fabricate latency','Not measured' in page.locator('.mc-card').filter(has=page.locator('h3',has_text='Request latency · p95')).inner_text())
    page.locator('[data-metrics-field="presence"]').select_option('missing')
    check('missing filter contains no recorded points',page.locator('.mc-point').count()==0)
    page.locator('[data-metrics-action="reset"]').click()
    page.locator('[data-metrics-field="run"]').select_option('execution_run:example-run-2@1')
    detection=page.locator('.mc-card').filter(has=page.locator('h3',has_text='Time to detection'))
    check('missing detection remains unmeasured for selected run','Not measured' in detection.inner_text())
    # Unknown metrics are discovered automatically, with no guessed unit conversion.
    page.evaluate("const x=clone(records('evidence')[0]);x.record.id='custom-graph';x.record.data.metric='custom_metric';x.record.data.unit='widgets';x.record.data.run_ref='execution_run:example-run-2@1';x.meta.ref=rid(x.record);state.entries.push(x);render();")
    check('imported custom metric gets graph automatically',page.locator('.mc-card').count()==33)
    page.evaluate("showDetail('scenario:EXAMPLE-RECOVERY@1')")
    check('scenario assertions and custom evidence have graphs',page.locator('#drawer .mc-card').count()==5)
    close(page);page.evaluate("showDetail('execution_run:example-run-1@1')")
    check('execution graph includes missing assertion',page.locator('#drawer .mc-card').count()==4)
    close(page);page.evaluate("showDetail('validation_run:example-validation-1@1')")
    check('validation graphs include pinned evidence and missing check',page.locator('#drawer .mc-card').count()==4)
    close(page);page.evaluate("showDetail('evidence:example-1-recovery_seconds@1')")
    check('individual evidence has graph',page.locator('#drawer .mc-card').count()==1)
    close(page);page.evaluate("showDetail('snapshot:example-aws@1')")
    check('snapshot has counts and coverage graphs',page.locator('#drawer .mc-card').count()==4)
    denied=page.locator('#drawer .mc-card').filter(has=page.locator('h3',has_text='cloudwatch'))
    check('denied collection count is missing not zero',denied.locator('.mc-point').count()==0)
    close(page);page.evaluate("showResource('snapshot:example-kubernetes@1','example-kubernetes-1')")
    check('numeric resource facts have graphs',page.locator('#drawer .mc-card').count()==2)
    close(page);page.evaluate("showDetail('report:example-report@1')")
    check('report view has frozen input graphs',page.locator('#drawer .mc-card').count()==4)
    with page.expect_download() as result:page.locator('[data-action="download-report"]').click()
    report_path=OUT/'interactive-report.html';result.value.save_as(report_path)
    report=browser.new_page(viewport={'width':1280,'height':900});report_errors=[];report.on('pageerror',lambda e:report_errors.append(str(e)))
    requests=[];report.on('request',lambda req:requests.append(req.url))
    report.set_content(report_path.read_text());report.wait_for_selector('.mc-card')
    check('exported report DOM runs offline with graphs',report.locator('.mc-card').count()==4)
    check('exported report keeps synthetic warning','SYNTHETIC EXAMPLE' in report.locator('.warning').inner_text())
    report.locator('.mc-svg').first.focus();report.keyboard.press('Home')
    check('exported report graph is interactive',report.locator('.mc-tooltip:not([hidden])').count()==1)
    check('exported report makes no network requests',not any(u.startswith(('http:','https:')) for u in requests))
    check('exported report has no script errors',not report_errors)
    report.close();close(page)
    # Mismatched inputs must not silently replace the pinned graph data.
    page.evaluate("get('evidence:example-1-recovery_seconds@1').meta.sha256='mismatch';showDetail('report:example-report@1')")
    check('report rejects evidence hash mismatch',page.locator('#drawer .mc-card').filter(has=page.locator('h3',has_text='Time to stable recovery')).locator('.mc-point').count()==0)
    close(page);route(page,'grafana')
    check('Grafana design lists every metric',page.locator('tbody tr').count()==32)
    with page.expect_download() as result:page.locator('[data-metrics-action="grafana"]').click()
    dash=json.loads(Path(result.value.path()).read_text())
    check('downloaded Grafana JSON has 33 graph panels',len([p for p in dash['panels'] if p['type']=='timeseries'])==33)
    page.locator('[data-metrics-action="example-view"]').click();page.wait_for_timeout(120)
    check('Grafana example resets incompatible workspace filters',page.locator('.mc-card').count()==32 and page.locator('.mc-card').filter(has=page.locator('.mc-point')).count()==32)
    page.locator('[data-metrics-field="query"]').fill('latency · p95')
    page.screenshot(path=str(OUT/'metrics-desktop.png'))
    page.set_viewport_size({'width':390,'height':844});page.wait_for_timeout(100)
    for name in ['metrics','grafana','overview','inventory']:
        route(page,name);check('mobile no document overflow '+name,page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'))
    route(page,'metrics');page.locator('.mc-card').first.scroll_into_view_if_needed();page.screenshot(path=str(OUT/'metrics-mobile.png'))
    check('preview has no JavaScript errors',not errors)
    page.close()
    # Real loopback service verifies token boundary and response CSP, not just a mock fetch.
    with tempfile.TemporaryDirectory() as tmp:
        token='metrics-browser-only-token-0123456789abcdef';app=create_app(Path(tmp)/'data',token=token)
        sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        server=uvicorn.Server(uvicorn.Config(app,log_level='error'))
        thread=threading.Thread(target=lambda:server.run(sockets=[sock]),daemon=True);thread.start()
        for _ in range(100):
            if server.started:break
            time.sleep(.02)
        live=browser.new_page(viewport={'width':1280,'height':900});live_errors=[];violations=[]
        live.on('pageerror',lambda e:live_errors.append(str(e)))
        live.on('console',lambda m:violations.append(m.text) if 'violates' in m.text and 'Content Security Policy' in m.text else None)
        base=f'http://127.0.0.1:{port}'
        response=urllib.request.urlopen(base,timeout=5);content=response.read().decode();csp=response.headers['Content-Security-Policy']
        # Meta CSP enforces the served script/style hashes in the DOM injection harness.
        meta='<meta http-equiv="Content-Security-Policy" content="'+html.escape(csp,quote=True)+'">'
        live.set_content(content.replace('<head>','<head>'+meta,1));live.wait_for_selector('h1',timeout=3000)
        def bridge(path,opts):
            url=base+'/'+path.lstrip('/')
            req=urllib.request.Request(url,data=opts.get('body','').encode() if opts.get('method','GET')!='GET' else None,headers=opts.get('headers',{}),method=opts.get('method','GET'))
            try:r=urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:r=e
            return {'status':r.status,'body':base64.b64encode(r.read()).decode(),'contentType':r.headers.get('content-type','')}
        live.expose_function('metricsHttpBridge',bridge)
        live.evaluate("()=>{window.fetch=async(path,opts={})=>{const r=await window.metricsHttpBridge(path,opts);return new Response(Uint8Array.from(atob(r.body),c=>c.charCodeAt(0)),{status:r.status,headers:{'Content-Type':r.contentType}});};}")
        route(live,'metrics')
        check('live metrics default to workspace not demo',live.locator('[data-metrics-field="source"]').input_value()=='workspace')
        check('locked service shows no samples',live.locator('.mc-point').count()==0)
        live.locator('#unlock-button').click();live.fill('#console-token',token);live.locator('#unlock-form button').click();wait_js(live,'state.unlocked')
        live.evaluate('openImport(APP_METRICS.examples)');live.locator('[data-action="review-import"]').click();wait_js(live,"!document.querySelector('#commit-import').disabled")
        live.locator('#commit-import').click();live.wait_for_timeout(180);route(live,'metrics')
        check('service imports and persists all metric records',len(app.state.store.all())==71)
        check('service graphs stored chart series',live.locator('path.mc-series').count()>0)
        check('service scalar evaluator unchanged',live.evaluate("get('evidence:example-metric-recovery_seconds@1').record.data.value===240"))
        check('served script hashes run under meta CSP',not violations and not live_errors)
        live.locator('#unlock-button').click()
        check('locking removes workspace graphs',live.locator('.mc-point').count()==0)
        live.close();server.should_exit=True;thread.join(timeout=3)
    browser.close()
(OUT/'metrics-browser-checks.json').write_text(json.dumps({'checks':results,'count':len(results),'boundary':'Browser navigation blocked: DOM injection, test SHA-256 bridge for about:blank, served script/style hashes enforced by meta CSP; UI fetch bridged to real loopback HTTP. Native browser navigation, fetch/CORS and CSP connect-src were not tested. Synthetic records only; no AWS, Docker/Podman/Kubernetes or Grafana server tested.'},indent=2))
print(f'{len(results)} metrics browser checks passed')
