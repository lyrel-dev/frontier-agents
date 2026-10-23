---
id: record-use-cases-UC-D08
kind: record
collection: use-cases
product: devops
title: Identify recurring incident patterns
order: 7
frozen: true
data:
  id: UC-D08
  platform: devops
  group: Reliability improvement
  title: Identify recurring incident patterns
  summary: Identify cross-incident conditions supported by investigation evidence.
  delivery: Built-in function
  cadence: Periodic or on demand
  availability: GA production operations
  inputs: Recent investigation history and managed learning context.
  output: Pattern summary, recurring-cause context and candidate prevention themes.
  sections:
  - D-M01
  - D-06
  - D-M07
  constraints: Historical similarity does not establish the cause of a new incident.
  example:
    $markdown: field-0001
  keywords:
  - incident pattern
  - recurring cause
  - similar incidents
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Reliability engineer
  objective: Identify cross-incident conditions supported by investigation evidence.
  completion:
  - Supporting investigation identities are retained.
  - Similar symptoms are distinguished from shared verified causes.
  - Proposed groupings can be challenged and revised.
  profiles:
  - PR-D-INCIDENT
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC11
  aliases:
  - Incident pattern identification
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Inspect historical context
    purpose:
      $markdown: field-0005
    mechanism: MX-D-RECALL
    dependency: optional
    condition: Relevant retained history is available.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-MEMORY
    effect: Context read
    verification:
      $markdown: field-0006
    on_failure:
      $markdown: field-0007
  - title: Evaluate investigation history
    purpose:
      $markdown: field-0008
    mechanism: MX-D-PREVENT
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-PREVENTION
    effect: Recommendation
    verification: Trace a proposed theme or improvement to supporting investigations.
    on_failure: Keep unsupported patterns as hypotheses and separate proposals from implemented changes.
  - title: Review the pattern grouping
    purpose:
      $markdown: field-0009
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0010
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
---

<!-- block: b-3b0e685103df51d38f62 -->
## example

<!-- block: b-b9260cfe72c95d3a85ab -->
<!-- field: field-0001 -->
Identify recurring checkout incident patterns and cite the investigations that support each pattern.
<!-- /field -->

<!-- block: b-bc9a2491f3375bb08c9b -->
## narrative / 0

<!-- block: b-3a7625ec04be5320b7a7 -->
<!-- field: field-0002 -->
Several investigations may share an operational weakness even when they were triggered by different alarms. Review the relevant investigation history and ask which causes or contributing conditions recur. Group the evidence by the proposed pattern and retain the supporting investigation identifiers so the grouping can be challenged.
<!-- /field -->

<!-- block: b-2d07bba95e8458259654 -->
## narrative / 1

<!-- block: b-65fa3114dfae51268aa7 -->
<!-- field: field-0003 -->
This analysis differs from retrieving the prior cause of one alarm: its purpose is to identify cross-incident themes worth prevention work. Similar symptoms without verified common causes should remain a candidate pattern. The next step is to review the prevention recommendations against those themes rather than assuming that a historical cluster explains the next incident.
<!-- /field -->

<!-- block: b-7579af0cbb7c540ba535 -->
## steps basis

<!-- block: b-461c2c869fc858129d93 -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-66ee6226b3ce5d9aa735 -->
## workflow / 0 / purpose

<!-- block: b-71e1de0f2f075b49ab8e -->
<!-- field: field-0005 -->
Locate recurring themes without assuming an identical cause.
<!-- /field -->

<!-- block: b-f4743cc3ffc8506a9a14 -->
## workflow / 0 / verification

<!-- block: b-93a184eacb6f57478396 -->
<!-- field: field-0006 -->
Distinguish entry existence, observable retrieval and correctness against current evidence.
<!-- /field -->

<!-- block: b-9e394dd3ad2e5546b1fd -->
## workflow / 0 / on failure

<!-- block: b-dba378e98b2658eda58a -->
<!-- field: field-0007 -->
Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.
<!-- /field -->

<!-- block: b-56c85972a5ce518bb552 -->
## workflow / 1 / purpose

<!-- block: b-bc397bb24d8751fb9abb -->
<!-- field: field-0008 -->
Examine common weaknesses across investigations.
<!-- /field -->

<!-- block: b-8324182b02485420878e -->
## workflow / 2 / purpose

<!-- block: b-78e7c95a7c51533fbc22 -->
<!-- field: field-0009 -->
Check each grouping against the cited investigations.
<!-- /field -->

<!-- block: b-34b07a01b6e65cd782bb -->
## workflow / 2 / verification

<!-- block: b-bd74061823c65d8692c0 -->
<!-- field: field-0010 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
