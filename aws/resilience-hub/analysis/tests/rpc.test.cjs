'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const contract = require('../api/contract.cjs');
const { createRuntime, validate } = require('../api/runtime.cjs');
const fixedNow = 1793874240000;
const fresh = options => createRuntime({ now: () => fixedNow, secret: 'test-secret', ...options });
const arn = (type, n, account = '111122223333') => `arn:aws:resiliencehub:eu-west-1:${account}:${type}/71000000-0000-4000-8000-${String(n).padStart(12, '0')}`;
const uuid = n => `71000000-0000-4000-8000-${String(n).padStart(12, '0')}`;
const checkout = arn('service', 403), commerce = arn('system', 101), critical = arn('policy', 201);
const principal = (id, role = 'reader', tenantId = 'northstar') => ({ principal: { id, tenantId, roles: [role] } });

test('all 44 published operation samples execute and validate on isolated fixture states', () => {
  assert.equal(contract.operations.length, 44);
  assert.equal(new Set(contract.operations.map(o => o.name)).size, 44);
  for (const operation of contract.operations) {
    const result = fresh().runSample(operation.name);
    assert.doesNotThrow(() => validate(operation.inputSchema, result.request), operation.name + ' request');
    assert.doesNotThrow(() => validate(operation.outputSchema, result.response), operation.name + ' response');
    assert.deepEqual(fresh().runSample(operation.name), result, operation.name + ' has a reproducible documented example');
  }
});

test('every seeded service, recommendation, and partial topology validates without erasing unknowns', () => {
  const runtime = fresh();
  for (const service of runtime.state.services) {
    for (const operation of ['GetService', 'GetServiceStatus', 'ListInputSources', 'ListFailureModeAssessments', 'ListFailureModeFindings', 'ListDependencies', 'ListTopologySnapshots', 'ListEvents']) assert.doesNotThrow(() => runtime.execute(operation, { serviceArn: service.arn }), service.id + ' ' + operation);
  }
  for (const rec of runtime.state.recommendations) {
    const owner = runtime.state.findingObservations.find(o => o.observationId === rec.observationId);
    assert.doesNotThrow(() => runtime.execute('GetRecommendation', { serviceArn: owner.serviceArn, findingId: owner.findingId, recommendationId: rec.id }));
  }
  const notifications = runtime.execute('GetService', { serviceArn: arn('service', 407, '444455556666') }).service;
  assert.equal(notifications.achievability.availabilitySlo, null);
  const topology = runtime.execute('ListTopologySnapshots', { serviceArn: arn('service', 408, '777788889999') }).topologySnapshots[0];
  assert.equal(topology.collectionStatus, 'PARTIAL');
  assert.equal(topology.nodes.find(n => n.status === 'UNRESOLVED').accountId, null);
});

test('idempotency returns the original response before version checks and rejects token reuse', () => {
  const runtime = fresh();
  const request = { serviceArn: checkout, description: 'Updated operator context', expectedVersion: 1, clientToken: 'idempotent-update' };
  const first = runtime.execute('UpdateService', request), after = structuredClone(runtime.state);
  assert.equal(first.service.version, 2);
  assert.deepEqual(runtime.execute('UpdateService', { ...request }), first);
  assert.deepEqual(runtime.state, after);
  assert.throws(() => runtime.execute('UpdateService', { ...request, description: 'Changed payload' }), { type: 'ConflictException' });
  assert.throws(() => runtime.execute('UpdateService', { ...request, clientToken: 'new-command' }), { type: 'ConflictException' });
  assert.deepEqual(runtime.state, after);
});

