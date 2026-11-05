'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const D = require('../src/mock-data.js');
const M = require('../src/model.js');

const at = step => { const state = M.createState(); while (state.step < step) M.advance(state); return state; };
const sorted = value => Array.isArray(value) ? value.map(sorted) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(k => [k, sorted(value[k])])) : value;
const sha = text => 'sha256:' + crypto.createHash('sha256').update(text, 'utf8').digest('hex');
const jsonHash = value => sha(JSON.stringify(sorted(value)));

test('fictional baseline has explicit task, execution, evidence, and collection counting units', () => {
  assert.deepEqual(M.validateData(), []);
  const state = M.createState(); const v = M.view(state);
  assert.equal(v.task.taskType, 'INVESTIGATION');
  assert.equal(v.task.priority, 'CRITICAL');
  assert.deepEqual(v.counts, { executions: 3, running: 2, records: 6, artifacts: 2, availableArtifacts: 2, timeline: 5, findings: 1, completeExecutions: 2 });
  assert.equal(M.portfolio(state).length, 3);
  assert.equal(v.now, '2026-11-05T14:12:30Z');
  assert.equal(v.coverage.status, 'partial');
  assert.equal(v.coverage.paginationStatus, 'partial');
  assert.ok(v.provenance.disclaimer.includes('synthetic'));
  assert.ok(v.scope.key.includes(v.scope.agentSpaceId));
  assert.equal(v.task.severity, undefined, 'Task priority is not recast as incident severity.');
});

test('identical execution and record IDs in different spaces do not join across scopes', () => {
  const state = M.createState();
  const ledger = M.view(state, 'inv-ledger-1105');
  const supplier = M.view(state, 'inv-supplier-1105');
  const a = ledger.records.find(r => r.executionId === 'run-root' && r.recordId === 'rec-001');
  const b = supplier.records.find(r => r.executionId === 'run-root' && r.recordId === 'rec-001');
  assert.equal(a.executionId, b.executionId);
  assert.equal(a.recordId, b.recordId);
  assert.notEqual(a.key, b.key);
  assert.notEqual(a.content.resource, b.content.resource);
  assert.notEqual(a.revisionId, b.revisionId);
  assert.ok(Object.values(ledger.sources).every(s => s.scopeKey === ledger.scope.key));
  assert.ok(Object.values(supplier.sources).every(s => s.scopeKey === supplier.scope.key));
  assert.equal(M.view(state, ledger.key).id, ledger.id);
  for (const v of [ledger, supplier]) for (const ex of v.executions) {
    assert.equal(ex.raw.taskId, undefined, 'Membership is retained from the ListExecutions request, not inserted into its native body.');
    assert.equal(ex.membership.query.taskId, v.id);
    assert.equal(ex.membership.query.agentSpaceId, v.scope.agentSpaceId);
  }
});

test('task completion, stopped executions, and summary availability remain independent', () => {
  const initial = M.view(M.createState());
  assert.equal(initial.task.status, 'IN_PROGRESS');
  assert.ok(initial.executions.some(e => e.executionStatus === 'STOPPED'));
  assert.equal(initial.summary.status, 'none');
  const candidate = M.view(at(1));
  assert.equal(candidate.task.status, 'IN_PROGRESS');
  assert.equal(candidate.summary.status, 'candidate');
  const completed = M.view(at(2));
  assert.equal(completed.task.status, 'COMPLETED');
  assert.ok(completed.executions.every(e => e.executionStatus === 'STOPPED'));
  assert.equal(completed.summary.status, 'pending');
  assert.equal(completed.summary.recordId, 'summary-final-02');
  assert.ok(!completed.records.some(r => r.recordId === completed.summary.recordId));
  assert.ok(completed.summary.sourceRefs.includes('event-checkout-completed'));
  assert.equal(completed.artifacts.find(a => a.id === 'artifact-summary-summary-final-02').body, null);
});

test('an exact completion pointer selects the referenced summary rather than a newer same-type record', () => {
  const v = M.view(at(3));
  assert.equal(v.summary.status, 'available');
  assert.equal(v.summary.recordId, 'summary-final-02');
  assert.equal(v.summary.sourceRefId, 'jr-checkout-final');
  const picked = v.records.find(r => r.sourceRefId === v.summary.sourceRefId);
  const newer = v.records.find(r => r.recordId === 'summary-note-03');
  assert.ok(newer.createdAt > picked.createdAt);
  assert.notEqual(v.summary.body, newer.content);
  assert.equal(v.summary.body, picked.content);
  assert.deepEqual(v.summary.candidates.filter(c => c.selected).map(c => c.recordId), ['summary-final-02']);
  const event = M.lookupSource(v, 'event-checkout-completed').payload;
  assert.equal(event.detail.metadata.execution_id, picked.executionId);
  assert.equal(event.detail.data.summary_record_id, picked.recordId);
});

