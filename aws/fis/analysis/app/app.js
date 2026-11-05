(function () {
  'use strict';
  const fixtures = window.FISFixtures;
  const model = window.FISModel;
  if (!fixtures || !model || !fixtures.runs.length) {
    document.getElementById('view-panel').innerHTML = '<div class="empty-state"><strong>The mock data could not load.</strong>Keep index.html and the app folder together, then reload.</div>';
    return;
  }
  const runs = fixtures.runs;
  const terminal = new Set(['completed', 'stopped', 'failed', 'cancelled']);
  const actionTerminal = new Set([...terminal, 'skipped']);
  const $ = id => document.getElementById(id);
  const esc = value => String(value == null ? '' : value).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
  const epoch = value => value == null ? NaN : typeof value === 'number' ? (value < 1e12 ? value * 1000 : value) : Date.parse(value);
  const iso = value => new Date(value).toISOString();
  const title = value => String(value || 'unknown').replace(/[_-]/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  const prettify = value => String(value || '').replace(/([a-z])([A-Z])/g, '$1 $2').replace(/[_-]/g, ' ').replace(/^./, c => c.toUpperCase());
  const clock = value => !Number.isFinite(value) ? '—' : `${Math.floor(Math.max(0, value) / 60).toString().padStart(2,'0')}:${Math.floor(Math.max(0,value) % 60).toString().padStart(2,'0')}`;
  const time = value => Number.isFinite(epoch(value)) ? new Date(epoch(value)).toISOString().slice(11,19) : 'Not reported';
  const elapsed = value => !Number.isFinite(value) ? '—' : value < 60 ? `${Math.floor(value)}s` : `${Math.floor(value/60)}m ${Math.floor(value%60)}s`;
  const state = {runKey:runs[0].key, cursor:runs[0].initialCursorSeconds || 0, view:'overview', playing:false, speed:5, runFilter:'all', runQuery:'', timeline:'timeline', target:'all', resourceQuery:'', source:'all', evidenceQuery:'', diagram:'01_execution', stops:{}, lastStatus:null};
  let timer, toastTimer;
  const baseRun = () => runs.find(run => run.key === state.runKey) || runs[0];
  const clockOrigin = run => epoch(run._mock?.clockOrigin || run.experiment.startTime || run.experiment.creationTime);
  const dateAt = (run, offset) => iso(clockOrigin(run) + offset * 1000);
  const offsetAt = (run, date) => (epoch(date) - clockOrigin(run)) / 1000;
  const statusLabel = value => ({in_progress:'Evaluating',not_assessed:'Not assessed',not_configured:'Not configured',not_requested:'Not requested',not_generated:'Not generated',unknown:'Unknown',completed:'Completed',partial:'Partial'}[value] || title(value));
  const badge = (value, label) => `<span class="badge ${esc(value)}"><span class="status-dot" aria-hidden="true"></span>${esc(label || statusLabel(value))}</span>`;
  const sourceName = source => ({fis:'FIS API',fis_api:'FIS API',fis_log:'FIS logs',fis_logs:'FIS logs',eventbridge:'EventBridge',cloudwatch:'CloudWatch',cloudtrail:'CloudTrail',application:'App command',app:'App command',mock_control:'Mock control'}[source] || source || 'Unknown source');
  const empty = (heading, description) => `<div class="empty-state"><div class="empty-symbol" aria-hidden="true">◌</div><strong>${esc(heading)}</strong>${esc(description)}</div>`;
  const json = value => esc(JSON.stringify(value, null, 2));
  function snapshot() {
    const original = baseRun();
    const run = model.getRunAt(original, state.cursor);
    const override = state.stops[state.runKey];
    if (!override || state.cursor < override.at) return run;
    const done = state.cursor >= override.at + 30;
    run.experiment = JSON.parse(JSON.stringify(override.snapshot.experiment));
    run.experiment.state = {status:done ? 'stopped' : 'stopping',reason:done ? 'Mock operator stop completed after outstanding cleanup.' : 'Mock operator stop requested. Outstanding post actions are completing.'};
    run.experiment.endTime = done ? dateAt(original, override.at + 30) : null;
    for (const action of Object.values(run.experiment.actions || {})) {
      const current = action.state && action.state.status;
      if (actionTerminal.has(current)) continue;
      if (!action.startTime || current === 'pending') {
        action.state = {status:'cancelled',reason:'The mock experiment stopped before this action started.'};
        action.startTime = null; action.endTime = null;
      } else {
        action.state = {status:done ? 'stopped' : 'stopping',reason:done ? 'Mock post-action cleanup completed.' : 'Waiting for mock post-action cleanup.'};
        action.endTime = done ? dateAt(original, override.at + 30) : null;
      }
    }
    if (run.experiment.experimentReportConfiguration) run.experiment.experimentReport = {state:{status:'pending',reason:'The original report is not valid for this simulated interruption.'},s3Reports:[]};
    run.assessment = {status:'inconclusive',summary:'This intervention changes the scenario. No recovery conclusion is available.',rule:'New post-intervention telemetry is required.',evidence:[]};
    run.telemetry = JSON.parse(JSON.stringify(override.snapshot.telemetry || {}));
    run.telemetry.interrupted = true;
    run.resolvedTargets = JSON.parse(JSON.stringify(override.snapshot.resolvedTargets || []));
    run.resolution = JSON.parse(JSON.stringify(override.snapshot.resolution || {}));
    run.safety = JSON.parse(JSON.stringify(override.snapshot.safety || {}));
    run.evidence = [...(override.snapshot.evidence || []),{id:'mock-stop-request',source:'mock_control',type:'stop-requested',occurredAt:dateAt(original,override.at),observedAt:dateAt(original,override.at),message:'Operator requested a simulated stop. No AWS request was made.'}];
    if (done) run.evidence.push({id:'mock-stop-completed',source:'mock_control',type:'stop-completed',occurredAt:dateAt(original,override.at + 30),observedAt:dateAt(original,override.at + 30),message:'Mock cleanup completed. Experiment stopped; workload recovery remains unassessed.'});
    return run;
  }
  function toast(message) { $('toast').textContent = message; $('toast').classList.add('visible'); clearTimeout(toastTimer); toastTimer = setTimeout(() => $('toast').classList.remove('visible'),3500); }
  function setPlaying(value) {
    state.playing = value;
    clearInterval(timer);
    if (value) {
      if (state.cursor >= baseRun().durationSeconds) state.cursor = 0;
      timer = setInterval(() => { state.cursor = Math.min(baseRun().durationSeconds, state.cursor + state.speed); if (state.cursor >= baseRun().durationSeconds) setPlaying(false); render(); },1000);
    }
    updateReplay();
  }
  function chooseRun(key) {
    const run = runs.find(item => item.key === key); if (!run) return;
    setPlaying(false); state.runKey = key; state.cursor = run.initialCursorSeconds || 0; state.target='all';state.source='all';state.resourceQuery='';state.evidenceQuery='';state.lastStatus=null;
    if ($('action-dialog').open) $('action-dialog').close();
    render();
    $('state-announcement').textContent = `${run.label} selected.`;
  }
  function setView(view) { state.view = view; render(); }
  function renderRunList() {
    const listStatus = run => run.key===state.runKey ? snapshot().experiment.state.status : model.getRunAt(run,run.initialCursorSeconds || 0).experiment.state.status;
    const filtered = runs.filter(run => {
      const s = listStatus(run);
      const mode = state.runFilter === 'active' ? !terminal.has(s) : state.runFilter === 'final' ? terminal.has(s) : true;
      return mode && `${run.label} ${run.application} ${run.environment} ${s} ${run.experiment.id}`.toLowerCase().includes(state.runQuery.toLowerCase());
    });
    $('run-count').textContent = runs.length;
    $('run-list').innerHTML = filtered.map(run => {
      const status = listStatus(run);
      const preview = run.experiment.experimentOptions.actionsMode === 'skip-all';
      return `<button class="run-card ${state.runKey===run.key?'selected':''}" data-run="${esc(run.key)}" aria-current="${state.runKey===run.key?'true':'false'}"><span class="run-card-top"><span class="run-kind">${preview?'Target preview':esc(run.application || 'Experiment')}</span><span class="run-state-dot ${esc(status)}" aria-label="${esc(statusLabel(status))}"></span></span><span class="run-card-title">${esc(run.label)}</span><span class="run-card-sub">${esc(statusLabel(status))} <span aria-hidden="true">·</span> ${esc(run.environment || 'staging')}</span></button>`;
    }).join('') || '<div class="side-empty">No experiments match your filters.</div>';
  }
  function renderHeader(run, summary) {
    const exp = run.experiment; const region = exp.arn.split(':')[3] || 'eu-central-1';
    $('run-header').innerHTML = `<div class="run-title-row"><div><div class="eyebrow">Experiment ${summary.isPreview?'preview':'run'} <span aria-hidden="true">/</span> ${esc(run.application || 'Platform resilience')}</div><h1 class="run-title">${esc(run.label)}</h1><p class="run-description">${esc(run.description || (summary.isPreview?'Verify resource selection and configuration before a future fault injection.':'Observe execution, selected scope and workload response in one place.'))}</p></div><div class="header-actions"><button class="button button-subtle" data-action="export"><span aria-hidden="true">↓</span> Export snapshot</button><button class="button button-danger" data-action="stop" ${terminal.has(exp.state.status) || exp.state.status==='stopping' || summary.isPreview?'disabled':''}>Simulate stop</button></div></div><div class="meta-row">${badge(exp.state.status)}${summary.isPreview?badge('preview','Target preview'):''}<span class="meta-separator"></span><span class="meta-chip">◈ ${esc(title(run.environment || 'staging'))}</span><span>${esc(region)}</span><span class="meta-separator"></span><span class="mono">${esc(exp.id)}</span><button class="meta-copy" data-action="copy-id" title="Copy experiment ID" aria-label="Copy experiment ID">⧉</button><span class="meta-separator"></span><span>${esc(run.owner || 'Platform engineering')}</span></div>`;
    const error=exp.state.error;
    if (['failed','stopped','stopping'].includes(exp.state.status)) {
      const location=error?.location;
      const actionName=typeof location==='string'&&location.startsWith('actions.')?location.slice(8):null;
      const actionExists=actionName && Object.prototype.hasOwnProperty.call(exp.actions||{},actionName);
      $('run-header').innerHTML+=`<div class="execution-explanation ${esc(exp.state.status)}"><strong>Execution ${esc(exp.state.status)}</strong><p>${esc(exp.state.reason||'No reason reported.')}</p>${error?`<div class="error-facts">${error.code?`<span>Code <code>${esc(error.code)}</code></span>`:''}${error.accountId?`<span>Account <code>${esc(error.accountId)}</code></span>`:''}${location?`<span>Location ${actionExists?`<button class="text-link" data-detail="${esc(actionName)}">${esc(location)} →</button>`:`<code>${esc(location)}</code>`}</span>`:''}</div>`:''}</div>`;
    }
  }
  function updateReplay() {
    const base = baseRun();
    $('play-replay').innerHTML = state.playing ? '<span aria-hidden="true">Ⅱ</span> Pause replay' : '<span aria-hidden="true">▶</span> Play replay';
    $('play-replay').setAttribute('aria-label',state.playing?'Pause replay':'Play replay');
    $('replay-cursor').max = base.durationSeconds; $('replay-cursor').value = state.cursor;
    $('replay-cursor').setAttribute('aria-valuetext',`${clock(state.cursor)} of ${clock(base.durationSeconds)} replay time`);
    $('replay-elapsed').textContent = clock(state.cursor); $('replay-total').textContent = clock(base.durationSeconds);
    $('replay-asof').textContent = `As of ${time(dateAt(base,state.cursor))} UTC`;
  }
  function renderOutcomes(run, s) {
    const count = s.counts || {}; const status = run.experiment.state.status;
    const finished = Number.isFinite(s.terminalPercent) ? Math.round(s.terminalPercent) : null;
    const assessment = run.assessment || {status:'not_assessed'};
    const assessmentLabels = {in_progress:'Evaluating',passed:'Criterion met',failed:'Criterion failed',not_assessed:'Not assessed',inconclusive:'Inconclusive'};
    const report = run.experiment.experimentReport;
    const reportStatus = report && report.state ? report.state.status : null;
    const reportLabel = s.isPreview ? 'Not generated' : !run.experiment.experimentReportConfiguration ? 'Not configured' : reportStatus === 'completed' ? 'Report ready' : reportStatus === 'failed' ? 'Report failed' : reportStatus === 'cancelled' ? 'Report cancelled' : reportStatus === 'running' ? 'Generating report' : reportStatus === 'pending' ? 'Report pending' : 'Not observed';
    const segments = Object.entries(count).filter(([key])=>actionTerminal.has(key)).map(([key,value])=>`<span class="progress-segment ${esc(key)}" style="width:${s.totalActions?value/s.totalActions*100:0}%" title="${esc(value+' '+key)}"></span>`).join('');
    const active = (count.running||0)+(count.initiating||0)+(count.stopping||0);
    $('outcome-cards').innerHTML = `<article class="outcome-card"><div class="outcome-label">Execution <span class="outcome-icon" aria-hidden="true">◉</span></div><div class="outcome-value ${status==='failed'?'red':status==='stopped'||status==='stopping'?'amber':'teal'}">${esc(statusLabel(status))}</div><div class="outcome-caption">${esc(elapsed(s.elapsedSeconds))} elapsed ${active?`<span aria-hidden="true">·</span> ${active} active ${active===1?'step':'steps'}`:''}</div></article><article class="outcome-card"><div class="outcome-label">Steps finished <span class="outcome-icon" aria-hidden="true">☷</span></div><div class="outcome-value">${finished===null?'—':finished+'%'} <small>${s.terminalActions} / ${s.totalActions}</small></div><div class="progress-track" aria-label="${s.terminalActions} of ${s.totalActions} steps in terminal states">${segments}</div><div class="outcome-caption">${s.completedActions} completed${s.skippedActions?` · ${s.skippedActions} skipped`:''}${count.failed?` · ${count.failed} failed`:''}${count.stopped?` · ${count.stopped} stopped`:''}${count.cancelled?` · ${count.cancelled} cancelled`:''}</div></article><article class="outcome-card"><div class="outcome-label">Workload assessment <span class="outcome-icon" aria-hidden="true">⌁</span></div><div class="outcome-value ${assessment.status==='failed'?'red':assessment.status==='passed'?'teal':''}">${esc(assessmentLabels[assessment.status] || statusLabel(assessment.status))}</div><div class="outcome-caption">${s.isPreview?'No faults executed':assessment.status==='not_assessed'?'No evaluated workload evidence':'External telemetry · defined criterion'}</div></article><article class="outcome-card"><div class="outcome-label">Evidence / report <span class="outcome-icon" aria-hidden="true">▤</span></div><div class="outcome-value ${reportStatus==='failed'?'red':''}" style="font-size:19px">${esc(reportLabel)}</div><div class="outcome-caption">${(run.evidence||[]).length} observed records ${s.isPreview?'· preview mode':'· independent lifecycle'}</div></article>`;
  }
  function renderTabs(run, summary) {
    const tabs = [['overview','Overview'],['actions','Actions',summary.totalActions],['resources','Selected resources',summary.resourceCountComplete?summary.selectedResourceCount:'…'],['evidence','Evidence',(run.evidence||[]).length],['model','Data model']];
    $('view-tabs').innerHTML = tabs.map(([key,label,count])=>`<button id="tab-${key}" role="tab" aria-selected="${state.view===key}" aria-controls="view-panel" tabindex="${state.view===key?'0':'-1'}" class="view-tab ${state.view===key?'active':''}" data-view="${key}">${label}${count!==undefined?`<span class="tab-count">${esc(count)}</span>`:''}</button>`).join('');
    $('view-panel').setAttribute('aria-labelledby',`tab-${state.view}`);
    $('view-panel').removeAttribute('aria-label');
    const age = summary.freshnessSeconds;
    $('observation-freshness').innerHTML = `<span></span>${Number.isFinite(age)?`Observed ${Math.round(age)}s ago`:'Observation unavailable'} · replay clock`;
    $('observation-freshness').className = `freshness ${age>30?'stale':''}`;
  }
  function timelinePanel(run, rows) {
    const base=baseRun();const max=base.durationSeconds;
    let body='';
    if (state.timeline==='dependencies') {
      const unresolved = new Map(rows.map(row=>[row.actionName || row.name,row]));const levels=[];const seen=new Set();let guard=0;
      while(unresolved.size && guard++<rows.length+1) {
        const level=[...unresolved.values()].filter(row=>(row.dependencies||[]).every(dep=>seen.has(dep)));
        if(!level.length) { levels.push([...unresolved.values()]);break; }
        levels.push(level);level.forEach(row=>{const name=row.actionName||row.name;seen.add(name);unresolved.delete(name);});
      }
      body=`<div class="dep-graph">${levels.map(level=>`<div class="dep-layer">${level.map(row=>`<button class="dep-node" data-detail="${esc(row.actionName||row.name)}"><strong>${esc(prettify(row.actionName||row.name))}</strong>${badge(row.status)}<small>${(row.dependencies||[]).length?`After: ${esc(row.dependencies.join(', '))}`:'No predecessors'}</small></button>`).join('')}</div>`).join('')}</div>`;
    } else {
      body=`<div class="timeline-axis"><span>Action</span><div class="axis-ticks">${[0,.25,.5,.75,1].map(f=>`<span>${clock(max*f)}</span>`).join('')}</div><span>Status</span></div>${rows.map(row=>{
        const start=offsetAt(base,row.startTime);const end=row.endTime?offsetAt(base,row.endTime):state.cursor;
        const left=Math.max(0,Math.min(100,start/max*100));const width=Math.max(.7,Math.min(100-left,(end-start)/max*100));
        const bar=Number.isFinite(start)?`<span class="timeline-bar ${esc(row.status)}" style="left:${left}%;width:${width}%" title="${esc(elapsed(row.durationSeconds ?? row.elapsedSeconds))}"></span>`:`<span class="timeline-label-empty">${row.status==='skipped'?'Skipped':row.status==='cancelled'?'Never started':'Not started'}</span>`;
        return `<button class="timeline-row" data-detail="${esc(row.actionName||row.name)}" aria-label="Inspect ${esc(row.actionName||row.name)}, ${esc(row.status)}"><span class="timeline-label"><strong>${esc(prettify(row.actionName||row.name))}</strong><small>${esc(row.actionId)}</small></span><span class="timeline-track">${bar}<span class="timeline-cursor" style="left:${Math.min(100,state.cursor/max*100)}%"></span></span>${badge(row.status)}</button>`;
      }).join('')}`;
    }
    return `<article class="panel"><div class="panel-header"><div><h2>Action execution</h2><p>${rows.length} named steps · select a step to inspect its evidence</p></div><div class="segmented" role="group" aria-label="Action visualization"><button data-timeline="timeline" class="${state.timeline==='timeline'?'active':''}" aria-pressed="${state.timeline==='timeline'}">Timeline</button><button data-timeline="dependencies" class="${state.timeline==='dependencies'?'active':''}" aria-pressed="${state.timeline==='dependencies'}">Dependencies</button></div></div>${body}<div class="panel-footer"><div class="timeline-legend"><span class="legend-item"><span class="legend-swatch"></span>Completed</span><span class="legend-item"><span class="legend-swatch running"></span>Running</span><span class="legend-item"><span class="legend-swatch pending"></span>Pending</span></div><span>${state.timeline==='timeline'?'Observed intervals · replay offset':'Layers show dependencies, not timing'}</span></div></article>`;
  }
  function chartPanel(run) {
    const telemetry=run.telemetry||{};const points=telemetry.points||[];const assessment=run.assessment||{};
    const base=baseRun();const max=base.durationSeconds;const W=680,H=175,pad={l:42,r:16,t:14,b:29};
    const values=points.map(p=>Number(p.value)).filter(Number.isFinite);const threshold=typeof telemetry.threshold==='number'?telemetry.threshold:NaN;const baseline=typeof telemetry.baseline==='number'?telemetry.baseline:NaN;
    const ymax=Math.max(10, ...values, Number.isFinite(threshold)?threshold:0,Number.isFinite(baseline)?baseline:0)*1.22;
    const min=Math.min(0,...points.map(p=>p.offsetSeconds));
    const offsetLabel=n=>(n<0?'−':'')+clock(Math.abs(n));
    const x=n=>pad.l+(n-min)/(max-min)*(W-pad.l-pad.r),y=n=>H-pad.b-n/ymax*(H-pad.t-pad.b);
    const path=points.filter(p=>Number.isFinite(Number(p.value))).map((p,i)=>`${i?'L':'M'}${x(p.offsetSeconds).toFixed(1)},${y(p.value).toFixed(1)}`).join(' ');
    const last=points.length?points[points.length-1]:null;
    const grid=[0,.5,1].map(f=>`<line x1="${pad.l}" x2="${W-pad.r}" y1="${y(ymax*f)}" y2="${y(ymax*f)}" stroke="#edf2f4"/><text x="${pad.l-9}" y="${y(ymax*f)+3}" font-size="8" fill="#91a5ae" text-anchor="end">${Math.round(ymax*f)}</text>`).join('');
    const ticks=min<0?[min,0,max/3,max*2/3,max]:[0,max/4,max/2,max*3/4,max];
    const axis=ticks.map(n=>`<text x="${x(n)}" y="${H-7}" font-size="8" fill="#91a5ae" text-anchor="middle">${offsetLabel(n)}</text>`).join('');
    const th=Number.isFinite(threshold)?`<line x1="${pad.l}" x2="${W-pad.r}" y1="${y(threshold)}" y2="${y(threshold)}" stroke="#c97c82" stroke-dasharray="5 5" stroke-width="1"/>`:'';
    const bl=Number.isFinite(baseline)?`<line x1="${pad.l}" x2="${W-pad.r}" y1="${y(baseline)}" y2="${y(baseline)}" stroke="#b3c8ce" stroke-dasharray="3 4"/>`:'';
    const area=points.length?`${path} L${x(last.offsetSeconds)},${H-pad.b} L${x(points[0].offsetSeconds)},${H-pad.b} Z`:'';
    const marks=points.filter((p,i)=>i%Math.max(1,Math.floor(points.length/12))===0 || i===points.length-1).map(p=>`<circle class="metric-point" cx="${x(p.offsetSeconds)}" cy="${y(p.value)}" r="2.5" fill="#087f82" stroke="white" stroke-width="1" tabindex="0" role="img" aria-label="${offsetLabel(p.offsetSeconds)}: ${esc(p.value)} ${esc(telemetry.unit || '')}"><title>${offsetLabel(p.offsetSeconds)} · ${esc(p.value)} ${esc(telemetry.unit || '')}</title></circle>`).join('');
    const chart=points.length?`<svg class="metric-chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(telemetry.metricLabel || 'Workload metric')} through the replay observation time"><defs><linearGradient id="metric-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#70bcb0" stop-opacity=".24"/><stop offset="1" stop-color="#70bcb0" stop-opacity=".02"/></linearGradient></defs>${grid}${axis}${th}${bl}<path d="${area}" fill="url(#metric-fill)"/><path d="${path}" fill="none" stroke="#087f82" stroke-width="2" stroke-linejoin="round"/>${marks}<line x1="${x(state.cursor)}" x2="${x(state.cursor)}" y1="${pad.t}" y2="${H-pad.b}" stroke="#b5cdd0" stroke-dasharray="3 3"/></svg>`:empty('No workload observations yet',run.experiment.experimentOptions.actionsMode==='skip-all'?'A target preview does not execute faults or assess resilience.':'Move the replay forward to observe telemetry.');
    return `<article class="panel"><div class="panel-header"><div><h2>Workload response</h2><p>${esc(telemetry.metricLabel || 'Application telemetry')} · synthetic CloudWatch observations</p></div><div class="chart-summary"><span class="chart-value">${last?esc(Number(last.value).toFixed(Number(last.value)%1?1:0)):'—'} <small>${esc(telemetry.unit || '')}</small></span></div></div><div class="chart-container">${chart}</div><div class="chart-footnotes"><span class="chart-key"><span></span>Observed response</span><span class="chart-key threshold"><span></span>Criterion ${Number.isFinite(threshold)?esc(threshold)+' '+esc(telemetry.unit||''):''}</span><span class="chart-key baseline"><span></span>Baseline</span></div><div class="assessment-strip ${esc(assessment.status)}">${badge(assessment.status || 'not_assessed')}<p>${esc(telemetry.interrupted?'Telemetry after the simulated intervention is unavailable. Recovery is not assessed.':assessment.summary || 'Workload assessment requires explicit criteria and sufficient telemetry.')}</p></div></article>`;
  }
  function scopePanel(run,s) {
    const targets=Object.entries(run.experiment.targets||{});const resources=model.selectedResources(run);const member=run.resolvedTargets||[];
    return `<article class="panel"><div class="panel-header"><div><h2>Selected scope</h2><p>Resources resolved for this run</p></div><span class="outcome-icon" aria-hidden="true">◎</span></div><div class="panel-body"><div class="scope-number">${s.selectedResourceCount ?? s.observedResourceCount ?? '—'}<small>${s.resourceCountComplete?'unique resources':'observed · incomplete'}</small></div><div class="scope-sub">${s.membershipCount} ${s.resourceCountComplete?'':'observed '}memberships across ${targets.length} target selectors</div>${targets.slice(0,4).map(([name,t])=>`<div class="scope-target"><div><div class="target-name">${esc(name)}</div><div class="target-kind">${esc(t.resourceType.replace(/^aws:/,''))} · ${esc(t.selectionMode)}</div></div><span class="scope-target-count">${s.resourceCountComplete?member.filter(r=>r.targetName===name).length:'…'}</span></div>`).join('')}<div class="account-stack">${(run.accounts||[]).slice(0,3).map(a=>`<span class="account-chip" title="Configured target account"><span></span>${esc(a.accountId)}</span>`).join('')}</div><p class="small-note">Selection describes configured exposure. Fault effects need separate evidence.</p></div><div class="panel-footer"><span>${s.resourceCountComplete?'Resolution collection complete':'Resolution not yet complete'}</span><button class="text-link" data-view="resources">Inspect resources →</button></div></article>`;
  }
  function safetyPanel(run) {
    const exp=run.experiment;const report=exp.experimentReport;const preview=exp.experimentOptions.actionsMode==='skip-all';
    const conditions=exp.stopConditions||[];const alarms=conditions.filter(c=>c.source==='aws:cloudwatch:alarm');
    const rstate=report?.state?.status;const artifacts=report?.s3Reports||[];
    const reportStatus=preview?'not_generated':!exp.experimentReportConfiguration?'not_configured':rstate||'unknown';
    const reportReason=preview?'Target previews do not generate experiment reports.':!exp.experimentReportConfiguration?'No report configuration was supplied.':report?.state?.reason||'Report state has not yet been observed.';
    let alarm='Not observed';
    const safety=run.safety;
    if(safety && epoch(safety.observedAt)<=epoch(run.now))alarm=safety.alarmState || 'Not observed';
    const lever=safety?.lever && epoch(safety.lever.observedAt)<=epoch(run.now)?safety.lever:null;
    return `<article class="panel"><div class="panel-header"><div><h2>Safety & report</h2><p>Controls and evidence readiness</p></div><span class="outcome-icon" aria-hidden="true">◇</span></div><div class="panel-body"><dl class="kv-list"><div class="kv-row"><dt>Stop conditions</dt><dd>${alarms.length?alarms.length+' CloudWatch alarm'+(alarms.length>1?'s':''):'None configured'}</dd></div><div class="kv-row"><dt>Alarm observation</dt><dd>${esc(alarm)}</dd></div><div class="kv-row"><dt>Safety lever</dt><dd>${lever?esc(statusLabel(lever.status)):'Not observed'}</dd></div><div class="kv-row"><dt>Lever scope</dt><dd><span class="mono">${esc(lever?.accountId||exp.arn.split(':')[4])}</span><br>${esc(exp.arn.split(':')[3])} · orchestrator</dd></div><div class="kv-row"><dt>Log schema</dt><dd>${exp.logConfiguration?.logSchemaVersion?'v'+esc(exp.logConfiguration.logSchemaVersion):'Not configured'}</dd></div></dl><div class="report-box"><div class="report-title"><strong>Experiment report</strong>${badge(reportStatus,rstate==='completed'?'Ready':statusLabel(reportStatus))}</div><p>${esc(reportReason)}</p>${report?.state?.error?`<pre class="report-error">${json(report.state.error)}</pre>`:''}${artifacts.length?`<p>${artifacts.length} synthetic artifact reference${artifacts.length>1?'s':''}.</p><button class="text-link" data-action="artifacts" style="margin-top:7px">View artifact reference →</button>`:''}</div></div></article>`;
  }
  function evidencePanel(run) {
    const records=[...(run.evidence||[])].sort((a,b)=>epoch(b.observedAt)-epoch(a.observedAt)).slice(0,4);
    return `<article class="panel feed-panel"><div class="panel-header"><div><h2>Recent evidence</h2><p>Observed by the replay clock</p></div><span class="count-bubble">${(run.evidence||[]).length}</span></div><div class="feed-list">${records.map(event=>`<div class="feed-row"><span class="feed-dot ${/error|fail/.test(event.type)?'error':/action/.test(event.type)?'action':''}"></span><div class="feed-body"><div class="feed-meta"><span class="feed-source">${esc(sourceName(event.source))}</span><span class="feed-time">${time(event.occurredAt)}</span></div><p>${esc(event.message)}</p></div></div>`).join('') || empty('No evidence yet','Advance the replay to collect observations.')}</div><div class="panel-footer"><span>Occurrence times shown · UTC</span><button class="text-link" data-view="evidence">All evidence →</button></div></article>`;
  }
  function actionTable(run,rows) {
    return `<article class="panel wide-panel"><div class="panel-header"><div><h2>Named action executions</h2><p>Each row is identified by experiment + action name, even when catalog types repeat.</p></div><button class="button button-subtle" data-action="export">↓ Export snapshot</button></div><div class="table-scroll"><table class="data-table"><thead><tr><th>Action / catalog capability</th><th>State</th><th>Start / end UTC</th><th>Elapsed</th><th>Predecessors</th><th>Selected scope</th></tr></thead><tbody>${rows.map(row=>`<tr><td><button class="row-link" data-detail="${esc(row.actionName||row.name)}"><div class="cell-title">${esc(row.actionName||row.name)}</div><div class="cell-sub mono">${esc(row.actionId)}</div></button></td><td>${badge(row.status)}</td><td>${time(row.startTime)}<div class="cell-sub">${row.endTime?time(row.endTime):actionTerminal.has(row.status)?'End not reported':'—'}</div></td><td>${esc(elapsed(row.durationSeconds??row.elapsedSeconds))}</td><td>${(row.dependencies||[]).map(name=>`<button class="text-link" data-detail="${esc(name)}">${esc(name)}</button>`).join('<br>')||'<span class="cell-sub">None</span>'}</td><td>${row.selectedResourceCount==null?'Unknown':row.selectedResourceCount} resources<div class="cell-sub">${Object.entries(row.targets||{}).map(([slot,target])=>esc(slot+' → '+target)).join('<br>')||'No resource target'}</div></td></tr>`).join('')}</tbody></table></div><div class="panel-footer">Input parameters remain strings. Initiation or completion does not supply an individual fault result for every selected resource.</div></article>${timelinePanel(run,rows)}`;
  }
  function resourceView(run,s) {
    const resources=model.selectedResources(run);const targets=Object.entries(run.experiment.targets||{});
    const filtered=resources.filter(r=>{
      const names=r.targetNames||[r.targetName];
      return(state.target==='all'||names.includes(state.target)) && JSON.stringify(r).toLowerCase().includes(state.resourceQuery.toLowerCase());
    });
    const rows=filtered.map(r=>{
      const raw=r.targetInformation||r.raw?.targetInformation||r.raw||{};
      const arn=r.arn||raw.arn||raw.resourceArn||'';
      const name=r.label||r.name||r.resourceId||r.id||arn.split('/').pop()||raw.pod_name||'Unnormalized identity';
      const account=r.accountId||raw.accountId||raw.account_id||(arn.split(':')[4])||'Unknown';
      const type=r.resourceType||r.type||'Unknown';
      return `<tr><td><div class="cell-title mono">${esc(name)}</div><div class="cell-sub mono">${esc(arn || JSON.stringify(raw))}</div></td><td>${esc(type.replace(/^aws:/,''))}</td><td class="mono">${esc(account)}</td><td>${(r.targetNames||[r.targetName]).filter(Boolean).map(n=>`<span class="type-chip">${esc(n)}</span>`).join('')}</td><td>${(r.actionNames||[]).map(n=>`<button class="text-link" data-detail="${esc(n)}">${esc(n)}</button>`).join('<br>')||'—'}</td></tr>`;
    }).join('');
    return `<article class="panel wide-panel"><div class="panel-header"><div><h2>Selected resources</h2><p>Resource identities are deduplicated; each target membership is preserved.</p></div>${badge(s.resourceCountComplete?'completed':'pending',s.resourceCountComplete?'Collection complete':'Incomplete collection')}</div><div class="scope-metrics"><div class="scope-metric"><strong>${s.selectedResourceCount??s.observedResourceCount??'—'}</strong><span>${s.resourceCountComplete?'Unique identified resources':'Observed identities · incomplete'}</span></div><div class="scope-metric"><strong>${s.membershipCount}</strong><span>${s.resourceCountComplete?'Target memberships':'Observed memberships · incomplete'}</span></div><div class="scope-metric"><strong>${targets.length}</strong><span>Named selectors</span></div><div class="scope-metric"><strong>${s.observedAccountCount??'—'}</strong><span>Accounts with resolved resources</span></div></div><div class="resource-tabs"><button class="resource-filter ${state.target==='all'?'active':''}" data-target="all">All selectors</button>${targets.map(([name])=>`<button class="resource-filter ${state.target===name?'active':''}" data-target="${esc(name)}">${esc(name)}</button>`).join('')}</div><div class="toolbar"><label class="search-grow"><span class="sr-only">Filter resources</span><input id="resource-search" type="search" placeholder="Filter by resource, account or action…" value="${esc(state.resourceQuery)}"></label><span class="toolbar-count">${filtered.length} observed identities</span></div>${rows?`<div class="table-scroll"><table class="data-table"><thead><tr><th>Resource identity</th><th>Resource type</th><th>Account</th><th>Target memberships</th><th>Bound actions</th></tr></thead><tbody>${rows}</tbody></table></div>`:empty(s.resourceCountComplete?'No matching resources':'Resources not yet available',s.resourceCountComplete?'Change the selector or search filter.':'Target resolution or collection is incomplete. This is not a confirmed zero.') }<div class="panel-footer">Selected resources describe membership. This view makes no per-resource success or recovery claim.</div></article><div class="details-grid">${targets.map(([name,t])=>`<article class="panel"><h3>${esc(name)}</h3><p class="small-note">Selector snapshot · ${esc(t.resourceType)}</p><pre class="config-code">${json(t)}</pre></article>`).join('')}</div>`;
  }
  function evidenceView(run) {
    const sources=[...new Set((baseRun().evidence||[]).map(e=>e.source))];if(state.stops[state.runKey])sources.push('mock_control');
    const filtered=(run.evidence||[]).filter(e=>(state.source==='all'||e.source===state.source) && JSON.stringify(e).toLowerCase().includes(state.evidenceQuery.toLowerCase())).sort((a,b)=>epoch(b.observedAt)-epoch(a.observedAt));
    return `<article class="panel"><div class="panel-header"><div><h2>Execution evidence</h2><p>Occurrence and observation timestamps are separate. All records are synthetic.</p></div><button class="button button-subtle" data-action="export">↓ Export snapshot</button></div><div class="toolbar"><label>Source <select id="evidence-source"><option value="all">All sources</option>${sources.map(source=>`<option value="${esc(source)}" ${state.source===source?'selected':''}>${esc(sourceName(source))}</option>`).join('')}</select></label><label class="search-grow"><span class="sr-only">Search evidence</span><input id="evidence-search" type="search" value="${esc(state.evidenceQuery)}" placeholder="Find action, account or message…"></label><span class="toolbar-count">${filtered.length} observed records</span></div>${filtered.map(event=>`<div class="audit-row"><div class="audit-row-time">${time(event.occurredAt)}<small>Occurred · UTC</small><small>Seen ${time(event.observedAt)}</small></div><div><span class="source-badge">${esc(sourceName(event.source))}</span></div><div class="audit-row-main"><p>${esc(event.message)}</p><code>${esc(event.type)}</code>${event.actionName?` <span class="footer-dot">·</span> <button class="text-link" data-detail="${esc(event.actionName)}">${esc(event.actionName)}</button>`:''}${event.accountId?` <span class="footer-dot">·</span> <code>${esc(event.accountId)}</code>`:''}</div></div>`).join('')||empty('No matching evidence','Change the source or text filter, or advance the replay.')}<div class="panel-footer">Records become visible at observation time. Absence of an error record is not evidence of per-account success.</div></article>`;
  }
  const diagrams=[['01_execution','Execution model'],['02_catalog_templates','Templates & catalog'],['03_targeting','Selected scope'],['04_evidence_reports','Evidence & reports'],['05_assessments','Workload assessment']];
  function modelView() {
    const entities=[
      ['ExperimentRun','AWS runtime aggregate','One run owns its configuration snapshot, current status and execution times.','experimentKey = scoped ID or ARN',false],
      ['ActionExecution','AWS nested run step','Named execution of a catalog capability. Same actionId can appear more than once.','experimentKey + actionName',false],
      ['ActionDependency','Application normalization','Each edge connects predecessor and successor names within the same run.','experimentKey + predecessor + successor',true],
      ['TargetSelection','AWS selector snapshot','Configured rules select resources once for the run. Slot bindings retain target names.','experimentKey + targetName',false],
      ['ResolvedTargetMembership','AWS data / normalized relation','Preserves target membership and generic identity maps, with optional canonical resource identity.','membershipKey + raw targetInformation',false],
      ['ResilienceAssessment','Application evaluation','A versioned criterion and workload evidence produce a verdict independently of FIS status.','assessmentKey + criterionRevision',true]
    ];
    return `<div class="model-intro"><div><div class="eyebrow">Reviewed logical model</div><h2>From AWS facts to operator understanding</h2><p>The demo preserves identity, scope and evidence boundaries from the analysis.</p></div><a class="button button-teal" href="aws_fis_experiment_action_model.pdf" target="_blank" rel="noopener">Read reviewed report ↗</a></div><div class="model-grid">${entities.map(([name,kind,desc,key,app])=>`<article class="entity-card ${app?'application':''}"><div class="entity-kind">${esc(kind)}</div><h3>${name}</h3><p>${esc(desc)}</p><div class="entity-key">${esc(key)}</div></article>`).join('')}</div><div class="relationship-note"><span aria-hidden="true">↳</span><span>Catalog type → named template step → named run execution. The run keeps its own configuration when a template changes.</span></div><article class="panel"><div class="panel-header"><div><h2>Entity relationship diagrams</h2><p>Five complementary views of the reviewed model</p></div><div class="diagram-actions"><a class="text-link" href="diagrams/${esc(state.diagram)}.svg" target="_blank" rel="noopener">Open full size ↗</a><a class="text-link" href="diagrams/${esc(state.diagram)}.mmd">Mermaid source ↗</a></div></div><div class="resource-tabs">${diagrams.map(([id,label])=>`<button class="resource-filter ${state.diagram===id?'active':''}" data-diagram="${id}">${label}</button>`).join('')}</div><div class="diagram-viewport" tabindex="0" aria-label="Scrollable entity relationship diagram"><img src="diagrams/${esc(state.diagram)}.svg" alt="${esc(diagrams.find(d=>d[0]===state.diagram)[1])} entity relationship diagram"></div></article><div class="model-relationships"><article class="panel"><h3>What can be derived</h3><div class="relation-row">Observed execution timing<span>AWS timestamps</span></div><div class="relation-row">Steps finished and outcomes<span>Complete action map</span></div><div class="relation-row">Selected scope and overlap<span>Resolved memberships</span></div><div class="relation-row">Workload change and recovery<span>External telemetry + rules</span></div></article><article class="panel"><h3>What remains explicit</h3><div class="relation-row">Unknown or missing values<span>Never coerced to zero</span></div><div class="relation-row">Source and observation time<span>Evidence provenance</span></div><div class="relation-row">Report readiness<span>Independent lifecycle</span></div><div class="relation-row">Action/resource effect<span>Needs specific evidence</span></div></article></div><p class="small-note">All workloads, accounts, resources and evidence shown in this application are synthetic. Model sources: <a href="report.md">reviewed report</a> · <a href="REVIEW.md">review record</a> · <a href="sources.json">official AWS source register</a>.</p>`;
  }
  function renderPanel(run,summary,rows) {
    if(state.view==='actions')return actionTable(run,rows);
    if(state.view==='resources')return resourceView(run,summary);
    if(state.view==='evidence')return evidenceView(run);
    if(state.view==='model')return modelView();
    return `<div class="overview-layout"><div class="overview-main">${timelinePanel(run,rows)}${chartPanel(run)}</div><div class="overview-side">${scopePanel(run,summary)}${safetyPanel(run)}${evidencePanel(run)}</div></div>`;
  }
  function render() {
    const active=document.activeElement;const activeId=active?.id;const selection=active && (active.tagName==='INPUT') ? [active.selectionStart,active.selectionEnd] : null;
    const focusAttribute=['data-run','data-action','data-detail','data-target','data-timeline','data-diagram','data-action-evidence'].find(name=>active?.hasAttribute(name));
    const focusScope=active?.parentElement?.closest('[id]')?.id;
    const focusSelector=focusAttribute?`[${focusAttribute}="${CSS.escape(active.getAttribute(focusAttribute))}"]`:null;
    const focusIndex=focusScope&&focusSelector?[...$(focusScope).querySelectorAll(focusSelector)].indexOf(active):0;
    const run=snapshot();const summary=model.summarize(run);const rows=model.actionRows(run);
    renderRunList();renderHeader(run,summary);updateReplay();renderOutcomes(run,summary);renderTabs(run,summary);$('view-panel').innerHTML=renderPanel(run,summary,rows);
    if(state.lastStatus!==run.experiment.state.status){if(state.lastStatus!==null)$('state-announcement').textContent=`${run.label}: ${statusLabel(run.experiment.state.status)}.`;state.lastStatus=run.experiment.state.status;}
    if($('action-dialog').open && $('action-dialog').dataset.action)renderActionDialog($('action-dialog').dataset.action);
    const restore=activeId?$(activeId):focusScope&&focusSelector?$(focusScope)?.querySelectorAll(focusSelector)[Math.max(0,focusIndex)]:null;
    if(restore && restore!==document.activeElement) { restore.focus({preventScroll:true});if(selection && restore.type!=='range')try{restore.setSelectionRange(...selection);}catch(_){} }
  }
  function renderActionDialog(name) {
    const run=snapshot();const rows=model.actionRows(run);const row=rows.find(r=>(r.actionName||r.name)===name);if(!row)return;
    const action=run.experiment.actions[name];const successors=rows.filter(r=>(r.dependencies||[]).includes(name));const resources=model.selectedResources(run,name);
    $('action-dialog-content').innerHTML=`<div class="dialog-header"><div class="dialog-heading"><span class="dialog-eyebrow">Action execution · named run step</span><button class="icon-button" data-action="close-detail" aria-label="Close action details">×</button></div><h2 id="action-dialog-title">${esc(prettify(name))}</h2><div class="dialog-type">${esc(action.actionId)} <span class="footer-dot">·</span> ${esc(name)}</div></div><div class="dialog-content"><div class="dialog-status">${badge(row.status)}<p>${esc(action.state?.reason||'No reason reported.')}</p></div><div class="dialog-columns"><div><section class="dialog-section"><h3>Execution facts</h3><dl class="kv-list"><div class="kv-row"><dt>Started</dt><dd>${time(row.startTime)}${row.startTime?' UTC':''}</dd></div><div class="kv-row"><dt>Ended</dt><dd>${time(row.endTime)}${row.endTime?' UTC':''}</dd></div><div class="kv-row"><dt>Elapsed / duration</dt><dd>${elapsed(row.durationSeconds??row.elapsedSeconds)}</dd></div><div class="kv-row"><dt>Selected resources</dt><dd>${row.selectedResourceCount??'Unknown'}</dd></div></dl></section><section class="dialog-section"><h3>Input parameters</h3><pre class="config-code">${json(action.parameters||{})}</pre></section></div><div><section class="dialog-section"><h3>Predecessors</h3><div class="dependency-chips">${(row.dependencies||[]).map(n=>`<button data-detail="${esc(n)}">${esc(n)}</button>`).join('')||'<span class="small-note">None</span>'}</div></section><section class="dialog-section"><h3>Successors</h3><div class="dependency-chips">${successors.map(r=>`<button data-detail="${esc(r.actionName||r.name)}">${esc(r.actionName||r.name)}</button>`).join('')||'<span class="small-note">None</span>'}</div></section><section class="dialog-section"><h3>Target-slot bindings</h3><pre class="config-code">${json(action.targets||{})}</pre></section></div></div><section class="dialog-section"><h3>Selected membership</h3>${resources.length?resources.slice(0,8).map(r=>{const raw=r.targetInformation||r.raw?.targetInformation||r.raw||{};return`<div class="detail-resource"><span class="mono">${esc(r.label||r.resourceId||r.id||r.arn||raw.arn||JSON.stringify(raw))}</span><code>${esc((r.targetNames||[]).join(', '))}</code></div>`;}).join(''):'<p class="small-note">No resolved resource identities are available for this step at the replay time.</p>'}<p class="small-note">This is selected scope. The generic FIS action response has no per-resource result.</p></section></div><div class="dialog-actions"><button class="button button-teal" data-action-evidence="${esc(name)}">Related evidence →</button><button class="button button-subtle" data-action="close-detail">Close</button></div>`;
  }
  function openDetail(name) { setPlaying(false); const dialog=$('action-dialog');dialog.dataset.action=name;renderActionDialog(name);if(!dialog.open)dialog.showModal(); }
  function openArtifacts() { setPlaying(false); const run=snapshot();const dialog=$('action-dialog');delete dialog.dataset.action;$('action-dialog-content').innerHTML=`<div class="dialog-header"><div class="dialog-heading"><span class="dialog-eyebrow">Independent report lifecycle</span><button class="icon-button" data-action="close-detail" aria-label="Close report details">×</button></div><h2 id="action-dialog-title">Report artifact references</h2></div><div class="dialog-content"><p class="small-note">These fictional S3 ARNs demonstrate the returned report model. They do not identify downloadable AWS objects.</p><pre class="config-code">${json(run.experiment.experimentReport)}</pre><h3>Report configuration snapshot</h3><pre class="config-code">${json(run.experiment.experimentReportConfiguration)}</pre></div><div class="dialog-actions"><button class="button button-subtle" data-action="close-detail">Close</button></div>`;dialog.showModal(); }
  function exportSnapshot() { const run=snapshot();const packet=model.exportSnapshot(run);const url=URL.createObjectURL(new Blob([JSON.stringify(packet,null,2)],{type:'application/json'}));const link=document.createElement('a');link.href=url;link.download=`fis-${run.key}-${Math.floor(state.cursor)}s.json`;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Synthetic snapshot exported with provenance and derived values.'); }
  document.addEventListener('click', async event=>{
    const control=event.target.closest('button,a');if(!control)return;
    if(control.classList.contains('brand')){event.preventDefault();chooseRun(runs[0].key);setView('overview');return;}
    if(control.dataset.run){chooseRun(control.dataset.run);return;}
    if(control.dataset.runFilter){state.runFilter=control.dataset.runFilter;document.querySelectorAll('[data-run-filter]').forEach(b=>{b.classList.toggle('active',b.dataset.runFilter===state.runFilter);b.setAttribute('aria-pressed',b.dataset.runFilter===state.runFilter);});renderRunList();return;}
    if(control.dataset.view){setView(control.dataset.view);return;}
    if(control.dataset.timeline){state.timeline=control.dataset.timeline;render();return;}
    if(control.dataset.detail){openDetail(control.dataset.detail);return;}
    if(control.dataset.target){state.target=control.dataset.target;render();return;}
    if(control.dataset.diagram){state.diagram=control.dataset.diagram;render();return;}
    if(control.dataset.actionEvidence){state.evidenceQuery=control.dataset.actionEvidence;state.source='all';$('action-dialog').close();setView('evidence');return;}
    switch(control.dataset.action){
      case 'export':exportSnapshot();break;
      case 'stop':setPlaying(false);$('stop-dialog').showModal();break;
      case 'close-detail':$('action-dialog').close();break;
      case 'artifacts':openArtifacts();break;
      case 'copy-id':try{await navigator.clipboard.writeText(baseRun().experiment.id);toast('Experiment ID copied.');}catch(_){toast(`Experiment ID: ${baseRun().experiment.id}`);}break;
    }
  });
  $('run-search').addEventListener('input',event=>{state.runQuery=event.target.value;renderRunList();});
  $('play-replay').addEventListener('click',()=>{setPlaying(!state.playing);render();});
  $('replay-cursor').addEventListener('input',event=>{state.cursor=Number(event.target.value);render();});
  $('replay-speed').addEventListener('change',event=>{state.speed=Number(event.target.value);});
  $('advance-replay').addEventListener('click',()=>{state.cursor=Math.min(baseRun().durationSeconds,state.cursor+30);render();});
  $('reset-replay').addEventListener('click',()=>{setPlaying(false);state.cursor=0;delete state.stops[state.runKey];render();toast('Replay reset. Simulated interventions cleared.');});
  $('model-shortcut').addEventListener('click',()=>setView('model'));
  $('confirm-stop').addEventListener('click',()=>{const run=snapshot();if(!terminal.has(run.experiment.state.status)){state.stops[state.runKey]={at:state.cursor,snapshot:JSON.parse(JSON.stringify(run))};}$('stop-dialog').close();render();toast('Mock stop requested. Advance 30 seconds to observe cleanup completion.');});
  $('view-panel').addEventListener('input',event=>{if(event.target.id==='resource-search'){state.resourceQuery=event.target.value;render();}if(event.target.id==='evidence-search'){state.evidenceQuery=event.target.value;render();}});
  $('view-panel').addEventListener('change',event=>{if(event.target.id==='evidence-source'){state.source=event.target.value;render();}});
  $('view-tabs').addEventListener('keydown',event=>{if(!['ArrowRight','ArrowLeft','Home','End'].includes(event.key))return;event.preventDefault();const tabs=[...$('view-tabs').querySelectorAll('[role=tab]')];let i=tabs.findIndex(t=>t.getAttribute('aria-selected')==='true');i=event.key==='Home'?0:event.key==='End'?tabs.length-1:(i+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length;setView(tabs[i].dataset.view);$('tab-'+state.view).focus();});
  for(const id of ['action-dialog','stop-dialog'])$(id).addEventListener('click',event=>{if(event.target!==$(id))return;const rect=$(id).getBoundingClientRect();if(event.clientX<rect.left||event.clientX>rect.right||event.clientY<rect.top||event.clientY>rect.bottom)$(id).close();});
  render();
})();
