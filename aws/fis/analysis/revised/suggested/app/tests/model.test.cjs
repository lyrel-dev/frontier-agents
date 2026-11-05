'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const {createHash} = require('node:crypto');
const {spawnSync} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const Fixtures = require('../fixtures.js');
const Model = require('../model.js');

const fixture = key => Fixtures.runs.find(run => run.key === key);
const view = (key, time) => Model.projectRun(fixture(key), time);
const step = (snapshot, key) => Model.getStep(snapshot, key);
const clone = value => JSON.parse(JSON.stringify(value));
const canonical = value => Array.isArray(value) ? value.map(canonical) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, canonical(value[key])])) : value;
const digest = value => 'sha256:' + createHash('sha256').update(JSON.stringify(canonical(value))).digest('hex');
const seconds = (run, at) => (Date.parse(at) - Date.parse(run.createdAt)) / 1000;
const command = {clientToken: 'demo-test-cancel', reason: 'Operator requests bounded reconciliation.'};
const cancellationAt = (key, at, later) => {
  const before = view(key, at);
  const result = Model.requestCancellation(before, command);
  return {before, result, after: Model.applyCancellation(view(key, later), result.intervention)};
};

test('the six fixtures have coherent Scenario, Revision, Run, StepRun, Attempt and Evidence identities', () => {
  assert.equal(Fixtures.runs.length, 6);
  assert.equal(new Set(Fixtures.runs.map(run => run.runId)).size, 6);
  for (const run of Fixtures.runs) {
    const snapshot = Model.projectRun(run, run.durationSeconds);
    assert.equal(snapshot.scenario.scenarioId, snapshot.revision.scenarioId);
    assert.equal(snapshot.scenarioRevisionId, snapshot.revision.scenarioRevisionId);
    assert.equal(snapshot.admission.revisionDigest, snapshot.revision.digest);
    assert.equal(new Set(snapshot.steps.map(item => item.stepKey)).size, snapshot.steps.length);
    for (const item of snapshot.steps) {
      assert.deepEqual(item.ref, {runId: run.runId, stepKey: item.stepKey});
      for (const attempt of item.attempts) {
        assert.deepEqual(attempt.ref, {runId: run.runId, stepKey: item.stepKey, attemptNo: attempt.attemptNo});
        assert.equal(attempt.runId, run.runId);
        assert.equal(attempt.stepKey, item.stepKey);
      }
    }
    assert.equal(new Set(snapshot.evidence.map(record => record.evidenceId)).size, snapshot.evidence.length);
    for (const record of snapshot.evidence) {
      assert.equal(record.runId, run.runId);
      if (record.producer) assert.ok(step(snapshot, record.producer.stepKey).attempts.some(attempt => attempt.attemptNo === record.producer.attemptNo));
    }
    for (const effect of snapshot.effects) {
      assert.equal(effect.originAttempt.runId, run.runId);
      assert.equal(effect.originAttempt.stepKey, effect.stepKey);
      assert.ok(step(snapshot, effect.stepKey).attempts.some(attempt => attempt.attemptNo === effect.originAttempt.attemptNo));
    }
  }
});

test('all 87 recorded operation inputs and successful outputs satisfy their retained pinned schemas', () => {
  const catalogue = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../../../docs/suggested/operation-catalog.json'), 'utf8'));
  const script = String.raw`
import json,sys
from jsonschema import Draft202012Validator,FormatChecker
data=json.load(sys.stdin); catalog=data['catalogue']; checked=0
for run in data['runs']:
 defs={d['stepKey']:d for d in run['revision']['definitions']}
 locks={d['uses']:d for d in run['revision']['operations']}
 for event in run['_events']:
  if event['kind']=='step_start': direction,key='inputSchema','resolvedInputs'
  elif event['kind']=='step_finish' and event['outcome']=='succeeded': direction,key='outputSchema','outputs'
  else: continue
  alias=defs[event['stepKey']]['uses']
  schema=catalog['revisions'][locks[alias]['implementationDigest']][direction]
  errors=list(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(event[key]))
  if errors: raise AssertionError(str((run['key'],event['stepKey'],direction,[e.message for e in errors])))
  checked+=1
print(checked)
`;
  const result = spawnSync('python3', ['-c', script], {input: JSON.stringify({catalogue, runs: Fixtures.runs}), encoding: 'utf8', maxBuffer: 4 * 1024 * 1024});
  assert.equal(result.status, 0, result.stderr || result.error && result.error.message);
  assert.equal(Number(result.stdout.trim()), 87);
});

