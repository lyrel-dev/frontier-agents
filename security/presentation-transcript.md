# AWS Security Agent: presentation transcript

Total 33:30, including 10:00 prepared-result demonstrations. No service-completion-time guarantee. Questions, preparation and live setup are additional.

## 1. Match the assessment to the evidence required

0:00–1:00; allocation 1:00

A design statement, a source finding and a reproduced runtime exploit answer different questions.

| Design | Source | Runtime |
|---|---|---|
| Are required controls described? | Does this code contain a security issue? | Can this issue be reproduced on this target? |

### Presenter notes

Introduce the assessment boundaries rather than a broad security promise. The requested product name is retained; the current documentation identifies it as part of AWS Continuum. Code review, design review and threat modeling are preview. Penetration testing has a separate availability and billing model. The presentation concentrates on selecting the right operation and interpreting its result.

Official documentation: [What is AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html) · [Review design findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


## 2. Four groups of functions

1:00–3:00; allocation 2:00

Separate analysis, runtime testing, repair proposals and evidence management.

| Group | Operations | Primary result |
|---|---|---|
| Design and threats | Requirement evaluation; threat modeling | Control assessment or modeled attack scenario |
| Source assessment | Full scan; diff scan; simulated validation | Code finding with separate validation state |
| Application testing | Scoped penetration test; selected revalidation | Observed test evidence against a target |
| Remediation/evidence | Proposed code repair; triage/export | Reviewable patch or assessment record |

### Presenter notes

A full scan and a diff scan differ in scope, not in whether the result is automatically true. Simulated validation adds an attempted exploit in a constructed environment; it is not a production test. Revalidation repeats selected previous findings and does not discover unrelated issues. A proposed patch and a report are outputs requiring review, not proof that the vulnerability was removed.

Official documentation: [What is AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html) · [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html) · [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)


## 3. Requirement review is not threat modeling

3:00–5:30; allocation 2:30

Use a fixed criterion to evaluate a control; use a threat model to reason about attacker paths.

|  | Design review | Threat model |
|---|---|---|
| Input | Design documents + enabled requirements | Scope documents, source context or both |
| Question | Is the applicable control demonstrated? | What can cross this trust boundary? |
| Output | Compliant / non-compliant / insufficient / N/A | Assets, flows and STRIDE-classified threats |
| Review focus | Applicability and missing evidence | Attacker prerequisites and architecture accuracy |

### Presenter notes

Use an authorization example. A design may state that object access is restricted to the owner but omit where the decision is enforced. Requirement review should expose the evidence gap. Threat modeling asks how a different identity could reach the object and which trust boundary would be crossed. Neither proves an exploit succeeds. Review the architecture model before prioritizing its generated threats.

Official documentation: [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html) · [Review design findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-design-findings.html) · [Create a threat model](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html) · [Review threat-model findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-threat-model-findings.html)


## 4. Requirement packs are controlled inputs

5:30–7:30; allocation 2:00

Generated requirements must be reviewed before they govern new assessments.

| Define | Review | Enable | Version |
|---|---|---|---|
| Applicability, compliant conditions and remediation | Edit imported or generated criteria | Enable the pack for new design/code reviews | Record the criteria used for each run |

Uploading replacement documents regenerates the entire custom pack, including manual requirements.

### Presenter notes

The control is more specific than upload our policy. Give each requirement an observable meaning and a clear non-applicability condition. Packs are shared across Agent Spaces, so an edit can affect more than the current review. Existing results are not recomputed when a pack changes. A framework-oriented pack helps identify relevant requirements; it does not certify compliance.

Official documentation: [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html) · [Generate requirements from documents](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)


## 5. Choose full-source or differential analysis intentionally

7:30–10:00; allocation 2:30

A changed-code review still needs surrounding source context.

|  | Full code review | Differential code review |
|---|---|---|
| Input | Repository branch or complete S3 source ZIP | PR change or source ZIP plus unified diff |
| Scope | Submitted codebase | Changed code interpreted in context |
| Preflight | Access and environment must succeed | Revision, artifact and trigger must match |
| No findings means… | No returned findings for that completed scope | Not a baseline assurance for unchanged code |

### Presenter notes

A skipped trigger, a failed preflight and a completed clean review must be visibly distinct. Before reviewing a finding, identify the exact source revision. For a programmatic diff job, a patch alone does not provide the source context the service expects. For PR reviews, verify the configured publication permissions and the branch or label filters rather than inferring success from an absence of comments.

Official documentation: [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html) · [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Review code findings in GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)


## 6. Simulated validation has four different outcomes

10:00–12:30; allocation 2:30

Do not collapse non-reproduction, failed execution and no attempt into 'safe'.

| Result | What it supports | Next question |
|---|---|---|
| Confirmed | Exploit succeeded in the simulated environment | Does the evidence match the affected path? |
| Not reproduced | Attempt did not reproduce under these conditions | Were dependencies and authentication representative? |
| Validation failed | Attempt was inconclusive due to an error | What failed in execution? |
| Not validated | No completed validation for this finding | Is another test required? |

### Presenter notes

State the environment prerequisite before showing results: the application must fit the supported simulated setup. A private dependency or startup failure is not evidence against a source finding. Conversely, a confirmed exploit should still be examined for its actual path and conditions. The result is stronger than a bare static assertion but remains bounded by the environment in which it was produced.

Official documentation: [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Perform a full code review](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-code-review-scan.html)


## 7. A runtime test needs four independent permissions

12:30–15:00; allocation 2:30

Control of the domain does not grant unrestricted application access or eliminate side effects.

| Target | Network | Identity | Test scope |
|---|---|---|---|
| Verified, associated domain and authorized environment | Reachable endpoint, configured private path if needed | Dedicated credentials and intended role | Included paths, exclusions, risk classes and limits |

Use disposable staging data and disable real external effects before exploratory traffic.

### Presenter notes

Explain which problem each configuration solves. A verified domain can still be unreachable. A reachable login page does not prove authenticated endpoints are exercised. A powerful test account can also produce misleading authorization coverage if the real risk concerns a less privileged user. Match identities and data to the specific behavior the team needs to assess and monitor target-side logs.

Official documentation: [Verify a test domain](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-test-domain.html) · [Enable penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html) · [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html) · [Provide test credentials](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html)


## 8. Retesting a finding is not a new penetration test

15:00–17:30; allocation 2:30

Deploy the fix to the original target before interpreting a revalidation result.

| Operation | Examines | Preserves |
|---|---|---|
| Full penetration test | Selected risk surface of the application | Run tasks and newly discovered findings |
| Selected revalidation | Validation steps for existing findings | Original finding plus separate retest history |
| Independent regression | Team-defined allowed and denied behavior | Application test evidence for the patched build |

Resolved means not reproduced in that revalidation; it does not establish whole-application security.

### Presenter notes

Use the same target and current valid credentials. Check the build identity at the target rather than the branch containing the fix. A revalidation can be narrowly useful after a small repair, but a wider change may introduce other paths that only a broader test or application regression suite covers. Retain the original evidence rather than replacing it with a new status label.

Official documentation: [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)


## 9. Do not confuse four finding attributes

17:30–19:30; allocation 2:00

Each attribute answers a different question.

| Attribute | Question | Not equivalent to |
|---|---|---|
| Severity | How serious could the impact be? | Agent certainty |
| Confidence | How confident is the agent in this finding? | Demonstrated exploitation |
| Validation | Was an exploit attempt made and reproduced? | Workflow disposition |
| Status / annotation | How has the organization handled it? | Verified removal of the defect |

### Presenter notes

Use one high-impact, unvalidated item and one lower-impact confirmed item. Neither can be prioritized on a single attribute alone. Inspect default filters before reporting totals. A report can include organization-authored notes; they must remain distinguishable from the service's assessment. Manual risk acceptance and a fixed vulnerability are different operational outcomes.

Official documentation: [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


## 10. A repair proposal needs behavior tests

19:30–21:30; allocation 2:00

Generating the diff is not the completion criterion.

| Inspect | Test | Deploy | Reassess |
|---|---|---|---|
| Source path, intended rule and proposed patch | Allowed behavior and denied behavior | Normal owner-approved delivery process | Code rereview or target revalidation as appropriate |

A patch that blocks legitimate access can remove the exploit and still be an unacceptable fix.

### Presenter notes

The source connection may support a PR or a downloadable diff depending on the route. Do not generalize that into automatic merge or deployment. The developer must preserve intended behavior while enforcing the control. For an ownership check, test both the owner and a different identity. The original assessment type determines what evidence is needed after the repair.

Official documentation: [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)


## 11. Demonstration: an authorization change before merge

21:30–26:30; allocation 5:00

Inspect revision, trigger, source path and validation state before judging the patch.

| Minutes | Action |
|---|---|
| 1 | Show the authorization rule, exact diff and intended allowed/denied cases. |
| 1 | Confirm the prepared review's revision, preflight and trigger behavior. |
| 1 | Trace one finding and identify its validation state. |
| 1 | Review a proposed patch against both allowed and denied tests. |
| 1 | State the merge decision and remaining runtime evidence gap. |

Fallback: Use a prepared, permission-cleared PR, finding and test output. Label the data as a prepared example; do not simulate a successful live scan.

### Presenter notes

Use the five one-minute steps in the procedure. Prepare a permission-cleared PR, its review record and positive/negative test output. This is a result-reading and decision exercise, not a promise that a scan completes in five minutes. The presenter must show why a finding is accepted, rejected or left unresolved rather than presenting an unexamined agent recommendation.

Official documentation: [Run a differential scan from S3](https://docs.aws.amazon.com/securityagent/latest/userguide/run-diff-scan-s3.html) · [Configure code-review triggers](https://docs.aws.amazon.com/securityagent/latest/userguide/configure-code-review-triggers.html) · [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Remediate code-review findings](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-code-scan-findings.html)


## 12. Demonstration: verify a deployed fix

26:30–31:30; allocation 5:00

A valid non-reproduction requires the patched build, functioning authentication and the intended endpoint.

| Minutes | Action |
|---|---|
| 1 | Show original finding, authorized target and deployed build identity. |
| 1 | Explain the test identities and safe data boundary. |
| 1 | Open a prepared revalidation job and inspect execution evidence. |
| 1 | Contrast Active, valid non-reproduction and authentication failure. |
| 1 | Show independent regression results and the narrowly scoped conclusion. |

Fallback: Walk through prepared original and retest evidence. Do not start an unbounded penetration test merely to fill a five-minute demonstration slot.

### Presenter notes

Show the original finding, the patched target and a prepared revalidation run. Contrast an active vulnerability with valid non-reproduction and with an authentication failure. Then show the application owner's allowed/denied regression results. The conclusion should name the specific finding and build, not state that the system is secure. Use prepared evidence if live prerequisites are absent.

Official documentation: [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Security guidance and testing boundaries](https://docs.aws.amazon.com/securityagent/latest/userguide/security-guidance.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)


## 13. An assessment record must preserve its boundary

31:30–33:30; allocation 2:00

Make the scope of a conclusion visible to the next engineer.

| Retain | Reason | Reject this shortcut |
|---|---|---|
| Revision/build, target and run ID | Identify what was examined | 'Latest scan passed' |
| Credentials/roles and executed tasks | Identify what was reachable | 'All endpoints were covered' |
| Validation state and evidence | Separate proof from hypothesis | 'Not reproduced means false positive' |
| Filters, gaps and annotations | Explain selected and omitted findings | 'PDF report means certified' |

### Presenter notes

The output should allow another engineer to understand what was tested without reconstructing the session. Report filters, task limits and missing access are part of the assessment boundary. This is a proposed record-keeping standard, not a claim that a generated report is sufficient for every audit. Questions and live account setup are outside the timed presentation.

Official documentation: [Code-review findings and validation states](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-scan-findings.html) · [Revalidate penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) · [Export penetration-test reports](https://docs.aws.amazon.com/securityagent/latest/userguide/export-penetration-report.html)

