# Consolidation path

## Target and sequencing

Build one modular application over a common identity/evidence/command contract. Preserve the existing analysis packages as source references and independent prototypes while moving shared concepts into this new contract. Establish correctness in a small read-oriented slice before adding provider mutation and workflow execution.

The current delivery completes **P1: model and operation contract**. Later phases below are implementation plans, with explicit acceptance gates. No phase assumes that an existing browser mock or in-memory RPC server supplies production persistence or authorization.

| Phase | Work and deliverable | Exit gate |
| --- | --- | --- |
| **P1 — model and contracts (this delivery)** | Pin `main`; inventory every source file; map all source concepts; define shared and module entities; publish class diagrams, JSON schemas, typed RPC operations and examples. | All 226 source files accounted for; every named source concept has a disposition; all 37 entities occur in schema, diagram and API coverage; examples and selected semantic cases validate. |
| **P2 — retained reads and collection** | Implement Workspace authorization, source-identity mapping, Connection references, append-only SourceRevision/Observation storage, Collection/ReadAttempt, projection publication and Snapshot retrieval. Add one read adapter per domain. | Same object through two connections deduplicates correctly; repeated polls preserve observation history; partial/failed/empty reads stay distinguishable; historical views work during current-source failure; scoped pagination and export access are enforced. |
| **P3 — durable local and provider commands** | Implement local configuration/WorkItem edits, idempotency reservation, durable command/outbox, independent overlay versions, provider dispatch and non-creating reconciliation. | Replay after a lost response/restart returns the original receipt; changed payload conflicts; out-of-band provider changes remain visible; unknown effects are retained; no local version is advertised as an AWS compare-and-swap. |
| **P4 — workflow execution** | Implement scenario publication/locks, trusted binding/admission, bounded DAG execution, step attempts, immutable criteria/evidence, cancellation fencing, finalization and protective holds. | Crash/retry/race tests establish persisted dispatch identity, fixed criterion denominator, no creating reconciliation after cancel, bounded cleanup and terminal INDETERMINATE when effects remain unknown. |
| **P5 — modular console shell** | Compose module navigation, service-centric overview, independent state dimensions, source inspection, historical compare and typed local/provider actions. | UI and API use the same selectors; every shown conclusion opens its exact retained evidence; unauthorized/missing/stale states stay visible; labels never imply stronger coverage or control than the contract. |
| **P6 — expansion driven by concrete use** | Add additional native administrative operations, more capture profiles, cross-provider inventory, schedules or richer authoring only when a product use case needs them. | New concepts have a defined lifecycle/owner; contract compatibility and source coverage are explicit; the shared foundation remains independent of provider-specific parsers. |

## Module dependencies

The foundation owns Workspace, Connection, source identity, collection, evidence, projections, snapshots, local work and command records. Provider modules register typed payload profiles and select their own source facts. They cannot edit another module's evidence or reuse its state enum solely because a label looks similar.

The workload catalog supplies System, UserJourney and Service identity for cross-module navigation. Resource inventory supplies explicit resource references. Health can map an impact to inventory; it does not own the resource. Resilience binds native services into the workload catalog; local catalog membership does not alter native policy assignment. Investigation can link service/resource/incident context through evidence. Workflow references published scenarios and typed adapter effects; it does not own the external Experiment or ResilienceAssessment lifecycle.

Cross-module views use typed references and immutable evidence publications. Modules can be disabled for a Workspace without deleting retained history. A disabled module rejects new work admission. Authorized cancellation, cleanup, reconciliation and historical reads remain available; disabling a module cannot abandon an outstanding effect. Retention policy still applies. This is configuration on Workspace, not a new plugin-management entity.

## Migration procedure

### 1. Freeze and classify the inputs

Use [inventory.json](inventory.json) as the source manifest and its commit as the provenance boundary. Do not import artifacts from an unmerged branch, a stale local checkout or a generated screenshot as if they were additional approved models. Existing reports, contracts and source registers explain semantics; fixtures provide synthetic examples only.

Classify each source concept using [MAPPING.md](MAPPING.md): canonical entity, owned value, typed source DTO, derived profile, explicit external reference or deferred command capability. Keep exact old names in the crosswalk. This makes removal, retention and intentional consolidation reviewable.

### 2. Establish scope and identity before transforming payloads

Create application Workspace boundaries and canonical ID mappings. Preserve the native owner tuple and parent scope on SourceIdentity, independently of Connection/authentication context. Map existing provider IDs to stable application aliases; do not use display names as joins.

Import local System/Journey/Service metadata with source provenance and one explicit membership authority. A native Resilience service ARN becomes a binding to the canonical Service. An AWS DevOps RegisteredService remains integration configuration; AgentSpace remains a provider scope. Unresolved summary IDs and unmatched Health entities stay unresolved until a documented rule and evidence support a match.

For each migration batch, retain an immutable manifest of source bytes/revisions, mappings, transformer version, diagnostics and output identities. An importer can replay the same manifest without creating duplicate domain entities. A revised transformation creates new derived publications while retaining prior provenance.

### 3. Import retained evidence without inventing history

SourceRevision stores distinct payloads. Existing repeated capture facts become Observation records only if the source actually supplies them. Where earlier prototypes retained only a current fixture or flattened local state, mark original collection time/coverage unavailable and preserve the raw source. Do not manufacture a successful historical read or a complete page chain to satisfy a new field.

New ReadAttempt records use the full new contract, including request/response revisions. Older collection histories lacking those facts can be retained as explicitly versioned legacy DTOs; the normalized current view reports the gap. Event/stream receipts use their own channel and do not require invented native reads.

