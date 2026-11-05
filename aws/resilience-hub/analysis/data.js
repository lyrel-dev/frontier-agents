/*
 * Northstar Commerce: deliberately fictional, deterministic demo fixtures.
 * Native API fields are retained alongside clearly named local conveniences.
 * All account numbers, ARNs, people, dependencies and operational signals are mock.
 * No credentials, SDK calls or network requests are made by this module.
 */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  if (root) root.RH_DATA = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  var NOW = '2026-11-05T10:24:00.000Z';
  var ACCOUNT = '111122223333';
  var PLATFORM_ACCOUNT = '444455556666';
  var FULFILLMENT_ACCOUNT = '777788889999';
  function uuid(n) { return '71000000-0000-4000-8000-' + String(n).padStart(12, '0'); }
  function arn(type, id, account) { return 'arn:aws:resiliencehub:eu-west-1:' + (account || ACCOUNT) + ':' + type + '/' + uuid(id); }
  function before(minutes) { return new Date(Date.parse(NOW) - minutes * 60000).toISOString(); }
  function after(minutes) { return new Date(Date.parse(NOW) + minutes * 60000).toISOString(); }
  function copy(value) { return JSON.parse(JSON.stringify(value)); }

  // Independent assessment responses for the unchanged fictional architecture.
  // These outcomes do not read mutable finding dispositions or operator comments.
  // A simulator completion is new mock evidence, never proof that a triage edit
  // repaired a resource. Notifications deliberately has incomplete evidence.
  var ASSESSMENT_OUTCOMES = {
    edge: ['ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE'],
    catalog: ['ACHIEVABLE', 'ACHIEVABLE', 'NOT_ACHIEVABLE', 'ACHIEVABLE'],
    checkout: ['NOT_ACHIEVABLE', 'NOT_ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE'],
    payments: ['ACHIEVABLE', 'NOT_ACHIEVABLE', 'ACHIEVABLE', 'NOT_ACHIEVABLE'],
    orders: ['ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE'],
    identity: ['ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE'],
    notifications: [null, null, null, null],
    fulfillment: ['ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE', 'ACHIEVABLE']
  };
  function assessmentResponse(serviceId) {
    if (!Object.prototype.hasOwnProperty.call(ASSESSMENT_OUTCOMES, serviceId)) return null;
    var values = ASSESSMENT_OUTCOMES[serviceId];
    return {
      fixtureId: 'northstar-' + serviceId + '-assessment-response-v1',
      configurationScenario: 'UNCHANGED_NORTHSTAR_ARCHITECTURE',
      provenance: 'INDEPENDENT_MOCK_ASSESSMENT_RESPONSE',
      components: { availabilitySlo: values[0], multiAz: values[1], multiRegion: values[2], dataRecovery: values[3] },
      collectionStatus: serviceId === 'notifications' ? 'PARTIAL' : 'COMPLETE',
      message: serviceId === 'notifications' ? 'The mock assessment completed without usable component outcomes.' : 'Explicit mock outcomes for unchanged architecture; finding disposition is not an evaluation input.'
    };
  }

  var scenarios = [
    { id: 'payment-latency', name: 'Payment latency rises', description: 'A fresh monitoring signal degrades Payments health; resilience posture is unchanged.', icon: 'activity' },
    { id: 'assessment-failed', name: 'Assessment fails', description: 'Payments receives an assessment failure. Its last successful posture remains visible.', icon: 'alert' },
    { id: 'assessment-completed', name: 'Assessment completes', description: 'A successful Orders assessment refreshes posture and captures current findings.', icon: 'check' },
    { id: 'new-dependency', name: 'Dependency discovered', description: 'Payments discovers a fraud-screening DNS dependency requiring operator review.', icon: 'network' },
    { id: 'telemetry-expired', name: 'Telemetry goes stale', description: 'Advance the demo clock beyond signal expiry. Missing current evidence becomes unknown health.', icon: 'clock' },
    { id: 'duplicate-delayed', name: 'Duplicate and delayed events', description: 'Replay one event and ingest an older monitoring signal without rolling back current health.', icon: 'history' }
  ];

  scenarios.forEach(function (scenario) { scenario.label = scenario.name; });

  function createState() {
    var systems = [
      { id: 'commerce', systemId: uuid(101), arn: arn('system', 101), name: 'Commerce platform', description: 'Discover products, place orders and securely complete payment across our European storefronts.', owner: 'Commerce SRE', createdAt: '2026-07-14T09:15:00.000Z', updatedAt: before(135), environment: 'Production' },
      { id: 'customer', systemId: uuid(102), arn: arn('system', 102, PLATFORM_ACCOUNT), name: 'Customer experience', description: 'Identity, account recovery and post-purchase care shared by web and mobile experiences.', owner: 'Customer Platform', createdAt: '2026-07-21T14:40:00.000Z', updatedAt: before(310), environment: 'Production' },
      { id: 'fulfillment', systemId: uuid(103), arn: arn('system', 103, FULFILLMENT_ACCOUNT), name: 'Order fulfillment', description: 'Coordinate warehouse dispatch, shipment updates and customer delivery notifications.', owner: 'Operations Engineering', createdAt: '2026-08-02T11:00:00.000Z', updatedAt: before(72), environment: 'Production' }
    ];
    var policies = [
      { id: 'critical', arn: arn('policy', 201), name: 'Tier 1 · Critical commerce', description: 'Objectives for revenue-critical checkout and authorization.', ownerAccountId: ACCOUNT, createdAt: '2026-07-10T09:00:00.000Z', components: { availabilitySlo: { target: 99.95 }, dataRecovery: { timeBetweenBackupsInMinutes: 60 }, multiAz: { rtoInMinutes: 5, rpoInMinutes: 0, disasterRecoveryApproach: 'ACTIVE_ACTIVE' }, multiRegion: { rtoInMinutes: 60, rpoInMinutes: 15, disasterRecoveryApproach: 'WARM_STANDBY' } } },
      { id: 'experience', arn: arn('policy', 202, PLATFORM_ACCOUNT), name: 'Tier 2 · Customer experience', description: 'Recovery and availability objectives for discovery and customer care.', ownerAccountId: PLATFORM_ACCOUNT, createdAt: '2026-07-12T13:00:00.000Z', components: { availabilitySlo: { target: 99.9 }, dataRecovery: { timeBetweenBackupsInMinutes: 240 }, multiAz: { rtoInMinutes: 15, rpoInMinutes: 5, disasterRecoveryApproach: 'HOT_STANDBY' }, multiRegion: { rtoInMinutes: 240, rpoInMinutes: 60, disasterRecoveryApproach: 'PILOT_LIGHT' } } },
      { id: 'platform', arn: arn('policy', 203, PLATFORM_ACCOUNT), name: 'Shared platform baseline', description: 'Direct objectives for identity, edge and messaging foundations.', ownerAccountId: PLATFORM_ACCOUNT, createdAt: '2026-07-09T09:30:00.000Z', components: { availabilitySlo: { target: 99.99 }, dataRecovery: { timeBetweenBackupsInMinutes: 60 }, multiAz: { rtoInMinutes: 5, rpoInMinutes: 0, disasterRecoveryApproach: 'ACTIVE_ACTIVE' }, multiRegion: { rtoInMinutes: 120, rpoInMinutes: 15, disasterRecoveryApproach: 'WARM_STANDBY' } } },
      { id: 'operations', arn: arn('policy', 204, FULFILLMENT_ACCOUNT), name: 'Tier 2 · Order operations', description: 'Durability and recovery objectives for warehouse and fulfillment workflows.', ownerAccountId: FULFILLMENT_ACCOUNT, createdAt: '2026-08-01T10:00:00.000Z', components: { availabilitySlo: { target: 99.9 }, dataRecovery: { timeBetweenBackupsInMinutes: 60 }, multiAz: { rtoInMinutes: 15, rpoInMinutes: 0, disasterRecoveryApproach: 'HOT_STANDBY' }, multiRegion: { rtoInMinutes: 240, rpoInMinutes: 60, disasterRecoveryApproach: 'BACKUP_AND_RESTORE' } } }
    ];
    var journeys = [
      { id: 'browse', userJourneyId: uuid(301), systemId: 'commerce', name: 'Discover a product', description: 'Search the storefront, compare products and retrieve personalized availability.', policyId: 'experience' },
      { id: 'buy', userJourneyId: uuid(302), systemId: 'commerce', name: 'Browse to buy', description: 'Sign in, create a basket, authorize payment and confirm a purchase.', policyId: 'critical' },
      { id: 'recovery', userJourneyId: uuid(303), systemId: 'customer', name: 'Recover an account', description: 'Verify a customer and deliver the account recovery challenge.', policyId: 'experience' },
      { id: 'support', userJourneyId: uuid(304), systemId: 'customer', name: 'Resolve a purchase issue', description: 'Authenticate the customer, inspect an order and arrange a payment adjustment.', policyId: 'experience' },
      { id: 'delivery', userJourneyId: uuid(305), systemId: 'fulfillment', name: 'Order to delivery', description: 'Release an order to a warehouse and keep the customer informed through delivery.', policyId: 'operations' }
    ];
    journeys.forEach(function (journey) {
      journey.policyArn = policies.find(function (policy) { return policy.id === journey.policyId; }).arn;
      journey.createdAt = '2026-08-04T09:00:00.000Z';
      journey.updatedAt = before(120);
    });

    var services = [
      { id: 'edge', name: 'Storefront edge', description: 'Regional ingress, static storefront delivery and API routing.', owner: 'Edge Platform', accountId: PLATFORM_ACCOUNT, regions: ['eu-west-1', 'eu-central-1'], associations: [{ systemId: 'commerce', journeyIds: ['browse', 'buy'] }, { systemId: 'customer', journeyIds: ['recovery'] }], policyId: 'platform', tier: 'Tier 1', healthState: 'HEALTHY', latency: 86, errorRate: 0.04, healthReason: 'Ingress availability and synthetic browse checks are within the monitoring thresholds.', postureFailures: [], assessmentStatus: 'SUCCESS', resourceCount: 18, eligibleCount: 3 },
      { id: 'catalog', name: 'Product catalog', description: 'Product search, pricing read models and stock availability.', owner: 'Catalog Engineering', accountId: ACCOUNT, regions: ['eu-west-1', 'eu-central-1'], associations: [{ systemId: 'commerce', journeyIds: ['browse', 'buy'] }], policyId: null, tier: 'Tier 1', healthState: 'HEALTHY', latency: 142, errorRate: 0.09, healthReason: 'Search latency and catalog read errors are stable.', postureFailures: ['MULTI_REGION_DISASTER_RECOVERY'], assessmentStatus: 'SUCCESS', resourceCount: 26, eligibleCount: 12 },
      { id: 'checkout', name: 'Checkout orchestration', description: 'Basket validation, checkout workflow and idempotent order submission.', owner: 'Commerce SRE', accountId: ACCOUNT, regions: ['eu-west-1'], associations: [{ systemId: 'commerce', journeyIds: ['buy'] }], policyId: 'critical', tier: 'Tier 1', healthState: 'DEGRADED', latency: 842, errorRate: 1.4, healthReason: 'Synthetic checkout p95 is above the 600 ms operating threshold in Ireland.', postureFailures: ['AVAILABILITY_SLO', 'MULTI_AZ_DISASTER_RECOVERY'], assessmentStatus: 'SUCCESS', resourceCount: 34, eligibleCount: 16 },
      { id: 'payments', name: 'Payments gateway', description: 'Payment authorization, fraud screening and settlement event publication.', owner: 'Payments Reliability', accountId: ACCOUNT, regions: ['eu-west-1', 'eu-central-1'], associations: [{ systemId: 'commerce', journeyIds: ['buy'] }, { systemId: 'customer', journeyIds: ['support'] }], policyId: 'critical', tier: 'Tier 1', healthState: 'HEALTHY', latency: 238, errorRate: 0.18, healthReason: 'Authorization success rate and processor response times are within the monitoring thresholds.', postureFailures: ['MULTI_AZ_DISASTER_RECOVERY', 'DATA_RECOVERY'], assessmentStatus: 'SUCCESS', resourceCount: 22, eligibleCount: 8 },
      { id: 'orders', name: 'Order ledger', description: 'Durable order state, event publication and customer order history.', owner: 'Order Platform', accountId: ACCOUNT, regions: ['eu-west-1', 'eu-central-1'], associations: [{ systemId: 'commerce', journeyIds: ['buy'] }, { systemId: 'customer', journeyIds: ['support'] }, { systemId: 'fulfillment', journeyIds: ['delivery'] }], policyId: 'critical', tier: 'Tier 1', healthState: 'HEALTHY', latency: 104, errorRate: 0.03, healthReason: 'Ledger reads, writes and replication lag are within operational thresholds.', postureFailures: [], assessmentStatus: 'IN_PROGRESS', resourceCount: 29, eligibleCount: 11 },
      { id: 'identity', name: 'Customer identity', description: 'Customer sessions, authentication and account recovery tokens.', owner: 'Identity Platform', accountId: PLATFORM_ACCOUNT, regions: ['eu-west-1', 'eu-central-1'], associations: [{ systemId: 'commerce', journeyIds: ['buy'] }, { systemId: 'customer', journeyIds: ['recovery', 'support'] }], policyId: 'platform', tier: 'Tier 1', healthState: 'HEALTHY', latency: 93, errorRate: 0.05, healthReason: 'Authentication synthetics are passing in both configured Regions.', postureFailures: [], assessmentStatus: 'FAILED', resourceCount: 16, eligibleCount: 4 },
      { id: 'notifications', name: 'Customer notifications', description: 'Transactional email, mobile push and delivery status notifications.', owner: 'Messaging Platform', accountId: PLATFORM_ACCOUNT, regions: ['eu-west-1'], associations: [{ systemId: 'commerce', journeyIds: ['buy'] }, { systemId: 'customer', journeyIds: ['recovery', 'support'] }, { systemId: 'fulfillment', journeyIds: ['delivery'] }], policyId: 'experience', tier: 'Tier 2', healthState: 'HEALTHY', latency: 185, errorRate: 0.2, healthReason: 'The last observed messaging checks passed; the monitoring feed is now overdue.', postureFailures: [], assessmentStatus: 'NOT_STARTED', resourceCount: 12, eligibleCount: 0 },
      { id: 'fulfillment', name: 'Warehouse fulfillment', description: 'Warehouse release, shipping label generation and carrier coordination.', owner: 'Operations Engineering', accountId: FULFILLMENT_ACCOUNT, regions: ['eu-west-1', 'us-east-1'], associations: [{ systemId: 'fulfillment', journeyIds: ['delivery'] }], policyId: 'operations', tier: 'Tier 2', healthState: 'DEGRADED', latency: 1260, errorRate: 0.7, healthReason: 'Dispatch queue age is 12 minutes; the carrier connector is processing below its expected rate.', postureFailures: [], assessmentStatus: 'SUCCESS', resourceCount: 31, eligibleCount: null }
    ];

    var componentNames = { availabilitySlo: 'AVAILABILITY_SLO', multiAz: 'MULTI_AZ_DISASTER_RECOVERY', multiRegion: 'MULTI_REGION_DISASTER_RECOVERY', dataRecovery: 'DATA_RECOVERY' };
    systems.forEach(function (system) { system.systemKey = system.id; system.systemArn = system.arn; });
    policies.forEach(function (policy) { policy.policyArn = policy.arn; });
    var observations = [], effectiveTargetObservations = [], policyContexts = [], assessments = [];
    services.forEach(function (service, index) {
      service.arn = arn('service', 401 + index, service.accountId);
      service.serviceArn = service.arn;
      service.createdAt = '2026-08-' + String(10 + index).padStart(2, '0') + 'T08:30:00.000Z';
      service.updatedAt = before(3 + index);
      service.observedAt = before(2);
      service.environment = 'Production';
      service.permissionModel = { invokerRoleName: 'NorthstarResilienceHubInvoker', crossAccountRoles: service.accountId === ACCOUNT ? [] : [{ crossAccountRoleArn: 'arn:aws:iam::' + ACCOUNT + ':role/NorthstarResilienceReadOnly' }] };
      service.tags = { Environment: 'production', Team: service.owner, Application: service.id };
      service.policyArn = service.policyId ? policies.find(function (policy) { return policy.id === service.policyId; }).arn : null;
      service.inputSources = [
        { id: service.id + '-cfn', inputSourceId: uuid(500 + index), type: 'CFN_STACK', name: 'northstar-' + service.id + '-prod', status: 'ACTIVE', sourceArn: 'arn:aws:cloudformation:eu-west-1:' + service.accountId + ':stack/northstar-' + service.id + '-prod/' + uuid(600 + index), observedAt: before(12) }
      ];
      if (service.id === 'checkout' || service.id === 'payments') service.inputSources.push({ id: service.id + '-eks', inputSourceId: uuid(550 + index), type: 'EKS', name: 'commerce-prod / ' + service.id, status: 'ACTIVE', observedAt: before(12) });
      var healthObservedAt = service.id === 'notifications' ? before(27) : before(1);
      service.health = { state: service.healthState, observedAt: healthObservedAt, expiresAt: service.id === 'notifications' ? before(17) : after(9), source: service.id === 'fulfillment' ? 'CloudWatch queue metrics + carrier synthetic' : 'CloudWatch metrics + synthetic journeys', reason: service.healthReason, latencyMs: service.latency, errorRate: service.errorRate, windowMinutes: 5, ruleVersion: 'northstar-runtime-v1', provenance: 'LOCAL_MONITORING_AGGREGATE' };
      service.health.observationId = 'health-' + service.id + '-initial';
      observations.push(Object.assign({ entityId: service.id, dimension: 'HEALTH' }, copy(service.health)));
      service.resourceDiscovery = { status: service.id === 'fulfillment' ? 'COMPLETED_WITH_FAILURES' : 'SUCCEEDED', lastRunAt: before(service.id === 'fulfillment' ? 1500 : 18), errorCode: service.id === 'fulfillment' ? 'ACCESS_DENIED' : null, error: service.id === 'fulfillment' ? 'The carrier integration account could not be read; previously observed resources are retained.' : null };
      service.dependencyDiscovery = { status: service.id === 'fulfillment' ? 'INITIALIZING' : 'ENABLED', eligibleResourceCount: service.eligibleCount, message: service.id === 'notifications' ? 'No eligible VPC-connected resources were found. DNS coverage is unavailable for this service.' : service.id === 'fulfillment' ? 'Collecting initial DNS query evidence.' : null, updatedAt: before(service.id === 'fulfillment' ? 5 : 18), requestedStatus: 'ENABLED' };
      var postureTime = before(service.id === 'fulfillment' ? 2940 : service.id === 'identity' ? 1380 : 62 + index * 8);
      var assessmentId = uuid(701 + index);
      var components = {};
      Object.keys(componentNames).forEach(function (name) { components[name] = service.id === 'notifications' ? null : service.postureFailures.indexOf(componentNames[name]) >= 0 ? 'NOT_ACHIEVABLE' : 'ACHIEVABLE'; });
      service.posture = { state: service.id === 'notifications' ? 'UNKNOWN' : service.postureFailures.length ? 'NOT_ACHIEVABLE' : 'ACHIEVABLE', components: components, observedAt: service.id === 'notifications' ? null : postureTime, assessmentId: service.id === 'notifications' ? null : assessmentId, source: 'GetService.achievability', ruleVersion: 'any-unachievable-v1', provenance: 'PROVIDER_COMPONENTS_WITH_LOCAL_SUMMARY', evaluatedProviderRevision: null };
      service.posture.observationId = 'posture-' + service.id + '-initial';
      if (service.id !== 'notifications') observations.push(Object.assign({ entityId: service.id, dimension: 'POSTURE' }, copy(service.posture)));
      if (service.id !== 'notifications') assessments.push({ id: service.id + '-last-success', assessmentId: assessmentId, serviceId: service.id, serviceArn: service.arn, status: 'SUCCESS', startedAt: new Date(Date.parse(postureTime) - 19 * 60000).toISOString(), endedAt: postureTime, totalFindings: 0, achievability: copy(components), cost: { amount: Number((2.45 + index * 0.34).toFixed(2)), currency: 'USD' }, errorCode: null, error: null, observedAt: before(2) });
      var applicable = [];
      if (service.policyId) applicable.push({ policyId: service.policyId, assignment: 'DIRECT', journeyId: null });
      service.associations.forEach(function (association) {
        association.journeyIds.forEach(function (journeyId) {
          var journey = journeys.find(function (item) { return item.id === journeyId; });
          applicable.push({ policyId: journey.policyId, assignment: 'INHERITED', journeyId: journey.id });
        });
      });
      service.applicablePolicies = applicable;
      var targetSpecs = [
        ['availabilitySlo', 'Availability SLO', '%', 'availabilitySlo', 'target', true],
        ['dataRecoveryTimeBetweenBackups', 'Backup interval', 'min', 'dataRecovery', 'timeBetweenBackupsInMinutes', false],
        ['multiAzRto', 'Multi-AZ RTO', 'min', 'multiAz', 'rtoInMinutes', false],
        ['multiAzRpo', 'Multi-AZ RPO', 'min', 'multiAz', 'rpoInMinutes', false],
        ['multiAzDrApproach', 'Multi-AZ approach', '', 'multiAz', 'disasterRecoveryApproach', false],
        ['multiRegionRto', 'Multi-Region RTO', 'min', 'multiRegion', 'rtoInMinutes', false],
        ['multiRegionRpo', 'Multi-Region RPO', 'min', 'multiRegion', 'rpoInMinutes', false],
        ['multiRegionDrApproach', 'Multi-Region approach', '', 'multiRegion', 'disasterRecoveryApproach', false]
      ];
      var approachRank = { ACTIVE_ACTIVE: 0, HOT_STANDBY: 1, WARM_STANDBY: 2, PILOT_LIGHT: 3, BACKUP_AND_RESTORE: 4 };
      service.effectiveTargets = targetSpecs.map(function (spec) {
        var candidates = applicable.map(function (assignment) {
          var policy = policies.find(function (item) { return item.id === assignment.policyId; });
          return { assignment: assignment, policy: policy, value: policy.components[spec[3]][spec[4]] };
        });
        candidates.sort(function (a, b) {
          if (typeof a.value === 'string') return approachRank[a.value] - approachRank[b.value];
          return spec[5] ? b.value - a.value : a.value - b.value;
        });
        var selected = candidates[0];
        return { metric: spec[0], label: spec[1], value: selected.value, unit: spec[2], policyId: selected.policy.id, policyName: selected.policy.name, ownership: selected.policy.ownerAccountId === service.accountId ? 'SELF' : 'CROSS_ACCOUNT', source: selected.policy.ownerAccountId === service.accountId ? 'SELF' : 'CROSS_ACCOUNT', assignment: selected.assignment.assignment, journeyId: selected.assignment.journeyId, resolvedPolicyArn: selected.policy.arn, resolutionEvidence: 'Verified mock policy membership and unique policy identity', provenance: 'MOCK_GET_SERVICE_EFFECTIVE_VALUES' };
      });
      var effectiveId = 'targets-' + service.id + '-initial';
      effectiveTargetObservations.push({ effectiveTargetObservationId: effectiveId, serviceId: service.id, serviceArn: service.arn, observedAt: service.id === 'notifications' ? before(2) : postureTime, targets: copy(service.effectiveTargets), evaluatedProviderRevision: null });
      service.effectiveTargetObservationId = effectiveId;
      policyContexts.push({ policyContextCaptureId: 'policy-context-' + service.id + '-initial', serviceArn: service.arn, observedAt: service.id === 'notifications' ? before(2) : postureTime, associations: copy(service.associations), applicablePolicies: copy(applicable), effectiveTargetObservationId: effectiveId, provenance: 'LOCAL_CAPTURE', assessedProviderRevision: null });
      service.policyContextCaptureId = 'policy-context-' + service.id + '-initial';
      service.posture.policyContextCaptureId = service.policyContextCaptureId;
      service.posture.assessmentLinkage = 'LOCAL_CORRELATION';
      service.posture.assessmentCorrelationBasis = 'Posture observed after this completed assessment; no evaluated provider policy revision is exposed.';
      var recordedPosture = observations.find(function (item) { return item.entityId === service.id && item.dimension === 'POSTURE'; });
      if (recordedPosture) {
        recordedPosture.policyContextCaptureId = service.policyContextCaptureId;
        recordedPosture.assessmentLinkage = service.posture.assessmentLinkage;
        recordedPosture.assessmentCorrelationBasis = service.posture.assessmentCorrelationBasis;
      }
      delete service.healthState; delete service.healthReason; delete service.latency; delete service.errorRate; delete service.postureFailures; delete service.eligibleCount;
    });
    assessments.push({ id: 'orders-active', assessmentId: uuid(720), serviceId: 'orders', serviceArn: services[4].arn, status: 'IN_PROGRESS', stepLabel: 'Analyzing service functions', startedAt: before(12), endedAt: null, totalFindings: null, cost: null, observedAt: before(2) });
    assessments.push({ id: 'identity-failed', assessmentId: uuid(721), serviceId: 'identity', serviceArn: services[5].arn, status: 'FAILED', startedAt: before(54), endedAt: before(48), totalFindings: null, cost: { amount: 0.64, currency: 'USD' }, errorCode: 'INVALID_PERMISSIONS', error: 'The assessment role cannot read the recovery stack in the secondary account.', observedAt: before(2) });

    var findingSpecs = [
      ['edge-cache', 'edge', 'LOW', 'OPEN', 'MISCONFIGURATION_AND_BUGS', 'AVAILABILITY_SLO', 'Cache invalidation lacks a rehearsal', 'The storefront release process has no recent rehearsal of a failed cache invalidation.', 'A failed invalidation can keep an obsolete storefront shell active until its TTL expires.', 'Rehearse a partial invalidation failure and document the rollback decision.'],
      ['catalog-region', 'catalog', 'HIGH', 'OPEN', 'SINGLE_POINT_OF_FAILURE', 'MULTI_REGION_DISASTER_RECOVERY', 'Search index recovery exceeds the target', 'The secondary search index is restored from snapshot and cannot meet the 60-minute regional recovery objective.', 'Restoring the current index from its latest snapshot takes approximately 145 minutes in the mock exercise.', 'Maintain a warm search cluster in the recovery Region and replicate index changes.'],
      ['catalog-refresh', 'catalog', 'MEDIUM', 'OPEN', 'EXCESSIVE_LOAD', 'AVAILABILITY_SLO', 'Catalog refresh competes with live traffic', 'Bulk catalog refresh and customer reads share the same worker pool.', 'The nightly refresh can exhaust workers during a promotion-driven traffic spike.', 'Separate bulk refresh workers from the customer read pool and cap refresh concurrency.'],
      ['checkout-az', 'checkout', 'HIGH', 'OPEN', 'SHARED_FATE', 'MULTI_AZ_DISASTER_RECOVERY', 'Checkout workers share one availability zone', 'All checkout workers are currently scheduled in eu-west-1a.', 'An availability zone disruption would remove the complete checkout worker fleet.', 'Distribute worker replicas across at least two availability zones using topology spread constraints.'],
      ['checkout-timeout', 'checkout', 'HIGH', 'OPEN', 'EXCESSIVE_LATENCY', 'AVAILABILITY_SLO', 'Payment retries can amplify checkout latency', 'The checkout retry budget can exceed the customer-facing request deadline.', 'Three synchronous authorization retries can keep requests open after clients have retried, increasing load.', 'Use a bounded end-to-end deadline, jittered backoff and an idempotency key for payment authorization.'],
      ['checkout-canary', 'checkout', 'LOW', 'IRRELEVANT', 'MISCONFIGURATION_AND_BUGS', 'AVAILABILITY_SLO', 'Mobile-only canary is outside this service boundary', 'A generated suggestion refers to the native mobile client, which is owned by another team.', 'The service boundary excludes mobile application delivery.', 'Track the mobile canary requirement in the mobile experience service.'],
      ['payments-db', 'payments', 'HIGH', 'OPEN', 'SINGLE_POINT_OF_FAILURE', 'MULTI_AZ_DISASTER_RECOVERY', 'Settlement writer has no automatic failover', 'The settlement database writer has no standby in a second availability zone.', 'Manual restoration exceeds the five-minute recovery target for a zone disruption.', 'Enable a Multi-AZ deployment and rehearse a controlled database failover.'],
      ['payments-backup', 'payments', 'MEDIUM', 'OPEN', 'MISCONFIGURATION_AND_BUGS', 'DATA_RECOVERY', 'Settlement backup interval is too long', 'Scheduled backups run every four hours against a one-hour recovery policy.', 'The configured schedule permits a recovery point older than the required backup interval.', 'Schedule hourly recovery points and verify that a selected recovery point can be restored.'],
      ['payments-trace', 'payments', 'LOW', 'RESOLVED', 'EXCESSIVE_LATENCY', 'AVAILABILITY_SLO', 'Authorization traces did not include processor wait time', 'The team has added processor-span timing to the authorization trace.', 'Updated instrumentation is present in the latest observed deployment.', 'Retain processor spans and alert on sustained p95 wait-time increases.'],
      ['orders-replay', 'orders', 'MEDIUM', 'RESOLVED', 'MISCONFIGURATION_AND_BUGS', 'DATA_RECOVERY', 'Order event replay needed an idempotency check', 'The replay consumer now checks a stable event identifier before applying state transitions.', 'The previously observed replay failure mode was removed in the latest observed configuration.', 'Keep the duplicate-event replay test in the deployment verification suite.'],
      ['orders-queue', 'orders', 'LOW', 'OPEN', 'EXCESSIVE_LOAD', 'AVAILABILITY_SLO', 'Backlog alarm has no ownership route', 'The order event backlog alarm has no explicit on-call route for off-hours incidents.', 'Detection exists, but delayed escalation can extend recovery from a growing backlog.', 'Route the backlog alarm to Order Platform on-call and document the drain procedure.'],
      ['identity-limit', 'identity', 'MEDIUM', 'OPEN', 'EXCESSIVE_LOAD', 'AVAILABILITY_SLO', 'Recovery traffic has no separate rate budget', 'Account recovery requests share an admission limit with normal sign-in traffic.', 'A recovery burst could consume capacity needed for successful sign-ins.', 'Apply a separate recovery request budget and monitor rejected recovery attempts.'],
      ['fulfillment-carrier', 'fulfillment', 'MEDIUM', 'OPEN', 'EXCESSIVE_LATENCY', 'AVAILABILITY_SLO', 'Carrier calls hold dispatch workers', 'A slow carrier response can occupy every worker in the dispatch pool.', 'The current pool has no independent bulkhead for carrier calls.', 'Isolate carrier requests behind a bounded queue and limit concurrent calls.'],
      ['fulfillment-recovery', 'fulfillment', 'LOW', 'RESOLVED', 'MISCONFIGURATION_AND_BUGS', 'MULTI_REGION_DISASTER_RECOVERY', 'Warehouse recovery runbook had an obsolete queue name', 'The warehouse recovery runbook now refers to the current recovery queue.', 'The updated runbook was observed after the maintenance review.', 'Keep queue identifiers generated from the deployed configuration.']
    ];
    var findings = findingSpecs.map(function (spec, index) {
      var service = services.find(function (item) { return item.id === spec[1]; });
      var finding = { id: spec[0], findingId: uuid(801 + index), serviceId: service.id, serviceArn: service.arn, observationId: 'finding-observation-' + spec[0] + '-detail-1', captureId: 'finding-capture-' + service.id + '-initial', name: spec[6], description: spec[7], reasoning: spec[8], severity: spec[2], status: spec[3], failureCategory: spec[4], policyComponent: spec[5], serviceFunctions: [service.id + '-primary-function'], updatedAt: before(90 + index * 3), representation: 'DETAIL', detailObservedAt: before(4), statusObservedAt: before(4), comment: spec[3] === 'IRRELEVANT' ? 'Reviewed with the mobile team. Outside this service boundary; their separate backlog tracks the requirement.' : spec[3] === 'RESOLVED' ? 'Change deployed and observed in the latest configuration review.' : '', verification: spec[3] === 'IRRELEVANT' ? 'SUPPRESSED' : 'LAST_ASSESSED' };
      var recommendations = [{ category: 'INFRASTRUCTURE_AND_CODE', title: index === 6 ? 'Add a standby settlement writer' : 'Address the configuration gap', suggestedChanges: [spec[9]], estimate: { amount: index === 6 ? 186 : index === 1 ? 420 : 0, currency: 'USD', basis: 'estimated additional monthly infrastructure', complexity: spec[2] === 'HIGH' ? 'MEDIUM' : 'LOW', source: 'Northstar engineering estimate', estimatedAt: before(180), confidence: 'ROUGH_ORDER_OF_MAGNITUDE' } }];
      if (spec[2] === 'HIGH' || index === 7 || index === 12) recommendations.push({ category: 'OBSERVABILITY', title: 'Make the failure visible', suggestedChanges: ['Add an owned alert and dashboard for ' + service.name.toLowerCase() + ' that distinguishes this failure from downstream symptoms.'], estimate: { amount: 0, currency: 'USD', basis: 'estimated additional monthly infrastructure', complexity: 'LOW', source: 'Northstar engineering estimate', estimatedAt: before(180), confidence: 'ROUGH_ORDER_OF_MAGNITUDE' } });
      if (spec[2] === 'HIGH' || index === 9) recommendations.push({ category: 'TESTING', title: 'Exercise recovery safely', suggestedChanges: ['Run a controlled recovery exercise in a representative environment and compare observed recovery time with the applicable objective.'], estimate: { amount: null, currency: 'USD', basis: 'cost not yet estimated', complexity: 'MEDIUM', source: 'Northstar engineering estimate', estimatedAt: before(180), confidence: 'UNESTIMATED' } });
      finding.recommendations = recommendations.map(function (recommendation, ordinal) {
        return Object.assign({ id: 'recommendation-' + spec[0] + '-' + ordinal + '-1', observationId: finding.observationId, sourceArrayOrdinal: 0, description: recommendation.suggestedChanges[0], capturedAt: before(4), enrichmentProvenance: 'LOCAL_PRODUCT_ENRICHMENT' }, recommendation);
      });
      finding.recommendationFields = {};
      [['infrastructureAndCodeRecommendations', 'INFRASTRUCTURE_AND_CODE'], ['observabilityRecommendations', 'OBSERVABILITY'], ['testingRecommendations', 'TESTING']].forEach(function (pair) {
        finding.recommendationFields[pair[0]] = finding.recommendations.some(function (rec) { return rec.category === pair[1]; }) ? 'PRESENT' : 'EMPTY';
      });
      return finding;
    });
    var findingCaptures = [], findingObservations = [];
    services.forEach(function (service) {
      var currentFindings = findings.filter(function (finding) { return finding.serviceId === service.id; });
      if (service.id === 'notifications') return;
      var captureId = 'finding-capture-' + service.id + '-initial';
      var assessment = assessments.find(function (item) { return item.serviceId === service.id && item.status === 'SUCCESS'; });
      findingCaptures.push({ id: captureId, captureId: captureId, serviceId: service.id, serviceArn: service.arn, captureStartedAt: before(6), captureEndedAt: before(4), collectionStatus: 'COMPLETE', listCoverage: { status: 'COMPLETE', pages: 1, filters: {}, findingsReturned: currentFindings.length }, detailCoverage: { status: 'COMPLETE', requested: currentFindings.length, hydrated: currentFindings.length, failed: 0 }, relatedAssessmentId: assessment ? assessment.assessmentId : null, correlationBasis: 'Latest completed assessment observed before this capture; ownership is not asserted.' });
      currentFindings.forEach(function (finding) {
        findingObservations.push({ observationId: 'finding-observation-' + finding.id + '-summary-1', captureId: captureId, serviceArn: service.arn, findingId: finding.findingId, representation: 'SUMMARY', observedAt: before(6), name: finding.name, severity: finding.severity, status: finding.status, recommendationPresence: 'NOT_FETCHED' });
        findingObservations.push({ observationId: finding.observationId, captureId: captureId, serviceArn: service.arn, findingId: finding.findingId, representation: 'DETAIL', observedAt: finding.detailObservedAt, name: finding.name, severity: finding.severity, status: finding.status, recommendationPresence: 'PRESENT', recommendationFields: copy(finding.recommendationFields), recommendationIds: finding.recommendations.map(function (rec) { return rec.id; }) });
      });
      if (assessment) assessment.totalFindings = currentFindings.length;
      service.openFindingsCount = currentFindings.filter(function (finding) { return finding.status === 'OPEN'; }).length;
      service.resolvedFindingsCount = currentFindings.filter(function (finding) { return finding.status === 'RESOLVED'; }).length;
    });

    var dependencySpecs = [
      ['checkout-payments', 'checkout', 'Payments API', 'payments.service.northstar.example', 'Internal · Ireland', 'HARD', 'Northstar', 'payments'],
      ['checkout-orders', 'checkout', 'Order ledger API', 'orders.service.northstar.example', 'Internal · Ireland', 'HARD', 'Northstar', 'orders'],
      ['payments-processor', 'payments', 'Card processor', 'api.eu.paybridge.example', 'External · EU', 'HARD', 'Paybridge', null],
      ['payments-vault', 'payments', 'Token vault', 'vault.payment.northstar.example', 'Internal · Frankfurt', 'HARD', 'Northstar', null],
      ['catalog-pricing', 'catalog', 'Pricing feed', 'prices.partner.example', 'External · EU', 'SOFT', 'Marketfeed', null],
      ['orders-warehouse', 'orders', 'Warehouse API', 'warehouse.service.northstar.example', 'Internal · Ireland', 'SOFT', 'Northstar', 'fulfillment'],
      ['identity-notifications', 'identity', 'Recovery messaging', 'notify.service.northstar.example', 'Internal · Ireland', 'HARD', 'Northstar', 'notifications'],
      ['fulfillment-carrier', 'fulfillment', 'Carrier label API', 'labels.eu.parcelpath.example', 'External · EU', 'HARD', 'Parcelpath', null],
      ['edge-catalog', 'edge', 'Catalog API', 'catalog.service.northstar.example', 'Internal · Ireland', 'HARD', 'Northstar', 'catalog']
    ];
    var dependencies = dependencySpecs.map(function (spec, index) {
      var service = services.find(function (item) { return item.id === spec[1]; });
      var item = { id: spec[0], dependencyId: uuid(901 + index), serviceId: service.id, serviceArn: service.arn, name: spec[2], dependencyName: spec[2], dnsName: spec[3], location: spec[4], criticality: spec[5], provider: spec[6], sourceRegions: ['eu-west-1'], lastDetectedTime: before(3 + index), comment: index === 2 ? 'Processor is required for card authorization. Monitor independently of our resilience posture.' : '', queryRange: { startTime: before(360), endTime: before(0), granularity: 'HOURLY', dataPoints: [6, 5, 4, 3, 2, 1].map(function (hour, i) { return { timestamp: before(hour * 60), queryCount: 2100 + index * 643 + [0, 320, -140, 760, 610, 415][i] }; }) }, firstObservedAt: '2026-10-19T11:00:00.000Z', governance: { allowedStatus: 'ALLOWED', source: 'Northstar supplier and service allow-list', observedAt: before(1440) } };
      if (spec[7]) item.resolution = { serviceId: spec[7], evidence: 'Operator-verified DNS ownership mapping in Northstar service catalog', confidence: 'VERIFIED_LOCAL', observedAt: before(1440), provenance: 'LOCAL_ENRICHMENT' };
      return item;
    });

    var topologies = services.map(function (service, index) {
      var region = service.regions[0];
      var topologyId = 'topology-' + service.id + '-initial';
      var partial = service.id === 'fulfillment';
      var nodes = [
        { id: 'ingress', resourceIdentifier: 'arn:aws:elasticloadbalancing:' + region + ':' + service.accountId + ':loadbalancer/app/' + service.id + '-prod/ab12cd34', name: service.id === 'edge' ? 'Storefront ingress' : 'Service ingress', type: 'AWS::ElasticLoadBalancingV2::LoadBalancer', region: region, accountId: service.accountId, status: 'KNOWN', x: 68, y: 132 },
        { id: 'worker-a', resourceIdentifier: 'arn:aws:ecs:' + region + ':' + service.accountId + ':service/commerce-prod/' + service.id + '-a', name: service.id === 'checkout' ? 'Workers · AZ a' : 'Worker pool · AZ a', type: 'AWS::ECS::Service', region: region, accountId: service.accountId, status: 'KNOWN', x: 265, y: 65 },
        { id: 'worker-b', resourceIdentifier: 'arn:aws:ecs:' + region + ':' + service.accountId + ':service/commerce-prod/' + service.id + '-b', name: service.id === 'checkout' ? 'Workers · same AZ a' : 'Worker pool · AZ b', type: 'AWS::ECS::Service', region: region, accountId: service.accountId, status: 'KNOWN', x: 265, y: 205 },
        { id: 'store', resourceIdentifier: 'arn:aws:rds:' + region + ':' + service.accountId + ':cluster:' + service.id + '-prod', name: service.id === 'payments' ? 'Settlement writer' : 'State store', type: 'AWS::RDS::DBCluster', region: region, accountId: service.accountId, status: 'KNOWN', x: 470, y: 92 },
        { id: 'queue', resourceIdentifier: 'arn:aws:sqs:' + region + ':' + service.accountId + ':' + service.id + '-events', name: 'Event queue', type: 'AWS::SQS::Queue', region: region, accountId: service.accountId, status: 'KNOWN', x: 470, y: 232 },
        { id: 'monitor', resourceIdentifier: partial ? 'unresolved:carrier-account-alarm' : 'arn:aws:cloudwatch:' + region + ':' + service.accountId + ':alarm:' + service.id + '-availability', name: partial ? 'External alarm · unresolved' : 'Availability alarm', type: partial ? 'Unknown' : 'AWS::CloudWatch::Alarm', region: partial ? null : region, accountId: partial ? null : service.accountId, status: partial ? 'UNRESOLVED' : 'KNOWN', x: 265, y: 342 }
      ];
      var edges = [
        { id: 'edge-1', source: 'ingress', target: 'worker-a', type: 'DATA_FLOW', label: 'routes requests', provenance: 'PROVIDER_EDGE' },
        { id: 'edge-2', source: 'ingress', target: 'worker-b', type: 'DATA_FLOW', label: 'routes requests', provenance: 'PROVIDER_EDGE' },
        { id: 'edge-3', source: 'worker-a', target: 'store', type: 'DATA_FLOW', label: 'reads and writes', provenance: 'PROVIDER_EDGE' },
        { id: 'edge-4', source: 'worker-b', target: 'store', type: 'DATA_FLOW', label: 'reads and writes', provenance: 'PROVIDER_EDGE' },
        { id: 'edge-5', source: 'worker-b', target: 'queue', type: 'DATA_FLOW', label: 'publishes events', provenance: 'PROVIDER_EDGE' },
        { id: 'edge-6', source: 'monitor', target: 'worker-b', type: 'OBSERVABILITY', label: 'observes availability', provenance: 'PROVIDER_EDGE' },
        { id: 'edge-7', source: 'worker-a', target: 'queue', type: 'PERMISSIONS', label: 'may publish', provenance: 'PROVIDER_EDGE' }
      ];
      nodes.forEach(function (node) { node.topologyId = topologyId; });
      edges.forEach(function (edge) { edge.topologyId = topologyId; edge.sourceResourceIdentifier = nodes.find(function (node) { return node.id === edge.source; }).resourceIdentifier; edge.destinationResourceIdentifier = nodes.find(function (node) { return node.id === edge.target; }).resourceIdentifier; edge.labelProvenance = 'LOCAL_DISPLAY_LABEL'; });
      return { id: topologyId, topologyId: topologyId, serviceId: service.id, serviceArn: service.arn, capturedAt: before(15), captureStartedAt: before(17), captureEndedAt: before(15), collectionStatus: partial ? 'PARTIAL' : 'COMPLETE', queryScope: { billable: false, regions: service.regions.slice(), illustration: 'Six-resource representative mock subgraph' }, resourceCount: nodes.filter(function (node) { return node.status === 'KNOWN'; }).length, totalServiceResourceCount: service.resourceCount, edgeCount: edges.length, unresolvedCount: partial ? 1 : 0, nodes: nodes, edges: edges, atomicSnapshot: false, provenance: 'LOCAL_ASSEMBLY_OF_MOCK_LIST_RESPONSES', coverageMessage: partial ? 'One external resource is unresolved; a resource page could not be read.' : 'All pages in this six-resource demonstration scope were collected.' };
    });

    var events = [
      { id: 'event-006', sourceEventId: uuid(1006), channel: 'TELEMETRY', streamOwner: 'northstar/checkout/runtime', type: 'RUNTIME_HEALTH_CHANGED', title: 'Checkout latency increased', message: 'Synthetic checkout p95 reached 842 ms. Live health is degraded; assessed posture is unchanged.', severity: 'WARNING', serviceId: 'checkout', entityType: 'Service', entityId: 'checkout', occurredAt: before(1), receivedAt: before(1), linkage: 'ASSERTED', refreshStatus: 'REFRESHED' },
      { id: 'event-005', sourceEventId: uuid(1005), channel: 'ENTITY_TIMELINE', streamOwner: services[7].arn, type: 'RESOURCE_DISCOVERY_UPDATED', title: 'Fulfillment discovery is partial', message: 'The carrier account could not be read. Known resources and unresolved references are retained.', severity: 'WARNING', serviceId: 'fulfillment', entityType: 'Service', entityId: 'fulfillment', occurredAt: before(5), receivedAt: before(4), linkage: 'ASSERTED', refreshStatus: 'REFRESHED' },
      { id: 'event-004', sourceEventId: uuid(1004), channel: 'EVENTBRIDGE', streamOwner: services[4].arn, type: 'Failure Mode Assessment Queued', title: 'Order ledger assessment started', message: 'A queued event triggered a list refresh. The assessment is now in progress.', severity: 'INFO', serviceId: 'orders', entityType: 'Assessment', entityId: uuid(720), occurredAt: before(12), receivedAt: before(11), linkage: 'ASSERTED', refreshStatus: 'REFRESHED' },
      { id: 'event-003', sourceEventId: uuid(1003), channel: 'EVENTBRIDGE', streamOwner: services[5].arn, type: 'Failure Mode Assessment Failed', title: 'Identity assessment failed', message: 'The assessment role lacks secondary-account access. Last successful posture from yesterday is retained.', severity: 'ERROR', serviceId: 'identity', entityType: 'Assessment', entityId: uuid(721), occurredAt: before(48), receivedAt: before(47), linkage: 'ASSERTED', refreshStatus: 'REFRESHED' },
      { id: 'event-002', sourceEventId: uuid(1002), channel: 'EVENTBRIDGE', streamOwner: services[3].arn, type: 'Failure Mode Assessment Completed', title: 'Payments posture refreshed', message: 'A completed assessment prompted GetService and finding refreshes. Two open findings need attention.', severity: 'INFO', serviceId: 'payments', entityType: 'Assessment', entityId: uuid(704), occurredAt: before(86), receivedAt: before(85), linkage: 'ASSERTED', refreshStatus: 'REFRESHED' },
      { id: 'event-001', sourceEventId: uuid(1001), channel: 'ENTITY_TIMELINE', streamOwner: services[2].arn, type: 'FINDING_STATUS_UPDATED', title: 'Mobile canary finding suppressed', message: 'The operator marked a suggestion irrelevant because mobile delivery is outside the checkout service boundary.', severity: 'INFO', serviceId: 'checkout', entityType: 'Finding', entityId: uuid(806), occurredAt: before(115), receivedAt: before(114), linkage: 'ASSERTED', refreshStatus: 'REFRESHED' }
    ];
    events.forEach(function (event) { event.eventKey = event.channel + '|' + event.streamOwner + '|' + event.sourceEventId; event.source = event.channel === 'EVENTBRIDGE' ? 'aws.resiliencehub' : event.channel === 'TELEMETRY' ? 'northstar.mock.monitoring' : 'resiliencehubv2 entity timeline'; event.mock = true; });
    return {
      schemaVersion: 2, now: NOW, organization: { name: 'Northstar Commerce', description: 'European digital commerce and fulfillment', environment: 'Production', mock: true },
      systems: systems, journeys: journeys, services: services, policies: policies, assessments: assessments, findings: findings,
      findingCaptures: findingCaptures, findingObservations: findingObservations, recommendations: findings.reduce(function (all, finding) { return all.concat(copy(finding.recommendations)); }, []), observations: observations, effectiveTargetObservations: effectiveTargetObservations, policyContexts: policyContexts,
      dependencies: dependencies, topologies: topologies, events: events,
      stats: { duplicateEvents: 0, staleEvents: 0, refreshes: 0, projectionRevision: 1, scenarioRuns: 0 },
      sequence: 2000, scenarioHistory: [], notes: { fixture: 'Fictional data; no AWS connection', topology: 'Representative subgraphs, not complete production resource inventories', estimates: 'All recommendation estimates are local Northstar examples' }
    };
  }
  return { createState: createState, scenarios: scenarios, initialTime: NOW, assessmentResponse: assessmentResponse };
});
