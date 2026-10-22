"""Publication blockers reproduced with isolated fixtures; no AWS access."""
from copy import deepcopy
from datetime import timedelta
from types import SimpleNamespace
import boto3
from botocore.stub import Stubber
import pytest
from conftest import Clock, run_trial
from test_delivery_components import native_fixture, approval, setup_service
from test_native_workflow import begin, NativeFake
from lab.setup import ConfigDraft
from lab.native_fis import Previews, PreviewAWS
from lab.execution_contract import verify_execution, execution_projection
from lab.acceptance import audit
from lab.util import Blocked, digest, iso


def proposal(config, store):
    s = setup_service(config, store)
    r = s.draft(ConfigDraft(configuration=config, base_digest=digest(config.model_dump(mode='json')),
                            rationale='Test-only approval for a local configuration edit.'))
    return s, r


def test_stopping_preview_cannot_lose_its_configuration(config, store):
    s, r = proposal(config, store)
    store.create('fis_preview', 'STOPPING', {'provider_id': 'test-only-preview'})
    with pytest.raises(Blocked, match='active'):
        s.commit(r['id'], approval(s.subject(r['id'])))
    assert store.meta('active_configuration') is None


@pytest.mark.parametrize('state', ['PENDING', 'DISPATCHING', 'UNKNOWN'])
def test_unsettled_intent_blocks_configuration_even_if_owner_state_is_stale(config, store, state):
    s, r = proposal(config, store)
    op = store.intent('test-stale-owner', 'target-preview', {'operation': 'test-only'})
    store.operation_state(op, state)
    with pytest.raises(Blocked, match='provider operations'):
        s.commit(r['id'], approval(s.subject(r['id'])))
    assert store.meta('active_configuration') is None


def waiting_preview(config, store):
    cfg, row, _, binding = native_fixture(config, store)
    clock = Clock()
    class IdentityOnly:
        def __init__(self, *args): pass
        def identity(self, side): return {'account': binding.workload.account_id}
        def call(self, *args, **kw): raise AssertionError('No extra AWS read or write is authorized')
        def write(self, *args, **kw): raise AssertionError('No remote start is authorized')
    previews = Previews(cfg, store, factory=IdentityOnly, clock=clock)
    job = previews.request(row['id'], approval(previews.subject(row['id'])))
    op = store.intent(job['id'], 'target-preview', {'side':'fault','service':'fis','operation':'start_experiment',
         'parameters':{'experimentTemplateId':row['data']['template_id'],'experimentOptions':{'actionsMode':'skip-all'}}})
    return previews, job, op, clock


def test_pending_preview_rechecks_approval_expiry(config, store):
    previews, job, op, clock = waiting_preview(config, store)
    clock.advance(1000)
    previews.step()
    assert store.entity(job['id'])['state'] == 'BLOCKED'
    assert 'expired' in store.entity(job['id'])['data']['reason']
    assert store.operation(job['id'], 'target-preview')['state'] == 'FAILED'
    assert not store.operation(job['id'], 'target-preview')['provider_id']


def test_cancel_pending_preview_does_not_send_a_start(config, store):
    previews, job, op, clock = waiting_preview(config, store)
    store.update(job['id'], changes={'abort_requested': True})
    previews.step()
    assert store.entity(job['id'])['state'] == 'BLOCKED'
    assert store.operation(job['id'], 'target-preview')['response']['code'] == 'CancelledBeforeDispatch'


def test_snapshot_projection_ignores_only_runtime_fields(config, store):
    _, row, _, _ = native_fixture(config, store)
    t = row['data']['template']
    e = {**deepcopy(t), 'id':'test-experiment', 'experimentTemplateId':t['id'],
         'experimentOptions':{**t.get('experimentOptions',{}), 'actionsMode':'run-all'}}
    e['actions']['Stop'].update(state={'status':'completed'}, startTime=iso(), endTime=iso(), description='runtime text')
    assert verify_execution(t, e, 'run-all') == digest(execution_projection(t))


