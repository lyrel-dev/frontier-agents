"""Measured exports and a Grafana dashboard for this implementation's instruments."""
from .util import dt

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


def prometheus(store):
    lines=['# Local derived measurements. Missing data is absent, not zero.',
           '# These gauges are not native AWS/DevOps Agent metric names.']
    for key,(title,_) in METRICS.items():
        lines.extend(['# HELP agent_validation_'+key+' '+title,'# TYPE agent_validation_'+key+' gauge'])
    for trial in store.entities('trial'):
        ref=trial['data'].get('assessment_id')
        if not ref: continue
        body=store.record(ref)['data']; labels=f'trial="{escape(trial["id"])}",arm="{escape(trial["data"]["arm"])}",campaign="{escape(trial["data"].get("campaign_id") or "standalone")}"'
        for key,val in body['metrics'].items():
            if key in METRICS and val is not None:
                lines.append(f'agent_validation_{key}{{{labels}}} {float(val)}')
        timestamp=trial['data'].get('observation_ends_at') or body['evaluated_at']
        lines.append(f'agent_validation_observed_timestamp_seconds{{{labels}}} {dt(timestamp).timestamp()}')
    return '\n'.join(lines)+'\n'


def dashboard():
    datasource={'type':'prometheus','uid':'${DS_PROMETHEUS}'}
    panels=[{'id':1,'type':'text','title':'Interpretation','gridPos':{'x':0,'y':0,'w':24,'h':4},
             'options':{'mode':'markdown','content':'Measured local experiment outputs. No seeded observations. Empty series stay **No data**. Diagnosis depends on cited human claim extraction. Timing anchors and unresolved gates are in the console report. No chart proves agent-attributable recovery. Protect the authenticated scrape endpoint; do not publish local tokens.'}}]
    definitions={**METRICS,'observation_age_seconds':('Age of the underlying observation','s')}
    for i,(key,(title,unit)) in enumerate(definitions.items()):
        expression=f'agent_validation_{key}{{trial=~"${{trial:regex}}"}}'
        if key=='observation_age_seconds': expression='time() - agent_validation_observed_timestamp_seconds{trial=~"${trial:regex}"}'
        panels.append({'id':i+2,'type':'timeseries','title':title,'datasource':datasource,
                       'gridPos':{'x':12*(i%2),'y':4+8*(i//2),'w':12,'h':8},
                       'targets':[{'refId':'A','expr':expression,'legendFormat':'{{campaign}} · {{trial}} · {{arm}}'}],
                       'fieldConfig':{'defaults':{'unit':'percentunit' if unit=='ratio' else unit,'noValue':'No data',
                                     'custom':{'spanNulls':False,'showPoints':'always','drawStyle':'points'}},'overrides':[]},
                       'options':{'tooltip':{'mode':'multi'},'legend':{'displayMode':'table','placement':'bottom'}}})
    return {'id':None,'uid':'devops-agent-validation-v03','title':'DevOps Agent · measured experiment results',
            'schemaVersion':39,'version':1,'timezone':'utc','time':{'from':'now-24h','to':'now'},'refresh':'30s','graphTooltip':2,
            'templating':{'list':[{'name':'DS_PROMETHEUS','type':'datasource','query':'prometheus'},
               {'name':'trial','label':'Trial','type':'query','datasource':datasource,
                'query':{'query':'label_values(agent_validation_observed_timestamp_seconds, trial)','refId':'trials'},
                'multi':True,'includeAll':True,'allValue':'.*','current':{'text':'All','value':'$__all'}}]},'panels':panels}
