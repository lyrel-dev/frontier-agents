---
id: record-use-cases-UC-F05
kind: record
collection: use-cases
product: finops
title: Investigate a cost anomaly
order: 26
frozen: true
data:
  id: UC-F05
  platform: finops
  group: Anomalies and optimization
  title: Investigate a cost anomaly
  summary: Quantify a cost anomaly and assess available evidence for an operational cause.
  delivery: Native analysis with optional automation
  cadence: On demand or supported anomaly event
  availability: Preview
  inputs: Cost Anomaly Detection record, Cost Explorer access and optional CloudTrail permission.
  output: Anomaly explanation with affected services, usage/rate analysis and correlated changes.
  sections:
  - F-M01
  - F-08
  - F-M05
  - F-03
  - F-05
  - F-M06
  constraints: CloudTrail events are correlated activity, not automatic proof of cause.
  example: Investigate the MemoryDB anomaly and separate usage, rate and correlated change evidence.
  keywords:
  - anomaly investigation
  - root cause
  - Cost Anomaly Detection
  narrative:
  - $markdown: field-0001
  - $markdown: field-0002
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: FinOps investigator
  objective: Quantify a cost anomaly and assess available evidence for an operational cause.
  completion:
  - Affected dimensions and monetary contributions reconcile.
  - Change correlation is distinguished from causal evidence.
  - Analysis completion and optional publication status remain separate.
  profiles:
  - PR-F-ANALYSIS
  - PR-F-AUTOMATION
  - PR-F-PUBLICATION
  variants:
  - name: On-demand investigation
    changes: Start from a chosen anomaly and explicit task.
    controls: No event automation is required.
  - name: Event-triggered investigation
    changes: Use the supported anomaly event and managed rule.
    controls: Invocation, queue, analysis and publication are inspected separately.
  schema_version: 2
  platforms:
  - finops
  legacy_ids:
  - F-UC07
  - F-UC08
  aliases:
  - On-demand cost anomaly investigation
  - Event-triggered anomaly response
  steps_basis:
    $markdown: field-0003
  workflow:
  - title: Match a supported anomaly event
    purpose:
      $markdown: field-0004
    mechanism: MX-F-EVENT
    dependency: conditional
    condition: The event-triggered profile is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-AUTOMATIONS
    - FT-F-TASKS
    effect: Task creation; publication is a separate configured step
    verification: Trace event, automation, task, analysis and destination result independently.
    on_failure: Inspect monitor conditions and rule permissions before changing the analytical prompt.
  - title: Create or inspect investigation work
    purpose:
      $markdown: field-0005
    mechanism: MX-F-TASK
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-TASKS
    effect: Execution and output
    verification: Match completed results to task identity and requested scope.
    on_failure: Distinguish absent, queued and failed tasks before retrying.
  - title: Analyze cost and change evidence
    purpose:
      $markdown: field-0006
    mechanism: MX-F-QUERY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SOURCES
    effect: Source read
    verification: Reconcile a material result using the same dates, metric, scope and dimensions.
    on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  - title: Publish to the reviewed channel
    purpose:
      $markdown: field-0007
    mechanism: MX-F-SLACK
    dependency: optional
    condition: A reviewed Slack destination is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SLACK
    effect: External publication
    verification: Review audience before invocation and inspect delivery afterward.
    on_failure:
      $markdown: field-0008
---

<!-- block: b-4d12b370172e57b7b659 -->
## narrative / 0

<!-- block: b-9367b9ccdb615539ae0b -->
<!-- field: field-0001 -->
A cost monitor identifies an unexpected increase. Inspect the anomaly record and query the affected cost dimensions for the relevant period. Where permissions allow, use operational-change records to investigate whether a workload or configuration change explains the increased usage or rate.
<!-- /field -->

<!-- block: b-0088618782ca5de6909a -->
## narrative / 1

<!-- block: b-7a0783fd83cb56c09864 -->
<!-- field: field-0002 -->
Keep numerical attribution and causal evidence separate. A nearby CloudTrail event provides a lead but does not necessarily explain the whole deviation. The final explanation should identify affected costs, supporting observations, and missing inputs. If change evidence is unavailable, preserve the reconciled cost contribution without inventing an operational cause.
<!-- /field -->

<!-- block: b-4af51ccede2c5b859f16 -->
## steps basis

<!-- block: b-829ca320a16e5fc383b8 -->
<!-- field: field-0003 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-5b9ea46e7d8350acb353 -->
## workflow / 0 / purpose

<!-- block: b-71af3bc36697576493f2 -->
<!-- field: field-0004 -->
Create work for the approved monitor and condition.
<!-- /field -->

<!-- block: b-0ddb82d1836658299bbb -->
## workflow / 1 / purpose

<!-- block: b-0365a7832e1e543b8739 -->
<!-- field: field-0005 -->
Retain the execution independently of its trigger.
<!-- /field -->

<!-- block: b-1a6d66a3ebe2539f89d4 -->
## workflow / 2 / purpose

<!-- block: b-72da230579da5cffaae3 -->
<!-- field: field-0006 -->
Quantify contributions and assess the supported explanation.
<!-- /field -->

<!-- block: b-d002e21fadc55737aa3b -->
## workflow / 3 / purpose

<!-- block: b-cae22ec8d6b0553b9994 -->
<!-- field: field-0007 -->
Deliver the permitted summary to the appropriate audience.
<!-- /field -->

<!-- block: b-4fc37350f869528c8585 -->
## workflow / 3 / on failure

<!-- block: b-4ad54f134f23581a9757 -->
<!-- field: field-0008 -->
Keep analysis completion separate from delivery failure; posting does not establish channel-reading capability.
<!-- /field -->
