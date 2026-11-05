# Entity and value reference

Generated from [schema.json](schema.json). Edit the schema, then run `python tools/render_model.py` from this package. [MODEL.md](../MODEL.md) defines the invariants and ownership rules that JSON Schema cannot express.

The model contains **37 entities**. Every entity except Workspace includes `workspaceId`. Foreign references must resolve in that workspace and satisfy the documented parent scope. Provider identifiers are retained separately from application IDs.

## Entity index

| Module | Entity | Owner | Identity |
| --- | --- | --- | --- |
| foundation | [Workspace](#workspace) | application | `workspaceId` |
| foundation | [Connection](#connection) | application | `workspaceId + connectionId` |
| foundation | [Resource](#resource) | observed | `workspaceId + resourceId` |
| foundation | [Collection](#collection) | collector | `workspaceId + collectionId` |
| foundation | [ReadAttempt](#readattempt) | collector | `workspaceId + collectionId + readAttemptId` |
| foundation | [SourceRevision](#sourcerevision) | retained evidence | `workspaceId + sourceRevisionId` |
| foundation | [Observation](#observation) | collector | `workspaceId + observationId` |
| foundation | [ProjectionRevision](#projectionrevision) | derived | `workspaceId + projectionRevisionId` |
| foundation | [Snapshot](#snapshot) | application retained capture | `workspaceId + snapshotId` |
| foundation | [WorkItem](#workitem) | application | `workspaceId + workItemId` |
| foundation | [Command](#command) | application | `workspaceId + commandId` |
| workload | [System](#system) | application | `workspaceId + systemId` |
| workload | [UserJourney](#userjourney) | application | `workspaceId + userJourneyId` |
| workload | [Service](#service) | application | `workspaceId + serviceId` |
| workload | [Dependency](#dependency) | observed plus local governance | `workspaceId + serviceId + dependencyId` |
| health | [HealthEvent](#healthevent) | observed | `workspaceId + healthEventId` |
| health | [EventContext](#eventcontext) | observed | `workspaceId + healthEventId + kind + contextKey` |
| health | [EntityImpact](#entityimpact) | observed | `workspaceId + eventContextId + scoped provider entity key` |
| health | [Communication](#communication) | derived grouping | `workspaceId + communicationId` |
| health | [LifecycleEntry](#lifecycleentry) | observed local identity | `workspaceId + lifecycleEntryId` |
| health | [ComponentDeployment](#componentdeployment) | observed inventory | `workspaceId + componentDeploymentId` |
| resilience | [ResiliencePolicy](#resiliencepolicy) | observed | `workspaceId + resiliencePolicyId` |
| resilience | [ResilienceAssessment](#resilienceassessment) | observed | `workspaceId + serviceId + resilienceAssessmentId` |
| resilience | [Finding](#finding) | observed | `workspaceId + serviceId + findingId` |
| resilience | [Recommendation](#recommendation) | immutable evidence plus local enrichment | `workspaceId + serviceId + findingId + detail observation + group + ordinal` |
| investigation | [AgentSpace](#agentspace) | observed | `workspaceId + agentSpaceId` |
| investigation | [Investigation](#investigation) | observed aggregate | `workspaceId + agentSpaceId + native taskId` |
| investigation | [Execution](#execution) | observed | `workspaceId + agentSpaceId + native executionId` |
| investigation | [JournalRecord](#journalrecord) | observed | `workspaceId + agentSpaceId + executionId + native recordId` |
| investigation | [ApprovalRequest](#approvalrequest) | observed control request | `workspaceId + approvalRequestId` |
| investigation | [Asset](#asset) | observed | `workspaceId + assetId` |
| workflow | [Scenario](#scenario) | application | `workspaceId + scenarioId` |
| workflow | [ScenarioRevision](#scenariorevision) | application immutable publication | `workspaceId + scenarioId + scenarioRevisionId` |
| workflow | [Run](#run) | application execution | `workspaceId + runId` |
| workflow | [StepRun](#steprun) | application execution | `workspaceId + runId + stepKey` |
| workflow | [StepAttempt](#stepattempt) | application execution facts | `workspaceId + runId + stepRunId + attemptNo` |
| fis | [Experiment](#experiment) | observed | `workspaceId + experimentId` |

## Entities

### Workspace

Application authorization and configuration boundary, distinct from AWS AgentSpace.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId`.

| Field | Type | Required |
| --- | --- | --- |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `enabledModules` | `List[enum]` | Yes |
| `organizationMemberships` | `List[OrganizationMembership]` | Yes |
| `organizationAccess` | `List[OrganizationAccess]` | Yes |

### Connection

Access path/credential reference, not native owner identity. Secrets remain outside the model.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId + connectionId`.

| Field | Type | Required |
| --- | --- | --- |
| `connectionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `provider` | `string` | Yes |
| `credentialRef` | `string` | Yes |
| `allowedScopes` | `List[OwningScope]` | Yes |
| `authorizationContextKey` | `string` | Yes |
| `enabled` | `boolean` | Yes |

### Resource

Canonical inventory identity with explicit stable or run-scoped boundary; does not represent all native objects.

**Owner:** observed. **Module:** foundation. **Identity:** `workspaceId + resourceId`.

| Field | Type | Required |
| --- | --- | --- |
| `resourceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `identityStability` | `enum` | Yes |
| `incarnationKey` | `string or null` | Yes |
| `selectedObservationId` | `Id or null` | Yes |
| `displayName` | `string or null` | Yes |
| `matches` | `List[ResourceMatch]` | Yes |

### Collection

A finite collection pass records its exact query set, including empty and failed reads.

**Owner:** collector. **Module:** foundation. **Identity:** `workspaceId + collectionId`.

| Field | Type | Required |
| --- | --- | --- |
| `collectionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `connectionId` | `Id` | Yes |
| `queries` | `List[CollectionQuery]` | Yes |
| `state` | `enum` | Yes |
| `startedAt` | `Timestamp` | Yes |
| `endedAt` | `Timestamp or null` | Yes |
| `coverage` | `List[Coverage]` | Yes |
| `projectionVersion` | `Version` | Yes |

### ReadAttempt

A single request attempt exists even if it returned zero objects or failed. It is immutable once settled.

**Owner:** collector. **Module:** foundation. **Identity:** `workspaceId + collectionId + readAttemptId`.

| Field | Type | Required |
| --- | --- | --- |
| `readAttemptId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `collectionId` | `Id` | Yes |
| `queryKey` | `string` | Yes |
| `attemptNo` | `Version` | Yes |
| `requestDigest` | `Digest` | Yes |
| `state` | `enum` | Yes |
| `startedAt` | `Timestamp` | Yes |
| `endedAt` | `Timestamp or null` | Yes |
| `providerRequestId` | `string or null` | Yes |
| `returnedCount` | `integer or null` | Yes |
| `nextTokenPresent` | `boolean or null` | Yes |
| `error` | `ReadError or null` | Yes |
| `authorizationContextKey` | `string` | Yes |
| `requestSourceRevisionId` | `Id` | Yes |
| `responseSourceRevisionId` | `Id or null` | Yes |

### SourceRevision

Immutable distinct source payload/envelope for one identity, representation and content digest. Observation time is recorded separately.

**Owner:** retained evidence. **Module:** foundation. **Identity:** `workspaceId + sourceRevisionId`.

| Field | Type | Required |
| --- | --- | --- |
| `sourceRevisionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `representation` | `enum` | Yes |
| `profile` | `string` | Yes |
| `profileVersion` | `string` | Yes |
| `sourceOperation` | `string` | Yes |
| `contentDigest` | `Digest` | Yes |
| `providerUpdatedAt` | `Timestamp or null` | Yes |
| `providerVersion` | `string or null` | Yes |
| `fieldPresence` | `List[FieldPresence]` | Yes |
| `payload` | `JsonValue` | Yes |
| `artifact` | `ArtifactRef or null` | Yes |
| `digestProfile` | `enum` | Yes |
| `payloadStorage` | `enum` | Yes |

### Observation

Immutable receipt/read observation of one revision. Repeated polls do not create new logical objects. Event/stream/local receipts may have no ReadAttempt; no native read is fabricated.

**Owner:** collector. **Module:** foundation. **Identity:** `workspaceId + observationId`.

| Field | Type | Required |
| --- | --- | --- |
| `observationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `sourceRevisionId` | `Id` | Yes |
| `readAttemptId` | `Id or null` | Yes |
| `connectionId` | `Id or null` | Yes |
| `observedAt` | `Timestamp` | Yes |
| `sourceTime` | `Timestamp or null` | Yes |
| `transportTime` | `Timestamp or null` | Yes |
| `expiresAt` | `Timestamp or null` | Yes |
| `authorizationContextKey` | `string` | Yes |
| `receiptKey` | `string or null` | Yes |
| `channel` | `enum` | Yes |

### ProjectionRevision

Immutable versioned derivation with retained inputs, coverage and rule digest. Current selection is a read view.

**Owner:** derived. **Module:** foundation. **Identity:** `workspaceId + projectionRevisionId`.

| Field | Type | Required |
| --- | --- | --- |
| `projectionRevisionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `projectionKey` | `string` | Yes |
| `profile` | `enum` | Yes |
| `profileVersion` | `string` | Yes |
| `subjectRefs` | `List[EntityRef]` | Yes |
| `inputRefs` | `List[EvidenceRef]` | Yes |
| `ruleDigest` | `Digest` | Yes |
| `asOf` | `Timestamp` | Yes |
| `generatedAt` | `Timestamp` | Yes |
| `coverage` | `List[Coverage]` | Yes |
| `value` | `JsonValue` | Yes |

### Snapshot

Immutable closed manifest and contents. CapturedAt never replaces provider/source time. Access remains checked on reads/exports.

**Owner:** application retained capture. **Module:** foundation. **Identity:** `workspaceId + snapshotId`.

| Field | Type | Required |
| --- | --- | --- |
| `snapshotId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `kind` | `enum` | Yes |
| `subjectRefs` | `List[EntityRef]` | Yes |
| `capturedAt` | `Timestamp` | Yes |
| `manifestDigest` | `Digest` | Yes |
| `sourceRevisionIds` | `List[Id]` | Yes |
| `observationIds` | `List[Id]` | Yes |
| `projectionRevisionIds` | `List[Id]` | Yes |
| `readAttempts` | `List[ReadAttempt]` | Yes |
| `coverage` | `List[Coverage]` | Yes |
| `contents` | `JsonValue` | Yes |
| `captureStartedAt` | `Timestamp` | Yes |
| `captureFinishedAt` | `Timestamp` | Yes |

### WorkItem

Local operator workflow over typed domain targets; completion does not establish provider recovery or remediation.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId + workItemId`.

| Field | Type | Required |
| --- | --- | --- |
| `workItemId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `title` | `string` | Yes |
| `targets` | `List[EntityRef]` | Yes |
| `state` | `enum` | Yes |
| `owner` | `AssigneeRef or null` | Yes |
| `snoozedUntil` | `Timestamp or null` | Yes |
| `resolutionEvidence` | `List[EvidenceRef]` | Yes |
| `actions` | `List[WorkAction]` | Yes |
| `priority` | `string` | Yes |
| `dueAt` | `Timestamp or null` | Yes |
| `verificationState` | `enum` | Yes |
| `verificationEvidence` | `List[EvidenceRef]` | Yes |

### Command

Durable intent and receipt; conditional local admission is not an AWS transaction. Unknown remote outcomes are reconciled without inventing success.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId + commandId`.

| Field | Type | Required |
| --- | --- | --- |
| `commandId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `operation` | `string` | Yes |
| `subjectRefs` | `List[EntityRef]` | Yes |
| `actor` | `ActorRef` | Yes |
| `clientToken` | `string` | Yes |
| `requestDigest` | `Digest` | Yes |
| `expectedVersion` | `Version or null` | Yes |
| `acceptedAt` | `Timestamp` | Yes |
| `state` | `enum` | Yes |
| `attempts` | `List[CommandAttempt]` | Yes |
| `effects` | `List[ExternalOperationRef]` | Yes |
| `resultRefs` | `List[EntityRef]` | Yes |
| `replayExpiresAt` | `Timestamp` | Yes |

### System

Business system. Provider system aliases are explicit; local metadata changes do not mutate AWS.

**Owner:** application. **Module:** workload. **Identity:** `workspaceId + systemId`.

| Field | Type | Required |
| --- | --- | --- |
| `systemId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `providerBindings` | `List[ProviderBinding]` | Yes |

### UserJourney

A user journey belongs to one system; its service set is derived from Service.memberships.

**Owner:** application. **Module:** workload. **Identity:** `workspaceId + userJourneyId`.

| Field | Type | Required |
| --- | --- | --- |
| `userJourneyId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `systemId` | `Id` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `providerBindings` | `List[ProviderBinding]` | Yes |

### Service

Business workload boundary, distinct from an AWS service family and a RegisteredService integration.

**Owner:** application. **Module:** workload. **Identity:** `workspaceId + serviceId`.

| Field | Type | Required |
| --- | --- | --- |
| `serviceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `memberships` | `List[ServiceMembership]` | Yes |
| `resourceIds` | `List[Id]` | Yes |
| `providerBindings` | `List[ProviderBinding]` | Yes |

### Dependency

Scoped service dependency. Provider classification and local governance have separate authority and version ownership.

**Owner:** observed plus local governance. **Module:** workload. **Identity:** `workspaceId + serviceId + dependencyId`.

| Field | Type | Required |
| --- | --- | --- |
| `dependencyId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `serviceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `targetResourceId` | `Id or null` | Yes |
| `targetServiceId` | `Id or null` | Yes |
| `rawClassification` | `string or null` | Yes |
| `selectedObservationId` | `Id or null` | Yes |
| `governance` | `LocalDecision` | Yes |

### HealthEvent

Shared provider Health event identity. EventBridge envelope IDs and recipient accounts are not this identity.

**Owner:** observed. **Module:** health. **Identity:** `workspaceId + healthEventId`.

| Field | Type | Required |
| --- | --- | --- |
| `healthEventId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `eventArn` | `string` | Yes |
| `eventTypeCode` | `string` | Yes |
| `serviceCode` | `string` | Yes |
| `impactedRegion` | `string or null` | Yes |
| `rawScopeCode` | `string or null` | Yes |
| `selectedSourceRevisionId` | `Id` | Yes |

### EventContext

Public/account/organization-summary evidence partition. Context-specific state never leaks into another context.

**Owner:** observed. **Module:** health. **Identity:** `workspaceId + healthEventId + kind + contextKey`.

| Field | Type | Required |
| --- | --- | --- |
| `eventContextId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `healthEventId` | `Id` | Yes |
| `kind` | `enum` | Yes |
| `contextKey` | `string` | Yes |
| `accountId` | `string or null` | Yes |
| `organizationId` | `string or null` | Yes |
| `selectedObservationId` | `Id or null` | Yes |
| `rawProviderStatus` | `string or null` | Yes |

### EntityImpact

Event-relative affected-entity record, not an inventory Resource or a global health state.

**Owner:** observed. **Module:** health. **Identity:** `workspaceId + eventContextId + scoped provider entity key`.

| Field | Type | Required |
| --- | --- | --- |
| `entityImpactId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `eventContextId` | `Id` | Yes |
| `healthEntityArn` | `string or null` | Yes |
| `entityValue` | `string or null` | Yes |
| `selectedObservationId` | `Id` | Yes |
| `rawProviderStatus` | `string or null` | Yes |
| `resourceMatches` | `List[ResourceMatch]` | Yes |

### Communication

Validated logical Health communication grouping, preserving conflicting pages and per-recipient delivery observations.

**Owner:** derived grouping. **Module:** health. **Identity:** `workspaceId + communicationId`.

| Field | Type | Required |
| --- | --- | --- |
| `communicationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `eventContextId` | `Id` | Yes |
| `notificationAccountContext` | `string or null` | Yes |
| `validatedBaseId` | `string or null` | Yes |
| `groupingRuleDigest` | `Digest` | Yes |
| `assemblyState` | `enum` | Yes |
| `pages` | `List[CommunicationPage]` | Yes |

### LifecycleEntry

Provider lifecycle catalog entry has no established stable provider ID; retain snapshot identity and explicit match provenance.

**Owner:** observed local identity. **Module:** health. **Identity:** `workspaceId + lifecycleEntryId`.

| Field | Type | Required |
| --- | --- | --- |
| `lifecycleEntryId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `catalogSnapshotId` | `Id` | Yes |
| `sourceRevisionId` | `Id` | Yes |
| `serviceCode` | `string` | Yes |
| `title` | `string` | Yes |
| `versionLabel` | `string or null` | Yes |
| `recommendedVersion` | `string or null` | Yes |
| `milestones` | `List[LifecycleMilestone]` | Yes |

### ComponentDeployment

An observed installed component/version on a resource, with explicit inventory provenance.

**Owner:** observed inventory. **Module:** health. **Identity:** `workspaceId + componentDeploymentId`.

| Field | Type | Required |
| --- | --- | --- |
| `componentDeploymentId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `resourceId` | `Id` | Yes |
| `componentKind` | `string` | Yes |
| `versionLabel` | `string` | Yes |
| `observationId` | `Id` | Yes |

### ResiliencePolicy

Provider resilience policy. Configured components stay optional; latency is not invented as a native policy component.

**Owner:** observed. **Module:** resilience. **Identity:** `workspaceId + resiliencePolicyId`.

| Field | Type | Required |
| --- | --- | --- |
| `resiliencePolicyId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `name` | `string` | Yes |
| `selectedObservationId` | `Id` | Yes |
| `components` | `List[PolicyComponent]` | Yes |
| `providerUpdatedAt` | `Timestamp or null` | Yes |

### ResilienceAssessment

Native service-scoped assessment execution; execution success, posture and runtime health remain independent.

**Owner:** observed. **Module:** resilience. **Identity:** `workspaceId + serviceId + resilienceAssessmentId`.

| Field | Type | Required |
| --- | --- | --- |
| `resilienceAssessmentId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `serviceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `rawExecutionStatus` | `string or null` | Yes |
| `selectedObservationId` | `Id or null` | Yes |
| `policyContextSnapshotId` | `Id or null` | Yes |
| `selectedPostureProjectionId` | `Id or null` | Yes |

### Finding

Service-scoped finding with no mandatory assessment foreign key. Detail absence is distinct from zero suggestions.

**Owner:** observed. **Module:** resilience. **Identity:** `workspaceId + serviceId + findingId`.

| Field | Type | Required |
| --- | --- | --- |
| `findingId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `serviceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `selectedSummaryObservationId` | `Id or null` | Yes |
| `selectedDetailObservationId` | `Id or null` | Yes |
| `currentCaptureCollectionId` | `Id or null` | Yes |
| `rawDisposition` | `string or null` | Yes |
| `rawSeverity` | `string or null` | Yes |
| `recommendationPresence` | `enum` | Yes |
| `recommendationIds` | `List[Id] or null` | Yes |

### Recommendation

Immutable suggested change anchored to one finding detail observation, group and ordinal. Later changed source content is a new recommendation.

**Owner:** immutable evidence plus local enrichment. **Module:** resilience. **Identity:** `workspaceId + serviceId + findingId + detail observation + group + ordinal`.

| Field | Type | Required |
| --- | --- | --- |
| `recommendationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `serviceId` | `Id` | Yes |
| `findingId` | `Id` | Yes |
| `findingDetailObservationId` | `Id` | Yes |
| `sourceRevisionId` | `Id` | Yes |
| `groupKey` | `string` | Yes |
| `ordinal` | `integer` | Yes |
| `suggestion` | `JsonValue` | Yes |
| `enrichment` | `RecommendationEnrichment` | Yes |

### AgentSpace

AWS workspace resource inside the application Workspace. Never merge it with the product authorization boundary.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId`.

| Field | Type | Required |
| --- | --- | --- |
| `agentSpaceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `name` | `string` | Yes |
| `selectedObservationId` | `Id` | Yes |
| `associations` | `List[AgentAssociation]` | Yes |

### Investigation

Native Task with taskType INVESTIGATION plus observed execution memberships and result views; no invented native GetInvestigation contract.

**Owner:** observed aggregate. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId + native taskId`.

| Field | Type | Required |
| --- | --- | --- |
| `investigationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `title` | `string` | Yes |
| `rawTaskStatus` | `string` | Yes |
| `nativeTaskVersion` | `Version or null` | Yes |
| `selectedTaskObservationId` | `Id` | Yes |
| `executionPointerIdentity` | `SourceIdentity or null` | Yes |
| `executionMemberships` | `List[TaskExecutionMembership]` | Yes |
| `externalReference` | `ExternalReference or null` | Yes |
| `primaryTaskIdentity` | `SourceIdentity or null` | Yes |

### Execution

Native DevOps execution in an AgentSpace; task membership is an observed relation, not a single foreign key.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId + native executionId`.

| Field | Type | Required |
| --- | --- | --- |
| `executionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `parentExecutionIdentity` | `SourceIdentity or null` | Yes |
| `rawExecutionStatus` | `string` | Yes |
| `agentSubTask` | `string` | Yes |
| `selectedObservationId` | `Id` | Yes |

### JournalRecord

Stable journal envelope identity with retained source revisions. Content stays arbitrary JSON; no assumed root-cause schema.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId + executionId + native recordId`.

| Field | Type | Required |
| --- | --- | --- |
| `journalRecordId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `executionId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `recordType` | `string` | Yes |
| `selectedSourceRevisionId` | `Id` | Yes |
| `selectedObservationId` | `Id` | Yes |

### ApprovalRequest

Approval decision and resume are separate commands; neither is evidence of tool execution success.

**Owner:** observed control request. **Module:** investigation. **Identity:** `workspaceId + approvalRequestId`.

| Field | Type | Required |
| --- | --- | --- |
| `approvalRequestId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `executionId` | `Id` | Yes |
| `nativeApprovalId` | `string` | Yes |
| `requestSourceRevisionId` | `Id` | Yes |
| `selectedObservationId` | `Id` | Yes |
| `rawState` | `string` | Yes |
| `actionDigest` | `Digest` | Yes |
| `decisionCommandIds` | `List[Id]` | Yes |
| `resumeCommandIds` | `List[Id]` | Yes |

### Asset

Native asset root; exact versions and files retain immutable source/content references and availability.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + assetId`.

| Field | Type | Required |
| --- | --- | --- |
| `assetId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `assetType` | `string` | Yes |
| `name` | `string` | Yes |
| `versions` | `List[AssetVersion]` | Yes |

### Scenario

Editable scenario metadata and draft; executions reference a published immutable ScenarioRevision.

**Owner:** application. **Module:** workflow. **Identity:** `workspaceId + scenarioId`.

| Field | Type | Required |
| --- | --- | --- |
| `scenarioId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `localUpdatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `draftDefinition` | `ScenarioDraft` | Yes |
| `defaultRevisionId` | `Id or null` | Yes |
| `archived` | `boolean` | Yes |

### ScenarioRevision

Validated immutable definition with complete operation/schema locks. Alias changes cannot change published meaning.

**Owner:** application immutable publication. **Module:** workflow. **Identity:** `workspaceId + scenarioId + scenarioRevisionId`.

| Field | Type | Required |
| --- | --- | --- |
| `scenarioRevisionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `scenarioId` | `Id` | Yes |
| `revisionNumber` | `Version` | Yes |
| `publishedAt` | `Timestamp` | Yes |
| `digest` | `Digest` | Yes |
| `definition` | `ScenarioDefinition` | Yes |

### Run

An admitted workflow execution; its phase, technical outcome, verdict and finalization remain separate.

**Owner:** application execution. **Module:** workflow. **Identity:** `workspaceId + runId`.

| Field | Type | Required |
| --- | --- | --- |
| `runId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `scenarioRevisionId` | `Id` | Yes |
| `inputSnapshotId` | `Id` | Yes |
| `phase` | `enum` | Yes |
| `executionOutcome` | `enum` | Yes |
| `assessmentVerdict` | `enum` | Yes |
| `assessmentFinality` | `enum` | Yes |
| `finalizationState` | `enum` | Yes |
| `effectState` | `enum` | Yes |
| `cancellationIntent` | `CancellationIntent or null` | Yes |
| `projectionVersion` | `Version` | Yes |
| `admittedAt` | `Timestamp` | Yes |
| `terminalAt` | `Timestamp or null` | Yes |
| `reducerVersion` | `string` | Yes |
| `asOfSequence` | `integer` | Yes |

### StepRun

Run-owned step lifecycle. Selection of an attempt is explicit; retry history is retained.

**Owner:** application execution. **Module:** workflow. **Identity:** `workspaceId + runId + stepKey`.

| Field | Type | Required |
| --- | --- | --- |
| `stepRunId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `runId` | `Id` | Yes |
| `stepKey` | `Id` | Yes |
| `selectedAttemptNo` | `Version or null` | Yes |
| `skipReason` | `string or null` | Yes |
| `phase` | `enum` | Yes |
| `outcome` | `enum or null` | Yes |

### StepAttempt

Immutable settled execution facts; late reconciliation adds observations without editing a sealed attempt.

**Owner:** application execution facts. **Module:** workflow. **Identity:** `workspaceId + runId + stepRunId + attemptNo`.

| Field | Type | Required |
| --- | --- | --- |
| `stepAttemptId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `runId` | `Id` | Yes |
| `stepRunId` | `Id` | Yes |
| `attemptNo` | `Version` | Yes |
| `dispatchKey` | `Id` | Yes |
| `outcome` | `enum` | Yes |
| `startedAt` | `Timestamp` | Yes |
| `settledAt` | `Timestamp or null` | Yes |
| `checkResult` | `CheckResult or null` | Yes |
| `externalOperations` | `List[ExternalOperationRef]` | Yes |
| `evidenceRefs` | `List[EvidenceRef]` | Yes |

### Experiment

Native AWS FIS experiment, possibly linked to a workflow attempt but independently observable. Actions are provider-owned named values.

**Owner:** observed. **Module:** fis. **Identity:** `workspaceId + experimentId`.

| Field | Type | Required |
| --- | --- | --- |
| `experimentId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `templateSourceRevisionId` | `Id or null` | Yes |
| `selectedObservationId` | `Id` | Yes |
| `rawExperimentState` | `string` | Yes |
| `actions` | `List[FISAction]` | Yes |
| `targetMemberships` | `List[TargetMembership]` | Yes |
| `resolutionCoverage` | `Coverage` | Yes |
| `report` | `FISReport` | Yes |

## Owned values and scalar contracts

Owned values have identity only within their owner or their pinned revision. Naming a shape does not create another CRUD resource. ReadAttempt, StepRun and StepAttempt remain explicit entities because their lifecycle and references require independent tracking.

| Shape | Meaning |
| --- | --- |
| `Id` | string |
| `Timestamp` | Epoch seconds, millisecond precision. Validators must use decimal arithmetic before ordering; reject higher precision. |
| `Version` | integer |
| `Digest` | string |
| `StringMap` | object |
| `JsonValue` | Retained native document content may be any JSON value; strict write DTOs never reuse this as their entire request. |
| `EntityRef` | An application identity in the containing workspace. Resolution must enforce the workspace, entity kind and parent ownership. |
| `OwningScope` | Resource owner, independent of the principal/connection used to observe it. Null is explicit global/not-applicable, never inferred from delivery recipient. |
| `SourceIdentity` | Stable native identity or explicit provisional source identity. Encode the complete tuple, never delimiter-join opaque components. Provider ARN aliases are preserved separately. |
| `ActorRef` | Authenticated human/service identity supplied by trusted runtime, not selected by request body. |
| `ArtifactRef` | Durable content locator with version and digest. A signed download URL is resolved separately and is never identity. |
| `EvidenceRef` | Immutable evidence reference with explicit type, in the same workspace. |
| `FieldPresence` | Presence is independent of value. Omitted detail cannot be converted into an empty collection. |
| `Coverage` | A bounded claim about a named query and time window; dimensions remain independent. |
| `CollectionQuery` | Exact request scope and declared question; pagination is not a universal proof of completeness. |
| `ReadError` | Observed technical/authorization failure; never substitute zero rows for failure. |
| `ProviderBinding` | Explicit observed relationship between a canonical entity and provider object. Importing/binding never grants remote write authority. |
| `ResourceMatch` | Explicit evidence-backed match, including ambiguity. Identity is not inferred solely from a display string. |
| `OrganizationMembership` | External, time-bounded organization membership; unrelated to notification recipients. |
| `OrganizationAccess` | Observed AWS Health organization integration status. Configuration, access and collection coverage are distinct. |
| `ServiceMembership` | Sole writable workload membership authority is Service.memberships. Reverse journey/system service lists are projections. |
| `LocalDecision` | Independently versioned operator metadata; cannot rewrite provider evidence. |
| `WorkAction` | Immutable append-only operator action owned by a WorkItem; no standalone CRUD root. |
| `CommandAttempt` | Owned dispatch/reconciliation attempt. Acceptance, remote effect and local completion are independent. |
| `ExternalOperationRef` | Provider effect identity may be unknown after a lost response. originEffectKey exists before dispatch and remains stable. |
| `EventDescription` | Localized text belongs to an event revision, not a mutable global event field. |
| `CommunicationPage` | An immutable candidate page, not an independently writable entity. Conflicting candidates are retained, not overwritten. |
| `LifecycleMilestone` | Identity is milestoneKey within a pinned catalog revision. Raw provider date preserves date precision. |
| `PolicyComponent` | Only reviewed native component families; optional configured components determine the assessment denominator. |
| `PolicyContext` | Frozen selection of assignment and effective-target evidence. Captured context is not proof of the exact AWS-evaluated policy revision. |
| `RecommendationEnrichment` | Local estimate/owner/workflow with its own revision, independent of immutable suggestion evidence. |
| `AgentAssociation` | Provider-owned scoped association, never a business Service or product Connection. Built-in serviceId aws need not resolve to a registered provider. |
| `TaskExecutionMembership` | Observed request/response association, not inferred ownership. An Execution has no single investigationId. |
| `ExternalReference` | Native linked-incident reference; may remain unresolved after its integration disappears. |
| `AssetVersion` | Exact provider asset version with retained source revision. latest is never an archival reference. |
| `AssetFile` | A file is identified by owning asset version and exact path, including case. |
| `GraphNode` | Snapshot-owned node; unknown/inferred identity remains qualified. |
| `GraphEdge` | Snapshot-owned typed edge. Causal claim, dependency, provider topology and sequence are different meanings. |
| `GraphContents` | Nodes/edges belong to one immutable capture. Unresolved endpoints use explicitly marked nodes, never fabricated resources. |
| `OperationLock` | Publish resolves exact implementation and schema digests; execution never re-resolves a mutable alias. |
| `StepDefinition` | Owned scenario-revision step with stable stepKey. Native FIS actions are not these workflow steps. |
| `ScenarioDefinition` | Bounded main and finalizer DAGs; language/operation contracts are pinned at publication. |
| `Admission` | Immutable run inputs, capabilities and criterion denominator. References grant no permission; trusted binding restricts effects. |
| `CheckResult` | Final immutable evaluation of one check. Missing evidence is not false, and technical success is not PASS. |
| `CancellationIntent` | First accepted intent is monotonic. Local cancellation cannot prove remote cessation. |
| `CriterionResult` | Assessment denominator is frozen; missing/skipped/error checks remain INCONCLUSIVE. |
| `Evaluation` | A new evaluation never overwrites the sealed run/experiment result it re-examines. |
| `LifecycleExposure` | Derived applicability with exact deployment, catalog revision, milestone and matching rule. |
| `InvestigationResult` | Phase-scoped selected result; completion events from another phase cannot replace it. |
| `StateDimension` | One independently meaningful status backed by explicit evidence. |
| `ServiceStatus` | Separate dimensions, selected policy context and explicit reasons. No universal healthy/successful flag. |
| `WorkspaceSummary` | One denominator of distinct authorized services. No denominator yields null percentage, not zero or 100. |
| `FISAction` | Native named action owned by an Experiment. Its state is read-only and cannot be stopped/restarted individually. |
| `TargetMembership` | Run-scoped resolved selection, never proof that fault was applied. Pod/container choices are different identity layers. |
| `FISReport` | Configured, absent configuration, unobserved and known report readiness are distinct. |
| `WorkflowPolicies` | Main/finalization budgets and trusted deployment concurrency are independent. |
| `BindingDeclaration` | Authoring declaration resolved against an authorized connection at admission. |
| `RetryPolicy` | Bounded read retries. Mutating retries require trusted adapter capability and resolved previous effect. |
| `ScenarioDraft` | Editable authoring document. Trusted publication resolves operation and schema locks; authors cannot grant capabilities by supplying a lock. |
| `ResolvedBinding` | Trusted admitted mapping from a declaration to a connection and constrained effect scope. A provider identity alone is not an access grant. |
| `EvidenceLocator` | Optional exact fragment attribution: JSON Pointer, asset path, or half-open Unicode code-point text offsets. Omitted locator means the entire retained value. |
| `RecommendationEstimate` | Local estimate with declared amount/currency/basis, complexity, source, time and confidence; separate from provider suggested-change evidence. |
| `AssigneeRef` | Resolved directory identity assigned to local work. A team/group is an assignee, never an authenticated audit actor. |

## Relationship register

All multiplicities describe the logical model; a partial cache can contain unresolved references. The full diagram is [complete-model.svg](../diagrams/complete-model.svg).

| From | Cardinality | To | Cardinality | Meaning |
| --- | --- | --- | --- | --- |
| Workspace | 1 | Connection | 0..* | scopes |
| Workspace | 1 | System | 0..* | catalogues |
| Workspace | 1 | WorkItem | 0..* | tracks |
| Connection | 1 | Collection | 0..* | access path |
| Collection | 1 | ReadAttempt | 0..* | owns |
| ReadAttempt | 0..1 | Observation | 0..* | records |
| SourceRevision | 1 | Observation | 0..* | observed as |
| Observation | 0..* | ProjectionRevision | 0..* | immutable inputs |
| SourceRevision | 0..* | ProjectionRevision | 0..* | immutable inputs |
| ProjectionRevision | 0..* | Snapshot | 0..* | pins |
| SourceRevision | 0..* | Snapshot | 0..* | pins |
| Command | 0..* | Observation | 0..* | reconciled by |
| Resource | 1 | ComponentDeployment | 0..* | hosts |
| System | 1 | UserJourney | 0..* | contains |
| System | 0..* | Service | 0..* | membership value |
| UserJourney | 0..* | Service | 0..* | membership value |
| Service | 0..* | Resource | 0..* | catalogue link |
| Service | 1 | Dependency | 0..* | scopes |
| HealthEvent | 1 | EventContext | 0..* | contextualized as |
| EventContext | 1 | EntityImpact | 0..* | qualified impacts |
| EventContext | 1 | Communication | 0..* | receives |
| EntityImpact | 0..* | Resource | 0..* | explicit match |
| Snapshot | 1 | LifecycleEntry | 0..* | catalogue capture |
| LifecycleEntry | 0..* | ProjectionRevision | 0..* | exposure input |
| ComponentDeployment | 0..* | ProjectionRevision | 0..* | exposure input |
| Service | 1 | ResilienceAssessment | 0..* | assessed by |
| Service | 1 | Finding | 0..* | scopes |
| Finding | 1 | Recommendation | 0..* | detail suggestions |
| ResiliencePolicy | 0..* | Snapshot | 0..* | captured context |
| Snapshot | 0..1 | ResilienceAssessment | 0..* | context evidence |
| AgentSpace | 1 | Investigation | 0..* | scopes |
| AgentSpace | 1 | Execution | 0..* | scopes |
| Investigation | 0..* | Execution | 0..* | observed memberships |
| Execution | 1 | JournalRecord | 0..* | publishes |
| Execution | 1 | ApprovalRequest | 0..* | requests |
| ApprovalRequest | 0..1 | Command | 0..* | decision or resume |
| AgentSpace | 1 | Asset | 0..* | owns |
| Investigation | 0..* | Snapshot | 0..* | historical subjects |
| Scenario | 1 | ScenarioRevision | 0..* | publishes |
| ScenarioRevision | 1 | Run | 0..* | executed as |
| Snapshot | 1 | Run | 0..* | pinned admission |
| Run | 1 | StepRun | 1..* | owns |
| StepRun | 1 | StepAttempt | 0..* | attempts |
| StepAttempt | 0..* | Experiment | 0..* | external effect reference |
| StepAttempt | 0..* | ResilienceAssessment | 0..* | external effect reference |
| WorkItem | 0..* | Command | 0..* | related intents |
