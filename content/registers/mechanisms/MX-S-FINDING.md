---
id: record-mechanisms-MX-S-FINDING
kind: record
collection: mechanisms
product: security
title: Finding evidence inspection
order: 19
frozen: true
data:
  id: MX-S-FINDING
  platform: security
  title: Finding evidence inspection
  features:
  - FT-S-FINDINGS
  sections:
  - S-05
  trigger: Assessment returns a finding
  state: Finding identity and evidence
  process:
    $markdown: field-0001
  effect: Finding review record
  verification: Give the finding a disposition using evidence, impact and application-owner context.
  on_failure: Preserve uncertainty and obtain missing evidence before closure.
  review:
    primary_section: S-05
    kind: Evidence-inspection and disposition workflow
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Inspect
      - Completed/in-progress run → Findings → select finding and trace its actions/logs.
      - Evidence and affected context
    - - Visibility
      - Review the unverified-findings filter before counting results.
      - Display scope
    - - Disposition
      - Review current and original values where edits exist.
      - Human decision versus generated attributes
    lifecycle:
    - - Finding observed
      - Inspect evidence
      - Confidence and supported impact can be assessed.
    - - Finding edited
      - Save current values
      - Latest attributes change; original view remains available.
    - - Repair proposed
      - Review/deploy/verify separately
      - An edited status does not establish deployed remediation.
    controls:
      $markdown: field-0005
    observable_output: Finding identity, supporting evidence, original/latest values and a reviewer disposition.
    undocumented:
      $markdown: field-0006
    test:
    - Use the synthetic authorization-finding fixture for a tabletop.
    - Trace the claim to the supplied identity, request and affected revision.
    - $markdown: field-0007
    claims:
    - source: SS405
      section: Default confidence filter; Review finding details; View original agent version
      assertion: Evidence, display filtering and original/latest attributes are distinct review surfaces.
  related_mechanisms:
  - id: MX-S-PERSONALIZE
    dependency: conditional
    condition:
      $markdown: field-0008
---

<!-- block: b-d19a0028bb3953d8a98e -->
## process

<!-- block: b-83f6f41df51851318b3d -->
<!-- field: field-0001 -->
Expose the affected context and supporting reproduction or source evidence for review.
<!-- /field -->

<!-- block: b-dfcc4508092b5372ad2c -->
## review / inputs

<!-- block: b-4e7af2910f37576e82de -->
<!-- field: field-0002 -->
Finding identifier, current/original attributes, validation evidence, assessment revision and application-owner context.
<!-- /field -->

<!-- block: b-750920ec69d4548fadc4 -->
## review / narrative / 0

<!-- block: b-c5b6e45146ba516993ff -->
<!-- field: field-0003 -->
A finding combines an observation with an interpretation of risk. Inspect the supporting request, response or source evidence before accepting that interpretation. The findings view can hide unverified items, so the visible count depends on the active filter.
<!-- /field -->

<!-- block: b-be112161d54452cd81d4 -->
## review / narrative / 1

<!-- block: b-362ea240b6cc57fcb3f5 -->
<!-- field: field-0004 -->
Editing a finding changes its recorded attributes; it does not repair the application. The separately documented Findings Personalization mechanism can also influence later similar findings. Read the original and latest values when determining whether a change reflects new vulnerability evidence or a revised organizational preference.
<!-- /field -->

<!-- block: b-3552f6bffcf052699737 -->
## review / controls

<!-- block: b-aa15ddbbab255189bfe2 -->
<!-- field: field-0005 -->
Generated reproduction scripts require review and an authorized target before execution. Finding counts and severity alone do not establish risk or coverage.
<!-- /field -->

<!-- block: b-8eff115d44fc591989c7 -->
## review / undocumented

<!-- block: b-01953dd6c34353259a88 -->
<!-- field: field-0006 -->
No calibrated probability interpretation of confidence or exhaustive false-negative rate is established.
<!-- /field -->

<!-- block: b-7b6ef0d8b92f51019482 -->
## review / test / 2

<!-- block: b-4506c1fc335d5b73a2ac -->
<!-- field: field-0007 -->
Hide/unhide unverified findings and verify that changed visibility is not reported as remediation.
<!-- /field -->

<!-- block: b-3c28794b221654fa8acb -->
## related mechanisms / 0 / condition

<!-- block: b-cbfa4a5107c25a65985c -->
<!-- field: field-0008 -->
Findings Personalization was enabled at test start and eligible edits are available; it changes finding attributes, not application state.
<!-- /field -->
