"""Regression tests for delivery provenance, finite adapters and frozen exports."""
import hashlib
import json
from copy import deepcopy
from datetime import timedelta
from pathlib import Path
import pytest
from conftest import FakeAWS, run_trial
from lab.aws import AWS, template_contract
from lab.models import Configuration
from lab.evaluation import evaluate_trial
from lab.report import report_html
from lab.util import Blocked, digest, iso, dt
from lab.metrics import dashboard


def test_sender_final_rejection_is_delivery_failure_not_agent_silence(rig,monkeypatch):
    original=FakeAWS.observe
    def observe(self,*args,**kwargs):
        response=original(self,*args,**kwargs)
        response['receipt']=None
        response['delivery_failure']={'accepted':False,'final':True,'reason_code':'DestinationRejected','attempted_at':iso(self.world.clock())}
        return response
    monkeypatch.setattr(FakeAWS,'observe',observe)
    rig['world'].no_task=True
    trial=run_trial(rig)
    assessment=rig['store'].record(trial['data']['assessment_id'])['data']
    assert assessment['dimensions']['delivery']['outcome']=='fail'
    assert assessment['dimensions']['response']['outcome']=='inconclusive'
    assert not any(w[2]=='create_backlog_task' for w in rig['world'].writes)


def test_late_probe_cannot_rewrite_pinned_measurements(rig):
    trial=run_trial(rig);store=rig['store'];aid=trial['data']['assessment_id'];assessment=store.record(aid)
    old_samples=store.record(assessment['data']['probe_capture_id'])['data']['samples']
    before=report_html(store,trial['id'])
    store.probe(trial['id'],{'scheduled_at':iso(dt(trial['data']['observation_ends_at'])+timedelta(seconds=1)),
                 'at':iso(dt(trial['data']['observation_ends_at'])+timedelta(seconds=1)),
                 'attempted':True,'success':False,'latency_ms':999,'probe_id':'test-late'})
    assert store.record(aid)['sha256']==assessment['sha256']
    assert store.record(assessment['data']['probe_capture_id'])['data']['samples']==old_samples
    after=report_html(store,trial['id'])
    # The report exports the pinned probe capture, not all newly arrived samples.
    assert 'test-late' not in after and assessment['sha256'] in after


def test_no_task_before_full_response_deadline_is_inconclusive(rig):
    rig['world'].no_task=True
    trial=run_trial(rig);store=rig['store']
    last=store.record(trial['data']['final_observation_id'])['data']
    modified=deepcopy(last)
    modified['receipt']['accepted_at']=iso(dt(trial['data']['observation_ends_at'])-timedelta(seconds=1))
    rec=store.put_record('observation',trial['id'],modified)
    store.update(trial['id'],changes={'final_observation_id':rec['id']})
    # Earlier positive receipts still exist and are evidence of an earlier delivery.
    # A separate trial containing only the late receipt tests the deadline guard.
    new=store.create('trial','CLOSED',{**trial['data'],'assessment_id':None,'final_observation_id':None})
    for r in store.records(trial['id']):
        if r['kind'] not in {'observation','assessment','probe_capture'}:
            store.put_record(r['kind'],new['id'],r['data'])
    rec=store.put_record('observation',new['id'],modified)
    store.update(new['id'],changes={'final_observation_id':rec['id']})
    for p in store.probes(trial['id']):store.probe(new['id'],p)
    result=evaluate_trial(store,new['id'],rig['config'].bindings[0])
    assert result['data']['dimensions']['response']['outcome']=='inconclusive'


@pytest.mark.parametrize('step',[
 {'name':'bad','action':'aws:executeScript','timeoutSeconds':10},
 {'name':'bad','action':'aws:executeAutomation','timeoutSeconds':10},
 {'name':'bad','action':'aws:branch','timeoutSeconds':10},
 {'name':'bad','action':'aws:executeAwsApi'},
 {'name':'bad','action':'aws:executeAwsApi','timeoutSeconds':0},
 {'name':'bad','action':'aws:executeAwsApi','timeoutSeconds':10,'maxAttempts':100},
 {'name':'bad','action':'aws:executeAwsApi','timeoutSeconds':10,'nextStep':'loop'},
 {'name':'bad','action':'aws:executeAwsApi','timeoutSeconds':10,'onCancel':'step:custom'},
])
def test_pinned_but_unbounded_or_programmable_runbooks_are_rejected(config,store,step):
    aws=AWS(config.bindings[0],store,'contract');aws.verified['change']={}
    content=json.dumps({'schemaVersion':'0.3','mainSteps':[step]})
    book=config.bindings[0].runbooks[0].model_copy(update={'content_sha256':hashlib.sha256(content.encode()).hexdigest()})
    aws.call=lambda *args,**kwargs:({'DocumentVersion':book.document_version,'DocumentType':'Automation','Content':content},'source')
    with pytest.raises(Blocked):aws.document(book)


@pytest.mark.parametrize('selector',[
 {'resourceTags':{'selected':'true'}},
 {'filters':[{'path':'State.Name','values':['running']}]},
 {'parameters':{'namespace':'default'}},
 {'selectionMode':'COUNT(1)'},
])
def test_pinned_fis_selector_templates_need_an_unimplemented_resolver(config,store,selector):
    binding=config.bindings[0];fault=binding.faults[0]
    target={'resourceType':'aws:ec2:instance','resourceArns':fault.target_arns,'selectionMode':'ALL',**selector}
    template={'id':fault.template_id,'roleArn':f'arn:aws:iam::{binding.workload.account_id}:role/FIS',
              'targets':{'host':target},'actions':{'stop':{'actionId':'aws:ec2:stop-instances','parameters':{'startInstancesAfterDuration':'PT1M'},'targets':{'Instances':'host'}}},
              'stopConditions':[{'source':'aws:cloudwatch:alarm','value':x} for x in fault.safety_alarm_arns]}
    fault=fault.model_copy(update={'template_sha256':digest(template_contract(template))})
    aws=AWS(binding,store,'selector');aws.verified['fault']={}
    aws.call=lambda *args,**kwargs:({'experimentTemplate':template},'source')
    with pytest.raises(Blocked):aws.template(fault)


def test_dashboard_has_one_panel_per_measured_family_and_no_zero_fill():
    dashboard_value=dashboard();panels=[x for x in dashboard_value['panels'] if x['type']=='timeseries']
    assert len(panels)==12
    assert len({x['id'] for x in dashboard_value['panels']})==len(dashboard_value['panels'])
    assert all('or vector(0)' not in x['targets'][0]['expr'] for x in panels)
    assert all(x['fieldConfig']['defaults']['custom']['spanNulls'] is False for x in panels)


def test_distribution_configuration_remains_empty_and_write_disabled():
    root=Path(__file__).resolve().parents[1]
    config=Configuration.model_validate_json((root/'config.json').read_text())
    assert not config.bindings and not config.enable_aws_writes
    for product in (root/'lab').glob('*.py'):
        assert 'from tests' not in product.read_text() and 'import conftest' not in product.read_text()
