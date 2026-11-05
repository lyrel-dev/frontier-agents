# Consolidated operations console — RPC protocol

**Version:** 2026-11-05. **Status:** phase-one contract specification. The deliverable defines the interface for the consolidated model; it does not implement an HTTP service, an AWS adapter, authentication, durable execution or a workflow scheduler. All JSON examples are synthetic and no example operation was executed.

The product exposes one operation-oriented facade and keeps module ownership explicit. Common evidence reads and authoring conventions are shared; Health events, resilience assessments, investigations, workflow Runs and native FIS experiments retain their distinct meanings. [OPERATIONS.md](OPERATIONS.md) describes the operation surface, [operations.json](operations.json) is the machine-readable catalog, and [rpc.schema.json](rpc.schema.json) defines exact inputs and outputs. Outputs reference the authoritative [model schema](../model/schema.json).

## 1. Wire format

| Concern | Contract |
| --- | --- |
| Method and path | `POST /` |
| Media type | `application/x-amz-json-1.1` for request, success and error JSON |
| Selector | `X-Amz-Target: ConsolidatedOperationsConsole_20261105.<Operation>` |
| Operation/member naming | PascalCase operations; lowerCamelCase JSON members |
| Success | HTTP 200 with the operation-specific result, including an asynchronous command receipt |
| Empty input | `{}`; an empty body is normalized to `{}` only for an operation whose schema accepts it |
| Failure | Non-2xx status; typed JSON error; `x-amzn-ErrorType` and `x-amzn-RequestId` headers |
| Correlation | A fresh `x-amzn-RequestId` for each HTTP attempt; `clientToken` identifies one logical mutation |
| Timestamps | Finite epoch seconds, maximum millisecond precision, validated before comparison or storage |
| Request limit | 1 MiB UTF-8 body, plus each schema's string/map/list bounds |
| Response budget | 8 MiB; list pages may contain fewer than `maxResults`; large source bytes use retained artifact references |
| Authentication | Trusted server context from the selected deployment's authentication layer; this specification does not choose or implement that layer |