test('admission and attempt digests bind actual values; declared connection capabilities are retained', () => {
  for (const run of Fixtures.runs) {
    assert.equal(run.admission.inputsDigest, digest(run.admission.inputs));
    const required = run.revision.yaml.match(/aws: \{kind: connection, capability: ([a-z_]+)\}/)[1];
    assert.ok(run.admission.bindings.aws.capabilities.includes(required));
    const snapshot = Model.projectRun(run, run.durationSeconds);
    for (const item of snapshot.steps) for (const attempt of item.attempts) assert.equal(attempt.resolvedInputsDigest, digest(attempt.resolvedInputs));
    for (const evidence of snapshot.evidence) assert.equal(evidence.contentDigest, digest(evidence.value));
  }
});

test('the same operation may have independent named step identities and separate results', () => {
  const snapshot = view('alarm-late');
  const transition = step(snapshot, 'alarm_transition');
  const receipt = step(snapshot, 'notification_received');
  assert.equal(transition.uses, receipt.uses);
  assert.notDeepEqual(transition.ref, receipt.ref);
  assert.notEqual(transition.attempts[0].dispatchKey, receipt.attempts[0].dispatchKey);
  assert.equal(transition.check.verdict, 'passed');
  assert.equal(receipt.check.verdict, 'failed');
});

test('predicate identity and expected claim do not change when input is unavailable', () => {
  for (const key of ['baseline_ok', 'alarm_transition', 'notification_received']) {
    const normal = step(view('alarm-passed'), key).check;
    const blocked = step(view('baseline-blocked'), key).check;
    assert.equal(normal.predicateDigest, blocked.predicateDigest);
    assert.equal(normal.expected, blocked.expected);
    assert.equal(normal.evaluatorImplementationDigest, blocked.evaluatorImplementationDigest);
  }
});

test('the required criterion denominator is frozen at every event boundary, including skips', () => {
  for (const run of Fixtures.runs) {
    const expected = run.admission.requiredCriteria;
    for (const time of new Set([0, ...run._events.map(event => event.at), run.durationSeconds])) {
      const snapshot = Model.projectRun(run, time);
      assert.deepEqual(snapshot.criteria.map(item => item.stepKey), expected);
      assert.equal(snapshot.assessment.requiredCount, expected.length);
      assert.equal(snapshot.assessment.passedCount + snapshot.assessment.failedCount + snapshot.assessment.pendingCount + snapshot.assessment.inconclusiveCount, expected.length);
    }
  }
  const cancelled = view('start-ambiguous');
  assert.equal(cancelled.assessment.requiredCount, 2);
  assert.equal(cancelled.assessment.inconclusiveCount, 2);
  assert.equal(step(cancelled, 'notification_received').attempts.length, 0);
});

test('a false criterion is technically successful; cleanup and run execution can succeed', () => {
  const snapshot = view('alarm-late');
  const check = step(snapshot, 'notification_received');
  assert.equal(check.outcome, 'succeeded');
  assert.equal(check.attempts[0].error, null);
  assert.equal(snapshot.execution.outcome, 'succeeded');
  assert.equal(snapshot.assessment.verdict, 'failed');
  assert.equal(snapshot.finalization.status, 'complete');
  assert.equal(snapshot.assessment.passedCount, 1);
  assert.equal(snapshot.assessment.failedCount, 1);
});

test('the baseline is a precondition rather than an additional required success criterion', () => {
  const snapshot = view('baseline-blocked');
  assert.equal(snapshot.preconditions.length, 1);
  assert.equal(snapshot.preconditions[0].verdict, 'failed');
  assert.equal(snapshot.assessment.requiredCount, 2);
  assert.equal(snapshot.assessment.verdict, 'inconclusive');
  assert.equal(snapshot.execution.outcome, 'blocked');
  assert.equal(step(snapshot, 'inject').attempts.length, 0);
  assert.equal(snapshot.effects.some(effect => effect.provider === 'aws/fis'), false);
  const cleanup = step(snapshot, 'stop_injection').attempts[0].outputs;
  assert.equal(cleanup.remoteDisposition, 'none');
  assert.equal(cleanup.reasonCode, 'NOT_DISPATCHED');
  assert.equal('originEffectKey' in cleanup, false);
  assert.deepEqual(cleanup.step, step(snapshot, 'inject').ref);
});

