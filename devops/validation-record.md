# AWS agents in daily engineering — validation record

Validated: 20 October 2026

Documentation audit of the supplied first-pass HTML report. No account, repository, deployment, or prompt was runtime-tested.

## Outcome

19 original capability entries: **9 confirmed, 7 qualified, 3 workflow examples**. Four preview entries remain in the audit but are excluded from the HTML explorer by default. All eight presentation sections have corrected, source-linked transcripts.

### Meaning of verdicts

Confirmed: the core claim is directly documented. Qualified: retain only with the stated prerequisites or limitations. Workflow example: an application of documented building blocks, not a separately established native feature. GA status does not imply output correctness or zero setup.

## Capability audit

### C01 — Incident triage and root-cause investigation

**Verdict:** Confirmed

**Product:** AWS DevOps Agent

**Availability:** GA production operations

**Delivery:** Native; connected data required

**Validated wording:** Correlates accessible metrics, logs, traces, code changes, and deployment history using application topology.

**Limits:** A proposed root cause remains an investigation result to verify, not a guarantee of diagnostic accuracy or complete data coverage.

**Prerequisites:** Create an Agent Space, connect relevant accounts and telemetry, and grant operator access. Configure alert/ticket triggers for automatic initiation.

**Example prompt / documented command:** Investigate the checkout 5xx increase after the last deployment. Separate observed evidence, competing hypotheses, and missing data.

**Recommended acceptance check:** Compare timestamps, resource identities, telemetry, and the deployed diff with the investigation evidence.

**Correction:** Retained; clarified data scope and evidence requirements.

**Official evidence:** S02, S03

<details><summary>Original wording</summary>

**Title:** Incident triage and root cause

**Product:** AWS DevOps Agent

**Status:** GA

**Claim:** Correlate alarms, metrics, logs, traces, deployment history and code changes.

**Prompt:** Investigate the checkout 5xx spike after the last deployment and rank evidence-backed causes.

**Validation:** Verify timeline, telemetry and deployment diff.

**Prerequisites:** Connected observability, application context and permissions.

</details>

### C02 — Mitigation recommendations and approved actions

**Verdict:** Qualified

**Product:** AWS DevOps Agent

**Availability:** GA operations; actions need opt-in

**Delivery:** Recommendation native; execution gated

**Validated wording:** Incident investigations can present mitigation proposals. Resource-changing directed actions are a separate, explicitly enabled execution path.

**Limits:** Do not equate a suggested rollback with permission to execute it. Directed actions require layered enablement and per-action approval; unsupported operations remain excluded.

**Prerequisites:** Recommendations need investigation context. Execution additionally needs Agent Space opt-in, scoped elevated access or integration configuration, and an authorized approver. Runbooks improve context but are not a universal prerequisite.

**Example prompt / documented command:** Propose a low-risk mitigation for the queue backlog. Include risk, verification, and rollback steps; do not execute changes.

**Recommended acceptance check:** Approve only a specific change after checking affected resources and recovery criteria.

**Correction:** Separated recommendations from execution and removed “runbooks required” as an absolute condition.

**Official evidence:** S03, S13

<details><summary>Original wording</summary>

**Title:** Mitigation recommendations

**Product:** AWS DevOps Agent

**Status:** GA

**Claim:** Suggest containment, rollback and remediation options for incidents.

**Prompt:** Propose low-risk mitigations for queue backlog, with rollback steps.

**Validation:** Human approval and blast-radius review.

**Prerequisites:** Runbooks and source integrations.

</details>

### C03 — On-demand service health

**Verdict:** Confirmed

**Product:** AWS DevOps Agent

**Availability:** GA production operations

**Delivery:** Native chat; connected data required

**Validated wording:** Chat supports resource questions, historical/current health metrics, alarm status, deployment history, and incident insights.

**Limits:** Answers depend on accessible telemetry and the selected Agent Space. A health summary is not a replacement for monitoring.

**Prerequisites:** Use an enabled Agent Space web app with the needed data. Older Agent Spaces may require updated chat permissions.

**Example prompt / documented command:** Summarize checkout health for the last 24 hours using available error, latency, utilization, and alarm data. State any missing signals.

**Recommended acceptance check:** Check the reporting window and compare figures with the source dashboards.

**Correction:** Retained; made telemetry and older-space permissions explicit.

**Official evidence:** S05

<details><summary>Original wording</summary>

**Title:** On-demand service health

**Product:** AWS DevOps Agent

**Status:** GA

**Claim:** Ask about latency, errors, saturation and recent changes in natural language.

**Prompt:** Summarize the API service health over 24 hours.

**Validation:** Cross-check monitoring dashboards.

**Prerequisites:** Agent Space and connected telemetry.

</details>

### C04 — Recurring incident prevention

**Verdict:** Confirmed

**Product:** AWS DevOps Agent

**Availability:** GA production operations

**Delivery:** Native recommendations

**Validated wording:** Analyzes investigation history to suggest improvements to observability, infrastructure, governance, and application code.

**Limits:** Recommendations do not automatically implement fixes or guarantee non-recurrence. The documented default evaluation cadence is weekly; manual evaluation is available.

**Prerequisites:** Provide relevant investigation history. Review the Improvements page; assign owners to accepted work.

