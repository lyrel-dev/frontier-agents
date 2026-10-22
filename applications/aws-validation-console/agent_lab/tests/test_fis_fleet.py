"""Test-only AWS catalogue responses and campaign state machines; no AWS access."""
from copy import deepcopy
from datetime import timedelta
import json
import pytest
import boto3
from botocore.stub import Stubber
from fastapi.testclient import TestClient
from conftest import ACCOUNT_A, ACCOUNT_B, TARGET, ALARM, approve, probe_samples
from lab.api import create_app
from lab.models import Configuration, Experiment
from lab.fis_catalog import Catalog, accounts
from lab.fis_campaigns import Fleet, QueueRequest, AttachContract, execution_gaps
from lab.fis_benchmark import benchmark, benchmark_csv
from lab.aws import template_contract
from lab.util import Blocked, digest, iso, dt

OP='operator-test-only-1234567890'; AP='approver-test-only-1234567890'


def template(identifier='EXTtest'):
    return {'id':identifier,'description':'Test-only AWS definition',
        'roleArn':f'arn:aws:iam::{ACCOUNT_B}:role/FISExecution',
        'targets':{'Instances':{'resourceType':'aws:ec2:instance','resourceArns':[TARGET],'selectionMode':'ALL'}},
        'actions':{'Stop':{'actionId':'aws:ec2:stop-instances','parameters':{'startInstancesAfterDuration':'PT1M'},'targets':{'Instances':'Instances'}}},
        'stopConditions':[{'source':'aws:cloudwatch:alarm','value':ALARM}],
        'experimentOptions':{'accountTargeting':'single-account','emptyTargetResolutionMode':'fail'}}


class Reader:
    def __init__(self, page_count=1, multi=False):
        self.calls=[]; self.page_count=page_count; self.multi=multi; self.wrong_identity=False; self.root=False; self.repeated=False; self.fail_detail=False
    def factory(self, profile): return self
    def client(self, service, **kwargs): self.region=kwargs['region_name'];return self
    def get_caller_identity(self):
        self.calls.append(('sts',{})); account=ACCOUNT_A if self.wrong_identity else ACCOUNT_B
        return {'Account':account,'Arn':f'arn:aws:iam::{account}:'+('root' if self.root else 'role/reader'),'ResponseMetadata':{'RequestId':'test-request'}}
    def list_experiment_templates(self, **params):
        self.calls.append(('templates',params.copy()));i=int(params.get('nextToken','0'))
        result={'experimentTemplates':[{'id':'EXTtest' if i==0 else 'EXT'+str(i),'description':'Test-only row'}]}
        if i+1<self.page_count: result['nextToken']='0' if self.repeated else str(i+1)
        return result
    def get_experiment_template(self, **params):
        self.calls.append(('detail',params.copy()))
        if self.fail_detail: raise RuntimeError('Test-only denied detail')
        t=template(params['id'])
        if self.multi: t['experimentOptions']['accountTargeting']='multi-account'
        return {'experimentTemplate':t,'ResponseMetadata':{'RequestId':'test-detail'}}
    def list_target_account_configurations(self, **params):
        self.calls.append(('targets',params.copy()))
        result={'targetAccountConfigurations':[{'accountId':ACCOUNT_B,'roleArn':f'arn:aws:iam::{ACCOUNT_B}:role/FIS'}]}
        if 'nextToken' not in params: result['nextToken']='accounts-2'
        return result
    def list_experiments(self, **params):
        self.calls.append(('history',params.copy()))
        result={'experiments':[{'id':'EXPtest'+str('nextToken' in params),'experimentTemplateId':'EXTtest','state':{'status':'completed'}}]}
        if 'nextToken' not in params: result['nextToken']='history-2'
        return result


def configuration(config):
    return config.model_copy(update={'fis_accounts':[
        __import__('lab.models',fromlist=['FISAccount']).FISAccount(id='test-discovery',name='Test-only account',account_id=ACCOUNT_B,profile='test-only',regions=['eu-central-1'])]})


def collect(config,store,reader=None):
    reader=reader or Reader(); c=Catalog(configuration(config),store,session_factory=reader.factory)
    job=c.request()
    for _ in range(100):
        c.step()
        if store.entity(job['id'])['state'] in {'COMPLETE','PARTIAL','ERROR','DENIED','CANCELLED'}:break
    return c,c.view(),reader


