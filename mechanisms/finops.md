# AWS FinOps Agent — mechanisms and enablement

Reviewed 21 October 2026. Independent checks and examples are proposed; no live workflow was executed.

## Mechanism model

A cost explanation combines retrieved account data, maintained organization files and remembered preferences or corrections. A remembered explanation is not a newly verified cost driver. Reconcile the data window and cost basis each time before acting on an interpretation.

Conversation corrections and investigation outcomes can become agent-specific memory. Uploaded context supplies maintained organization definitions. Scheduled or event-triggered tasks use that context but do not confer permission to resize infrastructure.

The service and all mechanisms in this guide are preview. Data access depends on the configured IAM role; external writes have action-specific approval behavior.

## F-M01 — Establish the agent identity and data boundary

**Surface:** FinOps console / creation wizard

**Availability:** Preview

**Activation:** Separate agent role and operator access

### Documented mechanism

An agent has its own IAM role, context, memory, tasks and artifacts. Account-data visibility follows the configured role; another agent is not a shared-memory extension.

### Enable and configure

Preview access and permissions to create the required roles and operator access.

1. Create the agent in the console and select or create its agent role.

2. Configure the operator web-application role and optional integrations.

3. Review the wizard settings and verify access from the intended operator identity.

### Scope and persistence

Content is isolated between agents. Storage and cross-region processing have a separately documented US data-location boundary.

### Independent checks — proposed

- Compare an allowed cost query with an intentionally unavailable data source.

- Record the agent identity and confirm the operator is not accidentally using another agent.

### Record to retain — proposed

Agent ID, role policies, operator scope, approved data-location assessment and test results.

### Stop, correct or remove

Change role policies and integrations through the administrative configuration; do not treat a chat instruction as an access restriction.

### Limits and fallback

A broad data role can expose more than the displayed report scope. Missing permissions can produce incomplete analysis.

Use a manually scoped cost export while resolving access; do not grant administrator access for convenience.

### Illustrative task — not executed

Illustrative: create a report-only evaluation agent using a narrowly scoped role and no external publishing integration.

### Official guidance

