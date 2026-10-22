import copy
import json
import sqlite3
import threading
from datetime import timedelta
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from lab.models import Configuration, Experiment, TrialRequest, CampaignRequest, ChangeProposal, Approval, Diagnosis
from lab.api import create_app
from lab.service import Service
from lab.store import Store
from lab.worker import Worker
from lab.evaluation import evaluate_trial,compare_campaign,buckets
from lab.broker import Broker
from lab.util import Blocked,UnknownRemoteState,iso,dt,digest
from conftest import approve,run_trial,probe_samples,TARGET


def test_empty_installation_has_no_records_or_aws_configuration(tmp_path):
    config=Configuration();store=Store(tmp_path/'empty')
    client=TestClient(create_app(config,store,'o'*32,'a'*32))
    assert client.get('/api/workspace').status_code==401
    data=client.get('/api/workspace',headers={'Authorization':'Bearer '+'o'*32}).json()
    assert data['entities']==[] and data['records']==[] and data['write_enabled'] is False

@pytest.mark.parametrize('mutation',[
 lambda c:c['bindings'][0].update(environment='production'),
 lambda c:c['bindings'][0]['workload'].update(account_id='111111111111'),
 lambda c:c['bindings'][0]['faults'][0].update(target_arns=['arn:aws:ec2:eu-central-1:999999999999:instance/x']),
 lambda c:c['bindings'][0]['checks'][0].update(operation='terminate_instances'),
 lambda c:c['bindings'][0]['runbooks'][0].update(document_version='$LATEST'),
 lambda c:c['bindings'][0]['probes'][0].update(url='http://169.254.169.254/latest/meta-data/'),
 lambda c:c['bindings'][0]['checks'][0].update(parameters={}),
 lambda c:c['bindings'][0]['checks'][0].update(expression='`true`'),
])
def test_configuration_rejects_dangerous_or_ambiguous_instruments(config_dict,mutation):
    mutation(config_dict)
    with pytest.raises(ValidationError):Configuration.model_validate(config_dict)

def test_unknown_schema_fields_rejected(spec):
    body=spec.model_dump();body['simulated']=True
    with pytest.raises(ValidationError):Experiment.model_validate(body)

def test_records_and_journal_are_immutable(store):
    r=store.put_record('test','owner',{'a':1},'test-id')
    with pytest.raises(Blocked):store.put_record('test','owner',{'a':2},'test-id')
    for table in ('records','events'):
        with store.connect() as db,pytest.raises(sqlite3.IntegrityError):db.execute(f'DELETE FROM {table}')
    assert store.record(r['id'])['data']=={'a':1}

def test_projection_concurrency_is_checked(store):
    e=store.create('trial','DRAFT',{})
    store.update(e['id'],state='READY',expected_revision=e['revision'])
    with pytest.raises(Blocked):store.update(e['id'],state='CLOSED',expected_revision=e['revision'])

def test_single_worker_ownership(config,store):
    a,b=Worker(config,store),Worker(config,store)
    a.acquire()
    try:
        with pytest.raises(RuntimeError):b.acquire()
    finally:a.release()
    b.acquire();b.release()

def test_uncertain_write_is_reconciled_not_repeated(rig):
    r=rig;trial=r['service'].trial(TrialRequest(experiment_ref=r['reference']));tid=trial['id']
    aws=r['world'].factory(r['config'].bindings[0],r['store'],tid);broker=Broker(r['store'],aws,True)
    r['world'].fail_write=True
    with pytest.raises(UnknownRemoteState):broker.execute(tid,'fault','fault','fis','start_experiment',{'experimentTemplateId':'EXTtest'})
    op=broker.execute(tid,'fault','fault','fis','start_experiment',{'experimentTemplateId':'EXTtest'})
    assert op['state']=='CONFIRMED' and len(r['world'].writes)==1
    assert r['store'].operation(tid,'fault')['token']==op['token']

def test_operation_request_cannot_change_on_retry(rig):
    store=rig['store'];store.intent('owner','fault',{'a':1})
    with pytest.raises(Blocked):store.intent('owner','fault',{'a':2})

def test_qualified_response_pipeline_runs_without_task_id_or_imported_measurements(rig):
    trial=run_trial(rig)
    assert trial['state']=='CLOSED'
    data=rig['store'].record(trial['data']['assessment_id'])['data']
    assert data['dimensions']['challenge']['outcome']=='pass'
    assert data['dimensions']['response']['outcome']=='pass'
    assert data['dimensions']['service_recovery']['outcome']=='pass'
    assert data['dimensions']['diagnosis']['outcome']=='not_assessed'
    assert data['dimensions']['attribution']['outcome']=='not_established'
    assert data['dimensions']['cleanup']['outcome']=='pass'
    assert all(w[2]!='create_backlog_task' for w in rig['world'].writes)

