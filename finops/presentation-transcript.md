# AWS FinOps Agent: presentation transcript

Total 31:30, including 8:00 prepared-result demonstrations. No service-completion-time guarantee. Questions, preparation and live setup are additional.

## 1. Keep source data, explanation and action separate

0:00–1:00; allocation 1:00

The service retrieves and interprets cost information; it does not make every explanation or recommendation an established fact.

| Source data | Analysis | External effect |
|---|---|---|
| Billing and optimization service responses | Scoped explanation, report or recommendation summary | Jira issue/comment or Slack publication |

### Presenter notes

The entire service remains preview. The presentation follows the data from its source to a reviewable result and then to a separately controlled publication. Cost Explorer supplies billing data; Cost Optimization Hub and Compute Optimizer supply optimization recommendations. A recommendation, forecast and actual saving are different kinds of information and must remain visibly distinct.

Official documentation: [What is AWS FinOps Agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 2. The functional map follows the source of truth

1:00–3:00; allocation 2:00

Do not turn categories of recommendations into invented agent optimization engines.

| Area | Operations | Authoritative source or object |
|---|---|---|
| Billing inquiry | Historical spend; forecast; commitments | Cost Explorer and permitted billing tools |
| Investigation | Compare periods; analyze anomaly | Scoped source data and detector event |
| Recommendation access | Filter and contextualize candidates | Cost Optimization Hub / Compute Optimizer |
| Delivery | Generate artifact; execute task | Task activities and generated artifact |
| Publishing | Create/comment in Jira; post to Slack | Actual issue, comment or channel message |

### Presenter notes

This map separates functions by what they operate on and return. An anomaly event comes from a detector; the agent investigates it. A rightsizing candidate comes from an optimization source; the agent can summarize it. Report generation changes representation, not the underlying numbers. Publication is an external write whose result should be checked in the destination.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html) · [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html) · [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 3. A cost comparison starts with a query contract

3:00–5:30; allocation 2:30

Reconciliation is impossible until the scopes match.

| Specify | Failure if omitted | Check |
|---|---|---|
| Accounts and filters | A different population of spend | Match the source-console selection |
| Periods and granularity | Unequal intervals or mixed cutoffs | Identify start/end and incomplete periods |
| Cost metric and currency | Different bases compared as equal | Retain the exact metric and units |
| Dimensions and owner mapping | Unallocated spend silently disappears | Include unknown/unallocated groups |

### Presenter notes

Use this contract before requesting an explanation. An increase may result from a different query rather than a change in the workload. This is why a chart or executive summary is not the first artifact to inspect. Reconcile the overall total and one material contributor against the same source settings, then investigate the remaining difference.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) · [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)


## 4. Worked example: 200 becomes 244

5:30–8:00; allocation 2:30

Synthetic teaching data: the 44 increase can be reconciled without claiming why it occurred.

| Component | Baseline | Current | Delta |
|---|---|---|---|
| Compute | 1,000 × 0.10 = 100 | 1,200 × 0.12 = 144 | +44 |
| Storage | 5,000 × 0.02 = 100 | 5,000 × 0.02 = 100 | 0 |
| Total | 200 | 244 | +44 / +22% |

Invented quantities and rates. Not AWS pricing, billing records or a measured agent result.

### Presenter notes

Compute the totals explicitly. Under the quantity-first convention, the quantity contribution is 200 additional units times the old rate, or 20. The rate contribution is the new quantity times the rate increase, or 24. The contributions total 44. Other conventions can allocate the interaction term differently. The numbers establish the decomposition, not whether a deployment or discount change caused it. A total-only fixture could not establish this split.

## 5. Anomaly detection is not causal proof

8:00–10:30; allocation 2:30

Trace the suspected cause to the affected resource and changed usage.

| Detector event | Cost contributors | Candidate change | Causal check |
|---|---|---|---|
| Anomaly ID, monitor and affected interval | Returned account/service/region dimensions | CloudTrail or deployment event, if accessible | Did this event change this resource's measured usage? |

