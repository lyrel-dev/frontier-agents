# AWS Security Agent

Design evaluation, source assessment and authorized application testing

Reviewed: 2026-10-21

A technical reference for application developers, security engineers and platform owners. The current official documentation identifies the service as part of AWS Continuum; this collection retains the requested AWS Security Agent name. The assessment modes are not interchangeable: each examines a different object and provides a different kind of evidence.

## Availability

On-demand penetration testing is generally available. Design review, threat modeling and code review remain preview in the cited documentation. Integration support, source-provider permissions and test-network access must be checked for the selected mode; service availability does not make every mode generally available.

Official documentation: [Pricing: capability status and task-hours semantics](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html) · [On-demand penetration testing general availability](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/) · [Document history and feature updates](https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html)


## Product objects

### Agent Space

The application assessment workspace and its configured source, target and access associations. Do not assume that a source connection is also permission to test the deployed application.

Official documentation: [What is AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)


### Requirement pack

A collection of security criteria evaluated during design and code reviews. Packs are shared across Agent Spaces; enabling a pack affects new reviews, not historical results.

Official documentation: [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)


### Assessment definition and run

A reusable review or test configuration versus one execution against particular source or target state. Keep the run ID and source revision; the latest configuration alone cannot describe an earlier result.

Official documentation: [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)


### Finding and validation result

A finding records a potential issue and its evidence. Severity, agent confidence, exploit validation and workflow status are separate attributes. Marking a finding resolved is not the same as executing a successful retest.

Official documentation: [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)


### Verified target domain

A domain verified and associated for testing. Domain verification and test credentials solve different problems: control of the destination versus the identity used inside the application.

Official documentation: [Verify a test domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html)


## Product functions

### Design and threat assessment

Evaluate intended controls and model threats before interpreting source or runtime observations.

#### S01 — Evaluate design documentation against enabled requirements

Availability: Preview. Activation: See invocation and prerequisites.

Design review compares the documented design with each applicable requirement. It evaluates what the design states, not what the production system actually enforces. The result can distinguish a demonstrated control, a documented violation, missing information and a requirement that does not apply.

**Input.** Design documents describing the workload and a set of enabled security requirements.

**Output.** Requirement-level results: compliant, non-compliant, insufficient data or not applicable, with supporting reasoning. Insufficient data is a request for evidence, not automatically a violation.

**Invocation and prerequisites.** Enable the intended requirement packs, create a design review with the relevant documents, then inspect the findings by requirement.

**Limitations and effects.** A compliant document does not establish a compliant implementation. A broad policy with vague applicability can create irrelevant findings; requirements and document versions must be recorded together.

**Proposed operator verification — not executed.** Use a document with one explicit control, one deliberate omission and one out-of-scope control. Confirm that missing evidence is distinguished from non-compliance and non-applicability.

Official documentation: [What is AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html) · [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html) · [Review design findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html)


#### S02 — Generate an application threat model

Availability: Preview. Activation: See invocation and prerequisites.

Threat modeling builds a system overview and identifies possible threats across assets, data flows and trust boundaries. Threats are classified using STRIDE and include prerequisites, actions, impacts and recommendations. This asks how the system could be attacked; it is not the same question as whether a fixed requirement is documented.

**Input.** Scope documents, source repositories, or both. Scope documents define the feature or design under analysis; source code supplies implementation context.

**Output.** A system model and threat records with severity and evidence. Operators can review and edit the model and threats before using them for engineering decisions.

**Invocation and prerequisites.** Enable threat modeling for the Agent Space, create a threat model with selected scope and sources, then start a run. Review the architecture interpretation before prioritizing the threat list.

**Limitations and effects.** An incorrect trust boundary can invalidate several otherwise plausible threats. A generated threat is not proof that an exploit succeeds on a running deployment.

**Proposed operator verification — not executed.** Reconcile identities, entry points, stores and trust boundaries with the system owners. For each selected threat, identify the actual attacker prerequisite and the control that should prevent the action.

Official documentation: [Enable threat modeling](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-threat-model.html) · [Create a threat model](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html) · [Review threat-model findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-threat-model-findings.html)


#### S10 — Generate structured requirements from policy documents

Availability: Documented. Activation: See invocation and prerequisites.

