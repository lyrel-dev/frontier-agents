# AWS Security Agent — documentation-validation record and presentation transcript

**Day-to-day application security · now part of AWS Continuum**

Documentation reviewed: **20 October 2026**. Independent synthesis of official AWS/Kiro sources; not an AWS publication.

**Scope:** Authorized application penetration testing, finding triage, remediation handoff, and explicitly labeled preview design/code workflows. This is the frontier agent formerly branded AWS Security Agent, not the separate gated-preview Continuum for code vulnerabilities offering.

**Overview:** Start with the established on-demand penetration-testing workflow on an authorized non-production application. Review evidence, route findings, propose fixes, and revalidate. Evaluate preview design, code, and CI/CD workflows separately rather than treating service-level GA as a blanket feature status.

**Read before adoption:** Penetration testing is GA, but code review, design review, threat modeling, and the documented CI/CD pipeline integration remain preview. Tests can alter application state. Use an authorized non-production target, narrow scope, and test-only credentials. [S03] [S05] [S29] [S10]

## Validation method and outcome

18 capability entries; eight presentation sections; 30 official references.

| Verdict | Entries | Meaning |
|---|---:|---|
| Confirmed | 2 | Core behavior directly documented. |
| Qualified | 16 | Documented behavior with material setup, access, or safety restrictions. |
| Workflow example | 0 | Author-proposed use of documented tools, not a separately established native feature. |

Verdicts are not maturity labels. A confirmed claim can still be preview. Every feature’s availability is recorded separately.

**Validation boundary:** Documentation review only. No AWS account, repository, application, permission policy, prompt, or agent workflow was exercised. Demonstrations and acceptance checks are proposed. No productivity, diagnostic-accuracy, detection-rate, or savings outcome was measured.

**Excluded from this first pass:** Production-target testing, unrestricted scanning, unsupported compliance guarantees, enterprise-wide vulnerability management, and the separate gated-preview Continuum for code vulnerabilities offering are outside this first pass. Preview workflows are hidden by default in the explorer.

## Recommended starting workflow

1. Create an Agent Space and authorize one verified, isolated staging target.

2. Run a bounded assessment with scoped credentials, current source context, and an operator watching execution.

3. Validate findings, review proposed fixes, and revalidate after deployment through the normal change process.

## Capability register

### C01 — Run an authorized application penetration test

**Area:** Penetration testing  
**Verdict:** Qualified  
**Availability:** GA · on-demand penetration testing  
**Delivery model:** Native; Agent Space and verified target

**Documented capability:** Launch an application-focused penetration test against configured targets and inspect discovered security findings. [S03] [S06] [S07] [S10]

**Boundary:** Testing can change data or application state. Domain verification is a technical prerequisite, not a substitute for authorization covering every affected system.

**Prerequisites:** Create an Agent Space, choose access and service roles, verify the target, and use a disposable non-production environment.

**Example task or prompt — author-created, not executed:**

> Prepare a scoped test of our staging application with written authorization, explicit excluded paths, and a named operator.

**Engineering acceptance check — recommendation:** Confirm ownership, authorization, test-data isolation, stop responsibility, and environment recovery before launching.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C02 — Test authenticated and private application paths

**Area:** Penetration testing  
**Verdict:** Qualified  
**Availability:** GA pentest workflow · optional configuration  
**Delivery model:** Native credential and VPC configuration

**Documented capability:** Authenticated testing and VPC connectivity let the agent exercise protected application routes when correctly configured. [S09] [S08] [S10]

**Boundary:** Credentials may expose additional application paths and supporting domains. A private network does not make testing harmless or remove scope obligations.

**Prerequisites:** Use test-only identities, validate login, configure the service role/network, and classify discovered domains before the test.

**Example task or prompt — author-created, not executed:**

> Configure a typical staging-user identity, confirm its login, and exclude production, billing, and destructive administration paths.

**Engineering acceptance check — recommendation:** Verify the identity has no production access and that every reachable dependency has the intended scope classification.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C03 — Give a test current source and architecture context

**Area:** Penetration testing  
**Verdict:** Confirmed  
**Availability:** Documented pentest configuration  
**Delivery model:** Native; connected repositories or uploaded resources

