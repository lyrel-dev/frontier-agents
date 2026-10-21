# AWS Security Agent

Authorized application assessments, findings, remediation proposals and revalidation.


Revision: 21 October 2026. Independent engineering field guide.


**Audience:** Application-security engineers, software teams and security platform owners

**Availability:** On-demand penetration testing: GA. Design review, threat modeling, code review and CI/CD integration are separate preview capabilities.

**Recommended starting decision:** Start with one explicitly authorized staging application. Assess the safety of real requests, then connect findings to reviewed repairs and revalidation.


## Decision brief

A security assessment is useful when the finding is understandable, the affected application is known, and the team can act on the evidence. An automatically generated severity label is not enough. The application owner needs a reproducible account of the issue, a repair decision and evidence that the repaired deployment no longer exhibits the tested behavior.

The running scenario is an authorized assessment of a staging application with synthetic data and test identities. It follows scope, testing, finding triage, proposed remediation and revalidation. Design and code analysis are presented as complementary preview paths, not as guarantees of complete coverage or interchangeable forms of penetration testing.


## Running use case

**Name:** Assess and repair an owned staging application

**Trigger:** A team wants evidence about an application change before deciding how to proceed with release.

**Scope:** Verified targets, written authorization, test accounts, synthetic data, explicit exclusions and a stop owner.

**Deliverable:** A triaged finding linked to the tested revision, a reviewed remediation proposal and revalidation evidence.

**Not Done:** A generated fix exists, but it has not been reviewed, deployed to the test target or reassessed.

**Done:** The authorized test, code review and revalidation records support an owner-approved disposition of the finding.


## 1. Make authorization and target safety explicit

Define the application, exact target addresses, permitted test window, identities, exclusions and stop authority. Domain verification is a technical prerequisite; it is not permission from every system owner affected by a request. A staging label alone does not prove that payments, emails or other downstream effects are disabled.

Penetration testing sends real requests and can change application state. Use synthetic data and appropriately limited test identities, and understand the configured execution and spend controls. The demo should be possible without touching production or a third party outside the authorization.

**Capability crosswalk:** C01, C02, C04

**Responsible role (team recommendation):** Application owner and security operator

**Input:** Written scope, verified target, test identities, approved network path and operational stop procedure.

**Artifact:** An assessment authorization and preflight record.

**Gate:** The owner has approved the targets and business effects, not merely a hostname.

**Fallback:** Stop preparation when authority or downstream effects are unclear; use a labeled schematic walkthrough instead.


## 2. Give the assessment current application context

Source code, architecture documents and authentication details help the assessment understand the application. Keep the code revision aligned with the deployed test target. Old design documents or credentials for the wrong role can distort both coverage and interpretation.

Use the documented credential and private-connectivity paths rather than pasting secrets into example prompts or reports. Record what was reachable and authenticated. A test that did not reach a protected workflow cannot provide evidence that the workflow is safe.

**Capability crosswalk:** C02, C03

**Responsible role (team recommendation):** Application owner and security operator

**Input:** Current code and design context, revision identity, approved credentials and reachable test routes.

**Artifact:** A context and coverage record attached to the assessment.

**Gate:** The team knows which roles, routes and deployed revision were actually in scope.

**Fallback:** Report inaccessible areas as coverage gaps and resolve setup before drawing broader conclusions.


## 3. Observe the run and triage the evidence

Monitor the authorized task and inspect findings as evidence about a particular application state. Prioritization should combine the reported impact, reproducibility, affected data or role, and the service owner's business context. Do not equate finding count with assessment quality.

Preserve the path from the observation to the affected revision and identity. A validated exploit path can be valuable, but a clean result is not proof that every vulnerability class or application route has been covered. Escalate uncertain findings for human review rather than turning uncertainty into a release assurance.

**Capability crosswalk:** C01, C04, C05

**Responsible role (team recommendation):** Security analyst

**Input:** Assessment execution details and finding evidence.

**Artifact:** A triaged finding with owner, affected scope, reproduction context and disposition.

**Gate:** The service owner understands the finding and the limits of the assessment.

**Fallback:** Pause or stop on unexpected effects and retain an incomplete-run record instead of treating it as a pass.


## 4. Review a proposed repair as an engineering change

With the appropriate repository configuration, a finding can lead to a proposed code repair. That proposal needs normal review for correctness, compatibility and test coverage. A patch that blocks the observed path may still create a regression or leave a related path unresolved.

Track the finding and repair in the team's existing issue system. A Jira handoff is useful only when the audience is appropriate and the ticket links the evidence, affected revision and acceptance test. Do not publish sensitive assessment details to a broader channel simply because an integration is connected.