test('create/read/update/delete preserves history and validates same-system references atomically', () => {
  const runtime = fresh();
  const system = runtime.execute('CreateSystem', { name: 'research-sandbox', clientToken: 'create-system' }).system;
  const journey = runtime.execute('CreateUserJourney', { systemArn: system.systemArn, name: 'Review a report', policyArn: critical, clientToken: 'create-journey' }).userJourney;
  const createService = { name: 'report-service', permissionModel: { invokerRoleName: 'ResilienceReadOnly' }, regions: ['eu-west-1'], associatedSystems: [{ systemArn: system.systemArn, userJourneyIds: [journey.userJourneyId] }], clientToken: 'create-service' };
  const svc = runtime.execute('CreateService', createService).service;
  assert.deepEqual(runtime.execute('GetUserJourney', { systemArn: system.systemArn, userJourneyId: journey.userJourneyId }).userJourney.serviceArns, [svc.serviceArn]);
  const snapshot = structuredClone(runtime.state);
  assert.throws(() => runtime.execute('UpdateService', { serviceArn: svc.serviceArn, associatedSystems: [{ systemArn: commerce, userJourneyIds: [journey.userJourneyId] }], expectedVersion: 1, clientToken: 'wrong-scope' }), { type: 'ResourceNotFoundException' });
  assert.deepEqual(runtime.state, snapshot);
  assert.throws(() => runtime.execute('DeleteSystem', { systemArn: system.systemArn, expectedVersion: 1, clientToken: 'nonempty-delete' }), { type: 'ConflictException' });
  assert.throws(() => runtime.execute('DeleteUserJourney', { systemArn: system.systemArn, userJourneyId: journey.userJourneyId, expectedVersion: 1, clientToken: 'assigned-journey' }), { type: 'ConflictException' });
  runtime.execute('UpdateService', { serviceArn: svc.serviceArn, associatedSystems: [], expectedVersion: 1, clientToken: 'detach' });
  runtime.execute('DeleteUserJourney', { systemArn: system.systemArn, userJourneyId: journey.userJourneyId, expectedVersion: 1, clientToken: 'delete-journey' });
  runtime.execute('DeleteSystem', { systemArn: system.systemArn, expectedVersion: 1, clientToken: 'delete-system' });
  runtime.execute('DeleteService', { serviceArn: svc.serviceArn, expectedVersion: 2, clientToken: 'delete-service' });
  assert.throws(() => runtime.execute('GetService', { serviceArn: svc.serviceArn }), { type: 'ResourceNotFoundException' });
  assert.equal(runtime.state.rpc.tombstones.length, 3);
  assert.ok(runtime.state.services.find(s => s.arn === svc.serviceArn).deletedAt);
});

test('deletion guards protect assigned policies and active assessments; historical reads survive deletion', () => {
  const runtime = fresh();
  assert.throws(() => runtime.execute('DeletePolicy', { policyArn: critical, expectedVersion: 1, clientToken: 'assigned-policy' }), { type: 'ConflictException' });
  assert.throws(() => runtime.execute('DeleteService', { serviceArn: arn('service', 405), expectedVersion: 1, clientToken: 'active-assessment' }), { type: 'ConflictException' });
  const before = runtime.execute('ListFailureModeAssessments', { serviceArn: checkout }).assessments;
  runtime.execute('DeleteService', { serviceArn: checkout, expectedVersion: 1, clientToken: 'delete-checkout' });
  assert.deepEqual(runtime.execute('ListFailureModeAssessments', { serviceArn: checkout }).assessments, before);
  assert.equal(runtime.execute('GetFailureModeFinding', { serviceArn: checkout, findingId: uuid(804) }).finding.findingId, uuid(804));
  assert.ok(runtime.execute('ListTopologySnapshots', { serviceArn: checkout }).topologySnapshots.length);
});

test('pagination is stable across mutations and signed against principal, operation, filters, and expiry', () => {
  let now = fixedNow;
  const runtime = fresh({ now: () => now, cursorTtlSeconds: 10 });
  const first = runtime.execute('ListServices', { systemArn: commerce, maxResults: 2 }, principal('alice'));
  runtime.execute('CreateService', { name: 'new-storefront', permissionModel: { invokerRoleName: 'ResilienceReader' }, regions: ['eu-west-1'], associatedSystems: [{ systemArn: commerce }], clientToken: 'new-page-member' });
  runtime.execute('DeleteService', { serviceArn: arn('service', 402), expectedVersion: 1, clientToken: 'remove-page-member' });
  const collected = [...first.services]; let token = first.nextToken;
  while (token) { const page = runtime.execute('ListServices', { systemArn: commerce, maxResults: 2, nextToken: token }, principal('alice')); collected.push(...page.services); token = page.nextToken; assert.equal(page.snapshot.snapshotId, first.snapshot.snapshotId); }
  assert.equal(collected.length, first.snapshot.totalResults);
  assert.equal(new Set(collected.map(s => s.serviceArn)).size, collected.length);
  assert.ok(collected.some(s => s.serviceArn === arn('service', 402)), 'deleted after capture remains in this snapshot');
  assert.ok(!collected.some(s => s.name === 'new-storefront'));
  assert.throws(() => runtime.execute('ListServices', { systemArn: commerce, nextToken: first.nextToken }, principal('bob')), { type: 'ValidationException' });
  assert.throws(() => runtime.execute('ListServices', { nextToken: first.nextToken }, principal('alice')), { type: 'ValidationException' });
  assert.throws(() => runtime.execute('ListSystems', { nextToken: first.nextToken }, principal('alice')), { type: 'ValidationException' });
  assert.throws(() => runtime.execute('ListServices', { systemArn: commerce, nextToken: first.nextToken + 'tamper' }, principal('alice')), { type: 'ValidationException' });
  now += 11000;
  assert.throws(() => runtime.execute('ListServices', { systemArn: commerce, nextToken: first.nextToken }, principal('alice')), { type: 'ValidationException' });
});

