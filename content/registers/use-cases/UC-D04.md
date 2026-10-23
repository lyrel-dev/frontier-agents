---
id: record-use-cases-UC-D04
kind: record
collection: use-cases
product: devops
title: Execute an approved mitigation and verify recovery
order: 3
frozen: true
data:
  id: UC-D04
  platform: devops
  group: Incident response
  title: Execute an approved mitigation and verify recovery
  summary: Carry out an eligible approved change and assess service recovery.
  delivery: Controlled action
  cadence: On demand
  availability: GA operations; directed actions require opt-in
  inputs:
    $markdown: field-0001
  output: Attributed action record and independently checked resulting state.
  sections:
  - D-M06
  - D-03
  - D-12
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - directed action
  - approval
  - mutation
  - CloudTrail
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Authorized incident operator
  objective: Carry out an eligible approved change and assess service recovery.
  completion:
  - Exact operation and target were approved.
  - Attributed resulting state is retained.
  - Recovery is assessed against current service measurements.
  profiles:
  - PR-D-ACTION
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC05
  aliases:
  - Approved directed mitigation
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Authorize and execute the eligible action
    purpose:
      $markdown: field-0007
    mechanism: MX-D-ACTION
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-ACTIONS
    effect: Resource or external-tool mutation
    verification: Inspect exact approval, attribution and resulting resource state.
    on_failure:
      $markdown: field-0008
  - title: Measure post-change service state
    purpose:
      $markdown: field-0009
    mechanism: MX-D-READ
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-SOURCES
    effect: Source read
    verification: Compare returned identifiers and a material measurement with the original source.
    on_failure: Report the failed read and withhold conclusions that require that source.
  - title: Decide whether recovery is established
    purpose:
      $markdown: field-0010
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0011
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
---

<!-- block: b-66561e32ebfe596da9de -->
## inputs

<!-- block: b-bde8e01a0fbb54fdbe3b -->
<!-- field: field-0001 -->
Directed-action enablement, eligible role or integration, correct tool classification and exact operation/resource approval.
<!-- /field -->

<!-- block: b-44a67b3f7a685c988d49 -->
## constraints

<!-- block: b-c92b867f16ef524fbcbb -->
<!-- field: field-0002 -->
Approval is scoped to a particular operation and resource. Tool misclassification can change expected approval behavior.
<!-- /field -->

<!-- block: b-045be82a3ff250148d8c -->
## example

<!-- block: b-621903cc69b05c048069 -->
<!-- field: field-0003 -->
After showing the exact target and parameters, request approval for the narrowly scoped change.
<!-- /field -->

<!-- block: b-5428ffb647a55641b3da -->
## narrative / 0

<!-- block: b-f617f94228bc511ca8f8 -->
<!-- field: field-0004 -->
An incident owner has accepted a narrowly scoped mitigation and wants to use the documented action path. Confirm Agent Space enablement, the target-account role or connected-tool configuration, and the classification of the operation. Review the actual parameters presented for approval; a broadly named role is not the approval record.
<!-- /field -->

<!-- block: b-8f9ae160917b5c089824 -->
## narrative / 1

<!-- block: b-573ead99a9915426b333 -->
<!-- field: field-0005 -->
After the operator approves the eligible action, inspect the resulting resource state and the available attribution evidence. Recovery must still be checked against service measurements. If execution is denied, locate the failed gate instead of widening all permissions. This workflow does not convert the earlier mitigation recommendation into standing authorization for subsequent changes.
<!-- /field -->

<!-- block: b-a17de415fb055a4094c0 -->
## steps basis

<!-- block: b-3e6d620b4dce5dcc9a41 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-7ef1ded2db335370aa22 -->
## workflow / 0 / purpose

<!-- block: b-20cc7dda8371512db058 -->
<!-- field: field-0007 -->
Apply the specific reviewed operation rather than standing authorization.
<!-- /field -->

<!-- block: b-d72c2ad3d1e05094b5c4 -->
## workflow / 0 / on failure

<!-- block: b-039ce272a0275967921d -->
<!-- field: field-0008 -->
Stop on a failed authorization gate; use the normal approved engineering process rather than bypassing it.
<!-- /field -->

<!-- block: b-b4541f6092255191bcc8 -->
## workflow / 1 / purpose

<!-- block: b-e28f8c498cc25a419728 -->
<!-- field: field-0009 -->
Determine whether the action had its intended effect.
<!-- /field -->

<!-- block: b-fa34af07682f54929a51 -->
## workflow / 2 / purpose

<!-- block: b-f7dd228f221552ce9bcb -->
<!-- field: field-0010 -->
Apply the declared recovery or rollback conditions.
<!-- /field -->

<!-- block: b-711c5b311185546c9ef9 -->
## workflow / 2 / verification

<!-- block: b-4bb04f8e68675a4fb7c9 -->
<!-- field: field-0011 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
