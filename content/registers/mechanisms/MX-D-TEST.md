---
id: record-mechanisms-MX-D-TEST
kind: record
collection: mechanisms
product: devops
title: Active deployed-application testing
order: 13
frozen: true
data:
  id: MX-D-TEST
  platform: devops
  title: Active deployed-application testing
  features:
  - FT-D-TEST
  sections:
  - D-09
  trigger: Authorized test execution
  state: Test profile and deployed target
  process:
    $markdown: field-0001
  effect: Application requests with possible writes
  verification: Inspect target revision, actual interactions, results and effects.
  on_failure: Stop unexpected effects and retain incomplete coverage.
  review:
    primary_section: D-09
    kind: Preview active-test workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Profile
      - 'Release Manager → Test profiles → Add test profile: name, target URL and UI/API type.'
      - Saved target definition
    - - Execution
      - Start testing and provide a bounded test intent.
      - Active run
    - - Environment
      - Use disposable staging data and suppress unintended downstream effects.
      - Team safety prerequisite
    lifecycle:
    - - Profile saved
      - Start testing
      - Plan generation and active requests begin.
    - - Requests executed
      - Review results
      - Failures, reproductions and observed behavior become available.
    - - Unexpected effect observed
      - Stop further authorized test activity and inspect target
      - No automatic undo of prior requests is asserted.
    controls: Infrastructure read permissions do not make application POST/PUT/DELETE requests harmless.
    observable_output: Test run, actual target, observed interactions and reproduction details.
    undocumented:
      $markdown: field-0005
    test:
    - Prepare a sandboxed checkout endpoint with synthetic records and disabled notifications.
    - Inspect expected request effects and one known validation error.
    - $markdown: field-0006
    claims:
    - source: DS413
      section: How release testing works; Defining test profiles; Reviewing results
      assertion: Testing sends real requests including writes and reports observed results.
    - source: DS415
      section: Feature availability by Region
      assertion: Release testing is a feature-specific preview path.
---

<!-- block: b-cf58ec6898fb5304afa1 -->
## process

<!-- block: b-3051bb092b1351cfa5be -->
<!-- field: field-0001 -->
Send selected test interactions and retain observed behavior.
<!-- /field -->

<!-- block: b-dabe5a875e6e51499c89 -->
## review / inputs

<!-- block: b-6c3f1fee3fde585b8524 -->
<!-- field: field-0002 -->
Test profile, deployed URL, UI/API type, test intent and authorized disposable application data.
<!-- /field -->

<!-- block: b-9d2a269622e157a9b672 -->
## review / narrative / 0

<!-- block: b-218edc1096b859399007 -->
<!-- field: field-0003 -->
Release testing generates a plan from change context or a stated intent and exercises a running application. Its requests can modify data. The relevant identity is therefore the deployed target and its test account, not just the repository branch.
<!-- /field -->

<!-- block: b-a1378122b08d5edfb7f1 -->
## review / narrative / 1

<!-- block: b-469c70f314ad5c87ab55 -->
<!-- field: field-0004 -->
Inspect the actual interactions and results. A generated plan is not executed coverage. This guide uses the documented profile and web-app path rather than copying inconsistent action names from different parts of the retrieved pipeline example.
<!-- /field -->

<!-- block: b-d058ccf2fa185251b044 -->
## review / undocumented

<!-- block: b-ba5e507f6a2859a484b4 -->
<!-- field: field-0005 -->
The documentation does not promise exhaustive coverage or transactional rollback of application writes.
<!-- /field -->

<!-- block: b-431ed32800935506b0f2 -->
## review / test / 2

<!-- block: b-b52f2b485c27504288db -->
<!-- field: field-0006 -->
An unexpected payment/notification path ends the exercise; do not treat later cancellation as rollback.
<!-- /field -->
