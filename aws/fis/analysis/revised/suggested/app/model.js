/* Pure projection for the synthetic assessment console. This is not a runner,
 * scheduler, expression evaluator, API client, or cloud adapter. */
(function (root, factory) {
  const value = factory();
  if (typeof module === 'object' && module.exports) module.exports = value;
  else root.AssessmentModel = value;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const PROJECTION_VERSION = 'assessment-ui-projection/1';
  const VERDICTS = new Set(['passed', 'failed', 'inconclusive']);
  const TERMINAL_DISPOSITIONS = new Set(['none', 'terminal']);
  const copy = value => value === undefined ? undefined : JSON.parse(JSON.stringify(value));
  const timestamp = value => typeof value === 'string' && Number.isFinite(Date.parse(value)) ? Date.parse(value) : null;
  const instant = (base, seconds) => new Date(Date.parse(base) + seconds * 1000).toISOString();
  const last = values => values.length ? values[values.length - 1] : null;
  const secondsBetween = (end, start) => timestamp(end) === null || timestamp(start) === null ? null : Math.max(0, (timestamp(end) - timestamp(start)) / 1000);
  const isSource = kind => kind === 'provider' || kind === 'receiver';
  const unresolved = effect => effect.requiresFinalization !== false && !TERMINAL_DISPOSITIONS.has(effect.disposition);
  const activeAttempt = step => step && last(step.attempts) && last(step.attempts).phase !== 'finished' ? last(step.attempts) : null;

  function getStep(snapshot, stepKey) {
    return snapshot.steps.find(step => step.stepKey === stepKey) || null;
  }

  function stepFromDefinition(definition, runId) {
    return Object.assign(copy(definition), {
      runId, ref: {runId, stepKey: definition.stepKey}, phase: 'pending', outcome: null,
      skipReason: null, startedAt: null, endedAt: null, attempts: [], check: null
    });
  }

  function startAttempt(snapshot, step, event, at, simulation) {
    if (!step || step.phase === 'finished' || activeAttempt(step)) return;
    const attemptNo = event.attemptNo || step.attempts.length + 1;
    const attempt = {
      runId: snapshot.runId, stepKey: step.stepKey, attemptNo,
      ref: {runId: snapshot.runId, stepKey: step.stepKey, attemptNo},
      phase: 'running', outcome: null, startedAt: at, endedAt: null,
      dispatchKey: event.dispatchKey || snapshot.runId + ':' + step.stepKey + ':' + attemptNo,
      resolvedInputs: copy(event.resolvedInputs || {}), resolvedInputsDigest: event.resolvedInputsDigest || null,
      outputs: null, error: null,
      externalRefs: [], checkpoint: copy(event.checkpoint || null), check: null,
      evidenceIds: [], synthetic: true
    };
    if (simulation) attempt.provenance = 'local-cancellation-simulation';
    step.attempts.push(attempt);
    step.phase = 'running';
    step.startedAt = step.startedAt || at;
  }

  function finishAttempt(step, event, at) {
    const attempt = activeAttempt(step);
    if (!attempt) return; // A sealed attempt never acquires later output or a new result.
    attempt.phase = 'finished';
    attempt.outcome = event.outcome;
    attempt.endedAt = at;
    attempt.outputs = copy(event.outputs === undefined ? {} : event.outputs);
    attempt.error = copy(event.error || null);
    attempt.reason = event.reason || null;
    step.phase = 'finished';
    step.outcome = event.outcome;
    step.endedAt = at;
  }

  function missingCheck(step, final) {
    const settled = step && step.phase === 'finished';
    return {
      verdict: final || settled ? 'inconclusive' : 'pending',
      reasonCode: step && step.skipReason || (settled ? 'CHECK_NOT_ESTABLISHED' : 'AWAITING_EVALUATION'),
      summary: final || settled ? 'The required claim was not established by an evaluated check.' : 'Waiting for this check and its evidence.',
      actual: null, expected: null, evidenceIds: [], evaluatedThrough: null,
      collection: 'unavailable', coverage: 'unknown', proof: null, window: null
    };
  }

  function criterionFor(snapshot, stepKey, required) {
    const step = getStep(snapshot, stepKey);
    const check = step && step.check ? copy(step.check) : missingCheck(step, snapshot.execution.phase === 'finished');
    if (check.verdict !== 'pending' && !VERDICTS.has(check.verdict)) {
      check.sourceVerdict = check.verdict;
      check.verdict = 'inconclusive';
      check.reasonCode = 'UNKNOWN_CHECK_VERDICT';
      check.summary = 'An unrecognized verdict cannot establish a passing claim.';
    }
    return Object.assign({stepKey, label: step ? step.label : stepKey, required}, check);
  }

  function deriveAssessment(snapshot) {
    snapshot.criteria = snapshot.admission.requiredCriteria.map(key => criterionFor(snapshot, key, true));
    snapshot.preconditions = snapshot.steps.filter(step => step.assessmentRole === 'precondition').map(step => criterionFor(snapshot, step.stepKey, false));
    const criteria = snapshot.criteria;
    const count = verdict => criteria.filter(criterion => criterion.verdict === verdict).length;
    const requiredCount = criteria.length;
    const passedCount = count('passed');
    const failedCount = count('failed');
    return {
      verdict: requiredCount === 0 ? 'not_evaluated' : failedCount ? 'failed' : passedCount === requiredCount ? 'passed' : 'inconclusive',
      final: snapshot.execution.phase === 'finished', requiredCount, passedCount, failedCount,
      inconclusiveCount: count('inconclusive'), pendingCount: count('pending')
    };
  }

  function deriveFinalization(snapshot) {
    const finalizers = snapshot.steps.filter(step => step.graph === 'finalizer');
    const begun = Boolean(snapshot.finalization.startedAt) || ['finalizing', 'finished'].includes(snapshot.execution.phase);
    const unresolvedEffects = begun ? snapshot.effects.filter(unresolved).map(copy) : [];
    const completedCount = finalizers.filter(step => step.outcome === 'succeeded').length;
    const settledCount = finalizers.filter(step => step.phase === 'finished').length;
    let status = 'not_started';
    if (begun) status = snapshot.execution.phase === 'finished' ? (completedCount === finalizers.length && !unresolvedEffects.length ? 'complete' : 'incomplete') : 'running';
    return {
      status, requiredCount: finalizers.length, completedCount, settledCount,
      unresolvedEffects, startedAt: snapshot.finalization.startedAt || null,
      endedAt: snapshot.execution.phase === 'finished' ? snapshot.execution.endedAt : null,
      protectiveHold: unresolvedEffects.some(effect => effect.requiresHold)
    };
  }

  function deriveExecution(snapshot) {
    const reasons = [];
    if (snapshot.effects.some(unresolved)) reasons.push('EXTERNAL_STATE_UNCONFIRMED');
    if (snapshot.steps.some(step => step.outcome === 'failed')) reasons.push('OPERATION_FAILED');
    if (snapshot.execution.termination === 'timed_out' || snapshot.steps.some(step => step.outcome === 'timed_out')) reasons.push('DEADLINE_EXCEEDED');
    if (snapshot.cancellation) reasons.push('CANCELLATION_ACCEPTED');
    if (snapshot.steps.some(step => step.skipReason === 'PRECONDITION_NOT_PASSED')) reasons.push('PRECONDITION_BLOCKED');
    const outcomes = {
      EXTERNAL_STATE_UNCONFIRMED: 'indeterminate', OPERATION_FAILED: 'failed',
      DEADLINE_EXCEEDED: 'timed_out', CANCELLATION_ACCEPTED: 'cancelled', PRECONDITION_BLOCKED: 'blocked'
    };
    return {outcome: reasons.length ? outcomes[reasons[0]] : 'succeeded', reasons};
  }

  function refresh(snapshot, sealed) {
    const assessment = deriveAssessment(snapshot);
    const finalization = deriveFinalization(snapshot);
    snapshot.assessment = sealed ? copy(sealed.assessment) : assessment;
    snapshot.finalization = sealed ? copy(sealed.finalization) : finalization;
    if (snapshot.execution.phase === 'finished') {
      const conclusion = sealed ? sealed.execution : deriveExecution(snapshot);
      snapshot.execution.outcome = conclusion.outcome;
      snapshot.execution.reasons = copy(conclusion.reasons);
    } else {
      snapshot.execution.outcome = null;
      snapshot.execution.reasons = [];
    }
    const observations = snapshot.evidence.filter(record => isSource(record.sourceKind)).map(record => ({source: record.source, observedAt: record.observedAt}));
    snapshot.effects.filter(effect => effect.observationKind === 'provider').forEach(effect => observations.push({source: effect.provider, observedAt: effect.observedAt}));
    const known = observations.filter(record => timestamp(record.observedAt) !== null && timestamp(record.observedAt) <= timestamp(snapshot.now));
    const bySource = {};
    const sourceLabels = {'aws/fis': 'AWS FIS', 'aws/cloudwatch.logs': 'CloudWatch Logs Insights'};
    known.forEach(record => {
      // Evidence labels and external-reference namespaces identify the same
      // supported authority; keep its latest observed fact in one freshness row.
      const source = sourceLabels[record.source] || record.source;
      if (!bySource[source] || timestamp(record.observedAt) > timestamp(bySource[source])) bySource[source] = record.observedAt;
    });
    const sourceTimes = Object.values(bySource).sort((a, b) => timestamp(a) - timestamp(b));
    const latest = last(sourceTimes);
    snapshot.observation = {
      lastSourceObservationAt: latest, ageSeconds: latest ? secondsBetween(snapshot.now, latest) : null,
      status: latest ? 'observed' : 'unknown',
      bySource: Object.entries(bySource).map(([source, observedAt]) => ({source, observedAt, ageSeconds: secondsBetween(snapshot.now, observedAt)})),
      sourceFrozenAt: snapshot.simulation ? snapshot.simulation.sourceFrozenAt : null
    };
    return snapshot;
  }

  function projectRun(fixture, cursorSeconds) {
    if (!fixture || !fixture.revision || !Array.isArray(fixture._events)) throw new TypeError('A complete synthetic trace is required.');
    const requested = cursorSeconds === undefined ? fixture.initialCursorSeconds : Number(cursorSeconds);
    if (!Number.isFinite(requested)) throw new TypeError('Replay cursor must be a finite number.');
    const cursor = Math.max(0, Math.min(fixture.durationSeconds, requested));
    const snapshot = {
      key: fixture.key, runId: fixture.runId, title: fixture.title, description: fixture.description,
      service: fixture.service, environment: fixture.environment, region: fixture.region,
      accounts: copy(fixture.accounts), owner: fixture.owner, synthetic: true,
      createdAt: fixture.createdAt, now: instant(fixture.createdAt, cursor), cursorSeconds: cursor,
      durationSeconds: fixture.durationSeconds, projectionVersion: PROJECTION_VERSION,
      reducerVersion: fixture.revision.reducerVersion, asOfSequence: 0,
      scenario: copy(fixture.scenario), revision: copy(fixture.revision),
      scenarioRevisionId: fixture.revision.scenarioRevisionId,
      admission: copy(fixture.admission),
      execution: {phase: 'queued', outcome: null, reason: null, reasons: [], startedAt: null, endedAt: null, termination: null},
      steps: fixture.revision.definitions.map(definition => stepFromDefinition(definition, fixture.runId)),
      criteria: [], preconditions: [], evidence: [], effects: [],
      finalization: {startedAt: null}, cancellation: null
    };
    let sealed = null;
    const events = fixture._events.map((event, order) => ({event, order})).sort((a, b) => a.event.at - b.event.at || a.order - b.order);
    for (const {event} of events) {
      if (event.at > cursor) break;
      const at = instant(fixture.createdAt, event.at);
      // The acquisition time, not the source's earlier event time, controls visibility.
      if (event.record && timestamp(event.record.observedAt) > timestamp(snapshot.now)) continue;
      snapshot.asOfSequence += 1;
      const step = event.stepKey ? getStep(snapshot, event.stepKey) : null;
      if (event.kind === 'evidence') {
        const record = copy(event.record);
        const producer = activeAttempt(getStep(snapshot, record.stepKey));
        if (producer) {
          record.producer = copy(producer.ref);
          producer.evidenceIds.push(record.evidenceId);
        }
        snapshot.evidence.push(record);
      } else if (event.kind === 'effect') {
        const record = copy(event.record);
        const previous = snapshot.effects.findIndex(effect => effect.originEffectKey === record.originEffectKey);
        if (previous < 0) snapshot.effects.push(record); else snapshot.effects[previous] = record;
        const observer = activeAttempt(getStep(snapshot, event.observedByStepKey));
        if (observer) observer.externalRefs.push(copy(record));
      } else if (!sealed && event.kind === 'step_start') {
        startAttempt(snapshot, step, event, at);
      } else if (!sealed && event.kind === 'step_finish') {
        finishAttempt(step, event, at);
      } else if (!sealed && event.kind === 'step_skip' && step && step.phase === 'pending') {
        step.phase = 'finished'; step.outcome = 'skipped'; step.skipReason = event.reasonCode; step.endedAt = at;
      } else if (!sealed && event.kind === 'check_result') {
        const attempt = activeAttempt(step);
        if (attempt && !attempt.check) { attempt.check = copy(event.check); step.check = copy(event.check); }
      } else if (!sealed && event.kind === 'cancellation' && !snapshot.cancellation) {
        snapshot.cancellation = copy(event.intent);
      } else if (!sealed && event.kind === 'run_phase') {
        snapshot.execution.phase = event.phase;
        snapshot.execution.reason = event.reason || null;
        snapshot.execution.termination = event.termination || snapshot.execution.termination;
        if (event.phase === 'running') snapshot.execution.startedAt = snapshot.execution.startedAt || at;
        if (event.phase === 'finalizing') snapshot.finalization.startedAt = snapshot.finalization.startedAt || at;
        if (event.phase === 'finished') {
          snapshot.execution.endedAt = at;
          refresh(snapshot, null);
          sealed = {execution: copy(snapshot.execution), assessment: copy(snapshot.assessment), finalization: copy(snapshot.finalization)};
        }
      }
    }
    return refresh(snapshot, sealed);
  }

  function summarize(snapshot) {
    return {
      phase: snapshot.execution.phase, outcome: snapshot.execution.outcome,
      executionLabel: snapshot.execution.outcome || snapshot.execution.phase,
      elapsedSeconds: secondsBetween(snapshot.execution.endedAt || snapshot.now, snapshot.execution.startedAt),
      totalSteps: snapshot.steps.length, finishedSteps: snapshot.steps.filter(step => step.phase === 'finished').length,
      activeSteps: snapshot.steps.filter(step => step.phase === 'running').length,
      requiredCriteria: snapshot.assessment.requiredCount, passedCriteria: snapshot.assessment.passedCount,
      failedCriteria: snapshot.assessment.failedCount, pendingCriteria: snapshot.assessment.pendingCount,
      inconclusiveCriteria: snapshot.assessment.inconclusiveCount, evidenceCount: snapshot.evidence.length,
      sourceAgeSeconds: snapshot.observation.ageSeconds, finalizationStatus: snapshot.finalization.status,
      unresolvedEffects: snapshot.finalization.unresolvedEffects.length,
      protectiveHold: snapshot.finalization.protectiveHold,
      canCancel: snapshot.execution.phase !== 'finished' && !snapshot.cancellation
    };
  }

  function filterEvidence(snapshot, options) {
    const {source, query, stepKey} = options || {};
    const needle = (query || '').trim().toLowerCase();
    return snapshot.evidence.filter(record => (!source || source === 'all' || record.source === source || record.sourceKind === source) &&
      (!stepKey || stepKey === 'all' || record.stepKey === stepKey) &&
      (!needle || JSON.stringify(record).toLowerCase().includes(needle)));
  }

  function exportSnapshot(snapshot) {
    // Allow-list: no fixture object, future event stream, replay duration or command cache.
    const keys = ['runId', 'title', 'service', 'environment', 'region', 'accounts', 'createdAt', 'now',
      'projectionVersion', 'reducerVersion', 'asOfSequence', 'scenario', 'revision', 'scenarioRevisionId',
      'admission', 'execution', 'steps', 'criteria', 'preconditions', 'evidence', 'effects', 'observation',
      'assessment', 'finalization', 'cancellation', 'simulation'];
    const result = {schemaVersion: 'assessment-observed-snapshot/1', synthetic: true,
      provenance: 'Synthetic observed projection; no cloud requests or live adapter execution.', observationCutoff: snapshot.now};
    keys.forEach(key => { if (snapshot[key] !== undefined) result[key] = copy(snapshot[key]); });
    return result;
  }

  function requestCancellation(snapshot, command) {
    const {clientToken, reason} = command || {};
    if (typeof clientToken !== 'string' || !clientToken.trim() || typeof reason !== 'string' || !reason.trim()) {
      return {receipt: {accepted: false, httpStatus: 400, code: 'INVALID_CANCELLATION', runId: snapshot.runId}, intervention: null};
    }
    const existing = snapshot.cancellation;
    if (existing && existing.clientToken === clientToken) {
      if (existing.reason !== reason) return {receipt: {accepted: false, httpStatus: 409, code: 'IDEMPOTENCY_CONFLICT', runId: snapshot.runId}, intervention: null};
      return {receipt: copy(existing.receipt), intervention: null};
    }
    if (snapshot.execution.phase === 'finished') {
      return {receipt: {accepted: false, httpStatus: 200, code: 'RUN_ALREADY_FINISHED', runId: snapshot.runId, outcome: snapshot.execution.outcome}, intervention: null};
    }
    if (existing) return {receipt: Object.assign(copy(existing.receipt), {joinedExistingIntent: true}), intervention: null};
    const receipt = {accepted: true, httpStatus: 202, commandId: 'demo_cancel_' + snapshot.runId + '_' + snapshot.cursorSeconds,
      runId: snapshot.runId, acceptedAt: snapshot.now, synthetic: true};
    return {
      receipt,
      intervention: {runId: snapshot.runId, atSeconds: snapshot.cursorSeconds, acceptedAt: snapshot.now,
        clientToken, reason, receipt: copy(receipt), capturedSnapshot: copy(snapshot), localBudgetSeconds: 45}
    };
  }

  function localControlEvidence(snapshot, at, suffix, title, summary) {
    return {
      evidenceId: 'ev_local_' + snapshot.runId + '_' + suffix, runId: snapshot.runId, stepKey: null,
      source: 'Local cancellation simulation', sourceKind: 'runtime', kind: 'control', title, summary,
      occurredAt: at, observedAt: at, collection: 'complete', coverage: 'not_applicable',
      sourceRecordId: 'local/' + snapshot.runId + '/' + suffix,
      schemaRef: null, contentDigest: null,
      value: {synthetic: true, cloudRequestsIssued: 0, remoteCessationEstablished: false},
      scope: {runId: snapshot.runId}, window: null, synthetic: true,
      provenance: 'local-cancellation-simulation'
    };
  }

  function finalizerInputs(snapshot, step) {
    // Resolve only the static ConnectionRef/StepRef forms in these retained demo
    // definitions. This is not a CEL interpreter and dispatches no operation.
    const resolve = value => {
      if (Array.isArray(value)) return value.map(resolve);
      if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, resolve(item)]));
      if (typeof value !== 'string') return value;
      const binding = value.match(/^\$\{\{ bindings\.([a-z_]+) \}\}$/);
      if (binding) return copy(snapshot.admission.bindings[binding[1]]);
      const reference = value.match(/^\$\{\{ steps\.([a-z_]+)\.ref \}\}$/);
      if (reference) return {runId: snapshot.runId, stepKey: reference[1]};
      if (value.includes('${{')) throw new TypeError('Unsupported expression in local mock finalizer.');
      return value;
    };
    return resolve(step.with);
  }

  function applyCancellation(projectedRun, intervention) {
    if (!intervention || projectedRun.cursorSeconds < intervention.atSeconds) return copy(projectedRun);
    if (projectedRun.runId !== intervention.runId) throw new TypeError('Cancellation belongs to another Run.');
    const snapshot = copy(intervention.capturedSnapshot);
    const at = intervention.acceptedAt;
    const deadlineSeconds = intervention.atSeconds + intervention.localBudgetSeconds;
    const deadline = instant(snapshot.createdAt, deadlineSeconds);
    const elapsed = projectedRun.cursorSeconds - intervention.atSeconds;
    const expired = elapsed >= intervention.localBudgetSeconds;
    snapshot.now = projectedRun.now;
    snapshot.cursorSeconds = projectedRun.cursorSeconds;
    snapshot.durationSeconds = Math.max(projectedRun.durationSeconds, deadlineSeconds);
    snapshot.cancellation = {commandId: intervention.receipt.commandId, clientToken: intervention.clientToken,
      reason: intervention.reason, acceptedAt: at, principal: 'synthetic/operator',
      source: 'local-cancellation-simulation', receipt: copy(intervention.receipt)};
    snapshot.simulation = {mode: 'local-cancellation', sourceFrozenAt: at,
      localBudgetSeconds: intervention.localBudgetSeconds, deadline, cloudRequestsIssued: 0,
      description: 'Source observations are frozen at the request. Only explicit local control facts advance; remote cessation is never invented.'};
    snapshot.evidence.push(localControlEvidence(snapshot, at, 'cancel_' + intervention.atSeconds,
      'Local cancellation intent accepted', 'Further main dispatch is fenced in this mock branch. Existing remote effects retain their last observed states.'));
    snapshot.asOfSequence += 1;
    snapshot.steps.filter(step => step.graph === 'main' && step.phase !== 'finished').forEach(step => {
      if (step.phase === 'running') {
        activeAttempt(step).terminalProvenance = 'local-cancellation-simulation';
        finishAttempt(step, {outcome: 'cancelled', outputs: {}, reason: 'Local mock dispatch fenced; remote effect remains independently tracked.'}, at);
      }
      else { step.phase = 'finished'; step.outcome = 'skipped'; step.skipReason = 'RUN_CANCELLED'; step.endedAt = at; }
    });
    snapshot.execution.phase = 'finalizing';
    snapshot.execution.outcome = null;
    snapshot.execution.endedAt = null;
    snapshot.execution.reason = 'Cancellation is accepted. Required finalizers await independent remote evidence.';
    snapshot.finalization.startedAt = snapshot.finalization.startedAt || at;
    const finalizers = snapshot.steps.filter(step => step.graph === 'finalizer');
    // Only dependency-ready finalizers acquire a local attempt. No remote call is simulated.
    finalizers.filter(step => step.phase === 'pending' && step.needs.every(key => getStep(snapshot, key).phase === 'finished')).forEach(step => {
      startAttempt(snapshot, step, {resolvedInputs: finalizerInputs(snapshot, step), checkpoint: {mode: 'local-only', remoteRequestsIssued: 0}}, at, true);
    });
    if (expired) {
      const pendingEffects = snapshot.effects.filter(unresolved);
      const noDispatch = snapshot.steps.filter(step => step.graph === 'main').every(step => step.attempts.length === 0);
      finalizers.forEach(step => {
        if (step.phase === 'finished') return;
        if (noDispatch) {
          if (step.phase === 'pending') startAttempt(snapshot, step, {resolvedInputs: finalizerInputs(snapshot, step)}, deadline, true);
          finishAttempt(step, {outcome: 'succeeded', outputs: {remoteDisposition: 'none', step: copy(activeAttempt(step).resolvedInputs.step), reasonCode: 'NOT_DISPATCHED', evidenceIds: []}}, deadline);
        } else if (step.phase === 'running') {
          activeAttempt(step).terminalProvenance = 'local-cancellation-simulation';
          finishAttempt(step, {outcome: 'timed_out', outputs: {}, error: {code: 'MOCK_RECONCILIATION_LIMIT', category: 'simulation', message: 'No additional source observations are available in this local branch.', retryable: false}}, deadline);
        } else {
          step.phase = 'finished'; step.outcome = 'skipped'; step.skipReason = 'MOCK_FINALIZATION_BUDGET_EXHAUSTED'; step.endedAt = deadline;
        }
      });
      snapshot.execution.phase = 'finished';
      snapshot.execution.endedAt = deadline;
      snapshot.execution.reason = pendingEffects.length ? 'The mock control budget expired with unresolved external effects. Source state is unchanged.' : noDispatch ? 'Cancellation completed before any operation was dispatched.' : 'The mock control budget ended without new cleanup observations.';
      snapshot.evidence.push(localControlEvidence(snapshot, deadline, 'budget_' + intervention.atSeconds,
        'Local mock budget ended', snapshot.execution.reason));
      snapshot.asOfSequence += 1;
    }
    return refresh(snapshot, null);
  }

  return {projectRun, summarize, filterEvidence, getStep, exportSnapshot, requestCancellation, applyCancellation};
}));
