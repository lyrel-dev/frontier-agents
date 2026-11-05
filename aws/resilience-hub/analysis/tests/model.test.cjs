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
  assert.equal(M.assessmentCoverage(state, payment).current, true);
  assert.equal(M.updateFinding(state, finding.id, 'RESOLVED', 'Standby configured; awaiting reassessment.').ok, true);
  assert.equal(finding.status, 'RESOLVED');
  assert.equal(finding.verification, 'UNVERIFIED');
  assert.equal(payment.reassessmentRequired, true, 'A newly claimed repair creates the same local reassessment obligation as the RPC command');
  assert.equal(M.assessmentCoverage(state, payment).current, false);
  assert.equal(M.assessmentCoverage(state, payment).lastKnown, true);
  assert.match(M.attentionReasons(state, payment).find(reason => reason.code === 'LOCAL_REASSESSMENT_REQUIRED').message, /claimed repair/);
  assert.equal(sameBytes(payment.posture), posture);
  assert.equal(sameBytes(payment.health), health);
  assert.equal(M.updateFinding(state, finding.id, 'IRRELEVANT', 'Temporary demo suppression.').ok, true);
  assert.equal(finding.verification, 'SUPPRESSED');
  assert.equal(M.metrics(state).suppressedFindings, 2);
  assert.equal(M.updateFinding(state, finding.id, 'CLOSED', '').ok, false);
  assert.equal(M.updateFinding(state, finding.id, 'OPEN', 'x'.repeat(2049)).ok, false);
  const original = M.createState();
  const priorResolved = original.findings.find(item => item.status === 'RESOLVED');
  const priorService = service(original, priorResolved.serviceId);
  assert.notEqual(priorService.reassessmentRequired, true, 'Initial resolved fixture records do not create a new obligation');
  M.updateFinding(original, priorResolved.id, 'RESOLVED', 'Comment-only update.');
  assert.notEqual(priorService.reassessmentRequired, true, 'A comment-only update does not assert a new repair');
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

test('assessment outcomes are independent of finding disposition and completion does not verify repair', () => {
  const results = ['OPEN', 'RESOLVED', 'IRRELEVANT'].map(status => {
    const state = M.createState();
    const checkout = service(state, 'checkout');
    const beforeHealth = sameBytes(checkout.health);
    const findings = state.findings.filter(finding => finding.serviceId === 'checkout' && finding.severity === 'HIGH');
    if (status !== 'OPEN') findings.forEach(finding => M.updateFinding(state, finding.id, status, 'Disposition only; the architecture is unchanged.'));
    assert.equal(M.startAssessment(state, 'checkout').ok, true);
    assert.equal(M.completeAssessment(state, 'checkout').ok, true);
    assert.equal(sameBytes(checkout.health), beforeHealth);
    assert.equal(checkout.posture.state, 'NOT_ACHIEVABLE');
    assert.equal(checkout.posture.configurationScenario, 'UNCHANGED_NORTHSTAR_ARCHITECTURE');
    findings.forEach(finding => {
      assert.equal(finding.status, status);
      assert.notEqual(finding.verification, 'CONFIRMED_AFTER_REASSESSMENT');
      if (status === 'RESOLVED') assert.equal(finding.verification, 'UNVERIFIED');
      if (status === 'IRRELEVANT') assert.equal(finding.verification, 'SUPPRESSED');
    });
    return { components: checkout.posture.components, fixtureId: checkout.posture.responseFixtureId };
  });
  assert.deepEqual(results[0], results[1]);
  assert.deepEqual(results[0], results[2]);
  const incomplete = M.createState();
  M.startAssessment(incomplete, 'notifications');
  M.completeAssessment(incomplete, 'notifications');
  assert.equal(service(incomplete, 'notifications').assessmentStatus, 'SUCCESS');
  assert.equal(M.servicePosture(incomplete, 'notifications').state, 'UNKNOWN');
  assert.equal(M.assessmentCoverage(incomplete, 'notifications').current, false);
});

test('attention is an explainable union including findings, resource coverage and changed assessment context', () => {
  const state = M.createState();
  assert.equal(M.metrics(state).attention, 8);
  for (const id of ['edge', 'orders']) assert.ok(M.attentionReasons(state, id).some(reason => reason.code === 'OPEN_FINDINGS'));
  const edge = service(state, 'edge');
  state.findings.filter(finding => finding.serviceId === edge.id).forEach(finding => { finding.status = 'IRRELEVANT'; });
  edge.dependencyDiscovery.message = 'Discovery completed successfully.';
  assert.equal(M.needsAttention(state, edge), false, 'An informational discovery message is not a coverage failure');
  edge.resourceDiscovery = { status: 'FAILED', lastRunAt: state.now, errorCode: 'ACCESS_DENIED', errorMessage: 'Recovery account cannot be read.' };
  assert.ok(M.attentionReasons(state, edge).some(reason => reason.code === 'RESOURCE_DISCOVERY_GAP' && reason.message.includes('Recovery account')));
  assert.equal(M.assessmentCoverage(state, edge).status, 'INACCESSIBLE');
  edge.resourceDiscovery = { status: 'SUCCEEDED', lastRunAt: state.now };
  edge.policyContextRefreshRequired = true;
  assert.ok(M.attentionReasons(state, edge).some(reason => reason.code === 'POLICY_CONTEXT_REFRESH_REQUIRED'));
  assert.equal(M.assessmentCoverage(state, edge).current, false);
  const metrics = M.metrics(M.createState());
  assert.ok(Object.values(metrics.attentionByDimension).reduce((total, count) => total + count, 0) > metrics.attention, 'Overlapping reasons do not sum into the distinct service total');
});

