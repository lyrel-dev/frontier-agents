'use strict';

const crypto = require('node:crypto');
const fixture = require('../data.js');
const model = require('../model.js');
const contract = require('./contract.cjs');
const clone = value => structuredClone(value);
const own = (value, key) => Object.prototype.hasOwnProperty.call(value, key);
const epoch = value => { const parsed = value == null ? null : typeof value === 'number' ? value : Date.parse(value) / 1000; return Number.isFinite(parsed) ? parsed : null; };
const iso = value => new Date(Math.round(value * 1000)).toISOString();
const canonical = value => value === null || typeof value !== 'object' ? JSON.stringify(value) : Array.isArray(value) ? '[' + value.map(canonical).join(',') + ']' : '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + canonical(value[key])).join(',') + '}';
const digest = value => crypto.createHash('sha256').update(canonical(value)).digest('hex');

class RpcError extends Error {
  constructor(type, message) { super(message); this.name = type; this.type = type; this.statusCode = contract.errors[type]?.statusCode || 500; }
  toJSON() { return { __type: contract.namespace + '#' + this.type, message: this.message }; }
}
const fail = (type, message) => { throw new RpcError(type, message); };
const invalid = message => fail('ValidationException', message);
const conflict = message => fail('ConflictException', message);

function assertJson(value, path = '$', visited = new Set()) {
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return;
  if (typeof value === 'number') { if (!Number.isFinite(value)) invalid(path + ' must contain finite JSON numbers.'); return; }
  if (!value || typeof value !== 'object' || visited.has(value)) invalid(path + ' must contain acyclic JSON data.');
  visited.add(value);
  for (const [key, child] of Object.entries(value)) assertJson(child, path + '.' + key, visited);
  visited.delete(value);
}

/** The deliberately small validator covers every keyword used by contract.cjs. */
function validate(schema, value, path = '$') {
  if (schema.$ref) return validate(contract.shapes[schema.$ref.split('/').pop()], value, path);
  if (schema.anyOf) {
    if (!schema.anyOf.some(branch => { try { validate(branch, value, path); return true; } catch (error) { if (error instanceof RpcError) return false; throw error; } })) invalid(path + ' has an invalid type or value.');
    return;
  }
  if (own(schema, 'const') && value !== schema.const) invalid(path + ' must equal ' + JSON.stringify(schema.const) + '.');
  if (schema.enum && !schema.enum.includes(value)) invalid(path + ' must be one of ' + schema.enum.join(', ') + '.');
  if (schema.type === 'null') { if (value !== null) invalid(path + ' must be null.'); return; }
  if (schema.type === 'string') {
    if (typeof value !== 'string') invalid(path + ' must be a string.');
    if (value.length < (schema.minLength || 0) || value.length > (schema.maxLength ?? Infinity)) invalid(path + ' has an invalid length.');
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) invalid(path + ' has an invalid format.');
  } else if (schema.type === 'number' || schema.type === 'integer') {
    if (typeof value !== 'number' || !Number.isFinite(value) || (schema.type === 'integer' && !Number.isInteger(value))) invalid(path + ' must be a finite ' + schema.type + '.');
    if (value < (schema.minimum ?? -Infinity) || value > (schema.maximum ?? Infinity)) invalid(path + ' is outside the allowed range.');
    if (schema['x-precision'] === 'milliseconds' && Math.round(value * 1000) / 1000 !== value) invalid(path + ' must have at most millisecond precision.');
  } else if (schema.type === 'boolean') {
    if (typeof value !== 'boolean') invalid(path + ' must be a boolean.');
  } else if (schema.type === 'array') {
    if (!Array.isArray(value)) invalid(path + ' must be an array.');
    if (value.length < (schema.minItems || 0) || value.length > (schema.maxItems ?? Infinity)) invalid(path + ' has an invalid number of items.');
    value.forEach((item, index) => validate(schema.items, item, path + '[' + index + ']'));
    if (schema.uniqueItems && new Set(value.map(canonical)).size !== value.length) invalid(path + ' contains duplicate items.');
  } else if (schema.type === 'object') {
    if (!value || typeof value !== 'object' || Array.isArray(value)) invalid(path + ' must be an object.');
    const keys = Object.keys(value);
    if (keys.length < (schema.minProperties || 0) || keys.length > (schema.maxProperties ?? Infinity)) invalid(path + ' has an invalid number of members.');
    for (const required of schema.required || []) if (!own(value, required)) invalid(path + '.' + required + ' is required.');
    for (const key of keys) {
      if (['__proto__', 'prototype', 'constructor'].includes(key)) invalid(path + ' contains a reserved member name.');
      if (schema.propertyNames) validate(schema.propertyNames, key, path + ' member name');
      if (own(schema.properties || {}, key)) validate(schema.properties[key], value[key], path + '.' + key);
      else if (schema.additionalProperties === false) invalid(path + '.' + key + ' is unknown or read-only.');
      else if (schema.additionalProperties && schema.additionalProperties !== true) validate(schema.additionalProperties, value[key], path + '.' + key);
    }
  } else {
    throw new Error('Unsupported contract schema at ' + path);
  }
}

