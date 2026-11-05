# Consolidated modular data model

## Model rule

**Every entity has stable identity and a version.** A version is a representation of its entity, not a separate domain entity. This rule applies to local configuration, provider-observed objects, collector records, workflow execution, retained evidence, derived results and commands.

The model contains **36 entities in seven modules**. SourceRevision becomes **Source** with stable `sourceId`; ProjectionRevision becomes **Projection** with stable `projectionId`; ScenarioRevision is folded into **Scenario**. Drafting, publication and archival produce versions of the same Scenario. Every entity requires `version`, `createdAt` and `updatedAt`.

[model/schema.json](model/schema.json) is the structural authority. [model/REFERENCE.md](model/REFERENCE.md) supplies all fields and owned values. [MAPPING.md](MAPPING.md) preserves the original source terminology and its disposition. This is a logical contract: it does not require a table per class, an event-sourcing implementation, or a particular database inheritance scheme.

## Draw.io class diagrams

Open the editable **[model.drawio atlas](diagrams/model.drawio)** in Draw.io. Its overview contains all 36 entities; focused pages provide the relationship detail at a practical reading scale. The overview intentionally selects connectors instead of routing every cross-module relationship across one canvas. The detailed pages cover the declared relationships.

| Module | Entities | Diagram |
| --- | --- | --- |
| Foundation (11) | Workspace, Connection, Resource, Collection, ReadAttempt, Source, Observation, Projection, Snapshot, WorkItem, Command | [Identity and commands](diagrams/foundation.svg) · [Evidence and history](diagrams/evidence.svg) |
| Workload (4) | System, UserJourney, Service, Dependency | [Workload](diagrams/workload.svg) |
| Health (6) | HealthEvent, EventContext, EntityImpact, Communication, LifecycleEntry, ComponentDeployment | [Health](diagrams/health.svg) |
| Resilience (4) | ResiliencePolicy, ResilienceAssessment, Finding, Recommendation | [Resilience](diagrams/resilience.svg) |
| Investigation (6) | AgentSpace, Investigation, Execution, JournalRecord, ApprovalRequest, Asset | [Investigation](diagrams/investigation.svg) |
| Workflow (4) | Scenario, Run, StepRun, StepAttempt | [Workflow and FIS](diagrams/workflow.svg) |
| FIS (1) | Experiment | [Workflow and FIS](diagrams/workflow.svg) |

[All-entity overview](diagrams/complete-model.svg) · [Diagram provenance and coverage](diagrams/manifest.json)

Class boxes show selected fields and versioning. Cardinalities are logical, within one Workspace, and conditional rules below still apply. Full fields remain in the generated reference. Common metadata is a contract shared by all entities; it is not a new entity with its own lifecycle.

## 1. Uniform identity and versioning

### Common metadata

| Member | Meaning |
| --- | --- |
| Type-specific ID | Opaque stable identity, such as `serviceId`, `sourceId` or `runId`. It does not change when a new version is published. |
| `workspaceId` | Application scope. Workspace itself is identified by this member. |
| `version` | Positive integer allocated by the owning authority. The first representation is version 1; a successor increments it. |
| `createdAt` | Time the application identity was created. It remains constant across the entity's versions. |
| `updatedAt` | Time this representation was published. It does not replace a provider, measurement, observation or execution timestamp. |

The exact retained representation is identified by **entity kind, Workspace, stable ID and version**. Every published version is immutable. A change publishes a successor; an exact replay returns its original result. A historical read resolves the requested version or reports its absence/unavailability. It never follows the current head as a fallback.

An unchanged ingestion can reuse the current entity version. A repeated genuine receipt still creates an Observation because the occurrence is new. When source content changes from A to B and later returns to A, Source keeps its identity and advances through versions 1, 2 and 3. Content storage may reuse A's bytes, but content equality cannot rewind version history.

