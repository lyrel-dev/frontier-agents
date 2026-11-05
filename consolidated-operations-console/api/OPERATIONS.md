# Consolidated operations console — RPC operations

API version **2026-11-05** · namespace `ConsolidatedOperationsConsole_20261105` · **101 operations**

**Status: phase-one design contracts.** There is no HTTP server, provider adapter, authentication implementation, scheduler or executed cloud mutation in this package. The schemas, examples and validation make the proposed interface reviewable. [Protocol](PROTOCOL.md) defines the shared semantics; [model](../MODEL.md) defines authority and identity.

All calls use `POST /` with `application/x-amz-json-1.1` and `X-Amz-Target: ConsolidatedOperationsConsole_20261105.<Operation>`. Successful calls use HTTP 200, including durable asynchronous command receipts. `Command.state=SUCCEEDED` means that command's documented effect succeeded; it does not imply successful assessment, healthy workload or verified repair.

Exact request/response schemas are in [rpc.schema.json](rpc.schema.json). [operations.json](operations.json) records scope, permissions, provenance, delivery phase and errors. [examples.json](examples.json) contains one complete synthetic request/response for every operation. Inputs are closed writable DTOs. Responses refer directly to the canonical model shapes; clients tolerate optional future response members and raw future provider vocabulary.

## Module index

