"""Runtime safeguards. AWS calls use SDK stubs; no account is accessed."""
from __future__ import annotations

from threading import Event
import time

import boto3
from botocore.stub import Stubber
import pytest

from lab.aws import AWS
from lab.fis_safety import read_safety_lever
from lab.broker import Broker
from lab.util import Blocked, UnknownRemoteState
from lab.worker import Worker
from conftest import TrialRequest, approve, probe_samples


def broker(rig, owner='guard-test'):
    adapter = rig['world'].factory(rig['config'].bindings[0], rig['store'], owner)
    return Broker(rig['store'], adapter, True), adapter


def start(b):
    return b.execute('guard-test', 'start', 'fault', 'fis', 'start_experiment',
                     {'experimentTemplateId': 'EXTtest'})


@pytest.mark.parametrize('state', ['engaged', 'engaging', 'unknown', None])
def test_blocked_lever_does_not_create_a_dispatch_intent(rig, state):
    rig['world'].safety_status = state
    b, _ = broker(rig)
    with pytest.raises(Blocked, match='not disengaged|could not be verified'):
        start(b)
    assert not rig['world'].writes
    assert rig['store'].operation('guard-test', 'start') is None
    assert rig['store'].records('guard-test', 'execution_guard')[-1]['data']['allowed'] is False


def test_unreadable_lever_is_not_an_implicit_permission(rig):
    b, adapter = broker(rig)
    def denied(**kwargs):
        raise RuntimeError('sensitive SDK exception text must not escape')
    adapter.get_safety_lever = denied
    with pytest.raises(Blocked, match='could not be verified') as exc:
        start(b)
    assert 'sensitive' not in str(exc.value)
    assert not rig['world'].writes
    assert rig['store'].operations() == []
    record = rig['store'].records('guard-test', 'execution_guard')[-1]['data']
    assert record['error_code'] == 'RuntimeError'
    assert 'sensitive' not in str(record)


def test_disengaged_lever_is_captured_and_start_occurs_once(rig):
    b, _ = broker(rig)
    initial = start(b)
    rig['world'].safety_status = 'engaged'
    assert start(b)['provider_id'] == initial['provider_id']
    assert len(rig['world'].writes) == 1
    guard = rig['store'].records('guard-test', 'execution_guard')
    assert len(guard) == 1 and guard[0]['data']['allowed'] is True
    assert rig['store'].record(guard[0]['data']['source_record_id'])['kind'] == 'aws'


def test_unknown_start_is_reconciled_even_when_lever_engages(rig):
    b, adapter = broker(rig)
    rig['world'].fail_write = True
    with pytest.raises(UnknownRemoteState):
        start(b)
    adapter.get_safety_lever = lambda **kwargs: pytest.fail('Reconciliation must not query the start gate')
    assert start(b)['state'] == 'CONFIRMED'
    assert len(rig['world'].writes) == 1


def test_stop_is_not_blocked_by_start_guard(rig):
    b, adapter = broker(rig)
    identifier = start(b)['provider_id']
    adapter.get_safety_lever = lambda **kwargs: pytest.fail('A safety stop cannot depend on a start guard')
    result = b.execute('guard-test', 'stop', 'fault', 'fis', 'stop_experiment', {'id': identifier})
    assert result['state'] == 'CONFIRMED'
    assert rig['world'].writes[-1][2] == 'stop_experiment'


def test_guard_is_checked_after_approval_not_just_onboarding(rig):
    s, e, store, clock = rig['service'], rig['engine'], rig['store'], rig['clock']
    t = s.trial(TrialRequest(experiment_ref=rig['reference']))
    s.qualify(t['id']); e.step(); approve(s, t['id'])
    from lab.util import iso
    store.meta('worker', {'state': 'running', 'heartbeat_at': iso(clock())})
    s.start(t['id']); probe_samples(store, t['id'], iso(clock()), 30)
    clock.advance(30); e.step()
    assert store.entity(t['id'])['state'] == 'EXPOSING'
    rig['world'].safety_status = 'engaged'
    e.step()
    assert store.entity(t['id'])['state'] == 'CLOSED_BLOCKED'
    assert rig['world'].writes == []


def test_safety_lever_read_uses_verified_workload_scope(config, store):
    aws = AWS(config.bindings[0], store, 'sdk-guard')
    client = boto3.client('fis', region_name='eu-central-1',
                         aws_access_key_id='TESTONLY', aws_secret_access_key='TESTONLY')
    sides = []
    aws.identity = lambda side: sides.append(side)
    aws.client = lambda side, service, write=False: client
    with Stubber(client) as stub:
        stub.add_response('get_safety_lever', {
            'safetyLever': {'id': 'default', 'state': {'status': 'disengaged'}},
            'ResponseMetadata': {'RequestId': 'test-request-id'}}, {'id': 'default'})
        result = read_safety_lever(aws)
        stub.assert_no_pending_responses()
    evidence = store.record(result['source'])['data']
    assert sides == ['fault']
    assert evidence['account_id'] == config.bindings[0].workload.account_id
    assert evidence['region'] == config.bindings[0].workload.region
    assert evidence['operation'] == 'get_safety_lever'
    assert evidence['request_id'] == 'test-request-id'


@pytest.mark.parametrize('lever', [
    {'id': 'other', 'state': {'status': 'disengaged'}},
    {'id': 'default', 'state': {}},
    {'id': 'default', 'state': {'status': 'unexpected'}}])
