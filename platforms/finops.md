# AWS FinOps Agent — platform capabilities and mechanisms

Agent-instance configuration, authorized data retrieval, persistent context, task orchestration, artifacts and external publication. Cost-anomaly investigation is an application of these abilities.

AWS FinOps Agent is documented as preview. Confirm current eligibility, service dependencies and data-processing boundaries before enabling it.

## Classification

**Platform capability**: A reusable ability exposed by the platform. Example: Retain operational context across investigations.

**Operation**: An action on a platform resource or configuration object. Example: Attach a memory store or change its active state.

**Mechanism**: The documented process connecting inputs, state, execution and outputs. Example: Select a store by description, then retrieve relevant entries.

**Use case**: An engineering problem that combines capabilities and mechanisms. Example: Investigate a recurring alarm while checking contradictory telemetry.

## Capability inventory

### F-C01 — Agent-instance isolation and role separation

**Group:** Instance and data access

Each agent instance has its own permissions, memory, files, task queue and integrations. Data access and operator access are separately configured.

**Platform resources:** Agent instance; agent role; operator role.

**Supported operations:** Create an instance; configure the data and operator roles; associate required integrations.

**Boundary:** Separate instances do not imply a shared organization-wide memory. Access to the agent can expose its shared context to its users.

**Sources:** [F02](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html), [F08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

### F-C02 — Authorized source-data retrieval

**Group:** Instance and data access

The agent queries authorized AWS services for cost data, recommendations and operational-change evidence.

**Platform resources:** Agent role; Cost Explorer data; recommendation sources; CloudTrail access.

**Supported operations:** Activate dependencies; grant required API actions; inspect data-source provenance and query filters.

**Boundary:** Removing a source permission can remove a particular analytical input without disabling all cost inquiry. Retrieved recommendations are not an independent optimization calculation.

**Sources:** [F03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [F06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

### F-C03 — Organization-specific reference context

**Group:** Context and retained state

Uploaded files provide account mappings, instructions and reporting conventions that the agent can read during work.

**Platform resources:** Context file; active or soft-deleted state; workspace visibility.

**Supported operations:** Upload, delete or restore files through the Context files workspace.

**Boundary:** The agent cannot modify or delete uploaded context files through conversation. Files are visible to users who can access that agent.

**Sources:** [F04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

### F-C04 — Persistent preferences and corrections

**Group:** Context and retained state

Conversational memory retains preferences, ownership details, corrections and previous task outcomes for subsequent sessions.

**Platform resources:** Agent-instance memory.

**Supported operations:** Ask the agent to remember, update or forget a non-sensitive fact or preference.

**Boundary:** Conversational memory is different from the source files containing similar facts. Do not assume that editing one automatically synchronizes the other.

**Sources:** [F04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

### F-C05 — Bounded conversation-context management

**Group:** Context and retained state

As the context limit approaches, older conversation portions are summarized while recent messages remain in full.

**Platform resources:** Conversation context; older-message summary; recent messages.

**Supported operations:** Inspect retained decisions and restate critical constraints when needed.

**Boundary:** Compaction is not verbatim recall or a guarantee that every detail survives. It is separate from cross-session memory.

**Sources:** [F04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

### F-C06 — Task queue and automation execution

**Group:** Execution, outputs and lifecycle

On-demand, scheduled and event-based tasks run through a shared queue; automations create tasks when their conditions match.

**Platform resources:** Task; automation; schedule; supported event rule; task history.

**Supported operations:** Create an on-demand task or automation; inspect queued and completed work; stop future creation by removing the automation.

**Boundary:** The reviewed preview documents Cost Anomaly Detection events, not an arbitrary general event-processing framework. Existing tasks have a separate lifecycle.

**Sources:** [F05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [F09](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

### F-C07 — Destination-specific external publication

**Group:** Execution, outputs and lifecycle

Configured Jira and Slack integrations support publishing actions with different approval rules by action and invocation path.

**Platform resources:** Destination integration; issue or comment action; channel post; approval and task history.

**Supported operations:** Review interactive Jira actions; configure automation destinations; inspect resulting external artifacts.

**Boundary:** There is no universal approval prompt for every write. Slack posts and pre-authorized automated Jira work differ from interactive Jira work.

**Sources:** [F06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

### F-C08 — Report artifact generation

**Group:** Execution, outputs and lifecycle

The service generates report artifacts in documented formats, including HTML, PDF and editable PowerPoint, and supports subsequent revision requests.

**Platform resources:** Report artifact; source data; report instructions.

**Supported operations:** Request a report, inspect its source breakdowns and revise presentation requirements.

**Boundary:** A generated chart or narrative must be reconciled to source data. Formatting quality does not establish numerical or causal accuracy.

**Sources:** [F07](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html), [F06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

### F-C09 — Object-specific data lifecycle

**Group:** Execution, outputs and lifecycle

Persistent agent data is distinct from the ephemeral session runtime, and deletion or stopping behavior depends on the object type.

**Platform resources:** Context file; memory; conversation; task; automation; agent instance.

**Supported operations:** Use the documented control for the intended object; review storage and inference location independently.

**Boundary:** Deleting an automation stops future task creation, not every retained execution record. Storage location is not a complete statement of processing geography.

**Sources:** [F08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [F10](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

## Mechanisms and enablement

### F-M01 — Source-backed analysis and permission dependencies

**Capabilities:** F-C01, F-C02, F-C08

**Trigger:** A request or task requires cost totals, recommendation data or evidence of operational changes.

**Process:** Agent role and query scope → Underlying AWS API results → Contextual interpretation → Reviewable answer or artifact

The service retrieves source data rather than modifying billing records. Optimization recommendations originate in Cost Optimization Hub and Compute Optimizer. The agent summarizes them; it does not generate the underlying optimization analysis.

**State and lifecycle:** The authorized data sources and filters determine the available evidence. Removing cloudtrail:LookupEvents removes change-event evidence without necessarily preventing basic cost inquiry.

**Enablement:**

1. Configure the agent data role and separate operator role through the supported setup path.
2. Activate the required upstream cost and recommendation services.
3. Inspect the actual policy actions and data filters rather than relying on a role name.

**Controls:** Reconcile numerical results and validate causal explanations separately. A temporal correlation with a deployment is not sufficient proof of the cost driver.

**Proposed verification:** Proposed check: reproduce a reported total using identical dates, basis, granularity and filters. Independently verify recommendation provenance and any change evidence. Record unavailable sources rather than filling gaps with assumptions.

**Sources:** [F03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [F06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [F07](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

### F-M02 — Reference files, conversational memory and compaction

**Capabilities:** F-C03, F-C04, F-C05

**Trigger:** A session or task uses organizational context, or a conversation approaches its context limit.

**Process:** Uploaded files or stated preferences → Persistent instance context → Session runtime loading → Answer or compacted conversation

Uploaded context is operator-maintained; conversational preferences can be remembered, updated or forgotten. Older conversation content is summarized as the context budget fills. These are separate state mechanisms.

**State and lifecycle:** Persistent files and memory are loaded into a session-isolated ephemeral runtime. Agent instances do not share this state.

**Enablement:**

1. Upload authoritative non-sensitive reference files through the Context files workspace.
2. Use explicit remember, update or forget requests for conversational preferences.
3. Test file retrieval and memory recall independently; restate critical constraints when evaluating compacted conversations.

**Controls:** All users with agent access can see context files. Updating memory does not establish that an uploaded file or prior conversation was also changed.

**Proposed verification:** Proposed check: establish a harmless preference, open a new conversation and examine its application. Correct or forget it and repeat. Use a different test for uploaded context so file retrieval is not mistaken for memory recall.

**Sources:** [F04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [F08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

### F-M03 — Event matching and queued execution

**Capabilities:** F-C06

**Trigger:** A configured anomaly event or schedule matches an automation.

**Process:** Monitor event or schedule → Managed rule and automation match → Queued task → Recorded execution result

The documented anomaly path connects Cost Anomaly Detection, managed EventBridge rules and task creation. On-demand, scheduled and event-based work shares the task queue.

**State and lifecycle:** An automation defines future invocation; each created task has its own execution history. The documented preview event source is Cost Anomaly Detection.

**Enablement:**

1. Configure the anomaly monitor and the agent permissions needed to manage the service's EventBridge rules.
2. Connect the intended destination and define explicit monitor or threshold conditions.
3. Inspect the resulting automation and rule; a conversational acknowledgement alone is not proof of registration.

**Controls:** IAM ownership and account conditions constrain rule management. Destination publishing may be pre-authorized when the automation is configured.

**Proposed verification:** Proposed check: trace an authorized test event through rule match, task creation, execution and destination result. Remove or disable the automation and verify that future tasks stop; examine existing tasks separately.

**Sources:** [F03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [F05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [F09](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

### F-M04 — Action- and invocation-specific publication approval

**Capabilities:** F-C07

**Trigger:** The agent creates a Jira issue, adds a Jira comment or posts a Slack message.

**Process:** Configured destination → Action and invocation type → Applicable approval rule → External artifact and history

Interactive and on-demand Jira issue/comment actions require approval. Scheduled or event-based Jira actions are pre-authorized when the automation is configured. Slack posting does not require an approval prompt, including interactive posting.

**State and lifecycle:** Task history records results. Automation setup is an authorization decision, not just a timing preference.

**Enablement:**

1. Connect only intended Jira projects and Slack destinations.
2. Inspect the content and destination for interactive Jira approvals.
3. For automations, review publishing instructions before enabling recurring or event-based execution.

**Controls:** Do not describe the service as approval-gated for all external writes. Prevent sensitive context from being placed into automatically published messages.

**Proposed verification:** Proposed check: in designated test destinations, inspect an interactive Jira approval, a pre-authorized automation result and a Slack post. Confirm the actual destination and record whether an approval prompt occurred.

**Sources:** [F06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [F05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

### F-M05 — Data lifecycle and processing boundaries

**Capabilities:** F-C01, F-C09

**Trigger:** An operator changes or removes retained context, an automation or the agent instance.

**Process:** Identify the object → Apply its supported control → Check retained versus inactive data → Confirm processing boundary

Context-file deletion is reversible soft deletion. Forget requests change memory. Deleting an automation stops future task creation. In the reviewed preview guidance, individual conversations and task records remain until agent deletion rather than supporting individual deletion.

**State and lifecycle:** The preview stores agent data in us-east-1; Bedrock inference may run in other US Regions. Persistent storage and ephemeral session execution are different layers.

**Enablement:**

1. Identify whether the intended target is a file, memory, conversation, task, automation or whole instance.
2. Use the documented workspace or lifecycle control for that object.
3. Review the current storage and cross-Region inference guidance before making a data-location assertion.

**Controls:** Soft deletion is not physical erasure. Stopping future automation is not equivalent to removing existing records or already published external artifacts.

**Proposed verification:** Proposed check: use non-sensitive test data to distinguish inactive, restored, forgotten and retained records. Do not delete a real agent merely to demonstrate lifecycle behavior.

**Sources:** [F08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [F10](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

## Optional verification exercise

Verify context, event execution and publication separately

Proposed prepared-result exercise; test data and test destinations only; 8 minutes.

1. 2 min — Inspect the agent data role and source-query scope.
2. 2 min — Compare a test memory preference with an uploaded reference file.
3. 2 min — Trace an anomaly event into an automation task and its result.
4. 2 min — Identify the publishing approval rule and reconcile the reported numbers.

**Acceptance:** Separate source-data accuracy, retained context, event execution and publishing authority. No measured savings or proven causality is inferred.

## Evidence boundary

Official product documentation supports the product statements. Configuration steps are documented guidance; verification exercises are proposed and were not executed. Selected critical sources were rechecked on 21 October 2026; other links are retained from the preceding review. This is not an exhaustive service catalog, a fresh audit of every historical claim, or a live AWS test.

## Official source register

- [F01 — Service scope](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html) — retained from preceding review
- [F02 — Creating an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html) — retained from preceding review
- [F03 — IAM setup and dependent services](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html) — selected content rechecked
- [F04 — Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html) — selected content rechecked
- [F05 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html) — selected content rechecked
- [F06 — Action approval and analytical boundaries](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) — selected content rechecked
- [F07 — Custom cost reporting and artifacts](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html) — retained from preceding review
- [F08 — Data protection and lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html) — selected content rechecked
- [F09 — Event-based anomaly response](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html) — retained from preceding review
- [F10 — Cross-Region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html) — retained from preceding review
