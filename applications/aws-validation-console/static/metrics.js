/* Console integration. Charts display evidence; the scalar evaluator is unchanged. */
'use strict';
const metricView={source:MODE==='preview'?'synthetic':'workspace',group:'all',query:'',run:'all',scope:'all',model:'all',from:'',to:'',presence:'all'};
ROUTES.splice(3,0,['metrics','Metrics','∿','Workspace']);
ROUTES.splice(ROUTES.length-1,0,['grafana','Grafana design','▥','System']);
function metricEntry(r){return {record:r,meta:{ref:rid(r),origin:'example',sha256:'synthetic-not-imported'}};}
function metricSource(){return metricView.source==='synthetic'?APP_METRICS.examples.records.map(metricEntry):state.entries;}
function metricMeta(metric,unit,title){const m=APP_METRICS.catalogue.find(x=>x.metric===metric&&x.unit===unit);return m||{metric,title:title||metric,unit,group:'Imported metrics',description:'Imported metric. Its measurement method and denominator must be documented by its source.',promql:null};}
function metricEvidence(e,entryMap,summaryOnly=false){
  const r=e.record,d=r.data,run=entryMap.get(d.run_ref)?.record;
  const base={ref:e.meta.ref,source:d.source,label:`${r.simulated?'Synthetic · ':''}${d.scope_id} · ${run?.id||d.run_ref} · r${r.revision}`,events:[],connected:false};
  if(d.series&&!summaryOnly)return {...base,connected:true,cadence:d.series.expected_interval_seconds,
    points:d.series.points.map(p=>({t:Date.parse(p.at),value:p.value,ref:e.meta.ref})),events:(d.series.events||[]).map(x=>({t:Date.parse(x.at),label:x.label}))};
  return {...base,points:[{t:Date.parse(d.window_end),value:d.value,ref:e.meta.ref}]};
}
function metricSpec(meta,evidence,entryMap,assertions=[],note=''){
  const limits=[];for(const a of assertions){if(a.metric!==meta.metric||a.unit!==meta.unit)continue;if(limits.some(l=>l.value===a.threshold&&l.operator===a.operator))continue;limits.push({value:a.threshold,operator:a.operator,label:`Scalar requirement ${a.operator}`});}
  const traces=evidence.filter(e=>e.record.data.metric===meta.metric&&e.record.data.unit===meta.unit).map(e=>metricEvidence(e,entryMap));
  const synthetic=evidence.length>0&&evidence.every(e=>e.record.simulated);
  return {...meta,traces,limits,synthetic,note:note||meta.description+' '+(evidence.some(e=>e.record.data.series)?'Lines use supplied chart samples. Gaps remain gaps. The separately supplied scalar summary is the evaluator input.':'Dots are window summaries or incident durations. No continuous history is inferred.')};
}
function metricDefinitions(entries){
  const map=new Map(APP_METRICS.catalogue.map(m=>[m.metric+'|'+m.unit,m]));
  for(const e of entries){const r=e.record;if(r.kind==='evidence'){const d=r.data,k=d.metric+'|'+d.unit;if(!map.has(k))map.set(k,metricMeta(d.metric,d.unit,r.title));}
    if(r.kind==='scenario')for(const a of r.data.assertions){const k=a.metric+'|'+a.unit;if(!map.has(k))map.set(k,metricMeta(a.metric,a.unit,a.title));}}
  return [...map.values()];
}
function selectedMetricEntries(entries){
  const map=new Map(entries.map(e=>[e.meta.ref,e]));
  return entries.filter(e=>{
    if(e.record.kind!=='evidence')return false;const d=e.record.data,run=map.get(d.run_ref)?.record,scenario=map.get(run?.data.scenario_ref)?.record;
    if(metricView.run!=='all'&&d.run_ref!==metricView.run)return false;
    if(metricView.scope!=='all'&&d.scope_id!==metricView.scope)return false;
    if(metricView.model!=='all'&&!scenario?.data.models.includes(metricView.model))return false;
    return true;
  });
}
function metricRange(spec){
  const low=metricView.from?Date.parse(metricView.from+'Z'):-Infinity,high=metricView.to?Date.parse(metricView.to+'Z'):Infinity;
  return {...spec,traces:spec.traces.map(t=>({...t,points:t.points.filter(p=>p.t>=low&&p.t<=high)}))};
}
function metricsPage(){
  const entries=metricSource(),map=new Map(entries.map(e=>[e.meta.ref,e])),evidence=selectedMetricEntries(entries);
  const definitions=metricDefinitions(entries),groups=[...new Set(definitions.map(m=>m.group))];
  const scopes=[...new Set(entries.filter(e=>e.record.kind==='evidence').map(e=>e.record.data.scope_id))];
  const runs=entries.filter(e=>e.record.kind==='execution_run');
    let specs=definitions.filter(m=>(metricView.group==='all'||m.group===metricView.group)&&(!metricView.query||(m.title+' '+m.metric+' '+m.description).toLowerCase().includes(metricView.query.toLowerCase())))
    .map(m=>{const ev=evidence.filter(e=>e.record.data.metric===m.metric&&e.record.data.unit===m.unit),refs=new Set(ev.map(e=>map.get(e.record.data.run_ref)?.record.data.scenario_ref));const limits=refs.size===1?entries.filter(e=>refs.has(e.meta.ref)).flatMap(e=>e.record.data.assertions||[]):[];return metricRange(metricSpec(m,ev,map,limits));});
  if(metricView.presence!=='all')specs=specs.filter(s=>(s.traces.some(t=>t.points.some(p=>p.value!==null)))===(metricView.presence==='recorded'));
  const recorded=specs.filter(s=>s.traces.some(t=>t.points.some(p=>p.value!==null))).length;
  const options=(values,current)=>values.map(x=>`<option value="${esc(typeof x==='string'?x:x[0])}" ${(typeof x==='string'?x:x[0])===current?'selected':''}>${esc(typeof x==='string'?x:x[1])}</option>`).join('');
  const select=(key,label,values)=>`<label>${label}<select data-metrics-field="${key}">${options(values,metricView[key])}</select></label>`;
  const sourceNotice=metricView.source==='synthetic'?'<strong>SYNTHETIC GRAPH EXAMPLE.</strong> Fictional measurements from 21 October 2026, 10:00–10:15 UTC. Nothing has been connected or imported.':'<strong>WORKSPACE EVIDENCE.</strong> Source and simulation labels are preserved per series. Imported values are not independently verified. A chart is not a readiness verdict.';
  return pageHeading('Observations / incident timelines / source evidence','Metrics','Inspect every defined metric, including missing evidence. Different scopes, runs and revisions remain separate series.',button('Grafana proposal →','route','data-route="grafana"')+`<button class="button secondary" data-metrics-action="download-example">Download example bundle</button>`)+
    `<div class="metrics-intro info ${metricView.source==='synthetic'?'warning':''}"><p>${sourceNotice}</p></div>`+
    `<div class="metrics-toolbar">${select('source','Data source',[['workspace','Workspace evidence'],['synthetic','Synthetic graph example']])}<label class="metrics-search">Search metrics<input id="metrics-query" data-metrics-field="query" type="search" placeholder="Latency, recovery, CPU, custom metric…" value="${esc(metricView.query)}"></label>${select('group','Metric group',[['all','All groups'],...groups])}${select('presence','Evidence',[['all','Recorded and missing'],['recorded','Recorded only'],['missing','Missing only']])}${select('model','Deployment applicability',[['all','All models'],...Object.entries(MODEL_NAMES)])}${select('scope','Evidence scope',[['all','All scopes (separate series)'],...scopes])}${select('run','Execution record',[['all','All runs (separate series)'],...runs.map(e=>[e.meta.ref,e.record.title])])}<label>From (UTC)<input data-metrics-field="from" type="datetime-local" value="${esc(metricView.from)}"></label><label>To (UTC)<input data-metrics-field="to" type="datetime-local" value="${esc(metricView.to)}"></label><button class="button secondary" data-metrics-action="reset">Reset filters</button></div>`+
    `<div class="metric-coverage"><span><strong>${specs.length}</strong>metric definitions shown</span><span><strong>${recorded}</strong>with recorded values in this view</span><span><strong>${specs.length-recorded}</strong>without values</span><span>No interpolation across missing samples</span></div>`+
    (metricView.from&&metricView.to&&metricView.from>metricView.to?info('The end of the selected range precedes its start. No values are displayed.','warning'):'')+
    `<div class="metric-charts-grid">${specs.map(s=>`<div>${MetricCharts.card(s)}<button class="text-link" data-metrics-action="definition" data-metric="${esc(s.metric)}" data-unit="${esc(s.unit)}">Measurement contract & Grafana query →</button></div>`).join('')||empty('No metric matches these filters','Reset the filters or import evidence using a metric identifier and explicit unit.')}</div>`;
}
function recordMetricSpecs(reference){
  const e=get(reference);if(!e)return [];const map=new Map(state.entries.map(x=>[x.meta.ref,x])),r=e.record,d=r.data;
  if(r.kind==='report')return d.validation_ref?recordMetricSpecs(d.validation_ref):[];
  if(r.kind==='snapshot')return snapshotMetricSpecs([e]);
  let evidence=[],assertions=[],warning='';
  if(r.kind==='evidence')evidence=[e];
  if(r.kind==='scenario'){assertions=d.assertions;const runs=new Set(records('execution_run').filter(x=>x.record.data.scenario_ref===reference).map(x=>x.meta.ref));evidence=records('evidence').filter(x=>runs.has(x.record.data.run_ref));}
  if(r.kind==='execution_run'){evidence=records('evidence').filter(x=>x.record.data.run_ref===reference);assertions=get(d.scenario_ref)?.record.data.assertions||[];}
  if(r.kind==='validation_run'){
    const scenario=get(d.scenario_ref);assertions=scenario&&d.input_hashes[d.scenario_ref]===scenario.meta.sha256?scenario.record.data.assertions:[];
    const refs=new Set((d.checks||[]).map(c=>c.evidence_ref).filter(Boolean));
    evidence=records('evidence').filter(x=>refs.has(x.meta.ref)&&d.input_hashes[x.meta.ref]===x.meta.sha256);
    warning='Only evidence linked by this validation and matching its input hash is plotted. Missing or mismatched inputs are omitted. Samples illustrate the source; the verdict uses its scalar summary.';
  }
  const defs=new Map();for(const a of assertions)defs.set(a.metric+'|'+a.unit,metricMeta(a.metric,a.unit,a.title));for(const x of evidence){const z=x.record.data;defs.set(z.metric+'|'+z.unit,metricMeta(z.metric,z.unit,x.record.title));}
  return [...defs.values()].map(m=>metricSpec(m,evidence.filter(x=>x.record.data.metric===m.metric&&x.record.data.unit===m.unit),map,assertions,warning));
}
function snapshotMetricSpecs(entries){
  const byConnection=new Map();for(const e of entries){const id=e.record.data.connection_id;if(!byConnection.has(id))byConnection.set(id,[]);byConnection.get(id).push(e);}
  const out=[];
  for(const [id,rows] of byConnection){
    const scopeIds=new Set(rows.flatMap(e=>e.record.data.coverage.map(c=>c.scope)));
    const mk=(metric,title,fn,note)=>({metric,title,unit:'resources',synthetic:rows.every(e=>e.record.simulated),limits:[],note,traces:[{label:id,source:'Immutable inspection snapshots',connected:false,events:[],ref:rows.map(e=>e.meta.ref).join('; '),points:rows.map(e=>({t:Date.parse(e.record.data.ended_at),value:fn(e)})).sort((a,b)=>a.t-b.t)}]});
    out.push(mk('resource_count',id+' · recorded resources',e=>e.record.data.resources.length,'Count of returned resource records, including partial snapshots. It does not establish total environment size or application health. Separate snapshots are not continuous telemetry.'));
    for(const scope of scopeIds)out.push(mk('scope_resource_count',id+' · '+scope,e=>{const c=e.record.data.coverage.find(x=>x.scope===scope);return c?.status==='complete'?c.resource_count:null;},'Only complete collection scopes produce a numeric point. Denied, truncated, missing and unrequested scopes are gaps, not zero resources.'));
  }
  return out;
}
function resourceMetricSpecs(reference,id){
  const current=get(reference);if(!current)return [];const d=current.record.data,target=d.resources.find(r=>r.id===id);if(!target)return [];
  const facts=Object.entries(target.facts).filter(([,v])=>typeof v==='number'||typeof v==='boolean');
  return facts.map(([key,val])=>({metric:'resource_'+key,title:target.name+' · '+key,unit:typeof val==='boolean'?'boolean':'reported units',synthetic:current.record.simulated,limits:[],note:'Configuration or runtime-state observation. Unit is not inferred from the field name. This is not a performance measurement.',traces:[{label:d.connection_id+' · '+id,source:'Allowlisted snapshot facts',connected:false,events:[],ref:reference,points:records('snapshot').filter(e=>e.record.data.connection_id===d.connection_id&&e.record.data.scope_id===d.scope_id&&e.record.simulated===current.record.simulated).map(e=>{const resource=e.record.data.resources.find(x=>x.id===id&&x.model===target.model);return {t:Date.parse(e.record.data.ended_at),value:resource&&typeof resource.facts[key]===typeof val?resource.facts[key]:null};}).sort((a,b)=>a.t-b.t)}]}));
}
function graphsSection(specs,title='Metric graphs'){
  return specs.length?`<section class="metrics-record"><h3>${esc(title)}</h3><p class="small-note">Hover or use arrow keys to inspect a sample. Drag to zoom. A single point means one recorded observation, not a measured trend.</p>${specs.map(s=>MetricCharts.card(s)).join('')}</section>`:'';
}
const originalStat=stat;
stat=function(label,value,note){const spec={metric:'workspace_count',title:label,unit:'records',synthetic:MODE==='preview',limits:[],note:'Current workspace count only. Historical counts are not reconstructed or invented.',traces:[{label:'Current workspace',source:'Loaded local records at view time',ref:'workspace',connected:false,events:[],points:[{t:Date.now(),value:typeof value==='number'?value:null}]}]};return originalStat(label,value,note).replace('</div><p>', '</div><p>').replace('</p></div>','</p>'+MetricCharts.card(spec,{mini:true,heading:false})+'</div>');};
const originalShowDetail=showDetail;
showDetail=function(reference){originalShowDetail(reference);const body=$('#drawer .dialog-body');if(body)body.insertAdjacentHTML('beforeend',graphsSection(recordMetricSpecs(reference)));MetricCharts.prune();};
const originalShowResource=showResource;
showResource=function(reference,id){originalShowResource(reference,id);const body=$('#drawer .dialog-body');if(body)body.insertAdjacentHTML('beforeend',graphsSection(resourceMetricSpecs(reference,id),'Numeric resource facts'));MetricCharts.prune();};
const originalRender=render;
render=function(){
  const wanted=state.route;if(wanted==='metrics'||wanted==='grafana'){
    state.route='overview';originalRender();state.route=wanted;renderNav();$('#breadcrumb-current').textContent=wanted==='metrics'?'Metrics':'Grafana design';$('#main').innerHTML=wanted==='metrics'?metricsPage():grafanaPage();
  }else{originalRender();
    if(state.route==='overview'){
      const evidence=records('evidence'),map=new Map(state.entries.map(e=>[e.meta.ref,e]));
      const keyMetrics=['request_error_ratio','detection_seconds','recovery_seconds','duplicate_transactions'];
      const specs=keyMetrics.map(k=>metricSpec(APP_METRICS.catalogue.find(m=>m.metric===k),evidence.filter(e=>e.record.data.metric===k),map));
      $('#main').insertAdjacentHTML('beforeend',`<section class="section-gap"><div class="panel-header"><div><h2>Incident measurements</h2><p>Recorded values, not an inferred deployment status.</p></div><a href="#metrics" class="text-link">All metrics →</a></div><div class="metric-charts-grid">${specs.map(s=>MetricCharts.card(s)).join('')}</div></section>`);
    }
    if(state.route==='inventory'){
      const rows=state.inventoryRef==='latest'?records('snapshot'):records('snapshot').filter(e=>e.meta.ref===state.inventoryRef);
      const specs=snapshotMetricSpecs(rows).filter(s=>s.metric==='resource_count');
      if(specs.length)$('#main').insertAdjacentHTML('beforeend',`<div class="section-gap metric-charts-grid">${specs.map(s=>MetricCharts.card(s)).join('')}</div>`);
    }
  }MetricCharts.prune();
};
function grafanaPage(){return pageHeading('Proposed instrumentation / portable dashboard','Grafana design','A versioned dashboard proposal with one interactive time-series panel per catalogue metric. It requires the documented metrics contract; importing it does not connect an AWS account.')+
  `<section class="grafana-preview"><h2>Operational readiness · proposed metrics</h2><p>${APP_METRICS.catalogue.length} metric panels plus source-observation age. Filter by environment, service, deployment model, scenario, run and provenance. Shared crosshair, time-range zoom, legend isolation, query inspection and data export use Grafana’s native controls.</p><div class="header-actions"><button class="button" data-metrics-action="grafana">Download dashboard JSON</button><button class="button secondary" data-metrics-action="contract">Download metric catalogue</button><button class="button secondary" data-metrics-action="example-view">Inspect synthetic graphs</button></div></section>`+
  info('<strong>No built-in FIS metrics are implied.</strong> Every <code>readiness_*</code> query is a proposed normalized measurement. A collector or recording rule must supply it. CloudWatch, Prometheus, workload probes and incident-system events remain separate sources.','warning')+
  panel('Setup and interpretation','Grafana Classic JSON; verify import against your installed release',`<div class="panel-body metrics-docs"><p>Import the JSON in Grafana and select a Prometheus data source using the <strong>Prometheus</strong> dashboard variable. Provide <code>readiness_run_info</code> with the filter labels, then emit the required measurement families. Set the actual scrape interval in the data source. The default provenance is <strong>measured</strong>.</p><p>Use <code>readiness_observed_timestamp_seconds</code>, labelled by metric, to distinguish recent scrapes from recent source observations. An exporter that repeats a stale gauge must not make it look like fresh evidence. The example does not contain alert rules or universal passing thresholds.</p><p>Deployments covered by the contract: EC2/Auto Scaling, both EKS hosting models, both ECS hosting models, Lambda, Docker, Podman and Kubernetes. Label applicability does not prove a collector supports a deployment.</p><p>Operational durations require verified events. FIS action completion alone cannot provide time to detection, acknowledgement, stable recovery or transaction correctness.</p></div>`)+
  `<div class="section-gap">${panel('Metric-to-panel mapping','These query names must be implemented or mapped to your existing instrumentation',`<div class="table-wrap"><table><thead><tr><th>Metric</th><th>Unit</th><th>Group</th><th>Query and definition</th></tr></thead><tbody>${APP_METRICS.catalogue.map(m=>`<tr><td>${esc(m.title)}<span class="cell-sub mono">${esc(m.metric)}</span></td><td>${esc(m.unit)}</td><td>${esc(m.group)}</td><td><button class="text-link" data-metrics-action="definition" data-metric="${esc(m.metric)}" data-unit="${esc(m.unit)}">Inspect contract →</button></td></tr>`).join('')}</tbody></table></div>`)}</div><div class="section-gap">${panel('Primary documentation','Reviewed 21 October 2026',`<div class="panel-body metrics-docs">${APP_METRICS.sources.map(s=>`<p>${esc(s.title)}<br>${safeLink(s.url)}</p>`).join('')}</div>`)}</div>`;}
