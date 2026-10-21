# AWS FinOps Agent

Cost analysis, anomaly investigation, reporting and engineering follow-up.


Revision: 21 October 2026. Independent engineering field guide.


**Audience:** FinOps practitioners, platform engineers and service owners

**Availability:** The entire service is preview. Review the documented US storage and inference boundary before supplying organizational data.

**Recommended starting decision:** Start with one cost question whose total can be independently reproduced. Keep infrastructure changes and financial commitments outside the analysis authority.


## Decision brief

The first question after a cost increase is not which resource to delete. It is whether the compared figures use the same period, account scope, currency and cost basis. Only then can the team decide whether the movement reflects usage, pricing, allocation, a change in workload behavior or incomplete data.

This report follows a synthetic storage-cost increase from reconciliation to a service-owned action. FinOps Agent can support inquiry, anomaly investigation, recommendation triage and reporting through permitted cost services. The analysis does not authorize a capacity change or purchase. Potential savings remain estimates until an implemented change is measured on a comparable basis.


## Running use case

**Name:** Explain a synthetic storage-cost increase

**Trigger:** A teaching dataset compares two complete 14-day periods and shows approximately 41% higher cost.

**Scope:** Explicit accounts, Regions, currency, date boundaries, tags and cost metric; synthetic figures are not an AWS account result.

**Deliverable:** A reconciled explanation, confidence and gaps, an engineering owner and a controlled follow-up.

**Not Done:** An attractive savings estimate is quoted without matching totals or checking operational constraints.

**Done:** The source total is reproducible, the driver is supported by evidence, and an owner accepts the next action and measurement plan.


## 1. Define the comparison before asking for an explanation

Write down the cost metric, currency, account group, Region filters and complete date windows. Clarify whether the comparison includes credits, refunds, amortization or allocation rules. Organizational context can identify owners and services, but it does not repair inconsistent billing filters.

Approve preview use and the documented processing boundary before uploading internal context. IAM and permitted cost services determine accessible data. Start with an account group whose owner can validate a material total rather than granting broad access to make every possible question answerable.

**Capability crosswalk:** C01, C09

**Responsible role (team recommendation):** FinOps analyst and cost owner

**Input:** Comparison contract, approved data scope and current ownership context.

**Artifact:** A reproducible cost-query definition with explicit exclusions.

**Gate:** The same query can be expressed in the underlying source service.

**Fallback:** Resolve metric or date mismatches before discussing causes or savings.


## 2. Reconcile the total and identify material contributors

Ask the agent to group the cost by useful dimensions and show the arithmetic behind the movement. Reproduce at least one material total in the source system using the same filters. A convincing explanation based on a different cost basis is not acceptable evidence.

Forecasts and commitment coverage can provide additional context, but they answer different questions from historical reconciliation. Separate observed spend from forecast values and contractual estimates. The synthetic demo illustrates this distinction; it is not evidence of a real account anomaly.

**Capability crosswalk:** C01, C02

**Responsible role (team recommendation):** FinOps analyst

**Input:** Matching cost queries for both comparison periods.

**Artifact:** A reconciled delta and a ranked set of contributing services or usage dimensions.

**Gate:** Totals, scope and arithmetic agree with an independent source check.

**Fallback:** Label unresolved discrepancies and withhold a causal conclusion until the totals are understood.


## 3. Investigate drivers without mistaking correlation for cause

An anomaly investigation can combine cost evidence with permitted operational context, including relevant change records. Ask which observations support a likely driver, which alternatives remain plausible, and which evidence is missing. A deployment occurring near the increase is a lead, not proof of causation.

Event-triggered investigation is a configured workflow. Confirm the anomaly event source, permissions and output destination, and decide how duplicate or incomplete events are handled. The team still needs an owner who reviews the result and can stop a noisy automation.

**Capability crosswalk:** C03, C08

**Responsible role (team recommendation):** Engineering and FinOps owners

**Input:** Reconciled movement, anomaly details and permitted change context.

**Artifact:** A driver analysis that separates observations, hypotheses and gaps.

**Gate:** The proposed explanation accounts for a material part of the observed change.

**Fallback:** Route an unresolved question to the workload owner instead of inventing a definitive cause.


## 4. Evaluate recommendations against operational constraints

Existing optimization recommendations can help prioritize investigation, but their projected savings are not an instruction to implement. Review utilization, resilience, performance and recovery requirements with the service owner. Avoid adding overlapping estimates as though every action can deliver its full saving independently.

For a storage recommendation, clarify whether the action changes retention, retrieval latency, durability assumptions or recovery procedures. The authorized change belongs in normal infrastructure and financial processes. The agent's useful output is a justified candidate with constraints and evidence.

**Capability crosswalk:** C04, C13

**Responsible role (team recommendation):** Service owner and FinOps reviewer

