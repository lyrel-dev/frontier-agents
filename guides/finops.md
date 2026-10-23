# AWS FinOps Agent

Instance configuration, cost analysis, context, and automation

AWS FinOps Agent is documented as a preview service for cost inquiry, reporting, anomaly investigation, and interpretation of upstream recommendations. Its instance retains organizational context and contains task automations and destination connections. A conversation, a queued task, and an automation are different objects. [FS501] [FS502] [FS503]

This guide separates those configuration facilities from their mechanisms: contextual reuse, conversation compaction, scheduled task creation, anomaly-event matching, and publication authorization. It then describes the managed analytical functions and their outputs. The use-case catalog supplies the approved operational objectives rather than another list of platform features.

**Reading conventions.** The dimensions below organize documented FinOps facilities; they do not imply a DevOps-style custom-agent API, arbitrary MCP tool registry, or shared cross-service memory. Official sources support product behavior. DOC/AWS/EXT colors identify ownership. Financial examples use synthetic values; verification procedures are proposed, not live account results.

Start with the agent overview and workflow walkthroughs. Use the subsequent capability chapters for detailed setup, lifecycle behavior and troubleshooting. The use-case catalog remains separate and unchanged.

## 01. The agent and its operating context

Start with one execution, then add coordinated responsibilities and the surrounding access scope. The same diagram is reused in the workflow walkthroughs.

### F-90 — An analysis request, its context, and the agent execution

AWS FinOps Agent answers cost-management questions using authorized AWS source services and organization-specific context. A question specifies a scope and analysis basis. Source services provide cost, anomaly or recommendation evidence. Uploaded files and persistent memory supply mappings, preferences and other context. The agent interprets the available material and produces an answer or artifact. [FS701] [FS703]

![FinOps analysis composition](../assets/diagrams/teaching-finops-agent.svg)

This is not the DevOps custom-agent definition model. Uploaded instructions and templates are context files, not a native SKILL.md registry. A task instruction specifies work, not another agent instance. Recommendation estimates retain the provenance of the upstream source; analysis does not itself authorize an infrastructure change or financial commitment. [FS701]

Read the picture from the question, through the authorized data path, to the result. The contextual inputs explain how organizational terms affect the answer, but they do not replace the source query or its dates, filters and cost basis.

### F-91 — How conversations and automations coordinate tasks

Ordinary requests can be answered directly in a conversation. When the user explicitly asks for a task, the service creates queued work. A scheduled or supported event-based automation creates new tasks when its condition matches. These are execution arrangements within the configured instance, not a roster of cooperating DevOps-style agents. [FS702]

![Direct interaction and task creation](../assets/diagrams/teaching-finops-coordination.svg)

Inspect the automation condition, task identity, analysis result and destination effect separately. A matching anomaly event does not establish that the task completed, and completed analysis does not establish successful publication. Stopping future task creation, cancelling current work and removing retained data have different consequences. [FS702]

The publication path also changes the control question. Jira actions started interactively or from an on-demand task request approval; scheduled or event-driven actions rely on authorization established during automation setup. Slack posting has no per-message approval prompt. There is no single universal approval switch for every effect. [FS702]

### F-92 — Agent-instance scope and source access

The instance groups its configured access, context, conversations, tasks and connections. Data-source permissions, operator access and publication destinations are separate controls. The detailed F-01, F-02 and F-05 sections define their resource identities and setup procedures. [FS701] [FS702]

![FinOps instance and its connections](../assets/diagrams/teaching-finops-space.svg)

Uploaded context files, retained memory and a conversation summary are different representations. Files are maintained through their workspace; conversational corrections update memory; compaction summarizes older conversation content. Applying one control does not update or delete all other copies of a fact. These distinctions matter when a report uses an outdated ownership mapping or format preference. [FS703]

The diagram shows the source-access and output paths without treating the instance as the underlying billing system or a shared memory across AWS agentic services. A verified source result remains necessary even when the organizational context is correctly configured.

## 02. Essential operational workflows

Follow the existing use cases through inputs, context, authorized operations, outputs and the decisions that require an engineer. Teaching priority is an editorial choice, not an AWS ranking.

### F-93 — Cost-analysis, reporting and optimization workflows

For the technical audience, the sequence begins with a reproducible cost inquiry, then anomaly investigation and reporting, before planning and optimization decisions. This teaching order is editorial; the approved cases remain separate.

![Source-backed analysis path](../assets/diagrams/teaching-finops-analysis.svg)

[Historical cost and usage analysis](../catalog/UC-F01.html) establishes accounts, interval, currency, metric, grouping and filters. [Anomaly investigation](../catalog/UC-F05.html) adds a reason to inspect a deviation and, when available, corroborating operational evidence. Numerical contribution, temporal correlation and an established cause are different conclusions. [FS701] [FS702]

![Reporting and publication path](../assets/diagrams/teaching-finops-reporting.svg)

[Periodic reporting](../catalog/UC-F04.html) reuses the query basis and adds a reviewed format, optional recurrence and an explicit destination. A report artifact can originate from a conversation or task; its content and publication outcome should be inspected separately. F-04 and F-M06 explain those controls. [FS702]

