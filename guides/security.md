# AWS Security Agent — configuration and operation

Engineering guide • documentation reviewed 22 October 2026

This guide describes application assessment configuration, authentication, execution, findings and evidence. The current guide identifies AWS Security Agent as part of AWS Continuum. On-demand penetration testing and the design, code, threat-model and pipeline paths have different availability. Confirm the selected feature and Region before adoption; a generally available penetration test does not make every assessment path generally available. [SS01] [SS02]

Official product behavior is cited. **Engineering procedures** and **synthetic exercises** below are authored recommendations, not additional service functions or records of a live test.

## 01. Product Functions and Resource Model

Define application scope, shared resources, assessment configurations, executions and findings.

### S-01 — Resources, scopes and functions

The product functions are application penetration testing, source-code analysis, design review, and threat modeling. Supporting platform capabilities include source connection, reusable configuration, authenticated/private access, requirement management, run observation, remediation and finding revalidation. Do not equate an entire assessment with a single hidden learning mechanism. [SS01] [SS03]

```text
Account / organization resources
  ├─ registered source integrations
  ├─ security requirement packs
  └─ identity configuration
              ↓ connect / assign / enable
Application Agent Space
  ├─ repositories, documents, user access, service settings
  ├─ penetration-test configuration → runs → findings → revalidation jobs
  ├─ code-review configuration → full scans / change-triggered reviews
  ├─ threat-model configuration → runs and model results
  └─ one-off design reviews → clone when a new assessment is needed
```

Registration makes an integration available; connecting a repository selects it for a space; enabling the assessment configures its use. These are separate actions. Requirements are shared resources, so the application boundary is not an isolation claim for every object. [SS03]

| Capability group | Resources and operators | Canonical sections |
|---|---|---|
| Identity and sources | Administrator, operator, Agent Space, integration, connected repository | S-02 |
| Target access | Verified domains, VPC route, target rules, credential definitions | S-03, S-M01 |
| Procedure reuse | Login Optimization and its learned skill | S-M02 |
| Assessment criteria | Managed/custom requirement packs and applicability | S-M03, S-M04 |
| Execution | Configuration, preflight, run, task-hour limit, logs | S-04 |
| Findings and repair | Finding evidence, proposed patch, deployed revision | S-05 |
| Targeted verification | Revalidation job and finding lineage | S-M05 |
| Data protection | Customer-managed key, branch key, encryption context, calling identity | S-M06 |
| Earlier feedback | Full/change-based code review, design review, threat model | S-06 |

## 02. Identity, Sources and Target Boundaries

Configure operator identity, repository sources, target rules and private access.

### S-02 — Set up identity and source access

The console is the administrative surface. The web app is the assessment workspace. IAM-based operators can enter through the console route; IAM Identity Center supports assigned users without requiring ordinary console access. Configure the intended operator identity, not just the administrator who creates the Agent Space. [SS04] [SS05]

**Configuration procedure:** create or select an Agent Space, establish the supported identity mode, register the source integration, connect the application's repositories, and enable the relevant feature. For a GitHub integration, verify whether the installation belongs to a personal account or organization and whether organization approval is required. A successful account registration does not mean a repository was connected. [SS03] [SS05] [SS06]

For code review, independently review the settings for vulnerability analysis, requirement evaluation, comments, and automatic remediation. Enabling one does not establish that all others are active. S3 can be a code source through its own supported configuration path; provider-specific integration instructions remain authoritative. [SS05]

**Engineering verification:** open the web app as the intended user, inspect the connected source and selected branch, and compare the source revision with the deployed test application. Record a known read and an expected denial. Do not place credentials in a repository or presentation to simplify the example.

### S-03 — Define the reachable surface before execution

Domain verification demonstrates control through a supported verification method, including DNS, HTTP or a private-VPC route. It is a technical prerequisite, not authorization for every downstream system the application can contact. Private testing additionally needs a supported VPC configuration, subnets, routing and security groups. [SS07]

The current penetration-test wizard separates three network rule classes. [SS08]

| Class | Intended behavior | Example in an authorized staging environment |
|---|---|---|
| Target | May be accessed and tested | `https://staging.example.test:8443` |
| Accessible | May be accessed to support the assessment, not attacked as a target | Approved login-provider or static-content endpoint |
| Out of scope | Must not be accessed; exclusions take precedence | A payment or production callback path |

