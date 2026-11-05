---
id: "aws-resilience-hub-rpc-provider-mapping"
title: "AWS Resilience Hub — Native API and workspace RPC mapping"
type: "api-mapping"
service: "aws-resilience-hub"
status: "reviewed-provider-contract"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "api-design"
  - "rpc"
  - "provider-boundary"
aliases:
  - "Resilience Hub native API mapping"
  - "Resilience workspace provider boundary"
related:
  - "index.md"
  - "../report.md"
  - "../review.md"
  - "../diagrams/01-business-structure.md"
  - "../diagrams/03-assessments-findings.md"
  - "../diagrams/04-dependencies-topology.md"
  - "../diagrams/05-events-observations.md"
---

# AWS Resilience Hub — Native API and workspace RPC mapping

**Reviewed on 5 November 2026.** This note maps the proposed operator-facing API to the current next-generation AWS Resilience Hub contracts. It describes integration boundaries and documented provider behavior. It does not certify an AWS connection or production implementation. Read it with the [API index](index.md), [data model](../report.md) and [review decisions](../review.md).

## 1. Protocol and ownership

`ResilienceWorkspace_20261105` is the proposed application's API namespace. Its `POST /`, `X-Amz-Target: ResilienceWorkspace_20261105.OperationName` and `application/x-amz-json-1.1` envelope are application design choices. AWS Resilience Hub v2 instead documents operation-specific paths such as `POST /v2/create-service` and `GET /v2/get-service?serviceArn=...`, with `application/json` responses. An adapter translates between those contracts; the namespace does not identify an AWS service endpoint. [P01] [P02]

The provider model is the next-generation `resiliencehubv2` client. The operation inventory includes additional testing, reporting, assertion, tagging and service-function features outside this initial operator workspace. The 44-operation workspace catalogue is a product scope, not the complete AWS operation catalogue. [P00]

| Mapping type | Meaning | Provider boundary |
| --- | --- | --- |
| `NATIVE_ADAPTER` | A corresponding native operation exists. | The adapter still translates transport, local metadata, field selection and response envelopes. A shared operation name does not promise wire compatibility. |
| `COMPOSED_READ` | The application reads provider records and/or stored observations to answer a richer query. | No single native operation returns that complete view. Collection, hydration, history and aggregation belong to the application. |
| `LOCAL` | The application manages its own record or command. | There is no native operation with that meaning. Provider reads may supply evidence for a local snapshot or enrichment. |
| `INGEST` | A trusted integration delivers an observation or event to the application. | This is an inbound application boundary, not an AWS Resilience Hub mutation. |

## 2. Operation mapping

The mapping below identifies the intended source of each operation. Provider-side calls shown for composed or local operations are acquisition strategies, not claims that a particular runtime makes those calls. Native operation names are verified against the current official client inventory. [P00]

### Systems, journeys, services and policies