test('query completion and a known zero cannot establish a claim with unknown source coverage', () => {
  const snapshot = view('logs-inconclusive');
  const query = step(snapshot, 'query_errors');
  const observation = query.attempts[0].outputs.observation;
  assert.equal(query.outcome, 'succeeded');
  assert.equal(observation.value.count, 0);
  assert.equal(observation.collection, 'complete');
  assert.equal(observation.coverage, 'unknown');
  assert.equal(snapshot.execution.outcome, 'succeeded');
  assert.equal(snapshot.assessment.verdict, 'inconclusive');
  assert.equal(snapshot.finalization.status, 'complete');
  assert.equal(step(view('logs-inconclusive', 30), 'query_errors').attempts[0].outputs, null);
});

test('missing evidence has absent value, not invented zero or empty result', () => {
  const snapshot = view('baseline-blocked');
  for (const observation of Object.values(step(snapshot, 'collect').attempts[0].outputs)) {
    assert.equal(observation.collection, 'unavailable');
    assert.equal(Object.hasOwn(observation, 'value'), false);
  }
  for (const criterion of snapshot.criteria) assert.equal(criterion.actual, null);
  assert.equal(view('alarm-live', 0).observation.ageSeconds, null);
});

test('a positive witness may pass before its observation window closes', () => {
  const snapshot = view('alarm-passed', 131);
  const observation = step(snapshot, 'collect').attempts[0].outputs.transition;
  assert.equal(observation.windowClosed, false);
  assert.equal(observation.collection, 'partial');
  assert.ok(Date.parse(observation.window.end) > Date.parse(snapshot.now));
  assert.equal(step(snapshot, 'alarm_transition').check.verdict, 'passed');
  assert.equal(step(snapshot, 'alarm_transition').check.proof, 'witness');
});

test('closed windows, witness links and clock margins remain internally consistent', () => {
  for (const run of Fixtures.runs) {
    const snapshot = Model.projectRun(run, run.durationSeconds);
    for (const item of snapshot.steps) for (const attempt of item.attempts) {
      for (const observation of Object.values(attempt.outputs || {})) {
        if (observation && observation.windowClosed && observation.window) assert.ok(Date.parse(observation.window.end) <= Date.parse(observation.observedAt));
        if (observation && observation.value && observation.value.records) {
          const sources = observation.evidenceIds.map(id => snapshot.evidence.find(record => record.evidenceId === id).sourceRecordId);
          for (const record of observation.value.records) assert.ok(sources.includes(record.sourceRecordId));
        }
      }
    }
    const receipt = snapshot.evidence.find(record => record.kind === 'notification-receipt');
    if (receipt) assert.ok(Math.abs(receipt.value.latencySeconds - receipt.value.deadlineSeconds) > receipt.value.clockUncertaintyMs / 1000);
  }
});

test('lost Start response retains an unknown effect, original intent and protective hold', () => {
  const snapshot = view('start-ambiguous');
  const effect = snapshot.effects.find(item => item.provider === 'aws/fis');
  assert.equal(effect.nativeId, null);
  assert.equal(effect.disposition, 'unknown');
  assert.equal(effect.providerState, null);
  assert.equal(effect.localState, 'unconfirmed');
  assert.equal(snapshot.execution.outcome, 'indeterminate');
  assert.equal(snapshot.finalization.status, 'incomplete');
  assert.equal(snapshot.finalization.unresolvedEffects.length, 1);
  assert.equal(Model.summarize(snapshot).protectiveHold, true);
  assert.equal(step(snapshot, 'inject').attempts.length, 1);
  assert.equal(step(snapshot, 'stop_injection').attempts[0].checkpoint.strategy, 'non-creating-reconciliation');
  assert.ok(snapshot.execution.reasons.includes('CANCELLATION_ACCEPTED'));
});

test('creating dispatch and its unknown effect appear atomically at the replay boundary', () => {
  const creates = new Set(['events/capture.open@1', 'aws/fis.start@1', 'aws/cloudwatch.logs.query@1']);
  for (const run of Fixtures.runs) for (const event of run._events.filter(item => item.kind === 'step_start')) {
    const definition = run.revision.definitions.find(item => item.stepKey === event.stepKey);
    if (!creates.has(definition.uses)) continue;
    const before = Model.projectRun(run, event.at - 0.001);
    const at = Model.projectRun(run, event.at);
    assert.equal(step(before, event.stepKey).attempts.length, 0);
    assert.equal(before.effects.some(effect => effect.stepKey === event.stepKey), false);
    assert.equal(step(at, event.stepKey).attempts.length, 1);
    assert.equal(at.effects.find(effect => effect.stepKey === event.stepKey).disposition, 'unknown');
  }
});

