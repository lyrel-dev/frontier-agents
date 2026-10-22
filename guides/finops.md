# AWS FinOps Agent — configuration and operation

Engineering guide • documentation reviewed 22 October 2026

AWS FinOps Agent is documented as preview. It queries permitted cost and operational sources, interprets the returned information, creates report artifacts and performs supported integration actions. It is not an unrestricted infrastructure-change or financial-purchase executor. Data storage and model inference have different location boundaries: the preview stores agent data in `us-east-1`, while inference may use other US Regions. [FS01] [FS08] [FS09]

This guide explains platform objects before showing their application. Product behavior has official references. **Engineering procedures** and **synthetic exercises** are original recommendations or examples; none is a live account result or a measured saving.

## 01. Platform overview and capabilities

Distinguish the agent instance, permissions, retained context, tasks and outputs.

### F-01 — Resource and authority model

```text
AWS account / Region
  Administrator policy → setup operations
  Registered Jira / Slack integration → agent connection / destination
  Agent data role → permitted AWS cost and operational APIs
  Operator role + user permission → web-app access
                      ↓
Agent instance
  ├─ context files, conversational memory, conversations
  ├─ automations → scheduled/event tasks ┐
  ├─ on-demand tasks ───────────────────┴─ shared queue → results
  └─ report artifacts → local download / configured publication
```

An integration is registered at account level; a connection binds it to an agent and destination. Each agent instance has its own permissions, retained context, task queue and connections. Instance separation is not a shared organization-wide memory service. [FS02] [FS03] [FS08]

| Product function | Supporting platform capabilities | Detailed treatment |
|---|---|---|
| Cost inquiry, comparisons, forecasts and coverage | Authorized source queries; organizational context; conversation | F-02, F-M01, F-M02 |
| Anomaly investigation | Cost Anomaly Detection; operational-change evidence; tasks | F-M01, F-M05 |
| Recommendation triage | Retrieval of upstream recommendations | F-M01 |
| Recurring reporting | Context, automation, queue, artifacts, destinations | F-M02 through F-M06 |
| Team handoff | Explicit external-action permissions and destination binding | F-05, F-M06 |

The recommendations underlying optimization analysis originate in Cost Optimization Hub and Compute Optimizer. The agent contextualizes those recommendations; its prose is not a new independent optimization calculation. [FS01] [FS06]

## 02. Access, sources and integrations

Establish role responsibilities, source-data dependencies and destination connections.

### F-02 — Configure four policy responsibilities and two service roles

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

### F-M01 — Source-backed analysis and recommendation provenance

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

### F-05 — Integration registration and destination connections

| Layer | Jira | Slack |
|---|---|---|
| Account registration | Supported Jira Cloud authorization flow | Workspace authorization |
| Agent connection | Selected Jira space/project key | Channel ID; application already added to that channel |
| Supported effects | Create issues; supported reads/comments | One-way posting and supported artifact sharing |
| Do not assume | On-premises support or arbitrary issue/workflow editing | Reading channel conversations, responding to mentions, editing/deleting posts |

Register the integration, complete authorization, then add the agent-specific connection and confirm its status. Inspect Pending/Active/Error/Inactive states rather than relying on the connection's name. An invalid Jira destination in unattended execution can fail instead of producing a clarifying conversation. A Slack membership error requires adding the app to the intended channel, not granting unrelated AWS permissions. [FS12] [FS13]

**Engineering procedure:** use designated test destinations, post a non-sensitive test result and record its actual location. Confirm that only the intended users can see it. API retries described in the integration guide address transient failures; they do not turn a permission or invalid-destination error into a successful publication.

## 03. Reference files, memory and compaction

Separate operator-maintained inputs, cross-session memory and within-session summaries.

### F-M02 — Uploaded reference files are operator-maintained context

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

### F-M03 — Conversational memory survives sessions; it is not a file update

Memory retains preferences, organizational context, corrections and prior task outcomes for subsequent work. Use explicit remember, update and forget requests to manage it. These requests do not imply that a matching uploaded file or earlier conversation has also changed. Persistent context is instance-local and loaded into a session-isolated runtime. [FS04] [FS08]

**Proposed verification:** remember a harmless preference such as displaying a cost-comparison table before commentary. Open a new conversation and check its application; correct or forget the preference and repeat. Independently test uploaded-file retrieval with a different fact. Record whether the preference was applied, not an unsupported claim about hidden model state.

For conflicting context, identify the authoritative source and update the relevant objects deliberately. Do not claim a documented automatic precedence rule between files and memory where the public guide does not specify one.

### F-M04 — Conversation compaction manages a bounded context