async function metricReportDocument(reference){
  const e=get(reference);if(!e||e.record.kind!=='report')throw new Error('Report record not found.');const r=e.record,specs=recordMetricSpecs(reference);
  const nonce=Array.from(crypto.getRandomValues(new Uint8Array(16))).map(n=>n.toString(16).padStart(2,'0')).join('');
  const payload=JSON.stringify(specs).replace(/</g,'\\u003c').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029');
  const css=`body{font-family:system-ui,sans-serif;margin:32px auto;padding:0 20px;max-width:1080px;color:#1b2b3a;background:#f3f6f8}h1{font-size:26px}pre{white-space:pre-wrap;overflow-wrap:anywhere}.warning{padding:16px;background:#fff4df;border:1px solid #dec38e;margin:20px 0}.report-charts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}table{border-collapse:collapse;width:100%}td,th{padding:8px;text-align:left;border-bottom:1px solid #dce3e8}.table-wrap{overflow:auto}@media(max-width:900px){.report-charts{grid-template-columns:1fr}}`+APP_METRICS.chart_css;
  const styleTag='sty'+'le',scriptTag='scr'+'ipt';
  const script=MetricCharts.source+'\nconst specs='+payload+';document.getElementById("graphs").innerHTML=specs.map(s=>MetricCharts.card(s)).join("");';
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'nonce-${nonce}'; script-src 'nonce-${nonce}'; img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'"><title>${esc(r.title)}</title><${styleTag} nonce="${nonce}">${css}</${styleTag}></head><body><h1>${esc(r.title)}</h1><p>${esc(reference)} · ${esc(shortDate(r.data.generated_at))}</p><div class="warning"><strong>${r.simulated?'SYNTHETIC EXAMPLE':'RECORDED VALIDATION REPORT'}</strong><p>${esc(r.data.outcome.toUpperCase())} · Graphs use only evidence pinned by the referenced validation with matching hashes. Samples supplement the separately evaluated scalar values. Missing inputs remain missing.</p></div><pre>${esc(r.data.body)}</pre><h2>Limitations</h2><ul>${r.data.limitations.map(x=>`<li>${esc(x)}</li>`).join('')}</ul><h2>Frozen metric graphs</h2><p>No network calls. Hover or use arrow keys to inspect values. Use drag-selection or zoom buttons to change the view; CSV retains raw samples.</p><div id="graphs" class="report-charts"></div>${specs.length?'':'<p>No linked, verifiable metric evidence is loaded for this report.</p>'}<${scriptTag} nonce="${nonce}">${script}</${scriptTag}></body></html>`;
}
downloadReport=async function(reference){const r=get(reference)?.record;if(!r)throw new Error('Report not found.');download(r.id+'.html',await metricReportDocument(reference),'text/html');};
document.addEventListener('metric-expand',event=>showDrawer(event.detail.title,'Current observation; historical values were not fabricated.',MetricCharts.card(event.detail)));
document.addEventListener('click',event=>{
  const el=event.target.closest('[data-metrics-action]');if(!el)return;event.preventDefault();
  const action=el.dataset.metricsAction;
  if(action==='grafana')download('operational-readiness-grafana.json',JSON.stringify(APP_METRICS.dashboard,null,2));
  if(action==='contract')download('readiness-metric-catalogue.json',JSON.stringify(APP_METRICS.catalogue,null,2));
  if(action==='download-example')download('synthetic-metrics-bundle.json',JSON.stringify(APP_METRICS.examples,null,2));
  if(action==='example-view'){metricView.source='synthetic';location.hash='metrics';}
  if(action==='reset'){Object.assign(metricView,{group:'all',query:'',run:'all',scope:'all',model:'all',from:'',to:'',presence:'all'});render();}
  if(action==='definition'){const m=metricMeta(el.dataset.metric,el.dataset.unit);showDrawer(m.title,'Measurement contract · '+m.metric,`<p>${esc(m.description)}</p><p>Unit: <strong>${esc(m.unit)}</strong></p>${m.promql?`<h3>Proposed PromQL</h3><pre class="metric-query">${esc(m.promql)}</pre><p>${esc(m.instrumentation)}</p>`:'<p>No Grafana query is proposed for this imported custom metric. Map it explicitly before use.</p>'}`);}
});
function metricFilter(event){const el=event.target.closest('[data-metrics-field]');if(!el)return;const key=el.dataset.metricsField;if(!Object.hasOwn(metricView,key))return;metricView[key]=el.value;if(key==='source'){metricView.run='all';metricView.scope='all';metricView.from='';metricView.to='';}
  const cursor=el.selectionStart;render();const next=$(`[data-metrics-field="${key}"]`);next?.focus();if(key==='query'&&next&&cursor!==null)next.setSelectionRange(cursor,cursor);
}
document.addEventListener('change',metricFilter);
document.addEventListener('input',e=>{if(e.target.dataset.metricsField==='query')metricFilter(e);});

