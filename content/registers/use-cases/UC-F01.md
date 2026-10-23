---
id: record-use-cases-UC-F01
kind: record
collection: use-cases
product: finops
title: Analyze historical cost and usage
order: 22
frozen: true
data:
  id: UC-F01
  platform: finops
  group: Cost analysis
  title: Analyze historical cost and usage
  summary: Answer a bounded historical cost question using reproducible source queries.
  delivery: Native function
  cadence: On demand
  availability: Preview
  inputs: Complete dates, metric, currency, account scope, grouping and optional ownership mapping.
  output: Reconciled total, breakdown or historical variance with attribution limits.
  sections:
  - F-M01
  - F-08
  - F-U01
  - F-M02
  constraints: A fluent answer is not a substitute for a reproducible source query.
  example:
    $markdown: field-0001
  keywords:
  - cost inquiry
  - natural language
  - cost explorer
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Cost analyst or service engineer
  objective: Answer a bounded historical cost question using reproducible source queries.
  completion:
  - Dates, metric, currency and filters are explicit.
  - Totals and component changes reconcile.
  - Unmapped ownership and unexplained causes remain visible.
  profiles:
  - PR-F-ANALYSIS
  variants:
  - name: Total inquiry
    changes: Return a bounded historical amount.
    controls: The amount alone does not explain workload behavior.
  - name: Dimensional breakdown
    changes: Group by supported source dimensions or reviewed ownership.
    controls: Keep ambiguous and unassigned records visible.
  - name: Variance decomposition
    changes: Compare complete matched periods.
    controls: Contribution arithmetic is distinct from causal proof.
  schema_version: 2
  platforms:
  - finops
  legacy_ids:
  - F-UC01
  - F-UC02
  - F-UC03
  aliases:
  - Natural-language cost inquiry
  - Cost variance decomposition
  - Cost breakdown by ownership dimension
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Retrieve defined cost evidence
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
  - title: Apply ownership context
    purpose:
      $markdown: field-0006
    mechanism: MX-F-FILES
    dependency: conditional
    condition: An ownership-enriched profile is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-FILES
    effect: Context read
    verification: Verify a known mapping and expose unmapped records.
    on_failure: Keep unassigned values visible and update the authoritative file deliberately.
  - title: Reconcile and interpret the result
    purpose:
      $markdown: field-0007
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0008
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
---

<!-- block: b-a8b40d8871a35a94b74d -->
## example

<!-- block: b-44ea09ae8f1a58b6b6b7 -->
<!-- field: field-0001 -->
Analyze the selected complete periods using the same basis; reconcile totals and explain only the changes supported by evidence.
<!-- /field -->

<!-- block: b-eeed7521ae1b5f288f58 -->
## narrative / 0

<!-- block: b-5f26692afeea5c67847c -->
<!-- field: field-0002 -->
A service owner asks how expenditure changed and which component requires investigation. Begin with the dates, cost metric, currency, scope and grouping. A total inquiry, owner breakdown and period comparison are analytical profiles of this bounded cost-analysis objective. Use reviewed ownership mappings only where the requested view needs them, and preserve unmapped values.
<!-- /field -->

<!-- block: b-4d106ca8478958dba3d6 -->
## narrative / 1

<!-- block: b-d0d5aa3acbcf522c9b1a -->
<!-- field: field-0003 -->
Reconcile totals and deltas against the same source basis before interpreting them. The largest monetary contribution identifies where to look next; it does not establish why the workload consumed that usage. Keep observed cost separate from forecasts and recommendation estimates, and retain unavailable evidence rather than inventing a single causal explanation.
<!-- /field -->

<!-- block: b-a1e87f57d8635579b6d0 -->
## steps basis

<!-- block: b-45cd34d9f5c85801869c -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-1d50936eb43f55d4a604 -->
## workflow / 0 / purpose

<!-- block: b-d145a4ea829e55c69ef9 -->
<!-- field: field-0005 -->
Answer the total, breakdown or variance question under one basis.
<!-- /field -->

<!-- block: b-398ad35d7b805352ad8b -->
## workflow / 1 / purpose

<!-- block: b-54588c1ceaf25828b8e1 -->
<!-- field: field-0006 -->
Use reviewed organization-specific mappings.
<!-- /field -->

<!-- block: b-2a0ee959b2ea5c23958d -->
## workflow / 2 / purpose

<!-- block: b-4d578d82a3ce5dc4bc8e -->
<!-- field: field-0007 -->
Check sums and distinguish monetary contribution from operational cause.
<!-- /field -->

<!-- block: b-f5bbb6ca62665ed886a1 -->
## workflow / 2 / verification

<!-- block: b-3ea4feef31c7577c8679 -->
<!-- field: field-0008 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
