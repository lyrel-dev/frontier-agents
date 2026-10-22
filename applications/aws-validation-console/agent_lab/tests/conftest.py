"""Test-only fixtures. They are never loaded by the application or a delivered preview."""
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pytest
from lab.models import Configuration, Experiment, TrialRequest, Approval
from lab.store import Store
from lab.service import Service
from lab.engine import Engine
from lab.util import digest,iso,dt
from lab.aws import template_contract

ACCOUNT_A='111111111111'; ACCOUNT_B='222222222222'
TARGET=f'arn:aws:ec2:eu-central-1:{ACCOUNT_B}:instance/i-0123456789abcdef0'
ALARM=f'arn:aws:cloudwatch:eu-central-1:{ACCOUNT_B}:alarm:validation-safety'
DOC=f'arn:aws:ssm:eu-central-1:{ACCOUNT_B}:document/ReviewedCapacityChange'

@pytest.fixture
def config_dict():
    template={'id':'EXTtest','roleArn':f'arn:aws:iam::{ACCOUNT_B}:role/FISExecution',
       'targets':{'Instances':{'resourceType':'aws:ec2:instance','resourceArns':[TARGET],'selectionMode':'ALL'}},
       'actions':{'Stop':{'actionId':'aws:ec2:stop-instances','parameters':{'startInstancesAfterDuration':'PT1M'},'targets':{'Instances':'Instances'}}},
       'stopConditions':[{'source':'aws:cloudwatch:alarm','value':ALARM}],
       'experimentOptions':{'accountTargeting':'single-account','emptyTargetResolutionMode':'fail'}}
    return {'enable_aws_writes':True,'bindings':[{
      'id':'test-binding','name':'SDK fixture only','agent':{'account_id':ACCOUNT_A,'region':'eu-central-1','profile':'agent'},
      'workload':{'account_id':ACCOUNT_B,'region':'eu-central-1','profile':'workload'},
      'agent_space_id':'space-test','association_id':'association-test','service_id':'test-service',
      'deployment_model':'ec2','environment':'nonproduction','fault_profile':'fault','change_profile':'change','requester_profile':'requester',
      'route':{'alarm_name':'test-incident','reference_system':'monitoring','reference_id_format':'{alarm_arn}',
               'receipt_log_group':'/test/receipts','route_contract':'The test fixture joins an exact alarm ARN reference, not a time-only candidate.'},
      'probes':[{'id':'get-health','title':'Test-only loopback probe','url':'http://127.0.0.1:9876/health',
                 'allowed_networks':['127.0.0.0/8'],'allow_loopback_http':True,'requests_per_second':1}],
      'checks':[
       {'id':'healthy','service':'ec2','operation':'describe_instances','parameters':{'InstanceIds':['i-0123456789abcdef0']},
        'expression':'Reservations[0].Instances[0].State.Name','expected':'running','purpose':'Verify the exact instance is running before and after the test.'},
       {'id':'fault-present','service':'ec2','operation':'describe_instances','parameters':{'InstanceIds':['i-0123456789abcdef0']},
        'expression':'Reservations[0].Instances[0].State.Name','expected':'stopped','purpose':'Independently verify the actual instance stop during the fault.'},
       {'id':'changed','service':'ssm','operation':'get_parameter','parameters':{'Name':'/test/change-marker','WithDecryption':False},
        'expression':'Parameter.Value','expected':'applied','purpose':'Test fixture for a verified implemented state; not a deployed runbook.'}],
      'faults':[{'id':'bounded-stop','title':'Bounded test instrument','template_id':'EXTtest','template_sha256':digest(template_contract(template)),
                 'target_arns':[TARGET],'allowed_action_ids':['aws:ec2:stop-instances'],'max_fault_seconds':60,
                 'baseline_checks':['healthy'],'fault_checks':['fault-present'],'cleanup_checks':['healthy'],
                 'safety_alarm_arns':[ALARM],'safety_review':'Test fixture: automatic start duration and independent cleanup read check.'}],
      'runbooks':[{'id':'capacity-change','title':'Test-only approved change','document_arn':DOC,'document_version':'1','content_sha256':'a'*64,
                   'parameters':{'AutomationAssumeRole':[f'arn:aws:iam::{ACCOUNT_B}:role/AutomationExecution']},
                   'timeout_seconds':60,'before_checks':['healthy'],'after_checks':['changed'],
                   'implementation_artifact':'test-only-reference','implementation_diff_sha256':'b'*64}],
      'metrics':[]}],'poll_seconds':2,'approval_ttl_seconds':900,'probe_gap_seconds':15}

@pytest.fixture
def config(config_dict): return Configuration.model_validate(config_dict)

