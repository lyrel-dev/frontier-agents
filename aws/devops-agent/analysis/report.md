---
title: "AWS DevOps Agent: reviewed investigation model and UI contract"
id: aws-devops-analysis-report
kind: obsidian-note
product: devops
type: reviewed-report
created: '2026-11-05'
updated: '2026-11-05'
reviewed: '2026-11-05'
source_cutoff: '2026-11-05'
api_version: '2026-01-01'
initial_model_commit: 1d10b2de6616ff3d94e97a579c6291cc3696c03a
status: reviewed-design
tags:
  - aws/devops-agent
  - investigation
  - data-model
  - operator-ui
related:
  - "README.md"
  - "REVIEW.md"
  - "QUALITY_REVIEW.md"
  - "annexes/Investigation_API_Catalog.md"
  - "annexes/Investigation_UI_Contract.md"
  - "annexes/Investigation_API_Sources.md"
---

<!-- block: obsidian-devops-investigation-data-model-decision -->
# AWS DevOps Agent: reviewed investigation model and UI contract


**Review date: 5 November 2026.** This report consolidates the initial investigation model, the live-view and historical-view contracts, and **all ten diagrams** into one reviewable document. The [single-page application](index.html) uses realistic fictional observations to make these distinctions visible. It performs no AWS calls.

The independent review retained the architecture: an investigation is a native `Task` of type `INVESTIGATION`, with request-observed execution membership, published journal records, explicit result references, and application-owned projections. The current Botocore file retrieved on the review date is byte-identical to the pinned source model. The catalog contains **63 native operations**, **19 detailed request tables**, and **52 selected entity/value tables**, comprising **339 expanded member rows**. These counts describe the catalog, not the number of business entities or a full semantic audit of all 560 model shapes. Reproducible comparisons and their limits are recorded in the [source register](annexes/Investigation_API_Sources.md).

The [adversarial follow-up](QUALITY_REVIEW.md) found that the first prototype's passing scenario did not establish several stated invariants. The corrected model deduplicates entities while preserving observations, keeps investigation and mitigation results separate, rejects ambiguous identity joins, pins the displayed Task's exact source, and retains historical exports independently of changing live comparisons. D07 adds the missing collection-attempt and coverage layer. The [validation record](VALIDATION.md) separates executable checks from browser observations and future AWS integration evidence.

### Review changes and interpretation

| Review point | Outcome |
| --- | --- |
| Native API drift | No change found between the pinned model and the current Botocore path retrieved for this review. |
| Completion and summary absence | The report now distinguishes an uncaptured notification, a completion notification with no summary pointer, and a pointer whose record has not been retrieved. |
| Scope and joins | The full scoped keys remain authoritative; compact ERD fields are selected attributes, not complete physical DDL. |
| Prototype provenance | Fixture-specific telemetry, findings and graph payloads are explicitly synthetic application profiles, not claimed AWS nested schemas. |
| Replay and clocks | A replay is an illustrative scenario sequence. Normalized mock timestamps and simulation time are not a capture of HTTP serialization, service latency or legal task transitions. |
| Historical evidence | Snapshots retain exact source and projection revisions; a new investigation observation cannot silently rewrite a reviewed snapshot. |

The [initial review record](REVIEW.md) is retained as a historical record; [QUALITY_REVIEW.md](QUALITY_REVIEW.md) gives the current finding disposition. Live account behavior, operational permissions, detailed journal-content profiles and undocumented action recipes remain implementation validation work.

### Reading map

| Material | Purpose |
| --- | --- |
| Sections 1–12 below | Native and derived entities, keys, state, timelines, graphs, artifacts and snapshots |
| Sections 13–15 below | Collection sequence, approval audit model and historical capture workflow |
| Section 16 below | Fictional prototype contract and production boundary |
| [API inventory and selected schemas](annexes/Investigation_API_Catalog.md) | All 63 operations, transport/error mappings and selected detailed field tables |
| [Proposed UI integration contract](annexes/Investigation_UI_Contract.md) | Stream/pagination/error/authorization design and 24 future capture scenarios; no implemented backend API |
| [Source and model provenance](annexes/Investigation_API_Sources.md) | Official links, exact model pins/hashes and historical verification record |

### Diagram index

| Diagram | Relationship explained | Editable source | Rendered SVG |
| --- | --- | --- | --- |
| D01 | Workspace, association and external reference | [Mermaid](diagrams/D01-workspace-associations.mmd) | [SVG](diagrams/D01-workspace-associations.svg) |
| D02 | Native core with an explicit membership table | [Mermaid](diagrams/D02-investigation-core.mmd) | [SVG](diagrams/D02-investigation-core.svg) |
| D03 | Every projection retains provenance | [Mermaid](diagrams/D03-projection-provenance.mmd) | [SVG](diagrams/D03-projection-provenance.svg) |
| D04 | Graph snapshot and typed edges | [Mermaid](diagrams/D04-graph-model.mmd) | [SVG](diagrams/D04-graph-model.svg) |
| D05 | Investigation references and native asset history | [Mermaid](diagrams/D05-artifacts-assets.mmd) | [SVG](diagrams/D05-artifacts-assets.svg) |
| D06 | Immutable application snapshots | [Mermaid](diagrams/D06-historical-snapshots.mmd) | [SVG](diagrams/D06-historical-snapshots.svg) |
| D07 | Collection evidence and bounded coverage | [Mermaid](diagrams/D07-collection-observations.mmd) | [SVG](diagrams/D07-collection-observations.svg) |
| U01 | Reconcile snapshots and journals | [Mermaid](diagrams/U01-live-reconciliation.mmd) | [SVG](diagrams/U01-live-reconciliation.svg) |
| U02 | Decision, resume and observed outcome | [Mermaid](diagrams/U02-approval-lifecycle.mmd) | [SVG](diagrams/U02-approval-lifecycle.svg) |
| U03 | Application snapshot workflow | [Mermaid](diagrams/U03-snapshot-workflow.mmd) | [SVG](diagrams/U03-snapshot-workflow.svg) |

## 1. Architecture decision

**Represent an investigation as a business aggregate over a native backlog Task, its discovered Executions, their JournalRecords, and separately sourced lifecycle notifications and results.** Retain the original responses. Build timelines, result cards, evidence links, graphs and historical snapshots as versioned application projections.

The public AWS DevOps Agent model does **not** define an `Investigation` structure or a `GetInvestigation` operation. Its work-item discriminator is `Task.taskType = INVESTIGATION`. The current native API has 63 operations; the relevant read path is `GetBacklogTask → ListExecutions → ListJournalRecords`. AWS's separately named Amazon AI Operations APIs are outside this analysis. [Actions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Operations.html) · [Task](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Task.html) · [ListExecutions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListExecutions.html)

Three distinctions determine whether the redesigned UI will be trustworthy:

