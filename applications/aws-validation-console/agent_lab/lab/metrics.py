"""Measured exports and a Grafana dashboard for this implementation's instruments."""
import math
from copy import deepcopy
from .util import dt, Blocked

METRICS={
 'impact_to_task_seconds':('Impact to native or assisted investigation task','s'),
 'benign_investigations':('Exactly scoped investigations during healthy benign control','investigations'),
 'probe_bucket_coverage_ratio':('Probe measurement coverage','ratio'),
 'completed_probe_requests':('Completed controlled probe requests','requests'),
 'failed_probe_requests':('Failed controlled probe requests','requests'),
 'bad_probe_seconds':('Duration of unhealthy probe windows','s'),
 'probe_latency_p95_ms':('Observed request latency p95','ms'),
 'stable_recovery_seconds':('Impact to stable recovery','s'),
 'incident_to_task_seconds':('Receipt or alarm to investigation task','s'),
 'incident_to_summary_seconds':('Receipt or alarm to published summary','s'),
 'impact_to_first_adjudicated_correct_finding_seconds':('Impact to first adjudicated correct finding','s'),
}


def escape(value):
    return str(value).replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')


def _assessment(store, trial):
    """Export only a trial's own assessment and its pinned configuration."""
    reference = trial['data'].get('assessment_id')
    if not reference:
        return None
    record = store.record(reference)
    if (record['kind'] != 'assessment' or record['owner'] != trial['id']
            or record['data'].get('trial_id') != trial['id']):
        raise Blocked('Metrics assessment does not belong to the selected trial')
    binding = store.record(trial['data']['binding_record_id'])
    experiment = store.record(trial['data']['experiment_ref'])
    for source in (binding, experiment):
        if record['data'].get('input_hashes', {}).get(source['id']) != source['sha256']:
            raise Blocked('Metrics scope is not pinned by the assessment')
    b, e = binding['data'], experiment['data']
    fault = next(f for f in b['faults'] if f['id'] == e['fault_id'])
    labels = {
        'trial': trial['id'], 'arm': trial['data']['arm'],
        'campaign': trial['data'].get('fleet_campaign_id') or trial['data'].get('campaign_id') or 'standalone',
        'assessment': record['id'], 'mode': e['mode'],
        'workload_account': b['workload']['account_id'], 'workload_region': b['workload']['region'],
        'service': b['service_id'], 'agent_account': b['agent']['account_id'],
        'agent_region': b['agent']['region'], 'agent_space': b['agent_space_id'],
        'fis_template': fault['template_id'], 'template_revision': fault['template_sha256'],
    }
    return record['data'], b, ','.join(f'{k}="{escape(v)}"' for k, v in labels.items())


def _numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def prometheus(store):
    lines = ['# Frozen local measurements, not live service health. Missing data is absent.',
             '# These gauges are not native AWS/DevOps Agent metric names.']
    for key, (title, _) in METRICS.items():
        lines.extend(['# HELP agent_validation_' + key + ' ' + title,
                      '# TYPE agent_validation_' + key + ' gauge'])
    lines.extend([
        '# HELP agent_validation_business_value Collected business measurement; inspect the pinned requirement and unit.',
        '# TYPE agent_validation_business_value gauge',
        '# HELP agent_validation_observed_timestamp_seconds End of the underlying observation, not the scrape time.',
        '# TYPE agent_validation_observed_timestamp_seconds gauge'])
    for trial in store.entities('trial'):
        captured = _assessment(store, trial)
        if captured is None:
            continue
        body, binding, labels = captured
        for key, value in body['metrics'].items():
            if key in METRICS and _numeric(value):
                lines.append(f'agent_validation_{key}{{{labels}}} {float(value)}')
        for check in body.get('business_checks', []):
            value = check.get('observed')
            definition = body.get('metric_definitions', {}).get('business_' + check['id'], {})
            if _numeric(value):
                metric = next((m for m in binding.get('metrics', []) if m['id'] == check.get('metric_id')), {})
                account = metric.get('account_id') or binding['workload']['account_id']
                extra = (f'metric_account="{escape(account)}",requirement="{escape(check["id"])}",'
                         f'category="{escape(check["category"])}",unit="{escape(definition.get("unit", "unknown"))}"')
                lines.append(f'agent_validation_business_value{{{labels},{extra}}} {float(value)}')
        timestamp = trial['data'].get('observation_ends_at') or body['evaluated_at']
        lines.append(f'agent_validation_observed_timestamp_seconds{{{labels}}} {dt(timestamp).timestamp()}')
    return '\n'.join(lines) + '\n'


