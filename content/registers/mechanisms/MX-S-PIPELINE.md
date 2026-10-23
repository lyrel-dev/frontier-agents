---
id: record-mechanisms-MX-S-PIPELINE
kind: record
collection: mechanisms
product: security
title: Pipeline invocation and result observation
order: 27
frozen: true
data:
  id: MX-S-PIPELINE
  platform: security
  title: Pipeline invocation and result observation
  features:
  - FT-S-PIPELINE
  sections:
  - S-06
  - S-09
  trigger: Authorized delivery step
  state: Pipeline execution and server-side job
  process:
    $markdown: field-0001
  effect: Assessment initiation
  verification: Retain revision and run identity and apply an explicit team gate to incomplete results.
  on_failure: Block or escalate under the declared gate; missing evidence is not success.
  review:
    primary_section: S-06
    kind: Post-deployment invocation mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Prerequisite
      - $markdown: field-0005
      - Existing assessment definition
    - - Identity
      - Configure the provider-specific OIDC path and supported integration step.
      - Short-lived pipeline authentication
    - - Decision
      - Set accepted threshold and explicit behavior for missing/incomplete results.
      - Team promotion policy
    lifecycle:
    - - Deployment completed
      - Authorized integration step
      - Server-side assessment job starts.
    - - Job running
      - Pipeline waits/observes
      - Runner completion is not yet assessment completion.
    - - Job result available
      - Apply declared gate
      - Promote, block or escalate using that result and revision.
    controls: This preview path is post-deployment assessment, not pull-request static analysis.
    observable_output: Pipeline execution, deployed change, assessment job and applied promotion decision.
    undocumented:
      $markdown: field-0006
    test:
    - Use a non-production pipeline with known deployed revision and saved assessment.
    - Retain the server job ID with the gate result.
    - $markdown: field-0007
    claims:
    - source: SS414
      section: Before you start; Post-deployment gate
      assertion:
        $markdown: field-0008
---

<!-- block: b-a1d56c9e2ffa5e899072 -->
## process

<!-- block: b-a761460706545454b924 -->
<!-- field: field-0001 -->
Start and observe the supported assessment independently of the pipeline runner.
<!-- /field -->

<!-- block: b-2d8ca4c1ba9550cabd81 -->
## review / inputs

<!-- block: b-ab76a3065797552689b8 -->
<!-- field: field-0002 -->
Existing penetration-test configuration with CI/CD mode, source connection, pipeline OIDC identity and deployed change identifiers.
<!-- /field -->

<!-- block: b-8af33703578252599807 -->
## review / narrative / 0

<!-- block: b-58d8767d59805ed79910 -->
<!-- field: field-0003 -->
The pipeline step starts and observes a server-side test of a deployed change. It does not create the application or replace the saved assessment scope, and it does not run the penetration-testing engine inside the delivery runner.
<!-- /field -->

<!-- block: b-4ffa94aff0405455a2ae -->
## review / narrative / 1

<!-- block: b-c77aa478dd2157538acf -->
<!-- field: field-0004 -->
Configure the release decision before enabling the integration. Invocation failure, unfinished assessment and a completed result above the selected severity threshold need distinct handling. This decision policy is authored team behavior, not a claim that every pipeline fails closed automatically.
<!-- /field -->

<!-- block: b-d28d4ef6b215543ab34a -->
## review / configuration / 0 / 1

<!-- block: b-6902d49014b25b0fb173 -->
<!-- field: field-0005 -->
Verify target and create a test with current credentials/network scope; enable CI/CD mode and record space/test IDs.
<!-- /field -->

<!-- block: b-a0800da990dd5773958e -->
## review / undocumented

<!-- block: b-a3b0102a9a0c52769077 -->
<!-- field: field-0006 -->
Exactly-once invocation, universal timeout behavior and identical provider semantics are not established.
<!-- /field -->

<!-- block: b-3517f5c683ec5c1c9906 -->
## review / test / 2

<!-- block: b-eb0a74fc844456d3a702 -->
<!-- field: field-0007 -->
Simulate unavailable/incomplete result; follow the declared blocking/escalation rule rather than passing silently.
<!-- /field -->

<!-- block: b-fe448095406c5fd19db4 -->
## review / claims / 0 / assertion

<!-- block: b-e0068f387f545ca197cf -->
<!-- field: field-0008 -->
The integration invokes an existing configured test, uses OIDC and observes server-side work.
<!-- /field -->