**Input:** Recommendation source, utilization evidence, service constraints and estimated benefit.

**Artifact:** A prioritized candidate with operational risks, owner and acceptance criteria.

**Gate:** The service owner accepts the trade-offs and the change is approved separately.

**Fallback:** Reject or defer recommendations that conflict with the service's reliability or data obligations.


## 5. Publish the result to the right audience

Turn the analysis into a report or tracked task with the comparison basis, important figures, uncertainty and next owner. Recurring reporting is useful when its schedule and audience are explicit. Context files and remembered preferences should be reviewed when ownership or reporting rules change.

Jira and Slack are external publication effects, not merely read-only analysis. Interactive Jira confirmation, automated-task behavior and Slack posting controls differ. Review the documented path and the destination audience before scheduling a task or sharing commercially sensitive cost information.

**Capability crosswalk:** C05, C06, C07, C10, C11, C12

**Responsible role (team recommendation):** Report owner

**Input:** Reviewed analysis, approved destination and named action owner.

**Artifact:** A report or ticket with evidence links and a concrete next step.

**Gate:** Audience, automatic-posting behavior and approval expectations match the chosen integration.

**Fallback:** Keep the result in a local report until the publication path and audience are approved.


## 6. Measure an implemented change on a comparable basis

After an independently authorized engineering change, compare the relevant cost and service indicators using a consistent measurement basis. Separate savings caused by the change from lower traffic, different prices or changed allocation. A smaller invoice alone does not establish that the recommendation delivered the estimated benefit.

Close the task only when the owner has reviewed both cost and operational outcomes. Capture rejected recommendations and analysis effort as well as accepted work. That gives the pilot a more meaningful scorecard than the number of reports produced or the sum of potential savings shown.

**Capability crosswalk:** C13

**Responsible role (team recommendation):** Engineering owner and cost owner

**Input:** Implemented change record, comparable observation windows and service-health evidence.

**Artifact:** A measured outcome with attribution limits and an owner-approved disposition.

**Gate:** Benefit and reliability implications are checked independently of the original recommendation.

**Fallback:** Leave benefit unclaimed when the comparison cannot isolate the effect or required data is incomplete.


## Detailed capability reference


### C01 — Explain cost changes by service, account, Region, or tag

**Claim:** Ask for cost breakdowns, comparisons, and trends using the supported dimensions available through the agent’s data sources.

**Availability:** Preview · us-east-1

**Delivery:** Native cost inquiry; permitted AWS sources

**Setup:** Create the agent and operator roles, enable relevant cost services, and establish the account scope you intend to analyze.

**Limit:** Results depend on source access and the chosen time range, granularity, filters, and cost basis. An inaccessible data source cannot be inferred from a fluent answer.

**Check:** Reproduce one material total in the source console with matching dates and filters before using the explanation.

**Prompt:** Compare this service’s cost for the last two complete weeks, grouped by account and Region. State filters and the cost basis used.

**Review record to retain (team recommendation):** Reproducible cost query, dimensioned totals, filters, and data-source cross-check.

Official documentation references: S06, S03, S04


### C02 — Inspect forecasts and commitment coverage

**Claim:** Cost inquiry includes forecasts and Savings Plans or Reserved Instance coverage, utilization, and recommendation questions.

**Availability:** Preview · us-east-1

**Delivery:** Native analysis; underlying billing APIs

**Setup:** Grant the relevant billing-data permissions and identify the accounts, period, and workload assumptions.

**Limit:** A forecast is not a budget guarantee or a purchase instruction. Commitment decisions need independent workload and financial review.

**Check:** Check forecast assumptions, coverage definitions, and workload stability; do not purchase based only on the generated summary.

**Prompt:** Summarize current commitment coverage and the next-period forecast for these accounts. Separate observed data from projections.

**Review record to retain (team recommendation):** Forecast/coverage figures with stated source, time horizon, and commitment assumptions.

Official documentation references: S06, S04


### C03 — Investigate a cost anomaly with operational context

**Claim:** Analyze cost drivers and distinguish likely usage or rate changes; CloudTrail access can add evidence about relevant operational events.

**Availability:** Preview · us-east-1

**Delivery:** Native investigation; optional CloudTrail access

**Setup:** Provide the anomaly or precise account/service/time window and grant only the additional read access needed.

**Limit:** Correlation is investigative, not proof of causation. Missing audit access or mismatched timestamps can limit the explanation.

**Check:** Validate the leading explanation against usage metrics, the deployment record, and the same billing interval.

**Prompt:** Investigate this storage-cost increase. Rank evidence-backed drivers, identify relevant changes, and state what remains uncertain.

**Review record to retain (team recommendation):** Anomaly investigation separating observed variance, supporting drivers, and uncertainty.

Official documentation references: S07, S15


### C04 — Prioritize existing optimization recommendations