@pytest.mark.parametrize('receipt,outcome',[(True,'fail'),(False,'inconclusive')])
def test_no_task_is_response_failure_only_when_delivery_is_proved(rig,receipt,outcome):
    rig['world'].no_task=True;rig['world'].no_receipt=not receipt
    trial=run_trial(rig);a=rig['store'].record(trial['data']['assessment_id'])['data']
    assert a['dimensions']['response']['outcome']==outcome
    assert not any(w[2]=='create_backlog_task' for w in rig['world'].writes)

def test_missing_collector_is_not_agent_silence(rig):
    rig['world'].collection_error=True;rig['world'].no_task=True
    trial=run_trial(rig);a=rig['store'].record(trial['data']['assessment_id'])['data']
    assert a['dimensions']['response']['outcome']=='inconclusive'

def test_healthy_replay_is_not_fabricated_response_success(rig):
    trial=run_trial(rig,bad_until=0);a=rig['store'].record(trial['data']['assessment_id'])['data']
    assert a['dimensions']['response']['outcome']=='not_eligible'
    assert a['metrics']['stable_recovery_seconds'] is None

def test_baseline_gap_blocks_fault(rig):
    s,e,store,c=rig['service'],rig['engine'],rig['store'],rig['clock']
    t=s.trial(TrialRequest(experiment_ref=rig['reference']));s.qualify(t['id']);e.step();approve(s,t['id'])
    store.meta('worker',{'state':'running','heartbeat_at':iso()});s.start(t['id'])
    c.value=dt(store.entity(t['id'])['data']['started_at'])+timedelta(seconds=30);e.step()
    assert store.entity(t['id'])['state']=='CLOSED_BLOCKED' and rig['world'].writes==[]

def test_approval_required_and_exact_subject(rig):
    s,e=rig['service'],rig['engine'];t=s.trial(TrialRequest(experiment_ref=rig['reference']));s.qualify(t['id']);e.step()
    with pytest.raises(Blocked):s.start(t['id'])
    subject=s.approval_subject(t['id'])
    with pytest.raises(Blocked):s.approve(t['id'],'start',Approval(expected_digest='0'*64,confirmation=subject['confirmation'],approver='test',rationale='Test exact approval rejection.'))

def test_http_origin_auth_and_approval_separation(rig):
    client=TestClient(create_app(rig['config'],rig['store'],'o'*32,'a'*32,service=rig['service']))
    headers={'Authorization':'Bearer '+'o'*32}
    assert client.post('/api/experiments',headers={**headers,'Origin':'https://evil.invalid'},json=rig['spec'].model_dump()).status_code==403
    t=rig['service'].trial(TrialRequest(experiment_ref=rig['reference']))
    assert client.post('/api/entities/'+t['id']+'/approve/start',headers=headers,json={}).status_code==403
    assert client.get('/',headers={'Host':'untrusted.invalid'}).status_code==400
    assert "unsafe-eval" not in client.get('/').headers['content-security-policy']
    assert client.get('/api/workspace',headers=headers).status_code==200

def test_invalid_actual_targets_abort(rig):
    rig['world'].target_mismatch=True
    trial=run_trial_allow_failure(rig)
    assert trial['state'] in {'CLOSED_ABORTED','ABORTING','RESTORE_REQUIRED'}

def run_trial_allow_failure(rig):
    s,e,store,c=rig['service'],rig['engine'],rig['store'],rig['clock']
    t=s.trial(TrialRequest(experiment_ref=rig['reference']));tid=t['id'];s.qualify(tid);e.step();approve(s,tid)
    store.meta('worker',{'state':'running','heartbeat_at':iso()});s.start(tid)
    c.value=dt(store.entity(tid)['data']['started_at']);probe_samples(store,tid,iso(c()),30);c.advance(30);e.step();e.step()
    for _ in range(20):c.advance(10);e.step()
    return store.entity(tid)

def test_diagnosis_requires_quotes_and_independent_oracle_sources(rig):
    t=run_trial(rig);store=rig['store'];find=next(r for r in store.records(t['id'],'finding') if r['data']['recordType']=='investigation_summary_md')
    truth=store.record(t['data']['ground_truth_id']);source=truth['data']['verified_checks'][0]['source_record_id']
    values=dict(reviewer='test reviewer',finding_record_id=find['id'],finding_quote='serving instance stopped',asserted_resource_arns=[TARGET],
                asserted_mechanism_code='capacity_loss',citations=[{'record_id':source,'quote':'stopped'}],rationale='The captured resource state supports the asserted failure mechanism.')
    review=rig['service'].diagnosis(t['id'],Diagnosis(**values))
    a=evaluate_trial(store,t['id'],rig['config'].bindings[0]);assert a['data']['dimensions']['diagnosis']['outcome']=='pass'
    values['finding_quote']='a fabricated cause absent from the source'
    with pytest.raises(Blocked):rig['service'].diagnosis(t['id'],Diagnosis(**values))

