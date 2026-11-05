'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const M = require('../model.js');

function service(state, id) { return state.services.find(item => item.id === id); }
function sameBytes(value) { return JSON.stringify(value); }

test('fixture preserves scoped relationship integrity and recommendation observation ownership', () => {
  const state = M.createState();
  assert.equal(state.services.length, 8);
  assert.equal(state.journeys.length, 5);
  assert.equal(new Set(state.services.map(item => item.arn)).size, 8);
  state.services.forEach(item => {
    item.associations.forEach(association => {
      assert.ok(state.systems.some(system => system.id === association.systemId));
      association.journeyIds.forEach(id => assert.ok(state.journeys.some(journey => journey.id === id && journey.systemId === association.systemId)));
    });
  });
  const observationKeys = new Set();
  state.findingObservations.forEach(observation => {
    const key = [observation.captureId, observation.serviceArn, observation.findingId, observation.representation].join('|');
    assert.ok(!observationKeys.has(key), key);
    observationKeys.add(key);
    const capture = state.findingCaptures.find(item => item.captureId === observation.captureId);
    assert.equal(capture.serviceArn, observation.serviceArn);
    if (capture.relatedAssessmentId) assert.ok(state.assessments.some(run => run.serviceArn === capture.serviceArn && run.assessmentId === capture.relatedAssessmentId));
  });
  state.findings.forEach(finding => {
    assert.equal('assessmentId' in finding, false, 'Finding has no invented native assessment foreign key');
    const observation = state.findingObservations.find(item => item.observationId === finding.observationId);
    assert.equal(observation.representation, 'DETAIL');
    finding.recommendations.forEach(rec => {
      assert.equal(rec.observationId, observation.observationId);
      assert.equal(rec.enrichmentProvenance, 'LOCAL_PRODUCT_ENRICHMENT');
      assert.equal(rec.estimate.source, 'Northstar engineering estimate');
    });
  });
  state.topologies.forEach(topology => {
    assert.equal(topology.resourceCount, topology.nodes.filter(node => node.status === 'KNOWN').length);
    topology.edges.forEach(edge => {
      assert.equal(edge.topologyId, topology.topologyId);
      assert.ok(topology.nodes.some(node => node.id === edge.source && node.topologyId === edge.topologyId));
      assert.ok(topology.nodes.some(node => node.id === edge.target && node.topologyId === edge.topologyId));
    });
    assert.equal(topology.atomicSnapshot, false);
  });
});

test('scope summaries deduplicate shared services and findings without inventing journey compliance', () => {
  const state = M.createState();
  assert.equal(M.servicesInScope(state, {}).length, 8);
  assert.equal(M.servicesInScope(state, { systemId: 'commerce' }).length, 7);
  assert.equal(M.servicesInScope(state, { systemId: 'customer' }).length, 5);
  assert.equal(M.servicesInScope(state, { systemId: 'fulfillment' }).length, 3);
  assert.equal(M.servicesInScope(state, { systemId: 'commerce', journeyId: 'buy' }).length, 7);
  assert.equal(M.servicesInScope(state, { systemId: 'customer', journeyId: 'buy' }).length, 0);
  const before = M.metrics(state, {});
  state.findings.push(structuredClone(state.findings[0]));
  state.services.push(structuredClone(state.services[0]));
  const after = M.metrics(state, {});
  assert.equal(after.totalServices, before.totalServices);
  assert.equal(after.openFindings, before.openFindings);
  assert.equal(after.contributorIds.length, new Set(after.contributorIds).size);
  assert.match(after.interpretation, /not certification/);
  assert.equal('journeyCompliance' in after, false);
});

test('effective target ownership and assignment are independent dimensions', () => {
  const state = M.createState();
  const inheritedSelf = service(state, 'catalog').effectiveTargets.find(target => target.ownership === 'SELF' && target.assignment === 'INHERITED');
  assert.ok(inheritedSelf);
  const directCrossAccount = service(state, 'notifications').effectiveTargets.find(target => target.ownership === 'CROSS_ACCOUNT' && target.assignment === 'INHERITED');
  assert.ok(directCrossAccount);
  state.services.forEach(item => {
    item.effectiveTargets.forEach(target => assert.equal(target.source, target.ownership));
    assert.equal(item.posture.evaluatedProviderRevision, null);
  });
});

test('runtime incident changes health independently from posture and findings', () => {
  const state = M.createState();
  const payment = service(state, 'payments');
  const postureBefore = sameBytes(payment.posture);
  const findingsBefore = sameBytes(state.findings);
  const result = M.applyScenario(state, 'payment-latency');
  assert.equal(result.ok, true);
  assert.equal(M.serviceHealth(state, payment).state, 'DEGRADED');
  assert.equal(sameBytes(payment.posture), postureBefore);
  assert.equal(sameBytes(state.findings), findingsBefore);
  assert.equal(result.event.channel, 'TELEMETRY');
});