test('current assessment coverage expires while retained history and partial evidence remain explicit', () => {
  const state = M.createState();
  const baseline = M.metrics(state);
  assert.equal(baseline.currentAssessed, 6);
  assert.equal(baseline.currentAssessmentCoverage, 75);
  assert.equal(baseline.lastKnownAssessed, 7);
  assert.equal(baseline.lastKnownAssessmentCoverage, 88);
  assert.equal(M.assessmentCoverage(state, 'identity').current, true, 'A failed newer run does not erase current evidence from a previous successful run');
  assert.equal(M.assessmentCoverage(state, 'fulfillment').status, 'PARTIAL');
  assert.equal(M.assessmentCoverage(state, 'fulfillment').stale, true);
  assert.equal(M.assessmentCoverage(state, 'notifications').status, 'UNASSESSED');
  state.now = new Date(Date.parse(state.now) + 48 * 60 * 60 * 1000).toISOString();
  const later = M.metrics(state);
  assert.equal(later.currentAssessed, 0);
  assert.equal(later.currentAssessmentCoverage, 0);
  assert.equal(later.lastKnownAssessed, 7);
  assert.equal(later.staleAssessmentEvidence, 7);
  assert.equal(M.metrics(state, { query: 'no-such-service' }).currentAssessmentCoverage, null, 'An empty denominator is not 0% coverage');
});

test('finding coverage qualifies observed zero, unknown statuses, incomplete collection and freshness', () => {
  const state = M.createState();
  const edge = service(state, 'edge');
  const finding = state.findings.find(item => item.serviceId === edge.id);
  finding.status = 'IRRELEVANT';
  assert.equal(M.findingCoverage(state, edge).exactOpenCount, 0);
  assert.equal(M.needsAttention(state, edge), false);
  const capture = state.findingCaptures.find(item => item.serviceArn === edge.arn);
  const incomplete = { captureId: 'newer-incomplete-attempt', serviceArn: edge.arn, captureStartedAt: state.now, captureEndedAt: null, collectionStatus: 'PARTIAL', listCoverage: { status: 'PARTIAL', filters: {} }, detailCoverage: { status: 'PARTIAL' } };
  state.findingCaptures.push(incomplete);
  assert.equal(M.findingCoverage(state, edge).latestCapture.captureId, incomplete.captureId, 'A newer incomplete attempt is not hidden by an older complete capture');
  assert.equal(M.findingCoverage(state, edge).status, 'PARTIAL');
  assert.equal(M.findingCoverage(state, edge).exactOpenCount, null);
  assert.equal(M.needsAttention(state, edge), true);
  state.findingCaptures = state.findingCaptures.filter(item => item.serviceArn !== edge.arn);
  assert.equal(M.findingCoverage(state, edge).observedOpenCount, 0);
  assert.equal(M.findingCoverage(state, edge).exactOpenCount, null);
  assert.equal(M.findingCoverage(state, edge).status, 'UNASSESSED');
  assert.ok(M.attentionReasons(state, edge).some(reason => reason.code === 'FINDING_COLLECTION_INCOMPLETE'), 'Missing finding coverage needs attention even when health and posture are good and all observed findings are closed');
  state.findingCaptures.push(capture);
  const observedAt = capture.captureEndedAt;
  delete capture.captureEndedAt;
  assert.equal(M.findingCoverage(state, edge).status, 'PARTIAL');
  assert.equal(M.findingCoverage(state, edge).observedAt, null);
  assert.equal(M.findingCoverage(state, edge).exactOpenCount, null);
  capture.captureEndedAt = observedAt;
  capture.listCoverage.filters = { severity: 'HIGH' };
  assert.equal(M.findingCoverage(state, edge).status, 'PARTIAL', 'A filtered list is only an observed subset');
  capture.listCoverage.filters = {};
  finding.status = 'FUTURE_PROVIDER_STATUS';
  assert.equal(M.findingCoverage(state, edge).unknownStatusCount, 1);
  assert.equal(M.findingCoverage(state, edge).exactOpenCount, null);
  finding.status = 'IRRELEVANT';
  state.now = new Date(Date.parse(state.now) + 25 * 60 * 60 * 1000).toISOString();
  assert.equal(M.findingCoverage(state, edge).status, 'STALE');
  assert.equal(M.findingCoverage(state, edge).stale, true);
  assert.equal(M.findingCoverage(state, edge).exactOpenCount, null);
});