**Capability crosswalk:** C06, C09

**Responsible role (team recommendation):** Development owner and code reviewer

**Input:** Accepted finding, permitted repository access and a repair owner.

**Artifact:** A reviewed PR/MR or repair plan linked to the original finding.

**Gate:** The proposed change passes independent review and normal delivery controls.

**Fallback:** Assign a manual repair when repository support, authorization or generated output is inadequate.


## 5. Deploy to the authorized target and revalidate

A code fix is not the same as a repaired deployed application. Record the revision deployed to the authorized test target before requesting revalidation. Compare the result with the original evidence and confirm that the targeted behavior is no longer reproducible under the intended conditions.

Export a point-in-time report that preserves the scope, results and unresolved limitations. Closing the issue is an owner decision supported by assessment evidence, code review and revalidation. None of those artifacts alone is a certificate that the application is secure.

**Capability crosswalk:** C07, C08

**Responsible role (team recommendation):** Security operator and application owner

**Input:** Reviewed repair deployed to the approved target and linked to the original finding.

**Artifact:** Revalidation outcome and point-in-time evidence report.

**Gate:** The closure decision identifies the tested revision and remaining risks.

**Fallback:** Keep the finding open or explicitly risk-accepted if revalidation is inconclusive or fails.


## 6. Add earlier feedback without overstating availability

Design reviews, organizational security requirements and threat models can make assumptions and trust boundaries inspectable before testing a running application. Code review can analyze full repositories or configured change triggers, with provider-specific remediation paths. These are distinct from the GA on-demand penetration-testing baseline.

Treat S3 differential-scan and CI/CD integrations as separate preview adoption decisions. A promotion gate needs explicit thresholds, timeout behavior and a policy for missing or inconclusive evidence. The team owns that release policy; an unavailable or unfinished scan should not silently become a green gate.

**Capability crosswalk:** C10, C11, C12, C13, C14, C15, C17, C18

**Responsible role (team recommendation):** Security programme owner

**Input:** Approved preview use, provider-specific integration and an explicit review or promotion policy.

**Artifact:** Design, threat-model or code findings and an auditable gate decision where configured.

**Gate:** Availability, source-provider support and failure behavior are checked for the exact workflow.

**Fallback:** Retain the existing review and security checks until the preview path is accepted for the intended use.


## Detailed capability reference


### C01 — Run an authorized application penetration test

**Claim:** Launch an application-focused penetration test against configured targets and inspect discovered security findings.

**Availability:** GA · on-demand penetration testing

**Delivery:** Native; Agent Space and verified target

**Setup:** Create an Agent Space, choose access and service roles, verify the target, and use a disposable non-production environment.

**Limit:** Testing can change data or application state. Domain verification is a technical prerequisite, not a substitute for authorization covering every affected system.

**Check:** Confirm ownership, authorization, test-data isolation, stop responsibility, and environment recovery before launching.

**Prompt:** Prepare a scoped test of our staging application with written authorization, explicit excluded paths, and a named operator.

**Review record to retain (team recommendation):** Assessment scope, run identifier, target version, request evidence, and prioritized findings.

Official documentation references: S03, S06, S07, S10


### C02 — Test authenticated and private application paths

**Claim:** Authenticated testing and VPC connectivity let the agent exercise protected application routes when correctly configured.

**Availability:** GA pentest workflow · optional configuration

**Delivery:** Native credential and VPC configuration

**Setup:** Use test-only identities, validate login, configure the service role/network, and classify discovered domains before the test.

**Limit:** Credentials may expose additional application paths and supporting domains. A private network does not make testing harmless or remove scope obligations.

**Check:** Verify the identity has no production access and that every reachable dependency has the intended scope classification.

**Prompt:** Configure a typical staging-user identity, confirm its login, and exclude production, billing, and destructive administration paths.

**Review record to retain (team recommendation):** Authenticated test scope, identity configuration, private connectivity, and affected endpoint record.

Official documentation references: S09, S08, S10


### C03 — Give a test current source and architecture context

**Claim:** Attach code, API documentation, and design material to guide application understanding. Connected resources can supply updated source for later runs.

**Availability:** Documented pentest configuration

**Delivery:** Native; connected repositories or uploaded resources

**Setup:** Connect relevant resources or upload sanitized documentation; verify repository reachability from a private test network.

**Limit:** Context does not guarantee complete endpoint coverage. Match the selected branch and documentation to the deployed target.

**Check:** Compare the deployed commit and API inventory with attached context; record untested critical paths for separate review.

