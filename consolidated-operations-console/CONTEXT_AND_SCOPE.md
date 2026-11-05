# Context and scope

## The application being defined

**Consolidated Operations Console** is an application that brings operational evidence and work for the same systems, services, resources and incidents into one workspace. Its modules cover AWS Health, resilience assessments, DevOps investigations and fault-injection/assessment workflows. A common application shell will eventually provide navigation, search, evidence inspection, historical review and operator work tracking.

This first step defines the **modular consolidated data model and its application API contracts**. It establishes the vocabulary, identity, ownership, references and invariants that future collectors, storage, orchestration and UI modules will share. It delivers reviewable schemas and examples, not a running console or a service connected to AWS.

The source boundary is `main` at **`d926a81c584b6b69f41bfb9641532c4f8f2d7cb3`**, inspected on **5 November 2026**. [INVENTORY.md](INVENTORY.md) lists all **226 active files** under the exact recursive pattern `aws/<service-name>/analysis/**`; [inventory.json](inventory.json) records their Git blob hashes, sizes and last commits. Earlier retired paths are listed separately. No source-package files are changed by this proposal.

## Existing work and what it contributes

| Source package | Existing work | Contribution to the new model |
| --- | --- | --- |
| [DevOps Agent](../aws/devops-agent/analysis/README.md) | Investigation analysis, native API catalog, ten diagrams, prototype, source audits and corrected evidence/history contracts | Scoped Task/Execution/Journal identities, observed membership, arbitrary journal content, phase-specific result selection, historical snapshots and independent approval/resume outcomes |
| [FIS](../aws/fis/analysis/README.md) | Native experiment/action analysis, five provider diagrams, report, prototype and quality review | Experiment/action control boundary, captured configuration, selected resource evidence, safety/report distinctions and frozen acceptance meaning |
| [General workflow under FIS](../aws/fis/analysis/workflow/README.md) | Six-entity workflow proposal, three diagrams, schemas, adapter catalog, API contract, examples and reference semantic checks | Scenario publication, immutable locks, admission snapshots, step attempts, criterion denominators, cancellation and reconciliation of uncertain effects |
| [Health](../aws/health/analysis/README.md) | Event/impact/lifecycle analysis, four diagrams, report and prototype | Public/account/organization context, communication-page/delivery separation, lifecycle catalog applicability and local work tracking |
| [Resilience Hub](../aws/resilience-hub/analysis/README.md) | v2 model, five diagrams, operator prototype, 44-operation RPC mock and reviewed contracts | Business structure, effective policy context, service-scoped findings, recommendation enrichment, discovery/topology and qualified status rollups |

There are four AWS service directories and six practical work packages: FIS has a separate generalized workflow, and Resilience has a separate RPC facade. These distinctions matter when planning reuse. The older source packages have different maturity levels; their presence is not evidence of a shared production backend.

## First-step deliverables

| Included now | Acceptance boundary |
| --- | --- |
| Complete source inventory and recovery of recorded design principles | Every source path and named model concept has a traceable disposition. Prior-chat retrieval was disabled; the recovered principles cite repository evidence. |
| Shared kernel and typed module entities | 37 entity definitions, their owned values, scoped identities, cardinalities, mutability and source ownership are explicit. |
| Machine-readable logical model | [model/schema.json](model/schema.json) is the canonical JSON Schema document; generated references and diagrams derive from it. It describes the normalized application contract, with raw native payloads retained separately. |
| Class diagrams for every entity | One complete class diagram plus focused module views, editable Mermaid and rendered SVG. |
| AWS RPC style application operations | Operation-specific inputs/outputs, errors, pagination, idempotency, concurrency and command boundaries; all operations are proposed contracts. |
| Source-to-target mapping and examples | Provider DTOs, local entities, owned values and derived projections are identified explicitly. No generic JSON fallback is used to claim full native semantic normalization. |
| Offline structural and semantic verification | Schema/example checks, cross-artifact coverage, source-inventory integrity and selected adversarial invariant cases. Runtime claims remain separate. |
| A staged consolidation path | Migration order, compatibility changes, preservation gates and the first implementation slice are stated. |

## Deferred implementation

The next stages will select and implement storage, authentication/authorization enforcement, collectors, durable command/replay persistence, the provider adapters, a workflow scheduler, expression evaluation, effect reconciliation, retention/export enforcement and the user interface. Those components are prerequisites for production guarantees; this package defines their contracts and acceptance gates.

This phase does not design a second IAM, organization directory, credential vault, notification service or general project-management system. It stores references to those owners. Deployment, regional architecture, database product and hosting choices remain open until workload and access requirements are established.

Native administrative breadth is deferred deliberately. For example, the DevOps API's Goal, Trigger, registered integration, private connection and operator-app configuration families remain explicitly typed retained adapter profiles. Their source identities and payloads are retained; they do not become speculative CRUD entities in the first shared model. The [crosswalk](MAPPING.md) and [adapter registry](model/adapter-profiles.json) enumerate those decisions.

## Users and key questions

The intended users are operators investigating incidents, service owners reviewing resilience and lifecycle exposure, and engineers authoring/reviewing assessment scenarios. The shared model should let them answer:

1. Which logical service, account/Region and resource does this item concern, and how was that relationship established?
2. What did the provider say, through which access path, and at what source and observation times?
3. What was actually collected, what is missing, and which exact evidence supports the displayed conclusion?
4. Which work or external effect was requested, accepted, observed and completed?
5. What did an earlier view or assessment mean at its recorded cutoff, even if current collection fails?

These questions explain why a few common evidence and command entities are necessary. Service-specific states remain in their modules because the questions they answer differ.

## Decisions and assumptions

| Decision | Rationale and limit |
| --- | --- |
| Workspace is the application authorization boundary | Every application record is workspace-scoped. AWS AgentSpace and provider owner scopes are separate concepts. The initial schema does not prescribe how identity federation realizes that boundary. |
| System, UserJourney and Service form a local workload catalog | They provide a common business context across modules. Existing Resilience native identities become explicit bindings; a local metadata edit has no implied AWS side effect. Native configuration changes use explicit provider commands. |
| A shared SourceIdentity value replaces a separate universal SourceObject entity | The exact native tuple plus immutable SourceRevision preserves identity/history without another mutable CRUD root. |
| SourceRevision, Observation and ProjectionRevision remain separate | They preserve payload changes, repeated collection and changing interpretation independently. |
| Composition is the extension mechanism | Modules own entity types, source profiles, projection rules and operations. There is no universal mutable entity with an untyped extensions map. Raw JSON is restricted to retained native documents and explicitly versioned schema/content boundaries. |
| Independent reevaluation can create an EVALUATION projection | This extends the earlier workflow's new-read-only-Run convention. The projection pins its inputs and evaluator; it never rewrites the original sealed run. A Run remains available when reevaluation needs orchestration. |
| One application RPC namespace is adopted | This follows the current request and the existing Resilience facade's conventions. Native AWS transports remain behind adapters. |

The [model](MODEL.md), [API protocol](api/PROTOCOL.md) and [plan](CONSOLIDATION_PLAN.md) make these decisions concrete. A future requirement should change the smallest owning module and preserve the shared evidence and compatibility rules.