| # | Workspace operation | Type | Native operation or source | Boundary |
| --- | --- | --- | --- | --- |
| 1 | `CreateSystem` | `NATIVE_ADAPTER` | `CreateSystem` | Local display metadata and revisions require separate storage. [P03] |
| 2 | `GetSystem` | `NATIVE_ADAPTER` | `GetSystem` | Native read requires `systemArn`; `systemId` is returned metadata. [P04] |
| 3 | `ListSystems` | `NATIVE_ADAPTER` | `ListSystems` | Native `systemSummaries`; detail hydration is additional work. [P05] |
| 4 | `UpdateSystem` | `NATIVE_ADAPTER` | `UpdateSystem` | Native fields are description and sharing configuration, not name. [P06] |
| 5 | `DeleteSystem` | `NATIVE_ADAPTER` | `DeleteSystem` | Local reference guards are additional rules. [P07] |
| 6 | `CreateUserJourney` | `NATIVE_ADAPTER` | `CreateUserJourney` | Parent system is request scope; membership is separate. [P08] |
| 7 | `GetUserJourney` | `NATIVE_ADAPTER` | `GetUserJourney` | Preserve the parent system scope in the local entity. [P00] [P09] |
| 8 | `ListUserJourneys` | `NATIVE_ADAPTER` | `ListUserJourneys` | Summaries omit policy and description. [P10] |
| 9 | `UpdateUserJourney` | `NATIVE_ADAPTER` | `UpdateUserJourney` | Name, description and policy are native; service membership is not. [P09] |
| 10 | `DeleteUserJourney` | `NATIVE_ADAPTER` | `DeleteUserJourney` | Requires both `systemArn` and `userJourneyId`. [P11] |
| 11 | `CreateService` | `NATIVE_ADAPTER` | `CreateService` | Permission model and Regions are required provider configuration. [P01] |
| 12 | `GetService` | `NATIVE_ADAPTER` | `GetService` | Input sources and monitoring health require separate reads. [P02] |
| 13 | `ListServices` | `NATIVE_ADAPTER` | `ListServices` | Summaries include dependency discovery but omit several detail fields. [P12] |
| 14 | `UpdateService` | `NATIVE_ADAPTER` | `UpdateService` | Owns system/journey associations and dependency-discovery configuration. [P13] |
| 15 | `DeleteService` | `NATIVE_ADAPTER` | `DeleteService` | Historical-observation retention is a local decision. [P14] |
| 16 | `CreatePolicy` | `NATIVE_ADAPTER` | `CreatePolicy` | Four native objective components; performance objectives remain local. [P15] |
| 17 | `GetPolicy` | `NATIVE_ADAPTER` | `GetPolicy` | A local revision is not an AWS-assessed policy revision. [P00] [P16] |
| 18 | `ListPolicies` | `NATIVE_ADAPTER` | `ListPolicies` | Native `policySummaries`; local enrichment is separate. [P17] |
| 19 | `UpdatePolicy` | `NATIVE_ADAPTER` | `UpdatePolicy` | Use the current SDK shape for `sharingEnabled`; see discrepancy below. [P18] [P19] |
| 20 | `DeletePolicy` | `NATIVE_ADAPTER` | `DeletePolicy` | Native request contains only the policy ARN. [P20] |

### Assessment, findings, recommendations and input sources

| # | Workspace operation | Type | Native operation or source | Boundary |
| --- | --- | --- | --- | --- |
| 21 | `CreateInputSource` | `NATIVE_ADAPTER` | `CreateInputSource` | Native response returns identifiers, not a full hydrated entity. [P21] |
| 22 | `ListInputSources` | `NATIVE_ADAPTER` | `ListInputSources` | Native summaries flatten the chosen configuration member. [P22] |
| 23 | `DeleteInputSource` | `NATIVE_ADAPTER` | `DeleteInputSource` | Requires service ARN and input-source ID. [P23] |
| 24 | `StartFailureModeAssessment` | `NATIVE_ADAPTER` | `StartFailureModeAssessment` | Starts an asynchronous provider workflow; start acceptance is not success. [P24] |
| 25 | `GetFailureModeAssessment` | `COMPOSED_READ` | `ListFailureModeAssessments` or retained assessment observation | No native operation with this name; match within service scope. [P00] [P25] |
| 26 | `ListFailureModeAssessments` | `NATIVE_ADAPTER` | `ListFailureModeAssessments` | Native `assessmentSummaries`; local historical enrichment is additional. [P25] |
| 27 | `GetFailureModeFinding` | `NATIVE_ADAPTER` | `GetFailureModeFinding` | Service-scoped identity; native body exposes no assessment foreign key. [P26] |
| 28 | `ListFailureModeFindings` | `NATIVE_ADAPTER` | `ListFailureModeFindings` | Native `findingsSummary`; no native assessment-ID filter. [P27] |
| 29 | `UpdateFailureModeFinding` | `NATIVE_ADAPTER` | `UpdateFailureModeFinding` | Native mutation requires status; a comment alone is insufficient. [P28] |
| 30 | `GetRecommendation` | `COMPOSED_READ` | `GetFailureModeFinding` plus local normalization/enrichment | No native recommendation identity or standalone get. [P00] [P26] |
| 31 | `ListRecommendations` | `COMPOSED_READ` | Finding details plus local normalization/enrichment | Three nested recommendation groups are normalized locally. [P26] |
| 32 | `UpdateRecommendationEnrichment` | `LOCAL` | No equivalent | Local name, description, cost, complexity or planning metadata cannot be written to the native recommendation shapes. [P26] |

