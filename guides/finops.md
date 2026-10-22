# AWS FinOps Agent

Architecture, cost-data sources, organizational context, and task execution

AWS FinOps Agent is documented as a preview service for cost inquiry, anomaly investigation, reporting, and the interpretation of upstream optimization recommendations. Its work begins with a defined comparison: the accounts, dates, cost basis, and dimensions under consideration. It combines authorized source results with the organization’s uploaded context and retained preferences, then produces an answer, a task result, or a report. [FS01]

This guide follows that sequence. It explains the instance and permissions first, identifies the supported data and collaboration integrations, and then separates reference files, persistent memory, and conversation summarization. The task chapter follows a scheduled or event-driven request into the queue and through publication. The worked example distinguishes a numerical cost contribution from evidence of an operational cause.

During the reviewed preview, agent data is stored in us-east-1 and inference can use other US Regions; those are different boundaries. Diagrams are logical service models. Examples and proposed checks are not live account results, purchase authorizations, or measured savings. [FS08] [FS09]

## 01. Service architecture

The instance persists configuration and context; conversations and tasks perform individual pieces of work. The resource model explains which state belongs to each.

### F-01 — The agent instance and its execution environment

AWS FinOps Agent combines authorized AWS data with an instance’s organizational context to perform cost-related work. The instance is the durable configuration: it has an agent data role, operator access, files, memory, connections, and a task queue. A conversation or task is a particular execution within that instance. This distinction explains why a saved automation can create many tasks and why cancelling one task does not remove the automation. [FS02] [FS05] [FS08]

![FinOps Agent logical architecture](../assets/diagrams/finops-architecture.svg)

The architecture separates data retrieval from interpretation and publication. Upstream services return cost records, anomalies, recommendations, or change events. Organizational context gives those records a business meaning, such as which team owns an account. The agent can produce an answer or artifact and, through a configured integration, publish supported results. The permissions for retrieving evidence and those for publishing a result are not interchangeable. [FS01] [FS03] [FS12] [FS13]

Each instance has its own retained content and execution records. The data-protection guide describes persistent encrypted storage and an ephemeral runtime isolated per session. Files and memory can be loaded into that runtime for use, while conversation and task records are retained separately. The ephemeral runtime should not be mistaken for the only place the data exists. [FS08]

| Function | Required platform abilities | Detailed explanation |
|---|---|---|
| Cost inquiry | Authorized source queries and a defined comparison basis | F-M01 |
| Organizational reporting | Context-file retrieval, retained preferences, report generation | F-M02, F-M03, F-04 |
| Anomaly investigation | Monitor event, automation, queue, source evidence | F-M05 |
| Recommendation review | Upstream recommendation retrieval and workload context | F-M01, F-08 |
| Recurring delivery | Scheduled task creation and an appropriate destination | F-03, F-05, F-M06 |

Optimization recommendations originate from the documented upstream recommendation services. The agent’s explanation can help a team interpret and route them, but it is not an independent measurement of realized savings. The next chapter identifies those sources and the permissions that make each one available. [FS01] [FS06]

## 02. Cost-data sources and collaboration connections

A cost conclusion depends on its source data and query basis. Collaboration destinations add a separate publication path with its own authorization and lifecycle.

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

### F-M01 — Cost queries and recommendation provenance

A cost question becomes a set of data queries with a specific comparison basis. The returned amounts, recommendations, and change records then support different conclusions. Reproducing the amount is the first step; explaining its cause requires additional evidence.

The agent translates an inquiry into supported data-source calls, interprets returned evidence using the instance's context, and generates a response or artifact. Cost Explorer totals, anomaly events, recommendation records and CloudTrail change records answer different questions. [FS01] [FS03]

| Evidence | Establishes | Does not establish by itself |
|---|---|---|
| Matching cost query | Spend for the specified dates, metric, scope and dimensions | Why a workload consumed that usage |
| Anomaly record | A detected deviation under the monitor's model | Root cause of the deviation |
| Recommendation source | An upstream optimization candidate and its assumptions | Realized saving or authorization to apply it |
| Operational event | A recorded change at a time | That the change caused the entire cost movement |

The right procedure is to reproduce the numerical result first, then evaluate the explanation. Fix the time window, cost metric, granularity, filters, currency and relevant allocation assumptions. Require the response to identify unavailable sources instead of filling their absence with a causal story. These comparison rules are engineering guidance, not a new query mode. [FS06]

**Read-only query example:**

```bash
aws ce get-cost-and-usage \
  --time-period Start=2026-09-01,End=2026-09-15 \
  --granularity DAILY --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE
```

The end date is exclusive. This example deliberately has no account, Region or tag filters; add the same approved filters used in the agent question before comparing results. Cost Explorer availability, permissions and API charges still apply. The command was not executed here and must not be compared to a differently scoped agent total. [FS14]

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

## 03. Organizational knowledge and session context

Uploaded mappings, retained preferences, and summarized conversations are different representations of organizational context. The operator must know which representation to correct.

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

![Reference files, memory, and the session runtime](../assets/diagrams/finops-context.svg)

The persistence boundary is the agent instance. The data-protection guide describes context and memory files in encrypted AWS-managed storage, loaded at session start into an isolated ephemeral runtime. Conversation and task records are retained alongside their own execution records. The guide does not establish a shared memory across instances or an automatic precedence rule that resolves conflicting statements in a file and a remembered preference. [FS08]