def test_malformed_safety_response_is_rejected(config, store, lever):
    aws = AWS(config.bindings[0], store, 'bad-guard')
    aws.identity = lambda side: None
    from types import SimpleNamespace
    aws.client = lambda *args, **kwargs: SimpleNamespace(get_safety_lever=lambda **params: {'safetyLever': lever})
    with pytest.raises(Blocked):
        read_safety_lever(aws)


class IdleEngine:
    def step(self):
        pass


def test_background_start_acquires_before_returning_and_rejects_duplicate(config, store):
    first = Worker(config, store, engine=IdleEngine())
    thread = first.start_background()
    try:
        assert first.owner is not None and thread.is_alive()
        assert store.meta('worker')['state'] == 'running'
        with pytest.raises(RuntimeError, match='already owns'):
            Worker(config, store, engine=IdleEngine()).start_background()
        assert thread.is_alive()
        with pytest.raises(RuntimeError, match='twice'):
            first.start_background()
    finally:
        first.stop(); thread.join(5)
    assert not thread.is_alive() and first.owner is None
    assert store.meta('worker')['state'] == 'stopped'


def test_engine_failure_is_recorded_and_releases_ownership(config, store):
    fail = Event()
    class FailingEngine:
        def step(self):
            if not fail.wait(2):
                raise AssertionError('Test did not signal failure')
            raise RuntimeError('test failure')
    worker = Worker(config, store, engine=FailingEngine())
    thread = worker.start_background()
    fail.set(); thread.join(5)
    assert not thread.is_alive() and worker.failure == 'RuntimeError'
    assert store.meta('worker')['state'] == 'failed'
    replacement = Worker(config, store, engine=IdleEngine())
    replacement.acquire(); replacement.release()


def test_probe_scheduler_failure_stops_worker(config, store):
    fail = Event()
    worker = Worker(config, store, engine=IdleEngine())
    def broken_probe():
        fail.wait(2)
        raise ValueError('test scheduling error')
    worker._probes = broken_probe
    thread = worker.start_background()
    fail.set(); thread.join(5)
    assert not thread.is_alive()
    assert store.meta('worker')['state'] == 'failed'


def test_shutdown_retains_lock_until_probe_drain_finishes(config, store):
    draining = Event(); release = Event()
    worker = Worker(config, store, engine=IdleEngine())
    def held_probe():
        worker.stop_event.wait(3)
        draining.set()
        release.wait(5)
    worker._probes = held_probe
    thread = worker.start_background()
    try:
        worker.stop()
        assert draining.wait(3)
        with pytest.raises(RuntimeError, match='already owns'):
            Worker(config, store, engine=IdleEngine()).start_background()
    finally:
        release.set(); thread.join(5)
    assert not thread.is_alive()
    replacement = Worker(config, store, engine=IdleEngine())
    replacement.acquire(); replacement.release()


def prepare_main(monkeypatch, tmp_path):
    import run
    cfg = tmp_path / 'empty.json'; cfg.write_text('{"bindings":[]}')
    monkeypatch.setattr('sys.argv', ['run.py', '--with-worker', '--config', str(cfg), '--data', str(tmp_path/'data')])
    monkeypatch.setenv('LAB_OPERATOR_TOKEN', 'operator-only-test-token-123456789')
    monkeypatch.setenv('LAB_APPROVAL_TOKEN', 'approver-only-test-token-123456789')
    return run


def test_combined_process_never_serves_when_workspace_is_owned(monkeypatch, tmp_path):
    from lab.store import Store
    from lab.models import Configuration
    run = prepare_main(monkeypatch, tmp_path)
    owner = Worker(Configuration(), Store(tmp_path/'data'), engine=IdleEngine())
    owner.acquire()
    class Server:
        def __init__(self, *args, **kwargs):
            pass
        def run(self):
            pytest.fail('HTTP must not start after worker lock failure')
    monkeypatch.setattr(run.uvicorn, 'Server', Server)
    try:
        with pytest.raises(RuntimeError, match='already owns'):
            run.main()
    finally:
        owner.release()


def test_combined_process_stops_http_and_exits_nonzero_on_worker_failure(monkeypatch, tmp_path):
    from lab.engine import Engine
    from lab.store import Store
    run = prepare_main(monkeypatch, tmp_path)
    serving = Event()
    def fail(self):
        assert serving.wait(5)
        raise RuntimeError('test engine failure')
    monkeypatch.setattr(Engine, 'step', fail)
    class Server:
        def __init__(self, *args, **kwargs):
            self.should_exit = False
        def run(self):
            serving.set()
            deadline = time.monotonic() + 5
            while not self.should_exit and time.monotonic() < deadline:
                time.sleep(.01)
            assert self.should_exit
    monkeypatch.setattr(run.uvicorn, 'Server', Server)
    with pytest.raises(SystemExit) as exc:
        run.main()
    assert exc.value.code == 1
    assert Store(tmp_path/'data').meta('worker')['state'] == 'failed'


def test_combined_process_drains_worker_on_normal_http_shutdown(monkeypatch, tmp_path):
    from lab.store import Store
    run = prepare_main(monkeypatch, tmp_path)
    class Server:
        def __init__(self, *args, **kwargs):
            pass
        def run(self):
            pass
    monkeypatch.setattr(run.uvicorn, 'Server', Server)
    run.main()
    assert Store(tmp_path/'data').meta('worker')['state'] == 'stopped'
