---
id: record-mechanisms-MX-S-CODE
kind: record
collection: mechanisms
product: security
title: Full-source or change-focused code assessment
order: 24
frozen: true
data:
  id: MX-S-CODE
  platform: security
  title: Full-source or change-focused code assessment
  features:
  - FT-S-CODE
  - FT-S-SOURCES
  sections:
  - S-06
  trigger: Eligible source-review invocation
  state: Revision, review mode and findings
  process:
    $markdown: field-0001
  effect: Source analysis; optional comments separately configured
  verification: Match results to the revision and record unassessed scope.
  on_failure: Obtain a current result when revision or trigger behavior makes prior evidence stale.
  review:
    primary_section: S-06
    kind: Source-analysis workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Full review
      - 'Web app → Code reviews → create: select sources and role; Start review.'
      - Saved source assessment
    - - Modes
      - Select vulnerability findings, requirement evaluation or both.
      - Analysis criteria
    - - Change guidance
      - Review supported provider triggers and .awssecurityagent/filtering.md on the main branch.
      - Change scope and filtering
    lifecycle:
    - - Review requested
      - Preflight
      - Source/environment prerequisites checked.
    - - Preflight fails
      - Fix access and start a new run
      - Static analysis has not completed.
    - - Source revision changes
      - Supported new review/reanalysis
      - Prior findings remain revision-specific.
    controls:
      $markdown: field-0005
    observable_output: Preflight results, reviewed revision, findings and any configured provider comments.
    undocumented:
      $markdown: field-0006
    test:
    - Review a known source fixture with exact commit identity.
    - Check that findings reference the expected revision and modes.
    - Deny source access or exclude a known fixture path; retain the resulting assessment gap.
    claims:
    - source: SS410
      section: Create and run a code review; Review findings
      assertion: Source preflight precedes analysis and has inspectable failure outcomes.
    - source: SS411
      section: How code review works; Filtering findings
      assertion: Change-trigger and main-branch filtering behavior are distinct configuration paths.
---

<!-- block: b-6a65a5373a3a5b679f17 -->
## process

<!-- block: b-5e58c36998aa5cceada0 -->
<!-- field: field-0001 -->
Analyze selected source in the configured vulnerability and requirement modes.
<!-- /field -->

<!-- block: b-0884c4f72fc75a419d57 -->
## review / inputs

<!-- block: b-f2a3a9af5c195cfe813c -->
<!-- field: field-0002 -->
Exact source revision, full/differential scope, selected review modes, enabled requirements and source-access role.
<!-- /field -->

<!-- block: b-620e446139dd5c96bab2 -->
## review / narrative / 0

<!-- block: b-b4a40bf058c75fc092ae -->
<!-- field: field-0003 -->
Full-source and change-focused reviews use related analysis but different evidence boundaries. Preflight must first obtain the source and prepare the environment. A failure at that stage is not a clean scan.
<!-- /field -->

<!-- block: b-6426ba0d83fe5dbfb7df -->
## review / narrative / 1

<!-- block: b-1a70401338145615910f -->
<!-- field: field-0004 -->
Repository-event settings and optional comments are distinct from a manually started full review. The documented filtering file is read from the repository main branch, so changing it only in an unmerged branch may not change the current review behavior.
<!-- /field -->

<!-- block: b-3f2a7c7bb138576d9821 -->
## review / controls

<!-- block: b-f063def853c858f5a909 -->
<!-- field: field-0005 -->
Read analysis, posted comments and proposed repairs are different effects. Excluded source is unassessed, not verified safe.
<!-- /field -->

<!-- block: b-53de84ffc12557e2b4e6 -->
## review / undocumented

<!-- block: b-ddc9914966525f1089fc -->
<!-- field: field-0006 -->
No complete vulnerability-discovery algorithm or exhaustive language/framework coverage is inferred from a successful run.
<!-- /field -->
