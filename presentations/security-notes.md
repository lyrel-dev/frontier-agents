# AWS Security Agent — HTML presentation reference



Open [security.html](security.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.



## 1. Product Functions and Security Resource Model

**Chapter:** Part I · Product Model. **Schedule:** 00:00–03:00. **Slide budget:** 03:00.

Application scope, assessment configuration, execution and finding lifecycle are different resource layers.



Layer | Primary objects | Purpose | Evidence

Account resources | Integrations, identity and requirement packs | Shared setup and reusable criteria | Provider registration and enabled packs

Agent Space | Application sources, users and settings | Application-specific boundary | Space ID and source connections

Assessment configuration | Targets, credentials, criteria and limits | Reusable definition for eligible assessment types | Saved configuration and revision

Execution | Run, job or review | Assess the current target or source | Status, identity and findings

Finding lifecycle | Finding, remediation, Jira link and revalidation | Track evidence through repair | Original and linked verification records



**Guide:** [S-01](../guides/security.html#S-01)



## 2. Security Use Case Taxonomy and Availability

**Chapter:** Part II · Use Case Catalog. **Schedule:** 03:00–05:00. **Slide budget:** 02:00.

Availability must be checked for the exact assessment type and integration.



Use case family | Representative work | Delivery | Availability boundary

Dynamic assessment | On-demand, authenticated and private penetration testing | Native assessment | On-demand penetration testing GA

Finding operations | Review, Jira tracking, remediation and revalidation | Native plus integrations | Feature-specific

Source review | Full, change-focused or differential code review | Configured review | Preview

Design analysis | Design review and threat modeling | Configured assessment | Preview

Security criteria | Requirement packs and policy evaluation | Configured reusable criteria | Preview workflows



**Guide:** [S-01](../guides/security.html#S-01), [S-04](../guides/security.html#S-04), [S-06](../guides/security.html#S-06)



## 3. Application Assessment Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 05:00–08:00. **Slide budget:** 03:00.

Domain verification, network access, credential retrieval and application login are separate prerequisites.



Use case | Required scope | Authentication | Output

On-demand penetration test | Verified staging target and written authority | Optional or required by route | Run findings and evidence

Authenticated workflow assessment | Representative test roles and protected routes | Direct or AWS-native credential strategy | Coverage by actual identity

Private application assessment | VPC route, DNS and security groups | Same application login model | Reachability and findings

Recurring assessment | Stable configuration and schedule | Current credentials at execution time | Separate scheduled runs

Login procedure reuse | Successful first authentication flow | Login Optimization enabled | Saved procedure used by later sessions



**Guide:** [S-03](../guides/security.html#S-03), [S-M01](../guides/security.html#S-M01), [S-M02](../guides/security.html#S-M02), [S-04](../guides/security.html#S-04)



## 4. Findings, Remediation and Verification Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 08:00–11:00. **Slide budget:** 03:00.

A proposed patch, deployed revision and revalidation result are separate records.



Use case | Input | Output | Closure evidence

Finding review and prioritization | Impact, confidence, reproduction and affected role | Disposition and remediation owner | Recorded decision and scope

Jira remediation tracking | Finding and approved project | Issue linked to finding | Issue state and comments

Proposed code remediation | Accepted finding and repository access | Patch or pull request | Independent review and tests

Finding revalidation | Deployed fix and selected original finding | Separate revalidation job | Linked Active or Resolved result

Broader regression assessment | Material application change | New full penetration test | New run rather than narrow replay



**Guide:** [S-05](../guides/security.html#S-05), [S-M05](../guides/security.html#S-M05)



## 5. Shift-Left Review Use Cases

**Chapter:** Part II · Use Case Catalog. **Schedule:** 11:00–14:00. **Slide budget:** 03:00.

Code, design, threat-model and requirement workflows have different inputs and lifecycles.



Use case | Primary input | Evaluation basis | Output

Repository code review | Repository or supported source package | Vulnerability analysis and configured requirements | Code findings and locations

Change-focused review | Pull request, merge request or differential source | Changed code and configured criteria | Revision-specific findings

Security requirement evaluation | Enabled requirement pack | Applicability and compliance criteria | Requirement findings

Design review | Current design material | Security requirements and design evidence | Design findings

Threat model | Architecture and scope sources | Assets, trust boundaries, flows and threats | Reusable model and findings



**Guide:** [S-M03](../guides/security.html#S-M03), [S-M04](../guides/security.html#S-M04), [S-06](../guides/security.html#S-06)



## 6. Identity, Repository and Target Configuration

**Chapter:** Part III · Scope and Authentication. **Schedule:** 14:00–17:00. **Slide budget:** 03:00.

Registration, connection, reachability and authorization must be validated separately.



Configuration area | Decision | Confirmation | Typical failure

Operator identity | Who can use the web application | Intended user can open the space | Setup administrator only

Repository registration | Provider authorization at account level | Integration visible | Registered but not connected to application

Repository connection | Repository and branch/source selection | Expected revision available | Latest branch differs from deployed target

Target rules | Target, accessible dependency and out-of-scope entries | Preflight shows intended reachability | Dependency accidentally treated as attack target

Private access | VPC route, DNS and security groups | Application endpoint reachable | Network error mistaken for login error



**Guide:** [S-02](../guides/security.html#S-02), [S-03](../guides/security.html#S-03)



## 7. Credential Resolution and Application Authentication

**Chapter:** Part III · Scope and Authentication. **Schedule:** 17:00–20:00. **Slide budget:** 03:00.

Credential retrieval can succeed while application authentication still fails.



Credential strategy | Service access requirement | Application step | Evidence

Direct test credential | Configured test account | Enter through documented login flow | Observed application role

Secrets Manager | Read access and same-account resource | Map secret fields to login controls | Successful retrieval and login

Role assumption | Trust and role permissions | Use returned temporary credentials | Assumed identity and protected path

Credential Lambda | Invoke permission and response contract | Apply dynamic credential within timeout | Invocation result and login

MFA/login instruction | Current instructions and required factors | Complete the application-specific flow | Save & Test result



**Guide:** [S-M01](../guides/security.html#S-M01)



## 8. Login Optimization

**Chapter:** Part III · Scope and Authentication. **Schedule:** 20:00–22:00. **Slide budget:** 02:00.

Login Optimization reuses authentication navigation; it is not general vulnerability memory.



First successful login | The service discovers the authorized navigation and authentication sequence.

Saved login procedure | The successful workflow is retained as a skill for the assessment configuration.

Later session or run | The retained procedure can be reused instead of rediscovering the login path.

Changed application flow | Verify the actual authenticated identity and update behavior rather than assuming reuse remains valid.



**Guide:** [S-M02](../guides/security.html#S-M02)



## 9. Assessment Configuration and Run Lifecycle

**Chapter:** Part IV · Assessment and Evidence Lifecycle. **Schedule:** 22:00–24:00. **Slide budget:** 02:00.

A completed run confirms execution, not exhaustive route or vulnerability-class coverage.



Object or state | Meaning | Operator action | Evidence

Draft | Incomplete setup | Finish prerequisites or discard | Missing fields

Saved configuration | Reusable target, credentials and options | Review before each run | Configuration revision

Run | Assessment against then-current target | Monitor, stop or inspect | Run ID, task hours and findings

Scheduled run | Future execution from the configuration | Review schedule and current credentials | Separate run history

Design review | Different one-off lifecycle | Clone to create new work | Independent review record



**Guide:** [S-04](../guides/security.html#S-04)



## 10. Security Requirements and Requirement Packs

**Chapter:** Part IV · Assessment and Evidence Lifecycle. **Schedule:** 24:00–27:00. **Slide budget:** 03:00.

Requirement generation replaces pack contents; evaluation applies the reviewed criteria to an assessment.



Operation | Input | State change | Control

Create or edit requirement | Applicability, compliance and remediation text | Pack content changes | Human review of criteria

Enable pack | Reviewed requirements | Available to subsequent eligible reviews | Assessment must select requirement evaluation

Evaluate requirement | Component evidence and enabled pack | Compliant, violating or inapplicable result | Inspect applicability and evidence

Generate from documents | Authoritative policy sources | Pack contents are regenerated | Replacement review before enablement

Version outside service | Governed source in Git or policy system | Independent change history | Do not rely on generated pack as sole authority



**Guide:** [S-M03](../guides/security.html#S-M03), [S-M04](../guides/security.html#S-M04)



## 11. Finding Lineage, Remediation and Revalidation

**Chapter:** Part IV · Assessment and Evidence Lifecycle. **Schedule:** 27:00–30:00. **Slide budget:** 03:00.

A Resolved revalidation result applies to the selected finding and execution conditions.



Original finding | Affected target, revision, identity and validation steps.

Remediation change | Reviewed code or configuration change linked to the finding.

Deployed repair | Known revision on the same authorized test environment.

Revalidation job | Current credentials repeat selected validation steps and preserve the original finding.



**Guide:** [S-05](../guides/security.html#S-05), [S-M05](../guides/security.html#S-M05)



## 12. Repository, Pipeline and External Tracking Integrations

**Chapter:** Part IV · Assessment and Evidence Lifecycle. **Schedule:** 30:00–32:00. **Slide budget:** 02:00.

Integrations move source material, triggers and evidence; they do not broaden the authorized target scope.



Integration | Primary use | Trigger or action | Boundary

Repository provider | Source access and code review | Configured scan or supported change event | Provider and source support vary

S3 source | Code package or design/context material | Selected when creating assessment | Shared across supported capabilities

CI/CD pipeline | Start configured assessment from delivery workflow | Server-side job invocation | Runner is not the assessment engine

Jira | Track findings and revalidation updates | Create issue or add result comment | Project and audience must be appropriate

Evidence export | Point-in-time review or audit record | Download supported report or finding content | Export is not a security certificate



**Guide:** [S-02](../guides/security.html#S-02), [S-05](../guides/security.html#S-05), [S-06](../guides/security.html#S-06)



## 13. Customer-Managed Encryption and Service Identities

**Chapter:** Part IV · Assessment and Evidence Lifecycle. **Schedule:** 32:00–34:00. **Slide budget:** 02:00.

Encryption configuration and processing geography are separate controls.



Element | Role in the mechanism | Review question

Customer KMS key | Protects service branch keys | Does the policy allow the intended service identities?

Branch key | Resource-specific stored key material | Which resource and encryption context apply?

Derived wrapping key | Protects data-encryption keys | Is the expected context present?

Administrator identity | Configures resources and key use | Is setup authority separated from daily use?

Web app / assessment / async identity | Performs different data operations | Does each path have the required and only required access?



**Guide:** [S-M06](../guides/security.html#S-M06)



## 14. Worked Example: Authorization Finding Through Revalidation

**Chapter:** Part V · Worked Example. **Schedule:** 34:00–42:00. **Slide budget:** 08:00.

Prepared staging evidence traces the finding, deployed repair and scoped revalidation result.



0–2 min | Inspect original finding | User A received account B test invoice in revision demo-r1

2–4 min | Inspect reviewed change | Ownership check added and revision demo-r2 deployed

4–6 min | Inspect revalidation context | Actual user A identity and selected path reached

6–8 min | Interpret result | Prepared denial supports the selected path; it does not establish whole-application security



**Guide:** [S-U01](../guides/security.html#S-U01), [S-M05](../guides/security.html#S-M05)



## 15. Troubleshooting Matrix and Assessment Limits

**Chapter:** Part VI · Troubleshooting. **Schedule:** 42:00–44:00. **Slide budget:** 02:00.

Troubleshooting follows the first failed prerequisite in the assessment chain.



Symptom | First object to inspect | Second check | Interpretation

No source available | Integration registration and repository connection | Branch or source package | Source setup failure

Target unreachable | Target/access/out-of-scope rules | VPC route, DNS and security groups | Network scope failure

Credential obtained, login failed | Login instructions and application changes | Actual test identity | Authentication failure

Requirement not evaluated | Pack enabled state | Assessment review mode | Criteria setup failure

Revalidation inconclusive | Deployment revision and target | Authentication and reached path | Do not close finding



**Guide:** [S-07](../guides/security.html#S-07), [S-08](../guides/security.html#S-08)