The service extracts security-relevant content and generates workload-level requirements with applicability, compliance criteria and remediation guidance. The operator reviews, edits or deletes the generated criteria before enabling the pack for new assessments.

**Input.** Security policies or standards in supported DOC, DOCX, Markdown, PDF or text files, submitted to a custom requirement pack.

**Output.** A custom pack of reviewable requirements. Generation does not show that an application meets the source policy.

**Invocation and prerequisites.** Security requirements → Custom security requirements packs → create or select a pack → Choose files → Generate requirements. Review and enable only after checking the generated criteria.

**Limitations and effects.** A new upload replaces all requirements in that pack, including hand-written entries. Concurrent uploads to the same pack are not allowed while generation is in progress.

**Proposed operator verification — not executed.** Map generated criteria back to selected source-policy clauses. Check applicability and observable compliance conditions; reject ambiguous or unsupported interpretations before enabling the pack.

Official documentation: [Generate requirements from documents](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html) · [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)


### Source-code assessment

Distinguish whole-codebase review, changed-code review and attempted runtime validation of source findings.

#### S03 — Analyze a complete source revision

Availability: Preview. Activation: See invocation and prerequisites.

Full code review performs context-aware static analysis across the submitted codebase for vulnerabilities and requirement violations. Preflight validates access and the analysis environment before scanning. Optional simulated validation is a later, distinct phase.

**Input.** A selected branch of a connected repository or a full-source ZIP in an authorized S3 location, plus enabled review settings and requirements.

**Output.** Findings tied to code locations, risk reasoning, evidence and suggested repairs; run logs and preflight results explain what actually executed.

**Invocation and prerequisites.** Code reviews → Create code review; select the source and service role, configure the review and start it. Inspect Preflight before interpreting the Findings tab.

**Limitations and effects.** A preflight failure means analysis did not proceed; an empty findings view is not an all-clear result. Dependency access, source completeness and filtering affect what is examined.

**Proposed operator verification — not executed.** Retain the source commit or S3 object version and run ID. Confirm successful preflight, inspect excluded paths and verify the source lines for one material finding.

Official documentation: [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html) · [Enable code reviews](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-code-review-scan.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)


#### S04 — Analyze changed code in a pull request or supplied diff

Availability: Preview. Activation: See invocation and prerequisites.

Differential review focuses findings on changed code while using surrounding source to interpret the change. A repository integration can post review comments; the programmatic S3 path starts a code-review job from submitted artifacts. These are invocation routes for changed-code analysis, not a full penetration test.

**Input.** Changed code with its full source context, provided by an eligible pull request integration or a full-source ZIP plus unified diff in S3.

**Output.** Findings associated with the change and, when configured, repository review comments. Provider support and publication permissions determine where results appear.

**Invocation and prerequisites.** Configure code-review comments and trigger filters for the repository. For the S3 route, provide both source and diff and use the documented StartCodeReviewJob request rather than uploading only the patch.

**Limitations and effects.** A diff-only review is not a complete baseline assessment of unchanged code. A skipped trigger and a successful review with no findings are different states.

**Proposed operator verification — not executed.** Use a controlled PR to test branch, draft and label filters. Confirm the job used the intended revision and changed lines; inspect whether a new commit actually caused a new run.

Official documentation: [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html) · [Review code findings in GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html) · [Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html) · [Enable code reviews](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-code-review-scan.html)


#### S05 — Attempt exploit validation of static findings in a simulated environment

Availability: Preview. Activation: See invocation and prerequisites.

After static analysis, the service provisions a simulated environment, starts the application and attempts to reproduce selected vulnerabilities. This adds runtime evidence to a source finding. It is not equivalent to testing the real deployed environment, its external services or production identity configuration.

**Input.** A code review with simulated validation enabled and an application that can run in the supported self-contained, containerized setup.

**Output.** Per-finding states such as confirmed, not reproduced, validation failed or not validated, together with available verification evidence.

**Invocation and prerequisites.** Enable simulated validation while configuring the code review. Check environment startup and dependency access before interpreting validation outcomes.

**Limitations and effects.** Validation failed is inconclusive. Not validated means no completed attempt for that finding. Not reproduced is limited to the attempted environment and conditions; it does not establish absence of the vulnerability.

