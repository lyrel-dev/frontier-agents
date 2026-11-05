# Consolidated Operations Console — RPC protocol

**API date:** 5 November 2026. **Contract revision:** 2. **Status:** phase-one model and operation specification. This package defines contracts and synthetic examples; it does not implement an HTTP service, authentication, persistence, an AWS adapter or a workflow scheduler.

Revision 2 corrects the first consolidated proposal: every entity uses the same version contract; source, projection and scenario histories are no longer separate revision resources. The namespace is **`ConsolidatedOperationsConsole_20261105V2`**. The earlier namespace is superseded, with explicit operation dispositions in [OPERATIONS.md](OPERATIONS.md); no compatibility aliases disguise changed identity or concurrency semantics.

[operations.json](operations.json) records all 108 operation contracts, permissions, effect categories and predecessor mappings. [rpc.schema.json](rpc.schema.json) defines exact requests, responses and errors against [the authoritative model](../model/schema.json). Examples describe independent situations with explicit prior-head preconditions, not one transaction log against the final fixture heads.

## 1. Wire format

| Concern | Contract |
| --- | --- |
| Method and path | `POST /` |
| Media type | `application/x-amz-json-1.1` for request, success and error JSON |
| Selector | `X-Amz-Target: ConsolidatedOperationsConsole_20261105V2.<Operation>` |
| Naming | PascalCase operations; lowerCamelCase JSON members |
| Success | HTTP 200 with the operation-specific result, including an admitted asynchronous command |
| Empty input | `{}`; an empty body is normalized only for an operation whose request schema accepts `{}` |
| Failure | Non-2xx status, typed JSON error, `x-amzn-ErrorType` and `x-amzn-RequestId` |
| Correlation | A fresh request ID per HTTP attempt; `clientToken` identifies one mutation intent |
| Time | Finite epoch seconds, maximum millisecond precision |
| Request limit | 1 MiB UTF-8 body plus the operation's string, map and collection bounds |
| Response budget | 8 MiB; a page may contain fewer than `maxResults`; large bytes use managed artifact references |
| Authentication | Trusted deployment context; this specification does not select or implement the authentication layer |