The POST root, target selector, media type and default numeric timestamp conventions follow the [Smithy AWS JSON 1.1 protocol](https://smithy.io/2.0/aws/protocols/aws-json-1_1-protocol.html), consulted 5 November 2026. The namespace, operation set, permissions, bounds, retention and concurrency guarantees are product choices. This is an **AWS RPC style facade**, with no claim of AWS endpoint compatibility, generated SDK availability, SigV4 support or protocol compliance certification.

```http
POST / HTTP/1.1
Host: console.example.invalid
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ConsolidatedOperationsConsole_20261105.GetService

{"serviceId":"svc-checkout"}
```

The example hostname is documentation only. Native services retain their own protocols. A future adapter uses the appropriate official SDK operation; it does not forward the facade body unchanged. A provider `SendMessage` response stream is collected as source evidence behind a finite console command receipt, rather than being passed through this RPC binding as a new streaming protocol.

## 2. Identity, scope and permission

The authenticated session establishes `workspaceId`, the acting principal and its current capabilities. Request bodies cannot select a tenant, role, actor, authorization context or provider credential. An input such as `connectionId` selects an already managed access path; it is independently checked against the subject and requested provider scope. `credentialBindingId` on the administrative connection command references an already registered credential binding, never secret bytes.

Workspace provisioning and selection, authentication federation and `enabledModules` administration belong to deployment/bootstrap management, outside this initial domain-operation surface. `GetWorkspace` reads the workspace already selected by that trusted context. Connection input uses the normalized provider namespace `aws` exactly.

Every canonical ID is opaque and meaningful only in its containing workspace. Every supplied parent must match the stored child's scope. For example, `GetFinding` requires `serviceId` and `findingId`; `GetJournalRecord` requires AgentSpace, execution and record identities. A wrong parent returns an absent/invisible result without searching another scope. `Execution` belongs to an AgentSpace; task membership is an explicit relation, so `GetExecution` does not invent a mandatory single investigation parent. A native provider identity remains the complete scoped tuple in `SourceIdentity`, independent of which connection observed it.

Permissions in the catalog, such as `console:Read`, `console:IngestEvidence`, `console:ManageCatalog`, `console:DecideApproval` and `console:StartRun`, are proposed application capabilities. They are not IAM action names or proof of AWS access. A deployment may group them into roles, but all authorization decisions remain server-owned. Read access, retained-content access, local configuration writes, source ingestion, rule publication and cloud-effect commands can be granted separately.

Authorization is rechecked on normal reads, token replay, pagination continuation, artifact access and command dispatch. A snapshot records historical evidence; it does not freeze the caller's entitlement to that evidence. Direct lookup by a SourceRevision ID must enforce the native owning scope and permitted observation provenance. A content digest, guessed ID or existing cross-module reference never substitutes for authorization.

Workspace membership alone does not expose evidence collected through a broader connection or principal. Getters authorize both the target and its evidence closure. List rows, counts, contributor sets and cached summaries are computed for the authorized subset; a broader cached total cannot leak hidden records. Cursor scope includes the current authorization epoch. Denied or expired content remains explicitly unavailable and is never substituted with an apparently fresh observation.

`GetProjectionRevision` and `GetSnapshot` require current access to the entire returned retained closure, including embedded values and contributor counts. If that access is incomplete, this initial contract denies the read; a future explicit redacted representation would need its own shape and qualified coverage. Generic lists return only authorized complete records and disclose no hidden aggregate count.

## 3. Operation categories and ownership

| Category | Authority and result |
| --- | --- |
| `READ` | Reads retained canonical entities or scoped, fully typed records. Does not silently trigger a fresh provider collection. |
| `LOCAL_COMMAND` | Changes a named local configuration or workflow record, or creates an immutable capture/publication. Returns that result and its durable Command receipt. |
| `INGEST` | A trusted collector records queries, requests, raw source revisions and observations. Validation checks its registered source profile and scope. |
| `DERIVE` | A trusted projector computes a new immutable ProjectionRevision from exact retained inputs and an authorized immutable rule. |
| `PROVIDER_COMMAND` | Admits an explicit narrow remote intent. Returns a Command; dispatch, uncertain outcome reconciliation and authoritative readback are separate. |
| `EXECUTION_COMMAND` | Admits or cancels a product workflow Run. Its execution, assessment and cleanup remain separate. |

`CreateSystem`, `CreateUserJourney`, `CreateService` and their local updates manage the canonical workload catalog. They do not create or rename AWS resources. Native configuration commands have explicit names, such as `UpdateResilienceServiceConfiguration`. Trusted provider bindings connect the two identity spaces. Matching names cannot establish that a Resilience Hub service, a DevOps registered integration and a business workload are the same entity.

Service membership write DTOs contain only `systemId` and `userJourneyIds`. The server validates same-system ownership and stamps local origin with no claimed source revision. A caller cannot mark a membership as imported or attach forged provider provenance. The trusted importer owns those source-backed mappings.

Immutable evidence, observed provider objects, graph values and owned execution children do not receive artificial CRUD operations. Ingestion produces source-backed records. `PublishProjection` accepts input references and the rule identity; it accepts no caller-provided result, verdict, coverage or generated timestamp. `CaptureSnapshot` builds a closed manifest from retained inputs; a client cannot create a replacement `RUN_INPUT` snapshot and attach it to an existing Run.

## 4. Writable fields, clearing and revisions

All request DTOs are closed. A read response is not an update input. Passing `workspaceId`, an acting `actor`, a provider status, an immutable ID, an observation timestamp or an arbitrary field not named by that operation fails validation before a mutation is accepted. Registered raw source payloads and scenario inputs are explicit exceptions to fixed field vocabularies: their known data is validated against a versioned source profile or pinned scenario input schema, with the same body-size bound. Neither is executable code merely because a document contains text.

The update rules are consistent:

- Omitted writable members preserve existing values.
- Empty strings and arrays are known supplied values; an array replaces that operation's complete owned collection after reference validation.
- A nullable local field is cleared only through that operation's enumerated `clearFields`. The same field cannot be assigned and cleared in one request. Description fields are non-null strings; `""` is a known empty description.
- Provider field detachment/clearing is available only after its specific adapter semantics have been established. No generic provider patch, `fieldsToClear` forwarding or copy-the-read-object update is provided.
- Every update must make at least one declared change. Validation and reference checks complete before any local write or durable command admission.

`expectedVersion` names the exact mutable local ownership boundary:

| Operation family | Version checked |
| --- | --- |
| Local System/UserJourney/Service/Connection/Scenario/WorkItem update | That entity's `version` |
| `PublishScenarioRevision` | The editable Scenario version whose draft is being published |
| `UpdateRecommendationEnrichment` | `recommendation.enrichment.version` |
| `UpdateDependencyGovernance` | `dependency.governance.version` |
| `CompleteCollection` | Explicit `expectedProjectionVersion` fences a collector completion, separately from configuration versions |
| Provider configuration command | Explicit `expectedSourceRevisionId` compares retained observation context; it is not an AWS conditional-write token |

Ordinary observation, event and projection arrival does not consume a local configuration version. Material local membership edits can invalidate a current derived view without changing a historical snapshot. Provider fields remain in their source evidence; a local edit time never fills a missing provider update time.

`assigneeSubjectId` assigns a WorkItem or recommendation owner through the trusted workspace directory; it never selects the acting principal. `RecordWorkItemVerification` records a separately authorized local judgment, rationale and exact supporting evidence under the WorkItem version. A `VERIFIED` judgment needs independent supporting evidence under the applicable verification policy; simply marking work resolved, suppressing a finding or observing an assessment complete is insufficient. This updates local verification metadata without writing provider status or posture. Recommendation estimates retain their amount, currency, basis, complexity, source, estimate time and confidence; the server separately stamps enrichment edit provenance/time.

Assignment can resolve to a person, group/team or service through `AssigneeRef`. Audit actors remain authenticated humans/services through `ActorRef`; assigning a team cannot make that team an acting authentication principal.

The server reserves mutation intent and compares versions atomically. A version conflict leaves local state unchanged and creates no remote dispatch. A caller fetches the current record, reviews the intervening change, and issues a new deliberate intent with a new token. It does not automatically substitute the newest version into the old command.

## 5. Idempotency and durable command receipts

Every mutation requires `clientToken`, an opaque 16–128 character value for one user or worker intent. The replay key is `(trusted workspace, trusted principal, operation, clientToken)`. Canonical request comparison includes the complete validated body, subject identities and preconditions. JSON object member ordering is insignificant; array order and omitted-versus-present values remain significant unless an operation explicitly defines otherwise. The canonicalization algorithm is a versioned implementation requirement, not a property of arbitrary JSON serialization.

This intent-token approach follows the [AWS Builders' Library discussion of safe idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/), consulted 5 November 2026. The concrete scope and retention choices below belong to the console. Equal request parameters do not prove equal intent; two deliberate identical runs use different tokens.

Processing order is significant:

1. Authenticate and authorize the operation and all referenced scopes.
2. Look up/reserve the token and compare its canonical intent.
3. If a matching successful receipt already exists, return the original operation result without reapplying current-version checks, re-resolving aliases or repeating side effects. A fresh HTTP request ID is still assigned.
4. Otherwise validate current versions, source preconditions, references, typed inputs and capability gates; atomically commit the intent and its applicable local result/dispatch record.
5. Dispatch provider work only from a durable fenced intent. Record attempts and uncertainty. Read the Command and resulting domain entities to obtain subsequent state.

A changed payload or precondition with the same token returns `IdempotencyConflictException`. A matching in-flight reservation returns `CommandInProgressException` with `commandId` when available and `retryAfterSeconds`; it does not execute the intent concurrently. Authorization is checked even on a replay so a retained response cannot bypass revoked access.

Authoring, local metadata and collection receipts are retained for at least 24 hours. Run admission/cancellation receipts are retained for the Run's lifetime and at least 90 days after terminal sealing. Commands with unresolved remote effects are not automatically purged. `Command.replayExpiresAt` is the **earliest permitted expiry under the current guarantee**; active or unresolved work extends it before expiry. An exact replay preserves its original receipt, so clients treat that original timestamp conservatively and query `GetCommand` for any later guarantee. After the published guarantee, reconcile the original resource and require a new deliberate intent before submitting another effect. These are future durable-store requirements; the files do not implement a receipt store.

Local replay safety does not supply a provider idempotency token. An adapter uses a native token when the specific operation supports one, deriving a stable provider-compatible token from the durable command identity if needed. A lost response for an operation without native replay support, including the reviewed DevOps approval/message commands, yields `OUTCOME_UNKNOWN`. It must be reconciled through a verified non-creating path. A local success receipt cannot invent a provider confirmation or guarantee exactly-once cloud effects.

## 6. Asynchronous operations and outcome boundaries

An HTTP 200 `Command` response means the documented command was accepted or its original receipt was replayed. Native commands initially return `state=ACCEPTED`. `GetCommand` later exposes dispatch/reconciliation state, retained effects and result references. A failed command is still a successful `GetCommand` read. Provider observations and domain projections are updated only from their own evidence.

| Command | What its acceptance establishes | Facts that need separate evidence |
| --- | --- | --- |
| `StartResilienceAssessment` | Intent to call native StartFailureModeAssessment | Assessment identity, execution outcome, posture and finding-specific remediation |
| `StartInvestigation` | Intent to create a backlog task of type INVESTIGATION | Actual execution start, journal/result content, and incident recovery |
| `DecideApproval` | A scoped decision intent for a validated chat request | Native decision response, subsequent resume, credential redemption and tool outcome |
| `ResumeExecution` | A separate scoped resume intent after a definitive matching decision | Actual resume observation and tool outcome; an opened/completed stream is insufficient |
| `StopExperiment` | Intent to stop the whole native FIS experiment | Native terminal state, post-action cleanup, workload recovery and report readiness |
| `StartRun` | Durable local admission of a Run and its pinned input snapshot | Main work, criteria, cleanup and every external effect |
| `RequestRunCancellation` | Atomic cancellation intent and fencing of further main dispatch | Remote cessation and successful required finalization |

`DecideApproval` initially supports single-use decisions for the exact observed scope. It verifies `expectedRequestSourceRevisionId` and `expectedActionDigest`; reusable grants and scope-pattern editing remain explicit later work. A decision cannot be inferred from text, a pending task status or a guessed tool name. `ResumeExecution` requires a definitively successful matching decision Command and the validated native approval/interrupt/tool-use context. A successful rejection is still a decision; its resume path carries that rejection. The synthetic resume example assumes the matching decision later reached that definitive state; it is not an instruction to resume immediately after an accepted receipt.

An approved request requires `singleUse=true`. A rejection omits that member, and its adapter omits native pattern and TTL fields. An `expectedSourceRevisionId` or approval-request revision must resolve to the exact named native object and appropriate representation, not merely to any visible revision in the workspace. Child/parent ownership, pinned source identity, connection authority and current source preconditions are semantic validations in addition to JSON Schema.

Run admission fixes the exact ScenarioRevision, inputs, allowed connection bindings, enabled steps and required-criterion denominator. Publication supplies trusted operation locks; authors cannot grant themselves capabilities through a draft. The Run stores execution outcome, assessment verdict/finality, finalization state and remote-effect state separately. Runtime skipping cannot shrink the admitted criterion denominator. All required criteria inapplicable at admission is `NOT_EVALUATED`, never automatic pass.

New Scenarios start unarchived and have no default revision. Archiving a Scenario prevents new Run admission while retaining published definitions and history. Exact replay of a previously admitted Run is checked before the current archive state and still returns its original receipt.

Cancellation fences new main dispatch, preserves the first accepted intent and reconciles effects already dispatched. Finalizers run under their own bounded budget. A response-lost start cannot be considered absent because it produced no handle; no creating Start may be reissued after cancellation just to discover its outcome. A sealed Run with unresolved effects remains indeterminate/incomplete. Late evidence and a new `EVALUATION` ProjectionRevision can explain a later understanding without rewriting that historical Run result.

## 7. Read models, lists and evidence completeness

A getter returns the exact retained canonical record with its selected evidence references. Historical IDs remain usable subject to retention and current access. A SourceRevision retains one scoped source identity, representation and immutable payload revision; Observation records the distinct receipt/read context. Repeated polling can add an Observation without creating a new native object. A source event ID is deduplicated only in its authenticated channel/stream scope; identical content alone cannot collapse distinct events.

Lists accept `maxResults` from 1 to 100, default 20, and an opaque `nextToken`. Responses contain `items`, `page` metadata and an optional top-level `nextToken`. An absent token ends the traversal; an empty page by itself does not. `items` contains full canonical records, not silently incomplete summary DTOs. A client can request a smaller page size to manage response size; the first request fixes that page size for the traversal.

`page.traversalId` identifies an ephemeral 15-minute pagination publication. It is not a domain Snapshot ID, cannot be passed to `GetSnapshot`, and grants no evidence-retention guarantee. Retained evidence Snapshots have their own identities, manifests and authorization.

The initial request freezes an ordered set of local record identities and revisions. Its signed/encrypted opaque token binds the workspace, principal, effective authorization scope, operation, parent identities, filters, page size, sort order and local snapshot sequence. It expires 15 minutes after the initial page; reads do not extend that lifetime. A continuation preserves the original query. Tampered or mismatched tokens are rejected; an expired token returns `PaginationTokenExpiredException`, requiring an explicit new traversal. Revocation invalidates access even if the snapshot itself remains retained.

| List family | Fixed order, with the ID as final tie-breaker |
| --- | --- |
| Scenario revisions | `revisionNumber` ascending |
| Step attempts | `attemptNo` ascending within the same StepRun |
| Observations | `observedAt` ascending |
| Projection revisions | `generatedAt` descending |
| Snapshots | `capturedAt` descending |
| Commands | `acceptedAt` descending |
| Runs | `admittedAt` descending |
| Other record lists | Canonical entity ID ascending |

This snapshot is local. It does not claim an atomic AWS view or complete provider visibility. `Collection` and `ReadAttempt` preserve empty/failed reads, request scope, traversal, detail hydration and independent source coverage. A newer incomplete attempt must qualify the current view while an older complete observation remains inspectable. A successful list or a token-free page is insufficient to prove the absence of resources, findings, notifications or errors.

The future collector's internal dispatch transaction creates a `STARTED` ReadAttempt and retains its normalized request SourceRevision before the source call. `RecordReadAttempt` settles that same ID once, with exact request and optional response revision references; it cannot change the reserved query, start time or authorization identity. `IngestObservation` can retain response/object evidence while the attempt is still active, avoiding a dependency on a not-yet-settled attempt. Settlement seals terminal facts. Empty responses still have request/response evidence; a lost response has an explicit unavailable response reference and error. The initial API does not pretend that post-call logging implemented durable pre-dispatch recovery.

Coverage uses independent pagination, detail, resolution, identity and claim fields, a scoped window and supporting attempts. The trusted collector/projector supplies its rationale through registered domain rules. A closed wall-clock interval is not automatically a source watermark. Negative claims need sufficient closed-scope evidence; a trustworthy positive witness can establish only the monotone claim defined by its evaluator. The FIS action count, selected target count, completed-step fraction and workload verdict remain different quantities.

## 8. Time, presence and historical meaning

Wire timestamps are epoch seconds at millisecond precision. Validators parse numeric values with decimal arithmetic, reject unsupported precision before any ordering/storage conversion, and compare/store the same accepted value. They reject NaN/infinity and string substitutes. Native higher-precision timestamps remain in retained raw evidence with explicit normalization information; the console does not silently truncate a value and then reorder evidence using its original precision.

Provider event time, provider update time, source measurement time, transport time, observed time, projection generation time and snapshot capture time have separate meanings. Missing provider dates stay unknown. Recomputing a projection or copying a snapshot cannot make old source evidence fresh. Tied or older observations remain historical unless a named source-selection rule supplies an independent reliable ordering; receipt arrival order is not that rule.

Presence is explicit: unavailable, not requested, omitted, null, known empty, known zero and unknown future values do not collapse. Request schemas keep writable enums strict; the source adapter preserves unfamiliar provider values and known-field presence in evidence. Closed JSON schemas describe this revision's producer contract; consuming clients preserve raw future provider vocabulary and tolerate compatible optional output additions. They must not default an unknown result to a successful or empty state.

`SourceRevision.payloadStorage` disambiguates content storage. `INLINE` can contain a legitimate JSON `null`. `ARTIFACT` has `payload:null` and a non-null versioned ArtifactRef; the referenced content's availability/access is checked independently. Artifact descriptors are validated against an authorized managed store, version and digest. Null payload alone never means an unavailable source or a successful empty result.

An immutable snapshot has a closed manifest of source revisions, observations, projection revisions and read attempts, including failed and empty attempts. It pins graph endpoints, policy contexts and historical evaluator inputs. Resilience posture uses the effective-target evidence associated with its own captured context; current policy edits cannot silently replace that bundle. Captured policy content is evidence of what the collector observed, not proof of the exact revision AWS evaluated.

## 9. Errors and retry decisions

Errors use an operation-independent JSON envelope:

```json
{
  "__type": "VersionConflictException",
  "code": "EXPECTED_VERSION_MISMATCH",
  "message": "The service configuration changed; read it before issuing a new intent.",
  "requestId": "req-stale-demo",
  "retryable": false
}
```

The response also includes `x-amzn-ErrorType: VersionConflictException` and its fresh request ID. The `code`, structured field paths and typed exception are stable parsing contracts; human message text is not. An optional `commandId` identifies an already reserved intent, and `retryAfterSeconds` governs a bounded retry delay.

| HTTP | Exception family | Expected handling |
| --- | --- | --- |
| 400 | ValidationException | Correct malformed/unknown fields, scalar precision, DAGs, tagged unions, or invalid cursor scope. No new effect was admitted. |
| 401 / 403 | UnauthenticatedException / AccessDeniedException | Establish current identity/scope; do not treat access failure as a transient empty result. |
| 404 | ResourceNotFoundException | Resolve the correct parent-scoped identity; invisible data is not disclosed. |
| 409 | VersionConflictException / IdempotencyConflictException / InvalidStateException | Read and reconcile; change intent only deliberately. |
| 409 | CommandInProgressException | Reconcile the named receipt and retry the identical token/payload after the supplied delay. |
| 410 | PaginationTokenExpiredException / EvidenceUnavailableException | Start a fresh traversal or surface unavailable evidence; do not infer absence or success. |
| 413 / 415 | RequestTooLargeException / UnsupportedMediaTypeException | Correct request size or transport. |
| 429 / 503 | ThrottlingException / ServiceUnavailableException | Retry with bounded backoff and jitter using the same intent token; respect retryAfterSeconds. |
| 500 | InternalServerException | Reconcile the durable receipt; a missing HTTP response does not establish that a side effect was absent. |

A retryable **console request** error is not permission to reissue an uncertain provider effect. The Command record and adapter-specific reconciliation decide that. The error schema does not expose stack traces, credentials or untrusted executable content.

## 10. Evolution and delivery gates

The namespace identifies this API version. Compatible changes include optional output members and new explicitly discoverable operations/profiles. Changes to identity scope, parent relationships, units, missing-value meaning, required input fields, state/assessment meaning, pagination, idempotency or authorization guarantees require a new version or a documented migration. A new source profile is an adapter extension; it does not automatically create a new top-level entity or a universal JSON update API.

The current deliverable establishes structural shapes and cross-record acceptance rules. Later delivery must prove the following before claiming the corresponding behavior:

| Delivery gate | Required implementation evidence |
| --- | --- |
| P2 read and ingest | Registered lossless adapters, authenticated source context, durable empty/failed read records, immutable source/observation storage, bounded local snapshots and evidence-authorized reads |
| P3 durable commands | Atomic token reservation and local versions, durable receipts/audit, per-provider DTO mapping, scope enforcement, unknown-outcome reconciliation and native readback |
| P4 workflow runtime | Trusted immutable operation registry, expression/type conformance, admission, attempt recovery, leases/fencing, cancellation races, required-criterion evaluation and bounded finalization |

The broad native management families remain in the source mapping and adapter profile registry; only the documented narrow command subset is defined here. The existing service prototypes and RPC mock remain intact. Their prior test results are source evidence, not validation of a newly implemented consolidated service.

## References

- [Canonical entity model](../MODEL.md), [migration mapping](../MAPPING.md), [adapter profiles](../model/adapter-profiles.json).
- [Resilience Workspace protocol precedent](../../aws/resilience-hub/analysis/api/protocol.md) and [quality review](../../aws/resilience-hub/analysis/quality-review.md).
- [Assessment workflow model](../../aws/fis/analysis/workflow/model.md), [prior HTTP binding](../../aws/fis/analysis/workflow/api.md) and [adapter semantics](../../aws/fis/analysis/workflow/adapters.md). This consolidated RPC binding supersedes that proposal's transport conventions for the new application, while preserving its lifecycle rules.
- [DevOps investigation UI/approval contract](../../aws/devops-agent/analysis/annexes/Investigation_UI_Contract.md) and [native API inventory](../../aws/devops-agent/analysis/annexes/Investigation_API_Catalog.md).
- [Smithy AWS JSON 1.1 protocol](https://smithy.io/2.0/aws/protocols/aws-json-1_1-protocol.html) and [AWS Builders' Library: safe idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/).
