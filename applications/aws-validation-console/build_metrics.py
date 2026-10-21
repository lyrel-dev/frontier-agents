"""Generate the metric catalogue, synthetic example bundle and proposed Grafana dashboard.
Generated assets are reproducible; no network calls or live measurements are made.
"""
from __future__ import annotations
import json, math
from datetime import datetime, timedelta, timezone
from pathlib import Path
ROOT = Path(__file__).resolve().parent
# key, title, unit, group, measurement contract, synthetic baseline, incident peak
DEFINITIONS = [
 ('request_rate','Completed request rate','requests/second','Customer impact','Completed requests per second for the selected workload; retain offered-load evidence separately.',480,290),
 ('request_error_ratio','Request error ratio','ratio','Customer impact','Failed completed requests divided by all completed requests in the same window and population. A zero denominator is missing, not zero errors.',.002,.09),
 ('availability_ratio','Successful transaction ratio','ratio','Customer impact','Successful synthetic business transactions divided by attempted transactions. This is not infrastructure uptime.',.998,.91),
 ('latency_p95_ms','Request latency · p95','milliseconds','Customer impact','95th percentile from the combined request histogram for the same window; do not average per-instance percentiles.',180,940),
 ('latency_p99_ms','Request latency · p99','milliseconds','Customer impact','99th percentile from the combined request histogram. Preserve failed and timed-out requests separately.',290,1700),
 ('detection_seconds','Time to detection','seconds','Response and recovery','First qualifying detection minus verified customer-impact start. Per incident, not MTTD. Unaffected or undetected incidents have no duration.',42,42),
 ('alert_delivery_seconds','Alert delivery delay','seconds','Response and recovery','Verified alert delivery minus qualifying detection. A missing delivery event is not a zero delay.',18,18),
 ('acknowledgement_seconds','Time to acknowledgement','seconds','Response and recovery','Responder acknowledgement minus verified alert delivery. Use incident-system timestamps, not dashboard views.',75,75),
 ('mitigation_seconds','Time to mitigation','seconds','Response and recovery','Verified containment of customer impact minus incident start. Specify the containment criterion.',170,170),
 ('recovery_seconds','Time to stable recovery','seconds','Response and recovery','Start of a verified stable-recovery interval minus incident start. Record the stability window; a healthy resource alone is insufficient.',240,240),
 ('rto_seconds','Recovery time objective','seconds','Response and recovery','Service-owned recovery objective for the tested business capability. This is a target, not an observed outcome.',180,180),
 ('data_loss_seconds','Observed recovery-point loss','seconds','Data and dependencies','Recoverable business-state lag at the disruption cut-off, established from a verified recovery boundary and acknowledged-write reconciliation. Record lost-write counts separately.',0,0),
 ('rpo_seconds','Recovery point objective','seconds','Data and dependencies','Service-owned allowable data-loss interval. Zero is an objective only when explicitly agreed.',0,0),
 ('duplicate_transactions','Duplicate business effects','transactions','Data and dependencies','Duplicate business effects found by reconciliation in the selected execution window, not the count of retried requests.',0,0),
 ('lost_acknowledged_writes','Lost acknowledged writes','transactions','Data and dependencies','Writes acknowledged before disruption but absent after recovery, measured with an independent reconciliation source.',0,0),
 ('queue_depth','Unprocessed messages','messages','Data and dependencies','Messages waiting for processing in the selected queue; retries and dead-letter messages need separate accounting.',12,820),
 ('queue_oldest_age_seconds','Oldest unprocessed message','seconds','Data and dependencies','Age of the oldest waiting message; it is not the average processing latency.',2,210),
 ('retry_amplification_ratio','Attempts per original operation','attempts/operation','Data and dependencies','Total attempts divided by original operations for the same window. Never divide by successful operations.',1.01,3.1),
 ('db_reconnect_seconds','Database reconnection time','seconds','Data and dependencies','First successful application transaction after failover minus verified database interruption.',62,62),
 ('capacity_restoration_seconds','Capacity restoration time','seconds','Capacity and saturation','Restoration of the specified healthy-capacity target minus confirmed capacity loss. Retain the target and readiness criterion.',210,210),
 ('healthy_capacity_ratio','Healthy capacity fraction','ratio','Capacity and saturation','Ready, traffic-serving capacity divided by the specified required capacity. Desired replicas are not ready replicas.',1,.62),
 ('cpu_utilization_ratio','CPU utilization','ratio','Capacity and saturation','Used CPU divided by the stated CPU capacity. Specify allocated versus host capacity; do not average incompatible denominators.',.42,.94),
 ('memory_utilization_ratio','Memory utilization','ratio','Capacity and saturation','Used memory divided by the stated limit or physical capacity. Preserve the denominator definition.',.54,.91),
 ('throttled_requests_ratio','Throttled request ratio','ratio','Capacity and saturation','Throttled attempts divided by all attempts in the same request population and window.',.001,.14),
 ('restart_count','Workload restarts','restarts','Capacity and saturation','Restarts in the specified window, computed from a reset-aware counter or event records. Not a lifetime total.',0,4),
 ('runbook_completion_ratio','Runbook steps completed','ratio','Operational evidence','Successfully verified required steps divided by all applicable required steps. A clicked checklist is not execution evidence.',.8,.8),
 ('automatic_recovery_ratio','Automatic recovery success','ratio','Operational evidence','Automatically recovered eligible incidents divided by all eligible incidents in an explicit comparable cohort; not a per-request ratio.',.75,.75),
 ('error_budget_consumed_ratio','Error budget consumed','ratio','Operational evidence','Bad events attributable to the experiment divided by the allocated budget for its declared SLO window. May exceed 1.',.04,.04),
 ('evidence_coverage_ratio','Required evidence coverage','ratio','Operational evidence','Required checks with usable evidence divided by all required checks. Coverage alone is not a passing validation.',.75,.75),
 ('incomplete_scope_count','Incomplete collection scopes','scopes','Operational evidence','Denied, errored, truncated or missing requested scopes. Zero says collection completed, not that the application is healthy.',1,1),
 ('telemetry_lag_seconds','Telemetry collection lag','seconds','Operational evidence','Collection timestamp minus the end of the measurement window; distinguish transport delay from stale observations.',4,45),
 ('fault_active','Confirmed fault active','boolean','Operational evidence','True only during a confirmed fault interval. It describes injection state, not the presence or absence of customer impact.',0,1),
]
MODELS = ['ec2','eks-ec2','eks-fargate','ecs-ec2','ecs-fargate','lambda','docker','podman','kubernetes']
SOURCES = [
 ('Grafana time-series panels','https://grafana.com/docs/grafana/latest/visualizations/panels-visualizations/visualizations/time-series/'),
 ('Grafana dashboard JSON models','https://grafana.com/docs/grafana/latest/visualizations/dashboards/build-dashboards/view-dashboard-json-model/'),
 ('Grafana provisioning','https://grafana.com/docs/grafana/latest/administration/provisioning/'),
 ('Prometheus template variables','https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/'),
 ('PromQL functions','https://prometheus.io/docs/prometheus/latest/querying/functions/'),
 ('Histogram aggregation','https://prometheus.io/docs/practices/histograms/'),
]
LABELS = ['environment','service','deployment_model','scenario','run_id','data_kind']
SELECTOR = ','.join(f'{k}=~"${{{k}:regex}}"' for k in LABELS)

