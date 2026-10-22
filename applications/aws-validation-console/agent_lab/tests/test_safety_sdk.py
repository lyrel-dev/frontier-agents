"""Provider contract tests with botocore Stubber; no AWS access is attempted."""
from contextlib import ExitStack
from copy import deepcopy
from datetime import timedelta
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import boto3
from botocore.stub import Stubber, ANY
from botocore.exceptions import ReadTimeoutError
import pytest
from pydantic import ValidationError

from lab.aws import AWS, template_contract, duration_seconds, compare
from lab.broker import Broker
from lab.models import Configuration, Binding, Probe, TrialRequest, CampaignRequest, ChangeProposal
from lab.probe import request as request_probe, permitted_addresses
from lab.util import Blocked, UnknownRemoteState, digest, iso,dt
from conftest import ACCOUNT_A,ACCOUNT_B,TARGET,ALARM,DOC,approve,run_trial,probe_samples


def adapter(config,store,services):
    a=AWS(config.bindings[0],store,'sdk-contract')
    clients={s:boto3.client(s,region_name='eu-central-1',aws_access_key_id='TESTONLY',aws_secret_access_key='TESTONLY') for s in services}
    a.client=lambda side,service,write=False: clients[service]
    return a,clients


def identity(account=ACCOUNT_A,root=False):
    return {'Account':account,'Arn':f'arn:aws:iam::{account}:root' if root else f'arn:aws:sts::{account}:assumed-role/Observer/test','UserId':'TESTONLY'}


@pytest.mark.parametrize('account,root,allowed',[(ACCOUNT_A,False,True),(ACCOUNT_B,False,False),(ACCOUNT_A,True,False)])
def test_sts_account_and_root_boundary(config,store,account,root,allowed):
    a,c=adapter(config,store,['sts'])
    with Stubber(c['sts']) as stub:
        stub.add_response('get_caller_identity',identity(account,root),{})
        if allowed: assert a.identity('agent')['account']==ACCOUNT_A
        else:
            with pytest.raises(Blocked):a.identity('agent')
        stub.assert_no_pending_responses()


def task(kind='INVESTIGATION'):
    return {'agentSpaceId':'space-test','taskId':'sdk-task','title':'SDK contract only','taskType':kind,'priority':'MEDIUM','status':'COMPLETED','createdAt':dt('2026-01-01T00:00:00Z'),'updatedAt':dt('2026-01-01T00:01:00Z'),'version':1}


@pytest.mark.parametrize('bad', ['space','kind','id',None])
def test_task_sdk_identity(config,store,bad):
    a,c=adapter(config,store,['devops-agent']);a.verified['agent']={}
    item=task()
    if bad=='space':item['agentSpaceId']='other-space'
    if bad=='kind':item['taskType']='EVALUATION'
    if bad=='id':item['taskId']='other-task'
    with Stubber(c['devops-agent']) as stub:
        stub.add_response('get_backlog_task',{'task':item},{'agentSpaceId':'space-test','taskId':'sdk-task'})
        if bad:
            with pytest.raises(Blocked):a.task('sdk-task')
        else: assert a.task('sdk-task')[0]['taskType']=='INVESTIGATION'


def test_pagination_complete_and_repeated_token(config,store):
    a,c=adapter(config,store,['devops-agent'])
    with Stubber(c['devops-agent']) as stub:
        stub.add_response('list_backlog_tasks',{'tasks':[task()],'nextToken':'token-one'},{'agentSpaceId':'space-test','limit':100})
        stub.add_response('list_backlog_tasks',{'tasks':[]},{'agentSpaceId':'space-test','limit':100,'nextToken':'token-one'})
        items,refs=a.pages('agent','devops-agent','list_backlog_tasks','tasks',agentSpaceId='space-test',limit=100)
        assert len(items)==1 and len(refs)==2
        stub.add_response('list_backlog_tasks',{'tasks':[],'nextToken':'loop'},{'agentSpaceId':'space-test'})
        stub.add_response('list_backlog_tasks',{'tasks':[],'nextToken':'loop'},{'agentSpaceId':'space-test','nextToken':'loop'})
        with pytest.raises(Blocked,match='Repeated'):a.pages('agent','devops-agent','list_backlog_tasks','tasks',agentSpaceId='space-test')