**Example prompt / documented command:** Review recurring checkout timeouts and propose the three most actionable prevention items, linked to the investigations that support them.

**Recommended acceptance check:** Confirm the evidence, assign ownership, and measure whether the incident pattern declines.

**Correction:** Retained; distinguished recommendations from implementation and added cadence.

**Official evidence:** S04

<details><summary>Original wording</summary>

**Title:** Recurring incident prevention

**Product:** AWS DevOps Agent

**Status:** GA

**Claim:** Analyze past incidents to recommend reliability improvements.

**Prompt:** Identify repeat timeout patterns and preventative changes.

**Validation:** Track proposals as owned tickets.

**Prerequisites:** Incident history.

</details>

### C05 — Scheduled SRE health summaries

**Verdict:** Qualified

**Product:** AWS DevOps Agent

**Availability:** Documented; setup-dependent

**Delivery:** Configured custom agent

**Validated wording:** Custom agents can generate recurring operational reports using a tailored prompt, selected MCP tools, skills, and attached memory stores.

**Limits:** A daily database report or slow-query check is a configured workflow, not an automatic built-in dashboard. Necessary database/log evidence must be accessible.

**Prerequisites:** Configure the agent and schedule, select read-only tools for the pilot, and supply the needed skills and context.

**Example prompt / documented command:** Create a daily checkout database health report from the connected sources. Report slow-query evidence only when available and flag gaps explicitly.

**Recommended acceptance check:** Review an initial run, data completeness, thresholds, tool calls, and unexpected findings before scheduling.

**Correction:** Replaced the vague “Conditional” label with explicit configuration requirements.

**Official evidence:** S06

<details><summary>Original wording</summary>

**Title:** Daily SRE health summaries

**Product:** AWS DevOps Agent

**Status:** Conditional

**Claim:** Schedule custom SRE agents to inspect slow queries, anomalies and logs.

**Prompt:** Produce a daily summary of database health and error spikes.

**Validation:** Validate thresholds and source evidence.

**Prerequisites:** Custom agent schedule and integrations.

</details>

### C06 — Production context from a coding environment

**Verdict:** Qualified

**Product:** AWS DevOps Agent

**Availability:** Documented; setup-dependent

**Delivery:** Remote integration

**Validated wording:** MCP-compatible clients can connect to DevOps Agent for operational queries and investigations. A2A is documented separately for agent-to-agent communication.

**Limits:** MCP, A2A, and ACP are distinct interfaces. A coding assistant does not gain production visibility merely because it is installed.

**Prerequisites:** Configure a supported client, the remote endpoint, authentication, Agent Space access, and required integrations.

**Example prompt / documented command:** Using the configured DevOps Agent connection, inspect the production health of checkout and return the supporting investigation links.

**Recommended acceptance check:** Confirm identity, account/Agent Space scope, source evidence, and permitted operations.

**Correction:** Separated MCP client/IDE access from A2A and ACP rather than presenting them as interchangeable.

**Official evidence:** S07, S08

<details><summary>Original wording</summary>

**Title:** Production context inside IDE

**Product:** AWS DevOps Agent

**Status:** Conditional

**Claim:** Connect operational investigations to supported coding assistants via MCP/A2A.

**Prompt:** Check production health for the service I am editing.

**Validation:** Check identity scope and investigation links.

**Prerequisites:** Supported client and MCP/A2A setup.

</details>

### C07 — Release risk and readiness review

**Verdict:** Confirmed

**Product:** AWS DevOps Agent

**Availability:** Preview · us-east-1

**Delivery:** Native preview; repository setup

**Validated wording:** Reviews changes for internal standards, cross-repository dependency risk, and access-control issues. Managed verification can also build, run, and test changes when enabled.

**Limits:** This is preview, not a GA release gate. A review recommendation is not proof that a deployment is safe.

**Prerequisites:** Use an Agent Space in us-east-1, connect GitHub/GitLab repositories, enable the relevant repository capabilities, and supply standards as needed.

**Example prompt / documented command:** Review this release candidate for dependency and policy risks. Identify evidence, affected code, missing permissions, and unresolved uncertainty.

**Recommended acceptance check:** Retain CI, policy checks, peer review, and release authorization.

**Correction:** Confirmed preview; added the Region restriction and distinguished optional managed verification.

**Official evidence:** S09, S10, S12, S15

<details><summary>Original wording</summary>

**Title:** Release risk analysis

**Product:** AWS DevOps Agent

**Status:** Preview

**Claim:** Assess code and dependency risk before production deployment.

**Prompt:** Assess this release candidate for risky changes.

**Validation:** Keep existing CI and release gates.

**Prerequisites:** Release management preview.

</details>

### C08 — Release QA and integration testing

**Verdict:** Qualified

**Product:** AWS DevOps Agent

**Availability:** Preview · us-east-1

**Delivery:** Native preview; deployed target required

**Validated wording:** Generates and executes exploratory UAT/regression plans against deployed web applications and REST APIs.

**Limits:** Tests can send real write requests and create, modify, or delete application data. This differs from managed code-review verification; it is not a blanket guarantee of coverage.

**Prerequisites:** Configure a deployed test target and test profile, necessary authentication/access, safe test data, and any pipeline trigger. Release management preview requires us-east-1.

