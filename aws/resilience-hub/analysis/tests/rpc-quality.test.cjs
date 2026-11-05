'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const { createRuntime } = require('../api/runtime.cjs');
const fixtures = require('../data.js');
const contract = require('../api/contract.cjs');
const now = 1793874240000;
const fresh = state => createRuntime({ now: () => now, secret: 'quality-review', ...(state ? { state } : {}) });
const checkout = fixtures.createState().services.find(service => service.id === 'checkout').arn;
const sample = name => fresh().runSample(name).request;
const createService = (runtime, overrides = {}) => runtime.execute('CreateService', { name: 'review-service', permissionModel: { invokerRoleName: 'Reader' }, regions: ['eu-west-1'], clientToken: 'review-service', ...overrides }).service;

test('sub-millisecond timestamps cannot roll back health and supported timestamps round-trip exactly', () => {
  const runtime = fresh(), request = sample('PutHealthObservation'), before = structuredClone(runtime.state);
  for (const observedAt of [now / 1000 + 0.0009, now / 1000 + 0.0001]) {
    assert.throws(() => runtime.execute('PutHealthObservation', { ...request, observation: { ...request.observation, observedAt } }), { type: 'ValidationException' });
  }
  assert.deepEqual(runtime.state, before);
  const first = runtime.execute('PutHealthObservation', { ...request, sourceEventId: 'millisecond-current', clientToken: 'millisecond-current', observation: { ...request.observation, state: 'HEALTHY', observedAt: now / 1000 + 0.001 } });
  assert.equal(first.serviceStatus.health.observedAt, now / 1000 + 0.001);
  const older = runtime.execute('PutHealthObservation', { ...request, sourceEventId: 'millisecond-older', clientToken: 'millisecond-older', observation: { ...request.observation, state: 'UNAVAILABLE', observedAt: now / 1000 } });
  assert.equal(older.selectedAsCurrent, false);
  assert.equal(older.serviceStatus.health.state, 'HEALTHY');
});

test('telemetry and event receipt do not consume a service configuration revision', () => {
  const runtime = fresh(), before = runtime.execute('GetService', { serviceArn: checkout }).service;
  runtime.execute('PutHealthObservation', sample('PutHealthObservation'));
  runtime.execute('IngestEvent', sample('IngestEvent'));
  const observed = runtime.execute('GetService', { serviceArn: checkout }).service;
  assert.equal(observed.version, before.version);
  assert.ok(observed.projectionVersion > before.projectionVersion);
  const edited = runtime.execute('UpdateService', { serviceArn: checkout, description: 'Ownership context reviewed', expectedVersion: before.version, clientToken: 'metadata-edit' }).service;
  assert.equal(edited.version, before.version + 1);
  assert.equal(edited.updatedAt, before.updatedAt, 'local edit time must not overwrite provider update time');
  assert.equal(edited.localUpdatedAt, now / 1000);
  assert.equal(edited.policyContextRefreshRequired, false);
  assert.equal(edited.reassessmentRequired, false);
  assert.equal(edited.refreshRequired, true, 'read reconciliation is distinct from reassessment');
});

test('policy metadata leaves evidence current while objective changes invalidate only derived context', () => {
  const runtime = fresh(), policyArn = runtime.state.policies.find(policy => policy.id === 'critical').arn;
  const before = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  runtime.execute('UpdatePolicy', { policyArn, description: 'Owner clarified', expectedVersion: 1, clientToken: 'policy-metadata' });
  const metadataOnly = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  assert.equal(metadataOnly.assessmentCoverage.current, before.assessmentCoverage.current);
  assert.equal(metadataOnly.policyContextRefreshRequired, false);
  runtime.execute('UpdatePolicy', { policyArn, availabilitySlo: { target: 99.999 }, expectedVersion: 2, clientToken: 'policy-objective' });
  const changed = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  assert.equal(changed.version, before.version);
  assert.ok(changed.projectionVersion > before.projectionVersion);
  assert.equal(changed.policyContextRefreshRequired, true);
  assert.equal(changed.reassessmentRequired, true);
  assert.equal(changed.rerunAssessment, null, 'a local flag must not invent the provider flag');
  assert.equal(changed.assessmentCoverage.current, false);
  assert.deepEqual(changed.posture, before.posture);
  assert.deepEqual(changed.effectivePolicyEvidence, before.effectivePolicyEvidence, 'retained evidence stays immutable until a real refresh');
});

