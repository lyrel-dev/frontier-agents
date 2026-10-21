# AWS Security Agent / AWS Continuum — mechanisms and enablement

Reviewed 21 October 2026. Independent checks and examples are proposed; no live workflow was executed.

## Mechanism model

Additional Learning Resources are application inputs, not evidence of a cross-incident training mechanism. A penetration test can use source code and design information, validate findings, propose repairs and rerun selected checks. Each stage has a different authorization and acceptance boundary.

Updated application context → scoped assessment → evidence and findings → reviewed/deployed repair → targeted revalidation. No configurable cross-run incident-memory switch was identified in the reviewed guidance. This is an evidence limitation, not a claim about undisclosed internals.

Penetration testing is generally available. Code review, design review and threat modeling are documented as preview; check feature and Region access before setup.

## S-M01 — Supply application context for a scoped test

**Surface:** Penetration-test creation / web application

**Availability:** Penetration testing GA

**Activation:** Select connected resources per test

### Documented mechanism

Additional Learning Resources supply source and application documents to the assessment. This is task context; the reviewed guidance does not identify it as a persistent incident-memory control.

### Enable and configure

An enabled Agent Space, authorized and verified target, and permission to provide the selected application materials.

1. Create a penetration test and define the target and exclusions.

2. At Additional Learning Resources, select connected resources or upload the relevant material.

3. Confirm the selected revision and network access needed by connected sources before starting.

### Scope and persistence

Test-selected context may contain source, API or design information. Connected sources can expose updated versions on subsequent use.

### Independent checks — proposed

- Use a staging target and a non-sensitive application note with a traceable revision.

- Inspect test context and coverage against that revision; verify the deployed application matches it.

### Record to retain — proposed

Target authorization, resource selection, revision identifiers, exclusions and test ID.

### Stop, correct or remove

Change selected resources for the next test. Use integration and repository access controls to restrict the available material.

### Limits and fallback

Adding context does not authorize out-of-scope testing or establish cross-run model training.

Exclude an unavailable source and record the coverage limitation; do not widen target access to resolve a document problem.

### Illustrative task — not executed

Illustrative context: a sanitized API description identifying a staging endpoint and the test roles permitted to use it.

### Official guidance

