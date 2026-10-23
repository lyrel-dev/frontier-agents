"""Independent trial and paired-replay evaluation; no single readiness score.

Probe outcomes are reconstructed from captured requests. A journal's existence,
recommendation status, or FIS completion cannot establish business recovery.
Semantic claim extraction is attributed human input; equality against an oracle
is not presented as an autonomous assessment of natural-language correctness.
"""
from __future__ import annotations
import math
from datetime import timedelta
from .models import Experiment
from .util import dt, iso, digest, Blocked

VERSION='response-experiment-0.5.1'


def text_content(value):
    if isinstance(value,str): return value
    if isinstance(value,list): return '\n'.join(text_content(x) for x in value)
    if isinstance(value,dict): return '\n'.join(text_content(v) for v in value.values())
    return str(value)


def percentile(values, fraction):
    if not values: return None
    values=sorted(values)
    return values[max(0, math.ceil(fraction*len(values))-1)]


def buckets(probes, start, end, spec: Experiment, rate):
    start,end=dt(start),dt(end); result=[]
    cursor=start
    while cursor+timedelta(seconds=spec.bucket_seconds)<=end:
        stop=cursor+timedelta(seconds=spec.bucket_seconds)
        rows=[p for p in probes if cursor<=dt(p['scheduled_at'])<stop]
        attempted=[p for p in rows if p.get('attempted')]
        expected=spec.bucket_seconds*rate
        delivered=len(attempted)/expected
        late=any(p.get('missed') or p.get('scheduling_lag_seconds',0)>min(5,spec.bucket_seconds/2) for p in rows)
        complete=delivered>=spec.minimum_delivery_ratio and not late
        errors=sum(not p.get('success') for p in attempted)
        error_ratio=errors/len(attempted) if attempted else None
        p95=percentile([p['latency_ms'] for p in attempted if p.get('latency_ms') is not None],.95)
        healthy=bool(complete and error_ratio is not None and error_ratio<=spec.max_error_ratio and p95 is not None and p95<=spec.max_latency_ms)
        result.append({'at':iso(cursor),'end':iso(stop),'requests':len(attempted),'expected_requests':expected,
                       'delivery_ratio':delivered,'complete':complete,'errors':errors,'error_ratio':error_ratio,
                       'latency_p95_ms':p95,'healthy':healthy})
        cursor=stop
    return result


def result(outcome, reason, sources=None):
    return {'outcome':outcome,'reason':reason,'source_record_ids':sources or []}