test('creation and child mutation audit events identify the actual scoped subject', () => {
  const runtime = fresh(), system = runtime.execute('CreateSystem', { name: 'audit-system', clientToken: 'audit-system' }).system;
  const systemEvents = runtime.execute('ListEvents', { entityType: 'System', entityId: system.systemArn }).events;
  assert.equal(systemEvents.length, 1);
  assert.equal(systemEvents[0].entityId, system.systemArn);
  const service = createService(runtime);
  const created = runtime.execute('ListEvents', { serviceArn: service.serviceArn }).events;
  assert.equal(created.length, 1);
  assert.equal(created[0].entityType, 'Service');
  assert.equal(created[0].entityId, service.serviceArn);
  assert.equal(created[0].serviceArn, service.serviceArn);
  const request = sample('UpdateFailureModeFinding');
  runtime.execute('UpdateFailureModeFinding', request);
  const findingEvents = runtime.execute('ListEvents', { serviceArn: checkout, entityType: 'Finding', entityId: request.findingId }).events;
  assert.ok(findingEvents.some(event => event.type === 'UpdateFailureModeFinding' && event.subjects.some(subject => subject.entityType === 'Finding' && subject.entityId === request.findingId && subject.serviceArn === checkout)));
});

test('raw event evidence and correlations survive ingestion without authoritatively patching a service', () => {
  const runtime = fresh(), before = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  const request = sample('IngestEvent');
  request.rawEvent.detail.achievability = { availabilitySlo: 'ACHIEVABLE' };
  const response = runtime.execute('IngestEvent', request);
  assert.deepEqual(response.event.rawEvent, request.rawEvent);
  assert.deepEqual(response.event.subjects, request.subjects);
  assert.deepEqual(response.event.correlationIds, request.correlationIds);
  const after = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  assert.deepEqual(after.posture, before.posture);
  assert.deepEqual(after.selectedObservations, before.selectedObservations);
  assert.equal(after.assessmentStatus, before.assessmentStatus);
  const state = structuredClone(runtime.state);
  assert.throws(() => runtime.execute('IngestEvent', { ...request, sourceEventId: 'bad-raw', clientToken: 'bad-raw', rawEvent: { number: Infinity } }), { type: 'ValidationException' });
  assert.deepEqual(runtime.state, state);
});

test('current configuration and retained posture resolve their own coherent policy context', () => {
  const state = fixtures.createState(), service = state.services.find(item => item.arn === checkout);
  const originalContext = state.policyContexts.find(item => item.policyContextCaptureId === service.policyContextCaptureId);
  const originalTarget = state.effectiveTargetObservations.find(item => item.effectiveTargetObservationId === originalContext.effectiveTargetObservationId);
  const newTarget = { ...structuredClone(originalTarget), effectiveTargetObservationId: 'new-current-targets' };
  newTarget.targets[0].value = 99.999;
  const newContext = { ...structuredClone(originalContext), policyContextCaptureId: 'new-current-context', effectiveTargetObservationId: newTarget.effectiveTargetObservationId };
  state.effectiveTargetObservations.push(newTarget); state.policyContexts.push(newContext);
  service.effectiveTargetObservationId = newTarget.effectiveTargetObservationId;
  service.policyContextCaptureId = newContext.policyContextCaptureId;
  const runtime = fresh(state);
  const current = runtime.execute('GetService', { serviceArn: checkout }).service.effectivePolicyEvidence;
  const retained = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus.effectivePolicyEvidence;
  assert.equal(current.policyContextCapture.policyContextCaptureId, newContext.policyContextCaptureId);
  assert.equal(current.effectiveTargetObservation.effectiveTargetObservationId, current.policyContextCapture.effectiveTargetObservationId);
  assert.equal(retained.policyContextCapture.policyContextCaptureId, originalContext.policyContextCaptureId);
  assert.equal(retained.effectiveTargetObservation.effectiveTargetObservationId, retained.policyContextCapture.effectiveTargetObservationId);
  assert.equal(retained.effectiveTargetObservation.targets.length, 8);
  assert.equal(retained.effectiveTargetObservation.targets[0].value, originalTarget.targets[0].value);
});

test('missing, null and empty recommendations remain distinguishable from complete captured evidence', () => {
  for (const [label, value] of [['OMITTED', undefined], ['NULL', null], ['EMPTY', []]]) {
    const state = fixtures.createState(), finding = state.findings.find(item => item.serviceArn === checkout);
    if (value === undefined) delete finding.recommendations; else finding.recommendations = value;
    const result = fresh(state).execute('GetFailureModeFinding', { serviceArn: checkout, findingId: finding.findingId }).finding;
    assert.equal(result.recommendationPresence, label);
    assert.deepEqual(result.recommendationIds, label === 'EMPTY' ? [] : null);
    assert.equal(result.findingCapture.captureId, result.captureId);
    assert.equal(result.findingObservation.observationId, result.observationId);
  }
  const runtime = fresh(), service = createService(runtime);
  const status = runtime.execute('GetServiceStatus', { serviceArn: service.serviceArn }).serviceStatus;
  assert.equal(status.openFindingsCount, null);
  assert.equal(status.findingCoverage.observedOpenCount, 0);
  assert.equal(status.findingCoverage.countMeaning, 'NO_CAPTURE');
});

