# AWS Security Agent — presentation transcript

30 minutes including 8 minutes of demonstrations. Questions and breaks are additional. Demo budgets are walkthrough allocations, not agent completion guarantees.


## 01. AWS Security Agent

**00:00–00:45 · 00:45 allocated**

**Takeaway:** Application-security evidence from design review to deployed-fix revalidation.

This deck remains scoped to the application-security capabilities in the original report. On-demand penetration testing is generally available; design review, code review, threat modeling and CI/CD integration have their own preview status. The demonstration uses an authorized staging application and a prepared evidence package, not an unapproved real-world target.

[S04 — What is AWS Security Agent?](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

[S03 — On-demand penetration testing generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)


## 02. Feature availability differs by security workflow

**00:45–02:00 · 01:15 allocated**

**Takeaway:** Use the feature’s own maturity and execution boundary.

The lifecycle view explains why a single “security agent” label is insufficient. A design review examines documents, a threat model proposes attack scenarios, source review examines code, and penetration testing exercises a running target. They produce different evidence and have different potential side effects. Availability is also feature-specific, so an organization can adopt the GA testing path without making the same approval decision for every preview capability.

[S03 — On-demand penetration testing generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

[S28 — Run penetration tests from CI/CD](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

[S29 — GitHub Actions scoped-pentest tutorial](https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html)


## 03. Use case · assess a tenant-isolation control

**02:00–03:15 · 01:15 allocated**

**Takeaway:** The unit of success is an accepted finding and verified repair—not a severity count.

The illustrative application has tenant-specific administration endpoints. The team wants to know whether an ordinary test identity can affect another tenant. No actual vulnerability is asserted here. Define dedicated tenants and identities, use synthetic data and keep all actions within the authorized staging scope. A useful result contains evidence and a clear affected path; closure requires a deployed fix and a focused reassessment.

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


## 04. Specify authorization and target effects before testing

**03:15–04:45 · 01:30 allocated**

**Takeaway:** Domain verification does not authorize every reachable dependency.

Domain verification is a product prerequisite, not a substitute for organizational authorization. Scope must cover the target, identities and any third-party or downstream services that might be exercised. A sandboxed worker can still mutate the application it reaches. Isolate the target data and disable payment, notification and other irreversible side effects. Assign a human stop owner with independent visibility of target health.

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[S09 — Provide testing credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)


## 05. Choose test scope and supply current context

**04:45–06:00 · 01:15 allocated**

**Takeaway:** Acceptance: context and credentials match the deployed version under test.

Choose the risk model deliberately: the default Web application scope covers web and API risks; Gen AI application focuses on LLM-backed surfaces. Gen AI scope uses a fixed set of risk types rather than the web scope’s risk exclusions. Match source and API context to the deployed revision. Test dedicated credentials before the assessment and review discovered domains. Target domains may be tested, accessible domains support navigation without attack, and out-of-scope domains must not be accessed. Private deployments require the configured VPC path.

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[S09 — Provide testing credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)


## 06. Configure run limits and inspect test effects

**06:00–07:15 · 01:15 allocated**

**Takeaway:** Acceptance: task hours are not wall-clock minutes; the operator owns the stop decision.

Task hours measure cumulative agent work, including parallel activity; they are not wall-clock minutes. A configured maximum task-hours limit stops work and preserves findings, whereas a service quota is not the same spending control. Reaching the run limit can still yield a Completed status, so inspect coverage rather than treating that label as a complete assessment. Monitor target health and define a stop owner before starting. The presentation reviews a prepared run rather than waiting for a full test.

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)


## 07. Demo · authorized staging assessment

**07:15–15:15 · 08:00 allocated**

**Takeaway:** Inspect a safe configuration, an active run view and one evidence-backed finding.

The eight-minute slot cannot be treated as a guarantee of a complete penetration test. Walk through setup and a completed result rather than waiting for a new scan. A prompt asking the agent to stop at a health threshold is not an independent circuit breaker; the operator and environment controls enforce the safety plan. Do not execute reproduction material against any target outside the authorized scope.

**Preflight:** Prepare a disposable staging app, independent health monitoring, a completed test and a named stop owner.

```text

Prepare the approved staging assessment with dedicated test accounts, explicit target and network scope, and the agreed work budget. Exclude payment and notification side effects through environment controls. The operator will monitor health and stop the job if the agreed threshold is crossed.

```

- 01:00 — **Verify authorization:** Show target ownership, test window and dedicated identities.

- 01:30 — **Inspect context:** Match source/deployment version, credentials and private reachability.

- 01:30 — **Inspect limits:** Show work budget, exclusions and the stop procedure.

- 02:00 — **Observe a run:** Use the prepared run view; correlate logs with target health.

- 02:00 — **Review one finding:** Read impact, reproduction evidence, coverage and the next engineering action.

**Success:** An authorized, bounded run and one inspectable evidence package; no claim of complete coverage.

**Fallback:** Use a sanitized completed run if setup or job latency prevents a live view. Label illustrative findings clearly.

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[S09 — Provide testing credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)


## 08. Examine finding evidence, impact and confidence

**15:15–16:45 · 01:30 allocated**

**Takeaway:** Severity without impact, confidence and coverage is not enough for a decision.

A finding should let a reviewer understand the affected behavior, the identity used, the observed result and the conditions needed to reproduce it. Inspect the action trace and the reported impact. Coverage matters: a clean result on an authenticated path does not establish that all other paths were tested. Accept or reject the finding on its evidence and business context, not on the severity label alone.

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)


## 09. A remediation proposal requires review and retesting

**16:45–18:15 · 01:30 allocated**

**Takeaway:** Acceptance: provider, repository visibility and source type determine delivery; the team reviews every fix.

Automatic or requested remediation creates code for review. Delivery depends on the source and provider: a connected private repository can receive a pull or merge request, while an S3 source can receive a diff. Public repository handling has disclosure restrictions, so do not promise a universal remediation PR. Test the change, preserve unrelated behavior and use normal deployment controls. A generated patch does not establish that the vulnerability is resolved.

[S13 — Enable finding remediation](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html)

[S25 — Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)

[S32 — Remediate a penetration-test finding](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)


## 10. Revalidate after the fix is deployed

**18:15–19:30 · 01:15 allocated**

**Takeaway:** Acceptance: “not reproduced” concerns this finding and this run—not a complete security certification.

Revalidation is a focused reassessment, not a new broad discovery scan. The fix must already be deployed to the original target for the result to be meaningful. The result does not overwrite the historical finding. Preserve the original evidence and the linked revalidation attempt. Broad architectural or application changes may justify a full new penetration test instead of relying only on selected findings.

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


## 11. Export evidence and hand work to the right owner

**19:30–20:30 · 01:00 allocated**

**Takeaway:** Sharing a report or ticket must preserve scope, revision and finding identity.

Generate the report from the selected penetration-test run and choose the severity, confidence, status and finding-type filters. Optional compliance-oriented sections and annotations preserve useful context, but do not establish certification. A completed run and an interim export have different evidence boundaries. Jira handoff requires a configured supported project. Keep finding identity, remediation links and reassessment status attached to the work item; ticket creation is not closure. Protect vulnerability details according to the intended audience.

[S15 — Export a penetration-test report](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)

[S16 — Create Jira issues for findings](https://docs.aws.amazon.com/securityagent/latest/userguide/export-findings-to-issue-tracker.html)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


## 12. Design review applies reusable requirements

**20:30–21:45 · 01:15 allocated**

**Takeaway:** Acceptance: review requirements and input assumptions before interpreting a finding.

Security requirements make the review specific to the organization, such as approved authentication patterns or data-access expectations. Treat them as review criteria rather than an infrastructure enforcement policy. A design assessment is only as complete as its inputs; missing interfaces and trust boundaries should become explicit questions. This capability remains a separately evaluated preview workflow.

[S17 — Perform a design review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-design-review.html)

[S18 — Security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)


## 13. Threat modeling connects design and code context

**21:45–22:45 · 01:00 allocated**

**Takeaway:** Acceptance: validate the agent’s system model before accepting its threat analysis.

A threat model is useful when the team recognizes its assets, data flows and trust boundaries. Provide both design scope and current source when that helps focus the assessment. The reviewer should correct the system overview before treating the resulting threats as exhaustive. Keep threat-model recommendations distinct from observed exploitable findings in a running penetration test.

[S31 — Threat modeling quickstart](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)


## 14. Code review has several entry points

**22:45–24:15 · 01:30 allocated**

**Takeaway:** Full-repository, change review and remediation share context—not identical triggers.

Repository review, change-triggered review and remediation answer different questions. PR/MR trigger filters can use target branches, events and provider-supported labels; filter groups replace the default trigger. Review comments and remediation are separate capabilities. The documented manual review comment is @AWS-Continuum-Pentesting review. Do not copy another agent’s review command or assume provider parity. Inspect findings, supported source paths and normal CI evidence before accepting a proposed repair. The code-review workflow remains preview.

[S21 — Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)

[S24 — Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html)

[S25 — Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)


## 15. Submit and verify a differential source review

**24:15–25:30 · 01:15 allocated**

**Takeaway:** A build submission calls a service; retain the source revision and scan evidence.

The documented S3 differential-review workflow uses uploaded source and diff context. Record the base and head revisions, approved bucket and role, scan identifier and returned findings. Review the source payload for secrets and unnecessary content before submission. A scan result is not itself authorization to merge or deploy; the promotion rule is a separately proposed team control.

[S27 — Run a differential code scan with S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html)


## 16. A passing delivery gate has limited assessment scope

**25:30–27:00 · 01:30 allocated**

**Takeaway:** Read scope, errors and baseline behavior—not just the pipeline color.

The pipeline integration is a post-deployment test, not a pre-merge code scan. It assesses the configured deployed change. A scoped-out result can pass without exercising a new attack surface, and infrastructure errors can be configured fail-open. The documented defaults therefore need explicit review. A passing run can also advance the baseline, so tightening the policy later does not necessarily revisit earlier accepted commits. This is a reason to verify the exact gate contract before using it for production sign-off.

[S28 — Run penetration tests from CI/CD](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

[S29 — GitHub Actions scoped-pentest tutorial](https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html)


## 17. Pilot one authorized finding-to-revalidation cycle

**27:00–28:30 · 01:30 allocated**

**Takeaway:** Assess one authorized target, review a finding and revalidate the repaired application.

Use one owned application to establish the entire operating loop. Check Region and inference behavior separately from feature availability. Measure confirmed findings, rejected or unsupported claims, reviewer effort, task consumption and successful fix closure. Track which critical paths were exercised and what remains unknown. Do not report a finding count as a security improvement unless the team has assessed and acted on it.

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[S30 — Resilience and regional availability](https://docs.aws.amazon.com/securityagent/latest/userguide/resilience.html)


## 18. Record authorization, findings and revalidation

**28:30–30:00 · 01:30 allocated**

**Takeaway:** Authorize the target. Inspect the evidence. Revalidate the deployed repair.

Close by distinguishing four things: a design concern, a source-code finding, an observed penetration-test finding and a verified repair. Each has a different evidence requirement. The team should adopt the first workflow it can operate safely and measure end to end, not every available preview at once. Questions come after the timed close. The feature crosswalk retains all 18 capability entries and their original qualifications for deeper reference.

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)
