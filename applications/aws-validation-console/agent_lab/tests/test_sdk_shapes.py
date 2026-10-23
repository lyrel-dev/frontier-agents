"""SDK model and API checks use installed schemas, never a cloud account."""
from types import SimpleNamespace
import botocore.session
from botocore import xform_name
from fastapi.testclient import TestClient
import pytest
from lab.api import create_app
from lab.models import Configuration, READS
from lab.sdk_shapes import input_shape
from lab.util import Blocked


def walk(model, described):
    if model is None:
        assert described == {}
        return
    assert described['type'] == model.type_name
    assert described['required'] == list(getattr(model, 'required_members', []))
    if model.type_name == 'structure':
        assert set(described['fields']) == set(model.members)
        for name, member in model.members.items():
            walk(member, described['fields'][name])
    elif model.type_name == 'list':
        walk(model.member, described['items'])
    elif model.type_name == 'map':
        walk(model.value, described['values'])


@pytest.mark.parametrize('service,operation', [(service, operation) for service, operations in sorted(READS.items()) for operation in sorted(operations)])
def test_every_allowlisted_read_input_has_a_complete_form_schema(service, operation):
    sdk = botocore.session.get_session().get_service_model(service)
    name = next(name for name in sdk.operation_names if xform_name(name) == operation)
    model = sdk.operation_model(name).input_shape
    walk(model, input_shape(model))


def test_cloudwatch_dimensions_remain_editable_through_authenticated_api(store):
    app = create_app(Configuration(), store, 'test-only-operator-token-12345', 'test-only-approver-token-12345')
    with TestClient(app) as client:
        path = '/api/setup/read-shape/cloudwatch/get_metric_data'
        assert client.get(path).status_code == 401
        response = client.get(path, headers={'Authorization':'Bearer test-only-operator-token-12345'})
        assert response.status_code == 200
        fields = response.json()['fields']['MetricDataQueries']['items']['fields']
        dimensions = fields['MetricStat']['fields']['Metric']['fields']['Dimensions']
        assert dimensions['items']['fields']['Name']['type'] == 'string'
        assert dimensions['items']['fields']['Value']['type'] == 'string'
    assert not store.operations() and not store.records()


def test_recursive_shape_is_rejected_instead_of_partially_described():
    model = SimpleNamespace(name='Cycle', type_name='structure', required_members=[], members={})
    model.members['again'] = model
    with pytest.raises(Blocked, match='Recursive'):
        input_shape(model)


@pytest.mark.parametrize('limit', ['depth', 'nodes'])
def test_complexity_limit_is_an_explicit_error(limit):
    child = SimpleNamespace(name='Value', type_name='string')
    model = SimpleNamespace(name='Root', type_name='structure', required_members=[], members={'value':child})
    with pytest.raises(Blocked, match='no partial'):
        input_shape(model, **({'max_depth':0} if limit == 'depth' else {'max_nodes':1}))
