---
title: "AWS DevOps Agent investigation model: initial review record"
id: aws-devops-analysis-review
kind: obsidian-note
product: devops
type: review-record
created: '2026-11-05'
updated: '2026-11-05'
reviewed: '2026-11-05'
source_cutoff: '2026-11-05'
api_version: '2026-01-01'
initial_model_commit: 1d10b2de6616ff3d94e97a579c6291cc3696c03a
status: historical-review-with-follow-up
tags:
  - aws/devops-agent
  - investigation
  - review
  - data-model
related:
  - "report.md"
  - "README.md"
  - "VALIDATION.md"
  - "annexes/Investigation_API_Sources.md"
---

# Initial model and documentation review

## Follow-up assessment

This record preserves the first source/schema and prototype review, completed for package commit `302128e5628acb4d832c20db79da2ab878c95e48`. **Its architecture assessment remains useful, but its nominal-fixture checks did not establish all claimed implementation invariants.** The subsequent [adversarial quality review](QUALITY_REVIEW.md) found and corrected cross-scope selection, duplicate counting, result-phase mixing, stale source inspection, damaged-state handling and a live dependency in historical rendering, along with documentation and verification gaps.

The current package has ten diagrams, including D07's collection-observation model; the initial nine-diagram statements below describe the earlier edition. The current [validation record](VALIDATION.md) reports 33 model and 9 UI regression tests, repeatable native-schema audits, independent Mermaid syntax checks and focused browser review. Use that record and [QUALITY_REVIEW.md](QUALITY_REVIEW.md) for the current disposition. Earlier review results are retained here so the additional corrections are visible rather than being presented as checks that had already passed.

## Initial outcome and scope

**The initial review considered the model suitable as a starting design for the operator prototype.** It retained the central architecture: a scoped native `Task` of type `INVESTIGATION`, discovered executions, published journal records, explicit result references, and separately versioned application projections. The limits of that conclusion remain: a schema review does not establish live account permissions, journal-content profiles, service timing or full AWS Operator Web App parity.

