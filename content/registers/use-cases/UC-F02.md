---
id: record-use-cases-UC-F02
kind: record
collection: use-cases
product: finops
title: Review a cost forecast
order: 23
frozen: true
data:
  id: UC-F02
  platform: finops
  group: Planning and commitments
  title: Review a cost forecast
  summary: Review a projection for an explicit horizon and assumptions.
  delivery: Native function
  cadence: On demand
  availability: Preview
  inputs: Forecast horizon, cost basis, account scope and supported upstream forecast source.
  output: Reviewed forecast with source and planning limitations.
  sections:
  - F-M01
  - F-08
  constraints: A projection is not realized expenditure and does not authorize a commitment purchase.
  example:
    $markdown: field-0001
  keywords:
  - forecast
  - commitment coverage
  - savings plans
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Cost planning owner
  objective: Review a projection for an explicit horizon and assumptions.
  completion:
  - Forecast horizon and source are identified.
  - Projected values are separate from observed spending.
  - Limitations relevant to planning are recorded.
  profiles:
  - PR-F-ANALYSIS
  variants: []
  schema_version: 2
  platforms:
  - finops
  legacy_ids:
  - F-UC04
  aliases:
  - Forecast and commitment coverage review
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Read forecast evidence
    purpose:
      $markdown: field-0005
    mechanism: MX-F-QUERY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SOURCES
    effect: Source read
    verification: Reconcile a material result using the same dates, metric, scope and dimensions.
    on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  - title: Review planning assumptions
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
---

<!-- block: b-3cd435849d29535ead09 -->
## example

<!-- block: b-3722a74fafc75fce89a0 -->
<!-- field: field-0001 -->
Review the forecast for the specified horizon and scope; separate projections from observed costs.
<!-- /field -->

<!-- block: b-e670a1a79f3d5d81bfe4 -->
## narrative / 0

<!-- block: b-57e8500c939350b7ad6f -->
<!-- field: field-0002 -->
A planning owner needs a projection for a defined future period. Specify the horizon, cost basis and account scope, then obtain the supported source forecast. Retain its assumptions and source rather than put the projection in the same column as expenditure already observed.
<!-- /field -->

<!-- block: b-27f6f7af478458d18ba6 -->
## narrative / 1

<!-- block: b-16d6e33810695f69b20a -->
<!-- field: field-0003 -->
Review the projection against known workload plans and record limits in the evidence. This outcome is distinct from assessing commitment coverage. A forecast does not authorize a purchase or establish what the next bill will be.
<!-- /field -->

<!-- block: b-f3728b8914e452a88f7f -->
## steps basis

<!-- block: b-e3c01d40711c5d828a03 -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-3662f645998e5b0e97e5 -->
## workflow / 0 / purpose

<!-- block: b-7acaf92f38945e9a8ee7 -->
<!-- field: field-0005 -->
Use the supported forecast source and declared horizon.
<!-- /field -->

<!-- block: b-e4a3853b74355b2e9b1d -->
## workflow / 1 / purpose

<!-- block: b-429a1330a6ee5acdb6d7 -->
<!-- field: field-0006 -->
Compare the projection with known workload plans and record uncertainty.
<!-- /field -->

<!-- block: b-82121cedee1f54fa98a7 -->
## workflow / 1 / verification

<!-- block: b-2ae71047bb6f5cd8a11e -->
<!-- field: field-0007 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