These example names are illustrative, not running targets. Specify the complete scheme and nonstandard port when applicable. The current wizard supports explicit nonstandard ports; an older troubleshooting page states only 80/443. This guide follows the newer task-specific wizard and records the conflict rather than repeating the older restriction. [SS08] [SS06]

**Configuration procedure:** prepare the verified target and explicit exclusions; choose public or private connectivity; add representative test credentials; complete the network rules after authentication discovery; inspect suggested extra domains before accepting them. Keep essential login dependencies reachable without turning them into attack targets. Only execute against systems and effects that their owners have authorized. [SS07] [SS08]

**Expected confirmation:** the saved configuration identifies the target, network path, credential roles and exclusions. Draft configuration and successful authentication preflight are different states. Neither proves that a complete assessment has run.

## 03. Authentication, Criteria and Protection Mechanisms

Examine credential resolution, login reuse, requirement evaluation, regeneration and encryption.

### S-M01 — Credential resolution precedes application authentication

The service first obtains a credential and then follows login instructions to apply it to the application. A successful secret retrieval is not a successful application login. Current configuration requires a credential name, access URL, method and login prompt; **Save & Test** or **Test All** exercises authentication and exposes success/failure information. [SS09] [SS08]

| Strategy | Required dependency | Typical failure to distinguish |
|---|---|---|
| Direct test credential | Correct application identity and instructions | Wrong login URL, role or form flow |
| Secrets Manager | Same-account secret; service role with `secretsmanager:GetSecretValue` and `secretsmanager:DescribeSecret` | Access denied versus unusable secret format |
| IAM role | Registered role with correct service trust and limited permissions | Role assumption versus how the temporary credential is used by the target |
| Lambda | Same-account function, invoke permission, synchronous completion within 30 seconds | Invocation/timeout versus invalid returned credential |

The Lambda input includes `pentest_arn` and `actor_identifier`. Login instructions explain the returned credential's application use. The following original function illustrates the response boundary only; it is not a deployable credential provider and deliberately contains no real secret. [SS09]

```python
def handler(event, context):
    required = ("pentest_arn", "actor_identifier")
    if not all(event.get(k) for k in required):
        raise ValueError("Missing assessment identity")
    # Retrieve or mint a scoped TEST credential using your approved backend.
    # Return its actual fields in the format explained by the login prompt.
    raise NotImplementedError("Connect an authorized test-credential backend")
```

Use the official trust/policy examples for the selected strategy, restricted to the actual account, space and resource. This snippet is a contract example, not proof that a particular output schema is universal. [SS09]

The newer authentication guide includes TOTP and email MFA. Email MFA uses a generated forwarding address associated with the test credential; it is not general permission to forward a real user's inbox. SMS, push and hardware-key flows are not supported in the reviewed guidance. Older cached text says email MFA is unsupported; the newer indexed page is used here. [SS09]

**Proposed verification:** inspect both credential-test status and the authenticated application's identity/role. Test an intended protected route and an excluded route using approved test data. When access fails, capture which stage failed: source access, credential generation, login navigation, MFA, or authorization inside the application.

### S-M02 — Login Optimization retains a successful procedure

The first successful authentication navigation can produce a skill describing the login workflow. Later sessions within the run and subsequent runs reuse it. This is learned procedural navigation, not a general incident-memory store or customer-controlled model retraining. [SS09]

**Enablement:** add at least one credential, open **Additional configuration → Login optimization**, and inspect the default-enabled toggle. Disabling reuse preserves the skill; re-enabling permits reuse again. The documentation describes adaptation to changed login flows, but does not disclose a general selection algorithm or promise a particular speed improvement. [SS09]

**Proposed test:** use a staging login flow that the team controls. Retain first-login and later-login evidence, then make an authorized change to the test flow. Verify the actual authenticated role on every run. Without observable reuse evidence, distinguish a successful login from a proven reuse of the learned procedure.

### S-M03 — Requirement evaluation applies reviewed criteria

A requirement contains a name/description, applicability, compliance criteria and optional remediation guidance. Applicability can distinguish a violation from a case to which the requirement does not apply. Packs group requirements; managed and custom packs differ in editability. Enabled packs inform subsequent eligible reviews, not retroactive rewrites of completed results. [SS14]

