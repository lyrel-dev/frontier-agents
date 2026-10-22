"""Credential-free component acceptance. Fixtures never ship as workspace data."""
from copy import deepcopy
from types import SimpleNamespace
from datetime import timedelta
import json
import pytest
import boto3
from botocore.stub import Stubber
from fastapi.testclient import TestClient
from conftest import ACCOUNT_A,ACCOUNT_B,TARGET,ALARM
from test_fis_fleet import collect,configuration,template
from lab.models import Configuration,Account,FISAccount,Binding,Fault,Approval,Experiment,BusinessRequirement
from lab.setup import Setup,ConfigDraft,AccountDraft,refresh,Compose
from lab.native_fis import Previews,PreviewAWS,target_key,target_identity,target_match,native_template,account_contract
from lab.business import evaluate
from lab.api import create_app
from lab.util import Blocked,digest,iso,dt,UnknownRemoteState

OP='operator-only-test-token-0123456789';AP='approval-only-test-token-0123456789'

class Profiles:
    available_profiles=['test-only','test-agent','test-workload','test-fault','test-change','test-requester']

def setup_service(config,store):
    names={a.profile for a in config.fis_accounts}
    for b in config.bindings:names.update([b.agent.profile,b.workload.profile,b.fault_profile,b.change_profile,b.requester_profile])
    provider=Profiles();provider.available_profiles=sorted(n for n in names if n)
    return Setup(config,store,session_factory=lambda profile=None:provider)

def approval(subject):return Approval(expected_digest=subject['digest'],confirmation=subject['confirmation'],approver='Test approver',rationale='Test-only precise scope approval.')

def native_fixture(config,store,*,multi=False):
    cfg=configuration(config)
    cfg.fis_accounts[0].execution_profile='test-only'
    c,v,_=collect(cfg,store)
    # collect constructs the same discovery account without executor; use resulting row.
    row=v['templates'][0];data=deepcopy(row['data']);t=deepcopy(data['template'])
    target={'targetName':'Instances','resourceType':'aws:ec2:instance','targetInformation':{'arn':TARGET}}
    configs=[];extra=[]
    if multi:
        other='333333333333'
        t['experimentOptions']['accountTargeting']='multi-account'
        t['targets']['Instances'].pop('resourceArns');t['targets']['Instances']['resourceTags']={'Test':'approved'}
        configs=[{'accountId':a,'roleArn':f'arn:aws:iam::{a}:role/FIS'} for a in [ACCOUNT_B,other]]
        extra=[{'account_id':other,'region':cfg.bindings[0].workload.region,'profile':'test-only','association_id':'other-association'}]
    data.update(template=t,contract_sha256=digest(__import__('lab.aws',fromlist=['template_contract']).template_contract(t)),target_accounts=configs)
    row=store.put_record('fis_template',row['owner'],data)
    targets=[target]
    if multi:targets.append({**target,'targetInformation':{'arn':TARGET.replace(ACCOUNT_B,'333333333333')}})
    preview=store.put_record('fis_preview_result','preview-fixture',{'template_record_id':row['id'],'template_id':t['id'],
      'account_id':ACCOUNT_B,'region':cfg.bindings[0].workload.region,'template_sha256':data['contract_sha256'],
      'target_accounts_sha256':digest(account_contract(configs)),'target_accounts':account_contract(configs),'targets':targets,'captured_at':iso()})
    b=cfg.bindings[0].model_dump(mode='json');b['orchestrator']={**b['workload'],'profile':'test-only'};b['target_accounts']=extra
    f=b['faults'][0];f.update(native_fis=True,preview_record_id=preview['id'],target_accounts_sha256=preview['data']['target_accounts_sha256'],
      resolved_targets=targets,target_arns=[target_identity(r) for r in targets],template_id=t['id'],template_sha256=data['contract_sha256'],
      independent_recovery='Reviewed test recovery independent of the local controller.',action_review='Test-only permission and action prerequisite review.')
    if multi:
        for phase in ['baseline_checks','fault_checks','cleanup_checks']:
            original=next(x for x in b['checks'] if x['id']==f[phase][0]);new={**original,'id':phase+'-other','account_id':'333333333333'}
            b['checks'].append(new);f[phase].append(new['id'])
    binding=Binding.model_validate(b)
    cfg.bindings=[binding]
    return cfg,row,preview,binding


