# Rules for mapping AWS constructs to the consolidated model

Map constructs described in the pinned AWS solution analyses into the consolidated model. These are application design rules, not claims about complete current AWS SDK coverage or implemented adapters.

Use the rules in this order: establish the source concept and scope; decide entity/value/reference/view/retained-DTO ownership; preserve identity, versions and evidence; then prove the claimed coverage. The same rules apply to all modules.

## Decision catalog

| Rule | Decision |
| --- | --- |
| [MAP-01](#map-01) | Count source concepts, aliases and target entities separately |
| [MAP-02](#map-02) | Promote a concept to an entity for identity and lifecycle |
| [MAP-03](#map-03) | Keep versions on the substantive entity |
| [MAP-04](#map-04) | Use owned values for details with one lifecycle owner |
| [MAP-05](#map-05) | Preserve full provider identity independently of access |
| [MAP-06](#map-06) | Give relationships one owner and explicit provenance |
| [MAP-07](#map-07) | Keep retained content, receipt and interpretation distinct |
| [MAP-08](#map-08) | Retain native DTO breadth without claiming normalization |
| [MAP-09](#map-09) | Use typed projections for conclusions and views |
| [MAP-10](#map-10) | Separate historical captures from ordinary version history |
| [MAP-11](#map-11) | Model collection coverage and per-item failures explicitly |
| [MAP-12](#map-12) | Preserve independent state dimensions and meanings |
| [MAP-13](#map-13) | Give local work and mixed authority explicit owners |
| [MAP-14](#map-14) | Separate API DTOs and commands from entity reads |
| [MAP-15](#map-15) | Treat admission, replay and external outcome as separate facts |
| [MAP-16](#map-16) | Preserve metric and evaluation meaning in typed contracts |
| [MAP-17](#map-17) | Keep presence, future provider values and units lossless |
| [MAP-18](#map-18) | Keep external identity and administration at their real boundary |
| [MAP-19](#map-19) | Require a concrete proof for each coverage claim |
| [MAP-20](#map-20) | Close gaps with the smallest coherent extension |

<a id="map-01"></a>

## MAP-01 — Count source concepts, aliases and target entities separately

Use a declared source population and retain source-service scope. Count a diagram symbol once per source service; collapse naming aliases only when the source establishes that they mean the same concept. Never treat mapping rows, native DTO names or spelling aliases as entity totals.

**Required evidence.**

- A pinned source file and exact declaration or dictionary entry
- An explicit alias decision and source semantic kind
- An independently extracted denominator and per-population counts

**Example.** The source Task and application Investigation aggregate remain two source constructs even when both contribute to consolidated Investigation. HealthEvent and HEALTH_EVENT can be spelling aliases of one concept.

**Failure to avoid.** Reporting 340 aliases or 174 mapping rows as 340 or 174 represented entities.

**Acceptance.** Every declared source symbol resolves to exactly one audited construct; source and target totals are reported as a many-to-many mapping.

**Sources.** [consolidated-operations-console/MAPPING.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/MAPPING.md) · [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json)

<a id="map-02"></a>

## MAP-02 — Promote a concept to an entity for identity and lifecycle

Use a first-class entity when the application needs to identify, authorize, retrieve, relate or retain the concept independently through its lifecycle. A native resource can supply that identity, but a native DTO or a screen section alone does not justify a new root. A scoped child may still be an entity when it has meaningful identity and lifecycle.

**Required evidence.**

- Stable or explicitly provisional identity with full scope
- A lifecycle and authoritative publisher
- A concrete cross-module use case requiring independent references or reads

**Example.** Experiment, Finding and Execution have substantive identities and lifecycle. An experiment action remains an owned FISAction when its control and interpretation belong to the Experiment.

**Failure to avoid.** Creating one console CRUD entity for every AWS response structure, action parameter or configuration block.

**Acceptance.** The proposed entity has one owner/version contract and an explicit use case that cannot be represented clearly as an owned value or retained source profile.

**Current contract evidence.** `#/$defs/Experiment`; `#/$defs/Finding`; `#/$defs/Execution`; `#/$defs/FISAction` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/DESIGN_PRINCIPLES.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/DESIGN_PRINCIPLES.md) · [aws/fis/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/report.md)

<a id="map-03"></a>

## MAP-03 — Keep versions on the substantive entity

Every entity has stable identity plus version, createdAt and updatedAt. An old revision/history class maps to a version of its substantive owner or to exact evidence of that owner. Do not introduce an entity whose only purpose is to hold a version. Provider versions, schema versions and attempt numbers remain separate domain values.

**Required evidence.**

- A documented logical key independent of content digest
- A source-ID/version migration rule
- Exact references to retained representations

**Example.** ScenarioRevision maps to a PUBLISHED Scenario version. AssetVersion maps to an Asset representation with nativeVersion/source/files. SourceRevision maps to Source identity plus version.

**Failure to avoid.** Reintroducing ScenarioRevision, SourceRevision or separate governance/enrichment version counters.

**Acceptance.** All target entities require the common metadata; owned values have no competing entity clock and historical reads never fall back to latest.

**Current contract evidence.** `#/$defs/Scenario`; `#/$defs/Asset`; `#/$defs/Source`; `#/$defs/EntityRef` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/MODEL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/MODEL.md) · [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md)

<a id="map-04"></a>

## MAP-04 — Use owned values for details with one lifecycle owner

Represent parameters, policy components, action details, files and configuration values inside their owning entity when they have no independent application lifecycle. Their local keys can identify members, but their changes advance the owner's version. A standalone value definition is insufficient unless an owner actually binds it.

**Required evidence.**

- A reachable typed owner property or a discriminator-enforced binding
- Collection semantics, member keys and relevant cardinality
- Owner-level concurrency and publication rules

**Example.** Asset.files contains AssetFile values and Scenario.definition contains StepDefinition values. A declared EventDescription type with no owner binding does not establish normalized description coverage.

**Failure to avoid.** Pointing a crosswalk to a value name that is absent, unbound, or reachable only through untyped JSON.

**Acceptance.** The typed value is reachable from the named owner under the correct discriminator, and the source concept's essential semantics can be expressed there.

**Current contract evidence.** `#/$defs/Asset/properties/files`; `#/$defs/Scenario/properties/definition`; `#/$defs/StepDefinition`; `#/$defs/EventDescription` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) · [aws/fis/analysis/workflow/model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/model.md)

<a id="map-05"></a>

## MAP-05 — Preserve full provider identity independently of access

Retain provider/service, partition, account, region, parent keys and native identity where applicable. A Connection records the authorized access path; it does not determine native object identity. Friendly names, unqualified IDs and digests cannot establish cross-source identity.

**Required evidence.**

- A source-specific identity tuple and stability statement
- Verified provider bindings or explicit unresolved identity
- The parent ownership required for reads and mutations

**Example.** Health event context qualifies impacts by event/account context. FIS pod identity includes cluster and namespace. Switching the reader connection does not create a new native object.

**Failure to avoid.** Joining different native objects by name, or duplicating an object for every credential/connection that observes it.

**Acceptance.** Identity is scoped and stable where supported; ambiguity remains explicit and no reference itself grants authority.

**Current contract evidence.** `#/$defs/SourceIdentity`; `#/$defs/OwningScope`; `#/$defs/Connection`; `#/$defs/ProviderBinding`; `#/$defs/ResourceMatch` in [model/schema.json](model/schema.json).

**Sources.** [aws/health/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md) · [aws/fis/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/report.md) · [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md)

<a id="map-06"></a>

## MAP-06 — Give relationships one owner and explicit provenance

Represent membership and association facts as owned values or qualified references unless they need an independent lifecycle. Specify the authoritative writer, parent consistency, direction and observation evidence. Derive inverse indexes instead of introducing a second mutable authority.

**Required evidence.**

- Owner and member identity
- Parent consistency and inverse-view rules
- Evidence for imported or inferred association claims

**Example.** Service owns System/UserJourney memberships. Execution task memberships are observed relations; one mandatory Investigation parent must not be invented.

**Failure to avoid.** Two editable service lists, fabricated parentage, or an unqualified inferred relationship presented as a provider fact.

**Acceptance.** A relationship's owner, key and evidence are explicit, and a historical relationship does not join current parent content silently.

**Current contract evidence.** `#/$defs/Service/properties/memberships`; `#/$defs/ServiceMembership`; `#/$defs/TaskExecutionMembership`; `#/$defs/Execution` in [model/schema.json](model/schema.json).

**Sources.** [aws/resilience-hub/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md) · [aws/devops-agent/analysis/annexes/Investigation_Data_Model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/annexes/Investigation_Data_Model.md)

<a id="map-07"></a>

## MAP-07 — Keep retained content, receipt and interpretation distinct

Map native content to Source, its observation occurrence to Observation, and a computed interpretation to Projection. A repeated poll can observe the same Source version. Changed content advances the Source; receipt order is not provider event order.

**Required evidence.**

- Stable source identity and representation/profile/operation key
- Exact Source reference on each observation
- Provider, transport, observation and local publication time meanings

**Example.** EventRevision and EntityRevision contribute retained Source versions and observations without creating new event or impact identities for every poll. A→B→A content yields successive versions, not a return to version 1.

**Failure to avoid.** Counting repeated receipts as new domain objects, conflating observation time with provider time, or refreshing evidence freshness by recomputing a view.

**Acceptance.** Source identity, observation occurrence and interpretation identity are independently explainable and use the same entity-version mechanism.

**Current contract evidence.** `#/$defs/Source`; `#/$defs/Observation`; `#/$defs/Projection` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/MODEL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/MODEL.md) · [aws/devops-agent/analysis/annexes/Investigation_Data_Model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/annexes/Investigation_Data_Model.md)

<a id="map-08"></a>

## MAP-08 — Retain native DTO breadth without claiming normalization

Keep native summaries, detail documents, streams, nested values and deferred administration shapes in registered Source profiles with their unknown fields and provider values. State explicitly when the representation remains raw retention. A profile's observedFields hints do not constitute an enforced normalized model or implemented adapter.

**Required evidence.**

- Registered profile and complete source identity
- Known field hints plus unknown-field/value retention policy
- Named normalization and mutation deferrals

**Example.** A native FIS template or DevOps Trigger can remain inspectable through Source without becoming a console CRUD root. A retained target selector is not a typed Experiment target-selection collection.

**Failure to avoid.** Calling an arbitrary Source.payload or an existing profile ID complete normalized coverage.

**Acceptance.** Retention coverage and typed model coverage have separate statuses; no unsupported product capability is inferred from a retained payload.

**Current contract evidence.** `#/$defs/Source/properties/payload`; `#/$defs/Source/properties/profile`; `#/$defs/FieldPresence` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json) · [consolidated-operations-console/CONTEXT_AND_SCOPE.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/CONTEXT_AND_SCOPE.md)

<a id="map-09"></a>

## MAP-09 — Use typed projections for conclusions and views

Represent a computed result with a declared Projection profile, a typed result shape, exact inputs, rule identity, cutoff and coverage. A UI view, timeline or graph name alone does not prove that a corresponding normalized profile exists. Preserve uncertainty and candidate selection rules.

**Required evidence.**

- A registered discriminator that binds to a schema
- Exact subject and input references
- Selection/reducer meaning and coverage requirements

**Example.** LIFECYCLE_EXPOSURE, INVESTIGATION_RESULT and EVALUATION are typed profiles. A retained TimelineItem profile must not be counted as a typed Projection profile unless its result contract is actually added.

**Failure to avoid.** Inventing an unavailable profile, presenting an inferred hypothesis as native truth, or dropping the rationale behind a current status.

**Acceptance.** The schema/profile combination can encode the source view's essential semantics, and later interpretation creates another representation without rewriting old evidence.

**Current contract evidence.** `#/$defs/Projection`; `#/$defs/LifecycleExposure`; `#/$defs/InvestigationResult`; `#/$defs/Evaluation` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) · [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json)

<a id="map-10"></a>

## MAP-10 — Separate historical captures from ordinary version history

Use Snapshot for a deliberate closed historical capture over exact entity representations and evidence. Use ordinary entity history for successive versions of one identity. Structural parent IDs and raw JSON must not become implicit joins to current state.

**Required evidence.**

- Exact retained members and closure rules
- Capture interval/cutoff and coverage
- Typed contents binding where normalized capture semantics are claimed

**Example.** A topology capture owns GraphContents; a policy-context capture owns PolicyContext. Snapshot.members pins entity versions instead of embedding competing authoritative entity copies.

**Failure to avoid.** Treating Snapshot as a universal untyped replacement for every missing model, or reconstructing an old assessment from today's policy/configuration.

**Acceptance.** Historical captures are reproducible from their exact members, and typed capture contents preserve the relevant source semantics.

**Current contract evidence.** `#/$defs/Snapshot`; `#/$defs/GraphContents`; `#/$defs/PolicyContext`; `#/$defs/EntityRef` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md) · [aws/resilience-hub/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md)

<a id="map-11"></a>

## MAP-11 — Model collection coverage and per-item failures explicitly

Represent bounded queries and reads with Collection and ReadAttempt, retaining empty successes and failures. Qualify pagination, detail, identity and claim coverage independently. A batch's failed item must retain its subject/context; HTTP success or a completed page chain does not prove a complete claim.

**Required evidence.**

- Fixed query, authorization and parent scope
- Request/response evidence including empty and partial success
- Error subject identity and independent coverage dimensions

**Example.** AWS Health failedSet entries need event/account attribution. A general transport ReadError alone cannot serve as a normalized item-error collection.

**Failure to avoid.** Treating HTTP 200 as complete success or mapping a collection of contextual item failures to one undifferentiated error.

**Acceptance.** The model can explain precisely what was requested, what returned, which subjects failed and what claims the evidence supports.

**Current contract evidence.** `#/$defs/Collection`; `#/$defs/ReadAttempt`; `#/$defs/ReadError`; `#/$defs/Coverage` in [model/schema.json](model/schema.json).

**Sources.** [aws/health/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md) · [aws/fis/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/report.md) · [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md)

<a id="map-12"></a>

## MAP-12 — Preserve independent state dimensions and meanings

Map provider state, technical execution, acceptance, cleanup, artifact readiness, local disposition and work verification separately. Preserve the original vocabulary and qualification. Similar labels from different AWS products are not interchangeable states or entity kinds.

**Required evidence.**

- Each state dimension's owner and evidence
- Unknown/unavailable semantics
- A documented mapping for every normalized interpretation

**Example.** The FIS report's local RESILIENCE_ASSESSMENT is an EVALUATION projection, not the native ResilienceAssessment entity. An approved tool action is not proof of resumed execution or success.

**Failure to avoid.** Merging distinct assessments because names match, or interpreting completed execution as successful acceptance or remediation.

**Acceptance.** Independent dimensions can disagree without losing information; source and target meanings are explicit in the crosswalk.

**Current contract evidence.** `#/$defs/Run`; `#/$defs/ServiceStatus`; `#/$defs/ResilienceAssessment`; `#/$defs/Evaluation`; `#/$defs/ApprovalRequest` in [model/schema.json](model/schema.json).

**Sources.** [aws/fis/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/report.md) · [aws/resilience-hub/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md) · [aws/devops-agent/analysis/annexes/Investigation_Data_Model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/annexes/Investigation_Data_Model.md)

<a id="map-13"></a>

## MAP-13 — Give local work and mixed authority explicit owners

Keep assignment, completion and verification in WorkItem. Keep recommendation estimates/notes and dependency governance in their owning entity as values with narrow write authority. All fields of a given entity still serialize through its one version boundary.

**Required evidence.**

- Field authority and command owner
- Exact verification evidence
- One expectedVersion guard for each changed entity

**Example.** Recommendation.enrichment has no independent workState or version. Dependency.governance has application authority while observed fields retain collector authority, using the same Dependency version.

**Failure to avoid.** Separate overlay clocks, duplicated task ownership, or local completion changing provider impact/finding state.

**Acceptance.** There is one owner for each editable value and no hidden mutation under an unchanged entity version.

**Current contract evidence.** `#/$defs/WorkItem`; `#/$defs/Recommendation/properties/enrichment`; `#/$defs/Dependency/properties/governance` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/DESIGN_PRINCIPLES.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/DESIGN_PRINCIPLES.md) · [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md)

<a id="map-14"></a>

## MAP-14 — Separate API DTOs and commands from entity reads

Map request/response wrappers as transport shapes, not domain entities. Expose deliberate operations with closed writable inputs. Distinguish a local catalog edit from native dispatch; a provider action is only present when an explicit command contract and authority exist.

**Required evidence.**

- Operation effect, permission and input/output schemas
- Named target entity and expected-version/source preconditions
- Native operation binding or explicit deferral

**Example.** UpdateService edits local catalog metadata; UpdateResilienceServiceConfiguration is an explicit provider command. A native SendMessage event union remains a stream DTO rather than another entity per event variant.

**Failure to avoid.** Generating CRUD from a native response shape or claiming a deferred AWS write exists because its payload is retained.

**Acceptance.** Read models and write DTOs are separate and every external effect has a named durable command boundary.

**Current contract evidence.** `#/$defs/Command`; `#/$defs/Service` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/api/operations.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/operations.json) · [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md)

<a id="map-15"></a>

## MAP-15 — Treat admission, replay and external outcome as separate facts

Map intent to Command and later outcome to authoritative observations and entity versions. Use immutable receipts, intent tokens and current authorization. A retryable console response cannot authorize blindly repeating an uncertain creating provider call.

**Required evidence.**

- Exact admitted intent and returned version references
- Replay identity and expiry guarantees
- Native effect identity and non-creating reconciliation

**Example.** A decision Command can be accepted before provider approval is definitive. ResumeExecution requires the exact successful decision version and approval context. Cancellation does not establish remote cessation or cleanup.

**Failure to avoid.** Replaying latest results instead of the original receipt, or conflating accepted stop/cancel with completed cleanup.

**Acceptance.** The application can distinguish requested, admitted, dispatched, observed, failed and uncertain effects without rewriting prior records.

**Current contract evidence.** `#/$defs/Command`; `#/$defs/ExternalOperationRef`; `#/$defs/CancellationIntent` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md) · [aws/fis/analysis/workflow/model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/model.md)

<a id="map-16"></a>

## MAP-16 — Preserve metric and evaluation meaning in typed contracts

When a metric, criterion or evaluation is normalized, retain query identity, dimensions, units, aggregation/window rules, missing-data semantics, threshold/evaluator identity and denominator. A generic binding or arbitrary inputs map is insufficient proof that those contracts exist.

**Required evidence.**

- Typed metric/query and criterion definitions or an explicitly pinned operation schema
- Exact evidence and evaluation cutoff
- Fixed required-criterion denominator and units/absence policy

**Example.** The admitted workflow criteria must not shrink when a step is skipped. A named MetricBinding crosswalk requires a real typed value/profile binding before it can be counted as normalized.

**Failure to avoid.** Treating a missing sample as zero, a JSON inputs bag as a metric model, or skipped checks as a higher pass rate.

**Acceptance.** A retained evaluation can be interpreted from its exact definition, evidence, denominator and evaluator contract; unknown inputs remain unknown.

**Current contract evidence.** `#/$defs/StepDefinition`; `#/$defs/CheckResult`; `#/$defs/Admission`; `#/$defs/Evaluation` in [model/schema.json](model/schema.json).

**Sources.** [aws/fis/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/report.md) · [aws/fis/analysis/workflow/model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/model.md)

<a id="map-17"></a>

## MAP-17 — Keep presence, future provider values and units lossless

Preserve unknown native fields/enums and distinguish omitted, null, empty, zero, unavailable and not requested. State units and time precision explicitly. Writable normalized inputs remain closed and strict; read tolerance must not manufacture success.

**Required evidence.**

- Source field-presence and raw-payload retention
- Units, time and normalization rules
- Output-tolerance and input-validation boundaries

**Example.** An omitted Health aggregate account breakdown is not zero affected accounts. Unknown FIS runtime state is retained instead of mapped to success. Native timestamp precision remains in source evidence if normalized precision differs.

**Failure to avoid.** Defaulting unfamiliar provider values to healthy/completed, or deleting richer detail because a later summary omits it.

**Acceptance.** A consumer can distinguish unavailable or unrequested information from a known value and inspect the original source when normalization is incomplete.

**Current contract evidence.** `#/$defs/FieldPresence`; `#/$defs/Source`; `#/$defs/Timestamp`; `#/$defs/StateDimension` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md) · [aws/health/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md)

<a id="map-18"></a>

## MAP-18 — Keep external identity and administration at their real boundary

Reference accounts, organizations, credentials, external resources and integration configuration without inventing duplicate ownership. Retain administrative breadth through named profiles until a concrete use case requires normalized management. Historical configuration is evidence, never a surviving permission grant.

**Required evidence.**

- Actual external owner and identity scope
- Current access checks independent of retained versions
- Explicit managed-versus-referenced responsibility

**Example.** Workspace is the application scope; AgentSpace is a native DevOps object. Account and organization references do not become new console tenancy entities, and a captured credential reference cannot restore revoked access.

**Failure to avoid.** Conflating provider account/AgentSpace with application tenancy or treating stored configuration as authorization.

**Acceptance.** The console owns only its stated domain and preserves the external identifiers and current authorization boundaries needed for its use cases.

**Current contract evidence.** `#/$defs/Workspace`; `#/$defs/AgentSpace`; `#/$defs/Connection`; `#/$defs/OrganizationMembership`; `#/$defs/OrganizationAccess` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/CONTEXT_AND_SCOPE.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/CONTEXT_AND_SCOPE.md) · [consolidated-operations-console/api/PROTOCOL.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/api/PROTOCOL.md)

<a id="map-19"></a>

## MAP-19 — Require a concrete proof for each coverage claim

Record source evidence, semantic kind, owner, exact schema paths, profile bindings and preserved invariants per construct. Distinguish NORMALIZED, RETAINED_ONLY, PARTIAL and UNMAPPED. A pointer's existence is structural evidence; semantic completeness still needs source-to-target review.

**Required evidence.**

- Source declaration and prior use
- Resolvable target schema pointers and registered profile IDs
- Essential semantic checks and any limitations

**Example.** A GraphEdge type proves typed endpoints and relationKind; it does not by itself prove preservation of every native edge relation/property grouping. A named but unbound EventDescription is not complete normalized coverage.

**Failure to avoid.** A green alias-existence check being reported as complete model or adapter coverage.

**Acceptance.** Every status is inspectable, denominators are reproducible, gaps have clear remedies, and runtime conformance is reported separately.

**Current contract evidence.** `#/$defs/GraphEdge`; `#/$defs/EventDescription` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/tools/validate.py](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/tools/validate.py) · [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json)

<a id="map-20"></a>

## MAP-20 — Close gaps with the smallest coherent extension

First bind an existing typed value correctly, then add a narrow owned value/profile if the use case requires it. Introduce a new entity only if identity, lifecycle and authority justify it under MAP-02. Keep consciously retained-only capabilities explicit and avoid generic mutable extension bags.

**Required evidence.**

- The user-facing use case affected by the gap
- The smallest typed owner/profile change and migration impact
- Validation examples and a deliberate API decision where writes are involved

**Example.** A missing Experiment selector collection or contextual batch-error collection usually calls for typed owned values, not ExperimentSelectorVersion or CollectionItemErrorVersion entities. Deferred native administration can stay retained-only.

**Failure to avoid.** Repairing coverage by adding a class for every source name, or claiming completeness by placing everything in generic JSON.

**Acceptance.** The correction restores required meaning while preserving a simple owner/version contract and explicit scope; entity count increases only when justified.

**Current contract evidence.** `#/$defs/Experiment`; `#/$defs/ReadAttempt`; `#/$defs/Source` in [model/schema.json](model/schema.json).

**Sources.** [consolidated-operations-console/DESIGN_PRINCIPLES.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/DESIGN_PRINCIPLES.md) · [consolidated-operations-console/CONSOLIDATION_PLAN.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/CONSOLIDATION_PLAN.md)

## Applying the catalog

Each row in the [source construct catalog](coverage/CATALOG.md) records its source evidence, semantic kind, exact target paths, profiles, coverage judgment and applicable rules. The [coverage audit](COVERAGE.md) reports the resulting populations and gaps. The current findings do not authorize treating raw retention as normalization or adding version-only entities.
