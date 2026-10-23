---
id: record-use-cases-UC-D02
kind: record
collection: use-cases
product: devops
title: Investigate a service incident
order: 1
frozen: true
data:
  id: UC-D02
  platform: devops
  group: Incident response
  title: Investigate a service incident
  summary: Establish an explanation supported by current incident evidence.
  delivery: Built-in function
  cadence: Event-driven or on demand
  availability: GA production operations
  inputs: Incident signal, service scope, UTC window, connected telemetry and deployment context.
  output: Investigation record with observations, hypotheses, root-cause versions and evidence.
  sections:
  - D-01
  - D-06
  - D-M01
  - D-03
  - D-12
  - D-M07
  - D-M02
  constraints: The output remains an investigation result to verify against current source data.
  example:
    $markdown: field-0001
  keywords:
  - incident
  - root cause
  - metrics
  - logs
  - traces
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Incident investigator
  objective: Establish an explanation supported by current incident evidence.
  completion:
  - Affected service and UTC interval are explicit.
  - Competing explanations and unavailable sources are retained.
  - The conclusion follows current observations or remains inconclusive.
  profiles:
  - PR-D-INCIDENT
  - PR-EVIDENCE
  variants:
  - name: New incident
    changes: Current evidence is sufficient to begin; prior history is not required.
    controls: Missing history never excuses missing current telemetry.
  - name: Recurring alarm
    changes: Read relevant monitor context and compare it with new observations.
    controls: Record knowledge existence, observed retrieval and diagnosis correctness separately.
  - name: Operator steering
    changes: Supply contrary evidence within the active investigation.
    controls: Steering does not authorize a production mutation.
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC02
  - D-UC03
  - D-UC13
  aliases:
  - Root-cause investigation
  - Investigation steering and hypothesis review
  - Recurring-alarm investigation with historical context
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Read current observations
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
  - title: Compare historical context
    purpose:
      $markdown: field-0006
    mechanism: MX-D-RECALL
    dependency: optional
    condition: Relevant historical context is available.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-MEMORY
    effect: Context read
    verification:
      $markdown: field-0007
    on_failure:
      $markdown: field-0008
  - title: Investigate and reconsider hypotheses
    purpose:
      $markdown: field-0009
    mechanism: MX-D-INVESTIGATE
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-INCIDENT
    - FT-D-SOURCES
    effect: Investigation record
    verification: Check conclusions against current observations and identify missing evidence.
    on_failure: Retain competing hypotheses or an inconclusive result instead of inventing certainty.
  - title: Record a verified correction
    purpose:
      $markdown: field-0010
    mechanism: MX-D-FEEDBACK
    dependency: conditional
    condition: A completed investigation requires verified correction.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-INCIDENT
    - FT-D-MEMORY
    effect: Retained correction
    verification: Inspect saved feedback and any exposed corrective entry.
    on_failure:
      $markdown: field-0011
---

<!-- block: b-ceb28be85dd953c7a719 -->
## example

<!-- block: b-3e8b68cee62b5f11823c -->
<!-- field: field-0001 -->
Investigate the checkout 5xx increase for the stated service and UTC window; separate observations, hypotheses and missing data.
<!-- /field -->

<!-- block: b-4adb72d5dc4e5fa3a80e -->
## narrative / 0

<!-- block: b-cb24a68ca2bd58df9a9c -->
<!-- field: field-0002 -->
A service owner sees elevated errors after a deployment. The investigation begins with the affected service, incident time, and symptoms, not with an assumed deployment defect. Connect the available logs, metrics, traces, repository context, and deployment records, then inspect how the investigation relates the observations across those sources.
<!-- /field -->

<!-- block: b-254cd38341585035b590 -->
## narrative / 1

<!-- block: b-3d47bf4906cd594f8f3e -->
<!-- field: field-0003 -->
The useful result identifies the measurements that support each explanation and the sources that could not be read. A deployment timestamp may provide a lead, but its proximity to the error increase is not sufficient proof of cause. When evidence conflicts, preserve the competing explanations and supply the missing observation through investigation steering rather than turning a plausible summary into a confirmed diagnosis.
<!-- /field -->

<!-- block: b-7942a03f403c5ed79b00 -->
## steps basis

<!-- block: b-4b6fff87cfc65541abae -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-41e2f80870f15b188f6a -->
## workflow / 0 / purpose

<!-- block: b-e326f28987255952a820 -->
<!-- field: field-0005 -->
Establish the present symptom and affected scope.
<!-- /field -->

<!-- block: b-8aca05b674ca50378efd -->
## workflow / 1 / purpose

<!-- block: b-b3fcff2fa26853f1b89e -->
<!-- field: field-0006 -->
Treat prior causes as hypotheses, not predetermined answers.
<!-- /field -->

<!-- block: b-8e62139f99d957058e25 -->
## workflow / 1 / verification

<!-- block: b-539a5ead70e358059d40 -->
<!-- field: field-0007 -->
Distinguish entry existence, observable retrieval and correctness against current evidence.
<!-- /field -->

<!-- block: b-f3b2d84904105aa5a5ca -->
## workflow / 1 / on failure

<!-- block: b-61b3fa93141d541a8f08 -->
<!-- field: field-0008 -->
Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.
<!-- /field -->

<!-- block: b-65a370ea5ff65c448610 -->
## workflow / 2 / purpose

<!-- block: b-a13e4b6ab1575037861c -->
<!-- field: field-0009 -->
Use current evidence and relevant operator steering.
<!-- /field -->

<!-- block: b-2347001928f65e2985c8 -->
## workflow / 3 / purpose

<!-- block: b-f9d73a132f185fa8802d -->
<!-- field: field-0010 -->
Preserve the actual cause when a completed diagnosis was wrong.
<!-- /field -->

<!-- block: b-82fcc21a679c51ff9791 -->
## workflow / 3 / on failure

<!-- block: b-3eec8e4551275fc58111 -->
<!-- field: field-0011 -->
Keep the verified correction in the incident system when downstream use cannot be observed.
<!-- /field -->
