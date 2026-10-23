#!/usr/bin/env python3
"""Check deep SDK forms against the real HTTP API; no AWS account is accessed."""
import argparse
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import uvicorn
from playwright.sync_api import sync_playwright
from lab.api import create_app
from lab.aws import template_contract
from lab.models import Configuration
from lab.store import Store
from lab.util import digest, iso
from setup_browser_checks import TestSetup as FixtureSetup, OP, AP, wait_state
from test_fis_fleet import template
from conftest import ACCOUNT_B, TARGET
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--native', action='store_true')
    parser.add_argument('--bridge', action='store_true')
    mode = parser.parse_args()
    if mode.native == mode.bridge:
        parser.error('Choose one explicit browser mode')
    checks = []
    def check(name, condition):
        assert condition, name
        checks.append(name)
        print('PASS', name, flush=True)
    with tempfile.TemporaryDirectory() as directory, patch('lab.setup_api.Setup', FixtureSetup):
        cfg = Configuration(fis_accounts=[{'id':'work','name':'Test-only workload','account_id':ACCOUNT_B,
                             'profile':'test-workload','regions':['eu-central-1']}])
        store = Store(directory)
        # Test-only discovery and preview records; no scenario, trial or measurement is seeded.
        job = store.create('fis_sync','COMPLETE',{'scope_ids':[],'requested_at':iso()})
        scope = store.create('fis_scope','COMPLETE',{'account_id':ACCOUNT_B,'region':'eu-central-1',
                    'discovery_id':job['id'],'connection_id':'work','phase':'complete','templates':0,'history':0})
        store.update(job['id'], changes={'scope_ids':[scope['id']]})
        t = template()
        record = store.put_record('fis_template',scope['id'],{'scope_id':scope['id'],'account_id':ACCOUNT_B,
                    'region':'eu-central-1','template_id':t['id'],'template':t,
                    'contract_sha256':digest(template_contract(t)),'target_accounts':[],'complete':True})
        preview = store.put_record('fis_preview_result','test-only-preview',{'template_record_id':record['id'],
                    'template_id':t['id'],'template_sha256':digest(template_contract(t)),
                    'target_accounts':[],'target_accounts_sha256':digest([]),'account_id':ACCOUNT_B,
                    'region':'eu-central-1','targets':[{'targetName':'Instances','resourceType':'aws:ec2:instance',
                    'targetInformation':{'arn':TARGET}}],'captured_at':iso(),'provider_id':'test-only-skip-all'})
        store.create('fis_preview','COMPLETE',{'provider_id':'test-only-skip-all','result_id':preview['id']})
        app = create_app(cfg, store, OP, AP)
        sock = socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
        server = uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=port,log_level='error',access_log=False))
        thread = threading.Thread(target=server.run,daemon=True);thread.start()
        for _ in range(100):
            if server.started:break
            time.sleep(.02)
        base = f'http://127.0.0.1:{port}'
        try:
            with sync_playwright() as pw:
                browser = pw.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
                page = browser.new_page(viewport={'width':1440,'height':1000});page.set_default_timeout(10000)
                errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
                if mode.native:
                    page.goto(base+'/setup',wait_until='networkidle')
                else:
                    def bridge(source,path,options):
                        assert path.startswith('/api/') and not path.startswith('//')
                        request=urllib.request.Request(base+path,data=options.get('body','').encode() if 'body' in options else None,
                                                       headers=options.get('headers',{}),method=options.get('method','GET'))
                        try:
                            with urllib.request.urlopen(request) as response:
                                return {'status':response.status,'body':response.read().decode(),'headers':dict(response.headers)}
                        except urllib.error.HTTPError as error:
                            return {'status':error.code,'body':error.read().decode(),'headers':dict(error.headers)}
                    page.expose_binding('__testHTTPBridge',bridge)
                    html=(ROOT/'static/setup.html').read_text()
                    for name in ('style','aws','setup'):
                        html=html.replace(f'<link rel="stylesheet" href="/static/{name}.css">','<style>'+(ROOT/f'static/{name}.css').read_text()+'</style>')
                    html=html.replace('<script defer src="/static/setup.js"></script>','');page.set_content(html)
                    page.evaluate("()=>{window.fetch=async(path,options={})=>{const r=await window.__testHTTPBridge(path,options);return new Response(r.body,{status:r.status,headers:r.headers})}}")
                    page.add_script_tag(content=(ROOT/'static/setup.js').read_text())
                page.get_by_role('button',name='Unlock',exact=True).click()
                page.get_by_label('Local operator token',exact=True).fill(OP)
                page.locator('#setup-modal').get_by_role('button',name='Unlock',exact=True).click()
                wait_state(page,'GuidedSetup.state().current!==null')
                page.locator('[data-stage=plan]').click()
                page.get_by_role('button',name='Add independent check',exact=True).click()
                row=page.locator('.setup-row').filter(has=page.get_by_label('Check ID',exact=True)).last
                row.get_by_label('AWS read service',exact=True).select_option('cloudwatch')
                row.get_by_label('Read operation',exact=True).select_option('get_metric_data')
                row.get_by_role('button',name='Build resource parameter fields',exact=True).click()
                row.get_by_role('button',name='Add MetricDataQueries item',exact=True).click()
                query=row.get_by_label('Add MetricDataQueries item field',exact=True)
                query.select_option('MetricStat')
                query.locator('..').locator('..').get_by_role('button',name='Add selected field',exact=True).first.click()
                metric=row.get_by_label('Add Metric field',exact=True)
                metric.select_option('Dimensions')
                metric.locator('..').locator('..').get_by_role('button',name='Add selected field',exact=True).first.click()
                row.get_by_role('button',name='Add Dimensions item',exact=True).click()
                row.get_by_label('Name',exact=True).fill('InstanceId')
                row.get_by_label('Value',exact=True).fill('i-123')
                check('nested CloudWatch dimensions retain typed Name and Value controls',
                      row.get_by_label('Name',exact=True).input_value()=='InstanceId' and
                      row.get_by_label('Value',exact=True).input_value()=='i-123')
                row.get_by_label('Read operation',exact=True).select_option('describe_alarms')
                check('switching operations discards the prior nested parameter tree',
                      row.get_by_label('Name',exact=True).count()==0)
                check('SDK form construction performs no provider operation and creates no trial',
                      not store.operations() and not store.entities('trial'))
                check('deep parameter editing raises no JavaScript errors',not errors)
                browser.close()
        finally:
            server.should_exit=True;thread.join(10)
    report={'passed':len(checks),'checks':checks,'native_navigation':mode.native,'browser_bridge':mode.bridge,
            'provider_access':'installed SDK models and test-only discovery/preview records; no AWS',
            'limits':[] if mode.native else ['DOM injection with real local HTTP bridge; native CSP/navigation unverified.']}
    (ROOT/'validation').mkdir(exist_ok=True)
    (ROOT/'validation/sdk-form-browser.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