| Module | Operations | Read | Mutating |
| --- | ---: | ---: | ---: |
| [foundation](#foundation) | 31 | 20 | 11 |
| [workload](#workload) | 17 | 10 | 7 |
| [health](#health) | 8 | 8 | 0 |
| [resilience](#resilience) | 14 | 8 | 6 |
| [investigation](#investigation) | 15 | 12 | 3 |
| [workflow](#workflow) | 13 | 8 | 5 |
| [fis](#fis) | 3 | 2 | 1 |

## Common field conventions

`clientToken` is required for every mutation. `expectedVersion` addresses the exact mutable local record named by the operation, including nested enrichment/governance. `expectedSourceRevisionId` is a local observed-evidence precondition, never an AWS conditional-write guarantee. `maxResults` is 1–100, default 20; `nextToken` is an opaque authorization-bound snapshot cursor. No JSON body accepts the acting user, role or workspace ID.

In the field tables, **required** members are marked with `*`. Every operation-specific response schema is a closed local validation snapshot; this does not require clients to reject future optional response members. Empty/null/missing/unknown remain distinct. A getter returns a retained record, not an implicit new provider read.

## foundation

### GetWorkspace

`READ` · permission `console:ReadWorkspace` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| Empty body | Send `{}` |

**Response:** `workspace: Workspace`.

- Workspace comes exclusively from authenticated context; the request cannot select a tenant.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### GetConnection

`READ` · permission `console:ReadConnections` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` * | `Id` |

**Response:** `connection: Connection`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListConnections

`READ` · permission `console:ReadConnections` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `enabled` | `boolean` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Connection>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### CreateConnection

`LOCAL_COMMAND` · permission `console:ManageConnections` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `name` * | `string` |
| `provider` * | `aws` |
| `credentialBindingId` * | `Id` |
| `allowedScopes` * | `List<OwningScope>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `connection: Connection`.

- Binds an already registered secret/identity reference after authorization; accepts no credential bytes.
- Requested scopes are checked against the caller's grant and the binding's capabilities; references do not grant access.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### UpdateConnection

`LOCAL_COMMAND` · permission `console:ManageConnections` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `connectionId` * | `Id` |
| `name` | `string` |
| `credentialBindingId` | `Id` |
| `allowedScopes` | `List<OwningScope>` |
| `enabled` | `boolean` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `connection: Connection`.

- Changes local connection configuration only; existing observations retain their original authorization provenance.
- Revocation is checked on every later read, replay and dispatch; disabling a connection does not erase historical evidence.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### GetResource

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resourceId` * | `Id` |

**Response:** `resource: Resource`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListResources

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` | `Id` |
| `resourceType` | `string` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Resource>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetCollection

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |

**Response:** `collection: Collection`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListCollections

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` | `Id` |
| `subject` | `EntityRef` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Collection>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListReadAttempts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ReadAttempt>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Includes failed and empty reads; their absence from returned object rows must not erase collection evidence.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetSourceRevision

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `sourceRevisionId` * | `Id` |

**Response:** `sourceRevision: SourceRevision`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetObservation

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `observationId` * | `Id` |

**Response:** `observation: Observation`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetProjectionRevision

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `projectionRevisionId` * | `Id` |

**Response:** `projectionRevision: ProjectionRevision`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### GetSnapshot

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `snapshotId` * | `Id` |

**Response:** `snapshot: Snapshot`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetWorkItem

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `workItemId` * | `Id` |

**Response:** `workItem: WorkItem`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### GetCommand

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `commandId` * | `Id` |

**Response:** `command: Command`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListSourceRevisions

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `identity` | `SourceIdentity` |
| `profile` | `string` |
| `representation` | `SUMMARY/DETAIL/EVENT/STREAM/ARTIFACT/CONFIGURATION/LOCAL_EVIDENCE` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<SourceRevision>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Native peripheral resources are retained typed profiles, including FIS templates/catalogs and DevOps registrations/triggers/goals.
- Representation and source identity are explicit; matching hashes do not merge different logical source records.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListObservations

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `sourceRevisionId` | `Id` |
| `collectionId` | `Id` |
| `subject` | `EntityRef` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Observation>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListProjectionRevisions

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `subject` | `EntityRef` |
| `profile` | `EVALUATION/LIFECYCLE_EXPOSURE/INVESTIGATION_RESULT/SERVICE_STATUS/WORKSPACE_SUMMARY` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ProjectionRevision>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Returns immutable derivations. Current selection is a view; re-evaluation creates another revision and never rewrites a sealed Run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListSnapshots

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `subject` | `EntityRef` |
| `kind` | `INVESTIGATION/TOPOLOGY/POLICY_CONTEXT/LIFECYCLE_CATALOG/RUN_INPUT/EVALUATION_INPUT` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Snapshot>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListWorkItems

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `target` | `EntityRef` |
| `state` | `OPEN/ACKNOWLEDGED/IN_PROGRESS/RESOLVED/DISMISSED` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<WorkItem>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListCommands

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `subject` | `EntityRef` |
| `operation` | `string` |
| `state` | `ACCEPTED/DISPATCHING/RECONCILING/SUCCEEDED/FAILED/CANCELED/OUTCOME_UNKNOWN` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Command>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### StartCollection

`INGEST` · permission `console:Collect` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` * | `Id` |
| `queries` * | `List<CollectionQuery>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `collection: Collection`.

- Admits a finite exact query set from the registered read-only adapter catalog; unknown operations or unauthorized scope fail admission.
- queryKey uniqueness, canonical requestDigest, filter types and operation-specific bounds are validated against that registered adapter.
- Completion, pagination, hydration, resolution and claim coverage remain independent facts.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### RecordReadAttempt

`INGEST` · permission `console:IngestEvidence` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `readAttemptId` * | `Id` |
| `state` * | `SUCCEEDED/FAILED` |
| `endedAt` * | `Timestamp` |
| `providerRequestId` * | `string or null` |
| `returnedCount` * | `integer or null` |
| `nextTokenPresent` * | `boolean or null` |
| `error` * | `ReadError or null` |
| `requestSourceRevisionId` * | `Id` |
| `responseSourceRevisionId` * | `Id or null` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `readAttempt: ReadAttempt`.

- Settles the same existing STARTED ReadAttempt created by the trusted collector dispatch transaction before the actual read; does not append a second attempt or fabricate a pre-call record after the fact.
- Trusted context assigns authorizationContextKey; a caller cannot forge its acting principal or provenance.
- The requestSourceRevisionId must equal the already retained normalized request envelope for this attempt. Response envelope references must belong to this exact request and scope, including empty responses.
- IngestObservation may retain response/object observations while the attempt is STARTED; settlement then references those revisions. A response-lost failure has an explicit null response reference, not a fabricated empty response.
- A settled attempt is immutable. Exact replay returns the original result; conflicting terminal facts reject. Query identity, attemptNo, requestDigest, startedAt and authorization provenance are server-owned.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### IngestObservation

`INGEST` · permission `console:IngestEvidence` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `channel` * | `API/EVENTBRIDGE/STREAM/LOCAL` |
| `readAttemptId` * | `Id or null` |
| `connectionId` * | `Id or null` |
| `observedAt` * | `Timestamp` |
| `sourceTime` * | `Timestamp or null` |
| `transportTime` * | `Timestamp or null` |
| `expiresAt` * | `Timestamp or null` |
| `receiptKey` * | `string or null` |
| `source` * | `SourceRevisionInput` |
| `clientToken` * | `string` |

**Response:** `sourceRevision: SourceRevision`; `observation: Observation`; `command: Command`.

- Atomically retains or resolves the immutable source revision and appends this distinct receipt observation.
- The registered versioned profile validates typed known members, source identity, representation and digest; raw unknown provider output remains retained evidence.
- payload is the intentionally opaque provider document, bounded by the body cap and adapter schema; it cannot patch canonical state or set a verdict.
- The adapter reconciles canonical entity indexes through verified mappings. Digest equality alone is not event identity; receipt dedupe includes the authenticated channel/scope.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `EvidenceUnavailableException`.

### CompleteCollection

`INGEST` · permission `console:IngestEvidence` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `expectedProjectionVersion` * | `Version` |
| `coverage` * | `List<Coverage>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `collection: Collection`.

- Seals collection coverage after every declared query has a settled or explicitly unresolved outcome; referenced attempts must belong to this collection.
- A coverage conclusion must be justified by registered collector rules. Successful or exhausted pages cannot alone claim source sufficiency.
- expectedProjectionVersion fences this collector completion only; it is not a configuration edit version or AWS conditional write.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### PublishProjection

`DERIVE` · permission `console:PublishProjection` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `projectionKey` * | `string` |
| `profile` * | `EVALUATION/LIFECYCLE_EXPOSURE/INVESTIGATION_RESULT/SERVICE_STATUS/WORKSPACE_SUMMARY` |
| `profileVersion` * | `string` |
| `subjectRefs` * | `List<EntityRef>` |
| `inputRefs` * | `List<EvidenceRef>` |
| `ruleDigest` * | `Digest` |
| `asOf` * | `Timestamp` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `projectionRevision: ProjectionRevision`.

- Executes an authorized registered immutable rule over the exact immutable inputs and appends a derived revision.
- The request cannot supply value, generatedAt, coverage or a desired verdict. The trusted projector derives them from the selected evidence.
- Every reference must be authorized, same-workspace and available. Missing evidence produces a qualified result or explicit failure; it never becomes success.
- Current projections and historical evaluations do not consume a local configuration version or modify prior revisions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### CaptureSnapshot

`LOCAL_COMMAND` · permission `console:CaptureEvidence` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `kind` * | `INVESTIGATION/TOPOLOGY/POLICY_CONTEXT/LIFECYCLE_CATALOG/EVALUATION_INPUT` |
| `subjectRefs` * | `List<EntityRef>` |
| `sourceRevisionIds` * | `List<Id>` |
| `observationIds` * | `List<Id>` |
| `projectionRevisionIds` * | `List<Id>` |
| `collectionIds` * | `List<Id>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `snapshot: Snapshot`.

- Builds a closed immutable manifest and typed contents from existing retained evidence, including failed/empty read attempts and coverage.
- The manifest does not consult mutable current fields after capture. capturedAt does not renew source timestamps or make paginated AWS reads atomic.
- RUN_INPUT snapshots are created only during StartRun admission; clients cannot replace a Run's inputs by creating a similarly named snapshot.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `EvidenceUnavailableException`.

### CreateWorkItem

`LOCAL_COMMAND` · permission `console:ManageWork` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `title` * | `string` |
| `targets` * | `List<EntityRef>` |
| `priority` | `CRITICAL/HIGH/MEDIUM/LOW` |
| `dueAt` | `Timestamp` |
| `assigneeSubjectId` | `Id` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `workItem: WorkItem`.

- Creates local operator work; no provider state or operational conclusion is implied.
- assigneeSubjectId resolves through the trusted workspace directory and assignment policy; it selects a work owner, never the acting principal.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### UpdateWorkItem

`LOCAL_COMMAND` · permission `console:ManageWork` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `workItemId` * | `Id` |
| `title` | `string` |
| `state` | `OPEN/ACKNOWLEDGED/IN_PROGRESS/RESOLVED/DISMISSED` |
| `priority` | `CRITICAL/HIGH/MEDIUM/LOW` |
| `dueAt` | `Timestamp` |
| `assigneeSubjectId` | `Id` |
| `snoozedUntil` | `Timestamp` |
| `resolutionEvidence` | `List<EvidenceRef>` |
| `note` | `string` |
| `clearFields` | `List<snoozedUntil/dueAt/owner>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `workItem: WorkItem`.

- Records a server-attributed WorkAction and advances only WorkItem.version.
- RESOLVED is an operator work state, not provider recovery, approved cloud work or verified remediation.
- A field cannot be both assigned and named in clearFields; assigneeSubjectId conflicts with clearing owner. Evidence citations retain their original meaning.
- The trusted directory resolves the assigned owner independently of the server-attributed acting principal. Verification uses its separate command.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### RecordWorkItemVerification

`LOCAL_COMMAND` · permission `console:VerifyWork` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `workItemId` * | `Id` |
| `result` * | `VERIFIED/FAILED/UNKNOWN` |
| `rationale` * | `string` |
| `evidenceRefs` * | `List<EvidenceRef>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `workItem: WorkItem`.

- Records a separately authorized, qualified local verification judgment and an immutable server-attributed action under the WorkItem version.
- All evidence must resolve to this work's target scope. VERIFIED requires independent supporting evidence under the registered verification policy; the same operator resolution action or assessment completion alone is insufficient.
- The result updates verificationState/verificationEvidence, not WorkItem.state or any provider status, posture or historical source record.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## workload

### CreateSystem

`LOCAL_COMMAND` · permission `console:ManageCatalog` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `name` * | `string` |
| `description` | `string` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `system: System`.

- Creates local canonical workload identity and metadata; it does not create an AWS resource.
- Provider aliases are established by trusted verified mapping, not by caller-supplied matching names.
- Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and sourceRevisionId=null. Imported provenance is reserved to the trusted importer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetSystem

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |

**Response:** `system: System`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListSystems

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<System>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### UpdateSystem

`LOCAL_COMMAND` · permission `console:ManageCatalog` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `name` | `string` |
| `description` | `string` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `system: System`.

- Updates only local fields under this record's version; an observation or projection does not cause a configuration conflict.
- Omitted fields are unchanged; an empty description is a known empty value; supplied arrays replace their complete owned membership set.
- Service is the sole membership writer. Every journey must belong to its paired system; a journey update cannot set a second service list.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### CreateUserJourney

`LOCAL_COMMAND` · permission `console:ManageCatalog` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `name` * | `string` |
| `description` | `string` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `userJourney: UserJourney`.

- Creates local canonical workload identity and metadata; it does not create an AWS resource.
- Provider aliases are established by trusted verified mapping, not by caller-supplied matching names.
- Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and sourceRevisionId=null. Imported provenance is reserved to the trusted importer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetUserJourney

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `userJourneyId` * | `Id` |

**Response:** `userJourney: UserJourney`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListUserJourneys

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<UserJourney>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### UpdateUserJourney

`LOCAL_COMMAND` · permission `console:ManageCatalog` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `userJourneyId` * | `Id` |
| `name` | `string` |
| `description` | `string` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `userJourney: UserJourney`.

- Updates only local fields under this record's version; an observation or projection does not cause a configuration conflict.
- Omitted fields are unchanged; an empty description is a known empty value; supplied arrays replace their complete owned membership set.
- Service is the sole membership writer. Every journey must belong to its paired system; a journey update cannot set a second service list.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### CreateService

`LOCAL_COMMAND` · permission `console:ManageCatalog` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `name` * | `string` |
| `description` | `string` |
| `memberships` | `List<MembershipInput>` |
| `resourceIds` | `List<Id>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `service: Service`.

- Creates local canonical workload identity and metadata; it does not create an AWS resource.
- Provider aliases are established by trusted verified mapping, not by caller-supplied matching names.
- Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and sourceRevisionId=null. Imported provenance is reserved to the trusted importer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetService

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |

**Response:** `service: Service`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListServices

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` | `Id` |
| `userJourneyId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Service>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Service membership is many-to-many and deduplicated by canonical serviceId; it does not establish journey execution order or end-to-end compliance.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### UpdateService

`LOCAL_COMMAND` · permission `console:ManageCatalog` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `name` | `string` |
| `description` | `string` |
| `memberships` | `List<MembershipInput>` |
| `resourceIds` | `List<Id>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `service: Service`.

- Updates only local fields under this record's version; an observation or projection does not cause a configuration conflict.
- Omitted fields are unchanged; an empty description is a known empty value; supplied arrays replace their complete owned membership set.
- Service is the sole membership writer. Every journey must belong to its paired system; a journey update cannot set a second service list.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### GetServiceStatus

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |

**Response:** `projectionRevision: ProjectionRevision`.

- Returns the currently selected SERVICE_STATUS projection under its named rule, including evidence/freshness/coverage. Clients do not infer current state from newest receipt time.
- No current selected projection returns ResourceNotFoundException with code PROJECTION_NOT_AVAILABLE, never an invented healthy/default object.
- Runtime health, native assessed posture, collection quality and operator workflow remain distinct dimensions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### GetWorkspaceSummary

`READ` · permission `console:ReadWorkspace` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| Empty body | Send `{}` |

**Response:** `projectionRevision: ProjectionRevision`.

- Returns the current qualified WORKSPACE_SUMMARY for the trusted caller's authorized workload scope, including exact distinct contributor identities, denominator and rule.
- An empty authorized scope has null percentages. Retained historical evidence is separate from current usable coverage; no end-to-end journey compliance is inferred.
- A cached broader summary must be recomputed/selected for the authorized scope; hidden records cannot leak through counts.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### GetDependency

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `dependencyId` * | `Id` |

**Response:** `dependency: Dependency`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListDependencies

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Dependency>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### UpdateDependencyGovernance

`LOCAL_COMMAND` · permission `console:ManageGovernance` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `dependencyId` * | `Id` |
| `decision` * | `ALLOWED/REVIEW/DENIED` |
| `reason` * | `string` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `dependency: Dependency`.

- expectedVersion addresses dependency.governance.version only; native classification remains separate.
- An allowed/denied decision is local governance. It neither changes DNS evidence nor grants/revokes network access.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## health

### GetHealthEvent

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |

**Response:** `healthEvent: HealthEvent`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListHealthEvents

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceCode` | `string` |
| `eventTypeCode` | `string` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<HealthEvent>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListEventContexts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `kind` | `PUBLIC/ACCOUNT/ORG_SUMMARY` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<EventContext>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListEntityImpacts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<EntityImpact>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Account/public/organization-summary evidence never leaks between contexts. Counts remain qualified by collection coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListCommunications

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Communication>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Conflicting and partial notification pages remain visible; delivery recipients do not redefine impacted account identity.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListLifecycleEntries

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `snapshotId` * | `Id` |
| `serviceCode` | `string` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<LifecycleEntry>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- snapshotId must identify a LIFECYCLE_CATALOG capture. Entries from different catalog snapshots are not merged by title.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetComponentDeployment

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resourceId` * | `Id` |
| `componentDeploymentId` * | `Id` |

**Response:** `componentDeployment: ComponentDeployment`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListComponentDeployments

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resourceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ComponentDeployment>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Lifecycle exposure is a separate versioned projection using these observed component versions and a pinned lifecycle catalog.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

## resilience

### GetResiliencePolicy

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resiliencePolicyId` * | `Id` |

**Response:** `resiliencePolicy: ResiliencePolicy`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListResiliencePolicies

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ResiliencePolicy>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetResilienceAssessment

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `resilienceAssessmentId` * | `Id` |

**Response:** `resilienceAssessment: ResilienceAssessment`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListResilienceAssessments

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ResilienceAssessment>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetFinding

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |

**Response:** `finding: Finding`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListFindings

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `disposition` | `OPEN/RESOLVED/IRRELEVANT` |
| `severity` | `LOW/MEDIUM/HIGH` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Finding>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Findings are service-scoped. No mandatory assessment filter or ownership FK is invented; capture-to-assessment is qualified correlation.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetRecommendation

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `recommendationId` * | `Id` |

**Response:** `recommendation: Recommendation`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListRecommendations

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `sourceRevisionId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Recommendation>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Instances are observation/group/ordinal scoped; historical equal text does not establish provider identity continuity.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### StartResilienceAssessment

`PROVIDER_COMMAND` · permission `console:RunResilienceAssessment` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedServiceVersion` * | `Version` |
| `clientToken` * | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `StartFailureModeAssessment`. These are mapped operations, not identical wire payloads.

- Pins the local service scope at admission, then requests native StartFailureModeAssessment. expectedServiceVersion is local only.
- GetCommand exposes the created assessment identity after readback. SUCCESS of assessment execution does not imply achievable posture or verified remediation.
- Findings remain service-scoped and independent of a particular run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### UpdateFindingDisposition

`PROVIDER_COMMAND` · permission `console:UpdateFindingDisposition` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedSourceRevisionId` * | `Id` |
| `clientToken` * | `string` |
| `disposition` * | `OPEN/RESOLVED/IRRELEVANT` |
| `comment` | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateFailureModeFinding`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedSourceRevisionId compares the local observed version before admission/dispatch; it does not create an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's revision or a stale unrelated summary is rejected even in the same workspace.
- Maps only status/comment. Disposition is an operator assertion, not a new posture or finding-specific verification.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### UpdateDependencyClassification

`PROVIDER_COMMAND` · permission `console:UpdateDependencyClassification` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `dependencyId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedSourceRevisionId` * | `Id` |
| `clientToken` * | `string` |
| `criticality` | `HARD/SOFT/UNKNOWN` |
| `comment` | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateDependency`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedSourceRevisionId compares the local observed version before admission/dispatch; it does not create an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's revision or a stale unrelated summary is rejected even in the same workspace.
- Native criticality/comment and local allowed/denied governance have separate commands and revision ownership.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### UpdateResiliencePolicyConfiguration

`PROVIDER_COMMAND` · permission `console:ManageProviderConfiguration` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `resiliencePolicyId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedSourceRevisionId` * | `Id` |
| `clientToken` * | `string` |
| `changes` * | `ResiliencePolicyChanges` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdatePolicy`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedSourceRevisionId compares the local observed version before admission/dispatch; it does not create an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's revision or a stale unrelated summary is rejected even in the same workspace.
- The narrow supported write subset has four native component families. Explicit detachment/component clearing is deferred until native semantics are verified.
- Policy changes invalidate current applicability without modifying captured policy contexts or historical posture.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### UpdateResilienceServiceConfiguration

`PROVIDER_COMMAND` · permission `console:ManageProviderConfiguration` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedSourceRevisionId` * | `Id` |
| `clientToken` * | `string` |
| `changes` * | `ResilienceServiceChanges` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateService`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedSourceRevisionId compares the local observed version before admission/dispatch; it does not create an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's revision or a stale unrelated summary is rejected even in the same workspace.
- Changes the verified Resilience Hub service profile only. Local UpdateService remains the canonical catalog/membership command.
- This initial write subset covers description, Regions, direct policy attachment and desired discovery state. Native creation/deletion, association replacement, permissions, report configuration and clearing remain deferred adapter commands.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### UpdateRecommendationEnrichment

`LOCAL_COMMAND` · permission `console:ManageRecommendationWork` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `recommendationId` * | `Id` |
| `title` | `string` |
| `effort` | `string` |
| `estimate` | `RecommendationEstimate` |
| `assigneeSubjectId` | `Id` |
| `workState` | `OPEN/PLANNED/IN_PROGRESS/DONE/DISMISSED` |
| `note` | `string` |
| `clearFields` | `List<title/effort/estimate/owner>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `recommendation: Recommendation`.

- expectedVersion refers to recommendation.enrichment.version; immutable source suggestion and observation identity never change.
- Estimate amount/currency/basis/complexity/source/time/confidence are typed local information, separate from native assessment execution cost.
- The trusted directory resolves assigneeSubjectId; the server stamps mutation provenance/updatedAt. Assignment is not acting identity and cannot be combined with clearing owner.
- Local work completion/estimates do not establish provider remediation or recommendation identity across generated observations.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## investigation

### GetAgentSpace

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |

**Response:** `agentSpace: AgentSpace`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListAgentSpaces

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<AgentSpace>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetInvestigation

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `investigationId` * | `Id` |

**Response:** `investigation: Investigation`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListInvestigations

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Investigation>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetExecution

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |

**Response:** `execution: Execution`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.
- AgentSpace is the owner scope. A single investigation foreign key is not required, preserving chat and shared/referenced executions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListExecutions

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `investigationId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Execution>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- The optional investigation filter uses explicit TaskExecutionMembership evidence. A linked task can reference an execution created elsewhere in the same AgentSpace.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetJournalRecord

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `journalRecordId` * | `Id` |

**Response:** `journalRecord: JournalRecord`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListJournalRecords

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<JournalRecord>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Journal record identity, raw native type and graph extraction provenance remain separate; a textual mention does not create a graph link.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetApprovalRequest

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `approvalRequestId` * | `Id` |

**Response:** `approvalRequest: ApprovalRequest`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListApprovalRequests

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ApprovalRequest>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- These are retained validated chat request contexts, not a fabricated native Get/ListApproval API. A waiting task or Markdown button is insufficient.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### GetAsset

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `assetId` * | `Id` |

**Response:** `asset: Asset`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListAssets

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Asset>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### StartInvestigation

`PROVIDER_COMMAND` · permission `console:StartInvestigation` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `connectionId` * | `Id` |
| `title` * | `string` |
| `description` | `string` |
| `priority` * | `CRITICAL/HIGH/MEDIUM/LOW/MINIMAL` |
| `clientToken` * | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `CreateBacklogTask`. These are mapped operations, not identical wire payloads.

- Requests CreateBacklogTask with taskType=INVESTIGATION; it is not a native operation named StartInvestigation.
- A task creation receipt does not prove execution started. Native task, execution and result observations are reconciled separately.
- The adapter maps the durable console intent to a stable provider token within native bounds; no raw tenant/actor is accepted.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### DecideApproval

`PROVIDER_COMMAND` · permission `console:DecideApproval` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `approvalRequestId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedRequestSourceRevisionId` * | `Id` |
| `expectedActionDigest` * | `Digest` |
| `decision` * | `APPROVED/REJECTED` |
| `singleUse` | `literal true` |
| `reason` | `string` |
| `clientToken` * | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateApprovalAction`. These are mapped operations, not identical wire payloads.

- First-release decision supports exact observed scope and single use only; reusable grants and pattern editing are explicitly deferred.
- APPROVED requires singleUse=true. REJECTED omits singleUse; the adapter also omits native pattern and TTL fields for rejection.
- Validates a complete authenticated chat request context and exact action digest, then invokes UpdateApprovalAction. It neither resumes the execution nor claims the tool ran.
- Native UpdateApprovalAction has no modeled idempotency token. A lost response is OUTCOME_UNKNOWN; local replay returns the receipt and must not repeat the remote mutation blindly.
- A successful rejection is a successful decision command, not a provider API failure.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### ResumeExecution

`PROVIDER_COMMAND` · permission `console:ResumeExecution` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `approvalRequestId` * | `Id` |
| `decisionCommandId` * | `Id` |
| `connectionId` * | `Id` |
| `clientToken` * | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `SendMessage`. These are mapped operations, not identical wire payloads.

- Requires a definitively successful matching decision Command, valid current authorization and a validated approval/interrupt/tool-use context.
- Constructs the native SendMessage APPROVAL_ACTION context from that retained request; the caller cannot substitute interrupt/tool IDs or widen approved scope.
- Decision, resume submission, credential redemption and actual tool outcome remain separate. Opening or completing a stream does not prove the tool succeeded.
- SendMessage has no modeled idempotency token. Persist stream fragments and unknown outcomes; do not blindly resend on disconnect.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

## workflow

### CreateScenario

`LOCAL_COMMAND` · permission `console:AuthorScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `name` * | `string` |
| `description` | `string` |
| `draftDefinition` * | `ScenarioDraft` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `scenario: Scenario`.

- Creates a local editable draft. An author cannot set trusted operation locks, capability grants or a published digest.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetScenario

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |

**Response:** `scenario: Scenario`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListScenarios

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `archived` | `boolean` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Scenario>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### UpdateScenario

`LOCAL_COMMAND` · permission `console:AuthorScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `name` | `string` |
| `description` | `string` |
| `draftDefinition` | `ScenarioDraft` |
| `archived` | `boolean` |
| `defaultRevisionId` | `Id` |
| `clearFields` | `List<defaultRevisionId>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `scenario: Scenario`.

- Only the draft/catalog record changes; a default revision must belong to this Scenario. No already admitted Run is redirected.
- Omitted fields preserve; clearFields=[defaultRevisionId] removes the default pointer. Supplying it and clearing it in one request is invalid.
- archived=true rejects new Run admission while preserving all published revisions and historical Runs; exact replay of an already admitted Run still returns its original receipt.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### PublishScenarioRevision

`LOCAL_COMMAND` · permission `console:PublishScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `expectedVersion` * | `Version` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `scenarioRevision: ScenarioRevision`.

- Compiles the exact current draft, resolves retained immutable implementation/schema locks and atomically publishes a new revision.
- Publication validates DAGs, dependency-scoped references, typed bindings, capability checks, required criteria, finalizers and fixed language/reducer semantics before any external work.
- The caller cannot submit a trusted lock or digest. Changing a later alias cannot alter this revision. Missing/revoked pinned artifacts reject future admission, never substitute.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### GetScenarioRevision

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `scenarioRevisionId` * | `Id` |

**Response:** `scenarioRevision: ScenarioRevision`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListScenarioRevisions

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ScenarioRevision>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### StartRun

`EXECUTION_COMMAND` · permission `console:StartRun` · implementation gate `P4_WORKFLOW_RUNTIME`

| Request member | Type |
| --- | --- |
| `scenarioRevisionId` * | `Id` |
| `subject` * | `EntityRef` |
| `expectedSubjectVersion` | `Version` |
| `inputs` * | `object` |
| `bindings` * | `object` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `run: Run`.

- Durably admits one Run, all StepRuns and a closed RUN_INPUT snapshot atomically; no claim that an AWS call has started.
- inputs are intentionally revision-defined and must pass its pinned closed input schema; unknown binding names, raw secrets, undeclared operations or unauthorized scope are rejected.
- Admission fixes enabled steps and the required-criterion denominator. Runtime skips/cancellation cannot shrink it; inapplicable admission criteria remain recorded.
- expectedSubjectVersion applies only when the subject is a local mutable configuration; it is not an AWS deployment lock. Material dispatch preconditions are rechecked by the adapter.
- A new execution intent uses a new clientToken. Pinned revision identity, never the default pointer, selects the program.
- The revision's owning Scenario must not be archived at new admission; archive state cannot redirect or cancel an already admitted Run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`, `EvidenceUnavailableException`.

### GetRun

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |

**Response:** `run: Run`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListRuns

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `scenarioRevisionId` | `Id` |
| `phase` | `ADMITTED/RUNNING/FINALIZING/TERMINAL` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Run>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### RequestRunCancellation

`EXECUTION_COMMAND` · permission `console:CancelRun` · implementation gate `P4_WORKFLOW_RUNTIME`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `reason` | `string` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `accepted: boolean`; `run: Run`.

- Atomically accepts monotonic cancellation intent and fences new main dispatch; it does not set a remote effect to stopped.
- Already sealed Run returns accepted=false and its unchanged terminal record. Exact replay preserves the original accepted receipt after later completion.
- Finalizers reconcile active/unknown effects, including a lost Start response with no handle. A creating Start must never be reissued after cancellation just to discover its result.
- Different cancellation tokens converge on the first accepted intent. Cleanup, execution result and workload verdict remain independently visible.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### ListRunSteps

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<StepRun>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Includes every compiled step, including skipped zero-attempt steps. No independent retry/stop/status-update command exists.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### ListStepAttempts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `stepRunId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<StepAttempt>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Ordered by attemptNo; polling/resume/transport retry remain within the same attempt. A new mutating attempt is forbidden while its predecessor's effect is unresolved.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

## fis

### GetExperiment

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `experimentId` * | `Id` |

**Response:** `experiment: Experiment`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.
- Native actions are keyed by experiment + actionName; their catalog actionId is not an execution identity.
- Selected memberships, applied effects, workload criteria and report readiness are separate evidence dimensions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`.

### ListExperiments

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` | `Id` |
| `runId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Experiment>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal ordered by the documented immutable key; nextToken is absent only at the end.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- runId filters only verified ExternalOperationRef links; imported experiments can have no product workflow Run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`.

### StopExperiment

`PROVIDER_COMMAND` · permission `console:StopExperiment` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `experimentId` * | `Id` |
| `connectionId` * | `Id` |
| `expectedSourceRevisionId` * | `Id` |
| `clientToken` * | `string` |
| `reason` | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `StopExperiment`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedSourceRevisionId compares the local observed version before admission/dispatch; it does not create an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's revision or a stale unrelated summary is rejected even in the same workspace.
- Requests native StopExperiment for the whole experiment; no individual native action stop/retry/pause command is fabricated.
- Stop acceptance, final native state, post-action cleanup, workload recovery and report completion remain separate.
- Starting new fault experiments is available only through an explicitly authorized pinned workflow adapter in this initial facade.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

## Entity coverage

Every canonical entity is returned by a named getter or scoped full-record list. Owned values are returned by their owner; no artificial CRUD lifecycle is introduced.

| Entity | Read operations |
| --- | --- |
| `Workspace` | `GetWorkspace` |
| `Connection` | `GetConnection`, `ListConnections` |
| `Resource` | `GetResource`, `ListResources` |
| `Collection` | `GetCollection`, `ListCollections` |
| `ReadAttempt` | `ListReadAttempts` |
| `SourceRevision` | `GetSourceRevision`, `ListSourceRevisions` |
| `Observation` | `GetObservation`, `ListObservations` |
| `ProjectionRevision` | `GetProjectionRevision`, `ListProjectionRevisions`, `GetServiceStatus`, `GetWorkspaceSummary` |
| `Snapshot` | `GetSnapshot`, `ListSnapshots` |
| `WorkItem` | `GetWorkItem`, `ListWorkItems` |
| `Command` | `GetCommand`, `ListCommands` |
| `System` | `GetSystem`, `ListSystems` |
| `UserJourney` | `GetUserJourney`, `ListUserJourneys` |
| `Service` | `GetService`, `ListServices` |
| `Dependency` | `GetDependency`, `ListDependencies` |
| `HealthEvent` | `GetHealthEvent`, `ListHealthEvents` |
| `EventContext` | `ListEventContexts` |
| `EntityImpact` | `ListEntityImpacts` |
| `Communication` | `ListCommunications` |
| `LifecycleEntry` | `ListLifecycleEntries` |
| `ComponentDeployment` | `GetComponentDeployment`, `ListComponentDeployments` |
| `ResiliencePolicy` | `GetResiliencePolicy`, `ListResiliencePolicies` |
| `ResilienceAssessment` | `GetResilienceAssessment`, `ListResilienceAssessments` |
| `Finding` | `GetFinding`, `ListFindings` |
| `Recommendation` | `GetRecommendation`, `ListRecommendations` |
| `AgentSpace` | `GetAgentSpace`, `ListAgentSpaces` |
| `Investigation` | `GetInvestigation`, `ListInvestigations` |
| `Execution` | `GetExecution`, `ListExecutions` |
| `JournalRecord` | `GetJournalRecord`, `ListJournalRecords` |
| `ApprovalRequest` | `GetApprovalRequest`, `ListApprovalRequests` |
| `Asset` | `GetAsset`, `ListAssets` |
| `Scenario` | `GetScenario`, `ListScenarios` |
| `ScenarioRevision` | `GetScenarioRevision`, `ListScenarioRevisions` |
| `Run` | `GetRun`, `ListRuns` |
| `StepRun` | `ListRunSteps` |
| `StepAttempt` | `ListStepAttempts` |
| `Experiment` | `GetExperiment`, `ListExperiments` |

## Prior operation migration

This table accounts for every operation in the prior 44-operation Resilience facade and 16-operation generalized workflow proposal. Preserving a model does not silently redefine a native command as a local metadata write. Changes of scope, transport or supported fields are explicit.

| Source | Prior operation | Consolidated operation(s) | Disposition and meaning |
| --- | --- | --- | --- |
| Resilience | `GetSystem` | `GetSystem`, `GetSourceRevision` | `CANONICAL_READ_WITH_NATIVE_FACET`. Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge. |
| Resilience | `ListSystems` | `ListSystems`, `ListSourceRevisions` | `CANONICAL_READ_WITH_NATIVE_FACET`. Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded. |
| Resilience | `GetUserJourney` | `GetUserJourney`, `GetSourceRevision` | `CANONICAL_READ_WITH_NATIVE_FACET`. Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge. |
| Resilience | `ListUserJourneys` | `ListUserJourneys`, `ListSourceRevisions` | `CANONICAL_READ_WITH_NATIVE_FACET`. Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded. |
| Resilience | `GetService` | `GetService`, `GetSourceRevision` | `CANONICAL_READ_WITH_NATIVE_FACET`. Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge. |
| Resilience | `ListServices` | `ListServices`, `ListSourceRevisions` | `CANONICAL_READ_WITH_NATIVE_FACET`. Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded. |
| Resilience | `CreateSystem` | Deferred | `DEFERRED_NATIVE_COMMAND`. Old commands created provider resources. New identically named catalog Create commands are LOCAL and are not migration aliases for native creation. |
| Resilience | `CreateUserJourney` | Deferred | `DEFERRED_NATIVE_COMMAND`. Old commands created provider resources. New identically named catalog Create commands are LOCAL and are not migration aliases for native creation. |
| Resilience | `CreateService` | Deferred | `DEFERRED_NATIVE_COMMAND`. Old commands created provider resources. New identically named catalog Create commands are LOCAL and are not migration aliases for native creation. |
| Resilience | `CreatePolicy` | Deferred | `DEFERRED_NATIVE_COMMAND`. Old commands created provider resources. New identically named catalog Create commands are LOCAL and are not migration aliases for native creation. |
| Resilience | `UpdateSystem` | Deferred | `DEFERRED_NATIVE_COMMAND`. Native description/sharing/journey/policy edits remain later adapter work; local UpdateSystem/UpdateUserJourney edit canonical metadata only. |
| Resilience | `UpdateUserJourney` | Deferred | `DEFERRED_NATIVE_COMMAND`. Native description/sharing/journey/policy edits remain later adapter work; local UpdateSystem/UpdateUserJourney edit canonical metadata only. |
| Resilience | `DeleteSystem` | Deferred | `DEFERRED_NATIVE_COMMAND`. Native destructive semantics/guards and preserved history need explicit later commands. No local delete substitutes for them. |
| Resilience | `DeleteUserJourney` | Deferred | `DEFERRED_NATIVE_COMMAND`. Native destructive semantics/guards and preserved history need explicit later commands. No local delete substitutes for them. |
| Resilience | `DeleteService` | Deferred | `DEFERRED_NATIVE_COMMAND`. Native destructive semantics/guards and preserved history need explicit later commands. No local delete substitutes for them. |
| Resilience | `DeletePolicy` | Deferred | `DEFERRED_NATIVE_COMMAND`. Native destructive semantics/guards and preserved history need explicit later commands. No local delete substitutes for them. |
| Resilience | `UpdateService` | `UpdateResilienceServiceConfiguration` | `NARROW_PROVIDER_SUBSET`. Description, Regions, direct policy attachment and discovery intent now have explicit native authority. Remaining native fields and clearing are deferred. |
| Resilience | `UpdatePolicy` | `UpdateResiliencePolicyConfiguration` | `NARROW_PROVIDER_SUBSET`. Typed native policy components/description/sharing; no generic clear or local rename forwarded to the provider. |
| Resilience | `GetPolicy` | `GetResiliencePolicy` | `RENAMED_TYPED_READ`. Explicitly names the resilience policy bounded context. |
| Resilience | `ListPolicies` | `ListResiliencePolicies` | `RENAMED_TYPED_READ`. Explicitly names the resilience policy bounded context. |
| Resilience | `CreateInputSource` | Deferred | `DEFERRED_NATIVE_COMMAND`. Retained input-source profile is in scope; provider CRUD is deferred. |
| Resilience | `DeleteInputSource` | Deferred | `DEFERRED_NATIVE_COMMAND`. Retained input-source profile is in scope; provider CRUD is deferred. |
| Resilience | `ListInputSources` | `ListSourceRevisions`, `GetSourceRevision` | `RETAINED_TYPED_PROFILE`. Use aws.resilience-hub.input-source/v1 and exact service-scoped source identity. |
| Resilience | `StartFailureModeAssessment` | `StartResilienceAssessment` | `EXPLICIT_ASYNC_COMMAND`. Receipt and later provider assessment identity are separate. |
| Resilience | `GetFailureModeAssessment` | `GetResilienceAssessment` | `RENAMED_TYPED_READ`. Retained service-scoped provider execution; no invented native Get call. |
| Resilience | `ListFailureModeAssessments` | `ListResilienceAssessments` | `RENAMED_TYPED_READ`. Stable local traversal, with independent upstream coverage. |
| Resilience | `GetFailureModeFinding` | `GetFinding` | `CANONICAL_READ_WITH_NATIVE_FACET`. Scoped finding; summary/detail observations and captures remain explicit. |
| Resilience | `ListFailureModeFindings` | `ListFindings` | `CANONICAL_READ_WITH_NATIVE_FACET`. No mandatory assessment ownership is inferred. |
| Resilience | `UpdateFailureModeFinding` | `UpdateFindingDisposition` | `EXPLICIT_ASYNC_COMMAND`. Native status/comment only; no posture or repair verification implied. |
| Resilience | `GetRecommendation` | `GetRecommendation` | `PRESERVED_WITH_CANONICAL_SCOPE`. Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained. |
| Resilience | `ListRecommendations` | `ListRecommendations` | `PRESERVED_WITH_CANONICAL_SCOPE`. Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained. |
| Resilience | `UpdateRecommendationEnrichment` | `UpdateRecommendationEnrichment` | `PRESERVED_WITH_CANONICAL_SCOPE`. Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained. |
| Resilience | `GetDependency` | `GetDependency` | `PRESERVED_WITH_CANONICAL_SCOPE`. Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained. |
| Resilience | `ListDependencies` | `ListDependencies` | `PRESERVED_WITH_CANONICAL_SCOPE`. Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained. |
| Resilience | `UpdateDependencyGovernance` | `UpdateDependencyGovernance` | `PRESERVED_WITH_CANONICAL_SCOPE`. Canonical IDs replace native URL-like keys; source identity and independent local versions remain retained. |
| Resilience | `UpdateDependency` | `UpdateDependencyClassification` | `EXPLICIT_ASYNC_COMMAND`. Provider criticality/comment remain separate from local governance. |
| Resilience | `CaptureTopologySnapshot` | `CaptureSnapshot` | `SHARED_CAPTURE`. kind=TOPOLOGY; preserves source times and closed manifest, not a native atomic snapshot. |
| Resilience | `GetTopologySnapshot` | `GetSnapshot` | `SHARED_CAPTURE`. Read the exact retained topology snapshot identity. |
| Resilience | `ListTopologySnapshots` | `ListSnapshots` | `SHARED_CAPTURE`. Filter kind=TOPOLOGY and the exact service subject. |
| Resilience | `GetServiceStatus` | `GetServiceStatus` | `QUALIFIED_PROJECTION_READ`. Returns currently selected SERVICE_STATUS ProjectionRevision with its evidence and independent dimensions. |
| Resilience | `GetWorkspaceSummary` | `GetWorkspaceSummary` | `QUALIFIED_PROJECTION_READ`. Returns WORKSPACE_SUMMARY for authorized contributors, with denominator and rule. |
| Resilience | `ListEvents` | `ListObservations`, `ListSourceRevisions` | `SHARED_EVIDENCE_READ`. Filter exact subjects/profile/channel evidence; delivery ID never becomes a HealthEvent ID. |
| Resilience | `PutHealthObservation` | `IngestObservation`, `PublishProjection` | `SHARED_TRUSTED_INGEST`. Retain runtime-health source evidence then derive SERVICE_STATUS. This is distinct from AWS Health Event ingestion. |
| Resilience | `IngestEvent` | `IngestObservation`, `StartCollection` | `SHARED_TRUSTED_INGEST`. Retains raw channel evidence and schedules authorized read collection; event body cannot patch authoritative state. |
| Workflow | `GetScenario` | `GetScenario` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListScenarios` | `ListScenarios` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `GetScenarioRevision` | `GetScenarioRevision` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListScenarioRevisions` | `ListScenarioRevisions` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `GetRun` | `GetRun` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListRuns` | `ListRuns` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `RequestRunCancellation` | `RequestRunCancellation` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListRunSteps` | `ListRunSteps` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListStepAttempts` | `ListStepAttempts` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `CreateScenario` | `CreateScenario` | `EXTENDED_AUTHORING_CONTRACT`. Creates metadata and a typed editable draft; trusted operation locks remain publication-owned. |
| Workflow | `UpdateScenario` | `UpdateScenario` | `RPC_REBINDING`. expectedVersion replaces If-Match; omission preserves and explicit allowed clears replace nullable PATCH ambiguity. |
| Workflow | `PublishScenarioRevision` | `UpdateScenario`, `PublishScenarioRevision` | `DRAFT_THEN_PUBLISH`. Update the typed draft, then publish its exact expected Scenario version; server compiles and resolves trusted locks. |
| Workflow | `StartRun` | `StartRun` | `RPC_REBINDING`. Pins canonical subject, revision, validated inputs and authorized bindings; retains immutable admission and criterion denominator. |
| Workflow | `ListRunEvidence` | `ListObservations`, `ListSourceRevisions`, `ListProjectionRevisions` | `SHARED_TYPED_EVIDENCE`. Filter the exact Run subject/producer references; raw source, receipt and derived evidence types stay explicit. |
| Workflow | `GetEvidence` | `GetSourceRevision`, `GetObservation`, `GetProjectionRevision`, `GetSnapshot` | `SHARED_TYPED_EVIDENCE`. Resolve the discriminated EvidenceRef kind; evidence is not collapsed into an untyped payload. |
| Workflow | `ListOperations` | `GetScenarioRevision` | `DYNAMIC_DISCOVERY_DEFERRED`. Published locks remain inspectable. Authorized discovery of executable adapter aliases is later registry work; facade operations.json is not that adapter registry. |

## Deliberately deferred command families

The previous service packages remain the detailed native API references. This first consolidation defines a narrow provider mutation surface; the rest remain typed source profiles and explicit later adapter work:

| Family | Retained now | Later command work |
| --- | --- | --- |
| Resilience provider systems/journeys/services/policies | Native source revisions, verified canonical bindings and selected configuration commands | Native creates/deletes, association replacement/detachment, permission/report/input-source configuration and destructive clears |
| FIS templates/catalog/resource types/safety lever | Typed source profiles; experiment reads and whole-experiment stop | Template CRUD and scope-wide safety-lever mutation after dedicated authorization and adapter semantics |
| DevOps registration/association/webhook/goal/recommendation/trigger/operator/private connection | Typed source DTOs and their exact scopes through SourceRevision reads | Provider management commands; no native recommendation is conflated with Resilience recommendation identity |
| Asset byte access | Versioned artifact references and read authorization boundary | Expiring artifact download/upload grants and binary transport, with independent content access |
| Workflow execution | Published program, admission, cancellation and owned execution read contracts | Durable dispatch, recovery, retries, leases, fences, source coverage and cloud adapters |
| Retention/deletion | Immutable evidence identity and unavailable/tombstone semantics | Retention policy execution and explicitly guarded destructive commands |

These are delivery boundaries, not discarded models. [MAPPING.md](../MAPPING.md) and [adapter-profiles.json](../model/adapter-profiles.json) retain every reviewed source concept and native family.
