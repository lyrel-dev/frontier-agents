---
id: record-use-cases-UC-G01
kind: record
collection: use-cases
product: architecture
title: Prepare an operational review
order: 29
frozen: true
data:
  id: UC-G01
  platform: architecture
  group: Operational governance
  title: Prepare an operational review
  summary: Prepare evidence-backed decisions, owners and follow-up for an operational review.
  delivery: Team-composed workflow
  cadence: Scheduled
  availability: Component feature eligibility applies; no native cross-product orchestrator
  inputs:
    $markdown: field-0001
  output: Decision-oriented agenda with evidence references, owners and next verification dates.
  sections:
  - A-05
  - A-06
  - A-U01
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - operational review
  - weekly review
  - review pack
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  platforms:
  - devops
  - finops
  - architecture
  actor: Operational review chair
  objective: Prepare evidence-backed decisions, owners and follow-up for an operational review.
  completion:
  - Reviewed inputs and prior actions retain source identity.
  - Required decisions and accountable owners are explicit.
  - Earlier actions are closed only with acceptance evidence.
  profiles:
  - PR-REVIEW
  variants:
  - name: Reliability review
    changes: Use health, deployments, incident patterns and prevention results.
    controls: Service measurements and engineering ownership remain authoritative.
  - name: Cost-management review
    changes: Use reconciled costs, anomalies, recommendations and measured outcomes.
    controls: Potential savings remain estimates until independently measured.
  - name: Combined team review
    changes: Use evidence from independently configured services.
    controls: No shared runtime, credentials or approval authority are implied.
  schema_version: 2
  legacy_ids:
  - D-UC10
  - F-UC06
  aliases:
  - Operational review pack
  - FinOps operational review pack
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Select review evidence
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
  - title: Prepare reliability evidence
    purpose:
      $markdown: field-0009
    mechanism: MX-D-CUSTOM
    dependency: conditional
    condition: The reliability review profile is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-CUSTOM
    - FT-D-HISTORY
    effect: Execution and output
    verification: Inspect tool arguments, failures and output against the task scope.
    on_failure: Mark incomplete output and resolve the failed prerequisite before repeating the run.
  - title: Prepare cost-management evidence
    purpose:
      $markdown: field-0010
    mechanism: MX-F-TASK
    dependency: conditional
    condition: The cost-management review profile is selected.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-TASKS
    effect: Execution and output
    verification: Match completed results to task identity and requested scope.
    on_failure: Distinguish absent, queued and failed tasks before retrying.
  - title: Record decisions and follow-up
    purpose:
      $markdown: field-0011
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0012
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
---

<!-- block: b-212584b6dce551b7b206 -->
## inputs

<!-- block: b-22c0cb5988d251dea3c1 -->
<!-- field: field-0001 -->
Reviewed reliability or cost evidence, prior action list, decision owners and reporting period.
<!-- /field -->

<!-- block: b-f16be2344c705d8082a5 -->
## constraints

<!-- block: b-c01a0fe391fb597aa2d6 -->
<!-- field: field-0002 -->
Independent products keep their own access and runtime state. A handoff does not transfer credentials or approval.
<!-- /field -->

<!-- block: b-6aa24544a6e35ac9ae92 -->
## example

<!-- block: b-2a40862ade7a506e86ce -->
<!-- field: field-0003 -->
Prepare the operational review from the reviewed reports and prior action list; identify decisions, evidence, owners and unresolved questions.
<!-- /field -->

<!-- block: b-b79ce61180ee51e5b418 -->
## narrative / 0

<!-- block: b-367134d19b3f54caa51f -->
<!-- field: field-0004 -->
An operational review starts with reviewed evidence and unresolved decisions, not with a request for another differently titled report. Select the reliability or cost-management profile, identify its period, and assemble relevant findings with the previous action list. Each input retains its source and execution identity so participants can question its interpretation.
<!-- /field -->

<!-- block: b-eab4cbef665251b78e8a -->
## narrative / 1

<!-- block: b-971314a85ab6577784b7 -->
<!-- field: field-0005 -->
Organize the meeting around decisions required, their supporting observations, accountable owners and the next verification date. Owners confirm progress and acceptance; silence is not completion. The profiles reuse this narrative while retaining their own data access and execution configuration. A combined meeting is a team-managed composition, not an AWS cross-agent orchestration feature.
<!-- /field -->

<!-- block: b-aadb25c3f01254cfab6f -->
## steps basis

<!-- block: b-0be426faa60e5fc9a454 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-f09393eccf8e505dab83 -->
## workflow / 0 / purpose

<!-- block: b-7175eee2233b57288e6c -->
<!-- field: field-0007 -->
Choose reliability or cost-management results and the prior action list.
<!-- /field -->

<!-- block: b-6e6f6e112f945c8f9007 -->
## workflow / 0 / verification

<!-- block: b-a81a410b30df5fd7aae2 -->
<!-- field: field-0008 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->

<!-- block: b-2e73223b185659cbb022 -->
## workflow / 1 / purpose

<!-- block: b-212c2510989554d4aa0a -->
<!-- field: field-0009 -->
Assemble selected service reports and incident themes.
<!-- /field -->

<!-- block: b-0f9dd31bc6b45ca4ad63 -->
## workflow / 2 / purpose

<!-- block: b-88df1c06575d5245b383 -->
<!-- field: field-0010 -->
Assemble reconciled costs, anomalies and recommendation dispositions.
<!-- /field -->

<!-- block: b-5098a7051bf95dbc8f70 -->
## workflow / 3 / purpose

<!-- block: b-1c90f208bc6255cb8d53 -->
<!-- field: field-0011 -->
Have owners confirm status, priority and acceptance rather than infer completion from silence.
<!-- /field -->

<!-- block: b-59c6a621c113533b8136 -->
## workflow / 3 / verification

<!-- block: b-8aec3ec72e9458a89fda -->
<!-- field: field-0012 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
