# Entity and value reference

Generated from [schema.json](schema.json). Edit the schema, then run `python tools/render_model.py` from this package. The editable layout is [model.drawio](../diagrams/model.drawio); generation preserves its geometry and waypoints. [MODEL.md](../MODEL.md) defines the invariants and ownership rules that JSON Schema cannot express.

The model contains **36 entities**. Every entity carries `version`, `createdAt` and `updatedAt`. Every entity except Workspace also carries `workspaceId`. A stable entity identity and its retained versions belong to the same entity type.

## Common version contract

| Property | Contract |
| --- | --- |
| First version | `1` |
| Next version | Current version plus `1` |
| Writes | Append next version under an atomic expectedVersion check; stored versions never change. |
| Exact historical reference | `EntityRef(kind,id,version)` |
| Live identity reference | `EntityIdentity(kind,id), explicitly live and never a historical pin` |
| Provider version | Separate domain fact; never substitutes for version. |

Write authority determines who may append the next version. Sealing rules constrain an entity lifecycle; they do not create an exception to immutable retained versions. An entity remains versioned even when it is normally created once or has already reached a terminal state.

## Entity index

| Module | Entity | Write authority | Identity |
| --- | --- | --- | --- |
| foundation | [Workspace](#workspace) | `APPLICATION` | `workspaceId` |
| foundation | [Connection](#connection) | `APPLICATION` | `workspaceId + connectionId` |
| foundation | [Resource](#resource) | `COLLECTOR` | `workspaceId + resourceId` |
| foundation | [Collection](#collection) | `COLLECTOR` | `workspaceId + collectionId` |
| foundation | [ReadAttempt](#readattempt) | `COLLECTOR` | `workspaceId + collectionId + readAttemptId` |
| foundation | [Source](#source) | `COLLECTOR` | `workspaceId + sourceId` |
| foundation | [Observation](#observation) | `COLLECTOR` | `workspaceId + observationId` |
| foundation | [Projection](#projection) | `DERIVATION` | `workspaceId + projectionId` |
| foundation | [Snapshot](#snapshot) | `APPLICATION` | `workspaceId + snapshotId` |
| foundation | [WorkItem](#workitem) | `APPLICATION` | `workspaceId + workItemId` |
| foundation | [Command](#command) | `APPLICATION` | `workspaceId + commandId` |
| workload | [System](#system) | `APPLICATION` | `workspaceId + systemId` |
| workload | [UserJourney](#userjourney) | `APPLICATION` | `workspaceId + userJourneyId` |
| workload | [Service](#service) | `APPLICATION` | `workspaceId + serviceId` |
| workload | [Dependency](#dependency) | `MIXED` | `workspaceId + serviceId + dependencyId` |
| health | [HealthEvent](#healthevent) | `COLLECTOR` | `workspaceId + healthEventId` |
| health | [EventContext](#eventcontext) | `COLLECTOR` | `workspaceId + healthEventId + kind + contextKey` |
| health | [EntityImpact](#entityimpact) | `COLLECTOR` | `workspaceId + eventContextId + scoped provider entity key` |
| health | [Communication](#communication) | `DERIVATION` | `workspaceId + communicationId` |
| health | [LifecycleEntry](#lifecycleentry) | `COLLECTOR` | `workspaceId + lifecycleEntryId` |
| health | [ComponentDeployment](#componentdeployment) | `COLLECTOR` | `workspaceId + componentDeploymentId` |
| resilience | [ResiliencePolicy](#resiliencepolicy) | `COLLECTOR` | `workspaceId + resiliencePolicyId` |
| resilience | [ResilienceAssessment](#resilienceassessment) | `COLLECTOR` | `workspaceId + serviceId + resilienceAssessmentId` |
| resilience | [Finding](#finding) | `COLLECTOR` | `workspaceId + serviceId + findingId` |
| resilience | [Recommendation](#recommendation) | `MIXED` | `workspaceId + serviceId + findingId + exact source reference + groupKey + ordinal (unless a stable native key is available)` |
| investigation | [AgentSpace](#agentspace) | `COLLECTOR` | `workspaceId + agentSpaceId` |
| investigation | [Investigation](#investigation) | `COLLECTOR` | `workspaceId + agentSpaceId + native taskId` |
| investigation | [Execution](#execution) | `COLLECTOR` | `workspaceId + agentSpaceId + native executionId` |
| investigation | [JournalRecord](#journalrecord) | `COLLECTOR` | `workspaceId + agentSpaceId + executionId + native recordId` |
| investigation | [ApprovalRequest](#approvalrequest) | `COLLECTOR` | `workspaceId + approvalRequestId` |
| investigation | [Asset](#asset) | `COLLECTOR` | `workspaceId + assetId` |
| workflow | [Scenario](#scenario) | `APPLICATION` | `workspaceId + scenarioId` |
| workflow | [Run](#run) | `WORKFLOW` | `workspaceId + runId` |
| workflow | [StepRun](#steprun) | `WORKFLOW` | `workspaceId + runId + stepKey` |
| workflow | [StepAttempt](#stepattempt) | `WORKFLOW` | `workspaceId + runId + stepRunId + attemptNo` |
| fis | [Experiment](#experiment) | `COLLECTOR` | `workspaceId + experimentId` |

## Entities

### Workspace

Application authorization and configuration boundary, distinct from AWS AgentSpace.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `enabledModules` | `List[enum]` | Yes |
| `organizationMemberships` | `List[OrganizationMembership]` | Yes |
| `organizationAccess` | `List[OrganizationAccess]` | Yes |

### Connection

Access path/credential reference, not native owner identity. Secrets remain outside the model.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId + connectionId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `connectionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `provider` | `string` | Yes |
| `credentialRef` | `string` | Yes |
| `allowedScopes` | `List[OwningScope]` | Yes |
| `authorizationContextKey` | `string` | Yes |
| `enabled` | `boolean` | Yes |

### Resource

Canonical inventory identity with explicit stable or run-scoped boundary; does not represent all native objects.

**Owner:** observed. **Module:** foundation. **Identity:** `workspaceId + resourceId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `resourceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `identityStability` | `enum` | Yes |
| `incarnationKey` | `string or null` | Yes |
| `selectedObservation` | `EntityRef or null` | Yes |
| `displayName` | `string or null` | Yes |
| `matches` | `List[ResourceMatch]` | Yes |

### Collection

One finite collection with immutable query definitions and changing lifecycle represented by ordinary entity versions. New query definitions require a new collection identity.

**Owner:** collector. **Module:** foundation. **Identity:** `workspaceId + collectionId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `collectionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `connection` | `EntityRef` | Yes |
| `queries` | `List[CollectionQuery]` | Yes |
| `state` | `enum` | Yes |
| `startedAt` | `Timestamp` | Yes |
| `endedAt` | `Timestamp or null` | Yes |
| `coverage` | `List[Coverage]` | Yes |
| `collector` | `ProcessingIdentity` | No |
| `selectionPolicy` | `ProcessingIdentity` | No |

### ReadAttempt

A single request attempt exists even if it returned zero objects or failed. It is immutable once settled.

**Owner:** collector. **Module:** foundation. **Identity:** `workspaceId + collectionId + readAttemptId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Lifecycle changes append versions. A settled/terminal record cannot be reopened; late reconciliation is new evidence and does not rewrite settled facts.

| Field | Type | Required |
| --- | --- | --- |
| `readAttemptId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `collectionId` | `Id` | Yes |
| `queryKey` | `string` | Yes |
| `attemptNo` | `PositiveInteger` | Yes |
| `requestDigest` | `Digest` | Yes |
| `state` | `enum` | Yes |
| `startedAt` | `Timestamp` | Yes |
| `endedAt` | `Timestamp or null` | Yes |
| `providerRequestId` | `string or null` | Yes |
| `returnedCount` | `integer or null` | Yes |
| `nextTokenPresent` | `boolean or null` | Yes |
| `error` | `ReadError or null` | Yes |
| `authorizationContextKey` | `string` | Yes |
| `requestSource` | `EntityRef` | Yes |
| `responseSource` | `EntityRef or null` | Yes |
| `itemErrors` | `List[CollectionItemError]` | No |
| `itemOutcome` | `enum` | No |

### Source

Versioned retained source representation. Stable sourceId is scoped by native identity, representation, profile and source operation, independently of payload digest or provider version. Changed accepted content appends a version; an unchanged poll observes the current version again. Optional normalized views and their normalization provenance are immutable members of this Source version. contentDigest hashes only the retained raw payload/artifact. A changed view or normalization rule appends a Source version even if raw bytes and contentDigest are unchanged; a repeated receipt reuses a version only when raw content, views and rule all agree.

**Owner:** retained evidence. **Module:** foundation. **Identity:** `workspaceId + sourceId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `sourceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
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
| `effectiveTargets` | `EffectiveTargets` | No |
| `eventSubjects` | `List[EventSubject]` | No |
| `subjectState` | `SubjectStateObservation` | No |
| `healthSignal` | `HealthSignalEvidence` | No |
| `postureEvidence` | `PostureEvidence` | No |
| `normalization` | `SourceNormalization` | No |

### Observation

Immutable receipt/read observation of one revision. Repeated polls do not create new logical objects. Event/stream/local receipts may have no ReadAttempt; no native read is fabricated.

**Owner:** collector. **Module:** foundation. **Identity:** `workspaceId + observationId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `observationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `source` | `EntityRef` | Yes |
| `readAttempt` | `EntityRef or null` | Yes |
| `connection` | `EntityRef or null` | Yes |
| `observedAt` | `Timestamp` | Yes |
| `sourceTime` | `Timestamp or null` | Yes |
| `transportTime` | `Timestamp or null` | Yes |
| `expiresAt` | `Timestamp or null` | Yes |
| `authorizationContextKey` | `string` | Yes |
| `receiptKey` | `string or null` | Yes |
| `channel` | `enum` | Yes |

### Projection

Versioned named derived view with exact input references, coverage and rule identity. New inputs or rule versions append an immutable version under the same projectionId.

**Owner:** derived. **Module:** foundation. **Identity:** `workspaceId + projectionId`.

**Write authority:** `DERIVATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `projectionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
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
| `derivation` | `DerivationContext` | No |
| `outputDigest` | `Digest` | No |

### Snapshot

A deliberate retained capture with a closed set of exact entity references and captured contents. Snapshot is a business capture, not a substitute for ordinary entity versioning. A corrected capture appends a Snapshot version; older captures stay unchanged.

**Owner:** application retained capture. **Module:** foundation. **Identity:** `workspaceId + snapshotId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `snapshotId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `kind` | `enum` | Yes |
| `subjectRefs` | `List[EntityRef]` | Yes |
| `capturedAt` | `Timestamp` | Yes |
| `manifestDigest` | `Digest` | Yes |
| `coverage` | `List[Coverage]` | Yes |
| `contents` | `JsonValue` | Yes |
| `captureStartedAt` | `Timestamp` | Yes |
| `captureFinishedAt` | `Timestamp` | Yes |
| `members` | `List[EntityRef]` | Yes |

### WorkItem

Local operator workflow over typed domain targets; completion does not establish provider recovery or remediation.

**Owner:** application. **Module:** foundation. **Identity:** `workspaceId + workItemId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `workItemId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `title` | `string` | Yes |
| `targets` | `List[EntityIdentity]` | Yes |
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

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `commandId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
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
| `requestSource` | `EntityRef` | No |
| `approvalDecision` | `ApprovalDecisionIntent` | No |
| `approvalResume` | `ApprovalResumeIntent` | No |

### System

Business system. Provider system aliases are explicit; local metadata changes do not mutate AWS.

**Owner:** application. **Module:** workload. **Identity:** `workspaceId + systemId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `systemId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `providerBindings` | `List[ProviderBinding]` | Yes |

### UserJourney

A user journey belongs to one system; its service set is derived from Service.memberships.

**Owner:** application. **Module:** workload. **Identity:** `workspaceId + userJourneyId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `userJourneyId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `systemId` | `Id` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `providerBindings` | `List[ProviderBinding]` | Yes |

### Service

Business workload boundary, distinct from an AWS service family and a RegisteredService integration.

**Owner:** application. **Module:** workload. **Identity:** `workspaceId + serviceId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `serviceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `memberships` | `List[ServiceMembership]` | Yes |
| `resourceIds` | `List[Id]` | Yes |
| `providerBindings` | `List[ProviderBinding]` | Yes |

### Dependency

Scoped service dependency. Provider classification and local governance have separate authority and version ownership.

**Owner:** observed plus local governance. **Module:** workload. **Identity:** `workspaceId + serviceId + dependencyId`.

**Write authority:** `MIXED`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `dependencyId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `serviceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `targetResourceId` | `Id or null` | Yes |
| `targetServiceId` | `Id or null` | Yes |
| `rawClassification` | `string or null` | Yes |
| `selectedObservation` | `EntityRef or null` | Yes |
| `governance` | `LocalDecision` | Yes |

### HealthEvent

Shared provider Health event identity. EventBridge envelope IDs and recipient accounts are not this identity.

**Owner:** observed. **Module:** health. **Identity:** `workspaceId + healthEventId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `healthEventId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `eventArn` | `string` | Yes |
| `eventTypeCode` | `string` | Yes |
| `serviceCode` | `string` | Yes |
| `impactedRegion` | `string or null` | Yes |
| `rawScopeCode` | `string or null` | Yes |
| `selectedSource` | `EntityRef` | Yes |

### EventContext

Public/account/organization-summary evidence partition. Context-specific state never leaks into another context.

**Owner:** observed. **Module:** health. **Identity:** `workspaceId + healthEventId + kind + contextKey`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `eventContextId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `healthEventId` | `Id` | Yes |
| `kind` | `enum` | Yes |
| `contextKey` | `string` | Yes |
| `accountId` | `string or null` | Yes |
| `organizationId` | `string or null` | Yes |
| `selectedObservation` | `EntityRef or null` | Yes |
| `rawProviderStatus` | `string or null` | Yes |
| `descriptions` | `List[EventDescription]` | No |

### EntityImpact

Event-relative affected-entity record, not an inventory Resource or a global health state.

**Owner:** observed. **Module:** health. **Identity:** `workspaceId + eventContextId + scoped provider entity key`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `entityImpactId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `eventContextId` | `Id` | Yes |
| `healthEntityArn` | `string or null` | Yes |
| `entityValue` | `string or null` | Yes |
| `selectedObservation` | `EntityRef` | Yes |
| `rawProviderStatus` | `string or null` | Yes |
| `resourceMatches` | `List[ResourceMatch]` | Yes |

### Communication

Validated logical Health communication grouping, preserving conflicting pages and per-recipient delivery observations.

**Owner:** derived grouping. **Module:** health. **Identity:** `workspaceId + communicationId`.

**Write authority:** `DERIVATION`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `communicationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `eventContextId` | `Id` | Yes |
| `notificationAccountContext` | `string or null` | Yes |
| `validatedBaseId` | `string or null` | Yes |
| `groupingRuleDigest` | `Digest` | Yes |
| `assemblyState` | `enum` | Yes |
| `pages` | `List[CommunicationPage]` | Yes |

### LifecycleEntry

Provider lifecycle catalog entry has no established stable provider ID; retain snapshot identity and explicit match provenance.

**Owner:** observed local identity. **Module:** health. **Identity:** `workspaceId + lifecycleEntryId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `lifecycleEntryId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `catalogSnapshot` | `EntityRef` | Yes |
| `source` | `EntityRef` | Yes |
| `serviceCode` | `string` | Yes |
| `title` | `string` | Yes |
| `versionLabel` | `string or null` | Yes |
| `recommendedVersion` | `string or null` | Yes |
| `milestones` | `List[LifecycleMilestone]` | Yes |

### ComponentDeployment

An observed installed component/version on a resource, with explicit inventory provenance.

**Owner:** observed inventory. **Module:** health. **Identity:** `workspaceId + componentDeploymentId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `componentDeploymentId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `resourceId` | `Id` | Yes |
| `componentKind` | `string` | Yes |
| `versionLabel` | `string` | Yes |
| `observation` | `EntityRef` | Yes |

### ResiliencePolicy

Provider resilience policy. Configured components stay optional; latency is not invented as a native policy component.

**Owner:** observed. **Module:** resilience. **Identity:** `workspaceId + resiliencePolicyId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `resiliencePolicyId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `name` | `string` | Yes |
| `selectedObservation` | `EntityRef` | Yes |
| `components` | `List[PolicyComponent]` | Yes |
| `providerUpdatedAt` | `Timestamp or null` | Yes |

### ResilienceAssessment

Native service-scoped assessment execution; execution success, posture and runtime health remain independent.

**Owner:** observed. **Module:** resilience. **Identity:** `workspaceId + serviceId + resilienceAssessmentId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `resilienceAssessmentId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `serviceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `rawExecutionStatus` | `string or null` | Yes |
| `selectedObservation` | `EntityRef or null` | Yes |
| `policyContextSnapshot` | `EntityRef or null` | Yes |
| `selectedPostureProjection` | `EntityRef or null` | Yes |

### Finding

Service-scoped finding with no mandatory assessment foreign key. Detail absence is distinct from zero suggestions.

**Owner:** observed. **Module:** resilience. **Identity:** `workspaceId + serviceId + findingId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `findingId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `serviceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `selectedSummaryObservation` | `EntityRef or null` | Yes |
| `selectedDetailObservation` | `EntityRef or null` | Yes |
| `currentCaptureCollection` | `EntityRef or null` | Yes |
| `rawDisposition` | `string or null` | Yes |
| `rawSeverity` | `string or null` | Yes |
| `recommendationPresence` | `enum` | Yes |
| `recommendationIds` | `List[Id] or null` | Yes |

### Recommendation

Captured suggestion with stable identity across repeated observations of the same Source version and normal versions for local enrichment. Without a native stable key, ordinal is not a join across changed source versions; operator workflow belongs to WorkItem.

**Owner:** immutable evidence plus local enrichment. **Module:** resilience. **Identity:** `workspaceId + serviceId + findingId + exact source reference + groupKey + ordinal (unless a stable native key is available)`.

**Write authority:** `MIXED`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `recommendationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `serviceId` | `Id` | Yes |
| `findingId` | `Id` | Yes |
| `findingDetailObservation` | `EntityRef` | Yes |
| `source` | `EntityRef` | Yes |
| `groupKey` | `string` | Yes |
| `ordinal` | `integer` | Yes |
| `suggestion` | `JsonValue` | Yes |
| `enrichment` | `RecommendationEnrichment` | Yes |
| `normalizedSuggestion` | `RecommendationContent` | No |

### AgentSpace

AWS workspace resource inside the application Workspace. Never merge it with the product authorization boundary.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `agentSpaceId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `name` | `string` | Yes |
| `selectedObservation` | `EntityRef` | Yes |
| `associations` | `List[AgentAssociation]` | Yes |

### Investigation

Native Task with taskType INVESTIGATION plus observed execution memberships and result views; no invented native GetInvestigation contract.

**Owner:** observed aggregate. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId + native taskId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `investigationId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `title` | `string` | Yes |
| `rawTaskStatus` | `string` | Yes |
| `nativeTaskVersion` | `PositiveInteger or null` | Yes |
| `selectedTaskObservation` | `EntityRef` | Yes |
| `executionPointerIdentity` | `SourceIdentity or null` | Yes |
| `executionMemberships` | `List[TaskExecutionMembership]` | Yes |
| `externalReference` | `ExternalReference or null` | Yes |
| `primaryTaskIdentity` | `SourceIdentity or null` | Yes |
| `artifactReferences` | `List[InvestigationArtifactReference]` | No |

### Execution

Native DevOps execution in an AgentSpace; task membership is an observed relation, not a single foreign key.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId + native executionId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `executionId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `parentExecutionIdentity` | `SourceIdentity or null` | Yes |
| `rawExecutionStatus` | `string` | Yes |
| `agentSubTask` | `string` | Yes |
| `selectedObservation` | `EntityRef` | Yes |

### JournalRecord

Stable journal envelope identity with retained source revisions. Content stays arbitrary JSON; no assumed root-cause schema.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + agentSpaceId + executionId + native recordId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `journalRecordId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `executionId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `recordType` | `string` | Yes |
| `selectedSource` | `EntityRef` | Yes |
| `selectedObservation` | `EntityRef` | Yes |
| `nativeAttribution` | `NativeUserAttribution or null` | No |

### ApprovalRequest

Approval decision and resume are separate commands; neither is evidence of tool execution success.

**Owner:** observed control request. **Module:** investigation. **Identity:** `workspaceId + approvalRequestId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `approvalRequestId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `executionId` | `Id` | Yes |
| `nativeApprovalId` | `string` | Yes |
| `requestSource` | `EntityRef` | Yes |
| `selectedObservation` | `EntityRef` | Yes |
| `rawState` | `string` | Yes |
| `actionDigest` | `Digest` | Yes |
| `decisionCommandIds` | `List[Id]` | Yes |
| `resumeCommandIds` | `List[Id]` | Yes |
| `invocation` | `ApprovalInvocation` | No |

### Asset

A versioned asset whose selected native version and exact files are ordinary fields. Asset history uses the same id/version contract as every entity.

**Owner:** observed. **Module:** investigation. **Identity:** `workspaceId + assetId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `assetId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `agentSpaceId` | `Id` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `assetType` | `string` | Yes |
| `name` | `string` | Yes |
| `nativeVersion` | `string` | Yes |
| `source` | `EntityRef` | Yes |
| `files` | `List[AssetFile]` | Yes |

### Scenario

One versioned scenario entity. Draft editing, publication and archival append versions with the same scenarioId. A Run pins an exact PUBLISHED version; current ARCHIVED head blocks new admissions.

**Owner:** application. **Module:** workflow. **Identity:** `workspaceId + scenarioId`.

**Write authority:** `APPLICATION`. **Sealing rule:** Published version content and locks are immutable. Editing opens a later DRAFT version; publishing or archiving appends another version. History is never reopened.

| Field | Type | Required |
| --- | --- | --- |
| `scenarioId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `name` | `string` | Yes |
| `description` | `string` | Yes |
| `state` | `enum` | Yes |
| `definition` | `ScenarioDraft or ScenarioDefinition` | Yes |
| `publishedAt` | `Timestamp or null` | Yes |
| `digest` | `Digest or null` | Yes |

### Run

Versioned admitted workflow execution pinning one exact published Scenario and input Snapshot. Phase, outcome, verdict and finalization remain independent; every state change appends Run.version.

**Owner:** application execution. **Module:** workflow. **Identity:** `workspaceId + runId`.

**Write authority:** `WORKFLOW`. **Sealing rule:** Lifecycle changes append versions. A settled/terminal record cannot be reopened; late reconciliation is new evidence and does not rewrite settled facts.

| Field | Type | Required |
| --- | --- | --- |
| `runId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `scenario` | `EntityRef` | Yes |
| `inputSnapshot` | `EntityRef` | Yes |
| `phase` | `enum` | Yes |
| `executionOutcome` | `enum` | Yes |
| `assessmentVerdict` | `enum` | Yes |
| `assessmentFinality` | `enum` | Yes |
| `finalizationState` | `enum` | Yes |
| `effectState` | `enum` | Yes |
| `cancellationIntent` | `CancellationIntent or null` | Yes |
| `admittedAt` | `Timestamp` | Yes |
| `terminalAt` | `Timestamp or null` | Yes |
| `reducerVersion` | `string` | Yes |
| `asOfSequence` | `integer` | Yes |
| `steps` | `List[EntityRef]` | Yes |
| `evidenceCitations` | `List[RunEvidenceCitation]` | No |

### StepRun

Run-owned step lifecycle. Selection of an attempt is explicit; retry history is retained.

**Owner:** application execution. **Module:** workflow. **Identity:** `workspaceId + runId + stepKey`.

**Write authority:** `WORKFLOW`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `stepRunId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `runId` | `Id` | Yes |
| `stepKey` | `Id` | Yes |
| `skipReason` | `string or null` | Yes |
| `phase` | `enum` | Yes |
| `outcome` | `enum or null` | Yes |
| `selectedAttempt` | `EntityRef or null` | Yes |
| `attempts` | `List[EntityRef]` | Yes |

### StepAttempt

Immutable settled execution facts; late reconciliation adds observations without editing a sealed attempt.

**Owner:** application execution facts. **Module:** workflow. **Identity:** `workspaceId + runId + stepRunId + attemptNo`.

**Write authority:** `WORKFLOW`. **Sealing rule:** Lifecycle changes append versions. A settled/terminal record cannot be reopened; late reconciliation is new evidence and does not rewrite settled facts.

| Field | Type | Required |
| --- | --- | --- |
| `stepAttemptId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `runId` | `Id` | Yes |
| `stepRunId` | `Id` | Yes |
| `attemptNo` | `PositiveInteger` | Yes |
| `dispatchKey` | `Id` | Yes |
| `outcome` | `enum` | Yes |
| `startedAt` | `Timestamp` | Yes |
| `settledAt` | `Timestamp or null` | Yes |
| `checkResult` | `CheckResult or null` | Yes |
| `externalOperations` | `List[ExternalOperationRef]` | Yes |
| `evidenceRefs` | `List[EvidenceRef]` | Yes |
| `recovery` | `AttemptRecovery` | No |

### Experiment

Native AWS FIS experiment, possibly linked to a workflow attempt but independently observable. Actions are provider-owned named values.

**Owner:** observed. **Module:** fis. **Identity:** `workspaceId + experimentId`.

**Write authority:** `COLLECTOR`. **Sealing rule:** Every stored version is immutable. Authorized changes append the next version of the same entity; provider state changes do not rewrite prior versions.

| Field | Type | Required |
| --- | --- | --- |
| `experimentId` | `Id` | Yes |
| `workspaceId` | `Id` | Yes |
| `version` | `Version` | Yes |
| `createdAt` | `Timestamp` | Yes |
| `updatedAt` | `Timestamp` | Yes |
| `identity` | `SourceIdentity` | Yes |
| `templateSource` | `EntityRef or null` | Yes |
| `selectedObservation` | `EntityRef` | Yes |
| `rawExperimentState` | `string` | Yes |
| `actions` | `List[FISAction]` | Yes |
| `targetMemberships` | `List[TargetMembership]` | Yes |
| `resolutionCoverage` | `Coverage` | Yes |
| `report` | `FISReport` | Yes |
| `targetSelections` | `List[FISTargetSelection]` | No |
| `targetSelectionCompleteness` | `enum` | No |
| `actionCompleteness` | `enum` | No |

## Owned values and scalar contracts

Owned values have no independent lifecycle or version stream. `EntityRef` is an exact reference value, not an entity. `EntityIdentity` explicitly means a live identity. A field carrying a historical input uses the exact reference contract.

| Shape | Meaning |
| --- | --- |
| `Id` | string |
| `Timestamp` | Epoch seconds, millisecond precision. Validators must use decimal arithmetic before ordering; reject higher precision. |
| `Version` | Application entity version, monotonically increasing within one stable entity identity. |
| `Digest` | string |
| `StringMap` | object |
| `JsonValue` | Retained native document content may be any JSON value; strict write DTOs never reuse this as their entire request. |
| `EntityRef` | Exact immutable representation of an entity in the containing workspace. Missing version is invalid; resolution never falls back to a current head. This is an owned reference value, not an entity. |
| `OwningScope` | Resource owner, independent of the principal/connection used to observe it. Null is explicit global/not-applicable, never inferred from delivery recipient. |
| `SourceIdentity` | Stable native identity or explicit provisional source identity. Encode the complete tuple, never delimiter-join opaque components. Provider ARN aliases are preserved separately. |
| `ActorRef` | Authenticated human/service identity supplied by trusted runtime, not selected by request body. |
| `ArtifactRef` | Durable content locator with version and digest. A signed download URL is resolved separately and is never identity. |
| `EvidenceRef` | Exact versioned evidence reference, optionally narrowed by a locator. This value never resolves to latest. |
| `FieldPresence` | Presence is independent of value. Omitted detail cannot be converted into an empty collection. |
| `Coverage` | A bounded claim about a named query and time window; dimensions remain independent. |
| `CollectionQuery` | Exact request scope and declared question; pagination is not a universal proof of completeness. |
| `ReadError` | Observed technical/authorization failure; never substitute zero rows for failure. |
| `ProviderBinding` | Explicit observed relationship between a canonical entity and provider object. Importing/binding never grants remote write authority. |
| `ResourceMatch` | Explicit evidence-backed match, including ambiguity. Identity is not inferred solely from a display string. |
| `OrganizationMembership` | External, time-bounded organization membership; unrelated to notification recipients. |
| `OrganizationAccess` | Observed AWS Health organization integration status. Configuration, access and collection coverage are distinct. |
| `ServiceMembership` | Sole writable workload membership authority is Service.memberships. Reverse journey/system service lists are projections. |
| `LocalDecision` | Owned local classification decision with actor and decision time. Changes advance the owning Dependency.version; it has no separate version lifecycle. |
| `WorkAction` | Immutable append-only operator action owned by a WorkItem; no standalone CRUD root. |
| `CommandAttempt` | Owned dispatch/reconciliation attempt. Acceptance, remote effect and local completion are independent. |
| `ExternalOperationRef` | Provider effect identity may be unknown after a lost response. originEffectKey exists before dispatch and remains stable. |
| `EventDescription` | Localized text owned by an EventContext version. source pins the exact contextual detail/stream representation; localeBasis distinguishes request locale from an explicit stream language. Omission of the owning descriptions field means unobserved, not an empty description. |
| `CommunicationPage` | An immutable candidate page, not an independently writable entity. Conflicting candidates are retained, not overwritten. |
| `LifecycleMilestone` | Identity is milestoneKey within a pinned catalog revision. Raw provider date preserves date precision. |
| `PolicyComponent` | Reviewed native component families. Existing target/unit maps and raw disasterRecoveryApproach remain read-tolerant. Optional normalized validates the known metric/unit subset without replacing raw values; missing means no validated view, and unknown native values remain retained. |
| `PolicyContext` | Frozen selection of assignment and effective-target evidence. Captured context is not proof of the exact AWS-evaluated policy revision. |
| `RecommendationEnrichment` | Owned local explanatory metadata and estimate. Changes advance Recommendation.version. Assignment and work state belong to WorkItem only. |
| `AgentAssociation` | Provider-owned scoped association, never a business Service or product Connection. Built-in serviceId aws need not resolve to a registered provider. |
| `TaskExecutionMembership` | Observed request/response association, not inferred ownership. An Execution has no single investigationId. |
| `ExternalReference` | Native linked-incident reference; may remain unresolved after its integration disappears. |
| `AssetFile` | A file is identified by owning asset version and exact path, including case. |
| `GraphNode` | Snapshot-owned node; unknown/inferred identity remains qualified. |
| `GraphEdge` | Snapshot-owned typed edge. Causal claim, dependency, provider topology and sequence are different meanings. |
| `GraphContents` | Nodes/edges belong to one immutable capture. Unresolved endpoints use explicitly marked nodes, never fabricated resources. Named view kinds preserve execution, stream, linked-task, evidence and configuration meaning. New normalized graph ingestion supplies nodeKind, resolution and assertion metadata; absent metadata in legacy captures remains unknown. |
| `OperationLock` | Publish resolves exact implementation and schema digests; execution never re-resolves a mutable alias. |
| `StepDefinition` | Owned scenario-revision step with stable stepKey. Native FIS actions are not these workflow steps. |
| `ScenarioDefinition` | Bounded main and finalizer DAGs; language/operation contracts are pinned at publication. |
| `Admission` | Immutable run inputs, capabilities and criterion denominator. References grant no permission; trusted binding restricts effects. |
| `CheckResult` | Final immutable evaluation of one check. Missing evidence is not false, and technical success is not PASS. |
| `CancellationIntent` | First accepted intent is monotonic. Local cancellation cannot prove remote cessation. |
| `CriterionResult` | Assessment denominator is frozen; missing/skipped/error checks remain INCONCLUSIVE. |
| `Evaluation` | A new evaluation never overwrites the sealed run/experiment result it re-examines. |
| `LifecycleExposure` | Derived applicability with exact deployment, catalog revision, milestone and matching rule. Source confirmed maps to APPLIES, excluded to DOES_NOT_APPLY, and candidate/unknown to UNKNOWN; optional sourceApplicability preserves CANDIDATE separately from UNKNOWN. Missing qualification remains unrecorded, never a confirmed match. |
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
| `EntityIdentity` | A logical entity identity for explicitly live navigation or work targeting. It does not select a historical representation or authorize a lookup. |
| `PositiveInteger` | A positive domain count or ordinal. It is not an entity version or concurrency token. |
| `CollectionItemError` | Owned Health failedSet entry scoped by event ARN and optional affected account. The containing ReadAttempt remains the one native HTTP request; transport failure is ReadAttempt.error. |
| `EffectiveTargetProvenance` | Native source is account ownership, not direct/inherited assignment. A policy name is not an ARN. Resolved identity requires independently retained evidence; absent provenance stays absent. |
| `EffectiveAvailabilityTarget` | One returned effective target. The value is observed, not defaulted; optional provenance preserves only evidence actually supplied. |
| `EffectiveDurationTarget` | One returned effective target. The value is observed, not defaulted; optional provenance preserves only evidence actually supplied. |
| `EffectiveRecoveryApproach` | One returned effective target. The value is observed, not defaulted; optional provenance preserves only evidence actually supplied. |
| `EffectiveTargets` | Service-scoped effectivePolicyValues normalized from the exact containing Source. Eight optional metric keys; missing is not zero. Recovery approaches are strings, durations integers in minutes and availability a percentage. |
| `NormalizedPolicyComponent` | Optional validated known-metric view of one PolicyComponent. Preserve unfamiliar native target keys and DR values in the owner/raw Source; omission of this view does not assert normalization. |
| `AssessmentCorrelation` | Optional observed same-service association. It is local temporal correlation and never asserts that the assessment owns a finding or evaluated the current policy. |
| `RecommendationContent` | One native nested recommendation item. Category identifies its source array; owner groupKey and ordinal preserve grouping and order. Absent suggestedChanges differs from an observed empty array. No provider ID, cost or title is invented. |
| `NativeTopologyProperty` | One returned Resilience Hub EdgeProperty. Known topology types are CONTAINMENT, DATA_FLOW, OBSERVABILITY and PERMISSIONS; unknown native values remain open. An absent topologyType is unknown. Optional label is LLM-inferred provenance, not measured traffic. |
| `SubjectReference` | Exact historical console entity and/or scoped native identity. Unresolved source identity is valid. Names alone are never identifiers. |
| `EventSubject` | Owned event-to-subject relationship with explicit asserted/inferred provenance. Envelope resources alone do not prove a normalized link. |
| `SubjectStateObservation` | Observed subject visibility/lifecycle evidence, retained without deleting historical entity versions. DELETED requires positive deletion evidence; a missing list row or authorization failure is NOT_VISIBLE or UNKNOWN. A historical reference keeps selecting its exact version. |
| `SignalMeasurement` | A named measured signal with an explicit unit; no metric value is inferred from a badge. |
| `HealthSignalEvidence` | Owned external runtime-health observation. Windows, measurement/receipt/expiry times, signal identity and aggregation rule remain explicit. Recomputing a projection never renews this evidence. |
| `PostureComponentOutcome` | Native component outcome with open provider status vocabulary; never convert a missing outcome into success. |
| `NativePostureEvidence` | Native service achievability with component outcomes, observed context and optional qualified assessment correlation. A captured context is not proof of the policy revision evaluated by AWS. |
| `DerivedPostureEvidence` | Derived system/journey attention with distinct contributing services/findings and captured membership evidence. It has no native achievability field; counts derive from distinct referenced identities under the recorded coverage. |
| `PostureEvidence` | NativePostureEvidence / DerivedPostureEvidence |
| `SourceNormalization` | Provenance for optional normalized Source views. inputContentDigest equals the containing raw contentDigest; ruleDigest pins the normalization rule. These members and their outputs belong to the immutable Source version. Raw payload digest does not hash the normalized view; changing a view/rule appends a version even when raw bytes are unchanged. |
| `FISTargetSelection` | Experiment-owned native target-map member. A selector with zero resolved resources still exists. Exact configuration remains in selectorObservation → Source; targetName is opaque, never parsed from a membership ID. |
| `EvidenceWindow` | Event-time half-open interval [start,end). Collection cutoff and observation time are separate; semantic validation enforces start <= end. |
| `TelemetryMetricIdentity` | object |
| `TelemetryQuery` | JsonValue / JsonValue |
| `MetricQueryDefinition` | Application query configuration stored as a versioned Source. Its Source identity/version is the binding identity. The intended event-time window is captured separately for each experiment association; nativeEvidence preserves raw provider context. |
| `MetricSample` | A measured numeric value. Missing samples are absent; they are never silently converted to zero. |
| `MetricObservationValue` | Normalized metric samples bound to an exact query Source version. COMPLETE describes collection, not proof of sufficient source coverage. Query units, period, normalization and event window must agree before numeric assessment. |
| `MetricRecoveryRule` | object |
| `MetricCriterionDefinition` | Pinned numeric criterion, including optional recovery/stability rule. FAIL on missing data is an explicit criterion policy and still requires its declared coverage assumptions; absence is never numeric zero. |
| `ExperimentMetricBinding` | Owned association in an evaluation input capture: exact Experiment, query and criterion Source versions plus event window, timing evidence and accepted observations. It can exist without any Run. |
| `TelemetryEvaluationInput` | Typed captured input for a standalone experiment evaluation. Every referenced record is included in Snapshot.members. Legacy generic evaluation contents remain retained input; they do not establish normalized telemetry bindings. |
| `SealedAttemptValue` | Exact retained resolved-input or checkpoint value and the immutable schema used to validate it. Content is not a scheduler lease, credential or editable input expression. |
| `WorkflowCheckpoint` | Resume checkpoint published in the existing attempt identity/version. Resume does not create a retry attempt. |
| `WorkflowExecutionError` | Technical failure only. A false assessment predicate belongs in CheckResult. Retry eligibility does not authorize replaying a potentially applied effect. |
| `AttemptRecovery` | Durable input/checkpoint/error envelope, owned and versioned by StepAttempt. Absent on legacy captures means not recorded; it does not establish resumability. |
| `RunEvidenceCitation` | Run-owned evidence citation. Evidence stays on the shared Source/Observation spine; exact producer/consumer attempts belong to the same Run. Imported evidence declares origin explicitly and does not invent a producing attempt. |
| `WorkflowObservationValue` | Typed adapter observation result, distinct from the Observation receipt entity. An unavailable value is absent; a completed empty result is explicit. valueSchemaDigest and normalizationDigest pin adapter conversion contracts. |
| `ProcessingIdentity` | Exact application processing implementation or policy identity. Version is the source implementation version, not an entity version; the digest pins its immutable definition. |
| `DerivationContext` | Reviewed derivation method and independently pinned parser/rule/model identities. Null means that component was not used; never attribute application confidence to AWS. |
| `NativeUserAttribution` | Observed native userReference. Preserve the supplied userId and userType, including future provider values. It is not a trusted ActorRef or proof of application authorization. |
| `PublishedConfidence` | Only a confidence value actually published by the cited source; no assumed scale and no conversion to an AWS confidence score. |
| `AssertionMetadata` | Assertion provenance, independent observation and validity clocks, and source-qualified uncertainty. Every explicit assertion cites exact retained evidence, including operator/application-origin evidence. |
| `ApprovalPattern` | Native tool and argument pin value; preserved exactly without guessing wildcard or case-normalization semantics. |
| `ApprovalAction` | Native ApprovalAction wire value; its members are optional in the pinned AWS model. A validated invocation contract separately requires the identifiers actually necessary for dispatch. |
| `ApprovalInvocation` | Normalized observed chat request profile. It is not a universal AWS ApprovalRequest entity. Preserve omitted fields on unsupported requests; only validated invocations can authorize decision/resume dispatch. |
| `ApprovalDecisionIntent` | Reconstructable single-use decision input. The finalPattern must exactly equal the validated requestedPattern selected by the pinned approvalRequest; reusable approvals and widened/narrowed patterns are outside this console operation. Command subjects pin the request, observed Source, Execution and AgentSpace; expectedVersion guards the exact ApprovalRequest. Decision acceptance is not resume or action success. |
| `ApprovalResumeIntent` | Exact decision and request context used for resume. Command subjects pin the request, decision, Execution and AgentSpace; expectedVersion guards that Execution. Decision, resume acceptance, and an observed action outcome are independent. |
| `InvestigationArtifactReference` | Channel-aware source reference; an A2A or journal nativeId is not an Asset ID. Optional asset resolution must be supported by retained evidence. A nearby fetched version is OBSERVED unless consumed-version evidence exists. Unknown media types and distinct absence reasons are preserved. |
| `ActionStageObservation` | One observed stage with its own exact source at the assertion owner. Decision/resume acceptance cannot be relabeled as an effect outcome. |
| `InvestigationAssertion` | Attributed published assertion in an application vocabulary. It neither invents AWS Finding/Hypothesis fields nor reconstructs private reasoning. Content remains faithful to its source; kind, subjects, provenance, disposition and action stage are typed. |
| `InvestigationAssertions` | Typed published-assertion projection. Owner Projection.version and outputDigest pin one immutable rendition; per-item IDs remain stable across renditions. supersedesItemId links a different item in this rendition or an explicitly cited earlier version of the same logical Projection; self-links, dangling targets and cycles reject. |
| `InvestigationTimelineItem` | A timeline item keeps source/evidence/receipt clocks separate. Parent/group links need explicit evidence and a same-rendition target, with no self-links or cycles; timestamps alone do not establish causality. supersedesItemId may target a different item in this rendition or an explicitly cited earlier version of the same logical Projection. Immutable rendition identity comes from the owning Projection version. |
| `InvestigationTimeline` | Typed application timeline. Deterministic same-time ordering is explicitly a local presentation policy, not a provider total-order guarantee. |
| `NormalizationDiagnostic` | Owned normalization diagnostic with raw and fallback values. MISSING means no usable value for that rule; Source.fieldPresence separately preserves absent versus present-null. It is not an entity or proof of complete native-schema validation. |

## Relationship register

All multiplicities describe the logical model; a partial cache can contain unresolved references. The [complete Draw.io atlas](../diagrams/model.drawio) distributes every association over readable detailed sheets. The [overview](../diagrams/complete-model.svg) contains all entities and a selected subset of associations.

| From | Cardinality | To | Cardinality | Meaning |
| --- | --- | --- | --- | --- |
| Workspace | 1 | Connection | 0..* | scopes |
| Workspace | 1 | System | 0..* | catalogues |
| Workspace | 1 | WorkItem | 0..* | tracks |
| Connection | 1 | Collection | 0..* | access path |
| Collection | 1 | ReadAttempt | 0..* | owns |
| ReadAttempt | 0..1 | Observation | 0..* | records |
| Source | 1 | Observation | 0..* | observed as |
| Observation | 0..* | Projection | 0..* | used as immutable input |
| Source | 0..* | Projection | 0..* | used as immutable input |
| Projection | 0..* | Snapshot | 0..* | captured in |
| Source | 0..* | Snapshot | 0..* | captured in |
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
| LifecycleEntry | 0..* | Projection | 0..* | exposure input |
| ComponentDeployment | 0..* | Projection | 0..* | exposure input |
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
| Scenario | 1 | Run | 0..* | published version used by |
| Snapshot | 1 | Run | 0..* | pinned admission |
| Run | 1 | StepRun | 1..* | owns |
| StepRun | 1 | StepAttempt | 0..* | attempts |
| StepAttempt | 0..* | Experiment | 0..* | external effect reference |
| StepAttempt | 0..* | ResilienceAssessment | 0..* | external effect reference |
| WorkItem | 0..* | Command | 0..* | related intents |