The review recovered the four source notes from [commit `1d10b2d`](https://github.com/lyrel-dev/frontier-agents/commit/1d10b2de6616ff3d94e97a579c6291cc3696c03a), independently compared official models and current AWS references, and consolidated the result in [report.md](report.md). That edition included nine diagrams. The source-level notes remain available and have since been updated as the [data model](annexes/Investigation_Data_Model.md), [API catalog](annexes/Investigation_API_Catalog.md), [UI contract](annexes/Investigation_UI_Contract.md), and [source register](annexes/Investigation_API_Sources.md).

The review date is **5 November 2026**. No AWS customer account, production investigation, live AWS API response or service mutation was used. All prototype incident data are fictional. Application checks are recorded in [VALIDATION.md](VALIDATION.md) and [README.md](README.md); they are not inferred from the earlier source-branch CI.

## Independent schema checks

| Check | Evidence and result |
| --- | --- |
| Current versus pinned Botocore | Fresh downloads were byte-identical: 357,369 bytes, SHA-256 `c9650e8c0aa3546f3f45ecb829f96223156bfc07f720b580bed23a7407aaad59`. |
| Pinned Go and JavaScript models | Both downloads matched their recorded pins and each other: 655,409 bytes, SHA-256 `df172e1f6c0692bb1e4d766a1961fd63aa53a5750a82cafcef5df2a96933c8c5`. |
| Operation count | The official Actions page and Botocore model each list **63** operations, including `ValidateAwsAssociations`. |
| Operation dictionary | All 63 HTTP methods/routes and top-level response-field lists matched the pinned model. |
| Detailed request dictionary | All 19 request tables matched member names, order, requiredness and wire location; referenced type representations were checked. |
| Selected entity/value dictionary | All 52 tables matched member names/order and requiredness; document and referenced type representations were checked. |
| Type boundary | No native `Investigation`, `Graph`, `GraphNode`, `GraphEdge`, `Finding`, `Hypothesis`, `RootCause` or `ReviewResult` shape was found in the reviewed model. |
| Native state inventory | Task has **11** status values; Execution has **6**, including `STOPPED` and excluding `COMPLETED`. The enums are not a transition matrix. |

The exact official source URLs and revision pins are in the [source register](annexes/Investigation_API_Sources.md). Botocore's 560 shapes include primitive aliases, containers, errors and wrappers; 560 is not a business-entity count. The current-path comparison was performed for Botocore. The Go/JavaScript comparison verifies the stated immutable pins, rather than asserting that every language SDK currently ships the same revision.

## Findings and changes incorporated

| ID | Finding | Resolution in the report and prototype contract |
| --- | --- | --- |
| R01 | Investigation is product terminology over the native Task resource. | Preserve `taskType = INVESTIGATION`, scoped task identity and an application aggregate; no invented `GetInvestigation` endpoint. |
| R02 | A list response can omit relationship context. | Retain the `ListExecutions(taskId)` request association because an Execution body has no task ID. Treat `Task.executionId` as an associated pointer, without assuming it is the entire execution set. |
| R03 | Completion has three different summary-selection conditions. | Explicitly separate an uncaptured completion notification, a captured completion with no summary pointer, and an exact pointer whose record is not yet retrieved. A received completion without `summary_record_id` does not promise eventual summary arrival. |
| R04 | Native journals carry arbitrary JSON, with an open record type. | Preserve objects, arrays, scalars, booleans and null. Rich findings and evidence require a documented or validated profile; an unknown type stays inspectable. |
| R05 | Compact ERDs can be mistaken for full physical schemas. | Retain the complete key/scope rules in prose and identify diagrams as logical views with selected attributes. Include owning partition/account/Region/Agent Space where applicable. |
| R06 | Source clocks and observation clocks have different meanings. | Keep incident time, journal creation, resource update, event subject time and application observation time distinct. Label normalized fixture timestamps separately from wire serialization. |
| R07 | An attachment request is not proof of consumption. | Tighten the wording: `SendMessage.assetIds` establishes the request's attachment-ID relation. Acceptance, actual use and the version actually consumed require their own observations. |
| R08 | A graph's structure does not establish the meaning or truth of its edges. | Keep graph kinds separate, scope endpoints to one graph snapshot, retain exact source locators and distinguish published, operator-confirmed and application-inferred assertions. |
| R09 | Derived objects need immutable history as well as logical continuity. | Preserve stable item IDs and separate immutable projection-revision IDs. Snapshot manifests reference the retained revisions, payload hashes and parser versions. |
| R10 | A completed investigation can resume in place. | Keep current views and retained historical captures separate. The demo replay is an illustrative sequence, not a claim about every allowed native state transition. |
| R11 | Native chat, EventBridge and A2A are different contracts. | Keep channel-specific identities and status semantics. Chat response completion does not complete a task; A2A terminality can precede artifact readiness. |
| R12 | Directed-action requests are chat-only. | Preserve the documented decision-then-resume protocol and distinguish permission, submission, observed action and recovery. Autonomous mutating-call failure does not manufacture an approval request. |
| R13 | Public mutation and recovery gaps remain. | Preserve absent expected-version/readback/idempotency contracts as implementation gaps. Do not infer a generic task-state setter or approval Get/List API. |
| R14 | The prototype may look like a native AWS product. | Explicitly label all incident data, graph profiles, telemetry and replay as fictional application behavior. Diagram/API coverage does not claim that every described production capability is implemented. |

These changes tighten interpretation and presentation. The reviewed native operation/member inventory required no schema correction.

## Prototype fixture and read-model review

A separate read-only review examined the fictional source envelopes, their temporal consistency, graph/source joins, result selection and the pure application model. The implementation owner incorporated the following corrections before final application validation.

| ID | Issue found | Incorporated correction |
| --- | --- | --- |
| F01 | A ledger journal published at 12:25 UTC contained metric points through 12:30 UTC. | Publication now occurs at 12:31 UTC, with observation at 12:31:06; all included points precede publication. |
| F02 | The operator-message journal preceded the creation of its owning follow-up execution. | Journal publication is 14:25:47 UTC, after the 14:25:46 execution creation. Explicit payload `occurredAt` retains the original 14:25:45 message time. |
| F03 | The attachment used the generic Asset JSON shape but omitted required documented attachment metadata. | `filename`, `extension` and UTF-8 byte `size` are present; generic native shape validation and documented profile validation remain separate. |
| F04 | The ledger chart's unit and aggregation were implicit in the projection. | Its demo telemetry now records metric, statistic, unit and window explicitly, and the chart cites the alarm for its threshold. |
| F05 | Artifact hashes covered a JSON-encoded string rather than the downloadable file bytes. | File hashes now cover raw UTF-8 Markdown/CSV bytes. Native source-object hashes continue to cover the declared canonical JSON representation. |
| F06 | Projection hashing occurred before the derivation identifier was added. | The retained derivation identifier is included before computing the payload hash; the hash can be reproduced from the returned projection with its self-hash field removed. |
| F07 | Missing external diagnostics made an exhausted journal query look like uncollected journal history. | Coverage separates query pagination from external evidence gaps, and the rollup is labeled in evidence scopes. |
| F08 | Timeline `recordedAt` always preferred source creation time, including a timed-out Task update. | Source-kind-aware selection uses Task/Execution update time, journal creation time, EventBridge subject time, or application observation time as appropriate. |

The bounded review checked **46 synthetic native-shaped objects** against the relevant pinned SDK shapes and **three EventBridge completion notifications** against the documented envelope. Required fields, enum/type representations, scope relationships and source/graph references were consistent. `GetAssetFile` correctly uses returned `file.content`; the similarly named upload value uses `body`, so no change to the returned fixture was needed.

An independent Node `crypto` comparison reproduced source payload, retained projection and downloadable-artifact SHA-256 hashes across all **18 task/stage combinations**. The final read-model validation reported no errors. The supplier timeout now records the source update at 13:50 UTC rather than Task creation at 13:30 UTC. The attachment's declared size matches its UTF-8 file content.

Version 4 attachment metadata remains an unused workspace-context fixture; the implemented model explicitly retrieves and preserves version 3. The package does not claim a visible version 3/version 4 comparison. The production model's richer channel adapters, action handling and payload captures remain distinct from the prototype's implemented demonstration.

These checks concern local fictional data and pure application calculations. Browser presentation, interaction, storage and export-flow checks are recorded in [VALIDATION.md](VALIDATION.md).

## Diagram review

All nine original diagrams are retained in the consolidated report and as editable `.mmd` files. The package's pinned **Pele 1.6.0** renderer produced all nine SVGs. Each was visually inspected at full resolution for labels, cardinalities, arrows, clipping and boundaries. The layouts use no more than two ER entities across a rank; the sequence diagram has four participants. All nine passed that rendering/readability review.

| Diagram | Semantic review focus | Result |
| --- | --- | --- |
| [D01](diagrams/D01-workspace-associations.svg) | Optional association resolution, built-in AWS services and embedded external reference | Retained; no mandatory universal registration FK |
| [D02](diagrams/D02-investigation-core.svg) | Scoped journal identity, observed task membership, optional execution parent | Retained with full scope rules in prose |
| [D03](diagrams/D03-projection-provenance.svg) | Immutable source/projection revisions and multiple citation locators | Retained; exact provenance remains reproducible |
| [D04](diagrams/D04-graph-model.svg) | Same-graph edge endpoint joins and attributed relationship meaning | Retained; unresolved endpoints remain explicit |
| [D05](diagrams/D05-artifacts-assets.svg) | Optional asset resolution and explicit versioned content | Retained; artifact ID is not automatically a native asset ID |
| [D06](diagrams/D06-historical-snapshots.svg) | Snapshot membership by source/projection revision | Retained; later live updates do not mutate a capture |
| [U01](diagrams/U01-live-reconciliation.svg) | Execution/journal pagination and retain-before-project ordering | Retained as proposed backend sequence |
| [U02](diagrams/U02-approval-lifecycle.svg) | Separate decision, resume and observed outcome | Retained as application audit model |
| [U03](diagrams/U03-snapshot-workflow.svg) | Retry, explicit partial capture and retained historical state | Retained as application presentation workflow |

The [diagram manifest](diagrams/manifest.json) maps source and rendered files. [Renderer evidence](qa/diagram-render.json) records each figure's dimensions and source/SVG hashes. Rerendering instructions are maintained with the application package. The Mermaid fences remain the readable editable form in Obsidian; the SVGs provide a renderer-independent presentation view.

Diagram validation covers the tested renderer and authored relationships. It does not establish AWS's internal database schema or every Obsidian/Mermaid version.

## Primary contracts revisited

| Contract | Current official reference |
| --- | --- |
| Native operation inventory | [Actions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Operations.html) |
| Work item identity/state | [Task](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Task.html) |
| Execution fields and status | [Execution](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Execution.html) |
| Task-to-execution discovery | [ListExecutions](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListExecutions.html) |
| Journal envelope and pagination | [JournalRecord](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_JournalRecord.html), [ListJournalRecords](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html) |
| External task reference | [ReferenceOutput](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ReferenceOutput.html) |
| Exact summary selection and absence | [EventBridge integration](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html) |
| Continued completed investigation | [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) |
| Streaming event union | [SendMessageEvents](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageEvents.html) |
| A2A terminal state and artifacts | [A2A server integration](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html) |
| Asset metadata, content and versions | [Asset](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Asset.html), [GetAssetContent](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetContent.html), [GetAssetFile](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssetFile.html) |
| Asset metadata profiles | [Managing assets](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html) |
| Task update surface | [UpdateBacklogTask](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_UpdateBacklogTask.html) |
| Backlog discovery restrictions | [ListBacklogTasks](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListBacklogTasks.html) |
| Chat-only approvals and separate resumption | [Directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) |

## Remaining implementation questions

The model deliberately preserves these questions for authorized service captures or AWS clarification:

- Versioned schemas for rich journal and streamed-block content, including tool calls, evidence, topology, review and artifact references.
- Journal consistency, retention, late arrival, mutation and pagination-token guarantees.
- Supported joins among backlog tasks, native executions, chat targets, subagents and A2A task identities.
- Exact native recipes for product actions such as fork, link correction and resume, and the accepted task-status transitions.
- Supported approval readback and recovery after an ambiguous decision/resume response.
- Reliable evidence of asset/configuration versions actually consumed by a particular run.

The [production UI contract](annexes/Investigation_UI_Contract.md) contains 24 proposed capture/acceptance scenarios. Local prototype tests verify the behavior of its fictional scenario and application model; they do not close these AWS service-contract gaps.
