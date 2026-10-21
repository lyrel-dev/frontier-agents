# AWS FinOps Agent — presentation transcript

27 minutes including 7 minutes of demonstrations. Questions and breaks are additional. Demo budgets are walkthrough allocations, not agent completion guarantees.


## 01. AWS FinOps Agent

**00:00–00:45 · 00:45 allocated**

**Takeaway:** Turn a cost question into reproducible evidence and owned engineering work.

The entire FinOps Agent service remains preview. This presentation focuses on the daily engineering value: cost explanation, anomaly investigation, recommendation triage and reporting. It does not grant infrastructure or purchasing authority. The illustrative storage-cost demo uses synthetic numbers to teach reconciliation; it is not an account result or a measured saving.

[F02 — What is AWS FinOps Agent?](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

[F16 — Cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)


## 02. Use case · explain a 41% storage-cost increase

**00:45–02:00 · 01:15 allocated**

**Takeaway:** A useful answer separates observed movement, likely drivers and unresolved uncertainty.

Use two complete 14-day periods and the same account, Region and cost basis. The 41 percent figure is an illustrative calculation used in the demo, not a real anomaly from the user’s account. Determine which service or usage type moved before proposing a cause. CloudTrail correlation can inform a hypothesis when access is configured, but time proximity alone does not establish causality.

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[F07 — Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)


## 03. Six practical capability families

**02:00–03:30 · 01:30 allocated**

**Takeaway:** The service helps analyze and route work; it does not apply resource changes.

The capability map is an analytical workflow: understand spend, investigate anomalies, retrieve optimization opportunities, produce reports, run tasks and route results. All are within the preview service. Recommendation output comes from connected cost-management sources and must not be presented as a second independent optimizer or a completed change. The native collaboration writes are explicit and limited.

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[F07 — Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

[F10 — Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 04. Data permissions determine analytical depth

**03:30–05:00 · 01:30 allocated**

**Takeaway:** Context adds business meaning; it does not grant access to missing sources.

Create the agent and operator access paths and activate the cost services needed for the pilot. Cost Explorer supplies cost and usage views; anomaly and optimizer services provide their own evidence. CloudTrail access can add change context. If a source is not permitted, the corresponding analytical depth is unavailable. The account-to-owner mapping is interpretive context, not a permission policy.

[F03 — Create an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

[F04 — IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[F07 — Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)


## 05. Cost inquiry needs a reproducible question

**05:00–06:30 · 01:30 allocated**

**Takeaway:** Acceptance: reconcile one material total using identical source filters.

A cost narrative is only reproducible when the time range, grouping, filters and cost basis are explicit. Choose complete periods for the demonstration to avoid treating a partial day as a trend. Reconcile at least one material total in the source view before sharing a report. Do not use an account-specific answer outside its documented scope.

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)


## 06. Forecasts and commitments inform a decision

**06:30–07:45 · 01:15 allocated**

**Takeaway:** Acceptance: a forecast is not a guaranteed bill, and a recommendation is not a purchase.

This capability helps the team understand expected spend and current commitment usage. Make the analysis period and assumptions visible. A recommendation may reflect a source service’s model and eligibility rules, and it still requires review against business constraints. Keep purchasing decisions with the authorized finance or platform owner. No commitment purchase is demonstrated here.

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)


## 07. Investigate an anomaly without overstating cause

**07:45–09:15 · 01:30 allocated**

**Takeaway:** Acceptance: label correlated changes as hypotheses until the causal mechanism is verified.

An anomaly investigation should answer what moved and how much before answering why. Higher usage, higher rates and mixed effects lead to different actions. When CloudTrail is available, compare candidate events with the service and cost timeline. A nearby change can be relevant without being the cause. Capture what additional evidence would distinguish the leading hypotheses.

[F07 — Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)


## 08. Demo · reconcile the storage-cost anomaly

**09:15–16:15 · 07:00 allocated**

**Takeaway:** Work from a labeled synthetic fixture, then demonstrate the source-reconciliation method.

The bundled synthetic fixture has fourteen baseline rows at $100 each, totaling $1,400, and fourteen comparison rows at $141 each, totaling $1,974. The difference is $574, or 41%. It deliberately contains no account, usage-type, quantity or rate breakdown, so it supports arithmetic reconciliation only—not driver attribution or a causal conclusion. These figures are invented for instruction. For an authorized real analysis, use matching date windows, filters and cost basis, then obtain the additional breakdown and event evidence. Any real Jira write still requires the configured approval.

**Preflight:** Use sanitized authorized cost access or the bundled synthetic fixture. Any real Jira write needs the configured confirmation.

```text

For authorized real data, compare storage costs for the selected accounts over two complete 14-day windows using the same unblended basis. Identify leading drivers only where breakdown evidence is available, separate usage from rate effects, and label correlated CloudTrail changes as hypotheses. For the bundled synthetic fixture, reconcile the $1,400 and $1,974 totals only; do not invent drivers. Do not modify infrastructure.

```

- 01:00 — **Set the query contract:** Fix complete periods, account scope, service grouping and basis.

- 01:30 — **Reconcile the totals:** Use the synthetic period totals for arithmetic; inspect driver breakdowns only with matching authorized data.

- 01:30 — **Separate effects:** Inspect usage and rate evidence instead of inferring from spend alone.

- 01:30 — **Challenge causality:** Compare a candidate change with evidence and alternative explanations.

- 01:30 — **Create the handoff:** Draft an owned follow-up and inspect the Jira confirmation boundary.

**Success:** A reproducible explanation and a bounded next step; no infrastructure mutation or claimed realized savings.

**Fallback:** The included fixture is sufficient to teach the method offline; it must remain visibly labeled synthetic.

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[F07 — Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

[F13 — Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)


## 09. Prioritize existing optimization recommendations

**16:15–17:45 · 01:30 allocated**

**Takeaway:** Acceptance: estimated monthly savings are not realized savings; the team executes changes separately.

The agent makes optimizer results easier to triage. Select reversible opportunities that fit the team’s operational constraints rather than sorting only by the largest estimate. Check utilization evidence, performance requirements and existing commitments. The generated ticket is the start of an engineering process. Measure results after an approved change using a comparable period, and do not double-count overlapping recommendations.

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)


## 10. Generate reports for a specific audience

**17:45–19:00 · 01:15 allocated**

**Takeaway:** Acceptance: every headline number retains its period, filters and cost basis.

An engineering report should emphasize owned resources and next actions; a leadership report may emphasize the overall trend and decisions required. The native report formats support those audiences, but visual polish does not verify the arithmetic. Reconcile key totals before distributing the artifact and make assumptions visible. Reports generated by the service are distinct from this documentation package.

[F10 — Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)


## 11. Tasks make work and history inspectable

**19:00–20:15 · 01:15 allocated**

**Takeaway:** Acceptance: inspect the first runs and disable a cadence that produces noise or stale information.

A task is useful when the team needs an inspectable execution record rather than a one-off chat answer. Begin with a report whose source totals have already been reconciled. Give the schedule an owner and a review cadence. A recurring task can continue producing misleading output if its context or source access changes, so inspect failures and data drift.

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 12. Anomaly-event automation needs an explicit trigger

**20:15–21:45 · 01:30 allocated**

**Takeaway:** Acceptance: this documented trigger is not a general automation engine for every cost threshold.

The event-driven workflow builds on Cost Anomaly Detection and an EventBridge rule. The prompt describes the response; the actual monitor and event configuration determine when it runs. Review the generated automation and its destination. Scheduled and event-based Jira actions can be pre-authorized at setup, so enablement is itself an approval decision rather than an expectation of a confirmation prompt for every run.

[F08 — Automated anomaly response](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 13. Context files and memory make reporting team-specific

**21:45–23:00 · 01:15 allocated**

**Takeaway:** Business context is interpretive guidance—not access control or an authoritative ledger.

Upload a reviewed account-to-team mapping and the reporting conventions the organization actually uses. Context files are read-only from the agent’s perspective; update the source through the supported management path. Memory can retain preferences, but stale or incorrect preferences need correction. Do not upload secrets or assume an owner field in a context file can change a Jira assignee automatically.

[F12 — Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)


## 14. Collaboration approval depends on action and trigger

**23:00–24:30 · 01:30 allocated**

**Takeaway:** Do not assume every outbound write prompts for confirmation.

The supported external writes are constrained. Jira issue and comment actions started in chat or on-demand require confirmation; the same actions can be pre-authorized in scheduled or event-based automations. Slack posting does not require a per-message approval prompt. The Slack integration is outbound rather than a channel command bot. Jira support is not general workflow administration and does not allow arbitrary assignee or status updates.

[F13 — Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

[F14 — Slack integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 15. Preview governance is part of the workflow

**24:30–25:45 · 01:15 allocated**

**Takeaway:** Approve storage, inference and destination boundaries before uploading organizational context.

The preview stores agent data in us-east-1 and can use inference within the originating US geography. Storage location and inference location are different questions. An organization must also approve the content sent to Jira or Slack. Keep role and integration scope narrow and account for underlying service/API consumption. This is a readiness recommendation, not legal or financial advice.

[F03 — Create an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

[F04 — IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

[F16 — Cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)


## 16. Measure reconciled analysis and verified follow-through

**25:45–27:00 · 01:15 allocated**

**Takeaway:** Accepted cost work is the outcome; estimated savings are only an input.

Begin with one account group and a known owner. Reconcile an analysis before automating it, investigate a representative anomaly, and send one approved recommendation through the team’s normal change process. Measure reviewer effort, accepted explanations, duplicate or noisy tickets and any independently observed post-change result. The presentation contains all 13 capability entries through the crosswalk below. Questions follow the timed close.

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)
