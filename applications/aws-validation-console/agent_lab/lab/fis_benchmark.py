"""Pinned, stratified agent-response benchmarks. No success-only leaderboard."""
from __future__ import annotations
from collections import Counter
import csv
import io
import math
from statistics import median
from .metrics import METRICS
from .util import Blocked, digest, iso


def percentile(values, quantile):
    if not values: return None
    data = sorted(values)
    return data[max(0, math.ceil(len(data)*quantile)-1)]


def benchmark(store, identifier):
    campaign = store.entity(identifier)
    if campaign['kind'] != 'fis_campaign': raise Blocked('Select a FIS response campaign')
    plan_record = store.record(campaign['data']['plan_id']); plan = plan_record['data']
    hashes = {plan_record['id']:plan_record['sha256']}; visited = set()
    def verify(rid, expected=None):
        record = store.record(rid)
        if expected is not None and record['sha256'] != expected: raise Blocked('Benchmark evidence hash mismatch')
        if rid in visited: return record
        if len(visited) >= 50000: raise Blocked('Benchmark dependency limit reached')
        visited.add(rid); hashes[rid] = record['sha256']
        for child, sha in record['data'].get('input_hashes', {}).items(): verify(child,sha)
        return record
    verify(plan_record['id'])
    attempts=[]; groups={}
    # Enumerate every planned attempt, including those never dispatched.
    for slot in range(campaign['data']['total']):
        entry = plan['entries'][slot % len(plan['entries'])]
        tid = identifier + '-trial-' + str(slot)
        try: trial = store.entity(tid)
        except KeyError: trial = None
        assessment = None; reason = None
        if trial and trial['data'].get('assessment_id'):
            assessment = verify(trial['data']['assessment_id'])
            if (assessment['kind'] != 'assessment' or assessment['owner'] != tid
                    or assessment['data'].get('trial_id') != tid):
                raise Blocked('Assessment belongs to another exposure')
        if trial and (trial['data']['experiment_ref'] != entry['experiment_ref']
                      or trial['data']['binding_sha256'] != entry['binding_sha256']):
            raise Blocked('Trial no longer matches its registered benchmark slot')
        dimensions = assessment['data']['dimensions'] if assessment else {}
        qualified = bool(trial and trial['state']=='CLOSED' and trial['data'].get('fault_state')=='completed' and assessment and
            all(dimensions.get(k,{}).get('outcome')=='pass' for k in ('challenge','measurement','cleanup','delivery')))
        outcome = dimensions.get('response',{}).get('outcome','not_assessed')
        if not qualified: reason = 'Closed exposure, independent effect, complete measurement, native delivery and cleanup are required.'
        specification=verify(entry['experiment_ref'])['data']
        binding_record=verify(entry['binding_record_id'])['data']
        business_definitions={}
        for requirement in specification.get('business_requirements',[]):
            instrument=next(m for m in binding_record['metrics'] if m['id']==requirement['metric_id'])
            business_definitions['business_'+requirement['id']]=(instrument['title']+' · '+requirement['aggregation'],instrument['unit'])
        agent_key = ':'.join([entry['agent_account'],entry['agent_region'],entry['agent_space_id']])
        group_key = entry['cohort_id'] + ':' + agent_key
        row={'slot':slot,'trial_id':tid if trial else None,'agent':agent_key,
             'cohort_id':entry['cohort_id'],'account_id':entry['account_id'],'region':entry['region'],
             'template_id':entry['template_id'],'template_sha256':entry['template_sha256'],
             'state':trial['state'] if trial else 'NOT_STARTED', 'qualified':qualified,
             'business_outcomes':{k:v.get('outcome') for k,v in dimensions.items() if k in ('data_correctness','collateral_regression','application')},
             'response_outcome':outcome,'diagnosis_outcome':dimensions.get('diagnosis',{}).get('outcome','not_assessed'),
             'assessment_id':assessment['id'] if assessment else None,
             'at':assessment['data']['evaluated_at'] if assessment else (trial['updated_at'] if trial else None),
             'started_at':trial['data'].get('started_at') if trial else None,
             'fault_duration_seconds':trial['data'].get('fault_duration_seconds') if trial else None,
             'trial_projection':trial,
             'metrics':assessment['data']['metrics'] if assessment else {}, 'metric_definitions':business_definitions, 'exclusion_reason':reason,
             'provider_experiment_id':trial['data'].get('fis_id') if trial else None}
        attempts.append(row)
        g=groups.setdefault(group_key,{'cohort_id':entry['cohort_id'],'agent':agent_key,'agent_label':entry['agent_label'],
            'template_id':entry['template_id'],'account_id':entry['account_id'],'region':entry['region'],'attempts':[]})
        g['attempts'].append(row)
    # Compare actual exposure and delivered requests against the first qualified
    # attempt per registered cohort, before summarizing any agent statistics.
    references = {}
    for row in attempts:
        if not row['qualified']:
            continue
        duration = row['fault_duration_seconds']
        requests = row['metrics'].get('completed_probe_requests')
        if not isinstance(duration,(int,float)) or duration <= 0 or not requests:
            row['qualified'] = False
            row['exclusion_reason'] = 'Actual FIS duration and delivered workload must be measured.'
            continue
        ref = references.setdefault(row['cohort_id'], row)
        tolerance = plan.get('comparability_tolerance', .1)
        if (abs(duration-ref['fault_duration_seconds'])/ref['fault_duration_seconds'] > tolerance
                or abs(requests-ref['metrics']['completed_probe_requests'])/ref['metrics']['completed_probe_requests'] > tolerance):
            row['qualified'] = False
            row['exclusion_reason'] = 'Actual exposure or delivered workload differs from the first qualified cohort attempt beyond the registered tolerance.'
        row['comparison_reference_trial'] = ref['trial_id']
    summaries=[]
    for group in groups.values():
        rows=group.pop('attempts'); eligible=[r for r in rows if r['qualified']]
        responses=Counter(r['response_outcome'] for r in eligible)
        measured={}
        for name, (title,unit) in {**METRICS,**(rows[0]['metric_definitions'] if rows else {})}.items():
            samples=[r['metrics'][name] for r in eligible if isinstance(r['metrics'].get(name),(int,float))
                     and not isinstance(r['metrics'][name],bool) and math.isfinite(r['metrics'][name])]
            measured[name]={'title':title,'unit':unit,'n':len(samples),'missing':len(eligible)-len(samples),
                            'median':median(samples) if samples else None,'p95_nearest_rank':percentile(samples,.95)}
        summaries.append({**group,'planned':len(rows),'registered':sum(r['state']!='NOT_STARTED' for r in rows),'started':sum(bool(r['started_at']) for r in rows),
            'qualified':len(eligible),'excluded_or_pending':len(rows)-len(eligible),'response_outcomes':dict(responses),
            'diagnosis_outcomes':dict(Counter(r['diagnosis_outcome'] for r in eligible)),
            'business_outcomes':{k:dict(Counter(r['business_outcomes'].get(k,'not_assessed') for r in eligible)) for k in ('data_correctness','collateral_regression','application')},
            'response_pass_fraction':responses['pass']/len(eligible) if eligible else None,
            'no_response_failures':sum(r['response_outcome']=='fail' and r['metrics'].get('incident_to_task_seconds') is None for r in eligible),
            'statistics':measured})
    body={'schema':'fis-agent-benchmark/v1','campaign_id':identifier,'plan_id':plan_record['id'],
          'generated_at':iso(),'campaign_state':campaign['state'],'attempts':attempts,'groups':summaries,
          'input_hashes':hashes,'campaign_projection':campaign,
          'limits':['Sequential real exposures; not simultaneous observation or randomized causal comparison.',
                    'Different account/service/template/workload/requirement cohorts are never pooled.',
                    'Latency quantiles condition on available measurements. Missing/no-response attempts are counted separately, never zero-filled.',
                    'Small-n p95 uses nearest rank and is descriptive, not a confidence guarantee.',
                    'Native task creation is not proof of correct diagnosis, remediation or prevention.',
                    'Agent knowledge carryover and trial order are retained in the plan; no reset of agent memory is assumed.',
                    'Source hashes detect inconsistency, not independently authenticated producer identity.']}
    return store.put_record('fis_benchmark',identifier,body)


def benchmark_csv(record):
    extra=sorted({k for r in record['data']['attempts'] for k in r.get('metric_definitions',{})})
    metric_fields=[*METRICS,*extra]
    out=io.StringIO(); fields=['slot','trial_id','agent','cohort_id','account_id','region','template_id','state',
                            'qualified','response_outcome','diagnosis_outcome','assessment_id','exclusion_reason','data_correctness','collateral_regression','application',*metric_fields]
    writer=csv.DictWriter(out,fieldnames=fields);writer.writeheader()
    for row in record['data']['attempts']:
        values={k:row.get(k) for k in fields};values.update({k:row['metrics'].get(k) for k in metric_fields})
        values.update({k:row.get('business_outcomes',{}).get(k,'not_assessed') for k in ('data_correctness','collateral_regression','application')})
        for key,value in values.items():
            if isinstance(value,str) and value.startswith(('=','+','-','@','\t','\r')): values[key]="'"+value
        writer.writerow(values)
    return out.getvalue()
