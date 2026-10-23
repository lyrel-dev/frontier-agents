# AWS FinOps Agent: presentation notes



Presentation: 63 minutes, including 8 minutes of prepared-result exercises. Questions and breaks are additional.



## 01. Instance roles and destination connections

00:00–02:00 · Workspace and resource organization

The instance uses separate data-access and operator roles. Account-level Jira or Slack registration is followed by an instance-specific project or channel connection.



![FinOps Agent: instance access and integration connections](../assets/diagrams/er-finops-scope.svg)



Detailed reference: [Agent instance, access roles and retained state](../guides/finops.html#F-01)


## 02. Instance, conversation, task, and artifact identities

02:00–05:00 · Workspace and resource organization

Identify the actual product object before configuring, invoking, correcting or removing it. The resource kind determines which operation is meaningful.



Object | Identity or membership | Lifecycle distinction

Agent instance | finops-agent AgentSpace actions and agentspace ARN | Service-specific scope; not a DevOps resource

Integration / connection | Account registration / instance destination binding | Authorization and destination selection differ

Conversation / task | Interaction / separately recorded execution | A direct answer need not create a task

Automation | Rule that creates future tasks | Deleting a rule does not delete existing work

File / memory / artifact | Reference input / retained context / output | Each has its own update and removal behavior


Detailed reference: [Conversations, automations, tasks and artifacts](../guides/finops.html#F-09)


## 03. Conversations, automations, tasks and artifacts

05:00–08:00 · Workspace and resource organization

A conversation may answer directly. An explicit task has a separate queue and execution record. An automation creates future tasks. Report artifacts can originate from a conversation or task.



![FinOps Agent: conversation, automation and task records](../assets/diagrams/er-finops-work.svg)



Detailed reference: [Conversations, automations, tasks and artifacts](../guides/finops.html#F-09)


## 04. Instance settings, task instructions, and automations

08:00–11:00 · Instance configuration and task definition

The instance exposes these facilities independently. A task instruction is not a DevOps custom-agent definition.



Control | What it configures

Data role | Authorized AWS data-source operations

Operator access | Entry and web-application operations

Context files and memory | Organization-specific reference and retained preferences

Task request | Instructions for one separately recorded execution

Automation | Future task creation on schedule or supported event

Destination connection | Agent-specific Jira project or Slack channel


Detailed reference: [Instance configuration and task instructions](../guides/finops.html#F-11)



Detailed reference: [Service access, storage location, and inference](../guides/finops.html#F-12)


## 05. Files, memory and conversation-context lifecycles

11:00–13:00 · Organizational knowledge and conversation context

Soft deletion and restoration apply to files. Forgetting updates memory. Compaction changes working context; these operations are not interchangeable.



![FinOps context: three independent lifecycle operations](../assets/diagrams/mechanism-finops-context.svg)



Detailed reference: [Context-file preparation and management](../guides/finops.html#F-M02)



Detailed reference: [Persistent preferences and corrections](../guides/finops.html#F-M03)



Detailed reference: [Conversation summarization and context limits](../guides/finops.html#F-M04)


## 06. Context files, memory and conversation compaction

13:00–16:00 · Organizational knowledge and conversation context

File retrieval, cross-session memory and within-session compaction require separate tests.



Mechanism | Producer | Typical content | Lifecycle

Reference file | Operator upload | Account ownership, allocation rules and reporting standards | Upload, soft delete and restore

Conversational memory | Conversation preferences, corrections and task outcomes | Preferences, corrections and ownership details | Update or forget across sessions

Conversation context | Current interaction | Recent messages and summarized older messages | Compaction near context limit

Ephemeral runtime | Service execution | Loaded persistent context for a session | Destroyed after session

Agent-instance boundary | Agent configuration | Instance-specific files, memory and queue | No shared memory across instances


Detailed reference: [Context-file preparation and management](../guides/finops.html#F-M02)



Detailed reference: [Persistent preferences and corrections](../guides/finops.html#F-M03)



Detailed reference: [Conversation summarization and context limits](../guides/finops.html#F-M04)


## 07. Conversation actions, queued tasks, and publication approval

16:00–18:00 · Task invocation and automation

A conversation can request Jira or Slack publication directly. Explicit tasks and automations use the queue. Jira confirmation depends on invocation mode; Slack has no per-message approval.



![FinOps tasks and destination-specific authorization](../assets/diagrams/mechanism-finops-publication.svg)



Detailed reference: [Tasks, schedules, and execution history](../guides/finops.html#F-03)



Detailed reference: [Anomaly events and task creation](../guides/finops.html#F-M05)



Detailed reference: [Publication permissions and approvals](../guides/finops.html#F-M06)


## 08. Tasks, schedules and event automations

18:00–21:00 · Task invocation and automation

An automation stores the trigger and task instructions. Each created task has its own execution history and publication result.



Object | Creation path | Execution behavior | Stop control

On-demand task | User request | Enters shared task queue | Cancel running task where supported

Scheduled automation | Prompt plus schedule | Creates a task at each match | Disable or delete future starts

Event automation | Prompt plus COST_ANOMALY trigger | Managed rule creates a task for matching event | Disable/delete automation

Task record | Created by request or automation | Tracks status and result | Record remains after automation removal

Delivery result | Task invokes configured destination | Records post/issue outcome | Inspect independently from analysis result


Detailed reference: [Tasks, schedules, and execution history](../guides/finops.html#F-03)



Detailed reference: [Anomaly events and task creation](../guides/finops.html#F-M05)


## 09. Reporting, anomaly investigation and optimization

21:00–24:00 · Task invocation and automation

Reporting formats source analysis. Anomaly investigation evaluates a deviation. Recommendation review prioritizes upstream proposals; savings measurement evaluates an implemented change using comparable periods.



Operational outcome | Completion evidence | Implementation boundary

Prepare a periodic cost report | Period and cost basis remain consistent. | Configured recurring task

Investigate a cost anomaly | Affected dimensions and monetary contributions reconcile. | Native analysis with optional automation

Prioritize optimization recommendations | Original source assumptions are retained. | Native function with team review

Measure the outcome of an implemented optimization | Before and after periods are comparable. | Composed workflow


Detailed reference: [Tasks, schedules, and execution history](../guides/finops.html#F-03)



Detailed reference: [Report generation and artifact management](../guides/finops.html#F-04)



Detailed reference: [Cost queries and recommendation provenance](../guides/finops.html#F-M01)


## 10. Cost-anomaly investigation: trigger and publication controls

24:00–27:00 · Task invocation and automation

Inspect event matching, task creation, source queries, and publication as separate steps. Jira approval depends on how the action starts. Slack publication requires destination review before invocation.



Step | Feature configuration | Acceptance boundary

Create work | Explicit task or supported anomaly automation | Event matching and queued execution are separate.

Investigate | Authorized cost, anomaly and optional change evidence | Reconcile amounts; correlation is not proven cause.

Publish to Jira | Configured project and invocation type | Interactive approval differs from setup-authorized automation.

Publish to Slack | Configured channel and audience | No per-message approval prompt; review scope before invocation.


Detailed reference: [Anomaly events and task creation](../guides/finops.html#F-M05)



Detailed reference: [Cost queries and recommendation provenance](../guides/finops.html#F-M01)



Detailed reference: [Publication permissions and approvals](../guides/finops.html#F-M06)


## 11. Data-source access and collaboration connections

27:00–29:00 · Data-source and collaboration integrations

AWS source access is controlled by the agent data role. Collaboration uses account-level registration and an agent-specific destination. Successful source retrieval and successful publication are independent checks.



![Data-source access and collaboration connections](../assets/diagrams/finops-integrations.svg)



Detailed reference: [Supported data sources and publication destinations](../guides/finops.html#F-08)



Detailed reference: [Jira projects and Slack channel connections](../guides/finops.html#F-05)


## 12. Cost-data and publication connections

29:00–31:00 · Data-source and collaboration integrations

Data-role permissions control AWS evidence retrieval. Provider registration and agent connections control the available collaboration destinations.



Source or destination | Information supplied | Interpretation

Cost Explorer | Cost and usage results, forecasts, coverage | Preserve dates, metric, account scope, and grouping.

Cost Anomaly Detection | Deviation and supported event source | A trigger for investigation, not proof of cause.

Cost Optimization Hub / Compute Optimizer | Upstream recommendation and estimate | Review assumptions; estimate is not realized saving.

CloudTrail | Recorded operational changes | Temporal association requires additional causal evidence.

Jira Cloud / Slack | Supported publication actions | Destination and invocation type determine the approval behavior.


Detailed reference: [Supported data sources and publication destinations](../guides/finops.html#F-08)


## 13. Jira and Slack publication controls

31:00–33:00 · Data-source and collaboration integrations

Approval behavior depends on both the action and the invocation path.



Action | Interactive or on-demand | Scheduled or event automation | Review point

Create Jira issue | Approval prompt | Pre-authorized during setup | Project, content and owner

Add Jira comment | Approval prompt | Pre-authorized during setup | Issue and disclosure scope

Post Slack message | No approval prompt | No approval prompt | Channel and sensitive content

Register integration | Account-level authorization | Same registration reused | Provider account/workspace

Bind destination | Agent-specific project or channel | Automation uses this binding | Actual connection and app membership


Detailed reference: [Jira projects and Slack channel connections](../guides/finops.html#F-05)



Detailed reference: [Publication permissions and approvals](../guides/finops.html#F-M06)


## 14. Source interfaces, stored data, and inference location

33:00–35:00 · Service access and data location

Storage geography, inference geography, and source authorization answer different configuration questions.



Boundary | Documented property

AWS source access | Data-role permissions for the named source services

Collaboration access | Registered Jira or Slack integration and instance connection

Persistent storage | Preview data stored in us-east-1

Inference | Can use other US Regions

Private-tool networking | No DevOps VPC resource-gateway interface is asserted for this service


Detailed reference: [Service access, storage location, and inference](../guides/finops.html#F-12)


## 15. Anomaly investigation and cost driver analysis

35:00–38:00 · Managed analytical functions

Numerical contribution, correlated change and established cause are different conclusions.



Evidence source | Question answered | Typical conclusion | Limit

Cost Anomaly Detection | What deviation was detected? | Affected service, account and impact | Detection is not causal proof

Cost Explorer | Was movement usage, rate or both? | Dimensioned contribution | Depends on chosen basis and filters

CloudTrail event history | Which API activity occurred nearby? | Candidate operational change | Temporal correlation only

Workload owner evidence | Did behavior or volume change? | Service-specific explanation | May remain unavailable

Automation history | Was the event matched and processed? | Task and delivery result | Delivery failure differs from investigation failure


Detailed reference: [Cost queries and recommendation provenance](../guides/finops.html#F-M01)



Detailed reference: [Anomaly events and task creation](../guides/finops.html#F-M05)


## 16. Optimization recommendation review

38:00–40:00 · Managed analytical functions

The agent surfaces and contextualizes recommendations; it does not authorize infrastructure or financial changes.



Review element | Source | Decision question | Record

Recommendation | Cost Optimization Hub or Compute Optimizer | What action and assumptions are proposed? | Recommendation ID and source

Estimated benefit | Upstream recommendation model | Does it overlap with another candidate? | Estimate and exclusions

Operational constraint | Service owner and telemetry | What reliability, performance or recovery requirement applies? | Accepted constraint

Authorization | Normal engineering and financial process | Who approves the change or commitment? | Change or purchase record

Measurement | Post-change cost and service data | Was the expected effect observed on a comparable basis? | Measured outcome and attribution limit


Detailed reference: [Cost queries and recommendation provenance](../guides/finops.html#F-M01)


## 17. Historical cost, forecasting and commitment coverage

40:00–43:00 · Managed analytical functions

Historical analysis reports observed cost under a specified query. Forecasting estimates a future period. Commitment coverage reports the covered share of eligible usage. Retain the source and calculation basis for each.



Operational outcome | Completion evidence | Implementation boundary

Analyze historical cost and usage | Dates, metric, currency and filters are explicit. | Native function

Review a cost forecast | Forecast horizon and source are identified. | Native function

Review commitment coverage | Commitment type, period and eligible scope are explicit. | Native function


Detailed reference: [Cost queries and recommendation provenance](../guides/finops.html#F-M01)



Detailed reference: [Supported data sources and publication destinations](../guides/finops.html#F-08)


## 18. Report artifacts and data lifecycle

43:00–45:00 · Interaction surfaces and report artifacts

Stopping future work, cancelling current work and removing retained data are different operations.



Object | Create or revise | Remove or stop | What may remain

Report artifact | Generate and request revision | Delete artifact | Externally copied report

Context file | Upload and restore | Soft delete | Retained recoverable content

Memory item | Remember or update | Forget | Independent file or conversation text

Task | Request or automation | Cancel execution | Task record and published output

Automation | Schedule or event trigger | Disable or delete | Previously created tasks

Agent instance | Create and configure | Delete whole instance | External artifacts and destinations


Detailed reference: [Report generation and artifact management](../guides/finops.html#F-04)



Detailed reference: [Retention, cancellation, and deletion](../guides/finops.html#F-M07)


## 19. Conversations, task history, and report artifacts

45:00–47:00 · Interaction surfaces and report artifacts

Not every answer is a task, and not every artifact has a task as its parent. A report revision must retain its intended analytical basis.



Workspace | Purpose

Conversation | Immediate analytical interaction

Tasks | Separately queued work and its results

Automations | Rules that create future tasks

Context files | Uploaded organizational reference material

Artifacts | Generated reports, including conversation-originated reports


Detailed reference: [Conversation, task history, and artifact interfaces](../guides/finops.html#F-15)


## 20. Access roles and source dependencies

47:00–50:00 · Administration, retention, and limits

Data access and team access should be tested independently and with known expected results.



Responsibility | Purpose | Source dependency | Acceptance test

Administrator permission | Create agent and permitted roles | Service setup APIs | Configured instance exists

Agent data role | Read cost, recommendation and event sources | Cost Explorer, CloudTrail and optimization services | Known query and source provenance

Operator role | Use supported web-app operations | Agent web application | Intended operator performs task

User permission | Enter the specific agent | Identity Center or IAM access | Non-admin user signs in

Event-rule permission | Manage service-owned matching rule | EventBridge and anomaly monitor | Automation and managed rule visible


Detailed reference: [Administrator, service, and operator permissions](../guides/finops.html#F-02)



Detailed reference: [Cost queries and recommendation provenance](../guides/finops.html#F-M01)


## 21. Troubleshooting matrix and preview limits

50:00–52:00 · Administration, retention, and limits

Validate data, retained context, execution and external effects as separate layers.



Symptom | First object to inspect | Second check | Interpretation

Total differs | Metric, dates, filters and dimensions | Accessible source and currency | Query contract failure

Context ignored | File state or memory item | New session and exact preference | Retrieval/retention failure

Automation did not run | Trigger, status and last-triggered time | Managed rule and event condition | Event matching failure

Task ran, no message | Task result | Destination connection and action result | Publication failure

Unexpected write | Action and invocation approval rule | Destination and automation setup | Control-model misunderstanding


Detailed reference: [Data, task, and integration failures](../guides/finops.html#F-06)



Detailed reference: [Documentation coverage and references](../guides/finops.html#F-07)


## 22. Retained context and session-local execution

52:00–55:00 · Worked example and reference material

Files, retained preferences, and conversation summaries supply different context. File restoration, memory correction, and conversation compaction operate on different state.



![FinOps Agent: retained inputs and session context](../assets/diagrams/er-finops-context.svg)



Detailed reference: [Context and evidence in reporting and anomaly use cases](../guides/finops.html#F-10)


## 23. Worked example: cost increase decomposition

55:00–63:00 · Worked example and reference material

Prepared quantities and rates demonstrate reconciliation, not AWS pricing or realized savings.



0–2 min | Confirm comparison contract | Two complete windows, same scope, metric, currency and basis

2–4 min | Reconcile totals | 1,400 baseline; 1,974 comparison; delta 574

4–6 min | Attribute arithmetic | Storage +200; requests +100; transfer +274

6–8 min | Assess causal evidence | Prepared export evidence supports transfer only; storage and request causes remain unresolved


Detailed reference: [Cost-variance analysis: worked example](../guides/finops.html#F-U01)