test('resuming a completed task preserves its earlier immutable historical capture', () => {
  const state = at(3);
  assert.equal(state.snapshots.length, 1);
  const captured = state.snapshots[0];
  const before = JSON.stringify(captured);
  const id = captured.snapshotId;
  assert.ok(Object.isFrozen(captured));
  assert.ok(Object.isFrozen(captured.view.records));
  assert.equal(captured.view.counts.records, 14);
  M.advance(state);
  const active = M.view(state);
  assert.equal(active.task.taskId, captured.taskId);
  assert.equal(active.task.status, 'IN_PROGRESS');
  assert.equal(active.counts.executions, 5);
  assert.equal(active.task.executionId, 'run-checkout-root', 'The associated execution ID is not assumed to be the newest one.');
  assert.equal(active.summary.isPriorCompletion, true);
  assert.equal(active.summary.title, 'Previous completed result');
  const history = M.view(state, active.id, id);
  assert.equal(history.task.status, 'COMPLETED');
  assert.equal(history.counts.records, 14);
  assert.equal(history.counts.executions, 4);
  assert.equal(history.newActivity, true);
  M.advance(state);
  assert.equal(M.view(state).summary.recordId, 'summary-followup-01');
  assert.equal(M.view(state).summary.isPriorCompletion, false);
  assert.equal(JSON.stringify(captured), before);
  assert.equal(M.exportSnapshot(state, active.id, id).investigation.summary.recordId, 'summary-final-02');
});

test('partial snapshots retain their gaps and separate capture time from collection time', () => {
  const state = M.createState();
  const info = M.captureSnapshot(state);
  const partial = M.exportSnapshot(state, D.scenario.primaryTaskId, info.snapshotId);
  assert.equal(partial.manifest.coverage.status, 'partial');
  assert.equal(partial.manifest.captureStartedAt, '2026-11-05T14:12:30Z');
  assert.equal(partial.manifest.captureFinishedAt, '2026-11-05T14:12:30Z');
  assert.equal(partial.manifest.collectionAsOf, '2026-11-05T14:12:28Z');
  while (state.step < 5) M.advance(state);
  assert.equal(M.view(state).coverage.status, 'complete');
  assert.equal(M.view(state, undefined, info.snapshotId).coverage.status, 'partial');
  assert.deepEqual(M.exportSnapshot(state, undefined, info.snapshotId).manifest.coverage, partial.manifest.coverage);
  const ledger = M.captureSnapshot(state, 'inv-ledger-1105');
  const ledgerExport = M.exportSnapshot(state, ledger.taskId, ledger.snapshotId);
  assert.equal(ledgerExport.manifest.captureStartedAt, D.scenario.stages[5].at);
  assert.equal(ledgerExport.manifest.collectionAsOf, '2026-11-05T12:42:10Z');
  assert.throws(() => M.view(state, 'inv-supplier-1105', ledger.snapshotId), /does not belong/);
});

test('unknown journal content is retained without object-shape assumptions', () => {
  const primary = M.view(at(3));
  const opaque = primary.records.find(r => r.recordType === 'demo.future_profile.v9');
  assert.deepEqual(opaque.content, ['opaque-vendor-content', 3, { futureField: true }]);
  assert.deepEqual(M.lookupSource(primary, opaque.sourceRefId).payload.content, opaque.content);
  const supplier = M.view(M.createState(), 'inv-supplier-1105');
  const nullRecord = supplier.records.find(r => r.recordId === 'rec-future');
  assert.equal(nullRecord.content, null);
  assert.ok(nullRecord.preview.includes('JSON null'));
  assert.equal(M.lookupSource(supplier, nullRecord.sourceRefId).payload.content, null);
  assert.equal(M.lookupSource(supplier, 'unavailable-source'), null);
});

test('exhausted pagination can coexist with missing external evidence and a timed-out task', () => {
  const v = M.view(M.createState(), 'inv-supplier-1105');
  assert.equal(v.task.status, 'TIMED_OUT');
  assert.equal(v.coverage.paginationStatus, 'complete');
  assert.equal(v.coverage.completeJournalQueries, 2);
  assert.ok(v.coverage.executions.every(r => r.paginationStatus === 'complete' && !r.hasMore));
  assert.equal(v.coverage.status, 'partial');
  assert.equal(v.summary.status, 'none');
  assert.ok(v.summary.reason.includes('terminal outcome'));
  assert.equal(v.artifacts[0].status, 'access_denied');
  assert.equal(v.artifacts[0].body, null);
  assert.equal(v.metrics.length, 0, 'A narrative error sample is not converted into an invented metric series.');
  const completed = M.view(M.createState(), 'inv-ledger-1105');
  assert.equal(completed.coverage.status, 'complete');
  assert.equal(completed.coverage.freshness, 'stale', 'Freshness is independent of complete historical pagination.');
});