**Procedure:** open **Security requirements**, select or create the pack, review applicability and criteria, enable it, and configure the design/code review to evaluate requirements. A vulnerability-only review is not the same evaluation mode. Inspect findings against the selected requirement, not merely the total count. [SS14] [SS05]

**Original example:** require an authorization check before returning an account-owned invoice. Applicability: handlers returning account-owned invoices. Compliance: the authenticated principal must be authorized for the invoice's owning account. A public static-document handler is inapplicable, not automatically compliant with an invoice rule. Test all three cases: compliant, violating and inapplicable.

### S-M04 — Regeneration replaces a pack's contents

Generating requirements from uploaded documents is a separate administrative mechanism. Supported input includes DOC, DOCX, Markdown, PDF and text. Select a custom pack, upload policy material, generate, inspect and edit the result, then enable it. [SS15]

Uploading new documents regenerates the pack and replaces existing requirements, including manually added ones. It is not an append operation. Do not start a competing upload while generation is running. Keep the governing policy and reviewed requirement source in Git; inspect the replacement before enabling it. A framework pack is not a compliance certificate. [SS15] [SS14]

### S-M06 — Customer-managed encryption uses several identities

The documented hierarchy uses a customer KMS key to protect a resource-specific branch key held in a service-managed DynamoDB store. The keyring derives wrapping keys used to protect data-encryption keys. Branch-key rotation and rotation of the KMS key are separate processes; old key versions remain necessary to decrypt older data. [SS18]

Resource-specific encryption context and identity determine authorization. The relevant actors are not interchangeable:

| Actor/path | Permission responsibility |
|---|---|
| Administrator using console | Caller permissions for configuration and forwarded operations |
| Web-app access role | Supported web-app data access |
| Assessment service role | Customer resources such as S3, secrets and logs |
| Service principal / asynchronous workflow | Service-managed background access as documented |

**Configuration procedure:** select a supported enabled symmetric key, apply the current role/service-principal policy statements with the documented resource and encryption-context conditions, and choose the key when creating the supported resource. An application default can be overridden by an explicit resource key; changing the default does not re-encrypt existing resources. Review the current example policies rather than granting all KMS actions to all four identities. [SS18]

**Failure diagnosis:** identify the calling identity and denied KMS action from authorized audit evidence; inspect the matching key policy, grants/role policy and encryption context. Re-enabling a deliberately disabled test key can restore access; deletion can make retained data permanently unavailable. Do not disable a production key merely to demonstrate this mechanism. [SS18]

## 04. Assessment, Remediation and Evidence Lifecycle

Follow saved configurations, runs, findings, repairs, revalidation and shift-left assessments.

### S-04 — Configuration, preflight and run lifecycle

A penetration-test configuration can be saved as a draft and completed through wizard steps for details, VPC, credentials, network and additional settings. It is reusable. A run is a separate execution against the then-current configuration and target. **Create** and **Create and execute** are not equivalent actions. [SS08]

Select sources and branch context deliberately: a latest repository branch is not necessarily the deployed revision. For private testing, configure approved network access and optional CloudWatch logging. For repeated tests, inspect the supported scheduling setup and associated Scheduler role rather than assuming that an external cron trigger is the only path. Complete schedule administration is linked to AWS rather than reproduced here. [SS07] [SS08]

Task-hours aggregate work across concurrent tasks; they are not wall-clock duration. The run's configured spending/work limit, account quota and any schedule are different controls. A run reaching its task-hour limit can complete without establishing exhaustive application coverage. Consult pricing before execution; cancelling does not erase work already performed. [SS08] [SS10] [SS11]

**Engineering run record:** capture the configuration ID, target revision, authenticated roles, exclusions, run ID, configured limit, start/end times and incomplete areas. Inspect findings and execution/log evidence while the run operates. Stop on unexpected effects; preserve an incomplete outcome rather than relabeling it a pass. These recordkeeping recommendations do not add product-level guarantees.

### S-05 — Findings, remediation and deployment are different objects

A finding identifies the issue and its supporting evidence in a particular assessment context. The review surface can expose description, code locations, evidence and a suggested fix. Configured remediation can produce a patch or pull request, with provider-specific behavior. For example, the reviewed GitHub path distinguishes private-repository pull requests from a downloadable diff for public repositories. [SS05] [SS12]

