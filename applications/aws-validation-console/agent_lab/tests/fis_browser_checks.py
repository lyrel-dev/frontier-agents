#!/usr/bin/env python3
"""AWS/FIS UI acceptance. Provider fixtures are confined to this harness.
--native navigates real HTTP; --bridge explicitly does not verify browser CSP.
"""
import argparse
import contextlib
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

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT/'tests')]
import uvicorn
from playwright.sync_api import sync_playwright
from lab.api import create_app
from lab.models import Configuration
from lab.store import Store
from lab.service import Service
from lab.fis_catalog import Catalog
from lab.fis_campaigns import Fleet
from conftest import config_dict, spec as fixture_spec
from test_fis_fleet import Reader, configuration

OP='fis-browser-test-only-operator-credential'
AP='fis-browser-test-only-approval-credential'

@contextlib.contextmanager
def serve(config, store):
    sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
    app=create_app(config,store,OP,AP)
    server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=port,log_level='error',access_log=False))
    thread=threading.Thread(target=server.run,daemon=True);thread.start()
    for _ in range(200):
        if server.started:break
        time.sleep(.02)
    if not server.started:raise RuntimeError('Local API did not start')
    try:yield f'http://127.0.0.1:{port}'
    finally:server.should_exit=True;thread.join(10)