1. **Task status, execution status and result availability are independent.** Task `COMPLETED`, execution `STOPPED`, chat `responseCompleted` and an available summary do not mean the same thing.
2. **Published envelopes are strongly defined; much of their content is not.** `JournalRecord.content` is an arbitrary JSON document and `recordType` an open string. The native model does not publish typed hypothesis, evidence, root-cause, topology or causal-graph structures.
3. **Completion is a checkpoint, not an immutable archive.** The product guide allows an operator to send a message to a completed investigation and continue it with its prior context. A historical view therefore needs an explicit “as of” snapshot. [Execution](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html) · [JournalRecord](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_JournalRecord.html) · [Chat with an investigation](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

This design supports a useful first release using documented APIs, while exposing uncertainty where richer payload schemas require validation. It does not claim full parity with the AWS Operator Web App.

### Evidence convention

| Label | Meaning in this study |
| --- | --- |
| **Native** | Explicit field, structure, operation or constraint in the public AWS API/official SDK model |
| **Documented profile** | Meaning or payload convention described in an AWS user guide but carried inside an open string/JSON value |
| **Derived** | Proposed application entity or calculation, retaining its source identifiers and derivation method |
| **Unverified** | Product behavior or useful UI feature whose complete public wire contract was not established |

All ER diagrams are **proposed logical storage/view models**. Their cardinalities describe the design; adjacent notes explain which relationships AWS guarantees and which the application records. They are not reverse-engineered AWS database diagrams. Boxes show selected attributes; the identity table and accompanying text define full scope and joins. These are not complete physical DDL schemas.

Scope is schema/documentation review as of **5 November 2026**. The API model remains version `2026-01-01`; its pinned model revisions are dated 21 October 2026. No customer account, production investigation or live service response was queried. [source and model provenance](annexes/Investigation_API_Sources.md) records the source pins, discrepancies and verification limits.

<!-- block: obsidian-devops-investigation-data-model-platform -->
## 2. API-wide entity map

The complete operation catalog is in [operation inventory and selected schemas](annexes/Investigation_API_Catalog.md). These resource families provide the surrounding model without forcing every configuration object into an investigation record.

| Family | Returned/manipulated entities | Relation to an investigation |
| --- | --- | --- |
| Agent Spaces | `AgentSpace`, preferences, tags, encryption settings | Workspace and authorization scope for tasks, runs, journals and assets |
| Service access | `RegisteredService`, `Association`, provider-specific configuration | Connections the workspace may use; current configuration is not proof of what a past run consumed |
| Incident/backlog work | `Task`, external `ReferenceOutput`, task filters | Investigation identity, title, priority, lifecycle, linked-incident references |
| Runtime history | `Execution`, `JournalRecord`, `UserReference` | Execution hierarchy and persisted published activity/content |
| Conversation | `ChatExecution`, `PendingMessage`, message/content-block unions, `SendMessageEvents` | Interactive conversation and incremental response rendering |
| Action authorization | `ApprovalPattern`, `ApprovalAction`, update response | Scoped decisions and resumption of paused tool calls; not an execution-success record |
| Prevention | `Goal`, `Recommendation`, goal schedule | Related improvement work; a Recommendation is not automatically an incident mitigation |
| Assets | `Asset`, version metadata, files/content, type summaries | Skills, instructions, attachments, custom agents, memory, test profiles, feedback |
| Automation | `Trigger`, condition/filter/schedule values | Invokes configured actions; the action can refer to a custom-agent asset |
| Operator access | Enable/get/disable operator-app responses, identity-provider configuration | Web application access configuration, not the investigation domain record |
| Private access | Private connection name/ARN/status, private network configuration | Connectivity context for registered integrations or release environments |
| Intake/operations | Webhook descriptors, account usage, tag maps | Intake endpoint configuration and account-level usage; not full incident telemetry |

These names and operations come from the [API action/type indexes](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Types.html) and the pinned SDK model. Some families return wrapper fields rather than a reusable named top-level entity. The catalog preserves those response fields.

### Diagram D01 — workspace, association and external reference

[Rendered SVG](diagrams/D01-workspace-associations.svg) · [Editable Mermaid](diagrams/D01-workspace-associations.mmd)

`SPACE` and `REGISTERED_SERVICE` below live inside the owning resource scope: partition, account and Region. The connection and authorization context used to read them is recorded separately. `EXTERNAL_REFERENCE` is a normalized copy of the optional value object embedded in a Task.

```mermaid
erDiagram
    direction TB
    SPACE ||--o{ ASSOCIATION : contains
    SPACE ||--o{ TASK : contains
    TASK ||--o| EXTERNAL_REFERENCE : embeds
    ASSOCIATION o|--o{ EXTERNAL_REFERENCE : resolves
    REGISTERED_SERVICE o|--o{ ASSOCIATION : optionally_resolves
    SPACE {
        string scope_key PK
        string agent_space_id PK
    }
    ASSOCIATION {
        string association_id PK
        string service_id
        string configuration_kind
    }
    TASK {
        string task_id PK
        string task_type
    }
    EXTERNAL_REFERENCE {
        string system
        string reference_id
        string association_id
        string resolved_association_key FK
        string reference_url
    }
    REGISTERED_SERVICE {
        string service_id PK
        string service_type
    }
```

**Relationship qualifications.** `Task.reference`, when present, includes `system`, `referenceId`, `referenceUrl` and `associationId`; `title` is optional. Association references can be unresolved in a partial or historical collection. Preserve the reference even if the current association no longer exists. [ReferenceOutput](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ReferenceOutput.html)

Do **not** make every `Association.serviceId` a mandatory foreign key to `RegisteredService`. AWS onboarding uses the literal service ID `aws` for built-in AWS configurations, including `aws` and `sourceAws` variants. It can also create multiple AWS account associations. Do not impose uniqueness on `(agentSpaceId, serviceId)`; identify the association by `associationId` and inspect its configuration discriminator. Registered provider-backed associations can resolve to a RegisteredService. [Association](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Association.html) · [CLI onboarding](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-cli-onboarding-guide.html)

A provider connection, a monitored resource and an evidence item are different identities. An association to an AWS account or repository does not establish that every resource in that account/repository was implicated in a particular investigation.

<!-- block: obsidian-devops-investigation-data-model-core -->
## 3. Investigation aggregate and keys

Define the application-level `Investigation` as:

```text
Investigation = Task where taskType is INVESTIGATION
              + observed task-to-execution memberships
              + execution hierarchy and journal records
              + lifecycle notifications and conversation observations
              + referenced results/assets
              + derived projections and historical snapshots
```

This is a composition rule, not an AWS response payload.

### Identity and scope

Use compound keys. Do not assume opaque IDs are globally unique across accounts, Regions, Agent Spaces or API channels. Encode the key tuple unambiguously; concatenating opaque components with an unescaped delimiter can create collisions.

| Application record | Recommended identity | Source of relationship |
| --- | --- | --- |
| OwningScope | `partition + owningAccountId + region` | Resource-owning ARN or authenticated account/endpoint context |
| ConnectionContext | Application connection ID plus authorization-context identity | Access path, collection policy and principal-sensitive cache boundary; separate from native entity identity |
| AgentSpace | `scopeKey + agentSpaceId` | Returned space or request context |
| Task / Investigation | `spaceKey + taskId` | Native Task |
| Execution | `spaceKey + executionId` | Native Execution |
| TaskExecutionMembership | `spaceKey + taskId + executionId` | The `ListExecutions` request and returned list |
| JournalRecord | `spaceKey + executionId + recordId` | Native journal envelope |
| JournalRecordRevision | Record key + content/envelope hash | Application capture of observed versions |
| Event notification | Channel + account/Region + native event ID | EventBridge envelope; retain raw event |
| Stream response/block | Execution + local request/session + response ID/index/ID when present | `SendMessage` stream; preserve unresolved identifiers |
| AssetVersion | `spaceKey + assetId + version` | Asset reads/version listing |
| AssetFileVersion | AssetVersion key + exact file path | File reads; file `version` identifies its asset version |
| Derived item/revision | Stable logical item ID; separate immutable projectionRevisionId for each rendition | Application projection and retained payload/hash |
| InvestigationSnapshot | Investigation key + immutable snapshot ID | Application archival policy |

The entity `scopeKey` identifies the owning partition/account/Region; a role change or a second connection to the same owning scope does not create a different native resource. Authorization context still belongs in read attempts, cache access and export checks. Keep Agent Space ARNs as aliases where APIs such as Goal and Recommendation return them. Use caller/endpoint context to scope bodies that omit account, Region, or Agent Space ID. A connected resource's account ID is not necessarily the service-owning account ID.

### Diagram D02 — native core with an explicit membership table

[Rendered SVG](diagrams/D02-investigation-core.svg) · [Editable Mermaid](diagrams/D02-investigation-core.mmd)

`SPACE` is omitted from the fields below for legibility; every key includes it.

```mermaid
erDiagram
    direction TB
    TASK ||--o{ TASK_EXECUTION : enumerates
    EXECUTION ||--o{ TASK_EXECUTION : observed_in
    EXECUTION o|--o{ EXECUTION : parent_of
    EXECUTION ||--o{ JOURNAL_RECORD : publishes
    JOURNAL_RECORD ||--|{ RECORD_REVISION : observed_as
    TASK {
        string task_id PK
        string task_type
        string execution_id
        string status
        int version
    }
    TASK_EXECUTION {
        string task_id PK,FK
        string execution_id PK,FK
        datetime observed_at
    }
    EXECUTION {
        string execution_id PK
        string parent_execution_id FK
        string execution_status
        string agent_type
        string agent_subtask
    }
    JOURNAL_RECORD {
        string execution_id PK,FK
        string record_id PK
        string record_type
        datetime created_at
    }
    RECORD_REVISION {
        string revision_id PK
        string record_key FK
        string payload_hash
        datetime first_observed_at
    }
```

**Why the junction exists.** `ListExecutions` requires a task ID, but its returned Execution does not contain `taskId`. Record the request/response association instead of losing that context. The design permits multiple observed memberships because the public shape does not establish global one-task ownership of an execution. It does not assert that the service routinely shares executions across tasks. [ListExecutions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListExecutions.html)

`Task.executionId` is optional and describes an associated execution. It is a useful pointer, not a documented substitute for enumerating all executions, nor proof of “latest execution,” “root execution” or “only execution.” `Execution.parentExecutionId` supplies an explicit hierarchy edge; if the parent has not been fetched, create an unresolved reference rather than dropping the child. [Task](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Task.html) · [Execution](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html)

`RECORD_REVISION` is application-owned. Its `first_observed_at` is the first retained observation of that payload revision, not a mutable freshness timestamp; later observations belong to D07. The public JournalRecord shape provides a record ID and creation time, but no update-version or finalization marker. Store a new observed revision when a record with the same ID has different content. This preserves evidence without claiming that AWS mutates records or exposes a revision API.

### Native field groups and meaning

| Entity | Native field groups | UI/model treatment |
| --- | --- | --- |
| Task | Required IDs/type/title, priority/status, created/updated timestamps, version | Investigation list/header; preserve raw enum values and snapshot versions |
| Task context | Optional description, reference, metadata, supportMetadata | Raw context plus explicitly validated parser profiles; do not invent severity, root cause, incident time range or error fields |
| Task linking | Optional primaryTaskId, hasLinkedTasks, statusReason | Linked incident relationship; not execution parentage or fork ancestry |
| Execution | Required space/execution IDs, agentSubTask, executionStatus, created/updated timestamps | Execution row/tree node and observed activity; agentSubTask is open text |
| Execution context | Optional parentExecutionId, agentType, uid | Parent relation and display context; uid is session identity, not a full user profile |
| JournalRecord | Required space/execution/record IDs, recordType, createdAt, content | Published record envelope; content is any JSON value; application retention is separate |
| Journal attribution | Optional userReference with userId/userType | Attribution when supplied; absence does not identify an internal agent by itself |

Exact requiredness and type constraints are in [operation inventory and selected schemas](annexes/Investigation_API_Catalog.md). Fields such as `rootCause`, `confidence`, `progressPercent`, `endedAt`, `duration` and `artifactIds` are not native Task fields.

### Linked tasks and forks

A linked task has an optional `primaryTaskId`. To find linked tasks, the backlog filter accepts `primaryTaskId`. A boolean `hasLinkedTasks` is an indication, not the linked-task collection or count. Keep each source task and its external reference: grouping several alerts under one investigation must not erase the individual tickets. [TaskFilter](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_TaskFilter.html)

The product UI documents forking, but the reviewed native create/update task requests do not expose a fork-parent ID, branch point or fork operation. **Do not reuse primaryTaskId to invent a fork relationship.** If a future documented contract or a validated payload supplies fork lineage, add an explicitly sourced relation type. [Incident workflow](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) · [CreateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html) · [UpdateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html)

<!-- block: obsidian-devops-investigation-data-model-status -->
## 4. Preserve separate state domains

| Domain | Published values or contract | Consequence |
| --- | --- | --- |
| Task.status | `PENDING_TRIAGE`, `LINKED`, `PENDING_START`, `IN_PROGRESS`, `PENDING_CUSTOMER_APPROVAL`, `COMPLETED`, `FAILED`, `TIMED_OUT`, `CANCELED`, `SKIPPED`, `WAITING` | Primary work-item state; show a distinct reason/linked destination where available |
| Execution.executionStatus | `FAILED`, `RUNNING`, `STOPPED`, `CANCELED`, `TIMED_OUT`, `WAITING` | Per-execution state; STOPPED alone does not prove success |
| Chat response | Created/in progress/completed/failed events, content-block events, heartbeat | State of one message response; never use as investigation completion |
| EventBridge investigation | Created, priority updated, in progress, completed, failed, timed out, cancelled, pending triage, linked, skipped event types | Lifecycle observations; no complete journal or chat history |
| EventBridge mitigation | In progress/completed/failed/timed out/cancelled event types | Separate phase milestone; `data.task_type` remains INVESTIGATION |
| Approval | `PENDING`, `APPROVED`, `REJECTED`, `REVOKED`, `REDEEMED` in the model | Authorization lifecycle; redeemed means credential mint at least once, not successful execution or mitigation |
| Application freshness/results | Proposed values such as fresh/stale, partial/complete-for-fetch, expected/retrieved/not-reported | Explicit local state with its own timestamps and reasons |

Sources: [Task](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Task.html), [Execution](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html), [SendMessage](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessage.html), [event detail reference](https://docs.aws.amazon.com/devopsagent/latest/userguide/integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-devops-agent-events-detail-reference.html), [directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html), pinned SDK.

EventBridge's `CANCELLED` differs from native `CANCELED`. Preserve the original channel/value and normalize only for display or query. EventBridge does not enumerate every native waiting/approval state, and it is not a substitute for the task read.

The API enum describes possible values, not all legal transitions. `UpdateBacklogTask` exposes `taskStatus` and an idempotency token; it does not publish a transition matrix or a version precondition. Do not offer a generic “set status” control or derive a compare-and-swap operation from `Task.version`. [production UI contract](annexes/Investigation_UI_Contract.md) specifies mutation boundaries.

A completed investigation can later continue. In the proposed data model, **finalized** means “this application's retained snapshot at a stated time and source version,” not a new AWS state.

<!-- block: obsidian-devops-investigation-data-model-journal -->
## 5. Journal content, results and evidence

### The native envelope is the reliable base

A JournalRecord contains these mandatory fields:

```text
agentSpaceId, executionId, recordId, recordType, createdAt, content
```

`content` is a JSON document. There is no outer-envelope `sequenceNumber`, `updatedAt`, `parentId`, `toolUseId`, `schemaVersion`, evidence list or result discriminated union. Optional `userReference` provides attribution. [JournalRecord](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_JournalRecord.html)

**Preserve unknown record types.** Render a raw structured view with a short readable preview, execution, timestamp and record ID. Dispatch known types through registered parsers. An unsupported type should not break the investigation page or silently disappear.

### Documented summary profiles

AWS documents two exact record-type strings:

| Purpose | recordType | Selection |
| --- | --- | --- |
| Investigation summary | `investigation_summary_md` | Match the completion event's `summary_record_id` when present |
| Mitigation summary | `mitigation_summary_md` | Match the mitigation completion event's `summary_record_id` when present |

An execution can have several summary records of a type. Call `ListJournalRecords` with the correct space, execution and type; traverse the required pages and select the exact record ID. There is no public single-record Get operation. A completed event may omit the summary pointer; failed, timed-out and cancelled events do not include it. Both investigation and mitigation events use task type INVESTIGATION, so use `detail-type` to choose the summary type. [EventBridge integration and summary retrieval](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html)

The `_md` convention identifies a summary intended for Markdown presentation. It does not change the outer `content` type from JSON to a string-only schema. Accept a string when actually returned; preserve unexpected forms and require a validated decoder for wrappers. Do not blindly assume `content.markdown` or `content.text` exists.

When no completion pointer was captured, show candidate summary records with their provenance. An application may choose the latest observed record as a display policy, but label that selection; a timestamp tie or incomplete page set does not establish an authoritative final summary.

### Completion and summary absence: three different cases

Keep these collection states separate:

| Observation | Meaning and presentation |
| --- | --- |
| No completion event was captured | The authoritative summary pointer is unknown. Show available candidates with a stated selection policy. |
| A captured `Completed` event omits `summary_record_id` | The AWS guide says no summary is available for that execution. Show a bounded “No summary reported for this execution” state; absence is not a promise of a later result. |
| A captured event supplies execution and record IDs, but the record has not been retrieved | Retain the exact pointer and the retrieval state. A pending, inaccessible or exhausted search is a collection outcome, distinct from the task lifecycle. |

The meaning of the second row comes from the [EventBridge summary contract](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html). A later lifecycle event or resumed investigation is a new observation; it does not retroactively change what an earlier notification contained.

### Proposed semantic entities

| Derived entity | Meaning | Source requirement |
| --- | --- | --- |
| Finding | A published observation or conclusion relevant to the incident | Exact journal/summary fragment or validated structured field |
| EvidenceItem | A measurement, log excerpt, query result, trace reference, change record or external document | Source record/path plus original system/time range when explicitly provided |
| Hypothesis | An asserted possible explanation with any published disposition | Validated payload or attributed extraction; no private reasoning reconstruction |
| RootCauseAssessment | The agent's or operator's stated causal assessment | Exact cited conclusion; distinguish an assertion from independent verification |
| MitigationProposal | Proposed steps, scope and prerequisites | Published proposal content; no assumption that it was approved or executed |
| ActionObservation | Observed request, approval, execution or outcome | Separate source for each stage; no success inference from permission grant |
| ReviewResult | A quality evaluation of an investigation | Explicit review result/source and scope; no invented universal review schema |
| ResultDocument | A versioned rendering of a summary or other document | Source record revision, parser version, selection reason and phase |
| ResourceReference | A referenced resource identifier or URL | Explicit payload reference; namespace/type provenance |
| ArtifactReference | A reference to a file, asset version, URI or inline result | Resolvable source locator; unknown or unavailable remains explicit |

This is an application vocabulary, not a list of AWS result types. Do not create empty “native” hypothesis/evidence fields that imply the service promised them. The product guide describes findings, tool activity, agent collaboration, root cause and mitigation presentation; it does not publish the nested JSON schema for all of them. [Incident workflow](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

### Diagram D03 — every projection retains provenance

[Rendered SVG](diagrams/D03-projection-provenance.svg) · [Editable Mermaid](diagrams/D03-projection-provenance.mmd)

`SOURCE_REVISION` can represent a journal revision, event, task/execution observation, stream block or a referenced asset version. `DERIVED_REVISION` retains an immutable rendition of a timeline entry, finding, result document or graph assertion. Its logical item ID provides continuity across revisions.

```mermaid
erDiagram
    direction TB
    SOURCE_OBJECT ||--|{ SOURCE_REVISION : observed_as
    SOURCE_REVISION ||--o{ PROJECTION_SOURCE : supports
    DERIVED_REVISION ||--|{ PROJECTION_SOURCE : cites
    DERIVATION ||--o{ DERIVED_REVISION : produces
    SOURCE_OBJECT {
        string source_key PK
        string source_channel
        string native_id
    }
    SOURCE_REVISION {
        string revision_id PK
        string payload_hash
        datetime first_observed_at
    }
    PROJECTION_SOURCE {
        string source_ref_id PK
        string projection_revision_id FK
        string revision_id FK
        string locator
    }
    DERIVED_REVISION {
        string projection_revision_id PK
        string item_id
        string payload_hash
        string item_kind
        string assertion_origin
    }
    DERIVATION {
        string derivation_id PK
        string parser_version
        string rule_or_model_version
    }
```

A projection revision retains its payload/hash and derivation identity immutably. Snapshots reference projectionRevisionId, never only a mutable logical item ID or parser-version label. One source_ref_id identifies each citation, allowing several locators into the same source revision. Operator annotations are captured as application-origin source objects with author/time, so they can also satisfy provenance requirements.

A locator is a JSON Pointer, source text range or asset path tied to an exact source revision. Hashes establish which content was used, not whether a claim is true. Preserve unsupported content so new parsers can improve the view without refetching inaccessible historical material.

Every projection declares whether it is a direct field mapping, a deterministic parse, an operator annotation or an application inference. Application-generated confidence scores must never be displayed as AWS-provided confidence.

<!-- block: obsidian-devops-investigation-data-model-timeline -->
### Collection observations are separate from source revisions

D07 describes **read-based collection observations**. EventBridge deliveries, chat-stream receipts and operator annotations retain their own channel receipts; they do not manufacture native ReadAttempt rows. Those receipts can cite the same D03 SourceRevision abstraction.

A retained payload revision answers **what data was observed**. A read attempt answers **when and how collection tried to obtain data**, including attempts that returned no objects or failed. Repeated reads of unchanged content must not create additional logical records or erase the evidence that the source was checked again. This is a proposed application contract, not an additional AWS entity family.

| Application entity | Required meaning | Identity and retained evidence |
| --- | --- | --- |
| CollectionPass | One bounded reconciliation attempt for an investigation | Scoped investigation key, pass ID, start/end, collector version and selection policy |
| ReadAttempt | One operation/page attempt, including empty success or failure | Attempt ID, pass ID, native operation, effective query fingerprint, start/receipt time, outcome, modeled error/status and request ID when available |
| SourceObservation | One observed occurrence of a retained source revision | Observation ID, read-attempt ID, source-revision ID and receipt time; repeated identical payloads may cite the same revision |
| SourceRevision | One distinct retained payload for a logical source | Scoped source key, declared hash/canonicalization scheme and payload hash; native version remains an observed value |
| CoverageClaim | What a particular pass established for a particular query | Pass ID, query fingerprint, chosen traversal bounds, exhausted/partial/error/unknown state, as-of time and unresolved-reference reasons |

A query fingerprint identifies a traversal: owning entity scope, operation, filter/order/page-size configuration and relevant connection/authorization context. It excludes the changing `nextToken`. Retain exact page-request parameters, input/output tokens, retries and attempt order separately. A CoverageClaim cites the supporting read-attempt IDs/page chain and the evaluation policy. Keep native pagination tokens opaque; a token from one query must not continue another. A failed or empty read still has a ReadAttempt even though it has no SourceObservation rows. Polling an unchanged record creates another observation, while the distinct-record and distinct-revision counts stay unchanged.

### Diagram D07 — collection evidence and bounded coverage

[Rendered SVG](diagrams/D07-collection-observations.svg) · [Editable Mermaid](diagrams/D07-collection-observations.mmd)

`SOURCE_REVISION` is the same retained-payload entity as D03. The diagram shows selected attributes; authorization context, exact query parameters, timing, pagination and error details remain part of the read-attempt record.

```mermaid
erDiagram
    direction TB
    COLLECTION_PASS ||--o{ READ_ATTEMPT : issues
    READ_ATTEMPT ||--o{ SOURCE_OBSERVATION : returns
    SOURCE_REVISION ||--o{ SOURCE_OBSERVATION : seen_as
    COLLECTION_PASS ||--o{ COVERAGE_CLAIM : evaluates
    COLLECTION_PASS {
        string collection_pass_id PK
        string investigation_key FK
        datetime started_at
        datetime finished_at
    }
    READ_ATTEMPT {
        string read_attempt_id PK
        string collection_pass_id FK
        string operation
        string query_fingerprint
        string outcome
    }
    SOURCE_OBSERVATION {
        string observation_id PK
        string read_attempt_id FK
        string revision_id FK
        datetime observed_at
    }
    SOURCE_REVISION {
        string revision_id PK
        string source_key
        string payload_hash
    }
    COVERAGE_CLAIM {
        string coverage_claim_id PK
        string collection_pass_id FK
        string query_fingerprint
        string state
        datetime as_of
    }
```

Keep these rules explicit when translating the logical model into storage and APIs:

1. **Identity, revision and observation have different counting units.** Count journal records by the full space/execution/record key. Count executions by the scoped execution key. Deduplicate repeated memberships. Preserve every distinct payload revision and its observations separately.
2. **Latest observed is a selection policy.** A delayed response does not automatically establish the latest service state. Retain native version/timestamps and the observation order, flag conflicting payloads, and publish the policy used by the current view. Equal timestamps need a deterministic local tie-break, not a claim of service ordering.
3. **Coverage is bounded.** Exhausted pages describe the queried scope at the recorded time. They do not establish all future records, every relevant external data source, successful artifact retrieval, or a transactionally consistent AWS snapshot. The UI should say “No known collection gaps” with its scope, not imply universal evidence completeness.
4. **Projection publication is atomic within the application.** A header, its source inspector, counters and selected result must reference the same published view revision. Retaining old revisions is useful only if current controls resolve the intended revision exactly.
5. **Snapshot readability is independent of a current refresh, subject to current authorization and retention policy.** Render authorized retained sources and projections first. A technical current-refresh failure makes comparison unavailable; it must not prevent viewing an already retained capture. Revoked access must not be bypassed through a historical cache. A comparison result needs its own freshness and error state.

The offline prototype applies identity, deduplication, source selection and retained-history rules to its fixture. It does not implement a backend CollectionPass/ReadAttempt store. The future collector must produce those observations before it can claim measured synchronization coverage.

## 6. Timeline model

The operator needs several related timelines, not one indiscriminate timestamp sort:

- **Work lifecycle:** creation, triage, linking, execution status observations and phase milestones.
- **Published investigation activity:** journal records, findings, summaries and validated tool/subagent activity.
- **Conversation and decisions:** operator messages, streamed responses, approvals and resume attempts.
- **Incident evidence:** the time the affected system produced a log, metric or change, when supplied.
- **Collection history:** when the UI's backend fetched or received each observation.

### TimelineItem contract — application proposal

| Field | Purpose |
| --- | --- |
| `itemId`, `projectionRevisionId`, `investigationKey` | Stable logical identity, immutable rendition identity and scope |
| `executionKey?`, `parentItemId?` | Grouping from explicit relations; absence is allowed |
| `category`, `phase?`, `title`, `body` | Operator-facing classification and content |
| `occurredAt?`, `occurredAtBasis` | Event/evidence time and its meaning; can be unknown |
| `recordedAt?` | Native journal creation or source update time |
| `observedAt` | Backend receipt/fetch time |
| `sourceRefs[]`, `derivationId` | Provenance and parser/model revision |
| `assertionOrigin` | Native field, documented profile, deterministic parse, operator statement, application inference |
| `availability`, `completeness` | Pending, complete-for-source, unsupported, inaccessible or partial |
| `relatedResourceRefs[]`, `artifactRefs[]` | Optional validated links |
| `supersedesItemId?` | Corrected/replaced projection, preserving earlier state |

The fields are proposed API/view-model fields for your backend, not AWS request fields. The local prototype implements a documented subset; the optional application HTTP routes in the UI annex remain design examples, not deployed endpoints.

**Time semantics matter.** Journal `createdAt` is record creation time. Task/execution `updatedAt` is the last update, not necessarily a finish timestamp. EventBridge `time` represents the investigation/mitigation update time, not receipt by EventBridge. An evidence timestamp inside content may describe a much earlier system event. Preserve all clocks instead of rewriting them into one inferred incident time. [JournalRecord](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_JournalRecord.html) · [Event detail reference](https://docs.aws.amazon.com/devopsagent/latest/userguide/integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-devops-agent-events-detail-reference.html)

For deterministic presentation, order records by source event time where its meaning is known, then by a stable local tie-break. State clearly that the tie-break is a UI rule: the journal API promises timestamp direction but no same-time total order. Execution hierarchy and stream sequence are independent ordering dimensions.

Do not compute a percentage complete from journal count or elapsed time. You can report elapsed wall time, visible execution states, observed record count and last successful synchronization. These are observations; the total amount of future agent work is not in the public model.

Detailed synchronization, partial-page behavior and metric definitions are in [production UI contract](annexes/Investigation_UI_Contract.md).



<!-- block: obsidian-devops-investigation-data-model-graphs -->
## 7. Graphs: distinguish the relation being shown

The native operation/type inventory contains no published `Graph`, `Node`, `Edge`, `Hypothesis` or `Finding` entity and no graph-retrieval operation. Some IAM/web-app documentation mentions topology capabilities; an IAM action name alone is not a complete public API request/response contract. [Actions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Operations.html) · [Data types](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Types.html)

Nevertheless, several useful graphs can be built. They have different evidentiary strength:

| Graph | Available basis | Reliability and presentation rule |
| --- | --- | --- |
| Execution hierarchy | `executionId + parentExecutionId` | Direct field mapping; missing parents remain unresolved |
| Stream block hierarchy | `contentBlockStart.id + parentId` within a response/session | Direct mapping only when IDs are supplied; does not establish a durable tool-call or journal relationship |
| Task-link graph | `primaryTaskId` and linked-task query results | Direct linked-incident relation; not a fork or causality graph |
| Evidence/argument graph | Validated journal content or attributed extracted claims | Derived; every assertion needs source locators and an assertion origin |
| Resource topology | Explicit resource/dependency evidence or another independently integrated topology service | Derived/integrated; the current AgentSpace configuration does not supply a general topology API |
| Change-to-symptom causal graph | Published causal claim plus supporting observations | A claim with provenance; temporal adjacency alone does not establish causality |
| Knowledge/configuration graph | Asset profiles, skill/memory references, integration configuration | Contextual graph; current configuration does not prove historic consumption by an execution |

The UI should name the view: **Execution tree**, **Evidence map**, **Resource dependencies**, **Linked incidents**, or **Configuration context**. A single “Graph” tab that merges all edge meanings would obscure the distinction between observed relationships and inferred explanations.

### Diagram D04 — graph snapshot and typed edges

[Rendered SVG](diagrams/D04-graph-model.svg) · [Editable Mermaid](diagrams/D04-graph-model.mmd)

This application graph is independent of any particular graph database. Source provenance uses the D03 model.

```mermaid
erDiagram
    direction TB
    GRAPH_SNAPSHOT ||--o{ GRAPH_NODE : contains
    GRAPH_SNAPSHOT ||--o{ GRAPH_EDGE : contains
    GRAPH_NODE ||--o{ GRAPH_EDGE : source
    GRAPH_NODE ||--o{ GRAPH_EDGE : target
    RESOURCE_REF o|--o{ GRAPH_NODE : represented_by
    GRAPH_SNAPSHOT {
        string graph_id PK
        string graph_kind
        string projection_version
    }
    GRAPH_NODE {
        string graph_id PK,FK
        string node_id PK
        string node_kind
        string resource_ref_id FK
    }
    GRAPH_EDGE {
        string graph_id PK,FK
        string edge_id PK
        string source_node_id FK
        string target_node_id FK
        string relation_kind
        string assertion_origin
    }
    RESOURCE_REF {
        string resource_ref_id PK
        string namespace
        string external_id
    }
```

Graph nodes and edges reference their immutable D03 projection revisions. Both edge endpoints join within the same graph snapshot: (graph_id, source_node_id) and (graph_id, target_node_id) reference (graph_id, node_id). Create clearly labeled placeholder nodes for unresolved endpoints; a placeholder represents a missing reference, not a fabricated resource.

Recommended node kinds are `execution`, `resource`, `observation`, `hypothesis`, `change`, `action` and `document`. Recommended relation kinds include `parent_execution`, `references`, `supports`, `contradicts`, `depends_on`, `precedes` and `asserted_cause_of`. These are application vocabularies, not AWS enums.

For each node/edge retain:

- Stable identity, graph kind and graph snapshot/projection version.
- Exact source references and parser/extractor version.
- Assertion origin: explicitly reported by the agent, operator-confirmed, independently observed, or inferred by the application.
- Any published confidence/disposition as a source value; absence stays absent.
- A display label and explanation separate from the raw evidence.
- Validity/observation times and unresolved/dangling-reference state.

Do not infer a causal edge from an execution parent edge, convert an unreferenced summary sentence into a confirmed root cause, or expose a guessed internal reasoning chain as the agent's actual reasoning. The application can show published reasoning artifacts and attributed extractions.

Charts have the same boundary: there is no universal native time-series schema in Task or JournalRecord. A metric chart needs validated points, units, aggregation, source query and time window from a supported payload or an additional telemetry integration. A prose mention of “CPU increased” cannot produce an exact numeric chart.

<!-- block: obsidian-devops-investigation-data-model-artifacts -->
## 8. Artifacts, assets and reproducibility

### Keep three artifact sources separate

1. **Native Asset API:** addressable assets with versions and files.
2. **Journal/stream result content:** inline summaries, references, tool results and other payloads.
3. **A2A artifacts:** protocol-level result artifacts returned through that separate interface.

An application `ArtifactReference` unifies discovery and presentation while preserving the source channel. It does not assert that an A2A artifact ID or a journal reference is a native `assetId`.

The Asset API exposes metadata and version separately from content. `GetAssetContent` returns a JSON response whose `content.zipFile` member contains the ZIP blob, alongside `version`; it is not a raw HTTP ZIP response. An SDK decodes the blob according to its language-specific representation. File retrieval returns path/content/version/timestamps, with content expressed as a text-or-bytes union. Use a specific `assetVersion` for reproducible historical reads; an unversioned read returns the latest. [Asset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Asset.html) · [GetAssetContent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetContent.html) · [GetAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetFile.html)

### Diagram D05 — investigation references and native asset history

[Rendered SVG](diagrams/D05-artifacts-assets.svg) · [Editable Mermaid](diagrams/D05-artifacts-assets.mmd)

`INVESTIGATION` and `ARTIFACT_REF` are application entities. The other entities normalize native Asset/version/file responses. A reference can remain inline or external, so its AssetVersion relation is optional.

```mermaid
erDiagram
    direction TB
    INVESTIGATION ||--o{ ARTIFACT_REF : references
    ASSET_VERSION o|--o{ ARTIFACT_REF : may_resolve
    ASSET ||--|{ ASSET_VERSION : observed_versions
    ASSET_VERSION ||--o{ ASSET_FILE : contains
    INVESTIGATION {
        string investigation_key PK
    }
    ARTIFACT_REF {
        string artifact_ref_id PK
        string source_kind
        string source_locator
        string resolution_state
        string asset_version_key FK
    }
    ASSET {
        string space_key PK
        string asset_id PK
        string asset_type
    }
    ASSET_VERSION {
        string asset_version_key PK
        int version
        string metadata_hash
    }
    ASSET_FILE {
        string asset_version_key PK,FK
        string path PK
        string content_kind
        string content_hash
    }
```

**No general investigation-to-asset foreign key is published.** Asset bodies omit task/execution IDs, and `ListAssets` has no execution/task filter. Scope comes from the request. An attachment ID sent through `SendMessage.assetIds` is an explicit request relationship; a generic asset in the same Agent Space is not automatically an output or input of that investigation. [ListAssets](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssets.html) · [SendMessage](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessage.html)

`SendMessage.assetIds` establishes a request attachment-ID relationship; acceptance and actual use are separate observations. The request does not specify the consumed version. A version retrieved nearby is an observed version unless the actual consumed version is independently established.

A useful `ArtifactReference` holds source channel, source record/block, native ID if present, URI/path, optional asset ID/version, content/media hints, retrieved hash, availability and retrieval authorization state. Preserve unknown media types. Missing, access denied, not yet published, unsupported and deleted are different states.

### Documented Asset profiles

The AWS managing-assets guide documents current types `skill`, `agents_md`, `attachment`, `custom_agent`, `memory_store`, `memory`, `test_profile` and `feedback`. The model itself uses an open asset-type string; query `ListAssetTypes` and tolerate future types. [Managing assets](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html)

Relevant documented links inside metadata are:

| Profile | Documented relationship | Investigation UI use |
| --- | --- | --- |
| custom_agent | `skills[]` and `memory_stores[]` refer to existing same-space asset IDs | Explain configuration when explicitly tied to an execution |
| memory | `memory_store_id` refers to the containing store asset | Knowledge context, with version/time qualifications |
| feedback | Optional `execution_id`, immutable after create | Associate recorded feedback with an execution; no native server-side execution filter on ListAssets |

These are **documented metadata profiles**, not newly typed fields in the generic Asset response. Separately, the native Trigger resource carries a JSON action document. The documented custom-agent action profile uses `Trigger.action.actionType = "create:task"` and `Trigger.action.task.agent = "custom:<assetId>"`; Trigger is not an Asset type. [Trigger](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Trigger.html) · [CLI example](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-cli-onboarding-guide.html) Do not infer that a historical run used the current versions of all referenced skills or memories. Preserve configuration snapshots when the application can collect them, and label whether they are known inputs or merely contemporaneous workspace context.

### Export and retention

For a defensible investigation export, include source envelopes/revisions, selected summaries, graph/timeline projections with parser versions, referenced asset versions actually retrieved, provenance locators, timestamps, known gaps and a manifest of hashes. Retain external URIs as references; copying external content requires appropriate access and retention policy.

The reviewed native contract does not establish a uniform journal retention window, a complete archive endpoint or an immutable final investigation package. If future access to the original record matters, the redesigned application needs its own authorized retention policy.

<!-- block: obsidian-devops-investigation-data-model-context -->
## 9. Results that belong beside the investigation

### Recommendations and goals

A `Recommendation` explicitly includes a `taskId` and optional `goalId`/`goalVersion`. Its content has a required summary and optional spec, alongside status, priority, ranking and version fields. `Goal` has current content/status/schedule plus last-task pointers. These are useful cross-links to prevention work. [Recommendation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Recommendation.html) · [Goal](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Goal.html)

Preserve their own identity and lifecycle. Recommendation priorities are HIGH/MEDIUM/LOW, while investigation task priorities have five values. A recommendation marked COMPLETED is not an investigation completion event. Do not classify every recommendation as the incident's root cause or immediate mitigation.

### Review and feedback

An investigation Review evaluates the published record and returns its assessment alongside the investigation; the product guide says it does not rerun or alter the investigation. It is analytically useful to retain both the reviewed source snapshot and the assessment. The reviewed native model does not define a universal `ReviewResult` structure or standalone Review CRUD family. Treat a rich review panel as a documented capability whose payload mapping still needs validation. [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html)

Feedback assets provide one documented execution association. Operator annotations written only in the redesigned UI are a separate application entity and must not be represented as feedback submitted to AWS until the relevant service call succeeds.

### Context snapshots

Configuration at read time may differ from configuration during the incident. Store `observedAt` and version/hash on Agent Space, association, asset and trigger context if retained for historical interpretation. Record explicit run-consumed inputs separately from current or contemporaneous configuration.

A relationship diagram can explain configured access without proving successful access. Tool permission failures, missing telemetry, inaccessible repositories and source-query failures must remain visible evidence gaps when published.

<!-- block: obsidian-devops-investigation-data-model-snapshots -->
## 10. Historical snapshots and result readiness

### Diagram D06 — immutable application snapshots

[Rendered SVG](diagrams/D06-historical-snapshots.svg) · [Editable Mermaid](diagrams/D06-historical-snapshots.mmd)

`SOURCE_REVISION` is the same concept as D03. A snapshot is a manifest of a captured set of sources and derived items; it is not a new AWS resource.

```mermaid
erDiagram
    direction TB
    INVESTIGATION ||--o{ SNAPSHOT : captured_as
    SNAPSHOT ||--|{ SNAPSHOT_SOURCE : freezes
    SOURCE_REVISION ||--o{ SNAPSHOT_SOURCE : included_in
    SNAPSHOT ||--o{ SNAPSHOT_PROJECTION : includes
    INVESTIGATION {
        string investigation_key PK
    }
    SNAPSHOT {
        string snapshot_id PK
        datetime capture_started_at
        datetime capture_finished_at
        string completion_basis
        string coverage_state
    }
    SNAPSHOT_SOURCE {
        string snapshot_id PK,FK
        string revision_id PK,FK
    }
    SOURCE_REVISION {
        string revision_id PK
        string source_key
        string payload_hash
    }
    SNAPSHOT_PROJECTION {
        string snapshot_id PK,FK
        string projection_revision_id PK,FK
        string payload_hash
    }
```

Capture task version, execution membership, all fetched journal revisions, completion events and exact summary pointers. Pin or copy the CollectionPass, supporting read-attempt/page-chain evidence and CoverageClaim revisions used by the capture; a later successful refresh must not rewrite earlier coverage. Include per-execution pagination coverage, unresolved references, inaccessible content and parser versions. Because the API does not provide a transactionally consistent cross-endpoint snapshot, record **capture start/end** and any source changes observed during collection.

A reasonable application policy is to perform terminal reconciliation, retrieve referenced results, compare a follow-up task/execution observation, and create a snapshot with the known coverage. Repeated identical reads increase confidence in stability; they do not prove a service-guaranteed finalization barrier. The UI should say “Snapshot captured at …” or “Available results as of …”.

If the investigation continues, retain the prior snapshot and produce new observations and a later snapshot. Do not silently rewrite the report an operator already reviewed.

### Availability is a structured object

Represent availability per phase/result, not as one `isDone` boolean:

| Application condition | Operator-facing treatment |
| --- | --- |
| Task active; records arriving | Show live activity and synchronization freshness |
| Task completed; summary pointer present; record not fetched | “Completed — retrieving referenced summary” |
| Task completed; captured completion event omitted the summary pointer | “Completed — no summary reported for this execution”; do not promise eventual arrival |
| Several summary records; no authoritative pointer captured | Show candidates and selected-display policy |
| Some executions/pages inaccessible | Show known results with partial coverage and the affected sources |
| Unknown record types | Show raw records plus unsupported-renderer count |
| Captured snapshot | Show capture window, source versions, completeness and later updates if any |
| Continued investigation | Keep old snapshot accessible; current view returns to live mode |

The EventBridge pointer contract is explicit. Separately, A2A documentation warns that terminal task status may precede result-artifact availability. That warning is not a published maximum lag or a native-journal consistency guarantee. [EventBridge summary retrieval](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html) · [A2A interface](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html)

<!-- block: obsidian-devops-investigation-data-model-feasibility -->
## 11. What the redesigned UI can promise

| Feature | Feasibility from reviewed contract | Additional work |
| --- | --- | --- |
| Investigation list/details | Native Task APIs | Scope, filters, pagination, stale/error presentation |
| Linked-incident view | Native primaryTaskId/reference fields | Preserve missing/historical associations |
| Execution tree | Native Execution parent relationship | Collect every task-scoped page, handle unresolved parents |
| Journal timeline/raw record inspector | Native journal envelope/content | Pagination, deterministic display, safe rendering |
| Live chat response | Native SendMessage EventStream | Session/block assembly, dropped-stream handling |
| Completion/mitigation milestones | Documented EventBridge events | Durable ingestion, dedupe, reconciliation |
| Exact summary retrieval | Documented record types + event pointer | Traverse pages, preserve unavailable/absent distinction |
| Versioned asset/file browser | Native Asset APIs | Only attach to investigations through explicit evidence |
| Rich tool/evidence timeline | Partly specified | Capture representative payloads and validate parser profiles |
| Hypothesis/causal graph | Application projection | Explicit assertions, source locators, provenance and uncertainty |
| Complete underlying telemetry charts | Not supplied as a universal investigation response | Validated query-result payloads or additional telemetry APIs |
| Immutable historical report | Application capability | Source retention, snapshot manifests and versioned projections |
| Complete operator-app feature parity | Not established | Resolve fork/resume/triage/readback/visibility contracts with AWS |

### Recommended storage boundary

Use a relational core for identities and joins, JSON storage for intact AWS payloads, and file/object storage for retained artifacts where necessary. Index derived entities for UI queries. The reviewed contract does not require a graph database: graph views can be materialized from node/edge tables with provenance.

Raw captures should survive a parser upgrade. A failed renderer must not corrupt source data; a new parser can rebuild projections against retained revisions. Historical results should retain the derivation version actually used, even if the current parser produces an improved view.

### Definition of a useful first release

Deliver an investigation list, separate lifecycle/freshness indicators, an execution tree, journal chronology, exact summary selection, linked tickets, explicit asset references and retained snapshots. Add a raw-record inspector with copy/export and an unknown-type fallback.

Promote richer evidence, tool-call, graph, review and approval-resumption experiences only after their payload profiles and recovery paths have been exercised against authorized representative investigations. The capture matrix and acceptance criteria are in [production UI contract](annexes/Investigation_UI_Contract.md).

<!-- block: obsidian-devops-investigation-data-model-conclusion -->
## 12. Design invariants

1. Investigation identity is the native backlog task identity scoped to account, Region and Agent Space.
2. Task-to-execution membership is retained from requests; the associated execution pointer is not the entire run set.
3. A lifecycle state is not a result-availability guarantee.
4. Every semantic result and graph assertion can be traced to a retained source revision or an explicit operator/application inference.
5. An unsupported content type remains visible and exportable.
6. A complete page traversal is coverage of that fetch, not a global immutable snapshot guarantee.
7. Current configuration is not automatically historical execution context.
8. Permission grant, resume acknowledgement, tool execution and verified mitigation outcome are separate facts.
9. Historical snapshots remain immutable in the application when the current investigation continues.
10. An AWS web-app feature or IAM action does not by itself establish a public SDK operation.

The following sections bring the three workflow diagrams into the same report. [operation inventory and selected schemas](annexes/Investigation_API_Catalog.md) retains exact fields, [production UI contract](annexes/Investigation_UI_Contract.md) retains the full synchronization/view contract, and [source and model provenance](annexes/Investigation_API_Sources.md) records evidence and model provenance.


## 13. Collection and live updates

The proposed backend first retains native observations, then builds the operator view. `ListExecutions(taskId)` establishes membership; `ListJournalRecords(executionId)` supplies the published record envelope. EventBridge is a lifecycle input that triggers reconciliation, while `SendMessage` streams the response to a chat interaction. A2A remains a separate adapter with its own task identity, state mapping and artifacts. The complete contracts are in the [production UI annex](annexes/Investigation_UI_Contract.md).

### Diagram U01 — reconcile snapshots and journals

[Rendered SVG](diagrams/U01-live-reconciliation.svg) · [Editable Mermaid](diagrams/U01-live-reconciliation.mmd)

This is a proposed backend sequence, not a service-guaranteed ordering. Background notifications and user requests can both trigger reconciliation.

```mermaid
sequenceDiagram
    participant UI as Operator UI
    participant B as UI backend
    participant AWS as AWS API
    participant S as Source store
    UI->>B: Open investigation
    B->>AWS: GetBacklogTask
    AWS-->>B: Task and version
    B->>S: Retain task observation
    B->>AWS: ListExecutions across all pages
    AWS-->>B: Executions and memberships
    loop Each discovered execution and page
        B->>AWS: ListJournalRecords
        AWS-->>B: Records and token
        B->>S: Upsert source revisions
    end
    B->>S: Build projections and coverage
    B-->>UI: View with freshness and gaps
    loop Poll or lifecycle notification
        B->>AWS: Reconcile affected sources
        AWS-->>B: Current observations
        B->>S: Retain and reproject
        B-->>UI: Revisioned view update
    end
```

A responsive implementation can render recent records before older history is loaded, while maintaining per-execution coverage. A complete page traversal means that particular fetch reached its end, not that all future records are known. Retain query/filter context, deduplicate scoped IDs, detect repeated page tokens, and preserve unresolved parents and unsupported JSON. A failed rich-content parser must leave the source record inspectable.

| Channel | Retained identity and observations | Role in the operator view |
| --- | --- | --- |
| Native reads | Scoped resource IDs, request membership, received payloads, observation times | Reconciled task/execution/journal/asset state |
| EventBridge | Event ID, source account/Region, detail type, subject IDs, source time, optional exact summary pointer | Published lifecycle observations and refresh triggers |
| Native chat stream | Local request/session, execution/response/block IDs where supplied, sequence/delta fragments | Incremental conversation response; interrupted assembly remains visible |
| A2A | Interface tenant, protocol task ID, status and artifact metadata | Explicit protocol adapter; terminal status and artifact availability remain distinct |

The native journal API supplies timestamp ordering and page tokens, with a maximum page size of 100; it does not publish a `since` filter, durable change cursor or same-timestamp causal order. Native stream `responseCompleted` closes one response and carries no final content capable of repairing missing blocks. An already terminal A2A investigation rejects a subscription; use its documented `GetTask` path and preserve any artifact-readiness gap. [Journal API](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html) · [Native stream union](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageEvents.html) · [A2A guide](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html)

## 14. Decisions and action observations

Directed-action approvals are documented for chat. An autonomous investigation's mutating tool call fails rather than opening that approval flow. The supported API sequence is a scoped `UpdateApprovalAction` decision followed by a separate `SendMessage` carrying approval-resumption context. An approval decision, a resume submission, an action observation and verified recovery are distinct records. [Directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

### Diagram U02 — decision, resume and observed outcome

[Rendered SVG](diagrams/U02-approval-lifecycle.svg) · [Editable Mermaid](diagrams/U02-approval-lifecycle.mmd)

These are application audit entities around the native command/value objects. APPROVAL_REQUEST identifies an observed request context, including execution/tool/interrupt IDs; it is not a claim that a reusable native approval can only be associated with one execution. Keep the space-scoped native approvalId separately. A decision does not prove a resume or action outcome.

```mermaid
erDiagram
    direction TB
    EXECUTION ||--o{ APPROVAL_REQUEST : pauses_for
    APPROVAL_REQUEST ||--o{ DECISION_ATTEMPT : resolved_by
    DECISION_ATTEMPT ||--o{ RESUME_ATTEMPT : followed_by
    EXECUTION ||--o{ ACTION_OBSERVATION : publishes
    APPROVAL_REQUEST o|--o{ ACTION_OBSERVATION : may_correlate
    EXECUTION {
        string execution_key PK
    }
    APPROVAL_REQUEST {
        string approval_key PK
        string approval_id
        string interrupt_id
        string tool_use_id
    }
    DECISION_ATTEMPT {
        string attempt_id PK
        string action
        string finalized_pattern_hash
        string submission_state
    }
    RESUME_ATTEMPT {
        string attempt_id PK
        string decision_attempt_id FK
        string submission_state
    }
    ACTION_OBSERVATION {
        string observation_id PK
        string outcome_kind
        string source_revision_id
    }
```

The diagram is an application audit model. It does not create a native approval-read endpoint or imply that every execution can be an interactive chat target. Preserve opaque tool, interrupt and approval identifiers, exact approved scope and each submission outcome. A response lost after submission creates an ambiguous outcome; a client cannot solve that by inventing idempotency or by broadening approval.

The reviewed native operation set has no companion approval Get/List/Revoke operation. `UpdateApprovalAction` and `SendMessage` have no modeled client-token input. A returned task version is also insufficient for native compare-and-swap: `UpdateBacklogTask` exposes no expected-version precondition. [Native actions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Operations.html) · [UpdateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html)

## 15. Capture and historical review

The snapshot is an application-owned historical artifact. Its manifest includes the task observation/version, execution membership, exact journal revisions, chosen summaries, retained artifact versions, immutable projection revisions, capture interval, parser versions, and the collection gaps known at capture.

### Diagram U03 — application snapshot workflow

[Rendered SVG](diagrams/U03-snapshot-workflow.svg) · [Editable Mermaid](diagrams/U03-snapshot-workflow.mmd)

These are **application presentation states**, not AWS Task transitions. A historical snapshot remains readable while the current investigation changes.

```mermaid
flowchart TB
    L["Live view"] -->|Manual capture or terminal observation| R["Reconcile sources"]
    R --> Q{"Capture query set reconciled?"}
    Q -->|Yes| S["Retain historical snapshot"]
    Q -->|No| P["Show partial results and gaps"]
    P -->|Retry| R
    P -->|Accept partial capture| S
    S -->|New activity in current view| L
```

A partial snapshot is allowed when explicitly requested by the application policy. Its stable identity means that its retained contents will not change; it does not mean the investigation data were complete. Later investigation activity updates the live view and can create a new snapshot. The original remains readable and comparable.

Useful comparisons include a new execution, added or changed source observations, a newly resolved exact summary pointer, a different artifact version, changed assertions and improved coverage. Label a parser-only projection change separately from newly collected AWS evidence. State durations are observation-dependent; neither task age nor `updatedAt - createdAt` establishes MTTR without a separate incident-start and recovery definition.

## 16. Prototype contract and production boundary

The [single-page application](index.html) is a **fictional operator demonstration** of this model. Its accounts, Agent Space, incident titles, telemetry points, deployments, resources, journals and conclusions are synthetic. Familiar AWS operation names, native field names and enum values illustrate the reviewed contract. The application does not query a customer AWS account, start an agent, change infrastructure or submit an approval.

The demonstration separates four levels of ownership:

| Prototype data | Ownership and interpretation |
| --- | --- |
| Task, execution, journal and asset-shaped fixtures | Synthetic examples of documented native envelopes, with normalized application timestamps |
| Completion-summary pointer | A fictional notification illustrating the documented exact-record selection rule |
| Timeline, findings, telemetry charts and evidence edges | Application projections over explicit synthetic profiles; they are not undocumented AWS schemas |
| Capture, comparison, replay controls and export | Local application behavior; replay timing is a presentation choice rather than an AWS performance claim |

When interpreting a demo source inspector, distinguish a **mock native-shaped observation** from a byte-for-byte HTTP capture. The source APIs use their documented timestamp encodings; SDK-normalized dates or application ISO strings are display/storage choices. Unsupported journal content can be an object, array, scalar, boolean or null and should remain inspectable.

The model hashes parsed source envelopes using its explicitly named `sorted-json-utf8/v1` algorithm; downloadable artifact hashes cover their UTF-8 file bodies. These hashes detect disagreement under the declared encoding. They do not preserve the original HTTP bytes, authenticate AWS origin, provide arbitrary-precision JSON-number handling, or make browser storage tamper-proof. Exact encoding, saved-state compatibility and public function behavior are documented in the [prototype model contract](app/MODEL_CONTRACT.md).

### Three distinct API surfaces

| Surface | Current contract and implementation |
| --- | --- |
| Native AWS API | Pinned REST-JSON/SigV4 inventory. The reviewed operation bindings include 28 `cp.` and 35 `dp.` endpoint prefixes, success codes and modeled errors. The catalog is the transport reference. |
| Prototype `DemoModel` | Implemented synchronous JavaScript functions over synthetic observations. Scoped lookup, projection, capture, restoration and export are exercised by tests; thrown errors are local exceptions, not HTTP responses. |
| Proposed application backend | Example HTTP resources and update concepts in the UI annex. Authentication, stable pagination, section failures, update ordering, cursor expiry, retention and export controls still require an implemented and validated service contract. |

The native error contract needs operation-aware treatment: 402 is modeled for service quota exhaustion, 413 for excessive content size, and a stream can report failure after a successful HTTP response. An absent modeled HTTP trait is not a license to invent one; the catalog distinguishes model facts from codes supplied by operation documentation. See the [transport and error tables](annexes/Investigation_API_Catalog.md).

The intended demonstration covers live analysis, result retrieval after a completed observation, evidence/record inspection, explicit artifact availability, and historical preservation when an investigation resumes. The [application README](README.md) is authoritative for implemented controls and their verification. This report describes the larger model; diagram coverage does not imply that the prototype implements every AWS API family or approval path.

An already selected historical capture remains renderable if current task and portfolio assembly fail; the UI marks current comparison unavailable and disables live capture/replay. This is a local failure-path regression, not a live outage experiment. Startup routing from an unavailable live view, backend retention and current authorization enforcement remain integration responsibilities. The screen presents the investigation result; the model also carries a separate mitigation result slot.

### What a production integration must add

1. An authorized backend and principal-sensitive cache boundaries for the actual owning account, Region and Agent Space.
2. SDK/API collectors with complete pagination, retries, conflict handling, observation retention and coverage manifests.
3. Representative captured fixtures for every rich journal/stream profile that the UI supports.
4. Validated identity joins for chat/A2A, exact result references and asset versions actually consumed.
5. Durable source and projection retention for reproducible history, with access and retention policy applied to exports.
6. A separately validated mutation and ambiguous-outcome recovery contract before enabling production actions.

The 24-case [capture matrix](annexes/Investigation_UI_Contract.md#8-capture-matrix-and-acceptance-criteria) distinguishes these future live-service checks from the local demo validation.

## 17. Sources and review provenance

The initial model came from [source commit `1d10b2d`](https://github.com/lyrel-dev/frontier-agents/commit/1d10b2de6616ff3d94e97a579c6291cc3696c03a). The independent review re-fetched the official pinned models, compared the current Botocore file, checked the catalog's operation and member contracts, and revisited the current AWS pages for native state, summaries, resumption, streaming, asset versions and approvals.

| Evidence | Reviewed result |
| --- | --- |
| Botocore API version | `2026-01-01` |
| Botocore current versus pinned file | Byte-identical at the review; 357,369 bytes |
| Botocore SHA-256 | `c9650e8c0aa3546f3f45ecb829f96223156bfc07f720b580bed23a7407aaad59` |
| Pinned Go and JavaScript models | 655,409 bytes each; identical to each other |
| Go/JavaScript SHA-256 | `df172e1f6c0692bb1e4d766a1961fd63aa53a5750a82cafcef5df2a96933c8c5` |
| Catalog checks | 63 routes/output-field lists and transport/error mappings; 19 requests and 52 selected type tables, 339 expanded member rows |
| Current diagram source set | D01–D07 and U01–U03; eight ERDs, one sequence diagram and one flowchart |
| Account-level evidence | No customer account, production response or live AWS mutation used |

The [source register](annexes/Investigation_API_Sources.md) contains exact official model URLs and the primary-reference map. [REVIEW.md](REVIEW.md) preserves the initial decisions; [QUALITY_REVIEW.md](QUALITY_REVIEW.md) records the adversarial corrections and remaining limits. Executed checks and current rendering results are in [VALIDATION.md](VALIDATION.md), rather than being inferred from the source-branch documentation checks.
