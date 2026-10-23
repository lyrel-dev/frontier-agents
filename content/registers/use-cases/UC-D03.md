---
id: record-use-cases-UC-D03
kind: record
collection: use-cases
product: devops
title: Prepare a mitigation plan
order: 2
frozen: true
data:
  id: UC-D03
  platform: devops
  group: Incident response
  title: Prepare a mitigation plan
  summary: Prepare a proposed change that a reviewer can approve, reject or revise.
  delivery: Built-in function
  cadence: On demand
  availability: GA production operations
  inputs: Reviewed incident evidence and a specific operational objective.
  output: Mitigation proposal suitable for operator approval or normal runbook execution.
  sections:
  - D-06
  - D-M06
  constraints:
    $markdown: field-0001
  example: Propose the lowest-risk mitigation, including blast radius, rollback and recovery checks.
  keywords:
  - mitigation
  - rollback
  - recovery
  - proposal
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Incident owner
  objective: Prepare a proposed change that a reviewer can approve, reject or revise.
  completion:
  - Target and proposed effect are explicit.
  - Risk, rollback and recovery checks are reviewable.
  - Planning has not been represented as execution.
  profiles:
  - PR-D-INCIDENT
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC04
  aliases:
  - Mitigation plan preparation
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Review the incident explanation
    purpose:
      $markdown: field-0005
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
  - title: Review the proposed mitigation
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
---

<!-- block: b-e0b7f9c94c2e5a91b897 -->
## constraints

<!-- block: b-834bcef196c45998bd3c -->
<!-- field: field-0001 -->
A proposal is not permission to execute. Unsupported or high-risk actions remain outside the action path.
<!-- /field -->

<!-- block: b-ebecdc83e2e25050b75b -->
## narrative / 0

<!-- block: b-e7aad4c925d651ab85b0 -->
<!-- field: field-0002 -->
Once the current evidence supports a likely failure mechanism, the incident owner needs a mitigation that can be reviewed. Ask for the proposed target, exact change, expected effect, risks, rollback, and recovery checks. Compare that proposal with the approved runbook and the evidence already collected, especially where the proposed action would affect another service.
<!-- /field -->

<!-- block: b-7f11ccb8a96753bdaf83 -->
## narrative / 1

<!-- block: b-dc81c3dc0b9051d9b91f -->
<!-- field: field-0003 -->
The output is a decision document: it should make it possible to approve, reject, or revise the proposal without guessing its effect. A generated plan remains separate from execution. It can be carried out through the ordinary engineering process, or through an eligible directed-action path after the additional controls described in the next use case have been satisfied.
<!-- /field -->

<!-- block: b-92d2958f51965a899ab8 -->
## steps basis

<!-- block: b-7abced2c9cba57869046 -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-e1a70025a3aa5aa58900 -->
## workflow / 0 / purpose

<!-- block: b-950c1475a50f5ce090b0 -->
<!-- field: field-0005 -->
Use evidence appropriate to the proposed mitigation.
<!-- /field -->

<!-- block: b-8476a3f37deb5e70b96e -->
## workflow / 1 / purpose

<!-- block: b-95d899ff829c5861b7b9 -->
<!-- field: field-0006 -->
Compare target, effect, risk and rollback with the approved procedure.
<!-- /field -->

<!-- block: b-743008b490d55422b83b -->
## workflow / 1 / verification

<!-- block: b-62f1afacc27f559ea2a9 -->
<!-- field: field-0007 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
