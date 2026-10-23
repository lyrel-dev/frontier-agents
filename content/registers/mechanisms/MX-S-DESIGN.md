---
id: record-mechanisms-MX-S-DESIGN
kind: record
collection: mechanisms
product: security
title: Point-in-time design assessment
order: 25
frozen: true
data:
  id: MX-S-DESIGN
  platform: security
  title: Point-in-time design assessment
  features:
  - FT-S-DESIGN
  sections:
  - S-06
  trigger: Current design submission
  state: One-off review and design evidence
  process:
    $markdown: field-0001
  effect: Review result
  verification: Separate missing evidence from demonstrated violation.
  on_failure: Use the documented new-review or clone path for changed design material.
  review:
    primary_section: S-06
    kind: Point-in-time design-review workflow
    inputs: Current design documents, application context and enabled security criteria.
    narrative:
    - $markdown: field-0002
    - $markdown: field-0003
    configuration:
    - - Submit
      - Select the design-review workflow and current design material.
      - Point-in-time subject
    - - Inspect
      - Open findings by requirement and read the compliance explanation.
      - Criteria and evidence
    - - Revise
      - Clone/create a new review with updated material.
      - Independent later assessment
    lifecycle:
    - - Design submitted
      - Review
      - Requirement-level findings produced.
    - - Evidence insufficient
      - Add the missing design information
      - Prepare a new assessment, not a fabricated pass.
    - - Design revised
      - Clone/new review
      - New point-in-time result; original review remains separate.
    controls: Design compliance is not implementation verification.
    observable_output: Reviewed files, requirement result and explanation.
    undocumented:
      $markdown: field-0004
    test:
    - Use a design fixture with an explicit identity boundary and one omitted control.
    - Verify the difference between violation and insufficient evidence.
    - $markdown: field-0005
    claims:
    - source: SS404
      section: Key differences between security capabilities
      assertion: Design reviews have a different one-off lifecycle.
    - source: SS412
      section: Understand statuses; Next steps
      assertion: Missing evidence and non-compliance differ; cloning creates a new review.
---

<!-- block: b-b07c9af9ad5e5a2ca3c6 -->
## process

<!-- block: b-17ae1b60b20159f09765 -->
<!-- field: field-0001 -->
Assess the submitted design against relevant criteria.
<!-- /field -->

<!-- block: b-945239174ea352398324 -->
## review / narrative / 0

<!-- block: b-e821b839880b54df887f -->
<!-- field: field-0002 -->
Design review evaluates a submitted description of the system. It does not observe whether the deployed implementation actually enforces that description. The review must distinguish a requirement violation from missing design evidence.
<!-- /field -->

<!-- block: b-da18473cec1b531aa6e1 -->
## review / narrative / 1

<!-- block: b-13e421cfd77d53d1891d -->
<!-- field: field-0003 -->
Its lifecycle is one-off rather than a reusable test configuration. Clone or create a new review for revised material so the earlier result remains attributable to its original documents.
<!-- /field -->

<!-- block: b-493d900694035e0a83c9 -->
## review / undocumented

<!-- block: b-6bdeaf7760ef5041b822 -->
<!-- field: field-0004 -->
Automatic refresh of existing design reviews and continuous synchronized system models are not documented.
<!-- /field -->

<!-- block: b-2b9a33b6782b5ac7b086 -->
## review / test / 2

<!-- block: b-130b0fe4b5e452ff94fa -->
<!-- field: field-0005 -->
Revise the document without rerunning; the old result must not be presented as a new assessment.
<!-- /field -->
