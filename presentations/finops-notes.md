# AWS FinOps Agent — HTML presentation reference



Open [finops.html](finops.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. Instance configuration and task execution are separate

**Chapter:** Platform model. **Schedule:** 00:00–02:00. **Slide budget:** 02:00.

Preview service; storage and inference geography must be reviewed separately.



Access | Agent data role and operator entry

Context | Uploaded files, memory and conversation

Work | Automation or request creates a queued task

Output | Answer, artifact or configured external action



**Guide:** [F-01](../guides/finops.html#F-01)



## 2. Four permission responsibilities are not one role

**Chapter:** Access and source data. **Schedule:** 02:00–05:00. **Slide budget:** 03:00.

Test data access and team access independently.



Responsibility | Purpose

Administrator | Create/configure service resources and permitted roles

Agent data role | Call authorized data services and manage required rules

Operator role | Supported web-app operations

User permission | Enter the configured agent as the intended person



**Guide:** [F-02](../guides/finops.html#F-02)



## 3. Numerical contribution and cause are different conclusions

**Chapter:** Access and source data. **Schedule:** 05:00–07:00. **Slide budget:** 02:00.

A nearby deployment alone does not explain the entire cost delta.



Source | What it can support

Cost query | Amount for fixed dates, metric and dimensions

Anomaly record | Detected deviation under the monitor

Recommendation | Upstream candidate and assumptions

Change event | Recorded operation at a time



**Guide:** [F-M01](../guides/finops.html#F-M01)



## 4. Files are reviewed reference inputs

**Chapter:** Context mechanisms. **Schedule:** 07:00–09:00. **Slide budget:** 02:00.

Everyone with access to the agent can see its context files.



Preparation | Use actual account identifiers, owners and reporting basis. Keep the maintained source in Git.

Controls | Upload/soft-delete/restore in the workspace. The agent reads but does not conversationally rewrite the file.

Limits | Supported formats, 10 MB per file and total context quota matter.



**Guide:** [F-M02](../guides/finops.html#F-M02)



## 5. Memory and file retrieval need different tests

**Chapter:** Context mechanisms. **Schedule:** 09:00–11:00. **Slide budget:** 02:00.

Updating memory does not establish that a reference file changed.



Remember | State a harmless preference

New session | Observe its application

Correct / forget | Change the retained memory

Retest | Check separately from uploaded source files



**Guide:** [F-M03](../guides/finops.html#F-M03)



## 6. Compaction summarizes a conversation, not all persistent state

**Chapter:** Context mechanisms. **Schedule:** 11:00–12:00. **Slide budget:** 01:00.

Do not infer verbatim retention or a documented hidden precedence algorithm.



What changes | Older messages are summarized as the conversation context fills. Recent messages remain in full.

How to review | Restate the current cost contract and unresolved questions before another material calculation.



**Guide:** [F-M04](../guides/finops.html#F-M04)



## 7. A task runs; an automation creates future tasks

**Chapter:** Tasks, publication and lifecycle. **Schedule:** 12:00–14:00. **Slide budget:** 02:00.

Removing an automation does not delete existing tasks or messages.



Definition | Schedule or supported event condition

Task creation | A separate execution record

Shared queue | On-demand and automated work

Result | Status, source evidence and artifacts



**Guide:** [F-03](../guides/finops.html#F-03)



## 8. Trace an anomaly through the complete event path

**Chapter:** Tasks, publication and lifecycle. **Schedule:** 14:00–16:00. **Slide budget:** 02:00.

No task and no delivered message are different failures.



Monitor | Cost Anomaly Detection

Managed rule | EventBridge condition and permissions

Automation | COST_ANOMALY trigger creates task

Execution | Inspect result and destination separately



**Guide:** [F-M05](../guides/finops.html#F-M05)



## 9. Integration registration precedes destination binding

**Chapter:** Tasks, publication and lifecycle. **Schedule:** 16:00–18:00. **Slide budget:** 02:00.

Inspect connection state and the actual destination.



Layer | Jira | Slack

Registration | Supported Cloud authorization | Workspace authorization

Agent connection | Selected project/space | Channel; app membership required

Boundary | No arbitrary workflow editing | One-way posting, not channel reading



**Guide:** [F-05](../guides/finops.html#F-05)



## 10. Approval rules depend on effect and invocation

**Chapter:** Tasks, publication and lifecycle. **Schedule:** 18:00–20:00. **Slide budget:** 02:00.

Schedule setup can authorize publication; review content and audience at that point.



Effect | Interactive / on-demand | Automation

Jira issue or comment | Approval prompt | Pre-authorized during setup

Slack post | No approval prompt | No approval prompt



**Guide:** [F-M06](../guides/finops.html#F-M06)



## 11. Stop and delete mean different things for different objects

**Chapter:** Tasks, publication and lifecycle. **Schedule:** 20:00–22:00. **Slide budget:** 02:00.

Whole-agent deletion is not an ordinary lifecycle demonstration.



Object | Control | What may remain

Context file | Soft delete / restore | Retained file content

Task | Cancel execution | Task record

Automation | Disable/delete future starts | Existing tasks

Artifact | Delete artifact | External published copies



**Guide:** [F-M07](../guides/finops.html#F-M07), [F-04](../guides/finops.html#F-04)



## 12. Exercise: reconcile the 41% increase before explaining it

**Chapter:** Prepared-result exercise. **Schedule:** 22:00–30:00. **Slide budget:** 08:00.

Synthetic quantities and rates—not AWS prices or a measured saving.



0–2 min | Check comparison contract | Two complete windows, same scope and cost basis

2–4 min | Reconcile component totals | 1,400 → 1,974; delta 574

4–6 min | Attribute arithmetic | Storage +200; requests +100; transfer +274

6–8 min | Evaluate prepared evidence | Extra export supports transfer only; other causes unresolved



**Guide:** [F-U01](../guides/finops.html#F-U01)



## 13. Validate each layer rather than one fluent answer

**Chapter:** Troubleshooting and coverage. **Schedule:** 30:00–32:00. **Slide budget:** 02:00.

Complete current policies and quotas remain the authoritative linked reference.



Data | Reproduce totals with identical metric, dates, filters and units.

State and execution | Test file retrieval, memory, event matching and queue status separately.

Effects | Inspect destination, approval path and retained records after a stop operation.



**Guide:** [F-06](../guides/finops.html#F-06), [F-07](../guides/finops.html#F-07)