def evaluate_trial(store, trial_id, binding):
    trial=store.entity(trial_id); data=trial['data']
    spec_record=store.record(data['experiment_ref']); spec=Experiment.model_validate(spec_record['data'])
    probe=next(p for p in binding.probes if p.id==spec.probe_id)
    records=store.records(trial_id); bykind={}
    for record in records: bykind.setdefault(record['kind'],[]).append(record)
    observations=bykind.get('observation',[])
    last=observations[-1]['data'] if observations else {}
    final_complete=bool(last.get('complete') and data.get('final_observation_id') and observations[-1]['id']==data['final_observation_id'])
    coverage_gaps=bykind.get('collection_error',[])+bykind.get('worker_gap',[])+bykind.get('observation_gap',[])
    source_set=[r['id'] for r in records]
    metrics={}; dimensions={}
    challenge=data.get('fault_confirmed',False) and data.get('targets_verified',False)
    if trial['state'] not in {'CLOSED','CLOSED_ABORTED','CLOSED_BLOCKED'}:
        dimensions['lifecycle']=result('inconclusive','Trial is not closed; this is an interim assessment.')
    elif trial['state']!='CLOSED':
        dimensions['lifecycle']=result('inconclusive','Aborted or blocked attempts remain in the denominator.')
    else: dimensions['lifecycle']=result('pass','The fixed observation interval and cleanup completed.')
    dimensions['challenge']=result('pass' if challenge else 'inconclusive',
        'Applied fault verified independently and exact resolved targets matched.' if challenge else 'Fault execution and intended effect are not both verified.')
    samples=store.probes(trial_id)
    probe_capture=store.put_record('probe_capture',trial_id,{'samples':samples,'samples_sha256':digest(samples)},'probe-capture-'+digest([trial_id,samples]))
    start=data.get('exposure_at'); end=data.get('observation_ends_at')
    rows=buckets(samples,start,end,spec,probe.requests_per_second) if start and end else []
    complete=bool(rows) and all(r['complete'] for r in rows) and not bykind.get('worker_gap')
    metrics['probe_bucket_coverage_ratio']=sum(r['complete'] for r in rows)/len(rows) if rows else None
    metrics['completed_probe_requests']=sum(r['requests'] for r in rows) if rows else None
    metrics['failed_probe_requests']=sum(r['errors'] for r in rows) if rows else None
    metrics['bad_probe_seconds']=sum(spec.bucket_seconds for r in rows if r['complete'] and not r['healthy']) if rows else None
    metrics['probe_latency_p95_ms']=percentile([p['latency_ms'] for p in samples if start and end and dt(start)<=dt(p['scheduled_at'])<dt(end) and p.get('attempted') and p.get('latency_ms') is not None],.95)
    bad=[r for r in rows if r['complete'] and not r['healthy']]
    impact=bad[0]['at'] if bad else None
    tail=[]
    for row in reversed(rows):
        if not row['healthy']: break
        tail.append(row)
    recovery=tail[-1]['at'] if impact and len(tail)*spec.bucket_seconds>=spec.stable_seconds else None
    metrics['stable_recovery_seconds']=(dt(recovery)-dt(impact)).total_seconds() if recovery else None
    dimensions['measurement']=result('pass' if complete else 'inconclusive',
        'Every probe bucket has the required real request delivery.' if complete else 'Insufficient traffic, late/missing probe slots or a worker gap prevents a complete measurement.')
    if not impact:
        dimensions['service_recovery']=result('not_eligible' if complete else 'inconclusive','No qualifying customer-path degradation was observed; do not invent a recovery duration.')
    elif recovery and complete:
        dimensions['service_recovery']=result('pass','The independently measured path returned to its stable healthy threshold under traffic.')
    else:
        dimensions['service_recovery']=result('fail' if complete else 'inconclusive','No verified trailing stable healthy interval under sufficient traffic.')
    alarms=[o['data']['alarm'] for o in observations if o['data'].get('alarm')]
    alarm=min(alarms,key=lambda x:x['at']) if alarms else None
    receipts=[o['data']['receipt'] for o in observations if o['data'].get('receipt')]
    receipt=min(receipts,key=lambda x:x['accepted_at']) if receipts else None
    tasks=[o['data']['task'] for o in observations if o['data'].get('task') and o['data'].get('correlation')!='ambiguous']
    task=min(tasks,key=lambda x:x['createdAt']) if tasks else None
    ambiguous=any(o['data'].get('correlation')=='ambiguous' for o in observations)
    delivery_failure=last.get('delivery_failure') if final_complete and not coverage_gaps else None
    if spec.mode=='assisted':
        dimensions['delivery']=result('not_assessed','Assisted investigation bypasses native incident delivery.')
    elif receipt:
        dimensions['delivery']=result('pass','The configured native integration emitted a correlated acceptance receipt. This is sender evidence, not independent AWS attestation.')
    elif delivery_failure and not task and not ambiguous:
        dimensions['delivery']=result('fail','The correlated sender recorded a final delivery rejection, with complete source reads. Agent reasoning is not assessed from this absence.')
    elif task and not ambiguous:
        dimensions['delivery']=result('inconclusive','An exactly correlated task exists, but independent delivery receipt evidence is absent.')
    else:
        dimensions['delivery']=result('inconclusive','Incident delivery is not proved; no task cannot be attributed solely to the agent.')
    metrics['impact_to_task_seconds']=(dt(task['createdAt'])-dt(impact)).total_seconds() if task and impact and dt(task['createdAt'])>=dt(impact) else None
    if data['arm']=='benign':
        scoped=last.get('benign_scope_complete') and final_complete and not coverage_gaps
        n=len(last.get('service_task_ids',[])) if scoped else None
        metrics['benign_investigations']=n
        if not complete or impact or not scoped or data.get('fis_id'):
            dimensions['benign_control']=result('inconclusive','A healthy fault-free window with complete exact service-reference enumeration is required. Dynamic reference contracts are not qualified here.')
        else:
            dimensions['benign_control']=result('pass' if n==0 and not alarm else 'fail','Counts native investigations and alarm transitions during this probe-healthy control, not all possible semantic false positives.')
    response_anchor=receipt['accepted_at'] if receipt else (alarm['at'] if alarm else impact)
    if impact and challenge:
        if task and not ambiguous and response_anchor:
            delay=(dt(task['createdAt'])-dt(response_anchor)).total_seconds()
            metrics['incident_to_task_seconds']=delay if delay>=0 else None
            dimensions['response']=result('inconclusive' if delay<0 else 'pass' if delay<=spec.response_deadline_seconds else 'fail',
                'Task creation is measured against '+('delivery receipt.' if receipt else 'alarm/impact; native delivery itself remains unverified.'))
        elif receipt and final_complete and not coverage_gaps and not ambiguous and end and (dt(end)-dt(receipt['accepted_at'])).total_seconds()>=spec.response_deadline_seconds:
            dimensions['response']=result('fail','Incident accepted, complete source reads, and no investigation before the fixed observation deadline.')
        else:
            dimensions['response']=result('inconclusive','Missing or ambiguous task correlation or collection gaps prevent a no-response verdict.')
    else: dimensions['response']=result('not_eligible' if complete and not impact else 'inconclusive','Positive response assessment requires a verified challenge and observed impact.')
    eligible_finding_ids={rid for o in observations for rid in o['data'].get('findings',[])}
    findings=[r for r in bykind.get('finding',[]) if r['id'] in eligible_finding_ids]
    summaries=[r for r in findings if r['data'].get('recordType')=='investigation_summary_md' and text_content(r['data'].get('content','')).strip()]
    if summaries and response_anchor:
        first=min(dt(r['data']['createdAt']) for r in summaries)
        metrics['incident_to_summary_seconds']=(first-dt(response_anchor)).total_seconds() if first>=dt(response_anchor) else None
    reviews=bykind.get('diagnosis',[])
    valid_reviews=[]
    for review in reviews:
        body=review['data']; finding=store.record(body['finding_record_id'])
        if finding['id'] not in eligible_finding_ids: continue
        semantic=body['asserted_mechanism_code']==spec.oracle.mechanism_code and set(body['asserted_resource_arns'])==set(spec.oracle.affected_resource_arns)
        semantic=semantic and not body['material_unsupported_claims']
        valid_reviews.append((review,semantic,finding))
    if valid_reviews and challenge:
        # A selected review is explicit. Later contradictory reviews do not silently overwrite history.
        selected=data.get('diagnosis_review_id')
        chosen=next((v for v in valid_reviews if v[0]['id']==selected),None)
        if chosen:
            dimensions['diagnosis']=result('pass' if chosen[1] else 'fail','Attributed structured extraction compared with the frozen oracle; semantic extraction remains a human judgment.',[chosen[0]['id'],chosen[2]['id']])
            correct=[v for v in valid_reviews if v[1]]
            if correct and impact:
                timestamp=min(dt(v[2]['data']['createdAt']) for v in correct)
                metrics['impact_to_first_adjudicated_correct_finding_seconds']=(timestamp-dt(impact)).total_seconds() if timestamp>=dt(impact) else None
        else: dimensions['diagnosis']=result('inconclusive','Select an explicit claim review; reviews are not automatically chosen by recency.')
    else: dimensions['diagnosis']=result('not_assessed','No grounded, cited structured diagnosis assessment is selected.')
    changes=[c for c in store.entities('change') if c['data'].get('trial_id')==trial_id]
    verified=[c for c in changes if c['state']=='VERIFIED']
    dimensions['intervention']=result('pass' if verified else 'not_assessed','An approved runbook changed the verified state.' if verified else 'No verified approved intervention executed.')
    temporal=False
    if recovery:
        for change in verified:
            if dt(change['data']['verified_at'])<=dt(recovery) and data.get('fault_end_at') and dt(recovery)<dt(data['fault_end_at']): temporal=True
    dimensions['attribution']=result('association_only' if temporal else 'not_established',
        'Recovery followed a verified agent-linked intervention while the fault remained active; uncontrolled confounders still prevent a causal claim.' if temporal else 'Observed recovery is not credited to the agent. Fault expiry, automatic recovery and human actions are alternatives.')
    dimensions['cleanup']=result('pass' if data.get('cleanup_verified') else 'fail' if trial['state']=='RESTORE_REQUIRED' else 'inconclusive',
        'Independent configured restoration checks passed.' if data.get('cleanup_verified') else 'Restoration is not verified; independent recovery may be required.')
    from .business import evaluate as evaluate_business
    business_checks,business_dimensions=evaluate_business(spec.business_requirements,last,closed=final_complete and trial['state']=='CLOSED',source_id=data.get('final_observation_id'))
    dimensions.update(business_dimensions)
    from .metrics import METRICS
    metric_definitions={k:{'title':v[0],'unit':v[1]} for k,v in METRICS.items()}
    for check in business_checks:
        metrics['business_'+check['id']]=check['observed']
        instrument=next(m for m in binding.metrics if m.id==check['metric_id'])
        metric_definitions['business_'+check['id']]={'title':instrument.title+' · '+check['aggregation'],'unit':instrument.unit,'requirement_id':check['id'],'category':check['category']}
    # Whole-window graphs and summaries derive only from captured observations.
    inputs={r['id']:r['sha256'] for r in records}
    inputs[spec_record['id']]=spec_record['sha256']
    binding_record=store.record(data['binding_record_id'])
    if binding_record['sha256']!=digest(binding.model_dump(mode='json')):
        raise Blocked('Assessment binding differs from the pinned trial configuration')
    inputs[binding_record['id']]=binding_record['sha256']
    inputs[probe_capture['id']]=probe_capture['sha256']
    body={'version':VERSION,'trial_id':trial_id,'lifecycle':trial['state'],'dimensions':dimensions,'metrics':metrics,
          'business_checks':business_checks,'metric_definitions':metric_definitions,'probe_buckets':rows,'impact_at':impact,'recovery_at':recovery,'native_alarm_at':alarm['at'] if alarm else None,
          'input_hashes':inputs,'probe_input_sha256':digest(samples),'probe_capture_id':probe_capture['id'],'evaluated_at':iso(),
          'limitations':['Results cover this authorized exposure, not general competence or production readiness.',
                         'No automatic causal credit is awarded to the agent.',
                         'Cited structured diagnostic claims use attributed human extraction, not an objective language-understanding oracle.',
                         'Local hashes detect consistency changes; they do not sign producer identity.']}
    record=store.put_record('assessment',trial_id,body)
    store.update(trial_id,changes={'assessment_id':record['id']},event='trial.assessed')
    return record


