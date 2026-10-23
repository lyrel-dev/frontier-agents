'use strict';
const state={token:'',workspace:null,config:null,view:new URLSearchParams(location.search).has('trial')?'trials':'overview',selected:new URLSearchParams(location.search).get('trial'),detail:null,offline:location.protocol==='file:'};
const $=s=>document.querySelector(s);
function el(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;}
function button(text,fn,cls='',disabled=false){const b=el('button',cls,text);b.type='button';b.disabled=disabled;b.addEventListener('click',()=>Promise.resolve().then(fn).catch(fail));return b;}
function pill(value){return el('span','pill '+String(value).toLowerCase(),String(value).replaceAll('_',' '));}
function toast(message){const n=$('#toast');n.textContent=message;n.style.display='block';setTimeout(()=>n.style.display='none',6000);}
function fail(error){toast(error.message||String(error));}
async function api(path,body,token=state.token){
  if(state.offline)throw Error('This offline file shows the empty interface. Run the backend to connect accounts or execute a trial.');
  const options={headers:{Authorization:'Bearer '+token}};
  if(body!==undefined){options.method='POST';options.headers['Content-Type']='application/json';options.body=JSON.stringify(body);}
  const response=await fetch('/api/'+path,options);
  if(!response.ok){let message;try{const e=await response.json();message=e.error||JSON.stringify(e.detail||e);}catch{message='HTTP '+response.status;}throw Error(message);}
  return response.json();
}
async function refresh(){
  if(!state.token)return;
  [state.workspace,state.config]=await Promise.all([api('workspace'),api('config')]);
  if(state.selected)state.detail=await api('entities/'+state.selected);
  render();
}
function lock(){state.token='';state.workspace=null;state.config=null;state.detail=null;state.selected=null;render();}
function modal(title,contents){$('#modal-title').textContent=title;$('#modal-body').replaceChildren(contents);$('#modal').showModal();}
function input(label,type='text',value='',required=true){const wrap=el('label','',label),box=el(type==='textarea'?'textarea':'input');if(type!=='textarea')box.type=type;box.value=value;box.required=required;wrap.append(box);return {wrap,box};}
function select(label,options){const wrap=el('label','',label),box=el('select');for(const [value,text]of options){const opt=el('option','',text);opt.value=value;box.append(opt);}wrap.append(box);return {wrap,box};}
function formFooter(form,label,submit){const error=el('div','error'),b=el('button','primary',label);b.type='submit';form.append(error,b);form.addEventListener('submit',async e=>{e.preventDefault();b.disabled=true;error.textContent='';try{await submit();$('#modal').close();await refresh();}catch(err){error.textContent=err.message;}finally{b.disabled=false;}});}
function showUnlock(){
  if(state.token){lock();return;}
  const form=el('form'),p=el('p','muted',state.offline?'Offline, empty interface. No account or experiment is connected. Start the included backend to use this console.':'Use the local console operator token. AWS access keys are not accepted here.');form.append(p);
  if(!state.offline){const token=input('Operator token','password');form.append(token.wrap);formFooter(form,'Unlock',async()=>{await api('workspace',undefined,token.box.value);state.token=token.box.value;});}
  modal('Unlock local workspace',form);
}
function pageTitle(kicker,title,description,actions=[]){const header=el('section','page-heading'),left=el('div');left.append(el('div','kicker',kicker),el('h1','',title),el('p','subtitle',description));const right=el('div','heading-actions');right.append(...actions);header.append(left,right);return header;}
function empty(title,description,action){const box=el('div','empty');box.append(el('div','empty-symbol','⌁'),el('h3','',title),el('p','',description));if(action)box.append(action);return box;}
function card(title,sub){const n=el('section','card'),h=el('div','card-title');h.append(el('h2','',title));if(sub)h.append(el('span','small muted',sub));n.append(h);return n;}
function chart(title,unit,series,events){const n=el('div');LabCharts.draw(n,{title,unit,series,events});return n;}
function route(view){state.view=view;state.selected=null;state.detail=null;render();}
async function inspect(id,view){state.view=view;state.selected=id;state.detail=await api('entities/'+id);render();}
function render(){
  const w=state.workspace;$('#unlock-button').textContent=state.token?'Lock workspace':'Unlock workspace';
  $('#write-state').textContent=w?.write_enabled?'AWS execution enabled':'Execution locked';$('#write-state').className='pill '+(w?.write_enabled?'inconclusive':'neutral');
  const heartbeat=w?.worker;$('#worker-status').textContent=heartbeat?'Worker '+heartbeat.state+' · '+new Date(heartbeat.heartbeat_at).toISOString().slice(11,19)+' UTC':'Worker not connected';
  for(const b of document.querySelectorAll('[data-view]'))b.classList.toggle('active',b.dataset.view===state.view);
  $('#breadcrumb').textContent=({overview:'Experiment console',trials:'Response trials',prevention:'Prevention campaigns',evidence:'Evidence & reports',connections:'Instruments & access'})[state.view];
  const host=$('#view');host.replaceChildren();
  if(state.selected&&state.detail){renderDetail(host);return;}
  ({overview:overview,trials:trials,prevention:campaigns,evidence:evidence,connections:connections})[state.view](host);
}
function overview(host){
  const entities=state.workspace?.entities||[],trials=entities.filter(x=>x.kind==='trial'),campaigns=entities.filter(x=>x.kind==='campaign');
  host.append(pageTitle('CONTROLLED EXPERIMENTS / INDEPENDENT EVIDENCE','Test the response. Verify the change.','Run qualified incidents against account B, inspect the Agent Space in account A, and test prevention recommendations through an approved change and matched replay.',[
    button('Register experiment',newExperiment,'primary',!state.token||!state.config?.bindings.length),button('View instruments',()=>route('connections'))]));
  const binding=state.config?.bindings?.[0],strip=el('section','connection-strip');
  for(const [i,title,value,note]of [[0,'ACCOUNT A · AGENT SPACE',binding?.agent_space_id||'No Agent Space connected',binding?.agent_account||'Observer access configured locally'],[1,'LOCAL EXPERIMENT CONTROLLER','Durable worker + evidence',state.workspace?.worker?.state||'Not connected'],[2,'ACCOUNT B · MONITORED SERVICE',binding?.service_id||'No service bound',binding?.workload_account||'Independent workload and fault access']]){
    if(i)strip.append(el('div','arrow','→'));const cell=el('div');cell.append(el('div','connection-label',title),el('div','connection-name',value),el('div','connection-sub',note));strip.append(cell);
  }host.append(strip);
  const stats=el('div','grid stats');
  const groups=[['REGISTERED TRIALS',trials.length,'Includes blocked and aborted attempts'],['ACTIVE EXPERIMENTS',trials.filter(t=>['BASELINING','EXPOSING','OBSERVING','CLEANING'].includes(t.state)).length,'No browser dependency'],['PREVENTION CAMPAIGNS',campaigns.length,'Recommendation → change → replay'],['REQUIRED RESTORATIONS',entities.filter(t=>t.state==='RESTORE_REQUIRED').length,'Never hidden by a successful graph']];
  for(const [label,value,note]of groups){const c=el('div','card');c.append(el('div','stat-label',label),el('div','stat-value',state.workspace?String(value):'—'),el('div','stat-note',note));stats.append(c);}host.append(stats);
  const grid=el('div','grid two-col'),activity=card('Experiment lifecycle','No invented results');
  const stages=el('div','stages');['Qualify','Baseline','Perturb','Investigate','Restore','Compare'].forEach((s,i)=>{const x=el('div','stage');x.append(el('b','',String(i+1).padStart(2,'0')),document.createTextNode(s));stages.append(x);});activity.append(stages);
  if(!trials.length)activity.append(empty('No measured trials yet','A trial is registered before the incident exists. Actual targets, task delivery, agent findings, interventions and service measurements are collected during execution.',button('Open response trials',()=>route('trials'))));
  else activity.append(trialTable(trials.slice(0,5)));
  const boundaries=card('What a result must prove');
  for(const [title,text]of [['Incident delivery','An exact reference joins the native incident path to the agent task. No automatic substitute investigation.'],['Correct diagnosis','A cited finding is compared with independently verified ground truth—not judged by document presence.'],['Effective prevention','A pinned recommendation is linked to a verified implementation and a comparable measured replay.'],['Safe execution','Bounded faults, separate approval credentials, persisted operation identities and verified cleanup.']]){const row=el('div','boundary-row');row.append(el('strong','',title),el('p','',text));boundaries.append(row);}grid.append(activity,boundaries);host.append(grid);
  host.append(el('div','notice','Non-production execution only. Live account acceptance is not implied by this interface. Missing evidence remains inconclusive; an agent summary is not a readiness certificate.'));
}
function experimentOptions(){return (state.workspace?.experiments||[]).map(r=>[r.id,r.data.title+' · r'+r.data.revision]);}
function trials(host){
  host.append(pageTitle('RESPONSE / END-TO-END TRIALS','Response trials','The worker owns qualification, real test traffic, bounded exposure, incident observation and restoration. A task ID is not required to register a trial.',[
    button('New trial',newTrial,'primary',!state.token||!experimentOptions().length),button('Register experiment',newExperiment,'',!state.token||!state.config?.bindings.length)]));
  const list=(state.workspace?.entities||[]).filter(x=>x.kind==='trial');const c=card('Execution ledger',list.length+' attempts');c.append(list.length?trialTable(list):empty('No trials registered','Configure your instruments, register the requirement and oracle, then qualify a trial. There are no sample incidents to mistake for live evidence.'));host.append(c);
  const definitions=card('Experiment definitions','Immutable revisions');
  for(const record of state.workspace?.experiments||[]){const row=el('div','boundary-row');row.append(el('strong','',record.data.title),el('p','',record.id+' · '+record.data.mode+' incident path'),button('Inspect contract',()=>showRecord(record.id)));definitions.append(row);}if(!(state.workspace?.experiments||[]).length)definitions.append(el('p','muted','No definitions registered. Definitions contain no outcome data.'));host.append(definitions);
}
function trialTable(rows){const wrap=el('div','table-wrap'),table=el('table');const head=el('tr');['Trial / arm','Lifecycle','Evidence','Actions'].forEach(s=>head.append(el('th','',s)));table.append(head);
  for(const row of rows){const tr=el('tr'),name=el('td'),status=el('td'),ev=el('td'),actions=el('td');name.append(el('span','title',row.data.title),el('code','',row.id),el('div','small muted',row.data.arm+(row.data.campaign_id?' · '+row.data.campaign_id:'')));status.append(pill(row.state));ev.textContent=row.data.assessment_id?'Assessment recorded':row.data.fis_id?'FIS '+row.data.fis_id:'Not exposed';actions.append(button('Inspect',()=>inspect(row.id,'trials')));tr.append(name,status,ev,actions);table.append(tr);}wrap.append(table);return wrap;}