**Example prompt / documented command:** Against the isolated staging checkout endpoint, test the payment flow using non-production credentials and test data; report actions and findings.

**Recommended acceptance check:** Review target safety, test intent, side effects, results, coverage gaps, and cleanup.

**Correction:** Added the missing mutation warning, environment distinction, and regional limit.

**Official evidence:** S11, S15

<details><summary>Original wording</summary>

**Title:** Release QA and integration testing

**Product:** AWS DevOps Agent

**Status:** Preview

**Claim:** Generate and run verification tests in configured environments.

**Prompt:** Test checkout flows for regression before release.

**Validation:** Review coverage, environment and flaky tests.

**Prerequisites:** Release management preview and test environment.

</details>

### C09 — Repository understanding

**Verdict:** Confirmed

**Product:** Kiro

**Availability:** GA Kiro IDE; documented capability

**Delivery:** Native coding assistance

**Validated wording:** Kiro chat can answer questions about a codebase, explain logic, and request changes with project context.

**Limits:** A proposed execution path is an explanation to inspect, not a certified dependency map or runtime trace.

**Prerequisites:** Open the relevant repository and provide the files and project context needed for the question.

**Example prompt / documented command:** Trace the checkout request from HTTP handler to persistence. Cite file paths and symbols, and identify uncertain steps.

**Recommended acceptance check:** Inspect the referenced implementation and compare it with tests or runtime observations.

**Correction:** Retained; removed any implication that inferred paths are verified runtime behavior.

**Official evidence:** S16, S22

<details><summary>Original wording</summary>

**Title:** Repository understanding

**Product:** Kiro

**Status:** GA

**Claim:** Explain unfamiliar modules, execution paths and dependencies.

**Prompt:** Trace a request from HTTP endpoint to database.

**Validation:** Inspect referenced source and tests.

**Prerequisites:** Kiro with repository access.

</details>

### C10 — Scoped features and bug fixes

**Verdict:** Confirmed

**Product:** Kiro

**Availability:** GA Kiro IDE; documented capability

**Delivery:** Native chat/spec workflow

**Validated wording:** Kiro supports iterative code changes and structured feature/bugfix specifications with requirements, design, and implementation tasks.

**Limits:** A generated plan or completed task does not establish acceptance, correctness, or production readiness.

**Prerequisites:** Provide repository access, acceptance criteria, project conventions, and an appropriate tool-permission policy.

**Example prompt / documented command:** Add request-ID propagation to checkout only. Propose a plan, implement the bounded change, and show the diff and test results.

**Recommended acceptance check:** Review scope and behavior, run tests, and keep the normal pull-request and CI process.

**Correction:** Retained; kept human acceptance and CI separate from agent task completion.

**Official evidence:** S16, S17

<details><summary>Original wording</summary>

**Title:** Scoped feature and bug implementation

**Product:** Kiro

**Status:** GA

**Claim:** Plan and implement bounded code changes.

**Prompt:** Add request-id propagation and show the diff.

**Validation:** Peer review, tests and CI.

**Prerequisites:** Repository and project rules.

</details>

### C11 — Unit-test creation

**Verdict:** Confirmed

**Product:** Kiro

**Availability:** GA Kiro IDE; documented capability

**Delivery:** Native generation; optional hooks

**Validated wording:** Kiro can generate tests; its documentation includes configured hooks that create unit tests when the agent changes source files.

**Limits:** Generated assertions and edge cases still require review. Hook automation must be configured, and tests must run in a suitable toolchain.

**Prerequisites:** Supply the test framework, fixtures, dependencies, and existing test conventions. Hooks are optional.

**Example prompt / documented command:** Add tests for checkout retry limits, timeouts, and empty inputs using the existing framework. Do not weaken assertions to make tests pass.

**Recommended acceptance check:** Run the tests, inspect assertions, and confirm the new cases fail when the relevant defect is reintroduced.

**Correction:** Retained; separated test generation from test quality and optional automation.

**Official evidence:** S18, S19

<details><summary>Original wording</summary>

**Title:** Unit test creation

**Product:** Kiro

**Status:** GA

**Claim:** Generate unit and edge-case tests.

**Prompt:** Test timeout, retries and null inputs in this module.

**Validation:** Run tests and inspect assertions.

**Prerequisites:** Test framework and repo access.

</details>

### C12 — IaC drafting and explanation

**Verdict:** Workflow example

**Product:** Kiro

**Availability:** GA coding tools; workflow-specific setup

**Delivery:** General assistance; optional integration

**Validated wording:** File editing and coding assistance can be applied to Terraform, CDK, or CloudFormation work. Kiro also documents an optional Terraform MCP integration.

**Limits:** The reviewed documentation does not substantiate a single built-in validator guaranteeing destructive-change detection and least-privilege analysis across all three IaC frameworks.

**Prerequisites:** Supply the IaC files and relevant tooling. Configure additional integrations explicitly when needed.

**Example prompt / documented command:** Explain this IaC diff and flag suspected destructive changes or broad permissions. Distinguish observations from assumptions; do not apply it.

**Recommended acceptance check:** Use the actual framework’s validation/plan/diff tooling, independent policy checks, and change approval.

