---
id: record-use-cases-UC-F06
kind: record
collection: use-cases
product: finops
title: Prioritize optimization recommendations
order: 27
frozen: true
data:
  id: UC-F06
  platform: finops
  group: Anomalies and optimization
  title: Prioritize optimization recommendations
  summary: Select actionable upstream recommendations under workload constraints.
  delivery: Native function with team review
  cadence: On demand
  availability: Preview
  inputs:
    $markdown: field-0001
  output: Prioritized candidate, rejected/deferred reason and accepted next step.
  sections:
  - F-M01
  - F-08
  - F-M02
  - F-05
  - F-M06
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - optimization
  - recommendation
  - Compute Optimizer
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Service and cost owner
  objective: Select actionable upstream recommendations under workload constraints.
  completion:
  - Original source assumptions are retained.
  - Overlapping savings estimates are not indiscriminately summed.
  - Accepted, deferred and rejected work has explicit reasons.
  profiles:
  - PR-F-ANALYSIS
  - PR-F-PUBLICATION
  variants: []
  schema_version: 2
  platforms:
  - finops
  legacy_ids:
  - F-UC09
  aliases:
  - Optimization recommendation triage
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Retrieve upstream recommendations
    purpose:
      $markdown: field-0007
    mechanism: MX-F-QUERY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-SOURCES
    effect: Source read
    verification: Reconcile a material result using the same dates, metric, scope and dimensions.
    on_failure: Withhold unsupported numerical or causal conclusions and identify missing sources.
  - title: Apply workload-owner context
    purpose:
      $markdown: field-0008
    mechanism: MX-F-FILES
    dependency: optional
    condition: The recommendation depends on uploaded mappings.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-FILES
    effect: Context read
    verification: Verify a known mapping and expose unmapped records.
    on_failure: Keep unassigned values visible and update the authoritative file deliberately.
  - title: Review candidate changes
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
  - title: Create an owned follow-up
    purpose:
      $markdown: field-0011
    mechanism: MX-F-JIRA
    dependency: optional
    condition: The destination and invocation-specific authorization are satisfied.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-F-JIRA
    effect: External publication
    verification: Inspect invocation type, action details, destination and resulting issue or comment.
    on_failure:
      $markdown: field-0012
---

<!-- block: b-c7ce6a2850b057fda728 -->
## inputs

<!-- block: b-f1068319540f593bae61 -->
<!-- field: field-0001 -->
Cost Optimization Hub or Compute Optimizer recommendation, workload evidence and owner constraints.
<!-- /field -->

<!-- block: b-87c7d92acd6456a7b98c -->
## constraints

<!-- block: b-6ba33708068a53bf9725 -->
<!-- field: field-0002 -->
The agent contextualizes upstream recommendations; it does not independently calculate or authorize the change.
<!-- /field -->

<!-- block: b-8564e1dee6e65ebaa311 -->
## example

<!-- block: b-6b898f6ed1cd5459a1c0 -->
<!-- field: field-0003 -->
Review the storage recommendations, identify overlapping savings and list the reliability constraints.
<!-- /field -->

<!-- block: b-5a0412bb6aa351e39e3f -->
## narrative / 0

<!-- block: b-0aa74347fff05aad8e03 -->
<!-- field: field-0004 -->
An optimization source proposes several changes for a service. Retrieve the original recommendations and inspect their assumptions, resource scope, and overlapping savings estimates. Add workload constraints such as latency, resilience, deployment risk, and ownership before prioritizing the candidates.
<!-- /field -->

<!-- block: b-1b21e8bb28f75b2fb534 -->
## narrative / 1

<!-- block: b-082db36836cc58debfa8 -->
<!-- field: field-0005 -->
Record why each candidate is accepted, deferred, or rejected and identify the normal engineering process for an accepted change. The underlying recommendations originate in the documented optimization services. The agent’s explanation does not independently measure future savings or authorize an infrastructure change.
<!-- /field -->

<!-- block: b-d19c755bc989560fb168 -->
## steps basis

<!-- block: b-36d61d0a546759fe8741 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-b4ea332c22865b46a2df -->
## workflow / 0 / purpose

<!-- block: b-7e4a954deb3f5651bbdc -->
<!-- field: field-0007 -->
Read the original candidates, assumptions and resource scope.
<!-- /field -->

<!-- block: b-5253356167c75f25970e -->
## workflow / 1 / purpose

<!-- block: b-369905570c8c52b78b6e -->
<!-- field: field-0008 -->
Use reviewed ownership and operating constraints.
<!-- /field -->

<!-- block: b-0550ff2ea2855883a481 -->
## workflow / 2 / purpose

<!-- block: b-52f2ec94b2c35880b835 -->
<!-- field: field-0009 -->
Compare reliability, performance and implementation risk with estimated benefit.
<!-- /field -->

<!-- block: b-5f3dd749661757d694a3 -->
## workflow / 2 / verification

<!-- block: b-b2e0f0f3cfa45ab295b4 -->
<!-- field: field-0010 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->

<!-- block: b-462665b87774553c8f6a -->
## workflow / 3 / purpose

<!-- block: b-26b804e41be0529db82e -->
<!-- field: field-0011 -->
Publish accepted work with evidence and acceptance criteria.
<!-- /field -->

<!-- block: b-2ee07560781b5ee38ace -->
## workflow / 3 / on failure

<!-- block: b-a5a4990116725a13919e -->
<!-- field: field-0012 -->
Stop incorrect destinations. Do not expect an interactive prompt to protect an unattended automation.
<!-- /field -->