def dashboard(store=None):
    datasource={'type':'prometheus','uid':'${DS_PROMETHEUS}'}
    panels=[{'id':1,'type':'text','title':'Interpretation','gridPos':{'x':0,'y':0,'w':24,'h':4},
             'options':{'mode':'markdown','content':'Frozen trial measurements re-exposed on each scrape, **not live workload time series**. Always inspect observation age. No seeded observations. Empty series stay **No data**. Diagnosis depends on cited human claim extraction. Timing anchors and unresolved gates are in the console report. No chart proves agent-attributable recovery. Protect the authenticated scrape endpoint; do not publish local tokens.'}}]
    definitions={**METRICS,'observation_age_seconds':('Age of the underlying observation','s')}
    for i,(key,(title,unit)) in enumerate(definitions.items()):
        expression=f'agent_validation_{key}{{trial=~"${{trial:regex}}",agent_space=~"${{agent_space:regex}}"}}'
        if key=='observation_age_seconds': expression='time() - agent_validation_observed_timestamp_seconds{trial=~"${trial:regex}",agent_space=~"${agent_space:regex}"}'
        panels.append({'id':i+2,'type':'timeseries','title':title,'datasource':datasource,
                       'gridPos':{'x':12*(i%2),'y':4+8*(i//2),'w':12,'h':8},
                       'targets':[{'refId':'A','expr':expression,'legendFormat':'{{workload_account}}/{{service}} · {{agent_space}} · {{trial}} · {{assessment}}'}],
                       'fieldConfig':{'defaults':{'unit':'percentunit' if unit=='ratio' else unit,'noValue':'No data',
                                     'custom':{'spanNulls':False,'showPoints':'always','drawStyle':'points'}},'overrides':[]},
                       'options':{'tooltip':{'mode':'multi'},'legend':{'displayMode':'table','placement':'bottom'}}})
    if store is not None:
        requirements={}
        for trial in store.entities('trial'):
            ref=trial['data'].get('assessment_id')
            if not ref: continue
            body=store.record(ref)['data']
            for check in body.get('business_checks',[]):
                definition=body.get('metric_definitions',{}).get('business_'+check['id'],{})
                requirements[(check['id'],check['category'],definition.get('unit','unknown'))]=definition.get('title',check['id'])
        for offset,((requirement,category,unit),title) in enumerate(sorted(requirements.items())):
            panel=deepcopy(panels[1]);index=len(definitions)+offset
            panel['id']=index+2;panel['title']=title+' ['+unit+']'
            panel['gridPos']={'x':12*(index%2),'y':4+8*(index//2),'w':12,'h':8}
            panel['targets'][0]['expr']='agent_validation_business_value{trial=~"${trial:regex}",agent_space=~"${agent_space:regex}",requirement="'+escape(requirement)+'",category="'+escape(category)+'",unit="'+escape(unit)+'"}'
            panel['fieldConfig']['defaults']['unit']={'Count':'short','Seconds':'s','Milliseconds':'ms','Percent':'percent','Bytes':'bytes'}.get(unit,'none')
            panels.append(panel)
    return {'id':None,'uid':'devops-agent-validation-v051','title':'DevOps Agent · measured experiment results',
            'schemaVersion':39,'version':1,'timezone':'utc','time':{'from':'now-24h','to':'now'},'refresh':'30s','graphTooltip':2,
            'templating':{'list':[{'name':'DS_PROMETHEUS','type':'datasource','query':'prometheus'},
               {'name':'agent_space','label':'Agent Space','type':'query','datasource':datasource,
                'query':{'query':'label_values(agent_validation_observed_timestamp_seconds, agent_space)','refId':'agents'},
                'multi':True,'includeAll':True,'allValue':'.*','current':{'text':'All','value':'$__all'}},
               {'name':'trial','label':'Trial','type':'query','datasource':datasource,
                'query':{'query':'label_values(agent_validation_observed_timestamp_seconds, trial)','refId':'trials'},
                'multi':True,'includeAll':True,'allValue':'.*','current':{'text':'All','value':'$__all'}}]},'panels':panels}