**Claim:** Retrieve and filter recommendations from Cost Optimization Hub and Compute Optimizer by useful engineering criteria such as service, account, effort, or estimated savings.

**Availability:** Preview · us-east-1

**Delivery:** Native retrieval and contextualization

**Setup:** Enable and authorize the relevant recommendation sources; provide workload ownership and operational constraints.

**Limit:** The agent summarizes those systems’ recommendations; it is not a separate optimizer and does not implement resource changes.

**Check:** Check utilization, reliability constraints, overlapping savings estimates, and the recommendation’s source date.

**Prompt:** List low-effort non-production recommendations for our team. Include source, resource, estimated benefit, and the checks required before changing it.

**Review record to retain (team recommendation):** Ranked optimization recommendations with resource IDs and operational constraints.

Official documentation references: S09, S15


### C05 — Generate a report for engineering or leadership

**Claim:** Create cost reports with charts and narrative in HTML, PDF, or editable PowerPoint format, then request revisions.

**Availability:** Preview · us-east-1

**Delivery:** Native artifact generation

**Setup:** Define the audience, period, cost basis, dimensions, and output format. Provide a template only in a supported context format.

**Limit:** Generated charts and interpretation need review. Output formats do not imply that PDF or PowerPoint files are accepted as context uploads.

**Check:** Reconcile totals, chart labels, periods, and ownership; distinguish estimated savings from realized savings.

**Prompt:** Create an HTML report for the platform review: spend by team, significant changes, unresolved anomalies, and a source-backed action list.

**Review record to retain (team recommendation):** Dated cost report recording query definition, charts, narrative, and unverified assumptions.

Official documentation references: S10, S12


### C06 — Turn a request into a tracked on-demand task

**Claim:** Explicitly requested on-demand tasks appear in the task queue alongside scheduled and event-driven work, with execution history.

**Availability:** Preview · us-east-1

**Delivery:** Native task queue and history

**Setup:** Specify that the request should become a task and define the expected output and connected destination.

**Limit:** An ordinary chat question does not automatically become a tracked task. External actions have their own approval rules.

**Check:** Confirm task creation and output, and inspect the history for failed tools, missing data, and external actions.

**Prompt:** Create an on-demand task to investigate the selected anomaly and produce a written evidence summary for review.

**Review record to retain (team recommendation):** Tracked on-demand task with owner, input scope, result, and completion status.

Official documentation references: S11


### C07 — Schedule recurring cost reports and reviews

**Claim:** Create recurring tasks in natural language and manage their configuration, status, and recorded runs through Automations.

**Availability:** Preview · us-east-1

**Delivery:** Native scheduled automations

**Setup:** Agree on a report owner, cadence, recipient scope, and stop conditions before enabling the automation.

**Limit:** Scheduled external actions can be pre-authorized. Recurrence does not establish that a report’s recipients or data remain appropriate over time.

**Check:** Inspect the stored schedule and first output, then disable or revise jobs that produce noise or outdated context.

**Prompt:** Prepare a weekly platform cost review with anomaly follow-up and a clearly separated list of unverified recommendations.

**Review record to retain (team recommendation):** Scheduled task definition, run history, output report, and reviewer.

Official documentation references: S11, S10, S15


### C08 — Trigger a workflow from a cost-anomaly event

**Claim:** An event-based automation can investigate a matching Cost Anomaly Detection event and produce configured outputs or handoffs.

**Availability:** Preview · us-east-1

**Delivery:** Native event automation; AWS prerequisites

**Setup:** Configure a cost-anomaly monitor, suitable trigger conditions, and approved output destinations; scope the automation role.

**Limit:** During preview the supported event type is cost anomaly, not arbitrary deployment or custom events. Existing monitors and EventBridge permissions are required.

**Check:** Validate event matching, duplicate handling, output visibility, and the automation’s disabled state before broader rollout.

**Prompt:** When a qualifying anomaly is detected in our non-production account group, investigate it and prepare a concise evidence summary.

**Review record to retain (team recommendation):** Event-trigger definition, source anomaly reference, investigation record, and notification log.

Official documentation references: S08, S04


### C09 — Supply account ownership and reporting context

**Claim:** Upload account-to-team mappings, cost categories, instructions, and report-format guidance using the documented text-based file types.

**Availability:** Preview · us-east-1

**Delivery:** Native context-file workspace

**Setup:** Use reviewed TXT, CSV, JSON, Markdown, HTML, or YAML files; prefer team identifiers over personal details.

**Limit:** Files are visible to everyone with agent access and should not contain sensitive or personal information. PDF and PPTX are not accepted context-file types.

**Check:** Check mappings against the authoritative inventory and review who can access the agent before uploading.

**Prompt:** Use this account-to-team map for reporting, identify unmapped accounts, and do not invent an owner for missing entries.