[FI: IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

[FC: Create a FinOps agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

[FP: Data protection](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

[FR: Cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

## F-M02 — Supply maintained organization context

**Surface:** Web application → Context files

**Availability:** Preview

**Activation:** Upload supported text files

### Documented mechanism

Uploaded context supplies owner mappings, categories, report structures and instructions. The agent reads this material but cannot edit or delete the files through chat.

### Enable and configure

Approved non-sensitive context and authorized users of the agent.

1. Open Context files and upload a focused supported file.

2. Use a new question to check the mapping or instruction.

3. Maintain the file in the workspace when organization definitions change.

### Scope and persistence

Files are available to users with access to the agent and used by its work.

### Independent checks — proposed

- Use a synthetic account-to-team mapping and verify a sampled attribution.

- Check for conflicting old context before accepting the result.

### Record to retain — proposed

Context filename, approved revision, sampled mapping and verification output.

### Stop, correct or remove

Delete removes a file from active context by soft deletion; Restore reactivates it.

### Limits and fallback

Do not upload personal or sensitive information. An owner mapping is not an IAM policy.

Provide the approved mapping explicitly for a single task and label the missing maintained context.

### Illustrative task — not executed

Illustrative file: a synthetic account identifier mapped to a team alias, without personal contact details.

### Official guidance

[FM: Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

[FP: Data protection](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

## F-M03 — Retain and correct preferences across sessions

**Surface:** Agent conversation

**Availability:** Preview

**Activation:** Natural-language remember, update and forget requests

### Documented mechanism

Memory can retain preferences, corrections and task outcomes for later sessions. This differs from an uploaded context file and from the summary of one long conversation.

### Enable and configure

A configured agent and non-sensitive facts appropriate to retain.

1. Ask the agent to remember a specific reporting preference or correction.

2. Start a separate conversation and check its use.

3. Request an update or forgetting of that specific entry when it is no longer valid.

### Scope and persistence

Memory belongs to the agent, not to every agent in the account.

### Independent checks — proposed

- Use a harmless synthetic reporting preference, not a secret.

- Test correction in a new session; retain the original data query for reconciliation.

### Record to retain — proposed

Memory request, agent ID, independent new-session output and correction record.

### Stop, correct or remove

Use the documented chat controls for memory; do not assume forgetting deletes earlier conversation records.

### Limits and fallback

A remembered cause must be rechecked against current data. No separate model-training switch is established by these instructions.

Provide the preference explicitly and record that cross-session recall was not demonstrated.

### Illustrative task — not executed

Illustrative: “Remember that this evaluation uses unblended costs grouped by Region. Treat prior investigation conclusions as hypotheses.”

### Official guidance

[FM: Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

[FD: Cost inquiry and data-source access](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[FP: Data protection](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

## F-M04 — Create bounded on-demand and scheduled tasks

**Surface:** Tasks / Automations workspaces

**Availability:** Preview

**Activation:** Explicit task request or recurring automation

### Documented mechanism

On-demand, scheduled and event-based work share a task queue. A task is created when requested; a normal cost question can remain an interactive answer.

### Enable and configure

An accessible agent, required data permissions and a bounded output definition.

1. Ask to create a task, or open Tasks → Create tasks.

2. For recurrence, describe the schedule and output in chat.

3. Inspect the created automation, its task history and destination before relying on it.

### Scope and persistence

Each trigger creates a task. Execution duration is distinct from the schedule and from presentation demo time.

### Independent checks — proposed

- Start with report generation and no Jira or Slack destination.

- Verify schedule interpretation, task state and artifact completeness.

### Record to retain — proposed

Task or automation definition, schedule, task IDs, artifact and acceptance decision.

### Stop, correct or remove

Disable or delete the automation to stop future triggers. Cancel a running task from its detail page where supported.

### Limits and fallback

External publishing behavior must be reviewed separately; a task may carry more effects than a read-only report.

Run the query interactively and retain a manual report while investigating task errors.

### Illustrative task — not executed

Illustrative: “Create a task to reconcile last month’s service costs using the approved cost basis. Produce a report; do not publish externally.”

### Official guidance

[FT: Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

[FP: Data protection](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

## F-M05 — Route cost anomaly events to an investigation

**Surface:** Chat setup / Automations / EventBridge

**Availability:** Preview

**Activation:** Monitor event plus configured response

### Documented mechanism

A Cost Anomaly Detection event starts a matching automation through an EventBridge managed rule. The agent then runs the configured investigation and destination action.

### Enable and configure

An anomaly monitor, the required EventBridge permissions and an approved destination connection.

1. Register Slack at account level, then bind the selected channel to the agent with Add connection.

2. In chat, specify the monitor or threshold, investigation and destination.

3. Open Automations and inspect the COST_ANOMALY trigger, status and associated tasks.

### Scope and persistence

The automation reacts to matching monitor events; it does not independently replace Cost Anomaly Detection.

### Independent checks — proposed

- Use an authorized test destination and inspect the exact monitor/threshold.

- Trace a matching event to a task and delivery record without deliberately generating unnecessary spend.

### Record to retain — proposed

Monitor, rule/automation identity, task ID, query evidence and destination result.

### Stop, correct or remove

Disable or delete the automation to stop new tasks. Existing task records remain.

### Limits and fallback

Slack delivery is not gated by per-message approval. Automatic Jira writes are pre-authorized during setup.

Investigate an existing anomaly on demand and label the missing event-routing evidence.

### Illustrative task — not executed

Illustrative: configure a staging evaluation monitor to send findings only to an approved test channel.

### Official guidance

[FE: Event-triggered cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

[FG: Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## F-M06 — Apply action-specific publishing controls

**Surface:** Chat, tasks and automations

**Availability:** Preview

**Activation:** Different approval behavior by action and origin

### Documented mechanism

Interactive or on-demand Jira issue/comment actions require confirmation. Scheduled and event-based Jira actions are pre-authorized. Slack posting does not require approval, including interactive use.

### Enable and configure

An approved integration and a destination appropriate for the data.

1. Inspect the Jira project or Slack channel connection.

2. For interactive Jira, review the displayed action details before confirming.

3. For automation, review the entire publishing instruction before enabling it.

### Scope and persistence

This is not a universal human-approval layer and is not authorization to resize infrastructure.

### Independent checks — proposed

- Test interactive Jira refusal/confirmation with a disposable issue.

- Verify automation and Slack publishing only in approved test destinations.

### Record to retain — proposed

Action type, invocation origin, destination, approval or pre-authorization record and delivery evidence.

### Stop, correct or remove

Remove or restrict integrations and disable automations when publishing is no longer approved.

### Limits and fallback

A prompt saying “ask first” should not be substituted for the product’s documented action controls.

Disable external publishing and retain the report for manual review.

### Illustrative task — not executed

Illustrative: generate a cost finding locally in the agent first, then separately authorize a disposable Jira issue.

### Official guidance

[FG: Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

[FT: Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

## F-M07 — Separate retained data from session summarization

**Surface:** Context, task and agent administration

**Availability:** Preview

**Activation:** Automatic summarization; explicit retention controls

### Documented mechanism

Long conversations can be summarized to fit the model context window. Persistent memory, files, conversation history, tasks and artifacts have different lifecycles; an ephemeral runtime does not imply ephemeral records.

### Enable and configure

An owner for retained agent data and a documented removal procedure.

1. Identify whether the unwanted item is context, memory, an artifact, a task or conversation history.

2. Use the specific deletion, forgetting, cancellation or automation control.

3. For categories without individual deletion during preview, evaluate whole-agent deletion with the owner.

### Scope and persistence

Conversation and task records can remain until agent deletion; soft-deleted context can be restored.

### Independent checks — proposed

- Check that disabled automation stops new tasks while historical tasks remain.

- Confirm removal behavior in a disposable agent before using it as a retention procedure.

### Record to retain — proposed

Data category, requested operation, responsible owner, retained residual records and verification result.

### Stop, correct or remove

Whole-agent deletion removes the interaction data and web-app link according to the documented lifecycle; review dependencies first.

### Limits and fallback

Do not equate a summary, a forgotten fact, a disabled automation and complete data removal.

Escalate retention requirements that the preview controls cannot satisfy; do not claim deletion based on an empty chat.

### Illustrative task — not executed

Illustrative: remove a synthetic preference, disable its reporting automation and document which history is still retained.

### Official guidance

[FP: Data protection](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

[FM: Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

## Proposed use-case exercise

Retain a reporting correction without accepting stale cost analysis

Optional 10-minute walkthrough; additional to the core programme. Not an agent-runtime guarantee.

Use a preview evaluation agent and synthetic preferences. Keep external publishing disconnected until separately approved.

### 1. Establish the data contract · 00:00–01:30

**Role:** FinOps reviewer · **Mechanism:** F-M01

State date window, cost basis, currency, filters and agent identity.

**Gate:** Repeatable query definition.

### 2. Load maintained context · 01:30–03:00

**Role:** Context owner · **Mechanism:** F-M02

Upload a sanitized team mapping and inspect a sample.

**Gate:** Mapping revision and correct attribution.

### 3. Remember a preference · 03:00–04:30

**Role:** Operator · **Mechanism:** F-M03

Request a reporting-format preference, not an unsupported root-cause conclusion.

**Gate:** Specific memory request retained.

### 4. Test a new session · 04:30–06:30

**Role:** FinOps reviewer · **Mechanism:** F-M03

Check the preference and reconcile the cost result independently.

**Gate:** New session plus source totals.

### 5. Inspect any automation effects · 06:30–08:30

**Role:** Integration owner · **Mechanism:** F-M06

Review schedule/event trigger and Jira/Slack destination behavior.

**Gate:** Action-specific approval boundary recorded.

### 6. Correct or remove the test data · 08:30–10:00

**Role:** Data owner · **Mechanism:** F-M07

Forget the preference and remove active context where appropriate.

**Gate:** Residual history acknowledged.

### Exit

The retained preference is correctly used, the cost numbers reconcile, and any publication is separately authorized. No savings outcome is asserted.

### Fallback

Use synthetic data and a prepared task history; do not generate cloud spend to trigger a demonstration.
