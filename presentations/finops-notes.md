# AWS FinOps Agent — presenter reference



The schedule includes prepared-result exercises. It is not a promise of live agent completion time. Questions and breaks are additional. Canonical guide sections are reproduced in speaker notes as reference, not as a required verbatim script.



## 1. Instance configuration and task execution are separate

**Schedule:** 00:00–02:00. **Type:** flow.

Preview service; storage and inference geography must be reviewed separately.

**Display content:**

Access | Agent data role and operator entry

Context | Uploaded files, memory and conversation

Work | Automation or request creates a queued task

Output | Answer, artifact or configured external action

**Canonical reference:** [F-01](../guides/finops.html#F-01)



## 2. Four permission responsibilities are not one role

**Schedule:** 02:00–05:00. **Type:** table.

Test data access and team access independently.

**Display content:**

Responsibility | Purpose

Administrator | Create/configure service resources and permitted roles

Agent data role | Call authorized data services and manage required rules

Operator role | Supported web-app operations

User permission | Enter the configured agent as the intended person

**Canonical reference:** [F-02](../guides/finops.html#F-02)



## 3. Numerical contribution and cause are different conclusions

**Schedule:** 05:00–07:00. **Type:** table.

A nearby deployment alone does not explain the entire cost delta.

**Display content:**

Source | What it can support

Cost query | Amount for fixed dates, metric and dimensions

Anomaly record | Detected deviation under the monitor

Recommendation | Upstream candidate and assumptions

Change event | Recorded operation at a time

**Canonical reference:** [F-M01](../guides/finops.html#F-M01)



## 4. Files are reviewed reference inputs

**Schedule:** 07:00–09:00. **Type:** columns.

Everyone with access to the agent can see its context files.

**Display content:**

Preparation | Use actual account identifiers, owners and reporting basis. Keep the maintained source in Git.

Controls | Upload/soft-delete/restore in the workspace. The agent reads but does not conversationally rewrite the file.

Limits | Supported formats, 10 MB per file and total context quota matter.

**Canonical reference:** [F-M02](../guides/finops.html#F-M02)



## 5. Memory and file retrieval need different tests

**Schedule:** 09:00–11:00. **Type:** flow.

Updating memory does not establish that a reference file changed.

**Display content:**

Remember | State a harmless preference

New session | Observe its application

Correct / forget | Change the retained memory

Retest | Check separately from uploaded source files

**Canonical reference:** [F-M03](../guides/finops.html#F-M03)



## 6. Compaction summarizes a conversation, not all persistent state

**Schedule:** 11:00–12:00. **Type:** columns.

Do not infer verbatim retention or a documented hidden precedence algorithm.

**Display content:**

What changes | Older messages are summarized as the conversation context fills. Recent messages remain in full.

How to review | Restate the current cost contract and unresolved questions before another material calculation.

**Canonical reference:** [F-M04](../guides/finops.html#F-M04)



## 7. A task runs; an automation creates future tasks

**Schedule:** 12:00–14:00. **Type:** flow.

Removing an automation does not delete existing tasks or messages.

**Display content:**

Definition | Schedule or supported event condition

Task creation | A separate execution record

Shared queue | On-demand and automated work

Result | Status, source evidence and artifacts

**Canonical reference:** [F-03](../guides/finops.html#F-03)



## 8. Trace an anomaly through the complete event path

**Schedule:** 14:00–16:00. **Type:** flow.

No task and no delivered message are different failures.

**Display content:**

Monitor | Cost Anomaly Detection

Managed rule | EventBridge condition and permissions

Automation | COST_ANOMALY trigger creates task

Execution | Inspect result and destination separately

**Canonical reference:** [F-M05](../guides/finops.html#F-M05)



## 9. Integration registration precedes destination binding

**Schedule:** 16:00–18:00. **Type:** table.

Inspect connection state and the actual destination.

**Display content:**

Layer | Jira | Slack

Registration | Supported Cloud authorization | Workspace authorization

Agent connection | Selected project/space | Channel; app membership required

Boundary | No arbitrary workflow editing | One-way posting, not channel reading

**Canonical reference:** [F-05](../guides/finops.html#F-05)



## 10. Approval rules depend on effect and invocation

**Schedule:** 18:00–20:00. **Type:** table.

Schedule setup can authorize publication; review content and audience at that point.

**Display content:**

Effect | Interactive / on-demand | Automation

Jira issue or comment | Approval prompt | Pre-authorized during setup

Slack post | No approval prompt | No approval prompt

**Canonical reference:** [F-M06](../guides/finops.html#F-M06)



## 11. Stop and delete mean different things for different objects

**Schedule:** 20:00–22:00. **Type:** table.

Whole-agent deletion is not an ordinary lifecycle demonstration.

**Display content:**

Object | Control | What may remain

Context file | Soft delete / restore | Retained file content

Task | Cancel execution | Task record

Automation | Disable/delete future starts | Existing tasks

Artifact | Delete artifact | External published copies

**Canonical reference:** [F-M07](../guides/finops.html#F-M07), [F-04](../guides/finops.html#F-04)



## 12. Exercise: reconcile the 41% increase before explaining it

**Schedule:** 22:00–30:00. **Type:** demo.

Synthetic quantities and rates—not AWS prices or a measured saving.

**Display content:**

0–2 min | Check comparison contract | Two complete windows, same scope and cost basis

2–4 min | Reconcile component totals | 1,400 → 1,974; delta 574

4–6 min | Attribute arithmetic | Storage +200; requests +100; transfer +274

6–8 min | Evaluate prepared evidence | Extra export supports transfer only; other causes unresolved

**Canonical reference:** [F-U01](../guides/finops.html#F-U01)



## 13. Validate each layer rather than one fluent answer

**Schedule:** 30:00–32:00. **Type:** columns.

Complete current policies and quotas remain the authoritative linked reference.

**Display content:**

Data | Reproduce totals with identical metric, dates, filters and units.

State and execution | Test file retrieval, memory, event matching and queue status separately.

Effects | Inspect destination, approval path and retained records after a stop operation.

**Canonical reference:** [F-06](../guides/finops.html#F-06), [F-07](../guides/finops.html#F-07)


