---
title: "AWS DevOps Agent investigation API sources and provenance"
id: aws-devops-analysis-investigation-api-sources
kind: obsidian-note
product: devops
type: source-index
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
  - "../report.md"
  - "../REVIEW.md"
---

<!-- block: obsidian-devops-investigation-api-sources-scope -->
# Investigation API evidence and validation

## 1. Review scope

This addendum was reviewed on **5 November 2026** to prepare an investigation-focused operator UI. It analyzes the official AWS DevOps Agent API, current AWS product guides, and official SDK service models. The original dossier and presentation retain their separate **31 October 2026** source cutoff; this is not a refresh of every claim in those earlier notes.

The analysis covers:

- All **63 native operations**, grouped by entity family.
- The official model's **560 shapes**, with explicit examination of investigation-relevant contracts.
- **19 request structures** and **52 selected returned/nested structures** expanded into the field catalog.
- Native task/execution/journal/message/asset identifiers, states, timestamps, pagination and mutations.
- Documented EventBridge, native chat-stream and A2A boundaries.
- Proposed logical entities for timelines, evidence, graphs, artifacts, provenance and immutable historical snapshots.
- **Nine Mermaid diagrams:** seven ER diagrams, one sequence diagram and one flowchart.
- A future implementation capture/acceptance matrix; no account-level test has been performed.

No live AWS API calls, production payloads, credentials, deployments or service mutations were used. The study establishes a public-contract-based design and identifies where representative service captures or an AWS clarification are still required.

<!-- block: obsidian-devops-investigation-api-sources-pins -->
## 2. Reproducible model provenance

The API version is `2026-01-01`. It is an interface version label, not the date this research was performed or a guarantee that later model revisions will be identical.