**Correction:** Reclassified as an assisted workflow rather than a separately verified native IaC validation feature.

**Official evidence:** S20, S21

<details><summary>Original wording</summary>

**Title:** Terraform / CDK / CloudFormation assistance

**Product:** Kiro

**Status:** GA

**Claim:** Author and inspect infrastructure-as-code changes.

**Prompt:** Review this Terraform module for destructive changes and broad IAM permissions.

**Validation:** Validate, plan, policy scan and approve.

**Prerequisites:** IaC repository and tooling.

</details>

### C13 — CI build-log diagnosis

**Verdict:** Workflow example

**Product:** Kiro

**Availability:** GA coding tools; workflow-specific setup

**Delivery:** Supplied logs or explicit integration

**Validated wording:** Kiro’s file, shell, and debugging capabilities can be used to inspect available build logs and propose a patch.

**Limits:** This is not evidence of an automatically connected, continuously monitoring CI diagnostic feature. Repository access alone does not supply remote pipeline logs.

**Prerequisites:** Provide the failing logs and build context, or configure authorized tooling that can retrieve them.

**Example prompt / documented command:** Analyze the supplied CI log. Find the earliest causal failure, propose a minimal patch, and list what still needs reproduction.

**Recommended acceptance check:** Reproduce the failure and rerun the same pipeline and environment after the change.

**Correction:** Reclassified as a workflow example; made CI log access explicit.

**Official evidence:** S20, S19

<details><summary>Original wording</summary>

**Title:** Build failure diagnosis

**Product:** Kiro

**Status:** Conditional

**Claim:** Interpret supplied CI logs and propose fixes.

**Prompt:** Find the first causal error in this pipeline log.

**Validation:** Re-run CI after the minimal fix.

**Prerequisites:** Build logs supplied or integrated.

</details>

### C14 — README and runbook drafting

**Verdict:** Workflow example

**Product:** Kiro

**Availability:** GA coding tools; workflow-specific setup

**Delivery:** General drafting; optional hooks

**Validated wording:** Kiro can edit repository files; configured hooks can generate companion documentation. A runbook is a practical use of those capabilities.

**Limits:** A generated runbook is not a verified operational procedure. Repository context may omit production configuration or recovery dependencies.

**Prerequisites:** Provide repository context, existing operational standards, and verified deployment/rollback information.

**Example prompt / documented command:** Draft a checkout deployment and rollback runbook from these inputs. Mark every command or assumption that needs operator confirmation.

**Recommended acceptance check:** Have a service owner validate commands, permissions, prerequisites, rollback safety, and recovery checks in a safe environment.

**Correction:** Retained as a clearly labeled drafting workflow, not guaranteed operational validation.

**Official evidence:** S18, S20

<details><summary>Original wording</summary>

**Title:** Runbook and README drafting

**Product:** Kiro

**Status:** GA

**Claim:** Create and update operational and developer documentation.

**Prompt:** Draft deployment and rollback runbook from this repository.

**Validation:** Verify every operational command.

**Prerequisites:** Repository context.

</details>

### C15 — AWS guidance and resource troubleshooting

**Verdict:** Qualified

**Product:** Amazon Q Developer

**Availability:** Documented; interface/permissions apply

**Delivery:** Native guidance; scoped resource access

**Validated wording:** Amazon Q Developer answers AWS implementation questions. AWS Console resource troubleshooting is separately documented and permission-dependent.

**Limits:** General AWS advice is not automatically based on your account’s effective IAM policies, organization controls, or live configuration.

**Prerequisites:** Choose the supported interface. For account-specific troubleshooting, grant the documented permissions and provide the relevant resource/error context.

**Example prompt / documented command:** Explain this S3 access-denied error. State which policies and resource facts you actually inspected and what remains unverified.

**Recommended acceptance check:** Check effective permissions, resource policy, relevant organization controls, and the original error.

**Correction:** Separated general guidance from authorized live-resource troubleshooting.

**Official evidence:** S23, S33

<details><summary>Original wording</summary>

**Title:** AWS implementation guidance

**Product:** Amazon Q Developer

**Status:** GA

**Claim:** Answer AWS architecture and implementation questions.

**Prompt:** Explain this S3 access-denied failure and IAM evaluation.

**Validation:** Verify effective policy and organization controls.

**Prerequisites:** Supported AWS interface and IAM access.

</details>

### C16 — IDE security and quality review

**Verdict:** Qualified

**Product:** Amazon Q Developer

**Availability:** Documented · IDE support ends 30 Apr 2027

**Delivery:** Native review; IDE/language limits

**Validated wording:** Amazon Q Developer reviews code for security and quality findings, with review scope and supported-language restrictions.

**Limits:** The guide describes filtering out unsupported languages, test code, and open-source code. Review findings are not a security certification; available features vary by IDE.

**Prerequisites:** Use a supported IDE/language combination and account entitlement; review quotas and the plugin lifecycle notice.

**Example prompt / documented command:** Review this change for security and correctness. Identify what was actually scanned, excluded, and left unresolved.

**Recommended acceptance check:** Reproduce findings, review fixes, and retain independent scanners and security review.

**Correction:** Added review exclusions and the precise IDE-plugin lifecycle scope.

**Official evidence:** S24, S31

<details><summary>Original wording</summary>

