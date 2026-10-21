# AWS Security Agent — platform capabilities and mechanisms

Application-scoped assessment configuration, authentication, reusable criteria, execution records and finding lineage. An assessment scenario is not itself a platform capability.

The current documentation identifies AWS Security Agent as part of AWS Continuum. Availability is feature-specific: do not apply penetration-testing availability to every design, code, threat-model or pipeline feature. Verify the selected feature before rollout.

## Classification

**Platform capability**: A reusable ability exposed by the platform. Example: Retain operational context across investigations.

**Operation**: An action on a platform resource or configuration object. Example: Attach a memory store or change its active state.

**Mechanism**: The documented process connecting inputs, state, execution and outputs. Example: Select a store by description, then retrieve relevant entries.

**Use case**: An engineering problem that combines capabilities and mechanisms. Example: Investigate a recurring alarm while checking contradictory telemetry.

## Capability inventory

### S-C01 — Application-scoped configuration

**Group:** Scope and application context

Agent Spaces organize an application's sources, assessment configurations, remediation settings and assigned users.

**Platform resources:** Agent Space; source connections; user assignments; assessment configuration.

**Supported operations:** Configure an application space; connect relevant evidence; assign users; manage configuration records.

**Boundary:** Some resources, including security requirements, are shared across spaces. Do not infer isolation for every resource from the Agent Space label.

**Sources:** [S01](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html)

### S-C02 — Application-context assembly

**Group:** Scope and application context

Selected repositories, documents, targets and credentials supply different forms of application evidence to assessments.

**Platform resources:** Source repository; design or scope document; endpoint configuration; credential definition.

**Supported operations:** Select sources and scope documents appropriate to the assessment; maintain the target and authentication context.

**Boundary:** A scope document states analytical focus; source code supplies system context. These inputs do not establish a general persistent incident-memory feature.

**Sources:** [S02](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html)

### S-C03 — Reusable assessment criteria

**Group:** Scope and application context

Enabled requirement packs supply applicability rules, compliance criteria and optional remediation guidance for design and code reviews.

**Platform resources:** Requirement pack; individual requirement; enabled state.

**Supported operations:** Create, inspect and enable packs; review generated requirements; configure the review to evaluate requirements.

**Boundary:** Requirement generation is not a compliance certification. Pack changes do not retroactively rewrite completed assessments.

