---
id: record-use-cases-UC-S08
kind: record
collection: use-cases
product: security
title: Consolidate and maintain security requirements
order: 21
frozen: true
data:
  id: UC-S08
  platform: security
  group: Assessment governance
  title: Consolidate and maintain security requirements
  summary: Maintain reviewed assessment criteria derived from authoritative policy.
  delivery: Composed workflow
  cadence: On demand
  availability: Preview workflows
  inputs: Governed policy sources, existing pack and reviewer.
  output: Reviewed replacement requirement pack and external change record.
  sections:
  - S-M04
  - S-M03
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - requirement generation
  - policy consolidation
  - pack
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Security policy owner
  objective: Maintain reviewed assessment criteria derived from authoritative policy.
  completion:
  - Conflicting policy sources are reconciled.
  - The replacement is compared with prior manual requirements.
  - Applicability and criteria are tested before enablement.
  profiles:
  - PR-S-REVIEW
  variants: []
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC13
  aliases:
  - Security requirement consolidation
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Reconcile governing policy
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
  - title: Generate the replacement pack
    purpose:
      $markdown: field-0008
    mechanism: MX-S-GENERATE
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-REQUIREMENTS
    effect: Configuration replacement
    verification: Compare with approved policy and prior manually added requirements.
    on_failure: Do not enable an unreviewed replacement; keep authoritative source in Git.
  - title: Test requirement applicability
    purpose:
      $markdown: field-0009
    mechanism: MX-S-CRITERIA
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-REQUIREMENTS
    effect: Assessment result
    verification: Check compliant, violating and inapplicable examples.
    on_failure: Revise ambiguous applicability; do not treat a pack as a compliance certificate.
---

<!-- block: b-64d35d16e1ca5c81a4ab -->
## constraints

<!-- block: b-837323a92f8a5dd08c71 -->
<!-- field: field-0001 -->
Regeneration replaces existing requirements, including manual entries. Keep the authoritative source outside the generated pack.
<!-- /field -->

<!-- block: b-dd106356db37527ca943 -->
## example

<!-- block: b-efe1170e676d586c8e17 -->
<!-- field: field-0002 -->
Regenerate the pack from the approved policy documents and identify which existing requirements would be replaced.
<!-- /field -->

<!-- block: b-b7cb9f25351658459f19 -->
## narrative / 0

<!-- block: b-380fd3b0f5ae5a708fd9 -->
<!-- field: field-0003 -->
Policy owners have revised several overlapping security standards. Reconcile the governing documents and identify the approved source before generating a replacement requirement pack. Compare the generated applicability and compliance statements with that source, including requirements that had previously been added manually.
<!-- /field -->

<!-- block: b-f8c150345bb35bed8430 -->
## narrative / 1

<!-- block: b-711402f53ec8582ab657 -->
<!-- field: field-0004 -->
Regeneration replaces the existing pack contents rather than appending to them. Review the proposed replacement before enabling it for subsequent assessments, and keep the policy and reviewed requirement source in Git. This is a controlled authoring workflow; it must not silently replace a working pack merely because new documents were uploaded.
<!-- /field -->

<!-- block: b-7756dc876eab55d58d0f -->
## steps basis

<!-- block: b-1d30a336325650c29da5 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-da62d61f0eef52fbb58b -->
## workflow / 0 / purpose

<!-- block: b-c3bc0e64895f59b7a0c6 -->
<!-- field: field-0006 -->
Identify approved source material and compare existing requirements.
<!-- /field -->

<!-- block: b-888b046093b05ce49272 -->
## workflow / 0 / verification

<!-- block: b-1c1c55b8a65e5264b97b -->
<!-- field: field-0007 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->

<!-- block: b-d1f5442db3f858dea8ec -->
## workflow / 1 / purpose

<!-- block: b-2d9ecf539a9c57dea3ca -->
<!-- field: field-0008 -->
Treat regeneration as replacement rather than append.
<!-- /field -->

<!-- block: b-6763f7cc53425f818f0a -->
## workflow / 2 / purpose

<!-- block: b-e292b478d9105b4ebd3a -->
<!-- field: field-0009 -->
Check compliant, violating and inapplicable examples.
<!-- /field -->
