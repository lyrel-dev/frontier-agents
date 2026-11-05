/* Pure read model for the fictional fixture. No network or browser storage access. */
(function (root, factory) {
  const data = typeof module === 'object' && module.exports ? require('./mock-data.js') : root.DemoData;
  const model = factory(data);
  if (typeof module === 'object' && module.exports) module.exports = model;
  if (root) root.DemoModel = model;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (D) {
  'use strict';
  const SCHEMA = 1;
  const PROJECTION = 'investigation-demo-projection/1.0.0';
  const clone = value => JSON.parse(JSON.stringify(value));
  const freeze = value => { if (value && typeof value === 'object' && !Object.isFrozen(value)) { Object.values(value).forEach(freeze); Object.freeze(value); } return value; };
  const canonical = value => {
    if (Array.isArray(value)) return '[' + value.map(canonical).join(',') + ']';
    if (value && typeof value === 'object') return '{' + Object.keys(value).sort().filter(k => value[k] !== undefined).map(k => JSON.stringify(k) + ':' + canonical(value[k])).join(',') + '}';
    return JSON.stringify(value);
  };
  // SHA-256 over UTF-8 canonical JSON. Synchronous so the same model runs offline
  // in a file:// browser and in Node without a platform-specific crypto adapter.
  const SHA_K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  function digest(text) {
    const input = new TextEncoder().encode(text);
    const bytes = new Uint8Array(Math.ceil((input.length + 9) / 64) * 64);
    bytes.set(input); bytes[input.length] = 0x80;
    const dv = new DataView(bytes.buffer); const bits = input.length * 8;
    dv.setUint32(bytes.length - 8, Math.floor(bits / 0x100000000)); dv.setUint32(bytes.length - 4, bits >>> 0);
    const h = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
    const w = new Uint32Array(64); const r = (x, n) => (x >>> n) | (x << (32 - n));
    for (let offset = 0; offset < bytes.length; offset += 64) {
      for (let i = 0; i < 16; i++) w[i] = dv.getUint32(offset + i * 4);
      for (let i = 16; i < 64; i++) {
        const s0 = r(w[i-15],7) ^ r(w[i-15],18) ^ (w[i-15] >>> 3);
        const s1 = r(w[i-2],17) ^ r(w[i-2],19) ^ (w[i-2] >>> 10);
        w[i] = (w[i-16] + s0 + w[i-7] + s1) >>> 0;
      }
      let [a,b,c,d,e,f,g,j] = h;
      for (let i = 0; i < 64; i++) {
        const t1 = (j + (r(e,6) ^ r(e,11) ^ r(e,25)) + ((e & f) ^ (~e & g)) + SHA_K[i] + w[i]) >>> 0;
        const t2 = ((r(a,2) ^ r(a,13) ^ r(a,22)) + ((a & b) ^ (a & c) ^ (b & c))) >>> 0;
        j=g; g=f; f=e; e=(d+t1)>>>0; d=c; c=b; b=a; a=(t1+t2)>>>0;
      }
      [a,b,c,d,e,f,g,j].forEach((v,i) => { h[i] = (h[i] + v) >>> 0; });
    }
    return h.map(v => v.toString(16).padStart(8, '0')).join('');
  }
  const hash = value => 'sha256:' + digest(canonical(value));
  const key = (scope, type, ...ids) => [scope, type, ...ids].join('|');
  const toISO = timestamp => typeof timestamp === 'number' ? new Date(timestamp * 1000).toISOString() : timestamp;
  const available = (rows, step) => rows.filter(row => row.from <= step);
  const latest = rows => rows.slice().sort((a,b) => a.from - b.from || a.observedAt.localeCompare(b.observedAt)).at(-1);
  const metaFor = id => {
    const result = D.taskMetadata.find(m => m.taskId === id || key(m.scopeKey, 'task', m.taskId) === id);
    if (!result) throw new RangeError('Unknown investigation: ' + id);
    return result;
  };
  function assertState(state) {
    if (!state || state.schemaVersion !== SCHEMA || !Number.isInteger(state.step) || state.step < 0 || state.step >= D.scenario.stages.length || !Array.isArray(state.snapshots) || !Number.isInteger(state.nextSnapshotNumber) || state.nextSnapshotNumber < 1) throw new TypeError('Invalid demo state; reset the scenario.');
  }
  function createState() { return { schemaVersion: SCHEMA, step: 0, snapshots: [], nextSnapshotNumber: 1 }; }
  function snapshotMetadata(entry) {
    return { snapshotId: entry.snapshotId, taskId: entry.taskId, title: entry.title, capturedAt: entry.capturedAt, taskStatus: entry.taskStatus, coverageStatus: entry.coverageStatus, recordCount: entry.recordCount, stage: entry.stage };
  }
  function projection(item, kind, sources) {
    const payload = clone(item);
    const evidence = (payload.sourceRefs || []).map(id => ({ id, revisionId: sources[id] && sources[id].revisionId, locator: sources[id] && sources[id].locator }));
    payload.projectionRevisionId = 'projection:' + kind + ':' + payload.id + ':' + digest(canonical({ payload, evidence, version: PROJECTION })).slice(0, 20);
    payload.derivationId = PROJECTION;
    payload.payloadHash = hash(payload);
    return payload;
  }
  function preview(content) {
    if (content === null) return 'JSON null — retained without interpretation';
    if (typeof content === 'string') return content.replace(/^#+\s*/gm, '').replace(/\s+/g, ' ').slice(0, 180);
    if (typeof content !== 'object') return 'JSON ' + typeof content + ': ' + String(content);
    if (!Array.isArray(content)) {
      for (const name of ['statement', 'message', 'conclusion', 'text', 'title']) if (typeof content[name] === 'string') return content[name].slice(0, 180);
    }
    return JSON.stringify(content).slice(0, 180);
  }
  function addSource(sources, row, kind, sourceKey, nativeId, title, operation, locator, query) {
    const payload = clone(row.raw);
    const payloadHash = hash(payload);
    sources[row.id] = {
      id: row.id, kind, title, nativeId, sourceKey, revisionId: sourceKey + '@' + payloadHash.slice(7, 27),
      observedAt: row.observedAt, locator: locator || '', payloadHash, payload,
      hashEncoding: 'canonical-json-utf8',
      scopeKey: row.scopeKey, operation: operation || null, query: query || null,
      synthetic: true, timestampEncoding: 'REST-JSON wire timestamps for executions/journals/assets; ISO 8601 for backlog/event timestamps'
    };
  }
  function summaryFor(task, records, events, sources) {
    const candidates = records.filter(r => ['investigation_summary_md', 'mitigation_summary_md'].includes(r.recordType));
    const event = events.slice().sort((a,b) => a.raw.time.localeCompare(b.raw.time)).at(-1);
    const base = { status: 'none', title: 'No summary available', body: '', recordId: null, executionId: null, sourceRefId: null, isPriorCompletion: false, selectionBasis: 'No authoritative summary reference', reason: 'No completed result reference has been observed.', sourceRefs: [], candidates: [] };
    let selected = null;
    if (event) {
      const d = event.raw.detail;
      base.sourceRefs = [event.id];
      base.executionId = d.metadata.execution_id || null;
      base.recordId = d.data.summary_record_id || null;
      if (!base.recordId) {
        base.reason = 'The captured completion event omits a summary reference; it reports no available summary for that execution.';
        base.selectionBasis = 'Captured completion event without summary_record_id';
      } else if (!base.executionId) {
        base.reason = 'The event carries a record reference but no execution mapping. An exact journal lookup cannot yet be constructed.';
        base.selectionBasis = 'Unresolved completion-event reference';
      } else {
        const type = event.raw['detail-type'].startsWith('Mitigation') ? 'mitigation_summary_md' : 'investigation_summary_md';
        selected = candidates.find(r => r.executionId === base.executionId && r.recordId === base.recordId && r.recordType === type) || null;
        base.selectionBasis = 'Exact completion-event execution_id + summary_record_id';
        if (selected) {
          base.status = 'available';
          base.sourceRefId = selected.sourceRefId;
          base.isPriorCompletion = ['IN_PROGRESS', 'WAITING', 'PENDING_CUSTOMER_APPROVAL'].includes(task.status);
          base.title = task.status === 'IN_PROGRESS' ? 'Previous completed result' : 'Referenced investigation result';
          base.body = typeof selected.content === 'string' ? selected.content : JSON.stringify(selected.content, null, 2);
          base.sourceRefs.push(selected.sourceRefId);
          base.reason = task.status === 'IN_PROGRESS' ? 'The investigation is active again. This is the previously completed result; the earlier snapshot remains retained.' : 'The exact event-referenced record is retrieved. Other records of the same type remain candidates.';
        } else {
          base.status = 'pending'; base.title = 'Referenced summary not retrieved';
          base.reason = 'A completion event names this exact record, but it is absent from the current collection. Task completion and result availability are separate.';
        }
      }
    } else if (candidates.length) {
      const candidate = candidates.slice().sort((a,b) => a.createdAt - b.createdAt || a.recordId.localeCompare(b.recordId)).at(-1);
      base.status = 'candidate'; base.title = 'Observed summary candidate';
      base.body = typeof candidate.content === 'string' ? candidate.content : JSON.stringify(candidate.content, null, 2);
      base.recordId = candidate.recordId; base.executionId = candidate.executionId;
      base.sourceRefId = candidate.sourceRefId;
      base.selectionBasis = 'Latest observed candidate; no completion pointer';
      base.reason = 'This candidate is available for review. No captured completion event identifies an authoritative final result.';
      base.sourceRefs = [candidate.sourceRefId];
    } else if (['TIMED_OUT', 'FAILED', 'CANCELED', 'SKIPPED'].includes(task.status)) {
      base.reason = 'No summary reference was observed for this terminal outcome. Available records and collection gaps remain inspectable.';
    }
    base.candidates = candidates.map(r => ({ recordId: r.recordId, executionId: r.executionId, title: sources[r.sourceRefId].title, timestamp: r.timestamp, selected: !!selected && r.key === selected.key, sourceRefId: r.sourceRefId }));
    return base;
  }
  function coverageFor(meta, executions, records, step, now, summary) {
    const scope = D.scopes.find(s => s.key === meta.scopeKey);
    const isPrimary = meta.taskId === D.scenario.primaryTaskId;
    const isSupplier = meta.taskId === 'inv-supplier-1105';
    const asOf = isPrimary ? ['2026-11-05T14:12:28Z','2026-11-05T14:17:18Z','2026-11-05T14:20:59Z','2026-11-05T14:21:10Z','2026-11-05T14:26:08Z','2026-11-05T14:32:58Z'][step] : isSupplier ? '2026-11-05T13:50:15Z' : '2026-11-05T12:42:10Z';
    const rows = executions.map(ex => {
      const unfinishedPage = isPrimary && ex.executionId === 'run-checkout-logs' && step < 3;
      const unavailableLog = isSupplier && ex.executionId === 'run-supplier-logs';
      const unresolvedSummary = summary.status === 'pending' && summary.executionId === ex.executionId;
      const status = unfinishedPage || unavailableLog || unresolvedSummary ? 'partial' : 'complete';
      return {
        executionId: ex.executionId, key: ex.key, label: ex.label, status,
        paginationStatus: unfinishedPage ? 'partial' : 'complete',
        pagesRead: isPrimary && ex.executionId === 'run-checkout-logs' && step >= 3 ? 2 : 1,
        hasMore: unfinishedPage, recordCount: records.filter(r => r.executionId === ex.executionId).length,
        observedAt: asOf,
        reason: unfinishedPage ? 'A nextToken remains; an older journal page is not yet collected.' : unavailableLog ? 'The journal query is exhausted, but its published collection error identifies missing external diagnostics.' : unresolvedSummary ? 'Current pages are exhausted, but the event-referenced summary is not retrieved.' : 'The available journal query is exhausted as of this observation.',
        query: { agentSpaceId: scope.agentSpaceId, executionId: ex.executionId, limit: 100, order: 'DESC' }
      };
    });
    const gaps = rows.filter(r => r.status === 'partial').map(r => ({ executionId: r.executionId, reason: r.reason }));
    const count = rows.length - gaps.length;
    return {
      status: gaps.length ? 'partial' : 'complete', label: count + ' of ' + rows.length + ' evidence scopes complete',
      paginationStatus: rows.some(r => r.paginationStatus === 'partial') ? 'partial' : 'complete',
      completeJournalQueries: rows.filter(r => r.paginationStatus === 'complete').length,
      asOf, freshness: Date.parse(now) - Date.parse(asOf) > 60000 ? 'stale' : 'current',
      executions: rows, gaps,
      note: 'Coverage describes these observed journal queries and known evidence gaps. Exhausted pagination does not prevent future records. Artifact access is reported separately. The demo uses deliberately reduced page sizes.'
    };
  }
  function metricsFor(meta, records) {
    if (meta.taskId === 'inv-supplier-1105') return [];
    if (meta.taskId === 'inv-ledger-1105') {
      const rec = records.find(r => r.sourceRefId === 'jr-ledger-failover');
      const alarm = records.find(r => r.sourceRefId === 'jr-ledger-alarm');
      return [{ id: 'ledger-retries', label: 'Worker retry rate', unit: rec.content.unit, aggregation: rec.content.statistic, query: rec.content.query, points: clone(rec.content.points), threshold: alarm.content.threshold, baseline: rec.content.points[0].value, sourceRefs: [rec.sourceRefId, alarm.sourceRefId], note: 'A historical synthetic observation window; no current database health inference. Baseline is the first published sample.' }];
    }
    const contributors = records.filter(r => ['jr-checkout-latency', 'jr-checkout-latency-2', 'jr-checkout-recovery'].includes(r.sourceRefId));
    const alarm = records.find(r => r.sourceRefId === 'jr-checkout-alarm');
    const points = contributors.flatMap(r => r.content.points).sort((a,b) => a.at.localeCompare(b.at));
    return [{ id: 'checkout-p95', label: 'Checkout request latency', unit: 'ms', aggregation: 'p95 · 120-second buckets', query: 'Demo CloudWatch request_duration · service=checkout-api · p95 · 120s buckets', points: clone(points), threshold: alarm.content.threshold, baseline: points.find(p => p.at === '2026-11-05T14:00:00Z').value, sourceRefs: [...contributors.map(r => r.sourceRefId), alarm.sourceRefId], note: 'Only published sample points are plotted. Baseline is the last pre-deployment sample at 14:00 UTC. Unobserved intervals are not additional measurements.' }];
  }
  function liveView(state, inputId) {
    assertState(state);
    const meta = metaFor(inputId || D.scenario.primaryTaskId);
    const scope = D.scopes.find(s => s.key === meta.scopeKey);
    const step = state.step; const now = D.scenario.stages[step].at;
    const taskRows = available(D.taskObservations, step).filter(r => r.scopeKey === meta.scopeKey && r.raw.taskId === meta.taskId);
    const taskRow = latest(taskRows); const task = clone(taskRow.raw);
    const membershipRows = available(D.memberships, step).filter(r => r.scopeKey === meta.scopeKey && r.taskId === meta.taskId);
    const executionIds = new Set(membershipRows.map(r => r.executionId));
    const exRows = available(D.executionObservations, step).filter(r => r.scopeKey === meta.scopeKey && executionIds.has(r.raw.executionId));
    const recordRows = available(D.journalRecords, step).filter(r => r.scopeKey === meta.scopeKey && executionIds.has(r.raw.executionId));
    const events = available(D.lifecycleEvents, step).filter(r => r.scopeKey === meta.scopeKey && r.raw.detail.metadata.task_id === meta.taskId);
    const activeArtifacts = available(D.artifactDefinitions, step).filter(r => r.taskId === meta.taskId);
    const artifactRefs = new Set(activeArtifacts.flatMap(r => r.sourceRefs));
    const sources = {};
    taskRows.forEach(r => addSource(sources, r, 'Native Task', key(meta.scopeKey, 'task', r.raw.taskId), r.raw.taskId, 'Task version ' + r.raw.version, 'GetBacklogTask', '', { agentSpaceId: scope.agentSpaceId, taskId: meta.taskId }));
    exRows.forEach(r => addSource(sources, r, 'Native Execution', key(meta.scopeKey, 'execution', r.raw.executionId), r.raw.executionId, D.executionLabels[r.raw.executionId], 'ListExecutions', '', { agentSpaceId: scope.agentSpaceId, taskId: meta.taskId }));
    recordRows.forEach(r => addSource(sources, r, 'Native JournalRecord envelope', key(meta.scopeKey, 'journal', r.raw.executionId, r.raw.recordId), r.raw.recordId, r.title, 'ListJournalRecords', '/content', { agentSpaceId: scope.agentSpaceId, executionId: r.raw.executionId }));
    events.forEach(r => addSource(sources, r, 'EventBridge notification', key(meta.scopeKey, 'eventbridge', r.raw.id), r.raw.id, r.raw['detail-type'], 'EventBridge delivery', '/detail'));
    available(D.assetObservations, step).filter(r => artifactRefs.has(r.id) && r.scopeKey === meta.scopeKey).forEach(r => addSource(sources, r, 'Native Asset', key(meta.scopeKey, 'asset', r.raw.assetId, r.raw.version), r.raw.assetId, 'Retrieved attachment version ' + r.raw.version, 'GetAsset', '', { agentSpaceId: scope.agentSpaceId, assetId: r.raw.assetId, assetVersion: r.raw.version }));
    available(D.assetFiles, step).filter(r => artifactRefs.has(r.id) && r.scopeKey === meta.scopeKey).forEach(r => addSource(sources, r, 'Native AssetFile', key(meta.scopeKey, 'asset-file', r.assetId, r.raw.version, r.raw.path), r.raw.path, r.raw.path + ' · version ' + r.raw.version, 'GetAssetFile', '/content/text', { agentSpaceId: scope.agentSpaceId, assetId: r.assetId, assetVersion: r.raw.version, path: r.raw.path }));
    const records = recordRows.map(r => Object.assign({}, clone(r.raw), {
      key: key(meta.scopeKey, 'journal', r.raw.executionId, r.raw.recordId), timestamp: toISO(r.raw.createdAt),
      preview: preview(r.raw.content), sourceRefId: r.id, revisionId: sources[r.id].revisionId,
      observedAt: r.observedAt, raw: clone(r.raw)
    })).sort((a,b) => a.createdAt - b.createdAt || a.key.localeCompare(b.key));
    const executions = membershipRows.map(m => {
      const observation = latest(exRows.filter(r => r.raw.executionId === m.executionId));
      const raw = clone(observation.raw); const children = records.filter(r => r.executionId === raw.executionId);
      return Object.assign({}, raw, {
        key: key(meta.scopeKey, 'execution', raw.executionId), label: D.executionLabels[raw.executionId],
        createdAtIso: toISO(raw.createdAt), updatedAtIso: toISO(raw.updatedAt), recordCount: children.length,
        recordIds: children.map(r => r.recordId), sourceRefs: [observation.id], membership: clone(m), raw
      });
    });
    const timeline = available(D.timelineDefinitions, step).filter(r => r.scopeKey === meta.scopeKey && r.taskId === meta.taskId).map(row => {
      const refs = row.sourceRefs.map(id => sources[id]);
      const recordedTimes = refs.map(s => {
        const timestamp = s.kind === 'Native Task' || s.kind === 'Native Execution'
          ? s.payload.updatedAt || s.payload.createdAt || s.observedAt
          : s.kind === 'EventBridge notification' ? s.payload.time || s.observedAt
          : s.kind === 'Native JournalRecord envelope' ? s.payload.createdAt || s.observedAt
          : s.observedAt;
        return toISO(timestamp);
      });
      const item = { id: row.id, title: row.title, body: row.body, category: row.category, phase: row.from >= 4 ? 'Follow-up' : 'Investigation', occurredAt: row.occurredAt, occurredAtBasis: row.category === 'collection' ? 'Application collection observation' : row.category === 'lifecycle' ? 'Native task/event timestamp' : 'Published payload timestamp', recordedAt: recordedTimes.sort().at(-1), observedAt: refs.map(s => s.observedAt).sort().at(-1), origin: row.origin, sourceRefs: row.sourceRefs, executionId: row.executionId };
      return projection(item, 'timeline', sources);
    }).sort((a,b) => a.occurredAt.localeCompare(b.occurredAt) || a.id.localeCompare(b.id));
    const findings = available(D.findingDefinitions, step).filter(r => r.taskId === meta.taskId).map(({ from, taskId, ...r }) => projection(r, 'finding', sources));
    const nodes = available(D.graphNodes, step).filter(r => r.taskId === meta.taskId).map(({ from, taskId, ...r }) => projection(r, 'graph-node', sources));
    const edges = available(D.graphEdges, step).filter(r => r.taskId === meta.taskId).map(({ from, taskId, ...r }) => projection(r, 'graph-edge', sources));
    const graph = { id: 'graph:' + meta.taskId + ':' + digest(canonical({ nodes, edges })).slice(0, 16), kind: 'evidence', title: 'Published evidence relationships', note: 'Relationships retain source attribution. An execution hierarchy is a separate graph; time order alone does not establish causality.', nodes, edges };
    const metrics = metricsFor(meta, records);
    const summary = summaryFor(task, records, events, sources);
    const artifacts = activeArtifacts.map(({ from, taskId, ...r }) => Object.assign(clone(r), { hash: r.body === null ? null : 'sha256:' + digest(r.body), hashEncoding: r.body === null ? null : 'utf8-content-bytes' }));
    if (metrics.length) {
      const metric = metrics[0];
      const body = 'timestamp,' + (metric.unit === 'ms' ? 'p95_ms' : 'retry_percent') + '\n' + metric.points.map(p => p.at + ',' + p.value).join('\n') + '\n';
      artifacts.push({ id: 'artifact-observed-metrics', name: 'Observed metric samples', filename: meta.taskId + '-observed-metrics.csv', kind: 'Derived export', mediaType: 'text/csv', status: 'available', sourceKind: 'Application projection', description: 'CSV generated only from the published mock observations shown in the chart.', body, hash: 'sha256:' + digest(body), hashEncoding: 'utf8-content-bytes', sourceRefs: metric.sourceRefs });
    }
    if (summary.status === 'available' || summary.status === 'candidate' || summary.status === 'pending') {
      artifacts.push({ id: 'artifact-summary-' + summary.recordId, name: summary.status === 'candidate' ? 'Summary candidate' : summary.isPriorCompletion ? 'Previous completed summary' : 'Referenced investigation summary', filename: summary.recordId + '.md', kind: summary.status === 'candidate' ? 'Candidate summary' : 'Referenced summary', mediaType: 'text/markdown', status: summary.status === 'pending' ? 'pending' : 'available', sourceKind: 'Journal record', description: summary.reason, body: summary.status === 'pending' ? null : summary.body, hash: summary.status === 'pending' ? null : 'sha256:' + digest(summary.body), hashEncoding: summary.status === 'pending' ? null : 'utf8-content-bytes', sourceRefs: summary.sourceRefs });
    }
    const coverage = coverageFor(meta, executions, records, step, now, summary);
    const isPrimary = meta.taskId === D.scenario.primaryTaskId;
    const phase = isPrimary ? Object.assign({}, D.scenario.stages[step], { number: step + 1, total: D.scenario.stages.length }) : { id: task.status === 'COMPLETED' ? 'completed-case' : 'partial-case', title: task.status === 'COMPLETED' ? 'Completed investigation' : 'Timed out · evidence incomplete', description: meta.description, number: 1, total: 1 };
    return {
      id: meta.taskId, key: key(meta.scopeKey, 'task', meta.taskId), task, meta: clone(meta), scope: clone(scope), now, phase,
      replay: { step: isPrimary ? step : 0, totalSteps: isPrimary ? D.scenario.stages.length : 1, canAdvance: isPrimary && step < D.scenario.stages.length - 1, stageLabels: isPrimary ? D.scenario.stages.map(s => s.title) : [phase.title], nextLabel: isPrimary && step < D.scenario.stages.length - 1 ? D.scenario.stages[step + 1].title : null },
      executions, records, timeline, findings, graph, metrics, summary, artifacts, coverage, sources,
      counts: { executions: executions.length, running: executions.filter(e => e.executionStatus === 'RUNNING').length, records: records.length, artifacts: artifacts.length, availableArtifacts: artifacts.filter(a => a.status === 'available').length, timeline: timeline.length, findings: findings.length, completeExecutions: coverage.executions.filter(e => e.status === 'complete').length },
      snapshots: state.snapshots.filter(s => s.taskId === meta.taskId).map(snapshotMetadata), isSnapshot: false, snapshot: null, newActivity: false,
      provenance: { fixtureVersion: D.scenario.version, projectionVersion: PROJECTION, timestampEncoding: 'View clocks are ISO 8601; raw native envelopes preserve their modeled timestamp representation.', disclaimer: D.scenario.disclaimer }
    };
  }
  function sourceManifest(v) {
    return Object.values(v.sources).map(s => ({ sourceKey: s.sourceKey, revisionId: s.revisionId, payloadHash: s.payloadHash, observedAt: s.observedAt })).sort((a,b) => a.sourceKey.localeCompare(b.sourceKey) || a.revisionId.localeCompare(b.revisionId));
  }
  function view(state, taskId, snapshotId) {
    const current = liveView(state, taskId);
    if (!snapshotId) return current;
    const retained = state.snapshots.find(s => s.snapshotId === snapshotId && s.taskId === current.id);
    if (!retained || !retained.view) throw new RangeError('Snapshot does not belong to this investigation.');
    const result = clone(retained.view);
    result.isSnapshot = true; result.snapshot = snapshotMetadata(retained);
    result.newActivity = hash(sourceManifest(current)) !== hash(sourceManifest(retained.view));
    return result;
  }
  function portfolio(state) {
    return D.taskMetadata.map(m => {
      const v = liveView(state, m.taskId);
      return { taskId: v.id, key: v.key, code: v.meta.code, title: v.task.title, service: v.meta.service, owner: v.meta.owner, region: v.scope.region, status: v.task.status, priority: v.task.priority, updatedAt: v.task.updatedAt, recordCount: v.counts.records, coverageStatus: v.coverage.status };
    });
  }
  function captureSnapshot(state, taskId) {
    const current = liveView(state, taskId);
    const n = state.nextSnapshotNumber++;
    const snapshotId = 'snapshot-' + String(n).padStart(3, '0');
    const metadata = { snapshotId, taskId: current.id, title: current.meta.code + ' · ' + current.phase.title, capturedAt: current.now, taskStatus: current.task.status, coverageStatus: current.coverage.status, recordCount: current.counts.records, stage: state.step };
    current.snapshots = []; current.isSnapshot = true; current.snapshot = clone(metadata); current.newActivity = false;
    const manifest = {
      snapshotId, investigationKey: current.key, captureStartedAt: current.now, captureFinishedAt: current.now,
      collectionAsOf: current.coverage.asOf,
      taskVersion: current.task.version, taskStatus: current.task.status, summarySelectionBasis: current.summary.selectionBasis,
      summaryPointer: { executionId: current.summary.executionId, recordId: current.summary.recordId },
      coverage: clone(current.coverage), executionMemberships: current.executions.map(e => clone(e.membership)),
      sources: sourceManifest(current), projectionRevisionIds: [...current.timeline, ...current.findings, ...current.graph.nodes, ...current.graph.edges].map(r => r.projectionRevisionId),
      assetVersions: current.artifacts.filter(a => a.assetId && Number.isInteger(a.version)).map(a => ({ assetId: a.assetId, version: a.version, hash: a.hash })),
      projectionVersion: PROJECTION, fixtureVersion: D.scenario.version,
      note: 'Application snapshot of a non-transactional collection. Known gaps are retained; completion does not imply incident recovery.'
    };
    state.snapshots.push(freeze(Object.assign({}, metadata, { manifest, view: clone(current) })));
    return clone(metadata);
  }
  function advance(state) {
    assertState(state);
    state.step = Math.min(state.step + 1, D.scenario.stages.length - 1);
    if (state.step === 3 && !state.snapshots.some(s => s.taskId === D.scenario.primaryTaskId && s.stage === 3)) captureSnapshot(state, D.scenario.primaryTaskId);
    return state.step;
  }
  function exportSnapshot(state, taskId, snapshotId) {
    const selected = view(state, taskId, snapshotId);
    const retained = snapshotId && state.snapshots.find(s => s.snapshotId === snapshotId && s.taskId === selected.id);
    return {
      schema: 'northstar.devops-investigation-export.v1', synthetic: true, exportedScenarioTime: selected.now,
      disclaimer: D.scenario.disclaimer,
      manifest: retained ? clone(retained.manifest) : { investigationKey: selected.key, sourceRevisions: sourceManifest(selected), taskVersion: selected.task.version, coverage: clone(selected.coverage), projectionVersion: PROJECTION, captureBasis: 'Current collected view; not a retained historical snapshot' },
      investigation: clone(selected)
    };
  }
  function lookupSource(v, id) { return v && v.sources && v.sources[id] ? clone(v.sources[id]) : null; }
  function validateData() {
    const errors = [];
    const allSources = [...D.taskObservations, ...D.executionObservations, ...D.journalRecords, ...D.lifecycleEvents, ...D.assetObservations, ...D.assetFiles];
    const sourceIds = new Set();
    allSources.forEach(r => { if (sourceIds.has(r.id)) errors.push('Duplicate source observation ID: ' + r.id); sourceIds.add(r.id); });
    for (let step = 0; step < D.scenario.stages.length; step++) {
      const state = createState(); state.step = step;
      for (const meta of D.taskMetadata) {
        let v;
        try { v = liveView(state, meta.taskId); } catch (e) { errors.push('Cannot assemble ' + meta.taskId + ' at ' + step + ': ' + e.message); continue; }
        const keys = v.records.map(r => r.key);
        if (new Set(keys).size !== keys.length) errors.push('Duplicate scoped journal key: ' + meta.taskId + ' at ' + step);
        const exIds = new Set(v.executions.map(e => e.executionId));
        v.records.forEach(r => { if (!exIds.has(r.executionId)) errors.push('Journal has no collected execution: ' + r.key); });
        v.executions.forEach(e => {
          if ('taskId' in e.raw) errors.push('Native execution acquired a fabricated taskId: ' + e.key);
          if (e.parentExecutionId && !exIds.has(e.parentExecutionId)) errors.push('Fixture execution parent unresolved: ' + e.key);
        });
        const nodes = new Set(v.graph.nodes.map(n => n.id));
        v.graph.edges.forEach(e => { if (!nodes.has(e.source) || !nodes.has(e.target)) errors.push('Graph endpoint unresolved: ' + e.id); });
        [...v.timeline, ...v.findings, ...v.graph.nodes, ...v.graph.edges, ...v.artifacts, ...v.metrics, v.summary].forEach(item => {
          (item.sourceRefs || []).forEach(id => { if (!v.sources[id]) errors.push('Source reference unresolved: ' + id); });
        });
        v.records.forEach(r => {
          if (Date.parse(r.observedAt) < r.createdAt * 1000) errors.push('Record observed before publication: ' + r.key);
          if (Date.parse(r.observedAt) > Date.parse(v.now)) errors.push('Future source leaked into view: ' + r.key);
          if (r.content && typeof r.content === 'object' && Array.isArray(r.content.points)) r.content.points.forEach(p => {
            if (Date.parse(p.at) > r.createdAt * 1000) errors.push('Metric point later than publication: ' + r.key);
            if (!Number.isFinite(p.value)) errors.push('Non-finite metric: ' + r.key);
          });
        });
      }
    }
    return [...new Set(errors)];
  }
  return Object.freeze({ createState, portfolio, view, advance, captureSnapshot, exportSnapshot, lookupSource, validateData });
});
