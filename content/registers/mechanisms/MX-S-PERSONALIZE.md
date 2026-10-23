---
id: record-mechanisms-MX-S-PERSONALIZE
kind: record
collection: mechanisms
product: security
title: Finding-edit personalization
order: 40
frozen: true
data:
  id: MX-S-PERSONALIZE
  platform: security
  title: Finding-edit personalization
  features:
  - FT-S-FINDINGS
  sections:
  - S-05
  trigger:
    $markdown: field-0001
  state: Retained finding preferences and original/latest finding attributes
  process:
    $markdown: field-0002
  effect: Finding-attribute personalization, not application remediation
  verification:
    $markdown: field-0003
  on_failure:
    $markdown: field-0004
  review:
    primary_section: S-05
    kind: Learned finding-preference mechanism
    inputs:
      $markdown: field-0005
    narrative:
    - $markdown: field-0006
    - $markdown: field-0007
    configuration:
    - - Enablement
      - $markdown: field-0008
      - Must be enabled at test start for learning
    - - Eligible input
      - Review edits in the most recent completed run.
      - Not arbitrary edits from all historical runs
    - - Inspection
      - Compare original/latest attributes and Personalization changes where shown.
      - Observed preference application
    lifecycle:
    - - Eligible edited finding
      - Next applicable run
      - Similar findings can receive personalized attributes.
    - - Later edit
      - Subsequent learning
      - Most recent edit replaces the earlier preference.
    - - Feature disabled
      - Run without personalization
      - Raw agent-produced findings are shown; preferences remain retained.
    controls:
      $markdown: field-0009
    observable_output: Original/latest attributes and a Personalization changes explanation on affected findings.
    undocumented:
      $markdown: field-0010
    test:
    - $markdown: field-0011
    - Inspect whether a later similar finding exposes the personalization change.
    - $markdown: field-0012
    claims:
    - source: SS405
      section: How personalization learns from your edits; Enable or disable Findings Personalization
      assertion:
        $markdown: field-0013
---

<!-- block: b-b8a2c04e5de355df9f6c -->
## trigger

<!-- block: b-fe6a02753beb5bc7bd24 -->
<!-- field: field-0001 -->
Eligible edits from the most recent completed test when personalization was enabled at test start
<!-- /field -->

<!-- block: b-ffa7e3b91c185c84b391 -->
## process

<!-- block: b-c690824adeeb58f6bcd3 -->
<!-- field: field-0002 -->
Apply eligible learned preferences to similar findings in subsequent penetration-test runs.
<!-- /field -->

<!-- block: b-4a9b9f44e17851bb9518 -->
## verification

<!-- block: b-d604369b7408572da1c9 -->
<!-- field: field-0003 -->
Inspect original/latest values and the Personalization changes explanation separately from vulnerability evidence.
<!-- /field -->

<!-- block: b-a1b0d590819257429a0e -->
## on failure

<!-- block: b-578c77f3237352dc8fe4 -->
<!-- field: field-0004 -->
Treat unobserved personalization as unverified; a severity change does not establish a repaired application.
<!-- /field -->

<!-- block: b-5eaef4194e1b51aca511 -->
## review / inputs

<!-- block: b-b4eb151618145b7ba4c9 -->
<!-- field: field-0005 -->
Eligible operator edits in the most recent completed penetration-test run and Findings Personalization enabled when the test starts.
<!-- /field -->

<!-- block: b-852910ee33065eed839d -->
## review / narrative / 0

<!-- block: b-123a820a429e538aae26 -->
<!-- field: field-0006 -->
Findings Personalization learns eligible edits and applies preferences to similar findings on later runs. It is distinct from discovering vulnerabilities, retaining a login procedure and replaying a finding. Learned changes can alter finding attributes without proving that application behavior changed.
<!-- /field -->

<!-- block: b-5d7b44cb550655bf8b69 -->
## review / narrative / 1

<!-- block: b-d0b0c2f9b7ed5771987a -->
<!-- field: field-0007 -->
Inspect the Personalization changes explanation and original values before interpreting a severity change. For status, the documented learnable signal is marking a finding FALSE_POSITIVE; other status updates are not equivalent learning inputs.
<!-- /field -->

<!-- block: b-f0537b0c9fd2531fabed -->
## review / configuration / 0 / 1

<!-- block: b-1091adc93d9d5031bda7 -->
<!-- field: field-0008 -->
Inspect Findings Personalization in the penetration-test configuration; documented default is enabled.
<!-- /field -->

<!-- block: b-b051fddf4ea2530f9e23 -->
## review / controls

<!-- block: b-70833f272e6f5a48992f -->
<!-- field: field-0009 -->
Personalized severity is not evidence of a repaired vulnerability. Disabling the feature is not deleting learned preferences.
<!-- /field -->

<!-- block: b-aa87cc647642562dbe9d -->
## review / undocumented

<!-- block: b-5c58623d04285adbb706 -->
<!-- field: field-0010 -->
Similarity thresholds, internal preference storage and a public preference CRUD resource are not established by the guide.
<!-- /field -->

<!-- block: b-cea29abe50095f67bf72 -->
## review / test / 0

<!-- block: b-2034159cd5fb5950b959 -->
<!-- field: field-0011 -->
Use a controlled staging finding whose risk context can be changed without modifying the application.
<!-- /field -->

<!-- block: b-f74327979acf558281ce -->
## review / test / 2

<!-- block: b-1ba35607086c5e3e9c4a -->
<!-- field: field-0012 -->
Disable personalization; compare raw output without claiming that retained preferences were deleted.
<!-- /field -->

<!-- block: b-dbebe4c6a4b4581e824c -->
## review / claims / 0 / assertion

<!-- block: b-9ab665ef59595a9fa874 -->
<!-- field: field-0013 -->
Learning uses eligible edits from the most recent completed run; false-positive status is special, and disabling preserves preferences.
<!-- /field -->
