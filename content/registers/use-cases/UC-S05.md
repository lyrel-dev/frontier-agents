---
id: record-use-cases-UC-S05
kind: record
collection: use-cases
product: security
title: Triage and prioritize security findings
order: 18
frozen: true
data:
  id: UC-S05
  platform: security
  group: Findings and repair
  title: Triage and prioritize security findings
  summary: Give findings an evidence-based disposition and accountable next action.
  delivery: Native operation
  cadence: On demand
  availability: Feature-specific
  inputs: Completed assessment findings and application-owner context.
  output: Prioritized finding with owner, disposition and remediation plan.
  sections:
  - S-05
  - S-09
  - S-M07
  constraints: Finding count or severity alone is not an adequate risk decision.
  example: Prioritize the findings using impact, confidence, affected role and reproduction evidence.
  keywords:
  - finding triage
  - prioritization
  - CVSS
  narrative:
  - $markdown: field-0001
  - $markdown: field-0002
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Finding owner
  objective: Give findings an evidence-based disposition and accountable next action.
  completion:
  - Impact and evidence are reviewed.
  - Finding identity is preserved.
  - Accepted work has an owner and acceptance test.
  profiles:
  - PR-S-REVIEW
  variants: []
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC06
  aliases:
  - Finding review and prioritization
  steps_basis:
    $markdown: field-0003
  workflow:
  - title: Review the finding in context
    purpose:
      $markdown: field-0004
    mechanism: MX-S-FINDING
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-FINDINGS
    effect: Finding review record
    verification: Give the finding a disposition using evidence, impact and application-owner context.
    on_failure: Preserve uncertainty and obtain missing evidence before closure.
  - title: Assign priority and responsibility
    purpose:
      $markdown: field-0005
    mechanism: null
    dependency: required
    condition: Applies to the selected implementation.
    actor: Responsible engineer or reviewer
    configuration_features: []
    effect: Team decision; no implicit service action
    verification:
      $markdown: field-0006
    on_failure: Keep the result unresolved and assign the missing decision or evidence to an owner.
  - title: Publish accepted work to Jira
    purpose:
      $markdown: field-0007
    mechanism: MX-S-JIRA
    dependency: optional
    condition: A permitted destination and disclosure scope are configured.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-JIRA
    effect: External publication
    verification: Inspect actual project audience and original finding linkage.
    on_failure: Keep the finding owned locally while resolving publication failure.
---

<!-- block: b-f0022c5a2e1c559eb793 -->
## narrative / 0

<!-- block: b-f82ffc50c88159c5919a -->
<!-- field: field-0001 -->
A completed assessment contains findings of different severity and evidential strength. Review each material finding in the context of the affected revision, reachable role, exposed data, and reproduction evidence. Add application-owner context before deciding which finding needs immediate repair and which requires more investigation.
<!-- /field -->

<!-- block: b-6f1bbf21b2ef5b37bc7e -->
## narrative / 1

<!-- block: b-73ce59ad80a3514aa5b3 -->
<!-- field: field-0002 -->
The outcome is a disposition and an accountable next action, not merely a sorted severity list. Findings with incomplete evidence should retain that uncertainty. Link accepted work to the original finding identifier so remediation, deployment, and later verification remain traceable even if the issue title or owner changes.
<!-- /field -->

<!-- block: b-5cc4d5ea147d576fb77a -->
## steps basis

<!-- block: b-7c2bcc082f775a7c9ca4 -->
<!-- field: field-0003 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-ba9e183627fc57fc80e2 -->
## workflow / 0 / purpose

<!-- block: b-8a0a82816ccc58acac6a -->
<!-- field: field-0004 -->
Evaluate the affected revision, application role and supporting evidence.
<!-- /field -->

<!-- block: b-93afc83bd6d35dd7b1ff -->
## workflow / 1 / purpose

<!-- block: b-bec6d03301975172982c -->
<!-- field: field-0005 -->
Use application impact and evidence rather than severity alone.
<!-- /field -->

<!-- block: b-3725de8acb31513db79c -->
## workflow / 1 / verification

<!-- block: b-cccafb756268527c9277 -->
<!-- field: field-0006 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->

<!-- block: b-b7fd3e4cd7525d0284ce -->
## workflow / 2 / purpose

<!-- block: b-6e164e2d420c5979950a -->
<!-- field: field-0007 -->
Preserve finding linkage in an appropriate project.
<!-- /field -->
