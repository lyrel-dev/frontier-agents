/* Browser presentation only. All assessment semantics live in model.js. */
(function () {
  'use strict';

  const M = window.AssessmentModel;
  const F = window.AssessmentFixtures;
  const $ = (id) => document.getElementById(id);
  if (!M || !F || !Array.isArray(F.runs) || !F.runs.length) {
    $('view-panel').innerHTML = '<div class="empty-state"><strong>The local dataset could not be loaded.</strong>Keep index.html and the app directory together, then reload this page.</div>';
    return;
  }

  const svg = (body) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${body}</svg>`;
  const icons = {
    execution: svg('<path d="M8 4h8l4 8-4 8H8l-4-8Z"/><path d="m10 8 6 4-6 4Z"/>'),
    assessment: svg('<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6Z"/><path d="m8 12 3 3 5-6"/>'),
    cleanup: svg('<path d="M20 7v5h-5M4 17v-5h5"/><path d="M6 7a7 7 0 0 1 12-1l2 3M4 15l2 3a7 7 0 0 0 12-1"/>'),
    lock: svg('<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>'),
    info: svg('<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7h.01"/>'),
    warning: svg('<path d="m12 3 10 18H2Z"/><path d="M12 9v5M12 17h.01"/>'),
    export: svg('<path d="M12 3v12m-4-4 4 4 4-4M5 16v5h14v-5"/>'),
    copy: svg('<rect x="8" y="8" width="12" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>'),
    branch: svg('<circle cx="6" cy="5" r="2"/><circle cx="6" cy="19" r="2"/><circle cx="18" cy="5" r="2"/><path d="M6 7v10M18 7v2a6 6 0 0 1-6 6H6"/>')
  };

  const state = {
    selected: F.runs[0].key,
    cursors: Object.fromEntries(F.runs.map((r) => [r.key, r.initialCursorSeconds || 0])),
    interventions: {}, tab: 'overview', runFilter: 'all', runSearch: '',
    workflowView: 'graph', evidenceQuery: '', evidenceSource: 'all', evidenceStep: '',
    stepQuery: '', stepFilter: 'all', playing: false, speed: 5,
    detailData: null, returnFocus: null, toastTimer: null, lastTick: 0
  };

  const esc = (value) => String(value == null ? '' : value).replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const human = (value) => String(value || 'unknown').replace(/[_-]/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
  const json = (value) => JSON.stringify(value === undefined ? null : value, null, 2);
  const short = (value, limit = 75) => {
    if (value === null || value === undefined) return 'Not observed';
    if (typeof value === 'boolean') return value ? 'True' : 'False';
    if (typeof value === 'string' || typeof value === 'number') {
      const s = String(value);
      return s.length > limit ? s.slice(0, limit - 1) + '…' : s;
    }
    const s = JSON.stringify(value);
    return s.length > limit ? s.slice(0, limit - 1) + '…' : s;
  };
  const statusOf = (value) => typeof value === 'string' ? value : value && (value.status || value.state || value.verdict) || 'unknown';
  const tone = (value) => {
    if (['succeeded','passed','complete','completed','terminal','adequate','sufficient','recovered'].includes(value)) return 'green';
    if (['running','collecting','finalizing','active','in_progress'].includes(value)) return 'teal';
    if (['failed','error','timed_out'].includes(value)) return 'red';
    if (['inconclusive','indeterminate','incomplete','unknown','partial','blocked','insufficient','cancelled'].includes(value)) return 'amber';
    if (['queued','pending'].includes(value)) return 'blue';
    return '';
  };
  const badge = (label, value = label, extra = '') => `<span class="badge ${tone(value)} ${extra}"><i aria-hidden="true"></i>${esc(label)}</span>`;
  const statusBadge = (value) => badge(human(value), value);
  const mark = (value) => `<span class="step-mark ${tone(value)} ${value === 'running' ? 'running' : ''}" aria-hidden="true">${value === 'running' ? '' : ['succeeded','passed'].includes(value) ? '✓' : ['failed','timed_out'].includes(value) ? '×' : ['skipped','cancelled'].includes(value) ? '−' : value === 'blocked' ? '!' : '·'}</span>`;
  const time = (value, date = false) => {
    if (!value) return 'Not observed';
    const d = new Date(value);
    if (!Number.isFinite(d.getTime())) return String(value);
    return date ? d.toISOString().replace('T', ' ').slice(0,19) + ' UTC' : d.toISOString().slice(11,19) + ' UTC';
  };
  const elapsed = (seconds) => {
    if (seconds == null || !Number.isFinite(Number(seconds))) return '—';
    const n = Math.max(0, Math.floor(Number(seconds)));
    return `${String(Math.floor(n / 60)).padStart(2,'0')}:${String(n % 60).padStart(2,'0')}`;
  };
  const age = (seconds) => seconds == null ? 'unknown' : seconds < 60 ? `${Math.floor(seconds)}s` : `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  const duration = (start, end, now) => start ? elapsed((new Date(end || now) - new Date(start)) / 1000) : '—';
  const refList = (refs) => Array.isArray(refs) ? refs.map((r) => typeof r === 'string' ? r : r.stepKey || r.key || r.step).filter(Boolean) : refs ? [String(refs)] : [];
  const outcome = (step) => step.outcome || step.phase;
  const codeBlock = (value) => `<pre class="code-block wrap"><code>${esc(typeof value === 'string' ? value : json(value))}</code></pre>`;
  const properties = (rows, className = 'detail-properties') => `<dl class="${className}">${rows.map(([label, value]) => `<div class="context-row"><dt>${esc(label)}</dt><dd>${value}</dd></div>`).join('')}</dl>`;
  const empty = (title, message, small = false) => `<div class="empty-state${small ? ' small' : ''}"><strong>${esc(title)}</strong>${esc(message)}</div>`;
  const fixture = () => F.runs.find((r) => r.key === state.selected);
  function projection(key = state.selected) {
    const run = F.runs.find((r) => r.key === key);
    const snapshot = M.projectRun(run, state.cursors[key]);
    return state.interventions[key] ? M.applyCancellation(snapshot, state.interventions[key]) : snapshot;
  }
  function getSummary(s) {
    return M.summarize(s);
  }
  function criterionFor(s, key) { return (s.criteria || []).concat(s.preconditions || []).find((c) => c.stepKey === key); }
  function operationName(uses) { return String(uses || '').replace(/@[^@]+$/, ''); }

  function renderRail() {
    const q = state.runSearch.trim().toLowerCase();
    const runs = F.runs.map((r) => ({ fixture: r, snapshot: projection(r.key) })).filter(({fixture: r, snapshot: s}) => {
      const active = s.execution.phase !== 'finished';
      return (state.runFilter === 'all' || (state.runFilter === 'active' ? active : !active)) && (!q || `${r.title} ${r.runId} ${r.service} ${r.environment} ${r.description}`.toLowerCase().includes(q));
    });
    $('run-count').textContent = `${runs.length}/${F.runs.length}`;
    document.querySelectorAll('[data-run-filter]').forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.runFilter === state.runFilter)));
    $('run-list').innerHTML = runs.length ? runs.map(({fixture: r, snapshot: s}) => {
      const status = s.execution.phase === 'finished' ? s.assessment.verdict : s.execution.phase;
      return `<li><button type="button" class="run-card" data-select-run="${esc(r.key)}" aria-current="${r.key === state.selected}" aria-label="Open ${esc(r.title)}"><span class="run-card-top"><span class="run-card-service">${esc(r.service)}</span><span class="status-dot ${tone(status)}" aria-hidden="true"></span></span><strong class="run-card-title">${esc(r.title)}</strong><span class="run-card-meta"><span>${esc(human(status))}</span><span class="dot-separator">·</span><span>${esc(r.environment)}</span></span></button></li>`;
    }).join('') : '<li class="rail-empty">No runs match this search.</li>';
  }

  function renderHeader(s, summary) {
    $('breadcrumb-service').textContent = s.service;
    $('run-header').innerHTML = `<div class="header-title-row"><div><div class="eyebrow">Assessment run <span aria-hidden="true">/</span> ${esc(s.environment)}</div><h1>${esc(s.title)}</h1><p class="run-description">${esc(s.description)}</p></div><div class="header-actions"><button id="export-snapshot" type="button" class="button button-quiet" data-export>${icons.export}Export snapshot</button><button id="cancel-run" type="button" class="button button-danger" data-cancel-run ${!summary.canCancel || state.interventions[s.key] ? 'disabled' : ''}>${state.interventions[s.key] ? (s.simulation ? 'Cancellation simulated' : 'Cancellation saved') : 'Simulate cancel'}</button></div></div><div class="metadata-row"><span class="meta-chip">${esc(s.service)}</span><span class="meta-chip">${esc(s.region)}</span><span>${esc((s.accounts || []).length)} account${(s.accounts || []).length === 1 ? '' : 's'}</span><span class="metadata-separator" aria-hidden="true"></span><button type="button" class="copy-id mono" data-copy-run aria-label="Copy run identifier">${esc(s.runId)} ${icons.copy}</button><span class="metadata-separator" aria-hidden="true"></span><button type="button" class="text-button" data-tab="definition">Revision ${esc(s.revision.version)} · pinned ${icons.lock.replace('<svg ', '<svg style="display:inline;width:10px;height:10px;vertical-align:-1px" ')}</button></div>`;

    const hasProtectiveHold = Boolean(s.finalization.protectiveHold);
    let notice = '';
    if (state.interventions[s.key] && !s.simulation) {
      notice = `<div class="notice-banner blue"><span class="icon">${icons.info}</span><div><strong>Viewing history before the saved cancellation</strong><p>The local intervention begins at ${esc(time(state.interventions[s.key].acceptedAt))}. Earlier replay observations remain unchanged. Reset clears the intervention.</p></div></div>`;
    } else if (s.simulation) {
      notice = `<div class="notice-banner"><span class="icon">${icons.warning}</span><div><strong>Cancellation requested in this local replay</strong><p>Main dispatch is stopped in the simulation. Source observations remain unchanged; external termination is not assumed. ${s.execution.phase === 'finished' ? 'The finalization budget has elapsed.' : 'Advance the replay to inspect the finalization result.'}</p></div></div>`;
    } else if (hasProtectiveHold && s.execution.phase === 'finished') {
      notice = `<div class="notice-banner"><span class="icon">${icons.warning}</span><div><strong>Protective hold · remote termination is unverified</strong><p>${esc(s.execution.reason || 'The run is sealed, but an active or unknown external operation remains unresolved. Reconcile the external effect before releasing the protection.')}</p></div></div>`;
    } else if (s.execution.outcome === 'blocked') {
      notice = `<div class="notice-banner blue"><span class="icon">${icons.info}</span><div><strong>Precondition blocked mutation</strong><p>${esc(s.execution.reason || 'The baseline check did not pass. No injection attempt was dispatched; required criteria remain inconclusive.')}</p></div></div>`;
    } else if (s.assessment.verdict === 'failed' && s.execution.outcome === 'succeeded') {
      notice = `<div class="notice-banner red"><span class="icon">${icons.info}</span><div><strong>The workflow completed; the service did not meet a required criterion</strong><p>An assertion can execute successfully and return a false result. Inspect the required criterion and its correlated evidence.</p></div></div>`;
    }
    $('run-notice').innerHTML = notice;
  }

  function renderOutcomes(s, summary) {
    const a = s.assessment;
    const e = s.execution.outcome || s.execution.phase;
    const f = s.finalization;
    const counts = [['passed',a.passedCount],['failed',a.failedCount],['inconclusive',a.inconclusiveCount],['pending',a.pendingCount]];
    const denominator = a.requiredCount || 0;
    const meter = counts.filter(([,count]) => count > 0).map(([kind,count]) => `<span class="${kind}" style="flex:${count}" title="${count} ${kind}"></span>`).join('');
    const evaluating = !a.final && a.pendingCount > 0 && a.failedCount === 0;
    const assessmentLabel = evaluating ? 'Evaluating' : human(a.verdict);
    const evidenceCaption = evaluating ? `${a.passedCount}/${denominator} passed · ${a.pendingCount} pending` : a.failedCount ? `${a.failedCount} failed · ${a.passedCount}/${denominator} passed` : a.inconclusiveCount ? `${a.inconclusiveCount} inconclusive · ${a.passedCount}/${denominator} passed` : `${a.passedCount}/${denominator} required criteria passed`;
    const unresolvedCount = Array.isArray(f.unresolvedEffects) ? f.unresolvedEffects.length : f.unresolvedEffects || 0;
    const cleanupCaption = f.status === 'not_started' ? `${f.requiredCount} finalizers defined · begins after main settles` : f.status === 'complete' ? `${f.completedCount}/${f.requiredCount} succeeded · no unresolved effects` : `${f.settledCount}/${f.requiredCount} settled · ${unresolvedCount} unresolved effects`;
    $('outcomes').innerHTML = `<article class="outcome-card"><div class="outcome-label">${icons.execution}<span>Execution</span></div><div class="outcome-value ${tone(e)}">${esc(human(e))}</div><p class="outcome-caption">${summary.finishedSteps}/${summary.totalSteps} steps settled · elapsed ${elapsed(summary.elapsedSeconds)}</p></article><article class="outcome-card"><div class="outcome-label">${icons.assessment}<span>Assessment</span></div><div class="outcome-value ${evaluating ? 'teal' : tone(a.verdict)}" title="Underlying assessment verdict: ${esc(a.verdict)}">${esc(assessmentLabel)}${!a.final ? '<span class="provisional">provisional</span>' : ''}</div><p class="outcome-caption">${esc(evidenceCaption)}</p><div class="criterion-meter" role="img" aria-label="${esc(counts.map(([kind,count]) => `${count} ${kind}`).join(', '))}; denominator ${denominator}">${meter || '<span class="pending" style="flex:1"></span>'}</div></article><article class="outcome-card"><div class="outcome-label">${icons.cleanup}<span>Finalization &amp; cleanup</span></div><div class="outcome-value ${tone(f.status)}">${esc(human(f.status))}${protectiveHold(s) ? '<span class="provisional">hold</span>' : ''}</div><p class="outcome-caption">${esc(cleanupCaption)}</p></article>`;
  }

  function protectiveHold(s) { return Boolean(s.finalization.protectiveHold); }
  function updateControls(s) {
    $('replay-cursor').max = replayLimit(s);
    $('replay-cursor').value = state.cursors[s.key];
    $('replay-cursor').setAttribute('aria-valuetext', `${elapsed(state.cursors[s.key])} elapsed, ${time(s.now)}`);
    $('cursor-label').textContent = elapsed(state.cursors[s.key]);
    $('duration-label').textContent = elapsed(replayLimit(s));
    $('replay-time').textContent = time(s.now);
    $('play-toggle').innerHTML = `<span aria-hidden="true">${state.playing ? 'Ⅱ' : '▶'}</span>${state.playing ? 'Pause' : 'Play'}`;
    $('play-toggle').setAttribute('aria-pressed', String(state.playing));
    $('play-toggle').setAttribute('aria-label', state.playing ? 'Pause synthetic replay' : 'Play synthetic replay');
    $('advance-replay').disabled = state.cursors[s.key] >= replayLimit(s);
    $('step-tab-count').textContent = s.steps.length;
    $('criteria-tab-count').textContent = s.assessment.requiredCount;
    $('evidence-tab-count').textContent = s.evidence.length;
    const sourceAge = s.observation && s.observation.ageSeconds;
    $('source-freshness').classList.toggle('stale', sourceAge == null);
    $('source-freshness').innerHTML = `<i aria-hidden="true"></i>${sourceAge == null ? 'No source observation' : `Latest source ${esc(age(sourceAge))} ago`}`;
    $('source-freshness').title = `Last source observation: ${time(s.observation && s.observation.lastSourceObservationAt, true)}. Replay time is not a new source observation.`;
    document.querySelectorAll('.view-tabs [data-tab]').forEach((button) => {
      const selected = button.dataset.tab === state.tab;
      button.setAttribute('aria-selected', String(selected));
      button.tabIndex = selected ? 0 : -1;
    });
    $('view-panel').setAttribute('aria-labelledby', `tab-${state.tab}`);
  }
  function replayLimit(s) {
    return s.durationSeconds;
  }

  function levels(steps) {
    const keys = new Set(steps.map((step) => step.stepKey));
    const remaining = steps.slice();
    const resolved = new Set();
    const result = [];
    while (remaining.length) {
      const next = remaining.filter((step) => refList(step.needs).filter((key) => keys.has(key)).every((key) => resolved.has(key)));
      if (!next.length) { result.push(remaining.slice()); break; }
      result.push(next);
      next.forEach((step) => { resolved.add(step.stepKey); remaining.splice(remaining.indexOf(step), 1); });
    }
    return result;
  }
  function workflowNode(step, s) {
    const check = criterionFor(s, step.stepKey);
    const status = outcome(step);
    return `<button type="button" class="workflow-node ${esc(status)}" data-step="${esc(step.stepKey)}" data-node="${esc(step.stepKey)}" aria-label="Inspect ${esc(step.label)}, execution ${esc(human(status))}${check ? `, ${check.required ? 'criterion' : 'precondition'} ${esc(human(check.verdict))}` : ''}">${mark(status)}<span class="workflow-node-main"><strong>${esc(step.label)}</strong><small title="${esc(step.uses)}">${esc(operationName(step.uses))}</small><span class="workflow-node-meta"><span>${esc(step.stepKey)}</span>${check ? badge(`${check.required ? 'Criterion' : 'Precondition'}: ${human(check.verdict)}`, check.verdict) : statusBadge(status)}</span></span></button>`;
  }
  function graph(steps, graphName, s) {
    if (!steps.length) return empty('No steps in this phase', 'The published revision does not define any.', true);
    return `<div class="workflow-graph" data-graph="${graphName}"><svg class="graph-edges" aria-hidden="true"></svg>${levels(steps).map((level) => { const parents = level.length === 1 ? refList(level[0].needs).filter((key) => steps.some((step) => step.stepKey === key)) : []; return `<div class="workflow-level"${parents.length === 1 ? ` data-align-parent="${esc(parents[0])}"` : ''}>${level.map((step) => workflowNode(step,s)).join('')}</div>`; }).join('')}</div>`;
  }
  function compactSteps(steps, s) {
    return steps.map((step) => `<div class="compact-step-row">${mark(outcome(step))}<div class="compact-step-main"><button type="button" data-step="${esc(step.stepKey)}"><strong>${esc(step.label)}</strong><small>${esc(step.stepKey)} · ${esc(step.assessmentRole || 'operation')}${refList(step.needs).length ? ` · needs ${esc(refList(step.needs).join(', '))}` : ''}</small></button></div>${statusBadge(outcome(step))}<span class="compact-step-time">${duration(step.startedAt,step.endedAt,s.now)}</span></div>`).join('');
  }
  function renderWorkflow(s) {
    const main = s.steps.filter((step) => step.graph === 'main');
    const finalizers = s.steps.filter((step) => step.graph === 'finalizer');
    return `<section class="panel"><header class="panel-header"><div><h2>Workflow execution</h2><p>One pinned revision. Inspect each operation and its observed attempts.</p></div><div class="segmented" role="group" aria-label="Workflow presentation"><button type="button" data-workflow-view="graph" aria-pressed="${state.workflowView === 'graph'}">Graph</button><button type="button" data-workflow-view="list" aria-pressed="${state.workflowView === 'list'}">List</button></div></header><div class="graph-section"><div class="phase-label"><i class="phase-line"></i>Main steps<span>${main.filter((step) => step.phase === 'finished').length}/${main.length} settled</span></div>${state.workflowView === 'graph' ? graph(main,'main',s) : compactSteps(main,s)}</div><div class="phase-barrier">${icons.lock}<span>All main steps settle before finalization · cleanup runs on every outcome</span></div><div class="graph-section finalizers"><div class="phase-label"><i class="phase-line"></i>Finalizers<span>${finalizers.filter((step) => step.phase === 'finished').length}/${finalizers.length} settled</span></div>${state.workflowView === 'graph' ? graph(finalizers,'finalizer',s) : compactSteps(finalizers,s)}</div><footer class="panel-footer"><div class="graph-legend"><span><strong>Execution:</strong></span><span><i class="green"></i>Succeeded</span><span><i class="teal"></i>Running</span><span><i></i>Pending / skipped</span><span><i class="red"></i>Failed / timed out</span><span>Check badges show assessment verdicts.</span></div><button type="button" class="text-button" data-tab="steps">Inspect all attempts →</button></footer></section>`;
  }
  function collectionTags(item) {
    return `${badge(`Collection: ${human(statusOf(item.collection))}`,statusOf(item.collection))}${badge(`Coverage: ${human(statusOf(item.coverage))}`,statusOf(item.coverage))}`;
  }
  function renderCriteriaSummary(s) {
    return `<section class="panel"><header class="panel-header"><div><h2>Required criteria</h2><p>${s.assessment.passedCount} passed of ${s.assessment.requiredCount} declared at admission</p></div><span class="tag">${s.assessment.requiredCount} required</span></header>${s.criteria.map((criterion) => `<article class="criterion-mini"><div class="criterion-mini-top"><span class="criterion-mini-title">${esc(criterion.label)}</span>${statusBadge(criterion.verdict)}</div><p>${esc(criterion.summary || 'Awaiting an observed check result.')}</p><div class="mini-values"><span>Expected <strong>${esc(short(criterion.expected,28))}</strong></span><span>Observed <strong>${esc(short(criterion.actual,28))}</strong></span></div>${criterion.verdict === 'inconclusive' ? `<p class="coverage-note">${esc(human(criterion.reasonCode || 'proof incomplete'))}</p>` : ''}<button type="button" class="text-button" data-criterion="${esc(criterion.stepKey)}">Inspect criterion &amp; proof →</button></article>`).join('')}<footer class="panel-footer"><span>Skipped checks remain in the denominator.</span><button type="button" class="text-button" data-tab="criteria">View all →</button></footer></section>`;
  }
  function renderEffects(s) {
    return `<section class="panel"><header class="panel-header"><div><h2>Remote effects</h2><p>Provider observations and local control facts</p></div><span class="tag">${s.effects.length}</span></header>${s.effects.length ? s.effects.map((effect) => `<article class="effect-item"><div class="effect-title"><strong>${esc(effect.provider || 'External operation')}</strong>${statusBadge(effect.disposition)}</div><code>${esc(effect.nativeId || 'Native identifier not recovered')}</code><p>${esc(effect.detail || 'Provider state requires independent reconciliation.')}</p><div class="effect-meta"><span>${effect.observationKind === 'local' ? 'Local: ' : 'Provider: '}${esc(human(effect.observationKind === 'local' ? effect.localState || 'unknown' : effect.providerState || 'unknown'))}</span><time>${esc(time(effect.observedAt))}</time></div><button type="button" class="text-button" data-effect="${esc(effect.originEffectKey)}">Inspect provider reference →</button></article>`).join('') : empty('No remote effect observed', 'A pending or undispatched operation is not evidence of a fault.', true)}${protectiveHold(s) ? `<div class="hold-note"><span class="icon">${icons.lock}</span><span>Protective hold remains until remote termination is observed.</span></div>` : '<footer class="panel-footer">Provider observations remain separate from local execution.</footer>'}</section>`;
  }
  function renderRecent(s) {
    const evidence = s.evidence.slice().sort((a,b) => new Date(b.observedAt) - new Date(a.observedAt)).slice(0,4);
    return `<section class="panel"><header class="panel-header"><div><h2>Recent evidence</h2><p>Ordered by observation time · source time can differ</p></div><button type="button" class="text-button" data-tab="evidence">All evidence →</button></header><div class="recent-evidence">${evidence.length ? evidence.map((item) => `<div class="recent-row"><span class="recent-dot" aria-hidden="true"></span><div class="recent-main"><div class="recent-meta"><span>${esc(item.source)}</span><time>${esc(time(item.observedAt))}</time></div><button type="button" data-evidence="${esc(item.evidenceId)}">${esc(item.title)}</button></div></div>`).join('') : empty('No evidence collected yet', 'Advance the replay to the next observation.', true)}</div></section>`;
  }
  function renderScope(s) {
    const subject = s.admission.subject;
    return `<section class="panel context-panel"><header class="panel-header"><div><h2>Admitted scope</h2><p>Captured before the first operation</p></div><span class="locked-tag">${icons.lock}Pinned</span></header>${properties([['Subject',esc(typeof subject === 'string' ? subject : subject && (subject.service || subject.name || subject.serviceId) || s.service)],['Environment',esc(s.environment)],['Region',esc(s.region)],['Revision',`<code>${esc(s.revision.scenarioRevisionId)}</code>`],['Created',esc(time(s.createdAt))],['Source observed',esc(time(s.observation && s.observation.lastSourceObservationAt))]],'context-list')}<div class="scope-accounts">${(s.accounts || []).map((account) => `<span class="tag mono">${esc(typeof account === 'string' ? account : account.accountId || short(account))}</span>`).join('')}</div><footer class="panel-footer"><button type="button" class="text-button" data-admission>Inspect bindings &amp; policies →</button></footer></section>`;
  }
  function renderOverview(s) {
    return `<div class="overview-layout"><div class="overview-main">${renderWorkflow(s)}${renderRecent(s)}</div><aside class="overview-side" aria-label="Assessment decision context">${renderCriteriaSummary(s)}${renderEffects(s)}${renderScope(s)}</aside></div>`;
  }

  function dependencies(step) {
    const refs = refList(step.needs);
    return refs.length ? `<div class="dependency-links">${refs.map((ref) => `<button type="button" class="dependency-link mono" data-step="${esc(ref)}">${esc(ref)}</button>`).join('')}</div>` : '<span class="muted">—</span>';
  }
  function renderSteps(s) {
    const q = state.stepQuery.toLowerCase().trim();
    const filtered = s.steps.filter((step) => (state.stepFilter === 'all' || step.graph === state.stepFilter || outcome(step) === state.stepFilter) && (!q || `${step.label} ${step.stepKey} ${step.uses}`.toLowerCase().includes(q)));
    const rows = ['main','finalizer'].map((section) => {
      const steps = filtered.filter((step) => step.graph === section);
      return steps.length ? `<tr class="table-section-row"><td colspan="7">${section === 'main' ? 'Main steps' : 'Finalizers · every outcome'}</td></tr>${steps.map((step) => `<tr><td><div class="step-cell">${mark(outcome(step))}<button type="button" class="row-button" data-step="${esc(step.stepKey)}"><span class="cell-title">${esc(step.label)}</span><span class="cell-sub mono">${esc(step.stepKey)}</span></button></div></td><td>${statusBadge(outcome(step))}</td><td><span class="cell-sub mono">${esc(step.uses)}</span></td><td>${dependencies(step)}</td><td>${esc(step.assessmentRole || 'Operation')}</td><td>${step.attempts.length}</td><td class="duration-cell">${duration(step.startedAt,step.endedAt,s.now)}</td></tr>`).join('')}` : '';
    }).join('');
    return `<section class="panel wide-panel"><header class="panel-header"><div><h2>Steps &amp; attempts</h2><p>Execution status describes the operation. Criterion verdicts describe the service assessment.</p></div><span class="tag">${s.steps.reduce((n,step) => n + step.attempts.length,0)} attempts observed</span></header><div class="toolbar"><label class="search-grow"><span class="sr-only">Search steps</span><input id="step-search" type="search" placeholder="Find a step or operation…" value="${esc(state.stepQuery)}"></label><label>Show<select id="step-filter"><option value="all">All steps</option><option value="main" ${state.stepFilter === 'main' ? 'selected' : ''}>Main steps</option><option value="finalizer" ${state.stepFilter === 'finalizer' ? 'selected' : ''}>Finalizers</option><option value="running" ${state.stepFilter === 'running' ? 'selected' : ''}>Running</option><option value="skipped" ${state.stepFilter === 'skipped' ? 'selected' : ''}>Skipped</option><option value="failed" ${state.stepFilter === 'failed' ? 'selected' : ''}>Failed</option></select></label><span class="toolbar-count">${filtered.length} of ${s.steps.length}</span></div>${filtered.length ? `<div class="table-scroll"><table class="data-table"><thead><tr><th>Step</th><th>Execution</th><th>Pinned operation</th><th>Needs</th><th>Assessment role</th><th>Attempts</th><th>Elapsed</th></tr></thead><tbody>${rows}</tbody></table></div>` : empty('No matching steps', 'Change the search or execution filter.')}<footer class="panel-footer"><span>Zero attempts means the operation was never dispatched.</span><span>All timestamps use UTC.</span></footer></section><div class="info-strip"><span class="icon">${icons.branch}</span><p><strong>Two dependency graphs.</strong> Main steps use their declared success or settlement gates. The finalizer graph begins after main steps settle and runs regardless of the assessment verdict. Inspect a step for its exact dependency policy and observed attempts.</p></div>`;
  }
  function criterionCard(c) {
    return `<article class="criterion-card"><header class="criterion-card-head"><div><div class="eyebrow">Required criterion · ${esc(c.stepKey)}</div><h3>${esc(c.label)}</h3></div>${statusBadge(c.verdict)}</header><p class="criterion-summary">${esc(c.summary || 'No observed check result is available at this replay position.')}</p><div class="criterion-observations"><div><span>Expected</span><strong>${esc(short(c.expected))}</strong></div><div><span>Observed</span><strong>${esc(short(c.actual))}</strong></div></div><div class="criterion-coverage">${collectionTags(c)}${c.reasonCode ? `<span class="tag">${esc(human(c.reasonCode))}</span>` : ''}</div><footer class="criterion-footer"><span>${(c.evidenceIds || []).length} evidence references · ${c.evaluatedThrough ? esc(time(c.evaluatedThrough)) : 'not evaluated yet'}</span><button type="button" class="text-button" data-criterion="${esc(c.stepKey)}">Inspect proof →</button></footer></article>`;
  }
  function renderCriteria(s) {
    return `<div class="section-heading"><div><h2>Required criteria</h2><p>The denominator is fixed at admission. Missing, skipped or unevaluable checks cannot silently pass.</p></div><span class="tag">${s.assessment.requiredCount} required</span></div><div class="criteria-grid">${s.criteria.map(criterionCard).join('')}</div><section class="panel precondition-panel"><header class="panel-header"><div><h2>Preconditions</h2><p>Gate the workflow before mutation; they are separate from the service criteria.</p></div><span class="tag">${(s.preconditions || []).length} checks</span></header>${(s.preconditions || []).length ? s.preconditions.map((check) => `<div class="precondition-row"><div><strong><button type="button" class="text-button" data-criterion="${esc(check.stepKey)}">${esc(check.label)}</button></strong><p>${esc(check.summary || 'Awaiting baseline evidence.')}</p></div>${statusBadge(check.verdict)}</div>`).join('') : empty('No preconditions', 'This revision declares no precondition checks.', true)}</section><div class="info-strip" style="margin-top:17px"><span class="icon">${icons.info}</span><p><strong>Proof follows the claim.</strong> A matching receipt can prove that a delivery occurred even when observation is partial. A negative or aggregate claim requires an adequate scope, a closed window, and complete collection. Unknown values remain unknown.</p></div>`;
  }
  function renderEvidence(s) {
    const sources = Array.from(new Set(s.evidence.map((item) => item.source).concat(state.evidenceSource !== 'all' ? [state.evidenceSource] : []))).sort();
    const evidence = M.filterEvidence(s,{source:state.evidenceSource === 'all' ? undefined : state.evidenceSource,query:state.evidenceQuery,stepKey:state.evidenceStep || undefined}).slice().sort((a,b) => new Date(b.observedAt) - new Date(a.observedAt));
    return `<section class="panel wide-panel"><header class="panel-header"><div><h2>Observed evidence</h2><p>Source records, query results and receiver receipts linked to the step that collected them.</p></div><button type="button" class="button button-small" data-export>${icons.export}Export observed snapshot</button></header><div class="toolbar"><label class="search-grow"><span class="sr-only">Search evidence</span><input id="evidence-search" type="search" placeholder="Find an observation or source record…" value="${esc(state.evidenceQuery)}"></label><label>Source<select id="evidence-source"><option value="all">All sources</option>${sources.map((source) => `<option value="${esc(source)}" ${state.evidenceSource === source ? 'selected' : ''}>${esc(source)}</option>`).join('')}</select></label><span class="toolbar-count">${evidence.length} of ${s.evidence.length}</span>${state.evidenceStep ? `<span class="active-filter">Step: <code>${esc(state.evidenceStep)}</code><button type="button" data-clear-evidence-step aria-label="Clear step evidence filter">×</button></span>` : ''}</div>${evidence.length ? evidence.map((item) => `<article class="evidence-row"><div class="evidence-time"><time>${esc(time(item.observedAt).replace(' UTC',''))}</time><small>observed · UTC</small></div><div class="evidence-main"><div class="evidence-tags"><span class="source-tag">${esc(item.source)}</span><span class="tag">${esc(human(item.kind))}</span><button type="button" class="dependency-link mono" ${!item.stepKey ? 'data-source-freshness' : item.stepKey === 'admission' ? 'data-admission' : `data-step="${esc(item.stepKey)}"`}>${esc(item.stepKey || 'runtime')}</button></div><button type="button" class="row-button" data-evidence="${esc(item.evidenceId)}"><span class="cell-title">${esc(item.title)}</span></button><p>${esc(item.summary)}</p></div><div class="evidence-side">${collectionTags(item)}<span>${item.occurredAt ? `occurred ${esc(time(item.occurredAt).replace(' UTC',''))}` : 'source time unknown'}</span></div></article>`).join('') : empty('No matching evidence', s.evidence.length ? 'Change the search, source or step filter.' : 'No source record has been observed at this replay position. Advance the replay to collect evidence.')}<footer class="panel-footer"><span>Export contains only the current projection; future replay events are excluded.</span><span>${esc(time(s.now,true))}</span></footer></section>`;
  }
  function renderDefinition(s) {
    const revision = s.revision;
    const operations = revision.operations || [];
    return `<div class="info-strip"><span class="icon">${icons.lock}</span><p><strong>Published revision ${esc(revision.version)} is immutable.</strong> This run keeps the submitted inputs, resolved bindings, required criteria and exact operation locks captured at admission. Digests and cloud identifiers in this demonstration are synthetic.</p></div><div class="definition-grid"><div class="definition-column"><section class="panel"><header class="panel-header"><div><h2>Scenario definition</h2><p>${esc(s.scenario && (s.scenario.displayName || s.scenario.name || s.scenario.title || s.scenario.scenarioId) || s.title)}</p></div><button type="button" class="button button-small" data-copy-definition>${icons.copy}Copy YAML</button></header><pre class="code-block"><code>${esc(revision.yaml || '# No YAML in this projection')}</code></pre><footer class="panel-footer"><span>Revision ${esc(revision.version)} · ${esc(time(revision.publishedAt,true))}</span><a href="../docs/suggested/examples/alarm-delivery.md" target="_blank" rel="noopener">Example notes ↗</a></footer></section><section class="panel"><header class="panel-header"><div><h2>Admission snapshot</h2><p>Resolved once; retained with the run</p></div><button type="button" class="text-button" data-admission>Inspect all →</button></header>${codeBlock({subject:s.admission.subject,inputs:s.admission.inputs,bindings:s.admission.bindings,requiredCriteria:s.admission.requiredCriteria})}</section></div><div class="definition-column"><section class="panel"><header class="panel-header"><div><h2>Revision identity</h2><p>Published content and lock</p></div><span class="locked-tag">${icons.lock}Pinned</span></header>${properties([['Scenario revision',`<code>${esc(revision.scenarioRevisionId)}</code>`],['Version',esc(revision.version)],['Content digest',`<code>${esc(revision.digest)}</code>`],['Published',esc(time(revision.publishedAt,true))]],'definition-properties')}<footer class="panel-footer"><a href="../docs/suggested/api.md" target="_blank" rel="noopener">Review publication &amp; run API ↗</a></footer></section><section class="panel"><header class="panel-header"><div><h2>Pinned operation lock</h2><p>Implementation and input/output schema digests</p></div><span class="tag">${operations.length}</span></header>${operations.map((operation) => `<div class="lock-row"><button type="button" class="row-button" data-operation="${esc(operation.uses)}"><strong>${esc(operation.uses)}</strong><code title="Implementation digest">implementation ${esc(operation.implementationDigest)}</code><code title="Input schema digest">input ${esc(operation.inputSchemaDigest)}</code><code title="Output schema digest">output ${esc(operation.outputSchemaDigest)}</code></button></div>`).join('')}<footer class="panel-footer"><a href="../docs/suggested/adapters.md" target="_blank" rel="noopener">Adapter semantics &amp; trust ↗</a></footer></section></div></div><div class="entity-strip">${[['Scenario → ScenarioRevision','A named workflow and its immutable published executable content.','Definition'],['Run → StepRun → StepAttempt','One admitted execution, logical graph steps and immutable dispatch attempts.','Execution'],['Evidence','Observed facts with provenance, source windows, cutoff and coverage.','Proof']].map(([name,description,label]) => `<article class="entity-card"><strong>${esc(name)}</strong><p>${esc(description)}</p><code>${esc(label)}</code></article>`).join('')}</div><div class="section-heading"><div><h2>Reviewed model diagrams</h2><p>Core entities, owned values and independent lifecycle axes.</p></div><a class="text-button" href="../docs/suggested/model.md" target="_blank" rel="noopener">Read the model ↗</a></div><div class="diagram-grid">${diagrams.map((diagram) => `<button type="button" class="diagram-card" data-diagram="${diagram.key}"><span>${diagram.category}</span><strong>${diagram.title} <span aria-hidden="true" style="display:inline">↗</span></strong><p>${diagram.description}</p></button>`).join('')}</div>`;
  }
  const diagrams = [
    {key:'01_entities',category:'Class diagram',title:'Six core entities',description:'Aggregate boundaries and cardinalities for the execution model.'},
    {key:'02_owned_values',category:'Class diagram',title:'Owned values & contracts',description:'Definitions, locks, attempts, evidence and the decision proof.'},
    {key:'03_lifecycle',category:'State diagram',title:'Execution & finalization',description:'Terminal execution, separate verdicts and unresolved remote effects.'}
  ];

  const renderers = {overview:renderOverview,steps:renderSteps,criteria:renderCriteria,evidence:renderEvidence,definition:renderDefinition};
  function captureFocus() {
    const active = document.activeElement;
    if (!active || active === document.body) return null;
    const attributes = ['data-step','data-evidence','data-criterion','data-effect','data-select-run','data-workflow-view','data-export','data-tab'];
    const attribute = attributes.find((key) => active.hasAttribute(key));
    return {id:active.id || null,attribute,value:attribute ? active.getAttribute(attribute) : null,start:active.selectionStart,end:active.selectionEnd};
  }
  function restoreFocus(saved) {
    if (!saved || document.querySelector('dialog[open]')) return;
    let element = saved.id && $(saved.id);
    if (!element && saved.attribute) element = Array.from(document.querySelectorAll(`[${saved.attribute}]`)).find((item) => item.getAttribute(saved.attribute) === saved.value);
    if (element && document.activeElement !== element) {
      element.focus({preventScroll:true});
      if (saved.start != null && ['search','text'].includes(element.type)) element.setSelectionRange(saved.start,saved.end);
    }
  }
  function render(options = {}) {
    const focus = captureFocus();
    const s = projection();
    const summary = getSummary(s);
    renderRail();
    renderHeader(s,summary);
    renderOutcomes(s,summary);
    updateControls(s);
    $('view-panel').innerHTML = renderers[state.tab](s);
    if (options.restoreFocus !== false) restoreFocus(focus);
    if (state.tab === 'overview' && state.workflowView === 'graph') requestAnimationFrame(() => drawEdges(s));
  }
  function drawEdges(s) {
    document.querySelectorAll('[data-graph]').forEach((container) => {
      let rect = container.getBoundingClientRect();
      const svgElement = container.querySelector('.graph-edges');
      const nodes = new Map(Array.from(container.querySelectorAll('[data-node]')).map((node) => [node.dataset.node,node]));
      // A lone child stays beneath its sole parent. This keeps skip-level edges
      // from crossing an unrelated node, including the narrow mobile graph.
      container.querySelectorAll('[data-align-parent]').forEach((row) => {
        const parent = nodes.get(row.dataset.alignParent);
        const child = row.querySelector('[data-node]');
        if (!parent || !child) return;
        const parentBox = parent.getBoundingClientRect();
        const width = Math.min(parentBox.width, rect.width);
        const left = Math.max(0, Math.min(rect.width - width, parentBox.left + parentBox.width / 2 - rect.left - width / 2));
        row.style.justifyContent = 'flex-start';
        child.style.width = `${width}px`;
        child.style.marginLeft = `${left}px`;
      });
      rect = container.getBoundingClientRect();
      svgElement.setAttribute('viewBox',`0 0 ${rect.width} ${rect.height}`);
      svgElement.innerHTML = s.steps.filter((step) => step.graph === container.dataset.graph).flatMap((step) => refList(step.needs).map((dependency) => {
        const parent = nodes.get(dependency), child = nodes.get(step.stepKey);
        if (!parent || !child) return '';
        const a = parent.getBoundingClientRect(), b = child.getBoundingClientRect();
        const x1 = a.left + a.width / 2 - rect.left, y1 = a.bottom - rect.top;
        const x2 = b.left + b.width / 2 - rect.left, y2 = b.top - rect.top;
        const bend = Math.max(8,(y2-y1)/2);
        return `<path class="${step.phase !== 'pending' ? 'observed' : ''}" d="M${x1},${y1} C${x1},${y1+bend} ${x2},${y2-bend} ${x2},${y2}"/>`;
      })).join('');
    });
  }

  function evidenceLinks(s, ids) {
    const evidence = (ids || []).map((id) => s.evidence.find((item) => item.evidenceId === id)).filter(Boolean);
    return evidence.length ? evidence.map((item) => `<div class="detail-evidence-link"><span class="source-tag">${esc(item.source)}</span><button type="button" class="text-button" data-evidence="${esc(item.evidenceId)}">${esc(item.title)} →</button></div>`).join('') : '<p class="fine-print">No observed evidence is linked at this replay position.</p>';
  }
  function openDetail({eyebrow,title,subtitle,body,data,copy = true}) {
    pause();
    const dialog = $('detail-dialog');
    if (!dialog.open) state.returnFocus = captureFocus();
    $('detail-eyebrow').textContent = eyebrow;
    $('detail-title').textContent = title;
    $('detail-subtitle').textContent = subtitle || '';
    $('detail-body').innerHTML = body;
    $('detail-body').scrollTop = 0;
    $('detail-copy').hidden = !copy;
    state.detailData = data;
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    $('detail-title').focus({preventScroll:true});
  }
  function inspectStep(key) {
    const s = projection();
    const step = M.getStep(s,key);
    if (!step) return toast('That step is not part of this run.');
    const check = criterionFor(s,key);
    const lock = (s.revision.operations || []).find((operation) => operation.uses === step.uses);
    const evidence = s.evidence.filter((item) => item.stepKey === key);
    const attempts = step.attempts.map((attempt) => `<article class="attempt-card"><header class="attempt-card-head"><strong>Attempt ${esc(attempt.attemptNo)}</strong>${statusBadge(attempt.outcome || attempt.phase)}</header><div class="attempt-card-body">${properties([['Started',esc(time(attempt.startedAt,true))],['Ended',esc(time(attempt.endedAt,true))],['Dispatch key',`<code>${esc(attempt.dispatchKey || 'Not dispatched')}</code>`]])}${attempt.error ? `<div class="error-box"><strong>${esc(attempt.error.code || attempt.error.type || 'Operation error')}</strong>${esc(typeof attempt.error === 'string' ? attempt.error : attempt.error.message || short(attempt.error,300))}</div>` : ''}<div class="detail-columns"><section class="detail-section"><h3>Resolved inputs</h3>${codeBlock(attempt.resolvedInputs)}</section><section class="detail-section"><h3>Observed outputs</h3>${codeBlock(attempt.outputs)}</section></div>${attempt.checkpoint ? `<section class="detail-section"><h3>Durable checkpoint</h3>${codeBlock(attempt.checkpoint)}</section>` : ''}${(attempt.externalRefs || []).length ? `<section class="detail-section"><h3>External operation references · historical attempt record</h3>${codeBlock(attempt.externalRefs)}</section>` : ''}</div></article>`).join('');
    openDetail({eyebrow:`${step.graph === 'finalizer' ? 'Finalizer' : 'Main step'} · ${key}`,title:step.label,subtitle:step.uses,data:step,body:`<div class="detail-status">${statusBadge(outcome(step))}${check ? badge(`Criterion: ${human(check.verdict)}`,check.verdict) : ''}<p>${step.attempts.length} observed attempt${step.attempts.length === 1 ? '' : 's'} · ${duration(step.startedAt,step.endedAt,s.now)} elapsed</p></div>${step.skipReason ? `<div class="notice-box amber">${esc(step.skipReason)}</div>` : ''}<div class="detail-columns"><section class="detail-section"><h3>Dependency contract</h3>${properties([['Graph',esc(human(step.graph))],['Needs',dependencies(step)],['After policy',esc(short(step.after || (step.graph === 'finalizer' ? 'settled' : 'succeeded')))],['Assessment role',esc(step.assessmentRole || 'None')]])}</section><section class="detail-section"><h3>Pinned implementation</h3>${lock ? codeBlock(lock) : '<p class="fine-print">No operation lock is present.</p>'}</section></div><section class="detail-section"><h3>Dispatch attempts</h3>${attempts || empty('No attempt dispatched', step.skipReason || 'The step is still pending. An absent attempt is not an observed success.',true)}</section><section class="detail-section"><h3>Evidence from this step</h3>${evidenceLinks(s,evidence.map((item) => item.evidenceId))}${evidence.length ? `<div class="detail-evidence-link"><button type="button" class="text-button" data-filter-step="${esc(key)}">Show ${evidence.length} exact step evidence records →</button></div>` : ''}</section>${check ? `<button type="button" class="button button-small" data-criterion="${esc(key)}">Inspect ${check.required ? 'required criterion' : 'precondition'} proof</button>` : ''}`});
  }
  function inspectCriterion(key) {
    const s = projection(), c = criterionFor(s,key);
    if (!c) return;
    openDetail({eyebrow:c.required ? 'Required criterion · included in denominator' : 'Precondition · gates mutation',title:c.label,subtitle:key,data:c,body:`<div class="detail-status">${statusBadge(c.verdict)}${c.reasonCode ? `<span class="tag">${esc(c.reasonCode)}</span>` : ''}</div><p>${esc(c.summary || 'No observed check result is available yet.')}</p><div class="detail-columns"><section class="detail-section"><h3>Expected</h3>${codeBlock(c.expected)}</section><section class="detail-section"><h3>Observed</h3>${codeBlock(c.actual)}</section></div><section class="detail-section"><h3>Decision boundary</h3>${properties([['Evaluated through',esc(time(c.evaluatedThrough,true))],['Collection',statusBadge(statusOf(c.collection))],['Coverage',statusBadge(statusOf(c.coverage))],['Required at admission',c.required ? 'Yes · remains in denominator' : 'Precondition; outside criterion denominator']])}</section><div class="detail-columns"><section class="detail-section"><h3>Proof contract</h3>${codeBlock({kind:c.proof,window:c.window,evaluatedThrough:c.evaluatedThrough,predicateDigest:c.predicateDigest,evaluatorVersion:c.evaluatorVersion})}</section><section class="detail-section"><h3>Collection &amp; coverage</h3>${codeBlock({collection:c.collection,coverage:c.coverage})}</section></div><section class="detail-section"><h3>Supporting evidence</h3>${evidenceLinks(s,c.evidenceIds)}</section><button type="button" class="button button-small" data-step="${esc(key)}">Inspect executing step &amp; attempts</button>`});
  }
  function receiptFacts(item) {
    const value = item.value;
    if (!value || !value.receivedAt) return '';
    return `<section class="detail-section"><h3>Receiver timing &amp; correlation</h3>${properties([
      ['Receiver receipt time',esc(time(value.receivedAt,true))],
      ['Collector ingestion time',esc(time(value.ingestedAt,true))],
      ['Alarm state change',esc(time(value.stateChangeTime,true))],
      ['Clock basis',esc(human(value.clockBasis || 'not specified'))],
      ['Clock uncertainty',value.clockUncertaintyMs == null ? 'Not specified' : `±${esc(value.clockUncertaintyMs)} ms (synthetic bound)`],
      ['Observed latency',value.latencySeconds == null ? 'Unknown' : `${esc(value.latencySeconds)} seconds`],
      ['Allowed latency',value.deadlineSeconds == null ? 'Not specified' : `${esc(value.deadlineSeconds)} seconds`],
      ['Intended receiver',`<code>${esc(value.receiverId || 'Unknown')}</code>`],
      ['Message identifier',`<code>${esc(value.messageId || 'Unknown')}</code>`],
      ['Claim',esc(human(value.claim || 'receiver receipt'))]
    ])}</section>`;
  }
  function inspectEvidence(id) {
    const s = projection(), item = s.evidence.find((e) => e.evidenceId === id);
    if (!item) return;
    openDetail({eyebrow:`Evidence · ${item.kind}`,title:item.title,subtitle:item.evidenceId,data:item,body:`<div class="detail-status"><span class="source-tag">${esc(item.source)}</span>${collectionTags(item)}</div><p>${esc(item.summary)}</p>${receiptFacts(item)}<section class="detail-section"><h3>Source provenance</h3>${properties([['Source',esc(item.source)],['Source record',`<code>${esc(item.sourceRecordId || 'No native identifier')}</code>`],['Schema reference',`<code>${esc(item.schemaRef || 'Not provided')}</code>`],['Content digest',`<code>${esc(item.contentDigest || 'Not provided')}</code>`],['Occurred at source',esc(time(item.occurredAt,true))],['Observed by collector',esc(time(item.observedAt,true))],['Collecting step',!item.stepKey ? 'Local runtime' : item.stepKey === 'admission' ? '<button type="button" class="text-button" data-admission>Run admission →</button>' : `<button type="button" class="text-button mono" data-step="${esc(item.stepKey)}">${esc(item.stepKey)} →</button>`]])}</section><div class="detail-columns"><section class="detail-section"><h3>Scope &amp; intended receiver</h3>${codeBlock(item.scope)}</section><section class="detail-section"><h3>Collection, window &amp; cutoff</h3>${codeBlock({collection:item.collection,coverage:item.coverage,window:item.window,evaluatedThrough:item.evaluatedThrough || item.value && item.value.evaluatedThrough || null})}</section></div><section class="detail-section"><h3>Observed value</h3>${codeBlock(item.value)}</section><div class="notice-box">Observation time records when this workspace learned a fact. Source occurrence time and the criterion cutoff determine whether that fact satisfies the claim.</div>`});
  }
  function inspectEffect(key) {
    const s = projection(), effect = s.effects.find((e) => e.originEffectKey === key);
    if (!effect) return;
    openDetail({eyebrow:'Remote effect · latest observed projection',title:effect.provider || 'External operation',subtitle:effect.nativeId || 'Native identifier not recovered',data:effect,body:`<div class="detail-status">${statusBadge(effect.disposition)}${effect.requiresHold && !['terminal','none'].includes(effect.disposition) ? badge('Protective hold','incomplete') : ''}</div><p>${esc(effect.detail)}</p>${properties([['Origin effect key',`<code>${esc(effect.originEffectKey)}</code>`],['Creating step',`<button type="button" class="text-button mono" data-step="${esc(effect.stepKey)}">${esc(effect.stepKey)} →</button>`],['Observation source',effect.observationKind === 'local' ? 'Local runtime control fact' : 'Provider observation'],[effect.observationKind === 'local' ? 'Local control state' : 'Provider state',esc(human(effect.observationKind === 'local' ? effect.localState || 'unknown' : effect.providerState || 'unknown'))],['Last observed',esc(time(effect.observedAt,true))],['Account',`<code>${esc(effect.accountId || 'Unknown')}</code>`],['Region',esc(effect.region || 'Unknown')]])}${effect.requiresHold && !['terminal','none'].includes(effect.disposition) ? '<div class="notice-box amber" style="margin-top:16px">A local cancellation receipt is not evidence of remote termination. This operation must be reconciled before releasing the protective hold.</div>' : ''}${effect.actions && effect.actions.length ? `<section class="detail-section" style="margin-top:20px"><h3>Provider action observations</h3>${codeBlock(effect.actions)}<p class="fine-print">FIS action details belong to the external experiment; they are not independently controllable workflow steps.</p></section>` : ''}<section class="detail-section" style="margin-top:20px"><h3>Complete observed reference</h3>${codeBlock(effect)}</section>`});
  }
  function inspectFreshness() {
    const s = projection();
    openDetail({eyebrow:'Source observation age',title:'What has actually been observed',subtitle:time(s.now,true),data:s.observation,body:`<div class="notice-box">Replay time advances locally. The latest observation across all sources does not establish freshness for every provider; each source retains its own observation time.</div><section class="detail-section" style="margin-top:20px"><h3>By source</h3>${(s.observation.bySource || []).length ? properties(s.observation.bySource.map((source) => [source.source,`${esc(time(source.observedAt,true))}<br>${esc(age(source.ageSeconds))} ago`])) : '<p class="fine-print">No provider observation has been recorded yet.</p>'}</section>${s.observation.sourceFrozenAt ? `<div class="notice-box amber">Source observations were frozen for this cancellation simulation at ${esc(time(s.observation.sourceFrozenAt,true))}.</div>` : ''}`});
  }
  function inspectAdmission() {
    const s = projection();
    openDetail({eyebrow:'Run admission · immutable snapshot',title:'Inputs, bindings & policies',subtitle:s.runId,data:s.admission,body:`<div class="notice-box">These values were resolved before dispatch. The required criterion list is retained even when a step is skipped or execution fails.</div><section class="detail-section" style="margin-top:20px"><h3>Admitted values</h3>${codeBlock(s.admission)}</section>`});
  }
  function inspectOperation(uses) {
    const s = projection(), operation = (s.revision.operations || []).find((o) => o.uses === uses);
    if (!operation) return;
    openDetail({eyebrow:'Published operation lock',title:operationName(uses),subtitle:uses,data:operation,body:`<div class="notice-box">This immutable lock pins implementation and schema content for replay and audit. All digest values in this local fixture are synthetic.</div><section class="detail-section" style="margin-top:20px"><h3>Lock record</h3>${codeBlock(operation)}</section><a href="../docs/suggested/adapters.md" target="_blank" rel="noopener">Read adapter semantics and the trust boundary ↗</a>`});
  }
  function inspectDiagram(key) {
    const diagram = diagrams.find((d) => d.key === key);
    if (!diagram) return;
    const base = `../diagrams/suggested/${key}`;
    openDetail({eyebrow:diagram.category,title:diagram.title,subtitle:diagram.description,copy:false,body:`<div class="diagram-preview"><img src="${base}.svg" alt="${esc(diagram.title)}: ${esc(diagram.description)}"></div><div class="diagram-document-links"><a href="${base}.svg" target="_blank" rel="noopener">Open full diagram ↗</a><a href="${base}.md" target="_blank" rel="noopener">Obsidian note ↗</a><a href="${base}.mmd" target="_blank" rel="noopener">Mermaid source ↗</a></div>`});
  }

  function toast(message) {
    $('toast').textContent = message;
    $('toast').classList.add('visible');
    clearTimeout(state.toastTimer);
    state.toastTimer = setTimeout(() => $('toast').classList.remove('visible'),3600);
  }
  async function copy(value, label) {
    try {
      await navigator.clipboard.writeText(value);
      toast(`${label} copied.`);
    } catch (_) {
      const area = document.createElement('textarea');
      area.value = value;
      area.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
      const host = document.querySelector('dialog[open]') || document.body;
      host.appendChild(area); area.select();
      const copied = document.execCommand('copy'); area.remove();
      toast(copied ? `${label} copied.` : 'Copy is unavailable in this browser. Use the exported snapshot.');
    }
  }
  function exportCurrent() {
    const s = projection(), data = M.exportSnapshot(s);
    const blob = new Blob([typeof data === 'string' ? data : json(data)],{type:'application/json'});
    const url = URL.createObjectURL(blob), link = document.createElement('a');
    link.href = url; link.download = `${s.runId}-observed-${Math.floor(state.cursors[s.key])}s.json`;
    document.body.appendChild(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url),1000);
    toast('Observed snapshot exported. Future replay events are excluded.');
  }
  function setTab(tab) {
    if (!renderers[tab]) return;
    state.tab = tab;
    render();
  }
  function pause() {
    state.playing = false;
    if ($('play-toggle')) {
      $('play-toggle').innerHTML = '<span aria-hidden="true">▶</span>Play';
      $('play-toggle').setAttribute('aria-pressed','false');
      $('play-toggle').setAttribute('aria-label','Play synthetic replay');
    }
  }
  function setCursor(value) {
    const s = projection();
    state.cursors[state.selected] = Math.max(0,Math.min(replayLimit(s),Number(value)));
    if (state.cursors[state.selected] >= replayLimit(s)) pause();
    render();
  }
  function openCancellation() {
    const s = projection();
    if (!getSummary(s).canCancel || state.interventions[s.key]) return;
    pause();
    state.returnFocus = captureFocus();
    $('cancel-dialog').showModal();
  }
  function confirmCancellation() {
    const s = projection();
    const reason = $('cancel-reason').value.trim() || 'Operator requested cancellation.';
    const result = M.requestCancellation(s,{clientToken:`demo-${s.runId}-${Math.floor(s.cursorSeconds)}`,reason});
    if (result.intervention) {
      state.interventions[s.key] = result.intervention;
      state.cancelAt = state.cancelAt || {};
      state.cancelAt[s.key] = s.cursorSeconds;
      $('cancel-dialog').close();
      render();
      toast('Cancellation accepted locally. External state remains unconfirmed.');
    } else {
      $('cancel-dialog').close();
      toast(result.receipt && (result.receipt.message || result.receipt.reason) || 'This run cannot accept a new cancellation.');
    }
  }

  document.addEventListener('click',(event) => {
    const button = event.target.closest('button');
    if (!button || button.disabled) return;
    const data = button.dataset;
    if (data.selectRun) {
      pause(); state.selected = data.selectRun;
      state.evidenceStep = ''; state.evidenceQuery = ''; state.evidenceSource = 'all';
      state.stepQuery = ''; state.stepFilter = 'all';
      render();
    } else if (data.runFilter) { state.runFilter = data.runFilter; renderRail(); }
    else if (data.tab) setTab(data.tab);
    else if (data.workflowView) { state.workflowView = data.workflowView; render(); }
    else if ('sourceFreshness' in data) inspectFreshness();
    else if (data.step) inspectStep(data.step);
    else if (data.criterion) inspectCriterion(data.criterion);
    else if (data.evidence) inspectEvidence(data.evidence);
    else if (data.effect) inspectEffect(data.effect);
    else if (data.operation) inspectOperation(data.operation);
    else if (data.diagram) inspectDiagram(data.diagram);
    else if ('admission' in data) inspectAdmission();
    else if ('export' in data) exportCurrent();
    else if ('copyRun' in data) copy(projection().runId,'Run identifier');
    else if ('copyDefinition' in data) copy(projection().revision.yaml,'Scenario YAML');
    else if ('cancelRun' in data) openCancellation();
    else if (data.closeDialog) $(data.closeDialog).close();
    else if (data.filterStep) {
      state.evidenceStep = data.filterStep;
      state.evidenceSource = 'all'; state.evidenceQuery = '';
      $('detail-dialog').close(); setTab('evidence');
      $('tab-evidence').focus({preventScroll:true});
    } else if ('clearEvidenceStep' in data) { state.evidenceStep = ''; render(); }
  });
  $('run-search').addEventListener('input',(event) => { state.runSearch = event.target.value; renderRail(); });
  $('view-panel').addEventListener('input',(event) => {
    if (event.target.id === 'evidence-search') { state.evidenceQuery = event.target.value; render(); }
    if (event.target.id === 'step-search') { state.stepQuery = event.target.value; render(); }
  });
  $('view-panel').addEventListener('change',(event) => {
    if (event.target.id === 'evidence-source') { state.evidenceSource = event.target.value; render(); }
    if (event.target.id === 'step-filter') { state.stepFilter = event.target.value; render(); }
  });
  $('replay-cursor').addEventListener('input',(event) => { pause(); setCursor(event.target.value); });
  $('play-toggle').addEventListener('click',() => {
    if (state.playing) pause();
    else {
      const s = projection();
      if (state.cursors[s.key] >= replayLimit(s)) state.cursors[s.key] = 0;
      state.playing = true; state.lastTick = performance.now();
    }
    render();
  });
  $('advance-replay').addEventListener('click',() => { pause(); setCursor(state.cursors[state.selected] + 30); });
  $('reset-replay').addEventListener('click',() => {
    pause(); delete state.interventions[state.selected];
    if (state.cancelAt) delete state.cancelAt[state.selected];
    state.cursors[state.selected] = fixture().initialCursorSeconds || 0;
    render(); toast('Original replay restored. Simulated cancellation cleared.');
  });
  $('replay-speed').addEventListener('change',(event) => { state.speed = Number(event.target.value); });
  $('confirm-cancel').addEventListener('click',confirmCancellation);
  $('detail-copy').addEventListener('click',() => copy(json(state.detailData),'Detail JSON'));
  document.querySelectorAll('dialog').forEach((dialog) => {
    dialog.addEventListener('close',() => { restoreFocus(state.returnFocus); });
    dialog.addEventListener('click',(event) => {
      if (event.target !== dialog) return;
      const bounds = dialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
    });
  });
  document.querySelector('.view-tabs').addEventListener('keydown',(event) => {
    if (!['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    const tabs = Array.from(document.querySelectorAll('.view-tabs [role="tab"]'));
    const index = tabs.indexOf(event.target);
    if (index < 0) return;
    event.preventDefault();
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? tabs.length - 1 : (index + (event.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
    setTab(tabs[next].dataset.tab);
    tabs[next].focus();
  });
  let resizeFrame;
  window.addEventListener('resize',() => { cancelAnimationFrame(resizeFrame); resizeFrame = requestAnimationFrame(() => { if (state.tab === 'overview') drawEdges(projection()); }); });
  document.addEventListener('visibilitychange',() => { if (document.hidden) pause(); });
  setInterval(() => {
    if (!state.playing) return;
    const now = performance.now(), delta = Math.min(1,(now-state.lastTick)/1000);
    state.lastTick = now;
    setCursor(state.cursors[state.selected] + delta*state.speed);
  },1000);

  render();
})();
