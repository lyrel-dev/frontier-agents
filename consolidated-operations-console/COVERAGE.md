# Model coverage audit

**Target:** main at [`20650d3`](https://github.com/lyrel-dev/frontier-agents/commit/20650d3cf051ad457378704c15f48f77565a611c). **Original analysis baseline:** [`d926a81`](https://github.com/lyrel-dev/frontier-agents/commit/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3). **Audit date:** 5 November 2026.

The consolidated model contains **36 uniformly versioned entities**. The broader source catalog identifies **63 substantive entity concepts** in the four original AWS solutions: **29 provider-owned** and **34 application-defined**. Of these, **38 are normalized**, **10 partial**, and **15 retained-only**; none is wholly unmapped. These are source concepts with identity/lifecycle, not a claim that the products expose that many standalone AWS resources or that the target needs that many entities.

The independently extractable source diagram population is broader than entities: the four AWS solutions declare **119 distinct model constructs**, and the shared workflow adds **11**, for **130**. All have registry aliases, but only **74/119 (62.2%)** of the four AWS solutions' constructs meet the normalized-core criterion. One source relationship, **ExperimentMetricBinding**, has no concrete representation despite its named registry row.

A source class/ER box is not necessarily an independent domain entity. These source populations include entities, owned values, relationships, external identities, derived views and former revision constructs. The audit does not turn every original box into a target entity.

## 1. Entity concepts represented from the original solutions

| Original solution | Substantive source entities | Provider-owned | Application-defined | Normalized | Partial | Retained only | Unmapped |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AWS Health | 12 | 3 | 9 | 11 | 0 | 1 | 0 |
| AWS Resilience Hub | 17 | 9 | 8 | 12 | 3 | 2 | 0 |
| AWS DevOps Agent | 21 | 11 | 10 | 11 | 5 | 5 | 0 |
| AWS FIS | 13 | 6 | 7 | 4 | 2 | 7 | 0 |
| Shared assessment workflow | 5 | 0 | 5 | 3 | 2 | 0 | 0 |

**Four AWS solutions:** 63 source entity concepts; 38 normalized, 10 partial, 15 retained-only, 0 unmapped. **Including shared workflow:** 68 substantive entity concepts. The original workflow's explicit six-entity table includes ScenarioRevision; this audit counts its five substantive identities separately from that pure history representation, which maps to Scenario.version.

The source-entity count is a documented semantic classification over the broader source catalog. It includes identity-bearing owned children and excludes pure historical representations (six across the four AWS solutions; seven including workflow ScenarioRevision), value objects, relationship records, external identity references and transport wrappers. It must not be substituted for the mechanically extracted diagram count below.

## 2. Fixed source-model coverage, including values and relationships

| Source model | Declared constructs | Normalized | Partial | Retained only | Unmapped | Normalized / total |
| --- | --- | --- | --- | --- | --- | --- |
| AWS Health | 23 | 20 | 1 | 2 | 0 | 87.0% |
| AWS Resilience Hub | 28 | 19 | 7 | 2 | 0 | 67.9% |
| AWS DevOps Agent | 34 | 21 | 11 | 2 | 0 | 61.8% |
| AWS FIS | 34 | 14 | 3 | 16 | 1 | 41.2% |
| Shared assessment workflow | 11 | 9 | 2 | 0 | 0 | 81.8% |
| **Four AWS solutions** | 119 | 74 | 22 | 22 | 1 | 62.2% |
| **Including shared workflow** | 130 | 83 | 24 | 22 | 1 | 63.8% |

**Normalized** means the source construct's essential application meaning has a bound typed representation. **Partial** means a typed core exists but a required distinction or binding is missing or ambiguous. **Retained only** means the source content is inspectable through a concrete retained representation/profile but is not fully normalized. **Unmapped** means no sufficient concrete representation was established. Percentages count only NORMALIZED in the numerator; there is no partial-credit weighting.

The denominator is extracted independently from class/ER declarations and relationship endpoints in the pinned source diagram files. Repeated symbols across pages count once per source service. The current registry is consulted only after that extraction. [Complete declaration-to-construct mapping](coverage/catalog.json) · [source-file/hash register and counts](coverage/report.json).

## 3. What the different counts mean

| Count | Population | What it does not establish |
| --- | --- | --- |
| 36 | Current first-class entity definitions; all require version/createdAt/updatedAt | 36 native AWS resources or one-to-one source entity preservation |
| 63 | Substantive native/application entity concepts reviewed in the four original solution catalogs | A target entity count or a complete live AWS resource inventory |
| 119 | Distinct named class/ER constructs in four AWS solution models | 119 independent native entities |
| 11 | Additional class/ER constructs in the application workflow model | Another AWS product or eleven extra target entities |
| 190 | Broader reviewed source-concept catalog, including named dictionary/control supplements | An SDK-wide or instance population |
| 52 | Selected DevOps returned/nested SDK types, audited separately | 52 additional business entities; this set overlaps model concepts |
| 182 | The earlier validator's 130 diagram names plus 52 native SDK shape names | 182 distinct source entities or semantic normalization proofs |
| 174 | Existing mapping rows | 174 distinct original entities; some rows group multiple concepts |
| 340 | Existing service/concept spelling aliases | 340 represented entities |
| 65 | Registered retained/native/normalized profiles | 65 implemented adapters or enforced native payload schemas |

### Source semantic kinds

| Source semantic kind | Fixed diagram population | Broader catalog |
| --- | --- | --- |
| NATIVE_RESOURCE | 23 | 29 |
| APPLICATION_ENTITY | 37 | 39 |
| OWNED_VALUE | 33 | 57 |
| RELATIONSHIP | 17 | 19 |
| EXTERNAL_IDENTITY | 7 | 11 |
| HISTORY_REPRESENTATION | 7 | 7 |
| DERIVED_VIEW | 5 | 14 |
| TRANSPORT_DTO | 0 | 6 |
| CONTROL_VALUE | 1 | 8 |

The kinds describe the source role as reviewed in the original solution. NATIVE_RESOURCE denotes an identity-bearing provider object in that solution; APPLICATION_ENTITY denotes an application-owned substantive object. HISTORY_REPRESENTATION is intentionally separate and maps to an owner's ordinary version/evidence mechanism. These labels are review classifications, not claims that all AWS SDK shapes are domain entities.

### Broader dictionary and native-shape audit

| Population | Total | Normalized | Partial | Retained only | Unmapped |
| --- | --- | --- | --- | --- | --- |
| Diagram + named dictionary/control concepts | 190 | 103 | 29 | 57 | 1 |
| 52 selected DevOps SDK types (separate) | 52 | 10 | 1 | 41 | 0 |

The broader catalog can expose missing semantics that were not drawn in a diagram. It is not added to the diagram or native-shape populations. [Every audited concept and its proof](coverage/CATALOG.md).

## 4. How source entities contribute to the 36-entity model

The registry's `canonicalEntity` rows name **31 distinct target entities** across the four AWS solutions. Including the application workflow names **35 of 36**. The remaining target is **Workspace**, introduced as a shared application boundary from earlier scope/context requirements. These are declared lineage counts; a partial source mapping remains partial even if its target entity exists.

| Source package | Registry mapping rows | Aliases | Distinct targets of canonicalEntity rows |
| --- | --- | --- | --- |
| AWS Health | 32 | 74 | 13 |
| AWS Resilience Hub | 40 | 67 | 13 |
| AWS DevOps Agent | 51 | 139 | 13 |
| AWS FIS | 34 | 38 | 3 |
| Shared assessment workflow | 17 | 22 | 6 |

Per-package target sets overlap through Source, Observation, Collection, Command and other shared entities, so these target counts must not be summed. The [machine report](coverage/report.json) lists the exact sets.

All 36 target entities pass the uniform version-field check. The model has 64 owned value definitions and five typed Projection result profiles. A schema reachability check finds **EventDescription** declared but unreachable from any entity: defining a type alone does not bind it into the model.

## 5. Findings and decisions

### COV-HR-01 — Localized EventDescription is declared but unbound

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/EventDescription` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Source/properties/payload` · [aws/health/analysis/report.md#3-core-entity-dictionary-and-keys](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md#3-core-entity-dictionary-and-keys)

**Recommended decision.** Bind the existing value to the correct contextual owner/profile if normalized description access is required; otherwise classify it explicitly as retained-only. Do not add a description entity.

**Affected constructs.** `health:EventDescription`.

### COV-HR-02 — Health failedSet item scope is absent from normalized errors

**Priority.** HIGH

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/ReadAttempt/properties/error` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/ReadError` · [aws/health/analysis/report.md#12-coverage-and-collection-model](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md#12-coverage-and-collection-model)

**Recommended decision.** Represent per-item event/account failure and partial-success outcome through a typed owned collection or registered response shape; keep transport failures separate.

**Affected constructs.** `health:CollectionItemError`.

### COV-HR-03 — OrganizationHealthAccess registry targets omit its actual owner

**Priority.** LOW

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Workspace/properties/organizationAccess` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/OrganizationAccess` · model/adapter-profiles.json mapping health/OrganizationHealthAccess

**Recommended decision.** Correct registry target metadata to include Workspace and the OrganizationAccess binding. The model already has the appropriate owned value.

**Affected constructs.** `health:OrganizationHealthAccess`.

### COV-HR-04 — Match confidence and lifecycle candidate semantics need an explicit disposition

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/ResourceMatch` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/LifecycleExposure` · [aws/health/analysis/report.md#assessment-and-matching](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/health/analysis/report.md#assessment-and-matching)

**Recommended decision.** Decide and document whether candidate maps to UNKNOWN and whether confidence is resolved from the rule/evidence or exposed as a small owned value. Avoid claiming exact semantic parity until that rule is explicit.

**Affected constructs.** `health:EntityResourceMatch`, `health:LifecycleExposure`.

### COV-HR-05 — Effective target values remain retained rather than normalized

**Priority.** HIGH

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/PolicyContext` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Source/properties/payload` · model/adapter-profiles.json profile aws.resilience-hub.effective-targets/v1 · [aws/resilience-hub/analysis/report.md#reviewed-policy-observation-model](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#reviewed-policy-observation-model)

**Recommended decision.** Keep the already normalized service-scoped observation envelope and exact PolicyContext references. Add a typed owned eight-metric value contract, with units and source-policy provenance, bound through the existing Source/profile or capture where normalized target-value access is required. Reconcile policyType versus ownership-source naming; do not infer a policy ARN or inheritance from a label.

**Affected constructs.** `resilience-hub:EffectiveTarget`, `resilience-hub:EffectivePolicyEvidence`.

### COV-HR-06 — Policy component read-shape validation can be tightened

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/PolicyComponent/properties/targets` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/PolicyComponent/properties/units` · [aws/resilience-hub/analysis/report.md#4-policy-structure-and-inheritance](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#4-policy-structure-and-inheritance)

**Recommended decision.** Retain the existing normalized PolicyComponent owner binding. Document or enforce allowed known metric keys, numeric/integer semantics and unit rules per component family; RPC ResiliencePolicyChanges and RecoveryTargetsInput already provide narrower native edit shapes. This is a validation-completeness finding, not a missing component representation or a reason to create another entity.

**Affected constructs.** `resilience-hub:PolicyComponent`.

### COV-HR-07 — Finding capture assessment correlation lacks a typed basis

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Collection` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/CollectionQuery` · [aws/resilience-hub/analysis/report.md#reviewed-capture-identity-and-detail-coverage](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#reviewed-capture-identity-and-detail-coverage)

**Recommended decision.** Preserve optional same-service related-assessment reference and correlation basis as a small owned capture/query-context value, or explicitly defer this former facade capability.

**Affected constructs.** `resilience-hub:FindingCapture`.

### COV-HR-08 — Recommendation identity is normalized but its content is arbitrary JSON

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Recommendation/properties/suggestion` · [aws/resilience-hub/analysis/report.md#recommendationentity-as-an-owned-value](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#recommendationentity-as-an-owned-value)

**Recommended decision.** Bind ordered suggestedChanges/category content to a typed value when normalized comparison/rendering is required. Retain raw provider evidence for extension and do not create native recommendation IDs.

**Affected constructs.** `resilience-hub:RecommendationEntity`.

### COV-HR-09 — Native topology edge property collections are not normalized

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/GraphEdge` · [aws/resilience-hub/analysis/report.md#10-topology-snapshots-and-graph-meaning](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#10-topology-snapshots-and-graph-meaning)

**Recommended decision.** Define lossless property expansion/grouping or an owned properties collection carrying native type and optional inferred label. Preserve source grouping and same-snapshot endpoints.

**Affected constructs.** `resilience-hub:TopologyEdge`, `resilience-hub:EdgeProperty`.

### COV-HR-10 — Operational event subject linkage remains untyped

**Priority.** HIGH

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Source` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Observation` · [aws/resilience-hub/analysis/report.md#12-temporal-model-for-the-operator-view](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#12-temporal-model-for-the-operator-view)

**Recommended decision.** Bind typed event subjects with role, scoped identity and linkage evidence if the timeline/subject use case is in scope. Native envelope resources alone do not establish those application relationships.

**Affected constructs.** `resilience-hub:EventSubject`.

### COV-HR-11 — Source reference tombstone semantics have no explicit target field

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/EntityRef` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/EntityIdentity` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/SourceIdentity` · [aws/resilience-hub/analysis/report.md#typed-subjects-observation-kinds-and-projection-times](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/resilience-hub/analysis/report.md#typed-subjects-observation-kinds-and-projection-times)

**Recommended decision.** Define the minimal deletion/visibility observation and how historical references resolve it; do not add a version-only or tombstone-only entity by default.

**Affected constructs.** `resilience-hub:EntityRef`.

### COV-HR-12 — Runtime-health and component-posture evidence are retained profiles

**Priority.** MEDIUM

**Evidence.** [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/Source/properties/payload` · [model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `#/$defs/StateDimension` · model/adapter-profiles.json profiles console.monitoring.health/v1 and aws.resilience-hub.posture/v1

**Recommended decision.** Keep retained evidence coverage separate from typed measurement/component-outcome coverage. Select concrete owned observation schemas from product use cases before claiming normalized signal or component parity.

**Affected constructs.** `resilience-hub:HealthObservation`, `resilience-hub:PostureObservation`.

### COV-HR-13 — Native administration and auxiliary configuration are intentional retention boundaries

**Priority.** INFO

**Evidence.** model/adapter-profiles.json · [consolidated-operations-console/CONTEXT_AND_SCOPE.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/CONTEXT_AND_SCOPE.md)

**Recommended decision.** Retain these registered native profiles and declare their product normalization/command deferrals explicitly. They do not each justify a new first-class entity.

**Affected constructs.** `health:EventType`, `health:AggregateSnapshot`, `resilience-hub:DependencyDiscoveryConfig`, `resilience-hub:PermissionModel`, `resilience-hub:InputSourceEntity`, `resilience-hub:ServiceResource`, `resilience-hub:ServiceFunction`, `resilience-hub:ResourceDiscovery`, `resilience-hub:DNS queryRange`.

### DEVOPS-COV-01 — Registry rows and aliases do not count independent entities

**Priority.** METHOD

**Finding.** The registry groups Task/Investigation and generic/journal-specific revisions as aliases, while the source assigns them different native/application or specialization roles. The 52 SDK shapes additionally contain many nested values and wrappers.

**Evidence.** [aws/devops-agent/analysis/annexes/Investigation_Data_Model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/annexes/Investigation_Data_Model.md#3-investigation-aggregate-and-keys) · [aws/devops-agent/analysis/annexes/Investigation_Data_Model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/annexes/Investigation_Data_Model.md#diagram-d02--native-core-with-an-explicit-membership-table) · [aws/devops-agent/analysis/annexes/Investigation_Data_Model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/devops-agent/analysis/annexes/Investigation_Data_Model.md#diagram-d03--every-projection-retains-provenance)

**Recommended decision.** Count the 34 independently extracted class/ER symbols as a fixed declaration benchmark, retain a separate semantic concept catalog, and show native resources, values and wrappers in separate subtotals.

**Affected constructs.** `devops-agent:Task`, `devops-agent:Investigation`, `devops-agent:SourceRevision`, `devops-agent:JournalRecordRevision`.

### DEVOPS-COV-02 — Timeline and richer investigation assertions are retained, not normalized projections

**Priority.** DEFERRED_NORMALIZATION

**Finding.** Named source profiles exist, but each has descriptive typedContent text, not a normalized result schema. Projection.profile is closed to five profiles and only INVESTIGATION_RESULT covers a dedicated DevOps result shape.

**Recommended decision.** Keep retention explicit in the coverage total. Promote a concrete supported use case through an owned typed result and registered Projection profile with exact provenance; do not introduce one new entity or revision entity per assertion kind.

**Affected constructs.** `devops-agent:TimelineItem`, `devops-agent:Finding`, `devops-agent:EvidenceItem`, `devops-agent:Hypothesis`, `devops-agent:RootCauseAssessment`, `devops-agent:MitigationProposal`, `devops-agent:ReviewResult`, `devops-agent:ActionObservation`.

### DEVOPS-COV-03 — Native journal attribution is not an ActorRef binding

**Priority.** MAPPING_OVERCLAIM

**Finding.** The crosswalk labels UserReference as an owned ActorReference, but JournalRecord has no attribution member and ActorRef is the trusted command actor {issuer,subject,kind}. Native userId/userType survives only in raw journal payload.

**Recommended decision.** Correct the crosswalk to retained-only until a distinct owned native-attribution value or explicit reviewed identity mapping is defined. Do not infer an actor when native attribution is absent.

**Affected constructs.** `devops-agent:UserReference`.

### DEVOPS-COV-04 — Graph structure exists but required graph meaning and provenance are incomplete

**Priority.** PARTIAL_NORMALIZATION

**Finding.** The model preserves owned endpoint keys, relationKind and evidence, but lacks an explicit node kind, assertion origin and unresolved-placeholder state. The source also distinguishes more graph-view meanings and provenance/validity facts than the current closed graphKind/claimKind fields.

**Recommended decision.** Add only the owned graph fields needed by supported graph views and retain exact evidence, rather than treating every graph node as a new canonical entity. Test an unresolved placeholder and an operator-asserted causal edge as semantic cases.

**Affected constructs.** `devops-agent:GraphSnapshot`, `devops-agent:GraphNode`, `devops-agent:GraphEdge`.

### DEVOPS-COV-05 — Approval context is pinned but invocation and scope values remain raw

**Priority.** PARTIAL_NORMALIZATION

**Finding.** ApprovalRequest pins source/digest and nativeApprovalId, but interruptId, toolUseId, tool and argumentPins are only described by a source profile. No ApprovalPattern/ApprovalAction owned model value exists. The original source itself warns that approval request content is not a universal native typed entity.

**Recommended decision.** Define and validate the particular observed request profile before dispatch. If typed normalized access is needed, add an owned invocation/scope value with field-presence semantics; preserve request source/digest and keep decision, resume and effect separate.

**Affected constructs.** `devops-agent:ApprovalRequest`, `devops-agent:ApprovalPattern`, `devops-agent:ApprovalAction`.

### DEVOPS-COV-06 — Collector and coverage-policy identity are not retained as typed metadata

**Priority.** PARTIAL_NORMALIZATION

**Finding.** The source CollectionPass contract includes collector version/selection policy and CoverageClaim retains evaluation policy. Current Collection/CollectionQuery/Coverage capture query, window, attempts, dimensions and rationale but no explicit versioned collector/policy binding.

**Recommended decision.** Represent collector/evaluation policy identity as a small owned binding on the appropriate collection/coverage owner, or explicitly defer it. Do not treat free-text rationale as an exact policy version or add policy-version entities.

**Affected constructs.** `devops-agent:CollectionPass`, `devops-agent:CoverageClaim`.

### DEVOPS-COV-07 — Generic artifact storage descriptors do not fully normalize cross-channel artifact references

**Priority.** PARTIAL_NORMALIZATION

**Finding.** Managed artifact locators, asset files and exact evidence locators are typed, but the original ArtifactReference carries channel/record/block/native-ID/optional-asset-resolution semantics and finer unavailability reasons that are not a single current owned value.

**Recommended decision.** Keep the source reference inspectable and state this as partial normalization. Add a channel-aware owned reference only when a concrete inline, A2A or native Asset use case requires it; never equate those identifiers.

**Affected constructs.** `devops-agent:ArtifactReference`.

### DEVOPS-COV-08 — The decision Command receipt does not expose a reconstructable decision input

**Priority.** PARTIAL_NORMALIZATION

**Finding.** The prior decision-attempt entity records action/finalized-pattern hash. The console has a typed DecideApproval request, but its readable Command record exposes only operation/requestDigest/subjects and lifecycle; it has no retained request source or typed decision value.

**Recommended decision.** Specify how an authorized historical audit resolves the exact submitted decision input from the Command. A typed owned intent value or exact request-source reference is sufficient; a standalone version entity is not required.

**Affected constructs.** `devops-agent:DecisionAttempt`.

### DEVOPS-COV-09 — Peripheral native resources are represented only by retained source profiles

**Priority.** INTENTIONAL_SCOPE

**Finding.** Each native resource has an explicit source profile and preserves identity/lifecycle vocabulary, but none has a normalized dedicated model or complete product capability. Homonyms are correctly kept separate from workload Service, resilience Recommendation, console Scenario and Connection.

**Recommended decision.** Count these as retained resource representations, not normalized entity coverage or implemented AWS integration. Promote a resource only after its domain use case and lifecycle authority justify that model/API surface.

**Affected constructs.** `devops-agent:RegisteredService`, `devops-agent:Goal`, `devops-agent:Recommendation`, `devops-agent:Trigger`, `devops-agent:PrivateConnection`.

### DEVOPS-COV-10 — SnapshotProjection crosswalk wording uses obsolete target field names

**Priority.** DOCUMENTATION

**Finding.** The preservation note still says imported legacy renditions are pinned in sourceRevisionIds, although the current Snapshot contract uses members of exact EntityRef(kind,id,version).

**Recommended decision.** Use sourceRevisionIds/projectionRevisionId only when naming old source vocabulary; describe current bindings as Snapshot.members with exact Source or Projection versions.

**Affected constructs.** `devops-agent:SnapshotProjection`.

### DEVOPS-COV-11 — Native Task normalization selects one task discriminator

**Priority.** INTENTIONAL_SCOPE

**Finding.** The pinned native Task catalog includes INVESTIGATION, EVALUATION, RELEASE_READINESS_REVIEW and RELEASE_TESTING. The normalized Investigation contract deliberately describes the INVESTIGATION facet only; other types are retained native task documents.

**Recommended decision.** Keep the Investigation concept normalized and report the broader native Task family as partial. Add another domain facet only for a supported use case, rather than pretending all task types are Investigations.

**Affected constructs.** `devops-agent:Task`, `devops-agent:Investigation`.

### COV-FIS-01 — Retained provider configuration is mislabeled as normalized owned values

**Priority.** MEDIUM

**Finding.** The mapping calls these ownedValue representations, but their named typed classes/properties do not exist. Complete payloads have deliberate Source retention paths. This is not data loss, but it is not normalized contract coverage.

**Evidence.** [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/Experiment` · [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json) — `mappings[sourceService=fis]`

**Recommended decision.** Mark retention-only explicitly with exact profile and JSON member paths. Promote only the small owned values required by current queries; native template/account/lever management can remain deferred.

**Affected constructs.** `fis:TargetSelection`, `fis:ExperimentTargetAccount`, `fis:StopCondition`, `fis:ActionParameterDefinition`, `fis:ActionTargetSlot`, `fis:TemplateAction`, `fis:TemplateTarget`, `fis:TemplateBinding`, `fis:TemplateDependency`, `fis:TemplateTargetAccount`.

### COV-FIS-02 — Resolved memberships lack a typed selector join

**Priority.** HIGH

**Finding.** Action bindings name selectors, but memberships provide only selectionKey, whose fixture value combines selector and resource. No documented typed selector field or canonical encoding makes that relation safely queryable. Empty selectors also have no normalized record.

**Evidence.** [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/TargetMembership` · [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/FISAction/properties/targetBindings` · [consolidated-operations-console/model/examples.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/examples.json) — `Experiment.targetMemberships.selectionKey=workers:instance-1`

**Recommended decision.** Use a small Experiment-owned selector value/key and an explicit selector reference/key on TargetMembership. Keep opaque membership identity separate; retain the complete raw selector and targetInformation in Source. No new entity is needed.

**Affected constructs.** `fis:ResolvedTargetMembership`, `fis:TargetSelection`, `fis:ActionTargetBinding`.

### COV-FIS-03 — Telemetry binding and experiment-assessment linkage are not concretely mapped

**Priority.** HIGH

**Finding.** MetricBinding/MetricBindingReference/CheckDefinition names in the crosswalk do not resolve to concrete value shapes or bound input schemas. ExperimentMetricBinding has no property/relation at all. The metric profile documents fields but does not bind typed samples or query/window/unit semantics. Evaluation can target an Experiment without a Run, so a Run-only generic input is insufficient.

**Evidence.** [aws/fis/analysis/report.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/report.md#9-workload-assessment-model) · [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/StepDefinition/properties/inputBindings` · [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json) — `aws.cloudwatch.metric/v1`

**Recommended decision.** Define narrow versioned profile/input schemas for telemetry queries, samples and criterion parameters; bind them to Source/Scenario or captured evaluation contents. Represent the experiment-to-exact-binding/window association as an owned reference value in captured evaluation context, preserving no-Run assessments.

**Affected constructs.** `fis:MetricBinding`, `fis:ExperimentMetricBinding`, `fis:MetricObservation`, `fis:AssessmentCriterion`.

### COV-FW-01 — Attempt recovery facts have no declared value contract

**Priority.** HIGH

**Finding.** The source specifies once-evaluated/sealed inputs, typed durable checkpoints and structured technical errors. The current attempt tracks identity, status, evidence and external effects but has no checkpoint/resolved-input contract or workflow error value. ReadError belongs to collection and is not a substitute.

**Evidence.** [aws/fis/analysis/workflow/adapters.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/adapters.md#1-common-adapter-contract) · [aws/fis/analysis/workflow/model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/model.md#5-retries-cancellation-and-finalization) · [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/StepAttempt`

**Recommended decision.** Add only the durable owned facts required for exact resume/input/error interpretation, or explicitly defer their normalization and identify their retained typed profile. Keep transient lease/queue implementation details outside the domain model.

**Affected constructs.** `workflow:StepAttempt`, `workflow:ExecutionError`.

### COV-FW-02 — Evidence ownership and production/import roles need an explicit consolidation rule

**Priority.** MEDIUM

**Finding.** Shared Source/Observation and exact references are appropriate, but they do not explicitly preserve the earlier run-owned evidence manifest, producer/import role, or the complete typed adapter Observation result. The mapping prose currently claims those roles remain explicit.

**Evidence.** [aws/fis/analysis/workflow/model.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/model.md#1-entities-ownership-and-identity) · [aws/fis/analysis/workflow/adapters.md](https://github.com/lyrel-dev/frontier-agents/blob/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3/aws/fis/analysis/workflow/adapters.md#1-common-adapter-contract) · [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/StepAttempt/properties/evidenceRefs` · [consolidated-operations-console/MAPPING.md](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/MAPPING.md) — `Evidence / Observation workflow rows`

**Recommended decision.** State how run evidence closure is selected and represent producer/consumer/import provenance as an owned citation value where required. Define registered adapter-result schemas for value/collection/coverage/scope/window. Do not add a duplicate Evidence or Version entity.

**Affected constructs.** `workflow:Evidence`, `workflow:Observation`.

### COV-FW-03 — A normalized profile advertises fields absent from its bound value

**Priority.** LOW

**Finding.** The profile and predecessor describe actual/expected summaries, but the bound CheckResult schema has neither. Core check outcome, evidence and cutoff are normalized, so this does not remove CheckResult concept coverage.

**Evidence.** [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json) — `console.workflow.check-result/v1.observedFields.typedContent` · [consolidated-operations-console/model/schema.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/schema.json) — `$defs/CheckResult`

**Recommended decision.** Say which details remain in retained Source and which are normalized, or add a narrow optional explanatory value if a reviewed use case requires it.

**Affected constructs.** `workflow:CheckResult`.

### COV-FW-04 — Evaluation profile identity wording retains removed revision-resource names

**Priority.** LOW

**Finding.** identityBasis still says projectionRevisionId and inputSnapshotId even though V2 uses a stable Projection identity/version and exact Snapshot reference.

**Evidence.** [consolidated-operations-console/model/adapter-profiles.json](https://github.com/lyrel-dev/frontier-agents/blob/20650d3cf051ad457378704c15f48f77565a611c/consolidated-operations-console/model/adapter-profiles.json) — `console.workflow.evaluation/v1.identityBasis`

**Recommended decision.** Update the profile wording to the current common entity/version/reference contract; do not reintroduce revision entities.

**Affected constructs.** `fis:ResilienceAssessment`.

## 6. Mapping rules and consolidation path

The [20-rule mapping catalog](MAPPING_RULES.md) makes the representation decision explicit. Its central boundary is: a substantive identity/lifecycle can justify an entity; details with one owner become typed values; versions remain on the substantive entity; interpretations need typed profiles; broad native DTOs may remain retained evidence with that limitation stated. Each audited construct links to the applicable rules.

Close gaps in this order:

1. Correct crosswalk/coverage claims so ownedValue or canonicalEntity labels cannot be mistaken for complete normalized support. Preserve the existing raw-source retention paths.
2. Bind already defined but unbound values and add only the missing owner-local structures required by existing use cases. Preserve one version and one write authority per owner.
3. Resolve identity/join, contextual-error, graph/evaluation and historical-capture distinctions before claiming source-model parity. Add semantic fixtures for each promised distinction.
4. Make an explicit scope decision for native administrative breadth and presentation-oriented views: keep them retained-only or add a narrow typed profile when needed.
5. Implement and test adapters, current authorization, persistence, replay and provider reconciliation at the later gates. Model coverage alone is not runtime coverage.

No gap in this audit justifies a version-only entity. The audit leaves the 36-entity schema and 108-operation contract unchanged; it identifies evidence-backed decisions for the next model correction.

## 7. Verification and reproducibility

```bash
python consolidated-operations-console/tools/build_coverage.py
python consolidated-operations-console/tools/build_coverage.py --check
```

The builder independently extracts the 130 source declarations, requires each to resolve exactly once, verifies the selected 52 SDK types, resolves every claimed schema pointer/profile and source heading/symbol, checks all 36 entity version contracts, and regenerates the catalog, counts and rulebook deterministically. It also requires the current model, registry and API contracts to match the pinned target review commit. If a contract changes, review the affected catalog judgments and deliberately update that baseline before claiming current coverage. Semantic judgments are documented review conclusions; pointer existence and a green alias check alone do not prove them.

The source evidence is frozen to the original repository analyses and their 226-file inventory. This audit does not claim all current AWS resources/SDK fields, live-account behavior, migration execution or implemented provider adapters.

## Files

- [coverage/CATALOG.md](coverage/CATALOG.md): every construct, source evidence, mapping proof, status and applicable rules.
- [coverage/catalog.json](coverage/catalog.json): machine-readable merged catalog and fixed diagram benchmark.
- [coverage/report.json](coverage/report.json): counts, source hashes, findings and exact input hashes.
- [MAPPING_RULES.md](MAPPING_RULES.md): human-readable mapping decisions.
- [coverage/mapping-rules.json](coverage/mapping-rules.json): rule catalog source.