test('unknown provider values, omitted timestamps and read-only permission variants do not fabricate evidence or fail reads', () => {
  const state = fixtures.createState(), service = state.services.find(item => item.arn === checkout);
  delete service.dependencyDiscovery;
  service.assessmentStatus = 'CANCELLED_BY_PROVIDER';
  service.resourceDiscovery.status = 'RETRY_SCHEDULED';
  service.posture.components.multiAz = 'INSUFFICIENT_EVIDENCE';
  service.permissionModel.crossAccountRoles = [{ crossAccountRoleArn: null }];
  const finding = state.findings.find(item => item.serviceArn === checkout);
  finding.status = 'ACKNOWLEDGED'; finding.severity = 'SEVERE';
  const policy = state.policies.find(item => item.id === 'critical'); delete policy.updatedAt;
  const runtime = fresh(state), result = runtime.execute('GetService', { serviceArn: checkout }).service;
  assert.equal(result.dependencyDiscovery.status, 'UNKNOWN');
  assert.equal(result.dependencyDiscovery.rawStatus, null);
  assert.equal(result.assessmentStatus, 'UNKNOWN'); assert.equal(result.rawAssessmentStatus, 'CANCELLED_BY_PROVIDER');
  assert.equal(result.resourceDiscovery.status, 'UNKNOWN'); assert.equal(result.resourceDiscovery.rawStatus, 'RETRY_SCHEDULED');
  assert.equal(result.achievability.multiAzRtoRpo, 'UNKNOWN');
  assert.ok(result.normalizationDiagnostics.some(diagnostic => diagnostic.rawValue === 'INSUFFICIENT_EVIDENCE'));
  assert.equal(result.permissionModel.crossAccountRoles[0].crossAccountRoleArn, null);
  const detail = runtime.execute('GetFailureModeFinding', { serviceArn: checkout, findingId: finding.findingId }).finding;
  assert.equal(detail.status, 'UNKNOWN'); assert.equal(detail.rawStatus, 'ACKNOWLEDGED');
  assert.equal(detail.severity, 'UNKNOWN'); assert.equal(detail.rawSeverity, 'SEVERE');
  assert.equal(runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus.findingCoverage.exactOpenCount, null);
  assert.equal(runtime.execute('GetPolicy', { policyArn: policy.arn }).policy.updatedAt, null);
  const input = runtime.execute('ListInputSources', { serviceArn: checkout }).inputSources[0];
  assert.equal(input.createdAt, null); assert.equal(typeof input.observedAt, 'number');
  assert.throws(() => runtime.execute('UpdateService', { serviceArn: checkout, expectedVersion: 1, clientToken: 'write-null-role', permissionModel: { invokerRoleName: 'Reader', crossAccountRoles: [{ crossAccountRoleArn: null }] } }), { type: 'ValidationException' });
});

test('official opaque ARN suffixes and native source, region and report bounds are respected', () => {
  const runtime = fresh();
  assert.throws(() => runtime.execute('GetService', { serviceArn: 'arn:aws:resiliencehub:us-east-1:111122223333:service/my-service:abc123' }), { type: 'ResourceNotFoundException' }, 'a documented ARN must pass schema validation before scoped lookup');
  const isoService = createService(runtime, { name: 'isolated-region', regions: ['us-iso-east-1'], clientToken: 'isolated-region' });
  assert.deepEqual(isoService.regions, ['us-iso-east-1']);
  const tags = runtime.execute('CreateInputSource', { serviceArn: checkout, resourceConfiguration: { resourceTags: [{ key: 'Environment', values: [] }] }, clientToken: 'empty-tag-values' }).inputSource;
  assert.deepEqual(tags.resourceConfiguration.resourceTags[0].values, []);
  const invalidSources = [
    { resourceTags: Array.from({ length: 11 }, (_, index) => ({ key: 'Tag' + index, values: [] })) },
    { resourceTags: [{ key: 'Tag', values: Array.from({ length: 11 }, (_, index) => 'Value' + index) }] },
    { eks: { clusterArn: 'arn:aws:eks:eu-west-1:111122223333:cluster/prod', namespaces: ['Uppercase'] } },
    { eks: { clusterArn: 'arn:aws:eks:eu-west-1:111122223333:cluster/prod', namespaces: Array.from({ length: 11 }, (_, index) => 'ns' + index) } }
  ];
  for (const resourceConfiguration of invalidSources) assert.throws(() => runtime.execute('CreateInputSource', { serviceArn: checkout, resourceConfiguration, clientToken: 'bad-source' }), { type: 'ValidationException' });
  const output = { s3: { bucketPath: 's3://northstar-reports/reviews', bucketOwner: '111122223333' } };
  assert.throws(() => createService(runtime, { name: 'too-many-reports', reportConfiguration: { reportOutputs: [output, output] }, clientToken: 'too-many-reports' }), { type: 'ValidationException' });
  assert.throws(() => runtime.execute('CreateSystem', { name: 'invalid-tags', tags: { Owner: 'contains"quote' }, clientToken: 'invalid-tags' }), { type: 'ValidationException' });
  assert.equal(contract.operations.length, 44);
});
