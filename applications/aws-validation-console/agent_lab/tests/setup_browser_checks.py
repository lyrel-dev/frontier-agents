#!/usr/bin/env python3
"""Exercise guided forms through the actual HTTP backend. AWS is test-only.

--native requires browser navigation; --bridge does not establish CSP acceptance.
No fixture is placed in the distributed workspace or preview.
"""
import argparse,json,os,socket,sys,tempfile,threading,time,urllib.request,urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from playwright.sync_api import sync_playwright
import uvicorn
from lab.api import create_app
from lab.models import Configuration
from lab.store import Store
from lab.setup import Setup
from lab.native_fis import account_contract
from lab.aws import template_contract
from lab.fis_campaigns import Fleet
from lab.util import digest,iso
from test_fis_fleet import template
from conftest import ACCOUNT_A,ACCOUNT_B,TARGET
ROOT=Path(__file__).resolve().parents[1]
OP='test-only-onboarding-operator-credential';AP='test-only-onboarding-approval-credential'
class Session:
    available_profiles=['test-agent','test-workload','test-executor']
    def __init__(self,profile=None):self.profile=profile
    def client(self,service,**kwargs):return self
    def get_caller_identity(self):
        a=ACCOUNT_A if self.profile=='test-agent' else ACCOUNT_B
        return {'Account':a,'Arn':f'arn:aws:iam::{a}:role/test-observer','ResponseMetadata':{'RequestId':'fixture-only'}}
    def list_agent_spaces(self,**kwargs):return {'agentSpaces':[{'agentSpaceId':'space-fixture','name':'Test-only Agent Space'}]}
    def list_associations(self,**kwargs):return {'associations':[{'associationId':'assoc-fixture','status':'valid','configuration':{'sourceAws':{'accountId':ACCOUNT_B,'accountType':'SECONDARY'}}}]}
    def list_experiment_templates(self,**kwargs):return {'experimentTemplates':[]}
    def describe_instances(self,**kwargs):return {'Reservations':[{'Instances':[{'InstanceId':'i-123','State':{'Name':'running'}}]}]}
class TestSetup(Setup):
    def __init__(self,c,s):super().__init__(c,s,session_factory=lambda profile=None:Session(profile))