def test_local_configuration_requires_installed_profiles(config,store):
    s=setup_service(config,store);data=config.model_dump(mode='json');data['fis_accounts']=[{'id':'bad','name':'bad','account_id':ACCOUNT_A,'profile':'not-installed','regions':['eu-central-1']}]
    with pytest.raises(Blocked,match='Install'):s.draft(ConfigDraft(configuration=data,base_digest=digest(config.model_dump(mode='json')),rationale='No new host profiles allowed.'))


def test_config_activation_is_atomic_persistent_and_stale_safe(config,store):
    s=setup_service(config,store);data=config.model_dump(mode='json');data['poll_seconds']=3
    draft=s.draft(ConfigDraft(configuration=data,base_digest=digest(config.model_dump(mode='json')),rationale='Test local configuration revision.'))
    sub=s.subject(draft['id']);s.commit(draft['id'],approval(sub))
    assert config.poll_seconds==3 and not store.operations()
    restarted=Configuration();refresh(restarted,store);assert restarted.poll_seconds==3
    with pytest.raises(Blocked,match='stale'):s.commit(draft['id'],approval(sub))


@pytest.mark.parametrize('kind,state',[('trial','BASELINING'),('trial','READY'),('trial','RESTORE_REQUIRED'),('fis_preview','RUNNING'),('fis_campaign','RUNNING'),('fis_scope','SCANNING')])
def test_config_activation_cannot_change_active_work(config,store,kind,state):
    s=setup_service(config,store);draft=s.draft(ConfigDraft(configuration=config,base_digest=digest(config.model_dump(mode='json')),rationale='Test configuration concurrency boundary.'))
    store.create(kind,state,{})
    with pytest.raises(Blocked,match='active'):s.commit(draft['id'],approval(s.subject(draft['id'])))
    assert store.meta('active_configuration') is None


def test_operator_cannot_activate_config_or_start_preview(store):
    client=TestClient(create_app(Configuration(),store,OP,AP))
    for path in ['/api/setup/approve/config/fake','/api/setup/approve/preview/fake']:
        assert client.post(path,headers={'Authorization':'Bearer '+OP},json={}).status_code==403
    assert not store.operations()


def test_empty_setup_does_not_create_aws_clients(store,monkeypatch):
    monkeypatch.setattr(boto3.Session,'available_profiles',property(lambda self:[]))
    client=TestClient(create_app(Configuration(),store,OP,AP))
    r=client.get('/api/setup',headers={'Authorization':'Bearer '+OP})
    assert r.status_code==200 and r.json()['configuration']['fis_accounts']==[]
    assert not store.entities() and not store.operations()


def test_target_policy_handles_arns_and_parameter_targets(config,store):
    cfg,row,preview,binding=native_fixture(config,store);f=binding.faults[0];target=preview['data']['targets'][0]
    assert target_match(f,[target],complete=True)
    assert target_identity(target)==TARGET
    pod={'resourceType':'aws:eks:pod','targetName':'Pods','targetInformation':{'namespace':'app','name':'pod-a','uid':'actual-uid'}}
    assert target_identity(pod).startswith('fis-resource:')
    assert target_key(pod)==pod
    with pytest.raises(Blocked):target_match(f,[pod])
    assert not target_match(f,[])
    with pytest.raises(Blocked):target_match(f,[],complete=True)