[SC: Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[SG: Security considerations and finding validation](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

## S-M02 — Authenticate a test without expanding its scope

**Surface:** Penetration-test authentication configuration

**Availability:** Penetration testing GA

**Activation:** Explicit test credentials or advanced credential flow

### Documented mechanism

Authentication lets the assessment reach authorized application behavior. The guide distinguishes direct credentials from advanced flows using IAM, Secrets Manager and Lambda.

### Enable and configure

Owner authorization, test identities with bounded privileges, valid login behavior and approved secret handling.

1. Open the authentication configuration for the test.

2. Choose the documented credential method; configure the login target and instructions where required.

3. Verify the test account and its allowed roles before launching the assessment.

### Scope and persistence

The credential method grants application access only within the intended test scope; network connectivity and target exclusions remain separate.

### Independent checks — proposed

- Sign in with the test identity through an approved manual check.

- Confirm both an allowed operation and a forbidden operation; inspect test logs for authentication failures.

### Record to retain — proposed

Redacted authentication method, test role, allowed operations, login check and revocation record.

### Stop, correct or remove

Revoke or rotate the test identity after the exercise. Stop the test if observed activity exceeds authorization.

### Limits and fallback

Credentials do not belong in steering, persistent memory, exported evidence or this repository.

Pause the test and repair the authorized credential flow; label unauthenticated coverage as incomplete.

### Illustrative task — not executed

Illustrative: configure a staging-only reviewer account with no billing, administrative or production privileges.

### Official guidance

[SA: Provide authentication credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

[SC: Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[SG: Security considerations and finding validation](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

## S-M03 — Validate and review reported findings

**Surface:** Penetration-test results

**Availability:** Penetration testing GA

**Activation:** Service validation plus reviewer inspection

### Documented mechanism

The service uses deterministic checks where possible and independent replay in other cases. Results distinguish validated findings from lower-confidence or unverified candidates.

### Enable and configure

A completed or progressing authorized assessment and access to its results.

1. Open the penetration-test results and inspect the finding evidence.

2. Review confidence, reproduction material and coverage, not just severity.

3. Inspect unverified candidates separately where the interface permits; do not silently promote them to confirmed defects.

### Scope and persistence

A finding relates to the tested application state and selected scope.

### Independent checks — proposed

- Have an authorized reviewer reproduce a selected finding safely in staging.

- Compare the request, identity, application version and impact with the report.

### Record to retain — proposed

Finding ID, evidence, confidence, affected version, reproduction decision and unresolved coverage.

### Stop, correct or remove

Keep active-test monitoring and stop responsibility with the authorized operator.

### Limits and fallback

Validation does not prove complete security coverage. A missing finding is not proof that a defect is absent.

Classify the finding as unresolved when reproduction or evidence is insufficient; do not convert uncertainty into a pass.

### Illustrative task — not executed

Illustrative review: distinguish an observed access-control violation from a hypothesis inferred from source code.

### Official guidance

[SG: Security considerations and finding validation](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

[SV: Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

## S-M04 — Maintain security requirements as explicit policy context

**Surface:** Security requirements console

**Availability:** Design/code review are preview

**Activation:** Enable a managed or custom requirement pack

### Documented mechanism

Requirement packs define criteria used during design and code reviews. They are shared across Agent Spaces, not a private memory of one application.

### Enable and configure

Access to security-requirement administration and an approved applicability definition.

1. Open Security requirements and select a managed pack or create a custom pack.

2. For a custom requirement, define applicability, compliance criteria and remediation guidance.

3. Enable the pack and run a new review to evaluate the change.

### Scope and persistence

Pack changes affect new reviews, not existing review results. Managed requirements are read-only.

### Independent checks — proposed

- Use one applicable example and one deliberately not-applicable example.

- Check the reported requirement identifier and retain the pack revision used for the review.

### Record to retain — proposed

Pack and requirement IDs, applicability, revision, review ID and reviewer decision.

### Stop, correct or remove

Disable a pack to exclude it from new reviews; preserve the approved custom definition before editing.

### Limits and fallback

Uploading new source documents regenerates the pack and replaces existing requirements, including manual entries. Framework packs do not certify compliance.

Keep a manually reviewed policy checklist while resolving pack applicability; do not reuse an old review as evidence of a new pack.

### Illustrative task — not executed

Illustrative policy: authenticated service endpoints must enforce ownership checks; explicitly exclude public health endpoints.

### Official guidance

[SP: Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

[SL: Resource hierarchy and lifecycle](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html)

[SB: Pricing and preview capability status](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## S-M05 — Enable proposed code repair per repository

**Surface:** Agent Space repository configuration / finding detail

**Availability:** Capability availability follows the originating review or test

**Activation:** Administrator enablement, then a finding repair request

### Documented mechanism

Repository remediation produces a proposed change for review. For the private GitHub path used here, the artifact is a pull request; other source providers can return different artifacts.

### Enable and configure

Enabled testing or code review, an authorized GitHub App registration and the relevant private repository.

1. Open the Agent Space Penetration test tab and choose the GitHub registration, or edit its Code review repository entry.

2. In the repository-capability wizard, enable Automatic remediation for the selected repository and choose Connect.

3. From a supported finding, request remediation and inspect the resulting change.

### Scope and persistence

The setting is repository-specific. It does not authorize merging or deployment.

### Independent checks — proposed

- Match the finding to changed lines and inspect the PR scope.

- Run regression and security checks independently before any approved merge.

### Record to retain — proposed

Finding-to-PR link, repository setting, commit IDs, test evidence and human review decision.

### Stop, correct or remove

Review or disable the repository remediation setting when no longer needed; keep branch protection independent.

### Limits and fallback

A proposed repair may be incomplete or introduce regressions. An open PR is not evidence that the running application is fixed.

Implement a reviewed manual repair when the repository or finding is unsupported; retain the original evidence.

### Illustrative task — not executed

Illustrative: request a repair for a confirmed staging access-control finding, without allowing auto-merge.

### Official guidance

[SE: Enable finding remediation](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html)

[SR: Remediate a penetration-test finding](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html)

## S-M06 — Revalidate a deployed repair

**Surface:** Completed test → findings panel

**Availability:** Documented penetration-test revalidation

**Activation:** Explicit selection of findings

### Documented mechanism

Revalidation repeats checks for selected findings against the running target. It creates a separate job and does not replace the original finding record.

### Enable and configure

A completed test, selected findings, a deployed candidate fix, reachable target and valid test authentication.

1. Deploy the reviewed repair to the originally authorized environment.

2. Select findings in the completed test and choose revalidation.

3. Review the new job status and evidence against the deployed version.

### Scope and persistence

This is targeted checking of known findings, not a new assessment for unrelated vulnerabilities.

### Independent checks — proposed

- Record the deployed commit and verify target/authentication health before interpreting the result.

- Distinguish a negative reproduction from an unreachable target or failed test.

### Record to retain — proposed

Original finding, deployed commit, revalidation job, result evidence and residual risk.

### Stop, correct or remove

Keep the original test record and the subsequent verification record; authorization remains scoped to the target.

### Limits and fallback

Resolved means the issue was not reproduced by that check. It is not an exhaustive assurance statement.

Mark verification inconclusive if the target or credentials fail; repair the test conditions before rerunning.

### Illustrative task — not executed

Illustrative: revalidate one repaired staging finding after deployment, with no expansion of the original scope.

### Official guidance

[ST: Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

## S-M07 — Connect an IDE scan through the Security Agent MCP server

**Surface:** Kiro Power / supported IDE integration

**Availability:** Code review and threat-model review are preview

**Activation:** Install the supported integration; authorize first-use provisioning

### Documented mechanism

The MCP integration packages code, uploads it to an account S3 bucket, starts a scan and retrieves findings. First use can provision an Agent Space, IAM role and bucket.

### Enable and configure

Configured AWS credentials with the documented setup and scan permissions; supported client and package runtime.

1. Install the AWS Security Agent Power in Kiro, following the official IDE integration procedure.

2. Review the AWS profile, Region and setup permissions before first use.

3. Request a scan of a disposable repository and inspect the created resources and findings.

### Scope and persistence

Source leaves the local machine. A differential scan can still upload full repository context with its diff.

### Independent checks — proposed

- Check the packaged source for secrets and unnecessary content before upload.

- Confirm bucket, role, scan ID and source revision; inspect generated fixes before committing.

### Record to retain — proposed

Redacted integration config, provisioned resources, source manifest, scan result and reviewer decision.

### Stop, correct or remove

Review installed hooks and MCP tools; remove or disable the integration when access is no longer approved.

### Limits and fallback

The AWS integration page and current Kiro configuration guide show different manual config paths. Prefer the supported Power setup and inspect the installed configuration rather than copying an older path. No runtime guarantee is assumed.

Use the documented console or repository review flow while resolving client-version differences.

### Illustrative task — not executed

Illustrative: scan a small synthetic repository containing no credentials or customer data, without requesting fixes.

### Official guidance

[SI: Run code security scans from an IDE](https://docs.aws.amazon.com/securityagent/latest/userguide/code-review-ide-integration.html)

[KC: MCP configuration](https://kiro.dev/docs/mcp/configuration/)

[SB: Pricing and preview capability status](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## Proposed use-case exercise

Carry application evidence through repair and revalidation

Optional 12-minute walkthrough; additional to the core programme. Not an agent-runtime guarantee.

Use an owned staging application and explicit test authorization. Have a completed finding and a prepared deployed-fix result; do not wait for a full penetration test.

### 1. Fix the authorization boundary · 00:00–02:00

**Role:** Application owner · **Mechanism:** S-M02

Identify the test target, identities, exclusions and stop owner.

**Gate:** Written scope and approved test roles.

### 2. Identify the application inputs · 02:00–03:30

**Role:** Security engineer · **Mechanism:** S-M01

Select context at a known source and deployment revision.

**Gate:** Context-to-target revision match.

### 3. Review one finding · 03:30–05:30

**Role:** Security reviewer · **Mechanism:** S-M03

Inspect evidence, confidence and reproducibility.

**Gate:** Safe reproduction or an explicit inconclusive result.

### 4. Inspect remediation setup · 05:30–07:30

**Role:** Repository administrator · **Mechanism:** S-M05

Check per-repository enablement and inspect the proposed repair.

**Gate:** Finding-linked PR, no merge implied.

### 5. Verify the deployed version · 07:30–09:00

**Role:** Release owner · **Mechanism:** S-M05

Use the normal change process and confirm the staging commit.

**Gate:** Independent tests and deployed revision recorded.

### 6. Revalidate and record residual risk · 09:00–12:00

**Role:** Security reviewer · **Mechanism:** S-M06

Review the targeted revalidation job and original finding together.

**Gate:** Reachable target, correct identity and evidence for the result.

### Exit

The finding, proposed code change, deployed version and revalidation result are linked. “Not reproduced” is not rewritten as complete security assurance.

### Fallback

Use previously authorized prepared results and label the demonstration as a walkthrough; no test runs against an unapproved target.