def main():
    p=argparse.ArgumentParser();p.add_argument('--native',action='store_true');p.add_argument('--bridge',action='store_true');a=p.parse_args()
    if a.native==a.bridge:p.error('Choose exactly one browser mode')
    checks=[];out=ROOT/'validation';out.mkdir(exist_ok=True)
    def check(label,value):
        assert value,label
        checks.append(label);print('PASS',label,flush=True)
    with tempfile.TemporaryDirectory() as d,patch('lab.setup_api.Setup',TestSetup):
        cfg=Configuration();store=Store(d);app=create_app(cfg,store,OP,AP)
        sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
        server=uvicorn.Server(uvicorn.Config(app,host='127.0.0.1',port=port,log_level='error',access_log=False))
        thread=threading.Thread(target=server.run,daemon=True);thread.start()
        for _ in range(100):
            if server.started:break
            time.sleep(.02)
        base=f'http://127.0.0.1:{port}'
        try:
            with sync_playwright() as pw:
                browser=pw.chromium.launch(headless=True,executable_path=os.getenv('CHROMIUM_PATH','/usr/bin/chromium'),args=['--no-sandbox'])
                page=browser.new_page(viewport={'width':1440,'height':1000});page.set_default_timeout(8000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                if a.native:page.goto(base+'/setup',wait_until='networkidle')
                else:
                    def bridge(source,path,options):
                        assert path.startswith('/api/') and not path.startswith('//')
                        req=urllib.request.Request(base+path,data=options.get('body','').encode() if 'body' in options else None,headers=options.get('headers',{}),method=options.get('method','GET'))
                        try:
                            with urllib.request.urlopen(req) as r:return {'status':r.status,'body':r.read().decode(),'headers':dict(r.headers)}
                        except urllib.error.HTTPError as e:return {'status':e.code,'body':e.read().decode(),'headers':dict(e.headers)}
                    page.expose_binding('__testHTTPBridge',bridge)
                    html=(ROOT/'static/setup.html').read_text()
                    for name in ('style','aws','setup'):html=html.replace(f'<link rel="stylesheet" href="/static/{name}.css">','<style>'+(ROOT/f'static/{name}.css').read_text()+'</style>')
                    html=html.replace('<script defer src="/static/setup.js"></script>','');page.set_content(html)
                    page.evaluate("()=>{window.fetch=async(path,options={})=>{const r=await window.__testHTTPBridge(path,options);return new Response(r.body,{status:r.status,headers:r.headers})}}")
                    page.add_script_tag(content=(ROOT/'static/setup.js').read_text())
                check('empty guided setup does not invent accounts or measurements',not store.entities() and not store.records())
                page.screenshot(path=str(out/'setup-empty-desktop.png'),full_page=True)
                page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(out/'setup-empty-mobile.png'),full_page=True)
                check('empty mobile layout has no overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                page.set_viewport_size({'width':1440,'height':1000})
                page.get_by_role('button',name='Unlock',exact=True).click();page.get_by_label('Local operator token',exact=True).fill(OP);page.locator('#setup-modal').get_by_role('button',name='Unlock',exact=True).click()
                page.wait_for_function('GuidedSetup.state().current!==null')
                page.screenshot(path=str(out/'setup-accounts-empty-desktop.png'),full_page=True)
                check('SDK names are selected without credential fields',page.get_by_label('Observer profile',exact=True).count()==1 and page.get_by_label('AWS access key',exact=True).count()==0)
                def approve_dialog():
                    text=page.locator('#setup-body pre').inner_text();subject=json.loads(text)
                    page.get_by_label('Approver name',exact=True).fill('Fixture reviewer')
                    page.get_by_label('Approval rationale',exact=True).fill('Test-only exact proposal approval.')
                    page.get_by_label('Exact confirmation',exact=True).fill(subject['confirmation'])
                    page.get_by_label('Separate local approval token',exact=True).fill(AP)
                    page.get_by_role('button',name='Approve exact operation',exact=True).click()
                    page.wait_for_function('!document.querySelector("#setup-modal").open')
                for cid,account,profile in [('work',ACCOUNT_B,'test-workload'),('agent',ACCOUNT_A,'test-agent')]:
                    page.locator('[data-stage=accounts]').click();page.get_by_label('Connection ID',exact=True).fill(cid)
                    page.get_by_label('Connection label',exact=True).fill('Test-only '+cid)
                    page.get_by_label('Expected 12-digit AWS account',exact=True).fill(account)
                    page.get_by_label('Regions, comma separated',exact=True).fill('eu-central-1')
                    page.get_by_label('Observer profile',exact=True).select_option(profile)
                    if cid=='work':page.get_by_label('FIS executor profile (optional)',exact=True).select_option('test-executor')
                    page.get_by_role('button',name='Review account configuration',exact=True).click()
                    page.get_by_role('button',name='Approve exact local configuration',exact=True).wait_for()
                    check(cid+' remains a proposal before approval',not any(c.id==cid for c in cfg.fis_accounts))
                    page.get_by_role('button',name='Approve exact local configuration',exact=True).click();approve_dialog()
                    check(cid+' activated in the backend without file editing',any(c.id==cid for c in cfg.fis_accounts))
                check('account activation makes no provider operations',not store.operations())
                page.locator('[data-stage=accounts]').click();page.get_by_role('button',name='Test reads · eu-central-1',exact=True).first.click()
                page.get_by_role('heading',name='Connection read checks').wait_for()
                check('connection verification reports read scope not mutation approval','mutation_permission_verified' in page.locator('#setup-body').inner_text())
                page.locator('#setup-close').click();page.locator('[data-stage=agents]').click()
                page.get_by_label('Agent connection',exact=True).select_option('agent');page.get_by_label('Agent Region',exact=True).fill('eu-central-1')
                page.get_by_role('button',name='Discover Agent Spaces',exact=True).click();page.get_by_role('heading',name='Observed Agent Spaces').wait_for()
                check('agent choices preserve exact secondary account association','assoc-fixture' in page.locator('#setup-body').inner_text())
                page.locator('#setup-close').click()
                # AWS snapshots are test-only backend fixtures, not imported product data.
                job=store.create('fis_sync','COMPLETE',{'scope_ids':[],'requested_at':iso()})
                scope=store.create('fis_scope','COMPLETE',{'account_id':ACCOUNT_B,'region':'eu-central-1','discovery_id':job['id'],'connection_id':'work','phase':'complete','templates':0,'history':0})
                store.update(job['id'],changes={'scope_ids':[scope['id']]})
                t=template();rec=store.put_record('fis_template',scope['id'],{'scope_id':scope['id'],'account_id':ACCOUNT_B,'region':'eu-central-1','template_id':t['id'],'template':t,'contract_sha256':digest(template_contract(t)),'target_accounts':[],'complete':True})
                preview=store.put_record('fis_preview_result','fixture-preview',{'template_record_id':rec['id'],'template_id':t['id'],'template_sha256':digest(template_contract(t)),'target_accounts':[],'target_accounts_sha256':digest([]),'account_id':ACCOUNT_B,'region':'eu-central-1','targets':[{'targetName':'Instances','resourceType':'aws:ec2:instance','targetInformation':{'arn':TARGET}}],'captured_at':iso(),'provider_id':'fixture-skip-only'})
                store.create('fis_preview','COMPLETE',{'provider_id':'fixture-skip-only','result_id':preview['id']})
                page.locator('[data-stage=plan]').click();page.get_by_label('Plan / binding ID',exact=True).wait_for()
                fields={'Plan / binding ID':'guided-trial','Plan title':'Test-only guided plan','Service ID':'test-service','Agent Region':'eu-central-1','Business-path HTTPS URL':'https://example.com/business','Allowed destination CIDRs, comma separated':'192.0.2.0/24','Maximum accepted latency (ms)':'1000','Maximum accepted error ratio':'0.01','Incident CloudWatch alarm name':'TestAlarm','Native external-reference system':'fixture-native','Reference ID format':'{alarm_arn}','Delivery receipt log group':'/fixture/receipts','Explain the actual source-to-task correlation':'Test-only exact alarm ARN is used as the integration reference.','Maximum fault runtime seconds':'60','Ground-truth mechanism code':'capacity-loss','Actual expected failure mechanism':'The approved serving instance becomes unavailable during the test.','Diagnosis rubric':'Identify the actual stopped resource and its impact with source citations.','Test hypothesis':'Native investigation responds to the controlled serving capacity interruption.','Action prerequisites and permission review':'Test-only reviewed target role permissions and action prerequisites.','Recovery that remains operable without this console':'Test-only independent restoration is reviewed before any authorized exposure.','Blast-radius and stop-alarm review':'Test-only exact instance and independent CloudWatch stop condition.'}
                for label,value in fields.items():page.get_by_label(label,exact=True).fill(value)
                page.get_by_label('Agent account connection',exact=True).select_option('agent');page.get_by_role('button',name='Load agent choices',exact=True).click()
                page.get_by_label('Agent Space',exact=True).select_option('space-fixture')
                page.get_by_label('Monitored workload connection',exact=True).select_option('work')
                check('workload association is selected from read agent data',page.get_by_label('Workload association ID',exact=True).input_value()=='assoc-fixture')
                for phase in ('baseline','fault','cleanup'):
                    page.get_by_role('button',name='Add independent check',exact=True).click()
                    box=page.locator('.setup-row').filter(has=page.get_by_label('Check ID',exact=True)).last
                    box.get_by_label('Check ID',exact=True).fill(phase+'-resource');box.get_by_label('Phase',exact=True).select_option(phase)
                    box.get_by_label('Verifier account connection',exact=True).select_option('work');box.get_by_label('AWS read service',exact=True).select_option('ec2')
                    box.get_by_label('Read operation',exact=True).select_option('describe_instances');box.get_by_role('button',name='Build resource parameter fields',exact=True).click()
                    box.get_by_label('Add Parameters field',exact=True).wait_for();box.get_by_label('Add Parameters field',exact=True).select_option('InstanceIds');box.get_by_role('button',name='Add selected field',exact=True).click()
                    box.get_by_role('button',name='Add InstanceIds item',exact=True).click();box.get_by_label('InstanceIds item',exact=True).fill('i-123')
                    box.get_by_label('JMESPath response field',exact=True).fill('Reservations[0].Instances[0].State.Name')
                    box.get_by_label('Expected value',exact=True).fill('stopped' if phase=='fault' else 'running')
                    box.get_by_label('Why this independently verifies the phase',exact=True).fill('Read the independently observed resource state for '+phase+'.')
                check('SDK fields create typed resource selectors without JSON editing',page.get_by_label('InstanceIds item',exact=True).count()==3)
                page.get_by_role('button',name='Add measured business metric',exact=True).click()
                page.get_by_label('Metric ID',exact=True).fill('lost-writes');page.get_by_label('Metric title',exact=True).fill('Independently reconciled writes');page.get_by_label('Metric account connection',exact=True).select_option('work')
                page.get_by_label('CloudWatch namespace',exact=True).fill('Test/Application');page.get_by_label('CloudWatch metric name',exact=True).fill('LostAcknowledgedWrites');page.get_by_label('CloudWatch unit',exact=True).fill('Count');page.get_by_label('Accepted value',exact=True).fill('0')
                page.get_by_label('Measurement population, denominator and interpretation',exact=True).fill('Independent reconciliation of all acknowledged operation IDs in each measured window.')
                page.get_by_role('button',name='Validate and review the complete plan',exact=True).click()
                for _ in range(100):
                    if page.get_by_role('button',name='Approve exact local configuration',exact=True).count():break
                    time.sleep(.03)
                check('guided submission validates all fields',page.get_by_role('button',name='Approve exact local configuration',exact=True).count()==1 or print(page.locator('#setup-status').inner_text()))
                draft=page.evaluate('GuidedSetup.state().draft')
                check('guided plan uses actual AWS definition fingerprint',draft['data']['configuration']['bindings'][0]['faults'][0]['template_sha256']==digest(template_contract(t)))
                check('guided plan pins business correctness separately',draft['data']['experiment']['business_requirements'][0]['category']=='data_correctness')
                page.get_by_role('button',name='Approve exact local configuration',exact=True).click();approve_dialog()
                check('plan activation atomically registers the executable contract',store.record('experiment:guided-trial@1')['kind']=='experiment' and len(cfg.bindings)==1)
                check('preparing a plan cannot dispatch a fault',not store.operations() and not store.entities('trial'))
                check('native prepared contract appears in AWS library',len(Fleet(cfg,store).library()['templates'][0]['contracts'])==1)
                page.set_viewport_size({'width':390,'height':844})
                for stage in ('accounts','agents','targets','plan','review'):
                    page.locator('[data-stage='+stage+']').click();page.wait_for_function('(s)=>GuidedSetup.state().stage===s',arg=stage)
                    check('mobile '+stage+' does not overflow',page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'))
                check('no token persisted in browser storage',page.evaluate('(()=>{try{return localStorage.length===0&&sessionStorage.length===0}catch{return true}})()'))
                page.locator('#setup-auth').click();check('locking clears configuration and draft',page.evaluate("GuidedSetup.state().current===null && GuidedSetup.state().draft===null && GuidedSetup.state().token===''") )
                check('no JavaScript exceptions',not errors)
                browser.close()
        finally:server.should_exit=True;thread.join(10)
    report={'passed':len(checks),'checks':checks,'native_navigation':a.native,'browser_bridge':a.bridge,'provider_access':'test-only SDK responses and preview records; no AWS','limits':['Fixture-backed guided form and HTTP contract acceptance, not IAM efficacy or real FIS/agent acceptance.']+([] if a.native else ['Native navigation and CSP enforcement not established in bridge mode.'])}
    (out/'setup-browser.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