**Sources:** [S03](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [S09](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

### S-C04 — Authenticated and private target access

**Group:** Authentication and execution

Verified domains, network configuration, application credentials and service permissions determine the reachable testing surface.

**Platform resources:** Target domain; VPC access configuration; service role; credential definition.

**Supported operations:** Verify intended targets; configure authorized connectivity; select credentials and instructions for each representative role.

**Boundary:** Domain verification, network reachability and authentication are distinct prerequisites. Successful credential retrieval does not prove successful application login.

**Sources:** [S04](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [S05](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

### S-C05 — Reuse of learned login procedures

**Group:** Authentication and execution

Login Optimization records successful authentication navigation and reuses the saved workflow in subsequent login sessions and runs.

**Platform resources:** Penetration-test configuration; learned login skill; Login optimization setting.

**Supported operations:** Provide credentials; leave the default enabled or change the toggle; observe behavior after login-flow changes.

**Boundary:** The documented learning concerns navigation and authentication, not a universal vulnerability-memory or model-retraining pipeline.

**Sources:** [S05](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

### S-C06 — Reusable configurations and separate runs

**Group:** Authentication and execution

Penetration tests, code reviews and threat models separate reusable configurations from individual execution records.

**Platform resources:** Assessment configuration; run; execution status and results.

**Supported operations:** Create or edit configurations; start subsequent runs; inspect results in their own execution context.

**Boundary:** The lifecycle is not identical across assessment types: design reviews use a different one-off model with cloning.

**Sources:** [S01](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html)

### S-C07 — Finding lineage and targeted replay

**Group:** Evidence and integration controls

Revalidation tests selected existing findings in a separate job while preserving links to the original findings.

**Platform resources:** Original finding; revalidation job; result; history links.

**Supported operations:** Select findings from a completed run; start revalidation; inspect reproduced or non-reproduced outcomes and lineage.

**Boundary:** Targeted revalidation is not broad new vulnerability discovery and does not establish that the application is secure.

**Sources:** [S06](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

### S-C08 — Repository-event integration

**Group:** Evidence and integration controls

Supported repository integration initiates configured analysis and presents findings through the development workflow.

**Platform resources:** Repository connection; review configuration; event-triggered execution; findings.

**Supported operations:** Configure a supported repository and review criteria; inspect the resulting execution and findings for the relevant revision.

**Boundary:** Treat integration configuration and the server-side assessment as separate components. A repository event does not authorize testing arbitrary application targets.

**Sources:** [S07](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [S01](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html)

### S-C09 — Customer-managed encryption configuration

**Group:** Evidence and integration controls

The service exposes customer-managed key configuration for supported data protection requirements.

**Platform resources:** KMS key and policy; service configuration; encrypted resources.

**Supported operations:** Configure a supported key and required permissions; review the documented effects before key-policy changes.

**Boundary:** Encryption configuration does not by itself establish processing geography. Check the applicable data-protection and inference guidance separately.

**Sources:** [S08](https://docs.aws.amazon.com/securityagent/latest/userguide/customer-managed-keys.html)

## Mechanisms and enablement

### S-M01 — Learned authentication navigation

**Capabilities:** S-C04, S-C05

**Trigger:** The first successful login session discovers how to navigate the configured application's authentication flow.

**Process:** Provided test credentials → Successful login navigation → Saved skill file → Reuse in later sessions

The service captures successful navigation as a skill. Later login sessions in the same run and future runs can apply it rather than repeat discovery.

**State and lifecycle:** Disabling Login Optimization preserves the saved skill. Re-enabling permits reuse; the documentation describes adaptation when the login flow changes.

**Enablement:**

1. Add at least one representative test credential to the penetration-test configuration.
2. Open Additional configuration → Login optimization. The section requires an existing credential.
3. Confirm the default-enabled toggle or deliberately disable it for a controlled comparison.

**Controls:** This learned procedure is scoped to authentication behavior. It is not evidence of general incident learning or model-weight changes.

**Proposed verification:** Proposed check: compare recorded first-run and later authentication behavior in an authorized staging application. Change the test login flow and inspect successful authentication and the observed role; do not equate faster navigation with broader security coverage.

**Sources:** [S05](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

### S-M02 — Credential resolution and target reachability

**Capabilities:** S-C01, S-C02, S-C04

**Trigger:** An assessment needs access to an authenticated or privately reachable application surface.

**Process:** Authorized target configuration → Service access to credential source → Application login instructions → Authenticated test surface

Direct input or supported AWS-native credential strategies supply credentials. For advanced strategies, the service resolves the configured resource, then follows login instructions to apply the result. Secrets Manager, role assumption and Lambda are separate strategies.

**State and lifecycle:** The current credential and target configuration determines reachable access. Domain verification and optional private connectivity remain separate configuration records.

**Enablement:**

1. Verify the permitted target and configure private connectivity when required.
2. Select a supported credential strategy and grant the service only the required source access.
3. Provide login instructions describing where and how the resolved credential is applied; use test accounts without production access.

**Controls:** Credential resolution can succeed while application login fails. A verified domain does not authorize every external system reached by the application.

**Proposed verification:** Proposed check: record the actual authenticated identity, application role and reachable paths. Exercise a permitted path and confirm an out-of-scope path remains excluded. Do not count an unauthenticated run as authenticated coverage.

**Sources:** [S04](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [S05](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

### S-M03 — Requirement-pack evaluation and regeneration

**Capabilities:** S-C03

**Trigger:** A configured review evaluates an enabled requirement pack, or an administrator regenerates requirements from documents.

**Process:** Reviewed requirement definitions → Enabled pack → Configured review mode → Requirement-level findings

Requirements express applicability and compliance criteria. Enabling a pack supplies criteria for subsequent eligible reviews; the review must be configured for requirement evaluation rather than only vulnerability analysis.

**State and lifecycle:** Uploading new source documents regenerates the entire pack and replaces existing requirements, including manually added ones. Prior completed assessments are not retrospectively rewritten.

**Enablement:**

1. Open Security requirements and create or select the required pack.
2. Review each requirement's applicability and compliance criteria before enabling the pack.
3. Configure the design or code review to evaluate requirements. Do not upload replacement documents unless replacing the existing pack content is intended.

**Controls:** Generated requirements need human review. A framework pack is not an audit result or guarantee of compliance.

**Proposed verification:** Proposed check: evaluate a known compliant example, a known violation and an explicitly inapplicable example. Check applicability and evidence, not only the number of findings. Keep requirement changes in Git or the governing source system.

**Sources:** [S03](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [S09](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

### S-M04 — Targeted revalidation with preserved lineage

**Capabilities:** S-C06, S-C07

**Trigger:** An operator selects existing findings after a repair is deployed to the original target environment.

**Process:** Original finding → Separate revalidation job → Repeated validation steps → Linked result history

The service authenticates using current configuration and repeats the selected findings' validation steps. It does not rediscover vulnerabilities or test unrelated areas.

**State and lifecycle:** The original finding is preserved. The separate job reports Active when reproduced and Resolved when not reproduced during that revalidation, with links between findings and jobs.

**Enablement:**

1. Deploy the repair to the environment used by the original completed test.
2. Open the run and choose Multiselect findings for revalidation.
3. Select the relevant findings, choose Revalidate findings, and inspect the new job and history links.

**Controls:** A non-reproduction result applies to the selected finding, target and execution conditions. It is not a whole-application assurance statement.

**Proposed verification:** Proposed check: retain the deployed revision, credential identity, finding identifier and new job identifier. Confirm that the expected target was reached and assess whether any login or environmental failure weakened the result.

**Sources:** [S06](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

## Optional verification exercise

Inspect learned login behavior and a finding revalidation

Proposed prepared-result exercise; authorized staging evidence only; 8 minutes.

1. 2 min — Inspect the test target, test credential and Login Optimization setting.
2. 2 min — Compare first and later successful login behavior.
3. 2 min — Inspect one original finding and the deployed repair revision.
4. 2 min — Trace its revalidation job and state the result's scope and limitations.

**Acceptance:** Distinguish authenticated access, learned login reuse and targeted finding revalidation; none establishes general application security.

## Evidence boundary

Official product documentation supports the product statements. Configuration steps are documented guidance; verification exercises are proposed and were not executed. Selected critical sources were rechecked on 21 October 2026; other links are retained from the preceding review. This is not an exhaustive service catalog, a fresh audit of every historical claim, or a live AWS test.

## Official source register

- [S01 — Configuration and run lifecycle](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html) — retained from preceding review
- [S02 — How the service uses application context](https://docs.aws.amazon.com/securityagent/latest/userguide/how-it-works.html) — retained from preceding review
- [S03 — Security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html) — retained from preceding review
- [S04 — Enable penetration testing](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html) — retained from preceding review
- [S05 — Authentication credentials and Login Optimization](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html) — selected content rechecked
- [S06 — Finding revalidation](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html) — selected content rechecked
- [S07 — Code review findings in GitHub](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html) — retained from preceding review
- [S08 — Customer-managed encryption keys](https://docs.aws.amazon.com/securityagent/latest/userguide/customer-managed-keys.html) — retained from preceding review
- [S09 — Requirement generation and replacement](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html) — selected content rechecked
- [S10 — Documentation history and feature changes](https://docs.aws.amazon.com/securityagent/latest/userguide/doc-history.html) — selected content rechecked
