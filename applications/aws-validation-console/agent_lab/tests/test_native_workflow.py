"""Native target execution regressions; all AWS behavior is isolated test code."""
from copy import deepcopy
from datetime import timedelta
from types import SimpleNamespace
import pytest
from conftest import Clock,World,FakeAWS,approve,probe_samples
from test_delivery_components import native_fixture,approval
from lab.native_fis import Previews,account_contract
from lab.models import TrialRequest
from lab.service import Service
from lab.engine import Engine
from lab.util import iso,dt,digest,Blocked

class NativeFake(FakeAWS):
    def write(self,side,service,op,p):
        result=super().write(side,service,op,p)
        if op=='start_experiment':
            v=self.world.experiments[result['experiment']['id']]
            for key in ('roleArn','targets','stopConditions'):
                v[key]=deepcopy(self.world.template.get(key))
            v['actions']=deepcopy(self.world.template['actions'])
            v['experimentOptions']={**self.world.template.get('experimentOptions',{}),'actionsMode':p['experimentOptions']['actionsMode'],'accountTargeting':self.world.targeting}
        return result
    def template(self,fault):
        return {'contract':self.world.template,'source':'fixture-definition','duration_upper_bound_seconds':60}
    def checks(self,ids):
        rows=[]
        for identifier in ids:
            c=next(c for c in self.b.checks if c.id==identifier)
            running=any(v.get('experimentOptions',{}).get('actionsMode')=='run-all' and not v.get('forced_stop') and (self.world.clock()-dt(v['startTime'])).total_seconds()<60 for v in self.world.experiments.values())
            value='stopped' if c.expected=='stopped' and running else 'running'
            r=self.store.put_record('aws',self.owner,{'test_fixture_only':True,'value':value,'account':c.account_id or self.b.workload.account_id})
            rows.append({'id':identifier,'passed':value==c.expected,'actual':value,'expected':c.expected,'source_record_id':r['id']})
        self.store.put_record('verification',self.owner,{'checks':rows,'all_passed':all(x['passed'] for x in rows)})
        return rows
    def experiment(self,identifier):
        v=dict(self.world.experiments[identifier]);elapsed=(self.world.clock()-dt(v['startTime'])).total_seconds()
        preview=v.get('experimentOptions',{}).get('actionsMode')=='skip-all'
        state='stopped' if v.get('forced_stop') else 'completed' if preview or elapsed>=60 else 'running'
        v['state']={'status':state};v['actions']={name:{**deepcopy(action),'state':{'status':'skipped' if preview else 'completed' if state=='completed' else 'running'}} for name,action in self.world.template['actions'].items()}
        if state!='running':v['endTime']=iso(dt(v['startTime'])+timedelta(seconds=1 if preview else 60))
        rows=deepcopy(self.b.faults[0].resolved_targets)
        if self.world.target_mismatch:rows[0]['targetInformation']['arn']+='-unapproved'
        rec=self.store.put_record('aws',self.owner,{'test_fixture_only':True,'experiment':v})
        return {'experiment':v,'resolved_targets':rows,'target_accounts':self.world.accounts,'target_sources':[rec['id']],'source_record_id':rec['id']}


def rig(config,spec,store,multi):
    cfg,row,preview,b=native_fixture(config,store,multi=multi)
    clock=Clock();world=World(clock);world.template=row['data']['template'];world.accounts=account_contract(row['data']['target_accounts']);world.targeting='multi-account' if multi else 'single-account'
    factory=lambda b,s,o:NativeFake(b,s,o,world)
    s=Service(cfg,store,aws_factory=factory,clock=clock);e=Engine(cfg,store,aws_factory=factory,clock=clock)
    ref=s.register(spec)['id'];return cfg,world,clock,s,e,ref


def begin(config,spec,store,multi=False):
    cfg,w,c,s,e,ref=rig(config,spec,store,multi)
    t=s.trial(TrialRequest(experiment_ref=ref));s.qualify(t['id']);e.step();assert store.entity(t['id'])['state']=='READY'
    approve(s,t['id']);store.meta('worker',{'state':'running','heartbeat_at':iso(c())});s.start(t['id'])
    started=store.entity(t['id'])['data']['started_at'];c.value=dt(started);probe_samples(store,t['id'],started,30);c.advance(30);e.step()
    assert store.entity(t['id'])['state']=='EXPOSING'
    return cfg,w,c,s,e,t['id']

