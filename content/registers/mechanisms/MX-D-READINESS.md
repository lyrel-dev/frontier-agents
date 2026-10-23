---
id: record-mechanisms-MX-D-READINESS
kind: record
collection: mechanisms
product: devops
title: Candidate release analysis
order: 12
frozen: true
data:
  id: MX-D-READINESS
  platform: devops
  title: Candidate release analysis
  features:
  - FT-D-READINESS
  - FT-D-SOURCES
  sections:
  - D-09
  trigger: Eligible readiness-review request
  state: Candidate revision and dependency context
  process:
    $markdown: field-0001
  effect: Readiness result
  verification: Match findings to the exact candidate and unresolved dependencies.
  on_failure: Treat unsupported repository or feature access as an unmet prerequisite.
  review:
    primary_section: D-09
    kind: Preview analysis and verification workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Eligibility
      - Check current release-management Region and repository support.
      - Feature-specific preview boundary
    - - Repository settings
      - Configure change-review triggering and automatic verification independently.
      - Two separate options
    - - Private verification
      - $markdown: field-0005
      - Build dependencies, not unrestricted network access
    lifecycle:
    - - Candidate selected
      - Start review
      - Analysis record is associated with the candidate.
    - - Verification enabled
      - Build and execute tests
      - Test evidence is added when execution succeeds.
    - - Access or context missing
      - Review reports gaps
      - Resolve the prerequisite and rerun; do not interpret as clean review.
    controls:
      $markdown: field-0006
    observable_output: Readiness report, candidate identity, findings and any Tests-tab results.
    undocumented:
      $markdown: field-0007
    test:
    - Use a non-production candidate with one known behavior change.
    - Compare findings and executed tests with that revision.
    - $markdown: field-0008
    claims:
    - source: DS412
      section: Getting started; Performing a code review; Automatic verification testing
      assertion:
        $markdown: field-0009
    - source: DS415
      section: Feature availability by Region
      assertion: Release-management eligibility differs from production operations.
---

<!-- block: b-ec7d80c2f07950da839e -->
## process

<!-- block: b-0910aa9dc96a52bda6ca -->
<!-- field: field-0001 -->
Review the proposed change for the operational risks supported by this preview path.
<!-- /field -->

<!-- block: b-92f3d59677f558669a86 -->
## review / inputs

<!-- block: b-6480f1ad302e578d94ab -->
<!-- field: field-0002 -->
Candidate branch/commit and connected repository context; optional managed verification environment.
<!-- /field -->

<!-- block: b-24b944e7059455a99639 -->
## review / narrative / 0

<!-- block: b-083e4587cf0e597a8fb2 -->
<!-- field: field-0003 -->
Readiness analysis examines a proposed code change. Optional verification builds and exercises the code in a managed environment; it is not a test of whichever production revision happens to be running. A report must therefore identify the candidate and whether verification actually ran.
<!-- /field -->

<!-- block: b-c3458fc8edee597588f7 -->
## review / narrative / 1

<!-- block: b-7bb5450c033751d499ae -->
<!-- field: field-0004 -->
Insufficient data or permissions are unresolved outcomes, not favorable release decisions. Automated triggers and verification are independently configured, so the presence of a review does not prove that a build/test environment was used.
<!-- /field -->

<!-- block: b-ee82d270b7d2591ab82d -->
## review / configuration / 2 / 1

<!-- block: b-657ff817ea845117ab1e -->
<!-- field: field-0005 -->
Select a verification environment with the required private route and runtime role when needed.
<!-- /field -->

<!-- block: b-251f5fc52c25542088dc -->
## review / controls

<!-- block: b-4e35124257e6543191ba -->
<!-- field: field-0006 -->
Code verification and active deployed-application testing have different subjects and effects.
<!-- /field -->

<!-- block: b-187f760dd68a5caf922e -->
## review / undocumented

<!-- block: b-c183ff4f514e5eaaa269 -->
<!-- field: field-0007 -->
Exact risk-scoring thresholds and guaranteed test coverage are not published; feature availability must be checked.
<!-- /field -->

<!-- block: b-25a9209c16545e838aeb -->
## review / test / 2

<!-- block: b-06044fa1de7e50588ff5 -->
<!-- field: field-0008 -->
Omit a required build dependency and require an incomplete or failed verification, not a pass.
<!-- /field -->

<!-- block: b-d411f4f1dd5a5ab8b6bc -->
## review / claims / 0 / assertion

<!-- block: b-e957784382905598a87c -->
<!-- field: field-0009 -->
Review and verification settings are independent; candidate and verification results are inspectable.
<!-- /field -->
