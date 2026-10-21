# AWS Security Agent — capability evidence record

Scope revision: 2026-10-21-three-agent-scope. This is a filtered record of the previously reviewed official evidence, not a new external documentation audit. Earlier editions are available through Git history.

## Current capability records

## C01 · Run an authorized application penetration test

**Documented function:** Launch an application-focused penetration test against configured targets and inspect discovered security findings.

**Availability:** GA · on-demand penetration testing

**Prerequisites:** Create an Agent Space, choose access and service roles, verify the target, and use a disposable non-production environment.

**Limitations:** Testing can change data or application state. Domain verification is a technical prerequisite, not a substitute for authorization covering every affected system.

**Proposed verification:** Confirm ownership, authorization, test-data isolation, stop responsibility, and environment recovery before launching.

- [S03 · On-demand penetration testing generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

- [S06 · Set up AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/setup-security-agent.html)

- [S07 · Enable a target domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html)

- [S10 · Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

## C02 · Test authenticated and private application paths

**Documented function:** Authenticated testing and VPC connectivity let the agent exercise protected application routes when correctly configured.

**Availability:** GA pentest workflow · optional configuration

**Prerequisites:** Use test-only identities, validate login, configure the service role/network, and classify discovered domains before the test.

**Limitations:** Credentials may expose additional application paths and supporting domains. A private network does not make testing harmless or remove scope obligations.

**Proposed verification:** Verify the identity has no production access and that every reachable dependency has the intended scope classification.

- [S09 · Provide testing credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

- [S08 · Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

- [S10 · Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

## C03 · Give a test current source and architecture context

**Documented function:** Attach code, API documentation, and design material to guide application understanding. Connected resources can supply updated source for later runs.

**Availability:** Documented pentest configuration

**Prerequisites:** Connect relevant resources or upload sanitized documentation; verify repository reachability from a private test network.

**Limitations:** Context does not guarantee complete endpoint coverage. Match the selected branch and documentation to the deployed target.

**Proposed verification:** Compare the deployed commit and API inventory with attached context; record untested critical paths for separate review.

- [S08 · Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

- [S11 · Security considerations and FAQs](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

## C04 · Control task expenditure and monitor execution

**Documented function:** Configure a maximum task-hours limit and monitor the run’s logs; stop work that takes an undesirable direction.

**Availability:** Documented pentest run controls

**Prerequisites:** Agree on a per-run work budget, excluded risk areas, an operator, and criteria for stopping the test.

**Limitations:** Task hours accumulate across parallel work and differ from wall-clock duration. Service quotas are not spending limits. A capped run can finish with partial coverage.

**Proposed verification:** Reconcile task hours with billing data and assess coverage separately from the run’s Completed status.

- [S08 · Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

- [S11 · Security considerations and FAQs](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

## C05 · Triage evidence rather than severity alone

**Documented function:** Inspect risk, confidence, affected endpoints, execution evidence, and reproduction details. Verification scripts are available when successfully generated and validated.

**Availability:** Documented pentest findings workflow

**Prerequisites:** Give a reviewer access to the run, logs, deployed build, and permitted reproduction environment.

**Limitations:** Not every finding has a script. Default filters can hide lower-confidence or unverified items; the visible count is not the complete security picture.

**Proposed verification:** Validate impact and reproducibility in the authorized test environment before assigning urgency or closing a finding.

- [S12 · Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

- [S10 · Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

## C06 · Request a proposed code fix for a pentest finding

**Documented function:** With remediation enabled for a connected repository, users can request a finding-specific fix delivered as a GitHub pull request.

**Availability:** Documented pentest remediation · repository setup required

**Prerequisites:** Authorize the GitHub app, enable remediation per repository in the Agent Space, and assign a human reviewer.

**Limitations:** Enabling remediation is not approval to merge or deploy. Generated changes can be incomplete, wrong, or visible to repository readers.

**Proposed verification:** Review the diff and test it normally, then deploy only through the existing change process.

- [S13 · Enable finding remediation](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html)

- [S10 · Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

## C07 · Revalidate a previously reported finding

**Documented function:** Revalidation checks selected existing findings against the application’s current reachable state.

**Availability:** Documented pentest revalidation

**Prerequisites:** Deploy the intended fix to the tested environment, retain working authentication, and select the completed run’s relevant findings.

**Limitations:** It does not search for new vulnerabilities. Resolved means the issue was not reproduced in this run, not that the application is globally secure.

**Proposed verification:** Inspect the separate revalidation job and evidence; use a broader test for substantial application changes.

- [S14 · Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

## C08 · Export a point-in-time evidence report

**Documented function:** Export a filtered penetration-test report with finding evidence and optional annotations for engineering or assurance review.

**Availability:** Documented pentest reporting

**Prerequisites:** Choose the run, finding filters, annotations, and intended audience; handle the resulting vulnerability details as sensitive.

**Limitations:** A compliance-oriented report layout is not a certification or a replacement for a required professional assessment. An interim report remains incomplete.

**Proposed verification:** Confirm report filters, run status, target version, and unresolved findings before sharing.

- [S15 · Export a penetration-test report](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)

## C09 · Create tracked Jira work from findings

**Documented function:** Create one Jira issue for each selected finding, carrying finding details and suggested remediation into a connected project.

**Availability:** Documented integration · pentest path; code path inherits preview

**Prerequisites:** Connect a Jira project to the Agent Space and agree on the project’s ownership and prioritization process.

**Limitations:** The project must support Task issues. Unlinking removes the association, not the Jira issue; the workflow is not documented here as full bidirectional synchronization.

**Proposed verification:** Check issue content, duplicate creation, project visibility, and the link back to the original finding.

- [S16 · Create Jira issues for findings](https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html)

## C10 · Review a design against organizational requirements

**Documented function:** Analyze design documents against enabled security requirements and return findings with remediation guidance.

**Availability:** Preview · design review

**Prerequisites:** Enable the relevant requirements and provide a sanitized, current design with clear trust boundaries.

**Limitations:** The result depends on document quality and the active requirement set; it is not an exhaustive architecture approval.

**Proposed verification:** Have an architect check assumptions and requirement applicability before treating a finding as a design decision.

- [S17 · Perform a design review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-design-review.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C11 · Maintain reusable organizational security criteria

**Documented function:** Security requirement packs provide reusable evaluation criteria; document import can help draft requirements for review.

**Availability:** Supports preview design and code reviews

**Prerequisites:** Choose managed or custom requirements, review any generated items, and enable the intended packs for subsequent reviews.

**Limitations:** An enabled pack is review configuration, not a guarantee of compliance. Imported statements need human checking for ambiguity and applicability.

**Proposed verification:** Test the criteria on known acceptable and unacceptable examples before relying on the findings.

- [S18 · Security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

- [S19 · Import security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C12 · Generate a reusable STRIDE threat model

**Documented function:** Use design scope documents, source context, or both to produce a system overview and STRIDE-classified threats with recommendations.

**Availability:** Preview · threat modeling

**Prerequisites:** Provide current architecture, trust boundaries, and relevant repositories or documents; define what is in scope.

**Limitations:** The model’s scope depends on the inputs: proposed-design documents and existing code serve different roles. It is not proof that every threat has been identified.

**Proposed verification:** Review assets, identities, data flows, boundaries, and omitted dependencies with an engineer familiar with the system.

- [S20 · Perform threat modeling](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-threat-model.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C13 · Scan a full codebase for security findings

**Documented function:** Run a full-code review against a connected supported repository or S3-hosted source and inspect file-level findings.

**Availability:** Preview · code review

**Prerequisites:** Connect the chosen source, select the branch or source package, configure access, and choose the intended review criteria.

**Limitations:** Provider setup and source support vary. A successful job is not assurance that all vulnerabilities or policy violations were found.

**Proposed verification:** Confirm the scanned revision, inspect finding context, and retain independent testing and code review.

- [S21 · Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)

- [S22 · Review code-scan findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)

- [S04 · What is AWS Security Agent?](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C14 · Review pull requests or merge requests on configured triggers

**Documented function:** Configured repository reviews post security findings on qualifying pull requests or merge requests, using the documented provider flow.

**Availability:** Preview · provider-specific PR/MR integration

**Prerequisites:** Enable code-review comments, select supported repositories, and test trigger/filter behavior on a controlled change.

**Limitations:** Branch, label, draft, and filter settings affect invocation. No comment can mean no trigger matched—not that a security scan passed.

**Proposed verification:** Inspect review execution and the exact commit; never use comment absence as a pass signal.

- [S23 · Review findings in pull requests](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

- [S24 · Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C15 · Receive a code-review fix as a PR, MR, or diff

**Documented function:** Supported connected private repositories can receive a PR or MR; S3 source and public GitHub paths use downloadable diffs.

**Availability:** Preview · remediation depends on source provider

**Prerequisites:** Enable the appropriate remediation capability and preserve the exact source revision used by the scan.

**Limitations:** Automated remediation is not supported for public GitLab or Bitbucket repositories in the documented matrix. Some findings require manual work.

**Proposed verification:** Apply and review through the normal repository process; verify the original finding and new regressions independently.

- [S25 · Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C17 · Submit a differential source review from a build workflow

**Documented function:** The documented API path accepts full source context in S3 together with a unified diff to focus a review on changed code.

**Availability:** Preview · S3/API code-review path

**Prerequisites:** Prepare approved S3 inputs and invoke the documented code-review job API from a suitably scoped build identity.

**Limitations:** It is not automatic discovery of your CI provider. The team must supply the correct source snapshot, diff base, permissions, and job handling.

**Proposed verification:** Validate source/diff consistency and handle failed or skipped jobs distinctly from a clean review.

- [S27 · Run a differential code scan with S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html)

- [S05 · Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

## C18 · Gate promotion using a scoped post-deployment pentest

**Documented function:** The documented integration tests a deployed change and can gate subsequent promotion using scoped findings and thresholds.

**Availability:** Public preview · CI/CD pipeline integration

**Prerequisites:** Configure a staging target, existing test setup, trusted OIDC role, diff baseline, thresholds, and explicit untested/error handling; begin with a dry run.

**Limitations:** It is not a pre-merge static check. Scoped-out changes can pass without dynamic testing; cancellation of the runner can leave a server-side job running.

**Proposed verification:** Validate every gate outcome and cancellation path. A passing pipeline must not be represented as a complete application assessment.

- [S28 · Run penetration tests from CI/CD](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

- [S29 · GitHub Actions scoped-pentest tutorial](https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html)

## Boundary

No live AWS account, workflow, penetration test or cost action was exercised in this scope revision.
