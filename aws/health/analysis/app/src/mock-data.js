/*
 * Fictional AWS Health demonstration fixtures.
 * No account, event, resource, or lifecycle date in this file describes a real
 * customer or an actual AWS notification. See meta.fictionNotice.
 * Works as a browser script and as a dependency-free CommonJS module.
 */
(function (root) {
  'use strict';

  const asOf = '2026-11-05T13:30:00Z';
  const organizationId = 'o-demo-northstar';
  const accountIds = {
    commerce: '111100001001',
    payments: '111100001002',
    data: '111100001003',
    shared: '111100001004',
    development: '111100001005'
  };

  const accounts = [
    { id: accountIds.commerce, name: 'Commerce production', environment: 'Production', owner: 'SRE' },
    { id: accountIds.payments, name: 'Payments production', environment: 'Production', owner: 'Payments' },
    { id: accountIds.data, name: 'Data platform', environment: 'Production', owner: 'Data' },
    { id: accountIds.shared, name: 'Shared services', environment: 'Shared', owner: 'Platform' },
    { id: accountIds.development, name: 'Development', environment: 'Development', owner: 'Developer Experience' }
  ];

  function event(id, service, typeCode, region, category, scope, title, summary, priority) {
    return {
      id,
      eventArn: 'arn:aws:health:' + region + '::event/' + service + '/' + typeCode + '/DEMO_' + id.replace(/-/g, '_').toUpperCase(),
      title, service, typeCode, category, scope, region, priority, summary
    };
  }

  const events = [
    event('evt-ec2-network', 'EC2', 'AWS_EC2_OPERATIONAL_ISSUE', 'eu-central-1', 'issue', 'ACCOUNT_SPECIFIC',
      'Packet loss on a subset of EC2 hosts',
      'AWS has reported intermittent connectivity affecting checkout hosts and a shared edge instance. Three observed entities are impaired; one broader impact marker has unknown scope.', 'critical'),
    event('evt-s3-public', 'S3', 'AWS_S3_OPERATIONAL_ISSUE', 'us-east-1', 'issue', 'PUBLIC',
      'Increased S3 API error rates in Northern Virginia',
      'A public service advisory is relevant to data ingestion and audit workloads. Notification receipt does not establish an affected account or resource.', 'high'),
    event('evt-lambda-runtime', 'LAMBDA', 'AWS_LAMBDA_PLANNED_LIFECYCLE_EVENT', 'eu-west-1', 'scheduledChange', 'ACCOUNT_SPECIFIC',
      'Plan the legacy Lambda runtime upgrade',
      'Three accounts share this illustrative runtime lifecycle event. A payment function has been upgraded locally, while AWS still reports its affected-entity state as pending.', 'high'),
    event('evt-rds-maintenance', 'RDS', 'AWS_RDS_MAINTENANCE_SCHEDULED', 'us-east-1', 'scheduledChange', 'ACCOUNT_SPECIFIC',
      'Review the warehouse database maintenance window',
      'A database maintenance window is scheduled for the writer and read replica. The team must review its failover plan; AWS has not established their present impact state.', 'medium'),
    event('evt-eks-support', 'EKS', 'AWS_EKS_PLANNED_LIFECYCLE_EVENT', 'us-west-2', 'scheduledChange', 'ACCOUNT_SPECIFIC',
      'Kubernetes support milestone is approaching',
      'The analytics cluster still needs an upgrade before a fictional support milestone. The development cluster was already upgraded and is reported resolved.', 'high'),
    event('evt-ec2-retirement', 'EC2', 'AWS_EC2_INSTANCE_RETIREMENT_SCHEDULED', 'eu-west-1', 'scheduledChange', 'ACCOUNT_SPECIFIC',
      'Replace a scheduled-to-retire payments worker',
      'One payments batch worker is scheduled for retirement tomorrow. A replacement plan needs an owner before the internal readiness deadline.', 'high'),
    event('evt-s3-access', 'S3', 'AWS_S3_OPEN_ACCESS_BUCKET_NOTIFICATION', 'eu-central-1', 'accountNotification', 'ACCOUNT_SPECIFIC',
      'Review public access on an audit export bucket',
      'An account-specific security notification requests review of a bucket access configuration. The notification is actionable without claiming a present availability impairment.', 'high'),
    event('evt-elb-recovered', 'ELASTICLOADBALANCING', 'AWS_ELASTICLOADBALANCING_API_ISSUE', 'eu-west-1', 'issue', 'ACCOUNT_SPECIFIC',
      'Load balancer API latency has recovered',
      'AWS has closed the event and reports both affected load balancers unimpaired. The SRE team is still verifying checkout recovery.', 'medium'),
    event('evt-rds-billing', 'RDS', 'AWS_RDS_DEMO_EXTENDED_SUPPORT_NOTICE', 'us-east-1', 'accountNotification', 'ACCOUNT_SPECIFIC',
      'Extended support billing notice for the warehouse',
      'An illustrative billing notice concerns the same database also listed in the maintenance event. AWS has supplied no affected-entity status for this notice.', 'low'),
    event('evt-ec2-oregon', 'EC2', 'AWS_EC2_OPERATIONAL_ISSUE', 'us-west-2', 'issue', 'ACCOUNT_SPECIFIC',
      'Oregon host connectivity details are incomplete',
      'Two of three illustrative resource pages have arrived. One observed development host is impaired, another has unknown state, and the latest regional API reconciliation is stale.', 'high')
  ];

  function context(id, eventId, accountId, statusCode, startTime, lastUpdatedTime, actionability, personas, description, extra) {
    const kind = accountId ? 'ACCOUNT' : 'PUBLIC';
    return Object.assign({
      id, eventId, kind, contextKey: accountId || 'PUBLIC',
      accountId: accountId || null, organizationId: null,
      statusCode, startTime, endTime: null, lastUpdatedTime,
      actionability: actionability || null, personas: personas || [], description,
      sourceKind: accountId ? 'DescribeEventDetailsForOrganization' : 'EventBridge public notification'
    }, extra || {});
  }

  const contexts = [
    context('ctx-network-commerce', 'evt-ec2-network', accountIds.commerce, 'open', '2026-11-05T12:42:00Z', '2026-11-05T13:26:00Z', null, ['OPERATIONS'],
      'Intermittent packet loss is affecting a subset of EC2 hosts in Frankfurt. Two checkout instances are currently reported impaired; a third is unimpaired. AWS continues investigating.'),
    context('ctx-network-shared', 'evt-ec2-network', accountIds.shared, 'open', '2026-11-05T12:42:00Z', '2026-11-05T13:26:00Z', null, ['OPERATIONS'],
      'The shared edge instance is reported impaired. An additional Health entity describes a wider connectivity scope that cannot yet be resolved to individual inventory resources.'),
    context('ctx-network-org', 'evt-ec2-network', null, 'open', '2026-11-05T12:42:00Z', '2026-11-05T13:26:00Z', null, ['OPERATIONS'],
      'Organization listing summary. Per-account detail and entity observations remain independent of this summary.',
      { kind: 'ORG_SUMMARY', contextKey: organizationId, organizationId, sourceKind: 'DescribeEventsForOrganization' }),
    context('ctx-s3-public', 'evt-s3-public', null, 'open', '2026-11-05T12:10:00Z', '2026-11-05T13:21:00Z', null, ['OPERATIONS'],
      'AWS has reported increased S3 API error rates in Northern Virginia. This public notification was delivered in two account contexts. No affected-account association or affected entity is asserted by this fixture.'),
    context('ctx-lambda-commerce', 'evt-lambda-runtime', accountIds.commerce, 'open', '2026-12-05T00:00:00Z', '2026-11-04T13:00:00Z', 'ACTION_REQUIRED', ['OPERATIONS'],
      'Illustrative runtime retirement notice: checkout-router remains pending; receipt-dispatch has been upgraded and is reported resolved. The future change date does not determine the provider event status.'),
    context('ctx-lambda-payments', 'evt-lambda-runtime', accountIds.payments, 'open', '2026-12-05T00:00:00Z', '2026-11-04T13:00:00Z', 'ACTION_REQUIRED', ['OPERATIONS'],
      'Illustrative runtime retirement notice: payment-webhook and payment-retry are still reported pending by AWS. The Payments team completed the payment-webhook upgrade after the last provider observation.'),
    context('ctx-lambda-development', 'evt-lambda-runtime', accountIds.development, 'open', '2026-12-05T00:00:00Z', '2026-11-04T13:00:00Z', 'ACTION_REQUIRED', ['OPERATIONS'],
      'The sandbox-order-simulator function is reported resolved. The shared event remains open in this fixture; preserve the returned context status rather than deriving it from dates or resource counts.'),
    context('ctx-rds-maintenance', 'evt-rds-maintenance', accountIds.data, 'upcoming', '2026-11-07T02:00:00Z', '2026-11-05T10:05:00Z', 'ACTION_MAY_BE_REQUIRED', ['OPERATIONS'],
      'A fictional database maintenance window is scheduled for 7 November. Review connection retry behavior and replica failover before the window. Both current affected-entity states are reported UNKNOWN.'),
    context('ctx-eks-data', 'evt-eks-support', accountIds.data, 'open', '2026-11-12T00:00:00Z', '2026-11-05T10:10:00Z', 'ACTION_REQUIRED', ['OPERATIONS', 'BILLING'],
      'The analytics cluster is pending an upgrade before an illustrative support milestone on 12 November. Any support and billing dates in this demonstration are fictional.'),
    context('ctx-eks-development', 'evt-eks-support', accountIds.development, 'open', '2026-11-12T00:00:00Z', '2026-11-05T10:10:00Z', 'ACTION_REQUIRED', ['OPERATIONS', 'BILLING'],
      'The development cluster is reported resolved after its upgrade. Inventory contains a newer version that has no matching entry in this reduced demo catalog.'),
    context('ctx-retirement-payments', 'evt-ec2-retirement', accountIds.payments, 'upcoming', '2026-11-06T10:00:00Z', '2026-11-05T08:00:00Z', 'ACTION_REQUIRED', ['OPERATIONS'],
      'The batch worker is pending retirement. Prepare and verify replacement capacity before the illustrative change window on 6 November.'),
    context('ctx-bucket-shared', 'evt-s3-access', accountIds.shared, 'open', '2026-11-05T12:35:00Z', '2026-11-05T12:50:00Z', 'ACTION_REQUIRED', ['SECURITY'],
      'Review the access policy for the demo audit-export bucket. The entity state is UNKNOWN, while the notification explicitly requires customer review.'),
    context('ctx-elb-commerce', 'evt-elb-recovered', accountIds.commerce, 'closed', '2026-11-05T08:20:00Z', '2026-11-05T11:47:00Z', null, ['OPERATIONS'],
      'AWS has closed this illustrative load balancer API event. Both observed load balancers are unimpaired. The independent operator verification task is still in progress.',
      { endTime: '2026-11-05T11:45:00Z' }),
    context('ctx-rds-billing', 'evt-rds-billing', accountIds.data, 'open', '2026-11-01T00:00:00Z', '2026-11-04T09:00:00Z', 'INFORMATIONAL', ['BILLING'],
      'Illustrative extended-support billing notice for warehouse-writer. The affected-entity status is absent in the source fixture. Absence is distinct from an explicit UNKNOWN status.'),
    context('ctx-oregon-development', 'evt-ec2-oregon', accountIds.development, 'open', '2026-11-05T13:02:00Z', '2026-11-05T13:18:00Z', null, ['OPERATIONS'],
      'Connectivity issues affect development runners in Oregon. The resource communication is incomplete: two of three reduced-size demonstration pages have been received. API reconciliation last succeeded at 12:10 UTC.',
      { sourceKind: 'EventBridge incomplete communication' })
  ];

  function resource(id, accountId, name, service, region, workload, owner, criticality, arn) {
    return { id, arn, accountId, name, service, region, workload, owner, criticality };
  }
  const resources = [
    resource('res-checkout-01', accountIds.commerce, 'checkout-api-01', 'EC2', 'eu-central-1', 'Checkout', 'SRE', 'critical', 'arn:aws:ec2:eu-central-1:111100001001:instance/i-0a111111111111111'),
    resource('res-checkout-02', accountIds.commerce, 'checkout-api-02', 'EC2', 'eu-central-1', 'Checkout', 'SRE', 'critical', 'arn:aws:ec2:eu-central-1:111100001001:instance/i-0a222222222222222'),
    resource('res-checkout-03', accountIds.commerce, 'checkout-api-03', 'EC2', 'eu-central-1', 'Checkout', 'SRE', 'critical', 'arn:aws:ec2:eu-central-1:111100001001:instance/i-0a333333333333333'),
    resource('res-edge-01', accountIds.shared, 'shared-edge-01', 'EC2', 'eu-central-1', 'Shared edge', 'Platform', 'high', 'arn:aws:ec2:eu-central-1:111100001004:instance/i-0b111111111111111'),
    resource('res-checkout-router', accountIds.commerce, 'checkout-router', 'LAMBDA', 'eu-west-1', 'Checkout', 'SRE', 'critical', 'arn:aws:lambda:eu-west-1:111100001001:function:demo-checkout-router'),
    resource('res-receipt-dispatch', accountIds.commerce, 'receipt-dispatch', 'LAMBDA', 'eu-west-1', 'Order notifications', 'SRE', 'medium', 'arn:aws:lambda:eu-west-1:111100001001:function:demo-receipt-dispatch'),
    resource('res-payment-webhook', accountIds.payments, 'payment-webhook', 'LAMBDA', 'eu-west-1', 'Payments', 'Payments', 'critical', 'arn:aws:lambda:eu-west-1:111100001002:function:demo-payment-webhook'),
    resource('res-payment-retry', accountIds.payments, 'payment-retry', 'LAMBDA', 'eu-west-1', 'Payments', 'Payments', 'critical', 'arn:aws:lambda:eu-west-1:111100001002:function:demo-payment-retry'),
    resource('res-order-simulator', accountIds.development, 'sandbox-order-simulator', 'LAMBDA', 'eu-west-1', 'Test orders', 'Developer Experience', 'low', 'arn:aws:lambda:eu-west-1:111100001005:function:demo-order-simulator'),
    resource('res-warehouse-writer', accountIds.data, 'warehouse-writer', 'RDS', 'us-east-1', 'Revenue analytics', 'Data', 'high', 'arn:aws:rds:us-east-1:111100001003:db:demo-warehouse-writer'),
    resource('res-warehouse-reader', accountIds.data, 'warehouse-reader', 'RDS', 'us-east-1', 'Revenue analytics', 'Data', 'high', 'arn:aws:rds:us-east-1:111100001003:db:demo-warehouse-reader'),
    resource('res-analytics-eks', accountIds.data, 'analytics-cluster', 'EKS', 'us-west-2', 'Analytics processing', 'Data', 'high', 'arn:aws:eks:us-west-2:111100001003:cluster/demo-analytics'),
    resource('res-development-eks', accountIds.development, 'development-cluster', 'EKS', 'us-west-2', 'Developer platform', 'Developer Experience', 'low', 'arn:aws:eks:us-west-2:111100001005:cluster/demo-development'),
    resource('res-payments-worker', accountIds.payments, 'payments-batch-worker', 'EC2', 'eu-west-1', 'Settlement', 'Payments', 'high', 'arn:aws:ec2:eu-west-1:111100001002:instance/i-0c111111111111111'),
    resource('res-audit-bucket', accountIds.shared, 'northstar-demo-audit-export', 'S3', 'eu-central-1', 'Audit exports', 'Security', 'high', 'arn:aws:s3:::northstar-demo-audit-export'),
    resource('res-checkout-alb', accountIds.commerce, 'checkout-alb', 'ELASTICLOADBALANCING', 'eu-west-1', 'Checkout', 'SRE', 'critical', 'arn:aws:elasticloadbalancing:eu-west-1:111100001001:loadbalancer/app/demo-checkout/50dc6c495c0c9188'),
    resource('res-catalog-alb', accountIds.commerce, 'catalog-alb', 'ELASTICLOADBALANCING', 'eu-west-1', 'Product catalog', 'SRE', 'high', 'arn:aws:elasticloadbalancing:eu-west-1:111100001001:loadbalancer/app/demo-catalog/50dc6c495c0c9222'),
    resource('res-dev-runner-01', accountIds.development, 'development-runner-01', 'EC2', 'us-west-2', 'CI runners', 'Developer Experience', 'low', 'arn:aws:ec2:us-west-2:111100001005:instance/i-0d111111111111111'),
    resource('res-dev-runner-02', accountIds.development, 'development-runner-02', 'EC2', 'us-west-2', 'CI runners', 'Developer Experience', 'low', 'arn:aws:ec2:us-west-2:111100001005:instance/i-0d222222222222222'),
    resource('res-session-cache', accountIds.commerce, 'checkout-session-cache', 'ELASTICACHE', 'eu-central-1', 'Checkout', 'SRE', 'high', 'arn:aws:elasticache:eu-central-1:111100001001:cluster:demo-session-cache')
  ];

  const eventById = Object.fromEntries(events.map(function (item) { return [item.id, item]; }));
  const contextById = Object.fromEntries(contexts.map(function (item) { return [item.id, item]; }));
  const resourceById = Object.fromEntries(resources.map(function (item) { return [item.id, item]; }));
  function impact(id, contextId, resourceId, statusCode, updatedAt, extra) {
    const ctx = contextById[contextId];
    const ev = eventById[ctx.eventId];
    const res = resourceId ? resourceById[resourceId] : null;
    return Object.assign({
      id, contextId,
      healthEntityArn: 'arn:aws:health:' + ev.region + ':' + ctx.accountId + ':entity/DEMO-' + id,
      entityValue: res ? res.arn : 'EC2_NETWORK_CONNECTIVITY_SCOPE',
      statusCode, updatedAt, resourceId: resourceId || null,
      kind: res ? 'resource' : 'scope_marker',
      metadata: res ? { matchMethod: 'exact_resource_arn', matchConfidence: 'confirmed' } : { impactExtent: 'Broad or unknown connectivity scope', matchMethod: 'unresolved', matchConfidence: 'unknown' }
    }, extra || {});
  }

  const entities = [
    impact('imp-network-checkout-01', 'ctx-network-commerce', 'res-checkout-01', 'IMPAIRED', '2026-11-05T13:26:00Z'),
    impact('imp-network-checkout-02', 'ctx-network-commerce', 'res-checkout-02', 'IMPAIRED', '2026-11-05T13:26:00Z'),
    impact('imp-network-checkout-03', 'ctx-network-commerce', 'res-checkout-03', 'UNIMPAIRED', '2026-11-05T13:26:00Z'),
    impact('imp-network-edge', 'ctx-network-shared', 'res-edge-01', 'IMPAIRED', '2026-11-05T13:26:00Z'),
    impact('imp-network-scope', 'ctx-network-shared', null, 'UNKNOWN', '2026-11-05T13:26:00Z'),
    impact('imp-lambda-router', 'ctx-lambda-commerce', 'res-checkout-router', 'PENDING', '2026-11-04T13:00:00Z'),
    impact('imp-lambda-receipt', 'ctx-lambda-commerce', 'res-receipt-dispatch', 'RESOLVED', '2026-11-04T13:00:00Z'),
    impact('imp-lambda-webhook', 'ctx-lambda-payments', 'res-payment-webhook', 'PENDING', '2026-11-04T13:00:00Z'),
    impact('imp-lambda-retry', 'ctx-lambda-payments', 'res-payment-retry', 'PENDING', '2026-11-04T13:00:00Z'),
    impact('imp-lambda-simulator', 'ctx-lambda-development', 'res-order-simulator', 'RESOLVED', '2026-11-04T13:00:00Z'),
    impact('imp-rds-writer', 'ctx-rds-maintenance', 'res-warehouse-writer', 'UNKNOWN', '2026-11-05T10:05:00Z'),
    impact('imp-rds-reader', 'ctx-rds-maintenance', 'res-warehouse-reader', 'UNKNOWN', '2026-11-05T10:05:00Z'),
    impact('imp-eks-analytics', 'ctx-eks-data', 'res-analytics-eks', 'PENDING', '2026-11-05T10:10:00Z'),
    impact('imp-eks-development', 'ctx-eks-development', 'res-development-eks', 'RESOLVED', '2026-11-05T10:10:00Z'),
    impact('imp-retirement-worker', 'ctx-retirement-payments', 'res-payments-worker', 'PENDING', '2026-11-05T08:00:00Z'),
    impact('imp-bucket-review', 'ctx-bucket-shared', 'res-audit-bucket', 'UNKNOWN', '2026-11-05T12:50:00Z'),
    impact('imp-elb-checkout', 'ctx-elb-commerce', 'res-checkout-alb', 'UNIMPAIRED', '2026-11-05T11:45:00Z'),
    impact('imp-elb-catalog', 'ctx-elb-commerce', 'res-catalog-alb', 'UNIMPAIRED', '2026-11-05T11:45:00Z'),
    impact('imp-rds-billing', 'ctx-rds-billing', 'res-warehouse-writer', null, '2026-11-04T09:00:00Z',
      { metadata: { matchMethod: 'exact_resource_arn', matchConfidence: 'confirmed', statusPresence: 'not_supplied', note: 'Same inventory database as imp-rds-writer; a different event-relative entity record.' } }),
    impact('imp-oregon-runner-01', 'ctx-oregon-development', 'res-dev-runner-01', 'IMPAIRED', '2026-11-05T13:18:00Z',
      { healthEntityArn: null, metadata: { matchMethod: 'exact_resource_arn', matchConfidence: 'confirmed', identitySource: 'event_bridge_entity_value', sourcePresence: 'Health entity ARN not supplied; API hydration pending.' } }),
    impact('imp-oregon-runner-02', 'ctx-oregon-development', 'res-dev-runner-02', 'UNKNOWN', '2026-11-05T13:18:00Z',
      { healthEntityArn: null, metadata: { matchMethod: 'exact_resource_arn', matchConfidence: 'confirmed', identitySource: 'event_bridge_entity_value', sourcePresence: 'Health entity ARN not supplied; API hydration pending.' } })
  ];

  const catalogEntries = [
    { id: 'catalog-lambda-legacy', service: 'LAMBDA', component: 'Lambda Python runtime', title: 'Python 3.11 runtime — illustrative timeline', version: 'python3.11', recommendedVersion: 'python3.13' },
    { id: 'catalog-lambda-current', service: 'LAMBDA', component: 'Lambda Python runtime', title: 'Python 3.13 runtime — demo catalog entry', version: 'python3.13', recommendedVersion: 'python3.13' },
    { id: 'catalog-rds-postgres', service: 'RDS', component: 'RDS PostgreSQL engine', title: 'PostgreSQL 14 — illustrative timeline', version: '14', recommendedVersion: '16' },
    { id: 'catalog-eks-kubernetes', service: 'EKS', component: 'EKS Kubernetes version', title: 'Kubernetes 1.34 — illustrative timeline', version: '1.34', recommendedVersion: '1.35' },
    { id: 'catalog-cache-redis', service: 'ELASTICACHE', component: 'ElastiCache Redis engine', title: 'Redis 6.2 — illustrative timeline', version: '6.2', recommendedVersion: '7.1' }
  ];
  const milestones = [
    { id: 'milestone-lambda-support', entryId: 'catalog-lambda-legacy', type: 'END_OF_SUPPORT', date: '2026-12-05T00:00:00Z', description: 'Fictional demonstration milestone: move matched Lambda functions to the recommended runtime before this date.', risks: ['END_OF_SUPPORT'], regions: ['all'] },
    { id: 'milestone-rds-support', entryId: 'catalog-rds-postgres', type: 'END_OF_SUPPORT', date: '2026-10-01T00:00:00Z', description: 'Fictional demonstration milestone: standard support has ended for matched engine deployments; review the illustrative extended-support exposure.', risks: ['END_OF_SUPPORT', 'BILLING'], regions: ['us-east-1', 'eu-west-1'] },
    { id: 'milestone-eks-support', entryId: 'catalog-eks-kubernetes', type: 'END_OF_SUPPORT', date: '2026-11-12T00:00:00Z', description: 'Fictional demonstration milestone: upgrade the matched cluster before the modeled support transition.', risks: ['END_OF_SUPPORT', 'BILLING'], regions: ['all'] },
    { id: 'milestone-cache-update', entryId: 'catalog-cache-redis', type: 'BLOCK_RESOURCE_UPDATE', date: '2027-02-01T00:00:00Z', description: 'Fictional demonstration milestone: updates to resources on this modeled version become restricted. This does not assert a present outage.', risks: ['AVAILABILITY'], regions: ['eu-central-1'] }
  ];
  const deployments = [
    { id: 'deployment-router', resourceId: 'res-checkout-router', component: 'Lambda Python runtime', version: 'python3.11', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-receipt', resourceId: 'res-receipt-dispatch', component: 'Lambda Python runtime', version: 'python3.13', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-webhook', resourceId: 'res-payment-webhook', component: 'Lambda Python runtime', version: 'python3.11', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-retry', resourceId: 'res-payment-retry', component: 'Lambda Python runtime', version: 'python3.11', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-simulator', resourceId: 'res-order-simulator', component: 'Lambda Python runtime', version: 'python3.13', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-writer', resourceId: 'res-warehouse-writer', component: 'RDS PostgreSQL engine', version: '14', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-reader', resourceId: 'res-warehouse-reader', component: 'RDS PostgreSQL engine', version: '14', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-analytics-eks', resourceId: 'res-analytics-eks', component: 'EKS Kubernetes version', version: '1.34', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' },
    { id: 'deployment-development-eks', resourceId: 'res-development-eks', component: 'EKS Kubernetes version', version: '1.35', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'unmatched' },
    { id: 'deployment-session-cache', resourceId: 'res-session-cache', component: 'ElastiCache Redis engine', version: '6.2', observedAt: '2026-11-05T12:00:00Z', matchStatus: 'matched' }
  ];
  const exposures = [
    { id: 'exposure-lambda-router', milestoneId: 'milestone-lambda-support', deploymentId: 'deployment-router', applicability: 'confirmed', reason: 'Observed service, runtime component, and exact version match; the milestone applies to all regions.', confidence: 'high' },
    { id: 'exposure-lambda-webhook', milestoneId: 'milestone-lambda-support', deploymentId: 'deployment-webhook', applicability: 'confirmed', reason: 'The 12:00 inventory scan still records python3.11. A later operator completion does not replace this inventory observation.', confidence: 'high' },
    { id: 'exposure-lambda-retry', milestoneId: 'milestone-lambda-support', deploymentId: 'deployment-retry', applicability: 'confirmed', reason: 'Observed service, runtime component, and exact version match; the milestone applies to all regions.', confidence: 'high' },
    { id: 'exposure-rds-writer', milestoneId: 'milestone-rds-support', deploymentId: 'deployment-writer', applicability: 'confirmed', reason: 'RDS PostgreSQL engine version 14 matches the catalog entry and the deployed region is included.', confidence: 'high' },
    { id: 'exposure-rds-reader', milestoneId: 'milestone-rds-support', deploymentId: 'deployment-reader', applicability: 'confirmed', reason: 'RDS PostgreSQL engine version 14 matches the catalog entry and the deployed region is included.', confidence: 'high' },
    { id: 'exposure-eks-analytics', milestoneId: 'milestone-eks-support', deploymentId: 'deployment-analytics-eks', applicability: 'confirmed', reason: 'The analytics cluster runs the exact modeled Kubernetes version and the milestone applies to all regions.', confidence: 'high' },
    { id: 'exposure-cache-proactive', milestoneId: 'milestone-cache-update', deploymentId: 'deployment-session-cache', applicability: 'confirmed', reason: 'Inventory matches the modeled Redis version and region. This proactive exposure has no associated Health event.', confidence: 'high' }
  ];

  function work(id, title, owner, state, priority, dueAt, updatedAt, text) {
    const actor = owner === 'Unassigned' ? 'Operations intake' : owner;
    return {
      id, title, owner, state, priority, dueAt, updatedAt,
      notes: text ? [{ id: id + '-note-1', at: updatedAt, actor, text }] : [],
      actions: [{ id: id + '-action-1', at: updatedAt, actor, type: state, fromState: 'new', toState: state, detail: text || 'Work item created in the fictional demo.' }]
    };
  }
  const workItems = [
    work('wi-ec2-network', 'Investigate checkout and edge connectivity', 'SRE', 'in_progress', 'critical', '2026-11-05T14:00:00Z', '2026-11-05T13:27:00Z', 'Traffic has been shifted away from the two impaired checkout instances. Platform is checking the shared edge path.'),
    work('wi-s3-public', 'Track the public S3 advisory', 'Data', 'acknowledged', 'high', '2026-11-05T13:45:00Z', '2026-11-05T13:24:00Z', 'Monitor ingestion retries. Public service exposure is relevant to our workload, but AWS has not reported account-specific impact here.'),
    work('wi-lambda-webhook', 'Upgrade the payment-webhook runtime', 'Payments', 'completed', 'high', '2026-12-01T17:00:00Z', '2026-11-05T13:20:00Z', 'Runtime upgrade deployed and smoke checks completed. Awaiting an AWS entity update and the next inventory scan; provider state remains PENDING.'),
    work('wi-rds-review', 'Review warehouse maintenance and failover', 'Data', 'new', 'medium', '2026-11-06T10:00:00Z', '2026-11-05T10:20:00Z', 'Confirm replica readiness and connection retry behavior before the fictional maintenance window.'),
    work('wi-eks-upgrade', 'Upgrade the analytics Kubernetes cluster', 'Data', 'in_progress', 'high', '2026-11-10T17:00:00Z', '2026-11-05T11:15:00Z', 'Add-on compatibility checks are complete. Schedule the cluster upgrade before the illustrative support milestone.'),
    work('wi-ec2-retirement', 'Prepare the payments worker replacement', 'Unassigned', 'new', 'high', '2026-11-06T07:00:00Z', '2026-11-05T08:15:00Z', 'Assign an owner to provision and validate replacement capacity.'),
    work('wi-bucket-review', 'Review audit-export bucket access', 'Security', 'new', 'high', '2026-11-05T16:00:00Z', '2026-11-05T12:55:00Z', 'Review the bucket policy and confirm that any public access is intended. No real bucket is accessed by this prototype.'),
    work('wi-elb-verify', 'Verify checkout recovery after the ELB event', 'SRE', 'in_progress', 'medium', '2026-11-05T15:00:00Z', '2026-11-05T12:05:00Z', 'AWS has closed the event. Continue application-level verification before completing this local work item.'),
    work('wi-oregon-feed', 'Reconcile the incomplete Oregon event', 'Platform', 'new', 'medium', '2026-11-05T14:00:00Z', '2026-11-05T13:22:00Z', 'Collect the missing communication page and refresh the stale regional API scope. Partial observations must remain visibly incomplete.')
  ];
  function target(id, workItemId, kind, targetId) {
    const record = { id, workItemId, contextId: null, impactId: null, exposureId: null };
    record[kind + 'Id'] = targetId;
    return record;
  }
  const workItemTargets = [
    target('target-network-commerce', 'wi-ec2-network', 'context', 'ctx-network-commerce'),
    target('target-network-shared', 'wi-ec2-network', 'context', 'ctx-network-shared'),
    target('target-public-watch', 'wi-s3-public', 'context', 'ctx-s3-public'),
    target('target-webhook', 'wi-lambda-webhook', 'impact', 'imp-lambda-webhook'),
    target('target-rds-review', 'wi-rds-review', 'context', 'ctx-rds-maintenance'),
    target('target-eks-upgrade', 'wi-eks-upgrade', 'exposure', 'exposure-eks-analytics'),
    target('target-retirement', 'wi-ec2-retirement', 'impact', 'imp-retirement-worker'),
    target('target-bucket', 'wi-bucket-review', 'impact', 'imp-bucket-review'),
    target('target-elb-verify', 'wi-elb-verify', 'context', 'ctx-elb-commerce'),
    target('target-oregon-feed', 'wi-oregon-feed', 'context', 'ctx-oregon-development')
  ];

  const coverage = [
    { id: 'coverage-frankfurt-api', accountId: null, region: 'eu-central-1', channel: 'API reconciliation', status: 'complete', lastSuccessAt: '2026-11-05T13:29:00Z', sourceUpdatedAt: '2026-11-05T13:26:00Z', eventId: null, pagesReceived: 1, totalPages: 1, reason: 'All requested event and entity pages were retrieved for this regional organization scope.' },
    { id: 'coverage-ireland-api', accountId: null, region: 'eu-west-1', channel: 'API reconciliation', status: 'complete', lastSuccessAt: '2026-11-05T13:28:00Z', sourceUpdatedAt: '2026-11-05T11:47:00Z', eventId: null, pagesReceived: 1, totalPages: 1, reason: 'The latest request completed. Older provider update times do not themselves mean collection is stale.' },
    { id: 'coverage-virginia-api', accountId: null, region: 'us-east-1', channel: 'API reconciliation', status: 'complete', lastSuccessAt: '2026-11-05T13:27:00Z', sourceUpdatedAt: '2026-11-05T13:21:00Z', eventId: null, pagesReceived: 1, totalPages: 1, reason: 'Account and public-event scope is configured. Public notifications remain separate from reported account impact.' },
    { id: 'coverage-oregon-api', accountId: null, region: 'us-west-2', channel: 'API reconciliation', status: 'stale', lastSuccessAt: '2026-11-05T12:10:00Z', sourceUpdatedAt: '2026-11-05T10:10:00Z', eventId: null, pagesReceived: null, totalPages: null, reason: 'No successful API reconciliation for 80 minutes at the frozen snapshot. The demo freshness policy is 15 minutes.' },
    { id: 'coverage-oregon-pages', accountId: accountIds.development, region: 'us-west-2', channel: 'EventBridge assembly', status: 'partial', lastSuccessAt: '2026-11-05T13:19:00Z', sourceUpdatedAt: '2026-11-05T13:18:00Z', eventId: 'evt-ec2-oregon', pagesReceived: 2, totalPages: 3, reason: 'Page 3 is missing. Resource rows intentionally represent a reduced-size pagination fixture; the known list is not an authoritative total.' }
  ];

  const updates = [
    { id: 'update-network-provider', eventId: 'evt-ec2-network', contextId: 'ctx-network-commerce', kind: 'aws', at: '2026-11-05T13:26:00Z', title: 'AWS updated the connectivity issue', body: 'Two checkout hosts remain impaired. A third is unimpaired. Account-specific entity evidence is retained separately from the organization summary.' },
    { id: 'update-network-operator', eventId: 'evt-ec2-network', contextId: 'ctx-network-commerce', kind: 'operator', at: '2026-11-05T13:27:00Z', title: 'SRE began mitigation', body: 'Traffic was shifted away from the two affected checkout hosts. The local work item is in progress; the AWS event remains open.' },
    { id: 'update-network-collection', eventId: 'evt-ec2-network', contextId: 'ctx-network-org', kind: 'collection', at: '2026-11-05T13:29:00Z', title: 'Frankfurt scope reconciled', body: 'The organization summary and account-specific details were refreshed without merging their contexts.' },
    { id: 'update-public-provider', eventId: 'evt-s3-public', contextId: 'ctx-s3-public', kind: 'aws', at: '2026-11-05T13:21:00Z', title: 'Public S3 advisory updated', body: 'The notification is public. Two notification-account contexts were observed, with no reported affected-account associations.' },
    { id: 'update-public-operator', eventId: 'evt-s3-public', contextId: 'ctx-s3-public', kind: 'operator', at: '2026-11-05T13:24:00Z', title: 'Data acknowledged the public advisory', body: 'The team is monitoring ingestion retries and workload exposure.' },
    { id: 'update-lambda-provider', eventId: 'evt-lambda-runtime', contextId: 'ctx-lambda-payments', kind: 'aws', at: '2026-11-04T13:00:00Z', title: 'AWS reported two pending payment functions', body: 'payment-webhook and payment-retry are PENDING in the latest provider snapshot.' },
    { id: 'update-lambda-operator', eventId: 'evt-lambda-runtime', contextId: 'ctx-lambda-payments', kind: 'operator', at: '2026-11-05T13:20:00Z', title: 'Payments completed the webhook upgrade', body: 'The local task is completed. Provider confirmation and inventory reconciliation are still outstanding.' },
    { id: 'update-rds-provider', eventId: 'evt-rds-maintenance', contextId: 'ctx-rds-maintenance', kind: 'aws', at: '2026-11-05T10:05:00Z', title: 'Maintenance window announced', body: 'The illustrative window begins on 7 November. Review is needed to determine application-specific actions.' },
    { id: 'update-eks-provider', eventId: 'evt-eks-support', contextId: 'ctx-eks-data', kind: 'aws', at: '2026-11-05T10:10:00Z', title: 'Analytics cluster remains pending', body: 'The development cluster is resolved, while the analytics cluster still needs an upgrade.' },
    { id: 'update-bucket-provider', eventId: 'evt-s3-access', contextId: 'ctx-bucket-shared', kind: 'aws', at: '2026-11-05T12:50:00Z', title: 'Bucket access review requested', body: 'Actionability is ACTION_REQUIRED. The affected-entity status remains UNKNOWN.' },
    { id: 'update-elb-provider', eventId: 'evt-elb-recovered', contextId: 'ctx-elb-commerce', kind: 'aws', at: '2026-11-05T11:47:00Z', title: 'AWS closed the load balancer event', body: 'Both affected load balancers are reported UNIMPAIRED.' },
    { id: 'update-elb-operator', eventId: 'evt-elb-recovered', contextId: 'ctx-elb-commerce', kind: 'operator', at: '2026-11-05T12:05:00Z', title: 'SRE continued recovery verification', body: 'Application checks remain in progress after provider closure.' },
    { id: 'update-billing-provider', eventId: 'evt-rds-billing', contextId: 'ctx-rds-billing', kind: 'aws', at: '2026-11-04T09:00:00Z', title: 'Illustrative billing notice received', body: 'The warehouse-writer appears in this event and the maintenance event. Its inventory resource identity is shared, while entity states are event-relative.' },
    { id: 'update-oregon-provider', eventId: 'evt-ec2-oregon', contextId: 'ctx-oregon-development', kind: 'aws', at: '2026-11-05T13:18:00Z', title: 'Oregon connectivity issue reported', body: 'One observed runner is impaired and another is UNKNOWN. The final resource page has not arrived.' },
    { id: 'update-oregon-collection', eventId: 'evt-ec2-oregon', contextId: 'ctx-oregon-development', kind: 'collection', at: '2026-11-05T13:19:00Z', title: 'Communication is incomplete', body: 'Two of three illustrative pages are present. Counts remain observed counts rather than a complete affected-resource total.' }
  ];

  const communications = [
    { id: 'comm-network-commerce', eventId: 'evt-ec2-network', contextId: 'ctx-network-commerce', notificationAccountId: accountIds.commerce, validatedBaseId: 'demo-network-1326', totalPages: 1, pagesReceived: 1, state: 'complete' },
    { id: 'comm-public-data', eventId: 'evt-s3-public', contextId: 'ctx-s3-public', notificationAccountId: accountIds.data, validatedBaseId: 'demo-public-1321', totalPages: 1, pagesReceived: 1, state: 'complete' },
    { id: 'comm-public-shared', eventId: 'evt-s3-public', contextId: 'ctx-s3-public', notificationAccountId: accountIds.shared, validatedBaseId: 'demo-public-1321', totalPages: 1, pagesReceived: 1, state: 'complete' },
    { id: 'comm-oregon-development', eventId: 'evt-ec2-oregon', contextId: 'ctx-oregon-development', notificationAccountId: accountIds.development, validatedBaseId: 'demo-oregon-1318', totalPages: 3, pagesReceived: 2, state: 'partial' }
  ];
  const communicationPages = [
    { id: 'page-network-1', communicationRecordId: 'comm-network-commerce', rawCommunicationId: 'demo-network-1326-1', page: 1, totalPages: 1 },
    { id: 'page-public-data-1', communicationRecordId: 'comm-public-data', rawCommunicationId: 'demo-public-1321-1', page: 1, totalPages: 1 },
    { id: 'page-public-shared-1', communicationRecordId: 'comm-public-shared', rawCommunicationId: 'demo-public-1321-1', page: 1, totalPages: 1 },
    { id: 'page-oregon-1', communicationRecordId: 'comm-oregon-development', rawCommunicationId: 'demo-oregon-1318-1', page: 1, totalPages: 3 },
    { id: 'page-oregon-2', communicationRecordId: 'comm-oregon-development', rawCommunicationId: 'demo-oregon-1318-2', page: 2, totalPages: 3 }
  ];
  const deliveries = [
    { id: 'delivery-network-primary', pageId: 'page-network-1', envelopeId: 'demo-envelope-network-primary', recipientAccountId: accountIds.shared, deliveryRegion: 'eu-central-1', backupEvent: false, sentAt: '2026-11-05T13:26:02Z', receivedAt: '2026-11-05T13:26:04Z' },
    { id: 'delivery-network-backup', pageId: 'page-network-1', envelopeId: 'demo-envelope-network-backup', recipientAccountId: accountIds.shared, deliveryRegion: 'us-west-2', backupEvent: true, sentAt: '2026-11-05T13:26:02Z', receivedAt: '2026-11-05T13:26:06Z' },
    { id: 'delivery-public-data', pageId: 'page-public-data-1', envelopeId: 'demo-envelope-public-data', recipientAccountId: accountIds.shared, deliveryRegion: 'us-east-1', backupEvent: false, sentAt: '2026-11-05T13:21:02Z', receivedAt: '2026-11-05T13:21:05Z' },
    { id: 'delivery-public-shared', pageId: 'page-public-shared-1', envelopeId: 'demo-envelope-public-shared', recipientAccountId: accountIds.shared, deliveryRegion: 'us-east-1', backupEvent: false, sentAt: '2026-11-05T13:21:02Z', receivedAt: '2026-11-05T13:21:06Z' },
    { id: 'delivery-oregon-1', pageId: 'page-oregon-1', envelopeId: 'demo-envelope-oregon-1', recipientAccountId: accountIds.shared, deliveryRegion: 'us-west-2', backupEvent: false, sentAt: '2026-11-05T13:18:02Z', receivedAt: '2026-11-05T13:18:05Z' },
    { id: 'delivery-oregon-2', pageId: 'page-oregon-2', envelopeId: 'demo-envelope-oregon-2', recipientAccountId: accountIds.shared, deliveryRegion: 'us-east-1', backupEvent: true, sentAt: '2026-11-05T13:18:02Z', receivedAt: '2026-11-05T13:19:00Z' }
  ];

  const data = {
    meta: {
      asOf,
      organization: { id: organizationId, name: 'Northstar Commerce' },
      scenarioLabel: 'Fictional operations snapshot · 5 November 2026',
      fixtureVersion: 1,
      allDataFictional: true,
      fictionNotice: 'All organization names, account IDs, resources, event ARNs, notices, and dates are fictional demonstration fixtures. Realistic service and version labels do not describe actual AWS events or support schedules.',
      lifecycleNotice: 'Illustrative lifecycle milestones only. Consult official AWS sources for actual version schedules.',
      paginationNotice: 'The incomplete notification is intentionally downscaled to a few representative rows to demonstrate page completeness. It does not claim these small messages reached an AWS payload-size limit.',
      sourceTitleNotice: 'Event titles and priority are locally authored presentation fields, not native AWS Health title or severity fields.',
      inventoryNotice: 'Inventory is a separate snapshot. Operator completion and an AWS entity update do not automatically rewrite an earlier inventory scan.',
      freshnessMinutes: 15,
      displayTimeZone: 'Europe/Zurich',
      orgHealthAccessStatus: 'ENABLED',
      delegatedAdministratorAccountId: accountIds.shared,
      regionLabels: { 'eu-central-1': 'Frankfurt', 'eu-west-1': 'Ireland', 'us-east-1': 'N. Virginia', 'us-west-2': 'Oregon' },
      baselineExpectedCounts: {
        events: 10, accounts: 5, regions: 4, contexts: 15,
        accountContexts: 13, publicContexts: 1, organizationSummaryContexts: 1,
        entities: 21, mappedEntityRecords: 20, distinctAffectedResources: 19, inventoryResources: 20,
        entityStatuses: { IMPAIRED: 4, UNIMPAIRED: 3, PENDING: 5, RESOLVED: 3, UNKNOWN: 5, NOT_SUPPLIED: 1 },
        eventStatuses: { open: 7, upcoming: 2, closed: 1 },
        activeIssueEvents: 3, publicEvents: 1, accountSpecificEvents: 9,
        confirmedLifecycleExposures: 7, unmatchedDeployments: 1,
        workItems: 9, workStates: { new: 4, acknowledged: 1, in_progress: 3, completed: 1, verified: 0 }
      }
    },
    accounts, events, contexts, entities, resources, workItems, workItemTargets,
    catalogEntries, milestones, deployments, exposures, coverage, updates,
    communications, communicationPages, deliveries,
    replay: {
      id: 'replay-webhook-confirmation',
      eventId: 'evt-lambda-runtime',
      contextId: 'ctx-lambda-payments',
      impactId: 'imp-lambda-webhook',
      newProviderStatus: 'RESOLVED',
      at: '2026-11-05T13:34:00Z',
      title: 'AWS confirmed the webhook runtime upgrade',
      body: 'payment-webhook is now reported RESOLVED. payment-retry remains PENDING, so the account event remains open. The local work item stays completed; inventory posture continues to reflect its earlier scan until a separate reconciliation.'
    }
  };

  root.HealthDemoData = data;
  if (typeof module !== 'undefined' && module.exports) module.exports = data;
})(typeof globalThis !== 'undefined' ? globalThis : this);
