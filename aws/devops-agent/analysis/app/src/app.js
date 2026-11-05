(function () {
  'use strict';
  const Model = globalThis.DemoModel;
  const Data = globalThis.DemoData;
  const diagrams = globalThis.LensDiagrams || [];
  const $ = (selector, root = document) => root.querySelector(selector);
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const paths = {
    lens: '<circle cx="12" cy="12" r="8.3"/><circle cx="12" cy="12" r="3.4"/><path d="M12 1v4m0 14v4M1 12h4m14 0h4"/>',
    search: '<circle cx="10.5" cy="10.5" r="6.2"/><path d="m15 15 4.8 4.8"/>',
    chevron: '<path d="m9 5 7 7-7 7"/>', down: '<path d="m6 9 6 6 6-6"/>',
    arrow: '<path d="M5 12h14m-5-5 5 5-5 5"/>', external: '<path d="M14 4h6v6m0-6-10 10"/><path d="M11 4H5a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-6"/>',
    activity: '<path d="M2 12h5l3-8 4 16 3-8h5"/>',
    clock: '<circle cx="12" cy="12" r="8.8"/><path d="M12 7v5l3.4 2"/>',
    layers: '<path d="m12 3 10 5-10 5L2 8l10-5Zm-9 9 9 5 9-5M3 16l9 5 9-5"/>',
    play: '<path d="m8 5 11 7-11 7V5Z"/>', pause: '<path d="M8 5v14M16 5v14"/>',
    next: '<path d="m5 5 10 7-10 7V5Zm13 0v14"/>', reset: '<path d="M3 11a9 9 0 1 1 2.6 7M3 4v7h7"/>',
    check: '<path d="m5 12 4.5 4.5L19 7"/>', cross: '<path d="m6 6 12 12M6 18 18 6"/>',
    alert: '<path d="m12 3 10 18H2L12 3Z"/><path d="M12 9v5m0 3v.1"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6m0-10v.1"/>',
    file: '<path d="M14 3H5v18h14V8l-5-5Zm0 0v5h5M8 12h8M8 16h6"/>',
    folder: '<path d="M3 6h7l2 3h9v11H3V6Z"/>',
    graph: '<rect x="2.5" y="3" width="6" height="5" rx="1"/><rect x="15.5" y="3" width="6" height="5" rx="1"/><rect x="9" y="16" width="6" height="5" rx="1"/><path d="M5.5 8v4h13V8M12 12v4"/>',
    branch: '<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M6 7v10m12-10v3c0 3-12 1-12 5"/>',
    bot: '<rect x="4" y="7" width="16" height="13" rx="3"/><path d="M12 3v4M9 12v2m6-2v2M9 17h6M2 11v5m20-5v5"/>',
    spark: '<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z"/>',
    database: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 4 16 4 16 0V5M4 12c0 4 16 4 16 0"/>',
    globe: '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    cloud: '<path d="M6 18a5 5 0 0 1-1-9.9 7 7 0 0 1 13.3-1.3A5.6 5.6 0 0 1 18 18H6Z"/>',
    shield: '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6l8-3Z"/><path d="m8 12 3 3 5-6"/>',
    snapshot: '<path d="M3 7h5l2-3h4l2 3h5v13H3V7Z"/><circle cx="12" cy="13" r="3.5"/>',
    download: '<path d="M12 3v12m-4-4 4 4 4-4M4 16v5h16v-5"/>',
    code: '<path d="m7 6-6 6 6 6m10-12 6 6-6 6M14 3l-4 18"/>',
    book: '<path d="M12 5c-3-3-9-2-9-2v17s6-1 9 2c3-3 9-2 9-2V3s-6-1-9 2v17"/>',
    list: '<path d="M8 5h13M8 12h13M8 19h13M3 5h.1M3 12h.1M3 19h.1"/>',
    menu: '<path d="M3 6h18M3 12h18M3 18h18"/>',
    lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V6a4 4 0 0 1 8 0v4m-4 5v2"/>',
    message: '<path d="M3 3h18v14H8l-5 4V3Z"/><path d="M7 8h10M7 12h7"/>',
    link: '<path d="m9 15 6-6m-8 4-2 2a3.5 3.5 0 0 0 5 5l4-4a3.5 3.5 0 0 0 0-5m3 0 2-2a3.5 3.5 0 0 0-5-5l-4 4a3.5 3.5 0 0 0 0 5"/>',
    zoom: '<circle cx="10" cy="10" r="6.5"/><path d="m15 15 6 6M10 7v6M7 10h6"/>',
    fit: '<path d="M8 3H3v5m13-5h5v5M3 16v5h5m13-5v5h-5M8 8h8v8H8V8Z"/>',
    minus: '<path d="M5 12h14"/>', filter: '<path d="M3 5h18l-7 8v7l-4-2v-5L3 5Z"/>',
    eye: '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    compare: '<path d="M8 3v18M16 3v18M3 8l5-5 5 5m-2 8 5 5 5-5"/>',
    hash: '<path d="M10 3 7 21M17 3l-3 18M3 9h18M2 15h18"/>'
  };
  const icon = (name, extra = '') => `<svg class="icon ${extra}" viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.file}</svg>`;
  const badge = (text, tone = '', dot = false) => `<span class="badge ${tone}">${dot ? '<i class="badge-dot"></i>' : ''}${esc(text)}</span>`;
  const statusLabel = status => ({IN_PROGRESS:'In progress',COMPLETED:'Completed',TIMED_OUT:'Timed out',FAILED:'Failed',WAITING:'Waiting',PENDING_CUSTOMER_APPROVAL:'Awaiting approval',PENDING_START:'Pending start',PENDING_TRIAGE:'Pending triage',CANCELED:'Canceled',LINKED:'Linked',SKIPPED:'Skipped',RUNNING:'Running',STOPPED:'Stopped'})[status] || status || 'Not supplied';
  const toneFor = status => ['COMPLETED'].includes(status) ? 'complete' : ['RUNNING','IN_PROGRESS'].includes(status) ? 'active' : ['FAILED','TIMED_OUT','CANCELED'].includes(status) ? 'failed' : ['WAITING','PENDING_CUSTOMER_APPROVAL','PENDING_START','PENDING_TRIAGE'].includes(status) ? 'waiting' : '';
  const originLabel = origin => ({native:'Native observation',native_field:'Native field',agent_reported:'Agent reported',agent:'Agent reported',operator_confirmed:'Operator confirmed',application_inference:'Application inference',application_derived:'Application derived',deterministic_parse:'Derived from source',demo_profile:'Demo payload profile',documented_profile:'Documented profile',operator:'Operator annotation'})[origin] || String(origin || 'Derived from source').replaceAll('_',' ');
  const categoryLabel = category => ({agent:'Agent activity',lifecycle:'Lifecycle',evidence:'Incident evidence',conversation:'Conversation',collection:'Collection'})[category] || category;
  const asDate = value => new Date(typeof value === 'number' && value < 1e12 ? value * 1000 : value);
  const validDate = value => value != null && Number.isFinite(asDate(value).getTime());
  const time = (value, seconds = false) => validDate(value) ? new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Zurich',hour:'2-digit',minute:'2-digit',...(seconds ? {second:'2-digit'} : {})}).format(asDate(value)) : 'Not supplied';
  const date = value => validDate(value) ? new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Zurich',day:'numeric',month:'short',year:'numeric'}).format(asDate(value)) : 'Not supplied';
  const stamp = value => validDate(value) ? `${date(value)} · ${time(value,true)} CET` : 'Not supplied';
  const shorten = (value, max = 85) => String(value ?? '').length > max ? String(value).slice(0,max - 1) + '…' : String(value ?? '');
  const pretty = value => JSON.stringify(value, null, 2);
  const STORAGE_KEY = 'lens-devops-demo-v1';
  let state = Model.createState();
  let storageAvailable = true;
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || 'null');
    if (saved && saved.version === 1 && saved.state && saved.state.schemaVersion === state.schemaVersion) {
      const candidate = saved.state;
      if (Number.isInteger(candidate.step) && candidate.step >= 0 && candidate.step < 6 && Array.isArray(candidate.snapshots)) {
        Model.view(candidate);
        state = candidate;
      }
    }
  } catch (_) { storageAvailable = false; }
  const ui = {taskId:Data.scenario.primaryTaskId,tab:'overview',snapshotId:null,queueSearch:'',timelineFilter:'all',timelineSearch:'',recordType:'all',artifactFilter:'all',diagramId:diagrams.some(d=>d.id==='D02')?'D02':diagrams[0]?.id,diagramZoom:1,diagramSource:false,playing:false,timer:null,mobileQueue:false,inspectorView:null,inspectorPayload:null};
  const tabs = [{id:'overview',label:'Overview',icon:'layers'},{id:'timeline',label:'Timeline',icon:'activity',count:'timeline'},{id:'evidence',label:'Evidence',icon:'graph',count:'findings'},{id:'executions',label:'Executions',icon:'branch',count:'executions'},{id:'artifacts',label:'Artifacts',icon:'folder',count:'artifacts'},{id:'history',label:'History',icon:'clock'},{id:'model',label:'Model & report',icon:'book'}];
  let toastTimer;
  function currentView() { return Model.view(state, ui.taskId, ui.snapshotId || undefined); }
  function liveView() { return Model.view(state, ui.taskId); }
  function persist() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify({version:1,state})); storageAvailable = true; }
    catch (_) { storageAvailable = false; }
  }
  function toast(message) {
    const el = $('#toast'); el.innerHTML = icon('check') + `<span>${esc(message)}</span>`; el.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(()=>{el.hidden = true;},4200);
  }
  function announce(message) { $('#live-announcement').textContent = message; }
  function markdown(value) {
    const inline = text => esc(text).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
    let list = false, output = '';
    for (const line of String(value ?? '').split(/\r?\n/)) {
      const bullet = /^\s*[-*]\s+(.+)$/.exec(line);
      if (bullet) { if(!list){output+='<ul>';list=true;} output+=`<li>${inline(bullet[1])}</li>`; continue; }
      if (list) { output+='</ul>'; list=false; }
      if (/^#{1,6}\s/.test(line)) output+=`<h3>${inline(line.replace(/^#{1,6}\s+/,''))}</h3>`;
      else if(line.trim()) output+=`<p>${inline(line)}</p>`;
    }
    return output + (list?'</ul>':'');
  }
  function safeFilename(name) { return String(name || 'investigation').replace(/[^a-zA-Z0-9_.-]/g,'-'); }
  function download(value, filename, mediaType = 'application/json') {
    const body = typeof value === 'string' ? value : pretty(value);
    const url = URL.createObjectURL(new Blob([body], {type:mediaType}));
    const a = document.createElement('a'); a.href = url; a.download = safeFilename(filename); a.hidden = true;
    document.body.append(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),30000);
  }
  function info(message, tone='neutral') { return `<div class="callout ${tone}">${icon(tone==='neutral'?'info':'alert')}<div>${message}</div></div>`; }
  function empty(title, message, glyph='file') { return `<div class="empty-state"><div class="empty-icon">${icon(glyph,'lg')}</div><h3>${esc(title)}</h3><p>${esc(message)}</p></div>`; }
  function sourceButton(ref, label='View source', extra='') { return ref ? `<button class="link-btn ${extra}" data-action="source" data-id="${esc(ref)}">${icon('link','sm')}${esc(label)}</button>` : ''; }
  function panelHead(title, right='', description='') { return `<div class="panel-head"><div><h2>${esc(title)}</h2>${description?`<p class="panel-kicker">${esc(description)}</p>`:''}</div>${right}</div>`; }
  function renderQueue() {
    const rows = Model.portfolio(state);
    const term = ui.queueSearch.toLowerCase();
    const filtered = rows.filter(row=>[row.title,row.code,row.service,row.owner,row.region,row.status].join(' ').toLowerCase().includes(term));
    $('#queue').classList.toggle('open',ui.mobileQueue);
    $('#queue').innerHTML = `<button class="icon-btn mobile-queue-close" data-action="close-queue" aria-label="Close investigation list">${icon('cross')}</button>
      <div class="brand"><div class="brand-symbol">${icon('lens','lg')}</div><div><div class="brand-wordmark">lens</div><div class="brand-subtitle">INVESTIGATION WORKSPACE</div></div></div>
      <div class="workspace-selector"><div class="flex"><span class="workspace-icon">${icon('layers','sm')}</span><span>Northstar Commerce<br><span class="tiny" style="color:#89a9b9">Operations · demo workspace</span></span></div>${icon('lock','sm')}</div>
      <label class="queue-search">${icon('search')}<input id="queue-search" value="${esc(ui.queueSearch)}" placeholder="Find an investigation" aria-label="Find an investigation" autocomplete="off"></label>
      <div class="queue-heading"><span>Investigations</span><span class="queue-count">${rows.length}</span></div>
      <nav class="investigation-list" aria-label="Select investigation">${filtered.length?filtered.map(row=>`<button class="investigation-btn ${row.taskId===ui.taskId?'selected':''}" data-action="select-task" data-id="${esc(row.taskId)}" ${row.taskId===ui.taskId?'aria-current="true"':''}><span class="queue-item-top"><span>${esc(row.code)}</span><span>${time(row.updatedAt)}</span></span><span class="queue-item-title">${esc(row.title)}</span><span class="queue-item-foot"><span><i class="queue-dot ${toneFor(row.status)}"></i>${esc(statusLabel(row.status))}</span><span class="queue-item-service">${row.taskId===Data.scenario.primaryTaskId?icon('activity','sm'):icon('file','sm')}</span></span></button>`).join(''):'<p class="queue-empty">No matching investigations.</p>'}</nav>
      <div class="queue-footer"><div class="queue-divider"></div><button class="queue-guide" data-action="tab" data-tab="model">${icon('book','sm')}<span>Reviewed model & diagrams</span></button><div class="queue-user"><div class="avatar">NS</div><div><div class="queue-user-name">Northstar SRE</div><div class="queue-user-role">Fictional operator workspace</div></div></div></div>`;
    $('#drawer-overlay').hidden = !ui.mobileQueue;
  }
  function renderTopbar(view) {
    $('#topbar').innerHTML = `<div class="topbar-left flex"><button class="mobile-menu" data-action="open-queue" aria-label="Open investigation list" aria-expanded="${ui.mobileQueue}">${icon('menu')}</button><div class="breadcrumb"><span>Operations</span>${icon('chevron','sm breadcrumb-root-chevron')}<span>Investigations</span>${icon('chevron','sm')}<span>${esc(view.meta.code)}</span></div></div><div class="topbar-right"><span class="scope-pill">${icon('globe','sm')}${esc(view.scope.region)}</span><span class="top-separator"></span><span class="clock-label">${time(view.now)} CET</span><span class="demo-badge" title="Fictional data. No AWS account connection."><i class="demo-dot"></i>Mock data</span></div>`;
  }
  function renderReplay(view, live) {
    if(ui.taskId!==Data.scenario.primaryTaskId) return `<div class="replay"><div class="flex muted small">${icon('file','sm')}<span>Historical demonstration case · ${esc(live.phase.title)}</span></div><button class="link-btn" data-action="select-task" data-id="${esc(Data.scenario.primaryTaskId)}">Open live replay ${icon('arrow','sm')}</button></div>`;
    const names = ['Investigate','Correlate','Completed','Result','Resume','Follow-up'];
    const replay = live.replay;
    return `<div class="replay" aria-label="Illustrative scenario replay"><div class="replay-title">${icon('activity','sm')}<span>Scenario replay</span></div><div class="replay-steps" aria-label="Scenario stage ${replay.step+1} of ${replay.totalSteps}">${names.map((name,i)=>`<span class="replay-step ${i<replay.step?'reached':''} ${i===replay.step?'current':''}" title="${esc(replay.stageLabels[i] || name)}"><span class="step-dot">${i<replay.step?'✓':i+1}</span><span class="step-name">${esc(name)}</span></span>`).join('')}</div><div class="replay-controls"><button class="btn small ${ui.playing?'':'primary'}" data-action="play" ${!replay.canAdvance&&!ui.playing?'disabled':''} aria-label="${ui.playing?'Pause':'Play'} scenario replay">${icon(ui.playing?'pause':'play','sm')}<span class="replay-play-label">${ui.playing?'Pause':'Play'}</span></button><button class="btn small" data-action="advance" ${!replay.canAdvance?'disabled':''} aria-label="Advance to next scenario stage" title="${esc(replay.nextLabel || 'Replay complete')}">${icon('next','sm')}Next</button><button class="icon-btn" data-action="reset" aria-label="Reset demo scenario" title="Reset demo scenario">${icon('reset','sm')}</button></div></div><p class="replay-caption">${ui.playing?'Playing':'Paused'} · ${esc(live.phase.description)}${view.isSnapshot?' · Live replay advances independently of this snapshot.':''}</p>`;
  }
  function renderStats(view) {
    const status = view.task.status;
    const resultLabels={none:'Collecting evidence',candidate:'Candidate available',pending:'Summary pending',available:'Result available'};
    const resultSub={none:'No referenced summary yet',candidate:'Awaiting authoritative selection',pending:'Exact result reference received',available:'Selected by completion reference'};
    if(['TIMED_OUT','FAILED','CANCELED','SKIPPED'].includes(status) && view.summary.status==='none') {
      resultLabels.none='No summary available'; resultSub.none='Available evidence is retained';
    }
    if((view.summary.isPriorCompletion || status==='IN_PROGRESS') && view.summary.status==='available') {
      resultLabels.available='Previous result retained'; resultSub.available='Follow-up investigation is active';
    }
    const complete = view.coverage.executions.filter(item=>item.status==='complete').length;
    return `<div class="status-grid">
      <section class="stat-card"><div class="stat-label">Task lifecycle ${icon('activity')}</div><div class="stat-value"><i class="stat-dot ${toneFor(status)}"></i><span class="${statusLabel(status).length>16?'small-value':''}">${esc(statusLabel(status))}</span></div><div class="stat-sub">Native task state · version ${esc(view.task.version)}</div></section>
      <section class="stat-card"><div class="stat-label">Investigation result ${icon('file')}</div><div class="stat-value"><span class="small-value">${resultLabels[view.summary.status] || esc(view.summary.status)}</span></div><div class="stat-sub">${resultSub[view.summary.status] || esc(view.summary.reason)}</div></section>
      <section class="stat-card"><div class="stat-label">Published records ${icon('layers')}</div><div class="stat-value"><span class="status-number">${view.counts.records}</span></div><div class="stat-sub">${view.counts.executions} executions · ${view.counts.running} running</div></section>
      <section class="stat-card"><div class="stat-label">Collection coverage ${icon('shield')}</div><div class="stat-value"><span class="small-value">${view.coverage.status==='complete'?'Evidence complete':'Evidence partial'}</span>${view.coverage.status==='partial'?icon('info','sm'):''}</div><div class="stat-sub">${complete} / ${view.coverage.executions.length} scopes without known gaps · ${view.coverage.freshness==='stale'?'stale observation':time(view.coverage.asOf)+' CET'}</div></section>
    </div>`;
  }
  function render() {
    const view = currentView(), live = liveView();
    renderQueue(); renderTopbar(view);
    const priority = String(view.task.priority || '').toLowerCase();
    const snapshotBanner = view.isSnapshot ? `<div class="snapshot-banner"><div class="flex" style="align-items:flex-start">${icon('lock')}<div><strong>Historical snapshot · ${esc(view.snapshot?.title || ui.snapshotId)}</strong><div class="sub">Captured ${stamp(view.snapshot?.capturedAt || view.now)}${view.newActivity?' · New activity is available in the live view.':' · Retained evidence and projections.'}</div></div></div><button class="btn small" data-action="return-live">${icon('activity','sm')}Return live</button></div>` : '';
    $('#workspace').innerHTML = `<div class="page-heading"><div><div class="eyebrow"><span class="tag">${esc(view.meta.code)}</span><span class="priority ${priority}">${icon('activity','sm')}${esc(view.task.priority || 'Unspecified')} priority</span>${view.isSnapshot?badge('Snapshot','blue'):badge('Investigation','outline')}</div><h1>${esc(view.task.title)}</h1><div class="page-description"><span>${esc(view.meta.service)}</span><i class="dot-separator"></i><span>${esc(view.scope.name || view.meta.spaceName)}</span><i class="dot-separator"></i><span>${esc(view.meta.owner)}</span><i class="dot-separator"></i><span>${date(view.task.createdAt)}</span></div></div><div class="page-actions"><button class="btn" data-action="export">${icon('download','sm')}Export ${view.isSnapshot?'snapshot':'view'}</button><button class="btn primary" data-action="capture">${icon('snapshot','sm')}Capture ${view.isSnapshot?'live state':'snapshot'}</button></div></div>${snapshotBanner}${renderReplay(view,live)}${renderStats(view)}
      <div class="tabs" role="tablist" aria-label="Investigation sections">${tabs.map(tab=>`<button class="tab ${ui.tab===tab.id?'active':''}" role="tab" id="tab-${tab.id}" aria-selected="${ui.tab===tab.id}" aria-controls="view-content" tabindex="${ui.tab===tab.id?'0':'-1'}" data-action="tab" data-tab="${tab.id}">${icon(tab.icon)}${tab.label}${tab.count?`<span class="tab-count">${view.counts[tab.count] ?? 0}</span>`:tab.id==='history'?`<span class="tab-count">${live.snapshots.length}</span>`:''}</button>`).join('')}</div>
      <div id="view-content" class="view-region" role="tabpanel" aria-labelledby="tab-${ui.tab}">${renderView(view,live)}</div>
      <footer class="view-footer"><span>${icon('shield')}Synthetic observations · ${esc(view.provenance.projectionVersion)} · Clock: Europe/Zurich</span><span class="footer-right">${view.isSnapshot?'Retained snapshot':`Observed at ${time(view.coverage.asOf,true)} CET`} · ${storageAvailable?'Saved in this browser':'Session memory only'}</span></footer>`;
  }
  function renderView(view,live) {
    return ({overview:renderOverview,timeline:renderTimeline,evidence:renderEvidence,executions:renderExecutions,artifacts:renderArtifacts,history:()=>renderHistory(view,live),model:renderModel})[ui.tab](view);
  }
  function timelineRow(item,full=false) {
    const glyph={agent:'bot',lifecycle:'activity',evidence:'search',conversation:'message',collection:'layers'}[item.category] || 'file';
    const timestamp = full ? item.occurredAt || item.recordedAt || item.observedAt : item.observedAt;
    const clockBasis = full ? (item.occurredAt?'event time':item.recordedAt?'record time':'collected') : 'collected';
    return `<button class="timeline-item" data-action="timeline-item" data-id="${esc(item.id)}"><span class="timeline-marker ${esc(item.category)}">${icon(glyph)}</span><span class="timeline-item-content"><span class="timeline-title">${esc(item.title)}</span><span class="timeline-desc" style="display:block">${esc(full?item.body:shorten(item.body,138))}</span><span class="timeline-tags"><span class="source-chip">${icon('link')}${item.sourceRefs.length} source${item.sourceRefs.length===1?'':'s'}</span>${full?`<span class="source-chip">${esc(originLabel(item.origin))}</span>`:''}<span class="source-chip">${esc(categoryLabel(item.category))}</span></span></span><span class="timeline-time">${time(timestamp,full)}<small>${clockBasis}</small></span></button>`;
  }
  function summaryPanel(view,compact=false) {
    const summary=view.summary;
    if(summary.status==='pending') return `<section class="panel">${panelHead('Investigation result',badge('Awaiting record','amber'))}<div class="panel-body">${info('<strong>Task completed. Summary still being retrieved.</strong><br>The completion notification names an exact result record. That record is not in the collected history yet.','')}<div class="working-note">${esc(summary.reason)}</div><div class="result-selection">${icon('link')}<span>Expected record <code>${esc(summary.recordId)}</code></span></div></div></section>`;
    if(summary.status==='available') {
      const selectedRecord=view.records.find(record=>record.recordId===summary.recordId && record.executionId===summary.executionId);
      const prior=summary.isPriorCompletion || view.task.status==='IN_PROGRESS';
      return `<section class="panel">${panelHead(prior?'Previous completed result':'Investigation result',badge(prior?'Follow-up active':'Referenced result',prior?'blue':'complete'))}<div class="panel-body">${prior?'<div class="notice-inline" style="margin-bottom:15px">'+icon('clock')+'<span>This summary belongs to the earlier completed phase. The resumed investigation is gathering additional evidence.</span></div>':''}<div class="result-body">${markdown(compact?shorten(summary.body,950):summary.body)}</div><div class="result-selection">${icon('shield')}<span>Exact summary record selected from the completion reference. ${summary.candidates.length>1?`${summary.candidates.length} candidates retained.`:''}</span></div><div style="margin-top:13px">${sourceButton(selectedRecord?.sourceRefId,'Inspect result and provenance')}</div></div></section>`;
    }
    if(summary.status==='none' && ['TIMED_OUT','FAILED','CANCELED','SKIPPED'].includes(view.task.status)) return `<section class="panel">${panelHead('Available investigation evidence',badge(statusLabel(view.task.status),toneFor(view.task.status)))}<div class="panel-body"><div class="finding-card" style="background:#f9fafb;border-color:#dfe7ec"><h3>No referenced summary is available.</h3><p style="color:#6a7e8d">${esc(summary.reason)}</p></div><div class="working-note">The collected evidence is retained. Investigation ${statusLabel(view.task.status).toLowerCase()} does not establish incident recovery.</div><button class="link-btn" style="margin-top:15px" data-action="tab" data-tab="executions">Inspect available records ${icon('arrow','sm')}</button></div></section>`;
    const finding = view.findings[0];
    return `<section class="panel">${panelHead('Working assessment',badge(summary.status==='candidate'?'Candidate result':'In progress',summary.status==='candidate'?'blue':'teal'))}<div class="panel-body">${finding?`<button class="finding-card" style="display:block;text-align:left;width:100%" data-action="finding" data-id="${esc(finding.id)}"><span class="badge teal">${esc(originLabel(finding.origin))}</span><h3>${esc(finding.title)}</h3><p>${esc(finding.summary)}</p><span class="finding-meta">${icon('link','sm')}${finding.sourceRefs.length} supporting source${finding.sourceRefs.length===1?'':'s'} ${icon('arrow','sm')}</span></button>`:`<div class="finding-card">${badge('Evidence gathering','teal')}<h3>The investigation is building an assessment.</h3><p>${esc(summary.reason || view.phase.description)}</p></div>`}<div class="working-note">${summary.status==='candidate'?'A candidate summary is available. The authoritative completion reference has not been observed.':'Published observations remain available while the agent continues its investigation.'}</div>${view.findings.length>1?`<div class="evidence-list">${view.findings.slice(1,3).map(f=>`<button class="evidence-row" data-action="finding" data-id="${esc(f.id)}"><span class="evidence-icon">${icon('search')}</span><span><strong>${esc(f.title)}</strong><span class="sub">${esc(shorten(f.summary,100))}</span></span>${icon('chevron')}</button>`).join('')}</div>`:''}</div></section>`;
  }
  function miniExecutions(view) {
    return `<section class="panel">${panelHead('Agent work',`<button class="link-btn" data-action="tab" data-tab="executions">${view.counts.executions} executions ${icon('arrow','sm')}</button>`)}<div class="panel-body"><div class="mini-executions">${view.executions.slice(0,4).map(ex=>`<button class="mini-execution" data-action="execution" data-id="${esc(ex.executionId)}" style="text-align:left"><span class="execution-role"><span class="execution-glyph">${icon(ex.parentExecutionId?'search':'bot')}</span><span><strong>${esc(ex.label)}</strong><small>${ex.recordCount} published record${ex.recordCount===1?'':'s'}</small></span></span>${badge(statusLabel(ex.executionStatus),toneFor(ex.executionStatus),true)}</button>`).join('')}</div></div><div class="panel-foot"><span>Published execution state</span><span>${time(view.coverage.asOf)} CET</span></div></section>`;
  }
  function renderOverview(view) {
    const recent=[...view.timeline].sort((a,b)=>asDate(b.observedAt)-asDate(a.observedAt)).slice(0,5);
    return `<div class="grid-overview"><div class="stack"><section class="panel">${panelHead('Published activity',`<button class="link-btn" data-action="tab" data-tab="timeline">View timeline ${icon('arrow','sm')}</button>`,'Latest collected observations, with their original evidence.') }<div class="timeline">${recent.map(item=>timelineRow(item)).join('')}</div><div class="panel-foot"><span class="flex">${icon('clock')}Times shown in CET</span><span>${view.counts.timeline} observed timeline entries</span></div></section>${view.metrics.length?renderMetric(view.metrics[0]):''}${view.coverage.status==='partial'?info(`<strong>The collected evidence has known gaps.</strong> ${esc(view.coverage.note)} <button class="link-btn" data-action="tab" data-tab="executions">Review coverage ${icon('arrow','sm')}</button>`):''}</div><div class="overview-side stack">${summaryPanel(view,true)}${miniExecutions(view)}<section class="panel">${panelHead('Investigation context')}<div class="panel-body"><dl class="manifest-list"><dt>Application</dt><dd>${esc(view.meta.service)}</dd><dt>Agent Space</dt><dd>${esc(view.scope.name || view.meta.spaceName)}</dd><dt>AWS Region</dt><dd>${esc(view.scope.region)}</dd><dt>Account</dt><dd class="mono">${esc(view.scope.accountId)}</dd><dt>Operator team</dt><dd>${esc(view.meta.owner)} <span class="muted">· demo metadata</span></dd></dl><div class="section-gap notice-inline">${icon('info')}<span>All evidence in this workspace is fictional. Live AWS data has not been connected.</span></div></div></section></div></div>`;
  }
  function renderTimeline(view) {
    const term=ui.timelineSearch.toLowerCase();
    const items=[...view.timeline].filter(item=>(ui.timelineFilter==='all'||item.category===ui.timelineFilter)&&[item.title,item.body,item.category].join(' ').toLowerCase().includes(term)).sort((a,b)=>asDate(b.occurredAt||b.recordedAt||b.observedAt)-asDate(a.occurredAt||a.recordedAt||a.observedAt));
    return `<div class="section-heading"><div><h2>Investigation timeline</h2><p>Published activity and incident evidence retain separate event, record, and collection clocks.</p></div>${badge(`${items.length} entries`,'outline')}</div><div class="view-toolbar"><div class="filters" aria-label="Filter timeline">${['all','agent','evidence','lifecycle','conversation','collection'].map(cat=>`<button class="filter ${ui.timelineFilter===cat?'active':''}" data-action="timeline-filter" data-filter="${cat}" aria-pressed="${ui.timelineFilter===cat}">${cat==='all'?'All activity':categoryLabel(cat)}</button>`).join('')}</div><label class="search-input">${icon('search')}<input class="input" id="timeline-search" aria-label="Search timeline" placeholder="Search published activity" value="${esc(ui.timelineSearch)}"></label></div><section class="panel"><div class="timeline timeline-full">${items.length?items.map(item=>timelineRow(item,true)).join(''):empty('No matching activity','Try another category or clear the search.','search')}</div></section><div class="section-gap notice-inline">${icon('info')}<span>Order is a display convention. Adjoining timestamps do not establish a causal relationship. Select any entry to inspect its sources.</span></div>`;
  }
  function renderMetric(metric) {
    const points=metric.points || [];
    if(!points.length) return '';
    const w=600,h=170,pad={l:39,r:14,t:14,b:28};
    const max=Math.max(1,...points.map(p=>p.value),metric.threshold||0,metric.baseline||0)*1.15;
    const first=asDate(points[0].at).getTime(),last=asDate(points[points.length-1].at).getTime();
    const x=p=>pad.l+(last===first?.5:(asDate(p.at).getTime()-first)/(last-first))*(w-pad.l-pad.r);
    const y=value=>pad.t+(1-value/max)*(h-pad.t-pad.b);
    const coords=points.map(p=>`${x(p).toFixed(1)},${y(p.value).toFixed(1)}`);
    const area=`M${pad.l},${h-pad.b} L${coords.join(' L')} L${x(points[points.length-1])},${h-pad.b} Z`;
    const latest=points[points.length-1];
    const valueText=Number(latest.value).toLocaleString('en-GB',{maximumFractionDigits:2});
    const unit=metric.unit || '';
    const pointLabelIndices=[...new Set([0,Math.floor((points.length-1)/2),points.length-1])];
    return `<section class="panel">${panelHead(metric.label,`<button class="link-btn" data-action="metric" data-id="${esc(metric.id)}">Inspect evidence ${icon('arrow','sm')}</button>`)}<div class="panel-body"><div class="metric-top"><div><span class="metric-value">${valueText}<span class="metric-unit">${esc(unit)}</span></span><div class="metric-caption">Latest observed point · ${time(latest.at,true)} CET</div></div>${badge('Synthetic telemetry','outline')}</div><div class="sparkline-wrap"><svg class="metric-chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="${esc(metric.label)}: ${points.length} synthetic points between ${time(points[0].at)} and ${time(latest.at)} CET; latest value ${valueText} ${esc(unit)}"><defs><linearGradient id="chart-fill-${esc(metric.id)}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#58aa96" stop-opacity=".19"/><stop offset="100%" stop-color="#58aa96" stop-opacity=".015"/></linearGradient></defs>${[0,.5,1].map(ratio=>{const value=ratio*max;return `<line class="chart-grid" x1="${pad.l}" y1="${y(value)}" x2="${w-pad.r}" y2="${y(value)}"/><text class="chart-label" x="${pad.l-8}" y="${y(value)+3}" text-anchor="end">${Math.round(value).toLocaleString('en-GB')}</text>`;}).join('')}<path d="${area}" fill="url(#chart-fill-${esc(metric.id)})"/>${metric.threshold!=null?`<line x1="${pad.l}" y1="${y(metric.threshold)}" x2="${w-pad.r}" y2="${y(metric.threshold)}" stroke="#d8b177" stroke-dasharray="4 4" stroke-width="1"/>`:''}<polyline points="${coords.join(' ')}" fill="none" stroke="#299182" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/><circle cx="${x(latest)}" cy="${y(latest.value)}" r="3.6" fill="#218b7e" stroke="white" stroke-width="2"/>${pointLabelIndices.map(i=>`<text class="chart-label" x="${x(points[i])}" y="${h-8}" text-anchor="${i===0?'start':i===points.length-1?'end':'middle'}">${time(points[i].at)}</text>`).join('')}</svg></div><div class="chart-legend"><span><i class="legend-line"></i>${esc(metric.aggregation || 'Observed series')}</span>${metric.threshold!=null?`<span><i class="legend-line amber"></i>Scenario threshold · ${esc(metric.threshold)} ${esc(unit)}</span>`:''}</div></div><div class="panel-foot"><span>${esc(shorten(metric.note || 'Source points retain their query and time window.',115))}</span><span>CET</span></div></section>`;
  }
  function splitLabel(value,limit=25) {
    const words=String(value).split(/\s+/),lines=[''];
    for(const word of words){const i=lines.length-1;if((lines[i]+' '+word).trim().length>limit&&lines[i])lines.push(word);else lines[i]+=(lines[i]?' ':'')+word;}
    return lines.slice(0,2).map((line,index)=>index===1&&lines.length>2?shorten(line+' '+lines.slice(2).join(' '),limit+2):line);
  }
  function graphSVG(graph) {
    if(!graph.nodes.length) return empty('Evidence graph is forming','Graph elements appear only when the collected sources support them.','graph');
    const width=600,nodeW=216,nodeH=88,rowH=146,top=28,rows=Math.ceil(graph.nodes.length/2),height=rows*rowH+8;
    const positions={};
    graph.nodes.forEach((node,i)=>{const lastSingle=i===graph.nodes.length-1&&graph.nodes.length%2;positions[node.id]={x:lastSingle?(width-nodeW)/2:(i%2?352:32),y:top+Math.floor(i/2)*rowH};});
    const edges=graph.edges.map(edge=>{
      const s=positions[edge.source],t=positions[edge.target];if(!s||!t)return '';
      let d,lx,ly;
      if(s.y===t.y){const right=t.x>s.x;const sx=s.x+(right?nodeW:0),tx=t.x+(right?0:nodeW),sy=s.y+nodeH/2;d=`M${sx} ${sy} C${(sx+tx)/2} ${sy-25} ${(sx+tx)/2} ${sy-25} ${tx} ${sy}`;lx=(sx+tx)/2;ly=sy-26;}
      else if(s.x===t.x && Math.abs(s.y-t.y)>rowH){
        // A long relationship uses the clear center corridor instead of passing
        // through an intervening node. The evidence fixtures have at most two
        // columns, so this route preserves both endpoints without a false join.
        const right=s.x>width/2,sx=s.x+(right?0:nodeW),tx=t.x+(right?0:nodeW),sy=s.y+nodeH/2,ty=t.y+nodeH/2;
        lx=width/2;ly=(sy+ty)/2-7;d=`M${sx} ${sy} L${lx} ${sy} L${lx} ${ty} L${tx} ${ty}`;
      }
      else {const down=t.y>s.y,sx=s.x+nodeW/2,tx=t.x+nodeW/2,sy=s.y+(down?nodeH:0),ty=t.y+(down?0:nodeH);const mid=(sy+ty)/2,diagonal=s.x!==t.x,curve=diagonal?mid+(down?-10:10):mid;d=`M${sx} ${sy} C${sx} ${curve} ${tx} ${curve} ${tx} ${ty}`;lx=(sx+tx)/2;ly=diagonal?mid+(down?-18:10):mid-5;}
      const labelLines=splitLabel(edge.label || edge.kind,17);
      return `<g class="graph-relation" data-action="graph-edge" data-id="${esc(edge.id)}" role="button" tabindex="0" aria-label="Inspect relationship: ${esc(edge.label)}"><path d="${d}" stroke="transparent" stroke-width="14" fill="none"/><path class="graph-edge ${String(edge.origin).includes('inference')?'inferred':''}" d="${d}" marker-end="url(#edge-arrow)"/><text class="graph-edge-label" x="${lx}" y="${ly}" text-anchor="middle">${labelLines.map((line,index)=>`<tspan x="${lx}" dy="${index?13:0}">${esc(line)}</tspan>`).join('')}</text></g>`;
    }).join('');
    const nodes=graph.nodes.map(node=>{const p=positions[node.id],lines=splitLabel(node.label,30);const css=['finding','hypothesis'].includes(node.kind)?'finding':node.kind==='resource'?'resource':node.kind==='change'?'change':'';return `<g class="graph-node ${css}" transform="translate(${p.x} ${p.y})" data-action="graph-node" data-id="${esc(node.id)}" role="button" tabindex="0" aria-label="Inspect ${esc(node.label)}"><rect width="${nodeW}" height="${nodeH}" rx="9"/><text class="graph-node-kind" x="13" y="18">${esc(String(node.kind).toUpperCase())}</text>${lines.map((line,i)=>`<text class="graph-node-label" x="13" y="${37+i*15}">${esc(line)}</text>`).join('')}<text class="graph-node-meta" x="13" y="74">${esc(shorten(originLabel(node.origin),29))} · ${node.sourceRefs.length} source${node.sourceRefs.length===1?'':'s'}</text></g>`;}).join('');
    return `<svg class="evidence-graph" viewBox="0 0 ${width} ${height}" role="group" aria-label="${esc(graph.title)}. Select a node or relationship to inspect its source."><defs><marker id="edge-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 1 9 5 0 9" fill="none" stroke="#9db7bd" stroke-width="1.7"/></marker></defs>${edges}${nodes}</svg>`;
  }
  function renderEvidence(view) {
    return `<div class="section-heading"><div><h2>Evidence & findings</h2><p>Every assertion remains connected to its published source.</p></div>${badge(`${view.graph.nodes.length} nodes · ${view.graph.edges.length} relationships`,'outline')}</div><div class="graph-layout"><div class="stack"><section class="panel">${panelHead(view.graph.title || 'Evidence relationships',badge('Derived view','teal'),view.graph.kind?String(view.graph.kind).replaceAll('_',' '):'')}<div class="graph-canvas">${graphSVG(view.graph)}</div><div class="graph-key"><span><i></i>Finding / hypothesis</span><span><i class="blue"></i>Resource</span><span><i class="amber"></i>Change</span><span><i class="gray"></i>Observation</span></div><div class="panel-body"><p class="notice-inline">${icon('info')}<span>${esc(view.graph.note || 'Select a node or relationship to inspect its evidence and assertion origin.')}</span></p></div></section>${view.metrics.map(renderMetric).join('')}</div><div class="graph-side stack"><section class="panel">${panelHead('Published findings',badge(`${view.findings.length}`,'outline'))}<div class="panel-body"><div class="source-list">${view.findings.length?view.findings.map(f=>`<button class="source-card" data-action="finding" data-id="${esc(f.id)}">${badge(f.disposition || 'Reported','teal')}<h3>${esc(f.title)}</h3><p>${esc(f.summary)}</p><span class="source-bottom"><span>${esc(originLabel(f.origin))}</span><span>${f.sourceRefs.length} sources →</span></span></button>`).join(''):'<p class="body-copy">No finding has been published in the collected evidence yet.</p>'}</div></div></section>${summaryPanel(view,true)}</div></div>`;
  }
  function renderExecutions(view) {
    const types=[...new Set(view.records.map(record=>record.recordType))].sort();
    if(ui.recordType!=='all'&&!types.includes(ui.recordType)) ui.recordType='all';
    const records=view.records.filter(record=>ui.recordType==='all'||record.recordType===ui.recordType).sort((a,b)=>asDate(b.timestamp)-asDate(a.timestamp));
    return `<div class="section-heading"><div><h2>Executions & journal</h2><p>Task membership, execution state, and published records remain independently inspectable.</p></div><button class="btn small" data-action="task-source">${icon('code','sm')}Task source</button></div><div class="record-layout"><div class="stack"><section class="panel">${panelHead('Execution hierarchy',badge(`${view.executions.length} executions`,'outline'))}<div>${view.executions.map(ex=>`<button class="execution-tree-row ${ex.parentExecutionId?'child':''}" data-action="execution" data-id="${esc(ex.executionId)}" style="text-align:left;width:${ex.parentExecutionId?'calc(100% - 27px)':'100%'}"><span class="execution-glyph">${icon(ex.parentExecutionId?'search':'bot')}</span><span class="execution-content"><h3>${esc(ex.label)}</h3><p>${esc(ex.agentType || 'Agent type not supplied')} · ${ex.recordCount} records</p><p class="mono" style="font-size:9px">${esc(ex.executionId)}</p></span>${badge(statusLabel(ex.executionStatus),toneFor(ex.executionStatus),true)}</button>`).join('')}</div><div class="panel-foot"><span>${icon('info','sm')}</span><span>Stopped is an execution state; it does not establish success.</span></div></section><section class="panel">${panelHead('Published journal records',badge(`${records.length}`,'outline'))}<div class="records-toolbar"><label class="flex muted tiny">Record type<select class="select" id="record-type" aria-label="Filter journal record type"><option value="all">All record types</option>${types.map(type=>`<option value="${esc(type)}" ${ui.recordType===type?'selected':''}>${esc(type)}</option>`).join('')}</select></label><span class="tiny muted">Newest record first</span></div><div class="record-list">${records.length?records.map(record=>`<button class="record-row" data-action="source" data-id="${esc(record.sourceRefId)}"><span class="evidence-icon">${icon(record.recordType.includes('summary')?'file':'code')}</span><span class="record-text"><strong>${esc(record.recordType)}</strong><small>${esc(shorten(record.preview,92))}</small></span><span class="record-time">${time(record.timestamp,true)}</span>${icon('chevron','sm')}</button>`).join(''):empty('No matching records','Select another journal record type.','file')}</div></section></div><div class="record-side stack"><section class="panel">${panelHead('Collection coverage',badge(view.coverage.status==='complete'?'Complete':'Partial',view.coverage.status==='complete'?'complete':'amber'))}<div class="panel-body"><p class="body-copy">${esc(view.coverage.note)}</p><div class="coverage-rows section-gap">${view.coverage.executions.map(ex=>`<div class="coverage-row"><div>${esc(ex.label)}<small>${ex.pagesRead} page${ex.pagesRead===1?'':'s'} collected · ${ex.recordCount} records</small><small>Journal pagination: ${ex.paginationStatus==='complete'?'exhausted':'more pages'}</small>${ex.status!=='complete'?`<small style="color:#9b783c">${esc(ex.reason)}</small>`:''}</div><div class="coverage-count">${badge(ex.status==='complete'?'Complete':'Partial',ex.status==='complete'?'complete':'amber')}</div></div>`).join('')}</div><div class="result-selection">${icon('clock')}<span>As of ${stamp(view.coverage.asOf)} · ${esc(view.coverage.freshness)} observation</span></div></div></section><section class="panel">${panelHead('What the journal preserves')}<div class="panel-body"><p class="body-copy">A record has an identity, execution, type, creation time, and JSON content. Its content may be an object, array, scalar, or null.</p><div class="section-gap notice-inline">${icon('shield')}<span>Demo payload profiles use the <code>demo.</code> namespace. They illustrate parsing; they are not AWS-defined record schemas.</span></div></div></section>${view.coverage.gaps.length?info(`<strong>Known collection gaps</strong><br>${view.coverage.gaps.map(gap=>esc(typeof gap==='string'?gap:gap.reason||pretty(gap))).join('<br>')}`):''}</div></div>`;
  }
  function renderArtifacts(view) {
    const filtered=view.artifacts.filter(item=>ui.artifactFilter==='all'||(ui.artifactFilter==='available'?item.status==='available':item.status!=='available'));
    const statusText={available:'Available',pending:'Not yet retrieved',access_denied:'Access denied',unresolved:'Unresolved reference'};
    return `<div class="section-heading"><div><h2>Artifacts & references</h2><p>Published results, attachments, and external references retain their own availability and version.</p></div>${badge(`${view.counts.availableArtifacts} / ${view.counts.artifacts} available`,'outline')}</div><div class="view-toolbar"><div class="filters">${[['all','All artifacts'],['available','Available'],['unavailable','Needs attention']].map(([key,label])=>`<button class="filter ${ui.artifactFilter===key?'active':''}" aria-pressed="${ui.artifactFilter===key}" data-action="artifact-filter" data-filter="${key}">${label}</button>`).join('')}</div><span class="small muted">Select an artifact to inspect its source.</span></div><div class="artifact-grid">${filtered.map(item=>`<button class="artifact-card" data-action="artifact" data-id="${esc(item.id)}"><span class="artifact-top"><span class="file-icon ${item.status!=='available'?'amber':item.sourceKind==='asset'?'blue':''}">${icon(item.status==='access_denied'?'lock':item.kind==='external'?'link':'file')}</span>${badge(statusText[item.status] || item.status,item.status==='available'?'complete':item.status==='access_denied'?'red':'amber')}</span><h3>${esc(item.name || item.filename)}</h3><p>${esc(item.description)}</p><span class="artifact-meta"><span class="artifact-mime">${esc(item.mediaType || item.kind || 'Content type unknown')}</span><span class="flex">${item.version!=null?`v${esc(item.version)}`:'Version not established'}${icon('arrow')}</span></span></button>`).join('')}</div>${!filtered.length?`<section class="panel">${empty('No matching artifacts','Try another availability filter.','folder')}</section>`:''}<div class="section-gap callout neutral">${icon('info')}<div>Asset attachment, result publication, and content retrieval are different observations. A current workspace asset does not establish which version an investigation consumed.</div></div>`;
  }
  function renderHistory(view,live) {
    const selected=view.isSnapshot?view.snapshot:null;
    const comparison=view.isSnapshot?view:live.snapshots.length?Model.view(state,ui.taskId,live.snapshots[live.snapshots.length-1].snapshotId):null;
    const snapMeta=selected || comparison?.snapshot;
    return `<div class="section-heading"><div><h2>Retained investigation history</h2><p>Capture the evidence, results, and coverage an operator actually reviewed.</p></div><button class="btn small" data-action="capture">${icon('snapshot','sm')}Capture live state</button></div><div class="history-layout"><section class="panel">${panelHead('Snapshots',badge(`${live.snapshots.length}`,'outline'))}${live.snapshots.length?`<div class="snapshot-list">${[...live.snapshots].reverse().map(snap=>`<button class="snapshot-card ${ui.snapshotId===snap.snapshotId?'selected':''}" data-action="select-snapshot" data-id="${esc(snap.snapshotId)}"><span class="between">${badge(statusLabel(snap.taskStatus),toneFor(snap.taskStatus))}<span class="tiny muted">${esc(snap.snapshotId)}</span></span><h3>${esc(snap.title)}</h3><p>${stamp(snap.capturedAt)}</p><span class="snapshot-meta"><span>${snap.recordCount} records</span><i class="dot-separator"></i><span>${snap.coverageStatus==='complete'?'Complete history':'Partial capture'}</span>${icon('arrow','sm')}</span></button>`).join('')}</div>`:empty('No snapshot captured yet','Capture the current view, or advance the replay until its first referenced result is retrieved.','snapshot')}<div class="panel-foot"><span>${icon('lock','sm')}</span><span>Retained views remain unchanged after new activity.</span></div></section><div class="stack">${comparison?`<section class="panel">${panelHead('Snapshot compared with live',view.isSnapshot?badge('Viewing snapshot','blue'):badge('Latest capture','outline'))}<table class="comparison-table"><thead><tr><th scope="col">Observation</th><th scope="col">Captured</th><th scope="col">Live view</th></tr></thead><tbody><tr><td>Task state</td><td>${badge(statusLabel(comparison.task.status),toneFor(comparison.task.status))}</td><td>${badge(statusLabel(live.task.status),toneFor(live.task.status))}</td></tr><tr><td>Task version</td><td>${comparison.task.version}</td><td>${live.task.version}</td></tr><tr><td>Executions</td><td>${comparison.counts.executions}</td><td>${live.counts.executions}</td></tr><tr><td>Journal records</td><td>${comparison.counts.records}</td><td>${live.counts.records}</td></tr><tr><td>Result availability</td><td>${esc(comparison.summary.status)}</td><td>${esc(live.summary.status)}</td></tr><tr><td>Collection coverage</td><td>${esc(comparison.coverage.status)}</td><td>${esc(live.coverage.status)}</td></tr><tr><td>Observed at</td><td>${time(comparison.coverage.asOf,true)} CET</td><td>${time(live.coverage.asOf,true)} CET</td></tr></tbody></table><div class="panel-body" style="padding-top:17px"><div class="history-actions">${!view.isSnapshot?`<button class="btn primary small" data-action="select-snapshot" data-id="${esc(snapMeta.snapshotId)}">${icon('eye','sm')}Open captured view</button>`:`<button class="btn primary small" data-action="return-live">${icon('activity','sm')}Return live</button>`}<button class="btn small" data-action="export-snapshot" data-id="${esc(snapMeta.snapshotId)}">${icon('download','sm')}Export capture</button></div></div></section><section class="panel">${panelHead('Capture manifest')}<div class="panel-body"><dl class="manifest-list"><dt>Snapshot</dt><dd><code>${esc(snapMeta.snapshotId)}</code></dd><dt>Captured at</dt><dd>${stamp(snapMeta.capturedAt)}</dd><dt>Task identity</dt><dd class="mono">${esc(comparison.task.taskId)}</dd><dt>Source observations</dt><dd>${Object.keys(comparison.sources).length} retained sources</dd><dt>Projection</dt><dd>${esc(comparison.provenance.projectionVersion)}</dd><dt>Coverage</dt><dd>${esc(comparison.coverage.note)}</dd></dl></div></section>`:`<section class="panel">${panelHead('A completed task can continue')}<div class="panel-body"><p class="body-copy">A later operator follow-up can resume the same investigation. Capturing a snapshot preserves the task version, execution membership, journal observations, artifact references, and the derived views shown at that moment.</p><div class="section-gap">${info('The replay automatically captures the first retrieved result before the investigation resumes. You can also capture a partial view at any time.','blue')}</div></div></section>`}<div class="callout neutral">${icon('info')}<div>Snapshots are application-owned captures. They record an observation window and known gaps; the native API does not promise a transactionally consistent cross-endpoint snapshot.</div></div></div></div>`;
  }
  function renderModel() {
    const diagram=diagrams.find(item=>item.id===ui.diagramId) || diagrams[0];
    return `<div class="section-heading"><div><h2>Reviewed model & report</h2><p>The documented AWS contract, the proposed application model, and all nine reviewed diagrams.</p></div><a class="btn small" href="report.md" target="_blank" rel="noopener">${icon('book','sm')}Read report ${icon('external','sm')}</a></div><div class="principle-grid"><div class="principle">${icon('layers')}<h3>Native objects stay native</h3><p>Investigation = Task of type INVESTIGATION, execution membership, and published journal records.</p></div><div class="principle">${icon('link')}<h3>Every derived view has a source</h3><p>Timelines, findings, graphs, and artifact references retain attribution and exact source revisions.</p></div><div class="principle">${icon('lock')}<h3>History stays reproducible</h3><p>Immutable application captures preserve the evidence reviewed before an investigation resumes.</p></div></div><div class="model-layout"><section class="panel"><div class="panel-head"><h3>Model diagrams</h3>${badge(`${diagrams.length}`,'outline')}</div><nav class="diagram-list" aria-label="Select model diagram">${diagrams.map(item=>`<button class="diagram-option ${item.id===diagram?.id?'active':''}" data-action="diagram" data-id="${esc(item.id)}" ${item.id===diagram?.id?'aria-current="true"':''}><span class="diagram-number">${esc(item.id)}</span><span><strong>${esc(item.title)}</strong><small>${item.type==='erDiagram'?'Entity relationships':item.type==='sequenceDiagram'?'Live synchronization':'Snapshot workflow'}</small></span></button>`).join('')}</nav></section><div class="stack"><section class="panel">${diagram?`${panelHead(diagram.title,`<div class="diagram-toolbar"><button class="btn small" data-action="diagram-fit" title="Fit diagram" aria-label="Fit diagram">${icon('fit','sm')}<span class="hide-narrow">Fit</span></button><button class="btn small" data-action="diagram-zoom" title="${ui.diagramZoom===1?'Enlarge diagram':'Restore diagram scale'}" aria-label="${ui.diagramZoom===1?'Enlarge diagram':'Restore diagram scale'}">${icon('zoom','sm')}<span class="hide-narrow">${ui.diagramZoom===1?'Zoom':'100%'}</span></button><button class="btn small" data-action="diagram-source" aria-pressed="${ui.diagramSource}" title="${ui.diagramSource?'View rendered diagram':'View Mermaid source'}" aria-label="${ui.diagramSource?'View rendered diagram':'View Mermaid source'}">${icon(ui.diagramSource?'eye':'code','sm')}</button><button class="btn small" data-action="diagram-download" title="Download SVG" aria-label="Download diagram SVG">${icon('download','sm')}</button></div>`)}${ui.diagramSource?`<pre class="diagram-source" tabindex="0">${esc(diagram.source)}</pre>`:`<div class="diagram-stage" tabindex="0" aria-label="Scrollable diagram: ${esc(diagram.title)}"><div class="diagram-svg-wrap ${ui.diagramZoom>1?'zoomed':''}" style="width:${Math.round(ui.diagramZoom*100)}%">${diagram.svg}</div></div>`}<div class="panel-foot"><span>Reviewed 5 Nov 2026 · ${esc(diagram.id)}</span><span class="flex"><a href="${esc(diagram.svgPath)}" target="_blank" rel="noopener">Open SVG</a><span>·</span><a href="${esc(diagram.sourcePath)}" download>Mermaid source</a></span></div>`:empty('Diagrams not bundled','Run the application build after rendering the reviewed diagrams.','graph')}</section><div class="callout neutral">${icon('info')}<div>The demonstration uses fictional observations and <code>demo.*</code> content profiles. It does not call AWS or prove live payload behavior. The report distinguishes native fields, documented conventions, and proposed application entities.</div></div></div></div><section class="panel section-gap">${panelHead('Analysis package','', 'Official API model reviewed as of 5 November 2026 · native API version 2026-01-01')}<div class="panel-body"><div class="report-links"><a class="btn small" href="report.md" target="_blank" rel="noopener">${icon('book','sm')}Reviewed report</a><a class="btn small" href="REVIEW.md" target="_blank" rel="noopener">${icon('shield','sm')}Review findings</a><a class="btn small" href="annexes/Investigation_API_Catalog.md" target="_blank" rel="noopener">${icon('code','sm')}API catalog</a><a class="btn small" href="annexes/Investigation_UI_Contract.md" target="_blank" rel="noopener">${icon('layers','sm')}UI contract</a><a class="btn small" href="annexes/Investigation_API_Sources.md" target="_blank" rel="noopener">${icon('link','sm')}Official sources</a></div></div></section>`;
  }
  function sourceRefs(refs,view) {
    return `<div class="inspector-sources">${(refs || []).map(ref=>{
      const source=Model.lookupSource(view,ref);
      return source?`<button class="inspector-source-btn" data-action="source" data-id="${esc(ref)}"><span class="source-reference">${esc(source.title)}<span>${esc(source.kind)} · ${esc(shorten(source.revisionId,44))}</span></span>${icon('chevron')}</button>`:`<div class="inspector-source-btn"><span class="source-reference">Reference unavailable<span>${esc(ref)}</span></span>${icon('alert')}</div>`;
    }).join('')}</div>`;
  }
  function inspect(title,eyebrow,body,view,payload=null) {
    ui.inspectorView=view; ui.inspectorPayload=payload;
    const dialog=$('#inspector');
    if(!dialog.open) ui.inspectorReturnFocus=document.activeElement;
    dialog.innerHTML=`<header class="inspector-header"><div><div class="inspector-eyebrow">${esc(eyebrow)}</div><h2 id="inspector-title">${esc(title)}</h2></div><button class="icon-btn" data-action="close-inspector" aria-label="Close details">${icon('cross')}</button></header><div class="inspector-body">${body}</div>`;
    if(!dialog.open) dialog.showModal();
    dialog.scrollTop=0;
    dialog.querySelector('[data-action="close-inspector"]').focus({preventScroll:true});
  }
  function inspectSource(id,view) {
    const source=Model.lookupSource(view,id);
    if(!source){inspect('Source not available','Source inspection',info('This reference is not present in the retained source collection.'),view);return;}
    inspect(source.title,'Source observation',`<div class="inspector-badges">${badge(source.kind,'blue')}${badge('Synthetic source','outline')}${view.isSnapshot?badge('Retained snapshot','blue'):''}</div><section class="inspector-section"><dl class="manifest-list"><dt>Native identity</dt><dd class="mono">${esc(source.nativeId || 'Not supplied')}</dd><dt>Source revision</dt><dd class="mono">${esc(source.revisionId)}</dd><dt>Observed at</dt><dd>${stamp(source.observedAt)}</dd><dt>Source locator</dt><dd><code>${esc(source.locator || '/')}</code></dd><dt>Canonical JSON hash</dt><dd class="mono">${esc(source.payloadHash || 'Not supplied')}</dd>${source.operation?`<dt>Read operation</dt><dd><code>${esc(source.operation)}</code></dd>`:''}</dl></section>${source.query?`<section class="inspector-section"><h3>Read query context</h3><pre class="raw-json" tabindex="0">${esc(pretty(source.query))}</pre></section>`:''}<section class="inspector-section"><div class="between" style="margin-bottom:12px"><h3 style="margin:0">Source payload</h3><button class="btn small" data-action="download-inspector">${icon('download','sm')}Export JSON</button></div><pre class="raw-json" tabindex="0">${esc(pretty(source.payload))}</pre></section><div class="callout neutral">${icon('info')}<div>Fictional, normalized source observation. Native field names and values illustrate the reviewed model; this is not a captured AWS response.</div></div>`,view,{value:source,filename:`source-${source.nativeId || id}.json`,mediaType:'application/json'});
  }
  function inspectTimeline(id,view) {
    const item=view.timeline.find(row=>row.id===id);if(!item)return;
    inspect(item.title,'Timeline entry',`<div class="inspector-badges">${badge(categoryLabel(item.category),'blue')}${badge(originLabel(item.origin),'teal')}</div><section class="inspector-section"><p>${esc(item.body)}</p></section><section class="inspector-section"><h3>Independent clocks</h3><dl class="manifest-list"><dt>Event time</dt><dd>${stamp(item.occurredAt)}</dd><dt>Record time</dt><dd>${stamp(item.recordedAt)}</dd><dt>Observed at</dt><dd>${stamp(item.observedAt)}</dd><dt>Projection revision</dt><dd class="mono">${esc(item.projectionRevisionId)}</dd>${item.executionId?`<dt>Execution</dt><dd class="mono">${esc(item.executionId)}</dd>`:''}</dl></section><section class="inspector-section"><h3>Source evidence</h3>${sourceRefs(item.sourceRefs,view)}</section><div class="callout neutral">${icon('info')}<div>Timeline placement is an application projection. Its clock and source attribution remain available for inspection.</div></div>`,view,{value:item,filename:`timeline-${item.id}.json`});
  }
  function inspectFinding(id,view) {
    const finding=view.findings.find(row=>row.id===id);if(!finding)return;
    inspect(finding.title,'Published finding',`<div class="inspector-badges">${badge(originLabel(finding.origin),'teal')}${badge(finding.disposition || 'Reported','outline')}</div><section class="inspector-section"><blockquote class="inspector-quote">${esc(finding.summary)}</blockquote></section><section class="inspector-section"><h3>Supporting evidence</h3>${sourceRefs(finding.sourceRefs,view)}</section><div class="callout neutral">${icon('info')}<div>Attribution describes who reported this finding. No numerical confidence or confirmed recovery is inferred from it.</div></div>`,view,{value:finding,filename:`finding-${finding.id}.json`});
  }
  function inspectGraphNode(id,view) {
    const node=view.graph.nodes.find(item=>item.id===id);if(!node)return;
    const relations=view.graph.edges.filter(edge=>edge.source===id || edge.target===id);
    inspect(node.label,'Evidence graph node',`<div class="inspector-badges">${badge(node.kind,'blue')}${badge(originLabel(node.origin),'teal')}</div>${node.subtitle?`<section class="inspector-section"><p>${esc(node.subtitle)}</p></section>`:''}<section class="inspector-section"><h3>Published sources</h3>${sourceRefs(node.sourceRefs,view)}</section><section class="inspector-section"><h3>Related assertions</h3><div class="inspector-sources">${relations.map(edge=>`<button class="inspector-source-btn" data-action="graph-edge" data-id="${esc(edge.id)}"><span>${esc(view.graph.nodes.find(n=>n.id===edge.source)?.label || edge.source)} <strong>${esc(edge.label)}</strong> ${esc(view.graph.nodes.find(n=>n.id===edge.target)?.label || edge.target)}</span>${icon('chevron')}</button>`).join('') || '<p>No related assertions in this graph revision.</p>'}</div></section><div class="notice-inline">${icon('info')}<span>Graph kind: ${esc(String(view.graph.kind).replaceAll('_',' '))}. Graph relationships keep their assertion origin.</span></div>`,view,{value:node,filename:`graph-node-${id}.json`});
  }
  function inspectGraphEdge(id,view) {
    const edge=view.graph.edges.find(item=>item.id===id);if(!edge)return;
    const from=view.graph.nodes.find(n=>n.id===edge.source),to=view.graph.nodes.find(n=>n.id===edge.target);
    inspect(edge.label || edge.kind,'Evidence relationship',`<div class="inspector-badges">${badge(edge.kind,'blue')}${badge(originLabel(edge.origin),'teal')}</div><section class="inspector-section"><dl class="manifest-list"><dt>Source node</dt><dd>${esc(from?.label || edge.source)}</dd><dt>Target node</dt><dd>${esc(to?.label || edge.target)}</dd><dt>Relationship</dt><dd>${esc(edge.label)}</dd><dt>Graph snapshot</dt><dd class="mono">${esc(view.graph.id)}</dd></dl></section><section class="inspector-section"><h3>Evidence for this relationship</h3>${sourceRefs(edge.sourceRefs,view)}</section>`,view,{value:edge,filename:`graph-edge-${id}.json`});
  }
  function inspectExecution(id,view) {
    const execution=view.executions.find(row=>row.executionId===id);if(!execution)return;
    inspect(execution.label,'Execution',`<div class="inspector-badges">${badge(statusLabel(execution.executionStatus),toneFor(execution.executionStatus),true)}${badge('Native execution','outline')}</div><section class="inspector-section"><dl class="manifest-list"><dt>Execution ID</dt><dd class="mono">${esc(execution.executionId)}</dd><dt>Parent execution</dt><dd class="mono">${esc(execution.parentExecutionId || 'Not supplied')}</dd><dt>Agent type</dt><dd>${esc(execution.agentType || 'Not supplied')}</dd><dt>Subtask</dt><dd>${esc(execution.agentSubTask)}</dd><dt>Created</dt><dd>${stamp(execution.createdAtIso || execution.createdAt)}</dd><dt>Updated</dt><dd>${stamp(execution.updatedAtIso || execution.updatedAt)}</dd><dt>Collected records</dt><dd>${execution.recordCount}</dd></dl></section><section class="inspector-section"><h3>Source observations</h3>${sourceRefs(execution.sourceRefs,view)}</section><section class="inspector-section"><h3>Native execution envelope</h3><pre class="raw-json" tabindex="0">${esc(pretty(execution.raw))}</pre></section><div class="callout neutral">${icon('info')}<div>Task membership is retained from the execution listing context. The returned execution body does not carry a task ID. A stopped execution is not, by itself, a successful result.</div></div>`,view,{value:execution.raw,filename:`execution-${id}.json`});
  }
  function inspectMetric(id,view) {
    const metric=view.metrics.find(row=>row.id===id);if(!metric)return;
    inspect(metric.label,'Telemetry evidence',`<div class="inspector-badges">${badge('Synthetic telemetry','outline')}${badge(metric.aggregation || 'Observed samples','teal')}</div><section class="inspector-section"><p>${esc(metric.note)}</p><dl class="manifest-list section-gap"><dt>Unit</dt><dd>${esc(metric.unit)}</dd><dt>Aggregation</dt><dd>${esc(metric.aggregation)}</dd><dt>Time window</dt><dd>${time(metric.points[0]?.at,true)}–${time(metric.points[metric.points.length-1]?.at,true)} CET</dd><dt>Query</dt><dd><code>${esc(metric.query)}</code></dd></dl></section><section class="inspector-section"><h3>Source evidence</h3>${sourceRefs(metric.sourceRefs,view)}</section><section class="inspector-section"><h3>Retained data points</h3><pre class="raw-json" tabindex="0">${esc(pretty(metric.points))}</pre></section>`,view,{value:metric,filename:`metric-${id}.json`});
  }
  function inspectArtifact(id,view) {
    const item=view.artifacts.find(row=>row.id===id);if(!item)return;
    const statusText={available:'Available',pending:'Not yet retrieved',access_denied:'Access denied',unresolved:'Unresolved reference'};
    const bodyAvailable=item.status==='available' && item.body!=null;
    const preview=bodyAvailable?`<div class="artifact-preview">${String(item.mediaType).includes('markdown')?`<div class="result-body">${markdown(item.body)}</div>`:`<pre class="artifact-content">${esc(typeof item.body==='string'?item.body:pretty(item.body))}</pre>`}</div>`:info(`<strong>${esc(statusText[item.status] || item.status)}</strong><br>${esc(item.status==='access_denied'?'The retained reference exists, but content access was denied. No content preview was collected.':item.status==='pending'?'The content has not yet been retrieved. A reference does not establish content availability.':'The reference has not been resolved to retrievable content.')}`,item.status==='access_denied'?'':'neutral');
    inspect(item.name || item.filename,'Artifact reference',`<div class="inspector-badges">${badge(statusText[item.status] || item.status,item.status==='available'?'complete':item.status==='access_denied'?'red':'amber')}${badge(item.sourceKind || 'Source reference','outline')}</div><section class="inspector-section"><p>${esc(item.description)}</p></section><section class="inspector-section"><dl class="manifest-list"><dt>Media type</dt><dd>${esc(item.mediaType || 'Not established')}</dd><dt>Asset ID</dt><dd class="mono">${esc(item.assetId || 'No native asset association')}</dd><dt>Asset version</dt><dd>${item.version!=null?esc(item.version):'Not established'}</dd><dt>${item.hashEncoding==='utf8-content-bytes'?'File SHA-256':'Payload hash'}</dt><dd class="mono">${esc(item.hash || 'Not established')}</dd>${item.hash?`<dt>Hash basis</dt><dd>${item.hashEncoding==='utf8-content-bytes'?'UTF-8 bytes of the downloadable content':'Canonical JSON representation'}</dd>`:''}</dl></section><section class="inspector-section"><div class="between" style="margin-bottom:12px"><h3 style="margin:0">${bodyAvailable?'Retained content':'Availability'}</h3>${bodyAvailable?'<button class="btn small" data-action="download-inspector">'+icon('download','sm')+'Download</button>':''}</div>${preview}</section><section class="inspector-section"><h3>Reference provenance</h3>${sourceRefs(item.sourceRefs,view)}</section>`,view,bodyAvailable?{value:typeof item.body==='string'?item.body:pretty(item.body),filename:item.filename || `${item.id}.txt`,mediaType:item.mediaType || 'text/plain'}:null);
  }
  function inspectTask(view) {
    const source=Object.values(view.sources).find(item=>item.kind==='task' || item.payload?.taskId===view.task.taskId && item.payload?.taskType);
    if(source) inspectSource(source.id,view);
    else inspect(view.task.title,'Native task envelope',`<div class="inspector-badges">${badge(statusLabel(view.task.status),toneFor(view.task.status))}${badge('Normalized synthetic task','outline')}</div><pre class="raw-json" tabindex="0">${esc(pretty(view.task))}</pre>`,view,{value:view.task,filename:`task-${view.task.taskId}.json`});
  }
  function pause() { clearInterval(ui.timer);ui.timer=null;ui.playing=false; }
  function advance() {
    if(!liveView().replay.canAdvance){pause();return;}
    const priorSnapshots=state.snapshots.length;
    Model.advance(state);persist();
    const live=liveView();
    if(!live.replay.canAdvance) pause();
    render();announce(`Scenario stage ${live.phase.number}: ${live.phase.title}. ${ui.snapshotId?'The historical snapshot is unchanged.':''}`);
    if(state.snapshots.length>priorSnapshots) toast('First referenced result captured. Its snapshot will remain unchanged.');
  }
  function togglePlay() {
    if(ui.playing){pause();render();return;}
    if(!liveView().replay.canAdvance)return;
    ui.playing=true;ui.timer=setInterval(advance,6500);render();announce('Scenario replay playing. Each stage advances after six and a half seconds.');
  }
  function setQueueOpen(open) {
    ui.mobileQueue=open;renderQueue();renderTopbar(currentView());
    (open?$('#queue-search'):$('.mobile-menu'))?.focus({preventScroll:true});
  }
  function selectTask(id) {
    if(!Model.portfolio(state).some(row=>row.taskId===id))return;
    const fromDrawer=ui.mobileQueue;
    pause();ui.taskId=id;ui.snapshotId=null;ui.tab='overview';ui.timelineFilter='all';ui.timelineSearch='';ui.recordType='all';ui.artifactFilter='all';ui.mobileQueue=false;render();announce(`Opened ${liveView().task.title}.`);
    if(fromDrawer) $('#workspace').focus({preventScroll:true});
  }
  function changeTab(tab) {
    if(!tabs.some(item=>item.id===tab))return;
    const fromDrawer=ui.mobileQueue;
    ui.tab=tab;ui.mobileQueue=false;render();
    if(fromDrawer) $('#workspace').focus({preventScroll:true});
  }
  function confirmReset() {
    pause();render();
    const dialog=$('#confirm-dialog');dialog.innerHTML=`<h2 id="confirm-title">Reset the demonstration?</h2><p>This restores the initial fictional scenario and removes snapshots saved by this demo in this browser. Download a snapshot first if you want to retain it.</p><div class="confirm-actions"><button class="btn" data-action="cancel-reset">Keep current state</button><button class="btn primary" data-action="confirm-reset">Reset scenario</button></div>`;dialog.showModal();
  }
  function reset() {
    pause();state=Model.createState();ui.taskId=Data.scenario.primaryTaskId;ui.snapshotId=null;ui.tab='overview';ui.timelineFilter='all';ui.timelineSearch='';ui.recordType='all';ui.artifactFilter='all';ui.queueSearch='';persist();$('#confirm-dialog').close();render();toast('Demo scenario reset.');
  }
  function exportView(snapshotId=ui.snapshotId) {
    const payload=Model.exportSnapshot(state,ui.taskId,snapshotId || undefined);
    const view=Model.view(state,ui.taskId,snapshotId || undefined);
    download(payload,`${view.meta.code}-${snapshotId || 'live-view'}.json`);toast(`${snapshotId?'Snapshot':'Current view'} exported as JSON.`);
  }
  document.addEventListener('click',event=>{
    const control=event.target.closest('[data-action]');if(!control || control.disabled)return;
    const action=control.dataset.action,id=control.dataset.id;
    const view=control.closest('#inspector')&&ui.inspectorView?ui.inspectorView:currentView();
    switch(action){
      case 'select-task':selectTask(id);break;
      case 'tab':changeTab(control.dataset.tab);break;
      case 'open-queue':setQueueOpen(true);break;
      case 'close-queue':setQueueOpen(false);break;
      case 'play':togglePlay();break;
      case 'advance':advance();break;
      case 'reset':confirmReset();break;
      case 'cancel-reset':$('#confirm-dialog').close();break;
      case 'confirm-reset':reset();break;
      case 'timeline-filter':ui.timelineFilter=control.dataset.filter;render();break;
      case 'artifact-filter':ui.artifactFilter=control.dataset.filter;render();break;
      case 'source':inspectSource(id,view);break;
      case 'task-source':inspectTask(view);break;
      case 'timeline-item':inspectTimeline(id,view);break;
      case 'finding':inspectFinding(id,view);break;
      case 'graph-node':inspectGraphNode(id,view);break;
      case 'graph-edge':inspectGraphEdge(id,view);break;
      case 'execution':inspectExecution(id,view);break;
      case 'metric':inspectMetric(id,view);break;
      case 'artifact':inspectArtifact(id,view);break;
      case 'close-inspector':$('#inspector').close();break;
      case 'download-inspector':if(ui.inspectorPayload){download(ui.inspectorPayload.value,ui.inspectorPayload.filename,ui.inspectorPayload.mediaType);toast('Retained content downloaded.');}break;
      case 'capture':{pause();const snap=Model.captureSnapshot(state,ui.taskId);ui.snapshotId=snap.snapshotId;ui.tab='history';persist();render();toast('Snapshot captured. You are viewing the retained state.');break;}
      case 'select-snapshot':if(liveView().snapshots.some(s=>s.snapshotId===id)){ui.snapshotId=id;ui.tab='history';render();announce('Historical snapshot opened.');}break;
      case 'return-live':ui.snapshotId=null;render();announce('Returned to the latest collected view.');break;
      case 'export':exportView();break;
      case 'export-snapshot':exportView(id);break;
      case 'diagram':ui.diagramId=id;ui.diagramZoom=1;ui.diagramSource=false;render();break;
      case 'diagram-fit':ui.diagramZoom=1;ui.diagramSource=false;render();break;
      case 'diagram-zoom':ui.diagramZoom=ui.diagramZoom===1?1.5:1;ui.diagramSource=false;render();break;
      case 'diagram-source':ui.diagramSource=!ui.diagramSource;render();break;
      case 'diagram-download':{const diagram=diagrams.find(d=>d.id===ui.diagramId);if(diagram)download(diagram.svg,diagram.svgPath.split('/').pop(),'image/svg+xml');break;}
    }
  });
  document.addEventListener('input',event=>{
    if(event.target.id==='queue-search'){
      const caret=event.target.selectionStart;ui.queueSearch=event.target.value;renderQueue();const input=$('#queue-search');input.focus();input.setSelectionRange(caret,caret);
    } else if(event.target.id==='timeline-search'){
      const caret=event.target.selectionStart;ui.timelineSearch=event.target.value;render();const input=$('#timeline-search');input.focus();input.setSelectionRange(caret,caret);
    }
  });
  document.addEventListener('change',event=>{if(event.target.id==='record-type'){ui.recordType=event.target.value;render();$('#record-type').focus();}});
  document.addEventListener('keydown',event=>{
    const target=event.target;
    if(target.matches('[role="tab"]') && ['ArrowLeft','ArrowRight','Home','End'].includes(event.key)){
      event.preventDefault();let index=tabs.findIndex(tab=>tab.id===ui.tab);index=event.key==='Home'?0:event.key==='End'?tabs.length-1:(index+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;changeTab(tabs[index].id);$(`#tab-${ui.tab}`).focus();
    } else if(target.matches('g[data-action][role="button"]') && ['Enter',' '].includes(event.key)){event.preventDefault();target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}
    else if(event.key==='Escape' && ui.mobileQueue){event.preventDefault();setQueueOpen(false);}
  });
  $('#drawer-overlay').addEventListener('click',()=>setQueueOpen(false));
  $('#inspector').addEventListener('close',()=>{ui.inspectorView=null;ui.inspectorPayload=null;const target=ui.inspectorReturnFocus?.isConnected?ui.inspectorReturnFocus:$(`#tab-${ui.tab}`);ui.inspectorReturnFocus=null;target?.focus({preventScroll:true});});
  window.addEventListener('pagehide',pause);
  render();
})();