test('coverage follows captured optional objectives and qualifies unknown context or native reassessment requests', () => {
  const state = M.createState();
  const edge = service(state, 'edge');
  const context = state.policyContexts.find(item => item.policyContextCaptureId === edge.posture.policyContextCaptureId);
  const capturedTargets = state.effectiveTargetObservations.find(item => item.effectiveTargetObservationId === context.effectiveTargetObservationId);
  capturedTargets.targets = capturedTargets.targets.filter(target => target.metric === 'availabilitySlo');
  edge.posture.components = { availabilitySlo: 'ACHIEVABLE' };
  assert.deepEqual(M.assessmentCoverage(state, edge).expectedComponents, ['availabilitySlo']);
  assert.equal(M.assessmentCoverage(state, edge).status, 'CURRENT', 'An availability-only captured policy does not require unconfigured recovery components');
  edge.effectiveTargets = [{ metric: 'multiAzRto', value: 15 }];
  state.policies.find(policy => policy.id === edge.policyId).components = { multiAz: { rtoInMinutes: 15 } };
  assert.equal(M.assessmentCoverage(state, edge).status, 'CURRENT', 'Current mutable policy data does not rewrite captured component applicability');
  edge.posture.components.availabilitySlo = null;
  assert.equal(M.assessmentCoverage(state, edge).status, 'PARTIAL');
  edge.posture.components.availabilitySlo = 'ACHIEVABLE';
  edge.posture.policyContextCaptureId = 'unavailable-context';
  assert.equal(M.assessmentCoverage(state, edge).status, 'PARTIAL');
  assert.equal(M.assessmentCoverage(state, edge).policyContextKnown, false);
  assert.equal(M.assessmentCoverage(state, edge).expectedComponents, null);
  edge.posture.policyContextCaptureId = context.policyContextCaptureId;
  capturedTargets.targets.push(null);
  assert.equal(M.assessmentCoverage(state, edge).status, 'PARTIAL', 'A null captured target is unknown evidence, not a crash or an omitted objective');
  assert.equal(M.assessmentCoverage(state, edge).policyContextKnown, false);
  capturedTargets.targets.pop();
  edge.reassessmentRequired = true;
  assert.equal(M.assessmentCoverage(state, edge).current, false);
  assert.equal(M.assessmentCoverage(state, edge).contextRefreshRequired, false, 'Material service changes are distinct from policy context invalidation');
  assert.ok(M.attentionReasons(state, edge).some(reason => reason.code === 'LOCAL_REASSESSMENT_REQUIRED'));
  delete edge.reassessmentRequired;
  edge.rerunAssessment = true;
  assert.equal(M.assessmentCoverage(state, edge).current, false);
  assert.ok(M.attentionReasons(state, edge).some(reason => reason.code === 'NATIVE_REASSESSMENT_REQUIRED'));
  delete edge.rerunAssessment;
  assert.equal(M.attentionReasons(state, edge).some(reason => reason.code === 'NATIVE_REASSESSMENT_REQUIRED'), false, 'An omitted provider flag is not invented');
});

test('unknown posture or unqualified captured evidence still requires attention', () => {
  for (const missing of ['capturedContext', 'successfulRun', 'unrecognizedPosture']) {
    const state = M.createState();
    const edge = service(state, 'edge');
    state.findings.filter(finding => finding.serviceId === edge.id).forEach(finding => { finding.status = 'IRRELEVANT'; });
    assert.equal(M.needsAttention(state, edge), false);
    if (missing === 'capturedContext') edge.posture.policyContextCaptureId = null;
    else if (missing === 'successfulRun') state.assessments = state.assessments.filter(run => run.serviceArn !== edge.arn);
    else {
      edge.posture.state = 'FUTURE_PROVIDER_STATE';
      assert.equal(M.servicePosture(state, edge).state, 'UNKNOWN');
      assert.equal(M.servicePosture(state, edge).rawState, 'FUTURE_PROVIDER_STATE');
    }
    assert.equal(M.assessmentCoverage(state, edge).current, false);
    const reasons = M.attentionReasons(state, edge);
    assert.deepEqual(reasons.map(reason => reason.code), [missing === 'unrecognizedPosture' ? 'POSTURE_UNKNOWN' : 'ASSESSMENT_EVIDENCE_GAP']);
    assert.equal(M.needsAttention(state, edge), true);
  }
});

test('equal-time health evidence remains historical and invalid observation windows are rejected before changes', () => {
  const state = M.createState();
  const payment = service(state, 'payments');
  const original = sameBytes(payment.health), count = state.observations.length;
  const tie = { ...structuredClone(payment.health), state: 'UNAVAILABLE', reason: 'An independent equal-time observation' };
  const result = M.applyHealthObservation(state, payment.id, tie, { sourceEventId: 'equal-time-observation' });
  assert.equal(result.stale, true);
  assert.equal(sameBytes(payment.health), original);
  assert.equal(state.observations.length, count + 1);
  const before = sameBytes(state);
  assert.equal(M.applyHealthObservation(state, payment.id, { ...tie, expiresAt: tie.observedAt }).ok, false);
  assert.equal(sameBytes(state), before);
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
