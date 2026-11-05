---
title: Investigation prototype model contract
date: '2026-11-05'
type: implementation-contract
status: implemented-design
model_version: '1.1.0'
tags:
  - aws/devops-agent
  - prototype
---

# Model contract

`mock-data.js` exports `DemoData`; `model.js` exports `DemoModel`. Both support browser globals and CommonJS. This is an **in-process JavaScript API over a fixed, fictional fixture**. It is not an HTTP service, AWS SDK wrapper, generic journal parser, or implemented production collector. The native AWS operations and the proposed backend HTTP boundary are documented separately in the [API catalog](../annexes/Investigation_API_Catalog.md) and [UI contract](../annexes/Investigation_UI_Contract.md).

Native envelopes are kept separate from demo metadata and derived projections. Native journal/execution timestamps use Unix seconds; view timestamps use ISO 8601. The fixed simulation clock is displayed in `Europe/Zurich` by the UI. Scenario controls represent observations chosen for this presentation; they do not establish a supported native transition recipe.

## Public API

| Function | Result |
| --- | --- |
| `createState()` | New serializable state `{ schemaVersion, step, snapshots, nextSnapshotNumber }`. No browser storage dependency. |
| `restoreState(value)` | Validates persisted schema-1 state, returns a detached copy, and deeply freezes retained captures. Throws `TypeError` for incomplete snapshots, duplicate identities, inconsistent counters/scopes, or content/manifest hash mismatches. |
| `portfolio(state)` | Three task rows: `{ taskId, key, code, title, service, owner, region, status, priority, updatedAt, recordCount, coverageStatus }`. |
| `view(state, investigationKey?, snapshotId?)` | A detached, scoped view. Default is `DemoData.scenario.primaryInvestigationKey`. A snapshot ID returns retained content even when current collection is unavailable. |
| `advance(state)` | Mutates `state.step` to the next of six stages and returns the new step; clamped at the final stage. Preserves snapshots. |
| `captureSnapshot(state, investigationKey?)` | Captures and freezes the current view, adds it to state, and returns metadata containing `snapshotId` and `investigationKey`. |
| `exportSnapshot(state, investigationKey?, snapshotId?)` | Returns a detached JSON export. Historical export content is byte-stable across later replay stages; transient live-comparison metadata is excluded from the retained payload. |
| `lookupSource(view, sourceRefId)` | Returns a detached source observation with exact payload, source/revision identity, observation time, locator, hash, and operation/query context; returns `null` for an unavailable ID, including inherited JavaScript property names. |
| `validateData()` | Returns detected fixture relationship and time errors. An empty array means these checks passed; this is not a complete native AWS schema validator. |

The selection argument accepts a native task ID only when it is unambiguous within the fixture, for compatibility. A repeated ID across Agent Spaces raises `RangeError`; callers must use the `key` returned by `portfolio`. Unknown investigations and snapshots belonging to another scoped investigation also raise `RangeError`. Invalid in-memory state raises `TypeError`; these synchronous errors are not HTTP status codes. Snapshot ID allocation rejects inconsistent counters before appending a capture.

Selection, filters, active tab, replay timer, and dialogs belong to the frontend. Recreating state resets the scenario. All changes are local simulation; no AWS mutations occur. `restoreState` accepts the persisted **state object**, not an exported investigation document. Portable export is implemented; importing arbitrary external investigation exports is not.

## `view` shape