An immutable fact can remain at version 1 throughout its lifetime. Requiring version metadata does not require an update operation for that fact. Conversely, a server-owned lifecycle record needs versioning even when clients cannot edit it. A Run, Collection or Command changes under its owning authority and publishes successive representations.

Provider `nativeVersion`, schema/profile versions, operation-lock versions, attempt numbers and reducer versions describe other things. They remain explicitly named domain metadata. None substitutes for the entity's `version`.

### Scope and uniqueness

Child scope remains part of logical uniqueness. A UserJourney belongs to one System. A Finding and Dependency belong to one Service. StepRun is unique within a Run by `stepKey`; StepAttempt is an execution attempt within that StepRun. JournalRecord includes AgentSpace, Execution and native record identity. A stable surrogate does not remove these constraints.

`SourceIdentity` is an owned value containing provider, service, resource type, owning scope, native identity and aliases. Its scope records partition, account, Region and relevant parent keys. Encode the tuple unambiguously; display names and delimiter-joined opaque strings are not keys. A provisional identity stays explicitly provisional until supported matching establishes an alias.

Connection identifies an authorized access path. Its principal and endpoint do not become the native owner. Two connections can observe the same native object; changing a role does not create another object. Workspace and native AgentSpace remain distinct scopes.

## 2. References and history

Two reference values make selection explicit:

| Value | Shape | Use |
| --- | --- | --- |
| `EntityIdentity` | `{kind, id}` | Deliberate navigation to a logical entity's current state. It makes no historical claim. |
| `EntityRef` | `{kind, id, version}` | Exact retained representation, used for evidence, decisions, captures, admission and historical relationships. |
| `EvidenceRef` | `{kind, id, version, locator?}` | Exact Source, Observation, Projection or Snapshot version, optionally selecting a field/content location. |

For example, `{ "kind": "Scenario", "id": "scenario-checkout", "version": 4 }` pins one published Scenario. It does not introduce a ScenarioVersion object. The same reference rule applies to Service, Connection, Command, ReadAttempt and every other entity.

Parent IDs used only for ownership and navigation remain IDs. They do not freeze the parent's current name or configuration. A capture or decision that depends on parent content must additionally pin that parent's version. A selected evidence reference always includes its version. Resolving any reference enforces Workspace, kind and parent scope as well as authorization.

A snapshot's manifest contains exact entity-version references for its retained closure. Every historical input required to interpret its contents is present and resolvable under that manifest. Latest aliases, ID-only evidence links and independently selected current records cannot fill a historical gap.

## 3. Ownership and publication authority

Versioning and edit authority are independent. The model identifies who can publish a successor and which fields or lifecycle transitions that authority owns.

| Authority | Examples | Publication rule |
| --- | --- | --- |
| Local application commands | Workspace, Connection, System, UserJourney, Service, WorkItem, Scenario | Validate the named writable fields and expected owning-entity version. Publish a successor atomically. |
| Trusted collector/normalizer | Resource, HealthEvent, EventContext, Finding, Execution, Experiment | Publish observed representations with exact retained evidence. Clients cannot set provider status. |
| Collector lifecycle | Collection, ReadAttempt, Observation | Retain failed, empty and successful reads. A settled fact is not reopened by a client. |
| Trusted derivation | Projection, Communication | Publish a result under registered rules, exact input versions and qualified coverage. |
| Workflow runtime | Run, StepRun, StepAttempt | Publish permitted lifecycle transitions and retain dispatch/admission identity. Sealing limits subsequent changes. |
| Command dispatcher/reconciler | Command | Preserve durable intent, dispatch attempts, uncertainty and observed outcome. |
| Capture service | Snapshot | Publish a closed manifest of retained versions. Any later correction uses another version of that capture; a distinct capture occurrence has its own identity. |

Local values such as Dependency governance and Recommendation enrichment are part of their owner. They have **no separate version counter**. Editing governance compares Dependency.version; editing enrichment compares Recommendation.version. A provider-observed change may therefore make an outstanding local edit stale. That conservative conflict is explicit; accepting an old edit must never silently overwrite newer evidence.

