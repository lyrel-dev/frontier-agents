---
id: record-use-cases-UC-D10
kind: record
collection: use-cases
product: devops
title: Consolidate and maintain operational procedures
order: 9
frozen: true
data:
  id: UC-D10
  platform: devops
  group: Operational knowledge
  title: Consolidate and maintain operational procedures
  summary: Maintain one reviewed procedure for the intended operational situation.
  delivery: Composed workflow
  cadence: On demand
  availability: GA skills
  inputs: Reviewed SOP, target agent types, actual tool names and expected evidence.
  output: Version-controlled SKILL.md bundle and a matching/nonmatching selection test.
  sections:
  - D-M04
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - SOP
  - runbook
  - skill
  - procedure consolidation
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Runbook owner
  objective: Maintain one reviewed procedure for the intended operational situation.
  completion:
  - Conflicting or stale instructions are resolved.
  - Actual tools and stop conditions are defined.
  - Applicability tests include matching and nonmatching requests.
  profiles:
  - PR-D-PROCEDURE
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC14
  aliases:
  - SOP consolidation into reusable skills
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Reconcile authoritative procedures
    purpose:
      $markdown: field-0006
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0007
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
  - title: Publish and test the procedural skill
    purpose:
      $markdown: field-0008
    mechanism: MX-D-SKILL
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SKILLS
    effect: Procedural context
    verification: Test matching and nonmatching requests and inspect exposed procedure or tool-use evidence.
    on_failure:
      $markdown: field-0009
---

<!-- block: b-d96db031052d5a509c27 -->
## constraints

<!-- block: b-07d26f08cf38535f9e75 -->
<!-- field: field-0001 -->
Consolidation and review are team work. A skill supplies procedure; it does not grant tools or permissions.
<!-- /field -->

<!-- block: b-ae8eb4d25eb856e096d6 -->
## example

<!-- block: b-5e210933b2e55ab1aa01 -->
<!-- field: field-0002 -->
Create a skill from the approved checkout timeout SOP and state when it should and should not load.
<!-- /field -->

<!-- block: b-b37292ac62d754cfa02d -->
## narrative / 0

<!-- block: b-60ed63f6b5f25593b974 -->
<!-- field: field-0003 -->
A team has several overlapping timeout SOPs maintained by different owners. First reconcile their scope, resolve contradictory steps, remove stale tool names, and identify the approved procedure. Only then package that procedure as a skill with a description that states when it applies and which agent types may use it.
<!-- /field -->

<!-- block: b-f972a174dfdc5e39836b -->
## narrative / 1

<!-- block: b-9a20c94da22e5e5d83e7 -->
<!-- field: field-0004 -->
Keep the reviewed source in Git and test a request that should match the skill alongside one that should not. The supporting references should explain the expected observations and the point at which the procedure stops or escalates. Consolidation is authored team work; skill selection is the platform mechanism. A skill neither creates the referenced tools nor grants permission to use them.
<!-- /field -->

<!-- block: b-85d2af05a96151418f7d -->
## steps basis

<!-- block: b-41e5feaf5d735c33aa6f -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-377e8e4715e256ccbe9d -->
## workflow / 0 / purpose

<!-- block: b-d1b4c9c79178586381d8 -->
<!-- field: field-0006 -->
Resolve conflicting scope, stale commands and ownership before packaging.
<!-- /field -->

<!-- block: b-506888c42bf652f28af6 -->
## workflow / 0 / verification

<!-- block: b-5762489ddf1e5a50a774 -->
<!-- field: field-0007 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->

<!-- block: b-0bed212727225126b264 -->
## workflow / 1 / purpose

<!-- block: b-07534b6348645cf2b493 -->
<!-- field: field-0008 -->
Make the reviewed procedure available to the intended agent scope.
<!-- /field -->

<!-- block: b-bf58189350c95e8c995c -->
## workflow / 1 / on failure

<!-- block: b-d1d858e71eb15112a73d -->
<!-- field: field-0009 -->
Correct applicability or missing tools; stop unsupported steps without implicitly widening permissions.
<!-- /field -->