test('coverage request scopes contain the native Agent Space ID and retain the unfinished query', () => {
  for (const task of M.portfolio(M.createState())) {
    const v = M.view(M.createState(), task.taskId);
    for (const row of v.coverage.executions) assert.equal(row.query.agentSpaceId, v.scope.agentSpaceId);
  }
  const initial = M.view(M.createState());
  const logs = initial.coverage.executions.find(r => r.executionId === 'run-checkout-logs');
  assert.equal(logs.hasMore, true);
  assert.equal(logs.paginationStatus, 'partial');
  const complete = M.view(at(3));
  const retrieved = complete.coverage.executions.find(r => r.executionId === logs.executionId);
  assert.equal(retrieved.pagesRead, 2);
  assert.equal(retrieved.hasMore, false);
  assert.ok(complete.records.some(r => r.recordId === 'rec-future'));
});

test('source and projection revision identities are stable when the evidence is unchanged', () => {
  const state = at(3); const before = M.view(state); const repeated = M.view(state);
  assert.deepEqual(before.sources, repeated.sources);
  assert.deepEqual(before.timeline, repeated.timeline);
  M.advance(state); const later = M.view(state);
  for (const item of before.timeline) {
    const stillPresent = later.timeline.find(r => r.id === item.id);
    assert.equal(stillPresent.projectionRevisionId, item.projectionRevisionId);
    assert.equal(stillPresent.payloadHash, item.payloadHash);
  }
  assert.equal(later.sources['jr-checkout-final'].revisionId, before.sources['jr-checkout-final'].revisionId);
  assert.notEqual(later.sources['task-checkout-v10'].revisionId, before.sources['task-checkout-v9'].revisionId);
});

test('source, projection, and downloadable artifact hashes match independent Node SHA-256', () => {
  const state = at(5);
  for (const task of M.portfolio(state)) {
    const v = M.view(state, task.taskId);
    for (const source of Object.values(v.sources)) {
      assert.equal(source.hashEncoding, 'canonical-json-utf8');
      assert.equal(source.payloadHash, jsonHash(source.payload), source.id);
    }
    for (const item of [...v.timeline, ...v.findings, ...v.graph.nodes, ...v.graph.edges]) {
      const { payloadHash, ...body } = item;
      assert.equal(payloadHash, jsonHash(body), item.id);
    }
    for (const artifact of v.artifacts) {
      if (artifact.status === 'available') {
        assert.equal(artifact.hashEncoding, 'utf8-content-bytes');
        assert.equal(artifact.hash, sha(artifact.body), artifact.id);
      } else assert.equal(artifact.hash, null);
    }
  }
});

test('evidence graph relationships cite exact scoped sources and distinguish alternative hypotheses', () => {
  const v = M.view(at(3)); const nodeIds = new Set(v.graph.nodes.map(n => n.id));
  for (const item of [...v.graph.nodes, ...v.graph.edges]) {
    assert.ok(item.sourceRefs.length);
    for (const id of item.sourceRefs) {
      const source = M.lookupSource(v, id);
      assert.ok(source.revisionId);
      assert.equal(source.scopeKey, v.scope.key);
      assert.equal(source.locator, '/content');
    }
  }
  for (const edge of v.graph.edges) assert.ok(nodeIds.has(edge.source) && nodeIds.has(edge.target));
  const negative = v.graph.edges.find(e => e.kind === 'contradicts');
  assert.equal(negative.target, 'hypothesis-db-saturation');
  assert.notEqual(negative.target, 'hypothesis-contention');
  assert.ok(v.graph.edges.filter(e => e.kind === 'asserted_cause_of').every(e => e.origin === 'Agent-reported assertion'));
});

