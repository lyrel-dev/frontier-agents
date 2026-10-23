---
id: record-use-cases-UC-D01
kind: record
collection: use-cases
product: devops
title: Triage incident signals
order: 0
frozen: true
data:
  id: UC-D01
  platform: devops
  group: Incident response
  title: Triage incident signals
  summary: Route a signal to the appropriate investigation or justified exclusion.
  delivery: Built-in function
  cadence: Event-driven
  availability: GA production operations
  inputs: Incident identity, correlation evidence, skip criteria and active investigations.
  output: Triage decision, reason and resulting investigation linkage.
  sections:
  - D-06
  constraints:
    $markdown: field-0001
  example: Explain why this alert was linked, skipped or scheduled for a new investigation.
  keywords:
  - triage
  - alert
  - ticket
  - linked
  - skipped
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: On-call engineer
  objective: Route a signal to the appropriate investigation or justified exclusion.
  completion:
  - Decision and reason are visible.
  - The resulting investigation or exclusion is identifiable.
  profiles:
  - PR-D-INCIDENT
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC01
  aliases:
  - Incident signal triage
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Inspect routing
    purpose:
      $markdown: field-0005
    mechanism: MX-D-TRIAGE
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-INCIDENT
    effect: Investigation linkage
    verification: Inspect the routing decision, reason and resulting investigation identity.
    on_failure: Correct routing through the supported unlink or unskip operation.
---

<!-- block: b-3f011a769ae05f0cacd9 -->
## constraints

<!-- block: b-dd936696bcdf5326ae8f -->
<!-- field: field-0001 -->
A triage decision is not a diagnosis. Incorrect linking or skipping requires a routing correction.
<!-- /field -->

<!-- block: b-7a53c4a7bbd556d7bb2b -->
## narrative / 0

<!-- block: b-9eaf11a3b8155aa5b8d1 -->
<!-- field: field-0002 -->
An on-call engineer receives several alerts for the same service. Before opening another investigation, the engineer needs to know whether the new signal belongs to work already in progress. Inspect the triage decision and its reason, then follow the primary investigation when the signal was linked. A skipped signal should identify the matching exclusion rather than disappear from the operating record.
<!-- /field -->

<!-- block: b-82d75e7981c6560bac85 -->
## narrative / 1

<!-- block: b-1bda838933c35a20b0c5 -->
<!-- field: field-0003 -->
When correlation is wrong, unlink the signal so it can be investigated separately. When a skip criterion excluded a relevant event, review that criterion and use the supported unskip operation. The result of this use case is correct routing and an identifiable investigation, not a root-cause conclusion. Root-cause analysis follows in the next use case.
<!-- /field -->

<!-- block: b-74902523296553abaca1 -->
## steps basis

<!-- block: b-013ad44edbb55504b637 -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-741080bd4a6e56cdb4d0 -->
## workflow / 0 / purpose

<!-- block: b-21a0d6889df05992b481 -->
<!-- field: field-0005 -->
Determine whether this signal requires independent work.
<!-- /field -->