**Documented capability:** Attach code, API documentation, and design material to guide application understanding. Connected resources can supply updated source for later runs. [S08] [S11]

**Boundary:** Context does not guarantee complete endpoint coverage. Match the selected branch and documentation to the deployed target.

**Prerequisites:** Connect relevant resources or upload sanitized documentation; verify repository reachability from a private test network.

**Example task or prompt — author-created, not executed:**

> Attach the deployed branch and current API description, and identify which user journeys matter most for this test.

**Engineering acceptance check — recommendation:** Compare the deployed commit and API inventory with attached context; record untested critical paths for separate review.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C04 — Control task expenditure and monitor execution

**Area:** Penetration testing  
**Verdict:** Qualified  
**Availability:** Documented pentest run controls  
**Delivery model:** Native task-hour cap, logs, and stop controls

**Documented capability:** Configure a maximum task-hours limit and monitor the run’s logs; stop work that takes an undesirable direction. [S08] [S05] [S11]

**Boundary:** Task hours accumulate across parallel work and differ from wall-clock duration. Service quotas are not spending limits. A capped run can finish with partial coverage.

**Prerequisites:** Agree on a per-run work budget, excluded risk areas, an operator, and criteria for stopping the test.

**Example task or prompt — author-created, not executed:**

> Set a bounded task-hour limit and inspect progress for scope drift or application instability before allowing further runs.

**Engineering acceptance check — recommendation:** Reconcile task hours with billing data and assess coverage separately from the run’s Completed status.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C05 — Triage evidence rather than severity alone

**Area:** Findings and remediation  
**Verdict:** Qualified  
**Availability:** Documented pentest findings workflow  
**Delivery model:** Native finding and log views

**Documented capability:** Inspect risk, confidence, affected endpoints, execution evidence, and reproduction details. Verification scripts are available when successfully generated and validated. [S12] [S10]

**Boundary:** Not every finding has a script. Default filters can hide lower-confidence or unverified items; the visible count is not the complete security picture.

**Prerequisites:** Give a reviewer access to the run, logs, deployed build, and permitted reproduction environment.

**Example task or prompt — author-created, not executed:**

> Review the highest-impact findings, separate confirmed evidence from assumptions, and inspect what the default filters exclude.

**Engineering acceptance check — recommendation:** Validate impact and reproducibility in the authorized test environment before assigning urgency or closing a finding.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C06 — Request a proposed code fix for a pentest finding

**Area:** Findings and remediation  
**Verdict:** Qualified  
**Availability:** Documented pentest remediation · repository setup required  
**Delivery model:** Native GitHub PR proposal

**Documented capability:** With remediation enabled for a connected repository, users can request a finding-specific fix delivered as a GitHub pull request. [S13] [S10]

**Boundary:** Enabling remediation is not approval to merge or deploy. Generated changes can be incomplete, wrong, or visible to repository readers.

**Prerequisites:** Authorize the GitHub app, enable remediation per repository in the Agent Space, and assign a human reviewer.

**Example task or prompt — author-created, not executed:**

> Request a minimal fix for this confirmed finding. Keep unrelated behavior unchanged and require regression coverage.

**Engineering acceptance check — recommendation:** Review the diff and test it normally, then deploy only through the existing change process.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C07 — Revalidate a previously reported finding

**Area:** Findings and remediation  
**Verdict:** Qualified  
**Availability:** Documented pentest revalidation  
**Delivery model:** Native focused verification run

**Documented capability:** Revalidation checks selected existing findings against the application’s current reachable state. [S14]

**Boundary:** It does not search for new vulnerabilities. Resolved means the issue was not reproduced in this run, not that the application is globally secure.

**Prerequisites:** Deploy the intended fix to the tested environment, retain working authentication, and select the completed run’s relevant findings.

**Example task or prompt — author-created, not executed:**

> Revalidate this finding after the patch reaches the same staging target. Record the deployed commit and any authentication changes.

**Engineering acceptance check — recommendation:** Inspect the separate revalidation job and evidence; use a broader test for substantial application changes.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C08 — Export a point-in-time evidence report

**Area:** Findings and remediation  
**Verdict:** Qualified  
**Availability:** Documented pentest reporting  
**Delivery model:** Native PDF export

