"""Deterministic scalar evidence evaluator. No shell, Python expressions, or remote queries."""
from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from .store import now, ref
VERSION = 'scalar-1.0'

def dt(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))

def aggregate(outcomes):
    if 'fail' in outcomes:
        return 'fail'
    if not outcomes or 'inconclusive' in outcomes:
        return 'inconclusive'
    if all(v == 'not_assessed' for v in outcomes):
        return 'not_assessed'
    return 'pass'

def evaluate(store, run_reference, evidence_refs=None):
    run_entry = store.get(run_reference)
    run = run_entry['record']
    if run['kind'] != 'execution_run':
        raise ValueError('run_ref must reference an execution_run')
    d = run['data']
    scenario_entry = store.get(d['scenario_ref'])
    scenario = scenario_entry['record']
    s = scenario['data']
    if evidence_refs is None:
        evidence = [e for e in store.all() if e['record']['kind'] == 'evidence' and e['record']['data']['run_ref'] == run_reference]
    else:
        if len(evidence_refs) != len(set(evidence_refs)):
            raise ValueError('Duplicate evidence reference')
        evidence = [store.get(k) for k in evidence_refs]
        if any(e['record']['kind'] != 'evidence' or e['record']['data']['run_ref'] != run_reference for e in evidence):
            raise ValueError('Every selected evidence record must belong to this run')
    hashes = {run_reference: run_entry['meta']['sha256'], d['scenario_ref']: scenario_entry['meta']['sha256']}
    hashes.update({e['meta']['ref']: e['meta']['sha256'] for e in evidence})
    provenance = [run_entry, scenario_entry, *evidence]
    if d.get('snapshot_ref'):
        snapshot_entry = store.get(d['snapshot_ref'])
        hashes[d['snapshot_ref']] = snapshot_entry['meta']['sha256']
        provenance.append(snapshot_entry)
    gates = []
    evaluation_time = dt(now())
    if d.get('ended_at') and dt(d['ended_at']) > evaluation_time:
        gates.append('The completed run ends in the future relative to the evaluator clock.')
    if d['execution_state'] != 'completed':
        gates.append('Execution is not recorded as completed.')
    if not s['assertions']:
        gates.append('The scenario has no machine-evaluable assertions. Narrative acceptance criteria were not scored.')
    if s['status'] != 'specified':
        gates.append('The scenario is a draft.')
    if s['fault_mode'] != 'none' and d.get('fault_confirmed') is not True:
        gates.append('Fault application has not been confirmed.')
    if run['simulated'] != scenario['simulated']:
        gates.append('The run and scenario have inconsistent simulation labels.')
    checks = []
    for a in s['assertions']:
        item = {'assertion_id': a['id'], 'title': a['title'], 'category': a['category'], 'required': a['required'], 'outcome': 'inconclusive', 'reason': '', 'expected': f"{a['operator']} {a['threshold']} {a['unit']}; at least {a['min_samples']} samples", 'observed': None, 'evidence_ref': None}
        candidates = [e for e in evidence if e['record']['data']['metric'] == a['metric']]
        if len(candidates) != 1:
            item['reason'] = 'No evidence for this metric.' if not candidates else 'More than one evidence record for this metric. Select one explicitly; windows are not merged.'
        else:
            entry = candidates[0]
            e = entry['record']['data']
            item['evidence_ref'] = entry['meta']['ref']
            item['observed'] = e['value']
            invalid = []
            if entry['record']['simulated'] != run['simulated']:
                invalid.append('Simulation labels differ')
            if e['scope_id'] != d['scope_id']:
                invalid.append('Scope differs from the run')
            if e['unit'] != a['unit']:
                invalid.append('Unit mismatch; no implicit conversion')
            if e['sample_count'] < a['min_samples']:
                invalid.append('Insufficient samples')
            if isinstance(e['value'], bool) != isinstance(a['threshold'], bool):
                invalid.append('Boolean/numeric type mismatch')
            # A scalar must cover the complete declared run interval; partial windows do not pass.
            if dt(e['window_start']) > dt(d['started_at']) or (d['ended_at'] and dt(e['window_end']) < dt(d['ended_at'])):
                invalid.append('Evidence does not cover the complete run interval')
            if dt(e['window_start']) < dt(d['started_at']) or (d['ended_at'] and dt(e['window_end']) > dt(d['ended_at'])):
                invalid.append('Evidence includes observations outside the declared run interval')
            lag = (dt(e['collected_at']) - dt(e['window_end'])).total_seconds()
            if dt(e['collected_at']) > evaluation_time:
                invalid.append('Evidence collection timestamp is in the future')
            if lag > a['max_collection_lag_seconds']:
                invalid.append('Evidence was collected after its permitted lag')
            if invalid:
                item['reason'] = '; '.join(invalid) + '.'
            else:
                op = a['operator']
                passed = (e['value'] <= a['threshold']) if op == 'lte' else ((e['value'] >= a['threshold']) if op == 'gte' else (e['value'] == a['threshold']))
                item['outcome'] = 'pass' if passed else 'fail'
                item['reason'] = 'The supplied value satisfies the assertion.' if passed else 'The supplied value exceeds or differs from the accepted limit.'
        checks.append(item)
    required = [c['outcome'] for c in checks if c['required']]
    outcome = 'inconclusive' if gates else aggregate(required)
    limitations = ['This result covers only the stated assertions and time interval; it is not a deployment-readiness certificate.', 'Scalar measurements and sample counts are supplied by collectors or importers; this evaluator does not independently reconstruct them from raw telemetry.', 'Content hashes support consistency checks, not proof of who produced the evidence.']
    if any(e['meta']['origin'] in ('imported', 'derived-from-import') for e in provenance):
        limitations.append('One or more inputs were imported. Source authenticity has not been verified.')
    if run['simulated']:
        limitations.append('SIMULATED DATA. This validation says nothing about an actual AWS account or local runtime.')
    return {'kind': 'validation_run', 'id': 'val-' + uuid4().hex[:16], 'revision': 1, 'title': f"Validation · {run['title']}", 'simulated': run['simulated'], 'data': {'run_ref': run_reference, 'scenario_ref': d['scenario_ref'], 'evaluator_version': VERSION, 'evaluated_at': now(), 'outcome': outcome, 'checks': checks, 'gates': gates, 'input_hashes': hashes, 'limitations': limitations}}