def fleet_plan(rig, *, repetitions=1, stop_on_failure=True):
    c,v,_=collect(rig['config'],rig['store'])
    fleet=Fleet(rig['config'],rig['store'],service=rig['service'],catalog=c)
    request=QueueRequest(title='Fixture campaign',entries=[{'template_record_id':v['templates'][0]['id'],'experiment_ref':rig['reference']}],
                         repetitions=repetitions,stop_on_failure=stop_on_failure,
                         knowledge_history_note='Test fixture: fixed order; prior agent history is not reset.')
    return fleet,fleet.create(request)


def test_empty_catalog_has_no_clients_or_seeded_data(store):
    def fail(*a):raise AssertionError('No AWS call permitted')
    c=Catalog(Configuration(),store,session_factory=fail)
    assert c.view()['coverage']=='not_collected'
    with pytest.raises(Blocked):c.request()
    c.step();assert not store.entities()


def test_all_template_and_history_pages_are_retained(config,store):
    c,v,r=collect(config,store,Reader(page_count=4))
    assert v['coverage']=='COMPLETE' and len(v['templates'])==4 and len(v['history'])==2
    assert all(row['data']['complete'] for row in v['templates'])
    assert [p.get('nextToken') for op,p in r.calls if op=='templates']==[None,'1','2','3']
    assert not store.operations()
    assert next(r for r in store.records(kind='fis_source') if r['data']['operation']=='get_experiment_template')['data']['request_id']=='test-detail'


def test_discovery_can_resume_across_catalog_instances(config,store):
    cfg=configuration(config);reader=Reader(page_count=3);first=Catalog(cfg,store,session_factory=reader.factory);j=first.request();first.step();first.step()
    second=Catalog(cfg,store,session_factory=reader.factory)
    for _ in range(30):second.step()
    assert store.entity(j['id'])['state']=='COMPLETE'
    assert len(second.view()['templates'])==3
    assert sum(op=='sts' for op,_ in reader.calls)==2


@pytest.mark.parametrize('flag',['wrong_identity','root'])
def test_identity_rejection_precedes_any_fis_read(config,store,flag):
    reader=Reader();setattr(reader,flag,True);c,v,_=collect(config,store,reader)
    assert v['coverage']=='PARTIAL' and not v['templates']
    assert all(op=='sts' for op,_ in reader.calls)


def test_repeated_tokens_and_budgets_do_not_claim_empty_success(config,store):
    r=Reader(page_count=5);r.repeated=True;c,v,_=collect(config,store,r)
    assert v['coverage']=='PARTIAL'
    assert any(s['state']=='ERROR' for s in v['scopes'])


def test_page_budget_is_explicit_partial(config,store):
    cfg=configuration(config).model_copy(update={'fis_discovery_max_pages':1})
    c=Catalog(cfg,store,session_factory=Reader(page_count=3).factory);j=c.request()
    for _ in range(20):c.step()
    assert store.entity(j['id'])['state']=='PARTIAL'
    assert c.view()['scopes'][0]['data']['error_code']=='PageBudgetReached'
    assert len(c.view()['templates'])==1


def test_multi_account_templates_are_discovered_with_target_account_pages(config,store):
    c,v,r=collect(config,store,Reader(multi=True))
    assert v['coverage']=='COMPLETE' and len(v['templates'][0]['data']['target_accounts'])==2
    assert any('Multi-account' in reason for reason in execution_gaps(v['templates'][0]['data']['template']))


def test_denied_template_stays_visible_but_scope_is_partial(config,store):
    r=Reader();r.fail_detail=True;c,v,_=collect(config,store,r)
    assert v['coverage']=='PARTIAL' and not v['templates'][0]['data']['complete']
    assert v['templates'][0]['data']['template_id']=='EXTtest'


def test_cancel_never_issues_an_aws_write(config,store):
    r=Reader();c=Catalog(configuration(config),store,session_factory=r.factory);j=c.request();c.step();c.cancel(j['id']);c.step()
    assert store.entity(j['id'])['state']=='CANCELLED' and not store.operations()


def test_duplicate_or_unknown_connection_selection_is_rejected(config,store):
    c=Catalog(configuration(config),store)
    for ids in [[],['unknown'],['test-discovery','test-discovery']]:
        with pytest.raises(Blocked):c.request(ids)