**Documented capability:** Export a filtered penetration-test report with finding evidence and optional annotations for engineering or assurance review. [S15]

**Boundary:** A compliance-oriented report layout is not a certification or a replacement for a required professional assessment. An interim report remains incomplete.

**Prerequisites:** Choose the run, finding filters, annotations, and intended audience; handle the resulting vulnerability details as sensitive.

**Example task or prompt — author-created, not executed:**

> Export the completed staging assessment with high-priority findings and reviewer notes, including scope and known omissions.

**Engineering acceptance check — recommendation:** Confirm report filters, run status, target version, and unresolved findings before sharing.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C09 — Create tracked Jira work from findings

**Area:** Findings and remediation  
**Verdict:** Confirmed  
**Availability:** Documented integration · pentest path; code path inherits preview  
**Delivery model:** Native issue export; connected Jira project

**Documented capability:** Create one Jira issue for each selected finding, carrying finding details and suggested remediation into a connected project. [S16]

**Boundary:** The project must support Task issues. Unlinking removes the association, not the Jira issue; the workflow is not documented here as full bidirectional synchronization.

**Prerequisites:** Connect a Jira project to the Agent Space and agree on the project’s ownership and prioritization process.

**Example task or prompt — author-created, not executed:**

> Export these reviewed findings to the security-remediation project, then let the normal team workflow assign owners.

**Engineering acceptance check — recommendation:** Check issue content, duplicate creation, project visibility, and the link back to the original finding.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C10 — Review a design against organizational requirements

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · design review  
**Delivery model:** Native document review

**Documented capability:** Analyze design documents against enabled security requirements and return findings with remediation guidance. [S17] [S05]

**Boundary:** The result depends on document quality and the active requirement set; it is not an exhaustive architecture approval.

**Prerequisites:** Enable the relevant requirements and provide a sanitized, current design with clear trust boundaries.

**Example task or prompt — author-created, not executed:**

> Review the proposed service-to-service authentication design against our enabled controls, and identify missing information explicitly.

**Engineering acceptance check — recommendation:** Have an architect check assumptions and requirement applicability before treating a finding as a design decision.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C11 — Maintain reusable organizational security criteria

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Supports preview design and code reviews  
**Delivery model:** Native requirement packs and document import

**Documented capability:** Security requirement packs provide reusable evaluation criteria; document import can help draft requirements for review. [S18] [S19] [S05]

**Boundary:** An enabled pack is review configuration, not a guarantee of compliance. Imported statements need human checking for ambiguity and applicability.

**Prerequisites:** Choose managed or custom requirements, review any generated items, and enable the intended packs for subsequent reviews.

**Example task or prompt — author-created, not executed:**

> Translate the approved logging standard into precise review criteria; flag obligations that cannot be assessed from design or source alone.

**Engineering acceptance check — recommendation:** Test the criteria on known acceptable and unacceptable examples before relying on the findings.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C12 — Generate a reusable STRIDE threat model

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · threat modeling  
**Delivery model:** Native model generation and reruns

**Documented capability:** Use design scope documents, source context, or both to produce a system overview and STRIDE-classified threats with recommendations. [S20] [S05]

**Boundary:** The model’s scope depends on the inputs: proposed-design documents and existing code serve different roles. It is not proof that every threat has been identified.

**Prerequisites:** Provide current architecture, trust boundaries, and relevant repositories or documents; define what is in scope.

**Example task or prompt — author-created, not executed:**

> Model threats for the proposed webhook ingestion flow, using the existing service as context and stating uncertain assumptions.

**Engineering acceptance check — recommendation:** Review assets, identities, data flows, boundaries, and omitted dependencies with an engineer familiar with the system.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C13 — Scan a full codebase for security findings

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · code review  
**Delivery model:** Native repository or S3-source review

**Documented capability:** Run a full-code review against a connected supported repository or S3-hosted source and inspect file-level findings. [S21] [S22] [S04] [S05]

**Boundary:** Provider setup and source support vary. A successful job is not assurance that all vulnerabilities or policy violations were found.

**Prerequisites:** Connect the chosen source, select the branch or source package, configure access, and choose the intended review criteria.

**Example task or prompt — author-created, not executed:**

> Review the release-candidate source for security risks and explain the evidence for each high-priority finding.

