---
id: record-use-cases-UC-S06
kind: record
collection: use-cases
product: security
title: Prepare a code-remediation proposal
order: 19
frozen: true
data:
  id: UC-S06
  platform: security
  group: Findings and repair
  title: Prepare a code-remediation proposal
  summary: Produce a reviewable source change for an accepted finding.
  delivery: Configured remediation
  cadence: On demand
  availability: Feature-specific; provider support applies
  inputs: Accepted finding, repository access and remediation configuration.
  output: Patch or pull request linked to the finding.
  sections:
  - S-05
  - S-09
  - S-M07
  constraints: A proposed patch is not a reviewed, deployed or verified repair.
  example:
    $markdown: field-0001
  keywords:
  - code remediation
  - patch
  - pull request
  narrative:
  - $markdown: field-0002
  - $markdown: field-0003
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Developer and security reviewer
  objective: Produce a reviewable source change for an accepted finding.
  completion:
  - The proposal matches the affected revision.
  - Tests and unrelated changes are reviewed.
  - Proposal, deployment and verification remain distinct.
  profiles:
  - PR-S-REVIEW
  variants: []
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC08
  aliases:
  - Proposed code remediation
  steps_basis:
    $markdown: field-0004
  workflow:
  - title: Confirm the finding evidence
    purpose:
      $markdown: field-0005
    mechanism: MX-S-FINDING
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-FINDINGS
    effect: Finding review record
    verification: Give the finding a disposition using evidence, impact and application-owner context.
    on_failure: Preserve uncertainty and obtain missing evidence before closure.
  - title: Create the supported repair proposal
    purpose:
      $markdown: field-0006
    mechanism: MX-S-FIX
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-FIX
    effect: Proposed repository change
    verification: Inspect revision, tests and unrelated changes before accepting the proposal.
    on_failure: Leave a failed or rejected proposal unfinished; merge is not deployment.
  - title: Review and test the candidate
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

<!-- block: b-b5eac66026e85f139e08 -->
## example

<!-- block: b-4b66962775fa5540a03c -->
<!-- field: field-0001 -->
Prepare a remediation change for the authorization finding and include tests; do not merge automatically.
<!-- /field -->

<!-- block: b-f821388d0924578fb7c4 -->
## narrative / 0

<!-- block: b-f0bb565915ca51b7834b -->
<!-- field: field-0002 -->
A developer has accepted a finding and wants a repair proposal against the affected source. Confirm the repository and supported remediation settings, then inspect the proposed patch or pull request. The review should include the security change, regression tests, and any unrelated behavior introduced by the proposal.
<!-- /field -->

<!-- block: b-598ddafe240f55ecafdf -->
## narrative / 1

<!-- block: b-4da9e1d055665e819a49 -->
<!-- field: field-0003 -->
Run the normal build and review process before deployment. A generated proposal that fails tests is unfinished work, and a merged revision that has not reached the target is not ready for revalidation. Preserve the finding identifier through the change and deployment records so the next test can evaluate the intended repair.
<!-- /field -->

<!-- block: b-6653bb5320b65c09ada8 -->
## steps basis

<!-- block: b-7842bdeb42e15544a898 -->
<!-- field: field-0004 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-ec00ff4e46d855b788fc -->
## workflow / 0 / purpose

<!-- block: b-c62909c278dc589a9a9a -->
<!-- field: field-0005 -->
Identify the defect and affected source.
<!-- /field -->

<!-- block: b-0bedc285917e5c5b92e6 -->
## workflow / 1 / purpose

<!-- block: b-2db728e77ac352bd8f41 -->
<!-- field: field-0006 -->
Produce the configured patch or pull request.
<!-- /field -->

<!-- block: b-45ca180dda0a5f5d9e2d -->
## workflow / 2 / purpose

<!-- block: b-c9844c34cf4c5baa81a2 -->
<!-- field: field-0007 -->
Use the normal build and review process; arrange deployment separately.
<!-- /field -->

<!-- block: b-24db93b75b475fbda678 -->
## workflow / 2 / verification

<!-- block: b-2f58e13faf8a5e3aa3e1 -->
<!-- field: field-0008 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
