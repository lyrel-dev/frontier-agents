from types import SimpleNamespace as NS, ModuleType
from copy import deepcopy
import json,socketserver,threading,sys
import pytest
import boto3
from botocore.stub import Stubber
from botocore.exceptions import ClientError
from app import connectors as m
from app.models import Bundle

AWS_CONFIG={'id':'test-aws','name':'Test account','kind':'aws','profile':None,'expected_account_id':'123456789012','regions':['eu-central-1'],'services':['ec2']}
IDENTITY={'Account':'123456789012','Arn':'arn:aws:iam::123456789012:role/Inspector','UserId':'test-user'}


def sdk_client(service):
    return boto3.client(service,region_name='eu-central-1',aws_access_key_id='test',aws_secret_access_key='test')


def test_aws_account_mismatch_blocks_inventory(monkeypatch):
    sts=sdk_client('sts');stub=Stubber(sts);stub.add_response('get_caller_identity',{**IDENTITY,'Account':'999999999999'},{})
    calls=[]
    def factory(name,**kwargs):calls.append(name);return sts
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=factory))
    with stub,pytest.raises(m.InspectionError,match='AccountMismatch'):m.inspect_aws(AWS_CONFIG)
    assert calls==['sts']


def test_aws_root_identity_refused(monkeypatch):
    sts=sdk_client('sts');stub=Stubber(sts);stub.add_response('get_caller_identity',{**IDENTITY,'Arn':'arn:aws:iam::123456789012:root'},{})
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=lambda *a,**kw:sts))
    with stub,pytest.raises(m.InspectionError,match='RootIdentityRejected'):m.inspect_aws(AWS_CONFIG)


def test_ec2_metadata_is_whitelisted(monkeypatch):
    sts,ec2=sdk_client('sts'),sdk_client('ec2')
    ss,es=Stubber(sts),Stubber(ec2)
    ss.add_response('get_caller_identity',IDENTITY,{})
    es.add_response('describe_instances',{'Reservations':[{'Instances':[{'InstanceId':'i-1234567890abcdef0','InstanceType':'t3.small','State':{'Name':'running','Code':16},'Placement':{'AvailabilityZone':'eu-central-1a'},'PrivateIpAddress':'10.1.2.3','Tags':[{'Key':'password','Value':'never-store-me'}]}]}]}, {})
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=lambda n,**kw:{'sts':sts,'ec2':ec2}[n]))
    with ss,es:r=m.inspect_aws(AWS_CONFIG)
    assert r['data']['identity']['account_id']=='123456789012'
    assert r['data']['coverage'][0]['status']=='complete'
    assert len(r['data']['resources'])==1
    assert 'never-store-me' not in json.dumps(r) and '10.1.2.3' not in json.dumps(r)
    Bundle.model_validate({'records':[r]})


def test_aws_access_denied_is_a_gap_not_empty_success(monkeypatch):
    sts,ec2=sdk_client('sts'),sdk_client('ec2');ss,es=Stubber(sts),Stubber(ec2)
    ss.add_response('get_caller_identity',IDENTITY,{})
    es.add_client_error('describe_instances',service_error_code='AccessDenied',service_message='sensitive SDK detail',expected_params={})
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=lambda n,**kw:{'sts':sts,'ec2':ec2}[n]))
    with ss,es:r=m.inspect_aws(AWS_CONFIG)
    assert r['data']['coverage'][0]['status']=='denied'
    assert r['data']['resources']==[] and 'sensitive SDK detail' not in json.dumps(r)


def test_page_cap_is_recorded_as_truncated():
    pages=[{'Items':[str(i)],'NextToken':str(i+1)} for i in range(20)]
    fake=NS(can_paginate=lambda method:True,get_paginator=lambda method:NS(paginate=lambda **kw:iter(pages)))
    c=m.Collector({'id':'test','kind':'aws'})
    result=c.pages(fake,'list_items','Items')
    assert len(result)==m.MAX_PAGES and c.truncated


def test_last_page_at_cap_is_not_falsely_truncated():
    pages=[{'Items':[str(i)],'NextToken':str(i+1) if i<4 else ''} for i in range(5)]
    fake=NS(can_paginate=lambda method:True,get_paginator=lambda method:NS(paginate=lambda **kw:iter(pages)))
    c=m.Collector({'id':'test','kind':'aws'})
    assert len(c.pages(fake,'list_items','Items'))==5 and not c.truncated