**Engineering acceptance check — recommendation:** Confirm the scanned revision, inspect finding context, and retain independent testing and code review.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C14 — Review pull requests or merge requests on configured triggers

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · provider-specific PR/MR integration  
**Delivery model:** Native code-change feedback

**Documented capability:** Configured repository reviews post security findings on qualifying pull requests or merge requests, using the documented provider flow. [S23] [S24] [S05]

**Boundary:** Branch, label, draft, and filter settings affect invocation. No comment can mean no trigger matched—not that a security scan passed.

**Prerequisites:** Enable code-review comments, select supported repositories, and test trigger/filter behavior on a controlled change.

**Example task or prompt — author-created, not executed:**

> Configure review for release-bound changes and verify that both an included and an excluded change produce the expected invocation behavior.

**Engineering acceptance check — recommendation:** Inspect review execution and the exact commit; never use comment absence as a pass signal.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C15 — Receive a code-review fix as a PR, MR, or diff

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · remediation depends on source provider  
**Delivery model:** Native fix proposal; delivery varies

**Documented capability:** Supported connected private repositories can receive a PR or MR; S3 source and public GitHub paths use downloadable diffs. [S25] [S05]

**Boundary:** Automated remediation is not supported for public GitLab or Bitbucket repositories in the documented matrix. Some findings require manual work.

**Prerequisites:** Enable the appropriate remediation capability and preserve the exact source revision used by the scan.

**Example task or prompt — author-created, not executed:**

> Generate a narrow remediation for this validated source finding and identify tests required to show that behavior is preserved.

**Engineering acceptance check — recommendation:** Apply and review through the normal repository process; verify the original finding and new regressions independently.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C16 — Start a code review from the developer’s IDE

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · MCP or Kiro Power integration  
**Delivery model:** Configured client integration with cloud scan

**Documented capability:** The IDE integration packages source for a service-backed code review and returns findings through the configured client. [S26] [S05]

**Boundary:** This is not an offline local-only scan: source is uploaded to S3. Initial setup can provision an Agent Space, role, and bucket and requires corresponding IAM permissions.

**Prerequisites:** Install the supported integration, review first-use provisioning permissions, and approve the code/data handling boundary.

**Example task or prompt — author-created, not executed:**

> Run a review of this approved repository through the configured security integration and show the submitted source scope.

**Engineering acceptance check — recommendation:** Check upload contents, resource ownership, retention settings, and returned scan revision before accepting the result.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C17 — Submit a differential source review from a build workflow

**Area:** Preview design and code  
**Verdict:** Qualified  
**Availability:** Preview · S3/API code-review path  
**Delivery model:** Native API; pipeline wiring is team-owned

**Documented capability:** The documented API path accepts full source context in S3 together with a unified diff to focus a review on changed code. [S27] [S05]

**Boundary:** It is not automatic discovery of your CI provider. The team must supply the correct source snapshot, diff base, permissions, and job handling.

**Prerequisites:** Prepare approved S3 inputs and invoke the documented code-review job API from a suitably scoped build identity.

**Example task or prompt — author-created, not executed:**

> Construct a review input from the current commit and its approved base, then fail setup checks when the diff does not match the uploaded source.

**Engineering acceptance check — recommendation:** Validate source/diff consistency and handle failed or skipped jobs distinctly from a clean review.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

### C18 — Gate promotion using a scoped post-deployment pentest

**Area:** Preview delivery integration  
**Verdict:** Qualified  
**Availability:** Public preview · CI/CD pipeline integration  
**Delivery model:** Native service job; configured pipeline integration

**Documented capability:** The documented integration tests a deployed change and can gate subsequent promotion using scoped findings and thresholds. [S28] [S29]

**Boundary:** It is not a pre-merge static check. Scoped-out changes can pass without dynamic testing; cancellation of the runner can leave a server-side job running.

**Prerequisites:** Configure a staging target, existing test setup, trusted OIDC role, diff baseline, thresholds, and explicit untested/error handling; begin with a dry run.

**Example task or prompt — author-created, not executed:**

> Add a staging-only gate that records whether the change was tested, scoped out, or unresolved, and stops server work during abort handling.

**Engineering acceptance check — recommendation:** Validate every gate outcome and cancellation path. A passing pipeline must not be represented as a complete application assessment.

