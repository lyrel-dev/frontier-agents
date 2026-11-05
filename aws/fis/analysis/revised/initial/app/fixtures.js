/* Fictional AWS FIS scenarios. Dates are normalized ISO instants for the UI,
 * not a byte-for-byte REST response. All schedules, labels, telemetry and
 * assessments are mock/product data. Nothing in this file calls AWS. */
(function (root, factory) {
  const data = factory();
  if (typeof module === 'object' && module.exports) module.exports = data;
  else root.FISFixtures = data;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const region = 'eu-central-1';
  const orchestrator = '111122223333';
  const paymentsAccount = '444455556666';
  const inventoryAccount = '777788889999';
  const at = (base, seconds) => new Date(Date.parse(base) + seconds * 1000).toISOString();
  const arn = (service, account, resource) => `arn:aws:${service}:${region}:${account}:${resource}`;
  const role = (account) => `arn:aws:iam::${account}:role/FISGameDayExecution`;
  const accounts = [
    { accountId: paymentsAccount, roleArn: role(paymentsAccount), description: 'Checkout platform · production EU' },
    { accountId: inventoryAccount, roleArn: role(inventoryAccount), description: 'Inventory platform · production EU' }
  ];

  const catalog = {
    'aws:fis:wait': {
      id: 'aws:fis:wait', label: 'Wait', service: 'AWS FIS',
      description: 'A configured observation interval.',
      parameters: { duration: { description: 'Duration of the wait.', required: true } }, targets: {},
      source: 'https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html'
    },
    'aws:network:disrupt-connectivity': {
      id: 'aws:network:disrupt-connectivity', label: 'Disrupt connectivity', service: 'Amazon VPC',
      description: 'Disrupt connectivity for the selected subnets.',
      parameters: { duration: { description: 'Configured disruption interval.', required: true }, scope: { description: 'Connectivity scope.', required: true } },
      targets: { Subnets: { resourceType: 'aws:ec2:subnet' } },
      source: 'https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html'
    },
    'aws:rds:failover-db-cluster': {
      id: 'aws:rds:failover-db-cluster', label: 'Fail over DB cluster', service: 'Amazon RDS',
      description: 'Fail over the selected database cluster.', parameters: {},
      targets: { Clusters: { resourceType: 'aws:rds:cluster' } },
      source: 'https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html'
    },
    'aws:ec2:stop-instances': {
      id: 'aws:ec2:stop-instances', label: 'Stop instances', service: 'Amazon EC2',
      description: 'Stop selected instances with a configured restart post action.',
      parameters: { startInstancesAfterDuration: { description: 'Interval before restarting instances.', required: false } },
      targets: { Instances: { resourceType: 'aws:ec2:instance' } },
      source: 'https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html'
    },
    'aws:ebs:pause-volume-io': {
      id: 'aws:ebs:pause-volume-io', label: 'Pause volume I/O', service: 'Amazon EBS',
      description: 'Pause I/O for selected EBS volumes.',
      parameters: { duration: { description: 'Configured pause interval.', required: true } },
      targets: { Volumes: { resourceType: 'aws:ec2:ebs-volume' } },
      source: 'https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html'
    }
  };

  function action(actionId, description, parameters, startAfter, targets) {
    return { actionId, description, parameters: parameters || {}, startAfter: startAfter || [], targets: targets || {}, state: { status: 'pending', reason: 'Waiting for experiment preparation or predecessor actions.' } };
  }

  function telemetryPoints(base, anchors, step) {
    const points = [];
    const first = anchors[0][0];
    const last = anchors[anchors.length - 1][0];
    for (let t = first; t <= last; t += step || 15) {
      let i = 0;
      while (i < anchors.length - 2 && t > anchors[i + 1][0]) i++;
      const left = anchors[i]; const right = anchors[i + 1];
      const ratio = (t - left[0]) / (right[0] - left[0]);
      const value = left[1] + (right[1] - left[1]) * ratio;
      points.push({ offsetSeconds: t, value: Math.round(value * 100) / 100, observedAt: at(base, t + 4) });
    }
    return points;
  }

  function evidence(base, key, offset, source, type, message, extra) {
    return Object.assign({ id: `${key}-${type}-${offset}`, source, type, occurredAt: at(base, offset), observedAt: at(base, offset + (source === 'FIS logs' ? 8 : 2)), message }, extra || {});
  }

  function common(config) {
    const start = config.start;
    const reportBucket = 'example-fis-gameday-evidence';
    const expArn = arn('fis', orchestrator, `experiment/${config.id}`);
    const alarmArn = arn('cloudwatch', orchestrator, `alarm:${config.alarm || config.key + '-guardrail'}`);
    return {
      key: config.key, label: config.label, description: config.description,
      application: config.application, environment: config.environment || 'Production EU',
      owner: config.owner || 'Platform Resilience', region, synthetic: true,
      experiment: {
        id: config.id, arn: expArn, experimentTemplateId: config.templateId,
        creationTime: at(start, -8), startTime: start,
        state: { status: config.finalStatus || 'completed', reason: config.finalReason || 'Experiment completed.' },
        actions: {}, targets: {},
        experimentOptions: { accountTargeting: config.multi ? 'multi-account' : 'single-account', actionsMode: config.preview ? 'skip-all' : 'run-all', emptyTargetResolutionMode: 'fail' },
        targetAccountConfigurationsCount: config.multi ? accounts.length : 0,
        roleArn: role(orchestrator),
        stopConditions: [{ source: 'aws:cloudwatch:alarm', value: alarmArn }],
        logConfiguration: { logSchemaVersion: 2, cloudWatchLogsConfiguration: { logGroupArn: arn('logs', orchestrator, 'log-group:/aws/fis/gamedays') }, s3Configuration: { bucketName: reportBucket, prefix: 'logs/' } },
        experimentReportConfiguration: { dataSources: { cloudWatchDashboards: [{ dashboardIdentifier: `arn:aws:cloudwatch::${orchestrator}:dashboard/${config.application.replace(/\s/g, '')}-resilience` }] }, outputs: { s3Configuration: { bucketName: reportBucket, prefix: 'reports/' } }, preExperimentDuration: 'PT2M', postExperimentDuration: 'PT2M' },
        tags: { Name: config.label, Application: config.application, Environment: config.environment || 'Production EU', Owner: config.owner || 'Platform Resilience', GameDay: '2026-11-eu' }
      },
      accounts: config.multi ? JSON.parse(JSON.stringify(accounts)) : [],
      resolvedTargets: [],
      resolution: { status: 'completed', complete: true, observedAt: at(start, 14) },
      observation: { lastSuccessfulFetchAt: at(start, config.initial), hydrated: true, source: 'GetExperiment · mock fixture' },
      durationSeconds: config.duration, executionDurationSeconds: config.executionEnd,
      initialCursorSeconds: config.initial,
      safety: {
        source: 'CloudWatch observations · mock telemetry', alarmArn,
        alarmState: 'OK', observedAt: at(start, 0),
        history: [{ alarmState: 'OK', occurredAt: at(start, -30), observedAt: at(start, -27) }],
        lever: { id: 'default', status: 'disengaged', reason: 'Game day window open.', accountId: orchestrator, region, observedAt: at(start, 0), source: 'GetSafetyLever · mock fixture' }
      },
      evidence: [
        evidence(start, config.key, 0, 'CloudTrail', 'StartExperiment', 'Experiment requested by resilience-operator@example.invalid.', { actor: 'resilience-operator@example.invalid' }),
        evidence(start, config.key, 1, 'EventBridge', 'experiment-state-change', 'Experiment moved from initiating to running.'),
        evidence(start, config.key, 8, 'FIS logs', 'target-resolution-end', 'Configured selectors resolved; membership records collected.')
      ],
      _mock: {
        clockOrigin: start, pollIntervalSeconds: 5, resolutionEndedAt: 8, resolutionCompleteAt: 14,
        finalStatus: config.finalStatus || 'completed', finalReason: config.finalReason || 'Experiment completed.',
        executionEnd: config.executionEnd,
        report: config.preview ? { kind: 'not_generated' } : { kind: 'completed', runningAt: config.executionEnd + 120, completedAt: config.executionEnd + 150, artifacts: [{ arn: `arn:aws:s3:::${reportBucket}/reports/${config.id}/experiment-report.pdf`, reportType: 'PDF' }] },
        assessmentAvailableAt: config.executionEnd + 120
      }
    };
  }

  const checkout = common({
    key: 'checkout-az', label: 'Checkout · zonal isolation',
    description: 'Exercise the checkout fallback path while isolating payment and inventory subnets in one Availability Zone.',
    application: 'Checkout', id: 'EXP9kLm2nPq4Rs6TuV8', templateId: 'EXT2aBc4dEf6gHi8jKl',
    start: '2026-11-05T09:00:00.000Z', multi: true, initial: 230, executionEnd: 520, duration: 760,
    alarm: 'checkout-p95-latency-high'
  });
  checkout.experiment.actions = {
    establishBaseline: action('aws:fis:wait', 'Capture a steady-state observation window', { duration: 'PT30S' }),
    isolatePayments: action('aws:network:disrupt-connectivity', 'Isolate checkout subnets in euc1-az2', { scope: 'availability-zone', duration: 'PT5M' }, ['establishBaseline'], { Subnets: 'checkoutAz' }),
    isolateInventory: action('aws:network:disrupt-connectivity', 'Isolate inventory subnets in the same AZ', { scope: 'availability-zone', duration: 'PT5M' }, ['establishBaseline'], { Subnets: 'inventoryAz' }),
    observeRecovery: action('aws:fis:wait', 'Observe checkout recovery after fault removal', { duration: 'PT2M' }, ['isolatePayments', 'isolateInventory'])
  };
  checkout.experiment.targets = {
    checkoutAz: { resourceType: 'aws:ec2:subnet', resourceTags: { FISCheckoutScope: 'true' }, parameters: { availabilityZoneIdentifier: 'euc1-az2' }, selectionMode: 'ALL' },
    inventoryAz: { resourceType: 'aws:ec2:subnet', resourceTags: { FISInventoryScope: 'true' }, parameters: { availabilityZoneIdentifier: 'euc1-az2' }, selectionMode: 'ALL' }
  };
  checkout.resolvedTargets = [
    { targetName: 'checkoutAz', resourceType: 'aws:ec2:subnet', targetInformation: { arn: arn('ec2', paymentsAccount, 'subnet/subnet-0a111111111111111') } },
    { targetName: 'checkoutAz', resourceType: 'aws:ec2:subnet', targetInformation: { arn: arn('ec2', paymentsAccount, 'subnet/subnet-0b222222222222222') } },
    { targetName: 'checkoutAz', resourceType: 'aws:ec2:subnet', targetInformation: { arn: arn('ec2', inventoryAccount, 'subnet/subnet-0c333333333333333') } },
    { targetName: 'inventoryAz', resourceType: 'aws:ec2:subnet', targetInformation: { arn: arn('ec2', inventoryAccount, 'subnet/subnet-0c333333333333333') } },
    { targetName: 'inventoryAz', resourceType: 'aws:ec2:subnet', targetInformation: { arn: arn('ec2', inventoryAccount, 'subnet/subnet-0d444444444444444') } }
  ];
  checkout.schedule = [
    { name: 'establishBaseline', start: 20, end: 50, outcome: 'completed' },
    { name: 'isolatePayments', start: 55, end: 355, outcome: 'completed' },
    { name: 'isolateInventory', start: 80, end: 380, outcome: 'completed' },
    { name: 'observeRecovery', start: 395, end: 515, outcome: 'completed' }
  ];
  checkout.telemetry = {
    metricLabel: 'Checkout latency · p95', unit: 'ms', threshold: 400, baseline: 128,
    criteria: 'p95 stays below 400 ms and returns below 180 ms for 60 seconds within 180 seconds of fault removal.',
    metricBinding: { namespace: 'Example/Checkout', metricName: 'RequestLatency', statistic: 'p95', period: 15, dimensions: { Environment: 'production-eu', Route: '/checkout' } },
    points: telemetryPoints(checkout.experiment.startTime, [[-120, 128], [0, 132], [45, 130], [90, 275], [165, 338], [240, 312], [330, 352], [390, 290], [435, 174], [495, 151], [600, 132], [750, 129]])
  };
  checkout.assessment = { status: 'passed', summary: 'Latency stayed within budget; the 60-second recovery window met the criterion.', rule: 'checkout-latency-v3', evidence: ['CloudWatch fixture: Checkout/RequestLatency p95', 'Recovery window 09:07:15–09:08:15 UTC'], recoverySeconds: 55 };
  checkout._mock.assessmentAvailableAt = 605;
  checkout.evidence.push(
    evidence(checkout.experiment.startTime, checkout.key, 20, 'FIS logs', 'action-start', 'Steady-state observation started.', { actionName: 'establishBaseline' }),
    evidence(checkout.experiment.startTime, checkout.key, 50, 'FIS logs', 'action-end', 'Baseline observation completed.', { actionName: 'establishBaseline' }),
    evidence(checkout.experiment.startTime, checkout.key, 55, 'FIS logs', 'action-start', 'Connectivity disruption initiated for checkoutAz.', { actionName: 'isolatePayments' }),
    evidence(checkout.experiment.startTime, checkout.key, 80, 'FIS logs', 'action-start', 'Connectivity disruption initiated for inventoryAz.', { actionName: 'isolateInventory' }),
    evidence(checkout.experiment.startTime, checkout.key, 210, 'CloudWatch', 'metric-observation', 'Latest p95 sample is below the 400 ms guardrail.'),
    evidence(checkout.experiment.startTime, checkout.key, 355, 'FIS logs', 'action-end', 'Checkout connectivity action completed.', { actionName: 'isolatePayments' }),
    evidence(checkout.experiment.startTime, checkout.key, 380, 'FIS logs', 'action-end', 'Inventory connectivity action completed.', { actionName: 'isolateInventory' }),
    evidence(checkout.experiment.startTime, checkout.key, 395, 'FIS logs', 'action-start', 'Post-fault recovery observation started.', { actionName: 'observeRecovery' }),
    evidence(checkout.experiment.startTime, checkout.key, 520, 'EventBridge', 'experiment-state-change', 'Experiment moved from running to completed.'),
    evidence(checkout.experiment.startTime, checkout.key, 605, 'Assessment', 'criterion-evaluated', 'Version 3 of the checkout latency criterion passed.')
  );

  const rds = common({
    key: 'rds-failover', label: 'Orders · Aurora writer failover',
    description: 'Verify that order writes return to steady state within the recovery objective after an Aurora writer failover.',
    application: 'Orders API', id: 'EXP3xYz5aBc7dEf9gHi', templateId: 'EXT7jKl9mNo1pQr3sTu',
    start: '2026-11-04T14:30:00.000Z', initial: 500, executionEnd: 290, duration: 540,
    alarm: 'orders-db-connection-errors'
  });
  rds.experiment.actions = {
    establishBaseline: action('aws:fis:wait', 'Capture pre-failover connection behavior', { duration: 'PT30S' }),
    failoverWriter: action('aws:rds:failover-db-cluster', 'Fail over the orders Aurora writer', {}, ['establishBaseline'], { Clusters: 'ordersCluster' }),
    observeRecovery: action('aws:fis:wait', 'Observe order write latency', { duration: 'PT3M' }, ['failoverWriter'])
  };
  rds.experiment.targets = { ordersCluster: { resourceType: 'aws:rds:cluster', resourceArns: [arn('rds', orchestrator, 'cluster:orders-eu-primary')], selectionMode: 'ALL' } };
  rds.resolvedTargets = [{ targetName: 'ordersCluster', resourceType: 'aws:rds:cluster', targetInformation: { arn: arn('rds', orchestrator, 'cluster:orders-eu-primary') } }];
  rds.schedule = [
    { name: 'establishBaseline', start: 10, end: 40, outcome: 'completed' },
    { name: 'failoverWriter', start: 45, end: 95, outcome: 'completed' },
    { name: 'observeRecovery', start: 100, end: 280, outcome: 'completed' }
  ];
  rds.telemetry = {
    metricLabel: 'Order writes · p95', unit: 'ms', threshold: 200, baseline: 86,
    criteria: 'Return below 200 ms for 60 seconds within 90 seconds of failover completion.',
    metricBinding: { namespace: 'Example/Orders', metricName: 'WriteLatency', statistic: 'p95', period: 15, dimensions: { Environment: 'production-eu' } },
    points: telemetryPoints(rds.experiment.startTime, [[-120, 86], [0, 89], [30, 88], [60, 880], [95, 720], [150, 490], [210, 275], [240, 185], [300, 120], [420, 93], [540, 86]])
  };
  rds.assessment = { status: 'failed', summary: 'AWS execution completed, but recovery took 145 seconds against a 90-second objective.', rule: 'orders-recovery-v2', evidence: ['CloudWatch fixture: Orders/WriteLatency p95', 'First qualifying window starts at 14:34:00 UTC'], recoverySeconds: 145, recoveryBudgetSeconds: 90 };
  rds._mock.assessmentAvailableAt = 365;
  rds.evidence.push(
    evidence(rds.experiment.startTime, rds.key, 45, 'FIS logs', 'action-start', 'Aurora failover action initiated.', { actionName: 'failoverWriter' }),
    evidence(rds.experiment.startTime, rds.key, 95, 'FIS logs', 'action-end', 'Aurora failover action completed.', { actionName: 'failoverWriter' }),
    evidence(rds.experiment.startTime, rds.key, 185, 'CloudWatch', 'metric-observation', 'Order write latency remains above 200 ms at the recovery deadline.'),
    evidence(rds.experiment.startTime, rds.key, 290, 'EventBridge', 'experiment-state-change', 'Experiment completed with all three actions completed.'),
    evidence(rds.experiment.startTime, rds.key, 365, 'Assessment', 'criterion-evaluated', 'Recovery criterion failed: 145 s observed, 90 s allowed.')
  );

  const stopped = common({
    key: 'alarm-stop', label: 'Payments · alarm-triggered stop',
    description: 'Exercise payment worker interruption under an error-rate guardrail and observe restart post-actions.',
    application: 'Payments', id: 'EXP5rSt7uVw9xYz1aBc', templateId: 'EXT8dEf0gHi2jKl4mNo',
    start: '2026-11-04T11:00:00.000Z', initial: 250, executionEnd: 215, duration: 420,
    finalStatus: 'stopped', finalReason: 'Experiment stopped following the payments error-rate stop condition.', alarm: 'payments-5xx-rate-high'
  });
  stopped.experiment.actions = {
    establishBaseline: action('aws:fis:wait', 'Observe payment traffic before stopping workers', { duration: 'PT25S' }),
    stopPaymentNodes: action('aws:ec2:stop-instances', 'Stop payment workers with a restart post action', { startInstancesAfterDuration: 'PT5M' }, ['establishBaseline'], { Instances: 'paymentWorkers' }),
    observeRecovery: action('aws:fis:wait', 'Observe recovery after workers restart', { duration: 'PT2M' }, ['stopPaymentNodes']),
    validateSteadyState: action('aws:fis:wait', 'Capture a final steady-state interval', { duration: 'PT1M' }, ['observeRecovery'])
  };
  stopped.experiment.targets = { paymentWorkers: { resourceType: 'aws:ec2:instance', resourceTags: { Service: 'payments', FaultInjection: 'enabled' }, selectionMode: 'COUNT(2)' } };
  stopped.resolvedTargets = ['i-0e555555555555555', 'i-0f666666666666666'].map(id => ({ targetName: 'paymentWorkers', resourceType: 'aws:ec2:instance', targetInformation: { arn: arn('ec2', orchestrator, `instance/${id}`) } }));
  stopped.schedule = [
    { name: 'establishBaseline', start: 10, end: 35, outcome: 'completed' },
    { name: 'stopPaymentNodes', start: 40, end: 208, plannedEnd: 340, stoppingAt: 168, outcome: 'stopped', reason: 'Stopped after the restart post action finished.' },
    { name: 'observeRecovery', start: null, end: 168, outcome: 'cancelled', reason: 'Experiment stopped before this action started.' },
    { name: 'validateSteadyState', start: null, end: 168, outcome: 'cancelled', reason: 'Experiment stopped before this action started.' }
  ];
  stopped._mock.stoppingAt = 168;
  stopped._mock.assessmentAvailableAt = 230;
  stopped.stopCause = { type: 'alarm', label: 'payments-5xx-rate-high', evidenceId: 'alarm-stop-alarm-state-change-166', source: 'CloudWatch alarm observation', confidence: 'observed' };
  stopped.safety.history.push({ alarmState: 'ALARM', occurredAt: at(stopped.experiment.startTime, 166), observedAt: at(stopped.experiment.startTime, 168) }, { alarmState: 'OK', occurredAt: at(stopped.experiment.startTime, 300), observedAt: at(stopped.experiment.startTime, 303) });
  stopped.telemetry = {
    metricLabel: 'Payment errors · 5xx', unit: '%', threshold: 2, baseline: 0.3,
    criteria: 'Payment 5xx error rate remains below 2% in the configured 60-second window.',
    metricBinding: { namespace: 'Example/Payments', metricName: 'ErrorRate', statistic: 'Average', period: 15, dimensions: { Environment: 'production-eu' } },
    points: telemetryPoints(stopped.experiment.startTime, [[-120, 0.3], [0, 0.2], [45, 0.4], [90, 2.4], [135, 4.8], [165, 6.8], [210, 3.2], [240, 1.1], [300, 0.4], [420, 0.3]])
  };
  stopped.assessment = { status: 'failed', summary: 'The error-rate objective was breached. Later recovery samples do not erase that breach.', rule: 'payments-error-rate-v4', evidence: ['CloudWatch alarm payments-5xx-rate-high', 'Error-rate series exceeded the 2% objective'], peakValue: 6.8 };
  stopped.evidence.push(
    evidence(stopped.experiment.startTime, stopped.key, 40, 'FIS logs', 'action-start', 'Instance stop action initiated.', { actionName: 'stopPaymentNodes' }),
    evidence(stopped.experiment.startTime, stopped.key, 166, 'CloudWatch', 'alarm-state-change', 'payments-5xx-rate-high entered ALARM.'),
    evidence(stopped.experiment.startTime, stopped.key, 168, 'EventBridge', 'experiment-state-change', 'Experiment moved from running to stopping.'),
    evidence(stopped.experiment.startTime, stopped.key, 185, 'CloudTrail', 'StartInstances', 'FIS requested instance restarts as the configured post action.', { actionName: 'stopPaymentNodes' }),
    evidence(stopped.experiment.startTime, stopped.key, 208, 'FIS logs', 'action-end', 'Instance action stopped after restart post-action processing.', { actionName: 'stopPaymentNodes' }),
    evidence(stopped.experiment.startTime, stopped.key, 215, 'EventBridge', 'experiment-state-change', 'Experiment reached stopped.'),
    evidence(stopped.experiment.startTime, stopped.key, 230, 'Assessment', 'criterion-evaluated', 'Error-rate criterion failed; workload recovery is observed separately.')
  );

  const failed = common({
    key: 'ebs-permission', label: 'Inventory · cross-account I/O pause',
    description: 'Pause selected inventory EBS volumes across target accounts and observe storage recovery.',
    application: 'Inventory', id: 'EXP6bCd8eFg0hIj2kLm', templateId: 'EXT9nOp1qRs3tUv5wXy',
    start: '2026-11-03T16:15:00.000Z', multi: true, initial: 220, executionEnd: 55, duration: 240,
    finalStatus: 'failed', finalReason: 'Pause volume I/O failed in a target account.'
  });
  failed.experiment.actions = {
    establishBaseline: action('aws:fis:wait', 'Observe the inventory storage baseline', { duration: 'PT20S' }),
    pauseVolumeIo: action('aws:ebs:pause-volume-io', 'Pause selected inventory EBS volumes', { duration: 'PT3M' }, ['establishBaseline'], { Volumes: 'inventoryVolumes' }),
    observeRecovery: action('aws:fis:wait', 'Observe I/O recovery', { duration: 'PT1M' }, ['pauseVolumeIo'])
  };
  failed.experiment.targets = { inventoryVolumes: { resourceType: 'aws:ec2:ebs-volume', resourceTags: { Service: 'inventory', FaultInjection: 'enabled' }, selectionMode: 'ALL' } };
  failed.resolvedTargets = [paymentsAccount, inventoryAccount].map((account, i) => ({ targetName: 'inventoryVolumes', resourceType: 'aws:ec2:ebs-volume', targetInformation: { arn: arn('ec2', account, `volume/vol-0${i + 1}777777777777777`) } }));
  failed.schedule = [
    { name: 'establishBaseline', start: 10, end: 30, outcome: 'completed' },
    { name: 'pauseVolumeIo', start: 35, end: 48, outcome: 'failed', reason: 'Target role in account 777788889999 is not authorized for ec2:PauseVolumeIO.' },
    { name: 'observeRecovery', start: null, end: 50, outcome: 'cancelled', reason: 'Experiment failed before this action started.' }
  ];
  failed._mock.error = { accountId: inventoryAccount, code: 'AuthorizationFailure', location: 'actions.pauseVolumeIo' };
  failed._mock.assessmentAvailableAt = 65;
  failed._mock.report = { kind: 'failed', runningAt: 175, completedAt: 195, error: { code: 'AccessDenied' }, reason: 'The mock reporting role could not write to the configured S3 prefix.' };
  failed.telemetry = {
    metricLabel: 'Inventory storage latency · p95', unit: 'ms', threshold: 80, baseline: 12,
    criteria: 'Evaluate storage recovery only when execution evidence establishes the intended fault ran.',
    metricBinding: { namespace: 'Example/Inventory', metricName: 'StorageLatency', statistic: 'p95', period: 15, dimensions: { Environment: 'production-eu' } },
    points: telemetryPoints(failed.experiment.startTime, [[-120, 12], [0, 13], [45, 14], [90, 12], [150, 13], [240, 12]])
  };
  failed.assessment = { status: 'inconclusive', summary: 'Action execution failed. A quiet metric series does not demonstrate resilience to the intended fault.', rule: 'inventory-io-recovery-v1', evidence: ['FIS action-error in account 777788889999', 'Incomplete evidence of intended fault execution'] };
  failed.evidence.push(
    evidence(failed.experiment.startTime, failed.key, 35, 'FIS logs', 'action-start', 'Pause volume I/O action initiated.', { actionName: 'pauseVolumeIo' }),
    evidence(failed.experiment.startTime, failed.key, 48, 'FIS logs', 'action-error', 'Access denied for ec2:PauseVolumeIO in inventory target account.', { actionName: 'pauseVolumeIo', accountId: inventoryAccount }),
    evidence(failed.experiment.startTime, failed.key, 55, 'EventBridge', 'experiment-state-change', 'Experiment moved from running to failed.'),
    evidence(failed.experiment.startTime, failed.key, 195, 'GetExperiment', 'report-state-observed', 'Report generation was observed failed; execution outcome remains failed independently.')
  );

  const preview = common({
    key: 'target-preview', label: 'Fulfillment · target preview',
    description: 'Inspect selected workers and volumes before a future game day. All fault actions are skipped.',
    application: 'Fulfillment', id: 'EXP7cDe9fGh1iJk3lMn', templateId: 'EXT0oPq2rSt4uVw6xYz',
    start: '2026-11-05T08:40:00.000Z', multi: true, preview: true, initial: 35, executionEnd: 22, duration: 60
  });
  preview.experiment.actions = {
    establishBaseline: action('aws:fis:wait', 'Configured baseline observation', { duration: 'PT30S' }),
    pauseVolumes: action('aws:ebs:pause-volume-io', 'Configured fulfillment I/O pause', { duration: 'PT2M' }, ['establishBaseline'], { Volumes: 'previewVolumes' }),
    stopWorkers: action('aws:ec2:stop-instances', 'Configured worker stop and restart', { startInstancesAfterDuration: 'PT3M' }, ['establishBaseline'], { Instances: 'previewWorkers' })
  };
  preview.experiment.targets = {
    previewVolumes: { resourceType: 'aws:ec2:ebs-volume', resourceTags: { Service: 'fulfillment' }, selectionMode: 'COUNT(2)' },
    previewWorkers: { resourceType: 'aws:ec2:instance', resourceTags: { Service: 'fulfillment' }, selectionMode: 'COUNT(2)' }
  };
  preview.resolvedTargets = [
    { targetName: 'previewVolumes', resourceType: 'aws:ec2:ebs-volume', targetInformation: { arn: arn('ec2', paymentsAccount, 'volume/vol-0a888888888888888') } },
    { targetName: 'previewVolumes', resourceType: 'aws:ec2:ebs-volume', targetInformation: { arn: arn('ec2', inventoryAccount, 'volume/vol-0b999999999999999') } },
    { targetName: 'previewWorkers', resourceType: 'aws:ec2:instance', targetInformation: { arn: arn('ec2', paymentsAccount, 'instance/i-0caaaaaaaaaaaaaaa') } },
    { targetName: 'previewWorkers', resourceType: 'aws:ec2:instance', targetInformation: { arn: arn('ec2', inventoryAccount, 'instance/i-0dbbbbbbbbbbbbbbb') } }
  ];
  preview.schedule = Object.keys(preview.experiment.actions).map(name => ({ name, start: null, end: 20, outcome: 'skipped', reason: 'Action skipped because actionsMode is skip-all.' }));
  preview.telemetry = { metricLabel: 'No workload assessment', unit: 'ms', threshold: null, baseline: null, points: [], criteria: 'Target previews validate selection, not fault execution permissions or workload resilience.' };
  preview.assessment = { status: 'not_assessed', summary: 'Target selection preview only. No faults were executed and no resilience verdict is assigned.', rule: null, evidence: [] };
  preview._mock.assessmentAvailableAt = 0;
  preview.evidence.push(
    evidence(preview.experiment.startTime, preview.key, 20, 'FIS logs', 'action-end', 'All configured actions skipped for the target preview.'),
    evidence(preview.experiment.startTime, preview.key, 22, 'EventBridge', 'experiment-state-change', 'Preview experiment completed. A later run may select different resources.')
  );

  const runs = [checkout, rds, stopped, failed, preview];
  runs.forEach(run => {
    run.experiment.endTime = at(run.experiment.startTime, run._mock.executionEnd);
    run.evidence.sort((a, b) => Date.parse(a.observedAt) - Date.parse(b.observedAt));
  });
  return {
    runs, catalog, accounts,
    metadata: {
      synthetic: true, version: '1.0', region, orchestratorAccountId: orchestrator,
      description: 'Fictional demonstration fixtures; no AWS API, credentials, billing or live resource operations.',
      timestampConvention: 'ISO 8601 UTC instants after application normalization.',
      scheduleConvention: 'schedule and _mock are replay-only configuration, not FIS response fields.',
      reportTypeConvention: 'PDF is a mock artifact type; the API reportType field is open-ended.'
    }
  };
}));