**Prompt:** Attach the deployed branch and current API description, and identify which user journeys matter most for this test.

**Review record to retain (team recommendation):** Input document/source-version inventory and findings tied to that context.

Official documentation references: S08, S11


### C04 — Control task expenditure and monitor execution

**Claim:** Configure a maximum task-hours limit and monitor the run’s logs; stop work that takes an undesirable direction.

**Availability:** Documented pentest run controls

**Delivery:** Native task-hour cap, logs, and stop controls

**Setup:** Agree on a per-run work budget, excluded risk areas, an operator, and criteria for stopping the test.

**Limit:** Task hours accumulate across parallel work and differ from wall-clock duration. Service quotas are not spending limits. A capped run can finish with partial coverage.

**Check:** Reconcile task hours with billing data and assess coverage separately from the run’s Completed status.

**Prompt:** Set a bounded task-hour limit and inspect progress for scope drift or application instability before allowing further runs.

**Review record to retain (team recommendation):** Task execution record with limits, elapsed use, relevant logs, and stop decision.

Official documentation references: S08, S05, S11


### C05 — Triage evidence rather than severity alone

**Claim:** Inspect risk, confidence, affected endpoints, execution evidence, and reproduction details. Verification scripts are available when successfully generated and validated.

**Availability:** Documented pentest findings workflow

**Delivery:** Native finding and log views

**Setup:** Give a reviewer access to the run, logs, deployed build, and permitted reproduction environment.

**Limit:** Not every finding has a script. Default filters can hide lower-confidence or unverified items; the visible count is not the complete security picture.

**Check:** Validate impact and reproducibility in the authorized test environment before assigning urgency or closing a finding.

**Prompt:** Review the highest-impact findings, separate confirmed evidence from assumptions, and inspect what the default filters exclude.

**Review record to retain (team recommendation):** Finding record with affected endpoint, reproduction evidence, confidence, and owner.

Official documentation references: S12, S10


### C06 — Request a proposed code fix for a pentest finding

**Claim:** With remediation enabled for a connected repository, users can request a finding-specific fix delivered as a GitHub pull request.

**Availability:** Documented pentest remediation · repository setup required

**Delivery:** Native GitHub PR proposal

**Setup:** Authorize the GitHub app, enable remediation per repository in the Agent Space, and assign a human reviewer.

**Limit:** Enabling remediation is not approval to merge or deploy. Generated changes can be incomplete, wrong, or visible to repository readers.

**Check:** Review the diff and test it normally, then deploy only through the existing change process.

**Prompt:** Request a minimal fix for this confirmed finding. Keep unrelated behavior unchanged and require regression coverage.

**Review record to retain (team recommendation):** Remediation code proposal linked to one finding and pending review/test evidence.

Official documentation references: S13, S10


### C07 — Revalidate a previously reported finding

**Claim:** Revalidation checks selected existing findings against the application’s current reachable state.

**Availability:** Documented pentest revalidation

**Delivery:** Native focused verification run

**Setup:** Deploy the intended fix to the tested environment, retain working authentication, and select the completed run’s relevant findings.

**Limit:** It does not search for new vulnerabilities. Resolved means the issue was not reproduced in this run, not that the application is globally secure.

**Check:** Inspect the separate revalidation job and evidence; use a broader test for substantial application changes.

**Prompt:** Revalidate this finding after the patch reaches the same staging target. Record the deployed commit and any authentication changes.

**Review record to retain (team recommendation):** Finding revalidation run and observed current behavior on the patched target.

Official documentation references: S14


### C08 — Export a point-in-time evidence report

**Claim:** Export a filtered penetration-test report with finding evidence and optional annotations for engineering or assurance review.

**Availability:** Documented pentest reporting

**Delivery:** Native PDF export

**Setup:** Choose the run, finding filters, annotations, and intended audience; handle the resulting vulnerability details as sensitive.

**Limit:** A compliance-oriented report layout is not a certification or a replacement for a required professional assessment. An interim report remains incomplete.

**Check:** Confirm report filters, run status, target version, and unresolved findings before sharing.

**Prompt:** Export the completed staging assessment with high-priority findings and reviewer notes, including scope and known omissions.

**Review record to retain (team recommendation):** Point-in-time exported report with applied filters, revision, and recorded annotations.

Official documentation references: S15


### C09 — Create tracked Jira work from findings

**Claim:** Create one Jira issue for each selected finding, carrying finding details and suggested remediation into a connected project.

**Availability:** Documented integration · pentest path; code path inherits preview

**Delivery:** Native issue export; connected Jira project

