# Source model consolidation map

**Source baseline:** `main` at [`d926a81`](https://github.com/lyrel-dev/frontier-agents/tree/d926a81c584b6b69f41bfb9641532c4f8f2d7cb3). The frozen [inventory](INVENTORY.md) covers all requested service-analysis paths. **Target:** contract revision 2, with 36 uniformly versioned entities.

This crosswalk preserves the source vocabulary as aliases. Older names such as SourceRevision, ScenarioRevision and AssetVersion remain in the **source** column so the previous work stays traceable. Their presence does not introduce those classes in the current model. The machine-readable source of the tables is [model/adapter-profiles.json](model/adapter-profiles.json).

## Representation rules

| Disposition | Meaning |
| --- | --- |
| `canonicalEntity` | A substantive concept among the 36 entities owns identity and lifecycle. Every entity carries version, createdAt and updatedAt. |
| `ownedValue` | A typed value/reference belongs to an entity version. It has no independent entity history or CRUD lifecycle. |
| `projectionProfile` | One of five typed Projection results with exact subject/input versions, rule and coverage. |
| `retainedAdapterDto` | A named provider or earlier application payload retained through a Source profile. Management/UI normalization can remain deferred while evidence is inspectable. |
| Deferred native mutation | An explicit future adapter command boundary, separate from a read DTO or a local edit. |

Exact references carry `{kind,id,version}`. Navigation that deliberately follows a logical identity uses EntityIdentity. Source.profile binds to the descriptor's full profileId and profileVersion; profile version is not entity version. Native shapes, fields and operation names retain their source spelling.

The registry has 174 mapping rows, 340 service/concept aliases and 65 profiles. Current target names and semantics are updated; source aliases, source paths and provider vocabulary are preserved.

## Canonical entities

| Module | Entities |
| --- | --- |
| foundation | `Workspace`, `Connection`, `Resource`, `Collection`, `ReadAttempt`, `Source`, `Observation`, `Projection`, `Snapshot`, `WorkItem`, `Command` |
| workload | `System`, `UserJourney`, `Service`, `Dependency` |
| health | `HealthEvent`, `EventContext`, `EntityImpact`, `Communication`, `LifecycleEntry`, `ComponentDeployment` |
| resilience | `ResiliencePolicy`, `ResilienceAssessment`, `Finding`, `Recommendation` |
| investigation | `AgentSpace`, `Investigation`, `Execution`, `JournalRecord`, `ApprovalRequest`, `Asset` |
| workflow | `Scenario`, `Run`, `StepRun`, `StepAttempt` |
| fis | `Experiment` |

## Changes from the first consolidation

| Earlier representation | Revision 2 representation | Preservation rule |
| --- | --- | --- |
| SourceRevision with a new ID per payload | Source with stable sourceId and version | Identity excludes content digest. Repeated observation reuses unchanged content; changed content publishes the next version. |
| ProjectionRevision with a rendition ID | Projection with stable projectionId and version | Inputs, rule and value remain pinned on each entity version. |
| Scenario plus ScenarioRevision | Scenario with DRAFT/PUBLISHED/ARCHIVED versions | Run pins an exact published version; current archive policy is checked separately. |
| ID-only evidence references | EntityRef/EvidenceRef with version | Missing or unavailable historical versions cannot resolve to current state. |
| projectionVersion and nested overlay versions | Universal owning-entity version | Write authority stays narrow; local and collector changes serialize through the same owner's version. |
| Snapshot-embedded ReadAttempt entities | Snapshot.members exact references | Capture closes over canonical retained versions, including failed/empty reads. |
| Asset.versions array | Asset nativeVersion/source/files in each version | Native version remains metadata; application history uses the ordinary Asset version mechanism. |
| Recommendation enrichment owner/workState | WorkItem assignment and state | Estimates/notes remain Recommendation-owned; operator work has one authority. |
| Recommendation identity tied to each poll | Exact Source-version-scoped suggestion identity | Repeated observations cannot multiply one captured suggestion. Changed source ordinals do not imply continuity. |

The richer source profiles preserve detail without adding a universal entity/attribute database. Graph nodes/edges, criteria, policy components, communication pages and artifact descriptors remain owned values. [MODEL.md](MODEL.md) explains ownership and version/reference rules; [CONSOLIDATION_PLAN.md](CONSOLIDATION_PLAN.md) covers migration.

## AWS Health crosswalk

| Source concepts | Consolidated representation | Required semantics |
| --- | --- | --- |
| `HealthEvent`, `HEALTH_EVENT` | `canonicalEntity` → `HealthEvent`; HealthEvent | Keep the full provider event ARN. Event counts do not multiply by context, receipt, or delivery. |
| `EventType`, `EVENT_TYPE` | `retainedAdapterDto` → `Source`; HealthEventType | Catalog classification is observed evidence; it cannot overwrite the classification actually reported on an event. |
| `EventContext`, `EVENT_CONTEXT` | `canonicalEntity` → `EventContext`; EventContext | Unique workspace/event/kind/non-null contextKey. PUBLIC has no affected-account or organization link; ACCOUNT has exactly one account; ORG_SUMMARY has exactly one organization and owns no impacts. |
| `EventRevision`, `EVENT_REVISION` | `canonicalEntity` → `Source`, `Observation`; Retained contextual event revision | Pin contextual source evidence and field presence. Summary absence does not erase hydrated detail. Event status, provider time and local observation time remain separate. |
| `EventDescription`, `EVENT_DESCRIPTION` | `ownedValue` → `Source`; LocalizedDescription | Locale and text belong to the exact event-context revision. The latest-description API does not provide an independent provider history entity. |
| `EntityImpact`, `ENTITY_IMPACT` | `canonicalEntity` → `EntityImpact`; EntityImpact | An event-relative construct may be a resource, group or broader marker. Preserve provisional local ID and optional Health entity ARN. Supplied account must agree with ACCOUNT context. |
| `EntityRevision`, `ENTITY_REVISION` | `canonicalEntity` → `Source`, `Observation`; Retained impact revision | Entity provider-update time is independent of parent event time; repeat reads do not create another impact. |
| `Account`, `ACCOUNT` | `ownedValue` → `Workspace`, `Connection`, `Resource`; AccountReference | Preserve partition and string account ID. Names and ownership are external enrichment; receipt is not impact or membership evidence. |
| `Organization`, `ORGANIZATION` | `ownedValue` → `Workspace`, `Connection`; OrganizationReference | Preserve external organization identity and scope; Health does not return a complete organization directory. |
| `OrganizationMembership`, `ORGANIZATION_MEMBERSHIP` | `ownedValue` → `Workspace`, `Source`; OrganizationMembership | Time-bounded account/organization relation with source evidence. Historical visibility can outlast current membership. |
| `OrganizationHealthAccess`, `ORG_HEALTH_ACCESS` | `retainedAdapterDto` → `Connection`, `Source`; OrganizationHealthAccessObservation | Observed integration state differs from requested state and backfill completeness; an empty enable/disable acknowledgement proves neither readiness nor coverage. |
| `EntityResourceMatch` | `ownedValue` → `EntityImpact`, `Resource`; ResourceMatch | Zero, one or several verified resource matches, each with method, confidence and exact evidence. Unresolved values and groups remain valid. |
| `Communication`, `COMMUNICATION` | `canonicalEntity` → `Communication`; Communication | Local communication identity differs from raw AWS communicationId. Preserve notification-account context, grouping method, expected pages, conflicts and assembly state. |
| `CommunicationPage`, `COMMUNICATION_PAGE` | `ownedValue` → `Communication`; CommunicationPage | Preserve exact raw communicationId and page number. Group a page suffix only when validated; require expected pages before claiming complete membership. |
| `MessageDelivery`, `MESSAGE_DELIVERY` | `ownedValue` → `Communication`, `Observation`, `Source`; DeliveryReference | Raw envelope is an exact Source; Observation records receipt. Logical page dedupe excludes backup delivery region/envelope ID; receipt metadata never becomes affected-account attribution. |
| `SourceConnection` | `canonicalEntity` → `Connection`; Connection | A collection/access path with capabilities, authorization context and monitored scope. Changing role/connection does not change native identity. |
| `CollectionRun` | `canonicalEntity` → `Collection`, `ReadAttempt`; Collection and ReadAttempt | A bounded collection owns attempts for each operation/page, including empty successes and failures; pagination completion applies only to that query. |
| `CollectionItemError` | `ownedValue` → `ReadAttempt`; CollectionItemError | Retain event/account-specific failedSet errors even when transport status is 200. Batch success is not inferred from HTTP status. |
| `CoverageAssessment` | `ownedValue` → `Collection`, `Snapshot`, `Projection`; Coverage | Pin query scope, page chain, errors, unavailable capabilities, freshness and policy. A snapshot freezes these values; later collection cannot improve old coverage. |
| `SourceObservation`, `SOURCE_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Retained payload and receipt | Source retains the document under stable identity/version; Observation is one receipt occurrence and pins its exact Source version. API, EventBridge and local channels retain their actual context. |
| `AggregateSnapshot`, `EventAggregate`, `EntityAggregate`, `AccountEntityAggregate`, `OrganizationEntityAggregate` | `retainedAdapterDto` → `Source`; Typed captured aggregate/query DTO | Retain query, requested breakdown, counting unit, time and completeness. An omitted account breakdown is not zero affected accounts. |
| `ServiceLifecycleEntry`, `ServiceLifecycle`, `SERVICE_LIFECYCLE_ENTRY` | `canonicalEntity` → `LifecycleEntry`; LifecycleEntry | Use stable local identity and retained Source versions; service/version is not a provider-guaranteed unique key. Preserve unresolved recommendedVersion. |
| `LifecycleMilestone`, `LifecycleEvent`, `LIFECYCLE_MILESTONE` | `ownedValue` → `LifecycleEntry`; LifecycleMilestone | Owner-local milestone identity/order, explicit date/type/risks/regions and exact entry revision. A new date does not erase prior history; missing regions is not all regions. |
| `InventoryResource`, `INVENTORY_RESOURCE` | `canonicalEntity` → `Resource`; Resource | Inventory identity is external and independent of Health entity identity. Resolve by qualified evidence, never name alone. |
| `ComponentDeployment`, `COMPONENT_DEPLOYMENT` | `canonicalEntity` → `ComponentDeployment`; ComponentDeployment | One observed resource component/version and its exact source/time. A resource can host multiple components; current inventory is not historical inventory. |
| `LifecycleExposure`, `LIFECYCLE_EXPOSURE` | `projectionProfile` → `Projection`, `ComponentDeployment`, `LifecycleEntry`; LifecycleExposure | Pin deployment evidence and milestone revision. Record applicability, method, confidence, rule version and cutoff; ambiguous/no match remains unknown. |
| `WorkItem`, `WORK_ITEM` | `canonicalEntity` → `WorkItem`; WorkItem | Local owner/priority/due/workflow, independent verification state/evidence and concurrency version; completing work never changes provider entity state or independently observed deployment. |
| `WorkItemTarget`, `WORK_ITEM_TARGET` | `ownedValue` → `WorkItem`; TargetReference | Each target is exactly one typed context, impact or exposure reference. Several targets can coordinate one item without inventing a provider incident-group ID. |
| `OperatorAction`, `OPERATOR_ACTION` | `ownedValue` → `WorkItem`, `Command`, `Source`; WorkItemAction | Append actor/time/action/evidence and local version under the work aggregate; retain source statements for provenance. An action audit is not provider success. |
| `Event`, `OrganizationEvent`, `EventDetails`, `OrganizationEventDetails` | `retainedAdapterDto` → `Source`; Health response representations | Summary/detail wrappers represent existing event/context identities; representation and present fields remain explicit. |
| `EventDetailsErrorItem`, `OrganizationEventDetailsErrorItem`, `OrganizationAffectedEntitiesErrorItem` | `ownedValue` → `ReadAttempt`; CollectionItemError | Provider batch errors retain exact shape/code and scoped item references. Do not fabricate missing successful items. |
| `EventFilter`, `OrganizationEventFilter`, `EntityFilter`, `OrganizationEntityFilter`, `OrganizationEntityAccountFilter`, `EventTypeFilter`, `DateTimeRange`, `ServiceLifecycleFilter`, `pagination token` | `ownedValue` → `ReadAttempt`, `Collection`; QueryScope | These are request/cursor values, not operational identities. Save exact effective query; keep native tokens opaque and separate from application cursors. |

Source documents: [report.md](../aws/health/analysis/report.md).

## AWS DevOps Agent crosswalk

| Source concepts | Consolidated representation | Required semantics |
| --- | --- | --- |
| `OwningScope` | `ownedValue` → `Source`, `Resource`; SourceIdentity owning scope | Partition/owning account/Region plus service-specific parent scope. Unambiguously encode opaque IDs; connection role is not native identity. |
| `ConnectionContext` | `ownedValue` → `Connection`, `ReadAttempt`; AuthorizationContext | Separate access/caching/export scope from source ownership. Current authorization still applies to historical data. |
| `AgentSpace`, `SPACE` | `canonicalEntity` → `AgentSpace`; AgentSpace | Scoped native Agent Space; it is not the console Workspace. Retain ARN aliases when supplied. |
| `RegisteredService`, `REGISTERED_SERVICE` | `retainedAdapterDto` → `Source`; RegisteredService | An integration registration is not a workload Service. Built-in serviceId aws need not resolve to one; preserve independent native identity. |
| `Association`, `ASSOCIATION` | `ownedValue` → `AgentSpace`, `Source`; AgentAssociation | Own association ID/configuration discriminator and optional registration resolution. Do not require serviceId uniqueness within a space. |
| `ExternalReference`, `EXTERNAL_REFERENCE`, `ReferenceInput`, `ReferenceOutput` | `ownedValue` → `Investigation`; ExternalReference | Keep system/referenceId/URL/associationId and unresolved historical association; an external alert/ticket is not replaced by task linking. |
| `Task`, `TASK`, `Investigation`, `INVESTIGATION` | `canonicalEntity` → `Investigation`; Native Task facet | INVESTIGATION task type projects to Investigation. Preserve task priority/type/status/version and scoped task ID. Other native task types remain typed task DTOs. |
| `TaskExecutionMembership`, `TASK_EXECUTION` | `ownedValue` → `Investigation`, `Execution`; TaskExecutionMembership | Explicit link observed from task-scoped ListExecutions request. Execution has no native taskId; allow multiple observed memberships and deduplicate repeated membership evidence. |
| `Execution`, `EXECUTION` | `canonicalEntity` → `Execution`; Execution | Scoped execution identity; explicit parent can remain unresolved. Task.executionId is a pointer, not proof of latest/root/only run. STOPPED is preserved. |
| `JournalRecord`, `JOURNAL_RECORD` | `canonicalEntity` → `JournalRecord`; JournalRecord | Scoped space/execution/record ID, open recordType, createdAt and arbitrary JSON content. Preserve unknown types/scalars/null. |
| `JournalRecordRevision`, `RECORD_REVISION`, `SourceRevision`, `SOURCE_REVISION` | `canonicalEntity` → `Source`; Versioned Source | Stable source identity and exact entity version retain the payload, representation and declared digest. The source alias names a retained version; it does not become a separate revision entity or a claimed native Journal revision API. |
| `SourceObject`, `SOURCE_OBJECT` | `ownedValue` → `Source`; SourceIdentity | The collision-free owning tuple/channel/native key is an owned SourceIdentity value on versioned Source. It is independent of content digest and access credentials. |
| `ProjectionSource`, `PROJECTION_SOURCE` | `ownedValue` → `Projection`, `Source`; EvidenceRef with EvidenceLocator | EvidenceRef pins kind, id and version with an optional typed EvidenceLocator. Distinct locations remain distinct citations without creating another entity or substituting current content. |
| `DerivedRevision`, `DERIVED_REVISION` | `canonicalEntity` → `Projection`, `Source`; Versioned Projection or retained Source | Stable interpretation identity plus version retains payload kind, assertion origin and exact derivation. The five normalized profiles use Projection. Other prior typed renditions retain original aliases, payload and derivation in application-origin Source versions; no separate rendition entity is created. |
| `Derivation`, `DERIVATION` | `ownedValue` → `Projection`, `Source`; Derivation | Parser/rule/model versions and deterministic policy are retained with the result; a parser upgrade cannot rewrite an old snapshot. |
| `CollectionPass`, `COLLECTION_PASS` | `canonicalEntity` → `Collection`; Collection | One bounded query-set reconciliation with target, collector/version, selection policy and capture window. |
| `ReadAttempt`, `READ_ATTEMPT` | `canonicalEntity` → `ReadAttempt`; ReadAttempt | Every request attempt keeps its identity across STARTED and settled versions. requestSource and nullable responseSource pin exact Source versions, including empty successful envelopes. Missing response remains unknown. Snapshot.members references the attempt version instead of copying another authoritative entity. |
| `SourceObservation`, `SOURCE_OBSERVATION` | `canonicalEntity` → `Observation`; Observation | Repeat receipt of unchanged content adds observation history without creating new logical records or revisions. Non-read channels do not invent ReadAttempts. |
| `CoverageClaim`, `COVERAGE_CLAIM`, `CollectionCoverage` | `ownedValue` → `Collection`, `Projection`, `Snapshot`; Coverage | Named query-set/pass, scope, as-of, page/attempt evidence, bounds, outcome and rule version; exhaustion is not an AWS finalization barrier. |
| `TimelineItem` | `retainedAdapterDto` → `Source`, `Observation`; InvestigationTimelineItem retained as LOCAL_EVIDENCE | Independent evidence/record/receipt clocks with basis, phase, provenance, availability and stable local ordering. No invented agent progress percentage. Retain the previous typed analysis rendition as application-origin evidence; a dedicated normalized projection variant is a future schema extension. |
| `Finding`, `EvidenceItem`, `Hypothesis`, `RootCauseAssessment`, `MitigationProposal`, `ReviewResult` | `retainedAdapterDto` → `Source`, `Observation`; InvestigationAssertion retained as LOCAL_EVIDENCE | Typed attributed findings/evidence/hypotheses/causal claims/proposals/reviews, each with exact source and derivation. These are not native Resilience Finding identities or recovered private reasoning. Retain the previous typed analysis rendition as application-origin evidence; a dedicated normalized projection variant is a future schema extension. |
| `ActionObservation`, `ACTION_OBSERVATION` | `retainedAdapterDto` → `Source`, `Observation`; ActionObservation retained as LOCAL_EVIDENCE | Request, decision, resume, execution and effect are independently sourced stages. Approval or credential redemption never proves success. Retain the previous typed analysis rendition as application-origin evidence; a dedicated normalized projection variant is a future schema extension. |
| `ResultDocument` | `projectionProfile` → `Projection`; InvestigationResult | Select per investigation/mitigation phase by exact completion pointer when present; preserve missing-pointer, no-summary-reported and unavailable-reference states. |
| `ResourceReference`, `RESOURCE_REF` | `ownedValue` → `Resource`, `Projection`; ResourceReference | Explicit namespace/ID/URL and resolution provenance. A connection, same-space location or temporal adjacency is not implication or consumption evidence. |
| `ArtifactReference`, `ARTIFACT_REF` | `ownedValue` → `Projection`, `Snapshot`, `Asset`; ArtifactReference | Preserve channel, exact locator, optional asset/version, availability, type, digest and authorization. A2A and journal IDs never become native asset IDs. |
| `GraphSnapshot`, `GRAPH_SNAPSHOT` | `canonicalEntity` → `Snapshot`; Snapshot with GraphContents | Named graph kind and immutable rendition; snapshots pin nodes/edges and Source versions, not an unversioned graph. |
| `GraphNode`, `GRAPH_NODE` | `ownedValue` → `Snapshot`; GraphNode | Unique within graph rendition, with node kind/exact source and optional resolved resource; explicit stub for unresolved endpoints. |
| `GraphEdge`, `GRAPH_EDGE` | `ownedValue` → `Snapshot`; GraphEdge | Both endpoints belong to the same graph snapshot. Keep relation type/assertion origin; execution parentage or temporal precedence is not causality. |
| `Asset`, `ASSET` | `canonicalEntity` → `Asset`; Asset | Space-scoped native asset and open type. Same Agent Space does not imply that a task used or produced it. |
| `AssetVersion`, `ASSET_VERSION`, `AssetVersionMetadata` | `ownedValue` → `Asset`, `Source`; Asset.nativeVersion, source and files | Each Asset version carries the exact nativeVersion, Source reference and files. Application version and native version remain distinct. No embedded AssetVersion history array or version-only entity is created. Requested attachment IDs do not establish consumed content. |
| `AssetFileVersion`, `AssetFile`, `ASSET_FILE`, `AssetFileSummary` | `ownedValue` → `Asset`, `Source`; AssetFileVersion | Exact asset version and path; preserve bytes/text representation and content digest. A file version is an asset version, not a separate invented native counter. |
| `InvestigationSnapshot`, `Snapshot`, `SNAPSHOT` | `canonicalEntity` → `Snapshot`; Snapshot | Immutable capture manifest with task/membership/results/sources/projections, frozen coverage and explicit captureStartedAt/captureFinishedAt. capturedAt does not replace these boundaries or provider times. A later continued investigation creates new evidence. |
| `SnapshotSource`, `SNAPSHOT_SOURCE` | `ownedValue` → `Snapshot`; SnapshotSourceReference | Exact Source versions plus captured attempt/page/coverage evidence. A later successful refresh cannot improve captured coverage. |
| `SnapshotProjection`, `SNAPSHOT_PROJECTION` | `ownedValue` → `Snapshot`; SnapshotProjectionReference | Exact projectionRevisionId/hash. Authorized retained content opens independently of live refresh; comparison has its own availability. Imported legacy renditions outside the five normalized profiles are pinned in sourceRevisionIds with their original revision identity and derivation retained. |
| `ChatExecution`, `PendingMessage`, `Message`, `UserMessageBlock`, `AssistantMessageBlock`, `SendMessageContext` | `retainedAdapterDto` → `Source`; Conversation DTOs | Preserve native content unions, session scope, queue versus history distinction and attribution. Chat response completion is not task completion. |
| `UserReference` | `ownedValue` → `JournalRecord`, `Source`; ActorReference | Only supplied userId/userType are facts; absent user data is unknown and uid alone is session identity. |
| `SendMessageEvents`, `SendMessageResponseCreatedEvent`, `SendMessageResponseInProgressEvent`, `SendMessageResponseCompletedEvent`, `SendMessageResponseFailedEvent`, `SendMessageContentBlockStartEvent`, `SendMessageContentBlockDeltaEvent`, `SendMessageContentBlockDelta`, `SendMessageTextDelta`, `SendMessageJsonDelta`, `SendMessageContentBlockStopEvent`, `SendMessageSummaryEvent`, `SendMessageHeartbeatEvent`, `SendMessageUsageInfo`, `stream response/block` | `retainedAdapterDto` → `Source`, `Observation`; Conversation stream events | Own response/session/block identities and sequence when supplied; preserve partial JSON, gaps and unknown branches. Stream cursor/parentage is not durable Journal identity. |
| `ApprovalRequest`, `APPROVAL_REQUEST` | `canonicalEntity` → `ApprovalRequest`; ApprovalRequest | Observed chat request with space-scoped approvalId, execution/interrupt/toolUse IDs and exact requested pattern. Do not synthesize from waiting status or prose. |
| `ApprovalPattern`, `ApprovalAction` | `ownedValue` → `ApprovalRequest`, `Command`; ApprovalPattern and ApprovalAction | Keep typed pins and exact IDs. Finalized scope may match or narrow requested scope, never widen it; decision and resume are separate. |
| `DecisionAttempt`, `DECISION_ATTEMPT` | `canonicalEntity` → `Command`; Approval decision command | Distinct decision command/audit with payload hash, actor and definitive/ambiguous outcome. Native UpdateApprovalAction has no modeled token/readback operation. |
| `ResumeAttempt`, `RESUME_ATTEMPT` | `canonicalEntity` → `Command`; Resume command | Separate command related to accepted decision. Stream-open does not prove resumed effect; lost-response uncertainty never triggers a blind mutating retry. |
| `Goal`, `GoalContent`, `GoalSchedule` | `retainedAdapterDto` → `Source`; PreventionGoal | Keep genuine space-scoped goal identity, lifecycle/version, typed content and scheduling/last-task relations. It is not a Scenario or an investigation completion. |
| `Recommendation`, `RecommendationContent` | `retainedAdapterDto` → `Source`; AgentRecommendation | Keep native recommendationId/taskId and optional goal/version with its native lifecycle and priority. This provider identity is distinct from the source-scoped Resilience suggestion identity. |
| `Trigger`, `TriggerCondition` | `retainedAdapterDto` → `Source`; AgentTrigger | Separate native automation resource with schedule union/open action; not an Asset or executable console Scenario. Current custom-agent links are not historical consumption. |
| `OperatorApp`, `Operator application`, `identity-provider configuration` | `retainedAdapterDto` → `Source`; OperatorAppConfiguration | Provider access configuration belongs to its Agent Space; it is not console authentication or investigation fact. |
| `PrivateConnection`, `PrivateConnectionSummary`, `private network configuration` | `retainedAdapterDto` → `Source`; ProviderPrivateConnection | Keep provider name/ARN/network/certificate/state; it is not the console Connection access path. |
| `Webhook` | `retainedAdapterDto` → `Source`; AssociationWebhook | Provider intake descriptor scoped to its association; configuration does not prove receipt of any incident/event. |
| `Account usage`, `UsageMetric` | `retainedAdapterDto` → `Source`; AccountUsage | Scoped usage-window metrics and limits; not incident telemetry, runtime success, or task recovery. |
| `TaskFilter`, `TaskSortField`, `TaskSortOrder` | `ownedValue` → `Collection`, `ReadAttempt`; TaskQuery | Keep provider filter combinations and exact order; a task leaving a filtered page is not deletion. No generic updated-since feed is implied. |
| `AssetTypeSummary`, `AssetContent`, `AssetFileBody`, `AssetFileContent`, `AssetSourceUrlContent`, `AssetZipContent` | `ownedValue` → `Asset`, `Source`; Asset content DTOs | Preserve type catalog, source URL and text/bytes/ZIP members. GetAssetContent carries ZIP bytes in JSON content.zipFile; native/upload limits remain adapter-specific. |
| `ServiceConfiguration`, `preferences`, `tags`, `encryption settings`, `AdditionalServiceDetails` | `ownedValue` → `AgentSpace`, `Source`; Provider configuration values | Known typed provider unions with raw unknown variants retained. Strict native write validation is separate from tolerant output ingestion. |

Source documents: [Investigation_Data_Model.md](../aws/devops-agent/analysis/annexes/Investigation_Data_Model.md).

## AWS FIS crosswalk

| Source concepts | Consolidated representation | Required semantics |
| --- | --- | --- |
| `EXPERIMENT_TEMPLATE`, `ExperimentTemplate` | `retainedAdapterDto` → `Source`; FisExperimentTemplate | Scoped native mutable template; pin observed configuration. It is not a Scenario; no provider revision guarantee is invented. |
| `CATALOG_ACTION`, `Action` | `retainedAdapterDto` → `Source`; FisActionCatalogEntry | Native catalog identity and retrieval revision. A catalog action ID does not identify each named runtime use. |
| `ACTION_PARAMETER_DEFINITION` | `ownedValue` → `Source`; FisParameterDefinition | Catalog-action parameter map key with supplied description/requiredness. Units/types/defaults require separately sourced adapter metadata. |
| `ACTION_TARGET_SLOT` | `ownedValue` → `Source`; FisTargetSlot | Catalog action plus slot name and supported resource type. Preserve slot identity through template/runtime bindings. |
| `RESOURCE_TYPE`, `TargetResourceType` | `retainedAdapterDto` → `Source`; FisTargetResourceType | Open provider resource-type identity and typed metadata; resolve actual resources only through a type-specific adapter. |
| `TEMPLATE_ACTION` | `ownedValue` → `Source`; FisTemplateAction | Template-scoped action name, actionId and parameters. Two names using one actionId remain two definitions. |
| `TEMPLATE_TARGET` | `ownedValue` → `Source`; FisTemplateTarget | Template-scoped selector definition; retain selection mode, parameters, filters and tags as supplied. |
| `TEMPLATE_BINDING` | `ownedValue` → `Source`; FisTemplateBinding | Action/slot references a named selector within the same template. |
| `TEMPLATE_DEPENDENCY` | `ownedValue` → `Source`; FisTemplateDependency | Named predecessor/successor edge within one template DAG; keep separate from console workflow dependencies. |
| `TEMPLATE_TARGET_ACCOUNT` | `ownedValue` → `Source`; FisTemplateTargetAccount | Template/account identity with role/reference metadata. Current template configuration cannot rewrite prior experiments. |
| `EXPERIMENT_RUN`, `Experiment` | `canonicalEntity` → `Experiment`; Experiment | Scoped native experiment identity with frozen run configuration. May exist without a console Run; a StepAttempt can explicitly refer to it. |
| `ACTION_EXECUTION` | `ownedValue` → `Experiment`; ExperimentAction | Experiment/action-name identity, raw state/reason/times and parameters. No independent stop/retry/pause operation is implied. |
| `ACTION_DEPENDENCY` | `ownedValue` → `Experiment`; ExperimentActionDependency | Same-experiment named-action DAG from runtime evidence, independent of product StepRuns. |
| `TARGET_SELECTION` | `ownedValue` → `Experiment`; ExperimentTargetSelector | Exact runtime selector snapshot; never read current template to reconstruct historical target intent. |
| `ACTION_TARGET_BINDING` | `ownedValue` → `Experiment`; ExperimentTargetBinding | Action-name/slot-to-selector link with owning experiment scope. |
| `EXPERIMENT_TARGET_ACCOUNT` | `ownedValue` → `Experiment`, `Source`; ExperimentTargetAccount | Run-scoped account configuration observation. Account inclusion alone creates neither child experiment nor per-account success. |
| `RESOLVED_TARGET_MEMBERSHIP` | `ownedValue` → `Experiment`, `Source`; ResolvedTargetMembership | Keep every selector membership and complete targetInformation. Deduplicate established Resource identity separately from membership. |
| `RESOURCE_IDENTITY` | `ownedValue` → `Resource`, `Experiment`; ResourceReference | Qualified type/account/Region/native key and match provenance. EKS pod scope includes cluster/namespace/name; container selection remains membership detail. |
| `TARGET_RESOLUTION_OBSERVATION` | `ownedValue` → `Collection`, `Experiment`, `Source`, `Observation`; Bounded target-resolution evidence and coverage | Resolution-ended evidence and exhausted page traversal are independent. A complete empty page does not by itself establish empty resolved scope. |
| `EXECUTION_EVIDENCE` | `canonicalEntity` → `Source`, `Observation`; Retained execution evidence | Exact source record/location with action/selector/account associations; top-level FIS log id is experiment ID, not an event ID. |
| `STATE_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Experiment/action state evidence | Preserve raw provider status, source timestamp and observation/capture interval; receipt order does not establish lifecycle order. |
| `EXPERIMENT_REPORT` | `ownedValue` → `Experiment`, `Source`; ExperimentReport | Report generation/readiness is independent of experiment execution and assessment. Eligibility/configuration presence and retrieval errors remain explicit. |
| `REPORT_ARTIFACT` | `ownedValue` → `Experiment`, `Snapshot`; ArtifactReference | Exact artifact descriptor/ARN/type and version/digest when known; access is authorized separately, and presence does not imply evaluation success. |
| `STOP_CONDITION` | `ownedValue` → `Experiment`, `Source`; FisStopCondition | Source/value retained; source=none is an explicit marker and creates no alarm reference. |
| `CLOUDWATCH_ALARM` | `ownedValue` → `Resource`; AlarmReference | Qualified external alarm identity. Alarm state/history is separately observed evidence, not an experiment aggregate. |
| `ALARM_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Alarm evidence | Exact state/transition with source/time/coverage; experiment termination cannot fabricate an alarm transition. |
| `AWS_SCOPE` | `ownedValue` → `Source`, `Resource`; SourceIdentity scope | Partition/account/Region is a provider ownership value, not tenant identity or a credential grant. |
| `SAFETY_LEVER` | `retainedAdapterDto` → `Source`; FisSafetyLever | Scoped native safety control; unknown hydration does not remove the native one-per-supported-scope relation. Writes remain explicit future adapter commands. |
| `METRIC_BINDING` | `ownedValue` → `Scenario`; MetricBinding | Versioned metric/query definition with dimensions, units, aggregation, period/windows/normalizer and source. |
| `EXPERIMENT_METRIC_BINDING` | `ownedValue` → `Run`, `Experiment`; MetricBindingReference | Exact binding revision and experiment/window use. It does not duplicate the metric definition or invent native linkage. |
| `METRIC_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Metric evidence | Typed samples with query/unit/window/coverage. Missing sample is not zero and prose is not a numeric series. |
| `ASSESSMENT_CRITERION` | `ownedValue` → `Scenario`; CheckDefinition | Immutable evaluator/predicate/threshold/unit/denominator semantics pinned with the revision or read-only reassessment specification. |
| `RESILIENCE_ASSESSMENT` | `projectionProfile` → `Projection`, `Snapshot`; EVALUATION projection | Local immutable evaluation, not native ResilienceAssessment. New evidence/rule/cutoff creates another EVALUATION revision over a frozen input Snapshot; an orchestration Run is optional. Preserve every historical assessment of an experiment. |
| `ASSESSMENT_EVIDENCE` | `ownedValue` → `StepAttempt`, `Projection`; EvidenceReference | Exact accepted Source versions/observations and evaluation cutoff, scoped to the Run through retained/imported references. |

Source documents: [report.md](../aws/fis/analysis/report.md).

## Assessment workflow crosswalk

| Source concepts | Consolidated representation | Required semantics |
| --- | --- | --- |
| `Scenario` | `canonicalEntity` → `Scenario`; Scenario | One stable scenarioId with common version metadata. DRAFT editing, PUBLISHED definition and ARCHIVED admission policy are states of successive Scenario versions. Names and digests are not identity. |
| `ScenarioRevision` | `canonicalEntity` → `Scenario`; Scenario at an exact PUBLISHED version | The source publication concept becomes a Scenario version with locked operation/schema/implementation/runtime contracts and digest. Run pins that exact version. Later draft/archive versions cannot mutate the published program. |
| `Run` | `canonicalEntity` → `Run`; Run | Run pins a published Scenario version and admission Snapshot version. Each Run version pins exact StepRun versions; historical verdicts cannot join current children. Execution outcome, acceptance and finalization remain separate. |
| `StepRun` | `canonicalEntity` → `StepRun`; StepRun | One identity per compiled main/finalizer step, including skipped steps. selectedAttempt pins an exact StepAttempt version; attemptNo remains a retry index on the attempt. Parent runId is ownership, not permission to resolve a historical run through current children. |
| `StepAttempt` | `canonicalEntity` → `StepAttempt`; StepAttempt | Unique (stepRunId,attemptNo), durable dispatch/effect intent, evidence and checkpoints. Poll/resume does not create a new attempt; ambiguous effects fence retries. |
| `Evidence` | `canonicalEntity` → `Source`, `Observation`; Shared evidence spine | Replace run-only Evidence root with immutable payload revision + receipt/import occurrence. Run owns an immutable evidence-reference manifest; producer/import origin and same-run citation authorization remain explicit. |
| `StepDefinition` | `ownedValue` → `Scenario`; StepDefinition | Owned stepKey, bindings, inputs, dependencies, timeout/retry/check role and main/finalizer phase belong to the containing Scenario version. They do not have independent version entities. |
| `OperationLock` | `ownedValue` → `Scenario`; OperationLock | Exact implementation/input/output schema digests and contract version; unavailable/revoked pin rejects execution without silent substitution. |
| `AdmissionSnapshot` | `ownedValue` → `Run`; AdmissionSnapshot | Exact revision, validated inputs, authorized resource/connection bindings and observed versions, enabled steps, required-criterion denominator and effective policy. |
| `DeploymentRef`, `ConnectionRef`, `ResourceRef` | `ownedValue` → `Run`, `Scenario`; BindingReference | Qualified external references; inventory and credentials remain separate. Resolving a reference never grants permission. |
| `CheckResult` | `ownedValue` → `StepAttempt`, `Projection`; CheckResult | Sealed verdict/reason, evaluator digest, actual/expected values, evidence refs and evaluation cutoff. False predicate is not technical failure. |
| `Observation` | `ownedValue` → `Source`, `Observation`; Typed evidence payload | The source workflow uses Observation for evidence content. Consolidated Observation names receipt identity; payload kind/coverage remains typed on the retained evidence profile. |
| `ExternalOperationRef` | `ownedValue` → `StepAttempt`, `Command`; ExternalOperationReference | Qualified provider handle plus stable originEffectKey even before remote ID is known. Native Experiment and logs query IDs are references, not a new generic Run. |
| `CancellationIntent` | `ownedValue` → `Run`, `Command`; CancellationIntent | First accepted principal/time/reason is monotonic, fences new main dispatch, and is independent of confirmed remote stop or cleanup. |
| `ArtifactRef` | `ownedValue` → `Source`, `Snapshot`; ArtifactReference | Store locator/version/media/length/digest; temporary download URL and access rights resolve separately. |
| `ExecutionError` | `ownedValue` → `StepAttempt`, `Command`; ExecutionError | Typed technical failure with safe diagnostics. Assessment false, transport failure and unresolved side effect have different meanings. |
| `capture-session handle`, `operation registry`, `criterion denominator`, `finalization result` | `ownedValue` → `StepAttempt`, `Scenario`, `Run`; Workflow control values | Capture handle is an external-operation reference; registry locks and reducer/denominator/finalization values belong to revision/run ownership, not extra CRUD roots. |

Source documents: [model.md](../aws/fis/analysis/workflow/model.md).

## AWS Resilience Hub crosswalk

| Source concepts | Consolidated representation | Required semantics |
| --- | --- | --- |
| `SystemEntity`, `SYSTEM` | `canonicalEntity` → `System`; System with provider binding | Console System owns local catalog metadata; verified native ARN/ID is an alias/import fact. ARN-less summaries retain unresolved partial identity, not a fabricated ARN. |
| `SYSTEM_SERVICE` | `ownedValue` → `Service`; SystemServiceMembership | One local Service membership authority, with provenance for imported native associatedSystems. Shared services deduplicate by canonical/provider identity, not path count. |
| `UserJourneyEntity`, `USER_JOURNEY` | `canonicalEntity` → `UserJourney`; UserJourney with provider binding | Belongs to one System; provider identity includes parent system scope. Local catalog changes never silently update native journey configuration. |
| `JOURNEY_SERVICE` | `ownedValue` → `Service`; JourneyServiceMembership | Selected journey belongs to the same associated System; derive journey service list from Service membership rather than two writable authorities. |
| `ServiceEntity`, `SERVICE` | `canonicalEntity` → `Service`; Service with provider binding | Console business service has opaque canonical identity and local configuration. Native ARN/configuration is an imported facet, not the universal service primary key. |
| `ResiliencePolicyEntity`, `POLICY` | `canonicalEntity` → `ResiliencePolicy`; ResiliencePolicy | Qualified policy identity with immutable Source versions; direct service/journey assignment stays explicit and no native system policy is invented. |
| `POLICY_COMPONENT` | `ownedValue` → `ResiliencePolicy`; PolicyComponent | Four typed native components: availabilitySlo, dataRecovery, multiAz, multiRegion. Local performance objectives require a separate namespace and units. |
| `EFFECTIVE_TARGET_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Effective-target evidence | Exact observed target bundle with original source/time; do not independently select latest values when displaying an older posture context. |
| `EFFECTIVE_TARGET` | `ownedValue` → `Source`; EffectiveTarget | Typed value/unit plus optional policy name and ownership. Name is not policy identity; SELF/CROSS_ACCOUNT is not DIRECT/INHERITED. |
| `POLICY_CONTEXT_CAPTURE`, `CapturedAssociation`, `PolicyAssignmentEvidence` | `ownedValue` → `Snapshot`, `ResilienceAssessment`; PolicyContextCapture | Immutable assignment/membership/policy hashes and exact effective-target Source version; observed context does not prove which policy revision AWS evaluated. |
| `AssessmentEntity`, `ASSESSMENT` | `canonicalEntity` → `ResilienceAssessment`; ResilienceAssessment | Native service/assessment identity. Execution SUCCESS is distinct from policy achievability, runtime health, finding count or verified remediation. |
| `FindingEntity`, `FINDING` | `canonicalEntity` → `Finding`; Finding | Native service/finding identity and observed summary/detail. Do not require assessment FK; optional same-service capture correlation has an explicit basis. |
| `FINDING_CAPTURE` | `canonicalEntity` → `Collection`, `ReadAttempt`; Finding collection | Capture list/page/detail scope/outcomes and optional qualified assessment correlation. New incomplete capture cannot claim old complete coverage is current. |
| `FINDING_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Finding evidence | Capture/service/finding/representation plus exact field presence; preserve summary versus detail and incomplete hydration. |
| `RecommendationEntity`, `RECOMMENDATION` | `canonicalEntity` → `Recommendation`; Recommendation | Without a stable native suggestion key, identity is finding + exact Source version + group/ordinal. Repeated observations of that same Source version reuse Recommendation identity. Ordinals in changed source content do not prove continuity. Enrichment publishes a new Recommendation version. |
| `RECOMMENDATION_ENRICHMENT`, `RecommendationEstimate` | `ownedValue` → `Recommendation`, `WorkItem`; RecommendationEnrichment and WorkItem | Title, effort, estimate and note are owned enrichment using Recommendation.version. WorkItem owns assignment and operator state. No nested enrichment version or duplicate owner/workState is maintained. Unknown cost stays unknown; enrichment cannot alter the captured suggestion. |
| `DependencyDiscoveryConfig`, `DEPENDENCY_DISCOVERY_CONFIG` | `ownedValue` → `Service`, `Source`; DependencyDiscoveryObservation | Provider-managed status/count/time/message separate from strict ENABLED/DISABLED desired write. Missing output is unknown, not disabled. |
| `DependencyEntity`, `DEPENDENCY` | `canonicalEntity` → `Dependency`; Dependency with provider evidence | Qualified service/dependency identity and DNS evidence; canonical relation/matches remain optional and sourced. No invented dependency-to-topology FK. |
| `DEPENDENCY_GOVERNANCE` | `ownedValue` → `Dependency`; Dependency.governance | Decision, rationale and audit actor are owned values governed by Dependency.version. Their write authority is local; they cannot alter provider classification, observed traffic or network permissions. There is no separate governance version counter. |
| `TopologyEntity`, `TOPOLOGY_SNAPSHOT` | `canonicalEntity` → `Snapshot`; Snapshot with GraphContents | Immutable typed graph capture with filters/window/coverage. Resource/edge pages are not an atomic AWS snapshot. |
| `TOPOLOGY_NODE` | `ownedValue` → `Snapshot`; GraphNode | Snapshot-local node identity and optional qualified Resource reference; unresolved endpoint is an explicit stub. |
| `TOPOLOGY_EDGE`, `EdgeProperty` | `ownedValue` → `Snapshot`; GraphEdge | Both endpoints share snapshot; retain every supplied relation/label/type property and provenance. Missing type does not default to data flow. |
| `ENTITY_REF` | `ownedValue` → `Source`, `Projection`, `WorkItem`; EntityReference | Typed/scoped provider/canonical key with resolved/unresolved/tombstone state. This is a reference contract, not a universal untyped entity table. |
| `EVENT`, `Event envelope` | `canonicalEntity` → `Source`, `Observation`; Operational event evidence | Channel/stream scope/source event ID dedupe, raw envelope and independent source/receipt times. It is not an AWS HealthEvent. |
| `EVENT_SUBJECT`, `Event subjects` | `ownedValue` → `Source`, `Observation`; EventSubject | Typed scoped subject/role/link evidence and parent scope; event arrival is refresh evidence, not a completed detail reconciliation. |
| `POSTURE_OBSERVATION` | `canonicalEntity` → `Source`, `Observation`; Posture evidence | Retain achievability and captured target context with explicit optional assessment correlation. Local finding disposition cannot rewrite posture. |
| `HEALTH_OBSERVATION`, `Health observation` | `canonicalEntity` → `Source`, `Observation`; Runtime health evidence | Monitoring signal identity, measuredAt, expiry and source; independent of AWS HealthEvent and policy posture. Ties/older observations do not win by arrival. |
| `CURRENT_PROJECTION`, `Service status projection` | `projectionProfile` → `Projection`; ServiceStatus and WorkspaceSummary | Separate execution/posture/runtime health/discovery/coverage/attention; retain exact contributor IDs and rule version. Recompute does not renew source freshness. |
| `InputSourceEntity`, `Input source` | `retainedAdapterDto` → `Source`; ServiceInputSource | Service-scoped source ID and exact typed configuration. Writes accept one supported union member; read-only MONITORING and unknown branches are not automatically creatable. |
| `ServiceResource` | `retainedAdapterDto` → `Source`, `Resource`; ServiceResourceObservation | Service-local resourceIdentifier/full descriptor/input-source ref plus optional established canonical Resource identity. Unqualified ID is not a global resource. |
| `ServiceFunction` | `retainedAdapterDto` → `Source`; ServiceFunction | Preserve service-scoped function references from findings and explicitly qualified resolution; no invented direct resource ARN. |
| `PermissionModel`, `ResourceDiscovery`, `ReportConfiguration`, `DevOpsAgentConfiguration` | `ownedValue` → `Service`, `Source`; Provider service configuration values | Keep strict native write DTO separate from nullable observed configuration. Report destination is not artifact readiness; agentSpaceArn is a link, not identity equivalence. |
| `AssessmentCost` | `ownedValue` → `ResilienceAssessment`; AssessmentCost | Provider execution cost/billable units; never the local cost estimate of a proposed remediation. |
| `DNS queryRange`, `buckets` | `ownedValue` → `Dependency`, `Source`; DnsQueryObservation | Exact start/end/granularity and timestamped counts. DNS activity cannot become latency, request success or availability. |
| `EffectivePolicyEvidence` | `ownedValue` → `Projection`, `Snapshot`; EffectivePolicyEvidence | Bundle references the exact effective-target observation used by its context, not an independently selected current target set. |
| `FindingCoverage`, `AssessmentCoverage`, `AttentionReason` | `ownedValue` → `Projection`; Coverage and AttentionReason | Explicit populations/counts, scope, freshness, reason codes and reducer version. Empty scope has no fabricated percentage or journey compliance. |
| `PageSnapshot` | `ownedValue` → `Collection`; PaginationSnapshot | Traversal infrastructure with principal/query/revision binding and expiry, not a business entity or native snapshot guarantee. |
| `Local revision`, `DeletionReceipt`, `tombstone` | `ownedValue` → `Command`, `Source`, `Projection`; Common entity metadata and command receipt | Every entity requires version, createdAt and updatedAt. Exact history keeps the same identity. Command/tombstone evidence preserves effect and retention meaning; deleting local metadata does not cascade into captured evidence or claim native deletion. |
| `NormalizationDiagnostic` | `ownedValue` → `Source`, `Projection`; NormalizationDiagnostic | Field path/raw value/presence/reason preserve unknown output vocabulary and invalid/partial data without relaxing command inputs. |
| `Workspace summary` | `projectionProfile` → `Projection`; WORKSPACE_SUMMARY projection | Deduplicate service contributors and keep separate runtime-health, policy-posture and assessment-coverage counts with scope, as-of time and reducer version. |

Source documents: [report.md](../aws/resilience-hub/analysis/report.md).

## Registered profiles

Profiles declare native/retained families and their normalization boundary. Their observedFields are conservative hints, not replacement native SDK schemas. Unsupported fields and provider values remain in the Source payload. A profile does not authorize native mutations. Full source shapes, read operations, identity rules and deferred mutation lists are in [the registry](model/adapter-profiles.json).

| Profile | Family | Canonical owners | Normalized binding |
| --- | --- | --- | --- |
| `aws.health.event/v1` | Event summaries and contextual details | `HealthEvent`, `EventContext` | Retained Source profile |
| `aws.health.entity-impact/v1` | Event-relative affected construct | `EntityImpact` | Retained Source profile |
| `aws.health.event-type/v1` | Event classification catalog | `Source` | Retained Source profile |
| `aws.health.lifecycle-entry/v1` | Service-version lifecycle catalog | `LifecycleEntry` | Retained Source profile |
| `aws.health.communication/v1` | EventBridge communication and delivery | `Communication` | Retained Source profile |
| `aws.health.organization-access/v1` | Organization aggregation configuration | `Connection`, `Source` | Retained Source profile |
| `aws.devops-agent.agent-space/v1` | Agent Space configuration | `AgentSpace` | Retained Source profile |
| `aws.devops-agent.registered-service/v1` | Integration registration | `Source` | Retained Source profile |
| `aws.devops-agent.association/v1` | Agent Space association | `AgentSpace`, `Source` | Retained Source profile |
| `aws.devops-agent.task/v1` | Backlog task | `Investigation` | Retained Source profile |
| `aws.devops-agent.execution/v1` | Agent execution | `Execution` | Retained Source profile |
| `aws.devops-agent.journal-record/v1` | Published journal record | `JournalRecord` | Retained Source profile |
| `aws.devops-agent.asset/v1` | Versioned native asset and files | `Asset` | Retained Source profile |
| `aws.devops-agent.conversation/v1` | Conversation and pending queue | `Source` | Retained Source profile |
| `aws.devops-agent.chat-stream/v1` | Native SendMessage event stream | `Source`, `Observation` | Retained Source profile |
| `aws.devops-agent.approval/v1` | Directed action approval context | `ApprovalRequest` | Retained Source profile |
| `aws.devops-agent.goal/v1` | Prevention goal | `Source` | Retained Source profile |
| `aws.devops-agent.recommendation/v1` | Native prevention recommendation | `Source` | Retained Source profile |
| `aws.devops-agent.trigger/v1` | Native automation trigger | `Source` | Retained Source profile |
| `aws.devops-agent.operator-app/v1` | Provider operator-app access | `Source` | Retained Source profile |
| `aws.devops-agent.private-connection/v1` | Provider private connectivity | `Source` | Retained Source profile |
| `aws.devops-agent.webhook/v1` | Association webhook descriptor | `Source` | Retained Source profile |
| `aws.devops-agent.account-usage/v1` | Account usage window | `Source` | Retained Source profile |
| `aws.fis.template/v1` | Reusable provider experiment template | `Source` | Retained Source profile |
| `aws.fis.action-catalog/v1` | Fault-action catalog | `Source` | Retained Source profile |
| `aws.fis.resource-type/v1` | Target resource-type catalog | `Source` | Retained Source profile |
| `aws.fis.experiment/v1` | Provider experiment execution | `Experiment` | Retained Source profile |
| `aws.fis.target-account/v1` | Template and experiment target accounts | `Experiment`, `Source` | Retained Source profile |
| `aws.fis.safety-lever/v1` | Scoped safety control | `Source` | Retained Source profile |
| `aws.fis.execution-evidence/v1` | Experiment logs and state events | `Source`, `Observation` | Retained Source profile |
| `aws.fis.report/v1` | Experiment report and artifacts | `Experiment`, `Source` | Retained Source profile |
| `aws.cloudwatch.alarm/v1` | Alarm state/history evidence | `Source`, `Observation` | Retained Source profile |
| `aws.cloudwatch.metric/v1` | Metric query/sample evidence | `Source`, `Observation` | Retained Source profile |
| `aws.logs.query/v1` | Logs Insights query and results | `Source`, `Observation` | Retained Source profile |
| `aws.resilience-hub.system/v1` | Native system catalog | `System` | Retained Source profile |
| `aws.resilience-hub.user-journey/v1` | Native user journey | `UserJourney` | Retained Source profile |
| `aws.resilience-hub.service/v1` | Native service configuration | `Service` | Retained Source profile |
| `aws.resilience-hub.policy/v1` | Native resilience policy | `ResiliencePolicy` | Retained Source profile |
| `aws.resilience-hub.effective-targets/v1` | Observed effective target values | `Source`, `Observation` | Retained Source profile |
| `aws.resilience-hub.assessment/v1` | Failure-mode assessment execution | `ResilienceAssessment` | Retained Source profile |
| `aws.resilience-hub.finding/v1` | Service-scoped failure-mode finding | `Finding` | Retained Source profile |
| `aws.resilience-hub.recommendation/v1` | Finding suggested change | `Recommendation` | Retained Source profile |
| `aws.resilience-hub.dependency/v1` | Observed service dependency | `Dependency` | Retained Source profile |
| `aws.resilience-hub.input-source/v1` | Native discovery input source | `Source` | Retained Source profile |
| `aws.resilience-hub.resource/v1` | Service resource inventory | `Source`, `Resource` | Retained Source profile |
| `aws.resilience-hub.service-function/v1` | Service-function context | `Source` | Retained Source profile |
| `aws.resilience-hub.event/v1` | Operational service/system/policy event | `Source`, `Observation` | Retained Source profile |
| `aws.resilience-hub.posture/v1` | Policy achievability evidence | `Source`, `Observation` | Retained Source profile |
| `console.health.aggregate/v1` | Health aggregate | `Source`, `Observation` | Retained Source profile |
| `console.health.lifecycle-exposure/v1` | Lifecycle exposure | `Projection` | projectionProfile=LIFECYCLE_EXPOSURE, schemaRef=schema.json#/$defs/LifecycleExposure |
| `console.investigation.timeline/v1` | Investigation timeline | `Source`, `Observation` | Retained Source profile |
| `console.investigation.assertion/v1` | Published investigation assertion | `Source`, `Observation` | Retained Source profile |
| `console.investigation.action-observation/v1` | Action stage observation | `Source`, `Observation` | Retained Source profile |
| `console.investigation.result/v1` | Phase-specific investigation result | `Projection` | projectionProfile=INVESTIGATION_RESULT, schemaRef=schema.json#/$defs/InvestigationResult |
| `console.investigation.graph/v1` | Typed investigation graph | `Snapshot` | snapshotKind=TOPOLOGY, schemaRef=schema.json#/$defs/GraphContents |
| `console.fis.target-resolution/v1` | FIS target resolution | `Experiment`, `Collection`, `Source`, `Observation` | Retained Source profile |
| `console.workflow.check-result/v1` | Sealed check result | `StepAttempt` | ownedValue=StepAttempt.checkResult, schemaRef=schema.json#/$defs/CheckResult |
| `console.resilience.topology/v1` | Captured topology | `Snapshot` | snapshotKind=TOPOLOGY, schemaRef=schema.json#/$defs/GraphContents |
| `console.resilience.status/v1` | Service/portfolio status | `Projection` | projectionProfile=SERVICE_STATUS, schemaRef=schema.json#/$defs/ServiceStatus |
| `console.monitoring.health/v1` | External runtime-health evidence | `Source`, `Observation` | Retained Source profile |
| `console.workflow.evaluation/v1` | Immutable reevaluation | `Projection`, `Snapshot` | projectionProfile=EVALUATION, schemaRef=schema.json#/$defs/Evaluation |
| `console.resilience.workspace-summary/v1` | Workspace summary | `Projection` | projectionProfile=WORKSPACE_SUMMARY, schemaRef=schema.json#/$defs/WorkspaceSummary |
| `console.inventory.resource/v1` | Independent inventory and deployment observation | `Resource`, `ComponentDeployment`, `Source`, `Observation` | Retained Source profile |
| `aws.devops-agent.lifecycle-event/v1` | Investigation and mitigation lifecycle notification | `Investigation`, `Execution`, `Source`, `Observation` | Retained Source profile |
| `console.collection.request/v1` | Retained collection request envelope | `Source`, `ReadAttempt` | Retained Source profile |

The migration preserves original source terms as navigation/provenance. It does not preserve rejected representation choices as current domain classes. Each new target follows the common version contract and the current user's instruction.
