'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fixtures = require('../fixtures.js');
const model = require('../model.js');
const find = key => fixtures.runs.find(run => run.key === key);
const copy = value => JSON.parse(JSON.stringify(value));

test('all fixture references, typed target bindings and dependency schedules are coherent', () => {
  const result = model.validateFixtures(fixtures);
  assert.equal(result.valid, true, result.errors.join('\n'));
  assert.equal(result.runCount, 5);
  assert.ok(result.assertions > 100);
});

test('repeated catalog IDs remain separate action executions and dependency branches', () => {
  const run = model.getRunAt(find('checkout-az'), 230);
  const rows = model.actionRows(run);
  const disruptions = rows.filter(row => row.actionId === 'aws:network:disrupt-connectivity');
  assert.deepEqual(disruptions.map(row => row.name), ['isolatePayments', 'isolateInventory']);
  assert.deepEqual(disruptions.map(row => row.status), ['running', 'running']);
  assert.deepEqual(rows.find(row => row.name === 'observeRecovery').dependencies, ['isolatePayments', 'isolateInventory']);
  assert.equal(model.summarize(run).terminalPercent, 25);
});

test('resource identity deduplication preserves overlapping target memberships', () => {
  const run = model.getRunAt(find('checkout-az'), 230);
  const summary = model.summarize(run);
  assert.equal(summary.membershipCount, 5);
  assert.equal(summary.selectedResourceCount, 4);
  assert.equal(summary.actionResourceAssociations, 5);
  assert.equal(summary.overlapResources.length, 1);
  assert.deepEqual(summary.overlapResources[0].targetNames, ['checkoutAz', 'inventoryAz']);
  assert.equal(model.selectedResources(run, 'isolatePayments').length, 3);
  assert.equal(model.selectedResources(run, 'establishBaseline').length, 0);
});

test('preview completion means all skipped, zero completed and no workload assessment', () => {
  const run = model.getRunAt(find('target-preview'), 35);
  const result = model.summarize(run);
  assert.equal(result.status, 'completed');
  assert.equal(result.terminalPercent, 100);
  assert.equal(result.skippedActions, 3);
  assert.equal(result.completedActions, 0);
  assert.equal(result.assessmentStatus, 'not_assessed');
  assert.equal(result.reportStatus, 'not_generated');
  assert.ok(model.actionRows(run).every(row => row.durationSeconds === null && row.startTime === null));
});

test('unresolved and partial target collections expose unknown totals instead of confirmed zero', () => {
  assert.equal(model.summarize(find('checkout-az'), 5).selectedResourceCount, null);
  const partial = copy(find('checkout-az'));
  partial.resolution.complete = false;
  partial.resolvedTargets = partial.resolvedTargets.slice(0, 1);
  const result = model.summarize(partial, 230);
  assert.equal(result.selectedResourceCount, null);
  assert.equal(result.observedResourceCount, 1);
  assert.equal(result.resourceCountComplete, false);
});

test('unknown resource identity remains raw and does not count as a canonical resource', () => {
  const unknown = copy(find('checkout-az'));
  unknown.resolvedTargets = [{ targetName: 'checkoutAz', resourceType: 'aws:ec2:subnet', targetInformation: { opaqueFutureIdentifier: 'unknown-to-adapter' } }];
  const result = model.summarize(unknown, 230);
  assert.equal(result.selectedResourceCount, null);
  assert.equal(result.unknownIdentityCount, 1);
  assert.equal(result.resources[0].resourceKey, null);
  assert.equal(result.resources[0].targetInformation.opaqueFutureIdentifier, 'unknown-to-adapter');
});

test('snapshot polling timestamps, event occurrence and event observation remain separate', () => {
  const run = model.getRunAt(find('checkout-az'), 58);
  assert.equal(run.snapshotCursorSeconds, 55);
  assert.equal(model.summarize(run).freshnessSeconds, 3);
  assert.equal(run.experiment.actions.isolatePayments.state.status, 'running');
  // The action-start event occurred at 55 but is ingested at 63; hide it at 58.
  assert.ok(!run.evidence.some(event => event.actionName === 'isolatePayments'));
  assert.ok(model.getRunAt(find('checkout-az'), 63).evidence.some(event => event.actionName === 'isolatePayments'));
});

