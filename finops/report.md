# AWS FinOps Agent

Cost-data access, investigation, recommendation retrieval and reporting

Reviewed: 2026-10-21

A technical reference for cloud-cost engineers and application owners. The agent is an interface over billing and optimization services, with its own tasks, context and publishing actions. It does not become the source of billing truth, independently generate every optimization recommendation, or execute infrastructure rightsizing.

## Availability

The whole service is in preview. The cited guidance places the agent and stored data in us-east-1 and permits inference processing within the US geography. Storage location, inference location and the regions of analyzed resources are different concepts.

Official documentation: [What is AWS FinOps Agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html) · [Storage and cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)


## Product objects

### Agent instance

An independently configured instance with its own IAM access, conversations, context, memory, tasks and artifacts. Registering an integration at account level does not share these contents between agents.

Official documentation: [Creating an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)


### Query scope

The accounts, time range, granularity, cost metric, currency and dimension filters used for a billing request. Two answers cannot be reconciled until these inputs match.

Official documentation: [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


### Task and automation

A task is one execution with instructions, activities, state and outputs. An automation defines a schedule or event trigger that creates tasks; cancelling one task does not disable the automation.

Official documentation: [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


### Context file and memory

A file supplied by a user is read-only to the agent and can define owners or reporting rules. Memory retains preferences or corrections. Neither changes source billing records or IAM scope.

Official documentation: [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)


### Integration and connection

OAuth registration is account-level; the agent-level connection selects a particular Jira project or Slack channel. An installed app alone does not establish a valid destination for a task.

Official documentation: [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)


## Product functions

### Billing-data inquiry

Retrieve measured spend, predictions and commitment metrics without confusing their meanings.

#### F01 — Retrieve and group historical costs and usage

Availability: Preview. Activation: See invocation and prerequisites.

The agent queries Cost Explorer and related permitted billing tools, then presents the selected data as totals and breakdowns. It can translate a natural-language request into source queries, but the underlying billing services remain the authority for the amounts.

**Input.** A billing question with account scope, period, granularity, cost metric and requested dimensions such as service, region or tag.

**Output.** A scoped cost or usage result, often with a table or chart. Missing permissions can make a source unavailable; that is not equivalent to zero spend.

**Invocation and prerequisites.** Ask in Chat for a specific interval and breakdown. Inspect the query/tool activity and restate the chosen scope in any resulting report.

**Limitations and effects.** Different cost metrics, date boundaries, currencies or filters can produce different totals. Tags and owner mappings do not guarantee that all spend is attributable.

**Proposed operator verification — not executed.** Reconcile the aggregate and at least one material group against Cost Explorer with identical settings. Require an explicit unallocated or unknown category rather than silently excluding unmatched accounts.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


#### F02 — Retrieve a cost forecast

Availability: Preview. Activation: See invocation and prerequisites.

The agent exposes forecasting data available from Cost Explorer. A forecast is a modeled estimate for a future interval, not a bill or a measured saving. The report must retain the forecast's horizon and source assumptions rather than presenting a single number as a guaranteed outcome.

**Input.** The account and cost scope, forecast horizon and requested comparison with measured spend.

**Output.** Forecast values and available uncertainty information from the underlying source, distinct from actual cost observations.

**Invocation and prerequisites.** Request the forecast for the named scope and period in Chat, then inspect the source response and how it is represented in a chart or report.

**Limitations and effects.** A forecast does not authorize a budget or a commitment purchase. A changed workload can make a historical pattern a poor guide to the next period.

**Proposed operator verification — not executed.** Label actuals and forecast separately; verify the boundary between completed and future periods. Do not manufacture an uncertainty range when the returned source result does not supply one.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


#### F03 — Inspect commitment coverage, utilization and purchase recommendations

Availability: Preview. Activation: See invocation and prerequisites.

The agent retrieves commitment-related data available through the permitted billing tools. Coverage asks how much eligible usage is covered; utilization asks how much purchased commitment was used. A purchase recommendation is a separate proposed financial decision based on the source service's assumptions.

**Input.** The relevant Savings Plans or Reserved Instances scope and period, plus the requested coverage, utilization or recommendation view.

**Output.** Source-derived commitment metrics or recommendation details. The guide does not equate a low coverage number with a requirement to buy more commitment.

**Invocation and prerequisites.** State which metric is required and request its scope and period with the answer. Review purchase recommendations separately from historical coverage and utilization.

**Limitations and effects.** The same purchase can increase coverage while creating underutilization if demand falls. The agent's answer is not a purchase execution or proof that future usage will match the assumed baseline.

**Proposed operator verification — not executed.** Have the responsible cost owner verify commitment term, payment option, eligible usage and demand assumptions in the source tool before any purchase process proceeds.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)


### Change and anomaly investigation

Explain a selected comparison or a detector-generated event while preserving uncertainty about cause.

#### F04 — Compare periods and investigate cost drivers

Availability: Preview. Activation: See invocation and prerequisites.

The agent retrieves scoped data and investigates which dimensions account for a cost change. Usage quantity, effective rate, resource mix and billing adjustments are different candidate explanations. A percentage increase in an aggregate is not itself a cause.

**Input.** Two explicitly comparable periods and the service/account/region or usage-type breakdown needed to explain their difference.

**Output.** A comparison and candidate drivers linked to the retrieved data. A defensible analysis retains an unexplained residual when available dimensions cannot reconcile the full difference.

**Invocation and prerequisites.** Ask for the absolute and relative change, the contribution of each returned dimension and the remaining unexplained amount. Request usage and rate evidence before attributing the change to either.

**Limitations and effects.** Unequal periods, cost-basis changes and incomplete attribution can create misleading comparisons. A cost increase near a deployment is temporal correlation until the relevant resource or usage effect is shown.

**Proposed operator verification — not executed.** Recalculate totals and contributions independently. If quantity/rate fields are unavailable, report that the split cannot be established instead of inferring it from total cost alone.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


#### F05 — Investigate a Cost Anomaly Detection event

Availability: Preview. Activation: See invocation and prerequisites.

The agent retrieves anomaly details, ranks contributing dimensions and investigates likely drivers. It can correlate cost data with CloudTrail activity when permitted. Detection originates in AWS Cost Anomaly Detection; the agent does not replace the monitor or guarantee the causal explanation.

**Input.** An existing cost anomaly or a matching detector event, the monitor identity and accessible billing evidence; CloudTrail access is optional supporting context.

**Output.** An investigation linked to the anomaly, affected scope and candidate causes, with task history when run asynchronously.

**Invocation and prerequisites.** Request analysis of a specific anomaly, or configure a cost-anomaly event automation for selected monitors and thresholds.

**Limitations and effects.** An absent or inaccessible CloudTrail event cannot prove that no change occurred. A correlated API event does not by itself prove that it produced the measured cost.

**Proposed operator verification — not executed.** Validate the anomaly's scope and compare the suspected change with the actual resource and usage increase. Preserve counter-evidence and indicate which causal links remain unconfirmed.

Official documentation: [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html) · [Event-triggered anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


### Optimization-recommendation access

Retrieve and contextualize recommendations generated by the underlying optimization services.

#### F06 — Retrieve and filter source-service optimization recommendations

Availability: Preview. Activation: See invocation and prerequisites.

The agent summarizes and contextualizes recommendations produced by those underlying services. It can filter and rank candidates and present current versus proposed configuration and implementation guidance. It does not generate its own independent optimization analysis or perform the resource change.

**Input.** Permitted Cost Optimization Hub and Compute Optimizer recommendation data, filtered by account, region, service, action type, effort or estimated savings.

**Output.** A shortlist of source recommendations with estimated savings, implementation considerations and source context. Rightsizing, idle-resource and commitment items are recommendation categories, not separate agent optimization engines.

**Invocation and prerequisites.** Ask for a specific recommendation scope and the original recommendation identifiers. Inspect source-service enrollment, data availability and permissions when expected items are missing.

**Limitations and effects.** Savings are estimates, not realized reductions. Alternative recommendations may overlap; summing them can double-count benefits. Performance, resilience and licensing constraints require owner review.

**Proposed operator verification — not executed.** Open the source recommendation, check its freshness and assumptions, identify mutually exclusive alternatives, and obtain workload-owner evidence before raising a change.

Official documentation: [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


### Reports and task execution

Create reviewable artifacts and manage discrete asynchronous work.

#### F07 — Generate and revise cost-report artifacts

Availability: Preview. Activation: See invocation and prerequisites.

The agent constructs a report with narrative, tables and charts from the retrieved cost or anomaly data. HTML is the documented default, with PDF and editable PowerPoint outputs also supported. A later request can revise an artifact; presentation formatting does not increase the evidential strength of its numbers.

**Input.** A defined report scope, source data, audience, layout instructions and optionally a reviewed template or organization context.

**Output.** A downloadable artifact associated with its originating task or conversation.

**Invocation and prerequisites.** Specify the period, metric, dimensions, required reconciliation table and output format. Inspect the resulting file in Artifacts and its source task before distributing it.

**Limitations and effects.** Charts can omit dimensions, mislabel periods or represent incomplete data. A professional-looking artifact is not an independently validated financial record.

**Proposed operator verification — not executed.** Reconcile every headline total, verify axes and units, and show the query scope and data cutoff in the report. Keep estimated savings and forecasts visibly separate from actuals.

Official documentation: [Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html) · [Web application and feedback](https://docs.aws.amazon.com/finops-agent/latest/userguide/how-do-i-interact-with-the-agent.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


#### F08 — Execute and inspect an asynchronous task

Availability: Preview. Activation: See invocation and prerequisites.

The service runs the task through its task queue while the conversation can continue. Task details expose instructions, activities, artifacts and state. Ordinary Chat requests remain conversational unless task creation is requested; an automation is the reusable trigger, not the individual run.

**Input.** Explicit instructions to create a task, or a scheduled/event automation that instantiates one.

**Output.** A task record with execution activity, status and any artifacts or publishing results.

**Invocation and prerequisites.** Ask Chat to create a task or use Tasks → Create tasks. Inspect the task detail page and any pending approvals; cancel a running task there when required.

**Limitations and effects.** Cancelling a task does not disable future scheduled runs. Deleting an automation does not delete prior task records. A finished task can still contain incomplete analysis that needs review.

**Proposed operator verification — not executed.** Trace one report or published message back to its task instructions and activity. Confirm that the task's time range was resolved as intended rather than carrying a stale interval from an earlier run.

Official documentation: [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html) · [Web application and feedback](https://docs.aws.amazon.com/finops-agent/latest/userguide/how-do-i-interact-with-the-agent.html) · [Data protection and deletion lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)


### External publishing

Treat Jira and Slack actions as destination-specific writes with different approval behavior.

#### F09 — Create a Jira issue in a connected project

Availability: Preview. Activation: See invocation and prerequisites.

The agent creates an issue in the selected project. Interactive and on-demand task creation requires approval; scheduled or event-based automation can pre-authorize this action at setup. Project routing does not include changing an assignee, priority or workflow status.

**Input.** A connected Jira Cloud project and proposed summary/description containing an anomaly or recommendation.

**Output.** A Jira issue and link to the originating agent task. Assignment and priority come from Jira project configuration rather than an owner-map command to the agent.

**Invocation and prerequisites.** Register the Jira integration, add the agent's project connection, then request the issue and inspect project, summary and description before approving an interactive action.

**Limitations and effects.** Jira Cloud only in the cited guidance. The agent cannot update issue fields, delete issues or administer workflows. A recommendation written into a ticket remains an unimplemented proposal.

**Proposed operator verification — not executed.** Use a test project to verify destination, default assignment and evidence links. Reject any claim that a named engineer was assigned unless Jira itself records that action.

Official documentation: [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) · [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


#### F10 — Read Jira issue state and append follow-up comments

Availability: Preview. Activation: See invocation and prerequisites.

The agent can read issue metadata to follow disposition and append a comment with updated analysis. Comment addition follows the same interactive versus pre-authorized automation distinction as issue creation. Reading a status is not authority to transition it.

**Input.** An accessible issue in a connected project, such as an issue created for a previous anomaly or recommendation.

**Output.** Retrieved issue metadata or a new comment linked to the ongoing task context.

**Invocation and prerequisites.** Specify the exact issue key and the proposed comment content. Inspect the approval for interactive or on-demand writes and the task history for automated writes.

**Limitations and effects.** The documented integration describes follow-up comments on issues the agent previously created. Do not generalize it into unrestricted project editing or automatic remediation-state transitions.

**Proposed operator verification — not executed.** Confirm the issue key, project connection and previous task relationship. Compare the actual Jira comment with the approved or pre-authorized content and avoid duplicate updates.

Official documentation: [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


#### F11 — Post results and artifacts to a connected Slack channel

Availability: Preview. Activation: See invocation and prerequisites.

The agent posts messages and artifacts to connected channels. During preview this is one-way: it does not read messages, accept commands, respond to mentions or continue a thread. Posting does not request per-message approval, even from an interactive task.

**Input.** An agent-level Slack channel connection and the result or supported artifact to publish.

**Output.** A Slack message or uploaded artifact with source context and task linkage.

**Invocation and prerequisites.** Register the workspace integration, add the app to the intended channel, create that channel's agent connection, then explicitly select the destination in the task or automation.

**Limitations and effects.** The agent cannot edit/delete the post or manage channel membership. A connected channel can expose cost data to a broader audience; a pending Jira approval does not hold back a separate Slack post.

**Proposed operator verification — not executed.** Test with non-sensitive content and verify audience, channel ID, artifact and source link. Restrict connections before creating unattended publishing workflows.

Official documentation: [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## Configuration mechanisms

### FM1 — Configure source access, operator access and publishing connections separately

The agent role reads the configured AWS data and supports required integrations; the operator role supports the web application. A user's access to the web application does not by itself prove the agent can query every desired billing source. OAuth registration and per-agent destination connections are additional boundaries.

1. In the creation wizard, choose or create the agent role and operator role. The official setup guide defines separate policies; both service roles trust finops-agent.amazonaws.com.
2. Enable and authorize the billing/optimization sources required for the intended functions. Verify Cost Explorer, Cost Anomaly Detection and source recommendation availability independently.
3. Sign in as the intended operator and test a minimal permitted query. Record the account scope and sources that are unavailable.
4. Register Jira or Slack at account level only when needed, then create agent-level connections for specific projects or channels. Do not infer a working destination from a registered integration alone.

**Lifecycle.** Each agent has isolated content and task data, although account-level integrations can be reused. Disconnecting a destination and deleting the agent are separate operations.

**Proposed verification.** Proposed check: verify one permitted query and one intentionally out-of-scope query; inspect actual role/tool errors. Validate a non-sensitive publishing action in a dedicated destination.

Official documentation: [Creating an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html) · [Setup and role policies](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html) · [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html) · [Data protection and deletion lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)


### FM2 — Use organization context and retained preferences without changing source facts

Context files supply account-owner mappings, category definitions and report rules. The agent reads these files but cannot edit them in conversation. Memory can retain preferences and corrections across sessions; long-conversation summarization is a separate context-management mechanism. Neither modifies Cost Explorer or proves that a previous causal conclusion was correct.

1. Upload a small reviewed account-owner mapping in Context files, with effective date and an explicit unknown-owner policy. Do not include sensitive personal data; users with access to the agent can see its context.
2. Ask Chat to remember a specific reporting preference or correction. Keep a record of the intended rule outside the agent as well.
3. Run a new session and inspect whether the requested attribution and report convention are applied. Check contradictory or stale mappings before assuming memory is authoritative.
4. Use Context files to soft-delete or restore uploaded content; ask Chat to forget a memory item. Do not expect deleting a context file to erase conversations or task records.

**Lifecycle.** Context files and memory are per-agent. Conversations and task records cannot be individually deleted during the documented preview; deleting an automation stops future runs but preserves prior tasks. Removing all interaction data requires deleting the agent after disconnecting integrations.

**Proposed verification.** Proposed check: include one mapped and one unmapped account, then correct the mapping and test a new session. Verify both attribution and totals; an owner label must not change the measured amount.

Official documentation: [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html) · [Data protection and deletion lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html) · [Web application and feedback](https://docs.aws.amazon.com/finops-agent/latest/userguide/how-do-i-interact-with-the-agent.html)


### FM3 — Configure recurring and anomaly-event automations

An automation stores the trigger and instructions and creates a new task for each matching occurrence. A scheduled report and an anomaly investigation use the same task facility but different trigger semantics. The current event mechanism is cost-anomaly-specific, not a general subscription to any AWS event.

1. First execute the intended instructions as an on-demand task and validate its scope, incomplete-data behavior and output.
2. For a recurring workflow, define the schedule in Chat and inspect the resulting automation's schedule, enabled state and resolved time basis in Automations.
3. For an anomaly workflow, select an existing Cost Anomaly Detection monitor, qualifying conditions and the required response. The service provisions an EventBridge managed rule; its role must allow the documented event configuration.
4. Connect the intended Slack channel before using the documented anomaly-to-Slack workflow. Review any automatic Jira creation as pre-authorization, not as a future approval prompt.
5. Inspect last-triggered time, task history and destination delivery. Disable the automation to stop future runs; cancel already-running tasks separately.

**Lifecycle.** A trigger arriving does not guarantee a complete analysis or successful publication. Expired OAuth credentials, missing sources and invalid destinations are task failures that require ownership.

**Proposed verification.** Proposed check: use a controlled permitted event or a prepared event record; verify monitor matching and task creation. Do not manufacture a billing anomaly and claim the live detector was tested.

Official documentation: [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html) · [Event-triggered anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) · [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)


### FM4 — Apply action-specific approval and data-location controls

Read-only queries and report generation do not require approval. Jira creation/comments require approval for interactive and on-demand work, but not when pre-authorized in a schedule or event automation. Slack posting requires no per-message approval. These controls do not grant permission to resize infrastructure or purchase commitments.

1. Before deployment, evaluate us-east-1 storage and US-geography inference against the organization's requirements; do not confuse workload region with agent-data location.
2. Inventory each external write in the task: issue creation, comment addition and Slack posting. Record the destination and whether setup pre-authorizes unattended execution.
3. Restrict connections to approved destinations. Keep an analysis-only task separate from a publishing task during initial validation.
4. Review task history for actual tool calls and publish results. Treat a generated draft, an approved action and a delivered external message as distinct states.

**Lifecycle.** Changing automation instructions or destination connections can change future effects. Cancelling or deleting one object does not undo a message already posted or an issue already created.

**Proposed verification.** Proposed check: reject a proposed Jira action and confirm no issue/comment appears; test Slack separately with non-sensitive content because it does not wait for the same gate.

Official documentation: [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) · [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html) · [Storage and cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html) · [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)


## Proposed operational procedures

### FU1 — Explain a cost increase without inventing a cause

Reconcile a selected cost delta and distinguish measured contributors from unconfirmed explanations.

**Use when:** An application owner reports higher spend or a detector identifies an anomaly in a known account/service scope.

**Not for:** Inferring a deployment's effect from temporal coincidence, comparing unequal billing scopes, or assigning a usage/rate split when the underlying fields are missing.

**Functions used:** F01, F04, F05, F07

**Inputs**

- Baseline and comparison intervals of known length; same cost metric, currency, accounts and filters.
- Totals plus a breakdown sufficient to reconcile the change; quantities and effective rates when a usage/rate explanation is required.
- Anomaly ID and monitor if applicable; deployment/resource events as optional causal evidence.
- Data cutoff, known credits/adjustments and an owner for unexplained residuals.

1. **Cost engineer — Lock the comparison contract.** Write the two periods and scope before querying. If the reported dashboard used a different metric or filter, reproduce that view first.

2. **Agent and engineer — Reconcile the difference.** Retrieve totals and contributors; recalculate absolute and percentage changes. Require the dimension contributions plus residual to equal the total difference.

3. **Engineer — Separate arithmetic from causality.** Where quantity and rate exist, explain the chosen decomposition convention. Where they do not, label the driver unresolved. Do not use a smooth chart as evidence.

4. **Agent and owner — Test a candidate operational cause.** Correlate any CloudTrail or deployment event with the specific resource and changed usage. Seek a counterexample, such as increased cost preceding the change.

5. **Cost engineer — Publish a bounded conclusion.** Report reconciled totals, supported contributors, uncertain causes and next required evidence. Review the artifact before choosing a publishing action.

**Acceptance:** The total delta reconciles to explained components plus residual, and every causal claim points to more than temporal coincidence. The report states the exact scope and cutoff.

**Stop:** Stop comparison if period, currency or cost basis cannot be matched. Stop driver attribution if the supporting quantity, rate or resource evidence is absent.

**Example instruction**

```text
Compare <baseline> and <current> using <metric/currency/account filters>. Reconcile the absolute delta by <dimensions> and retain any residual. Distinguish quantity, rate and mix only where source data supports the split. Treat correlated events as hypotheses. Do not publish externally or modify resources.
```

**Demonstration allocation:** 5 minutes.

- 1 min: Show the comparison contract and clearly labeled synthetic input table.
- 1 min: Recalculate baseline/current totals and the absolute and percentage delta.
- 1 min: Compute a quantity/rate decomposition and state its convention.
- 1 min: Contrast the arithmetic with the additional evidence needed for a deployment-cause claim.
- 1 min: Inspect a prepared report for scope, residual and uncertainty labels.

**Fallback:** Use the supplied arithmetic fixture. It demonstrates reconciliation only; it is not AWS billing data, service pricing or a live agent result.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


### FU2 — Turn one optimization recommendation into reviewable engineering work

Select a feasible source recommendation and create a bounded work item without claiming that savings are realized or that infrastructure was changed.

**Use when:** Cost Optimization Hub or Compute Optimizer has a current recommendation for a resource with an accountable owner.

**Not for:** Summing mutually exclusive alternatives, applying rightsizing without workload evidence, or expecting an owner-map file to set Jira assignee fields.

**Functions used:** F06, F09, F10

**Inputs**

- Original recommendation ID, source service, observation period and current/proposed configuration.
- Estimated savings and assumptions; alternatives affecting the same resource or commitment.
- Performance/resilience constraints and recent workload demand information from the resource owner.
- A connected Jira project and explicit interactive approval or reviewed automation authorization.

1. **Cost engineer — Retrieve the original recommendation.** Open the source record, confirm freshness and identify overlapping alternatives before creating a savings total.

2. **Workload owner — Decide whether the change is feasible.** Review peaks, latency, redundancy, compatibility and rollback. Reject or defer if source utilization is not representative of the intended workload.

3. **Agent and operator — Prepare the issue.** Include resource identity, source recommendation, estimate assumptions, verification plan and owner contact in the description. Select the connected project; do not claim to set assignee or priority.

4. **Operator — Approve and verify publication.** Approve the interactive issue creation, then inspect the actual Jira issue and its defaults. Keep deployment approval outside this action.

5. **Cost engineer — Measure after a separate approved change.** Once engineering deploys a change, compare a representative matched period and document workload differences. Read issue state or add a follow-up comment; do not imply the agent transitioned the workflow.

**Acceptance:** The issue points to a current source recommendation and records feasibility, implementation and measurement requirements. Estimated and realized savings remain separate fields.

**Stop:** Do not create an implementation commitment when the owner, source assumptions or rollback are unknown. Do not publish to an unapproved project or audience.

**Example instruction**

```text
Retrieve recommendation <id> and summarize its source, current/proposed configuration, estimate assumptions and overlapping alternatives. Draft a Jira issue in <connected project> with an independent verification plan. Request approval before creating it. Do not change resources or issue fields.
```

**Demonstration allocation:** 3 minutes.

- 1 min: Inspect a prepared recommendation and identify one overlapping alternative.
- 1 min: Review a draft issue, project defaults and the interactive approval boundary.
- 1 min: Contrast estimated savings with the future measurement required after an independently approved deployment.

**Fallback:** Use a prepared recommendation and draft issue; do not create a real ticket unless the connected project and operator authorization are explicitly available.

Official documentation: [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## Synthetic reconciliation: a 22% increase is arithmetic, not a diagnosis

Invented quantities and unit rates for a teaching example. Not AWS prices, billing data or measured agent output.

| Component | Baseline quantity | Baseline rate | Current quantity | Current rate | Baseline cost | Current cost |
|---|---|---|---|---|---|---|
| Compute | 1000 | 0.1 | 1200 | 0.12 | 100 | 144 |
| Storage | 5000 | 0.02 | 5000 | 0.02 | 100 | 100 |

Baseline total = 200; current total = 244; delta = 44; relative change = 44/200 = 22%. Under a quantity-first decomposition, quantity contribution = (1200-1000) × 0.10 = 20; rate contribution = 1200 × (0.12-0.10) = 24. Contributions sum to 44. A different decomposition convention can allocate the interaction term differently; state the convention. These calculations do not explain why quantity or rate changed. A deployment, discount change or billing adjustment needs separate evidence.

## Documentation qualifications

Optimization recommendations are attributed to their source services; this guide does not present retrieval as an independent agent optimization engine.

The interaction guide's general approval wording is qualified by the action-specific guardrail page: Jira automations are pre-authorized, and Slack posting has no per-message approval.

No undocumented general event subscription, Slack conversation listener, Jira workflow editor, infrastructure mutator or commitment-purchase action is inferred from the available integrations.

The worked example tests reconciliation logic only. There is no live billing-data reconciliation, agent-run benchmark or measured savings result in this deliverable.

## Official source register

- [What is AWS FinOps Agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html)

- [Creating an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

- [Setup and role policies](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

- [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

- [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

- [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

- [Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

- [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

- [Event-triggered anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

- [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

- [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

- [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

- [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)

- [Data protection and deletion lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

- [Web application and feedback](https://docs.aws.amazon.com/finops-agent/latest/userguide/how-do-i-interact-with-the-agent.html)

- [Storage and cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

No live product execution or measured operational benefit is claimed.
