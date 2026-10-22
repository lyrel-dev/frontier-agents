"""Validate the actual allowlisted SDK adapter, not a substitute adapter."""
import boto3
from botocore.stub import Stubber
from test_delivery_components import native_fixture,OP,AP
from fastapi.testclient import TestClient
from lab.aws import AWS
from lab.api import create_app
from lab.models import Configuration


def test_native_get_action_and_template_account_reads_use_real_adapter(config,store):
    cfg,row,p,b=native_fixture(config,store,multi=True)
    adapter=AWS(b,store,'sdk-native');client=boto3.client('fis',region_name='eu-central-1',aws_access_key_id='TESTONLY',aws_secret_access_key='TESTONLY')
    adapter.client=lambda side,service,write=False:client
    with Stubber(client) as stub:
        stub.add_response('get_action',{'action':{'id':'aws:ec2:stop-instances'}},{'id':'aws:ec2:stop-instances'})
        stub.add_response('list_target_account_configurations',{'targetAccountConfigurations':row['data']['target_accounts']},{'experimentTemplateId':row['data']['template_id'],'maxResults':100})
        result,source=adapter.call('fault','fis','get_action',id='aws:ec2:stop-instances')
        assert result['action']['id']=='aws:ec2:stop-instances'
        accounts,refs=adapter.pages('fault','fis','list_target_account_configurations','targetAccountConfigurations',experimentTemplateId=row['data']['template_id'],maxResults=100)
        assert len(accounts)==2
        assert store.record(source)['data']['account_id']==b.orchestrator.account_id
        stub.assert_no_pending_responses()


def test_native_multitarget_experiment_responses_use_correct_sdk_parameters(config,store):
    cfg,row,p,b=native_fixture(config,store,multi=True)
    adapter=AWS(b,store,'sdk-experiment');client=boto3.client('fis',region_name='eu-central-1',aws_access_key_id='TESTONLY',aws_secret_access_key='TESTONLY')
    adapter.client=lambda side,service,write=False:client;adapter.verified['fault']={}
    with Stubber(client) as stub:
        stub.add_response('get_experiment',{'experiment':{'id':'EXPfixture','state':{'status':'running'},'experimentOptions':{'accountTargeting':'multi-account','actionsMode':'run-all'}}},{'id':'EXPfixture'})
        stub.add_response('list_experiment_resolved_targets',{'resolvedTargets':p['data']['targets']},{'experimentId':'EXPfixture','maxResults':100})
        stub.add_response('list_experiment_target_account_configurations',{'targetAccountConfigurations':row['data']['target_accounts']},{'experimentId':'EXPfixture'})
        result=adapter.experiment('EXPfixture');assert len(result['target_accounts'])==2
        assert result['resolved_targets']==p['data']['targets'];stub.assert_no_pending_responses()


def test_all_allowlisted_read_operations_have_working_typed_parameter_shapes(store):
    app=TestClient(create_app(Configuration(),store,OP,AP));h={'Authorization':'Bearer '+OP}
    reads=app.get('/api/setup/read-operations',headers=h).json()
    for service,methods in reads.items():
        for op in methods:
            response=app.get('/api/setup/read-shape/'+service+'/'+op,headers=h)
            assert response.status_code==200,(service,op,response.text)
            assert response.json()['type']=='structure'
    assert not store.operations()