@pytest.mark.parametrize('mutation', ['role', 'target', 'parameter', 'action', 'dependency', 'stop', 'mode', 'template'])
def test_execution_snapshot_drift_is_rejected(config, store, mutation):
    _, row, _, _ = native_fixture(config, store)
    t = row['data']['template']
    e = {**deepcopy(t), 'id':'test-experiment', 'experimentTemplateId':t['id'],
         'experimentOptions':{**t.get('experimentOptions',{}), 'actionsMode':'run-all'}}
    if mutation=='role': e['roleArn'] += '-changed'
    if mutation=='target': e['targets']['Instances']['selectionMode']='COUNT(1)'
    if mutation=='parameter': e['actions']['Stop']['parameters']['startInstancesAfterDuration']='PT5M'
    if mutation=='action': e['actions']['Stop']['actionId']='aws:ec2:terminate-instances'
    if mutation=='dependency': e['actions']['Stop']['startAfter']=['Unapproved']
    if mutation=='stop': e['stopConditions']=[]
    if mutation=='mode': e['experimentOptions']['actionsMode']='skip-all'
    if mutation=='template': e['experimentTemplateId']='different-template'
    with pytest.raises(Blocked): verify_execution(t, e, 'run-all')


@pytest.mark.parametrize('multi', [False, True])
def test_runtime_definition_drift_requests_owned_restoration(config, spec, store, monkeypatch, multi):
    previous = NativeFake.experiment
    def changed(self, identifier):
        result = previous(self, identifier)
        if result['experiment']['experimentOptions']['actionsMode']=='run-all':
            result['experiment']['roleArn'] += '-unapproved'
        return result
    monkeypatch.setattr(NativeFake, 'experiment', changed)
    cfg, world, clock, svc, engine, tid = begin(config, spec, store, multi)
    engine.step()
    assert store.entity(tid)['state']=='ABORTING'
    assert store.entity(tid)['data']['fis_id']
    engine.step()
    assert any(operation=='stop_experiment' for _,_,operation,_ in world.writes)
    assert len([x for x in world.writes if x[2]=='start_experiment'])==2


def test_preview_reads_actual_experiment_account_roles_via_sdk(config, store):
    cfg, row, _, _ = native_fixture(config, store, multi=True)
    account = cfg.fis_accounts[0]
    session = boto3.Session(aws_access_key_id='TESTONLY', aws_secret_access_key='TESTONLY', region_name='eu-central-1')
    client = session.client('fis')
    a = PreviewAWS(account, 'eu-central-1', store, 'sdk-preview', factory=lambda **kw:session)
    a.clients[('fis',False)] = client
    with Stubber(client) as stub:
        stub.add_response('get_experiment', {'experiment':{'id':'test-preview','experimentOptions':{'accountTargeting':'multi-account','actionsMode':'skip-all'}}}, {'id':'test-preview'})
        stub.add_response('list_experiment_resolved_targets', {'resolvedTargets':[]}, {'experimentId':'test-preview','maxResults':100})
        stub.add_response('list_experiment_target_account_configurations', {'targetAccountConfigurations':row['data']['target_accounts']}, {'experimentId':'test-preview'})
        observed = a.experiment('test-preview')
        assert observed['target_accounts']==row['data']['target_accounts']
        assert len(observed['account_sources'])==1
        stub.assert_no_pending_responses()


def test_confirmed_no_response_is_auditable_without_fabricating_diagnosis(rig):
    rig['world'].no_task = True
    trial = run_trial(rig)
    report = audit(rig['store'], trial['id'])
    assert report['confirmed_no_response'] is True
    assert report['response_outcomes']['response']=='fail'
    assert report['response_outcomes']['diagnosis']=='not_assessed'
    assert 'diagnosis' not in report['blocking_checks']
    # The fixture does not contain authentic AWS metadata; overall remains blocked.
    assert 'source_account_scope' in report['blocking_checks']
    assert not report['live_acceptance_certified']


def test_absent_delivery_cannot_use_no_response_audit_exception(rig):
    rig['world'].no_task = True
    rig['world'].no_receipt = True
    trial = run_trial(rig)
    report = audit(rig['store'], trial['id'])
    assert report['confirmed_no_response'] is False
    assert 'diagnosis' in report['blocking_checks']
    assert 'delivery' in report['blocking_checks']
