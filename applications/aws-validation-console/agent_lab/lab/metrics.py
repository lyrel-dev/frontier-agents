"""Measured exports and a Grafana dashboard for this implementation's instruments."""
import math
from copy import deepcopy
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
    lines.extend(['# HELP agent_validation_business_value Collected scalar business requirement measurement; inspect the pinned requirement and unit.', '# TYPE agent_validation_business_value gauge'])
    for trial in store.entities('trial'):
        ref=trial['data'].get('assessment_id')
        if not ref: continue
        body=store.record(ref)['data']; labels=f'trial="{escape(trial["id"])}",arm="{escape(trial["data"]["arm"])}",campaign="{escape(trial["data"].get("campaign_id") or "standalone")}"'
        for key,val in body['metrics'].items():
            if key in METRICS and val is not None:
                lines.append(f'agent_validation_{key}{{{labels}}} {float(val)}')
        for check in body.get('business_checks',[]):
            value=check.get('observed'); definition=body.get('metric_definitions',{}).get('business_'+check['id'],{})
            if isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value):
                extra=f'requirement="{escape(check["id"])}",category="{escape(check["category"])}",unit="{escape(definition.get("unit","unknown"))}"'
                lines.append(f'agent_validation_business_value{{{labels},{extra}}} {float(value)}')
        timestamp=trial['data'].get('observation_ends_at') or body['evaluated_at']
        lines.append(f'agent_validation_observed_timestamp_seconds{{{labels}}} {dt(timestamp).timestamp()}')
    return '\n'.join(lines)+'\n'


def dashboard(store=None):
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
            panel['targets'][0]['expr']='agent_validation_business_value{trial=~"${trial:regex}",requirement="'+escape(requirement)+'",category="'+escape(category)+'",unit="'+escape(unit)+'"}'
            panel['fieldConfig']['defaults']['unit']={'Count':'short','Seconds':'s','Milliseconds':'ms','Percent':'percent','Bytes':'bytes'}.get(unit,'none')
            panels.append(panel)
    return {'id':None,'uid':'devops-agent-validation-v05','title':'DevOps Agent · measured experiment results',
            'schemaVersion':39,'version':1,'timezone':'utc','time':{'from':'now-24h','to':'now'},'refresh':'30s','graphTooltip':2,
            'templating':{'list':[{'name':'DS_PROMETHEUS','type':'datasource','query':'prometheus'},
               {'name':'trial','label':'Trial','type':'query','datasource':datasource,
                'query':{'query':'label_values(agent_validation_observed_timestamp_seconds, trial)','refId':'trials'},
                'multi':True,'includeAll':True,'allValue':'.*','current':{'text':'All','value':'$__all'}}]},'panels':panels}
