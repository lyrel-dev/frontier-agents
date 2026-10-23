---
id: record-use-cases-UC-F03
kind: record
collection: use-cases
product: finops
title: Review commitment coverage
order: 24
frozen: true
data:
  id: UC-F03
  platform: finops
  group: Planning and commitments
  title: Review commitment coverage
  summary: Assess coverage of eligible usage by existing commitments.
  delivery: Native function
  cadence: On demand
  availability: Preview
  inputs:
    $markdown: field-0001
  output: Reviewed commitment coverage observation.
  sections:
  - F-M01
  - F-08
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - forecast
  - commitment coverage
  - savings plans
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Commitment planning owner
  objective: Assess coverage of eligible usage by existing commitments.
  completion:
  - Commitment type, period and eligible scope are explicit.
  - Coverage observations are distinct from forecasts.
  - No purchasing authorization is implied.
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
    $markdown: field-0006
  workflow:
  - title: Read commitment evidence
    purpose:
      $markdown: field-0007
    mechanism: MX-F-QUERY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SOURCES
    effect: Source read
    verification: Reconcile a material result using the same dates, metric, scope and dimensions.
    on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  - title: Review coverage with service owners
    purpose:
      $markdown: field-0008
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0009
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
---

<!-- block: b-4e428cb6eecc5aeba569 -->
## inputs

<!-- block: b-b3bc3c90ea7555f59bae -->
<!-- field: field-0001 -->
Commitment type, observation period, eligible workload scope and supported coverage source.
<!-- /field -->

<!-- block: b-ba5c0627baa2508580ed -->
## constraints

<!-- block: b-6f5b5c45b83a5ef6a56d -->
<!-- field: field-0002 -->
Coverage, utilization and forecasts answer different questions. Purchasing requires its own decision and authority.
<!-- /field -->

<!-- block: b-4684612cc4be53ec9015 -->
## example

<!-- block: b-d8a121732c205531a437 -->
<!-- field: field-0003 -->
Review existing commitment coverage for the selected usage and period without recommending or executing a purchase.
<!-- /field -->

<!-- block: b-3921d4c5e17657249673 -->
## narrative / 0

<!-- block: b-c4bc3eaf78b256ee9be8 -->
<!-- field: field-0004 -->
A commitment planning owner needs to understand how existing commitments cover eligible usage. Specify the commitment type, workload scope and observation period. Inspect coverage directly instead of inferring it from a spending forecast or total account cost.
<!-- /field -->

<!-- block: b-82116a003a335fb4aa75 -->
## narrative / 1

<!-- block: b-92a4ec95fb3c523a8acc -->
<!-- field: field-0005 -->
Review the observation with service owners and distinguish a coverage gap from an instruction to buy. A purchasing decision has separate assumptions and authority. The case ends with a reviewed coverage assessment, not a transaction.
<!-- /field -->

<!-- block: b-be26b94debd1526bbc4b -->
## steps basis

<!-- block: b-bc4a4a009e4e507eae98 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-d2f7a966c969500c9d15 -->
## workflow / 0 / purpose

<!-- block: b-cfe04a4853f557fcb6eb -->
<!-- field: field-0007 -->
Inspect the supported commitment scope and period.
<!-- /field -->

<!-- block: b-44a205d3837e5e64be2e -->
## workflow / 1 / purpose

<!-- block: b-6ea3f87aa982586cb847 -->
<!-- field: field-0008 -->
Consider workload constraints before a separate purchasing decision.
<!-- /field -->

<!-- block: b-4e4998ee3a2957469f49 -->
## workflow / 1 / verification

<!-- block: b-1e3e3f4506f25ac4816a -->
<!-- field: field-0009 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
