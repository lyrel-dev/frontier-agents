(function () {
  'use strict';
  const Seed = globalThis.HealthDemoData;
  const Model = globalThis.HealthDemoModel;
  const Diagram = globalThis.HealthDemoDiagrams || {};
  const STORAGE_KEY = 'pulse-aws-health-demo-v1';
  const clone = value => JSON.parse(JSON.stringify(value));
  const e = value => String(value == null ? '' : value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const $ = selector => document.querySelector(selector);
  const paths = {
    grid:'M3 3h7v7H3z M14 3h7v7h-7z M3 14h7v7H3z M14 14h7v7h-7z',
    pulse:'M2 12h4l3-7 5 14 3-7h5',
    list:'M8 5h13 M8 12h13 M8 19h13 M3 5h.01 M3 12h.01 M3 19h.01',
    check:'M20 6 9 17l-5-5',
    tasks:'M9 5h11 M9 12h11 M9 19h11 M2 5l2 2 3-4 M2 12l2 2 3-4 M2 19l2 2 3-4',
    calendar:'M4 5h16v16H4z M8 3v4 M16 3v4 M4 10h16 M8 14h2 M14 14h2 M8 18h2',
    signal:'M4 20v-5 M9 20v-9 M14 20V7 M19 20V3',
    nodes:'M9 3h6v6H9z M2 16h6v6H2z M16 16h6v6h-6z M12 9v4 M5 16v-3h14v3',
    search:'M21 21l-5-5 M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0',
    arrow:'M5 12h14 M14 7l5 5-5 5',
    chevron:'m9 5 7 7-7 7',
    external:'M14 3h7v7 M21 3l-11 11 M10 3H3v18h18v-7',
    download:'M12 3v12 M7 10l5 5 5-5 M4 16v5h16v-5',
    play:'m8 4 12 8-12 8z',
    refresh:'M20 7a9 9 0 1 0 1 9 M20 2v6h-6',
    close:'M6 6l12 12 M6 18 18 6',
    globe:'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0 M3 12h18 M12 3c5 5 5 13 0 18 M12 3c-5 5-5 13 0 18',
    accounts:'M15 21v-3a6 6 0 0 0-12 0v3 M14 5a4 4 0 1 1-8 0 4 4 0 0 1 8 0 M17 10a4 4 0 0 1 4 4v5 M18 2a4 4 0 0 1 0 7',
    cube:'m12 3 9 5v9l-9 5-9-5V8z M3 8l9 5 9-5 M12 13v9 M8 5l9 5',
    warning:'m12 3 10 18H2z M12 9v5 M12 17v.1',
    info:'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0 M12 11v6 M12 7v.1',
    clock:'M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0 M12 7v5l3 2',
    shield:'m12 3 8 3v6c0 4-4 7-8 9-4-2-8-5-8-9V6z M8 12l3 3 5-6',
    file:'M4 3h10l6 6v12H4z M14 3v6h6 M8 13h8 M8 17h6',
    copy:'M8 8h13v13H8z M16 8V3H3v13h5',
    menu:'M3 6h18 M3 12h18 M3 18h18',
    bell:'M5 17h14l-2-3V9a5 5 0 0 0-10 0v5z M10 21h4',
    eye:'M2 12s4-7 10-7 10 7 10 7-4 7-10 7-10-7-10-7 M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0'
  };
  const icon = name => '<svg class="icon" aria-hidden="true" viewBox="0 0 24 24"><path d="' + (paths[name] || paths.cube) + '"></path></svg>';
  const nav = [
    ['overview','Overview','grid'],['events','Event feed','list'],['actions','Action center','tasks'],
    ['lifecycle','Lifecycle posture','calendar'],['coverage','Coverage','signal'],['model','Model & report','nodes']
  ];
  const views = {
    overview:['YOUR AWS ESTATE, IN CONTEXT','Health overview','Reported impact, upcoming changes, and the work that needs attention.'],
    events:['AWS-REPORTED EVIDENCE','Event feed','Explore each event in its account context, with source state and completeness.'],
    actions:['THE HUMAN SIDE OF RESPONSE','Action center','Own the response. Keep operator progress separate from AWS confirmation.'],
    lifecycle:['PLAN BEFORE THE CHANGE','Lifecycle posture','Match version timelines to deployed components and understand future exposure.'],
    coverage:['KNOW WHAT YOU CAN SEE','Collection coverage','Fresh collection and fresh provider evidence are different signals.'],
    model:['FROM EVIDENCE TO OPERATIONS','Model & report','The reviewed relationships behind this prototype, with editable diagrams and sources.']
  };
  let storageAvailable = true;
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null'); } catch (_) { storageAvailable = false; }
  const validStates = ['new','acknowledged','in_progress','completed','verified'];
  let workItems = clone(Seed.workItems);
  if (saved && saved.version === 1 && Array.isArray(saved.workItems)) {
    workItems = workItems.map(item => {
      const stored = saved.workItems.find(x => x && x.id === item.id);
      if (!stored) return item;
      if (validStates.includes(stored.state)) item.state = stored.state;
      if (typeof stored.owner === 'string' && stored.owner.length < 100) item.owner = stored.owner;
      if (typeof stored.updatedAt === 'string' && Number.isFinite(Date.parse(stored.updatedAt))) item.updatedAt = stored.updatedAt;
      if (Array.isArray(stored.notes)) item.notes = stored.notes.filter(x => x && typeof x.text === 'string' && typeof x.at === 'string').slice(-100);
      if (Array.isArray(stored.actions)) item.actions = stored.actions.filter(x => x && typeof x.at === 'string').slice(-100);
      return item;
    });
  }
  let data = clone(Seed);
  const filters = { q:'',account:'all',region:'all',category:'all',scope:'all',status:'all',actionability:'all' };
  const state = { view:nav.some(x => x[0] === location.hash.slice(1)) ? location.hash.slice(1) : 'overview',filters,detail:null,detailTab:'summary',diagram:'01-core-model',horizon:30,replayed:!!(saved && saved.version === 1 && saved.replayed),collectionAt:saved && saved.collectionAt || null,actionCounter:0 };
  function replayProvider() {
    const r = data.replay;
    const entity = data.entities.find(x => x.id === r.impactId);
    const context = data.contexts.find(x => x.id === r.contextId);
    entity.statusCode = r.newProviderStatus;
    entity.updatedAt = r.at;
    context.lastUpdatedTime = r.at;
    context.description = r.body;
    const event = data.events.find(x=>x.id===r.eventId);
    event.summary = 'AWS now reports payment-webhook resolved after the runtime upgrade. Other functions remain pending, so the shared event stays open. Local workflow and the earlier inventory observation remain separate.';
    if (Date.parse(r.at) > Date.parse(data.meta.asOf)) data.meta.asOf = r.at;
    if (!data.updates.some(x => x.id === r.id)) data.updates.push({id:r.id,eventId:r.eventId,contextId:r.contextId,kind:'aws',at:r.at,title:r.title,body:r.body});
  }
  if (state.replayed) replayProvider();
  if (state.collectionAt && Number.isFinite(Date.parse(state.collectionAt))) {
    data.coverage.forEach(x => { if (x.status === 'complete') x.lastSuccessAt = state.collectionAt; });
    if (Date.parse(state.collectionAt) > Date.parse(data.meta.asOf)) data.meta.asOf = state.collectionAt;
  }
  const byId = (list,id) => list.find(x => x.id === id);
  const accountName = id => (byId(data.accounts,id) || {}).name || 'Public context';
  const regionName = code => data.meta.regionLabels[code] || code;
  const fmtTime = value => value && Number.isFinite(Date.parse(value)) ? new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Zurich',hour:'2-digit',minute:'2-digit'}).format(new Date(value)) + ' CET' : 'Not supplied';
  const fmtDate = value => value && Number.isFinite(Date.parse(value)) ? new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Zurich',day:'numeric',month:'short',year:'numeric'}).format(new Date(value)) : 'Not supplied';
  const age = value => {
    if (!value || !Number.isFinite(Date.parse(value))) return 'Not supplied';
    const minutes = Math.max(0,Math.floor((Date.parse(data.meta.asOf)-Date.parse(value))/60000));
    if (minutes < 1) return 'Just now';
    if (minutes < 60) return minutes + 'm ago';
    if (minutes < 1440) return Math.floor(minutes/60) + 'h ago';
    return Math.floor(minutes/1440) + 'd ago';
  };
  const categoryLabel = v => ({issue:'Issue',scheduledChange:'Scheduled change',accountNotification:'Account notice'}[v] || v);
  const workflowLabel = v => ({new:'Needs attention',acknowledged:'Acknowledged',in_progress:'In progress',completed:'Awaiting verification',verified:'Verified'}[v] || v);
  function badge(value, label) {
    const colors = {open:'red',closed:'green',upcoming:'blue',mixed:'amber',IMPAIRED:'red',UNIMPAIRED:'green',PENDING:'amber',RESOLVED:'green',UNKNOWN:'gray',complete:'green',partial:'amber',stale:'amber',unavailable:'red',unknown:'gray',new:'amber',acknowledged:'blue',in_progress:'blue',completed:'purple',verified:'green',ACTION_REQUIRED:'amber',ACTION_MAY_BE_REQUIRED:'blue',INFORMATIONAL:'gray'};
    const labels = {open:'Open',closed:'Closed',upcoming:'Upcoming',mixed:'Mixed contexts',IMPAIRED:'Impaired',UNIMPAIRED:'Unimpaired',PENDING:'Pending action',RESOLVED:'Resolved',UNKNOWN:'Unknown',complete:'Complete',partial:'Partial',stale:'Stale',unavailable:'Unavailable',unknown:'Unknown',ACTION_REQUIRED:'Action required',ACTION_MAY_BE_REQUIRED:'Action may be required',INFORMATIONAL:'Informational'};
    if (value == null) return '<span class="badge gray outline">Not supplied</span>';
    return '<span class="badge '+(colors[value] || 'gray')+'"'+(value==='mixed'?' title="Local rollup of different account context states"':'')+'>'+e(label || labels[value] || workflowLabel(value))+'</span>';
  }
  const serviceName = value => ({LAMBDA:'Lambda',ELASTICLOADBALANCING:'ELB',BILLING:'Billing'}[value] || value);
  const serviceIcon = service => '<span class="service-icon svc-'+e(String(service).toLowerCase().replace(/[^a-z0-9]/g,''))+'">'+icon(service === 'RDS' ? 'cube' : service === 'S3' ? 'cube' : service === 'EKS' ? 'nodes' : service === 'IAM' ? 'shield' : 'cube')+'</span>';
  const pendingLabel = n => n + ' pending ' + (n === 1 ? 'entity' : 'entities');
  const priorityOrder = {critical:0,high:1,medium:2,low:3};
  const rows = () => Model.eventRows(data,filters);
  const selectedWork = () => Model.workRows(data,workItems,filters);
  function persist() {
    try { localStorage.setItem(STORAGE_KEY,JSON.stringify({version:1,workItems,replayed:state.replayed,collectionAt:state.collectionAt})); }
    catch (_) { storageAvailable = false; toast('Browser storage is unavailable. Changes remain in memory; export a snapshot before leaving.',true); }
  }
  let toastTimer;
  function toast(message,error) { clearTimeout(toastTimer);const el=$('#toast');el.textContent=message;el.classList.toggle('error',!!error);el.hidden=false;toastTimer=setTimeout(()=>{el.hidden=true;},6500); }
  function empty(title,description) { return '<div class="empty-state">'+icon('search')+'<strong>'+e(title)+'</strong><span>'+e(description)+'</span><br><button class="button button-secondary" data-action="clear">Clear filters</button></div>'; }
  function currentEvent(id) { return Model.eventRows(data,{q:'',account:filters.account,region:'all',category:'all',scope:'all',status:'all',actionability:'all'}).find(x=>x.id===id) || Model.eventRows(data,{}).find(x=>x.id===id); }
  function workForEvent(id) { return Model.workRows(data,workItems,{account:filters.account}).filter(x => (x.eventIds || []).includes(id)); }
  function coverageForEvent(id) {
    const event = byId(data.events,id);
    const accountIds = (currentEvent(id).accounts || []).map(c=>c.id);
    return data.coverage.filter(c=>(!c.accountId || accountIds.includes(c.accountId)) && (c.eventId===id || (!c.eventId && (!c.region || c.region==='all' || c.region===event.region))));
  }
  function coverageState(records) { const statuses=records.map(x=>x.status);return ['unavailable','partial','stale'].find(x=>statuses.includes(x)) || (records.length?'complete':'unknown'); }
  function metric(label,value,caption,name,accent,suffix) {
    return '<div class="metric accent-'+accent+'"><div class="metric-top"><span>'+e(label)+'</span><span class="metric-icon">'+icon(name)+'</span></div><div class="metric-value">'+e(value)+(suffix?'<small>'+e(suffix)+'</small>':'')+'</div><div class="metric-caption"><span class="dot '+(accent==='amber'?'amber':accent==='red'?'red':accent==='green'?'green':'blue')+'"></span>'+e(caption)+'</div></div>';
  }
  function renderMetrics() {
    const m=Model.metrics(data,filters), c=Model.coverageSummary(data,filters);
    const exposures=Model.lifecycleRows(data,filters).filter(x=>x.applicability==='confirmed' && Number.isFinite(x.daysUntil) && x.daysUntil>=0 && x.daysUntil<=30);
    const resources=new Set(exposures.map(x=>x.resource && x.resource.id || (byId(data.deployments,x.deploymentId)||{}).resourceId)); resources.delete(undefined);
    return '<div class="metric-grid">'+metric('Open AWS issues',m.openIssues,m.impairedEntities+' observed impaired entities','pulse','red')+metric('Pending entity actions',m.pendingEntities,'AWS state · independent of local work','tasks','amber')+metric('Lifecycle within 30 days',resources.size,'Distinct inventory resources · demo dates','calendar','blue')+metric('Complete collection scopes',c.complete,c.total-c.complete+' scopes partial or stale','signal',c.complete===c.total?'green':'amber','/ '+c.total)+'</div>';
  }
  function matrixMarkup() {
    const result=Model.serviceMatrix(data,filters);
    const matrixRows=Array.isArray(result)?result:result.rows || [];
    const regions=filters.region==='all'?Object.keys(data.meta.regionLabels):[filters.region];
    const serviceRows=matrixRows.filter(r=>['EC2','S3','RDS','LAMBDA','EKS'].includes(r.service));
    return '<section class="panel"><div class="panel-header"><div><h2>Service / region activity</h2><p class="panel-subtitle">Reported activity in the selected account scope</p></div><span class="small-kicker">'+regions.length+' '+(regions.length===1?'REGION':'REGIONS')+'</span></div><div class="matrix-wrap"><table class="matrix"><thead><tr><th>Service</th>'+regions.map(region=>'<th><strong>'+e(regionName(region))+'</strong>'+e(region)+'</th>').join('')+'</tr></thead><tbody>'+serviceRows.map(r=>'<tr><td><div class="matrix-service">'+serviceIcon(r.service)+e(serviceName(r.service))+'</div></td>'+regions.map(region=>{
      const cells=Array.isArray(r.cells)?r.cells:Object.values(r.cells||{}); const c=cells.find(x=>x.region===region)||{state:'unknown',count:0,label:'Coverage unknown'};
      const content=c.state==='issue'?'<span class="dot red"></span>'+e(c.count || (c.events||[]).length):c.state==='change'?'<span class="dot blue"></span>'+e(c.count || (c.events||[]).length):c.state==='unknown'?'?':'—';
      return '<td><button class="matrix-cell state-'+e(c.state)+'" data-matrix-service="'+e(r.service)+'" data-matrix-region="'+e(region)+'" aria-label="'+e(r.service+' '+region+': '+(c.label || c.state))+'" title="'+e(c.label || c.state)+'">'+content+'</button></td>';
    }).join('')+'</tr>').join('')+'</tbody></table></div><div class="matrix-footer"><div class="legend"><span><i class="dot red"></i>Active issue</span><span><i class="dot blue"></i>Change</span><span><i class="dot gray"></i>No issue reported</span><span>? Coverage gap</span></div><span>Event evidence, not a workload health check</span></div></section>';
  }
  function attentionMarkup() {
    const list=selectedWork().filter(w=>w.state!=='verified').sort((a,b)=>(priorityOrder[a.priority]??9)-(priorityOrder[b.priority]??9) || Date.parse(a.dueAt)-Date.parse(b.dueAt)).slice(0,3);
    return '<section class="panel"><div class="panel-header"><div><h2>Needs attention</h2><p class="panel-subtitle">Prioritized team response</p></div><span class="badge amber">'+selectedWork().filter(x=>x.state!=='verified').length+' tasks</span></div><div class="attention-list">'+list.map(w=>'<div class="attention-item"><div class="attention-icon '+(w.state==='completed'?'blue':'')+'">'+icon(w.state==='completed'?'eye':'tasks')+'</div><div class="attention-body"><button class="attention-title" data-work="'+e(w.id)+'">'+e(w.title)+'</button><div class="attention-subtitle"><span>'+e(w.owner)+'</span><span>·</span><span>'+e(workflowLabel(w.state))+'</span></div></div><span class="attention-tag '+(w.state==='completed'?'blue':'')+'">'+e(dueLabel(w.dueAt))+'</span></div>').join('')+(list.length?'':'<div class="empty-state">No work in this scope.</div>')+'</div><button class="panel-bottom-link" data-nav="actions">Open action center '+icon('arrow')+'</button></section>';
  }
  function eventTable(list,limit) {
    const all=list.slice().sort((a,b)=>(priorityOrder[a.priority]??9)-(priorityOrder[b.priority]??9)||Date.parse(b.updatedAt)-Date.parse(a.updatedAt));
    const shown=limit?all.slice(0,limit):all;
    if(!shown.length) return empty('No matching events','Try a different search or widen the selected scope.');
    return '<div class="table-scroll"><table class="events-table"><thead><tr><th>Event</th><th>Scope</th><th>AWS state</th><th>Observed entity state</th><th>AWS updated</th><th aria-label="Details"></th></tr></thead><tbody>'+shown.map(r=>'<tr><td><div class="event-name-cell">'+serviceIcon(r.service)+'<div><button class="event-title" data-event="'+e(r.id)+'">'+e(r.title)+'</button><span class="subline">'+e(serviceName(r.service))+' <span aria-hidden="true">·</span> '+e(categoryLabel(r.category))+' <span aria-hidden="true">·</span> '+e(r.region)+'</span></div></div></td><td><span class="scope-label">'+icon(r.scope==='PUBLIC'?'globe':'accounts')+(r.scope==='PUBLIC'?'Public advisory':e(r.accounts.length)+' '+(r.accounts.length===1?'account':'accounts'))+'</span><span class="subline">'+(r.scope==='PUBLIC'?'No reported account impact':e(r.accounts.length===1?r.accounts[0].name:'Reported account contexts'))+'</span></td><td>'+badge(r.status)+(r.coverage && r.coverage.state!=='complete'?'<div class="state-note">'+e(r.coverage.state)+' coverage</div>':'')+'</td><td><span class="entity-tally">'+(r.impairedCount?'<span class="dot red"></span> '+r.impairedCount+' impaired':r.pendingCount?'<span class="dot amber"></span> '+r.pendingCount+' pending':r.scope==='PUBLIC'?'—':r.unsuppliedCount?'Status not supplied':r.unknownCount?r.unknownCount+' unknown':r.entityCount+' observed')+'</span><span class="subline">'+(r.actionability==='ACTION_REQUIRED'?'Action required':r.actionability==='ACTION_MAY_BE_REQUIRED'?'Action may be required':r.scope==='PUBLIC'?'Relevance needs assessment':r.entityCount+' entity records')+'</span></td><td class="time-cell">'+e(age(r.updatedAt))+'<span class="subline">'+e(fmtTime(r.updatedAt))+'</span></td><td><button class="icon-button table-arrow" data-event="'+e(r.id)+'" aria-label="Open '+e(r.title)+'">'+icon('chevron')+'</button></td></tr>').join('')+'</tbody></table></div><div class="feed-footer"><span>Showing '+shown.length+' of '+all.length+' matching events · Counts reflect observed records</span><span>Provider state ≠ operator progress</span></div>';
  }
  function dueLabel(value) {
    if(!value)return 'No due date';
    const day = date => new Intl.DateTimeFormat('sv-SE',{timeZone:'Europe/Zurich',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date(date));
    const days=Math.round((Date.parse(day(value))-Date.parse(day(data.meta.asOf)))/86400000);
    return days<0?Math.abs(days)+'d overdue':days===0?'Due today':days===1?'Due tomorrow':'Due in '+days+'d';
  }
  function overview() { return renderMetrics()+'<div class="overview-grid">'+matrixMarkup()+attentionMarkup()+'</div><section class="panel"><div class="panel-header"><div><h2>Priority event feed</h2><p class="panel-subtitle">The latest evidence across your selected scope</p></div><button class="text-button" data-nav="events">View all events '+icon('arrow')+'</button></div>'+eventTable(rows(),5)+'</section>'; }
  function eventsView() {
    const categories=[['all','All events'],['issue','Issues'],['scheduledChange','Scheduled changes'],['accountNotification','Account notices']];
    return '<div class="filter-chips" role="group" aria-label="Event category">'+categories.map(c=>'<button class="chip '+(filters.category===c[0]?'active':'')+'" data-category="'+c[0]+'" aria-pressed="'+(filters.category===c[0])+'">'+c[1]+'</button>').join('')+'<button class="chip '+(filters.scope==='PUBLIC'?'active':'')+'" data-scope="PUBLIC" aria-pressed="'+(filters.scope==='PUBLIC')+'">Public advisories</button><button class="chip '+(filters.actionability==='ACTION_REQUIRED'?'active':'')+'" data-actionability="ACTION_REQUIRED" aria-pressed="'+(filters.actionability==='ACTION_REQUIRED')+'">Action required</button></div><section class="panel"><div class="panel-header"><div><h2>'+rows().length+' events in scope</h2><p class="panel-subtitle">Open an event to inspect account-specific state, entities and source history</p></div><label class="horizon-select">AWS state <select id="event-status"><option value="all" '+(filters.status==='all'?'selected':'')+'>All states</option><option value="open" '+(filters.status==='open'?'selected':'')+'>Open</option><option value="upcoming" '+(filters.status==='upcoming'?'selected':'')+'>Upcoming</option><option value="closed" '+(filters.status==='closed'?'selected':'')+'>Closed</option></select></label></div>'+eventTable(rows())+'</section>';
  }
  function workCard(w) {
    const pending = w.pendingProviderCount || 0;
    return '<article class="work-card"><div class="work-card-top"><span class="work-id">'+e(w.id.toUpperCase())+'</span>'+badge(w.state)+'</div><h3>'+e(w.title)+'</h3><div class="work-meta"><span class="owner-label"><i class="owner-dot">'+e(w.owner.split(' ').map(s=>s[0]).slice(0,2).join(''))+'</i>'+e(w.owner)+'</span><span>'+e(dueLabel(w.dueAt))+'</span></div><div class="work-evidence"><strong>'+ (pending?pendingLabel(pending)+' in AWS':w.state==='completed'?'Operator work completed':'AWS evidence linked')+'</strong><br>'+(w.state==='completed'?'Verify against source evidence before closing the response.':'Local progress changes do not update provider state.')+'</div><div class="work-card-actions">'+(w.state==='new'?'<button class="button button-secondary button-small" data-work-action="acknowledged" data-work-id="'+e(w.id)+'">Acknowledge</button>':'')+'<button class="button button-secondary button-small" data-work="'+e(w.id)+'">Open task '+icon('arrow')+'</button></div></article>';
  }
  function actionsView() {
    const list=selectedWork();
    const columns=[['Needs attention',['new','acknowledged'],'amber'],['In progress',['in_progress'],'blue'],['Verification',['completed','verified'],'green']];
    return '<div class="info-panel">'+icon('info')+'<p><strong>Team workflow and AWS state stay independent.</strong> Marking work complete records your progress. It does not resolve an AWS entity or remove a catalog-based exposure.</p></div><div class="work-board">'+columns.map(([title,states,color])=>{const matches=list.filter(x=>states.includes(x.state));return '<section class="board-column"><div class="board-heading"><span><i class="dot '+color+'"></i>'+title+'</span><span class="board-count">'+matches.length+'</span></div>'+matches.map(workCard).join('')+(matches.length?'':'<div class="blank-work">No tasks in this scope.</div>')+'</section>';}).join('')+'</div>';
  }
  function lifecycleView() {
    const all=Model.lifecycleRows(data,filters);
    const list=all.filter(x=>!x.unmatched && (!Number.isFinite(x.daysUntil)||x.daysUntil<=state.horizon)).sort((a,b)=>(a.daysUntil??9999)-(b.daysUntil??9999));
    const unmatched=all.filter(x=>x.unmatched).map(x=>x.deployment);
    const metricRow='<div class="metric-grid">'+metric('Confirmed exposures',all.filter(x=>x.applicability==='confirmed').length,'Deployment × milestone assessments','nodes','blue')+metric('Past a milestone',all.filter(x=>x.applicability==='confirmed'&&x.daysUntil<0).length,'Based on the captured inventory','clock','amber')+metric('Within 30 days',all.filter(x=>x.applicability==='confirmed'&&x.daysUntil>=0&&x.daysUntil<=30).length,'Fictional dates for this scenario','calendar','blue')+metric('Unmatched deployments',unmatched.length,'Applicability remains unknown','search','amber')+'</div>';
    return metricRow+'<div class="section-intro"><div><h2>Version exposure</h2><p>What the version catalog means for the components you run.</p></div><label class="horizon-select">Planning horizon <select id="horizon"><option value="30" '+(state.horizon===30?'selected':'')+'>30 days</option><option value="60" '+(state.horizon===60?'selected':'')+'>60 days</option><option value="90" '+(state.horizon===90?'selected':'')+'>90 days</option><option value="365" '+(state.horizon===365?'selected':'')+'>1 year</option></select></label></div><div class="split-layout"><section class="panel">'+(list.length?'<div class="table-scroll"><table class="data-table lifecycle-table"><thead><tr><th>Resource / component</th><th>Milestone</th><th>Timeline</th><th>Assessment</th><th></th></tr></thead><tbody>'+list.map(x=>{const resource=x.resource||byId(data.resources,(x.deployment||byId(data.deployments,x.deploymentId)).resourceId);const deployment=x.deployment||byId(data.deployments,x.deploymentId);const milestone=x.milestone||byId(data.milestones,x.milestoneId);const entry=x.entry||byId(data.catalogEntries,milestone.entryId);return '<tr class="interactive"><td><div class="resource-name"><button data-exposure="'+e(x.id)+'">'+e(resource.name)+'</button></div><span class="subline">'+e(entry.service)+' · '+e(deployment.version)+'<br>'+e(accountName(resource.accountId))+'</span></td><td><span class="entity-tally">'+e(milestone.type.replaceAll('_',' ').toLowerCase())+'</span><div>'+milestone.risks.map(r=>'<span class="risk-pill">'+e(r.replaceAll('_',' '))+'</span>').join('')+'</div></td><td><span class="due-date '+e(x.riskStatus)+'">'+e(fmtDate(milestone.date))+'</span><span class="subline">'+e(x.daysUntil<0?Math.abs(x.daysUntil)+'d past milestone':x.daysUntil===0?'Today':x.daysUntil+' days away')+'</span></td><td>'+badge(x.applicability==='confirmed'?'complete':'unknown',x.applicability==='confirmed'?'Matched':'Review match')+'<span class="subline">Inventory '+e(age(deployment.observedAt))+'</span></td><td><button class="icon-button" data-exposure="'+e(x.id)+'" aria-label="Inspect exposure for '+e(resource.name)+'">'+icon('chevron')+'</button></td></tr>';}).join('')+'</tbody></table></div><div class="feed-footer"><span>'+list.length+' exposure assessments in this horizon</span><span>All milestone dates are fictional</span></div>':empty('No milestones in this horizon','Widen the planning horizon or change the selected scope.'))+'</section><aside class="panel supporting-panel standalone-aside"><h3>How exposure is established</h3><div class="journey-step"><span>1</span><strong>Version catalog</strong>Source milestone, date, region and risk.</div><div class="journey-step"><span>2</span><strong>Observed deployment</strong>A separately collected resource and component version.</div><div class="journey-step"><span>3</span><strong>Matched exposure</strong>Explicit applicability, matching evidence and assessment time.</div><p>Operator completion does not change the inventory scan. Source evidence can arrive later.</p></aside></div>'+(unmatched.length?'<div class="unknown-inventory"><h4>'+icon('info')+' '+unmatched.length+' deployment has no catalog match</h4><p>'+unmatched.map(d=>e((byId(data.resources,d.resourceId)||{}).name)+' · '+e(d.component)+' '+e(d.version)).join(', ')+'. No matching milestone has been invented; support posture remains unknown.</p></div>':'');
  }
  function coverageView() {
    const summary=Model.coverageSummary(data,filters);const records=summary.records||[];
    const regions=filters.region==='all'?Object.keys(data.meta.regionLabels):[filters.region];
    return '<div class="section-intro"><div><h2>Source coverage</h2><p>Organization integration: '+e(data.meta.orgHealthAccessStatus)+' · '+summary.complete+' of '+summary.total+' collection scopes complete</p></div><button class="button button-secondary" data-action="refresh">'+icon('refresh')+' Refresh observations</button></div><div class="coverage-grid">'+regions.map(region=>{const rr=records.filter(x=>x.region===region||x.region==='all');const status=coverageState(rr);return '<div class="coverage-region"><span class="region-icon">'+icon('globe')+'</span><h3>'+e(regionName(region))+'</h3><p>'+e(region)+'</p>'+badge(status)+'</div>';}).join('')+'</div><section class="panel"><div class="panel-header"><div><h2>Collection scopes and gaps</h2><p class="panel-subtitle">A successful fetch does not rewrite the provider’s update timestamp</p></div></div><div class="table-scroll"><table class="data-table coverage-table"><thead><tr><th>Scope</th><th>Collection state</th><th>Last successful collection</th><th>Provider evidence</th><th>Completeness / reason</th></tr></thead><tbody>'+records.map(c=>'<tr><td><strong>'+e(c.accountId?accountName(c.accountId):'Organization / public feed')+'</strong><span class="subline">'+e(c.region)+' · '+e(c.channel)+'</span></td><td>'+badge(c.status)+'</td><td class="time-cell">'+e(fmtTime(c.lastSuccessAt))+'<span class="subline">'+e(age(c.lastSuccessAt))+'</span></td><td class="time-cell">'+e(fmtTime(c.sourceUpdatedAt))+'<span class="subline">'+e(age(c.sourceUpdatedAt))+'</span></td><td><div class="coverage-note">'+(c.totalPages?'<strong>'+c.pagesReceived+' / '+c.totalPages+' pages received</strong><br>':'')+e(c.reason || 'Collection is complete for this declared scope.')+'</div></td></tr>').join('')+'</tbody></table></div></section><div class="info-panel amber wide-note">'+icon('info')+'<p><strong>Coverage is part of the answer.</strong> Partial pagination, stale collection, and unsupplied entity states stay visible. A quiet or incomplete feed cannot establish that a workload is healthy. This scenario uses a downscaled page example to demonstrate assembly.</p></div>';
  }
  function modelView() {
    const models=[['01-core-model','Event & impact'],['02-history-delivery','History & delivery'],['03-lifecycle-posture','Lifecycle posture'],['04-operator-workflow','Operator workflow']];
    return '<div class="diagram-tabs" role="group" aria-label="Data model diagrams">'+models.map(x=>'<button class="'+(state.diagram===x[0]?'active':'')+'" data-diagram="'+x[0]+'" aria-pressed="'+(state.diagram===x[0])+'">'+x[1]+'</button>').join('')+'</div><div class="model-grid"><section class="panel diagram-panel" aria-label="'+e(models.find(x=>x[0]===state.diagram)[1])+' diagram">'+(Diagram[state.diagram]||'<div class="empty-state">Diagram source is included in the report.</div>')+'</section><aside class="panel supporting-panel"><h3>Reviewed model principles</h3><div class="model-fact"><h4>Context preserves meaning</h4><p>One event can have multiple account contexts. Public recipients do not become reported affected accounts; organization summaries own no entity impacts.</p></div><div class="model-fact"><h4>Three kinds of state</h4><p>AWS event/entity state, local workflow progress and inferred lifecycle posture have separate owners and clocks.</p></div><div class="model-fact"><h4>Evidence before assessment</h4><p>Inventory matching and complete collection support claims. Unknown applicability remains unknown.</p></div><div class="model-fact"><h4>A transparent simulation</h4><p>All accounts, incidents, dates and resource identifiers are fictional. Event titles and priority are local display fields, not native AWS fields.</p></div><div class="model-links"><a class="button button-secondary" href="report.pdf" target="_blank" rel="noopener">'+icon('file')+' Reviewed report · PDF '+icon('external')+'</a><a class="button button-secondary" href="report.md" target="_blank" rel="noopener">'+icon('file')+' Canonical report · Markdown</a><a class="button button-secondary" href="diagrams/'+e(state.diagram)+'.svg" target="_blank" rel="noopener">'+icon('external')+' Open full-size diagram · SVG</a><a class="button button-secondary" href="diagrams/'+e(state.diagram)+'.mmd" target="_blank" rel="noopener">'+icon('nodes')+' Editable Mermaid source</a></div></aside></div>';
  }
  const narrowNavigation=window.matchMedia('(max-width:760px)');
  function syncNavigation() {const closed=narrowNavigation.matches&&!document.body.classList.contains('nav-open');$('.sidebar').inert=closed;if(closed)$('.sidebar').setAttribute('aria-hidden','true');else $('.sidebar').removeAttribute('aria-hidden');}
  narrowNavigation.addEventListener('change',syncNavigation);
  function render() {
    const count=Model.metrics(data,{});
    $('#primary-nav').innerHTML=nav.map(([id,label,name],i)=>(i===5?'<div class="nav-separator"></div>':'')+'<button class="nav-item '+(state.view===id?'active':'')+'" data-nav="'+id+'" aria-label="'+label+'" '+(state.view===id?'aria-current="page"':'')+' title="'+label+'">'+icon(name)+'<span class="nav-text">'+label+'</span>'+(id==='events'?'<span class="nav-count">'+count.events+'</span>':id==='actions'?'<span class="nav-count">'+workItems.filter(x=>x.state!=='verified').length+'</span>':id==='coverage'?'<span class="nav-dot"></span>':'')+'</button>').join('');
    const [eyebrow,title,description]=views[state.view];$('#page-eyebrow').textContent=eyebrow;$('#page-title').textContent=title;$('#page-description').textContent=description;
    $('#scenario-clock').textContent=fmtDate(data.meta.asOf)+' · '+fmtTime(data.meta.asOf);
    $('#scenario-banner p').textContent='Fictional accounts, incidents and dates · '+fmtDate(data.meta.asOf)+', '+fmtTime(data.meta.asOf)+' · No AWS connection.';
    $('#replay-update').innerHTML=icon(state.replayed?'check':'play')+(state.replayed?'AWS update replayed':'Replay AWS update');$('#replay-update').disabled=state.replayed;
    $('#export-snapshot').innerHTML=icon('download')+'Export snapshot';
    $('#global-filters').hidden=state.view==='model';
    $('#clear-filters').hidden=!Object.entries(filters).some(([k,v])=>k==='q'?v!=='':v!=='all');
    $('#account-filter').value=filters.account;$('#region-filter').value=filters.region;
    const view=$('#view');view.setAttribute('aria-label',title);view.innerHTML=({overview,events:eventsView,actions:actionsView,lifecycle:lifecycleView,coverage:coverageView,model:modelView}[state.view])();
    $('#footer-provenance').textContent=storageAvailable?'AWS state and operator progress are tracked separately.':'Local storage unavailable · export to preserve session changes.';
    syncNavigation();
    if(state.detail && $('#detail-dialog').open) renderDetail();
  }
  function navigate(view) { if(!views[view])return;if(view!=='events')Object.assign(filters,{category:'all',scope:'all',status:'all',actionability:'all'});state.view=view;closeDetail();document.body.classList.remove('nav-open');$('#nav-scrim').hidden=true;$('#nav-toggle').setAttribute('aria-expanded','false');if(location.hash!=='#'+view)history.pushState(null,'','#'+view);render();window.scrollTo({top:0,behavior:'instant'}); }
  function detailHeader(kicker,title,description,tags) { return '<div class="drawer-head"><button class="icon-button drawer-close" data-action="close-detail" aria-label="Close detail panel" autofocus>'+icon('close')+'</button><div class="drawer-kicker">'+kicker+'</div><h2 id="detail-title">'+e(title)+'</h2><p>'+e(description)+'</p><div class="drawer-tags">'+tags+'</div></div>'; }
  let lastFocus=null;
  function openDetail(type,id) {lastFocus=document.activeElement;state.detail={type,id};state.detailTab='summary';renderDetail();if(!$('#detail-dialog').open)$('#detail-dialog').showModal();$('#detail-dialog').scrollTop=0;}
  function closeDetail() {if($('#detail-dialog').open)$('#detail-dialog').close();state.detail=null;if(lastFocus && lastFocus.isConnected)lastFocus.focus({preventScroll:true});}
  function renderDetail() {
    if(!state.detail)return;
    $('#detail-content').innerHTML=state.detail.type==='event'?eventDetail(state.detail.id):state.detail.type==='work'?workDetail(state.detail.id):state.detail.type==='exposure'?exposureDetail(state.detail.id):tourDetail();
  }
  function eventDetail(id) {
    const r=currentEvent(id);if(!r)return '';
    const ownedContexts=r.contexts.filter(x=>x.kind!=='ORG_SUMMARY');
    const cov=coverageForEvent(id);const gaps=cov.filter(x=>x.status!=='complete');const eventWork=workForEvent(id);
    let head=detailHeader(serviceIcon(r.service)+'<span>'+e(serviceName(r.service))+' · '+e(categoryLabel(r.category))+' · '+e(r.region)+'</span>',r.title,r.summary,badge(r.status)+(r.actionability?badge(r.actionability):'<span class="badge gray outline">Actionability not supplied</span>')+(gaps.length?badge(coverageState(cov),'Coverage '+coverageState(cov)):''));
    head+='<div class="drawer-tabs" role="group" aria-label="Event detail sections">'+[['summary','Overview'],['entities','Entities · '+r.entityCount],['timeline','Timeline'],['evidence','Model data']].map(([key,label])=>'<button data-detail-tab="'+key+'" class="'+(state.detailTab===key?'active':'')+'" aria-pressed="'+(state.detailTab===key)+'">'+label+'</button>').join('')+'</div><div class="drawer-body">';
    const gapNote=gaps.length?'<div class="info-panel amber">'+icon('warning')+'<p><strong>Observed evidence is incomplete or stale.</strong> '+gaps.map(x=>e(x.reason)).join(' ')+' Counts describe the records currently observed.</p></div>':'';
    if(state.detailTab==='summary') {
      head+=gapNote+'<div class="detail-stat-grid"><div class="detail-stat"><strong>'+r.accounts.length+'</strong><span>Reported affected accounts</span></div><div class="detail-stat"><strong>'+r.entityCount+'</strong><span>Observed entity records</span></div><div class="detail-stat"><strong>'+r.pendingCount+'</strong><span>Provider pending actions</span></div></div>';
      if(r.scope==='PUBLIC') head+='<div class="info-panel">'+icon('globe')+'<p><strong>Public service advisory.</strong> Delivery to an account does not establish account impact. Assess relevance using your inventory and workload telemetry.</p></div>';
      head+='<h3>AWS state by context</h3>'+ownedContexts.map(c=>'<article class="context-card"><div class="context-card-head"><strong>'+e(c.kind==='PUBLIC'?'Public service context':accountName(c.accountId))+'</strong>'+badge(c.statusCode)+'</div><p>AWS updated '+e(fmtDate(c.lastUpdatedTime))+' at '+e(fmtTime(c.lastUpdatedTime))+' · '+e(c.actionability?c.actionability.replaceAll('_',' ').toLowerCase():'Actionability not supplied')+'</p><p>'+e(c.description)+'</p></article>').join('');
      head+='<h3>Team response</h3>'+(eventWork.length?eventWork.map(w=>'<div class="context-card"><div class="context-card-head"><button class="event-title" data-work="'+e(w.id)+'">'+e(w.title)+'</button>'+badge(w.state)+'</div><p>'+e(w.owner)+' · '+e(dueLabel(w.dueAt))+'</p></div>').join(''):'<p class="coverage-note">No work item is linked to this event in the demo.</p>');
      head+='<h3>Event identity</h3><div class="arn-line"><button class="icon-button" data-copy-arn="'+e(r.eventArn)+'" aria-label="Copy event ARN">'+icon('copy')+'</button>'+e(r.eventArn)+'</div><dl class="key-value-list"><dt>Event type</dt><dd>'+e(r.typeCode)+'</dd><dt>Provider scope</dt><dd>'+e(r.scope)+'</dd><dt>Start / change date</dt><dd>'+e(fmtDate(ownedContexts[0]&&ownedContexts[0].startTime))+'</dd><dt>Latest source update</dt><dd>'+e(fmtDate(r.updatedAt))+' · '+e(fmtTime(r.updatedAt))+'</dd></dl>';
    } else if(state.detailTab==='entities') {
      head+=gapNote+'<div class="info-panel">'+icon('info')+'<p>Entity states are relative to this event. A Health entity can be an individual resource, a group, or a marker for broader impact.</p></div>';
      head+=r.entities.length?r.entities.map(entity=>{const resource=byId(data.resources,entity.resourceId),context=byId(data.contexts,entity.contextId);return '<article class="drawer-entity"><div class="drawer-entity-head"><div><strong>'+e(resource?resource.name:entity.kind==='group'?'Broader impact marker':entity.entityValue)+'</strong><span class="entity-id">'+e(entity.entityValue)+'</span></div>'+badge(entity.statusCode)+'</div><div class="entity-meta"><span>'+e(accountName(context.accountId))+'</span><span>AWS updated '+e(age(entity.updatedAt))+'</span></div><span class="subline">'+(resource?'Inventory match: '+e(resource.workload)+' · '+e(resource.owner):'No individual inventory resource is asserted')+'</span></article>';}).join(''):'<div class="empty-state">'+icon('globe')+'<strong>No affected entities reported</strong><span>Public visibility does not establish resource impact.</span></div>';
    } else if(state.detailTab==='timeline') {
      const contextIds=new Set(ownedContexts.map(c=>c.id));
      const updates=data.updates.filter(x=>x.eventId===id && (!x.contextId || contextIds.has(x.contextId))).map(x=>({...x}));
      eventWork.forEach(w=>(w.actions||[]).filter(a=>String(a.id).startsWith('local-')).forEach(a=>updates.push({id:a.id,kind:'operator',at:a.at,title:a.title||a.actionType||(a.toState?'Workflow: '+workflowLabel(a.toState):a.type)||'Workflow updated',body:a.body||a.text||a.detail||'Local work item '+w.id+' changed.'})));
      head+='<div class="info-panel">'+icon('clock')+'<p>AWS source time, collection time and operator action time remain separate. The clock is fixed to the demo scenario.</p></div>'+timelineMarkup(updates);
    } else {
      const sourceEvent=byId(data.events,id);const contexts=[...r.contexts,...(r.summaryContexts||[])];const ids=new Set(contexts.map(c=>c.id));const communicationIds=new Set((data.communications||[]).filter(c=>c.eventId===id && (!c.contextId || ids.has(c.contextId))).map(c=>c.id));
      head+='<p class="coverage-note">These records are fictional and normalized for the reviewed model. Title and priority are local presentation fields. ORG_SUMMARY is a local context kind.</p><pre class="json-view">'+e(JSON.stringify({healthEvent:sourceEvent,eventContexts:contexts,entityImpacts:data.entities.filter(x=>ids.has(x.contextId)),communications:(data.communications||[]).filter(x=>communicationIds.has(x.id)),pages:(data.communicationPages||[]).filter(x=>communicationIds.has(x.communicationRecordId))},null,2))+'</pre>';
    }
    return head+'</div>';
  }
  function timelineMarkup(updates) {return '<div class="timeline">'+updates.sort((a,b)=>Date.parse(b.at)-Date.parse(a.at)).map(u=>'<article class="timeline-item"><span class="timeline-marker '+e(u.kind)+'"></span><div class="timeline-meta"><strong>'+e(u.kind==='aws'?'AWS evidence':u.kind==='operator'?'Operator action':'Collection')+'</strong><time>'+e(fmtDate(u.at))+' · '+e(fmtTime(u.at))+'</time></div><h4>'+e(u.title)+'</h4><p>'+e(u.body)+'</p></article>').join('')+'</div>';}
  function workDetail(id) {
    const w=Model.workRows(data,workItems,{}).find(x=>x.id===id);if(!w)return '';
    const teams=[...new Set(['SRE','Platform','Payments','Data','Security','Developer Experience',w.owner])];
    let html=detailHeader(icon('tasks')+'<span>OPERATOR WORK · '+e(w.id.toUpperCase())+'</span>',w.title,'Assignments, progress and notes are saved in this browser. Provider evidence remains independent.',badge(w.state)+'<span class="badge gray">'+e(w.owner)+'</span>');
    html+='<div class="drawer-body"><div class="info-panel '+(w.pendingProviderCount?'amber':'')+'">'+icon('info')+'<p><strong>'+e(w.pendingProviderCount?pendingLabel(w.pendingProviderCount)+' still reported by AWS.':'Provider evidence remains separate.')+'</strong> Completing this task records operator progress; it does not change AWS state or an inventory-based lifecycle assessment.</p></div><div class="work-control"><h4>Manage the response</h4><span class="subline">Local workflow · Due '+e(fmtDate(w.dueAt))+'</span><div class="form-row"><label class="form-field">Assigned team<select id="work-owner" data-owner-for="'+e(w.id)+'">'+teams.map(t=>'<option '+(t===w.owner?'selected ':'')+'value="'+e(t)+'">'+e(t)+'</option>').join('')+'</select></label><label class="form-field">Workflow state<select id="work-state" data-state-for="'+e(w.id)+'">'+validStates.map(s=>'<option '+(s===w.state?'selected ':'')+'value="'+s+'">'+e(workflowLabel(s))+'</option>').join('')+'</select></label></div><div class="form-row">'+(w.state==='new'?'<button class="button button-secondary" data-work-action="acknowledged" data-work-id="'+e(w.id)+'">Acknowledge</button>':'')+(w.state!=='completed'&&w.state!=='verified'?'<button class="button button-primary" data-work-action="completed" data-work-id="'+e(w.id)+'">'+icon('check')+'Mark work complete</button>':'<span class="coverage-note">'+(w.state==='completed'?'Completed locally. Verify source or inventory evidence before marking verified.':'Operator verification is recorded separately from provider status.')+'</span>')+'</div></div>';
    html+='<h3>Linked AWS evidence</h3>'+((w.eventIds||[]).map(eventId=>{const r=currentEvent(eventId);return r?'<div class="context-card"><div class="context-card-head"><button class="event-title" data-event="'+e(r.id)+'">'+e(r.title)+'</button>'+badge(r.status)+'</div><p>'+e(r.region)+' · '+r.entityCount+' observed entity records · '+pendingLabel(r.pendingCount)+'</p></div>':'';}).join('')||'<p class="coverage-note">This work is linked to lifecycle or inventory evidence.</p>');
    html+='<form class="note-form" data-note-for="'+e(w.id)+'"><label class="form-field">Add a response note<textarea name="note" id="work-note" maxlength="2000" required placeholder="Record what you checked, changed, or still need to verify…"></textarea></label><button class="button button-secondary" type="submit">Add note</button></form>';
    if((w.notes||[]).length) html+='<h3>Notes</h3>'+w.notes.slice().reverse().map(n=>'<article class="note-entry"><span>'+e(n.actor||'Demo operator')+' · '+e(fmtDate(n.at))+' · '+e(fmtTime(n.at))+'</span><p>'+e(n.text)+'</p></article>').join('');
    if((w.actions||[]).length) html+='<h3>Operator history</h3>'+timelineMarkup(w.actions.map(a=>({kind:'operator',at:a.at,title:a.title||a.actionType||(a.toState?'Workflow: '+workflowLabel(a.toState):a.type)||'Workflow changed',body:a.body||a.text||a.detail||'Local task updated.'})));
    return html+'</div>';
  }
  function exposureDetail(id) {
    const x=Model.lifecycleRows(data,{}).find(x=>x.id===id);if(!x)return '';
    const deployment=x.deployment||byId(data.deployments,x.deploymentId),resource=x.resource||byId(data.resources,deployment.resourceId),milestone=x.milestone||byId(data.milestones,x.milestoneId),entry=x.entry||byId(data.catalogEntries,milestone.entryId);
    const linkedIds=new Set(data.entities.filter(i=>i.resourceId===resource.id).map(i=>(byId(data.contexts,i.contextId)||{}).eventId));
    return detailHeader(serviceIcon(entry.service)+'<span>LIFECYCLE EXPOSURE · '+e(resource.region)+'</span>',resource.name,entry.title+' · '+deployment.version,'<span class="badge blue">'+e(x.applicability)+' inventory match</span>')+'<div class="drawer-body"><div class="info-panel amber">'+icon('calendar')+'<p><strong>Fictional lifecycle date: '+e(fmtDate(milestone.date))+'.</strong> This is a catalog-to-inventory assessment, not a report of current impairment.</p></div><h3>Milestone</h3><div class="description-box"><strong>'+e(milestone.type.replaceAll('_',' ').toLowerCase())+'</strong><br>'+e(milestone.description)+'</div><dl class="key-value-list"><dt>Account</dt><dd>'+e(accountName(resource.accountId))+'</dd><dt>Owner / workload</dt><dd>'+e(resource.owner)+' · '+e(resource.workload)+'</dd><dt>Observed component</dt><dd>'+e(deployment.component)+' · '+e(deployment.version)+'</dd><dt>Inventory observed</dt><dd>'+e(fmtDate(deployment.observedAt))+' · '+e(fmtTime(deployment.observedAt))+'</dd><dt>Recommended version</dt><dd>'+e(entry.recommendedVersion||'Not supplied')+'</dd><dt>Applicable regions</dt><dd>'+e(milestone.regions.join(', '))+'</dd><dt>Risk tags</dt><dd>'+e(milestone.risks.join(', '))+'</dd><dt>Match evidence</dt><dd>'+e(x.reason)+'</dd></dl><h3>Related resource evidence</h3>'+[...linkedIds].filter(Boolean).map(eventId=>{const r=currentEvent(eventId);return '<div class="context-card"><div class="context-card-head"><button class="event-title" data-event="'+e(eventId)+'">'+e(r.title)+'</button>'+badge(r.status)+'</div><p>Joined through the same inventory resource. This relationship is locally derived.</p></div>';}).join('')+'<div class="info-panel wide-note">'+icon('info')+'<p>Completing work or replaying an AWS entity update leaves this earlier inventory observation intact. A new inventory observation is needed to establish a changed deployment.</p></div></div>';
  }
  function tourDetail() {
    return detailHeader(icon('play')+'<span>EXPLORE THE SCENARIO</span>','Evidence, response, and what comes next','A realistic fictional scenario designed to make the reviewed model tangible.','<span class="badge blue">Fixed clock · '+e(fmtTime(data.meta.asOf))+'</span>')+'<div class="drawer-body"><div class="context-card"><h3>1. Inspect an active incident</h3><p>Open the Frankfurt EC2 event. Compare reported account contexts, resource impacts and the unresolved broader-impact marker.</p><button class="text-button" data-event="evt-ec2-network">Inspect the incident →</button></div><div class="context-card"><h3>2. See a public advisory</h3><p>The S3 notification has delivery recipients, but zero AWS-reported affected accounts.</p><button class="text-button" data-event="evt-s3-public">Inspect public exposure →</button></div><div class="context-card"><h3>3. Replay an AWS confirmation</h3><p>The payment-webhook upgrade is completed locally while its AWS entity remains pending. Replay the update to resolve the provider entity; the work item and older inventory scan remain separate.</p><button class="text-button" data-action="replay">Replay provider update →</button></div><div class="context-card"><h3>4. Investigate a coverage gap</h3><p>The Oregon scenario has only two of three resource pages and a stale reconciliation. Known impacts stay visible while completeness remains uncertain.</p><button class="text-button" data-nav="coverage">Inspect collection coverage →</button></div><div class="context-card"><h3>5. Follow the model</h3><p>Explore the four diagrams and the reviewed report. All identifiers and dates are synthetic; no controls call AWS.</p><button class="text-button" data-nav="model">Open model & report →</button></div></div>';
  }
  function localTime() {state.actionCounter++;const times=[data.meta.asOf,...workItems.flatMap(w=>[w.updatedAt,...(w.actions||[]).map(x=>x.at),...(w.notes||[]).map(x=>x.at)])].map(Date.parse).filter(Number.isFinite);return new Date(Math.max(...times)+1000).toISOString();}
  function updateWork(id,change) {
    const w=byId(workItems,id);if(!w)return;
    const before=w.state,oldOwner=w.owner;
    if(change.state && validStates.includes(change.state))w.state=change.state;
    if(typeof change.owner==='string')w.owner=change.owner;
    if(before===w.state && oldOwner===w.owner)return;
    const at=localTime();w.updatedAt=at;w.actions=w.actions||[];
    w.actions.push({id:'local-'+Date.now()+'-'+state.actionCounter,at,actor:'Demo operator',actionType:change.owner?'assignment':'workflow',title:change.owner?'Assigned to '+w.owner:'Workflow: '+workflowLabel(w.state),body:change.owner?'Assignment changed from '+oldOwner+' to '+w.owner+'.':'Changed from '+workflowLabel(before)+' to '+workflowLabel(w.state)+'. AWS event and entity states were preserved.'});
    persist();render();toast(w.state==='completed'?'Work completed locally. AWS state and inventory exposure are unchanged.':change.owner?'Assignment saved in this browser.':'Workflow updated. AWS state is unchanged.');
  }
  function runReplay() {if(state.replayed){toast('This AWS update has already been replayed. Reset the demo to replay it again.');return;}state.replayed=true;replayProvider();persist();render();toast('AWS now reports payment-webhook resolved. Local workflow and the earlier inventory scan are unchanged.');}
  function clearFilters() {clearTimeout(searchTimer);Object.assign(filters,{q:'',account:'all',region:'all',category:'all',scope:'all',status:'all',actionability:'all'});$('#search').value='';render();}
  function downloadSnapshot() {const evidence=clone(data);delete evidence.workItems;const blob=new Blob([JSON.stringify({schema:'pulse-health-demo/v1',exportedAt:new Date().toISOString(),scenarioAsOf:data.meta.asOf,fictional:true,filters:clone(filters),scenarioEvidence:evidence,operatorWorkItems:workItems},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download='aws-health-demo-snapshot.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Snapshot exported with fictional provider data and local workflow.');}
  $('#account-filter').innerHTML='<option value="all">All accounts</option>'+data.accounts.map(a=>'<option value="'+e(a.id)+'">'+e(a.name)+'</option>').join('');
  $('#region-filter').innerHTML='<option value="all">All regions</option>'+Object.entries(data.meta.regionLabels).map(([id,label])=>'<option value="'+e(id)+'">'+e(label)+'</option>').join('');
  $('#nav-toggle').innerHTML=icon('menu');$('#search-icon').innerHTML=icon('search');$('#confirm-icon').innerHTML=icon('refresh');$('#reset-demo').innerHTML=icon('refresh')+'Reset demo scenario';
  document.addEventListener('click',async event=>{
    const target=event.target.closest('button,a');if(!target)return;
    if(target.dataset.nav){event.preventDefault();navigate(target.dataset.nav);return;}
    if(target.dataset.event){openDetail('event',target.dataset.event);return;}
    if(target.dataset.work){openDetail('work',target.dataset.work);return;}
    if(target.dataset.exposure){openDetail('exposure',target.dataset.exposure);return;}
    if(target.dataset.detailTab){state.detailTab=target.dataset.detailTab;renderDetail();return;}
    if(target.dataset.workAction){updateWork(target.dataset.workId,{state:target.dataset.workAction});return;}
    if(target.dataset.category){filters.category=target.dataset.category;render();return;}
    if(target.dataset.scope){filters.scope=filters.scope===target.dataset.scope?'all':target.dataset.scope;render();return;}
    if(target.dataset.actionability){filters.actionability=filters.actionability===target.dataset.actionability?'all':target.dataset.actionability;render();return;}
    if(target.dataset.matrixService){Object.assign(filters,{q:target.dataset.matrixService,region:target.dataset.matrixRegion,category:'all',scope:'all',status:'all',actionability:'all'});$('#search').value=filters.q;navigate('events');return;}
    if(target.dataset.diagram){state.diagram=target.dataset.diagram;render();return;}
    if(target.dataset.copyArn){try{await navigator.clipboard.writeText(target.dataset.copyArn);toast('Event ARN copied.');}catch(_){toast('Clipboard access is unavailable. Select the displayed ARN to copy it.',true);}return;}
    if(target.dataset.action==='close-detail'){closeDetail();return;}
    if(target.dataset.action==='clear'){clearFilters();return;}
    if(target.dataset.action==='replay'){runReplay();return;}
    if(target.dataset.action==='refresh'){state.collectionAt=new Date(Date.parse(data.meta.asOf)+60000).toISOString();data.meta.asOf=state.collectionAt;data.coverage.forEach(c=>{if(c.status==='complete')c.lastSuccessAt=state.collectionAt;});persist();render();toast('Demo refresh collected the same snapshots. Provider timestamps and known collection gaps are preserved.');return;}
  });
  document.addEventListener('change',event=>{
    const target=event.target;
    if(target.id==='account-filter'){filters.account=target.value;render();}
    if(target.id==='region-filter'){filters.region=target.value;render();}
    if(target.id==='horizon'){state.horizon=Number(target.value);render();}
    if(target.id==='event-status'){filters.status=target.value;render();}
    if(target.dataset.ownerFor)updateWork(target.dataset.ownerFor,{owner:target.value});
    if(target.dataset.stateFor)updateWork(target.dataset.stateFor,{state:target.value});
  });
  document.addEventListener('submit',event=>{
    const form=event.target;if(!form.dataset.noteFor)return;event.preventDefault();
    const text=new FormData(form).get('note').trim();if(!text)return;
    const w=byId(workItems,form.dataset.noteFor),at=localTime();w.notes=w.notes||[];w.notes.push({id:'note-'+Date.now(),actor:'Demo operator',at,text:text.slice(0,2000)});w.updatedAt=at;persist();renderDetail();toast('Response note saved locally.');
  });
  let searchTimer;$('#search').addEventListener('input',event=>{clearTimeout(searchTimer);const value=event.target.value;searchTimer=setTimeout(()=>{filters.q=value;render();},120);});
  $('#clear-filters').addEventListener('click',clearFilters);$('#export-snapshot').addEventListener('click',downloadSnapshot);$('#replay-update').addEventListener('click',runReplay);$('#scenario-explainer').addEventListener('click',()=>openDetail('tour','tour'));
  $('#reset-demo').addEventListener('click',()=>$('#confirm-dialog').showModal());$('#cancel-reset').addEventListener('click',()=>$('#confirm-dialog').close());
  $('#confirm-reset').addEventListener('click',()=>{try{localStorage.removeItem(STORAGE_KEY);}catch(_){}workItems=clone(Seed.workItems);data=clone(Seed);state.replayed=false;state.collectionAt=null;state.actionCounter=0;$('#confirm-dialog').close();closeDetail();clearFilters();toast('Original fictional scenario restored.');});
  $('#nav-toggle').addEventListener('click',()=>{const open=document.body.classList.toggle('nav-open');$('#nav-scrim').hidden=!open;$('#nav-toggle').setAttribute('aria-expanded',String(open));syncNavigation();if(open)$('.nav-item.active').focus();});
  $('#nav-scrim').addEventListener('click',()=>{document.body.classList.remove('nav-open');$('#nav-scrim').hidden=true;$('#nav-toggle').setAttribute('aria-expanded','false');syncNavigation();$('#nav-toggle').focus();});
  $('#detail-dialog').addEventListener('close',()=>{state.detail=null;});
  $('#detail-dialog').addEventListener('click',event=>{if(event.target===$('#detail-dialog')){const rect=event.target.getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)closeDetail();}});
  document.addEventListener('keydown',event=>{if(event.key==='Escape'&&document.body.classList.contains('nav-open')){document.body.classList.remove('nav-open');$('#nav-scrim').hidden=true;$('#nav-toggle').setAttribute('aria-expanded','false');syncNavigation();$('#nav-toggle').focus();}if(event.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)&&!$('#detail-dialog').open){event.preventDefault();if(state.view==='model')navigate('events');$('#search').focus();}});
  window.addEventListener('popstate',()=>{const next=location.hash.slice(1);if(views[next]){state.view=next;closeDetail();render();}});
  window.addEventListener('hashchange',()=>{const next=location.hash.slice(1);if(views[next]&&state.view!==next){state.view=next;closeDetail();render();}});
  render();
  if(!storageAvailable)toast('Local storage is unavailable. Export a snapshot to keep demo changes.',true);
})();
