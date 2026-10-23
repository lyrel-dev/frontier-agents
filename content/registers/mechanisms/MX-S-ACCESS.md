---
id: record-mechanisms-MX-S-ACCESS
kind: record
collection: mechanisms
product: security
title: Target scope and network access
order: 15
frozen: true
data:
  id: MX-S-ACCESS
  platform: security
  title: Target scope and network access
  features:
  - FT-S-TARGET
  sections:
  - S-03
  trigger: Configuration and target connection
  state: Targets, support paths, exclusions and private route
  process:
    $markdown: field-0001
  effect: Target connection
  verification: Confirm the permitted surface and exclusions in an authorized environment.
  on_failure: Stop when scope or owner authorization is unresolved.
  review:
    primary_section: S-03
    kind: Target-selection and reachability mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Target
      - 'Create/edit penetration test: select verified target URLs.'
      - Active test surface
    - - Supporting access
      - List necessary accessible URLs separately.
      - Navigation support, not attack targets
    - - Exclusions and network
      - Configure excluded paths and the approved VPC connectivity when required.
      - Scope and network controls
    lifecycle:
    - - Configuration saved
      - Preflight/connection attempted
      - Reachability is checked before meaningful target testing.
    - - Target unreachable
      - Correct approved route or name resolution
      - Rerun the prerequisite check without broadening authorization.
    - - Scope changed
      - Review authorization and save configuration
      - A future run has a different assessment surface.
    controls:
      $markdown: field-0005
    observable_output: Preflight outcome and records of the actual target and paths reached.
    undocumented:
      $markdown: field-0006
    test:
    - Use a non-production target, supporting login host and an explicit excluded fixture path.
    - Verify target access and intended application role.
    - A denied path or unresolved target must not produce a claim of assessed coverage.
    claims:
    - source: SS402
      section: Configure penetration test scope; Configure VPC resources
      assertion: Targets, supporting accessible URLs and excluded paths have different purposes.
    - source: SS418
      section: Review penetration test findings
      assertion: Failed preflight stops testing and must be inspected separately.
---

<!-- block: b-d13cfc3e583e5ba990d4 -->
## process

<!-- block: b-205aff7505335ed383af -->
<!-- field: field-0001 -->
Apply the configured reachability and target rules to assessment access.
<!-- /field -->

<!-- block: b-476b15ec8b6052c7817a -->
## review / inputs

<!-- block: b-d618f717fe855b5ca5d3 -->
<!-- field: field-0002 -->
Verified target domains, supporting accessible domains, excluded paths, applicable VPC route and authorized test scope.
<!-- /field -->

<!-- block: b-35a7c4bb705659fc907a -->
## review / narrative / 0

<!-- block: b-4112c5db2a865e8d9a4d -->
<!-- field: field-0003 -->
The test configuration separates attack targets from supporting navigation and excluded paths. A login provider can be reachable without becoming a vulnerability-testing target. A private route supplies connectivity; it does not widen the scope approved by the application owner.
<!-- /field -->

<!-- block: b-e3b86c92fb2b5be2a396 -->
## review / narrative / 1

<!-- block: b-7f423059b1855bb3ba97 -->
<!-- field: field-0004 -->
Treat reachability as a prerequisite. If a target cannot be reached, the missing result is a coverage gap. Broadening the target list or removing an exclusion is a scope change, not a routine network troubleshooting shortcut.
<!-- /field -->

<!-- block: b-4274f65118245fcd9e0d -->
## review / controls

<!-- block: b-bcb6505564605f149a2a -->
<!-- field: field-0005 -->
Ownership verification and network reachability are not substitutes for owner authorization. Active tests can change application state.
<!-- /field -->

<!-- block: b-1074fd07a0795c55a0c0 -->
## review / undocumented

<!-- block: b-3fae30de778c528c9f8f -->
<!-- field: field-0006 -->
The sources do not establish that every reachable path is exercised or that every excluded interaction has a uniform implementation across all targets.
<!-- /field -->