Field authority still remains narrow. A local governance command cannot set native classification. Recommendation enrichment cannot edit the suggested change. WorkItem owns assignment, work state, due dates and verification. Recommendation carries its estimate and explanatory enrichment without a second competing operator workflow.

Service.memberships is the sole writable catalogue membership. Reverse journey lists are derived. Native Resilience assignments and effective policy context remain provider evidence; a local catalogue edit cannot imply a native policy change. ProviderBinding records the established association.

## 4. Source, observation and interpretation

### Distinct concepts, one version mechanism

| Concept | Identity and content | Version behavior |
| --- | --- | --- |
| Source | One retained source document/representation with native identity, profile, source operation and payload | Changed retained content publishes a new Source version under the same sourceId. |
| Observation | One genuine read/receipt occurrence, with Connection, clocks and source reference | Repeated reads are different occurrences. Each Observation has the common version metadata and pins the Source version it saw. |
| Projection | One named interpretation in a registered profile and subject scope | New selected inputs or rules produce another Projection version; older results stay available. |

Source identity excludes content digest and provider version. Representation/profile scope distinguishes a summary from detail and a request envelope from a response. The exact source profile defines the identity tuple. Identical bodies from distinct native messages do not merge because their source identities differ.

The document's digest describes its declared bytes or canonical JSON representation. It is neither an entity ID nor a version number. `payloadStorage=INLINE` preserves arbitrary native JSON, including a real JSON null. `payloadStorage=ARTIFACT` requires an exact artifact reference and a null inline placeholder. FieldPresence distinguishes absent, unrequested, unavailable and redacted fields. Raw provider payloads do not become writable extension maps.

`digestProfile` declares raw-byte SHA-256 or canonical JSON hashing. Raw-byte mode requires retention of those bytes. Canonical JSON follows [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785). Hashes detect content disagreement; they do not authenticate the provider or establish access rights.

Projection holds a typed result under one of five profiles: `EVALUATION`, `LIFECYCLE_EXPOSURE`, `INVESTIGATION_RESULT`, `SERVICE_STATUS` and `WORKSPACE_SUMMARY`. It pins subject versions, exact input versions, rule identity, cutoff, generation time and coverage. Its identity and version are independent of the source entity's version. Recalculation cannot renew old source evidence.

### Collection and coverage

Collection is one finite pass over a declared query set. Its query definitions remain fixed for that collection identity; state and coverage publish later versions. ReadAttempt represents an actual request, including unsuccessful and empty requests, and pins request/response Source versions. A missing response stays unavailable rather than becoming an empty success.

API observations identify a ReadAttempt and pinned Connection. Event/stream/local observations retain the actual receipt channel and context without inventing a native read. An ingestion replay and a second genuine delivery are distinct cases.

Coverage records query scope, pagination, hydration, identity/resource resolution, failures, clocks and sufficiency for the claim. A complete list traversal is not a complete external history or an atomic capture across AWS APIs. Absence requires adequate evidence over a closed scope. Unknown, empty, zero, unavailable, stale and unconfigured remain different facts.

## 5. Snapshots and derived state

Snapshot represents an explicit capture. `members` pins entity versions, including Sources, Observations, Projections, Collections and ReadAttempts needed by the retained evidence closure. ReadAttempts are referenced through the common version contract rather than copied as a second authoritative entity inside the snapshot. Owned graph nodes, graph edges and profile-specific capture values remain snapshot content.

The current `CaptureSnapshot` contract creates a new capture at version 1. A guarded correction writer is deferred; the common history/read contract already supports retained later Snapshot versions. Uniform versioning does not require a generic update command for every entity.

The capture records a start/end interval, coverage and manifest digest. Capture time cannot replace source time. A historical artifact unavailable under retention or current authorization is reported as unavailable. A current document cannot silently substitute for it.