test('replay hides future telemetry, final verdicts and delayed evidence', () => {
  const run = model.getRunAt(find('rds-failover'), 150);
  assert.ok(run.telemetry.points.every(point => point.offsetSeconds <= 150 && Date.parse(point.observedAt) <= Date.parse(run.now)));
  assert.equal(run.assessment.status, 'in_progress');
  assert.equal(run.assessment.recoverySeconds, undefined);
  assert.ok(run.evidence.every(event => Date.parse(event.observedAt) <= Date.parse(run.now)));
  assert.ok(!run.experiment.endTime);
});

test('stopping remains nonterminal while the existing action completes post-actions', () => {
  const run = model.getRunAt(find('alarm-stop'), 185);
  const result = model.summarize(run);
  assert.equal(result.status, 'stopping');
  assert.equal(result.isTerminal, false);
  assert.equal(result.stoppingActions, 1);
  assert.equal(result.cancelledActions, 2);
  assert.equal(result.terminalPercent, 75);
  assert.equal(run.safety.alarmState, 'ALARM');
  assert.equal(run.safety.lever.status, 'disengaged');
  assert.equal(model.summarize(find('alarm-stop'), 220).status, 'stopped');
});

test('completed execution can have a failed workload criterion and a later report', () => {
  const run = find('rds-failover');
  const justEnded = model.summarize(run, 300);
  assert.equal(justEnded.status, 'completed');
  assert.equal(justEnded.reportStatus, 'pending');
  assert.equal(justEnded.assessmentStatus, 'in_progress');
  const result = model.summarize(run, 500);
  assert.equal(result.completedActions, 3);
  assert.equal(result.assessmentStatus, 'failed');
  assert.equal(result.reportStatus, 'completed');
});

test('failed execution preserves structured experiment error and account-scoped evidence', () => {
  const run = model.getRunAt(find('ebs-permission'), 220);
  assert.equal(run.experiment.state.status, 'failed');
  assert.equal(run.experiment.state.error.accountId, '777788889999');
  assert.equal(run.experiment.actions.pauseVolumeIo.state.error, undefined);
  assert.equal(model.summarize(run).assessmentStatus, 'inconclusive');
  assert.equal(model.summarize(run).reportStatus, 'failed');
  const errors = model.filterEvidence(run, { source: 'FIS logs', query: 'denied', actionName: 'pauseVolumeIo' });
  assert.equal(errors.length, 1);
  assert.equal(errors[0].accountId, '777788889999');
});

test('projections do not mutate fixtures and can be replayed backwards or forwards', () => {
  const source = find('checkout-az');
  const before = JSON.stringify(source);
  const later = model.getRunAt(source, 700);
  assert.equal(later.experiment.state.status, 'completed');
  const earlier = model.getRunAt(later, 230);
  assert.equal(earlier.experiment.state.status, 'running');
  assert.equal(earlier.assessment.status, 'in_progress');
  assert.equal(JSON.stringify(source), before);
});

test('missing action observations do not become synthetic completed steps', () => {
  const run = copy(find('rds-failover'));
  run.schedule = run.schedule.filter(item => item.name !== 'observeRecovery');
  delete run.experiment.actions.observeRecovery.state;
  const result = model.summarize(run, 500);
  assert.equal(result.status, 'completed');
  assert.equal(result.unknownActions, 1);
  assert.ok(result.terminalPercent < 100);
});

test('UI-supplied snapshot overrides are derived directly when no cursor is passed', () => {
  const run = copy(model.getRunAt(find('checkout-az'), 230));
  delete run._isProjection;
  run.experiment.state = { status: 'stopping', reason: 'Simulated operator stop requested.' };
  run.experiment.actions.isolatePayments.state.status = 'stopping';
  run.experiment.actions.isolateInventory.state.status = 'stopping';
  assert.equal(model.summarize(run).status, 'stopping');
  assert.equal(model.summarize(run).stoppingActions, 2);
  assert.equal(model.actionRows(run).filter(row => row.status === 'stopping').length, 2);
  assert.equal(model.selectedResources(run).length, 4);
});

test('a stale poll preserves the old execution snapshot and displays its observation age', () => {
  const run = copy(find('checkout-az'));
  run.observation.freezeAtSeconds = 50;
  const projected = model.getRunAt(run, 230);
  assert.equal(model.summarize(projected).freshnessSeconds, 180);
  assert.equal(projected.experiment.actions.isolatePayments.state.status, 'initiating');
  assert.ok(projected.evidence.some(event => event.actionName === 'isolatePayments'));
});

