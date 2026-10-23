"""Terminal publication and crash recovery; fixtures never access AWS."""
import pytest
from lab.finalization import finalize_trial
from lab.store import Store
from lab.util import Blocked, iso
from conftest import run_trial


def pending(store, *, aborted=False):
    trial=store.create('trial','FINALIZING',{'cleanup_verified':True,'aborted':aborted})
    capture=store.put_record('probe_capture',trial['id'],{'samples':[]})
    state='CLOSED_ABORTED' if aborted else 'CLOSED'
    body={'trial_id':trial['id'],'lifecycle':state,'probe_capture_id':capture['id'],
          'input_hashes':{capture['id']:capture['sha256']}}
    return trial,body,state


@pytest.mark.parametrize('aborted',[False,True])
def test_terminal_state_is_visible_only_with_its_pinned_assessment(store,monkeypatch,aborted):
    trial,body,state=pending(store,aborted=aborted)
    reader=Store(store.directory);event=store._event
    observed=[]
    def inspect_before_commit(db,owner,kind,data):
        event(db,owner,kind,data)
        if kind=='trial.closed':
            observed.append(reader.entity(owner))
            assert reader.records(owner,kind='assessment')==[]
    monkeypatch.setattr(store,'_event',inspect_before_commit)
    result=finalize_trial(store,trial['id'],body,expected_revision=trial['revision'],state=state,closed_at=iso())
    assert observed[0]['state']=='FINALIZING' and 'assessment_id' not in observed[0]['data']
    closed=reader.entity(trial['id'])
    assert closed['state']==state and closed['data']['assessment_id']==result['id']
    assert reader.record(result['id'])['data']==body


def test_failed_commit_rolls_back_result_and_terminal_state(store,monkeypatch):
    trial,body,state=pending(store);event=store._event
    def fail(db,owner,kind,data):
        event(db,owner,kind,data)
        if kind=='trial.closed':raise RuntimeError('Injected precommit failure')
    monkeypatch.setattr(store,'_event',fail)
    with pytest.raises(RuntimeError,match='precommit'):
        finalize_trial(store,trial['id'],body,expected_revision=trial['revision'],state=state,closed_at=iso())
    assert store.entity(trial['id'])==trial and store.records(trial['id'],kind='assessment')==[]
    monkeypatch.setattr(store,'_event',event)
    result=finalize_trial(store,trial['id'],body,expected_revision=trial['revision'],state=state,closed_at=iso())
    assert store.entity(trial['id'])['data']['assessment_id']==result['id']


@pytest.mark.parametrize('change',['revision','capture','cleanup','lifecycle'])
def test_stale_or_invalid_finalization_cannot_close_the_trial(store,change):
    trial,body,state=pending(store)
    if change=='revision':store.update(trial['id'],changes={'concurrent':True})
    if change=='capture':body['probe_capture_id']='nonexistent'
    if change=='cleanup':store.update(trial['id'],changes={'cleanup_verified':False});trial=store.entity(trial['id'])
    if change=='lifecycle':body['lifecycle']='CLOSED_ABORTED'
    with pytest.raises(Blocked):
        finalize_trial(store,trial['id'],body,expected_revision=trial['revision'],state=state,closed_at=iso())
    assert store.entity(trial['id'])['state']=='FINALIZING' and store.records(trial['id'],kind='assessment')==[]


def test_restart_resumes_finalization_without_a_second_provider_start(rig,monkeypatch):
    class Interrupted(BaseException):pass
    original=finalize_trial
    def interrupt(*args,**kwargs):raise Interrupted('Process lost before final commit')
    monkeypatch.setattr('lab.finalization.finalize_trial',interrupt)
    with pytest.raises(Interrupted):run_trial(rig)
    trial=rig['store'].entities('trial')[0]
    assert trial['state']=='FINALIZING' and not trial['data'].get('assessment_id')
    assert sum(w[2]=='start_experiment' for w in rig['world'].writes)==1
    monkeypatch.setattr('lab.finalization.finalize_trial',original)
    from lab.engine import Engine
    recovered=Engine(rig['config'],Store(rig['store'].directory),aws_factory=rig['world'].factory,clock=rig['clock'])
    recovered.step()
    trial=rig['store'].entity(trial['id'])
    assert trial['state']=='CLOSED'
    assert rig['store'].record(trial['data']['assessment_id'])['data']['lifecycle']=='CLOSED'
    assert sum(w[2]=='start_experiment' for w in rig['world'].writes)==1
