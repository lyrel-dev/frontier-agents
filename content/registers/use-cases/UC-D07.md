---
id: record-use-cases-UC-D07
kind: record
collection: use-cases
product: devops
title: Review deployment and change activity
order: 6
frozen: true
data:
  id: UC-D07
  platform: devops
  group: Operational reporting
  title: Review deployment and change activity
  summary: Establish which deployments and rollbacks affected the selected services.
  delivery: Configured custom agent
  cadence: On demand or scheduled
  availability: GA custom agents
  inputs: CI/CD integration, service ownership, revision identifiers and complete reporting window.
  output: Deployment report with revisions, outcomes, affected services and unresolved follow-up.
  sections:
  - D-03
  - D-07
  - D-12
  constraints: Requires connected pipeline tools and explicit interpretation of deployment states.
  example:
    $markdown: field-0001
  keywords:
  - deployment report
  - change report
  - CI/CD
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Release engineer
  objective: Establish which deployments and rollbacks affected the selected services.
  completion:
  - Deployment states and immutable revisions are traceable.
  - Source gaps are explicit.
  - Temporal association is not presented as proven cause.
  profiles:
  - PR-D-REPORT
  - PR-EVIDENCE
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC09
  aliases:
  - Deployment and change activity report
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Read delivery evidence
    purpose:
      $markdown: field-0005
    mechanism: MX-D-READ
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SOURCES
    effect: Source read
    verification: Compare returned identifiers and a material measurement with the original source.
    on_failure: Report the failed read and withhold conclusions that require that source.
  - title: Prepare the activity review
    purpose:
      $markdown: field-0006
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
  - title: Repeat the activity review
    purpose:
      $markdown: field-0007
    mechanism: MX-D-SCHEDULE
    dependency: conditional
    condition: Recurring reporting is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SCHEDULE
    - FT-D-HISTORY
    effect: Future invocation
    verification: Inspect saved timing and actual start; record the observation window independently.
    on_failure:
      $markdown: field-0008
---

<!-- block: b-b1b944b86e1359489a89 -->
## example

<!-- block: b-3891468112505ba99bd2 -->
<!-- field: field-0001 -->
List production deployments in the last seven complete days, including failed changes and linked incidents.
<!-- /field -->

<!-- block: b-30478960bb8d52a38cc2 -->
## narrative / 0

<!-- block: b-56eb03344e625b2f9f1c -->
<!-- field: field-0002 -->
A release engineer wants to review the changes delivered during the previous week. The input is deployment history with service and revision identifiers, not simply merged pull requests. Configure the task to distinguish attempted, successful, failed, and rolled-back deployments using the states exposed by the connected delivery tools.
<!-- /field -->

<!-- block: b-1a9c04b23ad8549bb656 -->
## narrative / 1

<!-- block: b-33f5d5e4fe12567d8c06 -->
<!-- field: field-0003 -->
The result should make it possible to trace a reported deployment to its source record and compare it with incidents in the same service and period. Similar timestamps are useful for investigation but do not establish causality. Missing pipeline access or ambiguous status mappings should be listed explicitly so the report is not presented as a complete release history.
<!-- /field -->

<!-- block: b-2a736944a53059028de9 -->
## steps basis

<!-- block: b-234561075a625f20a2a0 -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-e9433925bf89512eaf53 -->
## workflow / 0 / purpose

<!-- block: b-a8f34de80f2f5a32ae69 -->
<!-- field: field-0005 -->
Use actual deployment records rather than merged changes.
<!-- /field -->

<!-- block: b-c2dfccf2cd47567dabf0 -->
## workflow / 1 / purpose

<!-- block: b-43b797dacf1756fb8a5b -->
<!-- field: field-0006 -->
Normalize supported source states and expose unresolved mappings.
<!-- /field -->

<!-- block: b-7328bdcef9fe58e7b284 -->
## workflow / 2 / purpose

<!-- block: b-2328abecc1155795830d -->
<!-- field: field-0007 -->
Cover the declared complete period.
<!-- /field -->

<!-- block: b-2e181205a0545f52bd30 -->
## workflow / 2 / on failure

<!-- block: b-103deebeb8695738a65d -->
<!-- field: field-0008 -->
Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.
<!-- /field -->
