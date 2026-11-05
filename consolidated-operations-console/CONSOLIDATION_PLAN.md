# Consolidation path

## Target and sequencing

Build a modular application over **one identity, version and reference contract**. The current revision corrects the first model before collectors, commands or UI depend on its inconsistent version entities. Source analyses and prototypes remain traceable inputs.

| Phase | Work and deliverable | Exit gate |
| --- | --- | --- |
| **P1 — model and contracts** | Frozen source inventory; 36 uniformly versioned entities; source crosswalk; typed RPC contracts; editable Draw.io atlas and rendered pages. | Every entity requires common metadata; historical references resolve exact versions; no version-only classes; source mappings, examples, semantic cases and diagram layout checks pass. |
| **P2 — version storage, reads and collection** | Scoped identity mapping, atomic entity-version publication, current-head selection, historical retrieval, Sources/Observations, Collection/ReadAttempt and closed captures. Add one read adapter per domain. | Repeated reads reuse unchanged Source versions; changed and reverted content advances history; failed/partial/empty reads survive; exact historical retrieval works during current-source failure. |
| **P3 — local and provider commands** | Narrow local edits, expected-version checks, replay reservation, durable Command/outbox, provider dispatch and reconciliation. | Concurrent publishers cannot overwrite a version; replay survives response loss/restart; out-of-band provider state remains observable; uncertain effects are retained. |
| **P4 — workflow execution** | Scenario publication, pinned admission, typed operation locks, DAG execution, versioned run/step/attempt state, cancellation and finalization. | A historical Run resolves its own child versions; criteria cannot shrink after admission; dispatch identity survives crashes; cancellation cannot trigger creating reconciliation. |
| **P5 — modular console shell** | Shared navigation, current/history selection, source inspection, service overview, comparison and explicit actions. | Every conclusion opens its exact evidence; version selection is visible; layouts and actions reflect real authority and scope. |
| **P6 — demand-led extension** | Additional native administration, capture profiles, providers, schedules or authoring capabilities. | Each new entity has substantive identity/lifecycle; owned values remain owned; compatibility and source coverage are explicit. |

The model specifies required behavior. Source mocks and contract fixtures do not establish production persistence, authorization or cloud execution.

## Module dependencies

Foundation owns Workspace, Connection, Resource, collection, Source, Observation, Projection, Snapshot, WorkItem and Command. The common version/reference rule applies equally to every module. Provider-specific parsers and writable fields stay in their owning module.

The workload catalogue supplies System, UserJourney and Service identity. Health may match an impact to a Resource; it does not own the Resource. Resilience binds native service identity to the catalogue without turning a catalogue edit into a native policy change. Investigation links operational context through evidence. Workflow pins a Scenario version and exact admitted references while native Experiment and ResilienceAssessment retain independent lifecycles.

Disabling a module blocks new work admission but cannot abandon an outstanding effect. Authorized cancellation, cleanup, reconciliation and historical reads remain available under retention and current access policy. Module configuration belongs to Workspace and is versioned with it.

## Migration from the first consolidation

