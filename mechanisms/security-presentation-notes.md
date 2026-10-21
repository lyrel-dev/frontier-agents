# AWS Security Agent / AWS Continuum — mechanism reference speaker notes

All reference slides are untimed. Optional exercises are additional to the core programme.

## S-M01 — Supply application context for a scoped test

Additional Learning Resources supply source and application documents to the assessment. This is task context; the reviewed guidance does not identify it as a persistent incident-memory control.

**Setup:** Create a penetration test and define the target and exclusions. At Additional Learning Resources, select connected resources or upload the relevant material. Confirm the selected revision and network access needed by connected sources before starting.

**Proposed verification:** Use a staging target and a non-sensitive application note with a traceable revision. Inspect test context and coverage against that revision; verify the deployed application matches it.

**Boundary:** Adding context does not authorize out-of-scope testing or establish cross-run model training.

## S-M02 — Authenticate a test without expanding its scope

Authentication lets the assessment reach authorized application behavior. The guide distinguishes direct credentials from advanced flows using IAM, Secrets Manager and Lambda.

**Setup:** Open the authentication configuration for the test. Choose the documented credential method; configure the login target and instructions where required. Verify the test account and its allowed roles before launching the assessment.

**Proposed verification:** Sign in with the test identity through an approved manual check. Confirm both an allowed operation and a forbidden operation; inspect test logs for authentication failures.

**Boundary:** Credentials do not belong in steering, persistent memory, exported evidence or this repository.

## S-M03 — Validate and review reported findings

The service uses deterministic checks where possible and independent replay in other cases. Results distinguish validated findings from lower-confidence or unverified candidates.

**Setup:** Open the penetration-test results and inspect the finding evidence. Review confidence, reproduction material and coverage, not just severity. Inspect unverified candidates separately where the interface permits; do not silently promote them to confirmed defects.

**Proposed verification:** Have an authorized reviewer reproduce a selected finding safely in staging. Compare the request, identity, application version and impact with the report.

**Boundary:** Validation does not prove complete security coverage. A missing finding is not proof that a defect is absent.

## S-M04 — Maintain security requirements as explicit policy context

Requirement packs define criteria used during design and code reviews. They are shared across Agent Spaces, not a private memory of one application.

**Setup:** Open Security requirements and select a managed pack or create a custom pack. For a custom requirement, define applicability, compliance criteria and remediation guidance. Enable the pack and run a new review to evaluate the change.

**Proposed verification:** Use one applicable example and one deliberately not-applicable example. Check the reported requirement identifier and retain the pack revision used for the review.

**Boundary:** Uploading new source documents regenerates the pack and replaces existing requirements, including manual entries. Framework packs do not certify compliance.

## S-M05 — Enable proposed code repair per repository

Repository remediation produces a proposed change for review. For the private GitHub path used here, the artifact is a pull request; other source providers can return different artifacts.

**Setup:** Open the Agent Space Penetration test tab and choose the GitHub registration, or edit its Code review repository entry. In the repository-capability wizard, enable Automatic remediation for the selected repository and choose Connect. From a supported finding, request remediation and inspect the resulting change.

**Proposed verification:** Match the finding to changed lines and inspect the PR scope. Run regression and security checks independently before any approved merge.

**Boundary:** A proposed repair may be incomplete or introduce regressions. An open PR is not evidence that the running application is fixed.

## S-M06 — Revalidate a deployed repair

Revalidation repeats checks for selected findings against the running target. It creates a separate job and does not replace the original finding record.

**Setup:** Deploy the reviewed repair to the originally authorized environment. Select findings in the completed test and choose revalidation. Review the new job status and evidence against the deployed version.

**Proposed verification:** Record the deployed commit and verify target/authentication health before interpreting the result. Distinguish a negative reproduction from an unreachable target or failed test.

**Boundary:** Resolved means the issue was not reproduced by that check. It is not an exhaustive assurance statement.

## Optional use-case exercise



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