function createRuntime(options = {}) {
  let state = clone(options.state || fixture.createState());
  const clock = options.now || Date.now;
  const openedAt = clock();
  const initialDemoTime = Date.parse(state.now);
  const secret = options.secret || crypto.randomBytes(32);
  const tenantId = options.tenantId || 'northstar';
  const defaultPrincipal = options.principal || { id: 'demo-operator', tenantId, roles: ['reader', 'operator', 'admin', 'ingestor'] };
  const cursorTtlMs = (options.cursorTtlSeconds ?? contract.limits.cursorTtlSeconds) * 1000;
  const idempotencyTtlMs = (options.idempotencyTtlSeconds ?? contract.limits.idempotencyTtlSeconds) * 1000;
  const snapshots = new Map();
  let snapshotSequence = 0;
  const idempotency = new Map();
  const operations = new Map(contract.operations.map(operation => [operation.name, operation]));
  state.rpc = state.rpc || { sequence: 3000, eventSequence: 0, projectionVersion: 1, tombstones: [], recommendationEnrichments: {}, ingestedKeys: {} };
  for (const collection of ['systems', 'journeys', 'services', 'policies', 'assessments', 'findings', 'dependencies', 'topologies']) {
    for (const item of state[collection]) item.version ||= 1;
  }
  for (const service of state.services) for (const input of service.inputSources || []) input.version ||= 1;
  for (const service of state.services) service.projectionVersion ||= 1;
  for (const dependency of state.dependencies) dependency.governance.version ||= 1;
  for (const event of [...state.events].reverse()) { event.sequence ||= ++state.rpc.eventSequence; event.producerPrincipalId ??= null; event.trustedSource ??= false; }
  for (const recommendation of state.recommendations) {
    state.rpc.recommendationEnrichments[recommendation.id] ||= { title: recommendation.title || 'Recommendation', description: recommendation.description || '', estimate: clone(recommendation.estimate || null), version: 1, updatedAt: recommendation.capturedAt || state.now, provenance: 'LOCAL_PRODUCT_ENRICHMENT' };
  }

  function logicalNow(s) { return new Date(Math.max(Date.parse(s.now), initialDemoTime + Math.max(0, clock() - openedAt))).toISOString(); }
  function freshState(s) { s.now = logicalNow(s); }
  function nextId(s, prefix) { return prefix + '-' + (++s.rpc.sequence); }
  function nextUuid(s) { return '73000000-0000-4000-8000-' + String(++s.rpc.sequence).padStart(12, '0'); }
  function nextArn(s, type) { return `arn:aws:resiliencehub:eu-west-1:111122223333:${type}/${nextUuid(s)}`; }
  function active(items) { return items.filter(item => !item.deletedAt); }
  function get(s, collection, key, value, historical = false) {
    const item = s[collection].find(candidate => candidate[key] === value && (historical || !candidate.deletedAt));
    if (!item) fail('ResourceNotFoundException', collection + ' entity was not found in this workspace.');
    return item;
  }
  const service = (s, serviceArn, historical = false) => get(s, 'services', 'arn', serviceArn, historical);
  const system = (s, systemArn) => get(s, 'systems', 'arn', systemArn);
  const policy = (s, policyArn) => get(s, 'policies', 'arn', policyArn);
  function journey(s, systemArn, userJourneyId) {
    const parent = system(s, systemArn);
    const item = active(s.journeys).find(candidate => candidate.systemId === parent.id && candidate.userJourneyId === userJourneyId);
    if (!item) fail('ResourceNotFoundException', 'User journey was not found in the requested system.');
    return item;
  }
  function scoped(s, collection, p, field, historical = true) {
    service(s, p.serviceArn, historical);
    const item = s[collection].find(candidate => candidate.serviceArn === p.serviceArn && candidate[field] === p[field] && !candidate.deletedAt);
    if (!item) fail('ResourceNotFoundException', collection + ' entity was not found in the requested service.');
    return item;
  }
  function assertVersion(item, expectedVersion) { if ((item.version || 1) !== expectedVersion) conflict('expectedVersion does not match the current local version. Read the entity and retry with a new clientToken.'); }
  function bump(s, item) { item.version = (item.version || 1) + 1; item.localUpdatedAt = s.now; }
  function bumpProjection(s, item) { item.projectionVersion = (item.projectionVersion || 1) + 1; item.projectionComputedAt = s.now; }
  function assertChange(p, names) { if (!names.some(key => own(p, key))) invalid('At least one mutable field must be present.'); }
  function assertUniqueName(s, collection, name, within = () => true, except = null) {
    if (active(s[collection]).some(item => item !== except && within(item) && (item.providerName || item.id) === name)) conflict('An active entity with this name already exists in this scope.');
  }
  function associationRecords(s, associatedSystems = []) {
    const seen = new Set();
    return associatedSystems.map(association => {
      const parent = system(s, association.systemArn);
      if (seen.has(parent.id)) invalid('associatedSystems contains a duplicate system.');
      seen.add(parent.id);
      const journeys = association.userJourneyIds || [];
      if (new Set(journeys).size !== journeys.length) invalid('userJourneyIds contains duplicates.');
      return { systemId: parent.id, journeyIds: journeys.map(journeyId => journey(s, association.systemArn, journeyId).id) };
    });
  }
  function scopeServices(s, p) {
    if (p.userJourneyId && !p.systemArn) invalid('systemArn is required when userJourneyId is specified.');
    const parent = p.systemArn ? system(s, p.systemArn) : null;
    const j = p.userJourneyId ? journey(s, p.systemArn, p.userJourneyId) : null;
    return active(s.services).filter(item => (!parent || item.associations.some(a => a.systemId === parent.id && (!j || a.journeyIds.includes(j.id)))) && (!p.query || (item.name + ' ' + item.id + ' ' + item.description).toLowerCase().includes(p.query.toLowerCase())));
  }
  function refresh(s, item, { policyContext = false, reassessment = false } = {}) {
    item.refreshRequired = true;
    item.refreshRequestedAt = s.now;
    if (policyContext) { item.policyContextRefreshRequired = true; item.policyContextRefreshRequestedAt = s.now; }
    if (reassessment) item.reassessmentRequired = true;
  }
  function stampEvents(s, principal) {
    for (const event of [...s.events].reverse()) {
      if (!event.sequence) event.sequence = ++s.rpc.eventSequence;
      if (!own(event, 'producerPrincipalId')) event.producerPrincipalId = principal.id;
      if (!own(event, 'trustedSource')) event.trustedSource = false;
    }
  }
  function subject(entityType, entityId, context = {}, relationship = 'SUBJECT') {
    const item = { entityType, entityId, relationship };
    for (const key of ['serviceArn', 'systemArn', 'findingId']) if (context[key]) item[key] = context[key];
    return item;
  }
  function audit(s, name, p, response, principal) {
    const definitions = [
      ['system', 'System', 'systemArn'], ['userJourney', 'UserJourney', 'userJourneyId'],
      ['service', 'Service', 'serviceArn'], ['policy', 'Policy', 'policyArn'],
      ['inputSource', 'InputSource', 'inputSourceId'], ['assessment', 'Assessment', 'assessmentId'],
      ['finding', 'Finding', 'findingId'], ['recommendation', 'Recommendation', 'recommendationId'],
      ['dependency', 'Dependency', 'dependencyId'], ['topologySnapshot', 'TopologySnapshot', 'topologyId']
    ];
    const definition = definitions.find(([field]) => response[field]);
    const entity = definition ? response[definition[0]] : response.deletion;
    const type = definition ? definition[1] : name.replace(/^Delete/, '');
    const entityId = definition ? entity[definition[2]] : entity.resourceId;
    const context = { ...p, ...entity };
    if (type === 'Service') context.serviceArn = entityId;
    const subjects = [subject(type, entityId, context)];
    const add = item => { if (!subjects.some(existing => existing.entityType === item.entityType && existing.entityId === item.entityId && existing.serviceArn === item.serviceArn && existing.systemArn === item.systemArn)) subjects.push(item); };
    if (context.serviceArn && type !== 'Service') add(subject('Service', context.serviceArn, { serviceArn: context.serviceArn }, 'RELATED'));
    if (context.systemArn && type !== 'System') add(subject('System', context.systemArn, {}, 'RELATED'));
    if (type === 'Policy' || type === 'UserJourney') {
      for (const svc of active(s.services)) {
        const related = type === 'Policy'
          ? svc.policyArn === entityId || svc.associations.some(a => a.journeyIds.some(jid => s.journeys.some(j => j.id === jid && j.policyArn === entityId)))
          : svc.associations.some(a => a.journeyIds.some(jid => s.journeys.some(j => j.id === jid && j.userJourneyId === entityId && s.systems.some(system => system.id === j.systemId && system.arn === context.systemArn))));
        if (related) add(subject('Service', svc.arn, { serviceArn: svc.arn }, 'RELATED'));
      }
    }
    const svc = context.serviceArn ? s.services.find(item => item.arn === context.serviceArn) : null;
    model.recordEvent(s, { streamOwner: entityId, type: name, title: name + ' committed', message: 'Local mock command committed; no AWS request was made.', serviceId: svc?.id || null, serviceArn: context.serviceArn || null, entityType: type, entityId, subjects, rawEvent: null, correlationIds: [], producerPrincipalId: principal.id, trustedSource: true, source: 'resilience.workspace.mock', refreshStatus: 'LOCAL_ONLY' });
    stampEvents(s, principal);
  }
  function remove(s, collection, item, resourceId) {
    item.deletedAt = s.now; bump(s, item);
    const receipt = { resourceId, deleted: true, deletedAt: epoch(s.now), version: item.version, historyRetained: true };
    s.rpc.tombstones.push({ collection, ...receipt });
    return { deletion: receipt };
  }

  function normalized(value, allowed, diagnostics, path, fallback = 'UNKNOWN') {
    if (allowed.includes(value)) return value;
    diagnostics.push({ path, rawValue: value == null ? null : typeof value === 'string' ? value : JSON.stringify(value), normalizedValue: fallback, reason: value == null ? 'MISSING' : 'UNKNOWN_ENUM' });
    return fallback;
  }
  const assessmentStates = ['NOT_STARTED', 'PENDING', 'IN_PROGRESS', 'SUCCESS', 'FAILED'];
  const findingStates = ['OPEN', 'RESOLVED', 'IRRELEVANT'];
  const findingSeverities = ['HIGH', 'MEDIUM', 'LOW'];
  function achievability(value = {}, diagnostics = []) {
    value ||= {};
    return Object.fromEntries([['availabilitySlo', 'availabilitySlo'], ['multiAzRtoRpo', 'multiAz'], ['multiRegionRtoRpo', 'multiRegion'], ['dataRecoveryTimeBetweenBackups', 'dataRecovery']]
      .filter(([key, localKey]) => own(value, key) || own(value, localKey))
      .map(([key, localKey]) => { const raw = own(value, key) ? value[key] : value[localKey]; return [key, raw == null ? null : normalized(raw, ['ACHIEVABLE', 'NOT_ACHIEVABLE', 'UNKNOWN'], diagnostics, 'achievability.' + key)]; }));
  }
  function discoveryDto(value, parentDiagnostics = []) {
    const d = value || {}, normalizationDiagnostics = [];
    const status = normalized(d.status, ['ENABLED', 'DISABLED', 'INITIALIZING'], normalizationDiagnostics, 'dependencyDiscovery.status');
    parentDiagnostics.push(...normalizationDiagnostics);
    return { status, rawStatus: d.status ?? null, eligibleResourceCount: d.eligibleResourceCount ?? null, message: d.message ?? null, updatedAt: epoch(d.updatedAt), ...(['ENABLED', 'DISABLED'].includes(d.requestedStatus) ? { requestedStatus: d.requestedStatus } : {}), normalizationDiagnostics };
  }
  function resourceDiscoveryDto(value, parentDiagnostics = []) {
    const d = value || {}, normalizationDiagnostics = [];
    const status = normalized(d.status, ['NOT_STARTED', 'PENDING', 'RUNNING', 'IN_PROGRESS', 'SUCCEEDED', 'FAILED', 'COMPLETED_WITH_FAILURES'], normalizationDiagnostics, 'resourceDiscovery.status');
    parentDiagnostics.push(...normalizationDiagnostics);
    return { status, rawStatus: d.status ?? null, lastRunAt: epoch(d.lastRunAt), errorCode: d.errorCode ?? null, errorMessage: d.errorMessage ?? d.error ?? null, normalizationDiagnostics };
  }
  function permissionDto(p) {
    if (!p) return null;
    return { invokerRoleName: p.invokerRoleName ?? null, crossAccountRoles: Array.isArray(p.crossAccountRoles) ? p.crossAccountRoles.map(role => ({ crossAccountRoleArn: role.crossAccountRoleArn ?? role.arn ?? null, externalId: role.externalId ?? null })) : null };
  }
  function resolvedJourney(s, localId) { return localId ? s.journeys.find(item => item.id === localId || item.userJourneyId === localId) : null; }
  function journeyScope(s, localId) {
    const j = resolvedJourney(s, localId), parent = j && s.systems.find(item => item.id === j.systemId);
    return { systemArn: parent?.arn || null, userJourneyId: j?.userJourneyId || null };
  }
  function policyEvidenceDto(s, svc, diagnostics = [], usePostureContext = true) {
    const contextId = usePostureContext ? svc.posture?.policyContextCaptureId || svc.policyContextCaptureId : svc.policyContextCaptureId;
    const context = s.policyContexts.find(item => item.policyContextCaptureId === contextId && item.serviceArn === svc.arn);
    const targetId = context ? context.effectiveTargetObservationId : contextId ? null : svc.effectiveTargetObservationId;
    const target = s.effectiveTargetObservations.find(item => item.effectiveTargetObservationId === targetId && item.serviceArn === svc.arn);
    const effectiveTargetObservation = target ? {
      effectiveTargetObservationId: target.effectiveTargetObservationId, serviceArn: svc.arn, observedAt: epoch(target.observedAt),
      targets: (target.targets || []).map(t => ({ metric: t.metric, label: t.label || '', value: t.value ?? null, unit: t.unit || '', policyName: t.policyName ?? null, ownership: normalized(t.ownership ?? t.source, ['SELF', 'CROSS_ACCOUNT'], diagnostics, 'effectivePolicyEvidence.targets.' + t.metric + '.ownership'), rawOwnership: t.ownership ?? t.source ?? null, assignment: normalized(t.assignment, ['DIRECT', 'INHERITED'], diagnostics, 'effectivePolicyEvidence.targets.' + t.metric + '.assignment'), ...journeyScope(s, t.journeyId), resolvedPolicyArn: t.resolvedPolicyArn || null, resolutionEvidence: t.resolutionEvidence || null, provenance: t.provenance || 'LOCAL_CAPTURE' })),
      evaluatedProviderRevision: target.evaluatedProviderRevision ?? null, provenance: target.provenance || 'LOCAL_CAPTURE_OF_EFFECTIVE_TARGETS'
    } : null;
    const policyContextCapture = context ? {
      policyContextCaptureId: context.policyContextCaptureId, serviceArn: svc.arn, observedAt: epoch(context.observedAt),
      associations: (context.associations || []).map(a => {
        const parent = s.systems.find(item => item.id === a.systemId || item.arn === a.systemArn);
        return { systemArn: parent?.arn || a.systemArn || null, userJourneyIds: a.userJourneyIds || (a.journeyIds || []).map(jid => resolvedJourney(s, jid)?.userJourneyId).filter(Boolean), localSystemReference: a.systemId || a.systemArn || 'unresolved', identityResolution: parent ? 'LOCAL_REFERENCE' : 'UNRESOLVED' };
      }),
      applicablePolicies: (context.applicablePolicies || []).map(a => {
        const referenced = s.policies.find(item => item.id === a.policyId || item.arn === a.policyArn);
        return { policyArn: referenced?.arn || a.policyArn || null, assignment: normalized(a.assignment, ['DIRECT', 'INHERITED'], diagnostics, 'effectivePolicyEvidence.policyAssignment'), ...journeyScope(s, a.journeyId), localPolicyReference: a.policyId || a.policyArn || null, identityResolution: referenced ? 'LOCAL_REFERENCE' : 'UNRESOLVED' };
      }),
      effectiveTargetObservationId: context.effectiveTargetObservationId || null, assessedProviderRevision: context.assessedProviderRevision ?? null, provenance: context.provenance || 'LOCAL_CAPTURE'
    } : null;
    return { effectiveTargetObservation, policyContextCapture };
  }
  function findingCaptureDto(capture, diagnostics = []) {
    if (!capture) return null;
    const list = capture.listCoverage || {}, detail = capture.detailCoverage || {};
    return { captureId: capture.captureId, serviceArn: capture.serviceArn, captureStartedAt: epoch(capture.captureStartedAt), captureEndedAt: epoch(capture.captureEndedAt), collectionStatus: normalized(capture.collectionStatus, ['COMPLETE', 'PARTIAL', 'FAILED'], diagnostics, 'findingCapture.collectionStatus'), listCoverage: { status: normalized(list.status, ['COMPLETE', 'PARTIAL', 'FAILED'], diagnostics, 'findingCapture.listCoverage.status'), pages: list.pages ?? null, filters: clone(list.filters || {}), findingsReturned: list.findingsReturned ?? null }, detailCoverage: { status: normalized(detail.status, ['COMPLETE', 'PARTIAL', 'FAILED'], diagnostics, 'findingCapture.detailCoverage.status'), requested: detail.requested ?? null, hydrated: detail.hydrated ?? null, failed: detail.failed ?? null }, relatedAssessmentId: capture.relatedAssessmentId || null, correlationBasis: capture.correlationBasis || null };
  }
  function recommendationPresence(item) {
    if (item.representation === 'SUMMARY') return 'NOT_FETCHED';
    if (!own(item, 'recommendations') || item.recommendations === undefined) return 'OMITTED';
    if (item.recommendations === null) return 'NULL';
    return Array.isArray(item.recommendations) ? item.recommendations.length ? 'PRESENT' : 'EMPTY' : 'UNKNOWN';
  }
  function recommendationFieldDto(fields) {
    if (!fields) return null;
    return Object.fromEntries(['infrastructureAndCodeRecommendations', 'observabilityRecommendations', 'testingRecommendations'].map(key => [key, ['PRESENT', 'EMPTY', 'OMITTED', 'NULL', 'NOT_FETCHED'].includes(fields[key]) ? fields[key] : 'UNKNOWN']));
  }
  function findingObservationDto(observation, diagnostics = []) {
    if (!observation) return null;
    return { observationId: observation.observationId, captureId: observation.captureId || null, serviceArn: observation.serviceArn, findingId: observation.findingId, representation: normalized(observation.representation, ['SUMMARY', 'DETAIL'], diagnostics, 'findingObservation.representation'), observedAt: epoch(observation.observedAt), name: observation.name ?? null, severity: normalized(observation.severity, findingSeverities, diagnostics, 'findingObservation.severity'), status: normalized(observation.status, findingStates, diagnostics, 'findingObservation.status'), recommendationPresence: observation.recommendationPresence || 'UNKNOWN', recommendationFields: recommendationFieldDto(observation.recommendationFields), recommendationIds: Array.isArray(observation.recommendationIds) ? clone(observation.recommendationIds) : null };
  }
  function findingCoverageDto(s, svc) {
    const coverage = model.findingCoverage(s, svc);
    return { ...coverage, observedAt: epoch(coverage.observedAt), latestCapture: findingCaptureDto(coverage.latestCapture) };
  }
  function selectedObservationsDto(s, svc, diagnostics = []) {
    const h = svc.health, p = svc.posture;
    return {
      health: h ? { observationId: h.observationId || null, serviceArn: svc.arn, state: normalized(h.state, ['HEALTHY', 'DEGRADED', 'UNAVAILABLE', 'UNKNOWN'], diagnostics, 'selectedObservations.health.state'), rawState: h.state ?? null, observedAt: epoch(h.observedAt), expiresAt: epoch(h.expiresAt), source: h.source ?? null, reason: h.reason ?? null, ruleVersion: h.ruleVersion ?? null, provenance: h.provenance || 'LOCAL_MONITORING_AGGREGATE', latencyMs: h.latencyMs ?? null, errorRate: h.errorRate ?? null, windowMinutes: h.windowMinutes ?? null } : null,
      posture: p ? { observationId: p.observationId || null, serviceArn: svc.arn, state: normalized(p.state, ['ACHIEVABLE', 'NOT_ACHIEVABLE', 'UNKNOWN'], diagnostics, 'selectedObservations.posture.state'), rawState: p.state ?? null, achievability: achievability(p.components, diagnostics), observedAt: epoch(p.observedAt), source: p.source ?? null, ruleVersion: p.ruleVersion ?? null, provenance: p.provenance || 'LOCAL_CAPTURE', assessmentId: p.assessmentId || null, assessmentLinkage: p.assessmentLinkage || 'UNRESOLVED_CORRELATION', assessmentCorrelationBasis: p.assessmentCorrelationBasis || null, policyContextCaptureId: p.policyContextCaptureId || null, evaluatedProviderRevision: p.evaluatedProviderRevision ?? null } : null
    };
  }
  function systemDto(s, item) { return { systemArn: item.arn, systemId: item.systemId || item.id, name: item.providerName || item.id, description: item.description || '', createdAt: epoch(item.createdAt), updatedAt: epoch(item.updatedAt), localUpdatedAt: epoch(item.localUpdatedAt), sharingEnabled: item.sharingEnabled ?? null, kmsKeyId: item.kmsKeyId || null, tags: item.tags ?? null, displayName: item.displayName || item.name, version: item.version, normalizationDiagnostics: [], provenance: 'MOCK_NATIVE_FIELDS_WITH_LOCAL_METADATA' }; }
  function journeyDto(s, item) {
    const parent = s.systems.find(parent => parent.id === item.systemId);
    return { systemArn: parent.arn, userJourneyId: item.userJourneyId, name: item.name, description: item.description || '', policyArn: item.policyArn || null, serviceArns: active(s.services).filter(service => service.associations.some(a => a.systemId === item.systemId && a.journeyIds.includes(item.id))).map(service => service.arn), createdAt: epoch(item.createdAt), updatedAt: epoch(item.updatedAt), localUpdatedAt: epoch(item.localUpdatedAt), version: item.version, normalizationDiagnostics: [], provenance: 'MOCK_NATIVE_JOURNEY_WITH_LOCAL_MEMBERSHIP_PROJECTION' };
  }
  function observedShape(value, schema, diagnostics, path) {
    if (value == null) return null;
    try { validate(schema, value); return clone(value); }
    catch (error) {
      if (!(error instanceof RpcError)) throw error;
      diagnostics.push({ path, rawValue: JSON.stringify(value), normalizedValue: null, reason: 'INVALID_VALUE' });
      return null;
    }
  }
  function policyDto(s, item) {
    const normalizationDiagnostics = [], components = {};
    for (const key of ['availabilitySlo', 'multiAz', 'multiRegion', 'dataRecovery']) {
      if (!own(item.components || {}, key)) continue;
      const component = item.components[key];
      if (component == null) { components[key] = null; continue; }
      if (key === 'multiAz' || key === 'multiRegion') components[key] = { rtoInMinutes: component.rtoInMinutes ?? null, rpoInMinutes: component.rpoInMinutes ?? null, disasterRecoveryApproach: component.disasterRecoveryApproach == null ? null : normalized(component.disasterRecoveryApproach, ['ACTIVE_ACTIVE', 'HOT_STANDBY', 'WARM_STANDBY', 'PILOT_LIGHT', 'BACKUP_AND_RESTORE'], normalizationDiagnostics, key + '.disasterRecoveryApproach'), rawDisasterRecoveryApproach: component.disasterRecoveryApproach ?? null };
      else if (key === 'dataRecovery') components[key] = { timeBetweenBackupsInMinutes: component.timeBetweenBackupsInMinutes ?? null };
      else components[key] = observedShape(component, contract.shapes.AvailabilitySlo, normalizationDiagnostics, key);
    }
    return { policyArn: item.arn, name: item.providerName || item.id, displayName: item.displayName || item.name, description: item.description || '', ...components, createdAt: epoch(item.createdAt), updatedAt: epoch(item.updatedAt), localUpdatedAt: epoch(item.localUpdatedAt), sharingEnabled: item.sharingEnabled ?? null, kmsKeyId: item.kmsKeyId || null, tags: item.tags ?? null, version: item.version, normalizationDiagnostics, provenance: 'MOCK_NATIVE_POLICY_WITH_LOCAL_METADATA' };
  }
  function sourceDto(s, item, svc) {
    const configuration = item.resourceConfiguration || (item.sourceArn ? { cfnStackArn: item.sourceArn } : null);
    const normalizationDiagnostics = [];
    return { serviceArn: svc.arn, inputSourceId: item.inputSourceId, type: normalized(item.type, ['CFN_STACK', 'TAGS', 'TERRAFORM', 'EKS', 'DESIGN_FILE', 'MONITORING'], normalizationDiagnostics, 'inputSource.type'), rawType: item.type ?? null, createdAt: epoch(item.createdAt), localCreatedAt: epoch(item.localCreatedAt), localUpdatedAt: epoch(item.localUpdatedAt), resourceConfiguration: observedShape(configuration, contract.shapes.ResourceConfiguration, normalizationDiagnostics, 'inputSource.resourceConfiguration'), displayName: item.name || item.inputSourceId, status: item.status || 'UNKNOWN', version: item.version, observedAt: epoch(item.observedAt), normalizationDiagnostics, provenance: configuration ? 'MOCK_INPUT_SOURCE_CONFIGURATION' : 'MOCK_SOURCE_CONFIGURATION_NOT_CAPTURED' };
  }
  function serviceDto(s, item) {
    const normalizationDiagnostics = [];
    return { serviceArn: item.arn, name: item.providerName || item.id, displayName: item.displayName || item.name, description: item.description || '', createdAt: epoch(item.createdAt), updatedAt: epoch(item.updatedAt), localUpdatedAt: epoch(item.localUpdatedAt), observedAt: epoch(item.observedAt), associatedSystems: item.associations.map(a => ({ systemArn: s.systems.find(parent => parent.id === a.systemId).arn, userJourneyIds: a.journeyIds.map(journeyId => s.journeys.find(j => j.id === journeyId)?.userJourneyId).filter(Boolean) })), policyArn: item.policyArn || null, regions: item.regions ? clone(item.regions) : null, permissionModel: permissionDto(item.permissionModel), dependencyDiscovery: discoveryDto(item.dependencyDiscovery, normalizationDiagnostics), resourceDiscovery: resourceDiscoveryDto(item.resourceDiscovery, normalizationDiagnostics), achievability: achievability(item.posture?.components, normalizationDiagnostics), assessmentStatus: normalized(item.assessmentStatus, assessmentStates, normalizationDiagnostics, 'assessmentStatus'), rawAssessmentStatus: item.assessmentStatus ?? null, inputSourceIds: active(item.inputSources || []).map(source => source.inputSourceId), resourceCount: item.resourceCount ?? null, reportConfiguration: observedShape(item.reportConfiguration, contract.shapes.ReportConfiguration, normalizationDiagnostics, 'reportConfiguration'), devOpsAgentConfiguration: observedShape(item.devOpsAgentConfiguration, contract.shapes.DevOpsAgentConfiguration, normalizationDiagnostics, 'devOpsAgentConfiguration'), tags: item.tags ?? null, kmsKeyId: item.kmsKeyId || null, version: item.version, projectionVersion: item.projectionVersion || 1, refreshRequired: !!item.refreshRequired, policyContextRefreshRequired: !!item.policyContextRefreshRequired, reassessmentRequired: !!item.reassessmentRequired, rerunAssessment: typeof item.rerunAssessment === 'boolean' ? item.rerunAssessment : null, effectivePolicyEvidence: policyEvidenceDto(s, item, normalizationDiagnostics, false), normalizationDiagnostics, provenance: 'MOCK_NATIVE_SERVICE_WITH_LOCAL_METADATA' };
  }
  function assessmentDto(s, item) { const normalizationDiagnostics = []; return { serviceArn: item.serviceArn, assessmentId: item.assessmentId, status: normalized(item.status, assessmentStates, normalizationDiagnostics, 'assessment.status'), rawStatus: item.status ?? null, startedAt: epoch(item.startedAt), endedAt: epoch(item.endedAt), observedAt: epoch(item.observedAt), failureModeFindingsCount: item.totalFindings ?? null, achievability: achievability(item.achievability, normalizationDiagnostics), assessmentCost: item.assessmentCost || item.cost || null, assessmentStep: item.assessmentStep || item.stepLabel || null, errorCode: item.errorCode ?? null, errorMessage: item.errorMessage ?? item.error ?? null, version: item.version || 1, normalizationDiagnostics, provenance: 'LOCAL_RETAINED_MOCK_ASSESSMENT_OBSERVATION' }; }
  function findingDto(s, item) {
    const normalizationDiagnostics = [], presence = recommendationPresence(item);
    const capture = s.findingCaptures.find(c => c.captureId === item.captureId && c.serviceArn === item.serviceArn);
    const observation = s.findingObservations.find(o => o.observationId === item.observationId && o.serviceArn === item.serviceArn && o.findingId === item.findingId);
    return { serviceArn: item.serviceArn, findingId: item.findingId, name: item.name, description: item.description || '', reasoning: item.reasoning || '', severity: normalized(item.severity, findingSeverities, normalizationDiagnostics, 'finding.severity'), rawSeverity: item.severity ?? null, status: normalized(item.status, findingStates, normalizationDiagnostics, 'finding.status'), rawStatus: item.status ?? null, failureCategory: item.failureCategory, policyComponent: item.policyComponent, serviceFunctions: item.serviceFunctions || [], comment: item.comment || '', updatedAt: epoch(item.updatedAt), localUpdatedAt: epoch(item.localUpdatedAt), detailObservedAt: epoch(item.detailObservedAt), observationId: item.observationId || null, captureId: item.captureId || null, representation: normalized(item.representation, ['DETAIL', 'SUMMARY'], normalizationDiagnostics, 'finding.representation'), recommendationIds: ['PRESENT', 'EMPTY'].includes(presence) ? item.recommendations.map(rec => rec.id) : null, recommendationPresence: presence, recommendationFields: recommendationFieldDto(item.recommendationFields), findingCapture: findingCaptureDto(capture, normalizationDiagnostics), findingObservation: findingObservationDto(observation, normalizationDiagnostics), verification: item.verification || 'UNVERIFIED', version: item.version, normalizationDiagnostics, provenance: 'MOCK_PROVIDER_FINDING_WITH_LOCAL_CAPTURE_AND_DISPOSITION' };
  }
  function recommendationOwner(s, rec) { return s.findingObservations.find(observation => observation.observationId === rec.observationId && observation.representation === 'DETAIL'); }
  function recommendation(s, p) {
    service(s, p.serviceArn, true);
    const rec = s.recommendations.find(item => item.id === p.recommendationId);
    const owner = rec && recommendationOwner(s, rec);
    if (!rec || !owner || owner.serviceArn !== p.serviceArn || owner.findingId !== p.findingId) fail('ResourceNotFoundException', 'Recommendation was not found under the specified finding and service.');
    return rec;
  }
  function recommendationDto(s, item) {
    const owner = recommendationOwner(s, item), enrichment = s.rpc.recommendationEnrichments[item.id];
    const estimate = enrichment.estimate ? { ...clone(enrichment.estimate), estimatedAt: epoch(enrichment.estimate.estimatedAt) } : null;
    return { recommendationId: item.id, serviceArn: owner.serviceArn, findingId: owner.findingId, findingObservationId: item.observationId, category: item.category, sourceArrayOrdinal: item.sourceArrayOrdinal, suggestedChanges: clone(item.suggestedChanges || []), capturedAt: epoch(item.capturedAt), enrichment: { title: enrichment.title, description: enrichment.description, estimate, version: enrichment.version, updatedAt: epoch(enrichment.localUpdatedAt || enrichment.updatedAt), provenance: enrichment.provenance }, provenance: 'IMMUTABLE_MOCK_FINDING_RECOMMENDATION_OBSERVATION' };
  }
  function dependencyDto(s, item) { const normalizationDiagnostics = []; return { serviceArn: item.serviceArn, dependencyId: item.dependencyId, dependencyName: item.dependencyName || item.name, dnsName: item.dnsName || null, location: item.location, criticality: normalized(item.criticality, ['HARD', 'SOFT', 'UNKNOWN'], normalizationDiagnostics, 'dependency.criticality'), rawCriticality: item.criticality ?? null, comment: item.comment || '', provider: item.provider || '', sourceRegions: item.sourceRegions || [], lastDetectedTime: epoch(item.lastDetectedTime), updatedAt: epoch(item.updatedAt), localUpdatedAt: epoch(item.localUpdatedAt), governance: { ...clone(item.governance), observedAt: epoch(item.governance.observedAt), version: item.governance.version || 1 }, resolvedServiceArn: item.resolution ? s.services.find(service => service.id === item.resolution.serviceId)?.arn || null : null, version: item.version, normalizationDiagnostics, provenance: 'MOCK_DEPENDENCY_WITH_LOCAL_LOCATION_LABEL_AND_GOVERNANCE' }; }
  function topologyDto(s, item) { return { serviceArn: item.serviceArn, topologyId: item.topologyId, capturedAt: epoch(item.capturedAt), captureStartedAt: epoch(item.captureStartedAt), captureEndedAt: epoch(item.captureEndedAt), sourceObservedAt: epoch(item.sourceObservedAt || item.captureEndedAt), collectionStatus: item.collectionStatus, queryScope: clone(item.queryScope), resourceCount: item.resourceCount, totalServiceResourceCount: item.totalServiceResourceCount ?? null, edgeCount: item.edgeCount, unresolvedCount: item.unresolvedCount, nodes: item.nodes.map(n => ({ id: n.id, resourceIdentifier: n.resourceIdentifier, name: n.name, type: n.type, region: n.region, accountId: n.accountId, status: n.status })), edges: item.edges.map(e => ({ id: e.id, source: e.source, target: e.target, type: e.type, label: e.label || '', provenance: e.provenance })), atomicSnapshot: false, provenance: item.provenance, coverageMessage: item.coverageMessage, captureMode: item.captureMode || 'FIXTURE_CAPTURE', version: item.version || 1 }; }
  function eventDto(s, item) {
    const serviceArn = item.serviceArn || s.services.find(service => service.id === item.serviceId)?.arn || null;
    let subjects = item.subjects ? clone(item.subjects) : null;
    if (!subjects) {
      const rawType = item.entityType || 'Service', allowed = contract.shapes.EventSubject.properties.entityType.enum;
      const entityType = allowed.includes(rawType) ? rawType : 'UNKNOWN';
      let entityId = item.entityId || item.serviceId || 'unresolved', context = serviceArn ? { serviceArn } : {};
      if (entityType === 'Service' && serviceArn) entityId = serviceArn;
      if (entityType === 'Finding') entityId = s.findings.find(f => f.serviceArn === serviceArn && (f.id === entityId || f.findingId === entityId))?.findingId || entityId;
      if (entityType === 'Dependency') entityId = s.dependencies.find(d => d.serviceArn === serviceArn && (d.id === entityId || d.dependencyId === entityId))?.dependencyId || entityId;
      if (entityType === 'Assessment') entityId = s.assessments.find(a => a.serviceArn === serviceArn && (a.id === entityId || a.assessmentId === entityId))?.assessmentId || entityId;
      subjects = [subject(entityType, entityId, context)];
      if (serviceArn && entityType !== 'Service') subjects.push(subject('Service', serviceArn, { serviceArn }, 'RELATED'));
    }
    const primary = subjects.find(entry => entry.relationship === 'SUBJECT') || subjects[0];
    return { eventId: item.id, sourceEventId: item.sourceEventId, eventKey: item.eventKey, channel: item.channel, streamOwner: item.streamOwner, source: item.source || 'resilience.workspace.mock', type: item.type, title: item.title || item.type, message: item.message || '', severity: item.severity || 'INFO', serviceArn, entityType: primary?.entityType || item.entityType || 'UNKNOWN', entityId: primary?.entityId || item.entityId || 'unresolved', subjects, rawEvent: item.rawEvent ? clone(item.rawEvent) : null, correlationIds: clone(item.correlationIds || []), occurredAt: epoch(item.occurredAt), receivedAt: epoch(item.receivedAt), linkage: item.linkage || 'ASSERTED', refreshStatus: item.refreshStatus || 'REFRESH_REQUIRED', sequence: item.sequence, mock: true, producerPrincipalId: item.producerPrincipalId || null, trustedSource: !!item.trustedSource };
  }
  function statusDto(s, item) {
    const h = model.serviceHealth(s, item), p = model.servicePosture(s, item), normalizationDiagnostics = [];
    const health = { state: normalized(h.state, ['HEALTHY', 'DEGRADED', 'UNAVAILABLE', 'UNKNOWN'], normalizationDiagnostics, 'health.state'), rawState: h.rawState ?? null, observedAt: epoch(h.observedAt), expiresAt: epoch(h.expiresAt), stale: h.stale, source: h.source || '', reason: h.reason || '', observationId: h.observationId || null, provenance: h.provenance || 'LOCAL_MONITORING_AGGREGATE', ruleVersion: h.ruleVersion || '', ageMinutes: h.ageMinutes == null ? null : Math.max(0, h.ageMinutes), latencyMs: h.latencyMs ?? null, errorRate: h.errorRate ?? null, windowMinutes: h.windowMinutes ?? null };
    const posture = { state: normalized(p.state, ['ACHIEVABLE', 'NOT_ACHIEVABLE', 'UNKNOWN'], normalizationDiagnostics, 'posture.state'), rawState: item.posture?.state ?? null, achievability: achievability(p.components, normalizationDiagnostics), observedAt: epoch(p.observedAt), stale: p.stale, assessmentId: p.assessmentId || null, observationId: p.observationId || null, ruleVersion: p.ruleVersion || 'unknown', provenance: p.provenance || 'NO_ASSESSED_EVIDENCE', evaluatedProviderRevision: p.evaluatedProviderRevision || null, policyContextCaptureId: p.policyContextCaptureId || null };
    const findingCoverage = findingCoverageDto(s, item), coverage = model.assessmentCoverage(s, item);
    const assessmentCoverage = { ...coverage, observedAt: epoch(coverage.observedAt) };
    const dependencyDiscovery = discoveryDto(item.dependencyDiscovery, normalizationDiagnostics), resourceDiscovery = resourceDiscoveryDto(item.resourceDiscovery, normalizationDiagnostics);
    const effectivePolicyEvidence = policyEvidenceDto(s, item, normalizationDiagnostics), selectedObservations = selectedObservationsDto(s, item, normalizationDiagnostics);
    const assessmentStatus = normalized(item.assessmentStatus, assessmentStates, normalizationDiagnostics, 'assessmentStatus');
    const attentionReasons = model.attentionReasons(s, item).map(reason => ({ ...reason, observedAt: epoch(reason.observedAt) }));
    return { serviceArn: item.arn, health, posture, assessmentStatus, rawAssessmentStatus: item.assessmentStatus ?? null, dependencyDiscovery, resourceDiscovery, needsAttention: attentionReasons.length > 0, attentionReasons, findingCoverage, openFindingsCount: findingCoverage.exactOpenCount, assessmentCoverage, effectivePolicyEvidence, selectedObservations, computedAt: epoch(s.now), version: item.version, projectionVersion: item.projectionVersion || 1, refreshRequired: !!item.refreshRequired, policyContextRefreshRequired: !!item.policyContextRefreshRequired, reassessmentRequired: !!item.reassessmentRequired, rerunAssessment: typeof item.rerunAssessment === 'boolean' ? item.rerunAssessment : null, normalizationDiagnostics, provenance: 'LOCAL_OPERATOR_PROJECTION' };
  }

  function paginate(name, p, principal, field, rows) {
    const filters = Object.fromEntries(Object.entries(p).filter(([key]) => key !== 'nextToken' && key !== 'maxResults'));
    const scopeHash = digest({ tenantId, principalId: principal.id, roles: [...principal.roles].sort(), operation: name, filters });
    let snapshot, offset = 0;
    if (p.nextToken) {
      try {
        const [payload, signature, extra] = p.nextToken.split('.');
        if (extra || !payload || !signature) invalid('The pagination token is invalid.');
        const expected = crypto.createHmac('sha256', secret).update(payload).digest('base64url');
        const left = Buffer.from(signature), right = Buffer.from(expected);
        if (left.length !== right.length || !crypto.timingSafeEqual(left, right)) invalid('The pagination token is invalid.');
        const parsed = JSON.parse(Buffer.from(payload, 'base64url').toString('utf8'));
        snapshot = snapshots.get(parsed.snapshotId);
        if (!snapshot || snapshot.expiresAt <= clock() || parsed.scopeHash !== scopeHash || snapshot.scopeHash !== scopeHash || !Number.isInteger(parsed.offset) || parsed.offset < 0 || parsed.offset >= snapshot.rows.length) invalid('The pagination token is expired or does not match this principal, operation, and filter scope.');
        offset = parsed.offset;
      } catch (error) { if (error instanceof RpcError) throw error; invalid('The pagination token is invalid.'); }
    } else {
      for (const [key, cached] of snapshots) if (cached.expiresAt <= clock()) snapshots.delete(key);
      const createdAt = clock();
      snapshot = { snapshotId: 'snapshot-' + digest({ scopeHash, createdAt, ordinal: ++snapshotSequence }).slice(0, 24), scopeHash, createdAt, expiresAt: createdAt + cursorTtlMs, rows: clone(rows) };
      snapshots.set(snapshot.snapshotId, snapshot);
    }
    const size = p.maxResults || contract.limits.defaultMaxResults;
    const end = Math.min(offset + size, snapshot.rows.length);
    let nextToken;
    if (end < snapshot.rows.length) {
      const payload = Buffer.from(JSON.stringify({ snapshotId: snapshot.snapshotId, offset: end, scopeHash })).toString('base64url');
      nextToken = payload + '.' + crypto.createHmac('sha256', secret).update(payload).digest('base64url');
    }
    return { [field]: clone(snapshot.rows.slice(offset, end)), ...(nextToken ? { nextToken } : {}), snapshot: { snapshotId: snapshot.snapshotId, createdAt: snapshot.createdAt / 1000, expiresAt: snapshot.expiresAt / 1000, totalResults: snapshot.rows.length } };
  }
  const handlers = {};
  handlers.CreateSystem = (s, p) => {
    assertUniqueName(s, 'systems', p.name);
    const arn = nextArn(s, 'system'), systemId = arn.split('/').pop();
    const item = { id: systemId, systemId, systemArn: arn, arn, providerName: p.name, name: p.name, description: p.description || '', createdAt: s.now, updatedAt: s.now, sharingEnabled: p.sharingEnabled || false, kmsKeyId: p.kmsKeyId || null, tags: clone(p.tags || {}), version: 1 };
    s.systems.push(item); return { system: systemDto(s, item) };
  };
  handlers.GetSystem = (s, p) => ({ system: systemDto(s, system(s, p.systemArn)) });
  handlers.ListSystems = (s, p, principal) => paginate('ListSystems', p, principal, 'systems', active(s.systems).map(item => systemDto(s, item)));
  handlers.UpdateSystem = (s, p) => { const item = system(s, p.systemArn); assertVersion(item, p.expectedVersion); assertChange(p, ['description', 'sharingEnabled']); for (const key of ['description', 'sharingEnabled']) if (own(p, key)) item[key] = p[key]; bump(s, item); return { system: systemDto(s, item) }; };
  handlers.DeleteSystem = (s, p) => { const item = system(s, p.systemArn); assertVersion(item, p.expectedVersion); if (active(s.journeys).some(j => j.systemId === item.id) || active(s.services).some(service => service.associations.some(a => a.systemId === item.id))) conflict('Detach services and delete journeys before deleting this system.'); return remove(s, 'systems', item, item.arn); };
  handlers.CreateUserJourney = (s, p) => {
    const parent = system(s, p.systemArn), assignedPolicy = p.policyArn ? policy(s, p.policyArn) : null;
    if (active(s.journeys).some(j => j.systemId === parent.id && j.name === p.name)) conflict('A user journey with this name already exists in the system.');
    const userJourneyId = nextUuid(s), item = { id: userJourneyId, userJourneyId, systemId: parent.id, name: p.name, description: p.description || '', policyId: assignedPolicy?.id || null, policyArn: assignedPolicy?.arn || null, createdAt: s.now, updatedAt: s.now, version: 1 };
    s.journeys.push(item); return { userJourney: journeyDto(s, item) };
  };
  handlers.GetUserJourney = (s, p) => ({ userJourney: journeyDto(s, journey(s, p.systemArn, p.userJourneyId)) });
  handlers.ListUserJourneys = (s, p, principal) => { const parent = system(s, p.systemArn); return paginate('ListUserJourneys', p, principal, 'userJourneys', active(s.journeys).filter(j => j.systemId === parent.id && (!p.userJourneyId || j.userJourneyId === p.userJourneyId)).map(j => journeyDto(s, j))); };
  handlers.UpdateUserJourney = (s, p) => {
    const item = journey(s, p.systemArn, p.userJourneyId); assertVersion(item, p.expectedVersion); assertChange(p, ['name', 'description', 'policyArn']);
    if (own(p, 'name') && active(s.journeys).some(j => j !== item && j.systemId === item.systemId && j.name === p.name)) conflict('A user journey with this name already exists in the system.');
    for (const key of ['name', 'description']) if (own(p, key)) item[key] = p[key];
    if (own(p, 'policyArn')) { const assigned = p.policyArn ? policy(s, p.policyArn) : null; const changedPolicy = item.policyArn !== (assigned?.arn || null); item.policyId = assigned?.id || null; item.policyArn = assigned?.arn || null; if (changedPolicy) for (const svc of active(s.services)) if (svc.associations.some(a => a.journeyIds.includes(item.id))) { refresh(s, svc, { policyContext: true, reassessment: true }); bumpProjection(s, svc); } }
    bump(s, item); return { userJourney: journeyDto(s, item) };
  };
  handlers.DeleteUserJourney = (s, p) => { const item = journey(s, p.systemArn, p.userJourneyId); assertVersion(item, p.expectedVersion); if (active(s.services).some(svc => svc.associations.some(a => a.journeyIds.includes(item.id)))) conflict('Detach the user journey from services before deleting it.'); return remove(s, 'journeys', item, item.userJourneyId); };
  handlers.CreateService = (s, p) => {
    assertUniqueName(s, 'services', p.name);
    const associations = associationRecords(s, p.associatedSystems), assigned = p.policyArn ? policy(s, p.policyArn) : null;
    if (new Set(p.regions).size !== p.regions.length) invalid('regions contains duplicates.');
    const arn = nextArn(s, 'service'), id = arn.split('/').pop();
    const item = { id, arn, serviceArn: arn, providerName: p.name, name: p.name, description: p.description || '', associations, policyId: assigned?.id || null, policyArn: assigned?.arn || null, regions: clone(p.regions), permissionModel: clone(p.permissionModel), inputSources: [], createdAt: s.now, updatedAt: s.now, observedAt: s.now, dependencyDiscovery: { status: p.dependencyDiscovery === 'ENABLED' ? 'INITIALIZING' : 'DISABLED', requestedStatus: p.dependencyDiscovery || 'DISABLED', eligibleResourceCount: null, message: 'No discovery evidence captured yet.', updatedAt: s.now }, resourceDiscovery: { status: 'NOT_STARTED', lastRunAt: null }, assessmentStatus: 'NOT_STARTED', resourceCount: null, effectiveTargets: [], applicablePolicies: [], tags: clone(p.tags || {}), kmsKeyId: p.kmsKeyId || null, reportConfiguration: clone(p.reportConfiguration || null), devOpsAgentConfiguration: clone(p.devOpsAgentConfiguration || null), version: 1, refreshRequired: true };
    s.services.push(item); return { service: serviceDto(s, item) };
  };
  handlers.GetService = (s, p) => ({ service: serviceDto(s, service(s, p.serviceArn)) });
  handlers.ListServices = (s, p, principal) => paginate('ListServices', p, principal, 'services', scopeServices(s, p).map(item => serviceDto(s, item)));
  handlers.UpdateService = (s, p) => {
    const item = service(s, p.serviceArn); assertVersion(item, p.expectedVersion); const keys = ['description', 'associatedSystems', 'policyArn', 'regions', 'permissionModel', 'dependencyDiscovery', 'reportConfiguration', 'devOpsAgentConfiguration']; assertChange(p, keys);
    let contextChanged = false;
    const materialChanged = ['regions', 'permissionModel'].some(key => own(p, key) && canonical(item[key]) !== canonical(p[key])) || (own(p, 'dependencyDiscovery') && (item.dependencyDiscovery?.requestedStatus || item.dependencyDiscovery?.status) !== p.dependencyDiscovery);
    if (own(p, 'associatedSystems')) { const associations = associationRecords(s, p.associatedSystems); contextChanged ||= canonical(item.associations) !== canonical(associations); item.associations = associations; }
    if (own(p, 'policyArn')) { const assigned = p.policyArn ? policy(s, p.policyArn) : null; contextChanged ||= item.policyArn !== (assigned?.arn || null); item.policyId = assigned?.id || null; item.policyArn = assigned?.arn || null; }
    if (p.regions && new Set(p.regions).size !== p.regions.length) invalid('regions contains duplicates.');
    for (const key of ['description', 'regions', 'permissionModel', 'reportConfiguration', 'devOpsAgentConfiguration']) if (own(p, key)) item[key] = clone(p[key]);
    if (own(p, 'dependencyDiscovery') && (item.dependencyDiscovery?.requestedStatus || item.dependencyDiscovery?.status) !== p.dependencyDiscovery) item.dependencyDiscovery = { ...item.dependencyDiscovery, status: p.dependencyDiscovery === 'ENABLED' ? 'INITIALIZING' : 'DISABLED', requestedStatus: p.dependencyDiscovery, eligibleResourceCount: p.dependencyDiscovery === 'ENABLED' ? null : item.dependencyDiscovery?.eligibleResourceCount ?? null, message: p.dependencyDiscovery === 'ENABLED' ? 'Initialization is pending a future discovery refresh.' : 'Discovery disabled; historical dependencies are retained.', updatedAt: s.now };
    refresh(s, item, { policyContext: contextChanged, reassessment: contextChanged || materialChanged }); bump(s, item); bumpProjection(s, item); return { service: serviceDto(s, item) };
  };
  handlers.DeleteService = (s, p) => { const item = service(s, p.serviceArn); assertVersion(item, p.expectedVersion); if (s.assessments.some(a => a.serviceArn === item.arn && ['PENDING', 'IN_PROGRESS'].includes(a.status))) conflict('A service with an active assessment cannot be deleted.'); return remove(s, 'services', item, item.arn); };
  handlers.CreatePolicy = (s, p) => {
    assertUniqueName(s, 'policies', p.name);
    const components = Object.fromEntries(['availabilitySlo', 'multiAz', 'multiRegion', 'dataRecovery'].filter(key => own(p, key)).map(key => [key, clone(p[key])]));
    const arn = nextArn(s, 'policy'), item = { id: arn.split('/').pop(), arn, policyArn: arn, providerName: p.name, name: p.name, description: p.description || '', components, createdAt: s.now, updatedAt: s.now, sharingEnabled: p.sharingEnabled || false, kmsKeyId: p.kmsKeyId || null, tags: clone(p.tags || {}), version: 1 };
    s.policies.push(item); return { policy: policyDto(s, item) };
  };
  handlers.GetPolicy = (s, p) => ({ policy: policyDto(s, policy(s, p.policyArn)) });
  handlers.ListPolicies = (s, p, principal) => paginate('ListPolicies', p, principal, 'policies', active(s.policies).map(item => policyDto(s, item)));
  handlers.UpdatePolicy = (s, p) => {
    const item = policy(s, p.policyArn); assertVersion(item, p.expectedVersion); assertChange(p, ['description', 'sharingEnabled', 'availabilitySlo', 'multiAz', 'multiRegion', 'dataRecovery']);
    const objectivesChanged = ['availabilitySlo', 'multiAz', 'multiRegion', 'dataRecovery'].some(key => own(p, key) && canonical(item.components[key]) !== canonical(p[key]));
    for (const key of ['description', 'sharingEnabled']) if (own(p, key)) item[key] = p[key];
    for (const key of ['availabilitySlo', 'multiAz', 'multiRegion', 'dataRecovery']) if (own(p, key)) item.components[key] = clone(p[key]);
    if (objectivesChanged) for (const svc of active(s.services)) if (svc.policyArn === item.arn || svc.associations.some(a => a.journeyIds.some(jid => active(s.journeys).some(j => j.id === jid && j.policyArn === item.arn)))) { refresh(s, svc, { policyContext: true, reassessment: true }); bumpProjection(s, svc); }
    bump(s, item); return { policy: policyDto(s, item) };
  };
  handlers.DeletePolicy = (s, p) => { const item = policy(s, p.policyArn); assertVersion(item, p.expectedVersion); if (active(s.services).some(svc => svc.policyArn === item.arn) || active(s.journeys).some(j => j.policyArn === item.arn)) conflict('Detach this policy from all services and journeys before deleting it.'); return remove(s, 'policies', item, item.arn); };
  handlers.CreateInputSource = (s, p) => {
    const svc = service(s, p.serviceArn);
    for (const expression of p.resourceConfiguration.eks?.labelSelector?.matchExpressions || []) {
      const hasValues = Array.isArray(expression.values) && expression.values.length > 0;
      if (['IN', 'NOT_IN'].includes(expression.operator) !== hasValues) invalid('EKS selector IN/NOT_IN requires nonempty values; EXISTS/DOES_NOT_EXIST requires omitted or empty values.');
    }
    if (active(svc.inputSources).some(source => canonical(source.resourceConfiguration || (source.sourceArn ? { cfnStackArn: source.sourceArn } : null)) === canonical(p.resourceConfiguration))) conflict('This resource configuration is already registered for the service.');
    const type = { resourceTags: 'TAGS', cfnStackArn: 'CFN_STACK', tfStateFileUrl: 'TERRAFORM', eks: 'EKS', designFileS3Url: 'DESIGN_FILE' }[Object.keys(p.resourceConfiguration)[0]];
    const inputSourceId = nextUuid(s), item = { id: inputSourceId, inputSourceId, type, resourceConfiguration: clone(p.resourceConfiguration), name: type + ' source', status: 'REGISTERED', localCreatedAt: s.now, observedAt: s.now, version: 1 };
    svc.inputSources.push(item); refresh(s, svc, { reassessment: true }); bump(s, svc); bumpProjection(s, svc); return { inputSource: sourceDto(s, item, svc) };
  };
  handlers.ListInputSources = (s, p, principal) => { const svc = service(s, p.serviceArn, true); return paginate('ListInputSources', p, principal, 'inputSources', active(svc.inputSources).filter(input => !p.type || input.type === p.type).map(input => sourceDto(s, input, svc))); };
  handlers.DeleteInputSource = (s, p) => { const svc = service(s, p.serviceArn), item = active(svc.inputSources).find(input => input.inputSourceId === p.inputSourceId); if (!item) fail('ResourceNotFoundException', 'Input source was not found in the requested service.'); assertVersion(item, p.expectedVersion); refresh(s, svc, { reassessment: true }); bump(s, svc); bumpProjection(s, svc); return remove(s, 'inputSources', item, item.inputSourceId); };
  handlers.StartFailureModeAssessment = (s, p) => {
    const svc = service(s, p.serviceArn);
    if (s.assessments.some(a => a.serviceArn === svc.arn && ['PENDING', 'IN_PROGRESS'].includes(a.status))) conflict('An assessment is already active for this service.');
    const assessmentId = nextUuid(s), item = { id: assessmentId, assessmentId, serviceId: svc.id, serviceArn: svc.arn, status: 'PENDING', startedAt: s.now, endedAt: null, observedAt: s.now, totalFindings: null, version: 1 };
    s.assessments.push(item); svc.assessmentStatus = 'PENDING'; bumpProjection(s, svc); return { assessment: assessmentDto(s, item) };
  };
  handlers.GetFailureModeAssessment = (s, p) => ({ assessment: assessmentDto(s, scoped(s, 'assessments', p, 'assessmentId')) });
  handlers.ListFailureModeAssessments = (s, p, principal) => { service(s, p.serviceArn, true); return paginate('ListFailureModeAssessments', p, principal, 'assessments', s.assessments.filter(item => item.serviceArn === p.serviceArn && (!p.status || item.status === p.status)).sort((a, b) => b.startedAt.localeCompare(a.startedAt)).map(item => assessmentDto(s, item))); };
  handlers.GetFailureModeFinding = (s, p) => ({ finding: findingDto(s, scoped(s, 'findings', p, 'findingId')) });
  handlers.ListFailureModeFindings = (s, p, principal) => { service(s, p.serviceArn, true); return paginate('ListFailureModeFindings', p, principal, 'findings', s.findings.filter(item => item.serviceArn === p.serviceArn && (!p.status || item.status === p.status) && (!p.severity || item.severity === p.severity)).map(item => findingDto(s, item))); };
  handlers.UpdateFailureModeFinding = (s, p) => {
    service(s, p.serviceArn); const item = scoped(s, 'findings', p, 'findingId', false); assertVersion(item, p.expectedVersion);
    const previousStatus = item.status; item.status = p.status; if (own(p, 'comment')) item.comment = p.comment;
    if (previousStatus !== p.status) item.verification = p.status === 'RESOLVED' ? 'UNVERIFIED' : p.status === 'IRRELEVANT' ? 'SUPPRESSED' : 'OPEN';
    (item.dispositionHistory ||= []).push({ previousStatus, status: p.status, comment: item.comment, observedAt: s.now, provenance: 'LOCAL_MOCK_COMMAND' });
    item.statusObservedAt = s.now; bump(s, item); const svc = service(s, p.serviceArn); if (previousStatus !== p.status && p.status === 'RESOLVED') svc.reassessmentRequired = true; bumpProjection(s, svc); return { finding: findingDto(s, item) };
  };
  handlers.GetRecommendation = (s, p) => ({ recommendation: recommendationDto(s, recommendation(s, p)) });
  handlers.ListRecommendations = (s, p, principal) => {
    scoped(s, 'findings', p, 'findingId');
    if (p.findingObservationId && !s.findingObservations.some(o => o.observationId === p.findingObservationId && o.serviceArn === p.serviceArn && o.findingId === p.findingId && o.representation === 'DETAIL')) fail('ResourceNotFoundException', 'Finding detail observation was not found in this scope.');
    const records = s.recommendations.filter(item => { const owner = recommendationOwner(s, item); return owner?.serviceArn === p.serviceArn && owner.findingId === p.findingId && (!p.findingObservationId || owner.observationId === p.findingObservationId); });
    return paginate('ListRecommendations', p, principal, 'recommendations', records.map(item => recommendationDto(s, item)));
  };
  handlers.UpdateRecommendationEnrichment = (s, p) => {
    service(s, p.serviceArn); const rec = recommendation(s, p), enrichment = s.rpc.recommendationEnrichments[rec.id]; assertVersion(enrichment, p.expectedVersion); assertChange(p, ['title', 'description', 'estimate']);
    for (const key of ['title', 'description', 'estimate']) if (own(p, key)) enrichment[key] = clone(p[key]);
    if (enrichment.estimate && typeof enrichment.estimate.estimatedAt === 'number') enrichment.estimate.estimatedAt = iso(enrichment.estimate.estimatedAt);
    bump(s, enrichment); return { recommendation: recommendationDto(s, rec) };
  };
  handlers.GetDependency = (s, p) => ({ dependency: dependencyDto(s, scoped(s, 'dependencies', p, 'dependencyId')) });
  handlers.ListDependencies = (s, p, principal) => { service(s, p.serviceArn, true); return paginate('ListDependencies', p, principal, 'dependencies', s.dependencies.filter(item => item.serviceArn === p.serviceArn && (!p.criticality || item.criticality === p.criticality)).map(item => dependencyDto(s, item))); };
  handlers.UpdateDependency = (s, p) => { const item = scoped(s, 'dependencies', p, 'dependencyId', false); assertVersion(item, p.expectedVersion); assertChange(p, ['criticality', 'comment']); const changedCriticality = own(p, 'criticality') && item.criticality !== p.criticality; for (const key of ['criticality', 'comment']) if (own(p, key)) item[key] = p[key]; bump(s, item); const svc = service(s, p.serviceArn); refresh(s, svc, { reassessment: changedCriticality }); bumpProjection(s, svc); return { dependency: dependencyDto(s, item) }; };
  handlers.UpdateDependencyGovernance = (s, p) => { const item = scoped(s, 'dependencies', p, 'dependencyId', false); assertVersion(item.governance, p.expectedVersion); item.governance.allowedStatus = p.allowedStatus; item.governance.source = p.source; item.governance.observedAt = s.now; item.governance.version += 1; return { dependency: dependencyDto(s, item) }; };
  handlers.CaptureTopologySnapshot = (s, p) => {
    const svc = service(s, p.serviceArn), previous = s.topologies.filter(t => t.serviceArn === svc.arn).sort((a, b) => b.capturedAt.localeCompare(a.capturedAt))[0];
    if (!previous) conflict('No stored topology evidence is available to capture for this service.');
    const topologyId = nextId(s, 'topology'), item = { ...clone(previous), id: topologyId, topologyId, sourceObservedAt: previous.sourceObservedAt || previous.captureEndedAt, captureStartedAt: s.now, captureEndedAt: s.now, capturedAt: s.now, captureMode: 'LOCAL_COPY', provenance: 'LOCAL_CAPTURE_OF_EXISTING_MOCK_EVIDENCE', version: 1 };
    for (const node of item.nodes) node.topologyId = topologyId; for (const edge of item.edges) edge.topologyId = topologyId;
    s.topologies.push(item); return { topologySnapshot: topologyDto(s, item) };
  };
  handlers.GetTopologySnapshot = (s, p) => ({ topologySnapshot: topologyDto(s, scoped(s, 'topologies', p, 'topologyId')) });
  handlers.ListTopologySnapshots = (s, p, principal) => { service(s, p.serviceArn, true); return paginate('ListTopologySnapshots', p, principal, 'topologySnapshots', s.topologies.filter(t => t.serviceArn === p.serviceArn).sort((a, b) => b.capturedAt.localeCompare(a.capturedAt)).map(t => topologyDto(s, t))); };
  handlers.GetServiceStatus = (s, p) => ({ serviceStatus: statusDto(s, service(s, p.serviceArn)) });
  handlers.GetWorkspaceSummary = (s, p) => {
    const services = scopeServices(s, p), statuses = services.map(svc => statusDto(s, svc)), count = predicate => statuses.filter(predicate).length;
    const currentAssessedCount = count(status => status.assessmentCoverage.current), lastKnownAssessedCount = count(status => status.assessmentCoverage.lastKnown);
    const incompleteFindingServiceCount = count(status => status.findingCoverage.status !== 'COMPLETE');
    const observedOpenFindingCount = statuses.reduce((total, status) => total + status.findingCoverage.observedOpenCount, 0);
    const attentionByDimension = {};
    for (const status of statuses) for (const dimension of new Set(status.attentionReasons.map(reason => reason.dimension))) attentionByDimension[dimension] = (attentionByDimension[dimension] || 0) + 1;
    return { summary: {
      serviceCount: services.length,
      healthyCount: count(status => status.health.state === 'HEALTHY'), degradedCount: count(status => status.health.state === 'DEGRADED'),
      unavailableCount: count(status => status.health.state === 'UNAVAILABLE'), unknownHealthCount: count(status => status.health.state === 'UNKNOWN'),
      achievableCount: count(status => status.posture.state === 'ACHIEVABLE'), atRiskCount: count(status => status.posture.state === 'NOT_ACHIEVABLE'),
      unknownPostureCount: count(status => status.posture.state === 'UNKNOWN'), stalePostureCount: count(status => status.posture.stale),
      attentionCount: count(status => status.needsAttention), attentionByDimension,
      openFindingCount: incompleteFindingServiceCount ? null : observedOpenFindingCount, observedOpenFindingCount, incompleteFindingServiceCount,
      currentAssessedCount, lastKnownAssessedCount,
      currentAssessmentCoverage: services.length ? Math.round(currentAssessedCount * 100 / services.length) : null,
      lastKnownAssessmentCoverage: services.length ? Math.round(lastKnownAssessedCount * 100 / services.length) : null,
      partialAssessmentCount: count(status => status.assessmentCoverage.status === 'PARTIAL'), inaccessibleAssessmentCount: count(status => status.assessmentCoverage.status === 'INACCESSIBLE'), unassessedCount: count(status => status.assessmentCoverage.status === 'UNASSESSED'),
      contributorServiceArns: services.map(svc => svc.arn), membershipContext: services.map(svc => ({ serviceArn: svc.arn, associatedSystems: serviceDto(s, svc).associatedSystems })),
      projectionVersion: s.rpc.projectionVersion, computedAt: epoch(s.now), aggregationRule: 'COUNT_DISTINCT_SERVICE_ARN_IN_SCOPE', evidenceRuleVersion: 'assessment-evidence-24h-v2',
      interpretation: 'Operator attention and evidence coverage; this is not certification of end-to-end user journey compliance.'
    } };
  };
  handlers.ListEvents = (s, p, principal) => {
    if (p.serviceArn) service(s, p.serviceArn, true);
    if (p.entityId && !p.entityType) invalid('entityType is required when entityId is specified.');
    const events = s.events.map(e => eventDto(s, e)).filter(e => (!p.serviceArn || e.serviceArn === p.serviceArn || e.subjects.some(subject => subject.serviceArn === p.serviceArn)) && (!p.entityType || e.subjects.some(subject => subject.entityType === p.entityType && (!p.entityId || subject.entityId === p.entityId))) && (!p.channel || e.channel === p.channel) && (p.afterSequence === undefined || e.sequence > p.afterSequence)).sort((a, b) => b.sequence - a.sequence);
    return paginate('ListEvents', p, principal, 'events', events);
  };
  function sourceDedupe(s, key, payload) {
    const existing = s.rpc.ingestedKeys[key];
    if (!existing) return null;
    if (existing.fingerprint !== digest(payload)) conflict('The source event key already exists with different content.');
    return existing;
  }
  handlers.PutHealthObservation = (s, p, principal) => {
    const svc = service(s, p.serviceArn), observation = p.observation;
    if (observation.expiresAt <= observation.observedAt) invalid('observation.expiresAt must be later than observedAt.');
    if (observation.observedAt > epoch(s.now) + 300) invalid('observation.observedAt is more than five minutes ahead of the local clock.');
    const eventKey = 'TELEMETRY|' + p.streamOwner + '|' + p.sourceEventId, sourcePayload = { serviceArn: p.serviceArn, observation };
    const duplicate = sourceDedupe(s, eventKey, sourcePayload);
    if (duplicate) return { observationId: duplicate.observationId, selectedAsCurrent: false, duplicate: true, serviceStatus: statusDto(s, svc) };
    if (s.events.some(event => event.eventKey === eventKey)) conflict('This source event key is already retained from the seed history.');
    const observationId = nextId(s, 'health'), record = { ...clone(observation), observedAt: iso(observation.observedAt), expiresAt: iso(observation.expiresAt), observationId, entityId: svc.id, serviceArn: svc.arn, dimension: 'HEALTH', provenance: 'LOCAL_MONITORING_AGGREGATE', producerPrincipalId: principal.id };
    const selectedAsCurrent = !svc.health || observation.observedAt > epoch(svc.health.observedAt);
    s.observations.push(record);
    if (selectedAsCurrent) { svc.health = clone(record); bumpProjection(s, svc); }
    model.recordEvent(s, { channel: 'TELEMETRY', streamOwner: p.streamOwner, sourceEventId: p.sourceEventId, source: observation.source, type: 'RUNTIME_HEALTH_OBSERVATION', title: 'Monitoring observation received', message: observation.reason, serviceId: svc.id, entityType: 'Service', entityId: svc.id, occurredAt: record.observedAt, receivedAt: s.now, producerPrincipalId: principal.id, trustedSource: false, refreshStatus: selectedAsCurrent ? 'REFRESHED' : 'OLDER_OR_EQUAL_EVIDENCE' });
    stampEvents(s, principal);
    s.rpc.ingestedKeys[eventKey] = { fingerprint: digest(sourcePayload), observationId };
    return { observationId, selectedAsCurrent, duplicate: false, serviceStatus: statusDto(s, svc) };
  };
  handlers.IngestEvent = (s, p, principal) => {
    const svc = service(s, p.serviceArn);
    if (p.occurredAt > epoch(s.now) + 300) invalid('occurredAt is more than five minutes ahead of the local clock.');
    for (const linked of p.subjects || []) {
      if (linked.serviceArn && linked.serviceArn !== p.serviceArn) invalid('An event subject must remain in the ingested service scope.');
      if (linked.entityType === 'Service' && linked.entityId !== p.serviceArn) invalid('A Service subject entityId must equal the ingested serviceArn.');
      if (['Assessment', 'Finding', 'InputSource', 'Dependency', 'Recommendation', 'TopologySnapshot'].includes(linked.entityType) && linked.serviceArn !== p.serviceArn) invalid('A service-scoped child event subject requires the matching serviceArn.');
    }
    const eventKey = p.channel + '|' + p.streamOwner + '|' + p.sourceEventId;
    const sourcePayload = { ...p }; delete sourcePayload.clientToken;
    const duplicate = sourceDedupe(s, eventKey, sourcePayload);
    if (duplicate) return { event: eventDto(s, s.events.find(e => e.id === duplicate.eventId)), duplicate: true, refreshRequired: !!svc.refreshRequired, refreshOperations: ['GetService', 'ListFailureModeAssessments', 'ListFailureModeFindings', 'ListDependencies'] };
    const existing = s.events.find(event => event.eventKey === eventKey);
    if (existing) conflict('This source event key is already retained from the seed history.');
    const subjects = p.subjects?.length ? clone(p.subjects) : [subject('Service', svc.arn, { serviceArn: svc.arn })];
    const primary = subjects.find(linked => linked.relationship === 'SUBJECT') || subjects[0];
    const recorded = model.recordEvent(s, { channel: p.channel, streamOwner: p.streamOwner, sourceEventId: p.sourceEventId, source: p.source, type: p.type, title: p.title, message: p.message, severity: p.severity || 'INFO', serviceId: svc.id, serviceArn: svc.arn, entityType: primary.entityType, entityId: primary.entityId, subjects, rawEvent: clone(p.rawEvent || null), correlationIds: clone(p.correlationIds || []), occurredAt: iso(p.occurredAt), receivedAt: s.now, producerPrincipalId: principal.id, trustedSource: false, linkage: 'ASSERTED', refreshStatus: 'REFRESH_REQUIRED' });
    stampEvents(s, principal); refresh(s, svc); bumpProjection(s, svc);
    s.rpc.ingestedKeys[eventKey] = { fingerprint: digest(sourcePayload), eventId: recorded.event.id };
    return { event: eventDto(s, recorded.event), duplicate: false, refreshRequired: true, refreshOperations: ['GetService', 'ListFailureModeAssessments', 'ListFailureModeFindings', 'ListDependencies'] };
  };

  function execute(name, input, context = {}) {
    const operation = operations.get(name);
    if (!operation) invalid('Unknown operation: ' + String(name));
    const principal = context.principal || defaultPrincipal;
    if (!principal || principal.tenantId !== tenantId || typeof principal.id !== 'string' || !Array.isArray(principal.roles) || !operation.roles.some(role => principal.roles.includes(role))) fail('AccessDeniedException', 'The trusted principal is not authorized for this operation and workspace.');
    assertJson(input);
    validate(operation.inputSchema, input);
    const key = operation.mutating ? tenantId + '|' + principal.id + '|' + name + '|' + input.clientToken : null;
    const fingerprint = operation.mutating ? digest(input) : null;
    if (key) {
      const replay = idempotency.get(key);
      if (replay && replay.expiresAt > clock()) { if (replay.fingerprint !== fingerprint) conflict('clientToken was already used with a different request.'); return clone(replay.response); }
      for (const [id, replay] of idempotency) if (replay.expiresAt <= clock()) idempotency.delete(id);
    }
    const working = operation.mutating ? clone(state) : state;
    freshState(working);
    const response = handlers[name](working, clone(input), principal);
    // Ingestion duplicate keys are successful no-ops and do not emit another audit event.
    const duplicate = operation.mutating && response.duplicate;
    if (operation.mutating && !duplicate) {
      working.rpc.projectionVersion += 1;
      if (!['PutHealthObservation', 'IngestEvent'].includes(name)) audit(working, name, input, response, principal);
    }
    try { validate(operation.outputSchema, response); } catch (error) { if (error instanceof RpcError) throw new Error(name + ' produced invalid output: ' + error.message); throw error; }
    if (operation.mutating) {
      state = working;
      idempotency.set(key, { fingerprint, response: clone(response), expiresAt: clock() + idempotencyTtlMs });
    }
    return clone(response);
  }
  function runSample(name) {
    const operation = operations.get(name);
    if (!operation) invalid('Unknown sample operation.');
    const setup = [];
    function resolve(value) {
      if (typeof value === 'string' && value.startsWith('$setup.')) return value.slice(7).split('.').reduce((current, key) => current[key], setup);
      if (Array.isArray(value)) return value.map(resolve);
      if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, resolve(item)]));
      return value;
    }
    for (const item of operation.sampleSetup || []) setup.push(execute(item.operation, resolve(item.input)));
    const request = resolve(operation.sampleInput), response = execute(name, request);
    return { setup, request, response };
  }
  return { execute, runSample, get state() { return state; }, contract, get principal() { return clone(defaultPrincipal); } };
}

module.exports = { createRuntime, RpcError, validate, canonical };