**Review record to retain (team recommendation):** Versioned ownership/cost-allocation context and an exception list for unmapped resources.

Official documentation references: S12, S17


### C10 — Correct recurring preferences through memory

**Claim:** Tell the agent to remember, update, or forget preferences and corrections that affect later work.

**Availability:** Preview · us-east-1

**Delivery:** Native conversational memory

**Setup:** Keep authoritative ownership and policy in maintained sources and review remembered preferences after organizational changes.

**Limit:** Memory is distinct from uploaded files; the agent cannot modify or delete context files through conversation. Long conversations can be summarized.

**Check:** Ask a fresh scoped question to confirm the correction took effect without overwriting the authoritative context source.

**Prompt:** Update the reporting preference to show account and service first, and stop applying the old team grouping.

**Review record to retain (team recommendation):** Stored reporting preferences with corrections and a check for current applicability.

Official documentation references: S12


### C11 — Create Jira Cloud issues and follow-up comments

**Claim:** Create Jira issues, add comments to agent-created issues, and read supported issue fields through a connected project.

**Availability:** Preview · us-east-1

**Delivery:** Native Jira Cloud integration

**Setup:** Connect Jira Cloud and the intended project to the agent, then review project defaults, permissions, and issue visibility.

**Limit:** Jira Server/Data Center is not supported. The agent does not set assignee, priority, or status; ownership relies on Jira defaults or rules. Interactive/on-demand writes require approval; automated writes are pre-authorized.

**Check:** Confirm the approval behavior for the chosen path and inspect the actual issue assignment and contents in Jira.

**Prompt:** Prepare a Jira issue summarizing this verified cost concern, its account and resource, evidence, and the team’s required validation steps.

**Review record to retain (team recommendation):** Linked Jira work item with recommendation evidence, assignee, and follow-up status.

Official documentation references: S13, S15


### C12 — Post cost updates to a connected Slack channel

**Claim:** Post analysis or reporting updates to an authorized connected Slack channel.

**Availability:** Preview · us-east-1

**Delivery:** Native outbound Slack integration

**Setup:** Install and connect the app, join the destination channel as required, and verify the account/workspace and per-agent channel configuration.

**Limit:** The integration is one-way: it does not read channel conversations or accept mentions as commands. Posting does not require per-message approval.

**Check:** Confirm the destination and audience first; inspect task history and the delivered message afterward.

**Prompt:** Post the reviewed platform cost summary to the approved internal channel without account-owner personal details or sensitive attachments.

**Review record to retain (team recommendation):** Approved Slack message with cost context, scope, and source-report link.

Official documentation references: S14, S15


### C13 — Turn a recommendation into a controlled engineering change

**Claim:** A practical engineering workflow is to turn a reviewed recommendation into a normal change ticket, validate the change, and compare later costs.

**Availability:** Preview · us-east-1 · team-owned follow-through

**Delivery:** Suggested process around documented analysis and Jira handoff

**Setup:** Choose one low-risk opportunity with an owner, baseline, operational acceptance tests, approval, and a recovery plan.

**Limit:** The agent is not documented as autonomously resizing resources, deleting assets, or buying commitments. Implementation and rollback remain team responsibilities.

**Check:** Compare matched periods and workload levels after the independently approved change; account for regressions and implementation cost.

**Prompt:** Summarize this opportunity as a proposed change with assumptions and measurement criteria; do not describe estimated savings as achieved.

**Review record to retain (team recommendation):** Change ticket with proposed action, approvals, deployment evidence, and comparable post-change cost.

Official documentation references: S09, S13, S15


## Illustrative handoff

```yaml

analysis: COST-DEMO-001
data_kind: synthetic-teaching-fixture
periods: two-complete-14-day-windows
metric: stated-cost-basis
owner: service-owner
allowed_effects: [analyze-cost, draft-recommendation]
change_authority: separate-approval
benefit: estimate-until-independently-measured

```


## Readiness checklist

- [ ] Preview use and data-location boundaries are approved.

- [ ] Periods, currency, filters and cost basis are explicit.

- [ ] A material total reconciles to the source service.

- [ ] Observed movement is separated from causal hypotheses.

- [ ] Publication destinations and automation behavior are reviewed.

- [ ] Changes and purchases require separate approval; savings are not pre-claimed.


## Sources

- S01: [AWS frontier agents](https://aws.amazon.com/ai/frontier-agents/)

- S02: [What is AWS FinOps Agent?](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html)

- S03: [Create an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

- S04: [IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

- S05: [Chatting with the agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/chatting-with-finops-agent.html)

- S06: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

- S07: [Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

- S08: [Automated anomaly response](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

- S09: [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

- S10: [Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

- S11: [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

- S12: [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

- S13: [Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

- S14: [Slack integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)

- S15: [Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

- S16: [Cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

- S17: [Quotas](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html)


## Validation boundary

Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.
