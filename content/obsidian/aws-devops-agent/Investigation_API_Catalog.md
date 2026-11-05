---
title: AWS DevOps Agent API catalog for investigation UI design
id: obsidian-devops-investigation-api-catalog
kind: obsidian-note
product: devops
type: api-reference
created: '2026-11-05'
updated: '2026-11-05'
source_cutoff: '2026-11-05'
api_version: '2026-01-01'
status: schema-verified
tags:
  - aws/devops-agent
  - api
  - data-model
related:
  - '[[Investigation_Data_Model]]'
  - '[[Investigation_UI_Contract]]'
  - '[[Investigation_API_Sources]]'
---

<!-- block: obsidian-devops-investigation-api-catalog-scope -->
# AWS DevOps Agent API catalog

This appendix inventories all **63 operations** in the official service model and extracts the field contracts needed for an investigation UI. It complements [[Investigation_Data_Model]] and [[Investigation_UI_Contract]]. An operation or field inventory is not proof that every web-app behavior has a public API recipe.

The extraction uses the [pinned official Python SDK model](https://raw.githubusercontent.com/boto/botocore/27fc40eff0e85422e62858ee3d2e9a133bdb1038/botocore/data/devops-agent/2026-01-01/service-2.json), API version **2026-01-01**, checked on **5 November 2026** against the official AWS Go/JavaScript Smithy models and [Actions index](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Operations.html). Its **560 shapes** include wrappers, primitive aliases, errors, lists and maps; this is not an entity count. See [[Investigation_API_Sources]] for hashes and reconciliation notes.

**Notation:** requiredness describes the outer wire shape. Cross-field and state validation may still require optional members. An open string or JSON document is not expanded into an invented schema. Use the AWS SDK for serialization, timestamp decoding and binary bodies.

<!-- block: obsidian-devops-investigation-api-catalog-operations -->
## 1. Complete operation inventory

All routes are service-relative. HTTP POST does not imply a write: list operations include POST reads. Empty response fields mean an acknowledgement.

### Agent Space

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [CreateAgentSpace](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateAgentSpace.html) | `POST /v1/agentspaces` | `agentSpace`, `tags` |
| [GetAgentSpace](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAgentSpace.html) | `GET /v1/agentspaces/{agentSpaceId}` | `agentSpace`, `tags` |
| [ListAgentSpaces](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAgentSpaces.html) | `POST /v1/agentspaces/list` | `nextToken`, `agentSpaces` |
| [UpdateAgentSpace](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateAgentSpace.html) | `PATCH /v1/agentspaces/{agentSpaceId}` | `agentSpace` |
| [DeleteAgentSpace](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DeleteAgentSpace.html) | `DELETE /v1/agentspaces/{agentSpaceId}` | Acknowledgement |

### Service registration

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [RegisterService](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_RegisterService.html) | `POST /v1/register/{service}` | `serviceId`, `additionalStep`, `kmsKeyArn`, `tags` |
| [GetService](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetService.html) | `GET /v1/services/{serviceId}` | `service`, `tags` |
| [ListServices](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListServices.html) | `POST /v1/services/list` | `nextToken`, `services` |
| [DeregisterService](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DeregisterService.html) | `DELETE /v1/services/{serviceId}` | Acknowledgement |

### Association and webhook

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [AssociateService](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssociateService.html) | `POST /v1/agentspaces/{agentSpaceId}/associations` | `association`, `webhook` |
| [GetAssociation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssociation.html) | `GET /v1/agentspaces/{agentSpaceId}/associations/{associationId}` | `association` |
| [ListAssociations](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssociations.html) | `POST /v1/agentspaces/{agentSpaceId}/associations/list` | `nextToken`, `associations` |
| [UpdateAssociation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateAssociation.html) | `PATCH /v1/agentspaces/{agentSpaceId}/associations/{associationId}` | `association`, `webhook` |
| [DisassociateService](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DisassociateService.html) | `DELETE /v1/agentspaces/{agentSpaceId}/associations/{associationId}` | Acknowledgement |
| [ValidateAwsAssociations](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ValidateAwsAssociations.html) | `POST /v1/agentspaces/{agentSpaceId}/associations/validate` | Acknowledgement |
| [ListWebhooks](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListWebhooks.html) | `POST /v1/agentspaces/{agentSpaceId}/associations/{associationId}/webhooks/list` | `webhooks` |

### Backlog task

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [CreateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html) | `POST /backlog/agent-space/{agentSpaceId}/tasks` | `task` |
| [GetBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetBacklogTask.html) | `GET /backlog/agent-space/{agentSpaceId}/tasks/{taskId}` | `task` |
| [ListBacklogTasks](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListBacklogTasks.html) | `POST /backlog/agent-space/{agentSpaceId}/tasks/list` | `tasks`, `nextToken` |
| [UpdateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html) | `PATCH /backlog/agent-space/{agentSpaceId}/tasks/{taskId}` | `task` |

### Execution and journal

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [ListExecutions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListExecutions.html) | `POST /journal/agent-space/{agentSpaceId}/executions` | `executions`, `nextToken` |
| [ListJournalRecords](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html) | `POST /journal/agent-space/{agentSpaceId}/journalRecords` | `records`, `nextToken` |

### Chat and approval

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [CreateChat](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateChat.html) | `POST /agents/agent-space/{agentSpaceId}/chat/create` | `executionId`, `createdAt` |
| [ListChats](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListChats.html) | `GET /agents/agent-space/{agentSpaceId}/chat/list` | `executions`, `nextToken` |
| [SendMessage](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessage.html) | `POST /agents/agent-space/{agentSpaceId}/chat/sendMessage` | `events` |
| [ListPendingMessages](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListPendingMessages.html) | `POST /agents/agent-space/{agentSpaceId}/pendingMessages` | `agentSpaceId`, `executionId`, `messages`, `createdAt` |
| [UpdateApprovalAction](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateApprovalAction.html) | `POST /agents/agent-space/{agentSpaceId}/approvals/{approvalId}/update-action` | `approvalId`, `status`, `expiresAt` |

### Goal and recommendation

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [ListGoals](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListGoals.html) | `POST /backlog/agent-space/{agentSpaceId}/goals/list` | `goals`, `nextToken` |
| [UpdateGoal](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateGoal.html) | `PATCH /backlog/agent-space/{agentSpaceId}/goals/{goalId}` | `goal` |
| [GetRecommendation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetRecommendation.html) | `GET /backlog/agent-space/{agentSpaceId}/recommendations/{recommendationId}` | `recommendation` |
| [ListRecommendations](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListRecommendations.html) | `POST /backlog/agent-space/{agentSpaceId}/recommendations/list` | `recommendations`, `nextToken` |
| [UpdateRecommendation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateRecommendation.html) | `PATCH /backlog/agent-space/{agentSpaceId}/recommendations/{recommendationId}` | `recommendation` |

### Asset and file

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [CreateAsset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateAsset.html) | `POST /asset/agent-space/{agentSpaceId}/assets` | `asset` |
| [GetAsset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAsset.html) | `GET /asset/agent-space/{agentSpaceId}/assets/{assetId}` | `asset` |
| [UpdateAsset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateAsset.html) | `PATCH /asset/agent-space/{agentSpaceId}/assets/{assetId}` | `asset` |
| [DeleteAsset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DeleteAsset.html) | `DELETE /asset/agent-space/{agentSpaceId}/assets/{assetId}` | Acknowledgement |
| [ListAssets](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssets.html) | `GET /asset/agent-space/{agentSpaceId}/assets` | `items`, `nextToken` |
| [ListAssetTypes](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssetTypes.html) | `GET /asset/types` | `items`, `nextToken` |
| [ListAssetVersions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssetVersions.html) | `GET /asset/agent-space/{agentSpaceId}/assets/{assetId}/versions` | `items`, `nextToken` |
| [GetAssetContent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetContent.html) | `GET /asset/agent-space/{agentSpaceId}/assets/{assetId}/content` | `content`, `version` |
| [CreateAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateAssetFile.html) | `POST /asset/agent-space/{agentSpaceId}/assets/{assetId}/files/{path+}` | `file` |
| [GetAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetFile.html) | `GET /asset/agent-space/{agentSpaceId}/assets/{assetId}/files/{path+}` | `file` |
| [UpdateAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateAssetFile.html) | `PATCH /asset/agent-space/{agentSpaceId}/assets/{assetId}/files/{path+}` | `file` |
| [DeleteAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DeleteAssetFile.html) | `DELETE /asset/agent-space/{agentSpaceId}/assets/{assetId}/files/{path+}` | Acknowledgement |
| [ListAssetFiles](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssetFiles.html) | `GET /asset/agent-space/{agentSpaceId}/assets/{assetId}/files` | `items`, `nextToken` |

### Trigger

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [CreateTrigger](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateTrigger.html) | `POST /trigger/agent-space/{agentSpaceId}/triggers` | `trigger` |
| [GetTrigger](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetTrigger.html) | `GET /trigger/agent-space/{agentSpaceId}/triggers/{triggerId}` | `trigger` |
| [ListTriggers](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListTriggers.html) | `GET /trigger/agent-space/{agentSpaceId}/triggers` | `items`, `nextToken` |
| [UpdateTrigger](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateTrigger.html) | `PATCH /trigger/agent-space/{agentSpaceId}/triggers/{triggerId}` | `trigger` |
| [DeleteTrigger](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DeleteTrigger.html) | `DELETE /trigger/agent-space/{agentSpaceId}/triggers/{triggerId}` | Acknowledgement |

### Operator application

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [EnableOperatorApp](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_EnableOperatorApp.html) | `POST /v1/agentspaces/{agentSpaceId}/operator` | `agentSpaceId`, `operatorAppUrl`, `iam`, `idc`, `idp` |
| [GetOperatorApp](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetOperatorApp.html) | `GET /v2/agentspaces/{agentSpaceId}/operator` | `operatorAppUrl`, `iam`, `idc`, `idp` |
| [DisableOperatorApp](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DisableOperatorApp.html) | `DELETE /v1/agentspaces/{agentSpaceId}/operator` | Acknowledgement |
| [UpdateOperatorAppIdpConfig](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateOperatorAppIdpConfig.html) | `PATCH /v1/agentspaces/{agentSpaceId}/operator/idp` | `agentSpaceId`, `idp` |

### Private connection

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [CreatePrivateConnection](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreatePrivateConnection.html) | `POST /v1/private-connections` | `name`, `type`, `resourceGatewayId`, `hostAddress`, `vpcId`, `resourceConfigurationId`, `status`, `certificateExpiryTime`, `dnsResolution`, `failureMessage`, `tags` |
| [DescribePrivateConnection](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DescribePrivateConnection.html) | `GET /v1/private-connections/{name}` | `name`, `type`, `resourceGatewayId`, `hostAddress`, `vpcId`, `resourceConfigurationId`, `status`, `certificateExpiryTime`, `dnsResolution`, `failureMessage`, `tags` |
| [ListPrivateConnections](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListPrivateConnections.html) | `GET /v1/private-connections` | `privateConnections` |
| [UpdatePrivateConnectionCertificate](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdatePrivateConnectionCertificate.html) | `POST /v1/private-connections/{name}/certificate` | `name`, `type`, `resourceGatewayId`, `hostAddress`, `vpcId`, `resourceConfigurationId`, `status`, `certificateExpiryTime`, `dnsResolution`, `failureMessage` |
| [DeletePrivateConnection](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_DeletePrivateConnection.html) | `DELETE /v1/private-connections/{name}` | `name`, `status` |

### Account usage and tags

| Operation | HTTP route | Top-level response fields |
| --- | --- | --- |
| [GetAccountUsage](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAccountUsage.html) | `GET /usage/account` | `monthlyAccountInvestigationHours`, `monthlyAccountEvaluationHours`, `monthlyAccountSystemLearningHours`, `monthlyAccountOnDemandHours`, `monthlyAccountGraderHours`, `usagePeriodStartTime`, `usagePeriodEndTime` |
| [ListTagsForResource](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListTagsForResource.html) | `GET /tags/{resourceArn}` | `tags` |
| [TagResource](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_TagResource.html) | `POST /tags/{resourceArn}` | Acknowledgement |
| [UntagResource](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UntagResource.html) | `DELETE /tags/{resourceArn}` | Acknowledgement |

<!-- block: obsidian-devops-investigation-api-catalog-requests -->
## 2. Investigation read and command requests

Tables preserve exact member names and modeled constraints. URI/query/header parameters show their modeled location; other fields are request-body members. Mutation authorization and supported transitions require more than this syntactic contract.

### CreateBacklogTask

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `reference` | No | body | `ReferenceInput (structure)`; — |
| `taskType` | Yes | body | `TaskType (string)`; `INVESTIGATION` / `EVALUATION` / `RELEASE_READINESS_REVIEW` / `RELEASE_TESTING` |
| `title` | Yes | body | `BacklogTaskTitle (string)`; min 1; max 400 |
| `description` | No | body | `BacklogTaskDescription (string)`; min 0; max 10000 |
| `priority` | Yes | body | `Priority (string)`; `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `MINIMAL` |
| `clientToken` | No | body | `CreateBacklogTaskRequestClientTokenString (string)`; min 1; max 64; pattern `[\x21-\x7E]+`; idempotency token |

### GetBacklogTask

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetBacklogTask.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `taskId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |

### ListBacklogTasks

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListBacklogTasks.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `filter` | No | body | `TaskFilter (structure)`; — |
| `limit` | No | body | `ListBacklogTasksRequestLimitInteger (integer)`; min 1; max 1000 |
| `nextToken` | No | body | `NextToken (string)`; min 1; max 2048 |
| `sortField` | No | body | `TaskSortField (string)`; `CREATED_AT` / `PRIORITY` |
| `order` | No | body | `TaskSortOrder (string)`; `ASC` / `DESC` |

### UpdateBacklogTask

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `taskId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `taskStatus` | No | body | `TaskStatus (string)`; `PENDING_TRIAGE` / `LINKED` / `PENDING_START` / `IN_PROGRESS` / `PENDING_CUSTOMER_APPROVAL` / `COMPLETED` / `FAILED` / `TIMED_OUT` / `CANCELED` / `SKIPPED` / `WAITING` |
| `clientToken` | No | body | `UpdateBacklogTaskRequestClientTokenString (string)`; min 1; max 64; pattern `[\x21-\x7E]+`; idempotency token |

### ListExecutions

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListExecutions.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `taskId` | Yes | body | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `limit` | No | body | `Integer (integer)`; — |
| `nextToken` | No | body | `NextToken (string)`; min 1; max 2048 |

### ListJournalRecords

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `executionId` | Yes | body | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `limit` | No | body | `ListJournalRecordsRequestLimitInteger (integer)`; min 1; max 100 |
| `nextToken` | No | body | `NextToken (string)`; min 1; max 2048 |
| `recordType` | No | body | `String (string)`; — |
| `order` | No | body | `OrderType (string)`; `ASC` / `DESC` |

### ListPendingMessages

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListPendingMessages.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceId (string)`; pattern `[a-zA-Z0-9-]{1,64}` |
| `executionId` | Yes | body | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |

### CreateChat

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateChat.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `userId` | No | querystring | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+`; deprecated; see API documentation |
| `userType` | No | querystring | `UserType (string)`; `IAM` / `IDC` / `IDP` |

### ListChats

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListChats.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `userId` | No | querystring | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+`; deprecated; see API documentation |
| `maxResults` | No | querystring | `ListChatsRequestMaxResultsInteger (integer)`; min 1; max 20 |
| `nextToken` | No | querystring | `String (string)`; — |

### SendMessage

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessage.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `executionId` | Yes | body | `ChatExecutionId (string)`; min 32; max 50; pattern `[A-Za-z0-9_-]+` |
| `content` | Yes | body | `MessageContent (string)`; min 0; max 32768 |
| `context` | No | body | `SendMessageContext (structure)`; — |
| `userId` | No | body | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+`; deprecated; see API documentation |
| `assetIds` | No | body | `list<String>`; min 0; max 20 |
| `modelTier` | No | body | `String (string)`; — |

### UpdateApprovalAction

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateApprovalAction.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `approvalId` | Yes | uri | `ApprovalId (string)`; pattern `[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-7[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}` |
| `action` | Yes | body | `ApprovalActionType (string)`; `APPROVED` / `REJECTED` |
| `finalPattern` | No | body | `ApprovalPattern (structure)`; — |
| `reason` | No | body | `ApprovalReason (string)`; min 0; max 1024 |
| `ttlSeconds` | No | body | `UpdateApprovalActionRequestTtlSecondsInteger (integer)`; min 1; max 14400 |
| `singleUse` | No | body | `Boolean (boolean)`; — |

### ListAssets

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssets.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `assetType` | No | querystring | `AssetType (string)`; min 1; max 64 |
| `updatedAfter` | No | querystring | `Timestamp (timestamp)`; — |
| `updatedBefore` | No | querystring | `Timestamp (timestamp)`; — |
| `nextToken` | No | querystring | `NextToken (string)`; min 1; max 2048 |
| `maxResults` | No | querystring | `ListAssetsRequestMaxResultsInteger (integer)`; min 1; max 100 |

### GetAsset

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAsset.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `assetId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `assetVersion` | No | querystring | `GetAssetRequestAssetVersionInteger (integer)`; min 1 |

### ListAssetVersions

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssetVersions.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `assetId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `maxResults` | No | querystring | `ListAssetVersionsRequestMaxResultsInteger (integer)`; min 1; max 100 |
| `nextToken` | No | querystring | `NextToken (string)`; min 1; max 2048 |

### GetAssetContent

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetContent.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `assetId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `assetVersion` | No | querystring | `GetAssetContentRequestAssetVersionInteger (integer)`; min 1 |

### GetAssetFile

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetFile.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `assetId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `path` | Yes | uri | `AssetFilePath (string)`; min 1; max 512; pattern `[a-zA-Z0-9_./ ()-]+` |
| `assetVersion` | No | querystring | `GetAssetFileRequestAssetVersionInteger (integer)`; min 1 |

### ListAssetFiles

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssetFiles.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `assetId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `assetVersion` | No | querystring | `ListAssetFilesRequestAssetVersionInteger (integer)`; min 1 |
| `nextToken` | No | querystring | `NextToken (string)`; min 1; max 2048 |
| `maxResults` | No | querystring | `ListAssetFilesRequestMaxResultsInteger (integer)`; min 1; max 100 |

### ListRecommendations

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListRecommendations.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `taskId` | No | body | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `goalId` | No | body | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `status` | No | body | `RecommendationStatus (string)`; `PROPOSED` / `ACCEPTED` / `REJECTED` / `CLOSED` / `COMPLETED` / `UPDATE_IN_PROGRESS` |
| `priority` | No | body | `RecommendationPriority (string)`; `HIGH` / `MEDIUM` / `LOW` |
| `limit` | No | body | `ListRecommendationsRequestLimitInteger (integer)`; min 1; max 100 |
| `nextToken` | No | body | `NextToken (string)`; min 1; max 2048 |

### UpdateRecommendation

[Official operation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateRecommendation.html).

| Field | Required | Location | Type and constraints |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | uri | `AgentSpaceIdentifier (string)`; min 1; max 2048 |
| `recommendationId` | Yes | uri | `ResourceId (string)`; min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `status` | No | body | `RecommendationStatus (string)`; `PROPOSED` / `ACCEPTED` / `REJECTED` / `CLOSED` / `COMPLETED` / `UPDATE_IN_PROGRESS` |
| `additionalContext` | No | body | `String (string)`; — |
| `clientToken` | No | body | `UpdateRecommendationRequestClientTokenString (string)`; min 1; max 64; pattern `[\x21-\x7E]+`; idempotency token |

<!-- block: obsidian-devops-investigation-api-catalog-types -->
## 3. Returned entities and nested value objects

A name below is not necessarily an addressable AWS resource. Messages, approval actions, references, content blocks and events are value objects. TaskExecutionMembership, TimelineItem, GraphNode, ArtifactReference and InvestigationSnapshot are proposed application entities; they belong in the model note rather than this extracted dictionary.

### Task

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Task.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | `String (string)` | — |
| `taskId` | Yes | `String (string)` | — |
| `executionId` | No | `String (string)` | — |
| `title` | Yes | `String (string)` | — |
| `description` | No | `String (string)` | — |
| `reference` | No | `ReferenceOutput (structure)` | — |
| `taskType` | Yes | `TaskType (string)` | `INVESTIGATION` / `EVALUATION` / `RELEASE_READINESS_REVIEW` / `RELEASE_TESTING` |
| `priority` | Yes | `Priority (string)` | `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `MINIMAL` |
| `status` | Yes | `TaskStatus (string)` | `PENDING_TRIAGE` / `LINKED` / `PENDING_START` / `IN_PROGRESS` / `PENDING_CUSTOMER_APPROVAL` / `COMPLETED` / `FAILED` / `TIMED_OUT` / `CANCELED` / `SKIPPED` / `WAITING` |
| `createdAt` | Yes | `BackLogTimestamp (timestamp)` | format iso8601 |
| `updatedAt` | Yes | `BackLogTimestamp (timestamp)` | format iso8601 |
| `version` | Yes | `Integer (integer)` | — |
| `supportMetadata` | No | `JSON document` | any JSON value; nested schema not defined here |
| `metadata` | No | `JSON document` | any JSON value; nested schema not defined here |
| `primaryTaskId` | No | `String (string)` | — |
| `statusReason` | No | `String (string)` | — |
| `hasLinkedTasks` | No | `Boolean (boolean)` | — |

### TaskFilter

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_TaskFilter.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `createdAfter` | No | `BackLogTimestamp (timestamp)` | format iso8601 |
| `createdBefore` | No | `BackLogTimestamp (timestamp)` | format iso8601 |
| `priority` | No | `list<Priority>` | min 1; max 1 |
| `status` | No | `list<TaskStatus>` | min 1; max 1 |
| `taskType` | No | `list<TaskType>` | min 1; max 1 |
| `primaryTaskId` | No | `ResourceId (string)` | min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |

### ReferenceInput

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ReferenceInput.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `system` | Yes | `ReferenceInputSystemString (string)` | min 1; max 256 |
| `title` | No | `ReferenceInputTitleString (string)` | min 1; max 512 |
| `referenceId` | Yes | `ResourceId (string)` | min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `referenceUrl` | Yes | `ReferenceInputReferenceUrlString (string)` | min 1; max 2048 |
| `associationId` | Yes | `ResourceId (string)` | min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |

### ReferenceOutput

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ReferenceOutput.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `system` | Yes | `String (string)` | — |
| `title` | No | `String (string)` | — |
| `referenceId` | Yes | `String (string)` | — |
| `referenceUrl` | Yes | `String (string)` | — |
| `associationId` | Yes | `String (string)` | — |

### Execution

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | `String (string)` | — |
| `executionId` | Yes | `String (string)` | — |
| `parentExecutionId` | No | `String (string)` | — |
| `agentSubTask` | Yes | `String (string)` | — |
| `createdAt` | Yes | `JournalTimestamp (timestamp)` | — |
| `updatedAt` | Yes | `JournalTimestamp (timestamp)` | — |
| `executionStatus` | Yes | `ExecutionStatus (string)` | `FAILED` / `RUNNING` / `STOPPED` / `CANCELED` / `TIMED_OUT` / `WAITING` |
| `agentType` | No | `String (string)` | — |
| `uid` | No | `String (string)` | — |

### JournalRecord

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_JournalRecord.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | `String (string)` | — |
| `executionId` | Yes | `String (string)` | — |
| `recordId` | Yes | `String (string)` | — |
| `content` | Yes | `JSON document` | any JSON value; nested schema not defined here |
| `createdAt` | Yes | `JournalTimestamp (timestamp)` | — |
| `recordType` | Yes | `String (string)` | — |
| `userReference` | No | `UserReference (structure)` | — |

### UserReference

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UserReference.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `userId` | Yes | `String (string)` | — |
| `userType` | Yes | `UserType (string)` | `IAM` / `IDC` / `IDP` |

### ChatExecution

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ChatExecution.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `executionId` | Yes | `ResourceId (string)` | min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `createdAt` | Yes | `Timestamp (timestamp)` | — |
| `updatedAt` | No | `Timestamp (timestamp)` | — |
| `summary` | No | `String (string)` | — |

### PendingMessage

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_PendingMessage.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `messageId` | Yes | `String (string)` | — |
| `message` | Yes | `Message (structure union)` | one member |

### Message

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Message.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `userMessage` | No | `list<UserMessageBlock>` | — |
| `assistantMessage` | No | `list<AssistantMessageBlock>` | — |

### UserMessageBlock

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UserMessageBlock.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `text` | No | `String (string)` | — |
| `toolResult` | No | `JSON document` | any JSON value; nested schema not defined here |

### AssistantMessageBlock

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssistantMessageBlock.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `text` | No | `String (string)` | — |
| `toolUse` | No | `JSON document` | any JSON value; nested schema not defined here |

### SendMessageContext

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContext.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `currentPage` | No | `String (string)` | — |
| `lastMessage` | No | `String (string)` | — |
| `userActionResponse` | No | `String (string)` | — |
| `approvalAction` | No | `ApprovalAction (structure)` | — |

### ApprovalAction

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ApprovalAction.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `toolUseId` | No | `ToolUseId (string)` | min 1; max 256 |
| `interruptId` | No | `InterruptId (string)` | min 1; max 256 |
| `approvalId` | No | `ApprovalId (string)` | pattern `[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-7[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}` |
| `buttonText` | No | `ButtonText (string)` | min 1; max 256 |
| `action` | No | `ApprovalActionType (string)` | `APPROVED` / `REJECTED` |

### ApprovalPattern

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ApprovalPattern.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `tool` | Yes | `ToolIdentifier (string)` | min 1; max 256 |
| `argumentPins` | Yes | `map<ApprovalPinKey, ApprovalPinValue>` | min 0; max 20 |

### SendMessageEvents

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageEvents.html). **Streaming union: one event variant per event.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `responseCreated` | No | `SendMessageResponseCreatedEvent (structure)` | — |
| `responseInProgress` | No | `SendMessageResponseInProgressEvent (structure)` | — |
| `responseCompleted` | No | `SendMessageResponseCompletedEvent (structure)` | — |
| `responseFailed` | No | `SendMessageResponseFailedEvent (structure)` | — |
| `summary` | No | `SendMessageSummaryEvent (structure)` | — |
| `heartbeat` | No | `SendMessageHeartbeatEvent (structure)` | — |
| `contentBlockStart` | No | `SendMessageContentBlockStartEvent (structure)` | — |
| `contentBlockDelta` | No | `SendMessageContentBlockDeltaEvent (structure)` | — |
| `contentBlockStop` | No | `SendMessageContentBlockStopEvent (structure)` | — |

### SendMessageResponseCreatedEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageResponseCreatedEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `responseId` | No | `String (string)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageResponseInProgressEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageResponseInProgressEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `responseId` | No | `String (string)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageResponseCompletedEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageResponseCompletedEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `responseId` | No | `String (string)` | — |
| `usage` | No | `SendMessageUsageInfo (structure)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageResponseFailedEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageResponseFailedEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `responseId` | No | `String (string)` | — |
| `errorCode` | No | `String (string)` | — |
| `errorMessage` | No | `String (string)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageContentBlockStartEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockStartEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `index` | No | `Integer (integer)` | — |
| `type` | No | `String (string)` | — |
| `id` | No | `String (string)` | — |
| `parentId` | No | `String (string)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageContentBlockDeltaEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockDeltaEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `index` | No | `Integer (integer)` | — |
| `delta` | No | `SendMessageContentBlockDelta (structure union)` | one member |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageContentBlockDelta

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockDelta.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `textDelta` | No | `SendMessageTextDelta (structure)` | — |
| `jsonDelta` | No | `SendMessageJsonDelta (structure)` | — |

### SendMessageTextDelta

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageTextDelta.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `text` | No | `String (string)` | — |

### SendMessageJsonDelta

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageJsonDelta.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `partialJson` | No | `String (string)` | — |

### SendMessageContentBlockStopEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockStopEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `index` | No | `Integer (integer)` | — |
| `type` | No | `String (string)` | — |
| `text` | No | `String (string)` | — |
| `last` | No | `Boolean (boolean)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageSummaryEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageSummaryEvent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `content` | No | `String (string)` | — |
| `sequenceNumber` | No | `Integer (integer)` | — |

### SendMessageHeartbeatEvent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageHeartbeatEvent.html).

No modeled members.

### SendMessageUsageInfo

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageUsageInfo.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `inputTokens` | No | `Integer (integer)` | — |
| `outputTokens` | No | `Integer (integer)` | — |
| `totalTokens` | No | `Integer (integer)` | — |

### Asset

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Asset.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `assetId` | Yes | `ResourceId (string)` | min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `assetType` | Yes | `AssetType (string)` | min 1; max 64 |
| `metadata` | Yes | `JSON document` | any JSON value; nested schema not defined here |
| `version` | Yes | `Integer (integer)` | — |
| `createdAt` | Yes | `Timestamp (timestamp)` | — |
| `updatedAt` | Yes | `Timestamp (timestamp)` | — |

### AssetVersionMetadata

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetVersionMetadata.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `version` | Yes | `Integer (integer)` | — |
| `createdAt` | Yes | `Timestamp (timestamp)` | — |
| `updatedAt` | Yes | `Timestamp (timestamp)` | — |

### AssetTypeSummary

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetTypeSummary.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `assetType` | Yes | `AssetType (string)` | min 1; max 64 |
| `description` | Yes | `AssetTypeSummaryDescriptionString (string)` | min 0; max 1024 |

### AssetContent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetContent.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `file` | No | `AssetFileContent (structure)` | — |
| `zip` | No | `AssetZipContent (structure)` | — |
| `sourceUrl` | No | `AssetSourceUrlContent (structure)` | — |

### AssetFile

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetFile.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `path` | Yes | `AssetFilePath (string)` | min 1; max 512; pattern `[a-zA-Z0-9_./ ()-]+` |
| `content` | Yes | `AssetFileBody (structure union)` | one member |
| `metadata` | No | `JSON document` | any JSON value; nested schema not defined here |
| `version` | Yes | `Integer (integer)` | — |
| `createdAt` | Yes | `Timestamp (timestamp)` | — |
| `updatedAt` | Yes | `Timestamp (timestamp)` | — |

### AssetFileBody

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetFileBody.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `bytes` | No | `AssetFileBytes (blob)` | min 0; max 6291456 |
| `text` | No | `AssetFileText (string)` | min 0; max 6291456 |

### AssetFileContent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetFileContent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `path` | Yes | `AssetFilePath (string)` | min 1; max 512; pattern `[a-zA-Z0-9_./ ()-]+` |
| `body` | Yes | `AssetFileBody (structure union)` | one member |
| `metadata` | No | `JSON document` | any JSON value; nested schema not defined here |

### AssetFileSummary

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetFileSummary.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `path` | Yes | `AssetFilePath (string)` | min 1; max 512; pattern `[a-zA-Z0-9_./ ()-]+` |
| `metadata` | No | `JSON document` | any JSON value; nested schema not defined here |
| `version` | Yes | `Integer (integer)` | — |
| `createdAt` | Yes | `Timestamp (timestamp)` | — |
| `updatedAt` | Yes | `Timestamp (timestamp)` | — |

### AssetSourceUrlContent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetSourceUrlContent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `url` | Yes | `AssetContentUrl (string)` | min 1; max 2048; pattern `https://.*` |

### AssetZipContent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AssetZipContent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `zipFile` | Yes | `AssetZipBytes (blob)` | min 0; max 6291456 |

### AgentSpace

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AgentSpace.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `name` | Yes | `AgentSpaceName (string)` | min 1; max 255; pattern `[\p{L}\p{N}\p{P}\p{S}\p{Z}]+` |
| `description` | No | `Description (string)` | min 1; max 1000; pattern `[\p{L}\p{N}\p{P}\p{S}\p{Z}]+` |
| `locale` | No | `Locale (string)` | min 2; max 35; pattern `[a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*` |
| `createdAt` | Yes | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |
| `updatedAt` | Yes | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |
| `kmsKeyArn` | No | `KmsKeyArn (string)` | min 20; pattern `arn:aws[a-zA-Z-]*:kms:[a-z0-9-]+:[0-9]{12}:key/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}` |
| `agentSpaceId` | Yes | `AgentSpaceId (string)` | pattern `[a-zA-Z0-9-]{1,64}` |
| `preferences` | No | `map<AgentSpacePreferenceKey, Boolean>` | min 0; max 25 |

### RegisteredService

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_RegisteredService.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `serviceId` | Yes | `ServiceId (string)` | min 1; max 255; pattern `[a-zA-Z0-9_-]+` |
| `serviceType` | Yes | `Service (string)` | `github` / `slack` / `azure` / `azuredevops` / `msteams` / `dynatrace` / `servicenow` / `pagerduty` / `gitlab` / `eventChannel` / `mcpservernewrelic` / `mcpservergrafana` / `mcpserverdatadog` / `mcpserver` / `mcpserversplunk` / `azureidentity` / `mcpserversigv4` / `remoteagent` / `remoteagentsigv4` |
| `name` | No | `ServiceName (string)` | min 1; max 255; pattern `[\p{L}\p{N}\p{P}\p{S}\p{Z}]+` |
| `accessibleResources` | No | `list<Document>` | — |
| `additionalServiceDetails` | No | `AdditionalServiceDetails (structure union)` | one member |
| `kmsKeyArn` | No | `KmsKeyArn (string)` | min 20; pattern `arn:aws[a-zA-Z-]*:kms:[a-z0-9-]+:[0-9]{12}:key/[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}` |
| `privateConnectionName` | No | `PrivateConnectionName (string)` | min 3; max 30; pattern `[a-z0-9]([a-z0-9-]*[a-z0-9])?` |
| `createdAt` | Yes | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |
| `updatedAt` | Yes | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |

### Association

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Association.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `agentSpaceId` | Yes | `AgentSpaceId (string)` | pattern `[a-zA-Z0-9-]{1,64}` |
| `createdAt` | Yes | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |
| `updatedAt` | Yes | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |
| `status` | No | `ValidationStatus (string)` | `valid` / `invalid` / `pending-confirmation` |
| `associationId` | Yes | `AssociationId (string)` | min 1; max 255; pattern `[a-zA-Z0-9-]+` |
| `serviceId` | Yes | `ServiceId (string)` | min 1; max 255; pattern `[a-zA-Z0-9_-]+` |
| `configuration` | Yes | `ServiceConfiguration (structure union)` | one member |
| `capabilities` | No | `map<CapabilityType, CapabilityConfiguration>` | — |

### ServiceConfiguration

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ServiceConfiguration.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `sourceAws` | No | `SourceAwsConfiguration (structure)` | — |
| `aws` | No | `AWSConfiguration (structure)` | — |
| `github` | No | `GitHubConfiguration (structure)` | — |
| `slack` | No | `SlackConfiguration (structure)` | — |
| `dynatrace` | No | `DynatraceConfiguration (structure)` | — |
| `servicenow` | No | `ServiceNowConfiguration (structure)` | — |
| `mcpservernewrelic` | No | `MCPServerNewRelicConfiguration (structure)` | — |
| `mcpserverdatadog` | No | `MCPServerDatadogConfiguration (structure)` | — |
| `mcpserver` | No | `MCPServerConfiguration (structure)` | — |
| `gitlab` | No | `GitLabConfiguration (structure)` | — |
| `mcpserversplunk` | No | `MCPServerSplunkConfiguration (structure)` | — |
| `eventChannel` | No | `EventChannelConfiguration (structure)` | — |
| `azure` | No | `AzureConfiguration (structure)` | — |
| `azuredevops` | No | `AzureDevOpsConfiguration (structure)` | — |
| `mcpservergrafana` | No | `MCPServerGrafanaConfiguration (structure)` | — |
| `pagerduty` | No | `PagerDutyConfiguration (structure)` | — |
| `mcpserversigv4` | No | `MCPServerSigV4Configuration (structure)` | — |
| `remoteagent` | No | `RemoteAgentConfiguration (structure)` | — |
| `remoteagentsigv4` | No | `RemoteAgentSigV4Configuration (structure)` | — |
| `msteams` | No | `MSTeamsConfiguration (structure)` | — |
| `releaseManagement` | No | `ReleaseManagementConfiguration (structure)` | — |

### Recommendation

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Recommendation.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `agentSpaceArn` | Yes | `String (string)` | — |
| `recommendationId` | Yes | `String (string)` | — |
| `taskId` | Yes | `String (string)` | — |
| `goalId` | No | `String (string)` | — |
| `title` | Yes | `String (string)` | — |
| `content` | Yes | `RecommendationContent (structure)` | — |
| `status` | Yes | `RecommendationStatus (string)` | `PROPOSED` / `ACCEPTED` / `REJECTED` / `CLOSED` / `COMPLETED` / `UPDATE_IN_PROGRESS` |
| `priority` | Yes | `RecommendationPriority (string)` | `HIGH` / `MEDIUM` / `LOW` |
| `goalVersion` | No | `Long (long)` | — |
| `additionalContext` | No | `String (string)` | — |
| `rankPosition` | No | `RecommendationRankPositionInteger (integer)` | min 1 |
| `rankedAt` | No | `BackLogTimestamp (timestamp)` | format iso8601 |
| `createdAt` | Yes | `BackLogTimestamp (timestamp)` | format iso8601 |
| `updatedAt` | Yes | `BackLogTimestamp (timestamp)` | format iso8601 |
| `version` | Yes | `Long (long)` | — |

### RecommendationContent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_RecommendationContent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `summary` | Yes | `String (string)` | — |
| `spec` | No | `RecommendationContentSpecString (string)` | min 0; max 100000 |

### Goal

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Goal.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `agentSpaceArn` | Yes | `String (string)` | — |
| `goalId` | Yes | `String (string)` | — |
| `title` | Yes | `String (string)` | — |
| `content` | Yes | `GoalContent (structure)` | — |
| `status` | Yes | `GoalStatus (string)` | `ACTIVE` / `PAUSED` / `COMPLETE` |
| `goalType` | Yes | `GoalType (string)` | `CUSTOMER_DEFINED` / `ONCALL_REPORT` |
| `createdAt` | Yes | `BackLogTimestamp (timestamp)` | format iso8601 |
| `updatedAt` | Yes | `BackLogTimestamp (timestamp)` | format iso8601 |
| `lastEvaluatedAt` | No | `BackLogTimestamp (timestamp)` | format iso8601 |
| `lastTaskId` | No | `String (string)` | — |
| `lastSuccessfulTaskId` | No | `String (string)` | — |
| `version` | Yes | `Integer (integer)` | — |
| `evaluationSchedule` | No | `GoalSchedule (structure)` | — |

### GoalContent

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GoalContent.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `description` | Yes | `String (string)` | — |
| `objectives` | Yes | `String (string)` | — |

### Trigger

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Trigger.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `triggerId` | Yes | `ResourceId (string)` | min 1; max 128; pattern `[a-zA-Z0-9_.-]+` |
| `agentSpaceId` | Yes | `AgentSpaceId (string)` | pattern `[a-zA-Z0-9-]{1,64}` |
| `type` | Yes | `TriggerType (string)` | min 1; max 64 |
| `condition` | Yes | `TriggerCondition (structure union)` | one member |
| `action` | Yes | `JSON document` | any JSON value; nested schema not defined here |
| `status` | Yes | `TriggerStatus (string)` | min 1; max 64 |
| `createdAt` | Yes | `Timestamp (timestamp)` | — |
| `updatedAt` | Yes | `Timestamp (timestamp)` | — |

### TriggerCondition

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_TriggerCondition.html). **Union: select one member.**

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `schedule` | No | `ScheduleCondition (structure)` | — |

### Webhook

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Webhook.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `webhookUrl` | Yes | `WebhookWebhookUrlString (string)` | pattern `https://[a-zA-Z0-9.-]+(?:/.*)?` |
| `webhookType` | No | `WebhookType (string)` | `hmac` / `apikey` / `gitlab` / `pagerduty` |
| `webhookId` | Yes | `WebhookWebhookIdString (string)` | min 1; max 255 |

### PrivateConnectionSummary

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_PrivateConnectionSummary.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `name` | Yes | `PrivateConnectionName (string)` | min 3; max 30; pattern `[a-z0-9]([a-z0-9-]*[a-z0-9])?` |
| `type` | Yes | `PrivateConnectionType (string)` | `SELF_MANAGED` / `SERVICE_MANAGED` |
| `resourceGatewayId` | No | `ResourceGatewayArn (string)` | min 20; max 2048; pattern `arn:[a-z0-9\-]+:vpc-lattice:[a-zA-Z0-9\-]+:\d{12}:resourcegateway/rgw-[0-9a-z]{17}` |
| `hostAddress` | No | `IpAddressOrDnsName (string)` | min 3; max 255; pattern `[a-zA-Z0-9.:\-]+` |
| `vpcId` | No | `VpcId (string)` | min 5; max 50; pattern `vpc-(([0-9a-z]{8})\|([0-9a-z]{17}))` |
| `resourceConfigurationId` | No | `ResourceConfigurationArn (string)` | min 20; max 2048; pattern `(arn:[a-z0-9\-]+:vpc-lattice:[a-zA-Z0-9\-]+:\d{12}:resourceconfiguration/rcfg-[0-9a-z]{17}\|rcfg-[0-9a-z]{17})` |
| `status` | Yes | `PrivateConnectionStatus (string)` | `ACTIVE` / `CREATE_IN_PROGRESS` / `CREATE_FAILED` / `DELETE_IN_PROGRESS` / `DELETE_FAILED` |
| `certificateExpiryTime` | No | `SyntheticTimestamp_date_time (timestamp)` | format iso8601 |
| `dnsResolution` | No | `ResourceConfigDnsResolution (string)` | `PUBLIC` / `IN_VPC` |
| `failureMessage` | No | `FailureMessage (string)` | min 1; max 1000 |

### UsageMetric

[Official type](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UsageMetric.html).

| Field | Required | Referenced type | Constraints or representation |
| --- | --- | --- | --- |
| `limit` | Yes | `Integer (integer)` | — |
| `usage` | Yes | `Double (double)` | — |

<!-- block: obsidian-devops-investigation-api-catalog-semantics -->
## 4. Semantic constraints beyond the tables


### List behavior

- `ListBacklogTasks`: priority, status and taskType each allow one filter value even though their shapes are lists. Priority and status together require a type filter. Priority or status filters used alone permit sorting only by CREATED_AT. Creation-time filters cannot be combined with priority sorting. `createdAfter` is inclusive and `createdBefore` exclusive. There is no updated-time filter.
- `ListExecutions`: taskId is required, but returned Execution objects omit it; retain the request association. There is no modeled order, status or parent-execution filter.
- `ListJournalRecords`: at most 100 records per page, default descending timestamp order, arbitrary record-type filter. No modeled since filter, single-record lookup, update time, same-time tie-break, snapshot token or change-stream cursor.
- `ListPendingMessages` has no pagination parameters; it is a pending queue, not a guaranteed complete conversation archive.
- `ListAssets` is space-scoped, with type/update-time filters, not task or execution filters. Asset/file reads can specify assetVersion; preserve the returned version.

Sources: the linked operation pages and [TaskFilter](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_TaskFilter.html).

### Status and command behavior

- Native task/execution enums use `CANCELED`; EventBridge uses `CANCELLED`. Preserve raw values and channels when normalizing.
- ExecutionStatus has `STOPPED` but no `COMPLETED`. Its enum alone does not establish successful investigation completion.
- Task.version is described as an optimistic-locking version, but UpdateBacklogTask has no expectedVersion, version or ETag input. Adding an application field cannot create a native compare-and-swap guarantee.
- A TaskStatus update is not a documented transition matrix. No dedicated GetInvestigation, StopInvestigation, ForkInvestigation or ResumeInvestigation operation exists in this model.
- SendMessage streams a chat response. Its responseCompleted event does not complete the backlog task. userId is deprecated/ignored; identity comes from the authenticated session.
- Approval requires finalPattern and singleUse. A reusable approval additionally requires ttlSeconds between 1 and 14400. A single-use approval omits TTL. Rejection omits pattern, singleUse and TTL. The finalized pattern must match or narrow the requested invocation; it must not widen it. Resuming the paused execution is a separate SendMessage step.
- UpdateApprovalAction has no client-token input and no modeled companion Get/List/Revoke approval operation. Do not implement reconnect with an invented read method.

Sources: [UpdateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html), [Execution](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html), [SendMessage](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessage.html), [directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html), and the pinned model.

### Open content and identifiers

JournalRecord.content, task metadata/supportMetadata, asset metadata and tool-use/tool-result values are JSON documents. Preserve objects, arrays, strings, numbers, booleans and null without assuming a text property. The service model does not define graph, hypothesis, root-cause or typed investigation-result entities.

AssetType, recordType, agentType, agentSubTask and streamed block type are open strings. Current conventions belong in versioned parser profiles. IDs have different constraints across API families; do not validate all IDs as UUIDs.

BackLogTimestamp explicitly uses ISO 8601. Under REST-JSON, body timestamps without an explicit format use Unix seconds, potentially fractional, not epoch milliseconds; this applies to the execution/journal body fields. Query/header defaults must be handled separately. Let the SDK decode them, normalize to UTC, and preserve original values when needed for auditability. updatedAt is not an explicit finish timestamp. See the [AWS REST-JSON timestamp rules](https://smithy.io/2.0/aws/protocols/aws-restjson1-protocol.html#timestamp-serialization).

<!-- block: obsidian-devops-investigation-api-catalog-validation -->
## 5. Extraction verification

Generation checks that all 63 operations appear exactly once, resolves every field type, and carries requiredness, unions, enum values and modeled constraints from the pinned source. The selected dictionary expands 52 structures/value types. Provider-specific nested configurations remain linked to their official references.

This verifies a schema snapshot. It does not verify service deployment, caller authorization, undocumented payload schemas, timing or per-region runtime behavior. See the capture and acceptance plan in [[Investigation_UI_Contract]].