test('failed new assessment preserves the last trustworthy posture and its timestamp', () => {
  const state = M.createState();
  const payment = service(state, 'payments');
  const before = sameBytes(payment.posture);
  const findingsBefore = sameBytes(state.findings);
  assert.equal(M.applyScenario(state, 'assessment-failed').ok, true);
  assert.equal(payment.assessmentStatus, 'FAILED');
  assert.equal(sameBytes(payment.posture), before);
  assert.equal(sameBytes(state.findings), findingsBefore);
  assert.equal(state.assessments.filter(run => run.serviceId === 'payments' && run.status === 'FAILED').length, 1);
});

test('triage is a mutable disposition, not verified remediation or changed health', () => {
  const state = M.createState();
  const payment = service(state, 'payments');
  const posture = sameBytes(payment.posture), health = sameBytes(payment.health);
  const finding = state.findings.find(item => item.id === 'payments-db');
  assert.equal(M.updateFinding(state, finding.id, 'RESOLVED', 'Standby configured; awaiting reassessment.').ok, true);
  assert.equal(finding.status, 'RESOLVED');
  assert.equal(finding.verification, 'UNVERIFIED');
  assert.equal(sameBytes(payment.posture), posture);
  assert.equal(sameBytes(payment.health), health);
  assert.equal(M.updateFinding(state, finding.id, 'IRRELEVANT', 'Temporary demo suppression.').ok, true);
  assert.equal(finding.verification, 'SUPPRESSED');
  assert.equal(M.metrics(state).suppressedFindings, 2);
  assert.equal(M.updateFinding(state, finding.id, 'CLOSED', '').ok, false);
  assert.equal(M.updateFinding(state, finding.id, 'OPEN', 'x'.repeat(2049)).ok, false);
});

test('assessment workflow completes only an active scoped run and captures observations separately', () => {
  const state = M.createState();
  const checkout = service(state, 'checkout');
  const originalHealth = sameBytes(checkout.health);
  assert.equal(M.applyScenario(state, 'assessment-completed', 'checkout').ok, false);
  const started = M.startAssessment(state, 'checkout');
  assert.equal(started.ok, true);
  assert.equal(checkout.assessmentStatus, 'PENDING');
  assert.equal(M.startAssessment(state, 'checkout').ok, false);
  const completed = M.applyScenario(state, 'assessment-completed', 'checkout');
  assert.equal(completed.ok, true);
  assert.equal(checkout.assessmentStatus, 'SUCCESS');
  assert.equal(checkout.posture.assessmentId, started.assessmentId);
  assert.equal(sameBytes(checkout.health), originalHealth);
  const capture = state.findingCaptures.at(-1);
  assert.equal(capture.serviceArn, checkout.arn);
  assert.equal(capture.relatedAssessmentId, started.assessmentId);
  assert.equal(capture.listCoverage.status, 'COMPLETE');
  assert.equal(capture.detailCoverage.status, 'COMPLETE');
  assert.match(capture.correlationBasis, /no native/);
  assert.equal(M.serviceFindings(state, 'checkout').some(finding => 'assessmentId' in finding), false);
});

test('multiple captures retain immutable recommendation instances with valid historical observation references', () => {
  const state = M.createState();
  const originalRecommendations = structuredClone(state.recommendations);
  for (let pass = 0; pass < 2; pass += 1) {
    M.startAssessment(state, 'payments');
    M.completeAssessment(state, 'payments');
  }
  originalRecommendations.forEach(rec => assert.deepEqual(state.recommendations.find(item => item.id === rec.id), rec));
  state.findingObservations.filter(observation => observation.representation === 'DETAIL').forEach(observation => {
    (observation.recommendationIds || []).forEach(id => {
      const rec = state.recommendations.find(item => item.id === id);
      assert.ok(rec, 'Historical recommendation ' + id + ' resolves');
      assert.equal(rec.observationId, observation.observationId);
    });
  });
  assert.equal(new Set(state.recommendations.map(rec => rec.id)).size, state.recommendations.length);
});

test('detail capture distinguishes omitted recommendations from known empty recommendations', () => {
  const state = M.createState();
  const omitted = state.findings.find(finding => finding.id === 'payments-db');
  const empty = state.findings.find(finding => finding.id === 'payments-backup');
  delete omitted.recommendations;
  delete omitted.recommendationFields;
  empty.recommendations = [];
  empty.recommendationFields = { infrastructureAndCodeRecommendations: 'EMPTY', observabilityRecommendations: 'EMPTY', testingRecommendations: 'EMPTY' };
  M.startAssessment(state, 'payments');
  M.completeAssessment(state, 'payments');
  const omittedObservation = state.findingObservations.find(item => item.observationId === omitted.observationId);
  const emptyObservation = state.findingObservations.find(item => item.observationId === empty.observationId);
  assert.equal(omittedObservation.recommendationPresence, 'OMITTED');
  assert.equal(omittedObservation.recommendationIds, null);
  assert.equal(Object.hasOwn(omitted, 'recommendations'), false);
  assert.equal(emptyObservation.recommendationPresence, 'EMPTY');
  assert.deepEqual(emptyObservation.recommendationIds, []);
});