def test_recommendation_exact_version_and_lineage(config,store):
    a,c=adapter(config,store,['devops-agent']);a.verified['agent']={}
    item={'agentSpaceArn':f'arn:aws:aidevops:eu-central-1:{ACCOUNT_A}:agentspace/space-test','recommendationId':'rec-sdk','taskId':'sdk-task','title':'SDK contract','content':{'summary':'A captured recommendation','spec':'A specific deployment change'},'status':'PROPOSED','priority':'MEDIUM','createdAt':dt('2026-01-01T00:00:00Z'),'updatedAt':dt('2026-01-01T00:00:00Z'),'version':3}
    with Stubber(c['devops-agent']) as stub:
        stub.add_response('get_backlog_task',{'task':task('EVALUATION')},{'agentSpaceId':'space-test','taskId':'sdk-task'})
        stub.add_response('list_recommendations',{'recommendations':[item]},{'agentSpaceId':'space-test','taskId':'sdk-task','limit':100})
        stub.add_response('get_recommendation',{'recommendation':item},{'agentSpaceId':'space-test','recommendationId':'rec-sdk','recommendationVersion':3})
        response=a.recommendations('sdk-task')
        assert store.record(response['recommendation_record_ids'][0])['data']['recommendation']['version']==3
        stub.assert_no_pending_responses()


def test_fis_resolved_target_sdk_shape(config,store):
    a,c=adapter(config,store,['fis']);a.verified['fault']={}
    with Stubber(c['fis']) as stub:
        stub.add_response('get_experiment',{'experiment':{'id':'EXPtest','state':{'status':'running'}}},{'id':'EXPtest'})
        stub.add_response('list_experiment_resolved_targets',{'resolvedTargets':[{'resourceType':'aws:ec2:instance','targetName':'Instances','targetInformation':{'arn':TARGET}}]},
                          {'experimentId':'EXPtest','maxResults':100})
        assert a.experiment('EXPtest')['resolved_targets'][0]['targetInformation']['arn']==TARGET


def test_write_operations_match_sdk_request_contract(config,store):
    a,c=adapter(config,store,['fis','ssm','devops-agent']);a.verified={'fault':{},'change':{},'requester':{}}
    with ExitStack() as stack:
        f=stack.enter_context(Stubber(c['fis']));s=stack.enter_context(Stubber(c['ssm']));d=stack.enter_context(Stubber(c['devops-agent']))
        f.add_response('get_safety_lever',{'safetyLever':{'id':'default','state':{'status':'disengaged'}}},{'id':'default'})
        f.add_response('start_experiment',{'experiment':{'id':'EXPtest'}},{'experimentTemplateId':'EXTtest','clientToken':ANY,'tags':{'ValidationTrial':'contract-owner','ValidationOperation':ANY}})
        s.add_response('start_automation_execution',{'AutomationExecutionId':'00000000-0000-4000-8000-000000000001'},
            {'DocumentName':DOC,'DocumentVersion':'1','Parameters':{'AutomationAssumeRole':[f'arn:aws:iam::{ACCOUNT_B}:role/AutomationExecution']},'Mode':'Auto','ClientToken':ANY,'Tags':[{'Key':'ValidationTrial','Value':'contract-owner'},{'Key':'ValidationOperation','Value':ANY}]})
        d.add_response('create_backlog_task',{'task':task('EVALUATION')},{'agentSpaceId':'space-test','taskType':'EVALUATION','priority':'MEDIUM','title':'Contract','clientToken':ANY})
        broker=Broker(store,a,True)
        assert broker.execute('contract-owner','fis','fault','fis','start_experiment',{'experimentTemplateId':'EXTtest'})['provider_id']=='EXPtest'
        assert broker.execute('contract-owner','ssm','change','ssm','start_automation_execution',{'DocumentName':DOC,'DocumentVersion':'1','Parameters':{'AutomationAssumeRole':[f'arn:aws:iam::{ACCOUNT_B}:role/AutomationExecution']},'Mode':'Auto'})['state']=='CONFIRMED'
        assert broker.execute('contract-owner','eval','requester','devops-agent','create_backlog_task',{'agentSpaceId':'space-test','taskType':'EVALUATION','priority':'MEDIUM','title':'Contract'})['state']=='CONFIRMED'
        for stub in (f,s,d):stub.assert_no_pending_responses()


@pytest.mark.parametrize('value,expected',[('PT1M',60),('PT1H2M3S',3723),('PT0.5S',.5),('P1D',None),('PT',None),('',None)])
def test_only_bounded_durations(value,expected):
    if expected is None:
        with pytest.raises(Blocked):duration_seconds(value)
    else:assert duration_seconds(value)==expected


def test_malformed_success_remains_unknown_not_safe_failure(rig):
    adapter=rig['world'].factory(rig['config'].bindings[0],rig['store'],'bad-response')
    adapter.write=lambda *args:{}
    with pytest.raises(UnknownRemoteState):Broker(rig['store'],adapter,True).execute('bad-response','start','fault','fis','start_experiment',{'experimentTemplateId':'EXTtest'})
    assert rig['store'].operation('bad-response','start')['state']=='UNKNOWN'


def test_expired_approval_cannot_dispatch_after_a_healthy_baseline(rig):
    s,e,store,clock=rig['service'],rig['engine'],rig['store'],rig['clock']
    t=s.trial(TrialRequest(experiment_ref=rig['reference']));s.qualify(t['id']);e.step();approve(s,t['id'])
    store.meta('worker',{'state':'running','heartbeat_at':iso(clock())});s.start(t['id'])
    probe_samples(store,t['id'],iso(clock()),30);clock.advance(30);e.step()
    clock.advance(1000);e.step()
    assert store.entity(t['id'])['state']=='CLOSED_BLOCKED' and not rig['world'].writes


