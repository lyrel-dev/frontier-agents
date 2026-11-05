---
id: assessment-workflow-api
title: Assessment workflow API contract
status: reviewed-proposal
version: "0.2"
updated: "2026-11-05"
---

# Assessment workflow API contract

The API exposes authoring commands and immutable revisions, then a durable Run with read-only execution children and evidence. It does not allow a client to manufacture success by updating an outcome or retry an individual native FIS action.

This is a **proposed contract**, not an implemented server. The command names below define intent independently of transport. The HTTP binding preserves the resource-oriented interface proposed earlier and uses one consistent set of rules. The neighboring repository's RPC facade is a useful contract precedent; adopting its transport would be a separate product decision, not a reason to weaken these semantics.

## 1. Operations and writable ownership

All paths below have the `/v1` prefix. All JSON property names use lowerCamelCase. IDs are opaque strings; step keys use `[a-z][a-z0-9_]{0,63}`. Timestamps are RFC 3339 UTC strings with explicit `Z`. Durations in authoring use integer seconds with named `*Seconds` properties, avoiding ambiguous month/year durations.

| Operation | HTTP binding | Request fields | Response and effect |
| --- | --- | --- | --- |
| `CreateScenario` | `POST /scenarios` | `clientToken`, `displayName`, optional `description` | 201, Scenario, Location. Creates metadata only. |
| `GetScenario` | `GET /scenarios/{scenarioId}` | Path identity | 200, Scenario, strong ETag. |
| `ListScenarios` | `GET /scenarios` | Pagination; optional `archived` filter | 200, stable page of Scenario summaries. |
| `UpdateScenario` | `PATCH /scenarios/{scenarioId}` | `clientToken`; one or more of `displayName`, `description`, `defaultRevisionId`, `archived`; If-Match required | 200, updated Scenario, new ETag. No revision body or execution fields. |
| `PublishScenarioRevision` | `POST /scenarios/{scenarioId}/revisions` | `clientToken`, `document` conforming to authoring schema | 201, immutable revision and resolved lock, Location. Compilation is bounded and completes before publication. |
| `GetScenarioRevision` | `GET /scenarios/{scenarioId}/revisions/{scenarioRevisionId}` | Path identities, which must agree | 200, exact revision source, compiled definitions, lock and digest. |
| `ListScenarioRevisions` | `GET /scenarios/{scenarioId}/revisions` | Pagination | 200, immutable revision summaries. |
| `StartRun` | `POST /runs` | `clientToken`, `scenarioRevisionId`, `subject`, `inputs`, `bindings` | 201, durably queued Run, Location. No promise that execution or an AWS call has started. |
| `GetRun` | `GET /runs/{runId}` | Path identity | 200, Run projection, ETag, observation and projection provenance. A failed Run still returns 200. |
| `ListRuns` | `GET /runs` | Pagination; optional exact `scenarioId`, `deploymentRef`, `phase` filters | 200, summary page with projection version. |
| `RequestRunCancellation` | `POST /runs/{runId}:cancel` | `clientToken`, optional `reason` | 202 when accepted for an unsealed Run; 200 for an already sealed Run. Returns a durable receipt and current Run location. |
| `ListRunSteps` | `GET /runs/{runId}/steps` | Pagination | 200, all named step projections, including zero-attempt skipped steps. |
| `ListStepAttempts` | `GET /runs/{runId}/steps/{stepKey}/attempts` | Pagination | 200, immutable/active attempt facts in ascending attempt number. |
| `ListRunEvidence` | `GET /runs/{runId}/evidence` | Pagination; optional exact `stepKey`, `schemaRef` filters | 200, evidence envelopes. Large bodies remain artifact references. |
| `GetEvidence` | `GET /runs/{runId}/evidence/{evidenceId}` | Both identities must agree | 200, immutable envelope and access-checked content/reference. |
| `ListOperations` | `GET /operations` | Pagination; optional namespace filter | 200, operation contracts/capabilities visible to the caller. Visibility is not execution authorization. |

Archiving is explicit Scenario metadata. v0.2 has no general destructive delete API, arbitrary status PATCH, independent action-stop endpoint, per-step retry command or mutable Evidence update. A rerun is a new StartRun with a new token and a pinned revision. Historical data has a retention policy, not cascading deletion through a friendly-name resource.

For UpdateScenario, omitted fields preserve their values. `description: null` clears the description and `defaultRevisionId: null` clears the default pointer; null is invalid for the other writable fields. An empty description string is a known empty value. The default revision must belong to this Scenario. The run request always names a revision explicitly; changing the default pointer cannot redirect an already prepared request.

## 2. Admission request and response