[Forecast review](../catalog/UC-F02.html) concerns projected expenditure; [commitment-coverage review](../catalog/UC-F03.html) concerns covered eligible usage. Do not merge their horizons or denominators. [Optimization prioritization](../catalog/UC-F06.html) reviews source recommendations and constraints. [Outcome measurement](../catalog/UC-F07.html) examines a comparable period after an implemented change. An estimate is not the measured result. [FS701]

![Recommendation and team-decision path](../assets/diagrams/teaching-finops-optimization.svg)

The shared [operational-review case](../catalog/UC-G01.html) assembles reconciled reports, unresolved anomalies, original recommendation assumptions and measured outcomes into decisions owned by the team. It does not introduce native cross-service orchestration. The detailed capability chapters provide the access, context, task, output and retention procedures underlying this sequence.

## 03. Workspace and resource organization

The agent instance, connections, conversations, automations, tasks, and artifacts have different identities.

### F-01 — Agent instance, access roles and retained state

AWS FinOps Agent presents an independent agent instance in its console and web application. The IAM documentation uses service-specific AgentSpace action names, including `finops-agent:CreateAgentSpace`, and an `agentspace` resource path in the ARN. This is a naming correspondence within FinOps Agent, not proof that the instance is the same resource type as a DevOps Agent Space. The service namespace and its documented operations remain part of the identity. [FS50] [FS51]

The instance groups its permissions, retained context, task queue and connections. Two roles have separate responsibilities: the agent data role accesses source services, and the operator role supports web-application operations. End users also need their own entry permissions. A user successfully opening the application does not establish that the data role can perform a particular source query. [FS50] [FS51]

![Instance access and integration connections](../assets/diagrams/er-finops-scope.svg)

Collaboration configuration has two levels. An integration registers Jira or Slack authorization at account level. An agent connection selects the destination for a particular instance. The destination remains an external Jira project or Slack channel, and a published issue or message is not stored solely inside the FinOps task record. Source access, destination membership and publication behavior therefore need separate review. [FS55] [FS56]

Work starts either as a conversation or as a task. A direct conversation can answer a question without creating a task. An automation is a rule for creating future tasks on a schedule or supported event; it is not a task that is already running. Reports can be produced through conversations or task work, so the model does not require every artifact to have a universal task-parent field. [FS52] [FS58]

Retained files and memory supply context to the execution runtime. They survive differently from session state, and conversation compaction has a different purpose again. The context chapter follows these distinct representations rather than treating them as one mutable knowledge store. [FS53] [FS54]

