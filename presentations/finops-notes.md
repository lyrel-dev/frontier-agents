# AWS FinOps Agent — HTML presentation reference



Open [finops.html](finops.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. Product Functions and Agent Instance Resource Model

**Chapter:** Part I · Product Model. **Schedule:** 00:00–03:00. **Slide budget:** 03:00.

Agent configuration, source evidence, queued work and publication effects are separate layers.



Layer | Primary objects | Purpose | Evidence

Access | Administrator, agent role, operator role and user permission | Separate configuration, data and daily-use authority | Role ARN, policy and successful sign-in

Context | Reference files, memory and conversation | Supply organizational facts and preferences | File state, remembered item and current conversation

Work | On-demand task, schedule or event automation | Create queued execution | Task and automation records

Data sources | Cost, recommendation, anomaly and change APIs | Supply source evidence | Query filters and source provenance

Outputs | Answer, report artifact, Jira issue or Slack post | Deliver reviewable result | Artifact and destination history



**Guide:** [F-01](../guides/finops.html#F-01)



## 2. FinOps Use Case Taxonomy and Delivery Modes

**Chapter:** Part II · Use Case Catalog. **Schedule:** 03:00–05:00. **Slide budget:** 02:00.

The catalog separates analytical functions from scheduled execution and external publication.



Use case family | Representative work | Delivery | Primary control

Cost inquiry | Breakdowns, comparisons, trends and forecasts | Conversational native function | Query contract and source permissions

Anomaly and optimization | Root-cause analysis and recommendation triage | Native function using upstream services | Source provenance and operational review

Recurring reporting | Daily, weekly, monthly and operational review packs | Scheduled task and report artifact | Schedule, audience and report basis

Event automation | Investigate matching anomaly and publish result | Cost Anomaly Detection plus managed rule | Automation condition and destination

Collaboration | Jira follow-up and Slack publication | Configured integration | Action- and invocation-specific approval



**Guide:** [F-01](../guides/finops.html#F-01), [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04), [F-05](../guides/finops.html#F-05)



## 3. Cost Inquiry and Reporting Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 05:00–08:00. **Slide budget:** 03:00.

A usable report begins with a reproducible cost-query definition.



Use case | Required query contract | Output | Independent check

Cost breakdown | Dates, metric, currency, accounts and dimension | Service/account/Region/tag totals | Reproduce a material total

Period comparison | Complete comparable windows and same cost basis | Delta and ranked contributors | Check arithmetic and filters

Forecast review | Forecast horizon and source assumptions | Forecast and uncertainty | Separate forecast from observed spend

Commitment coverage review | Relevant commitment and utilization scope | Coverage and candidate gaps | Inspect source recommendation

Custom report | Audience, sections, figures and source basis | HTML, PDF or editable presentation artifact | Reconcile displayed values



**Guide:** [F-M01](../guides/finops.html#F-M01), [F-04](../guides/finops.html#F-04)



## 4. Anomaly Investigation and Cost Driver Analysis

**Chapter:** Part II · Use Case Catalog. **Schedule:** 08:00–11:00. **Slide budget:** 03:00.

Numerical contribution, correlated change and established cause are different conclusions.



Evidence source | Question answered | Typical conclusion | Limit

Cost Anomaly Detection | What deviation was detected? | Affected service, account and impact | Detection is not causal proof

Cost Explorer | Was movement usage, rate or both? | Dimensioned contribution | Depends on chosen basis and filters

CloudTrail event history | Which API activity occurred nearby? | Candidate operational change | Temporal correlation only

Workload owner evidence | Did behavior or volume change? | Service-specific explanation | May remain unavailable

Automation history | Was the event matched and processed? | Task and delivery result | Delivery failure differs from investigation failure



**Guide:** [F-M01](../guides/finops.html#F-M01), [F-M05](../guides/finops.html#F-M05)



## 5. Optimization Recommendation Review

**Chapter:** Part II · Use Case Catalog. **Schedule:** 11:00–13:00. **Slide budget:** 02:00.

The agent surfaces and contextualizes recommendations; it does not authorize infrastructure or financial changes.



Review element | Source | Decision question | Record

Recommendation | Cost Optimization Hub or Compute Optimizer | What action and assumptions are proposed? | Recommendation ID and source

Estimated benefit | Upstream recommendation model | Does it overlap with another candidate? | Estimate and exclusions

Operational constraint | Service owner and telemetry | What reliability, performance or recovery requirement applies? | Accepted constraint

Authorization | Normal engineering and financial process | Who approves the change or commitment? | Change or purchase record

Measurement | Post-change cost and service data | Was the expected effect observed on a comparable basis? | Measured outcome and attribution limit



**Guide:** [F-M01](../guides/finops.html#F-M01)



## 6. Recurring Reports and Operational Reviews

**Chapter:** Part II · Use Case Catalog. **Schedule:** 13:00–16:00. **Slide budget:** 03:00.

Report cadence, source window, audience and ownership should be configured explicitly.



Use case | Cadence | Core content | Audience

Daily cost pulse | Daily | Material movement, anomaly status and unresolved gaps | FinOps operations

Weekly service report | Weekly | Cost by service, owner, driver and recommendation status | Engineering and FinOps owners

Monthly management report | Monthly | Trend, forecast, commitment and actions | Leadership and finance

FinOps operational review | Weekly or monthly | Decisions, owners, rejected items and measured outcomes | Cross-functional review

Optimization backlog report | Scheduled | Candidate, source, estimated benefit, constraint and status | Platform and workload owners



**Guide:** [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04)



## 7. Context Files, Memory and Conversation Compaction

**Chapter:** Part III · Context and Automation. **Schedule:** 16:00–19:00. **Slide budget:** 03:00.

File retrieval, cross-session memory and within-session compaction require separate tests.



Mechanism | Producer | Typical content | Lifecycle

Reference file | Operator upload | Account ownership, allocation rules and reporting standards | Upload, soft delete and restore

Conversational memory | Explicit remember/update/forget request | Preferences, corrections and ownership details | Update or forget across sessions

Conversation context | Current interaction | Recent messages and summarized older messages | Compaction near context limit

Ephemeral runtime | Service execution | Loaded persistent context for a session | Destroyed after session

Agent-instance boundary | Agent configuration | Instance-specific files, memory and queue | No shared memory across instances



**Guide:** [F-M02](../guides/finops.html#F-M02), [F-M03](../guides/finops.html#F-M03), [F-M04](../guides/finops.html#F-M04)



## 8. Tasks, Schedules and Event Automations

**Chapter:** Part III · Context and Automation. **Schedule:** 19:00–22:00. **Slide budget:** 03:00.

An automation is a task factory; it is not the task or the external message.



Object | Creation path | Execution behavior | Stop control

On-demand task | User request | Enters shared task queue | Cancel running task where supported

Scheduled automation | Prompt plus schedule | Creates a task at each match | Disable or delete future starts

Event automation | Prompt plus COST_ANOMALY trigger | Managed rule creates a task for matching event | Disable/delete automation

Task record | Created by request or automation | Tracks status and result | Record remains after automation removal

Delivery result | Task invokes configured destination | Records post/issue outcome | Inspect independently from analysis result



**Guide:** [F-03](../guides/finops.html#F-03), [F-M05](../guides/finops.html#F-M05)



## 9. Jira and Slack Publication Controls

**Chapter:** Part III · Context and Automation. **Schedule:** 22:00–24:00. **Slide budget:** 02:00.

Approval behavior depends on both the action and the invocation path.



Action | Interactive or on-demand | Scheduled or event automation | Review point

Create Jira issue | Approval prompt | Pre-authorized during setup | Project, content and owner

Add Jira comment | Approval prompt | Pre-authorized during setup | Issue and disclosure scope

Post Slack message | No approval prompt | No approval prompt | Channel and sensitive content

Register integration | Account-level authorization | Same registration reused | Provider account/workspace

Bind destination | Agent-specific project or channel | Automation uses this binding | Actual connection and app membership



**Guide:** [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06)



## 10. Report Artifacts and Data Lifecycle

**Chapter:** Part III · Context and Automation. **Schedule:** 24:00–26:00. **Slide budget:** 02:00.

Stopping future work, cancelling current work and removing retained data are different operations.



Object | Create or revise | Remove or stop | What may remain

Report artifact | Generate and request revision | Delete artifact | Externally copied report

Context file | Upload and restore | Soft delete | Retained recoverable content

Memory item | Remember or update | Forget | Independent file or conversation text

Task | Request or automation | Cancel execution | Task record and published output

Automation | Schedule or event trigger | Disable or delete | Previously created tasks

Agent instance | Create and configure | Delete whole instance | External artifacts and destinations



**Guide:** [F-04](../guides/finops.html#F-04), [F-M07](../guides/finops.html#F-M07)



## 11. Access Roles and Source Dependencies

**Chapter:** Part IV · Access and Source Dependencies. **Schedule:** 26:00–29:00. **Slide budget:** 03:00.

Data access and team access should be tested independently and with known expected results.



Responsibility | Purpose | Source dependency | Acceptance test

Administrator permission | Create agent and permitted roles | Service setup APIs | Configured instance exists

Agent data role | Read cost, recommendation and event sources | Cost Explorer, CloudTrail and optimization services | Known query and source provenance

Operator role | Use supported web-app operations | Agent web application | Intended operator performs task

User permission | Enter the specific agent | Identity Center or IAM access | Non-admin user signs in

Event-rule permission | Manage service-owned matching rule | EventBridge and anomaly monitor | Automation and managed rule visible



**Guide:** [F-02](../guides/finops.html#F-02), [F-M01](../guides/finops.html#F-M01)



## 12. Worked Example: Cost Increase Decomposition

**Chapter:** Part V · Worked Example. **Schedule:** 29:00–37:00. **Slide budget:** 08:00.

Prepared quantities and rates demonstrate reconciliation, not AWS pricing or realized savings.



0–2 min | Confirm comparison contract | Two complete windows, same scope, metric, currency and basis

2–4 min | Reconcile totals | 1,400 baseline; 1,974 comparison; delta 574

4–6 min | Attribute arithmetic | Storage +200; requests +100; transfer +274

6–8 min | Assess causal evidence | Prepared export evidence supports transfer only; storage and request causes remain unresolved



**Guide:** [F-U01](../guides/finops.html#F-U01)



## 13. Troubleshooting Matrix and Preview Limits

**Chapter:** Part VI · Troubleshooting. **Schedule:** 37:00–39:00. **Slide budget:** 02:00.

Validate data, retained context, execution and external effects as separate layers.



Symptom | First object to inspect | Second check | Interpretation

Total differs | Metric, dates, filters and dimensions | Accessible source and currency | Query contract failure

Context ignored | File state or memory item | New session and exact preference | Retrieval/retention failure

Automation did not run | Trigger, status and last-triggered time | Managed rule and event condition | Event matching failure

Task ran, no message | Task result | Destination connection and action result | Publication failure

Unexpected write | Action and invocation approval rule | Destination and automation setup | Control-model misunderstanding



**Guide:** [F-06](../guides/finops.html#F-06), [F-07](../guides/finops.html#F-07)