As a conversation approaches its context limit, older messages are summarized while recent messages remain in full. This is within-conversation context management, distinct from persistent memory and uploaded files. The documentation does not promise verbatim retention or expose a general customer setting for the summarization algorithm. [FS04]

**Engineering procedure:** put critical constraints in a concise current task specification and reference the authoritative file or source record. When resuming a long conversation, ask the agent to restate the comparison basis and unresolved questions, then correct any discrepancy before requesting another calculation. This tests retained context; it does not prove that every earlier message remains available.

## 04. Tasks, publication and lifecycle

Trace task creation, event matching, report artifacts, approval and object-specific removal.

### F-03 — On-demand tasks, schedules and observation

A task is an execution record. An automation is a rule for creating future tasks. On-demand, scheduled and event-triggered work shares the queue. Asking a conversational question is not necessarily a request to create a durable task; task creation should be explicit. [FS05]

**On-demand procedure:** use the Tasks workspace or explicitly request a task, give its input scope and desired output, and inspect the resulting task. Check pending/running/completed or failure information and resulting artifacts. Do not treat a conversational acknowledgement as evidence that execution has finished. [FS05]

**Scheduled procedure:** define the required schedule and reporting window separately. Inspect the saved automation's trigger and next applicable execution information. For a daily report, a schedule time does not define whether the report covers the previous calendar day, rolling 24 hours or incomplete current day; specify the window. Removing the automation prevents future tasks but does not remove previously created tasks or published messages. [FS05] [FS08]

### F-M05 — Anomaly events become queued work through a managed rule

The documented event path is Cost Anomaly Detection → managed EventBridge rule → matching automation → task queue → analysis/result. During the reviewed preview, the event type is `COST_ANOMALY`; this does not establish an arbitrary customer-event orchestration platform. [FS05] [FS07]

**Enablement procedure:**

1. Configure a relevant Cost Anomaly Detection monitor and ensure the agent role can manage the service's EventBridge rules.
2. Connect any intended reporting destination using F-05. Set the destination before enabling automatic publication.
3. Request an automation naming the monitor/conditions and the intended investigation and output. Treat threshold values in example prompts as proposed configuration, not service defaults.
4. Open Automations and inspect the stored trigger type, status and last-triggered information. Inspect the created task separately after a matching event.
5. For a test, trace event identity, automation, task, result and external message. Then disable or remove the automation and verify that new matching work stops; existing tasks need separate handling.

AWS's IAM examples constrain rule management using service ownership and account conditions. Do not replace those conditions with broad EventBridge administration merely because task creation failed. [FS03] [FS07]

**Failure branch:** a registered automation with no task can mean there was no matching event, the monitor/condition is wrong, or rule permissions failed. A completed task with no message is a different destination/publication problem. Preserve these distinctions during diagnosis.

### F-04 — Report artifacts and revision

The service supports report artifacts including HTML, PDF and editable PowerPoint. A request can specify the audience, comparison basis, grouping and output format, and subsequent requests can revise the artifact. Source retrieval, calculations and artifact generation are different stages; formatted output is not independent proof that the totals are correct. [FS11]

**Procedure:** ask for one defined report, inspect the source breakdown and period, open/download the artifact, and verify at least one material total using the same source query. Request a revision that names the desired change rather than silently changing the comparison basis. When publishing, check that the file corresponds to the reviewed task and audience. [FS11] [FS06]

The artifact store has a separate default quota from context-file storage. Deleting an artifact does not necessarily delete external copies previously posted to a collaboration system. [FS10] [FS08]

### F-M06 — Approval depends on the action and invocation path

| Effect | Chat / on-demand task | Scheduled / event task |
|---|---|---|
| Jira issue or comment | Approval requested | Pre-authorized through automation setup |
| Slack post | No approval prompt | No approval prompt |

These are documented differences, not one universal human-approval rule. Automation setup is therefore an authorization decision as well as a scheduling decision. Connected destinations and supplied context must be appropriate for unattended publication. [FS06] [FS05]

**Proposed verification:** in test destinations, record the requested action, invocation type, observed prompt or lack of prompt, and the resulting artifact. A successful Slack post does not demonstrate Jira approval behavior. Removing a future schedule does not retract a previously published message.

### F-M07 — Data lifecycle follows the object, not a single delete command

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

## 05. Worked example

Reconcile cost components before assessing the limited evidence for a causal explanation.

### F-U01 — Worked example: decompose a cost increase

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

## 06. Troubleshooting and limits

Test the data, context, execution and destination layers separately.

### F-06 — Limits and troubleshooting decisions

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

## 07. Coverage and official evidence

Review scope exclusions and the source-review record.

### F-07 — Coverage and source-review record

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
