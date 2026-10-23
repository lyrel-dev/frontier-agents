---
id: record-mechanisms-MX-S-CRITERIA
kind: record
collection: mechanisms
product: security
title: Requirement applicability and evaluation
order: 22
frozen: true
data:
  id: MX-S-CRITERIA
  platform: security
  title: Requirement applicability and evaluation
  features:
  - FT-S-REQUIREMENTS
  sections:
  - S-M03
  trigger: Eligible review with requirement mode enabled
  state: Reviewed pack and criteria
  process:
    $markdown: field-0001
  effect: Assessment result
  verification: Check compliant, violating and inapplicable examples.
  on_failure: Revise ambiguous applicability; do not treat a pack as a compliance certificate.
  review:
    primary_section: S-M03
    kind: Requirement-applicability mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Define
      - $markdown: field-0005
      - Evaluation rule
    - - Enable
      - Enable the reviewed pack and select requirement evaluation in the eligible review mode.
      - Future assessment behavior
    - - Inspect
      - Review the stated reason for applicability and result.
      - Criterion-level evidence
    lifecycle:
    - - Pack disabled
      - Enable
      - Criteria apply to new eligible reviews.
    - - Requirement edited
      - Start new review
      - Updated criteria apply prospectively.
    - - Existing result
      - Pack changed
      - Historical review is not rewritten.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented:
      $markdown: field-0008
    test:
    - Prepare compliant, violating and deliberately inapplicable examples for one requirement.
    - Check applicability before the compliance verdict.
    - $markdown: field-0009
    claims:
    - source: SS408
      section: Overview; Enable or disable a pack
      assertion:
        $markdown: field-0010
    - source: SS412
      section: Understand compliance statuses
      assertion: Design reviews distinguish Insufficient data and Not applicable from compliance/violation.
---

<!-- block: b-421f6457acc55ff88cf3 -->
## process

<!-- block: b-d2fd02ad01cc5427ac42 -->
<!-- field: field-0001 -->
Evaluate supplied evidence against applicable requirements.
<!-- /field -->

<!-- block: b-55185497b26652c18284 -->
## review / inputs

<!-- block: b-d0d6cdea5f3d52428def -->
<!-- field: field-0002 -->
Enabled pack, requirement applicability/compliance definitions and eligible source/design review evidence.
<!-- /field -->

<!-- block: b-c3cf9517e0e35f7c9c51 -->
## review / narrative / 0

<!-- block: b-937d4099321051b5acd9 -->
<!-- field: field-0003 -->
Requirement evaluation first needs a criterion that applies to the subject. The compliance assessment then compares the supplied evidence with that criterion. Missing evidence is not the same as a demonstrated violation or an inapplicable requirement.
<!-- /field -->

<!-- block: b-a4094f2a379b5da59ee5 -->
## review / narrative / 1

<!-- block: b-d5d0304ff8fa50c6b9e4 -->
<!-- field: field-0004 -->
Packs are shared policy configuration. Enabling, disabling or editing one affects future eligible reviews, not the historical conclusions of reviews already completed. This shared reach makes requirement maintenance a cross-application change.
<!-- /field -->

<!-- block: b-e4a3a16065c05e57ab5b -->
## review / configuration / 0 / 1

<!-- block: b-52cf21b75586506285b8 -->
<!-- field: field-0005 -->
Security requirements → chosen pack → inspect applicability, compliance criteria and optional remediation guidance.
<!-- /field -->

<!-- block: b-79b15a2ed1885674b1e5 -->
## review / controls

<!-- block: b-49a49d7915b053cdb615 -->
<!-- field: field-0006 -->
Framework labels and managed packs are not compliance certification; applicability is part of the evaluated claim.
<!-- /field -->

<!-- block: b-3fcacfb4ca8657048970 -->
## review / observable output

<!-- block: b-ab7d6e3a98f859608f5a -->
<!-- field: field-0007 -->
Requirement-linked result and explanation, including missing-data or inapplicable distinctions where exposed.
<!-- /field -->

<!-- block: b-f0a8a4fec4f65161b3d0 -->
## review / undocumented

<!-- block: b-77dd69f9ef8756fd8828 -->
<!-- field: field-0008 -->
Full semantic evaluation rules and a deterministic false-positive/false-negative guarantee are not documented.
<!-- /field -->

<!-- block: b-df7af5c039b254ba9543 -->
## review / test / 2

<!-- block: b-cb5c22877b515d0ab5f4 -->
<!-- field: field-0009 -->
Remove decisive design evidence; require an insufficient-evidence interpretation, not assumed compliance.
<!-- /field -->

<!-- block: b-7f0e878255e7512fb685 -->
## review / claims / 0 / assertion

<!-- block: b-d92be849b2f0591eb148 -->
<!-- field: field-0010 -->
Enabled packs govern future eligible reviews and have distinct applicability/compliance fields.
<!-- /field -->
