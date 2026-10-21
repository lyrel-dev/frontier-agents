# AWS FinOps Agent — capability evidence record

Scope revision: 2026-10-21-three-agent-scope. This is a filtered record of the previously reviewed official evidence, not a new external documentation audit. Earlier editions are available through Git history.

## Current capability records

## C01 · Explain cost changes by service, account, Region, or tag

**Documented function:** Ask for cost breakdowns, comparisons, and trends using the supported dimensions available through the agent’s data sources.

**Availability:** Preview · us-east-1

**Prerequisites:** Create the agent and operator roles, enable relevant cost services, and establish the account scope you intend to analyze.

**Limitations:** Results depend on source access and the chosen time range, granularity, filters, and cost basis. An inaccessible data source cannot be inferred from a fluent answer.

**Proposed verification:** Reproduce one material total in the source console with matching dates and filters before using the explanation.

- [S06 · Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

- [S03 · Create an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

- [S04 · IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

## C02 · Inspect forecasts and commitment coverage

**Documented function:** Cost inquiry includes forecasts and Savings Plans or Reserved Instance coverage, utilization, and recommendation questions.

**Availability:** Preview · us-east-1

**Prerequisites:** Grant the relevant billing-data permissions and identify the accounts, period, and workload assumptions.

**Limitations:** A forecast is not a budget guarantee or a purchase instruction. Commitment decisions need independent workload and financial review.

**Proposed verification:** Check forecast assumptions, coverage definitions, and workload stability; do not purchase based only on the generated summary.

- [S06 · Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

- [S04 · IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

## C03 · Investigate a cost anomaly with operational context

**Documented function:** Analyze cost drivers and distinguish likely usage or rate changes; CloudTrail access can add evidence about relevant operational events.

**Availability:** Preview · us-east-1

**Prerequisites:** Provide the anomaly or precise account/service/time window and grant only the additional read access needed.

**Limitations:** Correlation is investigative, not proof of causation. Missing audit access or mismatched timestamps can limit the explanation.

**Proposed verification:** Validate the leading explanation against usage metrics, the deployment record, and the same billing interval.

- [S07 · Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)

- [S15 · Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## C04 · Prioritize existing optimization recommendations

**Documented function:** Retrieve and filter recommendations from Cost Optimization Hub and Compute Optimizer by useful engineering criteria such as service, account, effort, or estimated savings.

**Availability:** Preview · us-east-1

**Prerequisites:** Enable and authorize the relevant recommendation sources; provide workload ownership and operational constraints.

**Limitations:** The agent summarizes those systems’ recommendations; it is not a separate optimizer and does not implement resource changes.

**Proposed verification:** Check utilization, reliability constraints, overlapping savings estimates, and the recommendation’s source date.

- [S09 · Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

- [S15 · Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## C05 · Generate a report for engineering or leadership

**Documented function:** Create cost reports with charts and narrative in HTML, PDF, or editable PowerPoint format, then request revisions.

**Availability:** Preview · us-east-1

**Prerequisites:** Define the audience, period, cost basis, dimensions, and output format. Provide a template only in a supported context format.

**Limitations:** Generated charts and interpretation need review. Output formats do not imply that PDF or PowerPoint files are accepted as context uploads.

**Proposed verification:** Reconcile totals, chart labels, periods, and ownership; distinguish estimated savings from realized savings.

- [S10 · Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

- [S12 · Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

## C06 · Turn a request into a tracked on-demand task

**Documented function:** Explicitly requested on-demand tasks appear in the task queue alongside scheduled and event-driven work, with execution history.

**Availability:** Preview · us-east-1

**Prerequisites:** Specify that the request should become a task and define the expected output and connected destination.

**Limitations:** An ordinary chat question does not automatically become a tracked task. External actions have their own approval rules.

**Proposed verification:** Confirm task creation and output, and inspect the history for failed tools, missing data, and external actions.

- [S11 · Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

## C07 · Schedule recurring cost reports and reviews

**Documented function:** Create recurring tasks in natural language and manage their configuration, status, and recorded runs through Automations.

**Availability:** Preview · us-east-1

**Prerequisites:** Agree on a report owner, cadence, recipient scope, and stop conditions before enabling the automation.

**Limitations:** Scheduled external actions can be pre-authorized. Recurrence does not establish that a report’s recipients or data remain appropriate over time.

**Proposed verification:** Inspect the stored schedule and first output, then disable or revise jobs that produce noise or outdated context.

- [S11 · Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

- [S10 · Custom cost reporting](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

- [S15 · Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## C08 · Trigger a workflow from a cost-anomaly event

**Documented function:** An event-based automation can investigate a matching Cost Anomaly Detection event and produce configured outputs or handoffs.

**Availability:** Preview · us-east-1

**Prerequisites:** Configure a cost-anomaly monitor, suitable trigger conditions, and approved output destinations; scope the automation role.

**Limitations:** During preview the supported event type is cost anomaly, not arbitrary deployment or custom events. Existing monitors and EventBridge permissions are required.

**Proposed verification:** Validate event matching, duplicate handling, output visibility, and the automation’s disabled state before broader rollout.

- [S08 · Automated anomaly response](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

- [S04 · IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

## C09 · Supply account ownership and reporting context

**Documented function:** Upload account-to-team mappings, cost categories, instructions, and report-format guidance using the documented text-based file types.

**Availability:** Preview · us-east-1

**Prerequisites:** Use reviewed TXT, CSV, JSON, Markdown, HTML, or YAML files; prefer team identifiers over personal details.

**Limitations:** Files are visible to everyone with agent access and should not contain sensitive or personal information. PDF and PPTX are not accepted context-file types.

**Proposed verification:** Check mappings against the authoritative inventory and review who can access the agent before uploading.

- [S12 · Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

- [S17 · Quotas](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html)

## C10 · Correct recurring preferences through memory

**Documented function:** Tell the agent to remember, update, or forget preferences and corrections that affect later work.

**Availability:** Preview · us-east-1

**Prerequisites:** Keep authoritative ownership and policy in maintained sources and review remembered preferences after organizational changes.

**Limitations:** Memory is distinct from uploaded files; the agent cannot modify or delete context files through conversation. Long conversations can be summarized.

**Proposed verification:** Ask a fresh scoped question to confirm the correction took effect without overwriting the authoritative context source.

- [S12 · Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

## C11 · Create Jira Cloud issues and follow-up comments

**Documented function:** Create Jira issues, add comments to agent-created issues, and read supported issue fields through a connected project.

**Availability:** Preview · us-east-1

**Prerequisites:** Connect Jira Cloud and the intended project to the agent, then review project defaults, permissions, and issue visibility.

**Limitations:** Jira Server/Data Center is not supported. The agent does not set assignee, priority, or status; ownership relies on Jira defaults or rules. Interactive/on-demand writes require approval; automated writes are pre-authorized.

**Proposed verification:** Confirm the approval behavior for the chosen path and inspect the actual issue assignment and contents in Jira.

- [S13 · Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

- [S15 · Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## C12 · Post cost updates to a connected Slack channel

**Documented function:** Post analysis or reporting updates to an authorized connected Slack channel.

**Availability:** Preview · us-east-1

**Prerequisites:** Install and connect the app, join the destination channel as required, and verify the account/workspace and per-agent channel configuration.

**Limitations:** The integration is one-way: it does not read channel conversations or accept mentions as commands. Posting does not require per-message approval.

**Proposed verification:** Confirm the destination and audience first; inspect task history and the delivered message afterward.

- [S14 · Slack integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)

- [S15 · Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## C13 · Turn a recommendation into a controlled engineering change

**Documented function:** A practical engineering workflow is to turn a reviewed recommendation into a normal change ticket, validate the change, and compare later costs.

**Availability:** Preview · us-east-1 · team-owned follow-through

**Prerequisites:** Choose one low-risk opportunity with an owner, baseline, operational acceptance tests, approval, and a recovery plan.

**Limitations:** The agent is not documented as autonomously resizing resources, deleting assets, or buying commitments. Implementation and rollback remain team responsibilities.

**Proposed verification:** Compare matched periods and workload levels after the independently approved change; account for regressions and implementation cost.

- [S09 · Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

- [S13 · Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

- [S15 · Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

## Boundary

No live AWS account, workflow, penetration test or cost action was exercised in this scope revision.