```json
{
  "clientToken": "2b8b98c6-06d8-4cd3-8899-ff506d33ee96",
  "scenarioRevisionId": "scnrev_alarm_delivery_002",
  "subject": {
    "deploymentRef": "deployment_checkout_prod_euc1",
    "expectedDeploymentRevision": "release_2026_11_05"
  },
  "inputs": {
    "templateId": "EXT-synthetic00000001",
    "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-errors",
    "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
    "receiverId": "checkout-alarm-probe"
  },
  "bindings": {
    "aws": "connection_checkout_test",
    "receiver": "connection_dedicated_alarm_probe"
  }
}
```

`inputs` is validated against the revision's closed input schema. `bindings` may contain only names declared by that revision. Each value references a server-managed connection; it cannot contain credentials, a caller-selected IAM role to assume, an arbitrary endpoint or an executable script. `subject` is required even for read-only assessments so scope and authorization remain reviewable.

Admission atomically reserves the client token, checks authorization and expected inventory revision, validates the locked program and resolves references, then commits the Run and its immutable snapshot. Failures before durable admission create no Run and no provider side effect. Scope validation must check provider account/Region/resource constraints against the deployment policy. Merely attaching `deploymentRef` to a request does not constrain a FIS template's targets.

Provider selectors can resolve at execution time. The snapshot records the configured scope; actual selected membership is later evidence. If the product cannot constrain a provider operation to its authorized scope, admission or dispatch must reject it. It must not label a preview as proof that a later target set is identical.

```json
{
  "runId": "run_01_synthetic",
  "scenarioRevisionId": "scnrev_alarm_delivery_002",
  "execution": {
    "phase": "queued",
    "outcome": null,
    "reasons": []
  },
  "assessment": {
    "verdict": "inconclusive",
    "final": false,
    "requiredCount": 2,
    "passedCount": 0,
    "failedCount": 0,
    "inconclusiveCount": 0,
    "pendingCount": 2
  },
  "finalization": {
    "status": "not_started",
    "unresolvedEffects": []
  },
  "createdAt": "2026-11-05T09:00:00Z",
  "projection": {
    "version": 1,
    "reducerVersion": "assessment-reducer/0.2",
    "asOfSequence": 1,
    "computedAt": "2026-11-05T09:00:00Z"
  }
}
```

The two required criteria are alarm transition and receiver receipt. Precondition checks are shown separately and do not count as evidence that the workload passed. A real response also links to the admission snapshot and scoped child collections; it need not inline large definitions or raw logs.

`finalization.status` is `not_started | running | complete | incomplete`. Complete means all required finalizers settled successfully and every tracked effect is known terminal or proven absent. It does not mean all workload recovery criteria passed. Finished Runs with unresolved effects expose `incomplete` and terminal execution outcome `indeterminate`.

## 3. Idempotency and concurrent writes

All mutations require `clientToken`, an opaque 16–128 character identifier chosen for one user intent. The durable deduplication key is `(workspace, principal, operation, clientToken)`. The canonical payload includes path identity, writable fields and semantically relevant conditional headers such as `If-Match`; JSON member order is irrelevant. Reuse with a different payload or precondition returns 409 `IdempotencyConflict`. A repeated HTTP request gets a new request ID but keeps the logical command identity.

Replay lookup occurs **before** mutable version checks and before resolving operation tags or current deployment bindings again. A successful replay returns the original command receipt, status code and resource identity; clients GET the resource for its current projection. It must not create a second revision/Run or change the revision lock because the world changed after the first request.

The proposed retention rule is concrete: run-creation and cancellation receipts are retained for the Run's lifetime, including at least 90 days after sealing; unresolved Runs/effects and their receipts cannot be purged automatically. Other authoring mutation receipts are retained for at least 24 hours. Responses include `idempotencyExpiresAt` when expiration is known. After the documented retention period there is no replay guarantee; clients must reconcile the referenced resource and obtain a new user intent before creating work. These are product retention choices, not AWS service guarantees.

Token reservation, side-effect intent and durable command receipt require atomic storage semantics. A request with an in-flight matching reservation returns 409 `CommandInProgress` with `Retry-After` and an available command/resource location; it does not run concurrently. Authorization is rechecked on replay so a stored response cannot bypass revoked access. Provider-call uncertainty is recorded by the StepAttempt rules in [the model](model.md); HTTP idempotency alone does not provide exactly-once cloud effects.

Scenario updates require a strong ETag in `If-Match`. Missing precondition returns 428; mismatch returns 412 without a write. A valid exact replay is returned before this comparison. Revisions, evidence and run execution facts are not editable. `expectedDeploymentRevision` is a separate admission comparison against the inventory system; it is not an ETag for AWS resources. These conditional request and 201/202 distinctions follow [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html).