**Title:** IDE security and quality review

**Product:** Amazon Q Developer

**Status:** GA

**Claim:** Review code for quality and security findings in supported IDEs.

**Prompt:** Review changed files for security and correctness issues.

**Validation:** Reproduce findings and run scanners.

**Prerequisites:** IDE plugin; support ends April 2027.

</details>

### C17 — GitHub pull-request review

**Verdict:** Confirmed

**Product:** Amazon Q Developer

**Availability:** Preview

**Delivery:** GitHub app integration

**Validated wording:** Amazon Q Developer can automatically review newly opened or reopened pull requests. Later commits do not automatically trigger another review.

**Limits:** Use /q review in a new pull-request comment to request a subsequent review. This is a preview integration with usage and repository-role restrictions.

**Prerequisites:** Install the GitHub app, authorize selected repositories, and confirm an eligible repository role and review configuration.

**Example prompt / documented command:** /q review

**Recommended acceptance check:** Check the reviewed commit/diff, validate findings, and rerun required CI checks before merging.

**Correction:** Confirmed; added the important no-auto-rerun behavior for subsequent commits.

**Official evidence:** S25, S26

<details><summary>Original wording</summary>

**Title:** GitHub pull-request review

**Product:** Amazon Q Developer

**Status:** Preview

**Claim:** Automated review of newly opened or reopened PRs.

**Prompt:** Review this PR for high-risk defects.

**Validation:** Verify findings and rerun checks.

**Prerequisites:** GitHub integration in preview.

</details>

### C18 — GitHub issue-to-pull-request development

**Verdict:** Confirmed

**Product:** Amazon Q Developer

**Availability:** Preview

**Delivery:** GitHub app integration

**Validated wording:** The development label or /q dev in an issue can initiate code generation and a pull request using the issue and repository as context.

**Limits:** An opened pull request is not an accepted or deployed change. The integration is preview and subject to usage limits.

**Prerequisites:** Install and authorize the app; provide a specific issue title, description, and acceptance criteria.

**Example prompt / documented command:** /q dev

**Recommended acceptance check:** Review the proposed diff, test acceptance criteria, and approve through the normal merge process.

**Correction:** Confirmed; replaced the generic prompt with the documented trigger and kept merge ownership explicit.

**Official evidence:** S25, S27

<details><summary>Original wording</summary>

**Title:** GitHub issue-to-PR agent

**Product:** Amazon Q Developer

**Status:** Preview

**Claim:** Implement scoped GitHub issues and propose PRs.

**Prompt:** Implement the validation fix described in this issue.

**Validation:** Review diff and acceptance criteria.

**Prerequisites:** GitHub agent integration in preview.

</details>

### C19 — Supported Java and .NET transformations

**Verdict:** Qualified

**Product:** Amazon Q Developer

**Availability:** Documented · project/IDE constraints

**Delivery:** Specialized transformation workflow

**Validated wording:** Java transformation supports documented version pairs and Maven projects in supported IDEs. .NET transformation is a separate C# workflow in Visual Studio.

**Limits:** Java supports 8/11 to 17 or 21, 17 to 17 or 21, and 21 to 21. .NET has project/dependency restrictions and excludes UI layers such as Razor/WebForms.

**Prerequisites:** Validate the exact source/target, successful baseline build, supported IDE, dependencies, quotas, and network prerequisites. Review the IDE support end date.

**Example prompt / documented command:** Check this project against the documented transformation prerequisites before proposing an upgrade. List unsupported components and manual steps.

**Recommended acceptance check:** Review diffs and the readiness summary, then run integration and regression tests in the target runtime.

**Correction:** Replaced the broad legacy-upgrade statement with concrete support boundaries; positioned as backlog work, not a universal daily feature.

**Official evidence:** S28, S29, S30, S31

<details><summary>Original wording</summary>

**Title:** Supported legacy code transformations

**Product:** Amazon Q Developer

**Status:** Conditional

**Claim:** Assist supported Java and .NET transformations.

**Prompt:** Plan and implement a supported runtime upgrade.

**Validation:** Integration tests and dependency checks.

**Prerequisites:** Supported transformation workflow.

</details>

## Cross-cutting assertions

### G01 — DevOps Agent general availability

**Confirmed.** The service GA announcement is dated 31 March 2026. This is not evidence that every later feature is GA. Sources: S14, S12.

### G02 — Release-management preview and Region

**Qualified.** Readiness reviews and release testing remain preview and are documented for us-east-1 only. They are hidden by default in the day-to-day capability view. Sources: S12, S15.

### G03 — Kiro availability labels

**Qualified.** Kiro IDE/CLI product GA is confirmed. That status is not automatically applied to every surface, model, integration, or experimental feature; coding workflows are labeled separately. Sources: S22, S20.

### G04 — Amazon Q Developer retirement scope

**Confirmed.** The 30 April 2027 end-of-support notice applies to IDE plugins. It must not be rewritten as retirement of the entire Amazon Q Developer service. Sources: S31.

### G05 — Prioritizing Kiro for new adoption

**Recommendation.** Evaluating Kiro first for new coding-tool pilots is an advisory recommendation, not universal feature parity. The migration guide documents different routes for JetBrains and no native Kiro plugins for Visual Studio/Eclipse. Sources: S32.

