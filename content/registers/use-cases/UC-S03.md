---
id: record-use-cases-UC-S03
kind: record
collection: use-cases
product: security
title: Review a proposed application design
order: 16
frozen: true
data:
  id: UC-S03
  platform: security
  group: Source and design assessment
  title: Review a proposed application design
  summary: Evaluate a current design against applicable security requirements.
  delivery: Preview assessment
  cadence: On demand
  availability: Preview
  inputs: Current design material, application context and enabled requirement packs.
  output: Design findings and reviewed assumptions.
  sections:
  - S-06
  - S-09
  - S-M07
  - S-M03
  constraints: Design review uses a different one-off lifecycle from reusable run configurations.
  example:
    $markdown: field-0001
  keywords:
  - design review
  - architecture review
  - preview
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Architect and security reviewer
  objective: Evaluate a current design against applicable security requirements.
  completion:
  - Design revision and assumptions are explicit.
  - Missing evidence is separate from a demonstrated violation.
  - Accepted findings have owners.
  profiles:
  - PR-S-REVIEW
  variants: []
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC14
  aliases:
  - Design review
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Select current design evidence
    purpose:
      $markdown: field-0005
    mechanism: MX-S-CONTEXT
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-SOURCES
    effect: Source read
    verification: Compare source revision and system boundary with the intended subject.
    on_failure: Exclude mismatched context and document the resulting assessment limitation.
  - title: Apply reviewed criteria
    purpose:
      $markdown: field-0006
    mechanism: MX-S-CRITERIA
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-REQUIREMENTS
    effect: Assessment result
    verification: Check compliant, violating and inapplicable examples.
    on_failure: Revise ambiguous applicability; do not treat a pack as a compliance certificate.
  - title: Inspect the point-in-time assessment
    purpose:
      $markdown: field-0007
    mechanism: MX-S-DESIGN
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-DESIGN
    effect: Review result
    verification: Separate missing evidence from demonstrated violation.
    on_failure: Use the documented new-review or clone path for changed design material.
---

<!-- block: b-da07037479035ab9a776 -->
## example

<!-- block: b-215f8a33087b5f76a1f2 -->
<!-- field: field-0001 -->
Review the new payment design against the enabled security requirements and list unsupported assumptions.
<!-- /field -->

<!-- block: b-980bb52c22cb532bb471 -->
## narrative / 0

<!-- block: b-a357ce4ecabf5ab4a148 -->
<!-- field: field-0002 -->
A team proposes a new payment-service design before implementation. Submit the current design material and relevant application context for the eligible review, and identify the enabled requirements that govern it. The assessment should expose assumptions about identity, data flows, and trust boundaries that need owner confirmation.
<!-- /field -->

<!-- block: b-e89d74b3d25b5fa9a3be -->
## narrative / 1

<!-- block: b-0f423d69d21d5ba3b9d1 -->
<!-- field: field-0003 -->
Review the findings with the architect and distinguish missing design evidence from a demonstrated violation. Design review has a one-off lifecycle, with cloning used for a new review; it should not be described as an automatically refreshed continuous model. The result informs design work rather than approving the future implementation.
<!-- /field -->

<!-- block: b-b887b50837a0523aa6be -->
## steps basis

<!-- block: b-7fcafcbeb3ff5392bccf -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-b7ae644dac48515fbb13 -->
## workflow / 0 / purpose

<!-- block: b-68e445a3d5ac5674a7d0 -->
<!-- field: field-0005 -->
Identify the intended system and design revision.
<!-- /field -->

<!-- block: b-e9404a4391945d0ab583 -->
## workflow / 1 / purpose

<!-- block: b-b6168befcab453d88297 -->
<!-- field: field-0006 -->
Evaluate the requirements applicable to the design.
<!-- /field -->

<!-- block: b-704e0e85a9f455d2b874 -->
## workflow / 2 / purpose

<!-- block: b-6d3fe5a4a7e95e1b931f -->
<!-- field: field-0007 -->
Record findings and unresolved architectural assumptions.
<!-- /field -->