@pytest.mark.parametrize('multi',[False,True])
def test_native_preview_then_fault_and_cleanup_without_preentered_task(config,spec,store,multi):
    cfg,w,c,s,e,tid=begin(config,spec,store,multi)
    e.step();t=store.entity(tid);assert t['state']=='OBSERVING'
    starts=[p for _,_,op,p in w.writes if op=='start_experiment']
    assert [p['experimentOptions']['actionsMode'] for p in starts]==['skip-all','run-all']
    assert t['data']['fis_id']!=t['data']['dispatch_preview_id']
    probe_samples(store,tid,t['data']['exposure_at'],120,bad_until=60)
    for _ in range(12):c.advance(10);e.step()
    for _ in range(5):e.step()
    t=store.entity(tid);assert t['state']=='CLOSED'
    result=store.record(t['data']['assessment_id'])['data']
    assert result['dimensions']['challenge']['outcome']=='pass'
    assert result['dimensions']['response']['outcome']=='pass'
    assert result['dimensions']['cleanup']['outcome']=='pass'
    assert len(t['data']['resolved_target_arns'])==(2 if multi else 1)
    assert len([p for _,_,op,p in w.writes if op=='start_experiment'])==2


def test_changed_fresh_preview_stops_before_actual_fault(config,spec,store):
    cfg,w,c,s,e,tid=begin(config,spec,store,True);w.target_mismatch=True;e.step()
    assert all(p['experimentOptions']['actionsMode']=='skip-all' for _,_,op,p in w.writes if op=='start_experiment')
    assert store.entity(tid)['state'] in ('ABORTING','CLEANING','RESTORE_REQUIRED')


def test_new_resource_after_preview_requests_owned_stop(config,spec,store):
    cfg,w,c,s,e,tid=begin(config,spec,store,True);e.step();w.target_mismatch=True;c.advance(10);e.step()
    assert store.entity(tid)['state']=='ABORTING'
    e.step();assert any(op=='stop_experiment' for _,_,op,_ in w.writes)


def test_preview_terminal_invalid_result_closes_instead_of_forever_stopping(config,store):
    cfg,row,p,b=native_fixture(config,store)
    class P:
        def __init__(self,a,r,s,o):self.store,self.owner=s,o;self.b=SimpleNamespace(workload=SimpleNamespace(account_id=a.account_id,region=r),orchestrator=None)
        def identity(self,*a):return {}
        def call(self,*a,**k):return {'experimentTemplate':row['data']['template']},'test'
        def client(self,*a,**k):return self
        def get_safety_lever(self,**k):return {'safetyLever':{'id':'default','state':{'status':'disengaged'}}}
        def write(self,*a):return {'experiment':{'id':'preview-terminal-fixture'}}
        def experiment(self,*a):return {'experiment':{'id':'preview-terminal-fixture','experimentOptions':{'actionsMode':'skip-all'},'state':{'status':'completed'},'actions':{'Stop':{'state':{'status':'skipped'}}}},'resolved_targets':[]}
    jobs=Previews(cfg,store,factory=P)
    job=jobs.request(row['id'],approval(jobs.subject(row['id'])))
    jobs.step();assert store.entity(job['id'])['state']=='BLOCKED'
    assert store.entity(job['id'])['data']['remote_terminal'] is True
    before=len(store.operations());jobs.step();assert len(store.operations())==before

@pytest.mark.parametrize('value,outcome',[(0,'pass'),(2,'fail'),(None,'inconclusive')])
def test_closed_native_trial_scores_independent_business_metric(config,spec,store,value,outcome,monkeypatch):
    from lab.models import Metric,BusinessRequirement
    config.bindings[0].metrics=[Metric(id='reconciled',title='Test-only acknowledged-write reconciliation',namespace='Test/Application',metric_name='ReconciledLoss',statistic='Maximum',unit='Count',period_seconds=60)]
    spec.business_requirements=[BusinessRequirement(id='no-loss',metric_id='reconciled',category='data_correctness',aggregation='maximum',operator='lte',threshold=0,interpretation='Independently reconcile the acknowledged operation population in each interval.')]
    previous=NativeFake.observe
    def observed(self,*args,**kwargs):
        result=previous(self,*args,**kwargs)
        result['metrics']=[{'id':'reconciled','title':'Test-only reconciliation','unit':'Count','period_seconds':60,'complete':value is not None,'missing':1 if value is None else 0,'points':[{'at':result['start'],'value':value}]}]
        return result
    monkeypatch.setattr(NativeFake,'observe',observed)
    cfg,w,c,s,e,tid=begin(config,spec,store)
    e.step();t=store.entity(tid);probe_samples(store,tid,t['data']['exposure_at'],120,bad_until=60)
    for _ in range(12):c.advance(10);e.step()
    for _ in range(5):e.step()
    assessment=store.record(store.entity(tid)['data']['assessment_id'])['data']
    assert assessment['dimensions']['data_correctness']['outcome']==outcome
    assert assessment['metrics']['business_no-loss']==value
    assert assessment['dimensions']['collateral_regression']['outcome']=='not_assessed'


