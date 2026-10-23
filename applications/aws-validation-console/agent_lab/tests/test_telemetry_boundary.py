"""Security and metric identity checks. All provider evidence is test-only."""
from copy import deepcopy
from datetime import timedelta

from fastapi.testclient import TestClient
import pytest

from conftest import run_trial
from lab.api import create_app
from lab.hosting import allowed_hosts, metrics_secret
from lab.metrics import prometheus, dashboard
from lab.models import Configuration
from lab.util import Blocked, iso, utcnow

OP = 'test-operator-token-for-http-123456'
AP = 'test-approval-token-for-http-123456'
MP = 'test-metrics-readonly-token-123456'


def client(store):
    return TestClient(create_app(Configuration(), store, OP, AP, metrics_token=MP))


def test_scrape_token_has_no_workspace_or_write_authority(store):
    c = client(store)
    headers = {'Authorization': 'Bearer ' + MP}
    response = c.get('/api/metrics', headers=headers)
    assert response.status_code == 200
    assert 'version=0.0.4' in response.headers['content-type']
    assert response.headers['cache-control'] == 'no-store'
    for path in ('/api/workspace', '/api/config', '/api/setup', '/api/backup', '/api/grafana'):
        assert c.get(path, headers=headers).status_code == 403
    for path in ('/api/metrics', '/api/fis/sync', '/api/setup/accounts', '/api/setup/approve/config/absent'):
        assert c.post(path, headers=headers, json={}).status_code == 403
    assert c.head('/api/metrics', headers=headers).status_code == 403
    assert c.get('/api/metrics').status_code == 401
    assert not store.records() and not store.entities() and not store.operations()


@pytest.mark.parametrize('token', [OP, AP, 'tiny', 'a' * 23, 'a' * 513, 'x' * 30 + '\n'])
def test_metrics_token_cannot_reuse_authority_or_malformed_secret(store, token):
    with pytest.raises(ValueError):
        create_app(Configuration(), store, OP, AP, metrics_token=token)


def test_metric_secret_file_and_configuration_redaction(store, tmp_path):
    secret = tmp_path / 'metrics-token'
    secret.write_text(MP + '\n')
    assert metrics_secret({'LAB_METRICS_TOKEN_FILE': str(secret)}) == MP
    with pytest.raises(ValueError):
        metrics_secret({'LAB_METRICS_TOKEN': MP, 'LAB_METRICS_TOKEN_FILE': str(secret)})
    assert metrics_secret({}) is None
    c = client(store)
    for path in ('/api/config', '/api/workspace'):
        assert MP not in c.get(path, headers={'Authorization': 'Bearer ' + OP}).text
    assert MP not in str(store.meta('active_configuration'))


@pytest.mark.parametrize('host', ['*', '*.example.com', 'http://host', 'host:8787', 'x/y', 'x@host', 'a..b', 'a\n', ''])
def test_invalid_host_allowlists_are_rejected(host):
    with pytest.raises(ValueError):
        allowed_hosts([host])


def test_only_explicit_internal_hosts_are_allowed(store):
    c = TestClient(create_app(Configuration(), store, OP, AP, hosts=['localhost', 'console.internal']))
    assert c.get('/healthz', headers={'Host': 'console.internal'}).status_code == 200
    assert c.get('/healthz', headers={'Host': 'untrusted.example'}).status_code == 400
    assert allowed_hosts('localhost,console.internal') == ['localhost', 'console.internal']


def test_readiness_requires_current_worker_but_liveness_does_not(store):
    c = client(store)
    assert c.get('/healthz').status_code == 200
    assert c.get('/readyz').status_code == 503
    for state, timestamp in [('stopped', iso()), ('running', iso(utcnow()-timedelta(minutes=5))),
                             ('running', iso(utcnow()+timedelta(minutes=5))), ('running', 'invalid')]:
        store.meta('worker', {'state': state, 'heartbeat_at': timestamp})
        assert c.get('/readyz').status_code == 503
    store.meta('worker', {'state': 'running', 'heartbeat_at': iso()})
    assert c.get('/readyz').json() == {'status': 'ready'}
    assert not store.operations()


def test_export_preserves_frozen_agent_and_workload_scope(rig):
    trial = run_trial(rig)
    store = rig['store']
    text = prometheus(store)
    binding = store.record(trial['data']['binding_record_id'])['data']
    assert 'agent_space="' + binding['agent_space_id'] + '"' in text
    assert 'workload_account="' + binding['workload']['account_id'] + '"' in text
    assert 'assessment="' + trial['data']['assessment_id'] + '"' in text
    assert '# TYPE agent_validation_observed_timestamp_seconds gauge' in text
    rig['config'].bindings[0].agent_space_id = 'different-current-agent'
    assert prometheus(store) == text


def test_export_rejects_wrong_owner_and_unpinned_scope(rig):
    trial = run_trial(rig); store = rig['store']
    body = deepcopy(store.record(trial['data']['assessment_id'])['data'])
    other = store.put_record('assessment', 'another-trial', body)
    store.update(trial['id'], changes={'assessment_id': other['id']})
    with pytest.raises(Blocked, match='belong'):
        prometheus(store)
    body['input_hashes'].pop(trial['data']['binding_record_id'])
    wrong = store.put_record('assessment', trial['id'], body)
    store.update(trial['id'], changes={'assessment_id': wrong['id']})
    with pytest.raises(Blocked, match='pinned'):
        prometheus(store)


def test_dashboard_filters_agents_without_filling_missing_values():
    value = dashboard()
    assert 'agent_space' in {v['name'] for v in value['templating']['list']}
    for panel in value['panels']:
        if panel['type'] == 'timeseries':
            query = panel['targets'][0]['expr']
            assert '${agent_space:regex}' in query
            assert 'or vector(0)' not in query
    assert 'not live workload' in value['panels'][0]['options']['content']
