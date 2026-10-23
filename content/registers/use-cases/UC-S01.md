---
id: record-use-cases-UC-S01
kind: record
collection: use-cases
product: security
title: Assess a running application for vulnerabilities
order: 14
frozen: true
data:
  id: UC-S01
  platform: security
  group: Application assessment
  title: Assess a running application for vulnerabilities
  summary: Assess the explicitly authorized surface and record findings and coverage gaps.
  delivery: Configured application assessment
  cadence: Manual, recurring or supported pipeline path
  availability: On-demand and optional invocation paths have different feature eligibility
  inputs:
    $markdown: field-0001
  output: Assessment run with findings, evidence and coverage record.
  sections:
  - S-01
  - S-03
  - S-04
  - S-M01
  - S-09
  - S-M07
  - S-M02
  constraints:
    $markdown: field-0002
  example:
    $markdown: field-0003
  keywords:
  - penetration test
  - dynamic assessment
  - staging
  narrative:
  - $markdown: field-0004
  - $markdown: field-0005
  narrative_status: Authored engineering workflow using documented mechanisms; not an executed service result.
  actor: Application security engineer
  objective: Assess the explicitly authorized surface and record findings and coverage gaps.
  completion:
  - Target revision and owner authorization are retained.
  - Reached roles and paths are known.
  - Failures and exclusions remain coverage limitations.
  profiles:
  - PR-S-ASSESS
  - PR-S-PIPELINE
  variants:
  - name: Public or private network
    changes: Choose the actual target route.
    controls: Private reachability does not extend authorized scope.
  - name: Unauthenticated or selected roles
    changes: Choose the application identities to assess.
    controls: Login failure leaves protected paths unassessed.
  - name: Manual, recurring or pipeline invocation
    changes: Choose a supported trigger.
    controls: Each run records its own target revision, identities, limits and coverage.
  schema_version: 2
  platforms:
  - security
  legacy_ids:
  - S-UC01
  - S-UC02
  - S-UC03
  - S-UC04
  aliases:
  - On-demand application penetration test
  - Authenticated workflow assessment
  - Private application assessment
  - Recurring penetration test
  steps_basis:
    $markdown: field-0006
  workflow:
  - title: Assemble application context
    purpose:
      $markdown: field-0007
    mechanism: MX-S-CONTEXT
    dependency: optional
    condition: Source code or documentation is selected to enrich application context.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-SOURCES
    effect: Source read
    verification: Compare source revision and system boundary with the intended subject.
    on_failure: Exclude mismatched context and document the resulting assessment limitation.
  - title: Configure target access
    purpose:
      $markdown: field-0008
    mechanism: MX-S-ACCESS
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-TARGET
    effect: Target connection
    verification: Confirm the permitted surface and exclusions in an authorized environment.
    on_failure: Stop when scope or owner authorization is unresolved.
  - title: Authenticate the intended role
    purpose:
      $markdown: field-0009
    mechanism: MX-S-AUTH
    dependency: conditional
    condition: The profile includes authenticated paths.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-AUTH
    effect: Authentication requests
    verification: Check the actual application identity and protected route, not only credential retrieval.
    on_failure: Mark protected paths unassessed when login fails.
  - title: Reuse a successful login procedure
    purpose:
      $markdown: field-0010
    mechanism: MX-S-LOGIN
    dependency: optional
    condition: A usable retained procedure and its reuse setting are available.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-LOGIN
    effect: Authentication requests
    verification: Distinguish successful login from observable procedure reuse.
    on_failure: Retest a changed login flow; failed login is not a clean assessment.
  - title: Execute and inspect the run
    purpose:
      $markdown: field-0011
    mechanism: MX-S-RUN
    dependency: required
    condition: Applies to the selected implementation.
    actor: Service execution; accountable engineer reviews the result
    configuration_features:
    - FT-S-RUNS
    - FT-S-FINDINGS
    effect: Active application assessment
    verification: Record actual revision, roles, exclusions, limit and incomplete areas.
    on_failure: Treat incomplete or failed execution as a coverage gap, not a pass.
---

<!-- block: b-3390b5ae07c753679e9f -->
## inputs

<!-- block: b-a07ad84555f95ece953b -->
<!-- field: field-0001 -->
Authorized target, actual deployed revision, network scope, test identities where needed, sources and work limits.
<!-- /field -->

<!-- block: b-db56b418543559d8ab5e -->
## constraints

<!-- block: b-9242919c51cf538a9a93 -->
<!-- field: field-0002 -->
Testing can change application state. Network and identity variants preserve the same assessment objective but require their own authorization and coverage evidence.
<!-- /field -->

<!-- block: b-d30f224ada3651e595ba -->
## example

<!-- block: b-ff016a22c55a5a5e8f7b -->
<!-- field: field-0003 -->
Run the authorized staging penetration test with the stated target, exclusions and test identities.
<!-- /field -->

<!-- block: b-cf18e72c71bd56ca96d3 -->
## narrative / 0

<!-- block: b-78d265f4ef1d56cc87d2 -->
<!-- field: field-0004 -->
An application owner authorizes assessment of a deployed release. Establish the target surface, permitted effects, source context and execution limit before starting. Public versus private access and authenticated versus unauthenticated testing are independent configuration choices: they determine which paths can be examined, not four independent operational objectives.
<!-- /field -->

<!-- block: b-bc61a2466fbd5e6b9bc4 -->
## narrative / 1

<!-- block: b-3d726147501156d28e68 -->
<!-- field: field-0005 -->
Review the saved configuration and follow the resulting run. Record actual revision, roles reached, exclusions, findings and incomplete areas. A recurring schedule or pipeline may initiate later runs, but cannot preserve credentials or target state that have since changed. Interpret an absence of findings only within the paths actually assessed.
<!-- /field -->

<!-- block: b-74384a3f2145572ba3cb -->
## steps basis

<!-- block: b-5c02f0a427865a87b3ed -->
<!-- field: field-0006 -->
The workflow order, acceptance criteria and failure decisions are authored engineering guidance. Each mechanism links to documented service behavior and concrete configuration features.
<!-- /field -->

<!-- block: b-59b8bf378dd75f308159 -->
## workflow / 0 / purpose

<!-- block: b-6031eeda2b675c42b895 -->
<!-- field: field-0007 -->
Select source evidence matching the application and intended revision.
<!-- /field -->

<!-- block: b-296e5eb70e0f585a8b62 -->
## workflow / 1 / purpose

<!-- block: b-66c145b791fd592cb1d7 -->
<!-- field: field-0008 -->
Define public or private reachability without widening authority.
<!-- /field -->

<!-- block: b-8bc89c3b5b6556b885f3 -->
## workflow / 2 / purpose

<!-- block: b-4ace2636174a5882b17b -->
<!-- field: field-0009 -->
Reach the protected paths required by the profile.
<!-- /field -->

<!-- block: b-a597df9c571057d1acc6 -->
## workflow / 3 / purpose

<!-- block: b-c7b1a2cf73545852b8ff -->
<!-- field: field-0010 -->
Use documented navigation reuse without assuming it proves coverage.
<!-- /field -->

<!-- block: b-c6bcbed4cdf65e208e62 -->
## workflow / 4 / purpose

<!-- block: b-d5d19a3f264f5d17ad0a -->
<!-- field: field-0011 -->
Retain actual findings, target state and unassessed areas.
<!-- /field -->
