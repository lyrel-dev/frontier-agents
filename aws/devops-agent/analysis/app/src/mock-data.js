/* Fictional investigation fixture. Native envelopes and application metadata are separate.
 * No value in this file was collected from an AWS account. The demo.* record profiles
 * are application examples, not AWS-published schemas. See ../../report.md. */
(function (root, factory) {
  const data = factory();
  if (typeof module === 'object' && module.exports) module.exports = data;
  if (root) root.DemoData = data;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const iso = time => '2026-11-05T' + time + 'Z';
  const seconds = time => Date.parse(iso(time)) / 1000;
  const primary = 'inv-checkout-1105';
  const ledger = 'inv-ledger-1105';
  const supplier = 'inv-supplier-1105';
  const scopes = [
    { key: 'aws|111122223333|eu-central-1|a19085e2-1925-4c2a-bbee-30c3d54831d1', partition: 'aws', accountId: '111122223333', region: 'eu-central-1', agentSpaceId: 'a19085e2-1925-4c2a-bbee-30c3d54831d1', name: 'Commerce production' },
    { key: 'aws|444455556666|eu-west-1|b4836a21-5aec-4b44-91fb-13954b41a1b6', partition: 'aws', accountId: '444455556666', region: 'eu-west-1', agentSpaceId: 'b4836a21-5aec-4b44-91fb-13954b41a1b6', name: 'Partner services' }
  ];
  const scopeFor = taskId => taskId === supplier ? scopes[1] : scopes[0];
  const scenario = {
    id: 'northstar-checkout-2026-11-05', version: '1.1.0', primaryTaskId: primary,
    primaryInvestigationKey: scopes[0].key + '|task|' + encodeURIComponent(primary),
    organization: 'Northstar Commerce', timezone: 'Europe/Zurich',
    disclaimer: 'Fictional demonstration data. All incidents, accounts, people, resources and observations are synthetic. No AWS connection.',
    stages: [
      { id: 'investigating', title: 'Investigating', description: 'Checkout latency is elevated. The collector has one unfinished journal query.', at: iso('14:12:30') },
      { id: 'evidence', title: 'Evidence correlated', description: 'A configuration change and connection waits support the agent’s published finding. A candidate summary is available.', at: iso('14:17:20') },
      { id: 'completed-pending', title: 'Completed · result pending', description: 'The task is completed. Its completion event names a summary record that has not been retrieved yet.', at: iso('14:21:00') },
      { id: 'result-retrieved', title: 'Result retrieved', description: 'The exact referenced summary and remaining journal page are collected. A historical checkpoint is retained.', at: iso('14:21:12') },
      { id: 'resumed', title: 'Investigation resumed', description: 'An operator asks for recovery validation after a deployment rollback. The same investigation has a new execution.', at: iso('14:26:10') },
      { id: 'follow-up-complete', title: 'Follow-up complete', description: 'A later summary reports observed recovery. The earlier completed snapshot remains unchanged.', at: iso('14:33:00') }
    ]
  };
  const taskMetadata = [
    { taskId: primary, scopeKey: scopes[0].key, profile: 'checkout', code: 'INC-4721', service: 'Checkout API', owner: 'Maya Chen · Commerce SRE', region: 'eu-central-1', accountId: scopes[0].accountId, spaceName: scopes[0].name, description: 'Increased checkout latency after the afternoon application release. Correlate the change, logs and database observations.' },
    { taskId: ledger, scopeKey: scopes[0].key, profile: 'ledger', code: 'INC-4718', service: 'Ledger workers', owner: 'Jonas Weber · Data platform', region: 'eu-central-1', accountId: scopes[0].accountId, spaceName: scopes[0].name, description: 'A completed investigation into worker retries following an Aurora failover. No known collection gaps remain for the observed execution journal queries.' },
    { taskId: supplier, scopeKey: scopes[1].key, profile: 'supplier', code: 'INC-4720', service: 'Supplier gateway', owner: 'Amira Patel · Partner SRE', region: 'eu-west-1', accountId: scopes[1].accountId, spaceName: scopes[1].name, description: 'A timed-out investigation with an inaccessible external log source. The available evidence does not establish a root cause.' }
  ];
  const taskBase = {
    [primary]: { agentSpaceId: scopes[0].agentSpaceId, taskId: primary, executionId: 'run-checkout-root', title: 'Checkout latency after release v2.18.4', description: taskMetadata[0].description, taskType: 'INVESTIGATION', priority: 'CRITICAL', createdAt: iso('14:08:10'), reference: { system: 'PagerDuty', referenceId: 'INC-4721', referenceUrl: 'https://northstar.example.invalid/incidents/INC-4721', associationId: 'assoc-pagerduty-demo', title: 'Checkout p95 above 1.5 s' }, metadata: { demoProfile: 'northstar.incident.v1', environment: 'production' } },
    [ledger]: { agentSpaceId: scopes[0].agentSpaceId, taskId: ledger, executionId: 'run-root', title: 'Ledger worker retries during database failover', description: taskMetadata[1].description, taskType: 'INVESTIGATION', priority: 'HIGH', createdAt: iso('12:18:04') },
    [supplier]: { agentSpaceId: scopes[1].agentSpaceId, taskId: supplier, executionId: 'run-root', title: 'Supplier gateway TLS errors', description: taskMetadata[2].description, taskType: 'INVESTIGATION', priority: 'MEDIUM', createdAt: iso('13:30:00') }
  };
  const taskObservation = (id, from, taskId, status, version, updated, observed, reason) => ({
    id, from, scopeKey: scopeFor(taskId).key, observedAt: iso(observed || updated),
    raw: Object.assign({}, taskBase[taskId], { status, version, updatedAt: iso(updated) }, reason ? { statusReason: reason } : {})
  });
  const taskObservations = [
    taskObservation('task-checkout-v4', 0, primary, 'IN_PROGRESS', 4, '14:12:10', '14:12:28'),
    taskObservation('task-checkout-v7', 1, primary, 'IN_PROGRESS', 7, '14:17:00', '14:17:18'),
    taskObservation('task-checkout-v9', 2, primary, 'COMPLETED', 9, '14:20:58', '14:20:59'),
    taskObservation('task-checkout-v10', 4, primary, 'IN_PROGRESS', 10, '14:25:45', '14:26:08'),
    taskObservation('task-checkout-v13', 5, primary, 'COMPLETED', 13, '14:32:50', '14:32:58'),
    taskObservation('task-ledger-v8', 0, ledger, 'COMPLETED', 8, '12:41:30', '12:42:00'),
    taskObservation('task-supplier-v6', 0, supplier, 'TIMED_OUT', 6, '13:50:00', '13:50:12', 'Investigation time budget exhausted; external log access remained unavailable.')
  ];
  const executionLabels = {
    'run-checkout-root': 'Incident coordinator', 'run-checkout-change': 'Deployment analysis',
    'run-checkout-logs': 'Application logs', 'run-checkout-db': 'Database signals',
    'run-checkout-followup': 'Recovery validation', 'run-root': 'Incident coordinator',
    'run-ledger-db': 'Failover analysis', 'run-supplier-logs': 'External log collection'
  };
  const execution = (id, from, taskId, executionId, parent, status, created, updated, subTask, agentType) => ({
    id, from, scopeKey: scopeFor(taskId).key,
    observedAt: iso(taskId === ledger ? '12:42:01' : taskId === supplier ? '13:50:13' : ({ 0: '14:12:21', 1: '14:17:10', 2: '14:20:59', 4: '14:26:05', 5: '14:32:58' })[from]),
    raw: Object.assign({ agentSpaceId: scopeFor(taskId).agentSpaceId, executionId, agentSubTask: subTask, agentType: agentType || 'demo.investigator', executionStatus: status, createdAt: seconds(created), updatedAt: seconds(updated) }, parent ? { parentExecutionId: parent } : {})
  });
  const executionObservations = [
    execution('exec-checkout-root-1', 0, primary, 'run-checkout-root', null, 'RUNNING', '14:08:12', '14:12:20', 'Investigate checkout latency and publish supported findings.'),
    execution('exec-checkout-change-1', 0, primary, 'run-checkout-change', 'run-checkout-root', 'STOPPED', '14:09:00', '14:11:30', 'Inspect the release and configuration changes.', 'demo.change-analysis'),
    execution('exec-checkout-logs-1', 0, primary, 'run-checkout-logs', 'run-checkout-root', 'RUNNING', '14:09:05', '14:12:15', 'Correlate application errors and connection waits.', 'demo.log-analysis'),
    execution('exec-checkout-db-1', 1, primary, 'run-checkout-db', 'run-checkout-root', 'STOPPED', '14:12:40', '14:16:45', 'Compare database saturation with connection-pool behavior.', 'demo.metric-analysis'),
    execution('exec-checkout-root-2', 2, primary, 'run-checkout-root', null, 'STOPPED', '14:08:12', '14:20:58', 'Investigate checkout latency and publish supported findings.'),
    execution('exec-checkout-logs-2', 2, primary, 'run-checkout-logs', 'run-checkout-root', 'STOPPED', '14:09:05', '14:19:50', 'Correlate application errors and connection waits.', 'demo.log-analysis'),
    execution('exec-checkout-followup-1', 4, primary, 'run-checkout-followup', 'run-checkout-root', 'RUNNING', '14:25:46', '14:26:04', 'Validate recovery after the operator’s deployment rollback.', 'demo.recovery-validation'),
    execution('exec-checkout-followup-2', 5, primary, 'run-checkout-followup', 'run-checkout-root', 'STOPPED', '14:25:46', '14:32:50', 'Validate recovery after the operator’s deployment rollback.', 'demo.recovery-validation'),
    execution('exec-ledger-root-1', 0, ledger, 'run-root', null, 'STOPPED', '12:18:10', '12:41:30', 'Investigate ledger retries during failover.'),
    execution('exec-ledger-db-1', 0, ledger, 'run-ledger-db', 'run-root', 'STOPPED', '12:19:00', '12:38:00', 'Inspect Aurora failover and worker reconnections.', 'demo.database-analysis'),
    execution('exec-supplier-root-1', 0, supplier, 'run-root', null, 'TIMED_OUT', '13:30:05', '13:50:00', 'Investigate supplier TLS errors with available evidence.'),
    execution('exec-supplier-logs-1', 0, supplier, 'run-supplier-logs', 'run-root', 'FAILED', '13:31:00', '13:34:20', 'Retrieve external gateway logs.', 'demo.log-analysis')
  ];
  const membership = (taskId, executionId, from, at) => ({ taskId, executionId, scopeKey: scopeFor(taskId).key, from, observedAt: iso(at), operation: 'ListExecutions', query: { agentSpaceId: scopeFor(taskId).agentSpaceId, taskId } });
  const memberships = [
    membership(primary, 'run-checkout-root', 0, '14:08:12'), membership(primary, 'run-checkout-change', 0, '14:09:02'), membership(primary, 'run-checkout-logs', 0, '14:09:07'), membership(primary, 'run-checkout-db', 1, '14:12:41'), membership(primary, 'run-checkout-followup', 4, '14:25:47'),
    membership(ledger, 'run-root', 0, '12:18:11'), membership(ledger, 'run-ledger-db', 0, '12:19:01'), membership(supplier, 'run-root', 0, '13:30:06'), membership(supplier, 'run-supplier-logs', 0, '13:31:01')
  ];
  const record = (id, from, taskId, executionId, recordId, type, created, observed, content, title, userReference) => ({
    id, from, scopeKey: scopeFor(taskId).key, observedAt: iso(observed), title,
    raw: Object.assign({ agentSpaceId: scopeFor(taskId).agentSpaceId, executionId, recordId, recordType: type, createdAt: seconds(created), content }, userReference ? { userReference } : {})
  });
  const initialLatency = [
    ['13:58:00', 182], ['14:00:00', 190], ['14:02:00', 206], ['14:04:00', 740], ['14:06:00', 1510], ['14:08:00', 1840], ['14:10:00', 2190], ['14:12:00', 2320]
  ].map(([at, value]) => ({ at: iso(at), value }));
  const laterLatency = [['14:14:00', 2280], ['14:16:00', 2180]].map(([at, value]) => ({ at: iso(at), value }));
  const recoveryLatency = [['14:24:00', 2230], ['14:26:00', 880], ['14:28:00', 310], ['14:30:00', 205], ['14:32:00', 194]].map(([at, value]) => ({ at: iso(at), value }));
  const finalSummary = '# Checkout latency investigation\n\n## Published finding\nThe agent reports that release v2.18.4 reduced the checkout service connection-pool cap from 96 to 24. Requests waited for a database connection while database CPU and freeable memory stayed within the observed baseline.\n\n## Supporting observations\n- Checkout p95 increased from approximately 190 ms to 2,320 ms after the 14:02 UTC deployment.\n- Application logs show a 1,240 ms connection-acquisition wait.\n- The deployment configuration diff supplies the changed pool limit.\n- Database CPU was 31%; this observation does not support CPU saturation as the explanation.\n\n## Recommended next step\nHave the operator evaluate restoring the previous pool limit through the deployment workflow, then collect a fresh recovery window.\n\nThis result records an agent-reported cause. It does not itself establish that remediation ran or that the incident recovered.';
  const followupSummary = '# Recovery validation\n\nThe operator’s deployment workflow restored the pool limit to 96 at 14:24 UTC. Fresh telemetry collected through 14:32 UTC shows checkout p95 at 194 ms and connection-acquisition waits at 18 ms.\n\nThe agent reports recovery within this observed window. The original investigation summary remains retained in the earlier snapshot. Continue normal service monitoring; this result does not establish future availability.';
  const journalRecords = [
    record('jr-checkout-alarm', 0, primary, 'run-checkout-root', 'rec-001', 'demo.alarm.v1', '14:08:15', '14:08:18', { alarmName: 'checkout-p95-above-1500ms', state: 'ALARM', occurredAt: iso('14:08:00'), resource: 'checkout-api', threshold: 1500, unit: 'ms', statistic: 'p95' }, 'Checkout latency alarm'),
    record('jr-checkout-plan', 0, primary, 'run-checkout-root', 'rec-002', 'demo.plan.v1', '14:09:00', '14:09:03', { steps: ['Inspect recent deployments', 'Correlate application waits', 'Check database signals'], note: 'Published plan in a fictional payload profile; no private reasoning is modeled.' }, 'Published investigation plan'),
    record('jr-checkout-deploy', 0, primary, 'run-checkout-change', 'rec-001', 'demo.change.v1', '14:10:10', '14:10:14', { resource: 'checkout-api', deploymentId: 'deploy-8e61-demo', version: '2.18.4', occurredAt: iso('14:02:00'), change: { setting: 'DB_POOL_MAX', before: 96, after: 24 }, repository: 'northstar/checkout-demo', commit: 'e42a91d-demo' }, 'Deployment configuration diff'),
    record('jr-checkout-latency', 0, primary, 'run-checkout-logs', 'rec-001', 'demo.metric.v1', '14:12:05', '14:12:24', { resource: 'checkout-api', metric: 'request_duration', statistic: 'p95', unit: 'ms', query: 'Demo CloudWatch request_duration, service=checkout-api, p95, 120s buckets', window: { from: iso('13:58:00'), to: iso('14:12:00') }, points: initialLatency }, 'Checkout p95 latency samples'),
    record('jr-checkout-wait', 0, primary, 'run-checkout-logs', 'rec-002', 'demo.log.v1', '14:12:10', '14:12:25', { occurredAt: iso('14:11:48'), resource: 'checkout-api', message: 'Connection acquire exceeded 1000 ms', poolMax: 24, waitMs: 1240, requestId: 'req-7c98-demo', traceId: 'trace-df14-demo' }, 'Connection acquisition wait'),
    record('jr-checkout-attachment', 0, primary, 'run-checkout-root', 'rec-003', 'demo.artifact_ref.v1', '14:11:00', '14:11:05', { assetId: 'asset-checkout-runbook', path: 'checkout-recovery.md', relationship: 'Referenced attachment; the application separately retrieved version 3. This does not prove a consumed version.' }, 'Runbook attachment reference'),
    record('jr-checkout-db', 1, primary, 'run-checkout-db', 'rec-001', 'demo.database_observation.v1', '14:16:30', '14:17:05', { occurredAt: iso('14:16:00'), resource: 'orders-primary', cpuPercent: 31, freeableMemoryGiB: 21.6, databaseConnections: 124, maxConnections: 2000, conclusion: 'No database CPU or connection-limit saturation in the observed sample.' }, 'Database capacity observation'),
    record('jr-checkout-latency-2', 1, primary, 'run-checkout-logs', 'rec-003', 'demo.metric.v1', '14:16:40', '14:17:06', { resource: 'checkout-api', metric: 'request_duration', statistic: 'p95', unit: 'ms', query: 'Demo CloudWatch request_duration, service=checkout-api, p95, 120s buckets', window: { from: iso('14:14:00'), to: iso('14:16:00') }, points: laterLatency }, 'Later checkout latency samples'),
    record('jr-checkout-finding', 1, primary, 'run-checkout-root', 'rec-004', 'demo.finding.v1', '14:17:00', '14:17:09', { title: 'Reduced application pool limit is the leading explanation', assertionOrigin: 'agent-reported', disposition: 'supported', statement: 'The smaller pool is reported to cause application connection waits. Database saturation is not supported by the observed CPU and connection sample.', evidence: [{ executionId: 'run-checkout-change', recordId: 'rec-001', locator: '/content/change' }, { executionId: 'run-checkout-logs', recordId: 'rec-002', locator: '/content/waitMs' }, { executionId: 'run-checkout-db', recordId: 'rec-001', locator: '/content/cpuPercent' }] }, 'Agent-reported pool contention finding'),
    record('jr-checkout-trace-ref', 1, primary, 'run-checkout-root', 'rec-005', 'demo.artifact_ref.v1', '14:17:02', '14:17:10', { uri: 's3://northstar-demo-observability/checkout/2026-11-05/trace-bundle.json', mediaType: 'application/json', title: 'Detailed trace bundle' }, 'Trace bundle reference'),
    record('jr-checkout-draft', 1, primary, 'run-checkout-root', 'summary-draft-01', 'investigation_summary_md', '14:17:05', '14:17:12', '# Preliminary investigation summary\n\nConnection pool contention is the leading explanation. This is an observed candidate summary; no completion pointer selects it.', 'Preliminary summary candidate'),
    record('jr-checkout-final', 3, primary, 'run-checkout-root', 'summary-final-02', 'investigation_summary_md', '14:20:55', '14:21:08', finalSummary, 'Referenced investigation summary'),
    record('jr-checkout-newer-candidate', 3, primary, 'run-checkout-root', 'summary-note-03', 'investigation_summary_md', '14:20:57', '14:21:08', '# Supplemental summary note\n\nThis later record is a candidate of the same type. The completion event selects summary-final-02, so timestamp order does not make this the authoritative result.', 'Later unselected summary candidate'),
    record('jr-checkout-unknown', 3, primary, 'run-checkout-logs', 'rec-future', 'demo.future_profile.v9', '14:09:15', '14:21:05', ['opaque-vendor-content', 3, { futureField: true }], 'Unrecognized record retained from the final page'),
    record('jr-checkout-operator', 4, primary, 'run-checkout-followup', 'rec-001', 'demo.operator_message.v1', '14:25:47', '14:25:48', { occurredAt: iso('14:25:45'), text: 'The deployment pipeline has restored v2.18.3. Please validate checkout latency and connection waits for the next observation window.', author: 'Maya Chen', actionOwner: 'Operator deployment workflow' }, 'Operator requests recovery validation', { userId: 'demo-maya-chen', userType: 'IDC' }),
    record('jr-checkout-followup-plan', 4, primary, 'run-checkout-followup', 'rec-002', 'demo.plan.v1', '14:26:00', '14:26:05', { steps: ['Read the deployed configuration', 'Collect a fresh latency window', 'Compare connection waits'], note: 'The operator performed the deployment. This execution only validates observed recovery.' }, 'Recovery validation started'),
    record('jr-checkout-recovery', 5, primary, 'run-checkout-followup', 'rec-003', 'demo.recovery_observation.v1', '14:32:20', '14:32:25', { occurredAt: iso('14:32:00'), resource: 'checkout-api', deployment: { version: '2.18.3', poolMax: 96, changedAt: iso('14:24:00'), owner: 'Operator deployment workflow' }, connectionWaitMs: 18, metric: 'request_duration', statistic: 'p95', unit: 'ms', query: 'Demo CloudWatch request_duration, service=checkout-api, p95, 120s buckets', window: { from: iso('14:24:00'), to: iso('14:32:00') }, points: recoveryLatency, conclusion: 'Recovery observed within the collected window.' }, 'Fresh recovery observations'),
    record('jr-checkout-followup-summary', 5, primary, 'run-checkout-followup', 'summary-followup-01', 'investigation_summary_md', '14:32:45', '14:32:55', followupSummary, 'Referenced follow-up summary'),
    record('jr-ledger-alarm', 0, ledger, 'run-root', 'rec-001', 'demo.alarm.v1', '12:18:15', '12:18:18', { occurredAt: iso('12:17:00'), resource: 'ledger-workers', retryRatePercent: 8.4, threshold: 2, unit: '%' }, 'Ledger retry alarm'),
    record('jr-ledger-failover', 0, ledger, 'run-ledger-db', 'rec-001', 'demo.database_observation.v1', '12:31:00', '12:31:06', { occurredAt: iso('12:16:40'), resource: 'ledger-aurora', event: 'Writer failover', oldWriter: 'ledger-writer-a', newWriter: 'ledger-writer-b', reconnectSeconds: 37, metric: 'worker_retry_rate', statistic: 'Percentage per observation window', unit: '%', window: { from: iso('12:14:00'), to: iso('12:30:00') }, query: 'Demo RDS event and worker retry sample', points: [['12:14:00', 0.2], ['12:18:00', 8.4], ['12:22:00', 3.1], ['12:26:00', 0.4], ['12:30:00', 0.2]].map(([at, value]) => ({ at: iso(at), value })) }, 'Failover and retry correlation'),
    record('jr-ledger-summary', 0, ledger, 'run-root', 'summary-ledger-01', 'investigation_summary_md', '12:41:20', '12:42:08', '# Ledger retry investigation\n\nThe agent reports a short retry burst during a writer failover. Worker reconnections took 37 seconds. The collected retry sample returned to 0.2% by 12:30 UTC.\n\nThe operator should review connection retry backoff. These historical observations do not establish the current health of the database.', 'Referenced ledger investigation summary'),
    record('jr-supplier-alarm', 0, supplier, 'run-root', 'rec-001', 'demo.alarm.v1', '13:30:20', '13:30:25', { occurredAt: iso('13:29:00'), resource: 'supplier-gateway', error: 'TLS handshake failures', sampleCount: 38, windowMinutes: 5 }, 'Supplier TLS failure sample'),
    record('jr-supplier-denied', 0, supplier, 'run-supplier-logs', 'rec-001', 'demo.collection_error.v1', '13:34:20', '13:34:24', { integration: 'Partner log archive', operation: 'read_logs', status: 'access_denied', missingEvidence: 'Gateway-side TLS diagnostics', retryableAfterAccessRepair: true }, 'External log access denied'),
    record('jr-supplier-scalar', 0, supplier, 'run-root', 'rec-future', 'demo.opaque_signal.v2', '13:36:00', '13:36:04', null, 'Unknown record with JSON null content')
  ];
  const completion = (id, from, taskId, executionId, recordId, at, observed) => {
    const s = scopeFor(taskId);
    return { id, from, scopeKey: s.key, observedAt: iso(observed), raw: {
      version: '0', id: ({ 'event-checkout-completed': '10000000-0000-4000-8000-000000000001', 'event-checkout-followup': '10000000-0000-4000-8000-000000000002', 'event-ledger-completed': '10000000-0000-4000-8000-000000000003' })[id], 'detail-type': 'Investigation Completed', source: 'aws.aidevops', account: s.accountId, time: iso(at), region: s.region,
      resources: ['arn:aws:aidevops:' + s.region + ':' + s.accountId + ':agentspace/' + s.agentSpaceId],
      detail: { version: '1.0.0', metadata: { agent_space_id: s.agentSpaceId, task_id: taskId, execution_id: executionId }, data: { task_type: 'INVESTIGATION', priority: taskBase[taskId].priority, status: 'COMPLETED', created_at: taskBase[taskId].createdAt, updated_at: iso(at), summary_record_id: recordId } }
    } };
  };
  const lifecycleEvents = [
    completion('event-checkout-completed', 2, primary, 'run-checkout-root', 'summary-final-02', '14:20:58', '14:20:59'),
    completion('event-checkout-followup', 5, primary, 'run-checkout-followup', 'summary-followup-01', '14:32:50', '14:32:56'),
    completion('event-ledger-completed', 0, ledger, 'run-root', 'summary-ledger-01', '12:41:30', '12:41:32')
  ];
  const runbook = '# Checkout recovery checklist\n\n1. Confirm the release and configuration diff against the approved deployment.\n2. Have the operator evaluate restoring the previous connection-pool configuration.\n3. Use the deployment pipeline and its change controls.\n4. Collect fresh request latency and connection-wait observations.\n5. Record the validation window and remaining gaps.\n\nDemo attachment, retrieved at version 3. Its reference does not prove the agent consumed this version.';
  const runbookV4 = runbook + '\n\nPost-release note: review application connection capacity against the expected request load.';
  const assetObservations = [
    { id: 'asset-checkout-runbook-v3', from: 0, scopeKey: scopes[0].key, observedAt: iso('14:11:08'), raw: { assetId: 'asset-checkout-runbook', assetType: 'attachment', metadata: { title: 'Checkout recovery checklist', filename: 'checkout-recovery.md', extension: 'md', size: new TextEncoder().encode(runbook).length }, version: 3, createdAt: seconds('09:00:00'), updatedAt: seconds('11:30:00') } },
    { id: 'asset-checkout-runbook-v4', from: 4, scopeKey: scopes[0].key, observedAt: iso('14:26:00'), raw: { assetId: 'asset-checkout-runbook', assetType: 'attachment', metadata: { title: 'Checkout recovery checklist', filename: 'checkout-recovery.md', extension: 'md', size: new TextEncoder().encode(runbookV4).length, change: 'Added a post-release capacity note.' }, version: 4, createdAt: seconds('09:00:00'), updatedAt: seconds('14:25:00') } }
  ];
  const assetFiles = [
    { id: 'file-checkout-runbook-v3', from: 0, scopeKey: scopes[0].key, assetId: 'asset-checkout-runbook', observedAt: iso('14:11:09'), raw: { path: 'checkout-recovery.md', content: { text: runbook }, version: 3, createdAt: seconds('09:00:00'), updatedAt: seconds('11:30:00') } }
  ];
  const timeline = (id, from, taskId, title, body, category, at, refs, origin, executionId) => ({ id, from, taskId, scopeKey: scopeFor(taskId).key, title, body, category, occurredAt: iso(at), sourceRefs: refs, origin: origin || 'Published evidence', executionId: executionId || null });
  const timelineDefinitions = [
    timeline('tl-checkout-deploy', 0, primary, 'Release v2.18.4 deployed', 'The captured configuration diff changes DB_POOL_MAX from 96 to 24.', 'evidence', '14:02:00', ['jr-checkout-deploy'], 'Observed change', 'run-checkout-change'),
    timeline('tl-checkout-alarm', 0, primary, 'Checkout latency alarm opened', 'The p95 threshold of 1,500 ms was breached.', 'evidence', '14:08:00', ['jr-checkout-alarm'], 'Observed telemetry', 'run-checkout-root'),
    timeline('tl-checkout-start', 0, primary, 'Investigation created', 'The work item starts gathering deployment, log and database evidence.', 'lifecycle', '14:08:10', ['task-checkout-v4'], 'Native task field'),
    timeline('tl-checkout-plan', 0, primary, 'Investigation plan published', 'Inspect the release, correlate connection waits, then check database signals.', 'agent', '14:09:00', ['jr-checkout-plan'], 'Agent-published content', 'run-checkout-root'),
    timeline('tl-checkout-wait', 0, primary, 'Connection acquisition waited 1.24 s', 'An application log reports a pool maximum of 24.', 'evidence', '14:11:48', ['jr-checkout-wait'], 'Observed log', 'run-checkout-logs'),
    timeline('tl-checkout-db', 1, primary, 'Database saturation not supported', 'Observed database CPU is 31%, with 124 of 2,000 connections in use.', 'evidence', '14:16:00', ['jr-checkout-db'], 'Observed telemetry', 'run-checkout-db'),
    timeline('tl-checkout-finding', 1, primary, 'Pool contention reported as leading cause', 'The published finding links the configuration reduction with request waits.', 'agent', '14:17:00', ['jr-checkout-finding'], 'Agent-reported assertion', 'run-checkout-root'),
    timeline('tl-checkout-completed', 2, primary, 'Task completed; summary reference received', 'The event selects summary-final-02. Its content is not yet in the collected records.', 'lifecycle', '14:20:58', ['event-checkout-completed'], 'Native lifecycle notification'),
    timeline('tl-checkout-retrieved', 3, primary, 'Exact summary and remaining page retrieved', 'The selected summary is now available; a newer candidate remains unselected.', 'collection', '14:21:08', ['jr-checkout-final', 'jr-checkout-unknown'], 'Application collection observation'),
    timeline('tl-checkout-resumed', 4, primary, 'Operator resumes the investigation', 'Maya asks for validation after a rollback performed through the deployment pipeline.', 'conversation', '14:25:45', ['jr-checkout-operator'], 'Attributed operator message', 'run-checkout-followup'),
    timeline('tl-checkout-recovery', 5, primary, 'Recovery observed in fresh telemetry', 'p95 is 194 ms and connection waits are 18 ms in the collected recovery window.', 'evidence', '14:32:00', ['jr-checkout-recovery'], 'Observed telemetry', 'run-checkout-followup'),
    timeline('tl-checkout-followup-complete', 5, primary, 'Follow-up result completed', 'A second exact summary is retained without replacing the earlier snapshot.', 'lifecycle', '14:32:50', ['event-checkout-followup'], 'Native lifecycle notification'),
    timeline('tl-ledger-failover', 0, ledger, 'Aurora writer failed over', 'The captured event names a writer change; worker reconnections took 37 seconds.', 'evidence', '12:16:40', ['jr-ledger-failover'], 'Observed event', 'run-ledger-db'),
    timeline('tl-ledger-alarm', 0, ledger, 'Worker retry alarm opened', 'The observed retry rate reached 8.4%.', 'evidence', '12:17:00', ['jr-ledger-alarm'], 'Observed telemetry', 'run-root'),
    timeline('tl-ledger-result', 0, ledger, 'Investigation result collected', 'The exact summary reports a short retry burst and recommends reviewing backoff.', 'collection', '12:42:08', ['jr-ledger-summary'], 'Application collection observation'),
    timeline('tl-supplier-alert', 0, supplier, 'Gateway TLS failures observed', '38 handshake failures were reported in a five-minute sample.', 'evidence', '13:29:00', ['jr-supplier-alarm'], 'Observed telemetry', 'run-root'),
    timeline('tl-supplier-denied', 0, supplier, 'External log retrieval denied', 'Gateway-side diagnostics are unavailable to this collection scope.', 'collection', '13:34:20', ['jr-supplier-denied'], 'Collection error', 'run-supplier-logs'),
    timeline('tl-supplier-timeout', 0, supplier, 'Investigation timed out', 'The task stopped without enough evidence to establish a cause.', 'lifecycle', '13:50:00', ['task-supplier-v6'], 'Native task field')
  ];
  const findingDefinitions = [
    { id: 'finding-checkout-waits', from: 0, taskId: primary, title: 'Connection waits coincide with latency', summary: 'A 1,240 ms acquisition wait was observed after the release. The causal explanation is still being investigated.', disposition: 'Under investigation', origin: 'Observed evidence', sourceRefs: ['jr-checkout-wait', 'jr-checkout-latency'] },
    { id: 'finding-checkout-pool', from: 1, taskId: primary, title: 'Pool limit reduction is the leading explanation', summary: 'The agent reports that lowering DB_POOL_MAX from 96 to 24 produced application-side contention. Database saturation is not supported by the collected sample.', disposition: 'Agent-reported cause', origin: 'Agent-reported assertion', sourceRefs: ['jr-checkout-finding', 'jr-checkout-deploy', 'jr-checkout-wait', 'jr-checkout-db'] },
    { id: 'finding-checkout-recovery', from: 5, taskId: primary, title: 'Recovery observed after the operator’s rollback', summary: 'The collected recovery window shows p95 of 194 ms and connection waits of 18 ms after the pool was restored to 96.', disposition: 'Observed recovery window', origin: 'Observed telemetry', sourceRefs: ['jr-checkout-recovery'] },
    { id: 'finding-ledger', from: 0, taskId: ledger, title: 'Retry burst reported during writer failover', summary: 'The agent links the failover with a short worker reconnect interval. The observed retry rate returned to 0.2%.', disposition: 'Agent-reported cause', origin: 'Agent-reported assertion', sourceRefs: ['jr-ledger-summary', 'jr-ledger-failover'] },
    { id: 'finding-supplier', from: 0, taskId: supplier, title: 'Cause remains undetermined', summary: 'TLS failures are observed, but the inaccessible gateway log source prevents evaluating the server-side explanation.', disposition: 'Insufficient evidence', origin: 'Application coverage assessment', sourceRefs: ['jr-supplier-alarm', 'jr-supplier-denied'] }
  ];
  const node = (id, from, taskId, label, subtitle, kind, origin, refs) => ({ id, from, taskId, scopeKey: scopeFor(taskId).key, label, subtitle, kind, origin, sourceRefs: refs });
  const graphNodes = [
    node('change-release', 0, primary, 'Release v2.18.4', 'Deployment at 14:02 UTC', 'change', 'Observed change', ['jr-checkout-deploy']),
    node('resource-checkout', 0, primary, 'Checkout API', 'Observed p95: 2,320 ms', 'resource', 'Observed telemetry', ['jr-checkout-latency']),
    node('observation-wait', 0, primary, 'Connection waits', '1,240 ms acquisition wait', 'observation', 'Observed log', ['jr-checkout-wait']),
    node('observation-pool', 1, primary, 'Pool limit: 24', 'Previous limit: 96', 'observation', 'Observed change', ['jr-checkout-deploy']),
    node('resource-orders', 1, primary, 'Orders database', '31% CPU · 124 connections', 'resource', 'Observed telemetry', ['jr-checkout-db']),
    node('hypothesis-contention', 1, primary, 'Application pool contention', 'Agent-reported cause', 'hypothesis', 'Agent-reported assertion', ['jr-checkout-finding']),
    node('hypothesis-db-saturation', 1, primary, 'Database saturation', 'Not supported by this sample', 'hypothesis', 'Agent-reported assertion', ['jr-checkout-finding', 'jr-checkout-db']),
    node('observation-recovery', 5, primary, 'Observed recovery', '194 ms p95 · pool restored to 96', 'observation', 'Observed telemetry', ['jr-checkout-recovery']),
    node('ledger-db', 0, ledger, 'Aurora writer failover', '12:16:40 UTC', 'change', 'Observed event', ['jr-ledger-failover']),
    node('ledger-worker', 0, ledger, 'Ledger worker retries', '8.4% → 0.2% in observed window', 'resource', 'Observed telemetry', ['jr-ledger-alarm', 'jr-ledger-failover']),
    node('ledger-finding', 0, ledger, 'Reconnect interval', '37 seconds reported', 'hypothesis', 'Agent-reported assertion', ['jr-ledger-summary']),
    node('supplier-gateway', 0, supplier, 'Supplier gateway', '38 TLS failures observed', 'resource', 'Observed telemetry', ['jr-supplier-alarm']),
    node('supplier-gap', 0, supplier, 'Gateway log source', 'Access denied · evidence gap', 'unresolved', 'Collection observation', ['jr-supplier-denied'])
  ];
  const edge = (id, from, taskId, source, target, label, kind, origin, refs) => ({ id, from, taskId, scopeKey: scopeFor(taskId).key, source, target, label, kind, origin, sourceRefs: refs });
  const graphEdges = [
    edge('edge-release-checkout', 0, primary, 'change-release', 'resource-checkout', 'changes configuration', 'references', 'Observed change', ['jr-checkout-deploy']),
    edge('edge-wait-checkout', 0, primary, 'observation-wait', 'resource-checkout', 'observed in', 'references', 'Observed log', ['jr-checkout-wait']),
    edge('edge-release-pool', 1, primary, 'change-release', 'observation-pool', 'reduces limit', 'references', 'Observed change', ['jr-checkout-deploy']),
    edge('edge-pool-contention', 1, primary, 'observation-pool', 'hypothesis-contention', 'supports', 'supports', 'Agent-reported assertion', ['jr-checkout-finding']),
    edge('edge-wait-contention', 1, primary, 'observation-wait', 'hypothesis-contention', 'supports', 'supports', 'Agent-reported assertion', ['jr-checkout-finding']),
    edge('edge-db-saturation', 1, primary, 'resource-orders', 'hypothesis-db-saturation', 'does not support', 'contradicts', 'Agent-reported assertion', ['jr-checkout-finding', 'jr-checkout-db']),
    edge('edge-contention-checkout', 1, primary, 'hypothesis-contention', 'resource-checkout', 'reported cause of latency', 'asserted_cause_of', 'Agent-reported assertion', ['jr-checkout-finding']),
    edge('edge-recovery-checkout', 5, primary, 'observation-recovery', 'resource-checkout', 'new observation', 'references', 'Observed telemetry', ['jr-checkout-recovery']),
    edge('edge-ledger-failover', 0, ledger, 'ledger-db', 'ledger-finding', 'supports', 'supports', 'Agent-reported assertion', ['jr-ledger-summary']),
    edge('edge-ledger-retry', 0, ledger, 'ledger-finding', 'ledger-worker', 'reported cause of retries', 'asserted_cause_of', 'Agent-reported assertion', ['jr-ledger-summary']),
    edge('edge-supplier-gap', 0, supplier, 'supplier-gap', 'supplier-gateway', 'diagnostics unavailable', 'references', 'Collection observation', ['jr-supplier-denied'])
  ];
  const artifactDefinitions = [
    { id: 'artifact-runbook', from: 0, taskId: primary, name: 'Checkout recovery checklist', filename: 'checkout-recovery.md', kind: 'Attachment', mediaType: 'text/markdown', status: 'available', sourceKind: 'Native asset version', description: 'Retrieved version 3. The attachment reference alone does not establish which version the agent consumed.', body: runbook, assetId: 'asset-checkout-runbook', version: 3, sourceRefs: ['jr-checkout-attachment', 'asset-checkout-runbook-v3', 'file-checkout-runbook-v3'] },
    { id: 'artifact-traces', from: 1, taskId: primary, name: 'Detailed trace bundle', filename: 'trace-bundle.json', kind: 'Referenced object', mediaType: 'application/json', status: 'access_denied', sourceKind: 'Published journal reference', description: 'The simulated collector could not read the referenced S3 object. No file content is available.', body: null, sourceRefs: ['jr-checkout-trace-ref'] },
    { id: 'artifact-supplier-logs', from: 0, taskId: supplier, name: 'Gateway-side diagnostics', filename: 'gateway-diagnostics.json', kind: 'External evidence', mediaType: 'application/json', status: 'access_denied', sourceKind: 'Collection error', description: 'Access to the partner log source is denied. Repair access and collect new evidence before interpreting this gap.', body: null, sourceRefs: ['jr-supplier-denied'] }
  ];
  for (const row of [...findingDefinitions, ...artifactDefinitions]) row.scopeKey = scopeFor(row.taskId).key;
  const data = { scenario, scopes, taskMetadata, taskObservations, executionLabels, executionObservations, memberships, journalRecords, lifecycleEvents, assetObservations, assetFiles, timelineDefinitions, findingDefinitions, graphNodes, graphEdges, artifactDefinitions };
  const freeze = obj => { if (obj && typeof obj === 'object' && !Object.isFrozen(obj)) { Object.values(obj).forEach(freeze); Object.freeze(obj); } return obj; };
  return freeze(data);
});