test('trusted role and tenant checks reject unauthorized writes before inspecting entity existence', () => {
  const runtime = fresh();
  assert.ok(runtime.execute('GetService', { serviceArn: checkout }, principal('reader')).service);
  assert.throws(() => runtime.execute('UpdateService', { serviceArn: checkout, description: 'No', expectedVersion: 1, clientToken: 'denied' }, principal('reader')), { type: 'AccessDeniedException' });
  assert.throws(() => runtime.execute('GetService', { serviceArn: checkout }, principal('outsider', 'admin', 'different-workspace')), { type: 'AccessDeniedException' });
  assert.throws(() => runtime.execute('GetWorkspaceSummary', {}, principal('ingestor', 'ingestor')), { type: 'AccessDeniedException' });
});

test('strict request schemas reject read-only fields, invalid unions, wrong primitive types, and no-op patches', () => {
  const runtime = fresh(), snapshot = structuredClone(runtime.state);
  const requests = [
    ['GetService', { serviceArn: checkout, role: 'admin' }],
    ['UpdateService', { serviceArn: checkout, name: 'rename-is-not-native', expectedVersion: 1, clientToken: 'readonly' }],
    ['UpdateService', { serviceArn: checkout, dependencyDiscovery: 'INITIALIZING', expectedVersion: 1, clientToken: 'readonly-state' }],
    ['UpdateSystem', { systemArn: commerce, description: 'x', expectedVersion: '1', clientToken: 'wrong-type' }],
    ['CreateInputSource', { serviceArn: checkout, resourceConfiguration: { eks: { clusterArn: 'arn:aws:eks:eu-west-1:111122223333:cluster/prod', namespaces: ['checkout'] }, resourceTags: [{ key: 'Application', values: ['checkout'] }] }, clientToken: 'bad-union' }],
    ['ListServices', { maxResults: 101 }],
    ['GetWorkspaceSummary', { userJourneyId: uuid(302) }],
    ['UpdatePolicy', { policyArn: critical, expectedVersion: 1, clientToken: 'no-change' }],
    ['CreateService', { name: 'Spaces are not provider names', permissionModel: { invokerRoleName: 'Reader' }, regions: ['eu-west-1'], clientToken: 'bad-name' }]
  ];
  for (const [operation, input] of requests) assert.throws(() => runtime.execute(operation, input), { type: 'ValidationException' }, operation);
  assert.deepEqual(runtime.state, snapshot);
});

test('native adapter names permission and achievability fields without confusing display names', () => {
  const runtime = fresh(), result = runtime.execute('GetService', { serviceArn: checkout }).service;
  assert.equal(result.name, 'checkout');
  assert.equal(result.displayName, 'Checkout orchestration');
  const crossAccount = runtime.execute('GetService', { serviceArn: arn('service', 401, '444455556666') }).service.permissionModel.crossAccountRoles[0];
  assert.ok(crossAccount.crossAccountRoleArn);
  assert.equal(crossAccount.arn, undefined);
  assert.ok(own(result.resourceDiscovery, 'errorMessage'));
  assert.ok(own(result.achievability, 'multiAzRtoRpo'));
  assert.equal(result.achievability.multiAz, undefined);
  assert.equal(typeof result.createdAt, 'number');
});
function own(object, key) { return Object.prototype.hasOwnProperty.call(object, key); }