### G06 — Permissions, data handling, and approval

**Qualified.** Least-privilege access and review gates are recommended pilot controls. Product behavior differs: DevOps directed actions require explicit approval, whereas release testing can perform exploratory application writes. Review each product’s permissions and data settings. Sources: S13, S11, S34, S35, S36.

### G07 — Collaboration and handovers

**Qualified.** Operational reports and investigation insights are documented. Turning a result into a handover, runbook, or owned corrective-action ticket is a team workflow; universal automatic ticket creation is not asserted. Sources: S05, S04.

### G08 — Benefits and 30-day pilot

**Recommendation.** Cycle time, investigation quality, rework, and cost are proposed measurements, not verified productivity results. The revised pilot covers days 1–30 explicitly rather than treating four weeks as 30 days.

### G09 — Prompts and validation steps

**Recommendation.** Natural-language prompts and engineering acceptance checks are author-created examples, not AWS-prescribed syntax or tested demonstrations. The /q review and /q dev commands are documented exceptions. Sources: S26, S27.

### G10 — Maturity versus setup effort

**Corrected.** The former GA / Preview / Conditional selector mixed release maturity with implementation effort. The report now separates availability, delivery model, and evidence verdict.

### G11 — Presentation transcript rendering

**Corrected.** The original slide arrays had three values, but the renderer read a fourth value for speaker text, producing “undefined.” All eight sections now use explicit title, message, speaker, demonstration, and source fields.

### G12 — Validation scope

**Scope note.** All 19 original capability entries, eight transcript sections, general assertions, pilot recommendations, and source links were reviewed. This is a documentation audit—not an account-access test, deployment assessment, security certification, benchmark, or exhaustive inventory of newly added features.

## Presentation transcript

### 01 — Choose by engineering task

**On-screen message:** Production operations, coding assistance, and AWS guidance are different jobs.

**Speaker transcript:** Start with the task rather than treating every AWS-branded assistant as interchangeable. DevOps Agent supports production investigation and prevention. Its release-management features are preview. Kiro supports coding workflows, while Amazon Q Developer remains relevant to AWS guidance and existing integrations. The IDE-plugin support deadline is specifically 30 April 2027; it is not a retirement notice for the whole service. Our adoption recommendation is to evaluate Kiro for new coding pilots while checking the actual editor and feature requirements.

**Proposed demonstration — not executed:** Show the product and evidence filters. Explain that a workflow example is useful, but is not a separately documented product feature.

**Official evidence:** S01, S16, S23, S31, S32

### 02 — Make one small, reviewable code change

**On-screen message:** Comprehension → bounded change → tests → human review.

**Speaker transcript:** Use the development assistant to explain the relevant code, then ask for a small change with explicit acceptance criteria. Kiro supports chat-based changes and structured feature or bugfix specifications. Test generation is documented, but generated assertions are still code that needs review. Our proposed demonstration is a request-ID propagation fix with a narrow diff. Success means the desired behavior is reproduced and verified—not merely that the agent reports completion.

**Proposed demonstration — not executed:** Walk through the prompt, relevant files, proposed diff, new tests, and actual CI result. Label an unexecuted demonstration as proposed.

**Official evidence:** S16, S17, S18, S19

### 03 — Keep CI assistance distinct from release preview

**On-screen message:** Supplied-log triage is not an automatic CI connector.

**Speaker transcript:** The first-pass CI workflow is to provide a failed build log, identify a plausible causal error, and validate a minimal fix in the original pipeline. That is an application of coding tools, not a claim that Kiro is already watching every build. DevOps Agent has separate preview readiness reviews and managed verification testing. Exploratory release testing targets a deployed application and may change its data. Use a dedicated test environment and do not collapse these different verification modes into one feature.

**Proposed demonstration — not executed:** Compare a supplied-log example with the two documented preview testing paths. Identify the target environment before any execution.

**Official evidence:** S20, S10, S11, S12

### 04 — Investigate before authorizing remediation

**On-screen message:** Evidence → hypothesis → mitigation proposal → controlled action.

**Speaker transcript:** Begin with the affected service and a precise time window. DevOps Agent can correlate connected operational signals and expose investigation evidence. Ask the operator to distinguish observations from hypotheses and test the proposed explanation. A mitigation recommendation does not automatically authorize a production change. The documented directed-action path is disabled by default and requires explicit setup and approval. The pilot should begin with investigation and recommendation review before considering resource-changing access.

**Proposed demonstration — not executed:** Show an investigation timeline and a mitigation proposal. Review affected resources and recovery checks; do not run a production change for the demonstration.

**Official evidence:** S02, S03, S13

### 05 — Turn reliability findings into owned work

**On-screen message:** Prevention recommendations and scheduled reports need different setup.

**Speaker transcript:** Recurring incident analysis produces recommendations; a scheduled health report is a configured custom-agent workflow. Give either output an owner and a verification criterion. For infrastructure work, use Kiro’s drafting and explanation capabilities without presenting them as a guaranteed Terraform, CDK, and CloudFormation validator. A source-code diff does not by itself establish live production impact. Our proposed operating loop is to review the change with the real infrastructure tooling, deploy through existing controls, and compare the result with operational evidence.

