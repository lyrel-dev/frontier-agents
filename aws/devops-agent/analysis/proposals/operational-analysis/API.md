---
title: "Operational analysis: proposed RPC API"
id: operational-analysis-api-proposal
type: api-proposal
created: '2026-11-05'
updated: '2026-11-05'
status: proposed-unimplemented
model_version: '0.1'
tags:
  - operational-analysis
  - api-design
  - rpc
  - evidence
related:
  - README.md
  - AWS_EVIDENCE.md
  - DESIGN_REVIEW.md
---

# Operational analysis: proposed RPC API

This is a **proposed, unimplemented application contract** for the [seven-entity model](README.md). It follows the current [consolidated design principles](../../../../../consolidated-operations-console/DESIGN_PRINCIPLES.md) and [RPC protocol](../../../../../consolidated-operations-console/api/PROTOCOL.md). Its standalone namespace, `OperationalAnalysis_20261105`, is not a deployed AWS endpoint or an operation namespace already implemented by the consolidated console. Formal schemas and runtime enforcement remain implementation work.

## 1. One wire and version contract

| Concern | Proposed binding |
| --- | --- |
| Transport | `POST /`, request/success/error media type `application/x-amz-json-1.1` |
| Operation selector | `X-Amz-Target: OperationalAnalysis_20261105.<Operation>` |
| Names | PascalCase operations; lowerCamelCase JSON properties |
| Success | HTTP 200 with the operation-specific response, including durable queued admission |
| Failure | Non-2xx status, typed JSON exception, `x-amzn-ErrorType` and `x-amzn-RequestId` |
| Time | Finite UTC epoch seconds with at most millisecond precision; semantic intervals `[start, end)` |
| Authority | Workspace, actor and permissions established by trusted server context |

Every **Subject, Analysis, Assertion, QueryRun, Evidence, Assessment and Review** representation has `id`, `workspaceId`, positive server-assigned `version`, `createdAt` and `updatedAt`. Creation time remains constant; updatedAt records publication of that representation. Native event/capture times remain separate. Older versions are immutable.

Subject, Analysis and Assertion changes publish successor versions. QueryRun progress publishes successor versions of that same QueryRun; its owned specification, receipts, attempts, result manifest and coverage have no competing version counters. Evidence, Assessment and Review are append-only facts in this proposal and normally remain at version 1. Common versioning does not require public update commands for them.

Analysis.version changes only when its own definition/lifecycle changes. QueryRun progress does not change it. Updating an Assertion does not repoint the Analysis's pinned criterion binding automatically. A composed view selects exact entity versions; its publication sequence is a pagination/coherence boundary, not another entity version.

`EntityRef = {kind, id, version}` selects an exact representation. `EntityIdentity = {kind, id}` is reserved for explicit current navigation. Historical references never fall back to latest. Owned QuerySpec, AssertionResult and reference values acquire neither independent CRUD identities nor version-only entities.

## 2. Named operations and ownership

| Operation | Narrow input and effect |
| --- | --- |
| `CreateSubject` | Typed subject definition or binding to an existing authoritative catalogue; returns Subject version 1. |
| `UpdateSubject` | subjectId, expectedVersion and writable definition changes; publishes the next Subject version. |
| `CreateAnalysis` | Purpose, exact Subject references, interval and initially empty criterion bindings; create its owned Assertions, then bind their exact versions through UpdateAnalysis. |
| `UpdateAnalysis` | analysisId, expectedVersion and permitted metadata/definition/lifecycle changes. Closing is work management, not operational recovery. |
| `CreateAssertion` | analysisId, statement and typed EvaluationSpec; creates an analysis-owned Assertion. |
| `UpdateAssertion` | analysisId, assertionId, expectedVersion and statement/evaluation changes; preserves prior versions. |
| `StartQueryRun` | Exact analysisRef, specification and managed connectionRef; durably admits QueryRun version 1. |
| `RequestQueryCancellation` | queryRunId, expectedVersion and optional reason; records intent in a successor QueryRun version. |
| `GetQueryResult` | Exact queryRunRef; returns that version's owned receipt/result manifest, including failed or empty collection. |
| `IngestEvidence` | Registered capture/import/attestation profile and bounded content; authority determines trusted origin. |
| `CreateAssessment` | Exact analysisRef, input bindings, evidenceRefs and queryRunRefs; commits a bounded evaluation as Assessment version 1. |
| `RecordReview` | Exact assessmentRef, decision, rationale and optional cited evidence/superseded review reference; creates Review version 1. |
| `GetSubject`, `GetAnalysis`, `GetAssertion`, `GetQueryRun`, `GetEvidence`, `GetAssessment`, `GetReview` | Typed ID and optional version; omission explicitly selects the head once. Required parent identities must agree. |
| `ListSubjects`, `ListAnalyses`, `ListAssertions`, `ListQueryRuns`, `ListEvidence`, `ListAssessments`, `ListReviews` | Authorized, scoped stable pages of selected entity representations. |
| `ListEntityVersions` | EntityIdentity and pagination; exact EntityRefs in descending version order, with domain/history authorization. |
| `GetAnalysisView`, `ListTimeline` | Composed reads with selected exact references, labeled source clocks and publication context. They do not collect provider data. |

