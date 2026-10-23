---
id: record-mechanisms-MX-S-LOGIN
kind: record
collection: mechanisms
product: security
title: Successful login-procedure reuse
order: 17
frozen: true
data:
  id: MX-S-LOGIN
  platform: security
  title: Successful login-procedure reuse
  features:
  - FT-S-LOGIN
  sections:
  - S-M02
  trigger: Later eligible authentication session
  state: Retained login procedure and reuse setting
  process:
    $markdown: field-0001
  effect: Authentication requests
  verification: Distinguish successful login from observable procedure reuse.
  on_failure: Retest a changed login flow; failed login is not a clean assessment.
  review:
    primary_section: S-M02
    kind: Learned authentication-procedure mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Prerequisite
      - Configure a credential and complete a successful login.
      - Procedure-production input
    - - Reuse
      - $markdown: field-0005
      - Reuse control
    - - Verification
      - On later sessions, verify authenticated identity independently from any observable reuse.
      - Coverage prerequisite
    lifecycle:
    - - No successful login procedure
      - Successful navigation
      - A reusable skill file is produced.
    - - Procedure retained; reuse enabled
      - Later login
      - Saved navigation can be applied.
    - - Reuse disabled
      - Later login
      - Reuse stops; retained learning is preserved.
    - - Reuse re-enabled
      - Later login
      - Retained procedure becomes applicable again.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented:
      $markdown: field-0008
    test:
    - Use an authorized multistep staging login.
    - Compare first and later logins while verifying the same application role.
    - Change the login form; failure to reach the protected route remains a coverage gap.
    claims:
    - source: SS403
      section: Login Optimization
      assertion:
        $markdown: field-0009
    diagram: mechanism-security-learning
---

<!-- block: b-a5a8a406fd7c59ac8beb -->
## process

<!-- block: b-6e46ade4baf25237a019 -->
<!-- field: field-0001 -->
Reuse learned navigation where the setting and current login flow permit it.
<!-- /field -->

<!-- block: b-9672cf9d30b15ca29961 -->
## review / inputs

<!-- block: b-acaf1b7ca0c158acabb2 -->
<!-- field: field-0002 -->
Configured test credentials, a successfully discovered login flow and the Login Optimization setting.
<!-- /field -->

<!-- block: b-191cfbc1797e53c6999b -->
## review / narrative / 0

<!-- block: b-05cee34021305dec9161 -->
<!-- field: field-0003 -->
Successful navigation produces a reusable login procedure. Later login sessions can read that procedure instead of rediscovering the path. Reuse concerns navigation; it does not establish that an old credential remains valid or that the application still assigns the intended role.
<!-- /field -->

<!-- block: b-2c9d3d47993b5655a106 -->
## review / narrative / 1

<!-- block: b-4bb2bd67731c50118f25 -->
<!-- field: field-0004 -->
This is separate from finding personalization and vulnerability revalidation. A changed login flow calls for a fresh authentication check, while a changed vulnerability calls for assessment or revalidation. Switching off reuse is not a documented deletion of learned material.
<!-- /field -->

<!-- block: b-c6f937d437b656a5b163 -->
## review / configuration / 1 / 1

<!-- block: b-330e34b931f652d8bb20 -->
<!-- field: field-0005 -->
Inspect Login Optimization in the penetration-test configuration; the documentation identifies it as enabled by default.
<!-- /field -->

<!-- block: b-265ba35a383d55828490 -->
## review / controls

<!-- block: b-d3072d1edc09555b9cd0 -->
<!-- field: field-0006 -->
Test current credentials and role on each relevant run. Retained navigation is not a general-purpose incident memory.
<!-- /field -->

<!-- block: b-3196fbc5c9b35c0b9b96 -->
## review / observable output

<!-- block: b-b5d20a9bb6b55600ae75 -->
<!-- field: field-0007 -->
Authenticated session and, where exposed, evidence of reuse. Do not infer reuse solely from faster execution.
<!-- /field -->

<!-- block: b-dae8b21c2cb353c48a3e -->
## review / undocumented

<!-- block: b-efce1d56e6315d50a1d0 -->
<!-- field: field-0008 -->
No independent public CRUD API or guaranteed invalidation policy for the saved login skill is established.
<!-- /field -->

<!-- block: b-2aea147764005090b7e4 -->
## review / claims / 0 / assertion

<!-- block: b-c1f4a0066a645d57b25a -->
<!-- field: field-0009 -->
Successful navigation produces a skill reused in later sessions/runs; disabling reuse preserves learning.
<!-- /field -->