**Proposed demonstration — not executed:** Show one prevention item and its acceptance criteria, then an IaC diff alongside the framework’s own validation output.

**Official evidence:** S04, S06, S20, S21

### 06 — Treat findings as inputs, not certification

**On-screen message:** Keep independent security checks and explicit access controls.

**Speaker transcript:** Amazon Q Developer code reviews have supported-language, scope, and quota boundaries. A clean review is therefore not a statement that the entire system is secure. Likewise, an AWS explanation should not be described as account-specific analysis unless the relevant access and evidence are present. Retain independent scanners, peer review, least-privilege configuration, and a check of each product’s data handling. For existing Q IDE users, include the plugin support deadline in the transition plan.

**Proposed demonstration — not executed:** Inspect a finding, the files actually covered, and an independently reproduced result. Review tool permissions before any agent-run command.

**Official evidence:** S24, S33, S34, S35, S36, S31

### 07 — Make the handover evidence-linked

**On-screen message:** A useful output states what happened, what is known, and who acts next.

**Speaker transcript:** Operational chat can produce reports and investigation summaries. Our handover template adds the incident window, affected service, evidence links, unresolved questions, mitigation status, and action owners. This template is a team recommendation, not a claim of universal ticket automation. GitHub review and issue-to-PR capabilities are documented but remain preview. For Q’s GitHub reviews, a later commit does not automatically trigger another review; request a new one when needed.

**Proposed demonstration — not executed:** Compare an unsupported narrative with a reviewed handover. For the optional GitHub example, identify the reviewed commit and rerun trigger.

**Official evidence:** S05, S26, S27

### 08 — Approve expansion only on measured evidence

**On-screen message:** Use a bounded 30-day pilot; treat preview separately.

**Speaker transcript:** Choose one repository and one service. Establish a manual baseline, then record time to a verified outcome, factual errors, rework, and cost for the same kinds of tasks. Start with code comprehension, tests, supplied-log triage, and incident investigation. Add scheduled agents only after their data access and first-run outputs are checked. Keep preview evaluation in a separate track and check regional availability. The decision to expand should follow observed results; this report provides no measured productivity or reliability improvement.

**Proposed demonstration — not executed:** Use the day-by-day pilot phases below and agree on acceptance thresholds before starting.

**Official evidence:** S06, S15

## 30-day pilot — recommendation

### Days 1–7: Baseline and access

Choose one repository and one service. Record manual task outcomes and effort. Check editor fit, entitlements, Region, data handling, and permissions.

### Days 8–14: Developer workflows

Try bounded fixes, test generation, supplied-log triage, and documentation drafts. Record rejected suggestions and rework as well as successful results.

### Days 15–21: Operations workflows

Connect selected evidence sources. Compare incident hypotheses with known outcomes. Start with read-only investigation; test custom reports on demand before scheduling.

### Days 22–28: Repeat and compare

Repeat comparable tasks. Review accuracy, engineering effort, operational risk, and spend. Keep preview testing in an isolated, separately approved track.

### Days 29–30: Adoption decision

Accept, revise, or stop each workflow against the agreed criteria. Assign owners, retain evidence, and define when documentation should be rechecked.

## Official evidence register

Product documentation is used for behavior and limitations. Two official release announcements establish GA dates. All sources checked 20 October 2026.

### S01 — About AWS DevOps Agent

Product documentation. Section: Key features; How AWS DevOps Agent works.

Separates production operations, release management preview, and the Agent Space model.

https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html

### S02 — Production operations

Product documentation. Section: How production operations works; Getting started.

Documents telemetry correlation, topology, integrations, and investigation setup.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-production-operations-index.html

### S03 — Autonomous incident response

Product documentation. Section: Starting investigations; Inline mitigation proposals; Ask for human support.

Documents investigation entry points, evidence, mitigation proposals, and support escalation.

https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html

### S04 — Proactive incident prevention

Product documentation. Section: How proactive incident prevention works; Agent-ready specifications.

Documents recurring analysis, recommendation management, and implementation specifications.

https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html

### S05 — On Demand DevOps Tasks

Product documentation. Section: Tasks capabilities; Generating artifacts; Enabling Chat.

Documents operational questions, health reports, investigation steering, and chat prerequisites.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html

### S06 — Custom Agents

Product documentation. Section: Key concepts; How custom agents work; What custom agents can do.

Documents configurable prompts, selected tools, skills, memories, and scheduled reporting.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html

### S07 — Accessing DevOps Agent

Product documentation. Section: MCP integration; A2A integration; ACP integration.

Distinguishes IDE/client access from agent-to-agent and programmatic access.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html

### S08 — Connecting to the DevOps Agent MCP server

Product documentation. Section: Client connection instructions.

Documents the remote MCP connection and supported integration paths.

https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-connecting-to-the-devops-agent-mcp-server.html

### S09 — Release management

Product documentation. Section: Release readiness code review; Release testing; Getting started.

Documents standards, dependency, access-control, and testing capabilities.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html

### S10 — Release readiness code reviews

Product documentation. Section: Getting started; Automated verification testing.

Documents repository-level enablement and managed build/run/test verification.

https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html

### S11 — Release testing

Product documentation. Section: How release testing works; Defining test profiles; CI/CD pipelines.

