/* Pure projections over synthetic FIS fixtures. No network or DOM dependencies. */
(function (root, factory) {
  const model = factory();
  if (typeof module === 'object' && module.exports) module.exports = model;
  else root.FISModel = model;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const ACTION_STATES = ['pending', 'initiating', 'running', 'completed', 'cancelled', 'stopping', 'stopped', 'failed', 'skipped'];
  const TERMINAL_ACTION_STATES = new Set(['completed', 'cancelled', 'stopped', 'failed', 'skipped']);
  const TERMINAL_EXPERIMENT_STATES = new Set(['completed', 'cancelled', 'stopped', 'failed']);
  const ACTIVE_ACTION_STATES = new Set(['initiating', 'running', 'stopping']);
  const clone = object => JSON.parse(JSON.stringify(object));
  const finite = value => typeof value === 'number' && Number.isFinite(value);
  const instant = value => value == null ? null : Number.isFinite(Date.parse(value)) ? Date.parse(value) : null;
  const iso = (base, seconds) => new Date(Date.parse(base) + seconds * 1000).toISOString();
  const unique = list => [...new Set(list)];

  function getRunAt(input, requestedCursor) {
    if (!input || !input.experiment) throw new TypeError('A run with an experiment is required.');
    const source = input._sourceRun || input;
    const mock = source._mock || {};
    const defaultCursor = finite(source.initialCursorSeconds) ? source.initialCursorSeconds : 0;
    const maxCursor = finite(source.durationSeconds) ? source.durationSeconds : Math.max(0, requestedCursor || defaultCursor);
    const cursor = Math.min(maxCursor, Math.max(0, finite(requestedCursor) ? requestedCursor : defaultCursor));
    const origin = mock.clockOrigin || source.experiment.startTime || source.experiment.creationTime;
    const now = iso(origin, cursor);
    const pollInterval = mock.pollIntervalSeconds || 5;
    let snapshotCursor = Math.floor(cursor / pollInterval) * pollInterval;
    if (finite(source.observation?.freezeAtSeconds)) snapshotCursor = Math.min(snapshotCursor, source.observation.freezeAtSeconds);
    const run = clone(source);
    run.cursorSeconds = cursor;
    run.now = now;
    run.snapshotCursorSeconds = snapshotCursor;
    run._isProjection = true;
    Object.defineProperty(run, '_sourceRun', { value: source, enumerable: false });

    const experiment = run.experiment;
    const executionEnd = finite(mock.executionEnd) ? mock.executionEnd : source.executionDurationSeconds;
    const stopping = finite(mock.stoppingAt) && snapshotCursor >= mock.stoppingAt && snapshotCursor < executionEnd;
    const terminal = finite(executionEnd) && snapshotCursor >= executionEnd;
    if (terminal) {
      experiment.state = { status: mock.finalStatus || experiment.state.status, reason: mock.finalReason || experiment.state.reason };
      if (mock.error) experiment.state.error = clone(mock.error);
      experiment.endTime = iso(origin, executionEnd);
    } else {
      experiment.state = {
        status: stopping ? 'stopping' : snapshotCursor < 5 ? 'initiating' : 'running',
        reason: stopping ? 'Stopping the experiment and completing outstanding post actions.' : snapshotCursor < 5 ? 'Preparing the experiment and resolving targets.' : 'Experiment actions are in progress.'
      };
      delete experiment.endTime;
    }

    const scheduled = new Map((source.schedule || []).map(item => [item.name, item]));
    Object.entries(experiment.actions || {}).forEach(([name, action]) => {
      const item = scheduled.get(name);
      if (!item) return; // Unknown observations stay unknown; do not manufacture completion.
      delete action.startTime;
      delete action.endTime;
      let status = 'pending';
      let reason = 'Waiting for experiment preparation or predecessor actions.';
      if (item.start == null) {
        if (snapshotCursor >= item.end) {
          status = item.outcome;
          reason = item.reason || 'Action did not execute.';
        }
      } else if (snapshotCursor >= item.end) {
        status = item.outcome;
        reason = item.reason || (status === 'completed' ? 'Action completed.' : `Action ${status}.`);
        action.startTime = iso(origin, item.start);
        action.endTime = iso(origin, item.end);
      } else if (finite(item.stoppingAt) && snapshotCursor >= item.stoppingAt) {
        status = 'stopping';
        reason = 'Completing the configured post action before stopping.';
        action.startTime = iso(origin, item.start);
      } else if (snapshotCursor >= item.start) {
        status = 'running';
        reason = 'Action is running.';
        action.startTime = iso(origin, item.start);
      } else if (snapshotCursor >= Math.max(0, item.start - 5)) {
        status = 'initiating';
        reason = 'Action is preparing to start.';
      }
      action.state = { status, reason };
    });

    const resolutionAt = finite(mock.resolutionCompleteAt) ? mock.resolutionCompleteAt : 0;
    if (cursor < resolutionAt) {
      run.resolvedTargets = [];
      run.resolution = { status: 'resolving', complete: false, observedAt: now };
    }

    run.observation = Object.assign({}, source.observation, { lastSuccessfulFetchAt: iso(origin, snapshotCursor), snapshotAsOf: iso(origin, snapshotCursor) });

    const report = mock.report;
    delete experiment.experimentReport;
    if (report && report.kind !== 'not_generated') {
      let reportState = { status: 'pending', reason: 'Waiting for the experiment and configured post-experiment window.' };
      let s3Reports = [];
      if (snapshotCursor >= report.completedAt) {
        reportState = { status: report.kind, reason: report.reason || 'Report artifacts are available.' };
        if (report.error) reportState.error = clone(report.error);
        if (report.kind === 'completed') s3Reports = clone(report.artifacts || []);
      } else if (snapshotCursor >= report.runningAt) {
        reportState = { status: 'running', reason: 'Report generation is in progress.' };
      }
      experiment.experimentReport = { state: reportState, s3Reports };
    }

    run.evidence = (source.evidence || []).filter(event => {
      const seen = instant(event.observedAt);
      return seen !== null && seen <= instant(now);
    }).map(clone);
    if (run.telemetry) {
      run.telemetry.points = (source.telemetry.points || []).filter(point => point.offsetSeconds <= cursor && (point.observedAt == null || instant(point.observedAt) <= instant(now))).map(clone);
    }

    const isPreview = experiment.experimentOptions && experiment.experimentOptions.actionsMode === 'skip-all';
    const assessmentReady = cursor >= (mock.assessmentAvailableAt || 0);
    if (isPreview) {
      run.assessment = { status: 'not_assessed', summary: 'Target preview only. No faults executed; no resilience verdict assigned.', rule: null, evidence: [] };
    } else if (!assessmentReady) {
      run.assessment = {
        status: 'in_progress', summary: terminal ? 'Collecting the configured recovery window before evaluating the criterion.' : 'Collecting execution and workload observations.',
        rule: source.assessment ? source.assessment.rule : null, evidence: []
      };
    }

    if (run.safety) {
      const observations = (source.safety.history || []).filter(item => instant(item.observedAt) <= instant(now));
      run.safety.history = clone(observations);
      const latest = observations[observations.length - 1];
      run.safety.alarmState = latest ? latest.alarmState : null;
      run.safety.observedAt = latest ? latest.observedAt : null;
    }
    if (source.stopCause && (!finite(mock.stoppingAt) || cursor < mock.stoppingAt)) delete run.stopCause;
    return run;
  }

  function projection(input, cursor) {
    if (input && cursor === undefined && (input._isProjection || (finite(input.cursorSeconds) && input.now))) return input;
    return getRunAt(input, cursor);
  }

  function applyStopIntervention(projectedRun, intervention) {
    if (!intervention) return projectedRun;
    const stoppedAt = intervention.at;
    const captured = intervention.snapshot;
    if (!finite(stoppedAt) || !captured?.experiment || captured.cursorSeconds !== stoppedAt || instant(captured.now) === null) {
      throw new TypeError('A stop intervention requires its captured as-of snapshot and replay offset.');
    }
    if (projectedRun.experiment.id !== captured.experiment.id) throw new TypeError('The stop snapshot belongs to another experiment.');
    if (projectedRun.cursorSeconds < stoppedAt) return projectedRun;
    if (TERMINAL_EXPERIMENT_STATES.has(captured.experiment.state?.status) || captured.experiment.experimentOptions?.actionsMode === 'skip-all') {
      throw new TypeError('Only an active non-preview mock experiment can be stopped.');
    }

    // Start from the observations captured at the intervention. Projecting the
    // original scenario and replacing selected fields would leak future data
    // and falsely advance its successful-fetch timestamp.
    const run = clone(captured);
    run.now = projectedRun.now;
    run.cursorSeconds = projectedRun.cursorSeconds;
    run._isProjection = true;
    const completed = run.cursorSeconds >= stoppedAt + 30;
    const completedAt = iso(captured.now, 30);
    run.simulation = {
      kind: 'operator-stop', source: 'local replay', requestedAt: captured.now,
      asOf: run.now, cleanupDurationSeconds: 30,
      reportUnavailableReason: 'The original report does not describe this simulated interruption. No replacement report has been observed.'
    };
    if (completed) run.simulation.completedAt = completedAt;
    run.experiment.state = {
      status: completed ? 'stopped' : 'stopping',
      reason: completed ? 'Mock operator stop completed after outstanding cleanup.' : 'Mock operator stop requested. Outstanding post actions are completing.'
    };
    delete run.experiment.endTime;
    if (completed) run.experiment.endTime = completedAt;
    Object.values(run.experiment.actions || {}).forEach(action => {
      const status = action.state?.status;
      if (TERMINAL_ACTION_STATES.has(status)) return;
      if (!action.startTime || status === 'pending') {
        action.state = { status: 'cancelled', reason: 'The mock experiment stopped before this action started.' };
        delete action.startTime;
        delete action.endTime;
      } else {
        action.state = {
          status: completed ? 'stopped' : 'stopping',
          reason: completed ? 'Mock post-action cleanup completed.' : 'Waiting for mock post-action cleanup.'
        };
        delete action.endTime;
        if (completed) action.endTime = completedAt;
      }
    });
    delete run.experiment.experimentReport;
    delete run.stopCause;
    run.assessment = {
      status: 'inconclusive', summary: 'This intervention changes the scenario. No recovery conclusion is available.',
      rule: 'New post-intervention telemetry is required.', evidence: []
    };
    if (run.telemetry) run.telemetry.interrupted = true;
    run.evidence = (run.evidence || []).concat({
      id: `${run.key}-mock-stop-request-${stoppedAt}`, source: 'mock_control', type: 'stop-requested',
      occurredAt: captured.now, observedAt: captured.now,
      message: 'Operator requested a simulated stop. No AWS request was made.'
    });
    if (completed) run.evidence.push({
      id: `${run.key}-mock-stop-completed-${stoppedAt}`, source: 'mock_control', type: 'stop-completed',
      occurredAt: completedAt, observedAt: completedAt,
      message: 'Mock cleanup completed. Experiment stopped; workload recovery remains unassessed.'
    });
    return run;
  }

  function identity(record, index) {
    const info = record.targetInformation || {};
    const resourceArn = info.arn || info.resourceArn || info.resource_arn;
    let resourceKey = null; let accountId = null; let region = null; let displayName = null;
    let identityMethod = null; let identityScope = null;
    if (typeof resourceArn === 'string' && /^arn:[^:]+:[^:]+:[^:]*:[^:]*:.+/.test(resourceArn)) {
      resourceKey = resourceArn;
      identityMethod = 'arn'; identityScope = 'resource';
      const parts = resourceArn.split(':');
      region = parts[3] || null; accountId = parts[4] || null;
      const suffix = parts.slice(5).join(':');
      displayName = suffix.includes('/') ? suffix.slice(suffix.lastIndexOf('/') + 1) : suffix.slice(suffix.lastIndexOf(':') + 1);
    } else if (record.resourceType === 'aws:eks:pod' && info.cluster_arn && info.namespace && info.pod_name) {
      // Container choice belongs to the membership, not the pod identity. The
      // documented record has no pod UID, so this name key is scoped to a run;
      // it must not imply an identical pod incarnation across separate runs.
      resourceKey = [info.cluster_arn, info.namespace, info.pod_name].join('|');
      identityMethod = 'eks-pod-name'; identityScope = 'run';
      const parts = info.cluster_arn.split(':');
      region = parts[3] || null; accountId = parts[4] || null;
      displayName = `${info.namespace}/${info.pod_name}`;
    }
    return {
      key: resourceKey || `unidentified:${record.targetName}:${index}`, resourceKey,
      id: resourceKey ? displayName : null, arn: resourceArn || null,
      displayName: displayName || `Unidentified ${record.resourceType || 'resource'}`,
      accountId, region, resourceType: record.resourceType || null, identityKnown: Boolean(resourceKey),
      identityMethod, identityScope
    };
  }

  function selectedResources(input, actionName) {
    const run = projection(input);
    const actions = run.experiment.actions || {};
    const activeTargets = actionName ? new Set(Object.values((actions[actionName] || {}).targets || {})) : null;
    if (actionName && !actions[actionName]) return [];
    const byIdentity = new Map();
    (run.resolvedTargets || []).forEach((record, index) => {
      if (activeTargets && !activeTargets.has(record.targetName)) return;
      const resource = identity(record, index);
      const typeSafeKey = `${record.resourceType || 'unknown'}|${resource.key}`;
      const references = Object.entries(actions).filter(([, action]) => Object.values(action.targets || {}).includes(record.targetName));
      const names = references.map(([name]) => name);
      const bindings = references.flatMap(([name, action]) => Object.entries(action.targets || {}).filter(([, target]) => target === record.targetName).map(([slotName]) => ({ actionName: name, slotName, targetName: record.targetName })));
      if (byIdentity.has(typeSafeKey)) {
        const existing = byIdentity.get(typeSafeKey);
        existing.targetNames = unique(existing.targetNames.concat(record.targetName));
        existing.actionNames = unique(existing.actionNames.concat(names));
        existing.bindings.push(...bindings);
        existing.memberships.push(clone(record));
      } else {
        byIdentity.set(typeSafeKey, Object.assign(resource, { targetNames: [record.targetName], actionNames: names, bindings, memberships: [clone(record)], targetInformation: clone(record.targetInformation || {}) }));
      }
    });
    return [...byIdentity.values()].map(resource => Object.assign(resource, { actions: resource.actionNames, targetCount: resource.targetNames.length }));
  }

  function secondsBetween(end, start) {
    const last = instant(end); const first = instant(start);
    return last !== null && first !== null && last >= first ? (last - first) / 1000 : null;
  }

  function metricSeries(input) {
    const run = projection(input);
    const points = (run.telemetry?.points || []).filter(point => finite(point.offsetSeconds)).slice().sort((a, b) => a.offsetSeconds - b.offsetSeconds);
    const period = run.telemetry?.metricBinding?.period;
    const segments = [];
    let segment = []; let previous = null; let hasGaps = false;
    points.forEach(point => {
      const missing = !finite(point.value);
      const gap = previous && finite(period) && period > 0 && point.offsetSeconds - previous.offsetSeconds > period;
      if (missing || gap) {
        if (segment.length) segments.push(segment);
        segment = []; hasGaps = true;
      }
      if (!missing) segment.push(point);
      previous = point;
    });
    if (segment.length) segments.push(segment);
    const latestPoint = points.length && finite(points.at(-1).value) ? points.at(-1) : null;
    const measured = points.filter(point => point.offsetSeconds >= 0 && finite(point.value));
    return {
      segments, hasGaps, latestPoint,
      latestMetric: latestPoint ? latestPoint.value : null,
      peakMetric: measured.length ? Math.max(...measured.map(point => point.value)) : null
    };
  }

  function actionRows(input, cursor) {
    const run = projection(input, cursor);
    const schedule = new Map((run.schedule || []).map(item => [item.name, item]));
    return Object.entries(run.experiment.actions || {}).map(([name, action]) => {
      const status = action.state ? action.state.status : null;
      const terminal = TERMINAL_ACTION_STATES.has(status);
      const resources = selectedResources(run, name);
      const noTargets = Object.keys(action.targets || {}).length === 0;
      const complete = noTargets || Boolean(run.resolution && run.resolution.complete && resources.every(resource => resource.identityKnown));
      const item = schedule.get(name) || {};
      const observationTime = run.simulation?.asOf || run.observation?.snapshotAsOf || run.observation?.lastSuccessfulFetchAt;
      return {
        name, actionName: name, actionId: action.actionId, description: action.description || '',
        parameters: action.parameters || {}, targets: action.targets || {},
        status: status || 'unknown', state: action.state || {}, reason: action.state ? action.state.reason || '' : 'No state observation available.',
        startTime: action.startTime || null, endTime: action.endTime || null,
        dependencies: action.startAfter || [], startAfter: action.startAfter || [],
        dependencyStates: (action.startAfter || []).map(predecessor => ({ name: predecessor, status: run.experiment.actions[predecessor]?.state?.status || 'unknown' })),
        bindings: Object.entries(action.targets || {}).map(([slotName, targetName]) => ({ slotName, targetName })),
        resources, selectedResourceCount: complete ? resources.length : null,
        observedResourceCount: resources.filter(resource => resource.identityKnown).length,
        unidentifiedMembershipCount: resources.filter(resource => !resource.identityKnown).length, resourceCountComplete: complete,
        terminal, active: ACTIVE_ACTION_STATES.has(status),
        durationSeconds: secondsBetween(action.endTime, action.startTime),
        elapsedSeconds: action.endTime ? secondsBetween(action.endTime, action.startTime) : terminal ? null : secondsBetween(run.now, action.startTime),
        observedThroughTime: action.endTime || (terminal ? null : observationTime || null),
        observedElapsedSeconds: action.endTime ? secondsBetween(action.endTime, action.startTime) : terminal ? null : secondsBetween(observationTime, action.startTime),
        scheduledStartSeconds: finite(item.start) ? item.start : null,
        scheduledEndSeconds: finite(item.plannedEnd) ? item.plannedEnd : finite(item.end) ? item.end : null
      };
    });
  }

  function summarize(input, cursor) {
    const run = projection(input, cursor);
    const rows = actionRows(run);
    const status = run.experiment.state?.status || 'unknown';
    const counts = Object.fromEntries(ACTION_STATES.concat('unknown').map(state => [state, 0]));
    rows.forEach(row => { counts[ACTION_STATES.includes(row.status) ? row.status : 'unknown']++; });
    const hydrated = Boolean(run.observation && run.observation.hydrated && run.experiment.actions && typeof run.experiment.actions === 'object');
    const totalActions = hydrated ? rows.length : null;
    const terminalActions = rows.filter(row => row.terminal).length;
    const terminalFraction = totalActions ? terminalActions / totalActions : null;
    const resources = selectedResources(run);
    const complete = Boolean(run.resolution && run.resolution.complete && resources.every(resource => resource.identityKnown));
    const membershipCount = (run.resolvedTargets || []).length;
    const report = run.experiment.experimentReport;
    const isPreview = run.experiment.experimentOptions?.actionsMode === 'skip-all';
    const reportConfigured = Boolean(run.experiment.experimentReportConfiguration || report);
    const reportStatus = report?.state?.status || (isPreview ? 'not_generated' : reportConfigured ? 'unknown' : 'not_configured');
    const dependencyEdges = rows.flatMap(row => row.dependencies.map(from => ({ from, to: row.name, predecessor: from, successor: row.name })));
    const terminal = TERMINAL_EXPERIMENT_STATES.has(status);
    const metric = metricSeries(run);
    return {
      status, reason: run.experiment.state?.reason || '', isTerminal: terminal,
      totalActions, terminalActions, finishedActions: terminalActions,
      terminalFraction, terminalPercent: terminalFraction === null ? null : terminalFraction * 100,
      completedActions: counts.completed, skippedActions: counts.skipped, failedActions: counts.failed,
      cancelledActions: counts.cancelled, stoppedActions: counts.stopped,
      activeActions: counts.running + counts.initiating + counts.stopping,
      runningActions: counts.running, pendingActions: counts.pending, stoppingActions: counts.stopping, unknownActions: counts.unknown,
      counts, hydrated,
      elapsedSeconds: run.experiment.endTime ? secondsBetween(run.experiment.endTime, run.experiment.startTime) : terminal ? null : secondsBetween(run.now, run.experiment.startTime),
      preparationSeconds: secondsBetween(run.experiment.startTime, run.experiment.creationTime),
      selectedResourceCount: complete ? resources.length : null, uniqueResourceCount: complete ? resources.length : null,
      observedResourceCount: resources.filter(resource => resource.identityKnown).length, membershipCount, resourceCountComplete: complete,
      actionResourceAssociations: hydrated && rows.every(row => row.resourceCountComplete) ? rows.reduce((sum, row) => sum + row.resources.length, 0) : null,
      observedActionResourceAssociations: rows.reduce((sum, row) => sum + row.observedResourceCount, 0),
      unknownIdentityCount: resources.filter(resource => !resource.identityKnown).length,
      unidentifiedMembershipCount: resources.filter(resource => !resource.identityKnown).length,
      overlapResources: resources.filter(resource => resource.actionNames.length > 1),
      observedAccountCount: unique(resources.map(resource => resource.accountId).filter(Boolean)).length,
      configuredAccountCount: run.experiment.targetAccountConfigurationsCount ?? null,
      accountCount: run.experiment.targetAccountConfigurationsCount ?? null,
      isPreview, mode: run.experiment.experimentOptions?.actionsMode || 'unknown',
      reportStatus, reportArtifacts: report?.s3Reports || [],
      assessmentStatus: run.assessment?.status || 'not_assessed',
      freshnessSeconds: secondsBetween(run.now, run.observation?.lastSuccessfulFetchAt),
      latestMetric: metric.latestMetric,
      peakMetric: metric.peakMetric,
      evidenceCount: run.evidence.length, dependencyEdges, resources, rows, now: run.now
    };
  }

  function filterEvidence(input, options) {
    const run = projection(input);
    const opts = options || {};
    const query = String(opts.query || '').trim().toLowerCase();
    return (run.evidence || []).filter(event => {
      if (opts.source && opts.source !== 'all' && event.source !== opts.source) return false;
      if (opts.actionName && event.actionName !== opts.actionName) return false;
      if (query && ![event.message, event.type, event.source, event.actionName, event.accountId].filter(Boolean).join(' ').toLowerCase().includes(query)) return false;
      return true;
    }).sort((a, b) => instant(b.occurredAt) - instant(a.occurredAt));
  }

  function exportSnapshot(projectedRun) {
    if (!projectedRun?.experiment || !finite(projectedRun.cursorSeconds) || instant(projectedRun.now) === null) {
      throw new TypeError('Export requires an as-of projected run with cursorSeconds and now.');
    }
    // Do not replay the fixture here: the caller may have applied a local stop.
    const run = clone(projectedRun);
    const asOf = instant(run.now);
    const observed = value => {
      const timestamp = instant(value?.observedAt);
      return timestamp !== null && timestamp <= asOf;
    };
    run.evidence = (run.evidence || []).filter(observed);
    if (run.telemetry) {
      run.telemetry.points = (run.telemetry.points || []).filter(point =>
        finite(point.offsetSeconds) && point.offsetSeconds <= run.cursorSeconds &&
        (point.observedAt == null || observed(point))
      );
    }
    if (run.safety) {
      run.safety.history = (run.safety.history || []).filter(observed);
      if (!observed(run.safety)) {
        const latest = run.safety.history.reduce((previous, item) =>
          !previous || instant(item.observedAt) > instant(previous.observedAt) ? item : previous, null);
        run.safety.alarmState = latest ? latest.alarmState : null;
        run.safety.observedAt = latest ? latest.observedAt : null;
      }
      if (run.safety.lever && !observed(run.safety.lever)) delete run.safety.lever;
    }

    // Derive while projection identity and the full as-of shape are available.
    const derived = clone(summarize(run));
    derived.rows.forEach(row => {
      delete row.scheduledStartSeconds;
      delete row.scheduledEndSeconds;
    });
    ['_mock', 'schedule', '_isProjection', 'initialCursorSeconds', 'durationSeconds', 'executionDurationSeconds', 'stopCause'].forEach(key => delete run[key]);
    if (run.observation) delete run.observation.freezeAtSeconds;
    return {
      schema: 'fis-observatory/mock-snapshot/v1', synthetic: true,
      replay: { offsetSeconds: run.cursorSeconds, asOf: run.now },
      derived, run
    };
  }

  function validateFixtures(fixtures) {
    const runs = Array.isArray(fixtures) ? fixtures : fixtures.runs || [];
    const errors = []; const warnings = []; let assertions = 0;
    function check(condition, message) { assertions++; if (!condition) errors.push(message); }
    const keys = new Set();
    runs.forEach(run => {
      check(!keys.has(run.key), `${run.key}: duplicate run key`); keys.add(run.key);
      check(instant(run.experiment.startTime) !== null, `${run.key}: invalid startTime`);
      const actions = run.experiment.actions || {};
      const targets = run.experiment.targets || {};
      const schedule = new Map((run.schedule || []).map(item => [item.name, item]));
      const multiAccount = run.experiment.experimentOptions?.accountTargeting === 'multi-account';
      const configuredAccounts = new Set((run.accounts || []).map(account => account.accountId));
      const owningAccount = run.experiment.arn?.split(':')[4];
      const eligibleAccounts = multiAccount ? configuredAccounts : new Set([owningAccount]);
      check(schedule.size === (run.schedule || []).length, `${run.key}: duplicate replay schedule name`);
      check(run.experiment.targetAccountConfigurationsCount === (multiAccount ? configuredAccounts.size : 0), `${run.key}: target account configuration count mismatch`);
      const visiting = new Set(); const visited = new Set();
      function visit(name) {
        if (visiting.has(name)) { errors.push(`${run.key}: dependency cycle at ${name}`); return; }
        if (visited.has(name)) return;
        visiting.add(name);
        (actions[name]?.startAfter || []).forEach(predecessor => { if (actions[predecessor]) visit(predecessor); });
        visiting.delete(name); visited.add(name);
      }
      Object.entries(actions).forEach(([name, action]) => {
        check(schedule.has(name), `${run.key}/${name}: no replay schedule`);
        if (fixtures.catalog) check(Boolean(fixtures.catalog[action.actionId]), `${run.key}/${name}: unknown catalog action`);
        Object.entries(action.parameters || {}).forEach(([parameter, value]) => check(typeof value === 'string', `${run.key}/${name}: parameter ${parameter} must be a string`));
        Object.entries(fixtures.catalog?.[action.actionId]?.parameters || {}).forEach(([parameter, definition]) => {
          if (definition.required) check(typeof action.parameters?.[parameter] === 'string' && action.parameters[parameter].length > 0, `${run.key}/${name}: missing required parameter ${parameter}`);
        });
        (action.startAfter || []).forEach(predecessor => check(Boolean(actions[predecessor]), `${run.key}/${name}: missing predecessor ${predecessor}`));
        Object.entries(action.targets || {}).forEach(([slot, targetName]) => {
          check(Boolean(targets[targetName]), `${run.key}/${name}: missing target ${targetName}`);
          const expected = fixtures.catalog?.[action.actionId]?.targets?.[slot]?.resourceType;
          if (fixtures.catalog) check(Boolean(expected), `${run.key}/${name}: unknown target slot ${slot}`);
          if (expected && targets[targetName]) check(expected === targets[targetName].resourceType, `${run.key}/${name}: resource type mismatch`);
        });
        const item = schedule.get(name);
        if (item && item.start !== null) {
          check(item.end >= item.start, `${run.key}/${name}: action ends before start`);
          if (finite(run._mock?.resolutionEndedAt)) check(item.start >= run._mock.resolutionEndedAt, `${run.key}/${name}: starts before target resolution ends`);
          (action.startAfter || []).forEach(predecessor => {
            const prev = schedule.get(predecessor);
            if (prev && prev.start !== null) check(item.start >= prev.end, `${run.key}/${name}: starts before predecessor ends`);
          });
        }
        visit(name);
      });
      (run.resolvedTargets || []).forEach((record, index) => {
        check(Boolean(targets[record.targetName]), `${run.key}: orphan membership ${record.targetName}`);
        if (targets[record.targetName]) check(record.resourceType === targets[record.targetName].resourceType, `${run.key}: membership resource type mismatch for ${record.targetName}`);
        const accountId = identity(record, index).accountId;
        if (accountId) check(eligibleAccounts.has(accountId), `${run.key}: selected account ${accountId} is not configured`);
      });
      const eventIds = new Set();
      (run.evidence || []).forEach(event => {
        check(!eventIds.has(event.id), `${run.key}: duplicate evidence id ${event.id}`); eventIds.add(event.id);
        const occurredAt = instant(event.occurredAt); const observedAt = instant(event.observedAt);
        check(occurredAt !== null && observedAt !== null, `${run.key}: invalid evidence timestamp for ${event.id}`);
        if (occurredAt !== null && observedAt !== null) check(observedAt >= occurredAt, `${run.key}: evidence observed before occurrence`);
        if (event.actionName) check(Boolean(actions[event.actionName]), `${run.key}: orphan evidence action ${event.actionName}`);
      });
      if (run.experiment.experimentOptions.actionsMode === 'skip-all') check(run.schedule.every(item => item.outcome === 'skipped'), `${run.key}: preview contains non-skipped actions`);
      if (!run.resolution?.complete) warnings.push(`${run.key}: target collection intentionally incomplete`);
    });
    return { valid: errors.length === 0, errors, warnings, assertions, runCount: runs.length };
  }

  return { getRunAt, applyStopIntervention, summarize, actionRows, selectedResources, metricSeries, filterEvidence, exportSnapshot, validateFixtures, ACTION_STATES, TERMINAL_ACTION_STATES: [...TERMINAL_ACTION_STATES], TERMINAL_EXPERIMENT_STATES: [...TERMINAL_EXPERIMENT_STATES] };
}));
