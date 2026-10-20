# AWS FinOps Agent — documentation-validation record and presentation transcript

**Day-to-day cloud cost engineering · preview**

Documentation reviewed: **20 October 2026**. Independent synthesis of official AWS/Kiro sources; not an AWS publication.

**Scope:** Cost inquiry, anomaly investigation, recommendation triage, recurring reporting, and engineering handoff. All service features in this report are preview; no autonomous resource resizing, deletion, or commitment purchase is claimed.

**Overview:** Use the agent to turn AWS cost data into a specific engineering question: what changed, which account or service is responsible, what evidence supports the explanation, and what should a team investigate next. Keep infrastructure changes and financial commitments in existing approval processes.

**Read before adoption:** The entire service is preview in us-east-1. Stored context, conversations, memory, and artifacts remain there; inference can use other US Regions. Slack is outbound-only. Jira approvals depend on how the action starts, and optimization advice does not apply infrastructure changes. [S02] [S16] [S14] [S15]

## Validation method and outcome

13 capability entries; eight presentation sections; 17 official references.

| Verdict | Entries | Meaning |
|---|---:|---|
| Confirmed | 4 | Core behavior directly documented. |
| Qualified | 8 | Documented behavior with material setup, access, or safety restrictions. |
| Workflow example | 1 | Author-proposed use of documented tools, not a separately established native feature. |

Verdicts are not maturity labels. A confirmed claim can still be preview. Every feature’s availability is recorded separately.

**Validation boundary:** Documentation review only. No AWS account, repository, application, permission policy, prompt, or agent workflow was exercised. Demonstrations and acceptance checks are proposed. No productivity, diagnostic-accuracy, detection-rate, or savings outcome was measured.

**Excluded from this first pass:** Autonomous AWS resource remediation, commitment purchasing, arbitrary custom-event automation, inbound Slack commands, Jira workflow administration, and claims of realized savings are outside this first pass. All included features remain preview, not a GA production baseline.

## Recommended starting workflow

1. Approve preview use and the us-east-1 storage / US inference boundary before uploading organizational data.

2. Create roles, verify source-service access, and reconcile one cost breakdown against the original billing view.

3. Add a sanitized team map, then trial one owned report or anomaly workflow with explicit destination checks.

## Capability register

### C01 — Explain cost changes by service, account, Region, or tag

**Area:** Cost analysis  
**Verdict:** Confirmed  
**Availability:** Preview · us-east-1  
**Delivery model:** Native cost inquiry; permitted AWS sources

**Documented capability:** Ask for cost breakdowns, comparisons, and trends using the supported dimensions available through the agent’s data sources. [S06] [S03] [S04]

**Boundary:** Results depend on source access and the chosen time range, granularity, filters, and cost basis. An inaccessible data source cannot be inferred from a fluent answer.

**Prerequisites:** Create the agent and operator roles, enable relevant cost services, and establish the account scope you intend to analyze.

**Example task or prompt — author-created, not executed:**

> Compare this service’s cost for the last two complete weeks, grouped by account and Region. State filters and the cost basis used.

**Engineering acceptance check — recommendation:** Reproduce one material total in the source console with matching dates and filters before using the explanation.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C02 — Inspect forecasts and commitment coverage

**Area:** Cost analysis  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native analysis; underlying billing APIs

**Documented capability:** Cost inquiry includes forecasts and Savings Plans or Reserved Instance coverage, utilization, and recommendation questions. [S06] [S04]

**Boundary:** A forecast is not a budget guarantee or a purchase instruction. Commitment decisions need independent workload and financial review.

**Prerequisites:** Grant the relevant billing-data permissions and identify the accounts, period, and workload assumptions.

**Example task or prompt — author-created, not executed:**

> Summarize current commitment coverage and the next-period forecast for these accounts. Separate observed data from projections.

**Engineering acceptance check — recommendation:** Check forecast assumptions, coverage definitions, and workload stability; do not purchase based only on the generated summary.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C03 — Investigate a cost anomaly with operational context

**Area:** Investigation and optimization  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native investigation; optional CloudTrail access

**Documented capability:** Analyze cost drivers and distinguish likely usage or rate changes; CloudTrail access can add evidence about relevant operational events. [S07] [S15]

**Boundary:** Correlation is investigative, not proof of causation. Missing audit access or mismatched timestamps can limit the explanation.

**Prerequisites:** Provide the anomaly or precise account/service/time window and grant only the additional read access needed.