test('published, observed, and underlying incident times stay ordered and separately labeled', () => {
  const earliestExecutions = new Map();
  for (const ex of D.executionObservations) {
    const k = ex.scopeKey + '|' + ex.raw.executionId;
    earliestExecutions.set(k, Math.min(earliestExecutions.get(k) || Infinity, ex.raw.createdAt));
    assert.ok(ex.raw.createdAt <= ex.raw.updatedAt);
    assert.ok(ex.raw.updatedAt * 1000 <= Date.parse(ex.observedAt));
  }
  for (const r of D.journalRecords) {
    assert.ok(r.raw.createdAt >= earliestExecutions.get(r.scopeKey + '|' + r.raw.executionId), r.id);
    assert.ok(r.raw.createdAt * 1000 <= Date.parse(r.observedAt), r.id);
    for (const p of r.raw.content && Array.isArray(r.raw.content.points) ? r.raw.content.points : []) {
      assert.ok(Date.parse(p.at) <= r.raw.createdAt * 1000, r.id);
      assert.ok(Number.isFinite(p.value));
      assert.ok(r.raw.content.unit && r.raw.content.statistic && r.raw.content.window, 'A plotted sample needs sourced units, statistic, and time window.');
    }
  }
  const supplier = M.view(M.createState(), 'inv-supplier-1105');
  const timeout = supplier.timeline.find(i => i.id === 'tl-supplier-timeout');
  assert.equal(timeout.occurredAt, '2026-11-05T13:50:00Z');
  assert.equal(timeout.recordedAt, '2026-11-05T13:50:00Z');
  assert.equal(timeout.observedAt, '2026-11-05T13:50:12Z');
  const resumed = M.view(at(4)).timeline.find(i => i.id === 'tl-checkout-resumed');
  assert.equal(resumed.occurredAt, '2026-11-05T14:25:45Z');
  assert.equal(resumed.recordedAt, '2026-11-05T14:25:47.000Z');
});

test('metric projections only include available source points and sourced thresholds', () => {
  const initial = M.view(M.createState());
  const final = M.view(at(5));
  assert.equal(initial.metrics[0].points.length, 8);
  assert.equal(final.metrics[0].points.length, 15);
  assert.equal(initial.metrics[0].threshold, initial.sources['jr-checkout-alarm'].payload.content.threshold);
  assert.ok(initial.metrics[0].sourceRefs.includes('jr-checkout-alarm'));
  for (const state of [M.createState(), at(3), at(5)]) for (const task of M.portfolio(state)) {
    const v = M.view(state, task.taskId);
    for (const series of v.metrics) {
      const published = series.sourceRefs.flatMap(id => M.lookupSource(v, id).payload.content.points || []);
      assert.deepEqual(series.points, published.slice().sort((a,b) => a.at.localeCompare(b.at)));
      assert.ok(series.points.every(p => Date.parse(p.at) <= Date.parse(v.now)));
    }
  }
});

test('retrieved attachment version and downloadable bytes remain pinned after a newer asset exists', () => {
  const state = at(3); const historical = state.snapshots[0];
  M.advance(state);
  assert.ok(D.assetObservations.some(a => a.from <= state.step && a.raw.version === 4));
  const current = M.view(state).artifacts.find(a => a.id === 'artifact-runbook');
  const retained = M.view(state, undefined, historical.snapshotId).artifacts.find(a => a.id === 'artifact-runbook');
  assert.equal(current.version, 3);
  assert.equal(retained.version, 3);
  assert.equal(current.hash, retained.hash);
  const source = M.lookupSource(M.view(state), 'asset-checkout-runbook-v3');
  assert.equal(source.payload.metadata.filename, current.filename);
  assert.equal(source.payload.metadata.extension, 'md');
  assert.equal(source.payload.metadata.size, Buffer.byteLength(current.body, 'utf8'));
  assert.ok(current.description.includes('does not establish'));
});

test('views and exports are detached, serializable, and safely rehydrate through the public API', () => {
  const state = at(3); const original = M.view(state);
  original.task.status = 'FAILED';
  original.records[0].raw.content = 'edited copy';
  assert.equal(M.view(state).task.status, 'COMPLETED');
  assert.notEqual(M.view(state).records[0].raw.content, 'edited copy');
  const rehydrated = JSON.parse(JSON.stringify(state));
  assert.deepEqual(M.view(rehydrated), M.view(state));
  M.advance(rehydrated);
  assert.equal(M.view(rehydrated, undefined, state.snapshots[0].snapshotId).task.status, 'COMPLETED');
  const exported = M.exportSnapshot(rehydrated);
  exported.investigation.task.status = 'FAILED';
  assert.equal(M.view(rehydrated).task.status, 'IN_PROGRESS');
  assert.throws(() => M.view({ schemaVersion: 99, step: 0, snapshots: [], nextSnapshotNumber: 1 }), /Invalid demo state/);
  assert.throws(() => M.view(state, 'unrecognized-task'), /Unknown investigation/);
  while (state.step < 5) M.advance(state);
  assert.equal(M.advance(state), 5);
  assert.equal(M.view(state).replay.canAdvance, false);
  assert.equal(M.createState().snapshots.length, 0);
});