@pytest.fixture
def spec(config):
    return Experiment(id='incident-experiment',revision=1,title='Real-execution contract unit test',binding_id='test-binding',
      fault_id='bounded-stop',probe_id='get-health',baseline_seconds=30,observation_seconds=120,ingestion_wait_seconds=0,
      response_deadline_seconds=60,max_error_ratio=.01,max_latency_ms=500,stable_seconds=10,bucket_seconds=5,
      hypotheses='Test explicit response, evidence and restoration obligations, not a fabricated outcome.',
      oracle={'mechanism_code':'capacity_loss','mechanism_description':'One approved serving instance is stopped and capacity becomes unavailable.',
              'affected_resource_arns':[TARGET],'required_checks':['fault-present'],'rubric':'Identify the stopped serving instance and capacity mechanism with relevant evidence.'},
      intervention_runbook_ids=['capacity-change'])

@pytest.fixture
def store(tmp_path): return Store(tmp_path/'workspace')

class Clock:
    def __init__(self): self.value=datetime.now(timezone.utc)
    def __call__(self): return self.value
    def advance(self,seconds): self.value+=timedelta(seconds=seconds)

class World:
    def __init__(self,clock):
        self.clock=clock; self.experiments={}; self.tasks={}; self.automations={}; self.writes=[]
        self.fail_write=False; self.no_task=False; self.no_receipt=False; self.collection_error=False
        self.changed=False; self.qualify_fail=False; self.target_mismatch=False
    def factory(self,binding,store,owner): return FakeAWS(binding,store,owner,self)

class FakeAWS:
    def __init__(self,binding,store,owner,world): self.b=binding; self.store=store; self.owner=owner; self.world=world
    def identity(self,side): return {'account':self.b.agent.account_id if side in ('agent','requester') else self.b.workload.account_id,'principal':'test-principal'}
    def checks(self,ids):
        out=[]
        running=[r for r in self.world.experiments.values() if (self.world.clock()-dt(r['startTime'])).total_seconds()<60]
        for identifier in ids:
            actual='stopped' if identifier=='fault-present' and running else 'applied' if identifier=='changed' and self.world.changed else 'running'
            expected=next(c.expected for c in self.b.checks if c.id==identifier)
            source=self.store.put_record('aws',self.owner,{'test_fixture':True,'actual':actual,'resource':TARGET})
            out.append({'id':identifier,'passed':actual==expected,'actual':actual,'expected':expected,'source_record_id':source['id']})
        self.store.put_record('verification',self.owner,{'checks':out,'all_passed':all(x['passed'] for x in out)})
        return out
    def template(self,fault): return {'contract':{'test_template':fault.template_sha256},'source':'test-contract','duration_upper_bound_seconds':60}
    def qualify(self,spec):
        from lab.util import Blocked
        if self.world.qualify_fail: raise Blocked('Controlled qualification failure')
        return {'template':self.template(self.b.faults[0]),'qualified_at':iso(self.world.clock()),'binding_sha256':digest(self.b.model_dump(mode='json'))}
    def document(self,book): return {'sha256':book.content_sha256}
    def write(self,side,service,operation,params):
        self.world.writes.append((side,service,operation,params))
        if operation=='start_experiment':
            identifier='EXP-'+str(len(self.world.experiments)+1)
            value={'id':identifier,'experimentTemplateId':params['experimentTemplateId'],'startTime':iso(self.world.clock()),'tags':params['tags']}
            self.world.experiments[identifier]=value
            if self.world.fail_write: raise TimeoutError('Response lost after service accepted')
            return {'experiment':value}
        if operation=='stop_experiment': self.world.experiments[params['id']]['forced_stop']=True;return {'experiment':{'id':params['id']}}
        if operation=='create_backlog_task':
            identifier='TASK-'+str(len(self.world.tasks)+1);task={**params,'taskId':identifier,'createdAt':iso(self.world.clock()),'status':'COMPLETED'}
            self.world.tasks[identifier]=task;return {'task':task}
        if operation=='start_automation_execution':
            identifier='auto-'+str(len(self.world.automations)+1);self.world.automations[identifier]=params
            return {'AutomationExecutionId':identifier}
        if operation=='stop_automation_execution': return {}
        raise AssertionError(operation)
    def experiment(self,identifier):
        value=dict(self.world.experiments[identifier]);elapsed=(self.world.clock()-dt(value['startTime'])).total_seconds()
        status='stopped' if value.get('forced_stop') else 'completed' if elapsed>=60 else 'running'
        value['state']={'status':status};value['actions']={'Stop':{'state':{'status':'completed' if status=='completed' else 'running'}}}
        if status!='running': value['endTime']=iso(dt(value['startTime'])+timedelta(seconds=60))
        source=self.store.put_record('aws',self.owner,{'experiment':value})
        target=TARGET if not self.world.target_mismatch else TARGET+'-other'
        return {'experiment':value,'source_record_id':source['id'],'resolved_targets':[{'targetInformation':{'arn':target}}]}
    def observe(self,start,end,fault_at=None,assisted_task=None):
        if self.world.collection_error: raise RuntimeError('Controlled observation outage')
        now=dt(end);fault=dt(fault_at) if fault_at else now
        benign=self.store.entity(self.owner)['data']['arm']=='benign'
        alarm={'at':iso(fault+timedelta(seconds=2))} if not benign and now>=fault+timedelta(seconds=2) else None
        receipt={'accepted_at':iso(fault+timedelta(seconds=5))} if alarm and not self.world.no_receipt else None
        task=None;findings=[]
        if not benign and now>=fault+timedelta(seconds=10) and not self.world.no_task:
            task={'taskId':'native-task','createdAt':iso(fault+timedelta(seconds=10))}
            if now>=fault+timedelta(seconds=30):
                for typ,text in [('investigation_summary_md','The serving instance stopped, causing capacity loss.'),('mitigation_summary_md','Increase serving capacity with the reviewed deployment change.')]:
                    body={'recordType':typ,'createdAt':iso(fault+timedelta(seconds=30)),'content':{'text':text},'recordId':typ}
                    record=self.store.put_record('finding',self.owner,body,'finding-'+digest([self.owner,body])[:32]);findings.append(record['id'])
        return {'start':start,'end':end,'at':iso(self.world.clock()),'complete':True,'alarm':alarm,'receipt':receipt,'task':task,
                'findings':findings,'correlation':'exact_reference' if task else 'none','candidate_ids':[task['taskId']] if task else [],'service_task_ids':[task['taskId']] if task else [],'benign_scope_complete':True,'lifecycle':[],'metrics':[]}
    def pages(self,side,service,op,key,**kwargs):
        if op=='list_experiments': return list(self.world.experiments.values()),[]
        if op=='list_backlog_tasks': return list(self.world.tasks.values()),[]
        raise AssertionError(op)
    def recommendations(self,task_id):
        item={'recommendationId':'rec-test','version':3,'taskId':task_id,'title':'Add serving capacity','content':{'summary':'Increase serving capacity with the reviewed deployment change.'}}
        record=self.store.put_record('recommendation',self.owner,{'recommendation':item},'recommendation-'+digest([self.owner,item])[:32])
        return {'task':{'taskId':task_id,'status':'COMPLETED'},'recommendation_record_ids':[record['id']],'complete':True}
    def automation(self,execution_id):
        self.world.changed=True
        value={'AutomationExecutionId':execution_id,'AutomationExecutionStatus':'Success','DocumentVersion':'1','Parameters':self.world.automations[execution_id]['Parameters'],'DocumentName':DOC}
        source=self.store.put_record('aws',self.owner,{'execution':value});return {'execution':value,'source_record_id':source['id']}
    def task(self,task_id,task_type='INVESTIGATION'): return self.world.tasks[task_id],'test-task-source'