```javascript
{
  id, key, task, currentTaskSourceRefId, // id is native; key includes scope
  meta: { taskId, scopeKey, profile, code, service, owner,
    region, accountId, spaceName, description },
  scope: { key, partition, accountId, region, agentSpaceId, name },
  now, // fixed scenario timestamp as ISO string
  phase: { id, title, description, number, total },
  replay: { step, totalSteps, canAdvance, stageLabels, nextLabel },
  executions: [{ key, executionId, parentExecutionId, agentSubTask, agentType,
    executionStatus, createdAt, updatedAt, createdAtIso, updatedAtIso,
    label, recordCount, recordIds, sourceRefs, membership,
    membershipObservations, raw }],
  records: [{ key, recordId, executionId, recordType, createdAt, content,
    timestamp, preview, sourceRefId, revisionId, observedAt, raw,
    sourceRefs, revisionCount, observationCount, revisionSelectionBasis,
    revisions: [{ revisionId, payloadHash, sourceRefId,
      observationIds, observedAt }] }],
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
  results: { investigation: resultObject, mitigation: resultObject },
  summary: resultObject, // compatibility alias of results.investigation
  // resultObject includes:
  // { id, kind, recordType, status, referenceStatus, title, body,
  //   bodyFormat, rawContent, recordId, executionId, sourceRefId,
  //   isPriorCompletion, selectionBasis, reason, sourceRefs,
  //   completionReferences, candidates, projectionRevisionId,
  //   derivationId, payloadHash }
  artifacts: [{ id, name, filename, kind, mediaType, status, sourceKind,
    description, body, assetId, version, hash, hashEncoding, sourceRefs,
    summaryKind, executionId, recordId }],
  coverage: { status, label, paginationStatus, completeJournalQueries,
    asOf, freshness, note, gaps,
    executions: [{ executionId, label, status, paginationStatus, pagesRead, hasMore,
      recordCount, observedAt, reason }] },
  counts: { executions, running, records, artifacts, availableArtifacts,
    timeline, findings, completeExecutions },
  observationCounts: { journalObservations, journalRevisions,
    membershipObservations },
  sources: { [sourceRefId]: sourceObject },
  snapshots: [{ snapshotId, taskId, investigationKey, title, capturedAt, taskStatus,
    coverageStatus, recordCount, stage }],
  isSnapshot, snapshot, newActivity,
  liveObservationAvailability, liveComparisonReason, // historical comparison
  provenance: { fixtureVersion, projectionVersion, canonicalization,
    timestampEncoding, disclaimer }
}
```

This is an abbreviated shape, not JSON Schema. Optional fields are omitted when inapplicable. Timelines, findings, graph nodes/edges, metrics, result selections, and artifact descriptors also carry `projectionRevisionId`, `derivationId`, and `payloadHash`. All `sourceRefs` entries resolve to observations in `view.sources`; an observation resolves to an exact source revision. These references are application-owned and are not native journal fields.

## Identity, observations, and revisions

`view.id` is a native task ID; `view.key` is its canonical scoped application identity. The key builder appends percent-encoded type and opaque ID components to the existing scope key. For example, execution/record tuples `("a|b", "c")` and `("a", "b|c")` produce different journal keys. Callers compare complete keys and retain the original native IDs; they do not reconstruct AWS arguments by splitting keys.

All task selections, derived-item filters, historical membership checks, and snapshot lookups use the scoped identity. `currentTaskSourceRefId` points to the exact observation whose native payload is displayed in `view.task`, rather than the first task version collected.

The model distinguishes three counting units:

| Unit | Identity and behavior |
| --- | --- |
| Native journal record | One scoped Agent Space/execution/record tuple. Repeated pages do not increase `counts.records`. |
| Source revision | Source identity plus the hash of the parsed native envelope. Changed content is retained as another revision. |
| Collection observation | A distinct fixture observation ID and time. Repeated reads can observe the same revision. |

`records[].revisions` retains observed content renditions and their observation IDs. The current record uses the latest available collection observation, ordered by observation time with deterministic stage/ID ties. This is a local selection policy, **not an AWS record-version or consistency guarantee**. The original observations remain inspectable. Repeated execution membership observations similarly do not create additional executions; their listing contexts remain in `membershipObservations` and the capture manifest.

The fixed fixture's metric and finding profiles remain explicit application examples. This module does not infer a generic schema from an arbitrary journal payload. A production collector still needs validated parsers, concurrent-read ordering, source-authorization context, and section-specific collection outcomes.

## Result selection and availability

Each result kind is resolved independently. Only `Investigation Completed` selects `investigation_summary_md`; only `Mitigation Completed` selects `mitigation_summary_md`. Other lifecycle events remain evidence and cannot clear a prior selected result. A later mitigation result does not replace an investigation result.

| `referenceStatus` | Meaning |
| --- | --- |
| `not_observed` | No matching completion notification was captured. Same-kind records can be shown as candidates under the stated display policy. |
| `not_reported` | A captured completion omitted its summary reference. This is bounded to that completion/execution. |
| `exact` | The completion supplied a usable execution/record pair. Content may be available or still pending retrieval. |
| `unresolved` | A supplied pointer or ordering field cannot be interpreted safely, including an absent execution mapping or a malformed supplied ID. |
| `conflicting` | Equally timed completion notifications name different results. Arrival order does not resolve the conflict. |

`summary.status` is `none`, `candidate`, `pending`, `available`, or `unresolved`. Candidate selection uses the latest record creation time; the scoped key breaks ties only for deterministic presentation. This does not make a candidate authoritative. Completion references, candidate identities, and exact source observations remain available to explain selection.