Documents web/API exploratory tests, test setup, and the warning about real write operations.

https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html

### S12 — Working with DevOps Agent

Product documentation. Section: Release management (preview).

Explicitly identifies the release management capability family as preview.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent.html

### S13 — Working with directed actions

Product documentation. Section: Prerequisites; Enabling directed actions; Approving directed actions.

Documents disabled-by-default mutation, layered opt-in, and per-action operator approval.

https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html

### S14 — AWS DevOps Agent is now generally available

Official release announcement. Section: Announcement dated 31 March 2026.

Establishes the service GA date; not used as a feature-level operational specification.

https://aws.amazon.com/about-aws/whats-new/2026/03/aws-devops-agent-generally-available/

### S15 — Supported Regions

Product documentation. Section: Feature availability by Region; Considerations.

Release management preview is restricted to us-east-1; production capabilities have broader availability.

https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html

### S16 — Kiro IDE chat

Product documentation. Section: Key features; Choosing a workflow.

Documents codebase questions, edits, debugging, and workflow selection.

https://kiro.dev/docs/ide/chat/

### S17 — Kiro specs

Product documentation. Section: Core Structure; Three-Phase Workflow; Task Execution.

Documents requirements, design, implementation tasks, and feature/bugfix workflows.

https://kiro.dev/docs/specs/

### S18 — Kiro hooks

Product documentation. Section: What you can do with hooks; Setting up hooks.

Documents configurable event-triggered commands/prompts, companion tests, and documentation generation.

https://kiro.dev/docs/hooks/

### S19 — Kiro Java development guide

Product documentation. Section: Agent hooks; MCP servers.

Provides explicit unit-test generation examples and configured build-tool assistance.

https://kiro.dev/docs/guides/languages-and-frameworks/java-guide/

### S20 — Kiro built-in tools

Product documentation. Section: Tool catalog; File tools; Shell tools.

Documents file inspection/editing and command execution; availability varies by surface.

https://kiro.dev/docs/tools/

### S21 — Kiro MCP server directory

Product documentation. Section: Terraform entry.

Documents optional Terraform integration; it is not automatic built-in IaC validation.

https://kiro.dev/docs/mcp/servers/

### S22 — Kiro is generally available

Official release announcement. Section: Announcement dated 17 November 2025.

Establishes IDE/CLI product GA; does not make every feature or surface GA.

https://kiro.dev/blog/general-availability/

### S23 — What is Amazon Q Developer?

Product documentation. Section: Overview; Get started.

Documents AWS guidance and interface-specific development assistance.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html

### S24 — Reviewing code with Amazon Q Developer

Product documentation. Section: How it works; Types of code issues; Quotas.

Documents review scope, exclusions, security/quality checks, and quotas.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-reviews.html

### S25 — Amazon Q Developer GitHub quickstart

Product documentation. Section: Preview note; Install and authorize access.

Documents preview status, app installation, repository authorization, and usage limits.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/github-quickstart.html

### S26 — Reviewing code in GitHub

Product documentation. Section: Overview; Prerequisites; Initiating code reviews.

Documents new/reopened PR triggers, no automatic rerun on later commits, and /q review.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/github-code-reviews.html

### S27 — Developing features in GitHub

Product documentation. Section: Feature development; Iterating on generated code.

Documents the development label, /q dev, issue context, and generated pull requests.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/github-feature-development.html

### S28 — Upgrading Java versions

Product documentation. Section: Supported Java upgrades and IDEs; Prerequisites.

Documents supported Java version pairs, IDEs, and Maven requirements.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-transformation.html

### S29 — Transforming .NET applications

Product documentation. Section: Overview; Quotas.

Documents .NET porting/upgrades and reviewable transformation outputs.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/transform-dotnet-IDE.html

### S30 — Porting a .NET application in Visual Studio

Product documentation. Section: Step 1: Prerequisites.

Documents C# and project/dependency limitations, including excluded UI components.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/port-dotnet-application.html

### S31 — Amazon Q Developer IDE plugins end of support

Product documentation. Section: End-of-support notice; Migration.

Confirms 30 April 2027 for IDE plugins, not a retirement notice for all Amazon Q Developer.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html

### S32 — Migrating from Amazon Q Developer to Kiro

Product documentation. Section: Feature comparison; JetBrains; Visual Studio and Eclipse.

Documents migration options and the absence of native Kiro Visual Studio/Eclipse plugins.

https://kiro.dev/docs/upgrade-guides/migrating-from-q-developer/

### S33 — Asking Amazon Q to troubleshoot resources

Product documentation. Section: Resource troubleshooting and permissions.

Distinguishes conversational AWS guidance from permission-dependent resource troubleshooting.

https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/chat-actions-troubleshooting.html

### S34 — Limiting Agent Access in an AWS Account

Product documentation. Section: Access restriction guidance.

Provides product-specific guidance for constraining the agent’s AWS access.

https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html

### S35 — Kiro permissions

Product documentation. Section: Permission configuration.

Documents controls over agent file and tool access.

https://kiro.dev/docs/permissions/

### S36 — Kiro data protection

Product documentation. Section: Data protection guidance.

Source for reviewing data handling before enabling a developer workflow.

https://kiro.dev/docs/privacy-and-security/data-protection/