test('health ingestion preserves late evidence, treats equal timestamps as historical, and expires independently of posture', () => {
  let now = fixedNow;
  const runtime = fresh({ now: () => now });
  const postureBefore = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus.posture;
  const base = { serviceArn: checkout, streamOwner: 'northstar/checkout/runtime', observation: { state: 'HEALTHY', observedAt: fixedNow / 1000, expiresAt: fixedNow / 1000 + 60, source: 'Synthetic probes', reason: 'Recovery confirmed', ruleVersion: 'monitoring-v1' } };
  const current = runtime.execute('PutHealthObservation', { ...base, sourceEventId: 'new-signal', clientToken: 'health-new' });
  assert.equal(current.selectedAsCurrent, true); assert.equal(current.serviceStatus.health.state, 'HEALTHY');
  const afterFirst = runtime.state.observations.length;
  const duplicate = runtime.execute('PutHealthObservation', { ...base, sourceEventId: 'new-signal', clientToken: 'health-retry-new-token' });
  assert.equal(duplicate.duplicate, true); assert.equal(runtime.state.observations.length, afterFirst);
  const late = runtime.execute('PutHealthObservation', { ...base, sourceEventId: 'late-signal', observation: { ...base.observation, state: 'UNAVAILABLE', observedAt: base.observation.observedAt - 30 }, clientToken: 'health-late' });
  assert.equal(late.selectedAsCurrent, false); assert.equal(late.serviceStatus.health.state, 'HEALTHY');
  const sameTime = runtime.execute('PutHealthObservation', { ...base, sourceEventId: 'tied-signal', observation: { ...base.observation, state: 'DEGRADED' }, clientToken: 'health-tied' });
  assert.equal(sameTime.selectedAsCurrent, false);
  assert.equal(runtime.state.observations.length, afterFirst + 2);
  assert.deepEqual(sameTime.serviceStatus.posture, postureBefore);
  now += 61000;
  const expired = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  assert.equal(expired.health.state, 'UNKNOWN'); assert.equal(expired.health.rawState, 'HEALTHY'); assert.equal(expired.health.stale, true);
  assert.equal(expired.posture.state, postureBefore.state);
});

test('seeded and newly ingested event-key collisions cannot rewrite health or erase audit evidence', () => {
  const runtime = fresh();
  const before = structuredClone(runtime.state);
  assert.throws(() => runtime.execute('PutHealthObservation', { serviceArn: checkout, sourceEventId: uuid(1006), streamOwner: 'northstar/checkout/runtime', observation: { state: 'UNAVAILABLE', observedAt: fixedNow / 1000, expiresAt: fixedNow / 1000 + 300, source: 'Spoofed duplicate', reason: 'Must not replace evidence', ruleVersion: 'v1' }, clientToken: 'seed-collision' }), { type: 'ConflictException' });
  assert.deepEqual(runtime.state, before);
  const event = fresh().runSample('IngestEvent').request;
  runtime.execute('IngestEvent', event);
  assert.throws(() => runtime.execute('IngestEvent', { ...event, title: 'Changed event', clientToken: 'changed-source-event' }), { type: 'ConflictException' });
  const count = runtime.state.events.length;
  assert.equal(runtime.execute('IngestEvent', { ...event, clientToken: 'same-source-event' }).duplicate, true);
  assert.equal(runtime.state.events.length, count);
});

test('events only request refresh and cannot claim successful posture or assessment completion', () => {
  const runtime = fresh(), before = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  const request = fresh().runSample('IngestEvent').request;
  const result = runtime.execute('IngestEvent', request);
  assert.equal(result.event.trustedSource, false);
  assert.equal(result.event.source, 'aws.resiliencehub');
  assert.equal(result.event.producerPrincipalId, 'demo-operator');
  const after = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  assert.deepEqual(after.health, before.health); assert.deepEqual(after.posture, before.posture);
  assert.equal(after.assessmentStatus, before.assessmentStatus); assert.equal(after.refreshRequired, true);
});

test('recommendation enrichment is independently versioned and immutable observation ownership is enforced', () => {
  const runtime = fresh(), rec = runtime.state.recommendations[0], before = structuredClone(rec);
  const owner = runtime.state.findingObservations.find(o => o.observationId === rec.observationId);
  const request = { serviceArn: owner.serviceArn, findingId: owner.findingId, recommendationId: rec.id, title: 'Local implementation estimate', expectedVersion: 1, clientToken: 'enrichment-update' };
  const result = runtime.execute('UpdateRecommendationEnrichment', request).recommendation;
  assert.equal(result.enrichment.version, 2); assert.equal(result.findingObservationId, rec.observationId);
  assert.deepEqual(runtime.state.recommendations.find(r => r.id === rec.id), before);
  assert.throws(() => runtime.execute('GetRecommendation', { serviceArn: checkout, findingId: uuid(804), recommendationId: rec.id }), { type: 'ResourceNotFoundException' });
});