**Validation note:** Core behavior is documented; the example task and acceptance check are author recommendations, not executed demonstrations.

## Cross-cutting validation record

### G01 — Current name and excluded adjacent product

AWS positions the frontier agent as part of AWS Continuum. This report covers its pentest, design, code, and threat-model workflows, not the separate gated-preview Continuum for code vulnerabilities product. [S02] [S04]

### G02 — GA is capability-specific

The 31 March 2026 GA announcement establishes on-demand pentesting. Pricing documentation continues to label code review, design review, and threat modeling preview; the CI/CD tutorial explicitly labels its integration preview. [S03] [S05] [S29]

### G03 — Authorized testing can still have side effects

Use non-production data and test-only credentials. Scope exclusions and network controls reduce exposure but do not establish that every business-logic side effect is impossible. [S10] [S09]

### G04 — Coverage and certainty are separate from completion

AI-assisted testing does not guarantee discovery of every critical path. A completed or work-capped run and a Resolved revalidation status each require interpretation against scope and evidence. [S11] [S08] [S14]

### G05 — Documentation conflict: older FAQ versus newer procedures

The security FAQ still says there are no public APIs or CI/CD integrations. The dedicated CI/CD procedure and preview tutorial document an integration, and the differential-review page documents an API path. This report uses the specific procedures for those workflows and retains the preview and setup restrictions. [S11] [S28] [S29] [S27]

### G06 — Region and inference must be checked separately

Consult current regional availability and the feature-specific cross-region inference table before sending source or application data. Geographic and global routing differ, with feature exceptions; do not assume single-region processing or Zurich-local residency. Regional inference listings are not a universal feature-availability promise. [S30] [S10]

### G07 — Evidence export is not certification

PDF reports can support an assurance workflow but do not constitute certification or replace independently required assessments. Review audience, confidentiality, and the report’s documented limitations. [S15]

### G08 — Costs and generated fixes need human controls

Task hours are cumulative active work; quotas are not budget caps. Repository remediation proposes changes for engineering review and should not bypass test, approval, or deployment procedures. [S05] [S13] [S25]

## Structured presentation transcript

Eight sections. Speaking notes are ready to present; demonstrations remain proposed and unexecuted.

### 01 — Position the agent correctly

**On-screen message:** Application-security assistance, not a universal security sign-off.

**Speaker transcript:**

The current documentation places AWS Security Agent under AWS Continuum. For this presentation, the core routine-use path is on-demand penetration testing of an application we are authorized to test. The report also covers code, design, threat modeling, and delivery integration, but labels their preview status explicitly. Do not transfer the pentesting GA label to those features or to the separate gated-preview Continuum vulnerability-management offering. Our operating model keeps security and engineering accountable for scope, evidence, remediation priority, and acceptance.

**Proposed demonstration — not executed:** Show the capability filter with preview excluded, then enable preview to explain the separate evaluation track.

**Official evidence:** [S04] [S02] [S03] [S05] [S29]

### 02 — Set a safe and meaningful test scope

**On-screen message:** Authorization, staging isolation, and access are prerequisites.

**Speaker transcript:**

Start from an application and a specific test purpose. Verify the target domain, identify an operator, and prepare a non-production environment without live customer data. Authentication and private-network access can make testing more representative, but also increase the reachable surface. Our recommendation is to use realistic test identities and review every supporting domain after login. Check that excluded administrative and destructive paths remain excluded. Technical domain verification alone does not settle whether the organization is authorized to test every dependency involved in a user journey.

**Proposed demonstration — not executed:** Review a proposed staging test configuration and reject any credential or route that reaches production.

**Official evidence:** [S07] [S09] [S10] [S08]

### 03 — Supply context and observe the run

**On-screen message:** Measure coverage and task effort, not just a completion badge.

**Speaker transcript:**

Source and architecture context can make a test more relevant to the deployed application. Ensure the branch, API description, and target build agree. The agent’s exact exploration develops during execution, so the operator needs logs and a stop criterion rather than a promise of a fully predetermined sequence. Limit work using the available task-hour control and monitor application health separately. Task hours and elapsed time measure different things. When a run stops or reaches a limit, inspect what it actually tested and retain explicit gaps for the next assessment.