**Procedure:** select a material finding, verify the affected source and target revision, inspect reproduction or code evidence, request remediation only when the repository path is configured, then review and test the proposed change through the normal engineering process. A generated patch is neither deployment nor revalidation. [SS12]

**Engineering verification:** before closure, identify the exact deployed revision and re-run relevant regression tests. Retain rejected changes and failed builds as unfinished work. Use the finding ID as the link between assessment, change, deployment and revalidation—not similarity of issue titles.

### S-M05 — Revalidation replays selected finding evidence

After a repair reaches the original test environment, open the completed penetration-test run, choose **Multiselect findings for revalidation**, select findings, and choose **Revalidate findings**. The service starts a separate job using current authentication/configuration and repeats the selected validation steps. It does not conduct broad new discovery. [SS13]

```text
Original finding + deployed repair
                  ↓ selected validation steps
          Separate revalidation job
                  ↓
      Active: reproduced / Resolved: not reproduced
                  ↓
          linked finding and job history
```

The original finding is preserved and linked to the new job. A non-reproduction result is scoped to that finding and execution conditions. An authentication or environment failure can undermine its interpretation; inspect reachability before treating a result as evidence of repair. [SS13]

### S-06 — Code, design and threat-model workflows

| Assessment | Configuration and execution | Reviewable result |
|---|---|---|
| Code review | Connect sources, select vulnerability/requirement modes, start full review or configure supported repository events | Locations, evidence, suggested fixes; preflight failures remain separate |
| Design review | Submit a design for a one-off assessment; clone to create a new review | Design findings against relevant requirements |
| Threat model | Create a reusable definition with scope documents and source context, then start a run | System overview, boundaries, data flows and threats |

Code review preflight checks source and execution prerequisites before analysis. Ready-for-review repository events differ from draft changes; inspect the actual provider and configured trigger. Threat-model scope documents define what to analyze, while source documents/code provide system context. Do not treat them as interchangeable fields. [SS03] [SS05] [SS16] [SS17]

**Threat-model procedure:** in the web app, create the model, provide title, scope documents, sources and service role, optionally configure logs, save, then start a run. Review the inferred system model before relying on individual threats. Inspect severity, evidence and dispositions. A model generated from the wrong system boundary is not repaired merely by dismissing inconvenient threats. [SS16]

The full pipeline integration, complete design-review walkthrough and provider-specific remediation matrix are linked coverage, not reproduced procedures in this edition. This is an explicit limit of the guide, not a claim that those functions are absent.

## 05. Worked Finding Revalidation

Trace an authorization finding through a deployed repair and prepared revalidation evidence.

### S-U01 — Worked example: a repaired authorization check

**Synthetic, authorized-staging exercise.** Two test users belong to different customer accounts. The illustrative finding is that user A can receive a test invoice owned by account B. No live endpoint, credential or exploit execution is supplied.

| Evidence record | Before repair | Candidate repair | After deployment |
|---|---|---|---|
| Application revision | `demo-r1` | `demo-r2` under review | `demo-r2` deployed |
| Same-account test | Expected invoice returned | Regression test passes | Expected invoice returned |
| Cross-account test | Test invoice returned unexpectedly | Ownership check added; unit test passes | Access denied in prepared result |
| Identity evidence | User A / account A | Test principal controlled | User A / account A confirmed |

**Walkthrough:** inspect the original finding and target revision; review the proposed ownership check; verify that the prepared deployment record names `demo-r2`; select the finding for revalidation; inspect the new job and its linkage. The observation that a patch exists is not used as evidence of deployment. The prepared post-deployment denial supports only this tested path and identity.

**Failure branch:** if revalidation instead logs in as a privileged administrator, its result is not the intended test of user A. Correct the credential role and rerun the authorized verification. If no application path was reached, do not interpret the absence of reproduction as proof of repair.

**Expected deliverable:** a finding disposition linking original evidence, reviewed change, deployed revision, actual authenticated identity and targeted result, with untested routes stated explicitly. The fixture teaches evidence lineage; it is not an assessment result or a security guarantee.

## 06. Troubleshooting, Limits and Failure Modes

Diagnose the failed access, authentication, criteria, execution or evidence prerequisite.

### S-07 — Operational limits and failure diagnosis