test('finding dispositions, dependency governance, and queued assessments preserve independent dimensions', () => {
  const runtime = fresh(), before = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  runtime.execute('UpdateFailureModeFinding', { serviceArn: checkout, findingId: uuid(804), status: 'RESOLVED', expectedVersion: 1, clientToken: 'resolve-finding' });
  assert.equal(runtime.execute('GetFailureModeFinding', { serviceArn: checkout, findingId: uuid(804) }).finding.verification, 'UNVERIFIED');
  const dependency = runtime.execute('GetDependency', { serviceArn: checkout, dependencyId: uuid(901) }).dependency;
  const updated = runtime.execute('UpdateDependencyGovernance', { serviceArn: checkout, dependencyId: uuid(901), allowedStatus: 'DENIED', source: 'Supplier review', expectedVersion: 1, clientToken: 'deny-supplier' }).dependency;
  assert.equal(updated.criticality, dependency.criticality); assert.equal(updated.version, dependency.version); assert.equal(updated.governance.version, 2);
  const run = runtime.execute('StartFailureModeAssessment', { serviceArn: checkout, clientToken: 'start-assessment' }).assessment;
  assert.equal(run.status, 'PENDING');
  const after = runtime.execute('GetServiceStatus', { serviceArn: checkout }).serviceStatus;
  assert.deepEqual(after.posture, before.posture); assert.deepEqual(after.health, before.health);
  assert.equal(after.assessmentStatus, 'PENDING');
  assert.throws(() => runtime.execute('StartFailureModeAssessment', { serviceArn: checkout, clientToken: 'second-assessment' }), { type: 'ConflictException' });
});

test('topology capture preserves source observation time and graph scope without inventing a provider read', () => {
  const runtime = fresh();
  const original = runtime.execute('ListTopologySnapshots', { serviceArn: checkout }).topologySnapshots[0];
  const captured = runtime.execute('CaptureTopologySnapshot', { serviceArn: checkout, clientToken: 'capture' }).topologySnapshot;
  assert.notEqual(captured.topologyId, original.topologyId);
  assert.equal(captured.sourceObservedAt, original.sourceObservedAt);
  assert.deepEqual(captured.nodes, original.nodes); assert.deepEqual(captured.queryScope, original.queryScope);
  assert.equal(captured.atomicSnapshot, false); assert.equal(captured.captureMode, 'LOCAL_COPY');
  assert.equal(runtime.state.topologies.length, 9);
});

test('input-source lifecycle validates native union members and EKS selector relationships', () => {
  const runtime = fresh();
  const source = { serviceArn: checkout, resourceConfiguration: { eks: { clusterArn: 'arn:aws:eks:eu-west-1:111122223333:cluster/commerce-prod', namespaces: ['checkout'], labelSelector: { matchExpressions: [{ key: 'tier', operator: 'IN', values: ['api'] }] } } }, clientToken: 'eks-registration' };
  const registered = runtime.execute('CreateInputSource', source).inputSource;
  assert.equal(registered.type, 'EKS'); assert.equal(registered.version, 1);
  assert.deepEqual(registered.resourceConfiguration, source.resourceConfiguration);
  const found = runtime.execute('ListInputSources', { serviceArn: checkout, type: 'EKS' }).inputSources;
  assert.ok(found.some(s => s.inputSourceId === registered.inputSourceId));
  const before = structuredClone(runtime.state);
  const bad = structuredClone(source); bad.clientToken = 'bad-eks-relationship'; bad.resourceConfiguration.eks.labelSelector.matchExpressions[0].values = [];
  assert.throws(() => runtime.execute('CreateInputSource', bad), { type: 'ValidationException' });
  assert.deepEqual(runtime.state, before);
  runtime.execute('DeleteInputSource', { serviceArn: checkout, inputSourceId: registered.inputSourceId, expectedVersion: 1, clientToken: 'delete-eks-source' });
  assert.ok(!runtime.execute('ListInputSources', { serviceArn: checkout }).inputSources.some(s => s.inputSourceId === registered.inputSourceId));
  assert.ok(runtime.state.services.find(s => s.arn === checkout).inputSources.find(s => s.inputSourceId === registered.inputSourceId).deletedAt);
});