**Example task or prompt — author-created, not executed:**

> Investigate this storage-cost increase. Rank evidence-backed drivers, identify relevant changes, and state what remains uncertain.

**Engineering acceptance check — recommendation:** Validate the leading explanation against usage metrics, the deployment record, and the same billing interval.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C04 — Prioritize existing optimization recommendations

**Area:** Investigation and optimization  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native retrieval and contextualization

**Documented capability:** Retrieve and filter recommendations from Cost Optimization Hub and Compute Optimizer by useful engineering criteria such as service, account, effort, or estimated savings. [S09] [S15]

**Boundary:** The agent summarizes those systems’ recommendations; it is not a separate optimizer and does not implement resource changes.

**Prerequisites:** Enable and authorize the relevant recommendation sources; provide workload ownership and operational constraints.

**Example task or prompt — author-created, not executed:**

> List low-effort non-production recommendations for our team. Include source, resource, estimated benefit, and the checks required before changing it.

**Engineering acceptance check — recommendation:** Check utilization, reliability constraints, overlapping savings estimates, and the recommendation’s source date.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C05 — Generate a report for engineering or leadership

**Area:** Reporting and task management  
**Verdict:** Confirmed  
**Availability:** Preview · us-east-1  
**Delivery model:** Native artifact generation

**Documented capability:** Create cost reports with charts and narrative in HTML, PDF, or editable PowerPoint format, then request revisions. [S10] [S12]

**Boundary:** Generated charts and interpretation need review. Output formats do not imply that PDF or PowerPoint files are accepted as context uploads.

**Prerequisites:** Define the audience, period, cost basis, dimensions, and output format. Provide a template only in a supported context format.

**Example task or prompt — author-created, not executed:**

> Create an HTML report for the platform review: spend by team, significant changes, unresolved anomalies, and a source-backed action list.

**Engineering acceptance check — recommendation:** Reconcile totals, chart labels, periods, and ownership; distinguish estimated savings from realized savings.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C06 — Turn a request into a tracked on-demand task

**Area:** Reporting and task management  
**Verdict:** Confirmed  
**Availability:** Preview · us-east-1  
**Delivery model:** Native task queue and history

**Documented capability:** Explicitly requested on-demand tasks appear in the task queue alongside scheduled and event-driven work, with execution history. [S11]

**Boundary:** An ordinary chat question does not automatically become a tracked task. External actions have their own approval rules.

**Prerequisites:** Specify that the request should become a task and define the expected output and connected destination.

**Example task or prompt — author-created, not executed:**

> Create an on-demand task to investigate the selected anomaly and produce a written evidence summary for review.

**Engineering acceptance check — recommendation:** Confirm task creation and output, and inspect the history for failed tools, missing data, and external actions.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C07 — Schedule recurring cost reports and reviews

**Area:** Reporting and task management  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native scheduled automations

**Documented capability:** Create recurring tasks in natural language and manage their configuration, status, and recorded runs through Automations. [S11] [S10] [S15]

**Boundary:** Scheduled external actions can be pre-authorized. Recurrence does not establish that a report’s recipients or data remain appropriate over time.

**Prerequisites:** Agree on a report owner, cadence, recipient scope, and stop conditions before enabling the automation.

**Example task or prompt — author-created, not executed:**

> Prepare a weekly platform cost review with anomaly follow-up and a clearly separated list of unverified recommendations.

**Engineering acceptance check — recommendation:** Inspect the stored schedule and first output, then disable or revise jobs that produce noise or outdated context.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C08 — Trigger a workflow from a cost-anomaly event

**Area:** Investigation and optimization  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native event automation; AWS prerequisites

**Documented capability:** An event-based automation can investigate a matching Cost Anomaly Detection event and produce configured outputs or handoffs. [S08] [S04]

**Boundary:** During preview the supported event type is cost anomaly, not arbitrary deployment or custom events. Existing monitors and EventBridge permissions are required.

**Prerequisites:** Configure a cost-anomaly monitor, suitable trigger conditions, and approved output destinations; scope the automation role.

**Example task or prompt — author-created, not executed:**

> When a qualifying anomaly is detected in our non-production account group, investigate it and prepare a concise evidence summary.

**Engineering acceptance check — recommendation:** Validate event matching, duplicate handling, output visibility, and the automation’s disabled state before broader rollout.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C09 — Supply account ownership and reporting context

**Area:** Team context and controls  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native context-file workspace