def test_wrong_extracted_cause_fails_not_hidden_by_recovery(rig):
    t=run_trial(rig);store=rig['store'];find=next(r for r in store.records(t['id'],'finding') if r['data']['recordType']=='investigation_summary_md')
    source=store.record(t['data']['ground_truth_id'])['data']['verified_checks'][0]['source_record_id']
    rig['service'].diagnosis(t['id'],Diagnosis(reviewer='test',finding_record_id=find['id'],finding_quote='serving instance stopped',
         asserted_resource_arns=[TARGET],asserted_mechanism_code='different_cause',citations=[{'record_id':source,'quote':'stopped'}],
         rationale='This deliberately incorrect extraction checks the independent requirement decision.'))
    a=evaluate_trial(store,t['id'],rig['config'].bindings[0])
    assert a['data']['dimensions']['diagnosis']['outcome']=='fail' and a['data']['dimensions']['service_recovery']['outcome']=='pass'

def test_prevention_complete_chain_from_evaluation_to_verified_change_to_replay(rig):
    s,e,store=rig['service'],rig['engine'],rig['store']
    c=s.campaign(CampaignRequest(title='Test-only prevention contract',experiment_ref=rig['reference'],comparison={
       'claim':'prevent_recurrence','minimum_improvement':.25,'knowledge_history_note':'Paired sequential fixture; no live agent history or causal generalization is claimed.'}))
    baseline=run_trial(rig,c['id'])
    approve(s,c['id'],'evaluation');e.step();e.step()
    campaign=store.entity(c['id']);assert campaign['state']=='RECOMMENDATIONS'
    rid=campaign['data']['recommendation_ids'][0];s.pin_recommendation(c['id'],rid)
    proposal=s.propose_change(c['id'],ChangeProposal(runbook_id='capacity-change',source_record_id=rid,
       source_quote='Increase serving capacity',rationale='The exact approved capacity runbook realizes the selected recommendation.',proposer='Test only'))
    rig['clock'].advance(1)
    approve(s,proposal['id'],'change');e.step();e.step()
    assert store.entity(proposal['id'])['state']=='VERIFIED' and store.entity(c['id'])['state']=='REPLAY_READY'
    rig['clock'].advance(10)
    replay=run_trial(rig,c['id'],'treatment',bad_until=0)
    comparison=compare_campaign(store,c['id'],rig['config'].bindings[0])
    assert comparison['data']['outcome']=='pass',comparison['data']
    assert comparison['data']['recommendation_record_id']==rid
    assert set(comparison['data']['all_trial_ids'])=={baseline['id'],replay['id']}
    request=next(w[3] for w in rig['world'].writes if w[2]=='create_backlog_task')
    assert request['taskType']=='EVALUATION' and 'capacity_loss' not in request['description']
    assert not any('expected_cause' in json.dumps(w) for w in rig['world'].writes)

def test_no_prevention_pass_without_implemented_recommendation(rig):
    s=rig['service'];c=s.campaign(CampaignRequest(title='Unimplemented',experiment_ref=rig['reference'],comparison={
       'claim':'prevent_recurrence','knowledge_history_note':'No recommendation is implemented; comparison must not claim prevention.'}))
    run_trial(rig,c['id'])
    a=compare_campaign(rig['store'],c['id'],rig['config'].bindings[0]);assert a['data']['outcome']=='inconclusive'
    with pytest.raises(Blocked):s.trial(TrialRequest(experiment_ref=rig['reference'],campaign_id=c['id'],arm='treatment'))

def test_no_traffic_is_not_recovery(spec):
    start=iso();end=iso(dt(start)+timedelta(seconds=20))
    rows=buckets([],start,end,spec,1)
    assert all(r['complete'] is False and r['error_ratio'] is None for r in rows)

def test_restart_persistence_backup_and_intent_identity(store,tmp_path):
    r=store.put_record('source','owner',{'actual':'retained'});op=store.intent('owner','operation',{'operation':'test'})
    other=Store(store.directory);assert other.record(r['id'])['sha256']==r['sha256']
    assert other.operation('owner','operation')['token']==op['token']
    backup=tmp_path/'backup.sqlite3';store.backup(backup)
    with sqlite3.connect(backup) as db:assert db.execute('SELECT sha256 FROM records WHERE id=?',(r['id'],)).fetchone()[0]==r['sha256']

def test_exported_report_retains_graphs_hashes_no_network(rig):
    from lab.report import report_document
    trial=run_trial(rig);document,csp=report_document(rig['store'],trial['id'])
    assert 'connect-src \'none\'' in csp and 'LabCharts' in document
    assert trial['data']['assessment_id'] in document and 'export_sha256' in document

def test_prometheus_empty_is_absent_and_derived_metrics_are_measured(rig):
    from lab.metrics import prometheus,dashboard
    assert not any(line.startswith('agent_validation_') for line in prometheus(rig['store']).splitlines())
    trial=run_trial(rig);metrics=prometheus(rig['store'])
    assert 'agent_validation_failed_probe_requests{' in metrics
    assert 'synthetic' not in metrics
    assert len([p for p in dashboard()['panels'] if p['type']=='timeseries'])==12
