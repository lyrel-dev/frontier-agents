"""Preview cancellation/dispatch interleavings; isolated providers only."""
from copy import deepcopy
from types import SimpleNamespace
import pytest
from conftest import Clock
from test_delivery_components import native_fixture, approval
from lab.native_fis import Previews
from lab.preview_control import cancel, reserve_dispatch
from lab.util import Blocked, digest, dt, iso


class Driver:
    def __init__(self,a,r,s,o,world):
        self.store,self.owner,self.world=s,o,world
        self.b=SimpleNamespace(workload=SimpleNamespace(account_id=a.account_id,region=r),orchestrator=None)
    def identity(self,*args):return {}
    def call(self,*args,**kwargs):return {'experimentTemplate':self.world['template']},'fixture'
    def client(self,*args,**kwargs):return self
    def get_safety_lever(self,**kwargs):
        if self.world.get('cancel_at_guard'):cancel(self.store,self.owner)
        return {'safetyLever':{'id':'default','state':{'status':'disengaged'}}}
    def write(self,side,service,operation,parameters):
        self.world['writes'].append((operation,parameters))
        if operation=='stop_experiment':self.world['status']='stopped'
        if operation=='start_experiment' and self.world.get('cancel_after_reservation'):cancel(self.store,self.owner)
        return {'experiment':{'id':'EXP-preview-fixture'}}
    def experiment(self,identifier):
        t=deepcopy(self.world['template']);t.update(id=identifier,experimentTemplateId=t['id'],state={'status':self.world['status']})
        t['experimentOptions']={**t.get('experimentOptions',{}),'actionsMode':self.world.get('mode','skip-all')}
        for a in t['actions'].values():a['state']={'status':'skipped'}
        return {'experiment':t,'resolved_targets':self.world['targets'],'target_accounts':[]}


def fixture(config,store):
    cfg,row,preview,_=native_fixture(config,store)
    world={'template':row['data']['template'],'targets':preview['data']['targets'],'writes':[],'status':'running'}
    clock=Clock();factory=lambda a,r,s,o:Driver(a,r,s,o,world)
    jobs=Previews(cfg,store,factory=factory,clock=clock)
    job=jobs.request(row['id'],approval(jobs.subject(row['id'])))
    request={'side':'fault','service':'fis','operation':'start_experiment','parameters':{
        'experimentTemplateId':row['data']['template_id'],'experimentOptions':{'actionsMode':'skip-all'}}}
    return cfg,jobs,job,clock,world,request


def test_cancel_during_safety_read_cannot_dispatch(config,store):
    cfg,jobs,job,c,w,req=fixture(config,store);w['cancel_at_guard']=True
    jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED'
    assert w['writes']==[]
    assert store.operation(job['id'],'target-preview')['state']=='FAILED'


@pytest.mark.parametrize('pending',[False,True])
def test_cancel_and_stale_worker_snapshot_do_not_restart(config,store,pending):
    cfg,jobs,job,c,w,req=fixture(config,store)
    if pending:store.intent(job['id'],'target-preview',req)
    cancel(store,job['id']);jobs.advance(job)
    assert store.entity(job['id'])['state']=='BLOCKED' and w['writes']==[]
    if pending:assert store.operation(job['id'],'target-preview')['state']=='FAILED'


@pytest.mark.parametrize('pending',[False,True])
def test_exact_expiry_time_is_expired(config,store,pending):
    cfg,jobs,job,c,w,req=fixture(config,store)
    if pending:store.intent(job['id'],'target-preview',req)
    c.value=dt(job['data']['expires_at']);jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED' and w['writes']==[]


def test_approval_expiring_during_safety_read_is_checked_at_reservation(config,store,monkeypatch):
    cfg,jobs,job,c,w,req=fixture(config,store)
    original=Driver.get_safety_lever
    def expires(self,**kwargs):
        value=original(self,**kwargs);c.value=dt(job['data']['expires_at']);return value
    monkeypatch.setattr(Driver,'get_safety_lever',expires)
    jobs.step()
    assert w['writes']==[] and store.entity(job['id'])['state']=='BLOCKED'


def test_cancel_after_reservation_requests_stop_not_false_pre_dispatch_success(config,store):
    cfg,jobs,job,c,w,req=fixture(config,store);w['cancel_after_reservation']=True
    jobs.step();assert [op for op,_ in w['writes']]==['start_experiment','stop_experiment']
    assert store.entity(job['id'])['state']=='STOPPING'
    jobs.step();assert store.entity(job['id'])['state']=='BLOCKED'
    assert not store.records(owner=job['id'],kind='fis_preview_result')
    assert len([op for op,_ in w['writes'] if op=='start_experiment'])==1


def test_stop_requested_then_natural_completion_is_not_promoted(config,store):
    cfg,jobs,job,c,w,req=fixture(config,store);jobs.step()
    store.update(job['id'],state='STOPPING',changes={'reason':'Previous verification failed'})
    w['status']='completed';jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED'
    assert not store.records(owner=job['id'],kind='fis_preview_result')


