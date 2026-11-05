/* Pure selectors and deterministic mock commands; no AWS or monitoring adapter. */
(function (root, factory) {
  var data = typeof module === 'object' && module.exports ? require('./data.js') : root.RH_DATA;
  var api = factory(data);
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.RH_MODEL = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (data) {
  'use strict';

  var ACTIVE = ['PENDING', 'IN_PROGRESS'];
  var POSTURE_TTL_MINUTES = 24 * 60; // A local demo freshness rule, not an AWS retention limit.
  var COMPONENTS = { availabilitySlo: 'AVAILABILITY_SLO', multiAz: 'MULTI_AZ_DISASTER_RECOVERY', multiRegion: 'MULTI_REGION_DISASTER_RECOVERY', dataRecovery: 'DATA_RECOVERY' };
  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function currentTime(state) { return Date.parse(state.now); }
  function ageMinutes(state, timestamp) { return timestamp ? Math.max(0, (currentTime(state) - Date.parse(timestamp)) / 60000) : null; }
  function advance(state, minutes) { state.now = new Date(currentTime(state) + (minutes || 1) * 60000).toISOString(); return state.now; }
  function nextId(state, prefix) { state.sequence += 1; return prefix + '-' + state.sequence; }
  function nextUuid(state) { state.sequence += 1; return '72000000-0000-4000-8000-' + String(state.sequence).padStart(12, '0'); }
  function getService(state, service) { return typeof service === 'string' ? state.services.find(function (item) { return item.id === service || item.arn === service; }) : service; }
  function findingKey(finding) { return finding.serviceArn + '|' + finding.findingId; }
  function result(ok, message, extra) { return Object.assign({ ok: ok, message: message }, extra || {}); }
  function changed(state) { state.stats.projectionRevision += 1; }

  function servicesInScope(state, scope) {
    scope = scope || {};
    var systemId = scope.systemId || 'all', journeyId = scope.journeyId || 'all';
    var query = String(scope.query || '').trim().toLowerCase();
    var seen = new Set();
    return state.services.filter(function (service) {
      if (seen.has(service.arn)) return false;
      seen.add(service.arn);
      if (systemId !== 'all' && !service.associations.some(function (item) { return item.systemId === systemId; })) return false;
      if (journeyId !== 'all' && !service.associations.some(function (item) { return (systemId === 'all' || item.systemId === systemId) && item.journeyIds.indexOf(journeyId) >= 0; })) return false;
      if (query && [service.name, service.description, service.owner, service.id].join(' ').toLowerCase().indexOf(query) < 0) return false;
      return true;
    });
  }

  function serviceHealth(state, service) {
    service = getService(state, service);
    var stored = service && service.health;
    if (!stored) return { state: 'UNKNOWN', rawState: null, stale: false, ageMinutes: null, reason: 'No monitoring evidence is available.', source: null, observedAt: null, expiresAt: null };
    var expired = !stored.expiresAt || !Number.isFinite(Date.parse(stored.expiresAt)) || currentTime(state) >= Date.parse(stored.expiresAt);
    var known = ['HEALTHY', 'DEGRADED', 'UNAVAILABLE', 'UNKNOWN'].indexOf(stored.state) >= 0;
    return Object.assign({}, stored, { rawState: stored.state, state: expired || !known ? 'UNKNOWN' : stored.state, stale: expired, ageMinutes: ageMinutes(state, stored.observedAt), reason: expired ? 'Current monitoring evidence has expired. Last signal: ' + stored.reason : stored.reason });
  }

  function servicePosture(state, service) {
    service = getService(state, service);
    var stored = service && service.posture;
    if (!stored) return { state: 'UNKNOWN', components: {}, observedAt: null, ageMinutes: null, stale: false };
    var age = ageMinutes(state, stored.observedAt);
    // A stale posture is still the last known assessed result; freshness is independent.
    return Object.assign({}, stored, { ageMinutes: age, stale: age !== null && age > POSTURE_TTL_MINUTES, freshnessRule: '24-hour local demo review cadence' });
  }

  function serviceFindings(state, serviceId) {
    var service = getService(state, serviceId);
    if (!service) return [];
    var seen = new Set();
    return state.findings.filter(function (finding) {
      if (finding.serviceArn !== service.arn) return false;
      var key = findingKey(finding);
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  function discoveryGap(service) {
    var config = service.dependencyDiscovery;
    return !config || config.status !== 'ENABLED' || config.eligibleResourceCount === null || config.eligibleResourceCount === undefined || config.eligibleResourceCount === 0 || Boolean(config.message);
  }

  function needsAttention(state, service) {
    var health = serviceHealth(state, service), posture = servicePosture(state, service);
    return health.state !== 'HEALTHY' || posture.state !== 'ACHIEVABLE' || posture.stale || service.assessmentStatus === 'FAILED' || discoveryGap(service);
  }

  function metrics(state, scope) {
    var services = servicesInScope(state, scope);
    var serviceArns = new Set(services.map(function (service) { return service.arn; }));
    var seen = new Set();
    var findings = state.findings.filter(function (finding) {
      var key = findingKey(finding);
      if (!serviceArns.has(finding.serviceArn) || seen.has(key)) return false;
      seen.add(key); return true;
    });
    var healths = services.map(function (service) { return serviceHealth(state, service); });
    var assessed = services.filter(function (service) { return Boolean(service.posture && service.posture.observedAt && service.posture.state !== 'UNKNOWN'); }).length;
    var count = function (health) { return healths.filter(function (item) { return item.state === health; }).length; };
    return {
      services: services.length, totalServices: services.length, serviceIds: services.map(function (service) { return service.id; }),
      healthy: count('HEALTHY'), degraded: count('DEGRADED'), unavailable: count('UNAVAILABLE'), unknownHealth: count('UNKNOWN'),
      attention: services.filter(function (service) { return needsAttention(state, service); }).length,
      openFindings: findings.filter(function (finding) { return finding.status === 'OPEN'; }).length,
      highFindings: findings.filter(function (finding) { return finding.status === 'OPEN' && finding.severity === 'HIGH'; }).length,
      resolvedFindings: findings.filter(function (finding) { return finding.status === 'RESOLVED'; }).length,
      suppressedFindings: findings.filter(function (finding) { return finding.status === 'IRRELEVANT'; }).length,
      assessed: assessed, assessmentCoverage: services.length ? Math.round(100 * assessed / services.length) : 0,
      activeAssessments: services.filter(function (service) { return ACTIVE.indexOf(service.assessmentStatus) >= 0; }).length,
      failedAssessments: services.filter(function (service) { return service.assessmentStatus === 'FAILED'; }).length,
      discoveryGaps: services.filter(discoveryGap).length,
      staleServices: services.filter(function (service) { return serviceHealth(state, service).stale || servicePosture(state, service).stale; }).length,
      achievabilityAttention: services.filter(function (service) { return servicePosture(state, service).state === 'NOT_ACHIEVABLE'; }).length,
      contributorIds: services.map(function (service) { return service.arn; }),
      computedAt: state.now, aggregationRule: 'distinct-service-attention-v1',
      coverageLabel: 'Services with a last observed assessment result',
      membershipContext: services.map(function (service) { return { serviceArn: service.arn, associations: clone(service.associations) }; }),
      interpretation: 'Attention and coverage summary; this is not certification that every journey target is achievable.'
    };
  }

  function eventKey(event) { return event.channel + '|' + event.streamOwner + '|' + event.sourceEventId; }
  function recordEvent(state, fields) {
    var event = Object.assign({ id: nextId(state, 'event'), sourceEventId: nextUuid(state), channel: 'LOCAL', type: 'LOCAL_CHANGE', occurredAt: state.now, receivedAt: state.now, severity: 'INFO', linkage: 'ASSERTED', refreshStatus: 'LOCAL_ONLY', mock: true }, fields);
    event.eventKey = eventKey(event);
    if (state.events.some(function (existing) { return existing.eventKey === event.eventKey; })) {
      state.stats.duplicateEvents += 1;
      return { duplicate: true, event: event };
    }
    if (!event.source) event.source = event.channel === 'EVENTBRIDGE' ? 'aws.resiliencehub' : event.channel === 'TELEMETRY' ? 'northstar.mock.monitoring' : 'northstar.mock.operator';
    state.events.unshift(event);
    return { duplicate: false, event: event };
  }

  function applyHealthObservation(state, serviceId, observation, eventFields) {
    var service = getService(state, serviceId);
    if (!service) return result(false, 'Service not found.');
    var captured = Object.assign({ observationId: nextId(state, 'health'), entityId: service.id, dimension: 'HEALTH', provenance: 'LOCAL_MONITORING_AGGREGATE', ruleVersion: 'northstar-runtime-v1' }, clone(observation));
    var stale = service.health && Date.parse(captured.observedAt) < Date.parse(service.health.observedAt);
    var recorded = recordEvent(state, Object.assign({ channel: 'TELEMETRY', streamOwner: 'northstar/' + service.id + '/runtime', type: 'RUNTIME_HEALTH_CHANGED', title: service.name + ' health signal received', message: captured.reason, serviceId: service.id, entityType: 'Service', entityId: service.id, occurredAt: captured.observedAt, receivedAt: state.now, refreshStatus: stale ? 'OLDER_EVIDENCE' : 'REFRESHED' }, eventFields || {}));
    if (recorded.duplicate) return result(true, 'Duplicate event ignored; current health is unchanged.', { serviceId: service.id, event: recorded.event, duplicate: true });
    state.observations.push(captured);
    if (stale) {
      state.stats.staleEvents += 1;
      return result(true, 'Older monitoring evidence retained in history; current health is unchanged.', { serviceId: service.id, event: recorded.event, stale: true });
    }
    service.health = clone(captured);
    changed(state);
    return result(true, service.name + ' runtime health refreshed. Resilience posture is unchanged.', { serviceId: service.id, event: recorded.event });
  }

  function mergePresent(previous, patch) {
    var next = Object.assign({}, previous);
    Object.keys(patch).forEach(function (key) {
      var value = patch[key];
      if (value === undefined) return;
      if (value && typeof value === 'object' && !Array.isArray(value) && previous && previous[key] && typeof previous[key] === 'object' && !Array.isArray(previous[key])) next[key] = mergePresent(previous[key], value);
      else next[key] = clone(value);
    });
    return next;
  }

  function mergeServiceSummary(state, serviceId, patch, observedAt) {
    var service = getService(state, serviceId);
    if (!service) return result(false, 'Service not found.');
    if (service.observedAt && Date.parse(observedAt) < Date.parse(service.observedAt)) return result(false, 'Older summary does not replace the current projection.', { stale: true });
    // Omitted summary fields do not erase details. Explicit null and [] remain explicit.
    Object.assign(service, mergePresent(service, patch), { observedAt: observedAt });
    changed(state);
    return result(true, 'Present summary fields merged; hydrated detail retained.', { serviceId: service.id });
  }

  function startAssessment(state, serviceId) {
    var service = getService(state, serviceId);
    if (!service) return result(false, 'Service not found.');
    if (ACTIVE.indexOf(service.assessmentStatus) >= 0) return result(false, 'An assessment is already active for ' + service.name + '.', { serviceId: service.id });
    advance(state, 1);
    var run = { id: nextId(state, 'assessment'), assessmentId: nextUuid(state), serviceId: service.id, serviceArn: service.arn, status: 'PENDING', startedAt: state.now, endedAt: null, totalFindings: null, cost: null, observedAt: state.now };
    state.assessments.push(run);
    service.assessmentStatus = 'PENDING';
    service.observedAt = state.now;
    var recorded = recordEvent(state, { channel: 'EVENTBRIDGE', streamOwner: service.arn, type: 'Failure Mode Assessment Queued', title: service.name + ' assessment queued', message: 'A mock StartFailureModeAssessment response returned an assessment ID. The last observed posture remains visible while the new run is pending.', serviceId: service.id, entityType: 'Assessment', entityId: run.assessmentId, refreshStatus: 'REFRESHED', refreshOperations: ['ListFailureModeAssessments', 'GetService'] });
    state.stats.refreshes += 1;
    changed(state);
    return result(true, 'Assessment queued. Use “Assessment completes” to simulate its completion.', { serviceId: service.id, assessmentId: run.assessmentId, event: recorded.event });
  }

  function latestActiveAssessment(state, service) {
    return state.assessments.filter(function (run) { return run.serviceArn === service.arn && ACTIVE.indexOf(run.status) >= 0; }).sort(function (a, b) { return Date.parse(b.startedAt) - Date.parse(a.startedAt); })[0];
  }

  function captureFindings(state, service, assessment) {
    var findings = serviceFindings(state, service.id);
    var captureId = nextId(state, 'finding-capture');
    state.findingCaptures.push({ id: captureId, captureId: captureId, serviceId: service.id, serviceArn: service.arn, captureStartedAt: state.now, captureEndedAt: state.now, collectionStatus: 'COMPLETE', listCoverage: { status: 'COMPLETE', pages: 1, filters: {}, findingsReturned: findings.length }, detailCoverage: { status: 'COMPLETE', requested: findings.length, hydrated: findings.length, failed: 0 }, relatedAssessmentId: assessment.assessmentId, correlationBasis: 'Local mock list/detail refresh after a completed assessment; no native assessment-to-finding ownership is asserted.' });
    findings.forEach(function (finding) {
      var observationId = nextId(state, 'finding-observation');
      state.findingObservations.push({ observationId: nextId(state, 'finding-summary'), captureId: captureId, serviceArn: service.arn, findingId: finding.findingId, representation: 'SUMMARY', observedAt: state.now, name: finding.name, severity: finding.severity, status: finding.status, recommendationPresence: 'NOT_FETCHED' });
      var recommendationPresence = !Object.prototype.hasOwnProperty.call(finding, 'recommendations') || finding.recommendations === undefined ? 'OMITTED' : finding.recommendations === null ? 'NULL' : finding.recommendations.length === 0 ? 'EMPTY' : 'PRESENT';
      var recommendationIds = null;
      if (Array.isArray(finding.recommendations)) {
        finding.recommendations = finding.recommendations.map(function (rec) { return Object.assign({}, rec, { id: nextId(state, 'recommendation'), observationId: observationId, capturedAt: state.now }); });
        recommendationIds = finding.recommendations.map(function (rec) { return rec.id; });
        if (!state.recommendations) state.recommendations = [];
        state.recommendations.push.apply(state.recommendations, clone(finding.recommendations));
      }
      state.findingObservations.push({ observationId: observationId, captureId: captureId, serviceArn: service.arn, findingId: finding.findingId, representation: 'DETAIL', observedAt: state.now, name: finding.name, severity: finding.severity, status: finding.status, recommendationPresence: recommendationPresence, recommendationFields: finding.recommendationFields ? clone(finding.recommendationFields) : null, recommendationIds: recommendationIds });
      finding.observationId = observationId;
      finding.captureId = captureId;
      finding.detailObservedAt = state.now;
      if (finding.verification === 'UNVERIFIED' && finding.status === 'RESOLVED') {
        finding.verification = 'CONFIRMED_AFTER_REASSESSMENT';
        finding.verificationEvidence = { observedAt: state.now, source: 'Mock GetFailureModeFinding detail refresh', correlationBasis: 'The mock scenario returns the resolved finding after the assessment; the API exposes no assessment foreign key.' };
      }
    });
    return captureId;
  }

  function completeAssessment(state, serviceId) {
    var service = getService(state, serviceId || 'orders');
    if (!service) return result(false, 'Service not found.');
    var run = latestActiveAssessment(state, service);
    if (!run) return result(false, 'Start an assessment for ' + service.name + ' before completing it.', { serviceId: service.id });
    advance(state, 4);
    run.status = 'SUCCESS'; run.endedAt = state.now; run.observedAt = state.now;
    run.totalFindings = serviceFindings(state, service.id).length;
    run.cost = { amount: 3.72, currency: 'USD' };
    delete run.errorCode; delete run.error; delete run.stepLabel;
    // This is the fixture response of a successful GetService refresh, not a
    // production algorithm claiming that finding counts determine achievability.
    var nativeComponents = {};
    var findings = serviceFindings(state, service.id);
    Object.keys(COMPONENTS).forEach(function (component) {
      var unresolvedGap = findings.some(function (finding) { return finding.status === 'OPEN' && finding.policyComponent === COMPONENTS[component] && (finding.severity === 'HIGH' || (service.id === 'payments' && component === 'dataRecovery')); });
      nativeComponents[component] = unresolvedGap ? 'NOT_ACHIEVABLE' : 'ACHIEVABLE';
    });
    run.achievability = clone(nativeComponents);
    service.assessmentStatus = 'SUCCESS';
    service.observedAt = state.now;
    var policyContextCaptureId = nextId(state, 'policy-context');
    var effectiveTargetObservationId = nextId(state, 'targets');
    state.effectiveTargetObservations.push({ effectiveTargetObservationId: effectiveTargetObservationId, serviceId: service.id, serviceArn: service.arn, observedAt: state.now, targets: clone(service.effectiveTargets), evaluatedProviderRevision: null });
    state.policyContexts.push({ policyContextCaptureId: policyContextCaptureId, serviceArn: service.arn, observedAt: state.now, associations: clone(service.associations), applicablePolicies: clone(service.applicablePolicies), effectiveTargetObservationId: effectiveTargetObservationId, provenance: 'LOCAL_CAPTURE', assessedProviderRevision: null });
    service.effectiveTargetObservationId = effectiveTargetObservationId;
    service.policyContextCaptureId = policyContextCaptureId;
    service.posture = { observationId: nextId(state, 'posture'), state: Object.values(nativeComponents).indexOf('NOT_ACHIEVABLE') >= 0 ? 'NOT_ACHIEVABLE' : 'ACHIEVABLE', components: nativeComponents, observedAt: state.now, assessmentId: run.assessmentId, assessmentLinkage: 'LOCAL_CORRELATION', assessmentCorrelationBasis: 'Posture observed after this completed assessment; no evaluated provider policy revision is exposed.', policyContextCaptureId: policyContextCaptureId, source: 'Mock GetService.achievability refresh', ruleVersion: 'any-unachievable-v1', provenance: 'PROVIDER_COMPONENTS_WITH_LOCAL_SUMMARY', evaluatedProviderRevision: null };
    state.observations.push(Object.assign({ entityId: service.id, dimension: 'POSTURE' }, clone(service.posture)));
    captureFindings(state, service, run);
    var recorded = recordEvent(state, { channel: 'EVENTBRIDGE', streamOwner: service.arn, type: 'Failure Mode Assessment Completed', title: service.name + ' assessment completed', message: 'The completion event triggered authoritative mock service and finding reads. Runtime monitoring health is unchanged.', serviceId: service.id, entityType: 'Assessment', entityId: run.assessmentId, refreshStatus: 'REFRESHED', refreshOperations: ['GetService', 'ListFailureModeAssessments', 'ListFailureModeFindings', 'GetFailureModeFinding'] });
    state.stats.refreshes += 1;
    changed(state);
    return result(true, service.name + ' assessment completed. Posture and current finding observations were refreshed.', { serviceId: service.id, event: recorded.event, assessmentId: run.assessmentId });
  }

  function failAssessment(state, serviceId) {
    var service = getService(state, serviceId || 'payments');
    if (!service) return result(false, 'Service not found.');
    var run = latestActiveAssessment(state, service);
    if (!run) {
      var started = startAssessment(state, service.id);
      if (!started.ok) return started;
      run = latestActiveAssessment(state, service);
    }
    advance(state, 2);
    run.status = 'FAILED'; run.endedAt = state.now; run.observedAt = state.now;
    run.errorCode = 'INVALID_PERMISSIONS'; run.error = 'The mock assessment role cannot read a recovery resource in the secondary account.';
    run.cost = { amount: 0.48, currency: 'USD' }; run.totalFindings = null;
    service.assessmentStatus = 'FAILED'; service.observedAt = state.now;
    // Deliberately preserve service.posture and every prior posture observation.
    var recorded = recordEvent(state, { channel: 'EVENTBRIDGE', streamOwner: service.arn, type: 'Failure Mode Assessment Failed', title: service.name + ' assessment failed', message: 'A permissions error stopped the run. The last successful posture is retained with its original observation time.', severity: 'ERROR', serviceId: service.id, entityType: 'Assessment', entityId: run.assessmentId, refreshStatus: 'REFRESHED', refreshOperations: ['ListFailureModeAssessments', 'GetService'] });
    state.stats.refreshes += 1; changed(state);
    return result(true, 'Assessment failed. The last trustworthy posture was preserved.', { serviceId: service.id, event: recorded.event });
  }

  function updateFinding(state, findingId, status, comment) {
    var finding = state.findings.find(function (item) { return item.id === findingId; });
    if (!finding) return result(false, 'Finding not found.');
    if (['OPEN', 'RESOLVED', 'IRRELEVANT'].indexOf(status) < 0) return result(false, 'Select OPEN, RESOLVED or IRRELEVANT.');
    if (comment !== undefined && (typeof comment !== 'string' || comment.length > 2048)) return result(false, 'Finding comments must be no longer than 2,048 characters.');
    advance(state, 1);
    var previousStatus = finding.status;
    finding.status = status; finding.updatedAt = state.now; finding.statusObservedAt = state.now;
    if (comment !== undefined) finding.comment = comment;
    if (status !== previousStatus) finding.verification = status === 'RESOLVED' ? 'UNVERIFIED' : status === 'IRRELEVANT' ? 'SUPPRESSED' : 'OPEN';
    if (!finding.dispositionHistory) finding.dispositionHistory = [];
    finding.dispositionHistory.push({ previousStatus: previousStatus, status: status, comment: finding.comment, observedAt: state.now, actor: 'Demo operator', provenance: 'MOCK_UPDATE_FAILURE_MODE_FINDING' });
    var service = getService(state, finding.serviceId);
    service.openFindingsCount = serviceFindings(state, service.id).filter(function (item) { return item.status === 'OPEN'; }).length;
    service.resolvedFindingsCount = serviceFindings(state, service.id).filter(function (item) { return item.status === 'RESOLVED'; }).length;
    var recorded = recordEvent(state, { streamOwner: service.arn, type: 'FINDING_STATUS_UPDATED', title: finding.name, message: status === 'RESOLVED' ? 'Operator marked the finding resolved. Verification is pending; assessed posture and runtime health have not changed.' : status === 'IRRELEVANT' ? 'Operator suppressed this finding as irrelevant. Suppression does not establish remediation.' : 'Operator reopened the finding for investigation.', serviceId: service.id, entityType: 'Finding', entityId: finding.findingId, operation: 'UpdateFailureModeFinding', refreshStatus: 'LOCAL_ONLY' });
    changed(state);
    return result(true, status === 'RESOLVED' ? 'Marked resolved; verification is pending a later assessment and detail refresh.' : status === 'IRRELEVANT' ? 'Finding marked irrelevant. It remains available as a suppressed finding.' : 'Finding reopened.', { serviceId: service.id, event: recorded.event });
  }

  function updateDependency(state, dependencyId, criticality, comment) {
    var dependency = state.dependencies.find(function (item) { return item.id === dependencyId; });
    if (!dependency) return result(false, 'Dependency not found.');
    if (['HARD', 'SOFT', 'UNKNOWN'].indexOf(criticality) < 0) return result(false, 'Select HARD, SOFT or UNKNOWN.');
    if (comment !== undefined && (typeof comment !== 'string' || comment.length > 2048)) return result(false, 'Use a comment of at most 2,048 characters for this demo.');
    advance(state, 1);
    dependency.criticality = criticality;
    if (comment !== undefined) dependency.comment = comment;
    dependency.observedAt = state.now;
    var recorded = recordEvent(state, { streamOwner: dependency.serviceArn, type: 'DEPENDENCY_UPDATED', title: dependency.name + ' criticality updated', message: 'Criticality is now ' + criticality.toLowerCase() + ' for this consuming service. Local allow-list status and runtime health are unchanged.', serviceId: dependency.serviceId, entityType: 'Dependency', entityId: dependency.dependencyId, operation: 'UpdateDependency' });
    changed(state);
    return result(true, 'Dependency criticality updated for the consuming service.', { serviceId: dependency.serviceId, event: recorded.event });
  }

  function setDiscovery(state, serviceId, enabled) {
    var service = getService(state, serviceId);
    if (!service) return result(false, 'Service not found.');
    if (typeof enabled !== 'boolean') return result(false, 'Discovery configuration must be enabled or disabled.');
    advance(state, 1);
    service.dependencyDiscovery = Object.assign({}, service.dependencyDiscovery, { status: enabled ? 'INITIALIZING' : 'DISABLED', requestedStatus: enabled ? 'ENABLED' : 'DISABLED', eligibleResourceCount: enabled ? null : service.dependencyDiscovery ? service.dependencyDiscovery.eligibleResourceCount : null, message: enabled ? 'Collecting initial DNS query evidence. Eligibility is not known yet.' : 'Dependency discovery has been disabled by the demo operator.', updatedAt: state.now });
    var recorded = recordEvent(state, { streamOwner: service.arn, type: 'DEPENDENCY_DISCOVERY_UPDATED', title: service.name + ' discovery ' + (enabled ? 'enabled' : 'disabled'), message: enabled ? 'The mock UpdateService command sends ENABLED. The observed state is INITIALIZING until discovery evidence is refreshed.' : 'New dependency discovery is disabled; previously observed dependency history is retained.', serviceId: service.id, entityType: 'Service', entityId: service.id, operation: 'UpdateService' });
    changed(state);
    return result(true, enabled ? 'Discovery enabled. Initialization and eligibility are still pending.' : 'Dependency discovery disabled; history is retained.', { serviceId: service.id, event: recorded.event });
  }

  function discoverDependency(state) {
    var service = getService(state, 'payments');
    advance(state, 1);
    var existing = state.dependencies.find(function (item) { return item.id === 'payments-fraud'; });
    if (existing) return result(false, 'The fraud-screening dependency has already been discovered in this demo. Reset to replay it.', { serviceId: service.id });
    var dependency = { id: 'payments-fraud', dependencyId: nextUuid(state), serviceId: service.id, serviceArn: service.arn, name: 'Fraud screening API', dependencyName: 'Fraud screening API', dnsName: 'risk.eu.fraudshield.example', location: 'External · EU', criticality: 'UNKNOWN', provider: 'Fraudshield', sourceRegions: ['eu-west-1'], lastDetectedTime: state.now, firstObservedAt: state.now, comment: '', queryRange: { startTime: new Date(currentTime(state) - 6 * 3600000).toISOString(), endTime: state.now, granularity: 'HOURLY', dataPoints: [5, 4, 3, 2, 1, 0].map(function (hour, index) { return { timestamp: new Date(currentTime(state) - hour * 3600000).toISOString(), queryCount: 34 + index * 27 }; }) }, governance: { allowedStatus: 'REVIEW', source: 'Northstar supplier and service allow-list', observedAt: state.now } };
    state.dependencies.push(dependency);
    var recorded = recordEvent(state, { channel: 'EVENTBRIDGE', streamOwner: service.arn, type: 'New Dependency Discovered', title: 'New fraud-screening dependency', message: 'A stabilized DNS dependency was returned by the mock ListDependencies refresh. Criticality and allow-list review are pending. DNS counts are not availability measurements.', severity: 'WARNING', serviceId: service.id, entityType: 'Dependency', entityId: dependency.dependencyId, refreshStatus: 'REFRESHED', refreshOperations: ['ListDependencies'] });
    state.stats.refreshes += 1; changed(state);
    return result(true, 'Fraud-screening dependency discovered. Review its criticality and local governance status.', { serviceId: service.id, dependencyId: dependency.id, event: recorded.event });
  }

  function applyScenario(state, scenarioId, serviceId) {
    if (!data.scenarios.some(function (scenario) { return scenario.id === scenarioId; })) return result(false, 'Unknown demo scenario.');
    var outcome;
    if (scenarioId === 'payment-latency') {
      advance(state, 1);
      outcome = applyHealthObservation(state, 'payments', { state: 'DEGRADED', observedAt: state.now, expiresAt: new Date(currentTime(state) + 10 * 60000).toISOString(), source: 'CloudWatch metrics + payment synthetic', reason: 'Processor wait time increased: authorization p95 is 1,480 ms and 2.8% of requests fail. The 600 ms local runtime threshold is exceeded.', latencyMs: 1480, errorRate: 2.8, windowMinutes: 5 }, { title: 'Payment authorization latency increased', severity: 'WARNING' });
    } else if (scenarioId === 'assessment-failed') outcome = failAssessment(state, serviceId || 'payments');
    else if (scenarioId === 'assessment-completed') outcome = completeAssessment(state, serviceId || 'orders');
    else if (scenarioId === 'new-dependency') outcome = discoverDependency(state);
    else if (scenarioId === 'telemetry-expired') {
      advance(state, 16);
      var recorded = recordEvent(state, { streamOwner: 'northstar/monitoring', type: 'HEALTH_EVIDENCE_EXPIRED', title: 'Current monitoring evidence expired', message: 'The demo clock advanced 16 minutes without new monitoring observations. Health is now unknown where the source signal expired; retained posture is unchanged.', severity: 'WARNING', entityType: 'Portfolio', entityId: 'northstar', refreshStatus: 'LOCAL_ONLY' });
      changed(state);
      outcome = result(true, 'Demo time advanced. Expired monitoring evidence now produces unknown health.', { event: recorded.event });
    } else if (scenarioId === 'duplicate-delayed') {
      advance(state, 1);
      var original = state.events.find(function (event) { return event.serviceId === 'payments'; }) || state.events[0];
      recordEvent(state, Object.assign({}, clone(original), { receivedAt: state.now }));
      var observedAt = new Date(Date.parse(getService(state, 'payments').health.observedAt) - 30 * 60000).toISOString();
      outcome = applyHealthObservation(state, 'payments', { state: 'HEALTHY', observedAt: observedAt, expiresAt: new Date(Date.parse(observedAt) + 10 * 60000).toISOString(), source: 'Delayed payment synthetic sample', reason: 'A delayed sample reported healthy authorization before the latest observation.', latencyMs: 190, errorRate: 0.05, windowMinutes: 5 }, { title: 'Delayed payment signal retained in history', severity: 'INFO' });
      outcome.message = 'One duplicate was ignored and one older signal retained in history. Current health was not rolled back.';
      outcome.duplicate = true;
    }
    if (outcome && outcome.ok) {
      state.stats.scenarioRuns += 1;
      state.scenarioHistory.push({ id: scenarioId, at: state.now, serviceId: outcome.serviceId || null });
    }
    return outcome;
  }

  return {
    createState: data.createState, scenarios: data.scenarios, servicesInScope: servicesInScope, serviceHealth: serviceHealth,
    servicePosture: servicePosture, serviceFindings: serviceFindings, metrics: metrics, needsAttention: needsAttention,
    discoveryGap: discoveryGap, applyScenario: applyScenario, updateFinding: updateFinding, updateDependency: updateDependency,
    setDiscovery: setDiscovery, startAssessment: startAssessment, completeAssessment: completeAssessment,
    findingKey: findingKey, eventKey: eventKey, recordEvent: recordEvent, applyHealthObservation: applyHealthObservation,
    mergeServiceSummary: mergeServiceSummary, ageMinutes: ageMinutes
  };
});