### Dependencies, topology and operational views

| # | Workspace operation | Type | Native operation or source | Boundary |
| --- | --- | --- | --- | --- |
| 33 | `GetDependency` | `COMPOSED_READ` | `ListDependencies` or retained dependency observation | No native `GetDependency`; `GetDependencyInsights` is a different operation. [P00] |
| 34 | `ListDependencies` | `NATIVE_ADAPTER` | `ListDependencies` | Service-scoped provider dependency inventory. [P00] |
| 35 | `UpdateDependency` | `NATIVE_ADAPTER` | `UpdateDependency` | Native write changes criticality/comment, not an allowed-status decision. [P29] |
| 36 | `UpdateDependencyGovernance` | `LOCAL` | No equivalent | Allowed status and governance rationale are product-owned. [P29] |
| 37 | `GetTopologySnapshot` | `COMPOSED_READ` | Retained local topology capture | No native topology-ID lookup; captures originate in resource and edge reads. [P00] [P30] [P31] |
| 38 | `ListTopologySnapshots` | `COMPOSED_READ` | Retained local topology captures | No native topology history collection. [P00] |
| 39 | `CaptureTopologySnapshot` | `LOCAL` | `ListResources` + `ListServiceTopologyEdges` as acquisition inputs | Snapshot ID, capture time, completeness and count are local; capture is not an atomic AWS snapshot. [P30] [P31] |
| 40 | `GetServiceStatus` | `COMPOSED_READ` | Service, assessments, findings, discovery and health observations | Distinct dimensions remain separately evidenced. [P02] [P25] [P27] |
| 41 | `GetWorkspaceSummary` | `COMPOSED_READ` | Scoped entity observations and status projections | Workspace aggregation and coverage rules are local. |
| 42 | `ListEvents` | `COMPOSED_READ` | Local journal; native service/system/policy event collections and EventBridge may supply inputs | No unified native operation with this name. [P00] [P32] |
| 43 | `PutHealthObservation` | `INGEST` | No equivalent | External monitoring evidence, with source and observation time. |
| 44 | `IngestEvent` | `INGEST` | No equivalent | Trusted event receipt and deduplication; not an AWS write. [P32] |

## 3. Native create, update and delete fields

The following table records provider input fields, independently of any smaller facade subset. Required fields are **bold**. A native operation's optional field is not automatically a supported facade field. SDK timestamp objects and native JSON timestamp numbers also require explicit serialization at the facade boundary.

| Entity | Native create | Native update | Native delete and result |
| --- | --- | --- | --- |
| System | **`name`**; `description`, `sharingEnabled`, `kmsKeyId`, `tags`, `clientToken` | **`systemArn`**; `description`, `sharingEnabled` | `{systemArn}` → `{systemArn}`. [P03] [P06] [P07] |
| User journey | **`systemArn`, `name`**; `description`, `policyArn`, `clientToken` | **`systemArn`, `userJourneyId`**; `name`, `description`, `policyArn` | `{systemArn,userJourneyId}` → `{userJourneyId}`. [P08] [P09] [P11] |
| Service | **`name`, `permissionModel`, `regions`**; `associatedSystems`, `description`, `policyArn`, `dependencyDiscovery`, `reportConfiguration`, `devOpsAgentConfiguration`, `kmsKeyId`, `tags`, `clientToken` | **`serviceArn`**; `description`, `associatedSystems`, `policyArn`, `regions`, `permissionModel`, `dependencyDiscovery`, `reportConfiguration`, `devOpsAgentConfiguration` | `{serviceArn}` → `{serviceArn}`. [P01] [P13] [P14] |
| Policy | **`name`**; `description`, `availabilitySlo`, `multiAz`, `multiRegion`, `dataRecovery`, `sharingEnabled`, `kmsKeyId`, `tags`, `clientToken` | **`policyArn`**; `description`, `availabilitySlo`, `multiAz`, `multiRegion`, `dataRecovery`, `sharingEnabled` | `{policyArn}` → `{policyArn}`. [P15] [P18] [P20] |
| Input source | **`serviceArn`, `resourceConfiguration`**; `clientToken` | No native update operation | `{serviceArn,inputSourceId}` → same identifiers. Create also returns only these identifiers. [P21] [P23] |