PolicyContext pins the exact observed assignment and effective-target evidence, configured component set and supporting versions. It qualifies whether the provider supplied its actually evaluated revision. Observing policy content does not prove which exact policy revision AWS evaluated.

Graph keys and endpoints belong to the capture. Every referenced endpoint resolves within that graph; unresolved native objects retain qualified identity/evidence. Provider topology, dependency, sequence and causal hypotheses remain distinct relationship meanings.

Independent state dimensions remain explicit: provider status, coverage, technical execution, assessment verdict/finality, cleanup/effect state and local disposition. A completed WorkItem cannot clear Health impact. A successful execution can fail acceptance. A passed assessment does not prove remote effects are quiescent. Counts name their population and deduplication rule; an empty denominator does not yield automatic 100 percent.

## 6. Domain modules

### Workload and Health

System, UserJourney and Service supply the local workload catalogue. Resource is inventory identity; an affected-entity record or selected target is not automatically a Resource. ResourceMatch retains the matching rule and evidence. A captured pod name may identify a run-scoped selection without proving a stable incarnation across runs.

HealthEvent is native event identity. EventContext partitions PUBLIC, ACCOUNT and ORG_SUMMARY evidence. PUBLIC has no affected-account owner. ACCOUNT has one account. ORG_SUMMARY has organization scope and no EntityImpact children. A notification recipient does not create provider-reported account impact. EntityImpact retains its context and explicit inventory matches.

Communication groups validated logical pages while retaining conflicting candidates and delivery references. LifecycleEntry retains catalogue identity/matching limits and milestone content; ComponentDeployment retains observed inventory context. LifecycleExposure is a versioned Projection with exact deployment/catalogue inputs. Local acknowledgement, assignment and verification are WorkItem state. These boundaries preserve the [Health analysis](../aws/health/analysis/report.md).

### Resilience

ResilienceAssessment is a native service-scoped execution. Finding is also service-scoped and has no mandatory assessment foreign key. A relationship is retained only when source evidence supports it.

Recommendation preserves one captured suggestion and its allowed local enrichment. When no stable native suggestion ID exists, identity is scoped to Finding, exact Source version, group and ordinal. A repeated Observation of that same source does not create another Recommendation. An ordinal in a changed Source version does not prove continuity with the old suggestion. Enrichment changes use Recommendation.version; operator assignment/workflow belongs to WorkItem.

Policy components, assessment execution, retained posture and runtime health remain distinct. A failed new assessment does not delete prior posture; its freshness/context may change. Findings distinguish summary, detail, unknown suggestion availability and known empty suggestions. Native disposition/classification commands remain separate from local governance or work. See the [Resilience analysis](../aws/resilience-hub/analysis/report.md) and [source API contracts](../aws/resilience-hub/analysis/api/entities.md).

### Investigations

AgentSpace is the native provider scope. Investigation is the aggregate over a native Task of type INVESTIGATION. Execution membership is an observed relation; an Execution does not acquire a fictional single investigation parent. Task's execution pointer remains optional and does not imply latest/root/only membership.

JournalRecord preserves its envelope, arbitrary native content and pinned Source/Observation references. InvestigationResult distinguishes phase, selected evidence, expected-but-unavailable content, pending hydration, explicit no-summary and ambiguous candidates. A mitigation completion cannot replace investigation-phase evidence.

ApprovalRequest pins the observed request and action digest. Decision and resume are separate Commands. Their acceptance, later observed action execution and operational recovery remain distinct. Every Command has its own entity history.

Asset has the common entity version and captures an exact `nativeVersion`, source and files in that representation. It does not contain an embedded array of independent AssetVersion records. Application and native versions remain different fields. An asset link still does not prove a historical execution consumed it. See the [investigation data model](../aws/devops-agent/analysis/annexes/Investigation_Data_Model.md).

### Workflow and FIS

Scenario owns its definition and publication metadata. A DRAFT version carries authoring content. Publishing creates the next Scenario version in PUBLISHED state with validated input schema, expression contract, operation/schema/implementation locks and digest. The published version stays immutable. Editing it creates a later DRAFT version; it does not reopen that historical publication.

