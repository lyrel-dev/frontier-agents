---
id: record-use-cases-UC-S02
kind: record
collection: use-cases
product: security
title: Review source code for security issues
order: 15
frozen: true
data:
  id: UC-S02
  platform: security
  group: Source and design assessment
  title: Review source code for security issues
  summary: Assess an identified source revision for vulnerabilities and selected requirements.
  delivery: Preview assessment
  cadence: On demand
  availability: Preview
  inputs: Connected repository or S3 source, review mode and applicable requirement packs.
  output: Code findings with evidence, location and possible remediation.
  sections:
  - S-06
  - S-M03
  - S-09
  - S-M07
  - S-05
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - code review
  - repository
  - preview
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Application security reviewer
  objective: Assess an identified source revision for vulnerabilities and selected requirements.
  completion:
  - Review mode and exact revision are known.
  - Findings retain source context.
  - Preflight failure and stale results are explicit.
  profiles:
  - PR-S-REVIEW
  variants:
  - name: Full-source baseline
    changes: Analyze the selected full source scope.
    controls: The result does not test the deployed application.
  - name: Change-focused review
    changes: Analyze an eligible change with surrounding context.
    controls: Further revisions require matching review evidence under provider-specific behavior.
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC10
  - S-UC11
  aliases:
  - Repository code review
  - Change-focused code review
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Read selected source context
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
  - title: Run the selected review mode
    purpose:
      $markdown: field-0007
    mechanism: MX-S-CODE
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-CODE
    - FT-S-SOURCES
    effect: Source analysis; optional comments separately configured
    verification: Match results to the revision and record unassessed scope.
    on_failure: Obtain a current result when revision or trigger behavior makes prior evidence stale.
  - title: Evaluate applicable requirements
    purpose:
      $markdown: field-0008
    mechanism: MX-S-CRITERIA
    dependency: conditional
    condition: Requirement evaluation is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-REQUIREMENTS
    effect: Assessment result
    verification: Check compliant, violating and inapplicable examples.
    on_failure: Revise ambiguous applicability; do not treat a pack as a compliance certificate.
  - title: Review returned evidence
    purpose:
      $markdown: field-0009
    mechanism: MX-S-FINDING
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-FINDINGS
    effect: Finding review record
    verification: Give the finding a disposition using evidence, impact and application-owner context.
    on_failure: Preserve uncertainty and obtain missing evidence before closure.
---

<!-- block: b-b7174dac4d62525d8470 -->
## constraints

<!-- block: b-a85e75906dd95bb8a60b -->
<!-- field: field-0001 -->
Provider, source and availability limits apply. Completed review is not complete application coverage.
<!-- /field -->

<!-- block: b-007bca2091255d39b33d -->
## example

<!-- block: b-bb7dd2374a965a8ba0a1 -->
<!-- field: field-0002 -->
Review the repository for vulnerability findings and the enabled authorization requirements.
<!-- /field -->

<!-- block: b-d44f082c22055c47b772 -->
## narrative / 0

<!-- block: b-52a93d1fb4c95f84a263 -->
<!-- field: field-0003 -->
A team wants a baseline review of a repository or supported source package. Connect the intended source revision and select the eligible review modes. Vulnerability analysis and evaluation against enabled requirement packs answer related but different questions, so the requested criteria should be explicit.
<!-- /field -->

<!-- block: b-27b186a46d455fee8d50 -->
## narrative / 1

<!-- block: b-0c0a0f5f2441513f98f6 -->
<!-- field: field-0004 -->
Review findings in their code context and inspect preflight failures separately from completed analysis. The result applies to the selected source and modes; it is not a substitute for testing the deployed application. This preview workflow has provider and availability boundaries that must be checked before it becomes part of the delivery process.
<!-- /field -->

<!-- block: b-acb8c11b7b67589ebdb3 -->
## steps basis

<!-- block: b-3fb47693bf3354d8bdc7 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-0dfc1be3c5d6523f8509 -->
## workflow / 0 / purpose

<!-- block: b-591cbd42c87a5a758d74 -->
<!-- field: field-0006 -->
Use the revision and repository intended for review.
<!-- /field -->

<!-- block: b-21eb18e58a845d6b9aa6 -->
## workflow / 1 / purpose

<!-- block: b-5f9a894166a356c18da8 -->
<!-- field: field-0007 -->
Review a baseline or supported change-focused source.
<!-- /field -->

<!-- block: b-11bf81acd9f35b6f9a6d -->
## workflow / 2 / purpose

<!-- block: b-e6cc2b6766c65767829a -->
<!-- field: field-0008 -->
Apply reviewed organizational criteria.
<!-- /field -->

<!-- block: b-e52f1e2e8be55382addf -->
## workflow / 3 / purpose

<!-- block: b-b928a04d84b355f980bd -->
<!-- field: field-0009 -->
Decide which findings require further work.
<!-- /field -->