Tags have dedicated native operations in the client inventory. Their absence from an entity's update input does not imply that provider tags can never change. `kmsKeyId` likewise must not be added to an update input merely because it appears on the read entity. [P00] [P06] [P13] [P18]

### Resource names and display names

System, service and policy `name` is a provider resource name used in an ARN. Service and policy create schemas enforce 2–60 characters with pattern `[A-Za-z0-9][A-Za-z0-9_\-]{1,59}`; the System SDK describes the same no-space resource-name role. The initial facade can apply that shared provider-name constraint, while treating any human-friendly `displayName` as local metadata. [P01] [P03] [P15]

Journey `name` is an entity label, permits spaces and has pattern `[A-Za-z0-9][A-Za-z0-9 _\-]{1,59}`. `UpdateUserJourney` supports renaming. `UpdateSystem`, `UpdateService` and `UpdatePolicy` do not expose `name`; local display-name editing must not be represented as a provider rename. [P08] [P09] [P06] [P13] [P18]

### Membership and parent scope

A native service can contain multiple `associatedSystems` entries, each with `systemArn`, optional `systemName` and `userJourneyIds`. Journey service lists should be derived from these associations. A user-journey create/update result omits its parent `systemArn`; preserve the validated request scope rather than inventing an unscoped global journey key. `GetSystem` requires the ARN even though the returned entity also has a `systemId`. [P01] [P04] [P08] [P09]

### Input-source union

`resourceConfiguration` accepts exactly one of `resourceTags`, `cfnStackArn`, `tfStateFileUrl`, `eks` and `designFileS3Url`. EKS requires `clusterArn` and `namespaces`; `labelSelector` is optional. A native `type` discriminator is not a create-input member. `MONITORING` appears in the read/filter enum but has no corresponding create union member. No native update operation was found; changing source configuration therefore needs an explicit replacement workflow or a clearly local command. [P21] [P22] [P33] [P00]

## 4. Exact field corrections and enrichment boundaries

| Concern | Verified provider contract | Adapter or product decision |
| --- | --- | --- |
| Permission model | `invokerRoleName` is required when a permission model is supplied. Each cross-account role uses **`crossAccountRoleArn`**, with optional `externalId`. The same key appears in requests and responses. | Do not forward the earlier fixture key `arn`. [P01] [P02] [P13] |
| Achievability | `availabilitySlo`, `multiAzRtoRpo`, `multiRegionRtoRpo`, `dataRecoveryTimeBetweenBackups`. | A UI component key such as `multiAz` needs an explicit mapping; it is not the native achievability field. [P02] [P25] |
| Resource discovery | `status`, `lastRunAt`, `errorCode`, **`errorMessage`**. | Do not send or imply a native `error` field. [P02] |
| Dependency discovery | Read object contains `status`, `eligibleResourceCount`, `message`, `updatedAt`; service writes accept the configuration string `ENABLED` or `DISABLED`. | `INITIALIZING` is provider-managed; returned counters/timestamps are not write inputs. [P01] [P02] [P13] |
| Native policy components | Top-level `availabilitySlo`, `multiAz`, `multiRegion`, `dataRecovery`; no `components` wrapper. | A `components` wrapper in the abstract model must be unpacked by the adapter. Performance/latency/error objectives are local extensions. [P15] [P18] |
| Recommendations | Finding detail contains three recommendation groups with `suggestedChanges`. | Stable recommendation IDs, names, descriptions, cost and complexity are local normalization/enrichment. [P26] |
| Dependency write | `serviceArn`, `dependencyId`, optional `criticality` and `comment`; response is a flat dependency record. | A `{dependency: ...}` response wrapper and allowed-status governance are facade-owned. [P29] |
| Finding write | `serviceArn`, `findingId` and `status` are required; `comment` is optional. | No native severity edit, recommendation edit or assessment association can be inferred from this operation. [P28] |