`bodyFormat` is `markdown` for a string in the selected summary profile and `json` for an object, array, number, boolean, or null. `rawContent` preserves that JSON value. `available` means content was retrieved; it does not certify that a non-string value conforms to a rich document profile. Summary artifacts use matching Markdown/JSON media types and extensions. Unknown content is not silently cast into Markdown.

`isPriorCompletion` is true when the task has a later non-completed observation than the selected completion. It labels retained earlier results without interpreting an older task read as proof of a new phase. Native `STOPPED` remains an execution status with no success inference.

`artifacts[].status` is `available`, `pending`, `access_denied`, or `unresolved`. `coverage.status` is `complete` or `partial`, meaning the absence or presence of **known gaps in the observed execution journal scopes**. It is not a completeness claim for all executions, all external evidence, or the incident. `paginationStatus` separately describes the scripted journal query traversal. Freshness is a separate `current`/`stale` observation. The legacy field `counts.completeExecutions` counts observed execution scopes without known gaps; it does not count successfully completed executions.

Timeline `category` is `lifecycle`, `agent`, `evidence`, `conversation`, or `collection`. Optional native fields stay absent; view-only display fields can be `null`. All three timeline clocks retain their own meanings.

## Historical capture and persistence

Captures preserve native sources, their observation and revision identities, derived payloads, execution membership, selected pointers, coverage bounds, and retrieved asset versions. Manual capture may retain partial collection. The manifest records the fixed scenario capture time separately from the collection timestamp; neither is a real AWS transactional-snapshot guarantee.

Historical reading does not require current task collection to succeed. If comparison is unavailable, the retained view returns `liveObservationAvailability: "unavailable"`, an explanation, and `newActivity: null`. An unavailable comparison is not represented as “nothing changed.” When available, comparison includes source observations, memberships, result selection, derived renditions, and coverage—not only native content changes.

`restoreState` validates snapshot structure, scoped identities, counters, source hashes, native/source agreement, available artifact bytes, and manifest consistency. Newly captured views also have a whole-view hash. It returns detached state with deeply frozen snapshots. A checked-in original projection-1.0 saved-state fixture verifies that valid schema-1 captures remain readable without rewriting their retained content. Display adapters may add optional compatibility fields to a returned copy; a historical export uses the original captured payload.

Deep freezing protects ordinary in-process mutations through this API. It does **not** make browser storage immutable or authenticate an exported document. A user or another script can edit browser storage, replace an entire state object, or recompute hashes. There is no signed audit archive, server-owned retention, authenticated import, or multi-tab write-coordination protocol in this prototype.

## Hash contract

Source and projection `payloadHash` values are SHA-256 over the module's explicitly named `sorted-json-utf8/v1` representation: recursively sort object names by JavaScript UTF-16 string order, retain array order, serialize JSON primitives using `JSON.stringify`, add no whitespace, and hash the UTF-8 result. Inputs are parsed JSON values with finite numbers. Numeric-looking object names are sorted lexically; this is tested independently. No Unicode normalization is applied. This name identifies the local algorithm; it is not a claim of complete RFC8785 validation.

Source objects retain the older broad `hashEncoding: "canonical-json-utf8"` label and add the precise `canonicalization` identifier. New source and projection revision identities include the complete digest. Earlier captured truncated identifiers remain supported as historical identifiers.

Artifact `hash` values instead hash the UTF-8 downloadable file body (`hashEncoding: "utf8-content-bytes"`), matching exported Markdown/CSV/JSON bytes. Hashes of parsed native envelopes do not establish the exact original HTTP bytes, preserve arbitrary-precision JSON numbers beyond the JavaScript representation, authenticate AWS origin, or prove a claim true.

## Replay stages

1. **Investigating**: open task, partial journal collection, latency evidence.
2. **Evidence correlated**: published finding, metric correlation, candidate summary.
3. **Completed · result pending**: native task completed; EventBridge points to an exact summary not collected yet.
4. **Result retrieved**: exact referenced summary found, the chosen journal queries exhausted, and no known gaps in those observed scopes; an automatic historical checkpoint is captured if none exists for this stage.
5. **Investigation resumed**: the same task returns to active work with a new execution; earlier snapshot remains unchanged.
6. **Follow-up complete**: a later summary and additional observations become available; earlier snapshots are preserved.

The primary case is a checkout latency incident. The other cases are a completed database investigation and a timed-out investigation with partial evidence. Investigation priority is native task priority; it is not labeled incident severity.