test('finalizers follow settled ordering even when prior cleanup fails', () => {
  for (const run of Fixtures.runs) {
    const snapshot = Model.projectRun(run, run.durationSeconds);
    for (const item of snapshot.steps.filter(candidate => candidate.graph === 'finalizer')) {
      for (const dependency of item.needs) assert.ok(Date.parse(item.startedAt) >= Date.parse(step(snapshot, dependency).endedAt));
      assert.equal(item.after, 'settled');
    }
    for (const event of run._events.filter(item => item.kind === 'run_phase' && item.phase === 'finalizing')) {
      assert.ok(Model.projectRun(run, event.at).steps.filter(item => item.graph === 'main').every(item => item.phase === 'finished'));
    }
  }
  const snapshot = view('start-ambiguous');
  assert.equal(step(snapshot, 'stop_injection').outcome, 'failed');
  assert.equal(step(snapshot, 'close_capture').outcome, 'succeeded');
});

test('reconciliation updates the current effect without rewriting the sealed Start attempt', () => {
  const before = view('alarm-passed', 13);
  const after = view('alarm-passed');
  assert.deepEqual(step(before, 'inject').attempts[0], step(after, 'inject').attempts[0]);
  assert.equal(step(after, 'inject').attempts[0].externalRefs.at(-1).disposition, 'active');
  assert.equal(after.effects.find(effect => effect.provider === 'aws/fis').disposition, 'terminal');
  assert.equal(step(after, 'stop_injection').attempts[0].externalRefs.at(-1).disposition, 'terminal');
});

test('replay and exports suppress all unobserved evidence and outputs at every event boundary', () => {
  for (const run of Fixtures.runs) {
    const cutoffs = new Set([0, ...run._events.flatMap(event => [Math.max(0, event.at - 0.001), event.at])]);
    for (const time of cutoffs) {
      const snapshot = Model.projectRun(run, time);
      const text = JSON.stringify(Model.exportSnapshot(snapshot));
      for (const event of run._events.filter(item => item.kind === 'evidence' && (item.at > time || seconds(run, item.record.observedAt) > time))) {
        assert.equal(text.includes(event.record.evidenceId), false, run.key + ' at ' + time + ' leaked ' + event.record.evidenceId);
      }
      for (const item of snapshot.steps) for (const attempt of item.attempts) {
        assert.ok(Date.parse(attempt.startedAt) <= Date.parse(snapshot.now));
        if (attempt.phase !== 'finished') assert.equal(attempt.outputs, null);
        if (attempt.endedAt) assert.ok(Date.parse(attempt.endedAt) <= Date.parse(snapshot.now));
      }
      for (const record of snapshot.evidence) assert.ok(Date.parse(record.observedAt) <= Date.parse(snapshot.now));
      for (const check of [...snapshot.criteria, ...snapshot.preconditions]) {
        if (check.evaluatedThrough) assert.ok(Date.parse(check.evaluatedThrough) <= Date.parse(snapshot.now));
      }
      assert.equal(text.includes('"_events"'), false);
      assert.equal(text.includes('"durationSeconds"'), false);
      assert.equal(text.includes('"initialCursorSeconds"'), false);
    }
  }
});

test('receipt occurrence does not make it visible before ingestion', () => {
  assert.equal(view('alarm-live', 127).evidence.some(item => item.kind === 'notification-receipt'), false);
  const at128 = view('alarm-live', 128).evidence.find(item => item.kind === 'notification-receipt');
  assert.equal(seconds(fixture('alarm-live'), at128.occurredAt), 124);
  assert.equal(seconds(fixture('alarm-live'), at128.observedAt), 128);
});

test('the live initial projection has no future receipt, verdict, finished cleanup or report', () => {
  const snapshot = view('alarm-live');
  assert.equal(snapshot.execution.phase, 'running');
  assert.equal(snapshot.execution.outcome, null);
  assert.equal(snapshot.assessment.pendingCount, 2);
  assert.equal(snapshot.evidence.some(item => ['notification-receipt', 'artifact'].includes(item.kind)), false);
  assert.equal(step(snapshot, 'stop_injection').attempts.length, 0);
  assert.equal(snapshot.effects.find(item => item.provider === 'aws/fis').providerState, 'running');
  assert.equal(snapshot.effects.find(item => item.provider === 'aws/fis').actions[0].status, 'running');
});