**Documented capability:** Upload account-to-team mappings, cost categories, instructions, and report-format guidance using the documented text-based file types. [S12] [S17]

**Boundary:** Files are visible to everyone with agent access and should not contain sensitive or personal information. PDF and PPTX are not accepted context-file types.

**Prerequisites:** Use reviewed TXT, CSV, JSON, Markdown, HTML, or YAML files; prefer team identifiers over personal details.

**Example task or prompt — author-created, not executed:**

> Use this account-to-team map for reporting, identify unmapped accounts, and do not invent an owner for missing entries.

**Engineering acceptance check — recommendation:** Check mappings against the authoritative inventory and review who can access the agent before uploading.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C10 — Correct recurring preferences through memory

**Area:** Team context and controls  
**Verdict:** Confirmed  
**Availability:** Preview · us-east-1  
**Delivery model:** Native conversational memory

**Documented capability:** Tell the agent to remember, update, or forget preferences and corrections that affect later work. [S12]

**Boundary:** Memory is distinct from uploaded files; the agent cannot modify or delete context files through conversation. Long conversations can be summarized.

**Prerequisites:** Keep authoritative ownership and policy in maintained sources and review remembered preferences after organizational changes.

**Example task or prompt — author-created, not executed:**

> Update the reporting preference to show account and service first, and stop applying the old team grouping.

**Engineering acceptance check — recommendation:** Ask a fresh scoped question to confirm the correction took effect without overwriting the authoritative context source.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C11 — Create Jira Cloud issues and follow-up comments

**Area:** Collaboration  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native Jira Cloud integration

**Documented capability:** Create Jira issues, add comments to agent-created issues, and read supported issue fields through a connected project. [S13] [S15]

**Boundary:** Jira Server/Data Center is not supported. The agent does not set assignee, priority, or status; ownership relies on Jira defaults or rules. Interactive/on-demand writes require approval; automated writes are pre-authorized.

**Prerequisites:** Connect Jira Cloud and the intended project to the agent, then review project defaults, permissions, and issue visibility.

**Example task or prompt — author-created, not executed:**

> Prepare a Jira issue summarizing this verified cost concern, its account and resource, evidence, and the team’s required validation steps.

**Engineering acceptance check — recommendation:** Confirm the approval behavior for the chosen path and inspect the actual issue assignment and contents in Jira.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C12 — Post cost updates to a connected Slack channel

**Area:** Collaboration  
**Verdict:** Qualified  
**Availability:** Preview · us-east-1  
**Delivery model:** Native outbound Slack integration

**Documented capability:** Post analysis or reporting updates to an authorized connected Slack channel. [S14] [S15]

**Boundary:** The integration is one-way: it does not read channel conversations or accept mentions as commands. Posting does not require per-message approval.

**Prerequisites:** Install and connect the app, join the destination channel as required, and verify the account/workspace and per-agent channel configuration.

**Example task or prompt — author-created, not executed:**

> Post the reviewed platform cost summary to the approved internal channel without account-owner personal details or sensitive attachments.

**Engineering acceptance check — recommendation:** Confirm the destination and audience first; inspect task history and the delivered message afterward.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C13 — Turn a recommendation into a controlled engineering change

**Area:** Engineering workflow examples  
**Verdict:** Workflow example  
**Availability:** Preview · us-east-1 · team-owned follow-through  
**Delivery model:** Suggested process around documented analysis and Jira handoff

**Documented capability:** A practical engineering workflow is to turn a reviewed recommendation into a normal change ticket, validate the change, and compare later costs. [S09] [S13] [S15]

**Boundary:** The agent is not documented as autonomously resizing resources, deleting assets, or buying commitments. Implementation and rollback remain team responsibilities.

**Prerequisites:** Choose one low-risk opportunity with an owner, baseline, operational acceptance tests, approval, and a recovery plan.

**Example task or prompt — author-created, not executed:**

> Summarize this opportunity as a proposed change with assumptions and measurement criteria; do not describe estimated savings as achieved.

**Engineering acceptance check — recommendation:** Compare matched periods and workload levels after the independently approved change; account for regressions and implementation cost.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

## Cross-cutting validation record

### G01 — All capabilities remain preview

Every card inherits the service’s preview status. Preview is included by default because excluding it would hide the entire report; turning the filter off intentionally shows no routine GA baseline. [S02] [S01]

### G02 — Region and residency