def test_cooperative_deadline_records_error():
    c=m.Collector({'id':'test','kind':'aws'});c.deadline=0
    called=[];c.group('test',lambda:called.append(True))
    assert not called and c.coverage[0]['status']=='error'


@pytest.fixture
def fake_engine(tmp_path):
    payloads={
      '/version':{'Version':'test','ApiVersion':'1.41'},
      '/containers/json?all=true':[{'Id':'c1','Names':['/worker'],'Image':'example:1','State':'running','Status':'Up','Env':['SECRET=x']}],
      '/volumes':{'Volumes':[{'Name':'data','Driver':'local','Scope':'local','Mountpoint':'/secret/host/path'}]},
      '/networks':[{'Id':'n1','Name':'bridge','Driver':'bridge','Scope':'local','IPAM':{'Config':[{'Subnet':'10.0.0.0/8'}]}}]
    }
    requests=[]
    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            line=self.rfile.readline().decode().strip();method,path,_=line.split();requests.append((method,path))
            while self.rfile.readline() not in (b'\r\n',b'\n',b''):pass
            body=json.dumps(payloads[path]).encode()
            self.wfile.write(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: '+str(len(body)).encode()+b'\r\nConnection: close\r\n\r\n'+body)
    path=str(tmp_path/'engine.sock');server=socketserver.UnixStreamServer(path,Handler)
    worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
    yield path,requests
    server.shutdown();server.server_close();worker.join(timeout=2)


@pytest.mark.parametrize('kind',['docker','podman'])
def test_engine_reads_only_four_endpoints(fake_engine,kind):
    path,requests=fake_engine;r=m.inspect_engine({'id':'engine','name':'Engine','kind':kind,'socket':path})
    assert len(r['data']['resources'])==3
    assert all(x['status']=='complete' for x in r['data']['coverage'])
    assert len(requests)==4 and all(method=='GET' for method,_ in requests)
    assert 'SECRET' not in json.dumps(r) and '/secret/host/path' not in json.dumps(r)
    assert '10.0.0.0' not in json.dumps(r)
    Bundle.model_validate({'records':[r]})


def test_engine_rejects_other_endpoints():
    with pytest.raises(m.InspectionError,match='NotAllowlisted'):m.engine_get('/unused','/containers/c1/exec')


def test_missing_engine_socket_produces_explicit_gaps(tmp_path):
    r=m.inspect_engine({'id':'missing','kind':'podman','socket':str(tmp_path/'missing.sock')})
    assert len(r['data']['coverage'])==4
    assert all(x['status']=='error' for x in r['data']['coverage'])
    assert not r['data']['resources']


def test_kubernetes_scope_and_methods_with_sdk_double(monkeypatch):
    calls=[]
    class Configuration:
        verify_ssl=True
        host='https://local-test.invalid'
    class API:
        def __init__(self,c):pass
        def close(self):calls.append(('close',))
    class Core:
        def __init__(self,api):pass
        def __getattr__(self,name):
            def method(**kwargs):calls.append((name,kwargs));return NS(items=[],metadata=NS(_continue=None))
            return method
    fake=ModuleType('kubernetes')
    fake.client=NS(Configuration=Configuration,ApiClient=API,CoreV1Api=Core,AppsV1Api=Core)
    fake.config=NS(load_incluster_config=lambda **kwargs:None,load_kube_config=lambda **kwargs:None)
    monkeypatch.setitem(sys.modules,'kubernetes',fake)
    r=m.inspect_kubernetes({'id':'k','kind':'kubernetes','in_cluster':True,'namespaces':['team-a']})
    actual=[x for x in calls if x[0]!='close']
    assert len(actual)==6
    assert all(x[1]['namespace']=='team-a' for x in actual)
    assert all(x[0].startswith('list_namespaced_') and 'secret' not in x[0] and 'config_map' not in x[0] for x in actual)
    assert all(c['status']=='complete' for c in r['data']['coverage'])
    Bundle.model_validate({'records':[r]})


def test_kubernetes_tls_bypass_refused_with_sdk_double(monkeypatch):
    fake=ModuleType('kubernetes')
    fake.client=NS(Configuration=lambda:NS(verify_ssl=False))
    fake.config=NS(load_incluster_config=lambda **kwargs:None)
    monkeypatch.setitem(sys.modules,'kubernetes',fake)
    with pytest.raises(m.InspectionError,match='TLSVerificationRequired'):m.inspect_kubernetes({'id':'k','kind':'kubernetes','in_cluster':True,'namespaces':['team-a']})

class FakeClient:
    def __init__(self, responses): self.responses=responses
    def can_paginate(self, name): return False
    def __getattr__(self, name):
        return lambda **kwargs: deepcopy(self.responses[name])


def test_eks_profiles_are_distinct_from_managed_nodegroups(monkeypatch):
    eks=FakeClient({'list_clusters':{'clusters':['app']},'describe_cluster':{'cluster':{'arn':'cluster-1','status':'ACTIVE','version':'1.34'}},'list_nodegroups':{'nodegroups':['workers']},'describe_nodegroup':{'nodegroup':{'nodegroupArn':'nodegroup-1','status':'ACTIVE','capacityType':'ON_DEMAND','scalingConfig':{'desiredSize':2}}},'list_fargate_profiles':{'fargateProfileNames':['serverless']},'describe_fargate_profile':{'fargateProfile':{'fargateProfileArn':'profile-1','status':'ACTIVE','selectors':[{'namespace':'app'}]}}})
    clients={'sts':FakeClient({'get_caller_identity':IDENTITY}),'eks':eks}
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=lambda name,**kw:clients[name]))
    r=m.inspect_aws({**AWS_CONFIG,'services':['eks']})
    assert {x['model'] for x in r['data']['resources']}=={'shared','eks-ec2','eks-fargate'}
    assert all(x['status']=='complete' for x in r['data']['coverage'])
    assert not any(x['kind']=='Pod' for x in r['data']['resources'])
    Bundle.model_validate({'records':[r]})