**Setup:** Connect a Jira project to the Agent Space and agree on the project’s ownership and prioritization process.

**Limit:** The project must support Task issues. Unlinking removes the association, not the Jira issue; the workflow is not documented here as full bidirectional synchronization.

**Check:** Check issue content, duplicate creation, project visibility, and the link back to the original finding.

**Prompt:** Export these reviewed findings to the security-remediation project, then let the normal team workflow assign owners.

**Review record to retain (team recommendation):** Jira finding issue with assignment, reproduction evidence, and disposition.

Official documentation references: S16


### C10 — Review a design against organizational requirements

**Claim:** Analyze design documents against enabled security requirements and return findings with remediation guidance.

**Availability:** Preview · design review

**Delivery:** Native document review

**Setup:** Enable the relevant requirements and provide a sanitized, current design with clear trust boundaries.

**Limit:** The result depends on document quality and the active requirement set; it is not an exhaustive architecture approval.

**Check:** Have an architect check assumptions and requirement applicability before treating a finding as a design decision.

**Prompt:** Review the proposed service-to-service authentication design against our enabled controls, and identify missing information explicitly.

**Review record to retain (team recommendation):** Design-review findings mapped to versioned security requirements and source documents.

Official documentation references: S17, S05


### C11 — Maintain reusable organizational security criteria

**Claim:** Security requirement packs provide reusable evaluation criteria; document import can help draft requirements for review.

**Availability:** Supports preview design and code reviews

**Delivery:** Native requirement packs and document import

**Setup:** Choose managed or custom requirements, review any generated items, and enable the intended packs for subsequent reviews.

**Limit:** An enabled pack is review configuration, not a guarantee of compliance. Imported statements need human checking for ambiguity and applicability.

**Check:** Test the criteria on known acceptable and unacceptable examples before relying on the findings.

**Prompt:** Translate the approved logging standard into precise review criteria; flag obligations that cannot be assessed from design or source alone.

**Review record to retain (team recommendation):** Versioned requirement pack, change rationale, and review evidence.

Official documentation references: S18, S19, S05


### C12 — Generate a reusable STRIDE threat model

**Claim:** Use design scope documents, source context, or both to produce a system overview and STRIDE-classified threats with recommendations.

**Availability:** Preview · threat modeling

**Delivery:** Native model generation and reruns

**Setup:** Provide current architecture, trust boundaries, and relevant repositories or documents; define what is in scope.

**Limit:** The model’s scope depends on the inputs: proposed-design documents and existing code serve different roles. It is not proof that every threat has been identified.

**Check:** Review assets, identities, data flows, boundaries, and omitted dependencies with an engineer familiar with the system.

**Prompt:** Model threats for the proposed webhook ingestion flow, using the existing service as context and stating uncertain assumptions.

**Review record to retain (team recommendation):** STRIDE model with trust boundaries, assumptions, threats, and unresolved mitigations.

Official documentation references: S20, S05


### C13 — Scan a full codebase for security findings

**Claim:** Run a full-code review against a connected supported repository or S3-hosted source and inspect file-level findings.

**Availability:** Preview · code review

**Delivery:** Native repository or S3-source review

**Setup:** Connect the chosen source, select the branch or source package, configure access, and choose the intended review criteria.

**Limit:** Provider setup and source support vary. A successful job is not assurance that all vulnerabilities or policy violations were found.

**Check:** Confirm the scanned revision, inspect finding context, and retain independent testing and code review.

**Prompt:** Review the release-candidate source for security risks and explain the evidence for each high-priority finding.

**Review record to retain (team recommendation):** Code-review findings associated with exact repository/source revision.

Official documentation references: S21, S22, S04, S05


### C14 — Review pull requests or merge requests on configured triggers

**Claim:** Configured repository reviews post security findings on qualifying pull requests or merge requests, using the documented provider flow.

**Availability:** Preview · provider-specific PR/MR integration

**Delivery:** Native code-change feedback

**Setup:** Enable code-review comments, select supported repositories, and test trigger/filter behavior on a controlled change.

**Limit:** Branch, label, draft, and filter settings affect invocation. No comment can mean no trigger matched—not that a security scan passed.

**Check:** Inspect review execution and the exact commit; never use comment absence as a pass signal.

**Prompt:** Configure review for release-bound changes and verify that both an included and an excluded change produce the expected invocation behavior.

**Review record to retain (team recommendation):** PR or MR finding comments with trigger event, build revision, and reviewer disposition.

Official documentation references: S23, S24, S05


### C15 — Receive a code-review fix as a PR, MR, or diff

**Claim:** Supported connected private repositories can receive a PR or MR; S3 source and public GitHub paths use downloadable diffs.

