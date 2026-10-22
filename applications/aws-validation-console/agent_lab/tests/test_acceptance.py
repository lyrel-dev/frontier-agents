"""Test-only qualification doubles and provenance fixtures. No AWS account access."""
from copy import deepcopy
import json
from datetime import datetime, timezone
import boto3
from botocore.stub import Stubber
import pytest
from conftest import run_trial
from lab.models import Configuration
from lab.preflight import ReadOnlyAWS, run_preflight
from lab.acceptance import audit
from lab.util import Blocked, digest
from acceptance import main, save


class Reader:
    instances = []
    def __init__(self, binding, store, owner):
        self.binding = binding
        self.calls = []
        self.instances.append(self)
    def qualify(self, spec):
        self.calls.append('qualify')
        return {'test_fixture_only': True}
    def safety_lever(self):
        self.calls.append('safety_lever')
        return {'status': 'disengaged'}
    def observe(self, *args):
        self.calls.append('observe')
        return {'complete': True, 'metrics': []}


def test_empty_install_never_constructs_an_aws_client(store):
    def forbidden(*args):
        raise AssertionError('No network allowed')
    report = run_preflight(Configuration(), None, store, read_aws=True, aws_factory=forbidden)['data']
    assert report['status'] == 'blocked' and not report['aws_reads_attempted']
    assert not store.entities() and not store.operations()


def test_offline_plan_does_not_query_profiles(config, spec, store):
    def forbidden(*args):
        raise AssertionError('No network allowed')
    report = run_preflight(config, spec, store, aws_factory=forbidden)['data']
    assert report['status'] == 'blocked' and 'aws_reads' in report['blocking_checks']
    assert report['aws_write_operations'] == 0 and not report['execution_authorized']


def test_probe_requires_explicit_online_opt_in(config, spec, store):
    with pytest.raises(Blocked):
        run_preflight(config, spec, store, probe=True)


def test_readonly_adapter_denies_write_and_write_client(config, store):
    adapter = ReadOnlyAWS(config.bindings[0], store, 'test')
    with pytest.raises(Blocked):
        adapter.write('fault', 'fis', 'start_experiment', {})
    with pytest.raises(Blocked):
        adapter.client('fault', 'fis', write=True)


def test_read_checks_are_not_live_acceptance(config, spec, store):
    result = run_preflight(config, spec, store, read_aws=True, aws_factory=Reader)['data']
    assert result['status'] == 'read_checks_passed'
    assert result['execution_authorized'] is False and not result['trial_created']
    assert set(Reader.instances[-1].calls) == {'qualify', 'observe', 'safety_lever'}
    assert not store.entities() and not store.operations()
    for rid, sha in result['input_hashes'].items():
        assert store.record(rid)['sha256'] == sha


@pytest.mark.parametrize('status', ['engaged', 'engaging', None, 'unknown'])
def test_non_disengaged_safety_lever_blocks(config, spec, store, status):
    class Lever(Reader):
        def safety_lever(self): return {'status': status}
    result = run_preflight(config, spec, store, read_aws=True, aws_factory=Lever)['data']
    assert 'fis_safety_lever' in result['blocking_checks']


def test_failed_identity_or_pin_prevents_further_reads(config, spec, store):
    class Fail(Reader):
        def qualify(self, spec): raise Blocked('Wrong account')
        def observe(self, *args): raise AssertionError('Not allowed after mismatch')
        def safety_lever(self): raise AssertionError('Not allowed after mismatch')
    result = run_preflight(config, spec, store, read_aws=True, aws_factory=Fail)['data']
    assert result['status'] == 'blocked' and 'account_and_instrument_reads' in result['blocking_checks']


@pytest.mark.parametrize('mode', ['absent', 'partial', 'null', 'empty'])
def test_missing_metric_never_becomes_zero_or_pass(config_dict, spec, store, mode):
    config_dict['bindings'][0]['metrics'] = [{'id': 'health', 'title': 'Test-only metric', 'namespace': 'Test',
        'metric_name': 'Error', 'dimensions': {}, 'statistic': 'Sum', 'unit': 'Count', 'period_seconds': 60}]
    config = Configuration.model_validate(config_dict)
    class Missing(Reader):
        def observe(self, *args):
            points = [] if mode == 'empty' else [{'at': '2026-01-01T00:00:00Z', 'value': None if mode == 'null' else 0}]
            return {'complete': True, 'metrics': [] if mode == 'absent' else [
                {'id': 'health', 'complete': mode != 'partial', 'missing': int(mode == 'null'), 'points': points}]}
    result = run_preflight(config, spec, store, read_aws=True, aws_factory=Missing)['data']
    assert 'metric:health' in result['blocking_checks']