Preview runs and stores context, conversations, memory, and artifacts in us-east-1. Inference can occur in other US Regions. This is not an EU- or Switzerland-resident processing option. [S16]

### G03 — Permissions and charges are still real

Separate agent service-role access from operator access. Prerequisite AWS services and APIs have their own permissions and possible charges; no preview service fee does not mean every dependency is free. EventBridge automation setup also requires scoped management permissions. [S04] [S03] [S05]

### G04 — Analysis does not apply resource changes

Recommendations come from existing AWS optimization services. No resource resizing, deletion, or commitment purchase is asserted. Do not confuse read-oriented analysis with an absence of all writes: automations manage event rules and can send external messages. [S09] [S15] [S04]

### G05 — Approval depends on the action path

Chat or on-demand Jira issues/comments require approval. Scheduled/event-driven Jira actions are pre-authorized when configured. Slack posts require no per-message approval, so channel selection is a material control. [S15]

### G06 — Owner mapping is not a Jira assignment action

The context guidance discusses ownership-aware routing, but the Jira integration’s specific supported-action list does not include setting assignee, priority, or status. This report treats ownership context as ticket content and project routing; assignment is controlled by Jira defaults or rules. [S12] [S13]

### G07 — Context formats and access

Supported uploads are text-based formats, not PDF/PPTX. Context files are shared with the agent’s authorized users; memory correction does not edit those files. Sanitize organizational examples before use. [S12]

### G08 — Validate data semantics and source evidence

Match periods, dimensions, granularity, and cost basis before comparing numbers. Anomaly causes are investigative and reported savings are estimates until an approved change is measured. [S06] [S07] [S09] [S15]

## Structured presentation transcript

Eight sections. Speaking notes are ready to present; demonstrations remain proposed and unexecuted.

### 01 — Position FinOps Agent in the engineering workflow

**On-screen message:** Analyze and route cost work; keep change authority elsewhere.

**Speaker transcript:**

This is a preview service for cost analysis, anomaly investigation, recommendation triage, and reporting. Its engineering value is to turn a vague cost concern into evidence and a next action. It is not presented here as an infrastructure-remediation engine. A service owner still decides whether a capacity or configuration change is safe, and existing approval processes still govern financial commitments. Keep this scope distinct from DevOps incident response: cost evidence can inform an investigation, but the report does not claim general operational diagnosis or automatic production repair.

**Proposed demonstration — not executed:** Choose one engineering cost question and identify the service owner, billing period, evidence source, and possible follow-up action.

**Official evidence:** [S02] [S09] [S15]

### 02 — Establish a trustworthy cost baseline

**On-screen message:** The same number requires the same period, filters, and cost basis.

**Speaker transcript:**

Begin with a question that can be reproduced in the underlying billing view. Define the account scope, completed time periods, dimensions, and cost treatment. Ask the agent to expose these choices in its answer. Our suggested first check is a two-week comparison for a single service rather than an organization-wide explanation. Reconcile a material total before acting on the narrative. A forecast or commitment-coverage summary is a separate kind of output: useful for planning, but not a guarantee or an authorization to buy.

**Proposed demonstration — not executed:** Compare a generated breakdown with the equivalent source-console view and explain any difference before accepting the report.

**Official evidence:** [S06] [S04]

### 03 — Investigate an anomaly without overstating causality

**On-screen message:** Separate observed cost drivers from plausible explanations.

**Speaker transcript:**

An anomaly investigation can combine billing drivers with relevant operational events when the required access exists. A deployment or configuration change near a cost increase is evidence to examine, not a proven cause. Our proposed investigation record separates facts, hypotheses, and missing data. Validate the leading explanation with the responsible team and relevant usage information. Missing CloudTrail access should be visible as a limitation rather than silently filled with speculation. This approach makes the result suitable for an engineering handoff without presenting uncertain diagnosis as settled fact.

**Proposed demonstration — not executed:** Build a sample evidence table with observed cost movement, candidate operational changes, and the test needed to distinguish explanations.

**Official evidence:** [S07] [S15]

### 04 — Convert optimizer output into reviewable engineering work

**On-screen message:** Estimated benefit must survive reliability and workload checks.

**Speaker transcript:**

The agent retrieves and contextualizes recommendations from existing AWS optimization services. Use it to filter the backlog and surface opportunities that match a team’s account scope and constraints. Do not mistake a compelling summary for a safe implementation plan. Our suggested first opportunity is low-risk and reversible, with an owner and a baseline. Check workload variability, dependencies, and overlapping recommendations before combining estimated savings. Implementation remains in the normal engineering change process, followed by measurement on a comparable period. A generated ticket is a handoff, not a completed optimization.

