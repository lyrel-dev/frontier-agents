---
title: Investigation prototype model contract
date: '2026-11-05'
type: implementation-contract
status: implemented-design
tags:
  - aws/devops-agent
  - prototype
---

# Model contract

`mock-data.js` exports `DemoData`; `model.js` exports `DemoModel`. Both support browser globals and CommonJS. The fixture is entirely fictional. Native envelopes are kept separate from demo metadata and derived projections. Native journal/execution timestamps use Unix seconds; view timestamps use ISO 8601. The fixed simulation clock is displayed in `Europe/Zurich` by the UI.

## Public API

| Function | Result |
| --- | --- |
| `createState()` | New serializable state `{ schemaVersion, step, snapshots, nextSnapshotNumber }`. No browser storage dependency. |
| `portfolio(state)` | Three task rows: `{ taskId, key, code, title, service, owner, region, status, priority, updatedAt, recordCount, coverageStatus }`. |
| `view(state, taskId?, snapshotId?)` | A detached, task-scoped view. Default task is `DemoData.scenario.primaryTaskId`. A snapshot ID returns the retained view. |
| `advance(state)` | Mutates `state.step` to the next of six stages and returns the new step; clamped at the final stage. Preserves snapshots. |
| `captureSnapshot(state, taskId?)` | Captures and freezes the current view, adds it to state, returns metadata containing `snapshotId`. |
| `exportSnapshot(state, taskId?, snapshotId?)` | Returns a detached JSON-serializable export object. Historical exports use their retained source and projection data. |
| `lookupSource(view, sourceRefId)` | Source object with `id`, `kind`, `title`, `nativeId`, `revisionId`, `observedAt`, `locator`, `payloadHash`, `payload`, and optional native operation/query context; returns `null` if unavailable. |
| `validateData()` | Array of fixture relationship errors; empty means valid. |

Selection, filters, active tab, replay timer, and dialogs belong to the frontend. Recreating state resets the scenario. All state changes are local simulation; no AWS mutations occur.

## `view` shape

```javascript
{
  id, key, task, // task is the native Task envelope
  meta: { code, service, owner, region, accountId, spaceName, description },
  scope: { key, partition, accountId, region, agentSpaceId, name },
  now, // fixed scenario timestamp as ISO string
  phase: { id, title, description, number, total },
  replay: { step, totalSteps, canAdvance, stageLabels, nextLabel },
  executions: [{ key, executionId, parentExecutionId, agentSubTask, agentType,
    executionStatus, createdAt, updatedAt, createdAtIso, updatedAtIso,
    label, recordCount, recordIds, sourceRefs, raw }],
  records: [{ key, recordId, executionId, recordType, createdAt, content,
    timestamp, preview, sourceRefId, revisionId, observedAt, raw }],
  timeline: [{ id, projectionRevisionId, title, body, category, phase,
    occurredAt, recordedAt, observedAt, origin, sourceRefs, executionId }],
  findings: [{ id, title, summary, disposition, origin, sourceRefs }],
  graph: {
    id, kind, title, note,
    nodes: [{ id, label, subtitle, kind, origin, sourceRefs }],
    edges: [{ id, source, target, label, kind, origin, sourceRefs }]
  },
  metrics: [{ id, label, unit, aggregation, query, points: [{ at, value }],
    threshold, baseline, sourceRefs, note }],
  summary: { status, title, body, recordId, executionId, sourceRefId,
    isPriorCompletion, selectionBasis,
    reason, sourceRefs, candidates: [{ recordId, title, timestamp, selected }] },
  artifacts: [{ id, name, filename, kind, mediaType, status, sourceKind,
    description, body, assetId, version, hash, hashEncoding, sourceRefs }],
  coverage: { status, label, paginationStatus, completeJournalQueries,
    asOf, freshness, note, gaps,
    executions: [{ executionId, label, status, paginationStatus, pagesRead, hasMore,
      recordCount, observedAt, reason }] },
  counts: { executions, running, records, artifacts, availableArtifacts,
    timeline, findings, completeExecutions },
  sources: { [sourceRefId]: sourceObject },
  snapshots: [{ snapshotId, taskId, title, capturedAt, taskStatus,
    coverageStatus, recordCount, stage }],
  isSnapshot, snapshot, newActivity,
  provenance: { fixtureVersion, projectionVersion, timestampEncoding, disclaimer }
}
```

`summary.status` is `none`, `candidate`, `pending`, or `available`. `artifacts[].status` is `available`, `pending`, `access_denied`, or `unresolved`. `coverage.status` is `complete` or `partial`; freshness is a separate `current`/`stale` observation. `category` is `lifecycle`, `agent`, `evidence`, `conversation`, or `collection`. All `sourceRefs` entries are strings resolving in `view.sources`.

Optional native fields stay absent; optional view-only display fields can be `null`. A missing summary pointer is distinct from a supplied pointer whose record is not retrieved. `STOPPED` remains the native execution state, without a success inference.

`coverage.status` combines known evidence gaps; `paginationStatus` separately states whether the observed journal queries are exhausted. Thus the supplier investigation has complete journal pagination and incomplete external evidence. `summary.isPriorCompletion` identifies the earlier referenced result displayed while the same task is active again. Source/projection payload hashes use SHA-256 over canonical JSON. Artifact `hash` values use SHA-256 over the UTF-8 file body (`hashEncoding: "utf8-content-bytes"`), matching the downloaded Markdown/CSV bytes. Source objects identify `hashEncoding: "canonical-json-utf8"`.

## Replay stages

1. **Investigating**: open task, partial journal collection, latency evidence.
2. **Evidence correlated**: published finding, metric correlation, candidate summary.
3. **Completed · result pending**: native task completed; EventBridge points to an exact summary not collected yet.
4. **Result retrieved**: authoritative summary found, complete history; an automatic historical checkpoint is captured if none exists for this stage.
5. **Investigation resumed**: the same task returns to active work with a new execution; earlier snapshot remains unchanged.
6. **Follow-up complete**: a later summary and additional observations become available; earlier snapshots are preserved.

The primary case is a checkout latency incident. The other cases are a completed database investigation and a timed-out investigation with partial evidence. Investigation priority is native task priority; it is not labeled incident severity.
