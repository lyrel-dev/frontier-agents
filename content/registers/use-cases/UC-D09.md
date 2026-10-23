---
id: record-use-cases-UC-D09
kind: record
collection: use-cases
product: devops
title: Prioritize incident-prevention work
order: 8
frozen: true
data:
  id: UC-D09
  platform: devops
  group: Reliability improvement
  title: Prioritize incident-prevention work
  summary: Turn evidence-backed improvement proposals into owned engineering work.
  delivery: Built-in function
  cadence: Weekly or on demand
  availability: GA production operations
  inputs: Multiple incident investigations, team priorities and recommendation evaluation.
  output: Ranked recommendations with source incidents, expected effect and backlog state.
  sections:
  - D-06
  constraints:
    $markdown: field-0001
  example:
    $markdown: field-0002
  keywords:
  - prevention
  - improvements
  - recommendations
  - backlog
  narrative:
  - $markdown: field-0003
  - $markdown: field-0004
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Reliability owner
  objective: Turn evidence-backed improvement proposals into owned engineering work.
  completion:
  - Accepted proposals retain source incidents.
  - An owner and acceptance criterion are assigned.
  - Proposal status is distinct from implementation evidence.
  profiles:
  - PR-D-INCIDENT
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC12
  aliases:
  - Prevention recommendation backlog
  steps_basis:
    $markdown: field-0005
  workflow:
  - title: Inspect the prevention evaluation
    purpose:
      $markdown: field-0006
    mechanism: MX-D-PREVENT
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-PREVENTION
    effect: Recommendation
    verification: Trace a proposed theme or improvement to supporting investigations.
    on_failure: Keep unsupported patterns as hypotheses and separate proposals from implemented changes.
  - title: Prioritize and assign accepted work
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
---

<!-- block: b-547bec44289453019789 -->
## constraints

<!-- block: b-bd061b49753052a49cf0 -->
<!-- field: field-0001 -->
Recommendations are not automatically implemented and may age out when not kept or implemented.
<!-- /field -->

<!-- block: b-b397e8e48b3b57b392b8 -->
## example

<!-- block: b-b77dcf9b3dd85169bc14 -->
<!-- field: field-0002 -->
Run a prevention evaluation and return the highest-priority recommendations with affected incidents and owners.
<!-- /field -->

<!-- block: b-9f62ce7849be5fd982a4 -->
## narrative / 0

<!-- block: b-008b534aa23c5d45872c -->
<!-- field: field-0003 -->
The reliability owner has identified recurring themes and needs a manageable prevention backlog. Run or inspect the documented prevention evaluation, then review each recommendation against the incidents it addresses. Separate observability improvements, infrastructure changes, governance work, and code changes because they have different owners and acceptance evidence.
<!-- /field -->

<!-- block: b-fc6b3e7c67565ff2b578 -->
## narrative / 1

<!-- block: b-a9d2cb371d05592bb2ae -->
<!-- field: field-0004 -->
Keep an accepted recommendation linked to its source evidence and normal change process. A recommendation’s priority or estimated effect is not proof that the change has been implemented. During the next operational review, inspect actual progress and post-change observations. This closes the team’s improvement loop without claiming autonomous implementation or measured benefit before either exists.
<!-- /field -->

<!-- block: b-4687ccf7c9c65028bf34 -->
## steps basis

<!-- block: b-eb5a9d17f3ff566ab791 -->
<!-- field: field-0005 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-66fe84a58a4e5c09be9a -->
## workflow / 0 / purpose

<!-- block: b-68166fd9bc2459928159 -->
<!-- field: field-0006 -->
Identify proposals relevant to recurring weaknesses.
<!-- /field -->

<!-- block: b-8da180d60ac65cc18f24 -->
## workflow / 1 / purpose

<!-- block: b-39acf6ca85665a58a44b -->
<!-- field: field-0007 -->
Compare risk, dependencies and implementation effort through normal team review.
<!-- /field -->

<!-- block: b-cbbcb3db05ff50f8bfa2 -->
## workflow / 1 / verification

<!-- block: b-1c10eaef25615cd395fd -->
<!-- field: field-0008 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