**Proposed demonstration — not executed:** Review one proposed opportunity and write its operational acceptance criteria, rollback condition, and post-change cost measurement.

**Official evidence:** [S09] [S13]

### 05 — Build reporting that remains useful every week

**On-screen message:** A recurring artifact needs an owner, validation, and a stop condition.

**Speaker transcript:**

Reports can be produced in HTML, PDF, or editable PowerPoint and refined for a particular audience. A tracked on-demand task differs from a normal chat answer, and a scheduled task differs from a manually requested review. Our recommendation is to begin with one reporting cadence and a simple template rather than many notifications. Reconcile totals and labels on the first output, then inspect subsequent runs for drift and failures. Record who maintains the account mapping and who decides when the automation should be revised or disabled.

**Proposed demonstration — not executed:** Draft one platform-team report, request a tracked run, and inspect the planned recurrence before enabling delivery.

**Official evidence:** [S10] [S11]

### 06 — Add event-driven response only after prerequisites are ready

**On-screen message:** Cost-anomaly events are supported; arbitrary deployment events are not.

**Speaker transcript:**

Event-based workflows build on Cost Anomaly Detection and EventBridge permissions. They are not a general event bus for every engineering signal during this preview. Define the monitor, threshold conditions, account scope, and destination together. Our proposed rollout first validates that a relevant event produces one useful investigation rather than repeated noisy output. Keep historical tasks separate from the decision to disable future automation. Review destinations and write approvals at setup time because a scheduled or event-triggered action can behave differently from an interactive request.

**Proposed demonstration — not executed:** Review a proposed anomaly-trigger configuration, its expected output, a duplicate-event case, and the procedure to disable future runs.

**Official evidence:** [S08] [S11] [S04]

### 07 — Treat context and collaboration settings as access decisions

**On-screen message:** Outbound messaging and task ownership have specific limits.

**Speaker transcript:**

Organizational context helps translate account IDs into meaningful team work, but uploaded files are visible to users with access to the agent and must be sanitized. Memory corrections are not edits to those uploaded files. For collaboration, the supported capabilities are narrower than a generic assistant inside every application: Jira Cloud receives issues and comments, while Slack is an outbound destination rather than a command interface. Do not assume the agent assigns a ticket to an owner simply because it knows the team mapping. Inspect the actual destination, project defaults, and action-approval path.

**Proposed demonstration — not executed:** Inspect an account-to-team context file, a draft Jira issue, and a Slack destination; verify ownership and visibility without posting sensitive data.

**Official evidence:** [S12] [S13] [S14]

### 08 — Evaluate the preview with a controlled scorecard

**On-screen message:** Measure evidence quality, reviewer burden, and verified outcomes.

**Speaker transcript:**

Before enabling the preview, approve the US-based storage and inference boundary for the intended data. The proposed pilot then measures whether the agent reduces effort without creating inaccurate reports, noisy tickets, or unsafe assumptions. Record reconciled analyses, useful anomaly explanations, accepted opportunities, reporting corrections, and actual dependency costs. Treat savings as realized only after an approved change is measured under comparable conditions. Do not extrapolate a successful example into a guaranteed percentage benefit. Expansion should preserve human ownership and established operational controls.

**Proposed demonstration — not executed:** Review a pilot scorecard that separates estimated opportunity, approved change, measured result, and unresolved evidence gaps.

**Official evidence:** [S16] [S05] [S09]

## Recommended 30-day pilot

This is an adoption experiment, not a product feature or a vendor performance promise.

### Days 1–3 — Approve preview and access

Approve the US processing/storage boundary, configure least-privilege agent/operator access, and select one account group with a known owner.

### Days 4–7 — Reconcile basic analysis

Compare a small set of cost questions against matching source views. Record data filters, unsupported questions, and correction effort.

### Days 8–14 — Investigate and prioritize

Review one anomaly and a short optimizer backlog. Validate evidence with service owners; avoid implementation or purchase automation.

### Days 15–21 — Trial one recurring workflow

Build one scheduled report or cost-anomaly response. Check history, destinations, approval behavior, and disablement before expanding notifications.

### Days 22–30 — Measure controlled follow-through