def test_no_duplicate_account_region_configuration(config_dict):
    config_dict['fis_accounts']=[{'id':'one','name':'a','account_id':ACCOUNT_B,'profile':'one','regions':['eu-central-1']},
                                {'id':'two','name':'b','account_id':ACCOUNT_B,'profile':'two','regions':['eu-central-1']}]
    with pytest.raises(ValueError):Configuration.model_validate(config_dict)


def test_existing_bindings_supply_both_account_scopes(config):
    assert {a.account_id for a in accounts(config)}=={ACCOUNT_A,ACCOUNT_B}


def test_mapping_requires_exact_template_revision_and_native_mode(rig):
    f,campaign=fleet_plan(rig);view=f.library();row=view['templates'][0]
    assert len(row['contracts'])==1
    spec=rig['spec'].model_copy(update={'mode':'assisted'})
    with pytest.raises(Blocked):f.mapping(row['id'],spec)
    changed=rig['config'].model_copy(deep=True);changed.bindings[0].faults[0].template_sha256='b'*64
    with pytest.raises(Blocked):Fleet(changed,rig['store']).mapping(row['id'],rig['spec'])


def test_selector_templates_are_visible_but_not_authorized():
    t=template();t['targets']['Instances'].pop('resourceArns');t['targets']['Instances']['resourceTags']={'Service':'payments'}
    assert any('selector' in r for r in execution_gaps(t))


def test_queue_does_not_start_without_per_trial_approval(rig):
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step();rig['engine'].step()
    tid=rig['store'].entity(q['id'])['data']['active_trial_id']
    assert rig['store'].entity(tid)['state']=='READY'
    f.step();assert not rig['world'].writes
    assert rig['store'].entity(tid)['state']=='READY'


def test_restart_does_not_create_duplicate_child_or_provider_start(rig):
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step();rig['engine'].step()
    tid=rig['store'].entity(q['id'])['data']['active_trial_id']
    # Simulate losing the parent projection after deterministic child registration.
    rig['store'].update(q['id'],changes={'active_trial_id':None})
    new=Fleet(rig['config'],rig['store'],service=rig['service'],catalog=f.catalog);new.step()
    assert rig['store'].entity(q['id'])['data']['active_trial_id']==tid
    assert len(rig['store'].entities('trial'))==1 and not rig['world'].writes


def test_pause_blocks_even_direct_trial_start_atomically(rig):
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step();rig['engine'].step()
    tid=rig['store'].entity(q['id'])['data']['active_trial_id'];approve(rig['service'],tid)
    rig['store'].meta('worker',{'state':'running','heartbeat_at':iso(rig['clock']())})
    f.command(q['id'],'pause')
    with pytest.raises(Blocked):rig['service'].start(tid)
    assert not rig['world'].writes


def test_cancel_before_approval_never_creates_a_cloud_intent(rig):
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step();rig['engine'].step();f.command(q['id'],'cancel')
    f.step();f.step()
    assert rig['store'].entity(q['id'])['state']=='CANCELLED' and not rig['store'].operations()


def test_queue_executes_through_existing_engine_and_retains_a_benchmark(rig):
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step();rig['engine'].step()
    store=rig['store'];tid=store.entity(q['id'])['data']['active_trial_id'];approve(rig['service'],tid)
    store.meta('worker',{'state':'running','heartbeat_at':iso(rig['clock']())});f.step()
    t=store.entity(tid);assert t['state']=='BASELINING'
    probe_samples(store,tid,t['data']['started_at'],30);rig['clock'].advance(30)
    rig['engine'].step();rig['engine'].step();t=store.entity(tid);assert t['state']=='OBSERVING'
    probe_samples(store,tid,t['data']['exposure_at'],120,bad_until=60)
    for _ in range(12):rig['clock'].advance(10);rig['engine'].step()
    for _ in range(5):rig['engine'].step()
    assert store.entity(tid)['state']=='CLOSED'
    f.step();f.step();assert store.entity(q['id'])['state']=='COMPLETE'
    record=benchmark(store,q['id']);body=record['data']
    assert body['groups'][0]['planned']==1 and body['groups'][0]['qualified']==1
    assert body['attempts'][0]['provider_experiment_id']
    assert body['attempts'][0]['diagnosis_outcome']=='not_assessed'
    assert len([x for x in rig['world'].writes if x[2]=='start_experiment'])==1
    assert 'trial_id' in benchmark_csv(record)