def main():
    parser=argparse.ArgumentParser();modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--native',action='store_true');modes.add_argument('--bridge',action='store_true');args=parser.parse_args()
    checks=[];errors=[];output=ROOT/'validation';output.mkdir(exist_ok=True)
    def check(label,value):
        assert value,label
        checks.append(label);print('PASS',label,flush=True)
    def load(browser,base):
        page=browser.new_page(viewport={'width':1440,'height':1000});page.on('pageerror',lambda e:errors.append(str(e)))
        if args.native:page.goto(base,wait_until='networkidle')
        else:
            def bridge(source,path,options):
                assert path.startswith('/api/') and not path.startswith('//')
                req=urllib.request.Request(base+path,data=options.get('body','').encode() if 'body' in options else None,
                    headers=options.get('headers',{}),method=options.get('method','GET'))
                try:
                    with urllib.request.urlopen(req) as r:return {'status':r.status,'body':r.read().decode(),'headers':dict(r.headers)}
                except urllib.error.HTTPError as e:return {'status':e.code,'body':e.read().decode(),'headers':dict(e.headers)}
            page.expose_binding('__fisTestHTTP',bridge)
            html=(ROOT/'static/aws.html').read_text()
            for name in ['style.css','aws.css']:
                html=html.replace(f'<link rel="stylesheet" href="/static/{name}">','<style>'+(ROOT/'static'/name).read_text()+'</style>')
            for name in ['charts.js','aws.js']:html=html.replace(f'<script defer src="/static/{name}"></script>','')
            page.set_content(html)
            page.evaluate('()=>{window.fetch=async(p,o={})=>{const r=await window.__fisTestHTTP(p,o);return new Response(r.body,{status:r.status,headers:r.headers})}}')
            for name in ['charts.js','aws.js']:page.add_script_tag(content=(ROOT/'static'/name).read_text())
        return page
    def wait(page,expression):
        deadline=time.monotonic()+10
        while time.monotonic()<deadline:
            if page.evaluate(expression):return
            time.sleep(.05)
        raise AssertionError('UI state did not arrive: '+expression)
    def unlock(page):
        page.locator('#aws-unlock').click();page.get_by_label('Local operator token').fill(OP)
        page.locator('#aws-modal').get_by_role('button',name='Unlock',exact=True).click()
        wait(page,'Boolean(fleetState.token && fleetState.catalog && fleetState.queues)')
    with sync_playwright() as pw:
        browser=pw.chromium.launch(executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),headless=True,args=['--no-sandbox'])
        with tempfile.TemporaryDirectory() as tmp:
            store=Store(tmp)
            with serve(Configuration(),store) as base:
                page=load(browser,base)
                check('AWS FIS is the default application',page.title()=='AWS FIS · Agent benchmarks')
                check('empty catalogue has no seeded templates','No FIS catalogue loaded' in page.locator('body').inner_text())
                check('discovery disabled until accounts are configured',page.get_by_role('button',name='Discover all configured accounts').is_disabled())
                unlock(page)
                check('empty AWS workspace uses the authenticated backend',page.evaluate('fleetState.accounts.accounts.length===0'))
                check('unlock does not create trials or AWS operations',not store.entities() and not store.operations())
                for view in ['accounts','catalog','campaigns','benchmarks']:
                    page.locator('[data-view="'+view+'"]').click()
                    check('AWS navigation '+view,page.evaluate('fleetState.view')==view)
                page.locator('[data-view="catalog"]').click();page.screenshot(path=str(output/'fis-empty-desktop.png'),full_page=True)
                page.set_viewport_size({'width':390,'height':844})
                for view in ['accounts','catalog','campaigns','benchmarks']:
                    page.locator('[data-view="'+view+'"]').click()
                    check('empty mobile layout '+view,page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                page.locator('[data-view="catalog"]').click();page.screenshot(path=str(output/'fis-empty-mobile.png'),full_page=True)
                check('operator token never enters persistent browser storage',page.evaluate('(()=>{try{return !localStorage.length&&!sessionStorage.length}catch{return true}})()'))
                page.locator('#aws-unlock').click()
                check('locking clears catalogue, reports and credentials',page.evaluate('!fleetState.token && !fleetState.catalog && !fleetState.benchmark'))
                page.close()
        # This second workspace exists only during this test. No real SDK profile is accessed.
        with tempfile.TemporaryDirectory() as tmp:
            cfg=configuration(Configuration.model_validate(config_dict.__wrapped__()))
            store=Store(tmp);service=Service(cfg,store);spec=fixture_spec.__wrapped__(cfg);service.register(spec)
            reader=Reader(page_count=2);catalog=Catalog(cfg,store,session_factory=reader.factory);catalog.request()
            for _ in range(40):catalog.step()
            with serve(cfg,store) as base:
                page=load(browser,base);unlock(page)
                check('catalogue shows both paginated fixture templates',page.get_by_role('button',name='Inspect AWS definition',exact=True).count()==2)
                check('history is not presented as measured response','Historical FIS executions (2)' in page.locator('body').inner_text())
                page.get_by_label('Filter FIS templates').fill('EXT1')
                check('search filters actual template records',page.get_by_role('button',name='Inspect AWS definition',exact=True).count()==1)
                page.get_by_label('Filter FIS templates').fill('')
                page.get_by_role('button',name='Inspect AWS definition',exact=True).first.click()
                check('template inspection retains AWS action definitions','aws:ec2:stop-instances' in page.locator('#aws-modal-body').inner_text())
                page.locator('#aws-close').click()
                page.get_by_role('checkbox').first.check();page.get_by_role('button',name='Create campaign',exact=True).click()
                page.get_by_label('Campaign name').fill('Browser test only')
                page.get_by_label('Agent history, fixed order and carryover limitations').fill('Test-only fixed-order exposure. Agent history is not reset; no AWS call will occur in this browser test.')
                page.get_by_role('button',name='Register campaign',exact=True).click()
                wait(page,"fleetState.view==='campaigns' && fleetState.queues.campaigns.length===1")
                q=store.entities('fis_campaign')[0]
                check('UI registers a pinned actual campaign plan',q['state']=='PLANNED' and q['data']['total']==1)
                check('registration alone never dispatches a fault',not store.operations())
                page.get_by_role('button',name='Open queue',exact=True).click()
                page.get_by_role('button',name='Activate queue',exact=True).click()
                wait(page,"document.querySelector('#aws-modal-body').innerText.includes('Pause future dispatch')")
                check('activate invokes the durable queue API',store.entity(q['id'])['state']=='RUNNING')
                page.get_by_role('button',name='Pause future dispatch',exact=True).click()
                wait(page,"document.querySelector('#aws-modal-body').innerText.includes('Resume queue')")
                check('pause invokes the queue guard without starting a child',store.entity(q['id'])['state']=='PAUSED' and not store.entities('trial'))
                page.get_by_role('button',name='Freeze benchmark report',exact=True).click()
                wait(page,"fleetState.view==='benchmarks' && Boolean(fleetState.benchmark)")
                check('unstarted exposure remains in report','NOT STARTED' in page.locator('body').inner_text())
                check('missing measured latency does not become zero','not measured' in page.locator('body').inner_text())
                check('every unmeasured metric has an explicit empty plot',page.locator('#aws-view .chart-empty').count()==11)
                check('empty benchmark preserves null statistics',page.evaluate('fleetState.benchmark.data.groups.every(g=>Object.values(g.statistics).every(s=>s.n===0&&s.median===null))'))
                with page.expect_download() as dl:page.get_by_role('button',name='Export all attempts CSV').click()
                csv=Path(dl.value.path()).read_text()
                check('CSV includes unstarted attempts rather than successes only','NOT_STARTED' in csv)
                page.set_viewport_size({'width':390,'height':844})
                check('populated benchmark has no horizontal page overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                check('browser retains no approval credential',page.evaluate('!JSON.stringify(fleetState).includes("'+AP+'")'))
                check('test never issued a provider write',not store.operations())
                page.close()
        check('no JavaScript errors',not errors);browser.close()
    report={'passed':len(checks),'checks':checks,'native_navigation':args.native,'browser_bridge':args.bridge,
        'aws_access':False,'fixtures':'Second workspace uses test-only paginated discovery responses; no fixtures enter product assets.',
        'limitations':[] if args.native else ['DOM injection and real HTTP bridge; native CSP, navigation and fetch not verified by this run.']}
    (output/'fis-browser-review.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