**Proposed demonstration — not executed:** Compare attached source with the deployed commit, then inspect a sample run’s log, task-hours field, and coverage evidence.

**Official evidence:** [S08] [S05] [S11]

### 04 — Triage and route verified engineering work

**On-screen message:** Finding evidence and business impact determine the next step.

**Speaker transcript:**

Use severity as a starting point, then review affected behavior, confidence, and supporting evidence. Be aware of hidden or filtered results. A reproduction artifact can be useful when available, but no script should be run outside the authorized environment without review. After validating a finding, create a clear remediation item with the original evidence attached. Jira export is a handoff mechanism, not a replacement for the team’s ownership process. Avoid duplicate tickets and keep the link to the tested application version.

**Proposed demonstration — not executed:** Walk through one reviewed finding, its evidence and filters, then the fields required in its Jira issue.

**Official evidence:** [S12] [S16] [S10]

### 05 — Close the loop on a fix

**On-screen message:** A proposed patch, a deployment, and a revalidation are distinct events.

**Speaker transcript:**

When repository remediation is enabled, the agent can propose a finding-specific code change. An engineer must still review its logic and run the project’s checks. After the accepted fix is deployed to the tested environment, a focused revalidation can assess whether the existing finding is reproduced. That result is narrower than a new full assessment. Our closure record should include the original finding, patch revision, deployed revision, verification evidence, and any residual uncertainty. Larger behavioral changes justify a broader assessment rather than relying only on a targeted retest.

**Proposed demonstration — not executed:** Trace one finding through a proposed PR, normal review, staging deployment, and a separate revalidation job.

**Official evidence:** [S13] [S25] [S14] [S10]

### 06 — Evaluate preview design and code workflows deliberately

**On-screen message:** Preview feedback supplements—not replaces—established review.

**Speaker transcript:**

Design reviews use organizational requirements; threat models examine architecture and threats; source reviews inspect code. They answer different questions. A team should define input quality and review ownership before enabling any of them broadly. For repository-triggered feedback, verify that a scan actually ran on the intended revision. An absent comment may indicate that a filter excluded the change. The IDE path is cloud-backed and uploads source, so data handling and first-use provisioning need approval. Treat imported requirements and proposed fixes as reviewable work, not automatic policy truth.

**Proposed demonstration — not executed:** Compare a design finding, a threat-model assumption, and a code finding; show the evidence needed to validate each.

**Official evidence:** [S17] [S18] [S20] [S24] [S26] [S05]

### 07 — Understand the exact meaning of a delivery gate

**On-screen message:** A scoped-out pass is not a completed dynamic security test.

**Speaker transcript:**

The documented preview CI/CD integration operates after deployment to a testable target. Its result depends on change scoping and the configured gate behavior. A pipeline can pass because the change was out of scope without executing dynamic testing, while an unresolved scope decision requires a deliberate policy. Authentication uses configured trust and permissions; the pipeline must also manage the server-side job lifecycle. Our recommendation is to test dry-run, failure, scope-conflict, and cancellation cases before allowing a gate to influence promotion decisions.

**Proposed demonstration — not executed:** Review four hypothetical outcomes—tested, finding detected, scoped out, and scope conflict—and define their promotion and cleanup behavior.

**Official evidence:** [S28] [S29]

### 08 — Use evidence to decide whether to expand

**On-screen message:** Count validated findings and reviewer effort, not security claims.

**Speaker transcript:**

The proposed pilot evaluates whether this workflow produces actionable engineering work at an acceptable cost and review burden. Record confirmed findings, rejected findings, uncovered critical paths, accepted fixes, revalidation outcomes, and task expenditure. No productivity or detection-rate result is assumed. Export reports when useful for handoff, but retain their scope and qualification. Expansion should depend on repeated evidence that the test configuration, reviewers, and remediation process work together. Keep preview adoption separate from the baseline so a useful established workflow is not blocked by an immature optional integration.

**Proposed demonstration — not executed:** Review the pilot evidence register and distinguish assessed scope, verified fixes, outstanding gaps, and items requiring professional review.

**Official evidence:** [S15] [S05] [S12] [S14]

## Recommended 30-day pilot

This is an adoption experiment, not a product feature or a vendor performance promise.