The reviewed quota page distinguishes assessment capacity from spending controls. Examples include five concurrent penetration tests and five concurrent code-review runs as adjustable quotas, plus 20 requirement packs, 30 requirements per pack and 150 enabled requirements per account/Region as fixed limits. Confirm actual quotas and pricing before large-scale execution; a concurrency limit is not a financial budget. [SS10] [SS11]

| Symptom | Likely boundary | Next inspection |
|---|---|---|
| Repository missing | Registration or connection | Account type, installation approval, connected repo and feature setting |
| Credential source denied | Service-role resource access | Correct ARN/account, required read/invoke actions and trust |
| Secret resolves; login fails | Application flow | Access URL, instructions, MFA, identity and credential-test result |
| Private endpoint unreachable | Network | DNS, route/NAT requirements, egress, target rules and VPC configuration |
| Additional domain blocked | Target/access/exclusion rules | Login-derived domains; approve only necessary accessible endpoints |
| No requirement findings | Configuration/applicability | Enabled pack, selected evaluation mode, inapplicable versus compliant |
| New document removed a manual rule | Pack regeneration | Compare generated replacement with the governing Git source |
| Finding not reproduced | Target and authentication | Deployed revision, role reached and revalidation job evidence |
| Encrypted object inaccessible | KMS identity/context | Relevant role/principal, key state, action and context conditions |

This ordering is engineering guidance derived from the cited procedures. It does not claim that every error message has one unique cause. [SS06] [SS09] [SS18]

## 07. Coverage and Source Notes

Review coverage decisions, availability boundaries and official sources.

### S-08 — Coverage and evidence decisions

| Official subject | Treatment | Remaining boundary |
|---|---|---|
| Resource lifecycle and identities | Model plus setup sequence | Complete SSO and organization-policy deployment linked |
| Penetration testing | Configuration, target classes, credentials, run interpretation | Full GenAI risk-exception authoring not reproduced |
| Authentication | Strategy matrix, preflight, learned login reuse | No actual secrets or running credential backend |
| Requirements | Evaluation separated from destructive regeneration | Full managed-pack inventory linked |
| Code and threat models | Usable configuration sequence and result model | Complete CI/CD and provider compatibility matrix deferred |
| Findings and KMS | Lineage, remediation boundaries, key hierarchy and actors | Full policy documents remain official reference |
| Limits/troubleshooting | Selected operational constraints and diagnostic paths | Not an exhaustive error catalog |

**Version conflicts:** current indexed authentication/wizard pages include email MFA and nonstandard ports. Older cached authentication/troubleshooting pages contradict those points. The newer task-specific pages are used; the older troubleshooting source supports only the remaining diagnostics. Review date means retrieval, not a page publication date.

#### Official sources and reviewed sections

- [SS01] Service scope and feature distinctions.
- [SS02] Documentation history; feature announcements and availability.
- [SS03] Account versus space resources; configuration/run lifecycle by assessment type.
- [SS04] Administrative and assessment surfaces, application context.
- [SS05] Code-review setup, modes, preflight, full scans and findings.
- [SS06] Source registration and network troubleshooting; stale port restriction excluded.
- [SS07] Target verification, VPC/role/logging setup and optional scheduling; newer indexed content.
- [SS08] Current penetration-test wizard, network classes, credentials and task-hours; newer indexed content.
- [SS09] Credential methods, preflight, login reuse and MFA; newer indexed content resolves older cached text.
- [SS10] Quotas and adjustability; current indexed table.
- [SS11] Pricing versus capacity and cancellation implications.
- [SS12] Remediation provider behavior and proposed patches.
- [SS13] Revalidation initiation, results and lineage.
- [SS14] Requirement fields, applicability, activation and review behavior.
- [SS15] Requirement generation and replacement consequences.
- [SS16] Threat-model scope/source distinction, setup, preflight and result review.
- [SS17] Repository-triggered review and comments.
- [SS18] Hierarchical keyring, identities, encryption context and key lifecycle.

[SS01]: https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html
[SS02]: https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html
[SS03]: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
[SS04]: https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html
[SS05]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html
[SS06]: https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html
[SS07]: https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html
[SS08]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
[SS09]: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
[SS10]: https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html
[SS11]: https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html
[SS12]: https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html
[SS13]: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
[SS14]: https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html
[SS15]: https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html
[SS16]: https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html
[SS17]: https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html
[SS18]: https://docs.aws.amazon.com/securityagent/latest/userguide/customer-managed-keys.html