def test_planned_attempts_are_not_fabricated_measurements(rig):
    f,q=fleet_plan(rig,repetitions=3);body=benchmark(rig['store'],q['id'])['data']
    assert len(body['attempts'])==3 and body['groups'][0]['qualified']==0
    assert body['groups'][0]['response_pass_fraction'] is None
    assert all(x['state']=='NOT_STARTED' for x in body['attempts'])
    assert all(s['n']==0 and s['median'] is None for s in body['groups'][0]['statistics'].values())


def test_two_agent_bindings_form_separate_groups_not_fake_shared_exposure(rig):
    cfg=rig['config']; other=cfg.bindings[0].model_copy(deep=True);other.id='second-agent';other.agent_space_id='another-space';other.name='Another agent'
    cfg.bindings.append(other)
    second=rig['spec'].model_copy(update={'id':'second-definition','binding_id':other.id})
    ref=rig['service'].register(second)['id'];c,v,_=collect(cfg,rig['store']);f=Fleet(cfg,rig['store'],service=rig['service'],catalog=c)
    row=v['templates'][0]['id'];q=f.create(QueueRequest(title='Two agents',entries=[{'template_record_id':row,'experiment_ref':rig['reference']},{'template_record_id':row,'experiment_ref':ref}],knowledge_history_note='Same measured requirements; sequential replays with shared workload history.'))
    groups=benchmark(rig['store'],q['id'])['data']['groups']
    assert len(groups)==2 and groups[0]['cohort_id']==groups[1]['cohort_id']
    assert groups[0]['agent']!=groups[1]['agent']


def test_changed_requirements_split_comparison_cohorts(rig):
    s=rig['spec'].model_copy(update={'id':'different-deadline','response_deadline_seconds':30})
    ref=rig['service'].register(s)['id'];c,v,_=collect(rig['config'],rig['store']);f=Fleet(rig['config'],rig['store'],service=rig['service'],catalog=c);row=v['templates'][0]['id']
    q=f.create(QueueRequest(title='Different requirements',entries=[{'template_record_id':row,'experiment_ref':rig['reference']},{'template_record_id':row,'experiment_ref':ref}],knowledge_history_note='Different deadlines cannot be pooled into a single response score.'))
    assert len({g['cohort_id'] for g in benchmark(rig['store'],q['id'])['data']['groups']})==2


def test_api_auth_empty_install_and_definition_boundary(store):
    client=TestClient(create_app(Configuration(),store,OP,AP))
    assert client.get('/').status_code==200 and 'FIS experiment library' in client.get('/').text
    assert 'Response & prevention' in client.get('/response').text
    assert client.get('/api/fis/accounts').status_code==401
    headers={'Authorization':'Bearer '+OP}
    assert client.get('/api/fis/accounts',headers=headers).json()['accounts']==[]
    assert client.post('/api/fis/sync',headers=headers,json={}).status_code==409
    assert client.post('/api/fis/sync',headers=headers,json={'profile':'browser-injected'}).status_code==422
    assert client.get('/static/aws.js').status_code==200


def test_real_sdk_fis_read_shapes(config,store):
    # Stubber validates installed botocore operation names, fields and parameters.
    cfg=configuration(config)
    sts=boto3.client('sts',region_name='eu-central-1',aws_access_key_id='testing',aws_secret_access_key='testing')
    fis=boto3.client('fis',region_name='eu-central-1',aws_access_key_id='testing',aws_secret_access_key='testing')
    class Session:
        def client(self,service,**kw):return sts if service=='sts' else fis
    with Stubber(sts) as st, Stubber(fis) as fs:
        st.add_response('get_caller_identity',{'Account':ACCOUNT_B,'Arn':f'arn:aws:iam::{ACCOUNT_B}:role/Reader','UserId':'test'}, {})
        fs.add_response('list_experiment_templates',{'experimentTemplates':[{'id':'EXTtest','description':'test'}]}, {'maxResults':100})
        fs.add_response('get_experiment_template',{'experimentTemplate':template()}, {'id':'EXTtest'})
        fs.add_response('list_experiments',{'experiments':[]}, {'maxResults':100})
        c=Catalog(cfg,store,session_factory=lambda _:Session());j=c.request()
        for _ in range(8):c.step()
        assert store.entity(j['id'])['state']=='COMPLETE'
        st.assert_no_pending_responses();fs.assert_no_pending_responses()