test('an initial export preserves observed configuration without future failures or simulator schedules', () => {
  const run = model.getRunAt(find('ebs-permission'), 0);
  const before = JSON.stringify(run);
  const packet = model.exportSnapshot(run);
  const serialized = JSON.stringify(packet);
  assert.equal(packet.schema, 'fis-observatory/mock-snapshot/v1');
  assert.equal(packet.synthetic, true);
  assert.deepEqual(packet.replay, { offsetSeconds: 0, asOf: run.now });
  assert.equal(packet.run.experiment.state.status, 'initiating');
  assert.deepEqual(packet.run.experiment.actions.pauseVolumeIo.parameters, { duration: 'PT3M' });
  assert.doesNotMatch(serialized, /AuthorizationFailure|AccessDenied|"reportType"|scheduledStartSeconds|scheduledEndSeconds/);
  assert.deepEqual(packet.derived.reportArtifacts, []);
  assert.deepEqual(packet.run.experiment.experimentReport.s3Reports, []);
  assert.equal(packet.derived.elapsedSeconds, 0);
  for (const key of ['_mock', 'schedule', '_isProjection', 'initialCursorSeconds', 'durationSeconds', 'executionDurationSeconds', 'stopCause']) {
    assert.equal(Object.hasOwn(packet.run, key), false, `${key} must not be exported`);
  }
  assert.equal(JSON.stringify(run), before, 'Export must not modify the supplied projection');
  packet.run.experiment.actions.pauseVolumeIo.parameters.duration = 'changed-in-export';
  assert.equal(run.experiment.actions.pauseVolumeIo.parameters.duration, 'PT3M');
});

test('export hides future alarm and lever observations and future stop causes', () => {
  const run = model.getRunAt(find('alarm-stop'), 0);
  // An adapter can hold extra observations; export still respects its as-of time.
  run.safety.history = copy(find('alarm-stop').safety.history);
  run.safety.alarmState = 'ALARM';
  run.safety.observedAt = run.safety.history[1].observedAt;
  run.safety.lever.observedAt = new Date(Date.parse(run.now) + 1000).toISOString();
  run.stopCause = copy(find('alarm-stop').stopCause);
  run.observation.freezeAtSeconds = 0;
  const before = JSON.stringify(run);
  const packet = model.exportSnapshot(run);
  assert.equal(packet.run.safety.alarmState, 'OK');
  assert.equal(packet.run.safety.history.length, 1);
  assert.doesNotMatch(JSON.stringify(packet), /"ALARM"/);
  assert.equal(packet.run.safety.lever, undefined);
  assert.equal(packet.run.stopCause, undefined);
  assert.equal(packet.run.observation.freezeAtSeconds, undefined);
  assert.equal(JSON.stringify(run), before);
});

test('finalized exports preserve observed execution errors, report errors and ready artifacts', () => {
  const failed = model.exportSnapshot(model.getRunAt(find('ebs-permission'), 220));
  assert.equal(failed.run.experiment.state.error.code, 'AuthorizationFailure');
  assert.equal(failed.run.experiment.experimentReport.state.error.code, 'AccessDenied');
  assert.equal(failed.derived.failedActions, 1);
  assert.equal(failed.derived.reportStatus, 'failed');
  assert.ok(failed.run.evidence.some(event => event.type === 'action-error'));
  assert.equal(failed.run.safety.lever.status, 'disengaged');
  const completed = model.exportSnapshot(model.getRunAt(find('rds-failover'), 500));
  assert.equal(completed.derived.reportStatus, 'completed');
  assert.equal(completed.run.experiment.experimentReport.s3Reports.length, 1);
  assert.deepEqual(completed.derived.reportArtifacts, completed.run.experiment.experimentReport.s3Reports);
  assert.equal(completed.derived.assessmentStatus, 'failed');
});

test('export derives from supplied local intervention snapshots without replaying the original outcome', () => {
  const run = copy(model.getRunAt(find('checkout-az'), 230));
  delete run._isProjection;
  run.experiment.state = { status: 'stopping', reason: 'Local mock intervention.' };
  run.experiment.actions.isolatePayments.state.status = 'stopping';
  run.experiment.actions.isolateInventory.state.status = 'stopping';
  run.assessment = { status: 'inconclusive', summary: 'Post-intervention observations are unavailable.' };
  const packet = model.exportSnapshot(run);
  assert.equal(packet.run.experiment.state.status, 'stopping');
  assert.equal(packet.derived.status, 'stopping');
  assert.equal(packet.derived.stoppingActions, 2);
  assert.equal(packet.derived.assessmentStatus, 'inconclusive');
  assert.throws(() => model.exportSnapshot(find('checkout-az')), /as-of projected run/);
});
