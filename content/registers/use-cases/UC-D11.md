---
id: record-use-cases-UC-D11
kind: record
collection: use-cases
product: devops
title: Document service topology and dependencies
order: 10
frozen: true
data:
  id: UC-D11
  platform: devops
  group: Operational knowledge
  title: Document service topology and dependencies
  summary: Produce a reviewed service and dependency description.
  delivery: Built-in function with composed documentation
  cadence: On demand or refreshed
  availability: GA production operations
  inputs:
    $markdown: field-0001
  output: Topology view and environment summary that can support architecture documentation.
  sections:
  - D-05
  - D-12
  - D-M08
  - D-03
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - topology
  - dependency map
  - architecture documentation
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Service owner
  objective: Produce a reviewed service and dependency description.
  completion:
  - Observed and inferred relationships are distinguished.
  - Deployed revision and evidence are recorded.
  - Unresolved relationships have owners.
  profiles:
  - PR-D-KNOWLEDGE
  - PR-EVIDENCE
  variants: []
  schema_version: 2
  platforms:
  - devops
  legacy_ids:
  - D-UC16
  aliases:
  - Topology documentation and dependency map
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Inspect environment consolidation
    purpose:
      $markdown: field-0007
    mechanism: MX-D-TOPOLOGY
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-D-TOPOLOGY
    - FT-D-MEMORY
    effect: Retained context update
    verification: Check a known changed resource and relationship in the resulting version.
    on_failure:
      $markdown: field-0008
  - title: Check important source relationships
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
  - title: Maintain the reviewed description
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

<!-- block: b-ff6bb075bc9355138f20 -->
## inputs

<!-- block: b-d67c035e08185789816d -->
<!-- field: field-0001 -->
Connected accounts, discovery, Resource Explorer where applicable and relevant integrations.
<!-- /field -->

<!-- block: b-1c90306a1d8a59608b5b -->
## constraints

<!-- block: b-dd5cb882084f569f9ecc -->
<!-- field: field-0002 -->
Topology is a representation, not an authorization boundary or guaranteed complete inventory.
<!-- /field -->

<!-- block: b-3eb4dd1ca8e750649a7e -->
## example

<!-- block: b-b6b7c18dac105618b83d -->
<!-- field: field-0003 -->
Document the payments service containers, downstream dependencies, repositories and deployment boundaries; mark inferred relationships.
<!-- /field -->

<!-- block: b-0c63e9052ffd5c0e9f4f -->
## narrative / 0

<!-- block: b-daf4b8bcff7b58fe8c11 -->
<!-- field: field-0004 -->
A service owner needs an architecture description before changing a dependency. Start from discovered resources and the topology’s service, repository, pipeline, and dependency relationships. Compare those relationships with the deployed configuration and source revision, distinguishing directly observed relationships from inferred ones.
<!-- /field -->

<!-- block: b-b33698ddd190552aaf97 -->
## narrative / 1

<!-- block: b-c7034322118b504591ce -->
<!-- field: field-0005 -->
Write the reviewed result as a maintained service description with identifiers, evidence links, and unresolved edges. The topology is useful input to that document, but it is not a guaranteed complete inventory or an automatic update to the team’s architecture repository. This use case produces owner-reviewed documentation; the following refresh use case checks whether the underlying environment model has changed.
<!-- /field -->

<!-- block: b-66fed67403135b878fc9 -->
## steps basis

<!-- block: b-426676c0604356849ce9 -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-b6ec7188615156a69809 -->
## workflow / 0 / purpose

<!-- block: b-0fde7eb7e487517e9f98 -->
<!-- field: field-0007 -->
Use discovery and the resulting retained representation.
<!-- /field -->

<!-- block: b-9842acda225d52219daa -->
## workflow / 0 / on failure

<!-- block: b-b3b964b3114d5b2bbf74 -->
<!-- field: field-0008 -->
Mark stale or inferred relationships; do not substitute the graph for current configuration.
<!-- /field -->

<!-- block: b-0cfc72dd8d45526898ad -->
## workflow / 1 / purpose

<!-- block: b-7f94aa4576bc5e1b97ed -->
<!-- field: field-0009 -->
Compare graph edges with deployment and source evidence.
<!-- /field -->

<!-- block: b-2606c3f471dc5017a936 -->
## workflow / 2 / purpose

<!-- block: b-6037a9031e0d594f89cd -->
<!-- field: field-0010 -->
Record owner-verified relationships and unresolved discrepancies.
<!-- /field -->

<!-- block: b-4df47d12b6ab574c9909 -->
## workflow / 2 / verification

<!-- block: b-e57a02e6a55255109a16 -->
<!-- field: field-0011 -->
Record the decision with the source identifiers and evidence needed for the case completion criteria.
<!-- /field -->
