# Consolidated operations console — RPC operations

API date **2026-11-05** · **contract revision 2** · namespace `ConsolidatedOperationsConsole_20261105V2` · **108 operations**

**Status: phase-one design contracts.** There is no HTTP server, provider adapter, authentication implementation, scheduler or executed cloud mutation in this package. The schemas, examples and validation make the proposed interface reviewable. [Protocol](PROTOCOL.md) defines the shared semantics; [model](../MODEL.md) defines authority and identity.

All calls use `POST /` with `application/x-amz-json-1.1` and `X-Amz-Target: ConsolidatedOperationsConsole_20261105V2.<Operation>`. Successful calls use HTTP 200, including durable asynchronous command receipts. `Command.state=SUCCEEDED` means that command's documented effect succeeded; it does not imply successful assessment, healthy workload or verified repair.

Exact request/response schemas are in [rpc.schema.json](rpc.schema.json). [operations.json](operations.json) records scope, permissions, provenance, delivery phase and errors. [examples.json](examples.json) contains one complete synthetic request/response for every operation. Inputs are closed writable DTOs. Responses refer directly to the canonical model shapes; clients tolerate optional future response members and raw future provider vocabulary.

## Module index

| Module | Operations | Read | Mutating |
| --- | ---: | ---: | ---: |
| [foundation](#foundation) | 33 | 22 | 11 |
| [workload](#workload) | 17 | 10 | 7 |
| [health](#health) | 12 | 12 | 0 |
| [resilience](#resilience) | 14 | 8 | 6 |
| [investigation](#investigation) | 15 | 12 | 3 |
| [workflow](#workflow) | 14 | 8 | 6 |
| [fis](#fis) | 3 | 2 | 1 |

## Common field conventions

Every entity has one `version`, `createdAt` and `updatedAt`. `Get<Entity>` accepts optional `version`: explicit means exact, omitted means current head; no historical read falls back to latest. `ListEntityVersions` returns exact reference values for one logical identity. Evidence references contain `{kind,id,version}`; live navigation uses the distinct `{kind,id}` EntityIdentity value.

`clientToken` is required for every mutation. `expectedVersion` guards the whole named entity, including owned metadata; there are no nested overlay clocks. `expectedSource` pins native evidence and is never an AWS conditional-write guarantee. `maxResults` is 1–100, default 20; `nextToken` binds an authorization-scoped retained publication. No JSON body can choose the acting user, role or authenticated workspace.

In the field tables, **required** members are marked with `*`. Every operation-specific response schema is a closed local validation snapshot; this does not require clients to reject future optional response members. Empty/null/missing/unknown remain distinct. A getter returns a retained record, not an implicit new provider read.

## foundation

### GetWorkspace

`READ` · permission `console:ReadWorkspace` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `version` | `Version` |

**Response:** `workspace: Workspace`.

- Workspace comes exclusively from authenticated context; the request cannot select a tenant.
- version selects an exact immutable representation. Omission selects the current head; current authorization is always enforced, including historical reads.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListEntityVersions

`READ` · permission `console:ReadHistory` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `entity` * | `EntityIdentity` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<EntityRef>`; `page: Page`; `nextToken?: string`.

- Enumerates immutable exact references for one logical entity, ordered by descending version in a fixed traversal. References are values, not separately managed Version resources.
- Resolve each reference with that entity's Get operation and the returned version. Historical versions are never silently replaced by current heads.
- The current caller must hold both history capability and the entity's normal domain-read permission; each returned version must authorize its full retained closure.
- A Workspace identity must equal the already authenticated workspace. This operation cannot select another tenant or bypass domain parent/scope checks.
- The cursor binds entity kind/id, authenticated scope and the traversal's retained version set. It exposes no hidden version count.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetConnection

`READ` · permission `console:ReadConnections` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` * | `Id` |
| `version` | `Version` |

**Response:** `connection: Connection`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListConnections

`READ` · permission `console:ReadConnections` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `enabled` | `boolean` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Connection>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

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
| `version` | `Version` |

**Response:** `resource: Resource`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListResources

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` | `Id` |
| `resourceType` | `string` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Resource>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetCollection

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `version` | `Version` |

**Response:** `collection: Collection`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListCollections

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` | `Id` |
| `subject` | `EntityRef` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Collection>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetReadAttempt

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `readAttemptId` * | `Id` |
| `version` | `Version` |

**Response:** `readAttempt: ReadAttempt`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListReadAttempts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ReadAttempt>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Includes failed and empty reads; their absence from returned object rows must not erase collection evidence.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetSource

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `sourceId` * | `Id` |
| `version` | `Version` |

**Response:** `source: Source`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetObservation

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `observationId` * | `Id` |
| `version` | `Version` |

**Response:** `observation: Observation`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetProjection

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `projectionId` * | `Id` |
| `version` | `Version` |

**Response:** `projection: Projection`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetSnapshot

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `snapshotId` * | `Id` |
| `version` | `Version` |

**Response:** `snapshot: Snapshot`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetWorkItem

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `workItemId` * | `Id` |
| `version` | `Version` |

**Response:** `workItem: WorkItem`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetCommand

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `commandId` * | `Id` |
| `version` | `Version` |

**Response:** `command: Command`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListSources

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `identity` | `SourceIdentity` |
| `profile` | `string` |
| `representation` | `SUMMARY/DETAIL/EVENT/STREAM/ARTIFACT/CONFIGURATION/LOCAL_EVIDENCE` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Source>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Native peripheral resources are retained typed profiles, including FIS templates/catalogs and DevOps registrations/triggers/goals.
- Representation and source identity are explicit; matching hashes do not merge different logical source records.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListObservations

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `source` | `EntityRef` |
| `collectionId` | `Id` |
| `subject` | `EntityRef` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Observation>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListProjections

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `subject` | `EntityRef` |
| `profile` | `EVALUATION/LIFECYCLE_EXPOSURE/INVESTIGATION_RESULT/SERVICE_STATUS/WORKSPACE_SUMMARY/INVESTIGATION_TIMELINE/INVESTIGATION_ASSERTIONS` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Projection>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Returns current Projection heads. Each logical projection has ordinary entity versions; exact prior derivations remain readable without a ProjectionRevision entity.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListSnapshots

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `subject` | `EntityRef` |
| `kind` | `INVESTIGATION/TOPOLOGY/POLICY_CONTEXT/LIFECYCLE_CATALOG/RUN_INPUT/EVALUATION_INPUT` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Snapshot>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### ListWorkItems

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `target` | `EntityIdentity` |
| `state` | `OPEN/ACKNOWLEDGED/IN_PROGRESS/RESOLVED/DISMISSED` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<WorkItem>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

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

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### StartCollection

`INGEST` · permission `console:Collect` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connection` * | `EntityRef` |
| `queries` * | `List<CollectionQuery>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `collection: Collection`.

- Admits a finite exact query set from the registered read-only adapter catalog; unknown operations or unauthorized scope fail admission.
- queryKey uniqueness, canonical requestDigest, filter types and operation-specific bounds are validated against that registered adapter.
- Completion, pagination, hydration, resolution and claim coverage remain independent facts.
- Trusted collection admission records exact collector and selectionPolicy implementation identities on the Collection; caller input cannot forge these processing identities.

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
| `requestSource` * | `EntityRef` |
| `responseSource` * | `EntityRef or null` |
| `itemErrors` | `List<CollectionItemError>` |
| `itemOutcome` | `COMPLETE/PARTIAL/FAILED/NOT_APPLICABLE/UNKNOWN` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `readAttempt: ReadAttempt`.

- Settles the same existing STARTED ReadAttempt created by the trusted collector dispatch transaction before the actual read; does not append a second attempt or fabricate a pre-call record after the fact.
- Trusted context assigns authorizationContextKey; a caller cannot forge its acting principal or provenance.
- expectedVersion guards the existing STARTED ReadAttempt head. Settlement creates the next version of that same identity; prior STARTED representations remain intact.
- requestSource must equal the exact already retained request envelope for this attempt. Response references must belong to this exact request and scope, including empty responses.
- IngestObservation may retain response/object observations while the attempt is STARTED; settlement then references those revisions. A response-lost failure has an explicit null response reference, not a fabricated empty response.
- A settled attempt is immutable. Exact replay returns the original result; conflicting terminal facts reject. Query identity, attemptNo, requestDigest, startedAt and authorization provenance are server-owned.
- Optional itemErrors and itemOutcome preserve event/account failedSet entries. A successful HTTP response can have PARTIAL or FAILED item outcome while transport state remains SUCCEEDED; transport failures remain error. Omitting these fields means item outcome was not recorded, never complete success.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### IngestObservation

`INGEST` · permission `console:IngestEvidence` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `channel` * | `API/EVENTBRIDGE/STREAM/LOCAL` |
| `readAttempt` * | `EntityRef or null` |
| `connection` * | `EntityRef or null` |
| `observedAt` * | `Timestamp` |
| `sourceTime` * | `Timestamp or null` |
| `transportTime` * | `Timestamp or null` |
| `expiresAt` * | `Timestamp or null` |
| `receiptKey` * | `string or null` |
| `source` * | `SourceInput` |
| `clientToken` * | `string` |

**Response:** `source: Source`; `observation: Observation`; `command: Command`.

- Atomically resolves the stable Source identity independently of content digest, retains a new Source version when its accepted representation changes, and records a distinct Observation with an exact Source reference.
- An unchanged consecutive receipt reuses the current Source version only when raw content, optional normalized views and their rule provenance all agree. Changed normalization appends a version even with the same raw contentDigest. A→B→A publishes versions 1→2→3; byte deduplication cannot relabel the last observation as the old version 1.
- The registered versioned profile validates typed known members, source identity, representation and digest; raw unknown provider output remains retained evidence.
- payload is the intentionally opaque provider document, bounded by the body cap and adapter schema; it cannot patch canonical state or set a verdict.
- Optional normalized Source fields require their registered profile and normalization input/rule provenance. contentDigest remains the raw payload/artifact digest; inputContentDigest must agree with it. Unknown native content remains retained in payload and must not be rejected solely because it cannot populate a normalized view. Existing records without those optional fields are not claimed to be normalized.
- The adapter reconciles canonical entity indexes through verified mappings. Digest equality alone is not event identity; receipt dedupe includes the authenticated channel/scope.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `EvidenceUnavailableException`.

### CompleteCollection

`INGEST` · permission `console:IngestEvidence` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `collectionId` * | `Id` |
| `coverage` * | `List<Coverage>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `collection: Collection`.

- Seals collection coverage after every declared query has a settled or explicitly unresolved outcome; referenced attempts must belong to this collection.
- A coverage conclusion must be justified by registered collector rules. Successful or exhausted pages cannot alone claim source sufficiency.
- New coverage conclusions record the exact evaluationPolicy identity. Historical absence remains unknown; it cannot be assigned the current policy retroactively.
- expectedVersion guards the Collection head; completion publishes its next ordinary entity version. There is no second projectionVersion clock.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### PublishProjection

`DERIVE` · permission `console:PublishProjection` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `projectionKey` * | `string` |
| `profile` * | `EVALUATION/LIFECYCLE_EXPOSURE/INVESTIGATION_RESULT/SERVICE_STATUS/WORKSPACE_SUMMARY/INVESTIGATION_TIMELINE/INVESTIGATION_ASSERTIONS` |
| `profileVersion` * | `string` |
| `subjectRefs` * | `List<EntityRef>` |
| `inputRefs` * | `List<EvidenceRef>` |
| `ruleDigest` * | `Digest` |
| `asOf` * | `Timestamp` |
| `expectedVersion` * | `Version or null` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `projection: Projection`.

- Executes an authorized registered rule over exact entity-version inputs and publishes the next version of the same logical Projection.
- expectedVersion=null requires that the named projection identity does not exist; a positive value guards its current head. The first publication is version 1. Concurrent incompatible publication returns VersionConflictException.
- The request cannot supply value, generatedAt, coverage or a desired verdict. The trusted projector derives them from the selected evidence.
- INVESTIGATION_TIMELINE and INVESTIGATION_ASSERTIONS use their typed value contracts. The trusted projector records DerivationContext and outputDigest; every source citation is among inputRefs. Published claims preserve attribution and do not expose private model reasoning.
- Every reference must be authorized, same-workspace and available. Missing evidence produces a qualified result or explicit failure; it never becomes success.
- A new projection version does not change its source subjects or any earlier entity representation. Current-view selection never rewrites a sealed Run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### CaptureSnapshot

`LOCAL_COMMAND` · permission `console:CaptureEvidence` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `kind` * | `INVESTIGATION/TOPOLOGY/POLICY_CONTEXT/LIFECYCLE_CATALOG/EVALUATION_INPUT` |
| `subjectRefs` * | `List<EntityRef>` |
| `members` * | `List<EntityRef>` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `snapshot: Snapshot`.

- Builds a closed immutable manifest and typed contents from existing retained evidence, including failed/empty read attempts and coverage.
- All selected subjects and members use exact (kind,id,version) references. The server closes the authorized retained reference graph without resolving any member to latest; unavailable versions reject capture.
- The manifest does not consult mutable current fields after capture. capturedAt does not renew source timestamps or make paginated AWS reads atomic.
- RUN_INPUT snapshots are created only during StartRun admission; clients cannot replace a Run's inputs by creating a similarly named snapshot.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `EvidenceUnavailableException`.

### CreateWorkItem

`LOCAL_COMMAND` · permission `console:ManageWork` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `title` * | `string` |
| `targets` * | `List<EntityIdentity>` |
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
- Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and source=null. Imported provenance is reserved to the trusted importer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetSystem

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `version` | `Version` |

**Response:** `system: System`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListSystems

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<System>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

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

- Updates the named entity under its one expectedVersion and publishes the next immutable representation, including owned values. There is no separate configuration or overlay clock.
- Changes to separate Source, Observation or Projection identities do not change this entity. A material change to its own fields or verified bindings does advance its version.
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
- Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and source=null. Imported provenance is reserved to the trusted importer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetUserJourney

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `userJourneyId` * | `Id` |
| `version` | `Version` |

**Response:** `userJourney: UserJourney`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListUserJourneys

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<UserJourney>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

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

- Updates the named entity under its one expectedVersion and publishes the next immutable representation, including owned values. There is no separate configuration or overlay clock.
- Changes to separate Source, Observation or Projection identities do not change this entity. A material change to its own fields or verified bindings does advance its version.
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
- Membership inputs contain only local system/journey IDs; the server stamps origin=LOCAL and source=null. Imported provenance is reserved to the trusted importer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetService

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `version` | `Version` |

**Response:** `service: Service`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListServices

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `systemId` | `Id` |
| `userJourneyId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Service>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Service membership is many-to-many and deduplicated by canonical serviceId; it does not establish journey execution order or end-to-end compliance.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

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

- Updates the named entity under its one expectedVersion and publishes the next immutable representation, including owned values. There is no separate configuration or overlay clock.
- Changes to separate Source, Observation or Projection identities do not change this entity. A material change to its own fields or verified bindings does advance its version.
- Omitted fields are unchanged; an empty description is a known empty value; supplied arrays replace their complete owned membership set.
- Service is the sole membership writer. Every journey must belong to its paired system; a journey update cannot set a second service list.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### GetServiceStatus

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |

**Response:** `projection: Projection`.

- Returns the currently selected SERVICE_STATUS projection under its named rule, including evidence/freshness/coverage. Clients do not infer current state from newest receipt time.
- No current selected projection returns ResourceNotFoundException with code PROJECTION_NOT_AVAILABLE, never an invented healthy/default object.
- Runtime health, native assessed posture, collection quality and operator workflow remain distinct dimensions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetWorkspaceSummary

`READ` · permission `console:ReadWorkspace` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| Empty body | Send `{}` |

**Response:** `projection: Projection`.

- Returns the current qualified WORKSPACE_SUMMARY for the trusted caller's authorized workload scope, including exact distinct contributor identities, denominator and rule.
- An empty authorized scope has null percentages. Retained historical evidence is separate from current usable coverage; no end-to-end journey compliance is inferred.
- A cached broader summary must be recomputed/selected for the authorized scope; hidden records cannot leak through counts.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### GetDependency

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `dependencyId` * | `Id` |
| `version` | `Version` |

**Response:** `dependency: Dependency`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListDependencies

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Dependency>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

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

- expectedVersion addresses Dependency.version. The governance value has no independent version or CRUD lifecycle; changing it publishes the next Dependency representation.
- An allowed/denied decision is local governance. It neither changes DNS evidence nor grants/revokes network access.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## health

### GetHealthEvent

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `version` | `Version` |

**Response:** `healthEvent: HealthEvent`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListHealthEvents

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceCode` | `string` |
| `eventTypeCode` | `string` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<HealthEvent>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetEventContext

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `version` | `Version` |

**Response:** `eventContext: EventContext`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListEventContexts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `kind` | `PUBLIC/ACCOUNT/ORG_SUMMARY` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<EventContext>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetEntityImpact

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `entityImpactId` * | `Id` |
| `version` | `Version` |

**Response:** `entityImpact: EntityImpact`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListEntityImpacts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<EntityImpact>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Account/public/organization-summary evidence never leaks between contexts. Counts remain qualified by collection coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetCommunication

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `communicationId` * | `Id` |
| `version` | `Version` |

**Response:** `communication: Communication`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListCommunications

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `healthEventId` * | `Id` |
| `eventContextId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Communication>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Conflicting and partial notification pages remain visible; delivery recipients do not redefine impacted account identity.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetLifecycleEntry

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `lifecycleEntryId` * | `Id` |
| `version` | `Version` |

**Response:** `lifecycleEntry: LifecycleEntry`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListLifecycleEntries

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `catalogSnapshot` | `EntityRef` |
| `serviceCode` | `string` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<LifecycleEntry>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- catalogSnapshot, when supplied, is an exact LIFECYCLE_CATALOG capture. Entries are selected through that retained manifest, never through a later snapshot head; titles do not establish identity.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetComponentDeployment

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resourceId` * | `Id` |
| `componentDeploymentId` * | `Id` |
| `version` | `Version` |

**Response:** `componentDeployment: ComponentDeployment`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListComponentDeployments

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resourceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ComponentDeployment>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Lifecycle exposure is a separate versioned projection using these observed component versions and a pinned lifecycle catalog.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

## resilience

### GetResiliencePolicy

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `resiliencePolicyId` * | `Id` |
| `version` | `Version` |

**Response:** `resiliencePolicy: ResiliencePolicy`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListResiliencePolicies

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ResiliencePolicy>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetResilienceAssessment

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `resilienceAssessmentId` * | `Id` |
| `version` | `Version` |

**Response:** `resilienceAssessment: ResilienceAssessment`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListResilienceAssessments

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ResilienceAssessment>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetFinding

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `version` | `Version` |

**Response:** `finding: Finding`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

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

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Findings are service-scoped. No mandatory assessment filter or ownership FK is invented; capture-to-assessment is qualified correlation.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetRecommendation

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `recommendationId` * | `Id` |
| `version` | `Version` |

**Response:** `recommendation: Recommendation`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListRecommendations

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `source` | `EntityRef` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Recommendation>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- When no stable provider key exists, identity uses finding + exact Source version + group/ordinal. Repeated receipt observations of that same content do not create another recommendation; equal text alone cannot establish continuity across changed source versions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### StartResilienceAssessment

`PROVIDER_COMMAND` · permission `console:RunResilienceAssessment` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `connection` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`.

**Native adapter basis:** `StartFailureModeAssessment`. These are mapped operations, not identical wire payloads.

- Pins the local Service version and Connection at admission, then requests native StartFailureModeAssessment. expectedVersion is a Service precondition, not an AWS conditional-write token.
- GetCommand exposes the created assessment identity after readback. SUCCESS of assessment execution does not imply achievable posture or verified remediation.
- Findings remain service-scoped and independent of a particular run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### UpdateFindingDisposition

`PROVIDER_COMMAND` · permission `console:UpdateFindingDisposition` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `connection` * | `EntityRef` |
| `expectedSource` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |
| `disposition` * | `OPEN/RESOLVED/IRRELEVANT` |
| `comment` | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateFailureModeFinding`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedVersion guards the named entity head. expectedSource pins the exact source evidence for the native precondition; neither creates an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's version or a stale unrelated summary is rejected even in the same workspace.
- The exact Connection version is recorded at admission; current permissions, revocation and material provider preconditions are checked again at dispatch.
- Maps only status/comment. Disposition is an operator assertion, not a new posture or finding-specific verification.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### UpdateDependencyClassification

`PROVIDER_COMMAND` · permission `console:UpdateDependencyClassification` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `dependencyId` * | `Id` |
| `connection` * | `EntityRef` |
| `expectedSource` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |
| `criticality` | `HARD/SOFT/UNKNOWN` |
| `comment` | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateDependency`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedVersion guards the named entity head. expectedSource pins the exact source evidence for the native precondition; neither creates an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's version or a stale unrelated summary is rejected even in the same workspace.
- The exact Connection version is recorded at admission; current permissions, revocation and material provider preconditions are checked again at dispatch.
- Native criticality/comment and local allowed/denied governance have distinct commands and field authority; both materialize through ordinary versions of Dependency.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### UpdateResiliencePolicyConfiguration

`PROVIDER_COMMAND` · permission `console:ManageProviderConfiguration` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `resiliencePolicyId` * | `Id` |
| `connection` * | `EntityRef` |
| `expectedSource` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |
| `changes` * | `ResiliencePolicyChanges` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdatePolicy`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedVersion guards the named entity head. expectedSource pins the exact source evidence for the native precondition; neither creates an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's version or a stale unrelated summary is rejected even in the same workspace.
- The exact Connection version is recorded at admission; current permissions, revocation and material provider preconditions are checked again at dispatch.
- The narrow supported write subset has four native component families. Explicit detachment/component clearing is deferred until native semantics are verified.
- Policy changes invalidate current applicability without modifying captured policy contexts or historical posture.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### UpdateResilienceServiceConfiguration

`PROVIDER_COMMAND` · permission `console:ManageProviderConfiguration` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `connection` * | `EntityRef` |
| `expectedSource` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |
| `changes` * | `ResilienceServiceChanges` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateService`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedVersion guards the named entity head. expectedSource pins the exact source evidence for the native precondition; neither creates an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's version or a stale unrelated summary is rejected even in the same workspace.
- The exact Connection version is recorded at admission; current permissions, revocation and material provider preconditions are checked again at dispatch.
- Changes the verified Resilience Hub service profile only. Local UpdateService remains the canonical catalog/membership command.
- This initial write subset covers description, Regions, direct policy attachment and desired discovery state. Native creation/deletion, association replacement, permissions, report configuration and clearing remain deferred adapter commands.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### UpdateRecommendationEnrichment

`LOCAL_COMMAND` · permission `console:ManageRecommendationMetadata` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `serviceId` * | `Id` |
| `findingId` * | `Id` |
| `recommendationId` * | `Id` |
| `title` | `string` |
| `effort` | `string` |
| `estimate` | `RecommendationEstimate` |
| `note` | `string` |
| `clearFields` | `List<title/effort/estimate>` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `recommendation: Recommendation`.

- expectedVersion refers to Recommendation.version. Enrichment is an owned value without a second version clock; the complete Recommendation receives the next version.
- Estimate amount/currency/basis/complexity/source/time/confidence are typed local information, separate from native assessment execution cost.
- Assignment, work state, completion and verification belong exclusively to a WorkItem targeting this recommendation. This operation cannot maintain a competing recommendation workflow.
- Local estimates do not establish provider remediation or recommendation identity across changed source versions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## investigation

### GetAgentSpace

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `version` | `Version` |

**Response:** `agentSpace: AgentSpace`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListAgentSpaces

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<AgentSpace>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetInvestigation

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `investigationId` * | `Id` |
| `version` | `Version` |

**Response:** `investigation: Investigation`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListInvestigations

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Investigation>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetExecution

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `version` | `Version` |

**Response:** `execution: Execution`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.
- AgentSpace is the owner scope. A single investigation foreign key is not required, preserving chat and shared/referenced executions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListExecutions

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `investigationId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Execution>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- The optional investigation filter uses explicit TaskExecutionMembership evidence. A linked task can reference an execution created elsewhere in the same AgentSpace.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetJournalRecord

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `journalRecordId` * | `Id` |
| `version` | `Version` |

**Response:** `journalRecord: JournalRecord`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListJournalRecords

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<JournalRecord>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- Journal record identity, raw native type and graph extraction provenance remain separate; a textual mention does not create a graph link.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetApprovalRequest

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `approvalRequestId` * | `Id` |
| `version` | `Version` |

**Response:** `approvalRequest: ApprovalRequest`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListApprovalRequests

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<ApprovalRequest>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- These are retained validated chat request contexts, not a fabricated native Get/ListApproval API. A waiting task or Markdown button is insufficient.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetAsset

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `assetId` * | `Id` |
| `version` | `Version` |

**Response:** `asset: Asset`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
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

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### StartInvestigation

`PROVIDER_COMMAND` · permission `console:StartInvestigation` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `connection` * | `EntityRef` |
| `title` * | `string` |
| `description` | `string` |
| `priority` * | `CRITICAL/HIGH/MEDIUM/LOW/MINIMAL` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`.

**Native adapter basis:** `CreateBacklogTask`. These are mapped operations, not identical wire payloads.

- Requests CreateBacklogTask with taskType=INVESTIGATION; it is not a native operation named StartInvestigation.
- expectedVersion guards the AgentSpace head used for admission. The Connection version is pinned and current authority rechecked before dispatch.
- A task creation receipt does not prove execution started. Native task, execution and result observations are reconciled separately.
- The adapter maps the durable console intent to a stable provider token within native bounds; no raw tenant/actor is accepted.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### DecideApproval

`PROVIDER_COMMAND` · permission `console:DecideApproval` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `approvalRequestId` * | `Id` |
| `connection` * | `EntityRef` |
| `expectedRequestSource` * | `EntityRef` |
| `expectedActionDigest` * | `Digest` |
| `decision` * | `APPROVED/REJECTED` |
| `singleUse` | `literal true` |
| `reason` | `string` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`.

**Native adapter basis:** `UpdateApprovalAction`. These are mapped operations, not identical wire payloads.

- First-release decision supports exact observed scope and single use only; reusable grants and pattern editing are explicitly deferred.
- expectedVersion guards ApprovalRequest; expectedRequestSource selects its exact retained request content. A version from another request or source object is rejected.
- APPROVED requires singleUse=true. REJECTED omits singleUse; the adapter also omits native pattern and TTL fields for rejection.
- Validates a complete authenticated chat request context and exact action digest, then invokes UpdateApprovalAction. It neither resumes the execution nor claims the tool ran.
- Admission records reconstructable Command.approvalDecision with the exact ApprovalRequest version, request Source, action digest, decision, singleUse and copied requested pattern. Only VALIDATED observed invocation context is dispatchable; missing or unsupported context is rejected.
- Native UpdateApprovalAction has no modeled idempotency token. A lost response is OUTCOME_UNKNOWN; local replay returns the receipt and must not repeat the remote mutation blindly.
- A successful rejection is a successful decision command, not a provider API failure.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### ResumeExecution

`PROVIDER_COMMAND` · permission `console:ResumeExecution` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `agentSpaceId` * | `Id` |
| `executionId` * | `Id` |
| `approvalRequest` * | `EntityRef` |
| `decisionCommand` * | `EntityRef` |
| `connection` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`.

**Native adapter basis:** `SendMessage`. These are mapped operations, not identical wire payloads.

- Requires a definitively successful matching decision Command, valid current authorization and a validated approval/interrupt/tool-use context.
- Records Command.approvalResume with the exact request, successful decision Command, and native action identifiers. This dispatch receipt does not establish tool execution or action effect.
- expectedVersion guards Execution; approvalRequest and decisionCommand are exact retained representations. An ACCEPTED decision version is insufficient even if a later command version has succeeded.
- Constructs the native SendMessage APPROVAL_ACTION context from that retained request; the caller cannot substitute interrupt/tool IDs or widen approved scope.
- Decision, resume submission, credential redemption and actual tool outcome remain separate. Opening or completing a stream does not prove the tool succeeded.
- SendMessage has no modeled idempotency token. Persist stream fragments and unknown outcomes; do not blindly resend on disconnect.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## workflow

### CreateScenario

`LOCAL_COMMAND` · permission `console:AuthorScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `name` * | `string` |
| `description` | `string` |
| `definition` * | `ScenarioDraft` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `scenario: Scenario`.

- Creates Scenario version 1 in DRAFT state. An author cannot set trusted operation locks, publication state, version, timestamps or digest.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`.

### GetScenario

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `version` | `Version` |

**Response:** `scenario: Scenario`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListScenarios

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `state` | `DRAFT/PUBLISHED/ARCHIVED` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Scenario>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### UpdateScenario

`LOCAL_COMMAND` · permission `console:AuthorScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `name` | `string` |
| `description` | `string` |
| `definition` | `ScenarioDraft` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `scenario: Scenario`.

- Publishes the next ordinary Scenario version in DRAFT state, under the current entity expectedVersion. Previously published versions and admitted Runs remain unchanged.
- Omitted fields preserve draft values. Reopening a PUBLISHED or ARCHIVED head requires an explicit authoring definition; the server never treats locked published content as an editable draft implicitly.
- Editing an ARCHIVED head is a deliberate guarded reopening. The newly created DRAFT version does not make itself executable; StartRun still requires an exact PUBLISHED version.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### PublishScenario

`LOCAL_COMMAND` · permission `console:PublishScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `scenario: Scenario`.

- Compiles the exact current DRAFT representation, resolves immutable implementation/schema locks and creates the next PUBLISHED version of the same Scenario identity.
- Publication validates DAGs, dependency-scoped references, typed bindings, capability checks, required criteria, finalizers and fixed language/reducer semantics before any external work.
- The caller cannot submit a trusted lock or digest. A later alias change cannot alter a published version. Missing/revoked pinned artifacts reject future admission rather than substituting another implementation.
- GetScenario with version retrieves any retained representation; ListEntityVersions enumerates history. There is no ScenarioRevision resource or default revision pointer.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### ArchiveScenario

`LOCAL_COMMAND` · permission `console:AuthorScenario` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `scenarioId` * | `Id` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `scenario: Scenario`.

- Creates the next Scenario version in ARCHIVED state, retaining the prior definition and publication facts.
- A current ARCHIVED head blocks new Run admissions for every version of that Scenario. It does not redirect, cancel or change previously admitted Runs, and exact admission replay still returns its original receipt.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### StartRun

`EXECUTION_COMMAND` · permission `console:StartRun` · implementation gate `P4_WORKFLOW_RUNTIME`

| Request member | Type |
| --- | --- |
| `scenario` * | `EntityRef` |
| `subject` * | `EntityRef` |
| `inputs` * | `object` |
| `bindings` * | `object` |
| `clientToken` * | `string` |

**Response:** `command: Command`; `run: Run`; `snapshot: Snapshot`; `steps: List<StepRun>`.

- Durably admits one Run at version 1, its StepRuns and a closed RUN_INPUT snapshot atomically; no claim that an AWS call has started.
- scenario pins an exact PUBLISHED Scenario version. The current Scenario head is checked separately: ARCHIVED blocks new admission; a newer DRAFT does not replace the explicitly selected published program.
- subject and connection bindings pin exact versions. Admission requires the subject and binding versions still meet the current admission preconditions; current authorization and material provider preconditions are rechecked at dispatch.
- inputs must pass the published version's pinned closed input schema; unknown binding names, raw secrets, undeclared operations or unauthorized scope are rejected.
- Admission fixes enabled steps and the required-criterion denominator. Runtime skips/cancellation cannot shrink it; inapplicable admission criteria remain recorded.
- A new execution intent uses a new clientToken. Neither a latest selector nor a mutable default pointer may select the executed program.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`, `EvidenceUnavailableException`.

### GetRun

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `version` | `Version` |

**Response:** `run: Run`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListRuns

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `scenario` | `EntityRef` |
| `phase` | `ADMITTED/RUNNING/FINALIZING/TERMINAL` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Run>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### RequestRunCancellation

`EXECUTION_COMMAND` · permission `console:CancelRun` · implementation gate `P4_WORKFLOW_RUNTIME`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `reason` | `string` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |

**Response:** `command: Command`; `accepted: boolean`; `run: Run`.

- Under the supplied current Run.version, atomically records monotonic cancellation intent in the next version and fences new main dispatch. It does not set a remote effect to stopped.
- Exact replay is resolved before current-version checks. If the expectedVersion still matches an already sealed Run, the command returns accepted=false and that unchanged terminal representation.
- Finalizers reconcile active/unknown effects, including a lost Start response with no handle. A creating Start must never be reissued after cancellation just to discover its result.
- Concurrent cancellation intents converge on the first accepted intent after version/replay resolution. Cleanup, execution result and workload verdict remain independently visible.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

### GetStepRun

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `stepRunId` * | `Id` |
| `version` | `Version` |

**Response:** `stepRun: StepRun`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListRunSteps

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `runVersion` | `Version` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `parent: EntityRef`; `items: List<StepRun>`; `page: Page`; `nextToken?: string`.

- Selects the exact Run version when runVersion is supplied; otherwise selects its current head once. The response identifies that selected parent.
- Returns the exact StepRun versions named in Run.steps, never current child heads or a timestamp-based reconstruction. A missing referenced version fails the read.
- Pagination binds the selected parent version and its immutable member set. Current authorization applies to parent and every returned child.
- Includes every compiled step, including skipped zero-attempt steps. No independent retry/stop/status-update command exists.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### GetStepAttempt

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `stepRunId` * | `Id` |
| `stepAttemptId` * | `Id` |
| `version` | `Version` |

**Response:** `stepAttempt: StepAttempt`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListStepAttempts

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `runId` * | `Id` |
| `stepRunId` * | `Id` |
| `stepRunVersion` | `Version` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `parent: EntityRef`; `items: List<StepAttempt>`; `page: Page`; `nextToken?: string`.

- Selects the exact StepRun version when stepRunVersion is supplied; otherwise selects its current head once. The response identifies that selected parent.
- Returns the exact StepAttempt versions named in StepRun.attempts, never current child heads or a timestamp-based reconstruction. A missing referenced version fails the read.
- Pagination binds the selected parent version and its immutable member set. Current authorization applies to parent and every returned child.
- Ordered by attemptNo; polling/resume/transport retry remain within the same attempt. A new mutating attempt is forbidden while its predecessor's effect is unresolved.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

## fis

### GetExperiment

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `experimentId` * | `Id` |
| `version` | `Version` |

**Response:** `experiment: Experiment`.

- Returns retained canonical data with its provenance; does not fetch AWS synchronously.
- An explicit version selects that exact immutable representation. Omission selects the current head once. An absent/unavailable version never falls back to another version.
- Every supplied parent must agree with the stored record; a mismatch is not a cross-scope search.
- Native actions are keyed by experiment + actionName; their catalog actionId is not an execution identity.
- Selected memberships, applied effects, workload criteria and report readiness are separate evidence dimensions.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `EvidenceUnavailableException`.

### ListExperiments

`READ` · permission `console:Read` · implementation gate `P2_READ_AND_INGEST`

| Request member | Type |
| --- | --- |
| `connectionId` | `Id` |
| `runId` | `Id` |
| `maxResults` | `integer` |
| `nextToken` | `string` |

**Response:** `items: List<Experiment>`; `page: Page`; `nextToken?: string`.

- Stable local snapshot traversal returns one selected head per logical identity, pinned to the traversal's publication; nextToken is absent only at the end.
- Each returned entity carries version, createdAt and updatedAt. ListEntityVersions enumerates the retained versions of one identity separately.
- A completed local traversal does not establish complete upstream collection or claim coverage.
- runId filters only verified ExternalOperationRef links; imported experiments can have no product workflow Run.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `PaginationTokenExpiredException`, `EvidenceUnavailableException`.

### StopExperiment

`PROVIDER_COMMAND` · permission `console:StopExperiment` · implementation gate `P3_DURABLE_COMMANDS`

| Request member | Type |
| --- | --- |
| `experimentId` * | `Id` |
| `connection` * | `EntityRef` |
| `expectedSource` * | `EntityRef` |
| `clientToken` * | `string` |
| `expectedVersion` * | `Version` |
| `reason` | `string` |

**Response:** `command: Command`.

**Native adapter basis:** `StopExperiment`. These are mapped operations, not identical wire payloads.

- Admits a durable command and returns its receipt. Provider dispatch and authoritative observation reconciliation occur later.
- expectedVersion guards the named entity head. expectedSource pins the exact source evidence for the native precondition; neither creates an AWS compare-and-swap guarantee.
- The adapter resolves verified native aliases and enforces connection scope. An ambiguous provider response becomes OUTCOME_UNKNOWN until safe reconciliation.
- The source precondition must belong to this exact native object and an appropriate configuration/detail representation. A different object's version or a stale unrelated summary is rejected even in the same workspace.
- The exact Connection version is recorded at admission; current permissions, revocation and material provider preconditions are checked again at dispatch.
- Requests native StopExperiment for the whole experiment; no individual native action stop/retry/pause command is fabricated.
- Stop acceptance, final native state, post-action cleanup, workload recovery and report completion remain separate.
- Starting new fault experiments is available only through an explicitly authorized pinned workflow adapter in this initial facade.

**Errors:** `ValidationException`, `UnauthenticatedException`, `AccessDeniedException`, `ResourceNotFoundException`, `ThrottlingException`, `InternalServerException`, `ServiceUnavailableException`, `IdempotencyConflictException`, `CommandInProgressException`, `InvalidStateException`, `VersionConflictException`.

## Entity coverage

Every canonical entity is returned by a named getter or scoped full-record list. Owned values are returned by their owner; no artificial CRUD lifecycle is introduced.

| Entity | Read operations |
| --- | --- |
| `Workspace` | `GetWorkspace`, `ListEntityVersions` |
| `Connection` | `ListEntityVersions`, `GetConnection`, `ListConnections` |
| `Resource` | `ListEntityVersions`, `GetResource`, `ListResources` |
| `Collection` | `ListEntityVersions`, `GetCollection`, `ListCollections` |
| `ReadAttempt` | `ListEntityVersions`, `GetReadAttempt`, `ListReadAttempts` |
| `Source` | `ListEntityVersions`, `GetSource`, `ListSources` |
| `Observation` | `ListEntityVersions`, `GetObservation`, `ListObservations` |
| `Projection` | `ListEntityVersions`, `GetProjection`, `ListProjections`, `GetServiceStatus`, `GetWorkspaceSummary` |
| `Snapshot` | `ListEntityVersions`, `GetSnapshot`, `ListSnapshots` |
| `WorkItem` | `ListEntityVersions`, `GetWorkItem`, `ListWorkItems` |
| `Command` | `ListEntityVersions`, `GetCommand`, `ListCommands` |
| `System` | `ListEntityVersions`, `GetSystem`, `ListSystems` |
| `UserJourney` | `ListEntityVersions`, `GetUserJourney`, `ListUserJourneys` |
| `Service` | `ListEntityVersions`, `GetService`, `ListServices` |
| `Dependency` | `ListEntityVersions`, `GetDependency`, `ListDependencies` |
| `HealthEvent` | `ListEntityVersions`, `GetHealthEvent`, `ListHealthEvents` |
| `EventContext` | `ListEntityVersions`, `GetEventContext`, `ListEventContexts` |
| `EntityImpact` | `ListEntityVersions`, `GetEntityImpact`, `ListEntityImpacts` |
| `Communication` | `ListEntityVersions`, `GetCommunication`, `ListCommunications` |
| `LifecycleEntry` | `ListEntityVersions`, `GetLifecycleEntry`, `ListLifecycleEntries` |
| `ComponentDeployment` | `ListEntityVersions`, `GetComponentDeployment`, `ListComponentDeployments` |
| `ResiliencePolicy` | `ListEntityVersions`, `GetResiliencePolicy`, `ListResiliencePolicies` |
| `ResilienceAssessment` | `ListEntityVersions`, `GetResilienceAssessment`, `ListResilienceAssessments` |
| `Finding` | `ListEntityVersions`, `GetFinding`, `ListFindings` |
| `Recommendation` | `ListEntityVersions`, `GetRecommendation`, `ListRecommendations` |
| `AgentSpace` | `ListEntityVersions`, `GetAgentSpace`, `ListAgentSpaces` |
| `Investigation` | `ListEntityVersions`, `GetInvestigation`, `ListInvestigations` |
| `Execution` | `ListEntityVersions`, `GetExecution`, `ListExecutions` |
| `JournalRecord` | `ListEntityVersions`, `GetJournalRecord`, `ListJournalRecords` |
| `ApprovalRequest` | `ListEntityVersions`, `GetApprovalRequest`, `ListApprovalRequests` |
| `Asset` | `ListEntityVersions`, `GetAsset`, `ListAssets` |
| `Scenario` | `ListEntityVersions`, `GetScenario`, `ListScenarios` |
| `Run` | `ListEntityVersions`, `GetRun`, `ListRuns`, `ListRunSteps` |
| `StepRun` | `ListEntityVersions`, `GetStepRun`, `ListRunSteps`, `ListStepAttempts` |
| `StepAttempt` | `ListEntityVersions`, `GetStepAttempt`, `ListStepAttempts` |
| `Experiment` | `ListEntityVersions`, `GetExperiment`, `ListExperiments` |

## Prior operation migration

This table accounts for every operation in the 44-operation Resilience facade, 16-operation workflow proposal and 101-operation consolidated V1 proposal. V2 intentionally breaks the first consolidated contract; no misleading legacy revision-resource aliases are provided. Changes of scope, transport, version ownership and supported fields are explicit.

| Source | Prior operation | Consolidated operation(s) | Disposition and meaning |
| --- | --- | --- | --- |
| Resilience | `GetSystem` | `GetSystem`, `GetSource` | `CANONICAL_READ_WITH_NATIVE_FACET`. Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge. |
| Resilience | `ListSystems` | `ListSystems`, `ListSources` | `CANONICAL_READ_WITH_NATIVE_FACET`. Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded. |
| Resilience | `GetUserJourney` | `GetUserJourney`, `GetSource` | `CANONICAL_READ_WITH_NATIVE_FACET`. Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge. |
| Resilience | `ListUserJourneys` | `ListUserJourneys`, `ListSources` | `CANONICAL_READ_WITH_NATIVE_FACET`. Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded. |
| Resilience | `GetService` | `GetService`, `GetSource` | `CANONICAL_READ_WITH_NATIVE_FACET`. Local canonical identity is separate from the retained native profile; verified provider binding supplies the bridge. |
| Resilience | `ListServices` | `ListServices`, `ListSources` | `CANONICAL_READ_WITH_NATIVE_FACET`. Canonical catalog list plus typed native source profiles; unresolved native references are not silently discarded. |
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
| Resilience | `ListInputSources` | `ListSources`, `GetSource` | `RETAINED_TYPED_PROFILE`. Use aws.resilience-hub.input-source/v1 and exact service-scoped source identity. |
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
| Resilience | `GetServiceStatus` | `GetServiceStatus` | `QUALIFIED_PROJECTION_READ`. Returns currently selected SERVICE_STATUS Projection with its evidence and independent dimensions. |
| Resilience | `GetWorkspaceSummary` | `GetWorkspaceSummary` | `QUALIFIED_PROJECTION_READ`. Returns WORKSPACE_SUMMARY for authorized contributors, with denominator and rule. |
| Resilience | `ListEvents` | `ListObservations`, `ListSources` | `SHARED_EVIDENCE_READ`. Filter exact subjects/profile/channel evidence; delivery ID never becomes a HealthEvent ID. |
| Resilience | `PutHealthObservation` | `IngestObservation`, `PublishProjection` | `SHARED_TRUSTED_INGEST`. Retain runtime-health source evidence then derive SERVICE_STATUS. This is distinct from AWS Health Event ingestion. |
| Resilience | `IngestEvent` | `IngestObservation`, `StartCollection` | `SHARED_TRUSTED_INGEST`. Retains raw channel evidence and schedules authorized read collection; event body cannot patch authoritative state. |
| Workflow | `GetScenario` | `GetScenario` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListScenarios` | `ListScenarios` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `GetRun` | `GetRun` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListRuns` | `ListRuns` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `RequestRunCancellation` | `RequestRunCancellation` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListRunSteps` | `ListRunSteps` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `ListStepAttempts` | `ListStepAttempts` | `RPC_REBINDING`. Preserves scoped entity/lifecycle semantics; RPC body fields, typed errors and maxResults/nextToken replace resource HTTP conventions. |
| Workflow | `GetScenarioRevision` | `GetScenario` | `UNIFORM_ENTITY_VERSION`. Resolve the migrated Scenario identity and exact version; no separate revision identity exists. |
| Workflow | `ListScenarioRevisions` | `ListEntityVersions` | `UNIFORM_ENTITY_HISTORY`. Enumerate exact Scenario version refs, then GetScenario with version. DRAFT, PUBLISHED and ARCHIVED share one entity history. |
| Workflow | `CreateScenario` | `CreateScenario` | `EXTENDED_AUTHORING_CONTRACT`. Creates metadata and a typed editable draft; trusted operation locks remain publication-owned. |
| Workflow | `UpdateScenario` | `UpdateScenario` | `RPC_REBINDING`. expectedVersion replaces If-Match; omission preserves and explicit allowed clears replace nullable PATCH ambiguity. |
| Workflow | `PublishScenarioRevision` | `UpdateScenario`, `PublishScenario` | `DRAFT_THEN_PUBLISH`. Update the typed draft, then publish under expectedVersion; the server resolves trusted locks and creates the next version of the same Scenario. |
| Workflow | `StartRun` | `StartRun` | `RPC_REBINDING`. Pins canonical subject, exact published Scenario version, validated inputs and authorized connection versions; retains immutable admission and criterion denominator. |
| Workflow | `ListRunEvidence` | `ListObservations`, `ListSources`, `ListProjections` | `SHARED_TYPED_EVIDENCE`. Filter the exact Run subject/producer references; raw source, receipt and derived evidence types stay explicit. |
| Workflow | `GetEvidence` | `GetSource`, `GetObservation`, `GetProjection`, `GetSnapshot` | `SHARED_TYPED_EVIDENCE`. Resolve the discriminated EvidenceRef kind; evidence is not collapsed into an untyped payload. |
| Workflow | `ListOperations` | `GetScenario` | `DYNAMIC_DISCOVERY_DEFERRED`. An exact published Scenario version exposes its locks. Authorized discovery of executable adapter aliases is later registry work; facade operations.json is not that adapter registry. |
| Console V1 | `GetWorkspace` | `GetWorkspace` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetConnection` | `GetConnection` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListConnections` | `ListConnections` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CreateConnection` | `CreateConnection` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateConnection` | `UpdateConnection` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetResource` | `GetResource` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListResources` | `ListResources` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetCollection` | `GetCollection` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListCollections` | `ListCollections` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListReadAttempts` | `ListReadAttempts` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetSourceRevision` | `GetSource` | `BREAKING_CONTRACT_V2`. Stable Source identity plus version replaces the revision ID. |
| Console V1 | `GetObservation` | `GetObservation` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetProjectionRevision` | `GetProjection` | `BREAKING_CONTRACT_V2`. Stable Projection identity plus version replaces the revision ID. |
| Console V1 | `GetSnapshot` | `GetSnapshot` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetWorkItem` | `GetWorkItem` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetCommand` | `GetCommand` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListSourceRevisions` | `ListSources`, `ListEntityVersions` | `BREAKING_CONTRACT_V2`. List current Source heads; enumerate a Source identity's versions through the common history operation. |
| Console V1 | `ListObservations` | `ListObservations` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListProjectionRevisions` | `ListProjections`, `ListEntityVersions` | `BREAKING_CONTRACT_V2`. List current Projection heads and enumerate exact historical versions separately. |
| Console V1 | `ListSnapshots` | `ListSnapshots` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListWorkItems` | `ListWorkItems` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListCommands` | `ListCommands` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `StartCollection` | `StartCollection` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `RecordReadAttempt` | `RecordReadAttempt` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `IngestObservation` | `IngestObservation` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CompleteCollection` | `CompleteCollection` | `BREAKING_CONTRACT_V2`. expectedVersion replaces expectedProjectionVersion; completion creates the next Collection version. |
| Console V1 | `PublishProjection` | `PublishProjection` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CaptureSnapshot` | `CaptureSnapshot` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CreateWorkItem` | `CreateWorkItem` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateWorkItem` | `UpdateWorkItem` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `RecordWorkItemVerification` | `RecordWorkItemVerification` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CreateSystem` | `CreateSystem` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetSystem` | `GetSystem` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListSystems` | `ListSystems` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateSystem` | `UpdateSystem` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CreateUserJourney` | `CreateUserJourney` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetUserJourney` | `GetUserJourney` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListUserJourneys` | `ListUserJourneys` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateUserJourney` | `UpdateUserJourney` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CreateService` | `CreateService` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetService` | `GetService` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListServices` | `ListServices` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateService` | `UpdateService` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetServiceStatus` | `GetServiceStatus` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetWorkspaceSummary` | `GetWorkspaceSummary` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetDependency` | `GetDependency` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListDependencies` | `ListDependencies` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateDependencyGovernance` | `UpdateDependencyGovernance` | `BREAKING_CONTRACT_V2`. expectedVersion guards Dependency.version, including its owned governance value. |
| Console V1 | `GetHealthEvent` | `GetHealthEvent` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListHealthEvents` | `ListHealthEvents` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListEventContexts` | `ListEventContexts` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListEntityImpacts` | `ListEntityImpacts` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListCommunications` | `ListCommunications` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListLifecycleEntries` | `ListLifecycleEntries` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetComponentDeployment` | `GetComponentDeployment` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListComponentDeployments` | `ListComponentDeployments` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetResiliencePolicy` | `GetResiliencePolicy` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListResiliencePolicies` | `ListResiliencePolicies` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetResilienceAssessment` | `GetResilienceAssessment` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListResilienceAssessments` | `ListResilienceAssessments` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetFinding` | `GetFinding` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListFindings` | `ListFindings` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetRecommendation` | `GetRecommendation` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListRecommendations` | `ListRecommendations` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `StartResilienceAssessment` | `StartResilienceAssessment` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateFindingDisposition` | `UpdateFindingDisposition` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateDependencyClassification` | `UpdateDependencyClassification` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateResiliencePolicyConfiguration` | `UpdateResiliencePolicyConfiguration` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateResilienceServiceConfiguration` | `UpdateResilienceServiceConfiguration` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateRecommendationEnrichment` | `UpdateRecommendationEnrichment`, `CreateWorkItem`, `UpdateWorkItem` | `BREAKING_CONTRACT_V2`. Metadata uses Recommendation.version; assignment and work state move to WorkItem with its own identity/version. |
| Console V1 | `GetAgentSpace` | `GetAgentSpace` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListAgentSpaces` | `ListAgentSpaces` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetInvestigation` | `GetInvestigation` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListInvestigations` | `ListInvestigations` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetExecution` | `GetExecution` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListExecutions` | `ListExecutions` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetJournalRecord` | `GetJournalRecord` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListJournalRecords` | `ListJournalRecords` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetApprovalRequest` | `GetApprovalRequest` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListApprovalRequests` | `ListApprovalRequests` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetAsset` | `GetAsset` | `BREAKING_CONTRACT_V2`. Each Asset version carries nativeVersion/source/files directly; the embedded versions array is removed. |
| Console V1 | `ListAssets` | `ListAssets` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `StartInvestigation` | `StartInvestigation` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `DecideApproval` | `DecideApproval` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ResumeExecution` | `ResumeExecution` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `CreateScenario` | `CreateScenario` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetScenario` | `GetScenario` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListScenarios` | `ListScenarios` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `UpdateScenario` | `UpdateScenario`, `ArchiveScenario` | `BREAKING_CONTRACT_V2`. Editing creates a DRAFT version; archival is an explicit guarded intent; defaultRevisionId is removed. |
| Console V1 | `PublishScenarioRevision` | `PublishScenario` | `BREAKING_CONTRACT_V2`. Publication creates the next version of the same Scenario; no revision resource or alias is retained. |
| Console V1 | `GetScenarioRevision` | `GetScenario` | `BREAKING_CONTRACT_V2`. The published program is a Scenario representation selected by version. |
| Console V1 | `ListScenarioRevisions` | `ListEntityVersions` | `BREAKING_CONTRACT_V2`. One Scenario history includes draft, published and archived representations. |
| Console V1 | `StartRun` | `StartRun` | `BREAKING_CONTRACT_V2`. Exact scenario/subject/connection references replace revision IDs and optional subject guards; admission returns matching run, snapshot and step representations. |
| Console V1 | `GetRun` | `GetRun` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListRuns` | `ListRuns` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `RequestRunCancellation` | `RequestRunCancellation` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListRunSteps` | `ListRunSteps` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListStepAttempts` | `ListStepAttempts` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `GetExperiment` | `GetExperiment` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `ListExperiments` | `ListExperiments` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |
| Console V1 | `StopExperiment` | `StopExperiment` | `BREAKING_CONTRACT_V2`. Use the V2 namespace and revised DTO: every entity has version/createdAt/updatedAt; evidence and historical context use exact references. Existing operation names do not imply wire compatibility. |

## Deliberately deferred command families

The previous service packages remain the detailed native API references. This first consolidation defines a narrow provider mutation surface; the rest remain typed source profiles and explicit later adapter work:

| Family | Retained now | Later command work |
| --- | --- | --- |
| Resilience provider systems/journeys/services/policies | Versioned Source records, verified canonical bindings and selected configuration commands | Native creates/deletes, association replacement/detachment, permission/report/input-source configuration and destructive clears |
| FIS templates/catalog/resource types/safety lever | Typed source profiles; experiment reads and whole-experiment stop | Template CRUD and scope-wide safety-lever mutation after dedicated authorization and adapter semantics |
| DevOps registration/association/webhook/goal/recommendation/trigger/operator/private connection | Typed source DTOs and their exact scopes through Source reads | Provider management commands; no native recommendation is conflated with Resilience recommendation identity |
| Asset byte access | Versioned artifact references and read authorization boundary | Expiring artifact download/upload grants and binary transport, with independent content access |
| Workflow execution | Published program, admission, cancellation and owned execution read contracts | Durable dispatch, recovery, retries, leases, fences, source coverage and cloud adapters |
| Retention/deletion | Immutable evidence identity and unavailable/tombstone semantics | Retention policy execution and explicitly guarded destructive commands |

These are delivery boundaries, not discarded models. [MAPPING.md](../MAPPING.md) and [adapter-profiles.json](../model/adapter-profiles.json) retain every reviewed source concept and native family.
