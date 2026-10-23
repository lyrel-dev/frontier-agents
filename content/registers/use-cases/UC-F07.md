---
id: record-use-cases-UC-F07
kind: record
collection: use-cases
product: finops
title: Measure the outcome of an implemented optimization
order: 28
frozen: true
data:
  id: UC-F07
  platform: finops
  group: Anomalies and optimization
  title: Measure the outcome of an implemented optimization
  summary: Measure post-change cost and service behavior within defensible attribution limits.
  delivery: Composed workflow
  cadence: Periodic after change
  availability: Preview service; team process
  inputs: Implemented change record, comparable periods and service indicators.
  output: Measured outcome with attribution limits.
  sections:
  - F-U01
  - F-M01
  - F-08
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - savings measurement
  - post change
  - outcome
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Change owner
  objective: Measure post-change cost and service behavior within defensible attribution limits.
  completion:
  - Before and after periods are comparable.
  - Demand, prices and allocation changes are disclosed.
  - Observed change is not replaced with a prior savings estimate.
  profiles:
  - PR-F-ANALYSIS
  variants: []
  schema_version: 2
  platforms:
  - finops
  legacy_ids:
  - F-UC10
  aliases:
  - Post-change savings measurement
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Establish the implemented change and baseline
    purpose:
      $markdown: field-0006
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0007
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
  - title: Read comparable cost evidence
    purpose:
      $markdown: field-0008
    mechanism: MX-F-QUERY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SOURCES
    effect: Source read
    verification: Reconcile a material result using the same dates, metric, scope and dimensions.
    on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  - title: Assess the measured outcome
    purpose:
      $markdown: field-0009
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0010
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
---

<!-- block: b-8c336115a3f851468ad0 -->
## constraints

<!-- block: b-30d3903df4675a77962a -->
<!-- field: field-0001 -->
A lower bill does not prove the change caused the decrease; traffic, prices and allocation may differ.
<!-- /field -->

<!-- block: b-e32e915685e458ebbac7 -->
## example

<!-- block: b-94964d36d4c958f58ef0 -->
<!-- field: field-0002 -->
Compare the post-change period with a matched baseline and state what cannot be attributed to the change.
<!-- /field -->

<!-- block: b-348f5590a6065e6a9e61 -->
## narrative / 0

<!-- block: b-6f7d97c3d698581f91ca -->
<!-- field: field-0003 -->
An approved optimization has been implemented, and the owner wants to know what changed. Select comparable before-and-after periods and record traffic, pricing, allocation, and service-health differences that could affect the result. Reconcile the costs using the same metric and scope.
<!-- /field -->

<!-- block: b-09c6de1984325919b0ca -->
## narrative / 1

<!-- block: b-8139d525323057239c1f -->
<!-- field: field-0004 -->
Report the observed change together with its attribution limits. A lower bill is not sufficient evidence that the optimization caused the decrease when demand also fell. This is a team measurement workflow using source-backed analysis, not a service guarantee of savings. Unexplained differences remain part of the outcome rather than being removed from the report.
<!-- /field -->

<!-- block: b-65195a3802c05754845e -->
## steps basis

<!-- block: b-21de297281b95a559766 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-73ac8dbeb4dc595c84ab -->
## workflow / 0 / purpose

<!-- block: b-43916d2f79b65ad2a372 -->
<!-- field: field-0006 -->
Confirm deployment and select comparable observation periods.
<!-- /field -->

<!-- block: b-04e8b19cff675b729a48 -->
## workflow / 0 / verification

<!-- block: b-4f4f7edba6ce50ecb84c -->
<!-- field: field-0007 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->

<!-- block: b-580895af28765ec29955 -->
## workflow / 1 / purpose

<!-- block: b-3ec41f12671d58969a3a -->
<!-- field: field-0008 -->
Reconcile values under the same analytical basis.
<!-- /field -->

<!-- block: b-3f15f4b85fda59bba4cd -->
## workflow / 2 / purpose

<!-- block: b-1ce341c9ef815b318e0b -->
<!-- field: field-0009 -->
Account for other changes before attributing the difference.
<!-- /field -->

<!-- block: b-b1508f2bd8de5f519dd7 -->
## workflow / 2 / verification

<!-- block: b-20e6a0faa91c5f4f925a -->
<!-- field: field-0010 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
