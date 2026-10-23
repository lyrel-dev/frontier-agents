---
id: record-use-cases-UC-D06
kind: record
collection: use-cases
product: devops
title: Assess and report service health and trends
order: 5
frozen: true
data:
  id: UC-D06
  platform: devops
  group: Operational reporting
  title: Assess and report service health and trends
  summary: Produce a sourced health assessment or comparable-period report.
  delivery: Native inquiry or configured reporting
  cadence: On demand or scheduled
  availability: Selected native or custom-agent path; inspect feature-specific eligibility
  inputs:
    $markdown: field-0001
  output: Sourced health snapshot, period comparison or trend report.
  sections:
  - D-01
  - D-05
  - D-12
  - D-07
  - D-M07
  - D-03
  - D-M01
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - health
  - metrics
  - logs
  - alarms
  - on demand
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: On-call or service engineer
  objective: Produce a sourced health assessment or comparable-period report.
  completion:
  - Service dimensions and observation periods are explicit.
  - Material measurements reconcile with source queries.
  - Missing data and workload-mix changes are disclosed.
  profiles:
  - PR-D-QUERY
  - PR-D-REPORT
  - PR-EVIDENCE
  variants:
  - name: Current snapshot
    changes: A bounded recent observation of the selected service.
    controls: An unavailable source is a gap, not a healthy measurement.
  - name: Period or trend comparison
    changes: Compare complete periods under the same dimensions and aggregation.
    controls: Check denominator, traffic composition and source completeness.
  - name: Recurring service report
    changes: Run a reviewed definition repeatedly.
    controls: Schedule, observation window and destination remain separate settings.
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC06
  - D-UC08
  - D-UC19
  aliases:
  - On-demand service health query
  - Daily or weekly service health report
  - Metrics and error trend analysis
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Retrieve comparable measurements
    purpose:
      $markdown: field-0007
    mechanism: MX-D-READ
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SOURCES
    effect: Source read
    verification: Compare returned identifiers and a material measurement with the original source.
    on_failure: Report the failed read and withhold conclusions that require that source.
  - title: Answer a native health inquiry
    actor: Service execution; accountable engineer reviews the result
    purpose:
      $markdown: field-0008
    mechanism: MX-D-QUERY
    dependency: conditional
    condition: The built-in conversational snapshot profile is selected.
    configuration_features:
    - FT-D-QUERY
    - FT-D-SOURCES
    effect: Source read and conversational result
    verification: Inspect scope and reproduce a material observation from the same source query.
    on_failure:
      $markdown: field-0009
  - title: Interpret retained service context
    purpose:
      $markdown: field-0010
    mechanism: MX-D-RECALL
    dependency: optional
    condition: The report uses maintained service context.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-MEMORY
    effect: Context read
    verification:
      $markdown: field-0011
    on_failure:
      $markdown: field-0012
  - title: Run the reporting definition
    purpose:
      $markdown: field-0013
    mechanism: MX-D-CUSTOM
    dependency: conditional
    condition: A configured snapshot, comparison or recurring-report profile is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-CUSTOM
    - FT-D-HISTORY
    effect: Execution and output
    verification: Inspect tool arguments, failures and output against the task scope.
    on_failure: Mark incomplete output and resolve the failed prerequisite before repeating the run.
  - title: Create recurring invocations
    purpose:
      $markdown: field-0014
    mechanism: MX-D-SCHEDULE
    dependency: conditional
    condition: Recurring execution of the configured reporting profile is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SCHEDULE
    - FT-D-HISTORY
    effect: Future invocation
    verification: Inspect saved timing and actual start; record the observation window independently.
    on_failure:
      $markdown: field-0015
---

<!-- block: b-1041643149075338ae60 -->
## inputs

<!-- block: b-dfd2c2d2063e5441b21c -->
<!-- field: field-0001 -->
Service identity, complete periods, selected telemetry tools and report instructions; optional relevant context.
<!-- /field -->