The four policy components are optional in the create shape; `name` is the only required top-level field. If the workspace requires at least one usable objective, that is a product validation. Recovery targets use minutes; availability is a percentage. A local policy revision or stored target snapshot must not be described as the exact provider revision used by an assessment unless supporting evidence exists. [P15] [P18] [P25]

### Deliberate mock subsets and unknown values

The executable facade uses the provider's objective and configuration field names while applying a bounded local input surface. Its Terraform and design-file source URLs currently accept only `s3://` URIs; AWS also documents virtual-hosted S3 URLs. Recovery-minute fields have a local upper bound of 5,256,000, and finding/dependency comments have a local 2,048-character cap. These are mock-contract limits, not claims about AWS limits. The native-compatible create/update description limits are 500 characters for systems/journeys and 615 for services/policies; the facade's `clientToken` is limited to 63 characters. [P01] [P06] [P08] [P15] [P33]

Native achievability values in the reviewed shape are `ACHIEVABLE` and `NOT_ACHIEVABLE`. The facade also permits explicit `null` or local `UNKNOWN` to preserve missing observations; those values do not invent a third provider assessment result. An unresolved topology endpoint may similarly have `null` Region or account metadata. Keep those gaps visible rather than inferring a known provider location. See the generated [shape reference](shapes.md) for exact local requiredness and nullability. [P02] [P25] [P31]

### Documentation discrepancy: policy sharing

The direct `UpdatePolicy` API-reference page retrieved for this review omits `sharingEnabled`. The current official Botocore `update_policy` page includes it, along with `sharingEnabled` and `organizationId` in the result. This mapping uses the current SDK input for that field. Pin the SDK/model version used by a real adapter and re-check this difference during integration; do not silently claim both references have identical schemas. [P18] [P19]

## 5. Summary collections and detail hydration

| Native collection | Returned collection member | Additional detail or scope to preserve |
| --- | --- | --- |
| `ListSystems` | `systemSummaries` | Summary counts and identity are not a full `System`; use `GetSystem` when authorized and addressable. [P05] [P04] |
| `ListUserJourneys` | `userJourneySummaries` | Summary has ID, name and timestamps; policy/description need detail. Retain `systemArn` scope. [P10] |
| `ListServices` | `serviceSummaries` | Contains achievability and dependency discovery, but omits permission model, input sources and resource-discovery detail. [P12] [P02] |
| `ListPolicies` | `policySummaries` | Objective components appear in summaries; full policy metadata still differs. [P17] [P16] |
| `ListInputSources` | `inputSourceSummaries` | Configuration is flattened onto the summary; retain service scope. [P22] |
| `ListFailureModeAssessments` | `assessmentSummaries` | A composed get matches `assessmentId` within `serviceArn`; native list has no assessment-ID parameter. [P25] |
| `ListFailureModeFindings` | **`findingsSummary`** | Recommendation content requires finding detail. There is no native assessment-ID filter. [P27] [P26] |

A missing detail field on a list response is not evidence that the field was deleted. Hydrate deliberately and record partial coverage. Do not overwrite a known detail with absence from a summary. A local `items` list envelope is acceptable only as a documented normalization of these provider result members.

## 6. Mutation and consistency rules owned by the facade

### Null, omission and arrays

