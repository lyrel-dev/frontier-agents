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
    if (!stored) return { state: 'UNKNOWN', rawState: null, components: {}, observedAt: null, ageMinutes: null, stale: false };
    var age = ageMinutes(state, stored.observedAt);
    var known = ['ACHIEVABLE', 'NOT_ACHIEVABLE', 'UNKNOWN'].indexOf(stored.state) >= 0;
    // A stale posture is still the last known assessed result; freshness is independent.
    return Object.assign({}, stored, { rawState: stored.state == null ? null : stored.state, state: known ? stored.state : 'UNKNOWN', ageMinutes: age, stale: age !== null && age > POSTURE_TTL_MINUTES, freshnessRule: '24-hour local demo review cadence' });
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
    return !config || config.status !== 'ENABLED' || config.eligibleResourceCount === null || config.eligibleResourceCount === undefined || config.eligibleResourceCount === 0;
  }

  function resourceDiscoveryGap(service) {
    var config = service && service.resourceDiscovery;
    return !config || config.status !== 'SUCCEEDED';
  }

  function findingCoverage(state, service) {
    service = getService(state, service);
    var records = service ? serviceFindings(state, service.id) : [];
    var unknownStatusCount = records.filter(function (finding) { return ['OPEN', 'RESOLVED', 'IRRELEVANT'].indexOf(finding.status) < 0; }).length;
    var latest = service && (state.findingCaptures || []).filter(function (capture) { return capture && capture.serviceArn === service.arn; }).sort(function (a, b) { return (Date.parse(b.captureEndedAt) || Date.parse(b.captureStartedAt) || 0) - (Date.parse(a.captureEndedAt) || Date.parse(a.captureStartedAt) || 0); })[0] || null;
    var captureTime = latest && Date.parse(latest.captureEndedAt);
    var validTime = Number.isFinite(captureTime) && captureTime <= currentTime(state);
    var observedAt = validTime ? latest.captureEndedAt : null;
    var stale = validTime && currentTime(state) - captureTime > POSTURE_TTL_MINUTES * 60000;
    var listComplete = latest && latest.listCoverage && latest.listCoverage.status === 'COMPLETE' && Object.keys(latest.listCoverage.filters || {}).length === 0;
    var complete = Boolean(validTime && listComplete && latest.collectionStatus === 'COMPLETE' && latest.detailCoverage && latest.detailCoverage.status === 'COMPLETE' && !unknownStatusCount);
    var status = !latest ? 'UNASSESSED' : stale ? 'STALE' : complete ? 'COMPLETE' : 'PARTIAL';
    var observedOpenCount = records.filter(function (finding) { return finding.status === 'OPEN'; }).length;
    var reason = !latest ? 'No complete finding collection has been captured; an empty local store is not evidence of zero findings.' : !validTime ? 'The finding capture end time is missing or inconsistent, so completeness and freshness cannot be established.' : stale ? 'Retained finding evidence is older than the local 24-hour review cadence.' : complete ? 'Counts describe the complete retained capture and current local dispositions, not verified remediation.' : 'Only the observed subset is counted; collection, detail or status coverage is incomplete.';
    return { status: status, observedCount: records.length, observedOpenCount: observedOpenCount, unknownStatusCount: unknownStatusCount, exactOpenCount: status === 'COMPLETE' ? observedOpenCount : null, countMeaning: !latest ? 'NO_CAPTURE' : stale ? 'STALE_CAPTURE' : complete ? 'COMPLETE_CAPTURE' : 'OBSERVED_SUBSET', observedAt: observedAt, latestCapture: latest, stale: Boolean(stale), reason: reason };
  }

  function attentionReasons(state, service) {
    service = getService(state, service);
    if (!service) return [];
    var health = serviceHealth(state, service), posture = servicePosture(state, service), reasons = [];
    function add(code, dimension, severity, message, observedAt) {
      reasons.push({ code: code, dimension: dimension, severity: severity, message: message, observedAt: observedAt || null });
    }
    if (health.state !== 'HEALTHY') {
      var healthCode = health.stale ? 'HEALTH_EVIDENCE_EXPIRED' : health.state === 'UNKNOWN' ? 'HEALTH_UNKNOWN' : 'RUNTIME_HEALTH_' + health.state;
      add(healthCode, 'HEALTH', health.state === 'UNAVAILABLE' ? 'ERROR' : 'WARNING', health.reason || 'Usable current monitoring evidence is unavailable.', health.observedAt);
    }
    if (posture.state === 'NOT_ACHIEVABLE') add('UNMET_OBJECTIVES', 'POSTURE', 'WARNING', 'One or more last observed resilience objectives are not achievable.', posture.observedAt);
    if (posture.state === 'UNKNOWN') add('POSTURE_UNKNOWN', 'POSTURE', 'WARNING', 'Usable assessed posture evidence has not been observed.', posture.observedAt);
    if (posture.stale) add('POSTURE_STALE', 'POSTURE', 'WARNING', 'Last known posture is older than the local 24-hour review cadence.', posture.observedAt);
    var open = serviceFindings(state, service.id).filter(function (finding) { return finding.status === 'OPEN'; });
    if (open.length) {
      var high = open.filter(function (finding) { return finding.severity === 'HIGH'; }).length;
      var observed = open.map(function (finding) { return finding.detailObservedAt || finding.updatedAt; }).filter(Boolean).sort().reverse()[0];
      add('OPEN_FINDINGS', 'FINDINGS', high ? 'WARNING' : 'INFO', open.length + ' open failure mode finding' + (open.length === 1 ? '' : 's') + (high ? ', including ' + high + ' high severity.' : '.'), observed);
    }
    var findingEvidence = findingCoverage(state, service);
    if (findingEvidence.status !== 'COMPLETE') add('FINDING_COLLECTION_INCOMPLETE', 'FINDINGS', 'WARNING', findingEvidence.reason, findingEvidence.observedAt);
    if (service.assessmentStatus === 'FAILED') {
      var failed = (state.assessments || []).filter(function (run) { return run.serviceArn === service.arn && run.status === 'FAILED'; }).sort(function (a, b) { return Date.parse(b.endedAt || b.startedAt) - Date.parse(a.endedAt || a.startedAt); })[0];
      add('ASSESSMENT_FAILED', 'ASSESSMENT', 'ERROR', 'The latest assessment failed; previous trustworthy posture is retained.', failed && (failed.endedAt || failed.startedAt));
    }
    if (resourceDiscoveryGap(service)) {
      var resource = service.resourceDiscovery || {};
      add('RESOURCE_DISCOVERY_GAP', 'RESOURCE_DISCOVERY', resource.status === 'FAILED' ? 'ERROR' : 'WARNING', resource.errorMessage || resource.error || 'Resource discovery has not established complete coverage (' + (resource.status || 'UNKNOWN') + ').', resource.lastRunAt);
    }
    if (discoveryGap(service)) {
      var discovery = service.dependencyDiscovery || {};
      add('DEPENDENCY_DISCOVERY_GAP', 'DEPENDENCY_DISCOVERY', 'WARNING', discovery.message || (discovery.eligibleResourceCount === 0 ? 'No eligible dependency-discovery resources have been observed.' : 'Dependency-discovery coverage is not established.'), discovery.updatedAt);
    }
    if (service.policyContextRefreshRequired) add('POLICY_CONTEXT_REFRESH_REQUIRED', 'POLICY_CONTEXT', 'WARNING', 'Policy or membership context changed after the captured assessment context; reassessment is required.', service.policyContextRefreshRequestedAt || service.updatedAt);
    if (service.reassessmentRequired === true) add('LOCAL_REASSESSMENT_REQUIRED', 'ASSESSMENT', 'WARNING', 'A service change or claimed repair requires independent reassessment evidence.', service.reassessmentRequestedAt || service.updatedAt);
    if (service.rerunAssessment === true) add('NATIVE_REASSESSMENT_REQUIRED', 'POLICY_CONTEXT', 'WARNING', 'The observed provider response explicitly requests that the assessment be rerun.', service.observedAt);
    var coverage = assessmentCoverage(state, service);
    if (['ACHIEVABLE', 'NOT_ACHIEVABLE'].indexOf(posture.state) >= 0 && (!coverage.lastKnown || coverage.partial)) add('ASSESSMENT_EVIDENCE_GAP', 'ASSESSMENT', 'WARNING', coverage.reason, coverage.observedAt);
    return reasons;
  }

  function needsAttention(state, service) {
    return attentionReasons(state, service).length > 0;
  }

  function assessmentCoverage(state, service) {
    service = getService(state, service);
    var posture = servicePosture(state, service), resource = service && service.resourceDiscovery || {};
    // Component applicability belongs to the context captured with this posture,
    // never to a subsequently edited policy or today's association list.
    var context = service && (state.policyContexts || []).find(function (item) { return item.policyContextCaptureId === posture.policyContextCaptureId && item.serviceArn === service.arn; });
    var targets = context && (state.effectiveTargetObservations || []).find(function (item) { return item.effectiveTargetObservationId === context.effectiveTargetObservationId && item.serviceArn === service.arn; });
    var metricComponents = { availabilitySlo: 'availabilitySlo', dataRecoveryTimeBetweenBackups: 'dataRecovery', multiAzRto: 'multiAz', multiAzRpo: 'multiAz', multiAzDrApproach: 'multiAz', multiRegionRto: 'multiRegion', multiRegionRpo: 'multiRegion', multiRegionDrApproach: 'multiRegion' };
    var contextKnown = Boolean(targets && Array.isArray(targets.targets) && targets.targets.every(function (target) { return target && typeof target === 'object' && Object.prototype.hasOwnProperty.call(metricComponents, target.metric); }));
    var expectedComponents = contextKnown ? Array.from(new Set(targets.targets.map(function (target) { return metricComponents[target.metric]; }))) : null;
    var missingExpected = contextKnown && expectedComponents.some(function (key) { return ['ACHIEVABLE', 'NOT_ACHIEVABLE'].indexOf(posture.components && posture.components[key]) < 0; });
    var unknownTargets = contextKnown && targets.targets.some(function (target) { return target.value === undefined || target.value === null; });
    var hasPosture = ['ACHIEVABLE', 'NOT_ACHIEVABLE'].indexOf(posture.state) >= 0 && Number.isFinite(Date.parse(posture.observedAt));
    var successful = service && (state.assessments || []).some(function (run) {
      return run.serviceArn === service.arn && run.status === 'SUCCESS' && (posture.assessmentId ? run.assessmentId === posture.assessmentId : Date.parse(run.endedAt || run.observedAt) <= Date.parse(posture.observedAt));
    });
    var lastKnown = Boolean(hasPosture && successful);
    var inaccessible = resource.status === 'FAILED' && /ACCESS|PERMISSION|UNAUTHORIZED/i.test(String(resource.errorCode || ''));
    var contextRefreshRequired = Boolean(service && (service.policyContextRefreshRequired || service.rerunAssessment === true));
    var reassessmentRequired = Boolean(service && service.reassessmentRequired === true);
    var partial = lastKnown && (!contextKnown || !expectedComponents.length || missingExpected || unknownTargets || posture.collectionStatus === 'PARTIAL' || resourceDiscoveryGap(service) || contextRefreshRequired || reassessmentRequired);
    var stale = Boolean(lastKnown && posture.stale);
    var status = inaccessible ? 'INACCESSIBLE' : !lastKnown ? 'UNASSESSED' : partial ? 'PARTIAL' : stale ? 'STALE' : 'CURRENT';
    var reasons = [];
    if (!lastKnown) reasons.push('No usable posture with a retained successful assessment is available.');
    if (inaccessible) reasons.push('Resource coverage is inaccessible with the current permissions.');
    if (lastKnown && !contextKnown) reasons.push('The effective-objective context captured with this posture is unavailable.');
    if (lastKnown && contextKnown && !expectedComponents.length) reasons.push('No effective objectives were captured, so coverage cannot be asserted.');
    if (lastKnown && (missingExpected || unknownTargets)) reasons.push('Some expected objectives or component outcomes are missing from the captured evidence.');
    if (lastKnown && (posture.collectionStatus === 'PARTIAL' || resourceDiscoveryGap(service))) reasons.push('Resource or posture collection is incomplete.');
    if (service && service.policyContextRefreshRequired) reasons.push('The assessment context needs a refresh after configuration changes.');
    if (reassessmentRequired) reasons.push('A service change or claimed repair requires independent reassessment evidence.');
    if (service && service.rerunAssessment === true) reasons.push('The observed provider response explicitly requests reassessment.');
    if (stale) reasons.push('The evidence exceeds the local 24-hour review cadence.');
    if (status === 'CURRENT') reasons.push('Successful assessment evidence is complete and within the local 24-hour review cadence.');
    return { status: status, lastKnown: lastKnown, current: status === 'CURRENT', observedAt: hasPosture ? posture.observedAt : null, stale: stale, partial: Boolean(partial), inaccessible: inaccessible, contextRefreshRequired: contextRefreshRequired, policyContextKnown: contextKnown, expectedComponents: expectedComponents, ruleVersion: 'assessment-evidence-24h-v2', reason: reasons.join(' ') };
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
    var coverage = services.map(function (service) { return assessmentCoverage(state, service); });
    var assessed = coverage.filter(function (item) { return item.current; }).length;
    var lastKnownAssessed = coverage.filter(function (item) { return item.lastKnown; }).length;
    var coverageByStatus = {};
    ['CURRENT', 'STALE', 'PARTIAL', 'UNASSESSED', 'INACCESSIBLE'].forEach(function (status) { coverageByStatus[status] = coverage.filter(function (item) { return item.status === status; }).length; });
    var attentionByDimension = {};
    services.forEach(function (service) {
      var dimensions = new Set(attentionReasons(state, service).map(function (reason) { return reason.dimension; }));
      dimensions.forEach(function (dimension) { attentionByDimension[dimension] = (attentionByDimension[dimension] || 0) + 1; });
    });
    var count = function (health) { return healths.filter(function (item) { return item.state === health; }).length; };
    return {
      services: services.length, totalServices: services.length, serviceIds: services.map(function (service) { return service.id; }),
      healthy: count('HEALTHY'), degraded: count('DEGRADED'), unavailable: count('UNAVAILABLE'), unknownHealth: count('UNKNOWN'),
      attention: services.filter(function (service) { return needsAttention(state, service); }).length,
      openFindings: findings.filter(function (finding) { return finding.status === 'OPEN'; }).length,
      highFindings: findings.filter(function (finding) { return finding.status === 'OPEN' && finding.severity === 'HIGH'; }).length,
      resolvedFindings: findings.filter(function (finding) { return finding.status === 'RESOLVED'; }).length,
      suppressedFindings: findings.filter(function (finding) { return finding.status === 'IRRELEVANT'; }).length,
      assessed: assessed, assessmentCoverage: services.length ? Math.round(100 * assessed / services.length) : null,
      currentAssessed: assessed, lastKnownAssessed: lastKnownAssessed,
      currentAssessmentCoverage: services.length ? Math.round(100 * assessed / services.length) : null,
      lastKnownAssessmentCoverage: services.length ? Math.round(100 * lastKnownAssessed / services.length) : null,
      assessmentCoverageByStatus: coverageByStatus, staleAssessmentEvidence: coverage.filter(function (item) { return item.stale; }).length,
      partialAssessmentEvidence: coverage.filter(function (item) { return item.partial; }).length,
      attentionByDimension: attentionByDimension,
      activeAssessments: services.filter(function (service) { return ACTIVE.indexOf(service.assessmentStatus) >= 0; }).length,
      failedAssessments: services.filter(function (service) { return service.assessmentStatus === 'FAILED'; }).length,
      discoveryGaps: services.filter(discoveryGap).length,
      staleServices: services.filter(function (service) { return serviceHealth(state, service).stale || servicePosture(state, service).stale; }).length,
      achievabilityAttention: services.filter(function (service) { return servicePosture(state, service).state === 'NOT_ACHIEVABLE'; }).length,
      contributorIds: services.map(function (service) { return service.arn; }),
      computedAt: state.now, aggregationRule: 'distinct-service-attention-v2',
      coverageLabel: 'Services with current complete successful assessment evidence; retained historical coverage is separate',
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
    if (!observation || ['HEALTHY', 'DEGRADED', 'UNAVAILABLE', 'UNKNOWN'].indexOf(observation.state) < 0 || !Number.isFinite(Date.parse(observation.observedAt)) || !Number.isFinite(Date.parse(observation.expiresAt)) || Date.parse(observation.expiresAt) <= Date.parse(observation.observedAt)) return result(false, 'Health evidence needs a valid state, observation time and later expiry.');
    if (Date.parse(observation.observedAt) > currentTime(state) + 5 * 60000) return result(false, 'The health observation is more than five minutes ahead of the demo clock.');
    var captured = Object.assign({ observationId: nextId(state, 'health'), entityId: service.id, dimension: 'HEALTH', provenance: 'LOCAL_MONITORING_AGGREGATE', ruleVersion: 'northstar-runtime-v1' }, clone(observation));
    var stale = service.health && Date.parse(captured.observedAt) <= Date.parse(service.health.observedAt);
    var recorded = recordEvent(state, Object.assign({ channel: 'TELEMETRY', streamOwner: 'northstar/' + service.id + '/runtime', type: 'RUNTIME_HEALTH_CHANGED', title: service.name + ' health signal received', message: captured.reason, serviceId: service.id, entityType: 'Service', entityId: service.id, occurredAt: captured.observedAt, receivedAt: state.now, refreshStatus: stale ? 'OLDER_EVIDENCE' : 'REFRESHED' }, eventFields || {}));
    if (recorded.duplicate) return result(true, 'Duplicate event ignored; current health is unchanged.', { serviceId: service.id, event: recorded.event, duplicate: true });
    state.observations.push(captured);
    if (stale) {
      state.stats.staleEvents += 1;
      return result(true, 'Older or equal-time monitoring evidence retained in history; current health is unchanged.', { serviceId: service.id, event: recorded.event, stale: true });
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
      // Reading back a mutable disposition is not independent repair evidence.
      // Keep UNVERIFIED and SUPPRESSED until an explicit verification observation
      // is supplied by a separate evidence source.
    });
    return captureId;
  }

  function completeAssessment(state, serviceId) {
    var service = getService(state, serviceId || 'orders');
    if (!service) return result(false, 'Service not found.');
    var run = latestActiveAssessment(state, service);
    if (!run) return result(false, 'Start an assessment for ' + service.name + ' before completing it.', { serviceId: service.id });
    var response = data.assessmentResponse(service.id);
    if (!response) return result(false, 'No independent assessment response fixture exists for this service.', { serviceId: service.id });
    advance(state, 4);
    run.status = 'SUCCESS'; run.endedAt = state.now; run.observedAt = state.now;
    run.totalFindings = serviceFindings(state, service.id).length;
    run.cost = { amount: 3.72, currency: 'USD' };
    delete run.errorCode; delete run.error; delete run.stepLabel;
    var nativeComponents = clone(response.components);
    run.achievability = clone(nativeComponents);
    run.responseFixtureId = response.fixtureId;
    run.configurationScenario = response.configurationScenario;
    service.assessmentStatus = 'SUCCESS';
    service.observedAt = state.now;
    var policyContextCaptureId = nextId(state, 'policy-context');
    var effectiveTargetObservationId = nextId(state, 'targets');
    state.effectiveTargetObservations.push({ effectiveTargetObservationId: effectiveTargetObservationId, serviceId: service.id, serviceArn: service.arn, observedAt: state.now, targets: clone(service.effectiveTargets), evaluatedProviderRevision: null });
    state.policyContexts.push({ policyContextCaptureId: policyContextCaptureId, serviceArn: service.arn, observedAt: state.now, associations: clone(service.associations), applicablePolicies: clone(service.applicablePolicies), effectiveTargetObservationId: effectiveTargetObservationId, provenance: 'LOCAL_CAPTURE', assessedProviderRevision: null });
    service.effectiveTargetObservationId = effectiveTargetObservationId;
    service.policyContextCaptureId = policyContextCaptureId;
    var componentValues = Object.values(nativeComponents);
    var postureState = componentValues.indexOf('NOT_ACHIEVABLE') >= 0 ? 'NOT_ACHIEVABLE' : componentValues.length === 4 && componentValues.every(function (value) { return value === 'ACHIEVABLE'; }) ? 'ACHIEVABLE' : 'UNKNOWN';
    service.posture = { observationId: nextId(state, 'posture'), state: postureState, components: nativeComponents, observedAt: state.now, assessmentId: run.assessmentId, assessmentLinkage: 'LOCAL_CORRELATION', assessmentCorrelationBasis: 'Posture observed after this completed assessment; no evaluated provider policy revision is exposed.', policyContextCaptureId: policyContextCaptureId, source: 'Independent mock GetService.achievability response', ruleVersion: 'any-unachievable-v2', provenance: 'PROVIDER_COMPONENTS_WITH_LOCAL_SUMMARY', evaluatedProviderRevision: null, responseFixtureId: response.fixtureId, configurationScenario: response.configurationScenario, collectionStatus: response.collectionStatus };
    state.observations.push(Object.assign({ entityId: service.id, dimension: 'POSTURE' }, clone(service.posture)));
    captureFindings(state, service, run);
    var recorded = recordEvent(state, { channel: 'EVENTBRIDGE', streamOwner: service.arn, type: 'Failure Mode Assessment Completed', title: service.name + ' assessment completed', message: 'An independent mock response refreshed posture. Operator dispositions do not change these outcomes or verify repair. Runtime monitoring health is unchanged.', serviceId: service.id, entityType: 'Assessment', entityId: run.assessmentId, refreshStatus: 'REFRESHED', refreshOperations: ['GetService', 'ListFailureModeAssessments', 'ListFailureModeFindings', 'GetFailureModeFinding'] });
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
    if (status !== previousStatus && status === 'RESOLVED') service.reassessmentRequired = true;
    service.openFindingsCount = serviceFindings(state, service.id).filter(function (item) { return item.status === 'OPEN'; }).length;
    service.resolvedFindingsCount = serviceFindings(state, service.id).filter(function (item) { return item.status === 'RESOLVED'; }).length;
    var recorded = recordEvent(state, { streamOwner: service.arn, type: 'FINDING_STATUS_UPDATED', title: finding.name, message: status === 'RESOLVED' ? 'Operator marked the finding resolved. Verification is pending; assessed posture and runtime health have not changed.' : status === 'IRRELEVANT' ? 'Operator suppressed this finding as irrelevant. Suppression does not establish remediation.' : 'Operator reopened the finding for investigation.', serviceId: service.id, entityType: 'Finding', entityId: finding.findingId, operation: 'UpdateFailureModeFinding', refreshStatus: 'LOCAL_ONLY' });
    changed(state);
    return result(true, status === 'RESOLVED' ? 'Marked resolved; independent verification evidence is still required.' : status === 'IRRELEVANT' ? 'Finding marked irrelevant. It remains available as a suppressed finding.' : 'Finding reopened.', { serviceId: service.id, event: recorded.event });
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
    discoveryGap: discoveryGap, resourceDiscoveryGap: resourceDiscoveryGap, attentionReasons: attentionReasons, findingCoverage: findingCoverage, assessmentCoverage: assessmentCoverage, applyScenario: applyScenario, updateFinding: updateFinding, updateDependency: updateDependency,
    setDiscovery: setDiscovery, startAssessment: startAssessment, completeAssessment: completeAssessment,
    findingKey: findingKey, eventKey: eventKey, recordEvent: recordEvent, applyHealthObservation: applyHealthObservation,
    mergeServiceSummary: mergeServiceSummary, ageMinutes: ageMinutes
  };
});