def test_exactly_one_probe_only_when_requested(config, spec, store):
    calls = []
    def request(*args):
        calls.append(args)
        return {'attempted': True, 'success': True, 'latency_ms': 1}
    run_preflight(config, spec, store, read_aws=True, aws_factory=Reader, request=request)
    assert not calls
    result = run_preflight(config, spec, store, read_aws=True, probe=True, aws_factory=Reader, request=request)['data']
    assert len(calls) == 1 and result['status'] == 'read_checks_passed'
    assert not store.operations()


def test_assisted_or_missing_native_receipt_is_blocked_before_aws(config_dict, spec, store):
    config_dict['bindings'][0]['route']['receipt_log_group'] = None
    config = Configuration.model_validate(config_dict)
    result = run_preflight(config, spec, store, read_aws=True, aws_factory=Reader)['data']
    assert not result['aws_reads_attempted'] and 'receipt_adapter' in result['blocking_checks']
    spec = spec.model_copy(update={'mode': 'assisted'})
    result = run_preflight(config, spec, store, read_aws=True, aws_factory=Reader)['data']
    assert 'native_mode' in result['blocking_checks']


def test_get_safety_lever_sdk_contract(config, store):
    b = config.bindings[0]
    client = boto3.client('fis', region_name=b.workload.region, aws_access_key_id='test', aws_secret_access_key='test')
    adapter = ReadOnlyAWS(b, store, 'sdk-test')
    adapter.verified['fault'] = {'account': b.workload.account_id}
    adapter.clients[('fault', 'fis', False)] = client
    # Use the adapter's actual cache-key convention without credential resolution.
    adapter.client = lambda side, service, write=False: client
    with Stubber(client) as stub:
        stub.add_response('get_safety_lever', {'safetyLever': {'id': 'default',
            'arn': f'arn:aws:fis:{b.workload.region}:{b.workload.account_id}:safety-lever/default',
            'state': {'status': 'disengaged'}}, 'ResponseMetadata': {'RequestId': 'test-request-id'}}, {'id': 'default'})
        result = adapter.safety_lever()
        stub.assert_no_pending_responses()
    assert result['status'] == 'disengaged'
    source = store.record(result['source'])['data']
    assert source['request_id'] == 'test-request-id' and source['response_sha256'] == digest(source['response'])


def test_fixture_trial_cannot_claim_live_evidence(rig):
    trial = run_trial(rig)
    report = audit(rig['store'], trial['id'])
    assert report['status'] == 'blocked'
    assert 'source_account_scope' in report['blocking_checks']
    assert not report['live_acceptance_certified']


def test_frozen_audit_rejects_hash_mismatch(rig):
    trial = run_trial(rig)
    store = rig['store']
    assessment = deepcopy(store.record(trial['data']['assessment_id'])['data'])
    first = next(iter(assessment['input_hashes']))
    assessment['input_hashes'][first] = '0' * 64
    record = store.put_record('assessment', trial['id'], assessment)
    store.update(trial['id'], changes={'assessment_id': record['id']})
    with pytest.raises(Blocked, match='Pinned input mismatch'):
        audit(store, trial['id'])


def test_audit_retains_failure_instead_of_upgrading_to_pass(rig):
    rig['world'].no_task = True
    trial = run_trial(rig)
    report = audit(rig['store'], trial['id'])
    assert report['response_outcomes']['response'] == 'fail'
    assert report['status'] == 'blocked' and not report['live_acceptance_certified']


def test_audit_does_not_create_assessments_or_mutate_records(rig):
    trial = run_trial(rig)
    before = [r['id'] for r in rig['store'].records()]
    audit(rig['store'], trial['id'])
    assert before == [r['id'] for r in rig['store'].records()]


def test_cli_empty_config_writes_only_a_blocked_report(tmp_path):
    config = tmp_path / 'config.json'
    config.write_text('{"bindings":[],"enable_aws_writes":false}')
    output = tmp_path / 'report.json'
    assert main(['preflight', '--config', str(config), '--data', str(tmp_path / 'workspace'), '--output', str(output)]) == 2
    report = json.loads(output.read_text())
    assert report['status'] == 'blocked' and not report['aws_reads_attempted']
    assert output.stat().st_mode & 0o777 == 0o600


def test_reports_cannot_be_overwritten(tmp_path):
    path = tmp_path / 'report.json'
    save(path, {'status': 'blocked'})
    with pytest.raises(FileExistsError): save(path, {'status': 'reviewable'})
    assert json.loads(path.read_text())['status'] == 'blocked'


def test_audit_missing_workspace_does_not_create_a_database(tmp_path):
    missing = tmp_path / 'nonexistent'
    assert main(['audit', '--data', str(missing), '--trial', 'unknown', '--output', str(tmp_path/'report.json')]) == 2
    assert not missing.exists() and not (tmp_path/'report.json').exists()