## 4. Cancellation acceptance and races

```json
{
  "clientToken": "c2126bd9-ad48-46b0-9d97-fd601ec61b98",
  "reason": "Stop this assessment; customer traffic is elevated"
}
```

An accepted response has `accepted: true`, `acceptedAt`, `commandId`, `runId` and `statusUrl`. The acceptance transaction atomically sets the singleton cancellation intent and fences new main dispatch. It does not set the Run to cancelled immediately. Work dispatched before that fence can still be active; finalization must reconcile it.

If a different cancellation token arrives while cancellation is already accepted, it returns a receipt pointing to the existing intent without replacing its first reason, principal or accepted time. This is an idempotent convergence on one desired state, not an extra cancellation entity. Reusing an existing token with a different body still conflicts.

If normal completion seals the Run first, a new cancellation returns 200 with `accepted: false`, `reasonCode: RUN_ALREADY_FINISHED` and the current terminal projection. If cancellation acceptance wins the race before sealing, the terminal reducer includes that intent. An exact replay of an earlier accepted cancellation still returns its original 202 receipt after completion; GET reports the current outcome.

Do not retry an uncertain mutating Start operation after cancellation just to discover its handle: even an idempotent token can create new work if the original request never reached the provider. Use a reconciliation read that cannot create the effect. If none exists, record unknown remote disposition and retain the protective scope hold for operator resolution.

## 5. Read models, pagination and updates

Every list uses `pageSize` from 1 to 100, default 25, plus an opaque `pageToken`. The initial page freezes an ordered set of local record identities and versions for 15 minutes. The token binds workspace, principal, operation, parent identity, filters, order and snapshot sequence. Later pages preserve those parameters. Invalid tokens return 400; expired snapshots return 410 `PageSnapshotExpired`, requiring an explicit new traversal.

The response contains `items`, `snapshotSequence`, `observedAt`, and `nextPageToken` only when more items remain. Items in that traversal reflect the same local projection versions. The product does not claim an atomic snapshot across AWS APIs. Native pagination and detail hydration have separate collection coverage, and a missing list-summary field cannot erase already observed detail.

Run details expose source freshness independently of `computedAt`. Recomputing an old projection cannot make its source observations fresh. A production event feed may publish monotonic projection sequence numbers and support reconnection from a cursor, but v0.2's required public interface is polling GET. An unknown provider status remains raw evidence and maps to an unknown/indeterminate presentation; new provider values must not crash a client or silently count as success.

Artifact downloads require a fresh authorization decision. An Evidence envelope contains a stable reference, not a permanently valid signed URL. Retention expiration or redaction leaves an explicit unavailable reason; it must not retroactively change the original assertion result to passed. Reassessment that needs deleted evidence is inconclusive.

## 6. Errors and compatibility

Errors use `application/problem+json` with RFC 9457 `type`, `title`, `status`, `detail` and `instance`, plus `code`, `requestId` and optional `fieldErrors`. Human messages are not parsing contracts. A stable code and field path explain the actionable condition. [Problem Details specification](https://www.rfc-editor.org/rfc/rfc9457.html)

| HTTP status | Examples | Client action |
| --- | --- | --- |
| 400 | Malformed JSON, unsupported writable field, bad token or invalid scalar format | Correct the request. |
| 401 / 403 | Authentication absent / authorized identity lacks permission or binding scope | Establish appropriate access; do not retry as a transient failure. |
| 404 | Resource absent or not visible within trusted scope | Resolve the correct identity; no cross-workspace disclosure. |
| 409 | Token payload conflict, in-flight command, incompatible deployment revision, archived scenario | Reconcile the existing command/resource; change intent only deliberately. |
| 410 | Expired pagination snapshot or retained content no longer available | Start a new traversal or show unavailable evidence. |
| 412 / 428 | Stale / missing If-Match on authoring update | Fetch current Scenario and review before writing. |
| 422 | Valid JSON but invalid DAG, undeclared binding, unresolved lock, incompatible schema, invalid check role | Correct the authored contract; no provider work started. |
| 429 / 503 | Capacity or transient service availability | Respect Retry-After; reuse the same token for the same intent. |

Request schemas are closed and operation-specific. Output objects may add optional properties; tolerant clients preserve unknown provider vocabulary. Changing identity scope, units, verdict meaning, required request fields, pagination semantics or retry guarantees is a breaking contract change. A renamed operation requires a new API version or explicit alias, not an undocumented behavior swap.

The public API does not accept a role, tenant, projection version, raw credential, requested successful status or arbitrary provider URL from an untrusted caller. Read access to evidence and write access to a Run are separate permissions. A connection reference is authorized at admission and execution. The proposal's checks validate selected contracts, not these server enforcement mechanisms.