Green boxes identify AWS-defined concepts and cross-service dependencies such as IAM roles. Blue identifies our normalized groupings, including the evidence family used to discuss cost queries, anomalies and recommendations together. Those upstream results have different source identities; they are not one native FinOps Evidence resource. The [resource index](../catalog/resource-models.html#model-finops) makes this distinction explicit before the guide applies the model to reporting and anomaly investigation.

### F-09 — Conversations, automations, tasks and artifacts

A conversation represents interaction with the agent. A task represents separately recorded execution. An automation represents instructions for future task creation. These objects may be connected, but their lifecycles are not interchangeable. A request can be answered directly; an explicit task can enter the queue; and a recurring automation can create another task at each applicable start. [FS52]

![Conversation, automation and task records](../assets/diagrams/er-finops-work.svg)

The event-driven path adds a cross-service dependency. The documented preview uses Cost Anomaly Detection events and service-managed EventBridge rules. The automation matches the supported event and creates work. The public guide does not establish that every automation owns exactly one rule, so that multiplicity is left unspecified in the ER diagram. IAM conditions restrict management to the permitted managed rules rather than general administration of the event bus. [FS51] [FS52]

Results have identities outside this orchestration path. A source query is defined by dates, metric, scope and dimensions; a forecast, anomaly and recommendation are different upstream results. A report artifact contains an interpretation of those results. A Jira issue or Slack post is an external publication. The team should retain these references when it needs to reconstruct a decision, without assuming a universal service-side lineage graph that the public guide does not document. [FS57] [FS58]

| Object | Relevant change or stop operation | What the operation does not imply |
|---|---|---|
| Conversation | Continue or cancel applicable current work | Every answer becomes a task or artifact |
| Task | Inspect execution; cancel where supported | Its retained history or external publication is deleted |
| Automation | Update, disable or delete future work | Already-created tasks are cancelled |
| Agent connection | Change or remove the destination binding | Previously published messages are withdrawn |
| Context file | Soft delete or restore the uploaded input | A matching remembered fact is also changed |
| Report artifact | Inspect, revise, download or delete | Every downloaded or externally published copy disappears |

The object-specific data lifecycle is documented under F-M07. This table explains why an operator must identify the intended object before selecting an action. For example, replacing a weekly report requires checking for the previous automation as well as testing the new report; merely using a new task name can leave two schedules active. [FS52] [FS54]

Publication also depends on invocation mode. Jira actions requested interactively or through on-demand tasks require the documented approval, whereas scheduled or event-created actions use setup-time authorization. Slack does not present the same per-message approval prompt. A generic Result → Destination arrow is therefore incomplete unless the product, operation and invocation path are retained in the implementation profile. [FS57]

The model establishes relationships the reader can reason about; it does not provision them. The [feature/resource crosswalk](../catalog/resource-models.html#model-finops) links each approved feature reference to the actual instance, connection, task or context object and its supporting documentation.

## 04. Instance configuration and task definition

Instance settings control access and context; requests and automations define the work.

### F-11 — Instance configuration and task instructions

The instance is configured with data access, operator access, retained context, and supported integration connections. These settings determine which sources can be read and where results can be published. Instructions supplied for a task or automation specify the work; they are not a documented custom-agent system-prompt asset with a customer-selected MCP tool list. [FS502] [FS509]

| Customer control | Configuration surface | Applies to |
|---|---|---|
| Data role | Instance setup and IAM policy | Authorized AWS source calls |
| Operator access | Operator role and user permissions | Use of the instance's web application |
| Uploaded instructions or mappings | Context files workspace | Reusable organizational context |
| Request or task instructions | Conversation or task creation | The selected analysis or report |
| Recurring/event instructions | Automation configuration | Work created by future matching occurrences |
| Publication destination | Agent connection | Selected Jira project or Slack channel |

Create the instance through the wizard, configure the two role paths, and test entry as the intended operator. Then exercise a small source query under the actual data role. The context and task chapters describe the remaining controls. This configuration model should be read on its own terms rather than populated with facilities available in another AWS service. [FS502] [FS509]

## 05. Organizational knowledge and conversation context

Uploaded files, retained preferences, and compaction are three different context mechanisms.

### F-M02 — Context-file preparation and management

Reference files let the agent interpret account identifiers and costs in the organization’s terms. Their value depends on curation: a small current ownership mapping is more useful than a collection of contradictory copies. The operator maintains these files and decides which versions are active.

The Context files workspace accepts text, CSV, JSON, Markdown, HTML and YAML. The documented file limit is 10 MB; total context storage is 100 MB per agent by default. The agent can read these files but cannot modify or delete them through conversation. Users who can access the agent can see its context files. [FS04] [FS10]

**Procedure:** prepare a minimal, non-sensitive authoritative mapping, upload it through Context files, inspect its active state, and ask a question whose answer depends on one known entry. Delete/restore through the workspace when changing availability. Deletion is reversible soft deletion, not proof of physical erasure. [FS04]

**Original example:**

```yaml
schema: team-routing-v1
updated: 2026-10-22
accounts:
  staging-account-alias:
    owner: platform-team
    cost_basis: UnblendedCost
    publication: internal-test-channel-only
```

Use the identifiers actually available in your authorized queries; this alias is illustrative. Keep the source file under review in Git and upload a reviewed revision. A stale ownership mapping can produce the wrong destination even when the cost arithmetic is correct. A file statement about publication is prompt context, not a replacement for destination access controls.

### F-M03 — Persistent preferences and corrections

Persistent memory allows a later session to use preferences and corrections supplied earlier. For example, a team may specify the owner of a set of accounts, a preferred reporting breakdown, or a recommendation category that needs special treatment. The service can retain that context and apply it to later questions or tasks. This is a different path from uploading an account-mapping file, and it is different again from summarizing old messages within one long conversation. [FS04]

The persistence boundary is the agent instance. The data-protection guide describes context and memory files in encrypted AWS-managed storage, loaded at session start into an isolated ephemeral runtime. Conversation and task records are retained alongside their own execution records. The guide does not establish a shared memory across instances or an automatic precedence rule that resolves conflicting statements in a file and a remembered preference. [FS08]

Operators manage conversational memory by asking the agent to remember, update, or forget a specific fact. Uploads remain operator-maintained files: a request to forget a preference is not an edit to a CSV containing the same information. When ownership changes, identify which representation is authoritative, update the file where appropriate, and correct the retained preference separately. Earlier reports remain historical artifacts rather than being silently rewritten. [FS04] [FS08]

A useful acceptance exercise uses a harmless preference, such as placing the comparison table before commentary. Set it, start a new conversation, and check whether it is applied. Correct or forget it and repeat. Test file retrieval with a different known fact. These observations distinguish successful application of retained context from an assumption about hidden model state. The procedure is a proposed test, not a result observed in an AWS account.

Recovery is object-specific. A soft-deleted context file can be restored through its workspace; memory can be corrected conversationally; earlier conversations and task records have the documented preview retention restrictions. None of these controls proves a general backup-and-restore capability for an entire instance. F-M07 describes the supported lifecycle actions. [FS08]

### F-M04 — Conversation summarization and context limits

A long conversation has a different lifecycle from persistent memory. As earlier messages are summarized, the session preserves a condensed working context rather than every word of the exchange. Important comparison assumptions should therefore remain explicit in the current task and its authoritative reference material.

As a conversation approaches its context limit, older messages are summarized while recent messages remain in full. This is within-conversation context management, distinct from persistent memory and uploaded files. The documentation does not promise verbatim retention or expose a general customer setting for the summarization algorithm. [FS04]

**Engineering procedure:** put critical constraints in a concise current task specification and reference the authoritative file or source record. When resuming a long conversation, ask the agent to restate the comparison basis and unresolved questions, then correct any discrepancy before requesting another calculation. This tests retained context; it does not prove that every earlier message remains available.

## 06. Task invocation and automation

Explicit requests, schedules, and supported anomaly events create work through different start conditions.

### F-03 — Tasks, schedules, and execution history

Tasks provide execution records for requested work. Automations are definitions that create tasks later, either on a schedule or from a supported event. Their separate lifecycles explain why stopping future task creation does not remove a result that already exists.

A task is an execution record. An automation is a rule for creating future tasks. On-demand, scheduled and event-triggered work shares the queue. Asking a conversational question is not necessarily a request to create a durable task; task creation should be explicit. [FS05]

**On-demand procedure:** use the Tasks workspace or explicitly request a task, give its input scope and desired output, and inspect the resulting task. Check pending/running/completed or failure information and resulting artifacts. Do not treat a conversational acknowledgement as evidence that execution has finished. [FS05]

**Scheduled procedure:** define the required schedule and reporting window separately. Inspect the saved automation's trigger and next applicable execution information. For a daily report, a schedule time does not define whether the report covers the previous calendar day, rolling 24 hours or incomplete current day; specify the window. Removing the automation prevents future tasks but does not remove previously created tasks or published messages. [FS05] [FS08]

### F-M05 — Anomaly events and task creation

An anomaly event is the beginning of an investigation path, not its conclusion. The monitor produces the event, a managed rule and matching automation create work, and the task queue records execution. Publication follows only after a result exists and the destination path succeeds.

The documented event path is Cost Anomaly Detection → managed EventBridge rule → matching automation → task queue → analysis/result. During the reviewed preview, the event type is `COST_ANOMALY`; this does not establish an arbitrary customer-event orchestration platform. [FS05] [FS07]

**Enablement procedure:**

1. Configure a relevant Cost Anomaly Detection monitor and ensure the agent role can manage the service's EventBridge rules.
2. Connect any intended reporting destination using F-05. Set the destination before enabling automatic publication.
3. Request an automation naming the monitor/conditions and the intended investigation and output. Treat threshold values in example prompts as proposed configuration, not service defaults.
4. Open Automations and inspect the stored trigger type, status and last-triggered information. Inspect the created task separately after a matching event.
5. For a test, trace event identity, automation, task, result and external message. Then disable or remove the automation and verify that new matching work stops; existing tasks need separate handling.

AWS's IAM examples constrain rule management using service ownership and account conditions. Do not replace those conditions with broad EventBridge administration merely because task creation failed. [FS03] [FS07]

**Failure branch:** a registered automation with no task can mean there was no matching event, the monitor/condition is wrong, or rule permissions failed. A completed task with no message is a different destination/publication problem. Preserve these distinctions during diagnosis.

## 07. Data-source and collaboration integrations

AWS evidence sources and Jira/Slack destinations are configured for different operations.

### F-08 — Supported data sources and publication destinations

The data connections answer different financial and operational questions. Cost Explorer supplies cost and usage results. Anomaly Detection supplies a detected deviation. Optimization services supply candidate changes and savings estimates. CloudTrail supplies recorded API activity that may help explain a change. The agent combines these inputs; a permission to query one does not imply access to the others. [FS01] [FS03]

| System | Role in the workflow | Configuration dependency | Interpretation |
|---|---|---|---|
| AWS Cost Explorer | Cost and usage queries, forecasts, coverage and commitment analysis | Available cost data and the required role actions | Preserve the metric, dates, account scope, and grouping |
| AWS Cost Anomaly Detection | Anomaly monitor and event source | Relevant monitors and configured event automation | A deviation is a reason to investigate, not its explanation |
| AWS Cost Optimization Hub | Consolidated optimization recommendations | Service setup and authorized recommendation reads | Savings estimates belong to the source recommendation |
| AWS Compute Optimizer | Resource and rightsizing recommendations | Eligible resources and permitted reads | Review utilization assumptions and workload constraints |
| AWS CloudTrail | API-activity evidence | Permitted LookupEvents and relevant available records | A nearby change is evidence to evaluate, not proof of causality |
| Amazon EventBridge | Managed anomaly-to-task routing | Required managed-rule actions in the agent role | Creates work through the supported event path |
| Jira Cloud | Read connected issues; create issues and add comments | Account registration and agent-level project connection | No general issue-field, transition, deletion, or workflow-management capability |
| Slack | Post results to connected channels | Workspace registration, channel connection, and app membership | One-way publication in the documented preview |

This is the supported service-and-destination model described in the reviewed guides, not a claim of arbitrary external-tool connectivity. In particular, the existence of MCP integration in DevOps Agent should not be copied into this platform’s architecture. Exact AWS action requirements remain in the IAM setup guide. [FS03] [FS12] [FS13]

![Cost-data retrieval and collaboration connections](../assets/diagrams/finops-integrations.svg)

Jira and Slack each use an account-level registration plus a connection owned by the individual agent. The registration stores provider authorization; the connection selects a project or channel. That distinction makes it possible for two agents to use the same registered provider while having different destinations. It does not give either agent access to the other’s files, memory, or tasks. [FS12] [FS13] [FS08]

Test the paths separately. First reproduce a small cost query with known dates and dimensions. Then inspect a recommendation from its upstream source. Finally publish a non-sensitive test result to the intended destination and inspect where it arrived. A failed Slack post is not repaired by widening cost-data access. A missing CloudTrail event does not invalidate arithmetic that was reproduced independently, but it does limit the causal explanation.

### F-05 — Jira projects and Slack channel connections

Publication starts with a registered provider and an agent-specific destination. The registration establishes authorization to a Jira site or Slack workspace. The connection selects the project or channel used by one agent, so its state and audience must be checked separately from registration.

| Layer | Jira | Slack |
|---|---|---|
| Account registration | Supported Jira Cloud authorization flow | Workspace authorization |
| Agent connection | Selected Jira space/project key | Channel ID; application already added to that channel |
| Supported effects | Create issues; supported reads/comments | One-way posting and supported artifact sharing |
| Do not assume | On-premises support or arbitrary issue/workflow editing | Reading channel conversations, responding to mentions, editing/deleting posts |

Register the integration, complete authorization, then add the agent-specific connection and confirm its status. Inspect Pending/Active/Error/Inactive states rather than relying on the connection's name. An invalid Jira destination in unattended execution can fail instead of producing a clarifying conversation. A Slack membership error requires adding the app to the intended channel, not granting unrelated AWS permissions. [FS12] [FS13]

**Engineering procedure:** use designated test destinations, post a non-sensitive test result and record its actual location. Confirm that only the intended users can see it. API retries described in the integration guide address transient failures; they do not turn a permission or invalid-destination error into a successful publication.

## 08. Service access and data location

Service interfaces, persistent storage location, and inference geography are distinct properties.

### F-12 — Service access, storage location, and inference

FinOps Agent accesses the AWS sources and supported collaboration services described in F-08. The source-service permissions and destination connection establish the available interfaces. The reviewed guide does not expose the DevOps private-tool resource-gateway configuration, so this chapter does not invent a VPC connection object for FinOps Agent. [FS501] [FS509]

During the documented preview, persistent agent data is stored in `us-east-1`. Bedrock inference can take place in other US Regions. Storage location and inference location are separate properties and must both be considered when evaluating organizational data-location requirements. [FS505] [FS508]

Review the permitted input content before uploading it. Anyone with access to the agent can see its context files. An account-to-owner mapping is reference data, not an integration credential; credential values belong in the provider's supported authorization configuration. [FS504]

## 09. Execution runtime and publication control

Task queueing and session execution precede destination-specific publication controls.

### F-13 — Queued execution and session runtime

A direct question can be answered in the conversation. An explicit task request creates separately recorded work in the shared queue. Scheduled and event automations also create tasks. Queueing is the execution mechanism; the saved automation defines when and with which instructions that work is created. [FS503]

Persistent files and memory are separate from the ephemeral session runtime into which context is loaded. Instances do not share files, memory, or task queues. Session termination is therefore not the deletion operation for the persistent context. F-M07 describes object-specific removal and retention. [FS505]

Inspect task history for the requested source calls, results, and supported publication actions. Distinguish work that was not created, work waiting in the queue, analysis failure, and publication failure. These are diagnostic observations rather than an invented API status enumeration. [FS503]

Cancel current work through the supported control, and disable or remove the automation separately to prevent future work. Cancellation does not withdraw an external message that has already been published. [FS503] [FS505]

### F-M06 — Publication permissions and approvals

Publication authorization depends on both the destination and the way work was initiated. An unattended automation can carry authorization established during setup, while an interactive Jira action requests approval. Slack posting follows a different documented behavior, so a single blanket approval statement would be misleading.

| Effect | Chat / on-demand task | Scheduled / event task |
|---|---|---|
| Jira issue or comment | Approval requested | Pre-authorized through automation setup |
| Slack post | No approval prompt | No approval prompt |

These are documented differences, not one universal human-approval rule. Automation setup is therefore an authorization decision as well as a scheduling decision. Connected destinations and supplied context must be appropriate for unattended publication. [FS06] [FS05]

**Proposed verification:** in test destinations, record the requested action, invocation type, observed prompt or lack of prompt, and the resulting artifact. A successful Slack post does not demonstrate Jira approval behavior. Removing a future schedule does not retract a previously published message.

## 10. Managed analytical functions

Historical analysis, forecasting, coverage, anomaly inquiry, and recommendation analysis use different source results.

### F-14 — Cost inquiry, anomaly investigation, and recommendation analysis

The managed analytical functions consume different source-service results. Cost Explorer answers historical cost/usage, forecast, and commitment-coverage questions. Cost Anomaly Detection identifies a deviation for investigation. Cost Optimization Hub and Compute Optimizer supply optimization recommendations. CloudTrail records API activity that can help evaluate a possible explanation. [FS501]

| Analytical function | Result to interpret |
|---|---|
| Historical cost and usage | Amounts under specified dates, metric, filters, and dimensions |
| Forecast review | A source forecast with a stated horizon and assumptions |
| Commitment coverage | Coverage under the selected commitment type and eligible usage scope |
| Anomaly investigation | Reconciled cost drivers and evidence for candidate causes |
| Recommendation analysis | Upstream candidates and savings estimates interpreted against workload context |

These are supported analytical functions. A weekly cost report or a team optimization review is a use case that combines them with retained context, automation, or publication. Retrieving a savings estimate is not applying a resource change or measuring realized savings. [FS501] [FS06]

The causal inquiry starts after reconciling the numerical comparison. A matching CloudTrail event can support a hypothesis, but the query basis and workload evidence must establish how much of the movement it explains. F-M01 gives the source-query procedure, and F-U01 supplies the synthetic decomposition example.

### F-M01 — Cost queries and recommendation provenance

Historical amounts, forecasts, anomalies, and recommendations are different source results. Define the query parameters before comparing them. [FS01] [FS03]

| Evidence | Establishes | Does not establish by itself |
|---|---|---|
| Matching cost query | Spend for the specified dates, metric, scope and dimensions | Why a workload consumed that usage |
| Anomaly record | A detected deviation under the monitor's model | Root cause of the deviation |
| Recommendation source | An upstream optimization candidate and its assumptions | Realized saving or authorization to apply it |
| Operational event | A recorded change at a time | That the change caused the entire cost movement |

To verify the result, reproduce the numerical result first, then evaluate the explanation. Fix the time window, cost metric, granularity, filters, currency and relevant allocation assumptions. Require the response to identify unavailable sources instead of filling their absence with a causal story. These comparison rules are engineering guidance, not a new query mode. [FS06]

**Read-only query example:**

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-09-01,End=2026-09-15 \
  --granularity DAILY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

The end date is exclusive. This example deliberately has no account, Region or tag filters; add the same approved filters used in the agent question before comparing results. Cost Explorer availability, permissions and API charges still apply. The command was not executed here and must not be compared to a differently scoped agent total. [FS14]

## 11. Interaction surfaces and report artifacts

Conversations, task history, report generation, and external publication expose different outputs.

### F-15 — Conversation, task history, and artifact interfaces

The web application exposes conversation, Tasks, Automations, Context files, and Artifacts as different working areas. A conversation supports immediate questions. Tasks expose separately executed work. Automations define future starts. Artifacts retain generated reports. The administrative console configures the instance and access. [FS502] [FS503] [FS504] [FS507]

Report artifacts can originate in a conversation or a task. A follow-up request can revise a report; preserve the period, metric, and source scope when the requested revision concerns only format. F-04 describes report generation and supported output forms. [FS507]

Jira and Slack are external publication surfaces, not a shared conversation store. Their permitted operations and approval rules differ. A completed source analysis and successful external publication should be inspected separately through the available task record and the destination. [FS506]

### F-04 — Report generation and artifact management

A report is a presentation of an analysis, not another source of cost truth. Its usefulness depends on preserving the comparison basis and making the relevant calculations traceable. The artifact and the task that produced it should therefore remain linked when the report is revised or shared.

The service supports report artifacts including HTML, PDF and presentation formats documented by the service. A request can specify the audience, comparison basis, grouping and output format, and subsequent requests can revise the artifact. Source retrieval, calculations and artifact generation are different stages; formatted output is not independent proof that the totals are correct. [FS11]

**Procedure:** ask for one defined report, inspect the source breakdown and period, open/download the artifact, and verify at least one material total using the same source query. Request a revision that names the desired change rather than silently changing the comparison basis. When publishing, check that the file corresponds to the reviewed task and audience. [FS11] [FS06]

The artifact store has a separate default quota from context-file storage. Deleting an artifact does not necessarily delete external copies previously posted to a collaboration system. [FS10] [FS08]

## 12. Administration, retention, and limits

Role permissions, retained-data operations, and failure diagnosis must be applied to the correct object.

### F-02 — Administrator, service, and operator permissions

FinOps setup separates the person who administers the service, the identity used for data access, and the people who use the web application. A successful setup performed by an administrator does not prove that a regular operator can enter the agent or that the agent can read every required cost source.

AWS distinguishes administrator setup permissions, the agent's data policy, the operator role policy, and the web-app user's own access policy. They are not four names for the same permission set. [FS03]

| Responsibility | Attached to / used by | What to verify |
|---|---|---|
| Setup administration | Setup identity | May create/configure the service and permitted roles/integrations |
| Agent data access | Role assumed by the service | Actual source-service actions, account scope and required EventBridge permissions |
| Operator session | Operator role | Supported conversation, task, document and operator operations |
| Web-app entry | End-user identity | May access the configured agent through the supported route |

The setup path uses roles trusted by `finops-agent.amazonaws.com`. Automatically created roles include service-specific scoping. For existing roles, use the official trust and permission examples and adapt them to the intended account and instance. A role name cannot establish what actions its policy permits. [FS02] [FS03]

**Creation procedure:** complete the wizard's name, agent access, operator access, optional third-party integrations, and review steps. Open the agent from the console, inspect its connections, and test an authorized cost query. Then test the intended non-administrator user. Success for the setup identity does not prove team access. [FS02]

**Dependency review:** enable the cost/recommendation services required for the selected task and inspect whether the role permits the relevant APIs. For example, missing `cloudtrail:LookupEvents` removes an operational-change input without necessarily disabling Cost Explorer questions. Removing write access to customer infrastructure does not mean that Jira/Slack publishing is disabled; those effects follow separate integration rules. [FS03] [FS06]

### F-M07 — Retention, cancellation, and deletion

Stopping work, withdrawing active context, and removing retained data are different intentions. The service offers object-specific controls for those intentions. Choosing the correct operation requires knowing whether the object is an execution, a future trigger, a reference file, or a published artifact.

Persistent agent data and the ephemeral session runtime are separate. The preview uses AWS-managed encrypted storage. Agent instances do not share retained files or memory. [FS08]

| Object | Supported control and consequence |
|---|---|
| Context file | Soft delete; restore later through workspace |
| Memory | Ask to update or forget the specific information |
| Conversation | Individual deletion not supported in reviewed preview; retained until agent deletion |
| Task | Cancel execution where supported; record remains until agent deletion |
| Automation | Disable/delete future task creation; existing tasks remain separate |
| Artifact | Delete through its supported workspace; external copies are separate |
| Whole agent | Delete instance and associated retained service data; disconnect third-party integrations first |

Use the operation matching the intended outcome. In particular, cancel, forget, soft delete, disable and delete are not synonyms. Whole-agent deletion is unsuitable as an ordinary demonstration when meaningful data exists. [FS08] [FS02]

For data-location decisions, document both persistent storage (`us-east-1` in the reviewed preview) and cross-Region US inference. Do not describe the chosen console Region as the complete processing boundary. [FS09]

### F-06 — Data, task, and integration failures

Selected documented defaults are one agent per account/Region, 100 MB artifact storage, 10 MB per context upload and 100 MB total context storage. The per-file limit is fixed; relevant account/storage quotas may be adjustable. The reviewed integration limits include one account-level registration of each supported collaboration type and two connections of each type per agent. Check actual quotas before designing multiple destinations or isolated instances. [FS10]

| Symptom | Inspect | Result to establish |
|---|---|---|
| User cannot open agent | User policy and operator role, not only setup permissions | Intended user can enter and perform the supported operation |
| Total differs from console | Dates, exclusive end, metric, filters, currency, grouping | Same query reproduces the amount |
| No change evidence | Agent role and CloudTrail availability | Determine source absence before proposing a cause |
| Uploaded mapping ignored | File active state, identifiers and task scope | Known mapping can be retrieved separately from memory |
| Task never starts | Automation match and shared queue | Distinguish no task creation from queued execution |
| Jira action not visible | Destination binding, approval path and task result | Correct project and resulting issue/comment |
| Slack post denied | App membership, channel ID and connection state | App is in the configured channel and connection active |
| File cannot upload | Type, per-file size and total quota | Input is supported and storage available |
| Deleted automation still has records | Object lifecycle | No new tasks; old task records expected |

The table is engineering troubleshooting guidance based on the cited configuration and integration pages. It is not a claim of a native unified diagnostic workflow.

## 13. Worked example and reference material

The approved reporting and investigation cases are illustrated with a synthetic, reconcilable cost comparison.

### F-10 — Context and evidence in reporting and anomaly use cases

The approved reporting and anomaly cases reuse data access and context, but they start with different questions. A periodic report asks for a stable comparison over a defined period. An anomaly investigation asks what contributed to a detected deviation and what evidence supports an operational explanation. Both depend on source identity and query basis before retained preferences or formatting become useful. [FS52] [FS57] [FS58]

![Retained inputs and session context](../assets/diagrams/er-finops-context.svg)

For [UC-F04, prepare a periodic cost report](../catalog/index.html#UC-F04), the operator maintains authoritative ownership or allocation mappings in context files. The agent can read those files but does not rewrite them through conversation. Persistent memory can retain reporting preferences and corrections for subsequent work. Older messages within a long conversation may instead be summarized to fit the context window. These are separate mechanisms and should be tested with different known facts. [FS53]

The runtime loads retained context for a session, but ending that runtime is not deletion of the stored files, memory, conversations or artifacts. The configuration belongs to the instance, and the guide does not establish shared knowledge across instances. When a team changes ownership, it should update the authoritative mapping and the uploaded file deliberately rather than assuming a conversational correction changed every representation. [FS54]

For [UC-F05, investigate a cost anomaly](../catalog/index.html#UC-F05), the event-created variant adds an automation and managed-event dependency to the same analytical objective. Trace the source event to the matching automation, then to the queued task and its result. A task that never started indicates a different problem from a finished task whose Slack delivery failed. Review the condition and publication destination before enabling unattended operation. [FS52] [FS55] [FS56]

| Approved case | Product objects used | Evidence that belongs to the outcome |
|---|---|---|
| Historical cost analysis | Instance, source-access role and conversation or task | Reproducible query basis and reconciled figures |
| Periodic cost report | Context file, optional memory, automation, task and artifact | Reviewed period, comparisons, missing inputs and actual output |
| Anomaly investigation | Source anomaly, optional event rule, automation and task | Contributors, change evidence and unresolved causes |
| Recommendation prioritization | Upstream recommendation and workload context | Assumptions, conflicts, accepted or deferred decision |
| Post-change measurement | Before/after source data and engineering change record | Observed difference and explicit attribution limits |

The last column is an engineering acceptance model, not a list of automatically populated AWS fields. In particular, a cost decrease is not itself proof that a change caused the saving. A source recommendation is a candidate, not a purchase or infrastructure-change authorization. [FS57]

The shared operational-review case can consume these outputs alongside service-health reports. That handoff is a team process between independently scoped services. It preserves source and execution identities; it does not transfer credentials, merge memory or create a cross-product orchestration engine.

### F-U01 — Cost-variance analysis: worked example

**Synthetic fixture; USD; two complete 14-day windows; identical account, service and cost basis.** Rates and quantities are teaching values, not AWS prices. This fixture now includes quantities and rates, so it can support arithmetic attribution rather than just two totals.

| Component | Baseline quantity | Comparison quantity | Unit rate | Baseline cost | Comparison cost |
|---|---:|---:|---:|---:|---:|
| Storage quantity | 10,000 | 12,000 | 0.10 | 1,000 | 1,200 |
| Request quantity | 2,000,000 | 3,000,000 | 0.0001 | 200 | 300 |
| Transfer quantity | 2,000 | 4,740 | 0.10 | 200 | 474 |
| Total | — | — | — | 1,400 | 1,974 |

The delta is 574, or 41%. Component contributions are 200 storage, 100 requests and 274 transfer. The transfer component explains about 47.7% of the monetary delta, not 47.7% of all spending. Rates are unchanged in this fixture. These calculations can be reproduced without an agent.

**Prepared operational evidence:** a deployment at 10:02 UTC enabled a second export destination; a job log after that deployment records 2,740 additional transfer units. This is invented corroborating evidence. It supports the transfer-volume explanation in this fixture but cannot explain the additional storage and request quantities without more evidence.

**Walkthrough:** fix the query contract, reconcile all line items, compute each delta, inspect the prepared change/job evidence, and report a partial explanation. The expected answer identifies transfer as the largest contributor, marks the export change as supported by the supplied log, and leaves storage/request causes unresolved. Do not add potential recommendation savings to the historical delta.

**Failure branches:** a different cost metric or date window invalidates the comparison; missing job evidence leaves only a temporal association; lack of recommendation-service data prevents evaluating a candidate saving. A proposed lifecycle or capacity change requires a separate engineering decision and measurement plan.

The repository's deterministic fixture test verifies the arithmetic. It is not a test of the AWS service, recommendation quality or causal inference.

### F-07 — Documentation coverage and references

The guide follows a cost question from source access through context, task execution, and publication. The coverage table separates that explanation from complete IAM policies, service quotas, and provider-specific setup that remain in the official reference. A forecast, recommendation estimate, and observed cost are treated as distinct results throughout.

The reference register identifies the documented behavior behind these distinctions. The integration inventory and selected context and data-lifecycle guidance were rechecked on 22 October 2026. Earlier source qualifications remain applicable, and the worked arithmetic is synthetic. No account query, publication action, or measured savings outcome was executed for this guide.

| Official topic | Treatment | Boundary |
|---|---|---|
| Setup, roles, instance creation | Role/policy map and ordered setup | Exact account-specific IAM statements remain official examples |
| Cost and recommendation sources | Provenance, read-only query and reconciliation | No complete enumeration of every supported cost dimension |
| Files, memory, compaction | Separate mechanisms and lifecycle | No invented internal precedence or summary algorithm |
| Tasks and events | Configuration, rule/queue sequence and failure split | Preview event types only as documented |
| Reporting and integrations | Artifacts, destination binding and effect-specific approval | No live external publication performed |
| Data protection and quotas | Object matrix, location distinction, selected constraints | Complete current quota and policy tables linked |

#### Official sources and reviewed sections

- [FS01] Product functions and recommendation provenance.
- [FS02] Five creation steps, roles, team access, verification and deletion prerequisites.
- [FS03] Four policy responsibilities, trust, source actions and managed EventBridge permissions.
- [FS04] File formats/limits, upload/soft deletion, memory and compaction.
- [FS05] Task queue, manual/scheduled/event work and execution observation.
- [FS06] Supported effects, approval rules and analytical boundaries.
- [FS07] Cost Anomaly Detection, rule/automation setup and destination checks.
- [FS08] Persistent/runtime isolation and object-specific lifecycle.
- [FS09] Preview storage and US cross-Region inference.
- [FS10] Default quotas and adjustability.
- [FS11] Report formats, artifacts and revision.
- [FS12] Jira registration/connections, operations, states and failures.
- [FS13] Slack registration/connections, one-way behavior and membership failures.
- [FS14] Cost Explorer GetCostAndUsage request semantics; read-only example.

[FS01]: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
[FS02]: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
[FS03]: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
[FS04]: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
[FS05]: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
[FS06]: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
[FS07]: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
[FS08]: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
[FS09]: https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html
[FS10]: https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html
[FS11]: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
[FS12]: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
[FS13]: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
[FS14]: https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html
[FS401]: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
[FS402]: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
[FS403]: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
[FS404]: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
[FS405]: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
[FS406]: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
[FS407]: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
[FS408]: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
[FS409]: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
[FS50]: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
[FS501]: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
[FS502]: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
[FS503]: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
[FS504]: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
[FS505]: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
[FS506]: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
[FS507]: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
[FS508]: https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html
[FS509]: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
[FS51]: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
[FS510]: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
[FS52]: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
[FS53]: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
[FS54]: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
[FS55]: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
[FS56]: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
[FS57]: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
[FS58]: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
[FS701]: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
[FS702]: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
[FS703]: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