test('late artifacts do not rewrite sealed criterion cutoffs or run outcomes', () => {
  const sealed = view('alarm-passed', 163);
  const later = view('alarm-passed', 200);
  assert.deepEqual(later.execution, sealed.execution);
  assert.deepEqual(later.criteria, sealed.criteria);
  assert.deepEqual(later.assessment, sealed.assessment);
  assert.deepEqual(later.finalization, sealed.finalization);
  assert.equal(later.evidence.length, sealed.evidence.length + 1);
  assert.equal(later.evidence.at(-1).kind, 'artifact');
});

test('projections and rewinds never mutate source fixtures or earlier projections', () => {
  const baseline = JSON.stringify(Fixtures);
  const first = view('alarm-live', 110);
  const frozen = JSON.stringify(first);
  view('alarm-live', 200);
  view('alarm-live', 5);
  cancellationAt('alarm-live', 110, 200);
  assert.equal(JSON.stringify(first), frozen);
  assert.equal(JSON.stringify(Fixtures), baseline);
});

test('cancellation freezes source facts and cannot inherit a future receipt or provider stop', () => {
  const {before, after} = cancellationAt('alarm-live', 110, 200);
  assert.deepEqual(after.effects, before.effects);
  assert.deepEqual(after.evidence.filter(item => item.sourceKind !== 'runtime'), before.evidence.filter(item => item.sourceKind !== 'runtime'));
  assert.equal(after.evidence.some(item => ['notification-receipt', 'artifact'].includes(item.kind)), false);
  assert.equal(after.execution.outcome, 'indeterminate');
  assert.equal(after.finalization.status, 'incomplete');
  assert.equal(after.assessment.inconclusiveCount, 2);
  assert.equal(after.simulation.cloudRequestsIssued, 0);
  assert.equal(after.effects.find(item => item.provider === 'aws/fis').providerState, 'running');
  assert.equal(Model.summarize(after).protectiveHold, true);
});

test('local cancellation does not refresh source observation timestamps', () => {
  const {before, after} = cancellationAt('alarm-live', 110, 200);
  assert.equal(after.observation.lastSourceObservationAt, before.observation.lastSourceObservationAt);
  assert.equal(after.observation.ageSeconds, before.observation.ageSeconds + 90);
  assert.equal(after.observation.sourceFrozenAt, before.now);
  assert.ok(after.evidence.filter(item => item.source === 'Local cancellation simulation').every(item => item.sourceKind === 'runtime' && item.provenance === 'local-cancellation-simulation'));
  assert.equal(view('start-ambiguous').observation.ageSeconds, 225);
});

test('provider namespace and evidence label share one freshness row with the latest observation', () => {
  for (const [key, namespace, label, latestOffset] of [
    ['alarm-live', 'aws/fis', 'AWS FIS', 51],
    ['logs-inconclusive', 'aws/cloudwatch.logs', 'CloudWatch Logs Insights', 54]
  ]) {
    const snapshot = view(key);
    const rows = snapshot.observation.bySource.filter(item => [namespace, label].includes(item.source));
    assert.equal(rows.length, 1);
    assert.equal(rows[0].source, label);
    assert.equal(seconds(fixture(key), rows[0].observedAt), latestOffset);
    assert.equal(rows[0].ageSeconds, snapshot.cursorSeconds - latestOffset);
  }
});

test('cancellation racing an unacknowledged Start retains unknown identity and never retries Start', () => {
  const {after} = cancellationAt('alarm-live', 10, 100);
  const effect = after.effects.find(item => item.provider === 'aws/fis');
  assert.equal(effect.nativeId, null);
  assert.equal(effect.disposition, 'unknown');
  assert.equal(step(after, 'inject').attempts.length, 1);
  assert.equal(after.execution.outcome, 'indeterminate');
  assert.equal(after.effects.some(item => item.providerState === 'stopped'), false);
});