def test_subset_never_expands_outside_approved_resources(config,store):
    cfg,row,p,b=native_fixture(config,store,multi=True);f=b.faults[0].model_copy(update={'target_match':'subset'})
    assert target_match(f,[p['data']['targets'][0]],complete=True)
    changed=deepcopy(p['data']['targets'][0]);changed['targetInformation']['arn']+='-outside'
    with pytest.raises(Blocked):target_match(f,[changed],complete=True)


def test_multiaccount_requires_verifiers_in_each_phase(config,store):
    cfg,row,p,b=native_fixture(config,store,multi=True)
    raw=b.model_dump(mode='json');raw['faults'][0]['cleanup_checks']=[raw['faults'][0]['cleanup_checks'][0]]
    with pytest.raises(ValueError,match='every target'):Binding.model_validate(raw)


class NativeReader:
    def __init__(self,binding,store,t,configs):self.b,self.store,self.t,self.configs=binding,store,t,configs;self.calls=[]
    def side_account(self,side):return self.b.orchestrator or self.b.workload
    def identity(self,side):self.calls.append(('identity',side))
    def call(self,side,service,op,**params):
        self.calls.append((side,op))
        if op=='get_experiment_template':return {'experimentTemplate':self.t},'source'
        if op=='get_action':return {'action':{'id':params['id']}},'action-source'
        if op=='describe_alarms':return {'MetricAlarms':[{'AlarmArn':ALARM,'StateValue':'OK'}]},'alarm-source'
        raise AssertionError(op)
    def pages(self,*args,**kw):return self.configs,['accounts-source']


def test_multiaccount_native_definition_qualifies_without_rewriting(config,store):
    cfg,row,p,b=native_fixture(config,store,multi=True);reader=NativeReader(b,store,row['data']['template'],row['data']['target_accounts'])
    result=native_template(reader,b.faults[0])
    assert result['contract']['experimentOptions']['accountTargeting']=='multi-account'
    assert result['contract']['targets']['Instances']['resourceTags']=={'Test':'approved'}
    assert result['target_accounts']==account_contract(row['data']['target_accounts'])


@pytest.mark.parametrize('mutation',['definition','role','accounts','preview'])
def test_native_definition_drift_blocks_before_dispatch(config,store,mutation):
    cfg,row,p,b=native_fixture(config,store,multi=True);t=deepcopy(row['data']['template']);configs=deepcopy(row['data']['target_accounts']);f=b.faults[0]
    if mutation=='definition':t['actions']['Stop']['parameters']['startInstancesAfterDuration']='PT5M'
    if mutation=='role':t['roleArn']='arn:aws:iam::999999999999:role/other'
    if mutation=='accounts':configs[0]['roleArn']+='-different'
    if mutation=='preview':f=f.model_copy(update={'resolved_targets':[]})
    with pytest.raises(Blocked):native_template(NativeReader(b,store,t,configs),f)


def test_preview_approval_is_exact_and_writes_disabled_blocks(config,store):
    cfg,row,p,b=native_fixture(config,store);previews=Previews(cfg,store);sub=previews.subject(row['id'])
    wrong=approval(sub).model_copy(update={'confirmation':'different'})
    with pytest.raises(Blocked):previews.request(row['id'],wrong)
    cfg.enable_aws_writes=False
    with pytest.raises(Blocked,match='disabled'):previews.request(row['id'],approval(sub))
    assert not store.operations()


def test_preview_uses_actual_skip_all_sdk_request(store):
    account=FISAccount(id='fixture',name='Fixture only',account_id=ACCOUNT_B,regions=['eu-central-1'],profile='unused')
    session=boto3.Session(aws_access_key_id='testing',aws_secret_access_key='testing',region_name='eu-central-1')
    client=session.client('fis');adapter=PreviewAWS(account,'eu-central-1',store,'fixture',factory=lambda **kw:session)
    adapter.clients[('fis',True)]=client
    request={'clientToken':'original-token','experimentTemplateId':'EXTtest','experimentOptions':{'actionsMode':'skip-all'}}
    with Stubber(client) as stub:
        stub.add_response('start_experiment',{'experiment':{'id':'EXPtest'}},request)
        assert adapter.write('fault','fis','start_experiment',request)['experiment']['id']=='EXPtest'
    with pytest.raises(Blocked):adapter.write('fault','fis','start_experiment',{**request,'experimentOptions':{'actionsMode':'run-all'}})