@pytest.fixture
def rig(config,store,spec):
    clock=Clock();world=World(clock);service=Service(config,store,aws_factory=world.factory,clock=clock)
    reference=service.register(spec)['id'];engine=Engine(config,store,aws_factory=world.factory,clock=clock)
    return {'clock':clock,'world':world,'service':service,'engine':engine,'store':store,'config':config,'spec':spec,'reference':reference}


def approve(service,entity_id,purpose='start'):
    subject=service.approval_subject(entity_id,purpose)
    return service.approve(entity_id,purpose,Approval(expected_digest=subject['digest'],confirmation=subject['confirmation'],
             approver='Test approval token holder',rationale='Test-only explicit approval of the recorded exact instrument.'))


def probe_samples(store,tid,start,seconds,*,bad_until=0,healthy=True):
    for i in range(seconds):
        at=iso(dt(start)+timedelta(seconds=i))
        store.probe(tid,{'scheduled_at':at,'at':at,'received_at':at,'attempted':True,'success':healthy and i>=bad_until,
                         'latency_ms':25.0,'status':200 if healthy and i>=bad_until else 503,'probe_id':'get-health','scheduling_lag_seconds':0})


def run_trial(rig,campaign=None,arm='baseline',*,bad_until=60):
    s=rig['service'];store=rig['store'];e=rig['engine'];clock=rig['clock']
    trial=s.trial(TrialRequest(experiment_ref=rig['reference'],campaign_id=campaign,arm=arm));tid=trial['id']
    s.qualify(tid);e.step();assert store.entity(tid)['state']=='READY'
    approve(s,tid)
    store.meta('worker',{'state':'running','heartbeat_at':iso(clock())});s.start(tid)
    start=store.entity(tid)['data']['started_at'];clock.value=dt(start)
    probe_samples(store,tid,start,30)
    clock.advance(30);e.step();assert store.entity(tid)['state']=='EXPOSING'
    e.step();assert store.entity(tid)['state']=='OBSERVING'
    start=store.entity(tid)['data']['exposure_at']
    probe_samples(store,tid,start,120,bad_until=bad_until)
    for _ in range(12):clock.advance(10);e.step()
    for _ in range(4):e.step()
    return store.entity(tid)