test('before-dispatch cancellation produces proven no-op cleanup without fabricated effect identities', () => {
  const {after} = cancellationAt('alarm-live', 0, 60);
  assert.equal(after.effects.length, 0);
  assert.equal(after.execution.outcome, 'cancelled');
  assert.equal(after.finalization.status, 'complete');
  assert.equal(Model.summarize(after).protectiveHold, false);
  for (const item of after.steps.filter(candidate => candidate.graph === 'finalizer')) {
    assert.equal(item.attempts[0].outputs.remoteDisposition, 'none');
    assert.equal('originEffectKey' in item.attempts[0].outputs, false);
    assert.deepEqual(item.attempts[0].outputs.step, item.attempts[0].resolvedInputs.step);
  }
});

test('cancellation preserves conclusive checks already established before the request', () => {
  const {before, after} = cancellationAt('alarm-live', 140, 200);
  assert.deepEqual(after.criteria, before.criteria);
  assert.equal(after.assessment.verdict, 'passed');
  assert.equal(after.execution.outcome, 'indeterminate');
});

test('rewinding before a local cancellation reveals earlier history without modifying the intervention', () => {
  const {result} = cancellationAt('alarm-live', 110, 200);
  const baseline = JSON.stringify(result.intervention);
  assert.deepEqual(Model.applyCancellation(view('alarm-live', 50), result.intervention), view('alarm-live', 50));
  Model.applyCancellation(view('alarm-live', 160), result.intervention);
  assert.equal(JSON.stringify(result.intervention), baseline);
  assert.throws(() => Model.applyCancellation(view('alarm-late', 200), result.intervention), /another Run/);
});

test('cancellation receipt replay, token conflict, join and terminal race remain distinct', () => {
  const {result, after} = cancellationAt('alarm-live', 110, 200);
  assert.deepEqual(Model.requestCancellation(after, command).receipt, result.receipt);
  assert.equal(Model.requestCancellation(after, {...command, reason: 'Changed reason'}).receipt.code, 'IDEMPOTENCY_CONFLICT');
  assert.equal(Model.requestCancellation(view('alarm-passed'), command).receipt.accepted, false);
  assert.equal(Model.requestCancellation(view('alarm-passed'), command).receipt.code, 'RUN_ALREADY_FINISHED');
  const active = Model.applyCancellation(view('alarm-live', 120), result.intervention);
  assert.equal(Model.requestCancellation(active, {clientToken: 'new-token', reason: 'Join existing intent'}).receipt.joinedExistingIntent, true);
  assert.equal(Model.requestCancellation(active, {clientToken: '', reason: ''}).receipt.httpStatus, 400);
});

test('exports contain observed data only and no captured branch or future simulator trace', () => {
  const {after} = cancellationAt('alarm-live', 110, 200);
  const output = Model.exportSnapshot(after);
  const text = JSON.stringify(output);
  assert.equal(output.schemaVersion, 'assessment-observed-snapshot/1');
  for (const token of ['_events', 'capturedSnapshot', 'initialCursorSeconds', 'durationSeconds']) assert.equal(text.includes('"' + token + '"'), false);
  assert.equal(output.observationCutoff, after.now);
  output.execution.outcome = 'changed-in-download';
  assert.equal(after.execution.outcome, 'indeterminate');
});

test('unrecognized check verdicts fail closed and never count as a pass', () => {
  const changed = clone(fixture('alarm-passed'));
  changed._events.find(event => event.kind === 'check_result' && event.stepKey === 'notification_received').check.verdict = 'future-provider-value';
  const snapshot = Model.projectRun(changed);
  assert.equal(snapshot.assessment.verdict, 'inconclusive');
  assert.equal(snapshot.assessment.passedCount, 1);
  assert.equal(snapshot.criteria.find(item => item.stepKey === 'notification_received').reasonCode, 'UNKNOWN_CHECK_VERDICT');
});

test('source filters and replay cursor validation do not invent observations', () => {
  const snapshot = view('alarm-passed');
  assert.equal(Model.filterEvidence(snapshot, {source: 'SNS probe receiver'}).length, 1);
  assert.ok(Model.filterEvidence(snapshot, {stepKey: 'notification_received'}).every(item => item.stepKey === 'notification_received'));
  assert.equal(Model.filterEvidence(snapshot, {query: 'not-a-real-evidence-key'}).length, 0);
  assert.equal(Model.filterEvidence(snapshot).length, snapshot.evidence.length);
  assert.equal(Model.projectRun(fixture('alarm-live'), -20).cursorSeconds, 0);
  assert.throws(() => Model.projectRun(fixture('alarm-live'), NaN), /finite/);
});