def test_confirmed_provider_survives_local_attachment_failure(config,store,monkeypatch):
    cfg,jobs,job,c,w,req=fixture(config,store)
    original=store.update;once=[False]
    def failure(identifier,**kwargs):
        if identifier==job['id'] and kwargs.get('state')=='RUNNING' and not once[0]:
            once[0]=True;raise RuntimeError('Injected local attachment interruption')
        return original(identifier,**kwargs)
    monkeypatch.setattr(store,'update',failure)
    jobs.step();latest=store.entity(job['id'])
    assert latest['state']=='STOPPING' and latest['data']['provider_id']=='EXP-preview-fixture'
    assert latest['data']['started_at']==store.operation(job['id'],'target-preview')['created_at']
    jobs.step();jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED'
    assert [op for op,_ in w['writes']]==['start_experiment','stop_experiment']


def test_disabled_new_writes_do_not_prevent_stopping_known_preview(config,store):
    cfg,jobs,job,c,w,req=fixture(config,store);jobs.step()
    cfg.enable_aws_writes=False;cancel(store,job['id']);jobs.step();jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED'
    assert [op for op,_ in w['writes']]==['start_experiment','stop_experiment']


def test_unexpected_live_actions_mode_stops_owned_preview(config,store):
    cfg,jobs,job,c,w,req=fixture(config,store);w['mode']='run-all'
    jobs.step();assert [op for op,_ in w['writes']]==['start_experiment','stop_experiment']
    jobs.step();assert store.entity(job['id'])['state']=='BLOCKED'
    assert not store.records(owner=job['id'],kind='fis_preview_result')


@pytest.mark.parametrize('mutation',['request','mode','owner','subject'])
def test_reservation_rejects_invalid_authority(config,store,mutation):
    cfg,jobs,job,c,w,req=fixture(config,store)
    if mutation=='mode':req['parameters']['experimentOptions']['actionsMode']='run-all'
    op=store.intent(job['id'],'target-preview',req)
    if mutation=='request':op['request']['parameters']['experimentTemplateId']='unapproved'
    if mutation=='owner':store.update(job['id'],state='STOPPING')
    if mutation=='subject':store.update(job['id'],changes={'digest':'0'*64})
    with pytest.raises(Blocked):reserve_dispatch(store,op,c)
    assert store.operation(job['id'],'target-preview')['state']=='PENDING'


def test_reservation_and_cancel_remain_durable_with_independent_store(config,store):
    from lab.store import Store
    cfg,jobs,job,c,w,req=fixture(config,store);op=store.intent(job['id'],'target-preview',req)
    reserve_dispatch(store,op,c)
    second=Store(store.directory);cancel(second,job['id'])
    assert second.operation(job['id'],'target-preview')['state']=='DISPATCHING'
    assert second.entity(job['id'])['data']['abort_requested']
    assert any(e['type']=='operation.dispatching' for e in second.events(job['id']))


def test_preview_cancel_endpoint_is_authenticated_and_atomic(config,store):
    from fastapi.testclient import TestClient
    from lab.api import create_app
    from test_delivery_components import OP,AP
    cfg,jobs,job,c,w,req=fixture(config,store);store.intent(job['id'],'target-preview',req)
    client=TestClient(create_app(cfg,store,OP,AP));path='/api/setup/previews/'+job['id']+'/cancel'
    assert client.post(path).status_code==401
    response=client.post(path,headers={'Authorization':'Bearer '+OP})
    assert response.status_code==200 and response.json()['state']=='BLOCKED'
    assert store.operation(job['id'],'target-preview')['state']=='FAILED'


def test_cancel_during_terminal_verification_cannot_publish_success(config,store,monkeypatch):
    from lab import execution_contract
    cfg,jobs,job,c,w,req=fixture(config,store);w['status']='completed'
    original=execution_contract.verify_execution
    def concurrent_cancel(*args,**kwargs):
        original(*args,**kwargs);cancel(store,job['id'])
    monkeypatch.setattr(execution_contract,'verify_execution',concurrent_cancel)
    jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED'
    assert not store.records(owner=job['id'],kind='fis_preview_result')


def test_preview_publication_failure_rolls_back_result_and_terminal_state(config,store,monkeypatch):
    cfg,jobs,job,c,w,req=fixture(config,store);w['status']='completed'
    original=store._event
    def failed_event(db,owner,event,data):
        if event=='preview.completed':raise RuntimeError('Injected transaction failure')
        return original(db,owner,event,data)
    monkeypatch.setattr(store,'_event',failed_event)
    jobs.step()
    assert store.entity(job['id'])['state']=='BLOCKED'
    assert not store.records(owner=job['id'],kind='fis_preview_result')
