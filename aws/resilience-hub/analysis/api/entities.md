---
id: "resilience-workspace-api-entities"
title: "Entity model to API mapping"
type: "api-design"
service: "aws-resilience-hub"
status: "implemented-mock"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "data-model"
  - "api"
aliases:
  - "Resilience Hub DTO mapping"
related:
  - "index.md"
  - "shapes.md"
  - "aws-mapping.md"
  - "../report.md"
  - "../diagrams/01-business-structure.md"
  - "../diagrams/03-assessments-findings.md"
---

# Entity model to API mapping

The ten requested entity concepts remain the conceptual model. The API uses resource-scoped identities and explicit commands to read or manipulate them. The table below connects each concept to the implemented facade. Exact fields, requiredness and response examples are generated in the [shape reference](shapes.md) and individual [operation notes](index.md).

## The ten requested entities

| Concept | Identity and relationships | Operations | Ownership and interpretation |
| --- | --- | --- | --- |
| `SystemEntity` | `systemArn`; contains journeys and is associated with services | Create/Get/List/Update/DeleteSystem | Native-backed structure; local version and display label supplement provider fields. |
| `UserJourneyEntity` | `(systemArn, userJourneyId)`; optional policy; service membership is derived from service associations | Create/Get/List/Update/DeleteUserJourney | Native-backed journey. A projected service list is not a second writable membership authority. |
| `ServiceEntity` | `serviceArn`; many-to-many system/journey associations; input sources, assessments, findings and dependencies are service-scoped | Create/Get/List/Update/DeleteService; GetServiceStatus | Native-backed configuration plus a separate application status projection. |
| `ResiliencePolicyEntity` | `policyArn`; reusable direct service or journey assignments | Create/Get/List/Update/DeletePolicy | Availability SLO, data recovery, Multi-AZ and Multi-Region components. Latency/performance is monitoring evidence or a future local objective, not an invented native policy component. |
| `AssessmentEntity` | `(serviceArn, assessmentId)` | Start/Get/ListFailureModeAssessment(s) | Start and list are native-backed. Get is a composed lookup. Completion is separate from the resulting posture. |
| `FindingEntity` | `(serviceArn, findingId)`; observations record current summary/detail evidence | Get/List/UpdateFailureModeFinding(s) | A finding is service-scoped. Its disposition is mutable; provider severity and suggested changes are observed evidence. No mandatory assessment foreign key is introduced. |
| `RecommendationEntity` | Local `recommendationId` anchored to a finding detail observation and recommendation group/ordinal | GetRecommendation; ListRecommendations; UpdateRecommendationEnrichment | Native suggested-change content is normalized into an immutable observation-scoped record. Title, estimate, complexity and local workflow are enrichment. |
| `DependencyDiscoveryConfig` | Embedded in a service response; no standalone resource ID | GetService; ListServices; UpdateService | The write request is `dependencyDiscovery: ENABLED or DISABLED`. Returned status, eligible count, message and update time are observations. |
| `DependencyEntity` | `(serviceArn, dependencyId)` | GetDependency; ListDependencies; UpdateDependency; UpdateDependencyGovernance | Native classification updates and local allow/deny governance have distinct operations and provenance. |
| `TopologyEntity` | Local `topologyId`; service scope; nodes and edges belong to one capture | Capture/Get/ListTopologySnapshot(s) | Product capture of resource and edge observations. Resource count and collector coverage describe that capture, not guaranteed complete AWS visibility. |

The native basis and exact differences for every operation appear in [AWS mapping](aws-mapping.md). The report's source-backed analysis remains authoritative for the conceptual relationships: [business structure](../diagrams/01-business-structure.md), [policy context](../diagrams/02-policy-context.md), [assessments and findings](../diagrams/03-assessments-findings.md), [dependencies and topology](../diagrams/04-dependencies-topology.md), and [events and observations](../diagrams/05-events-observations.md).

The implemented `SystemEntity` DTO covers ARN-addressable systems in the complete mock workspace. Native limited-visibility system summaries can expose a system ID without an ARN. A production cross-account adapter therefore needs a partial reference/summary representation or explicit coverage result alongside this detail DTO. It must preserve the unresolved reference rather than inventing an ARN or calling `GetSystem` with a system ID. See the report's [business structure](../diagrams/01-business-structure.md) and the [native SystemSummary shape](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_SystemSummary.html).

## Supporting entities exposed by this API

| Supporting concept | Purpose | API surface |
| --- | --- | --- |
| Input source | Specifies how a service's resources are discovered; scoped to one service | CreateInputSource, ListInputSources, DeleteInputSource |
| Health observation | Immutable measured evidence with source, observation time and expiry | PutHealthObservation; projected through GetServiceStatus |
| Event envelope | Keeps delivery identity, source time, receipt time and linkage; does not replace an authoritative entity read | IngestEvent, ListEvents |
| Service status projection | Presents assessment execution, architecture posture, runtime health, discovery coverage and attention separately | GetServiceStatus |
| Workspace summary | Deduplicated counts for a selected system/journey service set, with evidence and rule context | GetWorkspaceSummary |
| Local revision and tombstone | Supports concurrent-edit detection and history retention in the mock store | Mutation responses and runtime history |

## Relationship invariants

1. A service can be associated with several systems and with several journeys within each associated system. Each selected journey must belong to the system in the same association. Updating service associations is the membership command; a journey update cannot independently overwrite a service list.
2. Shared services are deduplicated by service ARN before computing a system, journey or workspace denominator. Findings are deduplicated by `(serviceArn, findingId)`. An affected shared service is counted once even if it has several attention reasons.
3. A finding observation can record a summary, a hydrated detail or an incomplete refresh. Recommendation identity points to detail evidence. Changing an enrichment does not mutate the source observation or claim a provider recommendation ID.
4. An assessment ID on a local capture is a labelled correlation. Current findings can change independently of a run. Assessment cost is the cost of execution; recommendation cost is a local estimate of a proposed change.
5. A topology edge cannot cross snapshot identities. An unresolved node remains an explicit stub. Repeated captures preserve the observation times of copied data.
6. Event receipt order does not define the order of evidence. Older health observations remain in history and cannot roll the current projection backward.

These are implementation and modeling decisions. Their native evidence is documented in the [reviewed report](../report.md); the local behavior is exercised by the RPC and domain tests listed in the [validation record](../validation.md).

## Provider fields and product fields

The facade separates concerns by explicit DTO shape and operation provenance. In particular:

- Provider `name` remains the provider identifier for systems, services and policies. `displayName` is the user-facing product label. A display-label edit must not be translated into an unsupported AWS resource rename.
- The permission structure uses `crossAccountRoles[].crossAccountRoleArn`. Authorization to use a role is not established merely by receiving its ARN in a request.
- Native achievability uses `availabilitySlo`, `dataRecoveryTimeBetweenBackups`, `multiAzRtoRpo` and `multiRegionRtoRpo`. The existing browser model's shorter component keys are presentation normalization; the RPC DTO maps them deliberately.
- Discovery status and discovery eligibility describe the evidence pipeline. Runtime health comes from monitoring. Policy achievability comes from an assessment-derived provider observation. The three dimensions can disagree without the data being invalid.
- A local version, current UI edit time or observed policy hash is not an AWS evaluated policy revision. Provenance and source observation times survive normalization.

The [shared schemas](shapes.md) specify which fields are required, nullable or optional. Operation inputs are intentionally narrower than output entities, making writable ownership reviewable before a command is submitted.
