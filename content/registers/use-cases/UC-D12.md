---
id: record-use-cases-UC-D12
kind: record
collection: use-cases
product: devops
title: Audit resource configurations against approved standards
order: 11
frozen: true
data:
  id: UC-D12
  platform: devops
  group: Configuration assurance
  title: Audit resource configurations against approved standards
  summary: Assess selected resource settings against an explicit operational standard.
  delivery: Configured custom agent
  cadence: Scheduled
  availability: GA custom agents
  inputs:
    $markdown: field-0001
  output: Audit findings with resource identifiers, rule and observed value.
  sections:
  - D-07
  - D-M04
  - D-12
  - D-03
  constraints: Requires explicit tools and standards. It is not a built-in universal compliance engine.
  example:
    $markdown: field-0002
  keywords:
  - configuration audit
  - compliance audit
  - standards
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Platform engineer
  objective: Assess selected resource settings against an explicit operational standard.
  completion:
  - Each finding identifies resource, rule and observed value.
  - Unreadable resources remain unassessed.
  - An audit result does not imply permission to repair it.
  profiles:
  - PR-D-REPORT
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC18
  aliases:
  - Configuration audit
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Load the reviewed audit procedure
    purpose:
      $markdown: field-0006
    mechanism: MX-D-SKILL
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SKILLS
    effect: Procedural context
    verification: Test matching and nonmatching requests and inspect exposed procedure or tool-use evidence.
    on_failure:
      $markdown: field-0007
  - title: Read selected resource settings
    purpose:
      $markdown: field-0008
    mechanism: MX-D-READ
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SOURCES
    effect: Source read
    verification: Compare returned identifiers and a material measurement with the original source.
    on_failure: Report the failed read and withhold conclusions that require that source.
  - title: Run the configured audit
    purpose:
      $markdown: field-0009
    mechanism: MX-D-CUSTOM
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-CUSTOM
    - FT-D-HISTORY
    effect: Execution and output
    verification: Inspect tool arguments, failures and output against the task scope.
    on_failure: Mark incomplete output and resolve the failed prerequisite before repeating the run.
---

<!-- block: b-09fc5c56dace55679d00 -->
## inputs

<!-- block: b-e00481d3c8e85b478ff0 -->
<!-- field: field-0001 -->
Read-only configuration tools, approved standard, selected resource scope and report format.
<!-- /field -->

<!-- block: b-d6a8f378d3135aea92e4 -->
## example

<!-- block: b-1869fd04d3f45748ae15 -->
<!-- field: field-0002 -->
Audit staging security-group and logging settings against the attached operations standard; do not change resources.
<!-- /field -->

<!-- block: b-30a58be390755171aa90 -->
## narrative / 0

<!-- block: b-9b5c3d4a42ab582a8142 -->
<!-- field: field-0003 -->
An operations standard requires a small set of staging resources to have particular logging and access settings. Configure a custom task with read-only configuration tools, the explicit resource list, and the reviewed standard. Each reported finding should identify the resource, the applicable rule, and the actual value that was read.
<!-- /field -->

<!-- block: b-897c4118ffca5054a8a2 -->
## narrative / 1

<!-- block: b-fad948f4535258d69d71 -->
<!-- field: field-0004 -->
Review a known conforming and a known nonconforming example before scheduling the task. An unavailable read is an unassessed resource, not a pass. The output is a scoped configuration audit for the chosen rules; it is not a built-in universal compliance engine or permission to repair findings automatically.
<!-- /field -->

<!-- block: b-32621f161caf5111b76f -->
## steps basis

<!-- block: b-8939731a6f15547ea325 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-aeed792185145ef5bd6c -->
## workflow / 0 / purpose

<!-- block: b-5225193b33d25b08aa93 -->
<!-- field: field-0006 -->
Apply the scoped rules using actual tool references.
<!-- /field -->

<!-- block: b-4438957b43a75586a38a -->
## workflow / 0 / on failure

<!-- block: b-4d7becf428725da785c3 -->
<!-- field: field-0007 -->
Correct applicability or missing tools; stop unsupported steps without implicitly widening permissions.
<!-- /field -->

<!-- block: b-a28dfcdecdf051cea49a -->
## workflow / 1 / purpose

<!-- block: b-c74c316fc84054eab2bd -->
<!-- field: field-0008 -->
Obtain the observations needed for each rule.
<!-- /field -->

<!-- block: b-8a104c4c3f4a5042892d -->
## workflow / 2 / purpose

<!-- block: b-a9d25c72839f53af80bc -->
<!-- field: field-0009 -->
Produce findings and an explicit unassessed-resource record.
<!-- /field -->