| Official model | Repository commit | Commit time |
| --- | --- | --- |
| [Python SDK/Botocore service model](https://raw.githubusercontent.com/boto/botocore/27fc40eff0e85422e62858ee3d2e9a133bdb1038/botocore/data/devops-agent/2026-01-01/service-2.json) | `27fc40eff0e85422e62858ee3d2e9a133bdb1038` | 2026-10-21 18:09:16 UTC |
| [AWS SDK for Go v2 Smithy model](https://raw.githubusercontent.com/aws/aws-sdk-go-v2/e92707e9ed82a8800ab086bc2f5be33524b9d06b/codegen/sdk-codegen/aws-models/devops-agent.json) | `e92707e9ed82a8800ab086bc2f5be33524b9d06b` | 2026-10-21 18:08:21 UTC |
| [AWS SDK for JavaScript v3 Smithy model](https://raw.githubusercontent.com/aws/aws-sdk-js-v3/c5d8365175b93e38932d1aad1e07bed07a1b3641/codegen/sdk-codegen/aws-models/devops-agent.json) | `c5d8365175b93e38932d1aad1e07bed07a1b3641` | 2026-10-21 18:26:27 UTC |

Downloaded current-path models were compared byte-for-byte with these pinned revisions. The Go and JavaScript Smithy files are identical to each other.

| Model | Bytes | SHA-256 |
| --- | ---: | --- |
| Botocore | 357369 | `c9650e8c0aa3546f3f45ecb829f96223156bfc07f720b580bed23a7407aaad59` |
| Go and JavaScript Smithy | 655409 each | `df172e1f6c0692bb1e4d766a1961fd63aa53a5750a82cafcef5df2a96933c8c5` |

Model metadata identifies `DevOps Agent`, endpoint/signing name `aidevops`, REST-JSON and SigV4. SDK/CLI client naming is `devops-agent`. These names should not be interchanged indiscriminately in code, IAM policies and transport configuration.

The catalog was generated from member names, references, required lists, enums, ranges, patterns, union flags and HTTP bindings. It does not copy provider-specific long-form configuration prose into the investigation model.

### Recheck a pinned snapshot

The following optional read-only Python check verifies the primary model checksum and inventory size:

```python
import hashlib
import json
import urllib.request

url = (
    "https://raw.githubusercontent.com/boto/botocore/"
    "27fc40eff0e85422e62858ee3d2e9a133bdb1038/"
    "botocore/data/devops-agent/2026-01-01/service-2.json"
)
raw = urllib.request.urlopen(url, timeout=30).read()
assert hashlib.sha256(raw).hexdigest() == (
    "c9650e8c0aa3546f3f45ecb829f96223156bfc07f720b580bed23a7407aaad59"
)
model = json.loads(raw)
assert model["metadata"]["apiVersion"] == "2026-01-01"
assert len(model["operations"]) == 63
assert len(model["shapes"]) == 560
```

This pins the research evidence. A production implementation should compare its chosen SDK's model with this snapshot and review changes rather than assuming the API-version string alone detects drift.

<!-- block: obsidian-devops-investigation-api-sources-index -->
## 3. Primary reference map

Every operation and selected type in [complete API catalog](Investigation_API_Catalog.md) links to its official reference. The following pages supply the main semantic decisions in the model/UI notes.

| Source | Principal use |
| --- | --- |
| [API welcome](https://docs.aws.amazon.com/devopsagent/latest/APIReference/Welcome.html) | Service boundary |
| [Actions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Operations.html) | Supported native operation inventory; absence claims scoped to this inventory |
| [Data types](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Types.html) | Published type inventory |
| [Task](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Task.html) | Investigation discriminator, status, optional execution/link/reference fields |
| [TaskFilter](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_TaskFilter.html) | Creation-time bounds and linked-task filtering |
| [CreateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html) | Native create fields and idempotency |
| [GetBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetBacklogTask.html) | Task retrieval |
| [ListBacklogTasks](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListBacklogTasks.html) | Filter/sort restrictions and pagination |
| [UpdateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html) | Status update surface, absent expected-version field |
| [Execution](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html) | Parent relation, open agent labels and execution status |
| [ListExecutions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListExecutions.html) | Task-scoped membership retained from request context |
| [JournalRecord](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_JournalRecord.html) | Envelope fields, arbitrary JSON content and attribution |
| [ListJournalRecords](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html) | Record filtering/order, pagination and missing change-feed fields |
| [ReferenceOutput](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ReferenceOutput.html) | External incident and association reference |
| [ListPendingMessages](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListPendingMessages.html) | Pending queue rather than complete conversation archive |
| [SendMessage](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessage.html) | Interactive request, attachments, identity deprecation and stream |
| [SendMessageEvents](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageEvents.html) | Streaming union, content-block lifecycle |
| [SendMessageContext](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContext.html) | Approval resumption context |
| [SendMessageContentBlockStartEvent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockStartEvent.html) | Optional block ID/index/parent/sequence |
| [SendMessageContentBlockDelta](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockDelta.html) | Text-versus-JSON delta union |
| [SendMessageJsonDelta](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageJsonDelta.html) | Partial JSON fragment |
| [SendMessageContentBlockStopEvent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContentBlockStopEvent.html) | Optional accumulated block content |
| [SendMessageResponseCompletedEvent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageResponseCompletedEvent.html) | Response completion has no final content field |
| [ApprovalAction](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ApprovalAction.html) | Opaque resume/tool/approval identifiers |
| [ApprovalPattern](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ApprovalPattern.html) | Tool and argument pins |
| [Boto3 UpdateApprovalAction](https://docs.aws.amazon.com/boto3/latest/reference/services/devops-agent/client/update_approval_action.html) | Approval decision fields and constraints; fallback to pinned model if an HTML API route redirects |
| [AgentSpace](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_AgentSpace.html) | Workspace fields and inherited connection scope |
| [Association](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Association.html) | Service configuration and association identity |
| [RegisteredService](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_RegisteredService.html) | Registration context and provider details |
| [Asset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Asset.html) | Generic asset metadata/version, no task ID |
| [ListAssets](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListAssets.html) | Space/type/update filters, no execution filter |
| [GetAssetContent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetContent.html) | ZIP bytes and explicit returned version |
| [GetAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetFile.html) | File path/content/asset version |
| [Recommendation](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Recommendation.html) | Task/goal relationships and independent lifecycle |
| [Goal](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Goal.html) | Goal content, schedule and last-task pointers |
| [Trigger](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Trigger.html) | Separate native trigger resource and JSON action |
| [AWS REST-JSON protocol](https://smithy.io/2.0/aws/protocols/aws-restjson1-protocol.html) | Body timestamp serialization and union representation |

### AWS user-guide contracts

| Source | Principal use |
| --- | --- |
| [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) | Published operator workflow, mutable completion, chat/fork/triage behavior |
| [EventBridge integration](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html) | Exact summary record-type strings and retrieval procedure |
| [Event detail reference](https://docs.aws.amazon.com/devopsagent/latest/userguide/integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-devops-agent-events-detail-reference.html) | Optional execution/summary fields, cancellation spelling, phase distinction |
| [A2A server integration](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html) | Separate transport/identity/state domain, terminal subscription and artifact availability |
| [Directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) | Scoped approval then resume protocol |
| [Managing assets](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html) | Eight documented asset profiles and metadata relationships |
| [CLI onboarding](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-cli-onboarding-guide.html) | Built-in AWS service association and custom trigger examples |
| [Reviewing investigations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) | Assessment alongside an investigation, without rerunning it |
| [What's new](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html) | November 2 All-chats feature versus current native list parameters |

<!-- block: obsidian-devops-investigation-api-sources-conflicts -->
## 4. Reconciliation decisions

| Apparent conflict or missing contract | Decision applied |
| --- | --- |
| Product speaks of investigations; native types expose Task | Investigation is a derived business aggregate selected by taskType |
| API version stays 2026-01-01 while docs/features change | Pin model commit/hash and review date separately |
| Botocore eventstream flag versus Smithy/API union | SendMessageEvents is documented as a streaming union; one event variant |
| “Optimistic locking” description versus no task expected-version parameter | Keep returned version for observation; do not promise native compare-and-swap |
| Execution STOPPED versus Task COMPLETED | Preserve both domains; no success inference from STOPPED |
| Native CANCELED versus EventBridge CANCELLED | Preserve raw value/channel; normalize display explicitly |
| Completion may lack a summary; several summary records may exist | Use exact event pointer when available; otherwise label candidate selection |
| Product completion can be continued | Historical finalization belongs to immutable application snapshots |
| Native Asset metadata is open JSON, but guide defines profiles | Distinguish generic wire contract from documented type-specific profiles |
| Built-in serviceId aws versus registered provider services | Association registration resolution is optional; no universal serviceId FK/uniqueness |
| Trigger action is a document with a custom-agent reference | Keep Trigger separate from Asset metadata and preserve nested path |
| Approval response mentions later read states but no approval Get/List exists | Record recovery/readback as an unresolved public-contract gap |
| API HTML route for approval may redirect | Use current official SDK model and directed-actions/Boto3 docs |
| IAM/app capability names absent from 63-operation public model | Do not manufacture SDK calls or reverse-engineer private console endpoints |
| All-chats UI filter newer than modeled ListChats parameters | Record a capability gap; do not silently invent an All parameter |

Where a guide describes broader product behavior, the notes preserve that fact without fabricating the missing wire recipe. A negative inventory finding means “not present in the reviewed public model,” not “AWS cannot implement this internally.”

<!-- block: obsidian-devops-investigation-api-sources-validation -->
## 5. Initial source-branch verification record

The following records the initial model review on [source commit `1d10b2d`](https://github.com/lyrel-dev/frontier-agents/commit/1d10b2de6616ff3d94e97a579c6291cc3696c03a). Its rendering and publishing checks refer to that source-branch edition. The independent package refresh is documented in [REVIEW.md](../REVIEW.md), and application runtime checks are recorded separately in [README.md](../README.md).

| Check | Method and scope | Result |
| --- | --- | --- |
| Source pin integrity | Current-path bytes compared with pinned official commits; hashes recorded above | Passed |
| Complete operation inventory | Generated names/methods/routes/output-field lists compared to official model | 63 of 63 matched |
| Request dictionary | Names, order and requiredness compared to official model | 19 request tables matched |
| Selected type dictionary | Names, order and requiredness compared to official model | 52 type tables matched |
| Semantic review | Independent reviews of native joins, cardinalities, lifecycle, streams, approval and snapshot claims | Corrections incorporated |
| Mermaid syntax/rendering | Nine fenced diagrams parsed and rendered with Pele 1.6.0 | 9 of 9 rendered |
| Diagram readability | Full-resolution PNG review of cardinalities, labels, clipping and layout | Passed: all nine reviewed individually at full resolution |
| Repository integration | YAML/source loading, internal links, uniqueness and existing publishing workflow | Local checks passed; build/browser CI is linked to the repository commit |

The nine rendered diagrams use top-down layouts where appropriate, short labels, no HTML labels or click directives, and no more than five entities/participants across a horizontal rank. ER boxes intentionally show selected attributes, with complete scope/key rules in prose. The diagrams are logical design views, not a claim about AWS internal database schema.

Rendering verifies the authored diagrams under the tested renderer. It does not validate every Obsidian/Mermaid version or demonstrate real AWS lifecycle behavior. The future account-level capture plan is clearly separated in [production UI contract](Investigation_UI_Contract.md).

### Changes made during review

The review corrected or tightened:

- Optional resolution of external association references and complete scoped record joins.
- Multiple provenance locators into one source revision.
- Immutable projection-revision identities and snapshot membership.
- Graph endpoint scoping and unresolved-node behavior.
- Attachment ID versus actually consumed asset version.
- Trigger action-document semantics.
- Approval credential mint versus credential use/action success.
- Streaming union and optional block/response identifiers.
- Execution pagination in the sequence diagram.
- Explicit partial-snapshot capture and retained-history behavior.
- Summary/completion timestamp offset versus measured publication/retrieval latency.
- Backlog filter/sort restrictions, timestamp units and copyable regex constraints.

<!-- block: obsidian-devops-investigation-api-sources-maintenance -->
## 6. Maintenance procedure

When refreshing this addendum, fetch and pin the new official models, compare operation/member/enum changes, and separately review the EventBridge/A2A/user-guide contracts. Preserve the existing snapshot's evidence date and hashes.

Treat an added record type as an opportunity for a new parser profile, not a reason to discard old raw data. Run representative capture tests before claiming a supported semantic schema. Rerender affected diagrams and review both their API meaning and their visual output.

Any future implementation should publish its actual runtime validation results separately from this documentation-level review.

## 7. Independent package refresh

The package review on 5 November 2026 fetched the pinned Botocore, Go and JavaScript models again and verified the byte counts and SHA-256 values above. The Botocore current `develop` path was byte-identical to the pinned file at this review. The independent comparison found 63 matching operation routes/response-field lists, 19 matching request tables, and 52 matching selected type tables. No customer AWS account was queried.

The refresh preserves the six logical-model ERDs and the three UI-contract diagrams as editable Mermaid under `../diagrams/`. All nine appear together in the [reviewed report](../report.md). Its substantive clarification distinguishes an uncaptured completion notification, a captured completion that omits a summary pointer, and a pointer whose record is not yet retrieved. Prototype fixture schemas are explicitly application-owned.