Run pins a PUBLISHED Scenario version. A later current DRAFT does not invalidate explicitly selected older PUBLISHED versions. An ARCHIVED current Scenario head blocks new admission, even if the requested older version was published. Archival itself creates another Scenario version. Exact replay of an already admitted Run resolves before the current archive check. These controls distinguish immutable program selection from current admission policy without introducing a revision entity.

Admission also pins subject and Connection versions, validated inputs, allowed scope, enabled steps, concurrency identity and required criteria in a RUN_INPUT Snapshot. Runtime skips, cancellation and dependency failure cannot shrink the admitted denominator. A zero denominator means NOT_EVALUATED. Any conclusive required failure means FAIL; all required criteria passed means PASS; otherwise the result is INCONCLUSIVE.

Run, StepRun and StepAttempt use the same `version` field as other entities. `Run.steps` pins exact StepRun versions, and `StepRun.selectedAttempt` pins an exact StepAttempt version. A historical Run cannot derive its verdict by joining current children. Attempt number identifies a distinct execution attempt. Transport retry/polling retains that attempt; an intentional new operation attempt needs the required prior-effect reconciliation. Dispatch identity is persisted before the external call. Previously sealed conclusions and pinned evidence remain immutable.

Cancellation records monotonic intent, fences new main dispatch and permits required finalization under its own budget. A response-lost start is reconciled through non-creating reads. Unknown effects remain explicit, with the required protective hold. A later observation or Evaluation Projection can explain later knowledge without rewriting a pinned historical Run outcome. The [source workflow](../aws/fis/analysis/workflow/model.md) supplies the execution/evaluation distinctions.

Experiment is native FIS execution and remains independently observable from Run. Actions, selected targets and report details are owned values. Target selection is not proof of fault application; report readiness is separate from execution and acceptance. Native control remains at the experiment boundary. The [FIS review](../aws/fis/analysis/QUALITY_REVIEW.md) records these constraints.

## 7. API and storage consequences

Typed getters can select an exact version. `ListEntityVersions` lists the retained versions for a logical identity; it does not create a history entity. Current lists return a stable traversal of entity/version pairs. Owned-child lists select a parent version and its pinned child references. Expected-version checks apply to the entity being changed; ingestion and internal lifecycle publishers serialize their own transitions. Request bodies cannot supply their own version metadata or authority.

A provider precondition pins observed application evidence and the intended native scope. It is not an AWS compare-and-swap promise. Durable Command identity, idempotent admission, fenced dispatch and non-creating reconciliation preserve the distinction.

Persistence must enforce unique `(workspace, kind, id, version)` records, one current head per logical identity, atomic successor publication, authorized historical resolution and immutable prior versions. This contract leaves physical layout open. Content-addressed blobs, indexes and retention metadata may be implementation details without appearing as domain version entities.

Retained references must not be cascade-deleted through a friendly-name owner. Authorized deletion/retention can make content unavailable with an explicit reason; it cannot cause history to resolve to unrelated current data. Importing legacy data records actual provenance and unavailable history rather than manufacturing prior versions.

## 8. Extension and compatibility

A new module supplies typed entities, values, source profiles, operations and relationships. It reuses versioning, references, evidence and commands. Owned values inherit the owner's version. Independent entities need a concrete identity and lifecycle.

Unknown provider output vocabulary is retained conservatively. Writable inputs remain deliberate and closed. Identity, version selection, reference shape, state meaning, null/absence, replay and pagination semantics are compatibility boundaries.

This revision changes those contracts and uses the **`ConsolidatedOperationsConsole_20261105V2`** namespace. [CONSOLIDATION_PLAN.md](CONSOLIDATION_PLAN.md) maps the old revision-oriented surface to the uniform model; [REVIEW.md](REVIEW.md) records why the first consolidation required correction.