Route one accepted opportunity into the normal change process. Compare outcome and reviewer effort with the baseline; retain only useful automation.

### Recommended measures

Recommended measures: reconciled-answer rate; analyst and engineer review time; useful anomaly explanations; accepted versus rejected opportunities; reporting corrections; notification noise; actual underlying-service costs; and realized savings after separately approved changes. No results have been measured.

## Official source register

All sources checked on 20 October 2026. Recheck current documentation before enabling a workflow.

### S01 — AWS frontier agents

**Type:** Official product page  
**Relevant sections:** AWS FinOps Agent (preview)

Portfolio membership and preview designation.

[Open official source](https://aws.amazon.com/ai/frontier-agents/)

### S02 — What is AWS FinOps Agent?

**Type:** Product documentation  
**Relevant sections:** Capabilities; AWS data sources

Preview service scope and connected cost-management services.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html)

### S03 — Create an agent

**Type:** Product documentation  
**Relevant sections:** Agent and operator roles; sharing

Identity and per-agent setup; team access is permissioned.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

### S04 — IAM setup guide

**Type:** Product documentation  
**Relevant sections:** Service role; operator role; prerequisite services

Data-source permissions and EventBridge automation-management rights.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

### S05 — Chatting with the agent

**Type:** Product documentation  
**Relevant sections:** Using chat; preview charges

Underlying AWS APIs may incur charges even when preview service usage has no charge.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/chatting-with-finops-agent.html)

### S06 — Cost inquiry

**Type:** Product documentation  
**Relevant sections:** Dimensions; comparisons; forecasts; commitments

Natural-language analysis of accessible AWS cost data.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

### S07 — Cost anomaly investigation

**Type:** Product documentation  
**Relevant sections:** Cost drivers; CloudTrail analysis

Investigative evidence and optional operational correlation.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

### S08 — Automated anomaly response

**Type:** Product documentation  
**Relevant sections:** Prerequisites; event-based automation

Requires cost-anomaly monitors and EventBridge configuration; supported preview event type.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

### S09 — Optimization recommendations

**Type:** Product documentation  
**Relevant sections:** Sources; filtering; prioritization

Summarizes Cost Optimization Hub and Compute Optimizer recommendations.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

### S10 — Custom cost reporting

**Type:** Product documentation  
**Relevant sections:** Report formats; revisions; delivery

HTML, PDF, and editable PowerPoint reporting.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

### S11 — Task management

**Type:** Product documentation  
**Relevant sections:** On-demand tasks; schedules; task history

Explicit task creation, automations, and history.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

### S12 — Context files and memory

**Type:** Product documentation  
**Relevant sections:** File types; visibility; memory

Organizational context, upload restrictions, and preference corrections.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

### S13 — Jira integration

**Type:** Product documentation  
**Relevant sections:** Supported actions; limitations

Jira Cloud issue/comment handoff, not assignment/status management.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

### S14 — Slack integration

**Type:** Product documentation  
**Relevant sections:** Supported actions; limitations

One-way posting, channel configuration, no inbound commands.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)

### S15 — Agent guardrail controls

**Type:** Product documentation  
**Relevant sections:** Read/write actions; approval; accuracy

Action-dependent approvals and analytical limitations.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

### S16 — Cross-region inference

**Type:** Product documentation  
**Relevant sections:** Preview storage and inference locations

us-east-1 storage; inference within the originating US geography.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

### S17 — Quotas

**Type:** Product documentation  
**Relevant sections:** Per-agent limits

Resource and context limits remain relevant during preview.

[Open official source](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html)

---

### Reference links

[S01]: https://aws.amazon.com/ai/frontier-agents/ "AWS frontier agents"

[S02]: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html "What is AWS FinOps Agent?"

[S03]: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html "Create an agent"

[S04]: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html "IAM setup guide"

[S05]: https://docs.aws.amazon.com/finops-agent/latest/userguide/chatting-with-finops-agent.html "Chatting with the agent"

[S06]: https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html "Cost inquiry"

[S07]: https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html "Cost anomaly investigation"

[S08]: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html "Automated anomaly response"

[S09]: https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html "Optimization recommendations"

[S10]: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html "Custom cost reporting"

[S11]: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html "Task management"

[S12]: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html "Context files and memory"

[S13]: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html "Jira integration"

[S14]: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html "Slack integration"

[S15]: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html "Agent guardrail controls"

[S16]: https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html "Cross-region inference"

[S17]: https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html "Quotas"