**Proposed operator verification — not executed.** For a confirmed finding, inspect the executed path and evidence. For a failure or non-reproduction, inspect missing dependencies, authentication, timeouts and environment differences before dismissing the source finding.

Official documentation: [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)


### Deployed-application testing

Test an authorized target, then retest selected findings after a deployed fix.

#### S06 — Run a scoped penetration test against a deployed application

Availability: GA. Activation: See invocation and prerequisites.

The agent explores the authorized target, plans tests and attempts to validate security issues. The selected scope determines the risk classes: a web-application assessment differs from the generative-AI application scope. This operation sends real traffic to the target and can exercise application behavior.

**Input.** Verified and associated target domains, included and excluded paths, application scope, current credentials, network access and optional source/design context.

**Output.** A run with executed tasks, findings, evidence and coverage limitations. Run duration and billable task hours measure different things because work can execute concurrently.

**Invocation and prerequisites.** Enable penetration testing, verify the domain and create a penetration-test configuration. Set target scope, credentials, network access, risk selection and a maximum task-hours limit where appropriate before starting.

**Limitations and effects.** Credentials or networking failures can leave authenticated surfaces untested. A budget or run limit can stop work before coverage is complete. A risk class listed in scope does not mean every endpoint was tested for it.

**Proposed operator verification — not executed.** Verify the intended build and test identity at the target. Inspect executed tasks and access failures; compare the explored paths with the team's required test surface. Stop if real customer effects or out-of-scope traffic occur.

Official documentation: [Enable penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html) · [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html) · [Verify a test domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html) · [Provide test credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html) · [Pricing: capability status and task-hours semantics](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html) · [Document history and feature updates](https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html)


#### S07 — Retest selected existing penetration-test findings

Availability: Documented. Activation: See invocation and prerequisites.

Revalidation repeats the validation steps for the selected findings as a separate job. It does not discover new vulnerabilities or replace the original finding. The link between original evidence and subsequent attempts supports a remediation history.

**Input.** One or more findings from a completed run, with a fix already deployed to the same target and valid current authentication.

**Output.** Active when the issue is reproduced, or Resolved when it is not reproduced during the retest. A linked Jira issue can receive a result comment.

**Invocation and prerequisites.** Open the completed penetration-test run, choose Multiselect findings for revalidation, select the findings and choose Revalidate findings.

**Limitations and effects.** A patch existing only in a branch cannot change the running target's result. Resolved is scoped to that retest and is not an assurance that all related paths or regressions were tested.

**Proposed operator verification — not executed.** Confirm deployment identity and authentication before interpreting non-reproduction. Run the application's own regression tests and a broader test when the fix changes other trust boundaries.