Late summaries must not erase prior detailed finding evidence. Repeated notifications must not become new Health events. Duplicate journal observations must not inflate record counts. Preserve provider clocks, nullable fields, raw enums and separate local edit clocks.

### 4. Rebuild projections in parallel for comparison

Implement the reviewed rules as versioned projections over the retained data. Compare the existing prototype's result with the new projection, using the exact same source bundle. Differences need an explained source mapping, approved semantic correction or explicitly retained legacy limitation.

Compare meaningful dimensions: scope/identity counts; selected revision/observation; phase-specific result; criterion denominator and verdict; policy context; current versus retained assessment coverage; missing/detail states; notification recipients versus affected accounts; local versus native disposition. Pixel matching and a single overall status do not establish semantic parity.

Do not relabel previously overstated outputs as trustworthy historical results. Preserve their original bytes with a legacy rule/profile label, and publish corrected results with a new identity.

### 5. Add the API adapter layer

Keep the consolidated namespace distinct from existing prototypes. New operation-specific DTOs use [api/PROTOCOL.md](api/PROTOCOL.md). Route reads to retained publications; route local writes to their owning aggregate; route native writes through a durable Command and the real native SDK operation.

The main compatibility changes are deliberate:

| Earlier surface | Consolidated disposition |
| --- | --- |
| Resilience `Create/UpdateSystem`, `Create/UpdateUserJourney`, `Create/UpdateService` | New operations author the local workload catalog. Native provider provisioning/configuration is an explicit separate command boundary; do not silently switch old callers to different semantics. |
| Resilience `Start/Get/ListFailureModeAssessment` | `StartResilienceAssessment`, `GetResilienceAssessment`, `ListResilienceAssessments`; local identity maps to native service/assessment scope. |
| Resilience `Get/List/UpdateFailureModeFinding` | `GetFinding`, `ListFindings` and explicit `UpdateFindingDisposition`, with service scope and source precondition. |
| Resilience `UpdateDependency` versus `UpdateDependencyGovernance` | Preserve distinct provider classification and local governance commands. |
| Resilience `UpdateRecommendationEnrichment` | Preserve local enrichment and estimate, with its own version. |
| Resilience `CaptureTopologySnapshot` | `CaptureSnapshot` with TOPOLOGY content and closed retained evidence manifest. Existing snapshot IDs require an explicit alias/import map. |
| Resilience `PutHealthObservation`, `IngestEvent` | Trusted `IngestObservation`, typed source profiles and projection publication; raw events never patch current entity state directly. |
| FIS workflow resource HTTP API | Normalize to operation names under one RPC namespace, epoch-second timestamps and `expectedVersion`/`clientToken` fields. Preserve the stronger lifecycle, replay, frozen-input and proof semantics. |
| DevOps proposed HTTP view routes/local functions | Typed consolidated read operations over Investigation, Execution, JournalRecord, Snapshot and evidence; no claim that these facade names exist natively in AWS. |
| Health local acknowledgement/completion | WorkItem commands; provider Health lifecycle remains observed. |
| Native administrative breadth | Retain typed source DTOs; add explicit command contracts later with provider-specific permissions and clearing/concurrency behavior. |

The complete new surface is [api/OPERATIONS.md](api/OPERATIONS.md). Migration is a versioned client change, not an in-place reinterpretation of the existing Resilience mock namespace or FIS REST API.

### 6. Cut over one capability at a time

Start with source inspection and historical read views; then move local work tracking and catalog metadata. Introduce remote writes only after command/reconciliation gates pass. Move assessment execution last, since uncertain side effects and cancellation require stronger guarantees than a read model.

Retain old source packages for traceability. Replacing a prototype later should update its entry point and clearly state the replacement, without erasing its review history. This delivery adds only `consolidated-operations-console/`.

## Recommended first implementation slice

Use one synthetic checkout service as the initial read-only slice, matching [model/examples.json](model/examples.json). It links a Health event/account impact, a DevOps investigation, a Resilience assessment/finding, an FIS experiment and a completed workflow. Technical execution succeeds while an acceptance criterion fails; an operator can complete local review while provider impact and finding evidence remain open. This exercises the state distinctions with a small data set.

Build the foundation plus the typed read mappings for that slice. Demonstrate one repeated read of identical payload, one changed revision, one empty or failed read, one incomplete detail result, one conflicting or unavailable result selection and one historical snapshot that still opens when refresh fails. Add one expired observation and show current coverage falling while retained history remains available.

The first mutation slice should be `Create/UpdateWorkItem` and one local catalog edit, because their ownership is entirely local. The first provider command should be chosen for a documented native idempotency/reconciliation path and bounded effect scope. The live command choice requires the actual environment's capability and permission evidence; no universal exactly-once promise is part of the model.

## Decisions required before implementation

| Decision | Why it can wait until after model review |
| --- | --- |
| Deployment topology and database | The normalized ownership/identity boundaries are independent of one vendor or table layout; latency, tenancy, scale and recovery objectives determine the implementation. |
| Authentication and authorization integration | Workspace and trusted principal/Connection scopes are defined. The concrete identity provider and policy engine must match the target environment. |
| Retention and replay storage | Evidence, snapshots, token reservation and tombstone requirements are explicit. Organization policy determines durable storage and content expiry. |
| Native adapter support matrix | The registry retains every reviewed family. Production writes require exact current SDK models, permitted roles and observed service behavior. |
| Expression evaluator and operation artifacts | Published digests and trusted capability checks are specified. Runtime selection and conformance tests come with workflow execution. |
| Performance and paging limits | Contract bounds prevent unbounded calls. Large artifact payloads need content retrieval and authorization; realistic workload measurements determine tighter limits. |

The phase gates make these decisions reviewable without prematurely expanding the domain model.