@pytest.mark.parametrize('outcome,value,complete,closed,missing',[('pass',0,True,True,0),('fail',1,True,True,0),('inconclusive',None,True,True,1),('inconclusive',0,False,True,0),('inconclusive',0,True,False,0)])
def test_business_evidence_never_substitutes_availability(outcome,value,complete,closed,missing):
    requirement=BusinessRequirement(id='lost',metric_id='lost',category='data_correctness',aggregation='maximum',operator='eq',threshold=0,interpretation='Independently reconciled acknowledged writes over the declared incident interval.')
    checks,dims=evaluate([requirement],{'complete':True,'metrics':[{'id':'lost','complete':complete,'missing':missing,'points':[{'value':value}]}]},closed=closed,source_id='actual-capture')
    assert checks[0]['outcome']==outcome and dims['data_correctness']['outcome']==outcome
    assert dims['collateral_regression']['outcome']=='not_assessed'


def test_no_business_requirement_is_not_a_correctness_pass():
    checks,dims=evaluate([],{},closed=True)
    assert not checks and all(d['outcome']=='not_assessed' for d in dims.values())


def test_cross_origin_setup_approval_rejected(store):
    client=TestClient(create_app(Configuration(),store,OP,AP))
    r=client.post('/api/setup/approve/config/fake',headers={'Authorization':'Bearer '+AP,'Origin':'https://untrusted.example'},json={})
    assert r.status_code==403


def test_guided_plan_generates_native_contract_without_fault_duplication(config,store):
    cfg,row,p,b=native_fixture(config,store);cfg.fis_accounts.append(FISAccount(id='agent',name='Agent fixture',account_id=ACCOUNT_A,profile=cfg.bindings[0].agent.profile,regions=['eu-central-1']))
    s=setup_service(cfg,store);work=cfg.fis_accounts[0].id
    params={'template_record_id':row['id'],'preview_record_id':p['id'],'binding_id':'guided','name':'Guided test plan','agent_connection_id':'agent','agent_region':'eu-central-1','agent_space_id':b.agent_space_id,
      'workload_connection_id':work,'association_id':b.association_id,'service_id':'fixture-service','deployment_model':'ec2','maximum_fault_seconds':60,
      'independent_recovery':'The independent test restore path exists outside this controller.','action_review':'Test fixture action permissions and prerequisites reviewed.','safety_review':'Test fixture exact stop alarm and resource scope review.',
      'probe':b.probes[0],'checks':b.checks,'baseline_check_ids':b.faults[0].baseline_checks,'fault_check_ids':b.faults[0].fault_checks,'cleanup_check_ids':b.faults[0].cleanup_checks,
      'route':b.route,'oracle':{'mechanism_code':'capacity','mechanism_description':'Independently measured approved capacity loss during exposure.','affected_resource_arns':[TARGET],'required_checks':b.faults[0].fault_checks,'rubric':'Match the resource and mechanism with independently collected facts.'},
      'experiment_id':'guided','hypotheses':'The selected agent investigates the qualified service disruption.','observation_seconds':120,'response_deadline_seconds':60}
    plan=s.compose(Compose.model_validate(params));assert plan['kind']=='guided_plan'
    assert plan['data']['configuration']['bindings'][-1]['faults'][0]['template_sha256']==row['data']['contract_sha256']
    s.commit(plan['id'],approval(s.subject(plan['id'])))
    assert store.record('experiment:guided@1')['data']['binding_id']=='guided'
    assert next(b for b in cfg.bindings if b.id=='guided').faults[0].native_fis
    assert not store.operations()