**Availability:** Preview · remediation depends on source provider

**Delivery:** Native fix proposal; delivery varies

**Setup:** Enable the appropriate remediation capability and preserve the exact source revision used by the scan.

**Limit:** Automated remediation is not supported for public GitLab or Bitbucket repositories in the documented matrix. Some findings require manual work.

**Check:** Apply and review through the normal repository process; verify the original finding and new regressions independently.

**Prompt:** Generate a narrow remediation for this validated source finding and identify tests required to show that behavior is preserved.

**Review record to retain (team recommendation):** Proposed PR/MR or patch/diff and independent implementation tests.

Official documentation references: S25, S05


### C17 — Submit a differential source review from a build workflow

**Claim:** The documented API path accepts full source context in S3 together with a unified diff to focus a review on changed code.

**Availability:** Preview · S3/API code-review path

**Delivery:** Native API; pipeline wiring is team-owned

**Setup:** Prepare approved S3 inputs and invoke the documented code-review job API from a suitably scoped build identity.

**Limit:** It is not automatic discovery of your CI provider. The team must supply the correct source snapshot, diff base, permissions, and job handling.

**Check:** Validate source/diff consistency and handle failed or skipped jobs distinctly from a clean review.

**Prompt:** Construct a review input from the current commit and its approved base, then fail setup checks when the diff does not match the uploaded source.

**Review record to retain (team recommendation):** Build-submitted differential review record with full source baseline and unified diff.

Official documentation references: S27, S05


### C18 — Gate promotion using a scoped post-deployment pentest

**Claim:** The documented integration tests a deployed change and can gate subsequent promotion using scoped findings and thresholds.

**Availability:** Public preview · CI/CD pipeline integration

**Delivery:** Native service job; configured pipeline integration

**Setup:** Configure a staging target, existing test setup, trusted OIDC role, diff baseline, thresholds, and explicit untested/error handling; begin with a dry run.

**Limit:** It is not a pre-merge static check. Scoped-out changes can pass without dynamic testing; cancellation of the runner can leave a server-side job running.

**Check:** Validate every gate outcome and cancellation path. A passing pipeline must not be represented as a complete application assessment.

**Prompt:** Add a staging-only gate that records whether the change was tested, scoped out, or unresolved, and stops server work during abort handling.

**Review record to retain (team recommendation):** Post-deployment assessment result and separately recorded promotion decision.

Official documentation references: S28, S29


## Illustrative handoff

```yaml

assessment: SEC-DEMO-001
target: owned-staging-application
authorization: approved-scope-record
data: synthetic-only
revision: DEMO-A
finding: illustrative-finding-reference
repair: reviewed-branch-change
closure: deployed-revision-plus-revalidation
exclusions: [production, unapproved-third-parties]

```


## Readiness checklist

- [ ] Written authorization covers every target and relevant downstream effect.

- [ ] The test uses synthetic data and limited test identities.

- [ ] Source context and deployed revision agree.

- [ ] Execution, budget and stop ownership are configured.

- [ ] Findings and generated repairs receive independent review.

- [ ] Revalidation and closure identify the tested repaired revision.


## Sources

- S02: [AWS Continuum](https://aws.amazon.com/continuum/)

- S03: [On-demand penetration testing generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

- S04: [What is AWS Security Agent?](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

- S05: [Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

- S06: [Set up AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/setup-security-agent.html)

- S07: [Enable a target domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html)

- S08: [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

- S09: [Provide testing credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

- S10: [Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

- S11: [Security considerations and FAQs](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

- S12: [Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

- S13: [Enable finding remediation](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html)

- S14: [Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

- S15: [Export a penetration-test report](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)

- S16: [Create Jira issues for findings](https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html)

- S17: [Perform a design review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-design-review.html)

- S18: [Security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

- S19: [Import security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

- S20: [Perform threat modeling](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-threat-model.html)

- S21: [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)

- S22: [Review code-scan findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)

- S23: [Review findings in pull requests](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

- S24: [Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html)

- S25: [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)

- S27: [Run a differential code scan with S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html)

- S28: [Run penetration tests from CI/CD](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

- S29: [GitHub Actions scoped-pentest tutorial](https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html)

- S30: [Resilience and regional availability](https://docs.aws.amazon.com/securityagent/latest/userguide/resilience.html)


## Validation boundary

Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.


## Mechanisms and enablement extension

See the [detailed source-linked setup and verification guide](../mechanisms/security.md). It contains 6 records, a proposed six-step exercise and lifecycle controls. Existing presentation timing is unchanged.
