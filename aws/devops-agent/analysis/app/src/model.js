/* Pure read model for the fictional fixture. No network or browser storage access. */
(function (root, factory) {
  const data = typeof module === 'object' && module.exports ? require('./mock-data.js') : root.DemoData;
  const model = factory(data);
  if (typeof module === 'object' && module.exports) module.exports = model;
  if (root) root.DemoModel = model;
})(typeof globalThis !== 'undefined' ? globalThis : this, function (D) {
  'use strict';
  const SCHEMA = 1;
  const PROJECTION = 'investigation-demo-projection/1.1.0';
  const HASH_ENCODING = 'sorted-json-utf8/v1';
  const own = (value, name) => !!value && Object.prototype.hasOwnProperty.call(value, name);
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
  // Scope is an existing application connection/space key. Encode every opaque
  // suffix component so distinct execution/record tuples cannot alias via '|'.
  // No reader attempts to recover native IDs by splitting this display key.
  const key = (scope, type, ...ids) => [scope, ...[type, ...ids].map(v => encodeURIComponent(String(v)))].join('|');
  const taskKey = meta => key(meta.scopeKey, 'task', meta.taskId);
  const primaryKey = () => D.scenario.primaryInvestigationKey || taskKey(D.taskMetadata.find(m => m.taskId === D.scenario.primaryTaskId));
  const toISO = timestamp => typeof timestamp === 'number' ? new Date(timestamp * 1000).toISOString() : timestamp;
  const clock = value => Date.parse(toISO(value));
  const available = (rows, step) => rows.filter(row => row.from <= step);
  const latest = rows => rows.slice().sort((a,b) => clock(a.observedAt) - clock(b.observedAt) || a.from - b.from || String(a.id || '').localeCompare(String(b.id || ''))).at(-1);
  const groups = (rows, identity) => {
    const result = new Map();
    for (const row of rows) { const id = identity(row); if (!result.has(id)) result.set(id, []); result.get(id).push(row); }
    return result;
  };
  const metaFor = id => {
    const exact = D.taskMetadata.filter(m => taskKey(m) === id);
    if (exact.length === 1) return exact[0];
    const matches = D.taskMetadata.filter(m => m.taskId === id);
    if (matches.length > 1 || exact.length > 1) throw new RangeError('Ambiguous investigation ID; use its scoped key: ' + id);
    if (!matches.length) throw new RangeError('Unknown investigation: ' + id);
    return matches[0];
  };
  const belongs = meta => row => row.scopeKey === meta.scopeKey && row.taskId === meta.taskId;
  const snapshotKey = entry => entry.investigationKey || entry.manifest && entry.manifest.investigationKey;
  function assertState(state) {
    if (!state || state.schemaVersion !== SCHEMA || !Number.isInteger(state.step) || state.step < 0 || state.step >= D.scenario.stages.length || !Array.isArray(state.snapshots) || !Number.isSafeInteger(state.nextSnapshotNumber) || state.nextSnapshotNumber < 1) throw new TypeError('Invalid demo state; reset the scenario or restore a valid saved state.');
    const ids = new Set();
    for (const snapshot of state.snapshots) {
      if (!snapshot || typeof snapshot !== 'object' || !/^snapshot-\d+$/.test(snapshot.snapshotId || '') || ids.has(snapshot.snapshotId) || Number(snapshot.snapshotId.slice(9)) >= state.nextSnapshotNumber) throw new TypeError('Invalid saved snapshots: duplicate identity or inconsistent snapshot counter.');
      ids.add(snapshot.snapshotId);
      const v = snapshot.view, m = snapshot.manifest;
      if (!v || !m || !v.scope || !v.task || !v.sources || !v.counts || !v.coverage || !v.summary || !v.graph || !v.provenance || !v.meta || !v.phase || !v.replay || !Array.isArray(v.coverage.executions) || !Array.isArray(v.coverage.gaps) || !Array.isArray(v.graph.nodes) || !Array.isArray(v.graph.edges) || !['executions','records','timeline','findings','metrics','artifacts','snapshots'].every(k => Array.isArray(v[k]))) throw new TypeError('Invalid saved snapshot ' + snapshot.snapshotId + ': retained view or manifest is incomplete.');
      const expectedKey = key(v.scope.key, 'task', v.task.taskId);
      if (snapshot.taskId !== v.id || v.id !== v.task.taskId || v.task.agentSpaceId !== v.scope.agentSpaceId || v.meta.scopeKey !== v.scope.key || v.meta.taskId !== v.id || v.key !== expectedKey || snapshotKey(snapshot) !== expectedKey || m.investigationKey !== expectedKey || m.snapshotId !== snapshot.snapshotId || !v.snapshot || v.snapshot.snapshotId !== snapshot.snapshotId || v.snapshot.investigationKey && v.snapshot.investigationKey !== expectedKey || !Array.isArray(m.sources) || !Array.isArray(m.executionMemberships) || !Array.isArray(m.projectionRevisionIds) || !Array.isArray(m.assetVersions) || snapshot.recordCount !== v.records.length || v.counts.records !== v.records.length || v.counts.executions !== v.executions.length || snapshot.taskStatus !== v.task.status || snapshot.coverageStatus !== v.coverage.status) throw new TypeError('Invalid saved snapshot ' + snapshot.snapshotId + ': scope, identity, or counts disagree.');
    }
  }
  function createState() { return { schemaVersion: SCHEMA, step: 0, snapshots: [], nextSnapshotNumber: 1 }; }
  function snapshotMetadata(entry) {
    return { snapshotId: entry.snapshotId, taskId: entry.taskId, investigationKey: snapshotKey(entry), title: entry.title, capturedAt: entry.capturedAt, taskStatus: entry.taskStatus, coverageStatus: entry.coverageStatus, recordCount: entry.recordCount, stage: entry.stage };
  }
  function projection(item, kind, sources) {
    const payload = clone(item);
    const evidence = (payload.sourceRefs || []).map(id => ({ id, revisionId: sources[id] && sources[id].revisionId, locator: sources[id] && sources[id].locator }));
    payload.projectionRevisionId = 'projection:' + kind + ':' + payload.id + ':' + digest(canonical({ payload, evidence, version: PROJECTION }));
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
      id: row.id, observationId: row.id, kind, title, nativeId, sourceKey, revisionId: sourceKey + '@' + payloadHash.slice(7),
      observedAt: row.observedAt, locator: locator || '', payloadHash, payload,
      hashEncoding: 'canonical-json-utf8',
      canonicalization: HASH_ENCODING,
      scopeKey: row.scopeKey, operation: operation || null, query: query || null,
      synthetic: true, timestampEncoding: 'REST-JSON wire timestamps for executions/journals/assets; ISO 8601 for backlog/event timestamps'
    };
  }
  function summaryFor(kind, investigationKey, task, records, events, sources) {
    const label = kind === 'mitigation' ? 'Mitigation' : 'Investigation';
    const recordType = kind + '_summary_md';
    const candidates = records.filter(r => r.recordType === recordType);
    // Lifecycle status is not a summary selection rule. Resolve each documented
    // completion kind separately; failure/start notifications stay as evidence.
    const completed = [...groups(events.filter(e => e.raw['detail-type'] === label + ' Completed'), e => e.raw.id).values()].map(latest);
    const base = { id: investigationKey + '|result|' + kind, kind, recordType, status: 'none', referenceStatus: 'not_observed', title: 'No ' + kind + ' summary observed', body: '', bodyFormat: null, rawContent: null, recordId: null, executionId: null, sourceRefId: null, isPriorCompletion: false, selectionBasis: 'No authoritative summary reference', reason: 'No completed ' + kind + ' result reference has been observed.', sourceRefs: [], candidates: [], completionReferences: [] };
    const bindContent = record => {
      base.rawContent = clone(record.content);
      base.bodyFormat = typeof record.content === 'string' ? 'markdown' : 'json';
      base.body = base.bodyFormat === 'markdown' ? record.content : JSON.stringify(record.content, null, 2);
      base.sourceRefId = record.sourceRefId;
    };
    let selected = null, event = null;
    if (completed.length) {
      const invalidTime = completed.some(e => !Number.isFinite(clock(e.raw.time)));
      const newestTime = Math.max(...completed.map(e => clock(e.raw.time)));
      const newest = invalidTime ? completed : completed.filter(e => clock(e.raw.time) === newestTime);
      const refs = newest.map(e => {
        const metadata = e.raw.detail && e.raw.detail.metadata || {}, data = e.raw.detail && e.raw.detail.data || {};
        const validId = value => typeof value === 'string' && value.length > 0;
        const malformed = own(data,'summary_record_id') && !validId(data.summary_record_id) || own(metadata,'execution_id') && !validId(metadata.execution_id);
        return { sourceRefId: e.id, eventId: e.raw.id, executionId: validId(metadata.execution_id) ? metadata.execution_id : null, recordId: validId(data.summary_record_id) ? data.summary_record_id : null, malformed, occurredAt: e.raw.time, observedAt: e.observedAt };
      }).sort((a,b) => a.sourceRefId.localeCompare(b.sourceRefId));
      base.completionReferences = refs;
      base.sourceRefs = refs.map(r => r.sourceRefId);
      const pointers = new Set(refs.map(r => canonical([r.executionId,r.recordId])));
      const invalidPointer = refs.some(r => r.malformed);
      if (invalidTime || invalidPointer || pointers.size > 1) {
        base.status = 'unresolved'; base.referenceStatus = invalidTime || invalidPointer ? 'unresolved' : 'conflicting';
        base.title = invalidPointer ? 'Completion reference shape unsupported' : invalidTime ? 'Completion ordering unresolved' : 'Conflicting completion references';
        base.selectionBasis = 'No automatic selection among unresolved completion references';
        base.reason = invalidPointer ? 'A supplied execution or summary ID is not a non-empty string. The raw notification remains available; this is not evidence that the service omitted a summary.' : invalidTime ? 'A captured completion has an unsupported timestamp. The retained notifications cannot be reliably ordered.' : 'Equally timed completion notifications name different results. Their arrival order does not establish which result is authoritative.';
      } else {
        // Identical pointers at the same timestamp are equivalent for selection;
        // every observed reference remains cited, independent of input ordering.
        event = newest.slice().sort((a,b) => a.id.localeCompare(b.id))[0];
        base.executionId = refs[0].executionId; base.recordId = refs[0].recordId;
        if (!base.recordId) {
          base.referenceStatus = 'not_reported'; base.title = 'No summary reported for this execution';
          base.reason = 'The captured ' + kind + ' completion event omits a summary reference; it reports no available summary for that execution.';
          base.selectionBasis = 'Captured completion event without summary_record_id';
        } else if (!base.executionId) {
          base.status = 'unresolved'; base.referenceStatus = 'unresolved'; base.title = 'Summary execution reference unresolved';
          base.reason = 'The completion names a record but supplies no execution mapping. An exact journal lookup cannot yet be constructed.';
          base.selectionBasis = 'Unresolved completion-event reference';
        } else {
          base.referenceStatus = 'exact';
          selected = candidates.find(r => r.executionId === base.executionId && r.recordId === base.recordId) || null;
          base.selectionBasis = 'Exact ' + kind + ' completion-event execution_id + summary_record_id';
          if (selected) {
            base.status = 'available'; bindContent(selected);
            base.isPriorCompletion = task.status !== 'COMPLETED' && clock(task.updatedAt) > clock(event.raw.time);
            base.title = base.isPriorCompletion ? 'Previous completed ' + kind + ' result' : 'Referenced ' + kind + ' result';
            base.sourceRefs.push(selected.sourceRefId);
            base.reason = base.isPriorCompletion ? 'The task has a later non-completed observation. This is the retained earlier ' + kind + ' result; it is not a result for the current phase.' : 'The exact event-referenced record is retrieved. Other records of the same type remain candidates.';
          } else {
            base.status = 'pending'; base.title = 'Referenced ' + kind + ' summary not retrieved';
            base.reason = 'A completion event names this exact record, but it is absent from the current collection. Task completion and result availability are separate.';
          }
        }
      }
    } else if (candidates.length) {
      const candidate = candidates.slice().sort((a,b) => a.createdAt - b.createdAt || a.key.localeCompare(b.key)).at(-1);
      base.status = 'candidate'; base.title = 'Observed ' + kind + ' summary candidate'; bindContent(candidate);
      base.recordId = candidate.recordId; base.executionId = candidate.executionId;
      base.selectionBasis = 'Latest created candidate; scoped key breaks timestamp ties; no completion pointer';
      base.reason = 'This ' + kind + ' candidate is available for review. No captured completion event identifies an authoritative final result.';
      base.sourceRefs = [candidate.sourceRefId];
    } else if (['TIMED_OUT', 'FAILED', 'CANCELED', 'SKIPPED'].includes(task.status)) {
      base.reason = 'No ' + kind + ' summary reference was observed for this terminal outcome. Available records and collection gaps remain inspectable.';
    }
    base.candidates = candidates.map(r => ({ recordId: r.recordId, executionId: r.executionId, title: sources[r.sourceRefId].title, timestamp: r.timestamp, selected: !!selected && r.key === selected.key, sourceRefId: r.sourceRefId, revisionId: r.revisionId, revisionCount: r.revisionCount }));
    return projection(base, kind + '-result', sources);
  }
  function coverageFor(meta, executions, records, step, now, summary) {
    const scope = D.scopes.find(s => s.key === meta.scopeKey);
    const isPrimary = taskKey(meta) === primaryKey();
    const isSupplier = meta.profile === 'supplier';
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
      status: gaps.length ? 'partial' : 'complete', label: count + ' of ' + rows.length + ' observed execution scopes without known gaps',
      paginationStatus: rows.some(r => r.paginationStatus === 'partial') ? 'partial' : 'complete',
      completeJournalQueries: rows.filter(r => r.paginationStatus === 'complete').length,
      asOf, freshness: Date.parse(now) - Date.parse(asOf) > 60000 ? 'stale' : 'current',
      executions: rows, gaps,
      note: 'Coverage is bounded to these observed execution journal queries and known evidence gaps; it does not prove all executions or external evidence were discovered. Exhausted pagination does not prevent future records. Artifact access is reported separately. Page outcomes are scripted demo observations, not a native consistency guarantee.'
    };
  }
  function metricsFor(meta, records) {
    // A later revision has a different observation ID but the same record lineage.
    const observed = (record,id) => record.sourceRefId === id || (record.sourceRefs || []).includes(id);
    if (meta.profile === 'supplier') return [];
    if (meta.profile === 'ledger') {
      const rec = records.find(r => observed(r,'jr-ledger-failover'));
      const alarm = records.find(r => observed(r,'jr-ledger-alarm'));
      return [{ id: 'ledger-retries', label: 'Worker retry rate', unit: rec.content.unit, aggregation: rec.content.statistic, query: rec.content.query, points: clone(rec.content.points), threshold: alarm.content.threshold, baseline: rec.content.points[0].value, sourceRefs: [rec.sourceRefId, alarm.sourceRefId], note: 'A historical synthetic observation window; no current database health inference. Baseline is the first published sample.' }];
    }
    const contributors = records.filter(r => ['jr-checkout-latency', 'jr-checkout-latency-2', 'jr-checkout-recovery'].some(id => observed(r,id)));
    const alarm = records.find(r => observed(r,'jr-checkout-alarm'));
    const points = contributors.flatMap(r => r.content.points).sort((a,b) => a.at.localeCompare(b.at));
    return [{ id: 'checkout-p95', label: 'Checkout request latency', unit: 'ms', aggregation: 'p95 · 120-second buckets', query: 'Demo CloudWatch request_duration · service=checkout-api · p95 · 120s buckets', points: clone(points), threshold: alarm.content.threshold, baseline: points.find(p => p.at === '2026-11-05T14:00:00Z')?.value ?? null, sourceRefs: [...contributors.map(r => r.sourceRefId), alarm.sourceRefId], note: 'Only published sample points are plotted. Baseline uses the pre-deployment sample at 14:00 UTC when present. Unobserved intervals are not additional measurements.' }];
  }
  function liveView(state, inputId) {
    assertState(state);
    const meta = metaFor(inputId || primaryKey());
    const scope = D.scopes.find(s => s.key === meta.scopeKey);
    const step = state.step; const now = D.scenario.stages[step].at;
    const taskRows = available(D.taskObservations, step).filter(r => r.scopeKey === meta.scopeKey && r.raw.taskId === meta.taskId);
    const taskRow = latest(taskRows);
    if (!taskRow) throw new RangeError('Current task observation is unavailable: ' + taskKey(meta));
    const task = clone(taskRow.raw);
    const membershipRows = available(D.memberships, step).filter(belongs(meta));
    const executionIds = new Set(membershipRows.map(r => r.executionId));
    const exRows = available(D.executionObservations, step).filter(r => r.scopeKey === meta.scopeKey && executionIds.has(r.raw.executionId));
    const recordRows = available(D.journalRecords, step).filter(r => r.scopeKey === meta.scopeKey && executionIds.has(r.raw.executionId));
    const events = available(D.lifecycleEvents, step).filter(r => r.scopeKey === meta.scopeKey && r.raw.detail.metadata.task_id === meta.taskId);
    const activeArtifacts = available(D.artifactDefinitions, step).filter(belongs(meta));
    const artifactRefs = new Set(activeArtifacts.flatMap(r => r.sourceRefs));
    const sources = Object.create(null);
    taskRows.forEach(r => addSource(sources, r, 'Native Task', key(meta.scopeKey, 'task', r.raw.taskId), r.raw.taskId, 'Task version ' + r.raw.version, 'GetBacklogTask', '', { agentSpaceId: scope.agentSpaceId, taskId: meta.taskId }));
    exRows.forEach(r => addSource(sources, r, 'Native Execution', key(meta.scopeKey, 'execution', r.raw.executionId), r.raw.executionId, D.executionLabels[r.raw.executionId], 'ListExecutions', '', { agentSpaceId: scope.agentSpaceId, taskId: meta.taskId }));
    recordRows.forEach(r => addSource(sources, r, 'Native JournalRecord envelope', key(meta.scopeKey, 'journal', r.raw.executionId, r.raw.recordId), r.raw.recordId, r.title, 'ListJournalRecords', '/content', { agentSpaceId: scope.agentSpaceId, executionId: r.raw.executionId }));
    events.forEach(r => addSource(sources, r, 'EventBridge notification', key(meta.scopeKey, 'eventbridge', r.raw.id), r.raw.id, r.raw['detail-type'], 'EventBridge delivery', '/detail'));
    available(D.assetObservations, step).filter(r => artifactRefs.has(r.id) && r.scopeKey === meta.scopeKey).forEach(r => addSource(sources, r, 'Native Asset', key(meta.scopeKey, 'asset', r.raw.assetId, r.raw.version), r.raw.assetId, 'Retrieved attachment version ' + r.raw.version, 'GetAsset', '', { agentSpaceId: scope.agentSpaceId, assetId: r.raw.assetId, assetVersion: r.raw.version }));
    available(D.assetFiles, step).filter(r => artifactRefs.has(r.id) && r.scopeKey === meta.scopeKey).forEach(r => addSource(sources, r, 'Native AssetFile', key(meta.scopeKey, 'asset-file', r.assetId, r.raw.version, r.raw.path), r.raw.path, r.raw.path + ' · version ' + r.raw.version, 'GetAssetFile', '/content/text', { agentSpaceId: scope.agentSpaceId, assetId: r.assetId, assetVersion: r.raw.version, path: r.raw.path }));
    const records = [...groups(recordRows, r => key(meta.scopeKey, 'journal', r.raw.executionId, r.raw.recordId)).values()].map(observations => {
      const r = latest(observations);
      const revisions = [...groups(observations, observation => sources[observation.id].revisionId).values()].map(rows => {
        const observed = latest(rows), source = sources[observed.id];
        return { revisionId: source.revisionId, payloadHash: source.payloadHash, sourceRefId: observed.id, observationIds: rows.map(row => row.id).sort(), observedAt: observed.observedAt };
      }).sort((a,b) => clock(a.observedAt) - clock(b.observedAt) || a.revisionId.localeCompare(b.revisionId));
      return Object.assign({}, clone(r.raw), {
        key: key(meta.scopeKey, 'journal', r.raw.executionId, r.raw.recordId), timestamp: toISO(r.raw.createdAt),
        preview: preview(r.raw.content), sourceRefId: r.id, revisionId: sources[r.id].revisionId,
        observedAt: r.observedAt, raw: clone(r.raw), revisions, revisionCount: revisions.length,
        observationCount: observations.length, sourceRefs: observations.map(row => row.id).sort(),
        revisionSelectionBasis: 'Latest collection observation; this is not an AWS record-version guarantee.'
      });
    }).sort((a,b) => a.createdAt - b.createdAt || a.key.localeCompare(b.key));
    const executions = [...groups(membershipRows, r => key(meta.scopeKey, 'execution', r.executionId)).values()].map(memberships => {
      const m = latest(memberships);
      const observation = latest(exRows.filter(r => r.raw.executionId === m.executionId));
      if (!observation) throw new RangeError('Execution membership has no retained execution observation: ' + m.executionId);
      const raw = clone(observation.raw); const children = records.filter(r => r.executionId === raw.executionId);
      return Object.assign({}, raw, {
        key: key(meta.scopeKey, 'execution', raw.executionId), label: D.executionLabels[raw.executionId],
        createdAtIso: toISO(raw.createdAt), updatedAtIso: toISO(raw.updatedAt), recordCount: children.length,
        recordIds: children.map(r => r.recordId), sourceRefs: [observation.id], membership: clone(m), membershipObservations: clone(memberships), raw
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
    }).sort((a,b) => clock(a.occurredAt) - clock(b.occurredAt) || a.id.localeCompare(b.id));
    const findings = available(D.findingDefinitions, step).filter(belongs(meta)).map(({ from, taskId, ...r }) => projection(r, 'finding', sources));
    const nodes = available(D.graphNodes, step).filter(belongs(meta)).map(({ from, taskId, ...r }) => projection(r, 'graph-node', sources));
    const edges = available(D.graphEdges, step).filter(belongs(meta)).map(({ from, taskId, ...r }) => projection(r, 'graph-edge', sources));
    const graph = { id: 'graph:' + taskKey(meta) + ':' + digest(canonical({ nodes, edges })), kind: 'evidence', title: 'Published evidence relationships', note: 'Relationships retain source attribution. An execution hierarchy is a separate graph; time order alone does not establish causality.', nodes, edges };
    const metrics = metricsFor(meta, records).map(item => projection(item, 'metric', sources));
    const results = Object.fromEntries(['investigation','mitigation'].map(kind => [kind, summaryFor(kind, taskKey(meta), task, records, events, sources)]));
    const summary = results.investigation;
    const artifacts = activeArtifacts.map(({ from, taskId, ...r }) => Object.assign(clone(r), { hash: r.body === null ? null : 'sha256:' + digest(r.body), hashEncoding: r.body === null ? null : 'utf8-content-bytes' }));
    if (metrics.length) {
      const metric = metrics[0];
      const body = 'timestamp,' + (metric.unit === 'ms' ? 'p95_ms' : 'retry_percent') + '\n' + metric.points.map(p => p.at + ',' + p.value).join('\n') + '\n';
      artifacts.push({ id: 'artifact-observed-metrics', name: 'Observed metric samples', filename: meta.taskId + '-observed-metrics.csv', kind: 'Derived export', mediaType: 'text/csv', status: 'available', sourceKind: 'Application projection', description: 'CSV generated only from the published mock observations shown in the chart.', body, hash: 'sha256:' + digest(body), hashEncoding: 'utf8-content-bytes', sourceRefs: metric.sourceRefs });
    }
    for (const result of Object.values(results)) if (result.status !== 'none') {
      const hasContent = ['available','candidate'].includes(result.status);
      const markdown = result.bodyFormat !== 'json';
      artifacts.push({ id: 'artifact-summary-' + result.kind + '-' + (result.executionId || 'unresolved') + '-' + (result.recordId || 'unresolved'), summaryKind: result.kind, executionId: result.executionId, recordId: result.recordId, name: result.status === 'candidate' ? result.kind + ' summary candidate' : result.isPriorCompletion ? 'Previous completed ' + result.kind + ' summary' : 'Referenced ' + result.kind + ' summary', filename: (result.recordId || result.kind + '-summary') + (markdown ? '.md' : '.json'), kind: result.status === 'candidate' ? 'Candidate summary' : 'Referenced summary', mediaType: markdown ? 'text/markdown' : 'application/json', status: hasContent ? 'available' : result.status === 'unresolved' ? 'unresolved' : 'pending', sourceKind: 'Journal record', description: result.reason, body: hasContent ? result.body : null, hash: hasContent ? 'sha256:' + digest(result.body) : null, hashEncoding: hasContent ? 'utf8-content-bytes' : null, sourceRefs: result.sourceRefs });
    }
    const projectedArtifacts = artifacts.map(item => projection(item, 'artifact', sources));
    const coverage = coverageFor(meta, executions, records, step, now, summary);
    const isPrimary = taskKey(meta) === primaryKey();
    const phase = isPrimary ? Object.assign({}, D.scenario.stages[step], { number: step + 1, total: D.scenario.stages.length }) : { id: task.status === 'COMPLETED' ? 'completed-case' : 'partial-case', title: task.status === 'COMPLETED' ? 'Completed investigation' : 'Timed out · evidence incomplete', description: meta.description, number: 1, total: 1 };
    return {
      id: meta.taskId, key: taskKey(meta), task, currentTaskSourceRefId: taskRow.id, meta: clone(meta), scope: clone(scope), now, phase,
      replay: { step: isPrimary ? step : 0, totalSteps: isPrimary ? D.scenario.stages.length : 1, canAdvance: isPrimary && step < D.scenario.stages.length - 1, stageLabels: isPrimary ? D.scenario.stages.map(s => s.title) : [phase.title], nextLabel: isPrimary && step < D.scenario.stages.length - 1 ? D.scenario.stages[step + 1].title : null },
      executions, records, timeline, findings, graph, metrics, summary, results, artifacts: projectedArtifacts, coverage, sources,
      counts: { executions: executions.length, running: executions.filter(e => e.executionStatus === 'RUNNING').length, records: records.length, artifacts: artifacts.length, availableArtifacts: artifacts.filter(a => a.status === 'available').length, timeline: timeline.length, findings: findings.length, completeExecutions: coverage.executions.filter(e => e.status === 'complete').length },
      observationCounts: { journalObservations: recordRows.length, journalRevisions: records.reduce((n,r) => n + r.revisionCount, 0), membershipObservations: membershipRows.length },
      snapshots: state.snapshots.filter(s => snapshotKey(s) === taskKey(meta)).map(snapshotMetadata), isSnapshot: false, snapshot: null, newActivity: false,
      provenance: { fixtureVersion: D.scenario.version, projectionVersion: PROJECTION, canonicalization: HASH_ENCODING, timestampEncoding: 'View clocks are ISO 8601; raw native envelopes preserve their modeled timestamp representation.', disclaimer: D.scenario.disclaimer }
    };
  }
  function sourceManifest(v) {
    return Object.values(v.sources).map(s => ({ observationId: s.id, sourceKey: s.sourceKey, revisionId: s.revisionId, payloadHash: s.payloadHash, observedAt: s.observedAt })).sort((a,b) => a.sourceKey.localeCompare(b.sourceKey) || a.revisionId.localeCompare(b.revisionId) || a.observationId.localeCompare(b.observationId));
  }
  function projectionItems(v) {
    return [...v.timeline, ...v.findings, ...v.graph.nodes, ...v.graph.edges, ...v.metrics, ...v.artifacts, ...Object.values(v.results || {})];
  }
  function comparisonFingerprint(v) {
    return hash({ key: v.key, task: v.task, sources: sourceManifest(v), memberships: v.executions.map(e => e.membershipObservations || [e.membership]), projections: projectionItems(v).map(r => r.projectionRevisionId || r), summary: v.summary, coverage: v.coverage });
  }
  function currentTaskSource(v) {
    const matches = Object.values(v.sources).filter(s => s.kind === 'Native Task' && s.scopeKey === v.scope.key && s.payloadHash === hash(v.task));
    return matches.find(s => s.id === v.currentTaskSourceRefId) || matches.slice().sort((a,b) => clock(a.observedAt) - clock(b.observedAt) || a.id.localeCompare(b.id)).at(-1);
  }
  function restoreState(value) {
    // Persisted JSON is an input boundary, not a trusted in-memory state. Retain
    // well-formed schema-1 captures from projection1.0 without rewriting them.
    let restored;
    try { restored = clone(value); } catch (_) { throw new TypeError('Saved demo state is not serializable JSON.'); }
    assertState(restored);
    for (const snapshot of restored.snapshots) {
      const v = snapshot.view, m = snapshot.manifest;
      const invalid = reason => { throw new TypeError('Invalid saved snapshot ' + snapshot.snapshotId + ': ' + reason + '.'); };
      if (m.viewHash && m.viewHash !== hash(v)) invalid('captured view hash mismatch');
      for (const [id, source] of Object.entries(v.sources)) {
        if (!source || source.id !== id || source.scopeKey !== v.scope.key || !own(source, 'payload') || source.payloadHash !== hash(source.payload)) invalid('source identity, scope, or content hash mismatch');
        if (![source.sourceKey + '@' + source.payloadHash.slice(7), source.sourceKey + '@' + source.payloadHash.slice(7,27)].includes(source.revisionId)) invalid('source revision mismatch');
      }
      const selectedTask = currentTaskSource(v);
      if (!selectedTask || v.currentTaskSourceRefId && v.currentTaskSourceRefId !== selectedTask.id) invalid('current task source does not match the captured task');
      const recordKeys = new Set();
      for (const record of v.records) {
        if (!record || typeof record.recordType !== 'string' || record.key !== key(v.scope.key, 'journal', record.executionId, record.recordId) || recordKeys.has(record.key) || !own(v.sources, record.sourceRefId)) invalid('journal identity or source mismatch');
        recordKeys.add(record.key);
        if (canonical(record.raw) !== canonical(v.sources[record.sourceRefId].payload) || record.revisionId !== v.sources[record.sourceRefId].revisionId || Object.keys(record.raw).some(field => canonical(record[field]) !== canonical(record.raw[field]))) invalid('journal payload differs from its retained source');
      }
      const nativeExecutions = new Set();
      for (const execution of v.executions) {
        if (!execution || execution.key !== key(v.scope.key, 'execution', execution.executionId) || nativeExecutions.has(execution.key) || !execution.membership || execution.membership.scopeKey !== v.scope.key || execution.membership.taskId !== v.id || !Array.isArray(execution.sourceRefs) || !execution.sourceRefs.length) invalid('execution identity or membership mismatch');
        nativeExecutions.add(execution.key);
        if (!execution.sourceRefs.some(id => own(v.sources,id) && canonical(v.sources[id].payload) === canonical(execution.raw))) invalid('execution source mismatch');
        if (Object.keys(execution.raw).some(field => canonical(execution[field]) !== canonical(execution.raw[field]))) invalid('execution payload differs from its retained source');
      }
      for (const item of projectionItems(v)) {
        if (!item || !Array.isArray(item.sourceRefs) || item.sourceRefs.some(id => !own(v.sources,id))) invalid('projection source is unavailable');
        if (item.payloadHash) { const { payloadHash, ...body } = item; if (payloadHash !== hash(body)) invalid('projection content hash mismatch'); }
      }
      for (const artifact of v.artifacts) {
        if (artifact.status === 'available' && (typeof artifact.body !== 'string' || artifact.hash !== 'sha256:' + digest(artifact.body))) invalid('artifact file hash mismatch');
        if (artifact.status !== 'available' && artifact.body !== null) invalid('unavailable artifact contains an unvalidated body');
      }
      if (['available','candidate'].includes(v.summary.status)) {
        const source = own(v.sources,v.summary.sourceRefId) && v.sources[v.summary.sourceRefId];
        const content = source && source.payload.content;
        if (!source || v.summary.executionId !== source.payload.executionId || v.summary.recordId !== source.payload.recordId || v.summary.body !== (typeof content === 'string' ? content : JSON.stringify(content,null,2))) invalid('summary differs from the selected source');
      }
      const actual = sourceManifest(v);
      const legacy = m.sources.every(s => !own(s,'observationId'));
      const expected = legacy ? actual.map(({ observationId, ...r }) => r) : actual;
      if (canonical(m.sources) !== canonical(expected)) invalid('manifest source set differs from the retained view');
      if (m.taskVersion !== v.task.version || m.taskStatus !== v.task.status || m.summaryPointer && (m.summaryPointer.executionId !== v.summary.executionId || m.summaryPointer.recordId !== v.summary.recordId)) invalid('manifest task or summary pointer mismatch');
      freeze(snapshot);
    }
    return restored;
  }
  function view(state, taskId, snapshotId) {
    assertState(state);
    if (!snapshotId) return liveView(state, taskId);
    const retained = state.snapshots.find(s => s.snapshotId === snapshotId);
    if (!retained) throw new RangeError('Snapshot does not belong to this investigation.');
    const requested = taskId || primaryKey();
    const requestedKey = requested === snapshotKey(retained) ? requested : taskKey(metaFor(requested));
    if (snapshotKey(retained) !== requestedKey) throw new RangeError('Snapshot does not belong to this investigation.');
    const result = clone(retained.view);
    result.isSnapshot = true; result.snapshot = snapshotMetadata(retained);
    result.currentTaskSourceRefId = result.currentTaskSourceRefId || currentTaskSource(result).id;
    if (!result.summary.bodyFormat && result.summary.sourceRefId && own(result.sources,result.summary.sourceRefId)) result.summary.bodyFormat = typeof result.sources[result.summary.sourceRefId].payload.content === 'string' ? 'markdown' : 'json';
    try {
      const current = liveView(state, requestedKey);
      result.newActivity = comparisonFingerprint(current) !== comparisonFingerprint(retained.view);
      result.liveObservationAvailability = 'available';
    } catch (error) {
      result.newActivity = null; result.liveObservationAvailability = 'unavailable';
      result.liveComparisonReason = 'Retained history is available, but the current view could not be assembled: ' + error.message;
    }
    return result;
  }
  function portfolio(state) {
    return D.taskMetadata.map(m => {
      const v = liveView(state, taskKey(m));
      return { taskId: v.id, key: v.key, code: v.meta.code, title: v.task.title, service: v.meta.service, owner: v.meta.owner, region: v.scope.region, status: v.task.status, priority: v.task.priority, updatedAt: v.task.updatedAt, recordCount: v.counts.records, coverageStatus: v.coverage.status };
    });
  }
  function captureSnapshot(state, taskId) {
    const current = liveView(state, taskId);
    if (state.nextSnapshotNumber === Number.MAX_SAFE_INTEGER) throw new RangeError('Snapshot counter exhausted; create a new demo state.');
    const n = state.nextSnapshotNumber++;
    const snapshotId = 'snapshot-' + String(n).padStart(3, '0');
    const metadata = { snapshotId, taskId: current.id, investigationKey: current.key, title: current.meta.code + ' · ' + current.phase.title, capturedAt: current.now, taskStatus: current.task.status, coverageStatus: current.coverage.status, recordCount: current.counts.records, stage: state.step };
    current.snapshots = []; current.isSnapshot = true; current.snapshot = clone(metadata); current.newActivity = false;
    const manifest = {
      snapshotId, investigationKey: current.key, captureStartedAt: current.now, captureFinishedAt: current.now,
      collectionAsOf: current.coverage.asOf,
      taskVersion: current.task.version, taskStatus: current.task.status, summarySelectionBasis: current.summary.selectionBasis,
      summaryPointer: { executionId: current.summary.executionId, recordId: current.summary.recordId },
      coverage: clone(current.coverage), executionMemberships: current.executions.flatMap(e => clone(e.membershipObservations)),
      sources: sourceManifest(current), projectionRevisionIds: projectionItems(current).map(r => r.projectionRevisionId),
      assetVersions: current.artifacts.filter(a => a.assetId && Number.isInteger(a.version)).map(a => ({ assetId: a.assetId, version: a.version, hash: a.hash })),
      projectionVersion: PROJECTION, fixtureVersion: D.scenario.version, canonicalization: HASH_ENCODING,
      viewHash: hash(current),
      note: 'Application snapshot of a non-transactional collection. Known gaps are retained; completion does not imply incident recovery.'
    };
    state.snapshots.push(freeze(Object.assign({}, metadata, { manifest, view: clone(current) })));
    return clone(metadata);
  }
  function advance(state) {
    assertState(state);
    state.step = Math.min(state.step + 1, D.scenario.stages.length - 1);
    if (state.step === 3 && !state.snapshots.some(s => snapshotKey(s) === primaryKey() && s.stage === 3)) captureSnapshot(state, primaryKey());
    return state.step;
  }
  function exportSnapshot(state, taskId, snapshotId) {
    const selected = view(state, taskId, snapshotId);
    const retained = snapshotId && state.snapshots.find(s => s.snapshotId === snapshotId && snapshotKey(s) === selected.key);
    return {
      schema: 'northstar.devops-investigation-export.v1', synthetic: true, exportedScenarioTime: selected.now,
      disclaimer: D.scenario.disclaimer,
      manifest: retained ? clone(retained.manifest) : { investigationKey: selected.key, sourceRevisions: sourceManifest(selected), taskVersion: selected.task.version, coverage: clone(selected.coverage), projectionVersion: PROJECTION, captureBasis: 'Current collected view; not a retained historical snapshot' },
      // A historical export is the captured payload. Live comparison metadata is
      // display state and must not rewrite that export after later observations.
      investigation: clone(retained ? retained.view : selected)
    };
  }
  function lookupSource(v, id) { return v && own(v.sources,id) ? clone(v.sources[id]) : null; }
  function validateData() {
    const errors = [];
    const allSources = [...D.taskObservations, ...D.executionObservations, ...D.journalRecords, ...D.lifecycleEvents, ...D.assetObservations, ...D.assetFiles];
    const sourceIds = new Set();
    allSources.forEach(r => { if (sourceIds.has(r.id)) errors.push('Duplicate source observation ID: ' + r.id); sourceIds.add(r.id); });
    for (let step = 0; step < D.scenario.stages.length; step++) {
      const state = createState(); state.step = step;
      for (const meta of D.taskMetadata) {
        let v;
        try { v = liveView(state, taskKey(meta)); } catch (e) { errors.push('Cannot assemble ' + taskKey(meta) + ' at ' + step + ': ' + e.message); continue; }
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
        [...projectionItems(v)].forEach(item => {
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
  return Object.freeze({ createState, restoreState, portfolio, view, advance, captureSnapshot, exportSnapshot, lookupSource, validateData });
});