Operators manage conversational memory by asking the agent to remember, update, or forget a specific fact. Uploads remain operator-maintained files: a request to forget a preference is not an edit to a CSV containing the same information. When ownership changes, identify which representation is authoritative, update the file where appropriate, and correct the retained preference separately. Earlier reports remain historical artifacts rather than being silently rewritten. [FS04] [FS08]

A useful acceptance exercise uses a harmless preference, such as placing the comparison table before commentary. Set it, start a new conversation, and check whether it is applied. Correct or forget it and repeat. Test file retrieval with a different known fact. These observations distinguish successful application of retained context from an assumption about hidden model state. The procedure is a proposed test, not a result observed in an AWS account.

Recovery is object-specific. A soft-deleted context file can be restored through its workspace; memory can be corrected conversationally; earlier conversations and task records have the documented preview retention restrictions. None of these controls proves a general backup-and-restore capability for an entire instance. F-M07 describes the supported lifecycle actions. [FS08]

### F-M04 — Conversation summarization and context limits

A long conversation has a different lifecycle from persistent memory. As earlier messages are summarized, the session preserves a condensed working context rather than every word of the exchange. Important comparison assumptions should therefore remain explicit in the current task and its authoritative reference material.

As a conversation approaches its context limit, older messages are summarized while recent messages remain in full. This is within-conversation context management, distinct from persistent memory and uploaded files. The documentation does not promise verbatim retention or expose a general customer setting for the summarization algorithm. [FS04]

**Engineering procedure:** put critical constraints in a concise current task specification and reference the authoritative file or source record. When resuming a long conversation, ask the agent to restate the comparison basis and unresolved questions, then correct any discrepancy before requesting another calculation. This tests retained context; it does not prove that every earlier message remains available.

## 04. Tasks, reporting, and data lifecycle

Requests and automations create executions; executions produce results and artifacts. This chapter follows that sequence through publication and the supported retention controls.

### F-03 — Tasks, schedules, and execution history

Tasks provide execution records for requested work. Automations are definitions that create tasks later, either on a schedule or from a supported event. Their separate lifecycles explain why stopping future task creation does not remove a result that already exists.

A task is an execution record. An automation is a rule for creating future tasks. On-demand, scheduled and event-triggered work shares the queue. Asking a conversational question is not necessarily a request to create a durable task; task creation should be explicit. [FS05]

**On-demand procedure:** use the Tasks workspace or explicitly request a task, give its input scope and desired output, and inspect the resulting task. Check pending/running/completed or failure information and resulting artifacts. Do not treat a conversational acknowledgement as evidence that execution has finished. [FS05]

**Scheduled procedure:** define the required schedule and reporting window separately. Inspect the saved automation's trigger and next applicable execution information. For a daily report, a schedule time does not define whether the report covers the previous calendar day, rolling 24 hours or incomplete current day; specify the window. Removing the automation prevents future tasks but does not remove previously created tasks or published messages. [FS05] [FS08]

### F-M05 — Anomaly events and task creation

![Workflow: Anomaly events and task creation](../assets/diagrams/finops-automation.svg)

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

### F-04 — Report generation and artifact management

A report is a presentation of an analysis, not another source of cost truth. Its usefulness depends on preserving the comparison basis and making the relevant calculations traceable. The artifact and the task that produced it should therefore remain linked when the report is revised or shared.

The service supports report artifacts including HTML, PDF and presentation formats documented by the service. A request can specify the audience, comparison basis, grouping and output format, and subsequent requests can revise the artifact. Source retrieval, calculations and artifact generation are different stages; formatted output is not independent proof that the totals are correct. [FS11]

**Procedure:** ask for one defined report, inspect the source breakdown and period, open/download the artifact, and verify at least one material total using the same source query. Request a revision that names the desired change rather than silently changing the comparison basis. When publishing, check that the file corresponds to the reviewed task and audience. [FS11] [FS06]

The artifact store has a separate default quota from context-file storage. Deleting an artifact does not necessarily delete external copies previously posted to a collaboration system. [FS10] [FS08]

### F-M06 — Publication permissions and approvals

Publication authorization depends on both the destination and the way work was initiated. An unattended automation can carry authorization established during setup, while an interactive Jira action requests approval. Slack posting follows a different documented behavior, so a single blanket approval statement would be misleading.

| Effect | Chat / on-demand task | Scheduled / event task |
|---|---|---|
| Jira issue or comment | Approval requested | Pre-authorized through automation setup |
| Slack post | No approval prompt | No approval prompt |

These are documented differences, not one universal human-approval rule. Automation setup is therefore an authorization decision as well as a scheduling decision. Connected destinations and supplied context must be appropriate for unattended publication. [FS06] [FS05]

**Proposed verification:** in test destinations, record the requested action, invocation type, observed prompt or lack of prompt, and the resulting artifact. A successful Slack post does not demonstrate Jira approval behavior. Removing a future schedule does not retract a previously published message.

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

## 05. Cost-variance analysis

The synthetic example reconciles the monetary change before using limited operational evidence to explain only part of it.

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

## 06. Troubleshooting and operating limits

A numerical disagreement, a missing task, and a failed publication are different faults. Troubleshooting follows the corresponding data, execution, and destination paths.

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

## 07. Documentation coverage

The references document the source, context, task, and publication behaviors discussed here; unexecuted examples remain explicitly labeled.

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