A correlated event is a hypothesis. Missing CloudTrail evidence is not proof that no change occurred.

### Presenter notes

Keep the anomaly amount separate from the broader period comparison. If a deployment occurs near the increase, test whether the increase preceded it or affected resources outside its scope. If the required source is unavailable, report the gap. The agent's investigative explanation is a starting point for the owner, not a definitive billing-causality verdict.

Official documentation: [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html) · [Event-triggered anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 6. Four numbers with different meanings

10:30–12:30; allocation 2:00

Measured cost, forecast and recommendation estimates have different meanings.

| Number | Meaning | Decision boundary |
|---|---|---|
| Actual cost | Source billing observation under a defined scope | Reconcile the metric and cutoff |
| Forecast | Source model's estimate for a future interval | Retain horizon and available uncertainty |
| Estimated savings | Source recommendation under assumptions | Validate feasibility; avoid overlapping alternatives |
| Realized savings | Post-change measurement with matched scope | Control for demand and workload changes |

### Presenter notes

Realized savings is a proposed measurement the team performs after an approved change, not a field inferred from a recommendation. A forecast is not a budget authorization. For commitments, coverage and utilization answer different questions: eligible usage covered versus purchased commitment used. A purchase decision needs explicit demand and term assumptions, not simply a desire to increase one percentage.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 7. Source recommendations need owner review

12:30–15:00; allocation 2:30

The agent contextualizes source-service recommendations; engineering owns implementation and measurement.

| Inspect | Why it matters | Do not assume |
|---|---|---|
| Source record and date | Recommendations depend on observed workload | The newest chat answer means new source analysis |
| Proposed change | Shows the actual change being proposed | A generic 'save money' summary is implementable |
| Overlapping alternatives | Prevents double-counted estimates | Every listed estimate can be added |
| Workload constraints | Establishes feasibility for this workload | Low utilization guarantees safe downsizing |

### Presenter notes

Open the underlying recommendation before drafting work. Ask the workload owner whether the observed period included peak load and relevant redundancy constraints. Reject unsupported candidates rather than creating a large unowned backlog. The agent does not resize resources or buy commitments through the documented publishing actions. The subsequent engineering change should have its own authorization and regression plan.

Official documentation: [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 8. Context and memory do not change billing records

15:00–17:00; allocation 2:00

Owner mappings and reporting preferences must not silently alter measured totals.

| Mechanism | Who changes it | Lifecycle |
|---|---|---|
| Context file | User through Context files | Read-only to agent; soft-delete/restore |
| Memory | Remember/update/forget through Chat | Persists preferences and corrections per agent |
| Conversation summary | Automatic context-window management | Not the same as durable cross-session memory |
| Task/conversation record | Service record of execution | No individual deletion during documented preview |

### Presenter notes

Use a mapping example with a known account and an unknown account. The unknown one must remain visible and its cost must remain in the total. Context files are visible to users with access to the agent; they should not carry sensitive personal information. A correction can affect later interpretation, but it does not rewrite the underlying billing data or establish a model-training mechanism.

Official documentation: [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html) · [Data protection and deletion lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)


## 9. A task is one run; an automation creates runs

17:00–19:00; allocation 2:00

Cancelling current work and stopping future work are separate operations.

| Definition | Trigger | Task | Result |
|---|---|---|---|
| Instructions and allowed destinations | Schedule or supported cost-anomaly event | Activity, state, approvals and artifacts | Reviewed report or external delivery |

Disable the automation for future runs; cancel an already-running task separately.

### Presenter notes

Test the analysis as an on-demand task before making it recurring. For event automation, confirm the existing monitor, matching conditions and required EventBridge permissions. A task can fail because of missing source access or an expired publishing credential. The operational owner must inspect those failures; a schedule is not a guarantee that the intended report arrived or was complete.

Official documentation: [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html) · [Event-triggered anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html) · [Web application and feedback](https://docs.aws.amazon.com/finops-agent/latest/userguide/how-do-i-interact-with-the-agent.html) · [Data protection and deletion lifecycle](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)


## 10. Publishing controls are action-specific

19:00–21:30; allocation 2:30

Do not describe all writes as requiring approval.

| Action | Chat / on-demand task | Scheduled / event task |
|---|---|---|
| Create Jira issue | Approval required | Pre-authorized at setup |
| Add Jira comment | Approval required | Pre-authorized at setup |
| Post to Slack | No per-message approval | No per-message approval |
| Resize / buy commitments | Not a documented publishing action | Not made available by automation |

Jira cannot set assignee/priority/status here. Slack is posting-only during preview.

### Presenter notes

The account-level OAuth integration and the per-agent project or channel connection are both required. A Jira owner in a context file does not make the integration an assignee editor. Slack does not accept commands or respond to mentions through this preview connection. Review destination audience before enabling unattended publication; waiting for Jira approval does not hold back a separate Slack post.

Official documentation: [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) · [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html) · [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 11. Demonstration: reconcile before explaining

21:30–26:30; allocation 5:00

Use the synthetic fixture for arithmetic and prepared source evidence for interpretation.

| Minutes | Action |
|---|---|
| 1 | Show the comparison contract and clearly labeled synthetic input table. |
| 1 | Recalculate baseline/current totals and the absolute and percentage delta. |
| 1 | Compute a quantity/rate decomposition and state its convention. |
| 1 | Contrast the arithmetic with the additional evidence needed for a deployment-cause claim. |
| 1 | Inspect a prepared report for scope, residual and uncertainty labels. |

Fallback: Use the supplied arithmetic fixture. It demonstrates reconciliation only; it is not AWS billing data, service pricing or a live agent result.

### Presenter notes

Follow the five one-minute steps. The fixture is deliberately small so the audience can verify the calculation rather than trust a generated summary. State clearly that it is not a live billing query. Then show how a report should carry query scope, remaining residual and causal uncertainty. A deployment-cause conclusion requires evidence beyond the fixture.

Official documentation: [Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html) · [Cost anomaly detection and investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 12. Demonstration: recommendation to reviewable work

26:30–29:30; allocation 3:00

A ticket is a proposed change, not achieved savings.

| Minutes | Action |
|---|---|
| 1 | Inspect a prepared recommendation and identify one overlapping alternative. |
| 1 | Review a draft issue, project defaults and the interactive approval boundary. |
| 1 | Contrast estimated savings with the future measurement required after an independently approved deployment. |

Fallback: Use a prepared recommendation and draft issue; do not create a real ticket unless the connected project and operator authorization are explicitly available.

### Presenter notes

Inspect one prepared recommendation and one overlapping alternative. Review the draft issue and identify fields that the integration cannot set. Show the approval boundary using a prepared example unless an authorized test project is actually connected. End with the measurement required after engineering independently approves and deploys the change.

Official documentation: [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 13. Acceptance requires a traceable numerical result

29:30–31:30; allocation 2:00

A useful cost report makes both the arithmetic and the remaining uncertainty inspectable.

| Required evidence | Owner decision | Stop condition |
|---|---|---|
| Matched source-query scope | Are the totals comparable? | Unknown metric or incomplete period |
| Contributors plus residual | What is explained versus hypothesized? | Usage/rate claims without data |
| Recommendation ID and assumptions | Is the change feasible? | Overlapping or stale estimates |
| Actual destination record | Was the intended result published? | Unapproved audience or failed delivery |

### Presenter notes

Close by asking which operational decision the report enables. If it cannot identify the cost scope, the evidence for a driver or the owner of a proposed change, more generated prose will not help. The complete reference contains configuration and lifecycle instructions. No savings, accuracy or productivity outcome has been measured for this documentation, and questions are outside the timed session.

Official documentation: [Action-specific guardrails and accuracy limits](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html) · [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html) · [Jira connection and supported actions](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html) · [One-way Slack publishing](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)

