"""Publication regressions; --native also exercises actual browser navigation and fetch."""
from __future__ import annotations
import argparse, json, os, shutil, socket, sys, tempfile, threading, time
from pathlib import Path
import uvicorn
from playwright.sync_api import sync_playwright
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.server import create_app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', action='store_true', help='Require real loopback and file navigation; never falls back to injection.')
    args = parser.parse_args()
    results = []
    def check(name, condition):
        assert condition, name
        results.append({'name': name, 'result': 'pass'})
        print('PASS', name, flush=True)
    def wait_state(expression):
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if page.evaluate('() => (' + expression + ')'):
                return
            time.sleep(.05)
        raise AssertionError('Browser state timed out: ' + expression)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=os.environ.get('CHROMIUM_PATH') or shutil.which('chromium'), headless=True, args=['--no-sandbox'])
        page = browser.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        html = (ROOT/'static/console.html').read_text()
        page.set_content(html.replace("const MODE = location.protocol === 'file:' ? 'preview' : 'service';", "const MODE = 'preview';"))
        page.wait_for_selector('h1')
        check('200000 samples render without an argument-stack overflow', page.evaluate('''() => {
            const spec={title:'Large graph',metric:'large',unit:'count',limits:[],traces:Array.from({length:10},(_,j)=>({label:'run'+j,source:'test',ref:'test',connected:true,points:Array.from({length:20000},(_,i)=>({t:1000000+i*1000,value:i%13}))}))};
            const html=MetricCharts.card(spec);const range=MetricCharts.extent(spec);MetricCharts.prune();
            return html.includes('Large graph')&&range[0]===1000000&&range[1]===20999000;
        }'''))
        check('snapshot graphs separate scope and simulation identity', page.evaluate('''() => {
            const a=clone(records('snapshot')[0]),b=clone(a),c=clone(a);b.record.data.scope_id='other-account';c.record.simulated=false;
            const specs=snapshotMetricSpecs([a,b,c]).filter(s=>s.metric==='resource_count');
            return specs.length===3&&specs.every(s=>s.traces[0].points.length===1)&&specs.filter(s=>s.synthetic).length===2;
        }'''))
        check('snapshot CSV retains each point reference', page.evaluate('''() => {
            const a=clone(records('snapshot')[0]),b=clone(a);b.meta.ref='snapshot:second@1';
            const spec=snapshotMetricSpecs([a,b]).find(s=>s.metric==='resource_count');
            const csv=MetricCharts.csv(spec);return csv.includes('"snapshot:second@1"')&&csv.includes('"'+a.meta.ref+'"');
        }'''))
        check('text CSV formulas escaped while negative numbers remain numeric', page.evaluate('''() => {
            const csv=MetricCharts.csv({unit:'=unsafe',traces:[{label:'@unsafe',source:'+unsafe',ref:'-unsafe',points:[{t:1000,value:-2}]}]});
            return csv.includes('"-2"')&&csv.includes('"\\\'=unsafe"')&&csv.includes('"\\\'@unsafe"');
        }'''))
        check('HTML report preserves imported origin and hash', page.evaluate('''async () => {
            const entry=get('report:example-report@1');const html=await metricReportDocument(entry.meta.ref);
            return html.includes('Report origin:')&&html.includes(entry.meta.sha256)&&html.includes('IMPORTED OR EXAMPLE RESULT');
        }'''))
        check('preview execution gate cannot hide a failed requirement', page.evaluate('''async () => {
            const entry=get('execution_run:example-run-1@1'),previous=entry.record.data.fault_confirmed;
            entry.record.data.fault_confirmed=false;
            try {const v=await evaluatePreview(entry.meta.ref);return v.data.outcome==='fail'&&v.data.gates.length>0;} finally {entry.record.data.fault_confirmed=previous;}
        }'''))
        check('every Grafana legend distinguishes all scope labels', page.evaluate('''() => APP_METRICS.dashboard.panels.filter(p=>p.type==='timeseries').every(p=>['environment','service','deployment_model','scenario','run_id','data_kind'].every(k=>p.targets[0].legendFormat.includes('{{'+k+'}}')))'''))
        check('publication regressions have no JavaScript errors', not errors)
        page.close()
        if args.native:
            with tempfile.TemporaryDirectory() as directory:
                token = 'publication-test-only-token-0123456789abcdef'
                app = create_app(Path(directory)/'data', token=token)
                sock = socket.socket(); sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
                server = uvicorn.Server(uvicorn.Config(app, log_level='error'))
                thread = threading.Thread(target=lambda: server.run(sockets=[sock]), daemon=True)
                thread.start()
                for _ in range(200):
                    if server.started: break
                    time.sleep(.025)
                try:
                    page = browser.new_page(viewport={'width': 1440, 'height': 1000})
                    errors, violations = [], []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.on('console', lambda msg: violations.append(msg.text) if 'Content Security Policy' in msg.text else None)
                    response = page.goto(f'http://127.0.0.1:{port}/', wait_until='networkidle')
                    check('native navigation receives script-hash CSP', response.status == 200 and 'sha256-' in response.headers.get('content-security-policy', ''))
                    page.wait_for_selector('h1')
                    check('native unauthenticated API call rejected', page.evaluate("async () => (await fetch('/api/workspace')).status") == 401)
                    page.locator('#unlock-button').click(); page.fill('#console-token', token)
                    page.locator('#unlock-form button[type="submit"]').click(); wait_state('state.unlocked===true')
                    check('native unlock fetches real backend catalogue', page.evaluate("records('scenario').length===37&&records('snapshot').length===0"))
                    page.evaluate('openImport(APP_METRICS.examples)')
                    page.locator('[data-action="review-import"]').click(); wait_state("!document.querySelector('#commit-import').disabled")
                    page.locator('#commit-import').click(); wait_state("get('scenario:EXAMPLE-METRICS@1')!==undefined")
                    page.evaluate("location.hash='metrics'"); wait_state("document.querySelectorAll('.mc-card').length===32")
                    check('native metrics use imported workspace evidence', page.locator('.mc-card').count() == 32 and page.locator('.mc-card').filter(has=page.locator('.mc-point')).count() == 32)
                    page.evaluate("showDetail('execution_run:example-metric-timeline@1')")
                    page.locator('#drawer [data-action="evaluate"]').click(); wait_state("records('validation_run').length===1")
                    check('native evaluator preserves measured scalar failure', page.evaluate("records('validation_run')[0].record.data.outcome==='fail'&&records('validation_run')[0].record.data.evaluator_version==='scalar-1.1'"))
                    page.locator('#drawer [data-action="report"]').click(); wait_state("records('report').length===1")
                    with page.expect_download() as download:
                        page.locator('#drawer [data-action="download-report"]').click()
                    output = Path(directory)/'report.html'; download.value.save_as(output)
                    report = browser.new_page(); report_errors, requests = [], []
                    report.on('pageerror', lambda error: report_errors.append(str(error)))
                    report.on('request', lambda request: requests.append(request.url))
                    report.goto(output.as_uri(), wait_until='load'); report.wait_for_selector('.mc-card')
                    check('native file report renders pinned graphs', report.locator('.mc-card').count() == 3)
                    report.locator('.mc-svg').first.focus(); report.keyboard.press('Home')
                    check('native file report keyboard interaction works', report.locator('.mc-tooltip:not([hidden])').count() == 1)
                    check('native file report makes no remote requests', not any(url.startswith(('http:', 'https:')) for url in requests))
                    check('native file report has no script errors', not report_errors)
                    report.close()
                    page.evaluate("document.querySelector('#drawer').close()")
                    page.locator('#unlock-button').click()
                    check('native locking clears token and records', page.evaluate('state.token===""&&state.entries.length===0&&!state.unlocked'))
                    check('native service has no CSP or script errors', not errors and not violations)
                    page.close()
                finally:
                    server.should_exit = True; thread.join(timeout=10)
        browser.close()
    output = ROOT/'validation/publication-browser.json'; output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps({'passed': len(results), 'native_navigation': args.native, 'results': results}, indent=2)+'\n')
    print(f'{len(results)} publication browser checks passed; native={args.native}')

if __name__ == '__main__':
    main()
