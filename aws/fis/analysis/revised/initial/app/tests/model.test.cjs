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
  assert.equal(result.observedResourceCount, 0, 'An unidentified membership is not an observed resource identity');
  assert.equal(result.unidentifiedMembershipCount, 1);
});

test('pod container selections share one run-scoped pod identity and retain each membership', () => {
  const run = copy(model.getRunAt(find('checkout-az'), 230));
  const pod = { cluster_arn: 'arn:aws:eks:eu-central-1:444455556666:cluster/checkout', namespace: 'payments', pod_name: 'api-7fbd9c' };
  run.resolvedTargets = [
    { targetName: 'checkoutAz', resourceType: 'aws:eks:pod', targetInformation: { ...pod, target_container_name: 'api' } },
    { targetName: 'inventoryAz', resourceType: 'aws:eks:pod', targetInformation: { ...pod, target_container_name: 'proxy' } }
  ];
  const result = model.summarize(run);
  assert.equal(result.selectedResourceCount, 1);
  assert.equal(result.membershipCount, 2);
  assert.equal(result.resources[0].identityMethod, 'eks-pod-name');
  assert.equal(result.resources[0].identityScope, 'run', 'The name does not prove pod incarnation across runs');
  assert.deepEqual(result.resources[0].memberships.map(record => record.targetInformation.target_container_name), ['api', 'proxy']);
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

test('a configured report with no state observation stays unknown in summaries and exports', () => {
  const run = copy(model.getRunAt(find('rds-failover'), 500));
  delete run.experiment.experimentReport;
  assert.equal(model.summarize(run).reportStatus, 'unknown');
  assert.equal(model.exportSnapshot(run).derived.reportStatus, 'unknown');
  delete run.experiment.experimentReportConfiguration;
  assert.equal(model.summarize(run).reportStatus, 'not_configured');
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

test('an active timeline interval ends at the last observation rather than extending stale evidence', () => {
  const run = copy(find('checkout-az'));
  run.observation.freezeAtSeconds = 100;
  const projected = model.getRunAt(run, 230);
  const payment = model.actionRows(projected).find(row => row.name === 'isolatePayments');
  assert.equal(payment.observedThroughTime, '2026-11-05T09:01:40.000Z');
  assert.equal(payment.observedElapsedSeconds, 45);
  assert.equal(payment.elapsedSeconds, 175, 'Wall-clock elapsed time remains a different measure');
});

test('missing telemetry stays unknown and chart segments do not bridge missing samples', () => {
  const run = copy(model.getRunAt(find('checkout-az'), 230));
  run.telemetry.points = [
    { offsetSeconds: 0, value: null },
    { offsetSeconds: 15, value: null }
  ];
  assert.equal(model.summarize(run).latestMetric, null);
  assert.equal(model.summarize(run).peakMetric, null);
  assert.deepEqual(model.metricSeries(run).segments, []);
  // Out-of-order observation arrival must not make an older sample the latest.
  run.telemetry.points = [
    { offsetSeconds: 45, value: 160 }, { offsetSeconds: 0, value: 120 },
    { offsetSeconds: 15, value: null }, { offsetSeconds: 30, value: 150 },
    { offsetSeconds: 90, value: 170 }
  ];
  const series = model.metricSeries(run);
  assert.equal(series.latestMetric, 170);
  assert.equal(series.hasGaps, true);
  assert.deepEqual(series.segments.map(segment => segment.map(point => point.offsetSeconds)), [[0], [30, 45], [90]]);
  assert.equal(model.summarize(run).peakMetric, 170);
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

test('simulated stop keeps source observations frozen while its local lifecycle advances', () => {
  const source = find('checkout-az');
  const at = 230;
  const intervention = { at, snapshot: model.getRunAt(source, at) };
  const before = JSON.stringify(intervention);
  const requested = model.applyStopIntervention(model.getRunAt(source, at), intervention);
  assert.equal(requested.experiment.state.status, 'stopping');
  assert.equal(requested.experiment.actions.observeRecovery.state.status, 'cancelled');
  assert.equal(model.summarize(requested).stoppingActions, 2);
  const completing = model.applyStopIntervention(model.getRunAt(source, at + 29), intervention);
  assert.equal(completing.experiment.state.status, 'stopping');
  assert.ok(!completing.experiment.endTime);
  const completed = model.applyStopIntervention(model.getRunAt(source, 700), intervention);
  assert.equal(completed.experiment.state.status, 'stopped');
  assert.equal(completed.experiment.endTime, '2026-11-05T09:04:20.000Z');
  assert.equal(completed.experiment.actions.establishBaseline.state.status, 'completed');
  assert.equal(model.summarize(completed).stoppedActions, 2);
  assert.equal(completed.observation.lastSuccessfulFetchAt, intervention.snapshot.observation.lastSuccessfulFetchAt);
  assert.equal(completed.observation.snapshotAsOf, intervention.snapshot.observation.snapshotAsOf);
  assert.equal(model.summarize(completed).freshnessSeconds, 470);
  assert.deepEqual(completed.telemetry.points, intervention.snapshot.telemetry.points);
  assert.deepEqual(completed.resolvedTargets, intervention.snapshot.resolvedTargets);
  assert.deepEqual(completed.safety, intervention.snapshot.safety);
  assert.equal(completed.assessment.status, 'inconclusive');
  assert.equal(model.summarize(completed).reportStatus, 'unknown');
  assert.equal(completed.simulation.kind, 'operator-stop');
  assert.equal(completed.simulation.completedAt, '2026-11-05T09:04:20.000Z');
  const packet = model.exportSnapshot(completed);
  assert.equal(packet.run.simulation.kind, 'operator-stop');
  assert.equal(packet.derived.freshnessSeconds, 470);
  assert.doesNotMatch(JSON.stringify(packet), /criterion-evaluated|reportType/);
  assert.ok(packet.run.evidence.every(event => event.source === 'mock_control' || Date.parse(event.observedAt) <= Date.parse(intervention.snapshot.now)));
  const rewind = model.applyStopIntervention(model.getRunAt(source, at - 1), intervention);
  assert.equal(rewind.experiment.state.status, 'running');
  assert.equal(rewind.simulation, undefined);
  assert.equal(JSON.stringify(intervention), before, 'Local intervention projection must be immutable');
});

test('stop before target resolution does not acquire later memberships, alarms or source freshness', () => {
  const source = find('alarm-stop');
  const intervention = { at: 0, snapshot: model.getRunAt(source, 0) };
  const run = model.applyStopIntervention(model.getRunAt(source, 350), intervention);
  assert.equal(run.experiment.state.status, 'stopped');
  assert.equal(model.summarize(run).selectedResourceCount, null);
  assert.equal(model.summarize(run).observedResourceCount, 0);
  assert.equal(run.resolution.complete, false);
  assert.equal(run.safety.alarmState, 'OK');
  assert.equal(run.safety.history.length, 1);
  assert.equal(run.stopCause, undefined);
  assert.equal(model.summarize(run).freshnessSeconds, 350);
  assert.ok(Object.values(run.experiment.actions).every(action => action.state.status === 'cancelled'));
  assert.ok(run.evidence.every(event => event.source === 'mock_control'));
});

test('fixture validation rejects malformed event timestamps instead of comparing nulls', () => {
  const invalid = copy(fixtures);
  invalid.runs[0].evidence[0].occurredAt = 'not a timestamp';
  invalid.runs[0].evidence[0].observedAt = 'not a timestamp';
  const result = model.validateFixtures(invalid);
  assert.equal(result.valid, false);
  assert.ok(result.errors.some(error => /invalid evidence timestamp/.test(error)));
});

test('fixture validation enforces parameter strings and selected account and resource-type coverage', () => {
  const invalid = copy(fixtures);
  const run = invalid.runs[0];
  run.experiment.actions.isolatePayments.parameters.duration = 300;
  run.resolvedTargets[0].resourceType = 'aws:ec2:instance';
  run.resolvedTargets[1].targetInformation.arn = 'arn:aws:ec2:eu-central-1:000000000000:subnet/subnet-unknown';
  const result = model.validateFixtures(invalid);
  assert.equal(result.valid, false);
  assert.ok(result.errors.some(error => /parameter duration must be a string/.test(error)));
  assert.ok(result.errors.some(error => /membership resource type mismatch/.test(error)));
  assert.ok(result.errors.some(error => /selected account .* is not configured/.test(error)));
});