def compare_campaign(store,campaign_id,binding):
    campaign=store.entity(campaign_id); data=campaign['data']; spec=data['comparison']
    trials=[t for t in store.entities('trial') if t['data'].get('campaign_id')==campaign_id]
    eligible=[]; excluded=[]; controls=[]
    for trial in sorted(trials,key=lambda x:x['data'].get('started_at','')):
        aid=trial['data'].get('assessment_id')
        if trial['state']!='CLOSED' or not aid:
            excluded.append({'trial_id':trial['id'],'reason':'Not closed with an assessment'}); continue
        assessment=store.record(aid)
        d=assessment['data']['dimensions']
        if trial['data']['arm']=='benign':
            controls.append((trial,assessment)); continue
        if d['challenge']['outcome']!='pass' or d['measurement']['outcome']!='pass' or d['cleanup']['outcome']!='pass' or trial['data'].get('fault_state')!='completed':
            excluded.append({'trial_id':trial['id'],'reason':'Challenge, measurement, FIS completion or cleanup not qualified'}); continue
        if trial['data']['experiment_ref']!=data['experiment_ref']:
            excluded.append({'trial_id':trial['id'],'reason':'Different experiment revision'}); continue
        eligible.append((trial,assessment))
    base=[x for x in eligible if x[0]['data']['arm']=='baseline']
    treated=[x for x in eligible if x[0]['data']['arm']=='treatment']
    pairs=[]; blockers=[]
    change_id=data.get('change_id'); change=store.entity(change_id) if change_id else None
    if not data.get('recommendation_record_id') or not change or change['state']!='VERIFIED':
        blockers.append('No version-pinned recommendation linked to a verified implementation')
    for (baseline,ba),(replay,ra) in zip(base,treated):
        reasons=[]
        b,r=baseline['data'],replay['data']; bm,rm=ba['data']['metrics'],ra['data']['metrics']
        if b.get('resolved_target_arns')!=r.get('resolved_target_arns'): reasons.append('Resolved targets differ; automatic equivalence is not assumed')
        if b.get('binding_sha256')!=r.get('binding_sha256'): reasons.append('Instrument configuration changed')
        if not change or r.get('prevention_change_id')!=change_id or not r.get('change_still_verified'): reasons.append('Replay did not verify the linked changed state before and after exposure')
        if change and dt(b.get('closed_at',baseline['updated_at']))>=dt(change['data']['verified_at']): reasons.append('Baseline occurred after the implementation')
        traffic=bm.get('completed_probe_requests') or 0
        if not traffic or abs((rm.get('completed_probe_requests') or 0)-traffic)/traffic>spec['traffic_tolerance']: reasons.append('Delivered workload differs beyond the pre-registered tolerance')
        bd,rd=b.get('fault_duration_seconds'),r.get('fault_duration_seconds')
        if not bd or not rd or abs(rd-bd)/bd>spec['traffic_tolerance']: reasons.append('Actual fault duration is not comparable')
        if bm.get('failed_probe_requests',0)==0 and bm.get('bad_probe_seconds',0)==0: reasons.append('Baseline did not reproduce impact')
        configured_business=ra['data'].get('business_checks',[])
        if any(c['outcome']=='inconclusive' for c in configured_business):reasons.append('Required replay business/collateral evidence is incomplete')
        outcome='inconclusive'; reason='; '.join(reasons)
        if not reasons:
            bl,rl=bm.get('probe_latency_p95_ms'),rm.get('probe_latency_p95_ms')
            # Post-change latency is compared with baseline full-window latency;
            # per-bucket service limits independently guard healthy periods.
            regression=bl is not None and rl is not None and rl>bl*(1+spec['maximum_latency_regression_ratio'])
            if spec['claim']=='prevent_recurrence':
                ok=rm['bad_probe_seconds']==0 and rm['failed_probe_requests']==0 and not regression
                outcome='pass' if ok else 'fail'; reason='No recurrence in the matched measured challenge.' if ok else 'Impact recurred or the regression budget was exceeded.'
            elif spec['claim']=='reduce_impact':
                denominator=bm['bad_probe_seconds']
                improvement=(denominator-rm['bad_probe_seconds'])/denominator if denominator else None
                ok=improvement is not None and improvement>=spec['minimum_improvement'] and not regression
                outcome='pass' if ok else 'fail'; reason='Matched bad-probe-duration improvement: '+str(improvement)
            else:
                negatives=[(t,a) for t,a in controls if t['data'].get('prevention_change_id')==change_id and t['data'].get('change_still_verified')
                    and a['data']['dimensions'].get('benign_control',{}).get('outcome') in {'pass','fail'}
                    and a['data']['dimensions']['measurement']['outcome']=='pass' and a['data']['dimensions']['cleanup']['outcome']=='pass']
                bt,rt=bm.get('impact_to_task_seconds'),rm.get('impact_to_task_seconds')
                if not negatives or bt is None or rt is None or bt<=0:
                    outcome='inconclusive'; reason='Earlier investigation requires measured impact-to-task durations and a qualified post-change benign control.'
                else:
                    alerts=max(a['data']['metrics']['benign_investigations'] for t,a in negatives)
                    alarmed=any(a['data'].get('native_alarm_at') for t,a in negatives)
                    improvement=(bt-rt)/bt
                    ok=improvement>=spec['minimum_improvement'] and alerts<=spec['maximum_benign_investigations'] and not alarmed and not regression
                    outcome='pass' if ok else 'fail'; reason='Impact-to-native-investigation improvement: '+str(improvement)+'; benign investigations: '+str(alerts)+'. This is earlier investigation, not proof of autonomous detection.'
        if not reasons and any(c['outcome']=='fail' for c in configured_business):
            outcome='fail';reason='Replay failed a required business-data or collateral-regression check.'
        pairs.append({'baseline_trial':baseline['id'],'replay_trial':replay['id'],
                      'baseline_assessment':ba['id'],'replay_assessment':ra['id'],'outcome':outcome,'reason':reason,
                      'baseline_metrics':bm,'replay_metrics':rm})
    paired={p[k] for p in pairs for k in ('baseline_trial','replay_trial')}
    for trial,assessment in eligible:
        if trial['id'] not in paired: excluded.append({'trial_id':trial['id'],'reason':'No paired opposite-arm attempt in chronological order'})
    if len(pairs)<spec['minimum_pairs']: blockers.append('Fewer matched pairs than required by the registered plan')
    if any(p['outcome']=='fail' for p in pairs): outcome='fail'
    elif blockers or not pairs or any(p['outcome']!='pass' for p in pairs): outcome='inconclusive'
    else: outcome='pass'
    pinned={data['experiment_ref'],data['binding_record_id']}
    if data.get('recommendation_record_id'):pinned.add(data['recommendation_record_id'])
    if change and change['data'].get('verification_id'):pinned.add(change['data']['verification_id'])
    for pair in pairs:pinned.update([pair['baseline_assessment'],pair['replay_assessment']])
    for trial,assessment in controls:pinned.add(assessment['id'])
    input_hashes={rid:store.record(rid)['sha256'] for rid in pinned}
    record=store.put_record('comparison',campaign_id,{'version':VERSION,'campaign_id':campaign_id,'claim':spec['claim'],
        'outcome':outcome,'blockers':blockers,'pairs':pairs,'excluded_attempts':excluded,'all_trial_ids':[t['id'] for t in trials],
        'recommendation_record_id':data.get('recommendation_record_id'),'change_id':change_id,
        'plan_sha256':digest(spec),'input_hashes':input_hashes,'benign_controls':[{'trial_id':t['id'],'assessment_id':a['id']} for t,a in controls],'evaluated_at':iso(),
        'limitations':['A paired before/after result is evidence for this challenge, not randomized causal proof.',
                       'Agent Space history is not reset; carryover and learning are uncontrolled.',
                       'Resource replacements require a separately reviewed equivalence design; no implicit matching.',
                       'Failed, interrupted and unqualified attempts are retained and disclosed.']})
    store.update(campaign_id,changes={'comparison_id':record['id']},event='campaign.compared')
    return record
