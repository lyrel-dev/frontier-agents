---
id: record-use-cases-UC-D05
kind: record
collection: use-cases
product: devops
title: Prepare an incident-status bulletin
order: 4
frozen: true
data:
  id: UC-D05
  platform: devops
  group: Incident response
  title: Prepare an incident-status bulletin
  summary: Explain what changed in an active incident during a short observation window.
  delivery: Configured custom agent
  cadence: On demand; scheduling is not exact-minute
  availability: GA custom agents
  inputs:
    $markdown: field-0001
  output: 'Delta-focused status update: changed observations, open hypotheses, owner and next check.'
  sections:
  - D-03
  - D-07
  - D-12
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - minute report
  - incident update
  - rolling status
  - custom agent
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Incident commander
  objective: Explain what changed in an active incident during a short observation window.
  completion:
  - Incident and measurement window are identified.
  - Changed facts, hypotheses and next check are stated.
  - Generation time is distinguished from observation time.
  profiles:
  - PR-D-REPORT
  variants:
  - name: On-demand bulletin
    changes: Invoke for a specific lookback period.
    controls: Execution may lag the measurement window.
  - name: Recurring bulletin
    changes: Configure a supported trigger.
    controls: Flexible scheduling does not guarantee minute-by-minute delivery.
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC07
  aliases:
  - Incident status bulletin
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Read the current incident signals
    purpose:
      $markdown: field-0007
    mechanism: MX-D-READ
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SOURCES
    effect: Source read
    verification: Compare returned identifiers and a material measurement with the original source.
    on_failure: Report the failed read and withhold conclusions that require that source.
  - title: Prepare a delta-focused bulletin
    purpose:
      $markdown: field-0008
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
  - title: Create recurring bulletin work
    purpose:
      $markdown: field-0009
    mechanism: MX-D-SCHEDULE
    dependency: conditional
    condition: A non-real-time recurring profile is approved.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SCHEDULE
    - FT-D-HISTORY
    effect: Future invocation
    verification: Inspect saved timing and actual start; record the observation window independently.
    on_failure:
      $markdown: field-0010
---

<!-- block: b-dcdabc3a51895b9cb919 -->
## inputs

<!-- block: b-111f304b9fc256edbf90 -->
<!-- field: field-0001 -->
Custom agent, selected telemetry and incident tools, explicit five- or ten-minute window and output contract.
<!-- /field -->

<!-- block: b-be770e7c75285aa29584 -->
## constraints

<!-- block: b-eabc6e85c8b15117894c -->
<!-- field: field-0002 -->
Telemetry resolution, lookback period, schedule window, and execution time are different. The documented custom-agent schedule has a flexible window of up to 30 minutes.
<!-- /field -->

<!-- block: b-3bd2e484a01f5c6a8374 -->
## example

<!-- block: b-0fc506241a7555b2a595 -->
<!-- field: field-0003 -->
Report what changed in the active incident during the previous five complete minutes, including the observation window, generation time, and missing sources.
<!-- /field -->

<!-- block: b-f9799fcf7f905221bec0 -->
## narrative / 0

<!-- block: b-2b8b6b06fd3e57a888a7 -->
<!-- field: field-0004 -->
During an active incident, the incident commander needs a brief update that explains what has changed since the preceding observation. Configure a specialist task with the incident identifier, selected telemetry tools, and a short explicit lookback window. Ask for changed measurements, the status of open hypotheses, missing reads, and the next check rather than a repetition of the whole incident history.
<!-- /field -->

<!-- block: b-250ede4d899854b6a8d0 -->
## narrative / 1

<!-- block: b-c99288e2c71d56968437 -->
<!-- field: field-0005 -->
A report can analyze minute-resolution measurements without arriving every minute. The documented custom-agent schedule uses a flexible window of up to 30 minutes; execution time is additional. For time-critical updates, invoke the task on demand or use a separately tested triggering design. Record both the measurement window and report-generation time so a delayed bulletin is not mistaken for current telemetry.
<!-- /field -->

<!-- block: b-b531d906fbb652dc9324 -->
## steps basis

<!-- block: b-b6bd9cd95da759ebbb11 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-bf1011d7f1e950b38831 -->
## workflow / 0 / purpose

<!-- block: b-2387488f624e5e5d99d4 -->
<!-- field: field-0007 -->
Obtain the measurements for the declared short window.
<!-- /field -->

<!-- block: b-befa6cd1cb2454099d3a -->
## workflow / 1 / purpose

<!-- block: b-0ee930287bb85f3eb65f -->
<!-- field: field-0008 -->
Use the configured reporting procedure and inspect its invocation.
<!-- /field -->

<!-- block: b-506813a2ec295a1cb409 -->
## workflow / 2 / purpose

<!-- block: b-cb735c9199305ff589f2 -->
<!-- field: field-0009 -->
Repeat only within accepted timing constraints.
<!-- /field -->

<!-- block: b-a1b1680c5c165887bc84 -->
## workflow / 2 / on failure

<!-- block: b-f80496d4929b58329ca2 -->
<!-- field: field-0010 -->
Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.
<!-- /field -->
