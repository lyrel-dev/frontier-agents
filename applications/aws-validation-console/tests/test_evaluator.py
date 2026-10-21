from copy import deepcopy
import pytest
from app.store import Store,ref
from app.evaluator import evaluate

RUN='execution_run:example-run-1@1'

def changed_store(tmp_path,examples,mutator):
    records=deepcopy(examples['records'])
    records=[r for r in records if r['kind'] not in ('validation_run','report')]
    mutator(records)
    s=Store(tmp_path/'changed');s.import_bundle({'records':records})
    return s


def metric(records,name,run=RUN):
    return next(r for r in records if r['kind']=='evidence' and r['data']['run_ref']==run and r['data']['metric']==name)


def check(result,id):
    return next(c for c in result['data']['checks'] if c['assertion_id']==id)


def test_known_failure_and_missing_evidence_remain_distinct(store):
    r=evaluate(store,RUN)
    assert r['data']['outcome']=='fail'
    assert check(r,'restore')['outcome']=='fail'
    assert check(r,'duplicates')['outcome']=='inconclusive'


def test_missing_required_metric_prevents_pass(store):
    r=evaluate(store,'execution_run:example-run-2@1')
    assert r['data']['outcome']=='inconclusive'
    assert check(r,'detect')['outcome']=='inconclusive'


def test_all_required_checks_can_pass(tmp_path,examples):
    def mutate(records):
        metric(records,'recovery_seconds')['data']['value']=150
        e=deepcopy(metric(records,'request_error_ratio'));e['id']='new-duplicates';e['data'].update(metric='duplicate_transactions',value=0,unit='transactions')
        records.append(e)
    r=evaluate(changed_store(tmp_path,examples,mutate),RUN)
    assert r['data']['outcome']=='pass'


@pytest.mark.parametrize('field,value,reason',[
 ('scope_id','wrong-scope','Scope differs'),
 ('unit','milliseconds','Unit mismatch'),
 ('sample_count',2,'Insufficient samples'),
 ('value',True,'type mismatch'),
 ('window_start','2026-10-21T08:01:00Z','does not cover'),
 ('window_start','2026-10-21T07:59:00Z','outside'),
 ('window_end','2026-10-21T08:04:00Z','does not cover'),
 ('collected_at','2026-10-21T08:11:00Z','permitted lag'),
 ('collected_at','2099-10-21T08:05:00Z','future')
])
def test_evidence_gaps_do_not_pass(tmp_path,examples,field,value,reason):
    s=changed_store(tmp_path,examples,lambda rs:metric(rs,'request_error_ratio')['data'].__setitem__(field,value))
    c=check(evaluate(s,RUN),'request-errors')
    assert c['outcome']=='inconclusive' and reason in c['reason']


def test_extra_window_end_is_inconclusive(tmp_path,examples):
    def mutate(rs):metric(rs,'request_error_ratio')['data'].update(window_end='2026-10-21T08:06:00Z',collected_at='2026-10-21T08:06:00Z')
    assert check(evaluate(changed_store(tmp_path,examples,mutate),RUN),'request-errors')['outcome']=='inconclusive'


def test_duplicate_metrics_do_not_silently_choose_latest(tmp_path,examples):
    def mutate(rs):
        e=deepcopy(metric(rs,'request_error_ratio'));e['id']='duplicate-measurement';rs.append(e)
    s=changed_store(tmp_path,examples,mutate)
    assert check(evaluate(s,RUN),'request-errors')['outcome']=='inconclusive'
    selected=[e['meta']['ref'] for e in s.all() if e['record']['kind']=='evidence' and e['record']['data']['run_ref']==RUN and e['record']['id']!='duplicate-measurement']
    assert check(evaluate(s,RUN,selected),'request-errors')['outcome']=='pass'


@pytest.mark.parametrize('change',[{'fault_confirmed':None},{'fault_confirmed':False},{'execution_state':'failed'},{'execution_state':'aborted'},{'execution_state':'planned'}])
def test_invalid_execution_gates_preserve_known_failure(tmp_path,examples,change):
    def mutate(rs):next(r for r in rs if ref(r)==RUN)['data'].update(change)
    r=evaluate(changed_store(tmp_path,examples,mutate),RUN)
    assert r['data']['outcome']=='fail' and r['data']['gates']
    assert check(r,'restore')['outcome']=='fail'


def test_future_completed_run_is_gated(tmp_path,examples):
    def mutate(rs):next(r for r in rs if ref(r)==RUN)['data']['ended_at']='2099-10-21T08:05:00Z'
    r=evaluate(changed_store(tmp_path,examples,mutate),RUN)
    assert any('future' in g for g in r['data']['gates'])


def test_draft_without_assertions_cannot_pass(tmp_path,examples):
    def mutate(rs):next(r for r in rs if r['kind']=='scenario')['data'].update(status='draft',assertions=[])
    r=evaluate(changed_store(tmp_path,examples,mutate),RUN)
    assert r['data']['outcome']=='inconclusive' and not r['data']['checks']


def test_simulation_mismatch_is_not_accepted(tmp_path,examples):
    def mutate(rs):metric(rs,'request_error_ratio')['simulated']=False
    assert check(evaluate(changed_store(tmp_path,examples,mutate),RUN),'request-errors')['outcome']=='inconclusive'


def test_selected_evidence_must_belong_to_run(store):
    with pytest.raises(ValueError):evaluate(store,RUN,['evidence:example-2-request_error_ratio@1'])


def test_duplicate_selected_references_rejected(store):
    with pytest.raises(ValueError):evaluate(store,RUN,['evidence:example-1-request_error_ratio@1']*2)


def test_explicit_empty_selection_does_not_fall_back(store):
    r=evaluate(store,RUN,[])
    assert all(c['outcome']=='inconclusive' for c in r['data']['checks'])


def test_each_evaluation_has_new_id_but_same_input_hashes(store):
    a,b=evaluate(store,RUN),evaluate(store,RUN)
    assert a['id']!=b['id']
    assert a['data']['input_hashes']==b['data']['input_hashes']


def test_imported_inputs_remain_unverified(tmp_path,examples):
    s=Store(tmp_path/'imported');s.import_bundle(examples)
    assert any('authenticity' in x for x in evaluate(s,RUN)['data']['limitations'])


def test_execution_gate_prevents_pass_when_all_assertions_pass(tmp_path,examples):
    def mutate(records):
        next(r for r in records if ref(r)==RUN)['data']['fault_confirmed']=False
        metric(records,'recovery_seconds')['data']['value']=150
        e=deepcopy(metric(records,'request_error_ratio'));e['id']='gate-duplicates'
        e['data'].update(metric='duplicate_transactions',value=0,unit='transactions')
        records.append(e)
    result=evaluate(changed_store(tmp_path,examples,mutate),RUN)['data']
    assert all(c['outcome']=='pass' for c in result['checks'])
    assert result['outcome']=='inconclusive' and result['gates']