The reviewed native update inputs do not define a general patch language, `fieldsToClear` field or universal “JSON null means clear” rule. The facade must distinguish omitted input from an explicit local clear, and implement only clears supported by its provider adapter. Rejecting unsupported clears is preferable to silently omitting them and claiming success. Do not generalize the specific DevOps Agent disconnection behavior into a universal clearing mechanism. [P06] [P09] [P13] [P18]

If a facade operation treats arrays as complete replacement, document that rule at that operation. In particular, changing one service-to-journey membership must preserve the other validated associations when constructing `associatedSystems`. An empty list must not be interpreted as “no change” merely because it is falsy or has no members. These are application patch semantics; the provider's structured input does not itself establish a universal array merge contract.

### Delete guards and history

The delete request/response schemas above do not specify all cascade or referential-conflict behavior. Blocking a system delete while journeys exist, blocking a policy delete while local bindings remain, and preserving observations after a service disappears are conservative application policies. Label them as such, and keep provider conflict responses distinct from local guard failures. Do not fabricate a native cascade or a native guarantee that deleting a parent retains every child. [P07] [P11] [P14] [P20]

### Idempotency and optimistic concurrency

The reviewed create operations and assessment-start operation expose `clientToken`; the SDK documents automatic token population when omitted. Their operation pages do not specify a retention interval, exact scope or payload-mismatch guarantee. A durable facade should define those guarantees independently, bind a token to caller/operation/target and canonical request, and retain the result needed for safe replay. A local mock's in-memory replay behavior must not be presented as AWS's retention contract. [P03] [P21] [P24] [P33]

The reviewed update/delete schemas do not expose a generic expected-revision condition. Any `expectedRevision`, local entity revision or conflict check is facade-owned and cannot by itself prevent an out-of-band AWS edit. A production adapter needs read/reconcile behavior and must describe the remaining race. Native tokens must also not be invented for operations that lack a `clientToken` member. [P06] [P09] [P13] [P18]

### Pagination and collection consistency

The reviewed native lists generally accept `maxResults` from 1 to 100 and an opaque non-whitespace `nextToken` of 1–2000 characters. The operation references do not promise an immutable snapshot across pages, a fixed default page size or a token lifetime. Preserve the provider token as opaque data and consume all required pages before asserting complete coverage. [P05] [P12] [P17] [P22] [P25] [P27]

A facade cursor may have stronger operation/filter/revision binding and expiry rules. Those guarantees are local; a token that indexes an in-memory array is not an AWS pagination token. A topology capture should record the collection window and incomplete reads: paginating resources and topology edges is not a provider transaction. `ListResources` defaults to billable resources, so capture scope must explicitly account for that filter. [P30] [P31]

## 7. Error and event boundaries

Native create operations document `ServiceQuotaExceededException` with **HTTP 402**. Keep it distinct from throttling and from any local rate-limit decision. `ThrottlingException` is separately present in the official client and on assessment start. The native operation references also identify validation 400, access 403, missing resource 404, conflict 409 and internal failure 500 where applicable; not every operation lists every error. If the workspace chooses a different status or envelope, document the translation rather than describing it as the native wire result. [P15] [P21] [P00] [P24]

Native EventBridge notifications exist for assessment completion/failure/queueing, finding disposition and new dependency discovery. Delivery is best effort and may be delayed or missed. `IngestEvent` therefore belongs to the trusted application integration boundary; receiving an event is not proof that every affected detail has been refreshed. Reconciliation reads, event identity, ordering decisions and freshness indicators remain necessary application responsibilities. [P32]

`PutHealthObservation`, topology history, recommendation enrichment, dependency allowed status and workspace aggregates are local model features. Keep operational health, assessment execution state, resilience achievability, finding disposition, discovery progress and observation freshness separate. A successful assessment start, a resolved finding or enabled discovery does not alone establish current workload health.

## 8. Sources

All sources are official AWS documentation, reviewed on 2026-11-05. Operation availability follows the current client inventory; SDK fallbacks are used where an individual API-reference page was inaccessible or older.