The first consolidated contract is retained in Git at [`db142c8`](https://github.com/lyrel-dev/frontier-agents/commit/db142c84bcfd691d5c71071681731cac81a52c7b). Revision 2 changes identity/reference/version semantics and uses `ConsolidatedOperationsConsole_20261105V2`; it must not silently reinterpret a revision-1 client payload.

### 1. Keep the source baseline and vocabulary

The source manifest remains [inventory.json](inventory.json), pinned to `d926a81c584b6b69f41bfb9641532c4f8f2d7cb3`. It accounts for the 226 analysis files independently of changes to the consolidated package. Preserve source names such as ScenarioRevision or AssetVersion as aliases in the [mapping](MAPPING.md), not as current schema entities.

Classify each source concept as an entity, owned value, retained provider DTO, projection profile, external reference or deferred capability. Do not import off-main work or fabricate historical captures to satisfy a new contract.

### 2. Establish logical identity and version ownership

Map each old record to a stable logical identity, then assign versions within that identity. Retain an import manifest containing the old key, new kind/ID/version, source bytes, transformer version and diagnostics. This alias map makes migration replayable and preserves existing links.

| Old representation | New representation | Required migration behavior |
| --- | --- | --- |
| SourceRevision | Source ID plus version | Group by native identity, representation, profile and operation. Content digest is content evidence, not logical identity. Preserve ordering evidence; do not invent unknown intervening versions. |
| ProjectionRevision | Projection ID plus version | Group under the declared interpretation key/profile/subject identity scope. Preserve exact input and rule versions. |
| Scenario and ScenarioRevision | Scenario versions | Retain draft and published definitions as states of one Scenario. Published content keeps exact locks and digest. Map each old revision ID to its Scenario reference. |
| Local `version`, `projectionVersion`, overlay counters | Universal entity version | Serialize the complete owning representation. Preserve obsolete counters only as import provenance where needed; they are not the new concurrency authority. |
| Asset with embedded versions | Asset versions | Each representation captures one exact nativeVersion/source/file set. Keep native version and application version distinct. |
| ID-only evidence references | Exact EntityRef/EvidenceRef | Resolve the intended historical representation during migration. An ambiguous old reference remains unresolved; do not attach the current head. |
| Snapshot embedded ReadAttempts | Snapshot.members | Import canonical ReadAttempt versions and pin them in the capture manifest. Do not retain competing authoritative copies. |
| Recommendation workflow overlay | WorkItem plus owned enrichment | Move assignment/work state to WorkItem; estimates/notes remain on Recommendation under its entity version. |

`createdAt` records application identity creation and `updatedAt` records version publication. A migration timestamp must not masquerade as a missing native creation time or historical observation time. Where source ordering is unavailable, retain that limitation instead of asserting a reconstructed event history.

### 3. Build exact history before current views

Implement immutable representations and atomic current-head publication before source refresh or editing can use them. All references needed by evidence, decisions and capture must include versions. Parent IDs used for structural ownership do not implicitly load current parent content into a historical response.

ReadAttempt retains its fixed collection/query identity and versions through dispatch/settlement. Connection references pin the access configuration used for collection or admission. A Connection's historical version does not preserve an authorization grant after current access has been revoked.

A repeated genuine Observation can point at the same Source version. Changed content creates the next Source version. A→B→A advances version history even if the final bytes match an earlier blob. Source identity and event/receipt identity prevent distinct native objects or deliveries from collapsing solely because their bytes match.

### 4. Rebuild derived views and captures

Recompute declared Projection profiles from exact retained inputs and versioned rules. Compare results using the same source bundle as the earlier prototype. Differences need an explained correction, mapping or retained source limitation.

Check identity counts, selected versions, phase-specific results, required criteria, policy context, field presence, native versus local disposition and coverage. Pixel similarity or one overall status cannot establish semantic parity.

Snapshot.members closes over the exact versions used by its contents, including failures and empty reads. Correcting a capture publishes a new Snapshot version under that capture's identity; a distinct capture occurrence has its own identity. Previous versions and their meaning stay available under retention.

The initial operation surface supplies capture creation at version 1. A guarded Snapshot correction writer is deferred until a concrete correction workflow requires it; history support does not introduce generic CRUD.

Recommendation identity uses the stable native suggestion key when supplied. Otherwise it is scoped to Finding, exact Source version, group and ordinal. Repeated observations of that source reuse the same captured suggestion; a matching ordinal in changed content cannot establish continuity.

### 5. Migrate operation contracts explicitly

Typed getters take an optional version selector. Omission requests current state; a supplied version requests exactly that representation. History listing and pagination retain the selected entity/version pairs. Return the actual entity version to clients.

| Earlier surface | Revision 2 behavior |
| --- | --- |
| GetSourceRevision / GetProjectionRevision | GetSource / GetProjection with stable ID and optional exact version. |
| GetScenarioRevision / ListScenarioRevisions | GetScenario at an exact version and ListEntityVersions for the logical Scenario. |
| PublishScenarioRevision | PublishScenario creates the next PUBLISHED Scenario version. |
| UpdateScenario with archive/default revision fields | UpdateScenario creates a later DRAFT; ArchiveScenario changes current admission policy by publishing ARCHIVED. Old publication IDs are replaced by exact Scenario references. |
| StartRun using scenarioRevisionId | Pin the selected PUBLISHED Scenario and admitted subject/Connection versions. Current ARCHIVED head blocks new admission; an intervening DRAFT does not rewrite older publications. |
| CompleteCollection using expectedProjectionVersion | Compare the Collection's common expectedVersion. |
| Governance/enrichment edits using nested counters | Compare the owning Dependency or Recommendation version; update only the operation's allowed fields. |
| Native configuration preconditions using source revision IDs | Pin the observed Source version and verify native scope; this remains observed context, not provider atomicity. |
| CaptureSnapshot with revision-ID arrays | Supply/assemble exact entity-version members and validate the retained closure. |

Local catalogue operations continue to edit local metadata. Explicit native commands retain separate effect semantics. A local UpdateService cannot be used as a transparent replacement for native provider provisioning/configuration. The complete operation surface and predecessor dispositions are in [api/OPERATIONS.md](api/OPERATIONS.md).

### 6. Cut over one capability at a time

Move source inspection and historical reads first, then local WorkItem/catalogue operations. Introduce provider writes after durable command/reconciliation gates pass. Introduce workflow execution after versioned run/step/attempt selection, admission, cancellation and effect handling are implemented and tested.

Keep source analyses available as provenance. Updating a prototype's entry point later should name its successor without erasing review history. This revision changes only `consolidated-operations-console/`.

## First implementation slice

Use the synthetic checkout-service example to join Health impact, a DevOps investigation, a Resilience finding/assessment, an FIS Experiment and a workflow Run. Exercise these cases together:

1. A source document is read twice unchanged, changes, then returns to earlier bytes without regressing its entity version.
2. Service configuration changes while an earlier Snapshot and Run continue to resolve the original Service version.
3. Collection and ReadAttempt progress through lifecycle versions, including empty/failed outcomes.
4. Scenario is drafted, published and edited again; a Run pins the older published version, while archive policy is checked on the current head.
5. Run pins its own StepRun versions, and each selected StepAttempt reference is exact. Current child changes cannot alter historical verdicts.
6. Technical execution succeeds while acceptance fails, and operator review completes while native impact/finding evidence remains open.
7. Historical evidence still opens during current-source failure; expired evidence qualifies current coverage without rewriting the past.

The first local mutation slice is WorkItem and one catalogue edit. Choose the first provider command only when actual environment permissions and native replay/reconciliation support are known.

## Implementation decisions left open

| Decision | Required basis |
| --- | --- |
| Database and deployment | Tenant scale, latency, recovery and retention objectives; the logical version contract does not prescribe physical layout. |
| Identity and authorization integration | Trusted Workspace/principal binding, historical evidence closure access and provider permission boundaries. |
| Version/replay retention | Atomic publication, immutable old representations, tombstone handling, evidence closure and guaranteed replay lifetime. |
| Native adapter matrix | Current SDK models, declared profiles, permitted roles and observed operation behavior. |
| Expression/operation runtime | Locked implementation artifacts, typing/capability checks, cancellation and race conformance. |
| Performance and paging | Realistic record sizes, historical query volume and authorization costs while retaining bounded API behavior. |

The phase gates require implementation evidence for each capability before the console claims its behavior.