def test_restore_required_reserves_environment(rig):
    s,e,store=rig['service'],rig['engine'],rig['store']
    old=store.create('trial','RESTORE_REQUIRED',{'title':'unresolved'})
    t=s.trial(TrialRequest(experiment_ref=rig['reference']));s.qualify(t['id']);e.step();approve(s,t['id'])
    store.meta('worker',{'state':'running','heartbeat_at':iso(rig['clock']())})
    with pytest.raises(Blocked,match='Only one'):s.start(t['id'])


def test_restart_resumes_same_fis_identity(rig):
    s,e,store,clock=rig['service'],rig['engine'],rig['store'],rig['clock']
    t=s.trial(TrialRequest(experiment_ref=rig['reference']));tid=t['id'];s.qualify(tid);e.step();approve(s,tid)
    store.meta('worker',{'state':'running','heartbeat_at':iso(clock())});s.start(tid)
    probe_samples(store,tid,iso(clock()),30);clock.advance(30);e.step();e.step()
    external=store.entity(tid)['data']['fis_id']
    from lab.engine import Engine
    replacement=Engine(rig['config'],store,aws_factory=rig['world'].factory,clock=clock)
    replacement.step()
    assert store.entity(tid)['data']['fis_id']==external
    assert sum(w[2]=='start_experiment' for w in rig['world'].writes)==1


def test_abort_stops_owned_fault_and_records_abort(rig):
    s,e,store,clock=rig['service'],rig['engine'],rig['store'],rig['clock']
    t=s.trial(TrialRequest(experiment_ref=rig['reference']));tid=t['id'];s.qualify(tid);e.step();approve(s,tid)
    store.meta('worker',{'state':'running','heartbeat_at':iso(clock())});s.start(tid)
    probe_samples(store,tid,iso(clock()),30);clock.advance(30);e.step();e.step()
    s.abort(tid)
    for _ in range(7):clock.advance(2);e.step()
    assert any(w[2]=='stop_experiment' for w in rig['world'].writes)
    assert store.entity(tid)['state']=='CLOSED_ABORTED'


def test_observation_loss_never_proves_agent_silence(rig):
    rig['world'].no_task=True;rig['world'].collection_error=True
    t=run_trial(rig)
    a=rig['store'].record(t['data']['assessment_id'])['data']
    assert a['dimensions']['response']['outcome']=='inconclusive'


def test_unknown_ssm_has_no_blind_retry(rig):
    aws=rig['world'].factory(rig['config'].bindings[0],rig['store'],'unknown-change')
    count=[]
    def write(*args):count.append(args);raise TimeoutError('Accepted outcome unknown')
    aws.write=write;broker=Broker(rig['store'],aws,True)
    for _ in range(2):
        with pytest.raises(UnknownRemoteState):broker.execute('unknown-change','apply','change','ssm','start_automation_execution',{'DocumentName':DOC,'DocumentVersion':'1','Parameters':{'AutomationAssumeRole':['arn:aws:iam::222222222222:role/AutomationExecution']}})
    assert len(count)==1


def test_observation_operator_cannot_invoke_mutation_adapter(config,store):
    a,c=adapter(config,store,[])
    with pytest.raises(Blocked):a.write('workload','ec2','terminate_instances',{'InstanceIds':['i-test']})
    with pytest.raises(Blocked):a.call('workload','ssm','send_command',DocumentName='anything')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=='/redirect':
            self.send_response(302);self.send_header('Location','http://169.254.169.254/');self.end_headers();return
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"business_ok":true}')
    def log_message(self,*args):pass


@pytest.mark.parametrize('path,expected',[('/health',True),('/redirect',False)])
def test_real_loopback_probe_no_redirect(tmp_path,path,expected):
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        p=Probe(id='local-test',title='test-only actual HTTP probe',url=f'http://127.0.0.1:{server.server_port}{path}',allowed_networks=['127.0.0.1/32'],allow_loopback_http=True,json_expression='business_ok',expected_json_value=True)
        response=request_probe(p,iso())
        assert response['attempted'] and response['success']==expected and response['latency_ms']>=0
        assert 'body' not in response
    finally:server.shutdown();server.server_close()


def test_dns_outside_approved_cidr_is_blocked(monkeypatch):
    p=Probe(id='boundary',title='CIDR boundary',url='https://example.invalid/',allowed_networks=['10.0.0.0/8'])
    monkeypatch.setattr(socket,'getaddrinfo',lambda *args,**kwargs:[(socket.AF_INET,socket.SOCK_STREAM,6,'',('169.254.169.254',443))])
    with pytest.raises(Blocked):permitted_addresses(p)