| ID | Source |
| --- | --- |
| P00 | [ResilienceHubV2 client operation inventory](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2.html) |
| P01 | [CreateService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html) |
| P02 | [GetService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetService.html) |
| P03 | [CreateSystem — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/create_system.html) |
| P04 | [GetSystem — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/get_system.html) |
| P05 | [ListSystems](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListSystems.html) |
| P06 | [UpdateSystem](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UpdateSystem.html) |
| P07 | [DeleteSystem — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/delete_system.html) |
| P08 | [CreateUserJourney](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateUserJourney.html) |
| P09 | [UpdateUserJourney — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_user_journey.html) |
| P10 | [ListUserJourneys — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/list_user_journeys.html) |
| P11 | [DeleteUserJourney — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/delete_user_journey.html) |
| P12 | [ListServices](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListServices.html) |
| P13 | [UpdateService — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_service.html) |
| P14 | [DeleteService — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/delete_service.html) |
| P15 | [CreatePolicy](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreatePolicy.html) |
| P16 | [GetPolicy](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetPolicy.html) |
| P17 | [ListPolicies](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListPolicies.html) |
| P18 | [UpdatePolicy — current official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_policy.html) |
| P19 | [UpdatePolicy — API reference discrepancy](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UpdatePolicy.html) |
| P20 | [DeletePolicy](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_DeletePolicy.html) |
| P21 | [CreateInputSource](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateInputSource.html) |
| P22 | [ListInputSources](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListInputSources.html) |
| P23 | [DeleteInputSource](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_DeleteInputSource.html) |
| P24 | [StartFailureModeAssessment — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/start_failure_mode_assessment.html) |
| P25 | [ListFailureModeAssessments](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeAssessments.html) |
| P26 | [GetFailureModeFinding](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetFailureModeFinding.html) |
| P27 | [ListFailureModeFindings](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeFindings.html) |
| P28 | [UpdateFailureModeFinding — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_failure_mode_finding.html) |
| P29 | [UpdateDependency — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_dependency.html) |
| P30 | [ListResources](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListResources.html) |
| P31 | [ListServiceTopologyEdges](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListServiceTopologyEdges.html) |
| P32 | [EventBridge notification types and delivery](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-notifications.html) |
| P33 | [CreateInputSource union details — official SDK](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/create_input_source.html) |

[P00]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2.html
[P01]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html
[P02]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetService.html
[P03]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/create_system.html
[P04]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/get_system.html
[P05]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListSystems.html
[P06]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UpdateSystem.html
[P07]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/delete_system.html
[P08]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateUserJourney.html
[P09]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_user_journey.html
[P10]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/list_user_journeys.html
[P11]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/delete_user_journey.html
[P12]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListServices.html
[P13]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_service.html
[P14]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/delete_service.html
[P15]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreatePolicy.html
[P16]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetPolicy.html
[P17]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListPolicies.html
[P18]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_policy.html
[P19]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UpdatePolicy.html
[P20]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_DeletePolicy.html
[P21]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateInputSource.html
[P22]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListInputSources.html
[P23]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_DeleteInputSource.html
[P24]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/start_failure_mode_assessment.html
[P25]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeAssessments.html
[P26]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetFailureModeFinding.html
[P27]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeFindings.html
[P28]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_failure_mode_finding.html
[P29]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_dependency.html
[P30]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListResources.html
[P31]: https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListServiceTopologyEdges.html
[P32]: https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-notifications.html
[P33]: https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/create_input_source.html

## Related notes

- [[api/index|Workspace API reference]]
- [[report|Abstract entity model]]
- [[review|Model review decisions]]
- [[diagrams/01-business-structure|Business structure ER diagram]]
- [[diagrams/03-assessments-findings|Assessment and finding ER diagram]]
- [[diagrams/04-dependencies-topology|Dependency and topology ER diagram]]
- [[diagrams/05-events-observations|Event and observation ER diagram]]