def test_ecs_explicit_and_unknown_launch_models(monkeypatch):
    services=[{'serviceArn':'s-ec2','serviceName':'ec2','status':'ACTIVE','launchType':'EC2'}, {'serviceArn':'s-fargate','serviceName':'fargate','status':'ACTIVE','capacityProviderStrategy':[{'capacityProvider':'FARGATE_SPOT'}]}, {'serviceArn':'s-custom','serviceName':'custom','status':'ACTIVE','capacityProviderStrategy':[{'capacityProvider':'custom-pool'}]}]
    ecs=FakeClient({'list_clusters':{'clusterArns':['arn:example/cluster']},'list_services':{'serviceArns':[s['serviceArn'] for s in services]},'describe_services':{'services':services},'list_tasks':{'taskArns':['task-ec2','task-fg']},'describe_tasks':{'tasks':[{'taskArn':'task-ec2','launchType':'EC2','lastStatus':'RUNNING'},{'taskArn':'task-fg','launchType':'FARGATE','lastStatus':'RUNNING'}]}})
    clients={'sts':FakeClient({'get_caller_identity':IDENTITY}),'ecs':ecs}
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=lambda name,**kw:clients[name]))
    r=m.inspect_aws({**AWS_CONFIG,'services':['ecs']});models={x['id']:x['model'] for x in r['data']['resources']}
    assert models['s-ec2']=='ecs-ec2' and models['s-fargate']=='ecs-fargate'
    assert models['s-custom']=='shared' and models['task-fg']=='ecs-fargate' and models['task-ec2']=='ecs-ec2'
    Bundle.model_validate({'records':[r]})


def test_lambda_summary_excludes_environment_and_layers(monkeypatch):
    fn=FakeClient({'list_functions':{'Functions':[{'FunctionArn':'fn-1','FunctionName':'worker','Runtime':'python3.13','MemorySize':128,'Timeout':30,'Version':'$LATEST','Environment':{'Variables':{'PASSWORD':'not-in-output'}},'Layers':[{'Arn':'unverified-layer'}]}]}})
    clients={'sts':FakeClient({'get_caller_identity':IDENTITY}),'lambda':fn}
    monkeypatch.setattr(boto3,'Session',lambda **kwargs:NS(client=lambda name,**kw:clients[name]))
    r=m.inspect_aws({**AWS_CONFIG,'services':['lambda']})
    assert r['data']['resources'][0]['model']=='lambda'
    assert 'not-in-output' not in json.dumps(r) and 'unverified-layer' not in json.dumps(r)
    Bundle.model_validate({'records':[r]})