<!-- block: b-2fca7d011e8157ada660 -->
## constraints

<!-- block: b-8d38701f74af5ba1af5b -->
<!-- field: field-0002 -->
A conversational health answer does not replace monitoring or prove complete signal coverage.
<!-- /field -->

<!-- block: b-784c392a14ad5c8eaddd -->
## example

<!-- block: b-9cc8db56fca0566b8b4b -->
<!-- field: field-0003 -->
Report service health for the declared period and comparison basis, showing material changes and unavailable signals.
<!-- /field -->

<!-- block: b-a32b31f7a6585657994e -->
## narrative / 0

<!-- block: b-8493e3161b665bddb2f2 -->
<!-- field: field-0004 -->
The incoming engineer needs to know whether the service is healthy, what changed, and which observations are missing. Define the service scope and reporting period first. Retrieve the selected measurements, compare significant differences with a baseline when needed, and connect material observations to incident and deployment evidence. A recent snapshot and a multiweek trend are analytical profiles of the same reporting objective.
<!-- /field -->

<!-- block: b-677485b0d2b4577b9dc5 -->
## narrative / 1

<!-- block: b-bd5d805ace5f54fd9a9a -->
<!-- field: field-0005 -->
Review a material measurement against its source before relying on the report. Keep missing telemetry visible and consider workload changes before interpreting a trend. Recurrence preserves the agreed reporting basis; it does not create a different objective. An operational review can subsequently use this report to decide priorities and owners.
<!-- /field -->

<!-- block: b-b7dd90a701e559909938 -->
## steps basis

<!-- block: b-c8660e9269c85d05a895 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-2cc9943fade6546d8c08 -->
## workflow / 0 / purpose

<!-- block: b-d5684f775479551bb54e -->
<!-- field: field-0007 -->
Read logs, metrics and incidents under one reporting basis.
<!-- /field -->

<!-- block: b-94d1220119df5b3ea80c -->
## workflow / 1 / purpose

<!-- block: b-ea44c42edcaa5f56ac8b -->
<!-- field: field-0008 -->
Use the built-in query path for the native snapshot profile.
<!-- /field -->

<!-- block: b-50926b34e27d50e5a268 -->
## workflow / 1 / on failure

<!-- block: b-6162a5e2763051639b74 -->
<!-- field: field-0009 -->
Name the missing source and qualify or withhold the answer; creating a custom agent does not by itself repair source access.
<!-- /field -->

<!-- block: b-28c94c1104ad55498a40 -->
## workflow / 2 / purpose

<!-- block: b-87ccba169d1b5b678ab5 -->
<!-- field: field-0010 -->
Resolve known mappings or relationships when relevant.
<!-- /field -->

<!-- block: b-264c998de10a555487df -->
## workflow / 2 / verification

<!-- block: b-c9c8b53b6f1b5a788a2c -->
<!-- field: field-0011 -->
Distinguish entry existence, observable retrieval and correctness against current evidence.
<!-- /field -->

<!-- block: b-71d4a82636f45991b7e5 -->
## workflow / 2 / on failure

<!-- block: b-2bd15b2f324a50a793b4 -->
<!-- field: field-0012 -->
Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.
<!-- /field -->

<!-- block: b-4437cd4a583f565293b6 -->
## workflow / 3 / purpose

<!-- block: b-48d1819144765d388a1a -->
<!-- field: field-0013 -->
Produce the configured snapshot, comparison or trend report.
<!-- /field -->

<!-- block: b-fdd9ed3040ef59dc9174 -->
## workflow / 4 / purpose

<!-- block: b-660a95164dd35260a93a -->
<!-- field: field-0014 -->
Repeat the reporting contract without changing its basis.
<!-- /field -->

<!-- block: b-8352a9d1ea6055299bd8 -->
## workflow / 4 / on failure

<!-- block: b-9a12e6999cd951d0b1f0 -->
<!-- field: field-0015 -->
Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.
<!-- /field -->
