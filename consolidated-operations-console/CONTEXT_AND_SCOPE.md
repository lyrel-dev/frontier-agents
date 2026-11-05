# Context and scope

## Application context

**Consolidated Operations Console** brings operational evidence and work for the same systems, services, resources and incidents into one workspace. Its modules cover AWS Health, resilience assessments, DevOps investigations and fault-injection/assessment workflows. A future common shell supplies navigation, search, source inspection, historical comparison and operator work tracking.

The first step defines a **modular consolidated data model and application API contracts**. It establishes identity, ownership, lifecycle, versioning and references before selecting collectors, storage, orchestration or UI implementation.

The source baseline remains `main` at **`d926a81c584b6b69f41bfb9641532c4f8f2d7cb3`**. [INVENTORY.md](INVENTORY.md) lists all **226 active files** recursively under `aws/<service-name>/analysis/**`, with hashes, sizes and last commits in [inventory.json](inventory.json). Retired paths are listed separately. The review of the first consolidated package starts from [`db142c8`](https://github.com/lyrel-dev/frontier-agents/commit/db142c84bcfd691d5c71071681731cac81a52c7b); that newer commit does not silently expand the frozen AWS source inventory.

## Governing correction

The user's current instruction establishes three requirements: **every entity is versioned; versions do not become separate domain entities; all diagrams use Draw.io with reviewed layouts**. Contract revision 2 applies these requirements to the schema, references, operations, examples, mappings and diagrams together.

The earlier package gave seven entities a local `version`, used `projectionVersion` elsewhere, left many changing records unversioned, and introduced separate SourceRevision, ProjectionRevision and ScenarioRevision classes. Those choices were made in the consolidation and are corrected here. They are not attributed to an earlier user preference. Personal Context was disabled, so unobserved earlier conversations are not evidence. [DESIGN_PRINCIPLES.md](DESIGN_PRINCIPLES.md) distinguishes this explicit instruction from guidance recovered in repository documents.

## Existing work and its contribution

| Source package | Existing work | Contribution retained in the new model |
| --- | --- | --- |
| [DevOps Agent](../aws/devops-agent/analysis/README.md) | Investigation analysis, native API catalogue, ten diagrams, prototype and reviews | Scoped Task/Execution/Journal identities, observed membership, arbitrary journal content, phase-specific result selection, history and independent approval/resume outcomes |
| [FIS](../aws/fis/analysis/README.md) | Native experiment/action analysis, five diagrams, report, prototype and quality review | Experiment/action control boundary, captured configuration, selected-resource evidence and independent report/safety/acceptance meanings |
| [General workflow under FIS](../aws/fis/analysis/workflow/README.md) | Workflow proposal, schemas, three diagrams, adapter/API contracts and semantic cases | Published definition locks, admission inputs, attempt identity, criterion denominator, cancellation and uncertain-effect reconciliation |
| [Health](../aws/health/analysis/README.md) | Event/impact/lifecycle analysis, four diagrams, report and prototype | Public/account/organization context, communication and delivery distinction, catalogue applicability and local operator work |
| [Resilience Hub](../aws/resilience-hub/analysis/README.md) | Model, five diagrams, operator prototype, 44-operation RPC mock and reviews | Workload structure, policy context, service-scoped findings, recommendation content, topology and qualified status rollups |

There are four service directories and six practical packages: FIS includes a generalized workflow package and Resilience includes a separate RPC facade. Their maturity ranges from analysis to executable demonstrations; they do not establish a shared production backend.

## First-step deliverables

| Included | Acceptance boundary |
| --- | --- |
| Source inventory and crosswalk | Preserve every source path and named source concept's disposition, including older revision terminology as aliases. |
| Uniform entity model | All 36 entities require stable identity, `version`, `createdAt` and `updatedAt`. Write authority is explicit. Owned values inherit their owner's version. |
| Historical reference contract | Exact references carry entity kind, ID and version. Current navigation is separately identified. A historical read never substitutes the latest version. |
| Machine-readable schema | [model/schema.json](model/schema.json) defines normalized entities and typed values; retained native payloads remain inspectable. |
| Draw.io class diagrams | An editable multi-page [atlas](diagrams/model.drawio), complete entity coverage, focused relationship views and rendered exports. |
| AWS RPC style operations | Typed requests/responses, version selection and preconditions, errors, pagination, replay and explicit command boundaries. |
| Connected examples and checks | Verify schema consistency and selected cross-record/history invariants using synthetic data. |
| Consolidation path | Stage collection, persistence, commands, execution and UI with concrete acceptance gates. |

## Scope boundaries

Implementation of storage, authentication/authorization enforcement, collectors, durable replay, provider adapters, scheduling, expression evaluation, effect reconciliation, retention/export enforcement and UI follows model review. Those capabilities have acceptance gates in [CONSOLIDATION_PLAN.md](CONSOLIDATION_PLAN.md).

The model references existing credential, identity and organization owners. It does not prescribe a new IAM, credential vault, notification platform or general project-management product. Deployment topology and database selection depend on the later operating requirements.

Native administrative breadth remains in named adapter profiles until a concrete workflow needs an operation. DevOps Goals, Triggers, integration registrations, private connections and operator-app configuration retain their provider identity and payloads. Their presence in an SDK does not create a speculative CRUD root in the console.

## User questions the model must answer

1. Which service, resource and native owning scope does this item concern, and what establishes that relationship?
2. Which version am I reading, who may publish its successor, and which exact versions supported a past decision?
3. What did the source report, through which access path, and at which source and observation times?
4. What was collected, what is missing, and what evidence supports the displayed conclusion?
5. Which work or effect was requested, accepted, observed and completed?
6. What did an earlier assessment mean at its cutoff when the current source or definition has changed?

These questions keep identity, history and authority in the common contract while preserving domain-specific meaning.

## Decisions

| Decision | Rationale and limit |
| --- | --- |
| One versioning rule for every entity | Versioning records the complete representation. It does not grant user edit access or alter provider semantics. |
| Source, Observation and Projection are distinct concepts | They model a retained source document, an occurrence of observing it, and an interpreted result. Each has stable identity and its own versions; none is a version-only class. |
| Scenario owns authoring and publication | A published Scenario version contains locked definitions. Run pins that version. Drafting and archiving create later versions of the same Scenario. |
| Workspace is the application boundary | Provider AgentSpace, owning accounts and access paths keep their separate meanings. |
| System, UserJourney and Service form a local catalogue | Native identities are evidence-backed bindings. Local edits have no implied provider side effect. |
| WorkItem owns operator work | Recommendation enrichment supplies estimates/notes; assignment and work lifecycle belong to WorkItem. |
| Snapshot pins entity versions | Its manifest closes over retained evidence, including failed/empty ReadAttempts, without copying independently authoritative entities. |
| Composition supports extension | New typed modules/profiles reuse common versions, references, evidence and command contracts. There is no universal mutable extension bag. |
| RPC contract revision 2 is explicit | Identity and reference changes are breaking changes. The namespace is `ConsolidatedOperationsConsole_20261105V2`. |

The [model](MODEL.md), [protocol](api/PROTOCOL.md), [mapping](MAPPING.md) and [review](REVIEW.md) specify the consequences of these choices.
