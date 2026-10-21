# AWS FinOps Agent — mechanism reference speaker notes

All reference slides are untimed. Optional exercises are additional to the core programme.

## F-M01 — Establish the agent identity and data boundary

An agent has its own IAM role, context, memory, tasks and artifacts. Account-data visibility follows the configured role; another agent is not a shared-memory extension.

**Setup:** Create the agent in the console and select or create its agent role. Configure the operator web-application role and optional integrations. Review the wizard settings and verify access from the intended operator identity.

**Proposed verification:** Compare an allowed cost query with an intentionally unavailable data source. Record the agent identity and confirm the operator is not accidentally using another agent.

**Boundary:** A broad data role can expose more than the displayed report scope. Missing permissions can produce incomplete analysis.

## F-M02 — Supply maintained organization context

Uploaded context supplies owner mappings, categories, report structures and instructions. The agent reads this material but cannot edit or delete the files through chat.

**Setup:** Open Context files and upload a focused supported file. Use a new question to check the mapping or instruction. Maintain the file in the workspace when organization definitions change.

**Proposed verification:** Use a synthetic account-to-team mapping and verify a sampled attribution. Check for conflicting old context before accepting the result.

**Boundary:** Do not upload personal or sensitive information. An owner mapping is not an IAM policy.

## F-M03 — Retain and correct preferences across sessions

Memory can retain preferences, corrections and task outcomes for later sessions. This differs from an uploaded context file and from the summary of one long conversation.

**Setup:** Ask the agent to remember a specific reporting preference or correction. Start a separate conversation and check its use. Request an update or forgetting of that specific entry when it is no longer valid.

**Proposed verification:** Use a harmless synthetic reporting preference, not a secret. Test correction in a new session; retain the original data query for reconciliation.

**Boundary:** A remembered cause must be rechecked against current data. No separate model-training switch is established by these instructions.

## F-M04 — Create bounded on-demand and scheduled tasks

On-demand, scheduled and event-based work share a task queue. A task is created when requested; a normal cost question can remain an interactive answer.

**Setup:** Ask to create a task, or open Tasks → Create tasks. For recurrence, describe the schedule and output in chat. Inspect the created automation, its task history and destination before relying on it.

**Proposed verification:** Start with report generation and no Jira or Slack destination. Verify schedule interpretation, task state and artifact completeness.

**Boundary:** External publishing behavior must be reviewed separately; a task may carry more effects than a read-only report.

## F-M05 — Route cost anomaly events to an investigation

A Cost Anomaly Detection event starts a matching automation through an EventBridge managed rule. The agent then runs the configured investigation and destination action.

**Setup:** Register Slack at account level, then bind the selected channel to the agent with Add connection. In chat, specify the monitor or threshold, investigation and destination. Open Automations and inspect the COST_ANOMALY trigger, status and associated tasks.

**Proposed verification:** Use an authorized test destination and inspect the exact monitor/threshold. Trace a matching event to a task and delivery record without deliberately generating unnecessary spend.

**Boundary:** Slack delivery is not gated by per-message approval. Automatic Jira writes are pre-authorized during setup.

## F-M06 — Apply action-specific publishing controls

Interactive or on-demand Jira issue/comment actions require confirmation. Scheduled and event-based Jira actions are pre-authorized. Slack posting does not require approval, including interactive use.

**Setup:** Inspect the Jira project or Slack channel connection. For interactive Jira, review the displayed action details before confirming. For automation, review the entire publishing instruction before enabling it.

**Proposed verification:** Test interactive Jira refusal/confirmation with a disposable issue. Verify automation and Slack publishing only in approved test destinations.

**Boundary:** A prompt saying “ask first” should not be substituted for the product’s documented action controls.

## F-M07 — Separate retained data from session summarization

Long conversations can be summarized to fit the model context window. Persistent memory, files, conversation history, tasks and artifacts have different lifecycles; an ephemeral runtime does not imply ephemeral records.

**Setup:** Identify whether the unwanted item is context, memory, an artifact, a task or conversation history. Use the specific deletion, forgetting, cancellation or automation control. For categories without individual deletion during preview, evaluate whole-agent deletion with the owner.

**Proposed verification:** Check that disabled automation stops new tasks while historical tasks remain. Confirm removal behavior in a disposable agent before using it as a retention procedure.

**Boundary:** Do not equate a summary, a forgotten fact, a disabled automation and complete data removal.

## Optional use-case exercise



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