def test_campaign_concurrent_pause_is_not_overwritten(rig, monkeypatch):
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step();rig['engine'].step()
    original=f._advance
    def race(entity):
        f.command(entity['id'],'pause')
        raise Blocked('A concurrent worker failure must not undo the pause')
    monkeypatch.setattr(f,'_advance',race);f.step()
    assert rig['store'].entity(q['id'])['state']=='PAUSED'


def test_only_one_fleet_campaign_can_own_dispatch(rig):
    f,q=fleet_plan(rig)
    body=rig['store'].record(q['data']['plan_id'])['data']
    q2=f.create(QueueRequest(title='Other queue',entries=[{k:e[k] for k in ('template_record_id','experiment_ref')} for e in body['entries']],knowledge_history_note=body['knowledge_history_note']))
    f.command(q['id'],'activate')
    with pytest.raises(Blocked):f.command(q2['id'],'activate')


def test_unresolved_operations_block_queue_progression(rig):
    f,q=fleet_plan(rig);f.command(q['id'],'activate')
    rig['store'].create('change','RESTORE_REQUIRED',{'reason':'test-only unresolved restoration'})
    f.step()
    assert rig['store'].entity(q['id'])['state']=='PAUSED' and not rig['store'].entities('trial')


def test_benchmark_missing_response_is_failure_not_zero_latency(rig):
    # Explicit source fixture: verify aggregation, not an AWS behavior claim.
    f,q=fleet_plan(rig);f.command(q['id'],'activate');f.step()
    store=rig['store'];tid=store.entity(q['id'])['data']['active_trial_id']
    dimensions={k:{'outcome':'pass'} for k in ('challenge','measurement','cleanup','delivery')}
    dimensions['response']={'outcome':'fail'};dimensions['diagnosis']={'outcome':'not_assessed'}
    a=store.put_record('assessment',tid,{'trial_id':tid,'dimensions':dimensions,'metrics':{'completed_probe_requests':120,'incident_to_task_seconds':None},'evaluated_at':iso(),'input_hashes':{}})
    store.update(tid,state='CLOSED',changes={'assessment_id':a['id'],'fault_state':'completed','fault_duration_seconds':60,'started_at':iso()})
    b=benchmark(store,q['id'])['data'];g=b['groups'][0]
    assert g['no_response_failures']==1 and g['response_pass_fraction']==0
    assert g['statistics']['incident_to_task_seconds']['median'] is None


def test_benchmark_checks_actual_exposure_comparability(rig):
    f,q=fleet_plan(rig,repetitions=2);f.command(q['id'],'activate');f.step()
    store=rig['store'];tid=store.entity(q['id'])['data']['active_trial_id'];base=store.entity(tid)
    for index,duration in [(0,60),(1,20)]:
        current=q['id']+'-trial-'+str(index)
        if index:store.create('trial','CLOSED',{**base['data'],'fis_slot':index},current)
        dims={k:{'outcome':'pass'} for k in ('challenge','measurement','cleanup','delivery','response')}
        a=store.put_record('assessment',current,{'trial_id':current,'dimensions':dims,'metrics':{'completed_probe_requests':120,'incident_to_task_seconds':5},'evaluated_at':iso(),'input_hashes':{}})
        store.update(current,state='CLOSED',changes={'assessment_id':a['id'],'fault_state':'completed','fault_duration_seconds':duration,'started_at':iso()})
    b=benchmark(store,q['id'])['data']
    assert b['groups'][0]['qualified']==1 and b['groups'][0]['excluded_or_pending']==1
    assert 'Actual exposure' in b['attempts'][1]['exclusion_reason']


def test_read_failure_in_one_account_does_not_hide_another(config,store):
    from lab.models import FISAccount
    cfg=configuration(config)
    cfg.fis_accounts.append(FISAccount(id='other',name='Test wrong account',account_id=ACCOUNT_A,profile='wrong',regions=['eu-west-1']))
    c=Catalog(cfg,store,session_factory=Reader().factory);j=c.request()
    for _ in range(30):c.step()
    assert store.entity(j['id'])['state']=='PARTIAL'
    assert {s['state'] for s in c.view()['scopes']}=={'COMPLETE','ERROR'}
    assert c.view()['templates'][0]['data']['account_id']==ACCOUNT_B