def test_business_metric_preserves_unit_in_runtime_exports_and_dashboard(rig):
    # Export formatting only: test fixture, not an assessment of any AWS workload.
    from lab.metrics import prometheus, dashboard
    from conftest import run_trial
    store=rig['store'];trial=run_trial(rig)
    previous=store.record(trial['data']['assessment_id'])['data']
    body=deepcopy(previous)
    body['business_checks']=[{'id':'no-loss','category':'data_correctness','observed':0}]
    body['metrics']['business_no-loss']=0
    body['metric_definitions']={'business_no-loss':{'title':'Acknowledged write loss · maximum','unit':'Count'}}
    rec=store.put_record('assessment',trial['id'],body)
    store.update(trial['id'],changes={'assessment_id':rec['id']})
    text=prometheus(store)
    assert 'requirement="no-loss",category="data_correctness",unit="Count"} 0.0' in text
    panels=[p for p in dashboard(store)['panels'] if p['type']=='timeseries']
    assert len(panels)==13
    assert panels[-1]['title']=='Acknowledged write loss · maximum [Count]'
    assert 'requirement="no-loss"' in panels[-1]['targets'][0]['expr']
    body['business_checks'][0]['observed']=None
    rec=store.put_record('assessment',trial['id'],body);store.update(trial['id'],changes={'assessment_id':rec['id']})
    assert not any(x.startswith('agent_validation_business_value{') for x in prometheus(store).splitlines())


@pytest.mark.parametrize('replay_value,expected',[(2,'fail'),(None,'inconclusive')])
def test_prevention_cannot_pass_when_business_check_fails_or_is_missing(rig,monkeypatch,replay_value,expected):
    from lab.models import Experiment,Metric,BusinessRequirement,CampaignRequest,ChangeProposal
    from lab.evaluation import compare_campaign
    from conftest import run_trial
    s,e,store=rig['service'],rig['engine'],rig['store']
    binding=rig['config'].bindings[0]
    binding.metrics=[Metric(id='reconciled',title='Test reconciliation',namespace='Test/Application',metric_name='Loss',statistic='Maximum',unit='Count',period_seconds=60)]
    spec=Experiment.model_validate(store.record(rig['reference'])['data']);spec.revision+=1
    spec.business_requirements=[BusinessRequirement(id='no-loss',metric_id='reconciled',category='data_correctness',aggregation='maximum',operator='lte',threshold=0,interpretation='Independent reconciliation of acknowledged business operations.')]
    rig['reference']=s.register(spec)['id']
    previous=FakeAWS.observe
    def observation(self,*args,**kwargs):
        result=previous(self,*args,**kwargs)
        value=replay_value if self.store.entity(self.owner)['data']['arm']=='treatment' else 0
        result['metrics']=[{'id':'reconciled','complete':value is not None,'missing':1 if value is None else 0,'points':[{'at':result['start'],'value':value}]}]
        return result
    monkeypatch.setattr(FakeAWS,'observe',observation)
    campaign=s.campaign(CampaignRequest(title='Test-only paired business requirement',experiment_ref=rig['reference'],comparison={'claim':'prevent_recurrence','knowledge_history_note':'This is isolated software-test data; no AWS efficacy claim.'}))
    run_trial(rig,campaign['id'])
    approve(s,campaign['id'],'evaluation');e.step();e.step()
    recommendation=store.entity(campaign['id'])['data']['recommendation_ids'][0]
    s.pin_recommendation(campaign['id'],recommendation)
    change=s.propose_change(campaign['id'],ChangeProposal(runbook_id='capacity-change',source_record_id=recommendation,source_quote='Increase serving capacity',rationale='Exact fixture runbook maps the captured recommendation to the reviewed change.',proposer='Test'))
    rig['clock'].advance(1);approve(s,change['id'],'change');e.step();e.step()
    rig['clock'].advance(10);replay=run_trial(rig,campaign['id'],'treatment',bad_until=0)
    measurement=store.record(replay['data']['assessment_id'])['data']
    assert measurement['metrics']['failed_probe_requests']==0
    comparison=compare_campaign(store,campaign['id'],binding)['data']
    assert comparison['outcome']==expected