All mutations require clientToken. Updates are closed, operation-specific DTOs; a response entity is not an update body. Omitted fields are unchanged. Declared arrays replace their owned collection; nullable fields clear only through explicitly permitted clearFields. Assignment and clearing of the same field conflict. Unknown native values remain evidence with diagnostics; absent, null, empty and zero stay distinct. There is no direct QueryRun-state or computed-verdict patch. Rerunning creates another QueryRun; reevaluation creates another Assessment.

## 3. Durable query admission

This fictional example invokes an application adapter contract, not native AWS StartQuery:

```http
POST / HTTP/1.1
Content-Type: application/x-amz-json-1.1
X-Amz-Target: OperationalAnalysis_20261105.StartQueryRun
```

```json
{
  "clientToken": "query-checkout-errors-0001",
  "analysisRef": {"kind": "Analysis", "id": "analysis-checkout", "version": 3},
  "connectionRef": {"kind": "Connection", "id": "connection-prod-observer", "version": 2},
  "specification": {
    "adapterRef": "aws.cloudwatch.logs-insights@1",
    "subjectRefs": [{"kind": "Subject", "id": "subject-checkout", "version": 2}],
    "window": {"start": 1793869200, "end": 1793869500},
    "parameters": {
      "queryLanguage": "CWLI",
      "logGroupIdentifiers": ["arn:aws:logs:eu-central-1:000000000000:log-group:/example/checkout"],
      "queryString": "fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp asc | limit 1000"
    },
    "limits": {"timeoutSeconds": 60, "maxRows": 1000}
  }
}
```

Connection is an exact external reference to an existing access-management context, not an eighth entity introduced here. Admission and dispatch verify current permissions, connection validity and actual provider scope. The frozen QuerySpec retains resolved Subject/resource bindings, effective interval translation, access context, parameters and immutable adapter/schema versions. Aliases resolve once before dispatch; retries cannot select a different implementation. Limits are qualified collection bounds, not a guaranteed hard cloud-spending cap.

Successful admission returns HTTP 200:

```json
{
  "accepted": true,
  "queryRun": {
    "id": "query-checkout-01",
    "workspaceId": "workspace-example",
    "version": 1,
    "createdAt": 1793869560,
    "updatedAt": 1793869560,
    "analysisRef": {"kind": "Analysis", "id": "analysis-checkout", "version": 3},
    "state": "queued",
    "provider": null,
    "coverage": {"state": "not_started"}
  }
}
```

The excerpt omits the stored specification/receipt fields. It acknowledges durable admission, not AWS start or success. Later QueryRun versions retain native status separately from local collection state. A provider job can finish while result retrieval fails. Assessment pins one exact QueryRun version and its coherent result manifest; overlapping partial polls are not automatically unioned.

Cancellation is guarded by the current QueryRun version after replay handling. Acceptance publishes intent and dispatch fencing, not remote termination. A new request against the current sealed version returns accepted:false without change; a stale new request conflicts. Exact replay returns the original accepted representation. Lost start responses remain indeterminate and require non-creating reconciliation rather than duplicate dispatch.

## 4. Explicit assessment basis and operator decision

CreateAssessment does not accept a desired verdict. EvidenceRef adds locator and inputRole to exact kind/id/version. The role names the evaluator input; supporting/refuting/context stance belongs to the resulting citation.

```http
X-Amz-Target: OperationalAnalysis_20261105.CreateAssessment
```

```json
{
  "clientToken": "assessment-checkout-0001",
  "analysisRef": {"kind": "Analysis", "id": "analysis-checkout", "version": 3},
  "bindings": [{
    "instanceKey": "alarm-delivery-checkout-incident",
    "evidenceRefs": [
      {"kind": "Evidence", "id": "evidence-alarm-17", "version": 1, "locator": "/events/0", "inputRole": "transitions"},
      {"kind": "Evidence", "id": "evidence-sns-92", "version": 1, "locator": "/", "inputRole": "envelopes"},
      {"kind": "Evidence", "id": "evidence-receiver-12", "version": 1, "locator": "/", "inputRole": "deliveries"}
    ]
  }],
  "queryRunRefs": [
    {"kind": "QueryRun", "id": "query-alarm-01", "version": 5},
    {"kind": "QueryRun", "id": "query-receiver-01", "version": 4}
  ],
  "includeRequirementRollup": true
}
```

The server freezes all expected instances from the selected Analysis version: exact Assertion versions, targets, intervals and phases. Supplied bindings cannot shrink that set. Missing bindings yield inconclusive results; unknown/mismatched instance references reject. Empty evidence selection can truthfully yield inconclusive results; an Assessment must select at least one assertion instance.

Assessment stores the exact evidence/run references, frozen receipts/failures and coverage, resolved scope, knowledge cutoff and evaluator/runtime contracts. At admission the backend freezes the local publication cutoff; every selected reference must exist by that cutoff. Exact references govern inputs, not a query for latest state. Authorized cross-analysis reuse preserves original origin and capture time. Bounded evaluation commits the immutable result before returning success; longer reasoning first supplies attributed evidence through an explicit acquisition workflow.