### Days 1–3 — Authorize and isolate

Select one owned staging application, approve scope and test identities, establish an Agent Space, and nominate security and service owners.

### Days 4–7 — Establish a baseline

Run a bounded assessment with matching source/context. Record task hours, tested paths, health impact, and evidence quality.

### Days 8–14 — Triage and repair

Review findings, export accepted work to the existing backlog, and trial one repository fix proposal under normal review controls.

### Days 15–21 — Revalidate and compare

Deploy accepted fixes to staging and revalidate the original findings. Repeat a comparable assessment where broader changes justify it.

### Days 22–30 — Optional preview track

Only after separate approval, evaluate one design/code or pipeline-preview workflow. Decide expansion from verified outcomes, costs, and uncovered scope.

### Recommended measures

Recommended measures: independently confirmed findings; reviewer time; false-positive/rework rate; critical-path coverage gaps; accepted fixes; reproducibility after deployment; and task hours per comparable scope. These are pilot measures, not measured results or vendor detection guarantees.

## Official source register

All sources checked on 20 October 2026. Recheck current documentation before enabling a workflow.

### S01 — AWS frontier agents

**Type:** Official product page  
**Relevant sections:** Meet the frontier agents

Portfolio membership.

[Open official source](https://aws.amazon.com/ai/frontier-agents/)

### S02 — AWS Continuum

**Type:** Official product page  
**Relevant sections:** Frontier agent; capability availability

Current umbrella naming and separation from gated-preview code-vulnerability management.

[Open official source](https://aws.amazon.com/continuum/)

### S03 — On-demand penetration testing generally available

**Type:** Official release announcement  
**Relevant sections:** Announcement dated 31 March 2026

Establishes GA for on-demand penetration testing, not every related feature.

[Open official source](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

### S04 — What is AWS Security Agent?

**Type:** Product documentation  
**Relevant sections:** Key capabilities

Current product naming and lifecycle scope.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

### S05 — Pricing and billing

**Type:** Product documentation  
**Relevant sections:** Billable capabilities; task hours; quotas

Preview status for code/design/threat-model features; task time differs from elapsed time.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

### S06 — Set up AWS Security Agent

**Type:** Product documentation  
**Relevant sections:** Access methods; first Agent Space

IAM Identity Center or IAM-only access and administrative setup.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/setup-security-agent.html)

### S07 — Enable a target domain

**Type:** Product documentation  
**Relevant sections:** Verification methods

Domain verification and private-VPC verification distinctions.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html)

### S08 — Create a penetration test

**Type:** Product documentation  
**Relevant sections:** Scope; VPC; context; maximum task hours

Configuration and execution boundaries.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

### S09 — Provide testing credentials

**Type:** Product documentation  
**Relevant sections:** Authentication configuration

Authenticated access setup; credentials must be scoped to the test.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

### S10 — Security best practices

**Type:** Product documentation  
**Relevant sections:** Non-production testing; validation; cross-region inference

Side effects, generated-code review, and processing-location considerations.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

### S11 — Security considerations and FAQs

**Type:** Product documentation  
**Relevant sections:** Coverage; dynamic test plan; operational impact

Used for coverage and monitoring caveats. Older no-API/no-CI statements conflict with newer procedure pages.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)

### S12 — Review penetration-test findings

**Type:** Product documentation  
**Relevant sections:** Findings; logs; evidence; verification scripts

Finding confidence and evidence availability.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

### S13 — Enable finding remediation

**Type:** Product documentation  
**Relevant sections:** Prerequisites; enable per repository

GitHub-based user-requested fixes require repository configuration.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html)

### S14 — Revalidate findings

**Type:** Product documentation  
**Relevant sections:** Prerequisites; interpretation of results

Focused checks on existing findings, not new-vulnerability discovery.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

### S15 — Export a penetration-test report

**Type:** Product documentation  
**Relevant sections:** Report options; compliance limitations

PDF evidence exports are not compliance certification.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)

### S16 — Create Jira issues for findings

**Type:** Product documentation  
**Relevant sections:** Issue creation; unlinking

Connected project must permit Task issue type; unlinking does not delete.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html)

### S17 — Perform a design review

**Type:** Product documentation  
**Relevant sections:** Upload and review