const originalBasicReview=basicReview;
basicReview=function(bundle){
  const result=originalBasicReview(bundle);
  for(const r of bundle.records){if(r.kind!=='evidence'||!r.data.series)continue;const d=r.data,s=d.series;
    if(!Array.isArray(s.points)||!s.points.length||s.points.length>20000||typeof s.description!=='string')throw new Error('Chart series requires a description and 1–20,000 ordered samples.');
    if(s.expected_interval_seconds!=null&&(!Number.isInteger(s.expected_interval_seconds)||s.expected_interval_seconds<1||s.expected_interval_seconds>604800))throw new Error('Invalid chart sample cadence.');
    let last=-Infinity;const lo=Date.parse(d.window_start),hi=Date.parse(d.window_end);
    if(!Number.isFinite(lo)||!Number.isFinite(hi))throw new Error('Invalid evidence window.');
    for(const p of s.points){const t=Date.parse(p.at);if(!Number.isFinite(t)||t<=last||t<lo||t>hi)throw new Error('Chart samples must increase strictly inside the evidence window.');if(p.value!==null&&(MetricCharts.numeric(p.value)===null||(typeof p.value==='boolean') !== (typeof d.value==='boolean')))throw new Error('Chart samples must be finite numbers or booleans matching the summary, or null.');last=t;}
    if(s.events&&!Array.isArray(s.events))throw new Error('Chart events must be an array.');
    for(const e of s.events||[]){const t=Date.parse(e.at);if(typeof e.label!=='string'||!Number.isFinite(t)||t<lo||t>hi)throw new Error('Chart events must have a label and a timestamp inside the evidence window.');}
  }return result;
};
// Remove graph data from closed drawers, including when the service is locked.
$('#drawer').addEventListener('close',()=>{if(!$('#drawer').open){$('#drawer-content').replaceChildren();MetricCharts.prune();}});