test('health expiry returns unknown and stale while retaining historical evidence', () => {
  const state = M.createState();
  assert.equal(M.serviceHealth(state, 'notifications').state, 'UNKNOWN');
  assert.equal(M.serviceHealth(state, 'notifications').rawState, 'HEALTHY');
  const payment = service(state, 'payments');
  const original = sameBytes(payment.health), posture = sameBytes(payment.posture);
  assert.equal(M.applyScenario(state, 'telemetry-expired').ok, true);
  assert.equal(M.serviceHealth(state, payment).state, 'UNKNOWN');
  assert.equal(M.serviceHealth(state, payment).stale, true);
  assert.equal(sameBytes(payment.health), original);
  assert.equal(sameBytes(payment.posture), posture);
  assert.equal(M.metrics(state).unknownHealth, 8);
});

test('event identity is channel and stream scoped; duplicate and delayed signals cannot roll back health', () => {
  const state = M.createState();
  M.applyScenario(state, 'payment-latency');
  const payment = service(state, 'payments');
  const before = sameBytes(payment.health), eventCount = state.events.length;
  const result = M.applyScenario(state, 'duplicate-delayed');
  assert.equal(result.ok, true);
  assert.equal(sameBytes(payment.health), before);
  assert.equal(state.stats.duplicateEvents, 1);
  assert.equal(state.stats.staleEvents, 1);
  assert.equal(state.events.length, eventCount + 1);
  assert.equal(state.events[0].refreshStatus, 'OLDER_EVIDENCE');
  const source = state.events[0];
  const otherChannel = M.recordEvent(state, Object.assign({}, source, { channel: 'LOCAL' }));
  assert.equal(otherChannel.duplicate, false);
  const otherOwner = M.recordEvent(state, Object.assign({}, source, { streamOwner: 'another-owner' }));
  assert.equal(otherOwner.duplicate, false);
});

test('dependency discovery and governance are distinct from topology and runtime health', () => {
  const state = M.createState();
  const payment = service(state, 'payments'), topologyBefore = sameBytes(state.topologies), healthBefore = sameBytes(payment.health);
  const count = state.dependencies.length;
  assert.equal(M.applyScenario(state, 'new-dependency').ok, true);
  assert.equal(state.dependencies.length, count + 1);
  const dependency = state.dependencies.find(item => item.id === 'payments-fraud');
  assert.equal(dependency.criticality, 'UNKNOWN');
  assert.equal(dependency.governance.allowedStatus, 'REVIEW');
  assert.equal(dependency.resolution, undefined);
  assert.equal(M.updateDependency(state, dependency.id, 'HARD', 'Required for card payments.').ok, true);
  assert.equal(dependency.governance.allowedStatus, 'REVIEW');
  assert.equal(sameBytes(state.topologies), topologyBefore);
  assert.equal(sameBytes(payment.health), healthBefore);
  assert.equal(M.setDiscovery(state, 'notifications', false).ok, true);
  assert.equal(service(state, 'notifications').dependencyDiscovery.status, 'DISABLED');
  assert.equal(M.setDiscovery(state, 'notifications', true).ok, true);
  assert.equal(service(state, 'notifications').dependencyDiscovery.status, 'INITIALIZING');
  assert.equal(service(state, 'notifications').dependencyDiscovery.eligibleResourceCount, null);
  assert.equal(M.discoveryGap(service(state, 'notifications')), true);
});

test('summary hydration retains omitted detail and distinguishes null, empty and zero', () => {
  const state = M.createState();
  const payment = service(state, 'payments');
  const permissions = sameBytes(payment.permissionModel), sources = sameBytes(payment.inputSources);
  const description = payment.description;
  assert.equal(M.mergeServiceSummary(state, 'payments', { name: 'Payments gateway refreshed', dependencyDiscovery: { eligibleResourceCount: 0 } }, state.now).ok, true);
  assert.equal(payment.description, description);
  assert.equal(sameBytes(payment.permissionModel), permissions);
  assert.equal(sameBytes(payment.inputSources), sources);
  assert.equal(payment.dependencyDiscovery.eligibleResourceCount, 0);
  assert.equal(payment.dependencyDiscovery.status, 'ENABLED');
  assert.equal(M.discoveryGap(payment), true);
  M.mergeServiceSummary(state, 'payments', { description: null, inputSources: [] }, state.now);
  assert.equal(payment.description, null);
  assert.deepEqual(payment.inputSources, []);
  assert.equal(M.mergeServiceSummary(state, 'payments', { name: 'Old name' }, '2026-10-01T00:00:00.000Z').stale, true);
  assert.equal(payment.name, 'Payments gateway refreshed');
});