Design documents evaluated against configured requirements.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-design-review.html)

### S18 — Security requirements

**Type:** Product documentation  
**Relevant sections:** Requirement packs; enabled requirements

Shared organizational review criteria.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

### S19 — Import security requirements

**Type:** Product documentation  
**Relevant sections:** Generate and review requirements

Document-derived requirements need administrative review.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

### S20 — Perform threat modeling

**Type:** Product documentation  
**Relevant sections:** Scope and context; model output

STRIDE threats and architecture context; reusable runs.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-threat-model.html)

### S21 — Perform a full code review

**Type:** Product documentation  
**Relevant sections:** Source configuration; scan creation

Repository or S3-hosted source review.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)

### S22 — Review code-scan findings

**Type:** Product documentation  
**Relevant sections:** Finding details; statuses

Location, severity, risk, and remediation context.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html)

### S23 — Review findings in pull requests

**Type:** Product documentation  
**Relevant sections:** PR/MR review findings

Provider-specific code-change feedback.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

### S24 — Configure code-review triggers

**Type:** Product documentation  
**Relevant sections:** Filter groups; matching behavior

No matching trigger means no review comment; remediation settings are separate.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html)

### S25 — Remediate code-review findings

**Type:** Product documentation  
**Relevant sections:** Source-specific remediation

PR/MR versus downloadable diff; public-provider restrictions.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)

### S26 — Code review from an IDE

**Type:** Product documentation  
**Relevant sections:** MCP/Power setup; first-use resources

Source is uploaded to S3/service infrastructure; initial IAM provisioning matters.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/code-review-ide-integration.html)

### S27 — Run a differential code scan with S3

**Type:** Product documentation  
**Relevant sections:** Source and diff inputs; API job

Full source context and unified diff supplied to a review API.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html)

### S28 — Run penetration tests from CI/CD

**Type:** Product documentation  
**Relevant sections:** Post-deployment gate; scoping; OIDC; cancellation

Scoped-out and scope-conflict outcomes; server job lifecycle.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

### S29 — GitHub Actions scoped-pentest tutorial

**Type:** Product documentation  
**Relevant sections:** Public preview notice; post-deployment setup

Explicit preview status for the pipeline integration.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html)

### S30 — Resilience and regional availability

**Type:** Product documentation  
**Relevant sections:** Regional availability; inference

Regional access and cross-region inference are separate checks.

[Open official source](https://docs.aws.amazon.com/securityagent/latest/userguide/resilience.html)

---

### Reference links

[S01]: https://aws.amazon.com/ai/frontier-agents/ "AWS frontier agents"

[S02]: https://aws.amazon.com/continuum/ "AWS Continuum"

[S03]: https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/ "On-demand penetration testing generally available"

[S04]: https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html "What is AWS Security Agent?"

[S05]: https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html "Pricing and billing"

[S06]: https://docs.aws.amazon.com/securityagent/latest/userguide/setup-security-agent.html "Set up AWS Security Agent"

[S07]: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html "Enable a target domain"

[S08]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html "Create a penetration test"

[S09]: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html "Provide testing credentials"

[S10]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html "Security best practices"

[S11]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html "Security considerations and FAQs"

[S12]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html "Review penetration-test findings"

[S13]: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html "Enable finding remediation"

[S14]: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html "Revalidate findings"

[S15]: https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html "Export a penetration-test report"

[S16]: https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html "Create Jira issues for findings"

[S17]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-design-review.html "Perform a design review"

[S18]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html "Security requirements"

[S19]: https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html "Import security requirements"

[S20]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-threat-model.html "Perform threat modeling"

[S21]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html "Perform a full code review"

[S22]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html "Review code-scan findings"

[S23]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html "Review findings in pull requests"

[S24]: https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html "Configure code-review triggers"

[S25]: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html "Remediate code-review findings"

[S26]: https://docs.aws.amazon.com/securityagent/latest/userguide/code-review-ide-integration.html "Code review from an IDE"

[S27]: https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html "Run a differential code scan with S3"

[S28]: https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html "Run penetration tests from CI/CD"

[S29]: https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html "GitHub Actions scoped-pentest tutorial"

[S30]: https://docs.aws.amazon.com/securityagent/latest/userguide/resilience.html "Resilience and regional availability"