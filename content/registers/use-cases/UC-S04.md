---
id: record-use-cases-UC-S04
kind: record
collection: use-cases
product: security
title: Develop and review an application threat model
order: 17
frozen: true
data:
  id: UC-S04
  platform: security
  group: Source and design assessment
  title: Develop and review an application threat model
  summary: Produce a reviewed system representation and evidence-backed threats for a defined scope.
  delivery: Preview assessment
  cadence: On demand
  availability: Preview
  inputs: Architecture documents, code/context sources and explicit system boundary.
  output: Assets, trust boundaries, flows, threats and model findings.
  sections:
  - S-06
  - S-09
  - S-M07
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - threat model
  - trust boundary
  - data flow
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Threat-model reviewer
  objective: Produce a reviewed system representation and evidence-backed threats for a defined scope.
  completion:
  - Boundaries and flows are reviewed before threats.
  - Source assumptions and inferred edges remain visible.
  - Threat dispositions refer to the selected model run.
  profiles:
  - PR-S-REVIEW
  variants: []
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC15
  aliases:
  - Threat modeling
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Assemble scope and source inputs
    purpose:
      $markdown: field-0006
    mechanism: MX-S-CONTEXT
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-SOURCES
    effect: Source read
    verification: Compare source revision and system boundary with the intended subject.
    on_failure: Exclude mismatched context and document the resulting assessment limitation.
  - title: Construct and review the model
    purpose:
      $markdown: field-0007
    mechanism: MX-S-THREAT
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-THREAT
    - FT-S-SOURCES
    effect: Model result
    verification: Review inferred boundaries before interpreting individual threats.
    on_failure: Correct input scope when the model represents the wrong system.
  - title: Resolve model assumptions
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

<!-- block: b-09bf0764c1c25e45a61c -->
## constraints

<!-- block: b-16b7bec220305d9b842b -->
<!-- field: field-0001 -->
Inferred system context requires review; the model is not a complete guarantee of threat coverage.
<!-- /field -->

<!-- block: b-798b2af31d325b74b573 -->
## example

<!-- block: b-ea9cb32cea9451fd862b -->
<!-- field: field-0002 -->
Create a threat model for the checkout service and mark inferred flows that require owner confirmation.
<!-- /field -->

<!-- block: b-194fef2e379d51cea711 -->
## narrative / 0

<!-- block: b-f0e0606b6bc05d4da509 -->
<!-- field: field-0003 -->
A service boundary has changed and the team needs an updated threat model. Supply explicit scope documents and the relevant architecture and source evidence. Review the inferred system overview, components, data flows, and trust boundaries before evaluating individual threats.
<!-- /field -->

<!-- block: b-85b864ed8ae854f69be1 -->
## narrative / 1

<!-- block: b-37a6cc0d2af25916af63 -->
<!-- field: field-0004 -->
Correct an incorrect boundary at the model input rather than dismissing every threat that follows from it. Retain evidence for the accepted threats and identify inferred relationships that remain unverified. The result is a reviewed model for that scope and run, not proof that every possible threat has been discovered.
<!-- /field -->

<!-- block: b-58f73636a3eb540ebf3a -->
## steps basis

<!-- block: b-ae465175e78950499f71 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-6f38aa7ae24f5d57bcd1 -->
## workflow / 0 / purpose

<!-- block: b-dcf88c4823b35f64953d -->
<!-- field: field-0006 -->
Separate analytical focus from implementation context.
<!-- /field -->

<!-- block: b-b90c3990e1be5bd2964c -->
## workflow / 1 / purpose

<!-- block: b-68e11e4311495c8680ac -->
<!-- field: field-0007 -->
Examine system boundaries before individual threats.
<!-- /field -->

<!-- block: b-ca6c06d8f1375ae084e4 -->
## workflow / 2 / purpose

<!-- block: b-4770a78a831154cf95b5 -->
<!-- field: field-0008 -->
Correct inputs and assign unresolved relationships to owners.
<!-- /field -->

<!-- block: b-fbe6f09eea2254e9a7f5 -->
## workflow / 2 / verification

<!-- block: b-190486045d3553afb444 -->
<!-- field: field-0009 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