Verdicts are supported, refuted, inconclusive and not_applicable. Conflict is an inconclusive reason. Only policy-designated required requirements enter a requested rollup; diagnostic hypotheses do not. Known required refutation dominates other missing inputs. Empty required sets and empty/unresolved target domains cannot produce readiness success. Without a requested rollup, omit it.

```http
X-Amz-Target: OperationalAnalysis_20261105.RecordReview
```

```json
{
  "clientToken": "review-checkout-operator-0001",
  "assessmentRef": {"kind": "Assessment", "id": "assessment-checkout-01", "version": 1},
  "decision": "request_evidence",
  "rationale": "Obtain a correlated receipt for the intended operations endpoint."
}
```

Decisions are accept, challenge and request_evidence. The backend assigns actor and recorded time. Accepting an accurate refutation does not make the service compliant. An optional supersedesReviewRef identifies an earlier decision about that same Assessment by the same reviewer; other reviewers' decisions remain independent.

Manual judgment enters through an attributed manual-attestation Evidence profile, with trusted submission actor/channel and preserved rationale/citations. A pinned human-attestation evaluator interprets it under the Assertion's policy. It is not relabeled native measurement. Review remains a separate act.

## 5. Provenance, history and pagination

A caller may submit claimed provenance, not manufacture trusted producer authority. IngestEvidence distinguishes verified collector context from imported claimed origin/capture time. Imports preserve those original claims and their verification status, recording actual ingestion actor/time separately. Verified migrations retain established original provenance. Neither operation replaces an old capture time with today's import time or authenticates a claim merely because its schema is valid.

References and digests confer no access. Exact historical reads, evidence closures and payload downloads recheck current authorization. Unknown/invisible versions fail rather than falling back to head. Retention/redaction returns an explicit unavailable result; a current payload is never substituted. A collector's access-denied observation can explain a gap; a caller forbidden from the input receives an authorization error before assessment admission.

Lists use maxResults 1–100, default 20, and opaque nextToken. The first page freezes exact entity versions. Tokens bind workspace, principal/authorization context, operation, parents, filters, ordering and local publication. They expire after 15 minutes without extension. Expiry requires explicit restart/resynchronization; native continuation tokens remain adapter internals.

```json
{
  "items": [],
  "page": {"publicationSequence": 84, "expiresAt": 1793870700}
}
```

A top-level nextToken appears only when traversal continues; an empty page alone does not end it. publicationSequence is read coherence, not an entity clock. Historical Analysis reads return that version's definition; reproducible conclusions use exact Assessment references rather than joining current children. Initial live updates use polling, with no unimplemented streaming-replay guarantee.

## 6. Replay, concurrency and typed errors

Processing order is authenticate/authorize, compare/reserve token, return exact replay, then check fresh-command preconditions. Replay identity is trusted workspace, principal, operation and clientToken. Canonical intent includes exact references and expectedVersion. Changed intent under one token conflicts. Replay returns the original result versions; GET without version explicitly navigates to current state.

Named updates and cancellation use expectedVersion for their entity owner. Owned values have no independent guard. Matching replay precedes this comparison; current authorization always applies. QueryRun admission/cancellation receipts remain for the run's lifetime and at least 90 days after sealing; unresolved dispatch prevents automatic expiry. Other creation receipts remain while their resources are retained, and authoring receipts remain at least 24 hours. In-flight matching commands return a typed conflict, any known entityRef and retry delay. These protocol receipts introduce no Command entity. After expiry, reconcile before creating new work. Local versions/idempotency do not provide distributed AWS compare-and-swap or provider exactly-once effects.

```json
{
  "__type": "VersionConflictException",
  "code": "EXPECTED_VERSION_MISMATCH",
  "message": "Read the current Analysis before issuing a different edit.",
  "requestId": "request-example-01",
  "retryable": false
}
```

Use 400 ValidationException for malformed/invalid inputs; 401/403 for authentication/authorization; 404 for unknown/invisible identity/version; 409 for version, intent or state conflicts; 410 for expired pagination/unavailable evidence; 413/415 for size/media errors; 429/503 for throttling/transient availability; and 500 for internal failure. Stable codes and field paths guide recovery. Successfully reading a failed QueryRun returns HTTP 200 with its technical error/coverage, never a fabricated empty result.

## 7. Contract provenance

The [current consolidated correction](../../../../../consolidated-operations-console/DESIGN_PRINCIPLES.md) governs common versioning and RPC. Earlier [FIS ownership/replay rules](../../../../fis/analysis/workflow/api.md), [Resilience evidence boundaries](../../../../resilience-hub/analysis/api/protocol.md) and [validation-console evaluation semantics](../../../../../applications/aws-validation-console/docs/DESIGN.md) supply useful context where compatible. The former REST binding, independent authoring counters and result epochs are superseded here; they are not claimed as current user preferences or wire-compatible alternatives.