Official documentation: [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


### Remediation and evidence management

Produce reviewable repair proposals and retain results without turning workflow status into a security guarantee.

#### S08 — Generate a code-remediation proposal

Availability: Preview. Activation: See invocation and prerequisites.

Code remediation generates a repair for review. Depending on the supported source route, the result is a pull or merge request or a downloadable diff. The source integration's write permission and remediation setting are separate from the permission to scan.

**Input.** A source finding, associated code and a source connection capable of returning the proposed change.

**Output.** A proposed patch and its explanation, not an accepted, merged, deployed or independently verified fix.

**Invocation and prerequisites.** Select Remediate code on an eligible finding and inspect the provider-specific result. For S3 sources, review the downloadable diff before applying it in the team's repository.

**Limitations and effects.** The change may remove intended behavior, miss another entry point or introduce a regression. Provider and repository eligibility affect whether an automated PR is available; do not assume universal write support.

**Proposed operator verification — not executed.** Review authorization logic and behavior, run positive and negative tests, then deploy through the normal change process. Use code rereview or target revalidation according to the original finding type.

Official documentation: [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html) · [Enable code reviews](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-code-review-scan.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)


#### S09 — Triage findings and export assessment evidence

Availability: Documented. Activation: See invocation and prerequisites.

The findings interface supports review of evidence and workflow disposition. Penetration-test report generation exports a selected set of findings and can include organization-authored annotation notes. Filtering controls what is shown or exported; it does not alter the set of tests that actually ran.

**Input.** Assessment findings with severity, confidence, validation evidence and the organization's disposition or annotations.

**Output.** A reviewable assessment record or PDF report. Organization annotations are distinct from the agent's assessment. Exporting a report does not confer compliance or certification.

**Invocation and prerequisites.** Inspect finding details and active confidence/status filters. From a penetration-test run, use Generate report and explicitly choose findings and annotation options.

**Limitations and effects.** A high-confidence-only view can hide unresolved findings. A workflow status such as resolved or accepted is not the same as confirmed exploit validation or successful revalidation.

**Proposed operator verification — not executed.** Before sharing a report, record run ID, source/build, target, test window, filters and unresolved coverage gaps. Reconcile exported totals against the selected findings, not the default dashboard alone.

Official documentation: [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)


## Configuration mechanisms

### SM1 — Configure criteria independently of the review being run

Requirement packs supply explicit evaluation criteria for design and code review. Managed requirements are read-only; custom requirements can be written, cloned or generated from existing policy documents. These criteria are not a learned memory of previous penetration-test incidents.

1. In the AWS console, open Security requirements and select the managed or custom packs relevant to the application.
2. For a custom requirement, specify applicability, observable compliant/non-compliant conditions and remediation guidance. Avoid a criterion such as 'use secure authentication' without a testable meaning.
3. To generate requirements from existing policies, upload supported documents into a custom pack and review the generated criteria before enabling it.
4. Enable the pack before a new design or code review. Record the pack version or reviewed definition with the assessment.
5. Treat a new document upload as replacement: it regenerates all requirements in that pack, including previously hand-written entries.

**Lifecycle.** Pack enablement and edits affect new reviews, not past results. A custom copy of a managed requirement does not automatically inherit later managed updates. Packs are shared across Agent Spaces, so changes need an identified owner.

**Proposed verification.** Proposed check: evaluate deliberately complete, incomplete and non-applicable design examples and verify that the criterion discriminates between them. Do not equate an enabled framework pack with an audit opinion.

Official documentation: [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html) · [Generate requirements from documents](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html) · [Review design findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html)


### SM2 — Configure source access and PR triggers as separate controls

Repository or S3 access determines what can be analyzed. Review-comment publication, remediation writes and automated triggers are separate settings. The effective review boundary is the combination of source revision, trigger configuration, analysis settings and file/context filters.

1. Connect the supported source provider or authorize the S3 bucket/prefix. Associate the intended source with the Agent Space and verify the service role's access.
2. Enable code-review comments and code-remediation writes only where required; do not grant source write access merely to perform static analysis.
3. Configure repository triggers for target branch, relevant event, draft state and supported labels. The documented branch expressions use RE2 full-name regular expressions, not shell globs.
4. Test condition groups: conditions within a group combine with AND; groups combine with OR. Label-based conditions are provider-dependent.
5. For GitHub filtering guidance, review .awssecurityagent/filtering.md on the default branch. Distinguish IgnorePatterns from ContextHints; hints are not an access-control mechanism.

**Lifecycle.** Changing filters changes future invocation or result selection. A manually requested review may bypass trigger filters; verify the documented provider command and settings before relying on them as a review gate.

**Proposed verification.** Proposed check: create matching and non-matching test changes, including a draft and a target-branch mismatch. Record the run IDs or the reason no run occurred. Inspect both review comments and the underlying run state.

Official documentation: [Connect GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-github.html) · [Configure S3 source access](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html) · [Enable code reviews](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-code-review-scan.html) · [Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html) · [Review code findings in GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html) · [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html)


### SM3 — Authorize the runtime target, identity and test surface

Testing authorization requires more than a URL. The registered domain establishes a permitted target; network configuration makes it reachable; credentials determine the authenticated surface. The test scope and exclusions limit what the service should exercise. None makes a production side effect harmless.

1. Verify domain control using the documented mechanism and associate the domain with the Agent Space. For private targets, follow the private-domain and VPC requirements rather than assuming public DNS verification covers the network path.
2. Create a test configuration with the intended URLs, excluded paths and selected risk classes. Use the generative-AI scope only when testing that application's LLM-related risks.
3. Provide dedicated test credentials through the supported credential flow. Check login and any required authentication step against the actual target before starting.
4. Supply relevant design/source context and network configuration. Restrict the test identity and replace payments, outbound messages and other irreversible effects with safe staging equivalents.
5. Set a task-hours limit and supervise run logs. Distinguish a graceful limit stop from a complete assessment.

**Lifecycle.** Changing credentials or a deployment can invalidate comparison with an earlier run. Domain association removal is distinct from deleting a registration. Keep target-side audit records for each test window.

**Proposed verification.** Proposed check: prove that the test identity reaches the required surface and cannot access out-of-scope data. Inspect real executed tasks rather than only configured risk categories.

Official documentation: [Verify a test domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html) · [Enable penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html) · [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html) · [Provide test credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html) · [Document history and feature updates](https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html) · [Pricing: capability status and task-hours semantics](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)


### SM4 — Interpret severity, confidence, validation and workflow status independently

Severity describes potential impact; confidence describes the agent's confidence in the finding; validation records an exploit attempt; workflow status records disposition. These are four different axes. A low-confidence high-impact issue still requires triage, and a manually resolved finding is not a successful runtime retest.

1. Inspect active confidence and status filters before counting findings or exporting a report. The code-review guide documents a high-confidence default; other assessment screens can use different defaults.
2. Read preflight and task logs before interpreting an empty list. Failed access or startup is an assessment failure, not absence of vulnerabilities.
3. For simulated validation, retain confirmed, not reproduced, validation failed and not validated distinctly.
4. For a deployed fix, start a revalidation job and retain its link to the original finding. Keep organization-authored risk acceptance or annotations separate from agent evidence.

**Lifecycle.** Revalidation adds a new result and does not overwrite the original. Findings can be filtered or dispositioned without changing what was tested. No documented general incident-memory retraining mechanism is inferred from these features.

**Proposed verification.** Proposed check: review one confirmed finding, one inconclusive validation and one accepted-risk item. The final report should make all three states distinguishable without reading hidden notes.

Official documentation: [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)


## Proposed operational procedures

### SU1 — Assess an authorization change before merging it

Determine whether a specific code change weakens an authorization boundary, and identify what still needs runtime testing.

**Use when:** A developer changes ownership checks, tenant scoping or role enforcement in a repository with configured review access.

**Not for:** Replacing code-owner review, proving production security from a passing diff review, or using a source-only result to claim exploitability.

**Functions used:** S03, S04, S05, S08

**Inputs**

- Base/head commit IDs and a complete source revision with the actual changed lines.
- The intended authorization rule and one allowed and one denied request, specified by the application owner.
- Relevant enabled requirements, PR trigger settings and excluded paths.
- A reproducible build and test harness; simulated validation only if the application fits its prerequisites.

1. **Developer — Define expected behavior.** State which principal may access which object and under what tenant/role condition. A request being authenticated does not establish that object access is authorized.

2. **Operator — Confirm that a review ran.** Check source revision, changed-line scope and preflight. If a filter skipped the PR or source access failed, fix that instead of interpreting no comments as a clean review.

3. **Developer and security reviewer — Trace the finding to code.** Follow the request through routing, identity extraction and ownership checks. Determine whether the finding is on an executed path and whether a relevant check exists elsewhere.

4. **Operator — Interpret validation separately.** For an optional simulated attempt, inspect runtime setup and evidence. Keep failed or unperformed attempts unresolved; do not downgrade a source issue merely because private dependencies prevented startup.

5. **Developer — Review the proposed repair.** Check that the patch enforces the intended rule without blocking allowed requests. Run positive and negative regression tests; deploy normally and test the runtime boundary when required.

**Acceptance:** A decision tied to the exact change, a disposition for each relevant finding and executable allowed/denied regression tests. Remaining runtime assumptions are listed explicitly.

**Stop:** Do not approve based on missing comments, a failed preflight, unknown source revision or a generated patch without behavior tests.

**Example instruction**

```text
Assess the change from <base> to <head> for the rule <principal/object/tenant condition>. Identify the actual code path and evidence for any bypass. Separate source findings from demonstrated runtime exploitation. Do not merge or deploy a repair.
```

**Demonstration allocation:** 5 minutes.

- 1 min: Show the authorization rule, exact diff and intended allowed/denied cases.
- 1 min: Confirm the prepared review's revision, preflight and trigger behavior.
- 1 min: Trace one finding and identify its validation state.
- 1 min: Review a proposed patch against both allowed and denied tests.
- 1 min: State the merge decision and remaining runtime evidence gap.

**Fallback:** Use a prepared, permission-cleared PR, finding and test output. Label the data as a prepared example; do not simulate a successful live scan.

Official documentation: [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html) · [Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)


### SU2 — Verify a deployed fix for a cross-user access finding

Confirm whether a previously observed authorization failure can still be reproduced on the patched staging build.

**Use when:** A completed authorized penetration test has a relevant finding and the proposed repair is deployed to the original target.

**Not for:** Testing a third-party target, discovering unrelated vulnerabilities through revalidation, or declaring the entire application secure after one non-reproduction.

**Functions used:** S06, S07, S09

**Inputs**

- Original run/finding ID, evidence, target URL and tested path.
- Patched build identifier and deployment time; proof that the running target uses that build.
- Two disposable test identities and test records with explicit ownership, where the application supports such testing.
- Authorization, exclusions, current credentials, target-side logs and a cleanup owner.

1. **Application owner — Verify the environment.** Confirm the patched build and current test identity. Seed disposable records and disable real outbound effects. Stop if the original finding cannot be mapped to the intended target.

2. **Operator — Run targeted revalidation.** Select the existing finding and start its separate revalidation job. Do not describe this as a new full penetration test.

3. **Security reviewer — Inspect the result and prerequisites.** If Active, inspect reproduction evidence and return to remediation. If Resolved, check that authentication and the intended endpoint worked; a login failure must not be accepted as a fixed authorization control.

4. **Developer — Run independent regressions.** Verify that the legitimate owner can still access its record and a different identity cannot. These are proposed application-specific tests, not a claimed built-in universal test fixture.

5. **Operator — Retain the evidence and decide breadth.** Record original and revalidation IDs, build, test identities' roles and application logs. Run a broader assessment if the fix alters other routes or trust boundaries.

**Acceptance:** Non-reproduction under valid test conditions plus passing allowed/denied application tests. The record states exactly which finding and build were tested and what remains outside scope.

**Stop:** Stop if the patched build is not deployed, credentials fail, the target differs or the test touches real customer data or external side effects.

**Example instruction**

```text
Revalidate finding <finding-id> on the authorized staging target after build <build-id>. Preserve the link to the original run. Report whether the same issue is reproduced and identify authentication or execution failures separately.
```

**Demonstration allocation:** 5 minutes.

- 1 min: Show original finding, authorized target and deployed build identity.
- 1 min: Explain the test identities and safe data boundary.
- 1 min: Open a prepared revalidation job and inspect execution evidence.
- 1 min: Contrast Active, valid non-reproduction and authentication failure.
- 1 min: Show independent regression results and the narrowly scoped conclusion.

**Fallback:** Walk through prepared original and retest evidence. Do not start an unbounded penetration test merely to fill a five-minute demonstration slot.

Official documentation: [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)


## Documentation qualifications

The general security-guidance FAQ has contained older statements about API and CI availability that conflict with newer feature-specific API and pipeline tutorials. This guide follows the documented full-source/diff job and current integration pages, not the older blanket statement.

Default confidence filtering differs between assessment views and documentation revisions. The operating procedure requires inspection of the actual filter instead of asserting one default for every screen.

A requirement evaluation, generated threat, static finding, simulated exploit and deployed-target revalidation are different evidence classes. None alone establishes application-wide security or certification.

This guide does not assume that previous assessments become a general incident-memory store. Reusable source context, requirement packs and linked retest history are the documented mechanisms described here.

## Official source register

- [What is AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

- [Pricing: capability status and task-hours semantics](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

- [On-demand penetration testing general availability](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

- [Document history and feature updates](https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html)

- [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

- [Generate requirements from documents](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

- [Review design findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html)

- [Enable threat modeling](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-threat-model.html)

- [Create a threat model](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html)

- [Review threat-model findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-threat-model-findings.html)

- [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)

- [Enable code reviews](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-code-review-scan.html)

- [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)

- [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html)

- [Review code findings in GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

- [Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html)

- [Connect GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/connect-github.html)

- [Configure S3 source access](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-s3-bucket.html)

- [Enable penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html)

- [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

- [Verify a test domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html)

- [Provide test credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

- [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

- [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

- [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)

- [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)

No live product execution or measured operational benefit is claimed.