function campaigns(host){host.append(pageTitle('PREVENTION / CHANGE AND RETEST','Prevention campaigns','Register the comparison before the baseline. Retrieve an actual EVALUATION recommendation, verify its implementation, and replay the same approved challenge.',[
 button('New campaign',newCampaign,'primary',!state.token||!experimentOptions().length)]));
 const list=(state.workspace?.entities||[]).filter(x=>x.kind==='campaign');
 if(!list.length){host.append(card('Recommendation-to-result evidence chain'));host.lastChild.append(empty('No prevention campaigns','A recommendation marked implemented is not a prevention result. A campaign requires measured baseline incidents, a pinned version, a verified change and a qualified replay.'));return;}
 for(const c of list){const x=card(c.data.title);x.append(pill(c.state),el('p','muted',c.data.comparison.claim.replaceAll('_',' ')),el('code','small',c.id),el('p','small muted','Registered comparison: '+c.data.plan_sha256),button('Open campaign',()=>inspect(c.id,'prevention'),'primary'));host.append(x);}
}
function evidence(host){host.append(pageTitle('EVIDENCE / PROVENANCE','Evidence & reports','Inspect source responses, operation identities, independently measured samples, pinned assessments and campaign comparisons.',[
 button('Export Grafana dashboard',async()=>LabCharts.download('agent-validation-grafana.json',JSON.stringify(await api('grafana'),null,2),'application/json'),'',!state.token),button('Backup SQLite',backup,'',!state.token)]));
 const records=(state.workspace?.records||[]).filter(r=>['assessment','comparison','diagnosis','recommendation','change_verification','workflow_error'].includes(r.kind));
 if(!records.length){host.append(empty('No evidence has been collected','Sources are captured by the backend. The application has no endpoint for importing fabricated measurements or overwriting prior evidence.'));return;}
 const wrap=el('div','card table-wrap'),table=el('table'),header=el('tr');['Kind','Record','Captured','Open'].forEach(s=>header.append(el('th','',s)));table.append(header);
 for(const r of records.slice().reverse()){const row=el('tr');row.append(el('td','',r.kind),el('td','small',r.id),el('td','small',r.created_at));const td=el('td');td.append(button('Inspect',()=>showRecord(r.id)));row.append(td);table.append(row);}wrap.append(table);host.append(wrap);
}
function connections(host){host.append(pageTitle('QUALIFICATION / ADMINISTRATOR BOUNDARIES','Instruments & access','Connections and execution instruments are configured on the host. The browser cannot introduce AWS keys, arbitrary target URLs, SDK operations or runbook parameters.'));
 const bindings=state.config?.bindings||[];
 if(!bindings.length){const c=card('No environment is configured');c.append(el('p','muted','Populate the configuration template with your two account IDs, Agent Space, existing association, native incident reference contract, workload endpoint and approved FIS template.'),el('pre','',`python configure.py --schema\npython configure.py --check config.local.json\npython run.py --config config.local.json --with-worker`),el('p','small muted','Execution is disabled in the distributed configuration. No credentials, accounts, scenarios or measurements are preloaded.'));host.append(c);return;}
 for(const b of bindings){const c=card(b.name,b.environment+' · '+b.deployment_model);c.append(el('pre','',JSON.stringify(b,null,2)));host.append(c);}
 host.append(el('div','notice','This release executes duration-bounded FIS templates with explicit ARN targets. Selector-based EKS pod targets, destructive one-shot faults, and local-runtime fault injection are not qualified by this adapter. Unsupported definitions are blocked rather than labelled supported.'));
}
async function showRecord(id){const record=await api('records/'+encodeURIComponent(id));const box=el('div');box.append(el('p','small muted','SHA-256 '+record.sha256),el('pre','',JSON.stringify(record.data,null,2)),button('Download record',()=>LabCharts.download(id.replaceAll(':','-')+'.json',JSON.stringify(record,null,2),'application/json')));modal(record.kind+' · '+id,box);}
function renderDetail(host){
 const {entity,records,events,operations,probes}=state.detail,d=entity.data;
 const actions=[button('Back',()=>route(entity.kind==='campaign'?'prevention':entity.kind==='trial'?'trials':'prevention'))];
 if(entity.kind==='trial'){
  if(['DRAFT','BLOCKED'].includes(entity.state))actions.push(button('Qualify instruments',()=>command('trials/'+entity.id+'/qualify'),'primary'));
  if(entity.state==='READY'){actions.push(button('Approve exact trial',()=>approval(entity.id,'start')));actions.push(button('Start approved trial',()=>command('trials/'+entity.id+'/start'),'primary',!d.start_approval_id));}
  if(!['CLOSED','CLOSED_BLOCKED','CLOSED_ABORTED','DRAFT','READY'].includes(entity.state))actions.push(button('Abort and restore',()=>abortDialog(entity.id),'danger'));
  if(entity.state==='RESTORE_REQUIRED')actions.push(button('Recheck restoration',()=>command('trials/'+entity.id+'/retry-cleanup'),'danger'));
  if(d.ground_truth_id)actions.push(button('Assess diagnosis',()=>diagnosisForm(entity,records)));
  if(d.assessment_id)actions.push(button('Reassess pinned evidence',()=>command('trials/'+entity.id+'/assess')));
 }
 if(entity.kind==='campaign'){
  if(entity.state==='BASELINES'){actions.push(button('Add baseline trial',()=>createCampaignTrial(entity,'baseline'),'primary'));actions.push(button('Request evaluation',()=>approval(entity.id,'evaluation')));}
  if(entity.state==='REPLAY_READY'){actions.push(button('Create matched replay',()=>createCampaignTrial(entity,'treatment'),'primary'));actions.push(button('Compare evidence',()=>command('campaigns/'+entity.id+'/compare')));actions.push(button('Add benign control',()=>createCampaignTrial(entity,'benign')));}
 }
 if(entity.kind==='change'){
  if(entity.state==='PROPOSED')actions.push(button('Approve exact runbook',()=>approval(entity.id,'change'),'primary'));
  if(['VERIFIED','RESTORE_REQUIRED'].includes(entity.state))actions.push(button('Approve rollback',()=>approval(entity.id,'rollback'),'danger'));
 }
 if(entity.state==='UNKNOWN_REMOTE_STATE')actions.push(button('Reconcile provider identity',()=>reconcileForm(entity)));
 actions.push(button('Export JSON',()=>exportEntity(entity.id)),button('Download report',()=>downloadReport(entity.id)));
 host.append(pageTitle(entity.kind.toUpperCase()+' / '+entity.id,d.title||entity.id,'State transitions and source evidence are retained. Approvals apply only to the exact recorded target and action.',actions));
 host.append(pill(entity.state));if(d.blocking_reason)host.append(el('div','notice',d.blocking_reason));
 const reftext=el('div','details-grid');for(const [label,value]of [['Actual FIS experiment',d.fis_id],['Agent evaluation task',d.evaluation_task_id],['Pinned recommendation',d.recommendation_record_id],['Executing Automation',d.automation_id]]){if(value){const c=card(label);c.append(el('code','',value));reftext.append(c);}}host.append(reftext);
 if(entity.kind==='trial'){
   const progress=el('div','stages');['QUALIFYING','BASELINING','EXPOSING','OBSERVING','CLEANING','CLOSED'].forEach((s,i)=>{const n=el('div','stage'+(entity.state===s?' active':''));n.append(el('b','',String(i+1).padStart(2,'0')),document.createTextNode(s.replaceAll('_',' ')));progress.append(n);});host.append(progress);
   renderTrialGraphs(host,entity,records,probes,events);
   for(const change of (state.workspace?.entities||[]).filter(x=>x.kind==='change'&&x.data.trial_id===entity.id)){const c=card(change.data.title,'Linked intervention');c.append(pill(change.state),button('Inspect intervention',()=>inspect(change.id,'trials')));host.append(c);}
   const assessment=records.find(r=>r.id===d.assessment_id);if(assessment)renderAssessment(host,assessment.data);
   const findings=records.filter(r=>r.kind==='finding');const fc=card('Agent findings',findings.length+' captured versions');
   if(!findings.length)fc.append(el('p','muted','No investigation or mitigation summary has been collected. Publication of a summary is not proof of correctness.'));
   for(const f of findings){const row=el('div','boundary-row');row.append(el('strong','',f.data.recordType),el('p','small muted',f.data.createdAt+' · '+f.id),el('pre','',textContent(f.data.content)),button('Inspect source',()=>showRecord(f.id)));if(f.data.recordType==='mitigation_summary_md'&&entity.state==='OBSERVING')row.append(button('Map approved intervention',()=>changeForm(entity,f)));fc.append(row);}host.append(fc);
 }
 if(entity.kind==='campaign'){
  const c=card('Prevention evidence chain');for(const [title,value]of [['Registered claim',d.comparison.claim],['Evaluation task',d.evaluation_task_id],['Recommendation version',d.recommendation_record_id],['Verified implementation',d.change_id],['Comparison',d.comparison_id]]){const row=el('div','boundary-row');row.append(el('strong','',title),el('p','muted',value||'Not yet recorded'));c.append(row);}host.append(c);
  for(const r of records.filter(x=>x.kind==='recommendation')){const box=card(r.data.recommendation.title,'Version '+r.data.recommendation.version);box.append(el('pre','',textContent(r.data.recommendation.content)));if(['RECOMMENDATIONS','CHANGE_REVIEW'].includes(entity.state))box.append(button('Pin this version',()=>command('campaigns/'+entity.id+'/pin',{record_id:r.id}),'primary'));if(r.id===d.recommendation_record_id)box.append(button('Map implementation',()=>changeForm(entity,r)));host.append(box);}
  const cs=(state.workspace?.entities||[]).filter(x=>x.kind==='change'&&x.data.campaign_id===entity.id);for(const c of cs){const box=card(c.data.title);box.append(pill(c.state),button('Inspect and approve',()=>inspect(c.id,'prevention')));host.append(box);}
  const linked=(state.workspace?.entities||[]).filter(x=>x.kind==='trial'&&x.data.campaign_id===entity.id);if(linked.length)host.append(trialTable(linked));
  const comparison=records.find(x=>x.id===d.comparison_id);if(comparison){const c=card('Matched comparison');c.append(pill(comparison.data.outcome));for(const reason of comparison.data.blockers)c.append(el('p','muted',reason));for(const pair of comparison.data.pairs){c.append(el('p','',pair.baseline_trial+' → '+pair.replay_trial),pill(pair.outcome),el('p','muted',pair.reason));const graphs=el('div','metric-grid');for(const metric of ['bad_probe_seconds','failed_probe_requests','probe_latency_p95_ms'])graphs.append(chart(metric.replaceAll('_',' '),'recorded scalar',[{name:'Baseline',isolated:true,points:[{t:comparison.created_at,value:pair.baseline_metrics[metric]}]},{name:'Replay',isolated:true,points:[{t:comparison.created_at,value:pair.replay_metrics[metric]}]}]));c.append(graphs);}host.append(c);}
 }
 const sources=card('Evidence and operation ledger');
 const details=el('details');details.append(el('summary','',records.length+' immutable records'));const table=el('div','table-wrap');for(const r of records.slice().reverse()){const row=el('div','boundary-row');row.append(el('span','small',r.kind+' · '+r.created_at+' · '),button(r.id,()=>showRecord(r.id)));table.append(row);}details.append(table);sources.append(details);
 for(const op of operations){const row=el('div','boundary-row');row.append(el('strong','',op.name+' · '+op.state),el('code','small',op.provider_id||op.id),el('p','small muted','Request digest '+op.request_sha256));sources.append(row);}host.append(sources);
 const timeline=card('Lifecycle journal','Most recent 40 events');const list=el('ul','event-list');for(const e of events.slice(-40).reverse()){const li=el('li');li.append(el('time','',e.at.slice(11,19)+' UTC'),el('b','',e.type));list.append(li);}timeline.append(list);host.append(timeline);
}
function renderTrialGraphs(host,entity,records,probes,events){
 const grid=el('div','metric-grid');const markers=events.filter(e=>['trial.exposure_started','trial.fault_verified','trial.cleanup_verified','trial.closed','trial.abort_requested'].includes(e.type)).map(e=>({t:e.at,label:e.type}));
 grid.append(chart('Independent probe latency','ms',[{name:'Recorded GET requests',points:probes.map(p=>({t:p.at,value:p.attempted?p.latency_ms:null})),interval_ms:15000}],markers));
 grid.append(chart('Independent business probe outcome','1 = success',[{name:'Recorded GET responses',points:probes.map(p=>({t:p.at,value:p.attempted?Number(p.success):null})),interval_ms:15000}],markers));
 const obs=records.filter(r=>r.kind==='observation').at(-1);for(const m of obs?.data.metrics||[])grid.append(chart(m.title,m.unit,[{name:(m.account_id||'Primary workload')+' / '+(m.region||'configured Region')+' · '+m.id,points:m.points.map(p=>({t:p.at,value:p.value,source:obs.id})),interval_ms:m.period_seconds*1000}],markers));
 const assessment=records.find(r=>r.id===entity.data.assessment_id);
 if(assessment)for(const [key,value]of Object.entries(assessment.data.metrics)){const def=assessment.data.metric_definitions?.[key];grid.append(chart(def?.title||key.replaceAll('_',' '),def?.unit||(key.endsWith('_seconds')?'s':key.endsWith('_ms')?'ms':'measured'),[{name:'Pinned assessment',isolated:true,points:value===null?[]:[{t:assessment.created_at,value,source:assessment.id}]}]));}
 host.append(grid);
}
function renderAssessment(host,assessment){const c=card('Separate validation claims','No aggregate readiness score');const table=el('table');for(const [name,result]of Object.entries(assessment.dimensions)){const tr=el('tr'),td=el('td');td.append(pill(result.outcome));tr.append(el('td','',name.replaceAll('_',' ')),td,el('td','muted',result.reason));table.append(tr);}c.append(table);host.append(c);}
function textContent(value){if(typeof value==='string')return value;if(Array.isArray(value))return value.map(textContent).join('\n');if(value&&typeof value==='object')return Object.values(value).map(textContent).join('\n');return String(value??'');}
async function command(path,body={}){await api(path,body);await refresh();}
function newTrial(){const f=el('form'),spec=select('Experiment revision',experimentOptions());f.append(spec.wrap,el('p','form-note','The draft is registered immediately. Qualification, approval and start are separate actions. No task ID or measurement is entered.'));formFooter(f,'Register trial',async()=>{const t=await api('trials',{experiment_ref:spec.box.value,arm:'baseline'});state.selected=t.id;state.view='trials';});modal('Register response trial',f);}
async function createCampaignTrial(campaign,arm){const t=await api('trials',{experiment_ref:campaign.data.experiment_ref,campaign_id:campaign.id,arm});await inspect(t.id,'trials');await refresh();}
function newCampaign(){const f=el('form'),title=input('Campaign title'),spec=select('Experiment revision',experimentOptions()),claim=select('Pre-registered prevention claim',[['prevent_recurrence','Prevent recurrence'],['reduce_impact','Reduce impact'],['detect_earlier','Detect earlier — requires benign controls']]),history=input('History, trial ordering and known confounders','textarea'),improvement=input('Required relative improvement (0–1)','number'),pairs=input('Minimum matched pairs','number','1');
 improvement.box.step='.01';improvement.box.min='.01';improvement.box.max='1';f.append(title.wrap,spec.wrap,claim.wrap,improvement.wrap,pairs.wrap,history.wrap);formFooter(f,'Register comparison plan',async()=>{const c=await api('campaigns',{title:title.box.value,experiment_ref:spec.box.value,comparison:{claim:claim.box.value,minimum_improvement:Number(improvement.box.value),minimum_pairs:Number(pairs.box.value),knowledge_history_note:history.box.value}});state.selected=c.id;state.view='prevention';});modal('Register prevention campaign',f);}