The root POST, target selector, media type and default numeric timestamp conventions follow the [Smithy AWS JSON 1.1 protocol](https://smithy.io/2.0/aws/protocols/aws-json-1_1-protocol.html). The namespace, operation set, permissions, bounds and concurrency rules are application choices. This is an AWS RPC style facade; AWS endpoint compatibility, SigV4 support and generated SDK conformance are separate implementation concerns.

```http
POST / HTTP/1.1
Host: console.example.invalid
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ConsolidatedOperationsConsole_20261105V2.GetService

{"serviceId":"svc-checkout","version":1}
```

The example host is documentation only. An adapter uses the real provider's SDK and transport; it does not forward the console body unchanged. Native response streams are retained behind the finite command and evidence contracts.

## 2. Scope and authority

The authenticated session establishes the Workspace, acting principal and current permissions. Body fields cannot select a tenant, role, actor or credential. A supplied Connection reference selects an already managed access path and an exact configuration version; it grants no authority itself. Admission and dispatch still check the caller, the connection's current validity, provider scope and revocation.

Workspace provisioning/selection, identity federation and module administration remain deployment concerns. `GetWorkspace` reads the already selected Workspace. A Workspace identity passed to `ListEntityVersions` must equal that trusted Workspace; the generic history operation cannot select another tenant.

Canonical IDs are opaque and scoped to Workspace. Every supplied parent must match the target's stored ownership. For example, a Finding is scoped to Service and a JournalRecord to AgentSpace/Execution. A wrong parent is an absent/invisible result, never a cross-scope search. Execution has an AgentSpace owner and observed task memberships; the API does not invent one mandatory investigation parent.

Structural parent IDs identify relationships only. They do not implicitly load the latest mutable parent into a historical response. If a historical view displays the parent's name, configuration or other mutable content, that parent's exact version must be retained in the view's evidence or capture.

Source identity retains its complete provider ownership tuple independently of the observing connection. Matching names, hashes or unqualified native IDs cannot establish object identity. Provider bindings are established by trusted mapping, not arbitrary caller assertions.

Current authorization is checked on reads, history, pagination, token replay, artifact access and provider dispatch. Historical versions do not preserve a caller's former entitlement. Getters authorize the target and its retained evidence closure. Projection and Snapshot reads require authorization to the complete returned closure, including embedded contributor values/counts; this initial contract denies an incomplete read rather than inventing an undocumented redacted shape. Lists expose authorized complete rows and no hidden aggregate count.

Catalog permissions are proposed application capabilities, not IAM action names. `ListEntityVersions` requires history capability and the entity's domain-read permission. It cannot become a generic route around domain authorization.

## 3. One version contract for every entity

Every entity representation contains the same metadata:

| Member | Meaning |
| --- | --- |
| The entity's named ID | Stable logical identity within Workspace |
| `version` | Positive server-assigned integer for an immutable representation of that identity |
| `createdAt` | Local creation time of the logical entity; constant across its versions |
| `updatedAt` | Local publication time of this representation; nondecreasing across versions |

A successful material change appends the next version of the same entity. It never rewrites an older representation. The whole entity is the concurrency boundary, including owned values. There is no separate `projectionVersion`, nested enrichment/governance clock, `localUpdatedAt`, or independently addressable Version entity. Provider-native version strings, schema/profile versions and attempt numbers retain their own domain meanings; none substitutes for entity `version`.

Versioning does not grant arbitrary write access. A Source is collector-owned, a Projection is derivation-owned, and workflow facts have workflow authority. A sealed Observation or completed attempt may only have its initial/sealed representations. A new writer is not added merely to exercise version 2. `CaptureSnapshot` currently creates a new logical capture at version 1; a guarded correction writer is explicitly deferred, while any retained Snapshot versions use the same read contract.

### Stable domain identity and history

`Source` represents one scoped native identity, representation, profile and source operation. Content digest and provider version do not determine its logical ID. An unchanged consecutive poll can reference the same Source version in a new Observation. An accepted A → B → A content sequence produces versions 1 → 2 → 3; byte deduplication cannot relabel the last state as version 1. This sequence is local retained history, not proof that provider event time has the same ordering.

`Projection` represents a named view over subject identities. New accepted inputs or rule versions produce another version of that view. Input references pin exact versions; an interpretation never changes the source subjects or makes their evidence newer.

`Scenario` owns DRAFT, PUBLISHED and ARCHIVED representations under one identity. Publication creates the next ordinary Scenario version with validated definition and locks. A Run pins an exact PUBLISHED Scenario representation. `Asset` likewise carries its native content version, Source reference and files directly on each Asset representation; there is no nested inventory of application versions.

### Reference values

| Value | Shape and use |
| --- | --- |
| `EntityIdentity` | `{kind,id}` for live navigation or a deliberately continuing target, such as WorkItem targets |
| `EntityRef` | `{kind,id,version}` for an exact retained entity representation |
| `EvidenceRef` | The same exact fields, restricted to Source, Observation, Projection or Snapshot, with an optional typed locator |

References are values owned by their containing entity, not additional resources. Evidence, command results, admission bindings and snapshot members use exact references. Parent identity links and WorkItem navigation targets are explicitly identity-only; they cannot be substituted for evidence.

### Exact getters and common history

Every entity has `Get<Entity>` with optional `version` (Workspace identity remains server-selected). An explicit version means exactly that representation. Omission selects the current head once. An unknown, unavailable or unauthorized version never falls back to another version. A visible known version with unavailable retained content returns an explicit unavailable error; unknown/invisible identity or version returns the appropriate not-found/access outcome.

`ListEntityVersions` accepts an `EntityIdentity` and pagination, and returns exact EntityRef values ordered by descending version. It enumerates history without inventing Version entities. Resolve a returned reference through the entity's normal getter and its version. Ordinary domain lists return one selected head per logical identity at their fixed traversal publication.

`GetServiceStatus` and `GetWorkspaceSummary` are current-selection convenience operations. Their results are versioned Projection records; historical retrieval uses `GetProjection(projectionId,version)`.

## 4. Operations, writable fields and concurrency

| Category | Authority and effect |
| --- | --- |
| `READ` | Reads retained entities, exact history or a typed current selector; it does not silently collect fresh provider data |
| `LOCAL_COMMAND` | Changes a local entity or creates a capture/publication, returning the result and durable Command |
| `INGEST` | A trusted collector records scoped collection, Source and Observation facts |
| `DERIVE` | An authorized rule computes a Projection from exact inputs; the caller cannot provide the result |
| `PROVIDER_COMMAND` | Admits a narrow external intent; dispatch, reconciliation and observed outcome are separate |
| `EXECUTION_COMMAND` | Admits/cancels an application Run; execution, verdict and cleanup remain distinct |

Local catalogue operations create/edit System, UserJourney and Service metadata. They do not create or rename native AWS resources. Explicit provider commands, such as `UpdateResilienceServiceConfiguration`, operate through verified native bindings. Service remains the sole writer of catalogue membership; reverse journey/service membership is a view.

Requests are closed operation-specific DTOs, not copied read models. Clients cannot set entity versions, server timestamps, actor provenance, provider statuses or derived verdicts. Raw source payloads and scenario inputs are deliberate bounded exceptions to fixed vocabularies, validated against the registered source profile or pinned scenario schema.

Omitted writable fields preserve their values. An array replaces its declared complete owned collection. Empty values retain their explicit meaning. Nullable local members are cleared only through an operation's enumerated `clearFields`; assignment and clearing of the same field is invalid. Provider detachment/clearing is available only where its adapter contract has been established. Validation and reference checks occur before durable admission.

`expectedVersion` always guards the named entity head:

| Operation family | Guarded entity |
| --- | --- |
| Local catalogue, Connection, WorkItem or Scenario edit | That entity, including all owned values |
| Recommendation enrichment | Recommendation; metadata has no independent version |
| Dependency governance | Dependency; governance has no independent version |
| Read-attempt settlement / collection completion | ReadAttempt / Collection |
| Scenario publication / archival | Scenario |
| Run cancellation | Run |
| Provider mutation | Its named canonical target, plus an exact `expectedSource` evidence reference where required |
| New assessment / investigation | The Service / AgentSpace context used for admission |
| Projection publication | Projection; `expectedVersion:null` requires absence of its logical key, a positive value guards its current head |

A material change to an entity's own fields or bindings advances its version. A change to a separate Source, Observation or Projection identity does not. If new evidence changes a domain entity's selected-source reference or other owned field, that domain entity receives a new version too. This avoids both competing clocks and unversioned changes hidden behind a stable version number.

Version reservation and local changes are atomic. A conflict creates no new local representation and no provider dispatch. The caller reads, reviews the change and creates a deliberate new intent; it must not blindly insert a newer version into the old command. Native preconditions compare retained context, not a distributed AWS compare-and-swap. Out-of-band provider changes and lost responses still require reconciliation.

WorkItem solely owns assignment, work state, completion and verification. Recommendation enrichment contains metadata/estimate only. `RecordWorkItemVerification` records an authorized local judgment and exact supporting evidence; local completion or an assessment's technical completion cannot prove provider remediation. Directory assignees can be people/groups/services, while acting principals remain authenticated actors.

## 5. Idempotency and Command versions

Every mutation requires `clientToken`, an opaque 16–128 character intent token. Its replay key is `(trusted workspace, trusted principal, operation, clientToken)`. Canonical request comparison includes all identities, exact references and preconditions. Object member order is insignificant; array order and omitted-versus-present values remain significant unless explicitly stated otherwise. Production canonicalization is a versioned implementation requirement.

Processing order is fixed:

1. Authenticate and authorize the operation and referenced scopes.
2. Reserve/look up the token and compare canonical intent.
3. Return an exact matching successful receipt before current-head/precondition checks, without rerunning work or resolving a reference to latest.
4. Otherwise validate current versions, references, source context, typed inputs and capabilities; atomically persist admission and applicable local results/dispatch intent.
5. Dispatch from the durable fenced intent, then record Command versions as state changes are observed.

A changed payload or precondition with the same token returns `IdempotencyConflictException`. A matching in-flight reservation returns `CommandInProgressException`, the known command ID and a retry delay. Replay still requires current authorization.

A receipt pins the returned entity and Command versions. If Command version 1 was ACCEPTED and version 2 later became SUCCEEDED, replay returns the original version-1 receipt. `GetCommand` without version selects the current head; `GetCommand` with version 1 retrieves the accepted representation. Result references never drift to later object versions.

Authoring, local metadata and collection receipts are retained for at least 24 hours. Run admission/cancellation receipts are retained for the Run's lifetime and at least 90 days after terminal sealing. Unresolved external effects prevent automatic purge. `Command.replayExpiresAt` is the earliest permitted expiry under the current guarantee; active/uncertain work extends it before expiry in a later Command version. The original receipt remains unchanged, so a caller queries current Command for an extended guarantee.

Local replay safety does not supply provider idempotency. An adapter uses a native token only where supported, with a stable mapping from the command identity. A lost response without native replay protection becomes `OUTCOME_UNKNOWN` and requires non-creating reconciliation. Two deliberate identical runs use different tokens. These contracts follow the intent-token reasoning in the [AWS Builders' Library discussion of safe retries](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/); the console's scope/retention choices are explicit application policy.

## 6. Admission, publication and asynchronous outcomes

HTTP 200 for an asynchronous command means the documented intent was admitted or its original receipt replayed. Provider commands initially return an ACCEPTED Command. Later Command versions describe dispatch/reconciliation, while domain objects advance only from their own authoritative observations. A failed command can still be read successfully with `GetCommand`.

| Command | Admission establishes | Separate evidence remains necessary |
| --- | --- | --- |
| StartResilienceAssessment | Intent to call native StartFailureModeAssessment | Assessment identity, execution outcome, posture and finding-specific remediation |
| StartInvestigation | Intent to create an investigation Task | Execution, journal/result content and workload recovery |
| DecideApproval | Decision intent for an exact validated request | Definitive provider decision, resume and tool outcome |
| ResumeExecution | Resume intent tied to a definitive decision version | Resume observation, credential redemption and actual tool effects |
| StopExperiment | Intent to stop the native experiment | Terminal native state, cleanup, recovery and report availability |
| StartRun | Run, StepRuns and frozen input Snapshot admitted atomically | Execution, criteria, cleanup and every external effect |
| RequestRunCancellation | Monotonic cancellation intent and dispatch fencing | Remote cessation and completed required finalization |

`DecideApproval` guards the ApprovalRequest version, exact `expectedRequestSource` and action digest. APPROVED requires `singleUse=true`; REJECTED omits it and its adapter omits native pattern/TTL fields. `ResumeExecution` requires an exact successful decision Command version and exact approval context. An ACCEPTED decision version is insufficient even if the command's current head later succeeds. Neither operation infers approval from text, a pending task or a guessed tool name. Lost native decision/resume responses are uncertain effects, not permission to resend blindly.

Scenario creation/editing produces DRAFT versions. Reopening a PUBLISHED or ARCHIVED head through `UpdateScenario` requires an explicit authoring definition and the current expectedVersion. `PublishScenario` validates the draft, resolves trusted implementation/schema locks and creates the next PUBLISHED version. `ArchiveScenario` creates the next ARCHIVED version. There is no separate ScenarioRevision resource or mutable default pointer.

`StartRun` requires the exact PUBLISHED Scenario, subject and Connection versions. It checks the current Scenario head independently: ARCHIVED blocks new admissions; a later DRAFT does not replace the explicitly selected earlier publication. It pins inputs, bindings, enabled steps and required-criterion denominator. Runtime skips cannot shrink that denominator. The response includes matching Run, Snapshot and StepRun representations, making the admitted versions inspectable.

A RUN_INPUT Snapshot captures the workload subjects, published definition and authorized input evidence. It does not point back to a future terminal Run. Run points outward to its input Snapshot and exact StepRun versions; StepRun owns exact attempt references and selectedAttempt. This direction prevents historical admission from acquiring later execution facts through a cycle.

Cancellation checks the supplied Run version and records the first accepted intent in the next version. Replay is resolved first. If a new request names the current sealed version, it returns `accepted:false` and the unchanged Run. A stale new intent conflicts instead of silently changing its preconditions. Finalizers use their own bounded budget and non-creating reconciliation; they cannot reissue a creating Start after cancellation merely to discover a lost handle. Unknown effects remain visible and retain the required protection/hold. Later evidence or a new Evaluation Projection can explain a later understanding without rewriting a sealed Run or attempt.

## 7. Lists, parent selections and collection coverage

Lists accept `maxResults` 1–100, default 20, and opaque `nextToken`. Responses contain `items`, `page` metadata and optional `nextToken`; absent token ends traversal, while an empty page alone does not. Ordinary lists return full entity representations, one head per identity selected at the initial publication. `ListEntityVersions` deliberately returns exact reference values. A historical version is read explicitly, not mixed into an ordinary current-object list.

`ListRunSteps(runId,runVersion?)` selects a Run representation and returns the exact StepRun versions in `Run.steps`. `ListStepAttempts(runId,stepRunId,stepRunVersion?)` selects a StepRun and returns its exact `attempts`. Both responses identify the selected parent. If the parent version is omitted, its head is selected once; child resolution still uses exact references. A later child version cannot change an earlier parent response.

`page.traversalId` identifies a 15-minute local pagination publication, not a domain Snapshot. The initial call freezes the ordered exact representations/member set. The token binds Workspace, principal, authorization epoch, operation, parents and their selected versions, filters, page size, sort order and publication sequence. Continuations preserve the query and do not extend expiry. Tampered/mismatched tokens reject; expiry returns `PaginationTokenExpiredException`; revoked access remains revoked.

| List family | Fixed order |
| --- | --- |
| Entity history | Version descending for one identity |
| Run steps | Compiled step order retained in the selected Run.steps |
| Step attempts | attemptNo ascending within the selected StepRun representation |
| Observations | observedAt ascending, then ID |
| Projections | generatedAt descending, then ID |
| Snapshots | capturedAt descending, then ID |
| Commands | acceptedAt descending, then ID |
| Runs | admittedAt descending, then ID |
| Other entity lists | Canonical ID ascending |

A local traversal does not establish an atomic AWS view or complete upstream coverage. Collection queries are fixed for a Collection identity. Before dispatch, the trusted collector durably records ReadAttempt version 1 in STARTED state with exact request Source and authorization context. `RecordReadAttempt` uses expectedVersion to publish settlement under that same identity. A receipt may pin the STARTED attempt while a later coverage record pins its settled version; references do not retarget automatically.

Empty responses retain request/response evidence. A lost response has an explicit unavailable response and error. Collection completion publishes its next version with independently qualified pagination, detail, resolution, identity and claim coverage. A complete list or quiet interval alone cannot establish absence; negative assertions need adequate closed-scope evidence. A positive witness only proves the limited claim defined by its evaluator.

## 8. Time, presence and closed historical captures

Validators parse timestamps with decimal arithmetic, reject unsupported precision before ordering/storage conversion, and compare/store the same accepted value. Native higher precision remains in raw retained evidence with normalization information. NaN, infinity and string substitutes reject.

Entity createdAt/updatedAt are local record times. Provider event/update/measurement time, transport time, observedAt, generatedAt and capture times remain separate facts. Recomputing a projection cannot make its inputs fresh. Receipt order is not provider event order; source selection uses a named rule and exact evidence.

Unknown, unavailable, not requested, omitted, null, known empty and known zero stay distinct. Writable enums are strict; native reads preserve future provider values and field presence. Consumers tolerate compatible optional output additions without defaulting unfamiliar results to success.

`Source.payloadStorage=INLINE` can contain a legitimate JSON null. `ARTIFACT` uses payload:null and a non-null versioned managed ArtifactRef. Null alone never means unavailable content or an empty successful result. Retained content access remains independently authorized.

Snapshot.members is a closed set of exact entity references, including the subjects, selected evidence and supporting reads required by the captured representation. The server closes declared schema references; arbitrary provider JSON is not scanned as if every kind/id/version-shaped value were a domain reference. Structural identity links do not introduce an implicit join to latest. Coverage and capture cutoff must be consistent with member publication times; a capture cannot contain facts recorded after it closed.

The manifest digest covers the complete Snapshot representation except manifestDigest, with members sorted by kind/id/version under the declared canonicalization profile. The fixture implementation is a restricted deterministic JSON example, not a general RFC 8785 conformance claim. Digests detect content mismatch; they do not authenticate provider truth or preserve a revoked entitlement.

## 9. Errors and recovery

```json
{
  "__type":"VersionConflictException",
  "code":"EXPECTED_VERSION_MISMATCH",
  "message":"The service changed; read it before issuing a new intent.",
  "requestId":"req-stale-demo",
  "retryable":false
}
```

Typed exception, stable code and structured field paths are parsing contracts; the human message is not. Optional commandId identifies an admitted/in-flight intent and retryAfterSeconds gives a bounded retry delay.

| HTTP | Exception family | Recovery |
| --- | --- | --- |
| 400 | ValidationException | Correct fields, unions, precision, invalid references/inputs or cursor scope |
| 401/403 | UnauthenticatedException / AccessDeniedException | Establish current identity/authority; never treat denial as an empty result |
| 404 | ResourceNotFoundException | Resolve the exact visible identity/version and required parents; never fall back to head |
| 409 | VersionConflictException / IdempotencyConflictException / InvalidStateException | Read/reconcile, then deliberately change intent if appropriate |
| 409 | CommandInProgressException | Inspect the receipt and retry the identical token/payload after the supplied delay |
| 410 | PaginationTokenExpiredException / EvidenceUnavailableException | Restart traversal or surface unavailable retained content; do not infer absence/success |
| 413/415 | RequestTooLargeException / UnsupportedMediaTypeException | Correct size/transport |
| 429/503 | ThrottlingException / ServiceUnavailableException | Bounded backoff/jitter with the same intent token |
| 500 | InternalServerException | Reconcile the durable receipt; a missing response does not prove absence of effects |

A retryable console error does not authorize reissuing an uncertain provider mutation. The Command and adapter-specific reconciliation decide that. Errors expose neither credentials nor stack traces.

## 10. Compatibility and implementation gates

V2 is a breaking correction of the proposed V1 contract, not a migration of a claimed deployed service. All 101 V1 operations have explicit dispositions, as do the 44 earlier Resilience facade operations and 16 workflow operations. Removed revision-resource operations map to normal entity getters/history and PublishScenario; nested version guards map to their entity owner. Existing names with changed reference or metadata shapes are not wire-compatible aliases.

Compatible future additions include optional output fields and explicitly discoverable operations/profiles. Identity scope, version ownership, parent semantics, units, required inputs, reference selection, state/verdict meaning, pagination, replay and authorization changes require deliberate versioning/migration. Typed adapter profiles extend provider coverage without automatically creating CRUD entities.

| Gate | Evidence still required |
| --- | --- |
| P2 retained reads/ingest | Lossless registered adapters, exact version persistence, source scope, historical authorization, failed/empty read retention and publication-bound pagination |
| P3 commands | Atomic version/token reservation, immutable receipts, durable intent/outbox, provider mapping, current scope checks and non-creating reconciliation |
| P4 workflow | Trusted locks, typed expression conformance, atomic admission, exact child publications, leases/fencing, cancellation races and bounded finalization |

The current checks establish schemas, examples and selected invariants. They do not establish these future runtime guarantees. Native administrative breadth and a guarded Snapshot correction writer remain explicit later work. Existing service prototypes and their results remain source evidence about those earlier packages.

## References

- [Model](../MODEL.md), [mapping](../MAPPING.md), [adapter profiles](../model/adapter-profiles.json), [validation](../VALIDATION.md).
- [Resilience RPC precedent](../../aws/resilience-hub/analysis/api/protocol.md) and [quality review](../../aws/resilience-hub/analysis/quality-review.md).
- [Workflow model](../../aws/fis/analysis/workflow/model.md), [prior HTTP binding](../../aws/fis/analysis/workflow/api.md), [adapter semantics](../../aws/fis/analysis/workflow/adapters.md).
- [DevOps approval/UI contract](../../aws/devops-agent/analysis/annexes/Investigation_UI_Contract.md), [native API catalogue](../../aws/devops-agent/analysis/annexes/Investigation_API_Catalog.md).
- [Smithy AWS JSON 1.1](https://smithy.io/2.0/aws/protocols/aws-json-1_1-protocol.html), [AWS Builders' Library: safe idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/).


## Optional traversal cardinality

`Page.totalResults`, when supplied, is the exact count of the authorized, filtered result set at the traversal's retained `asOfSequence`. It shares the scope and lifetime of `traversalId`, `createdAt` and `expiresAt`; it must not change between pages of that traversal. A new authorization/filter/publication scope requires a new traversal.

Omit the member when the count was not computed. Zero asserts an established empty result set. Never substitute the current page length, an upstream provider aggregate, or an incomplete collection count. Finishing a local traversal still does not establish complete AWS collection coverage. Existing responses without this optional member remain valid.