def catalogue():
    result=[]
    for key,title,unit,group,description,base,peak in DEFINITIONS:
        result.append(dict(metric=key,title=title,unit=unit,group=group,description=description,
            promql=f'readiness_{key}{{{SELECTOR}}}',
            instrumentation='Proposed normalized gauge; not emitted by AWS FIS or this console. Requires a collector/recording rule with this measurement contract.'))
    return result

def dashboard(metrics):
    ds={'type':'prometheus','uid':'${DS_PROMETHEUS}'}
    variables=[{'name':'DS_PROMETHEUS','label':'Prometheus','type':'datasource','query':'prometheus','refresh':1},
        {'name':'data_kind','label':'Provenance','type':'custom','query':'measured,synthetic','current':{'text':'measured','value':'measured'},'options':[{'text':'measured','value':'measured','selected':True},{'text':'synthetic','value':'synthetic','selected':False}],'multi':False,'includeAll':False}]
    prior=['data_kind']
    for name in LABELS[:-1]:
        sel=','.join(f'{p}=~"${{{p}:regex}}"' for p in prior)
        variables.append({'name':name,'label':name.replace('_',' ').title(),'type':'query','datasource':ds,
            'definition':f'label_values(readiness_run_info{{{sel}}}, {name})',
            'query':{'qryType':1,'query':f'label_values(readiness_run_info{{{sel}}}, {name})','refId':f'var-{name}'},
            'refresh':2,'sort':1,'multi':True,'includeAll':True,'allValue':'.*','current':{'text':'All','value':'$__all'}})
        prior.append(name)
    panels=[{'id':1,'type':'text','title':'Read this before interpreting the graphs','gridPos':{'x':0,'y':0,'w':24,'h':4},
        'options':{'mode':'markdown','content':'**PROPOSED DASHBOARD — no account is connected by importing this file.**\n\nQueries require the normalized `readiness_*` contract in `docs/METRICS.md`. They are not native AWS/FIS metrics. Provenance defaults to **measured**; switch to **synthetic** only for a separate demonstration source. Missing series remain **No data**. No universal passing limits are embedded. Incident durations are per-incident observations, not MTTD/MTTR. Source observation age must be checked before trusting a repeated gauge value.'}}]
    y=4;pid=2
    unit_map={'ratio':'percentunit','seconds':'s','milliseconds':'ms','requests/second':'reqps','boolean':'short'}
    for group in dict.fromkeys(m['group'] for m in metrics):
        panels.append({'id':pid,'type':'row','title':group,'collapsed':False,'panels':[],'gridPos':{'x':0,'y':y,'w':24,'h':1}});pid+=1;y+=1
        subset=[m for m in metrics if m['group']==group]
        for i,m in enumerate(subset):
            panels.append({'id':pid,'type':'timeseries','title':m['title'],'description':m['description']+' '+m['instrumentation'],
                'datasource':ds,'gridPos':{'x':(i%2)*12,'y':y+(i//2)*8,'w':12,'h':8},
                'targets':[{'refId':'A','expr':m['promql'],'legendFormat':'{{environment}} · {{service}} · {{deployment_model}} · {{scenario}} · {{run_id}} · {{data_kind}}','range':True,'instant':False,'editorMode':'code'}],
                'fieldConfig':{'defaults':{'unit':unit_map.get(m['unit'],'short'),'noValue':'No data','color':{'mode':'palette-classic'},
                    'custom':{'drawStyle':'line','lineInterpolation':'linear','lineWidth':2,'fillOpacity':8,'spanNulls':False,'showPoints':'auto','pointSize':4,'axisPlacement':'auto','axisLabel':m['unit'],'hideFrom':{'legend':False,'tooltip':False,'viz':False}}},'overrides':[]},
                'options':{'tooltip':{'mode':'multi','sort':'none'},'legend':{'displayMode':'table','placement':'bottom','showLegend':True,'calcs':['lastNotNull','min','max']}}});pid+=1
        y+=math.ceil(len(subset)/2)*8
    panels.append({'id':pid,'type':'timeseries','title':'Age of source observations','description':'time() minus the source window end. Every exporter must emit this companion gauge, labelled with metric. A scraped gauge can remain present after its underlying observation is stale.',
        'datasource':ds,'gridPos':{'x':0,'y':y,'w':24,'h':8},'targets':[{'refId':'A','expr':f'time() - readiness_observed_timestamp_seconds{{{SELECTOR}}}','legendFormat':'{{metric}} · {{environment}} · {{service}} · {{deployment_model}} · {{scenario}} · {{run_id}} · {{data_kind}}','range':True}],
        'fieldConfig':{'defaults':{'unit':'s','noValue':'No data','custom':{'spanNulls':False,'drawStyle':'line','lineInterpolation':'linear'}},'overrides':[]},'options':{'tooltip':{'mode':'multi'},'legend':{'displayMode':'list','placement':'bottom','showLegend':True}}})
    return {'id':None,'uid':'aws-readiness-metrics-v1','title':'Operational readiness · proposed metrics','tags':['operational-readiness','proposed-contract'],'timezone':'utc','schemaVersion':39,'version':1,'editable':True,'graphTooltip':2,'time':{'from':'now-1h','to':'now'},'refresh':'30s','templating':{'list':variables},'annotations':{'list':[{'builtIn':1,'datasource':{'type':'grafana','uid':'-- Grafana --'},'enable':True,'hide':True,'iconColor':'rgba(0, 211, 255, 1)','name':'Annotations & Alerts','type':'dashboard'}]},'panels':panels}

def examples():
    def rec(kind,id,title,data):return dict(kind=kind,id=id,revision=1,title=title,simulated=True,data=data)
    start=datetime(2026,10,21,10,0,tzinfo=timezone.utc)
    iso=lambda seconds:(start+timedelta(seconds=seconds)).isoformat().replace('+00:00','Z')
    assertions=[dict(id='errors',title='Request error ratio',metric='request_error_ratio',operator='lte',threshold=.01,unit='ratio',category='application'),dict(id='restore',title='Stable recovery',metric='recovery_seconds',operator='lte',threshold=180,unit='seconds',category='recovery'),dict(id='duplicates',title='Duplicate effects',metric='duplicate_transactions',operator='eq',threshold=0,unit='transactions',category='data')]
    scenario=rec('scenario','EXAMPLE-METRICS','Synthetic incident timeline · example only',dict(status='specified',models=MODELS,domain='Metric visualization',hypothesis='Demonstrate graphs, missing samples and scalar requirements without inspecting an environment.',procedure='Synthetic fixture only. This example does not execute any action.',fault_mode='none',assertions=assertions,limitations=['Illustrative limits are not service-approved SLOs.','Chart samples do not determine the scalar evaluator result.']))
    run=rec('execution_run','example-metric-timeline','Synthetic service interruption',dict(scenario_ref='scenario:EXAMPLE-METRICS@1',execution_type='simulated',execution_state='completed',scope_id='synthetic:checkout',targets=['fictional-service'],started_at=iso(0),ended_at=iso(900),fault_confirmed=True,notes='Fictional impact begins at +300s; detection +342s; acknowledgement +435s; mitigation +470s; stable recovery begins +540s. No environment was tested.'))
    events=[{'at':iso(t),'label':label,'kind':kind} for t,label,kind in [(300,'Fault and impact begin (example)','fault_start'),(342,'Detection (example)','detected'),(435,'Acknowledged (example)','acknowledged'),(470,'Mitigated (example)','mitigated'),(540,'Stable recovery begins (example)','recovered'),(600,'Fault removed (example)','fault_end')]]
    event_metrics={'detection_seconds','alert_delivery_seconds','acknowledgement_seconds','mitigation_seconds','recovery_seconds','rto_seconds','data_loss_seconds','rpo_seconds','duplicate_transactions','lost_acknowledged_writes','db_reconnect_seconds','capacity_restoration_seconds','runbook_completion_ratio','automatic_recovery_ratio','error_budget_consumed_ratio','evidence_coverage_ratio','incomplete_scope_count'}
    rows=[scenario,run]
    for index,(key,title,unit,group,desc,base,peak) in enumerate(DEFINITIONS):
        value=bool(base) if unit=='boolean' else base
        d=dict(run_ref='execution_run:example-metric-timeline@1',scope_id='synthetic:checkout',metric=key,value=value,unit=unit,sample_count=1 if key in event_metrics else 10000,window_start=iso(0),window_end=iso(900),collected_at=iso(905),source='Synthetic graph fixture; no AWS, runtime or incident source queried.',notes='Window summary is independently supplied for evaluator examples. It is not calculated from chart samples. Synthetic values and limits must not be used for readiness approval.')
        if key not in event_metrics:
            points=[]
            for t in range(0,901,10):
                bump=1 if 300<=t<390 else max(0,1-(t-390)/150) if 390<=t<540 else 0
                val=base+(peak-base)*bump+(base*.035*math.sin(t/23+index) if key!='fault_active' else 0)
                if key=='restart_count':val=4 if t>=300 else 0
                if key=='fault_active':val=300<=t<600
                if unit=='ratio':val=max(0,min(1,val))
                # Explicit gap and omitted cadence point exercise both gap paths.
                if t==450 and key in {'latency_p95_ms','request_error_ratio'}:val=None
                if t==460 and key=='latency_p95_ms':continue
                points.append(dict(at=iso(t),value=None if val is None else val if isinstance(val,bool) else round(val,6)))
            d['series']=dict(description='Synthetic 10-second window observations. Missing intervals are intentional; no interpolation is valid.',expected_interval_seconds=10,points=points,events=events)
        rows.append(rec('evidence','example-metric-'+key,title+' · synthetic',d))
    # Normalize using the actual interchange contract; guarantees importability.
    from app.models import Bundle
    return Bundle.model_validate(dict(schema_version='1.0',kind='validation_bundle',records=rows)).model_dump(mode='json')

def build():
    metrics=catalogue();dash=dashboard(metrics);demo=examples()
    def write(path,value):
        p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
    write('grafana/operational-readiness.json',dash)
    write('grafana/metric-catalogue.json',metrics)
    write('examples/metrics-series.json',demo)
    from app.models import Bundle
    write('schemas/validation-bundle.schema.json',Bundle.model_json_schema())
    return dict(catalogue=metrics,dashboard=dash,examples=demo,sources=[dict(title=t,url=u) for t,u in SOURCES],chart_css=(ROOT/'static/metrics.css').read_text())

if __name__=='__main__':
    build();print('Built metric catalogue, Grafana dashboard, schema and synthetic example bundle.')