function newExperiment(){
 const f=el('form'),title=input('Experiment title'),id=input('Definition ID (letters, numbers, hyphens)'),binding=select('Configured environment',(state.config?.bindings||[]).map(b=>[b.id,b.name])),fault=select('Approved fault instrument',[]),probe=select('Real workload probe',[]),mode=select('Incident path',[['native','Native incident delivery'],['assisted','Assisted investigation — not a delivery test']]);
 const hypothesis=input('Requirement and test purpose','textarea'),code=input('Ground-truth mechanism code'),cause=input('Expected causal mechanism (not sent to agent)','textarea'),rubric=input('Diagnosis rubric and acceptable causal explanation','textarea'),error=input('Maximum request error ratio (0–1)','number'),latency=input('Maximum request latency (milliseconds)','number'),seconds=input('Observation duration (seconds)','number','600');error.box.step='.001';
 function options(){const b=state.config.bindings.find(x=>x.id===binding.box.value);fault.box.replaceChildren();probe.box.replaceChildren();for(const r of b.faults){const o=el('option','',r.title);o.value=r.id;fault.box.append(o);}for(const r of b.probes){const o=el('option','',r.title);o.value=r.id;probe.box.append(o);}}binding.box.onchange=options;options();
 f.append(title.wrap,id.wrap,binding.wrap,fault.wrap,probe.wrap,mode.wrap,hypothesis.wrap,code.wrap,cause.wrap,rubric.wrap,error.wrap,latency.wrap,seconds.wrap,el('p','form-note','Use service-owned limits. The initial oracle references the approved fault targets and configured verifiers; inspect the registered contract before approval. Advanced definitions can be uploaded as strict JSON.'));
 f.append(button('Upload definition JSON',()=>jsonForm('Register a full experiment contract',async data=>api('experiments',data))));
 formFooter(f,'Register immutable definition',async()=>{const b=state.config.bindings.find(x=>x.id===binding.box.value),chosen=b.faults.find(x=>x.id===fault.box.value);await api('experiments',{id:id.box.value,revision:1,title:title.box.value,binding_id:b.id,fault_id:chosen.id,probe_id:probe.box.value,mode:mode.box.value,hypotheses:hypothesis.box.value,observation_seconds:Number(seconds.box.value),max_error_ratio:Number(error.box.value),max_latency_ms:Number(latency.box.value),oracle:{mechanism_code:code.box.value,mechanism_description:cause.box.value,affected_resource_arns:chosen.targets,required_checks:chosen.fault_checks||[b.checks[0].id],rubric:rubric.box.value},intervention_runbook_ids:[]});state.view='trials';});modal('Register experiment',f);
}
function jsonForm(title,submit,seed={}){const f=el('form'),box=el('textarea','json');box.required=true;box.value=JSON.stringify(seed,null,2);const upload=el('input');upload.type='file';upload.accept='.json,application/json';upload.onchange=async()=>{if(upload.files[0])box.value=await upload.files[0].text();};f.append(el('p','form-note','Strict schema validation applies. Imported definitions cannot add new credentials, targets or execution instruments.'),upload,box);formFooter(f,'Validate and save',()=>submit(JSON.parse(box.value)));modal(title,f);}
async function approval(id,purpose){const subject=await api('entities/'+id+'/approval/'+purpose),f=el('form'),name=input('Approver name'),reason=input('Approval rationale','textarea'),token=input('Separate local approval token','password'),confirm=input('Type the exact confirmation shown below');f.append(el('p','notice','This authorizes a real AWS operation when the worker dispatches it. Review the exact targets, pinned versions, parameters and rollback before approving.'),el('pre','',JSON.stringify(subject.subject,null,2)),el('pre','',subject.confirmation),name.wrap,reason.wrap,confirm.wrap,token.wrap);formFooter(f,'Approve exact '+purpose,()=>api('entities/'+id+'/approve/'+purpose,{expected_digest:subject.digest,confirmation:confirm.box.value,approver:name.box.value,rationale:reason.box.value},token.box.value));modal('Execution approval',f);}
function abortDialog(id){const f=el('form');f.append(el('p','notice','Abort requests stopping and restoration. It is not proof of cleanup. Do not close an unresolved trial or assume an AWS write failed merely because the connection timed out.'));formFooter(f,'Request abort and cleanup',()=>api('trials/'+id+'/abort',{}));modal('Abort active experiment',f);}
function diagnosisForm(entity,records){const findings=records.filter(r=>r.kind==='finding'&&r.data.recordType==='investigation_summary_md');if(!findings.length){toast('No actual investigation summary is available to assess.');return;}const f=el('form'),finding=select('Collected finding',findings.map(x=>[x.id,x.data.createdAt+' · '+x.data.recordId])),name=input('Reviewer'),quote=input('Exact finding quotation','textarea'),resources=input('Asserted affected ARNs, one per line','textarea'),mechanism=input('Mechanism code asserted by the finding'),evidence=input('Verifier source record ID'),evidenceQuote=input('Exact quote from the independent verifier response','textarea'),reason=input('Rubric-based rationale','textarea');f.append(el('p','notice','Extract what the agent actually asserted. Do not copy the expected answer into the claim. Citations must belong to the independent ground-truth capture.'),finding.wrap,name.wrap,quote.wrap,resources.wrap,mechanism.wrap,evidence.wrap,evidenceQuote.wrap,reason.wrap);formFooter(f,'Save cited claim assessment',()=>api('trials/'+entity.id+'/diagnosis',{reviewer:name.box.value,finding_record_id:finding.box.value,finding_quote:quote.box.value,asserted_resource_arns:resources.box.value.split('\n').map(x=>x.trim()).filter(Boolean),asserted_mechanism_code:mechanism.box.value,citations:[{record_id:evidence.box.value,quote:evidenceQuote.box.value}],rationale:reason.box.value,material_unsupported_claims:[]}));modal('Structured diagnosis assessment',f);}
function changeForm(entity,source){const binding=state.config.bindings.find(b=>state.workspace.experiments.find(e=>e.id===entity.data.experiment_ref)?.data.binding_id===b.id)||state.config.bindings[0];if(!binding?.runbooks.length){toast('No pinned implementation runbooks are configured. Register and review the exact implementation on the host first.');return;}const f=el('form'),book=select('Administrator-registered runbook',binding.runbooks.map(x=>[x.id,x.title+' · version '+x.version])),name=input('Proposer'),quote=input('Exact recommendation or mitigation quotation','textarea'),reason=input('Why this reviewed implementation realizes the recommendation','textarea');f.append(el('p','notice','Agent text is not executed. This maps the recommendation to a pre-registered, version-pinned Automation runbook and deployed-state verifiers.'),el('pre','',textContent(source.data)),book.wrap,name.wrap,quote.wrap,reason.wrap);formFooter(f,'Create change proposal',async()=>{const c=await api('entities/'+entity.id+'/changes',{runbook_id:book.box.value,source_record_id:source.id,source_quote:quote.box.value,rationale:reason.box.value,proposer:name.box.value});state.selected=c.id;state.view='prevention';});modal('Map recommendation to exact implementation',f);}
function reconcileForm(entity){const f=el('form'),op=select('Uncertain operation',state.detail.operations.filter(o=>['UNKNOWN','DISPATCHING'].includes(o.state)).map(o=>[o.id,o.name+' · '+o.id])),provider=input('Provider experiment, task or Automation ID');f.append(el('p','notice','The backend will read and verify the provider operation against the original intent. It will not accept an unrelated ID or repeat the write.'),op.wrap,provider.wrap);formFooter(f,'Read and reconcile',()=>api('entities/'+entity.id+'/reconcile',{operation_id:op.box.value,provider_id:provider.box.value}));modal('Reconcile an uncertain operation',f);}
async function exportEntity(id){const data=await api('entities/'+id+'/export');LabCharts.download(id+'.json',JSON.stringify(data,null,2),'application/json');}
async function downloadReport(id){const r=await fetch('/api/entities/'+id+'/report',{headers:{Authorization:'Bearer '+state.token}});if(!r.ok)throw Error('Report export failed');LabCharts.download(id+'.html',await r.text(),'text/html');}
async function backup(){const r=await fetch('/api/backup',{headers:{Authorization:'Bearer '+state.token}});if(!r.ok)throw Error('Backup failed');const a=document.createElement('a');a.href=URL.createObjectURL(await r.blob());a.download='agent-validation.sqlite3';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
$('#modal-close').onclick=()=>$('#modal').close();$('#unlock-button').onclick=showUnlock;$('#refresh-button').onclick=()=>refresh().catch(fail);
for(const b of document.querySelectorAll('[data-view]'))b.addEventListener('click',()=>route(b.dataset.view));
setInterval(()=>{if(state.token&&!$('#modal').open)refresh().catch(e=>{if(e.message==='Unauthorized')lock();});},10000);
render();
