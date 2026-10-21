# AWS DevOps Agent

Incident investigation, service-status analysis and release-readiness workflows.


Revision: 21 October 2026. Independent engineering field guide.


**Audience:** On-call engineers, SREs, platform engineers and service owners

**Availability:** Production operations: GA. Release management: preview; assess each feature and Region separately.

**Recommended starting decision:** Start with one read-heavy investigation workflow. Add action paths only after the evidence and authorization boundaries have been tested.


## Decision brief

During an incident, the hard part is rarely opening another dashboard. It is connecting the affected service, the deployment that preceded the symptom, and the evidence that distinguishes a plausible explanation from the actual failure. DevOps Agent brings those sources into an investigation context; the engineer still decides whether the evidence justifies a mitigation.

This report follows an illustrative checkout failure after a retry-policy change. The useful result is not a fluent root-cause statement. It is a traceable investigation, a controlled next action, and a verification record. The same context can support daily health questions and prevention work. Release-readiness review and active release testing are a distinct preview path, not a capability that becomes generally available merely because production operations are GA.


## Running use case

**Name:** Checkout errors after a retry-policy release

**Trigger:** A supplied incident snapshot shows rising checkout 5xx errors after deployment DEMO-A.

**Scope:** One team-owned service, explicit environment and UTC incident window, selected repositories and telemetry.

**Deliverable:** Evidence-backed incident handoff with a mitigation candidate, owner, rollback assumptions and recovery checks.

**Not Done:** The agent has written a plausible explanation, but the deployed revision and telemetry have not been compared.

**Done:** The service owner has accepted or rejected the explanation, authorized any change separately, and recorded independent recovery evidence.


## 1. Establish the operational boundary

Begin with the service and the incident window, not an unrestricted instruction to fix production. An Agent Space gathers account configuration, integrations and application context. Its topology helps the investigation understand relationships; underlying IAM and integration permissions determine what can actually be accessed.

Connect a known-good deployment reference and the telemetry needed to challenge the incident hypothesis. Missing logs are an evidence gap, not a reason to grant broad write permissions. Validate one expected read and one harmless out-of-scope denial before relying on the configuration.

**Capability crosswalk:** C01, C06

**Responsible role (team recommendation):** Platform/on-call owner

**Input:** Service identity, environment, incident window, deployed revision, relevant telemetry and repository access.

**Artifact:** A scope record and a short inventory of available and missing evidence.

**Gate:** The service owner can explain the access boundary and identify who can stop the work.

**Fallback:** Keep the incident in the normal on-call process while missing evidence or permissions are repaired.


## 2. Investigate, then challenge the explanation

An alert, ticket or on-demand question can start the operational workflow. Ask the agent to separate observations, hypotheses and missing data. For the checkout example, the deployment time, affected resources and request failures need to agree before the change becomes the leading explanation.

Use follow-up questions to test alternatives: an upstream timeout, a capacity limit, or an unrelated configuration change. A confident answer does not eliminate competing causes. The engineer compares material claims with the source systems and preserves the evidence links for the incident record.

**Capability crosswalk:** C01, C03

**Responsible role (team recommendation):** Incident investigator

**Input:** Incident signal and scoped operational context.

**Artifact:** A hypothesis ledger with supporting observations, contrary evidence and unresolved gaps.

**Gate:** At least one material claim is independently checked against its source.

**Fallback:** Record an inconclusive investigation rather than inventing a cause or waiting indefinitely.


## 3. Separate a recommendation from an authorized action

A mitigation proposal should state the intended effect, blast radius, validation criteria and reversal plan. In the example, reducing retries may be a candidate, but a service owner must consider whether it hides errors or shifts load elsewhere. Recommendations are reviewable artifacts, not implicit permission to modify resources.

Directed actions have their own enablement, access and approval controls. Keep the action decision attached to the exact target and operation. An approval to investigate is not approval to deploy, and a broad instruction in chat is not a substitute for the configured authorization path.

**Capability crosswalk:** C02

**Responsible role (team recommendation):** Incident commander or change approver

**Input:** Reviewed hypothesis and a specific mitigation candidate.

**Artifact:** An action decision with owner, target, allowed effect, rollback and verification criteria.

**Gate:** The effect is authorized through the correct product and team controls.

**Fallback:** Execute through the established runbook or change process when the agent action path is not approved.


## 4. Turn an incident into owned prevention work

After recovery, recurring incident patterns can inform observability, resilience, infrastructure and deployment improvements. Convert a useful recommendation into a bounded engineering item rather than leaving it as an unowned report. Preserve the original incident references so the proposed fix can be evaluated against the actual failure.

Daily health summaries are configured custom-agent workflows. Specify the question, tools, skills, schedule and audience explicitly. A scheduled prompt cannot see a database or monitoring system that has not been connected, and an automated summary still needs an owner who handles missing or stale data.

**Capability crosswalk:** C04, C05

**Responsible role (team recommendation):** Service owner and SRE

**Input:** Validated incident record, historical incidents and a named follow-up owner.

**Artifact:** A prioritized improvement item or configured recurring operational report.

**Gate:** The item has measurable acceptance criteria and the scheduled output has a recipient and stop owner.

**Fallback:** Use the existing backlog and manual report until the integrations provide adequate evidence.


## 5. Review the next release without confusing the test paths

The follow-up retry-policy change can be reviewed for release risk. Readiness review evaluates a code change and its dependencies, policies and access implications; managed verification can add build or test evidence. These are release-preview features and should be piloted separately from the production investigation baseline.

Active release testing instead interacts with a running application. Browser or API requests can create, update or delete data and trigger business effects. Use a disposable staging target, test identities and disabled external side effects. Infrastructure write access being disabled does not make application testing read-only.

**Capability crosswalk:** C07, C08

**Responsible role (team recommendation):** Release owner

**Input:** Candidate revision, application context, and an authorized staging target where active testing is used.

**Artifact:** Release findings, reproduction details and explicit residual risks.

**Gate:** The release owner checks both feature availability and the actual effects allowed against the test target.

**Fallback:** Use prepared results or the ordinary test suite rather than testing a production endpoint to keep a demo moving.


## 6. Hand off code work and close on independent evidence

An investigation can hand a bounded implementation task to a coding workflow. Kiro can help with code understanding, changes and tests; Amazon Q Developer has separate AWS guidance, review and transformation capabilities. Those companion tools are retained in the inventory, but they are not renamed as native DevOps Agent features.

Close the loop with a reviewed change, the normal delivery process and an independent check of the original service symptom. IaC drafts, build-log diagnoses and runbooks remain team-composed uses of coding tools. Measure accepted investigations and completed follow-ups, not the number of agent responses.

**Capability crosswalk:** C06, C09, C10, C11, C12, C13, C14, C15, C16, C17, C18, C19

**Responsible role (team recommendation):** Development reviewer and SRE

**Input:** Evidence-linked issue with affected repository, constraints, test expectations and reviewer.

**Artifact:** Reviewed code or operational change plus a recovery or regression-test record.

**Gate:** A human reviewer accepts the result; deployment authority and access remain local to their own systems.

**Fallback:** Keep a failed or inconclusive change visible as unfinished work rather than closing the incident on generated text.


## Detailed capability reference


### C01 — Incident triage and root-cause investigation

**Claim:** Correlates accessible metrics, logs, traces, code changes, and deployment history using application topology.

**Availability:** GA production operations

**Delivery:** Native; connected data required

**Setup:** Create an Agent Space, connect relevant accounts and telemetry, and grant operator access. Configure alert/ticket triggers for automatic initiation.

**Limit:** A proposed root cause remains an investigation result to verify, not a guarantee of diagnostic accuracy or complete data coverage.

**Check:** Compare timestamps, resource identities, telemetry, and the deployed diff with the investigation evidence.

**Prompt:** Investigate the checkout 5xx increase after the last deployment. Separate observed evidence, competing hypotheses, and missing data.

**Review record to retain (team recommendation):** Incident timeline linked to deployed changes, telemetry, alternative hypotheses, and missing data.

Official documentation references: S02, S03


### C02 — Mitigation recommendations and approved actions

**Claim:** Incident investigations can present mitigation proposals. Resource-changing directed actions are a separate, explicitly enabled execution path.

**Availability:** GA operations; actions need opt-in

**Delivery:** Recommendation native; execution gated

**Setup:** Recommendations need investigation context. Execution additionally needs Agent Space opt-in, scoped elevated access or integration configuration, and an authorized approver. Runbooks improve context but are not a universal prerequisite.

**Limit:** Do not equate a suggested rollback with permission to execute it. Directed actions require layered enablement and per-action approval; unsupported operations remain excluded.

**Check:** Approve only a specific change after checking affected resources and recovery criteria.

**Prompt:** Propose a low-risk mitigation for the queue backlog. Include risk, verification, and rollback steps; do not execute changes.

**Review record to retain (team recommendation):** Mitigation proposal, affected resources, operator approval record, and observed change effects.

Official documentation references: S03, S13


### C03 — On-demand service health

**Claim:** Chat supports resource questions, historical/current health metrics, alarm status, deployment history, and incident insights.

**Availability:** GA production operations

**Delivery:** Native chat; connected data required

**Setup:** Use an enabled Agent Space web app with the needed data. Older Agent Spaces may require updated chat permissions.

**Limit:** Answers depend on accessible telemetry and the selected Agent Space. A health summary is not a replacement for monitoring.

**Check:** Check the reporting window and compare figures with the source dashboards.

**Prompt:** Summarize checkout health for the last 24 hours using available error, latency, utilization, and alarm data. State any missing signals.

**Review record to retain (team recommendation):** Timestamped service-status response with the identifiers and data windows queried.

Official documentation references: S05


### C04 — Recurring incident prevention

**Claim:** Analyzes investigation history to suggest improvements to observability, infrastructure, governance, and application code.

**Availability:** GA production operations

**Delivery:** Native recommendations

**Setup:** Provide relevant investigation history. Review the Improvements page; assign owners to accepted work.

**Limit:** Recommendations do not automatically implement fixes or guarantee non-recurrence. The documented default evaluation cadence is weekly; manual evaluation is available.

**Check:** Confirm the evidence, assign ownership, and measure whether the incident pattern declines.

**Prompt:** Review recurring checkout timeouts and propose the three most actionable prevention items, linked to the investigations that support them.

**Review record to retain (team recommendation):** Prevention backlog item linked to repeated incidents and a named technical owner.

Official documentation references: S04


### C05 — Scheduled SRE health summaries

**Claim:** Custom agents can generate recurring operational reports using a tailored prompt, selected MCP tools, skills, and attached memory stores.

**Availability:** Documented; setup-dependent

**Delivery:** Configured custom agent

**Setup:** Configure the agent and schedule, select read-only tools for the pilot, and supply the needed skills and context.

**Limit:** A daily database report or slow-query check is a configured workflow, not an automatic built-in dashboard. Necessary database/log evidence must be accessible.

**Check:** Review an initial run, data completeness, thresholds, tool calls, and unexpected findings before scheduling.

**Prompt:** Create a daily checkout database health report from the connected sources. Report slow-query evidence only when available and flag gaps explicitly.

**Review record to retain (team recommendation):** Dated scheduled health report with configured data sources and exceptions.

Official documentation references: S06


### C06 — Production context from a coding environment

**Claim:** MCP-compatible clients can connect to DevOps Agent for operational queries and investigations. A2A is documented separately for agent-to-agent communication.

**Availability:** Documented; setup-dependent

**Delivery:** Remote integration

**Setup:** Configure a supported client, the remote endpoint, authentication, Agent Space access, and required integrations.

**Limit:** MCP, A2A, and ACP are distinct interfaces. A coding assistant does not gain production visibility merely because it is installed.

**Check:** Confirm identity, account/Agent Space scope, source evidence, and permitted operations.

**Prompt:** Using the configured DevOps Agent connection, inspect the production health of checkout and return the supporting investigation links.

**Review record to retain (team recommendation):** Operational query response with service, time window, and referenced source evidence.

Official documentation references: S07, S08


### C07 — Release risk and readiness review

**Claim:** Reviews changes for internal standards, cross-repository dependency risk, and access-control issues. Managed verification can also build, run, and test changes when enabled.

**Availability:** Preview · us-east-1

**Delivery:** Native preview; repository setup

**Setup:** Use an Agent Space in us-east-1, connect GitHub/GitLab repositories, enable the relevant repository capabilities, and supply standards as needed.

**Limit:** This is preview, not a GA release gate. A review recommendation is not proof that a deployment is safe.

**Check:** Retain CI, policy checks, peer review, and release authorization.

**Prompt:** Review this release candidate for dependency and policy risks. Identify evidence, affected code, missing permissions, and unresolved uncertainty.

**Review record to retain (team recommendation):** Release-readiness findings, reviewed changes, and disposition by the release owner.

Official documentation references: S09, S10, S12, S15


### C08 — Release QA and integration testing

**Claim:** Generates and executes exploratory UAT/regression plans against deployed web applications and REST APIs.

**Availability:** Preview · us-east-1

**Delivery:** Native preview; deployed target required

**Setup:** Configure a deployed test target and test profile, necessary authentication/access, safe test data, and any pipeline trigger. Release management preview requires us-east-1.

**Limit:** Tests can send real write requests and create, modify, or delete application data. This differs from managed code-review verification; it is not a blanket guarantee of coverage.

**Check:** Review target safety, test intent, side effects, results, coverage gaps, and cleanup.

**Prompt:** Against the isolated staging checkout endpoint, test the payment flow using non-production credentials and test data; report actions and findings.

**Review record to retain (team recommendation):** Test scope, executed requests, recorded side effects, findings, and application build identifier.

Official documentation references: S11, S15


### C09 — Repository understanding

**Claim:** Kiro chat can answer questions about a codebase, explain logic, and request changes with project context.

**Availability:** GA Kiro IDE; documented capability

**Delivery:** Native coding assistance

**Setup:** Open the relevant repository and provide the files and project context needed for the question.

**Limit:** A proposed execution path is an explanation to inspect, not a certified dependency map or runtime trace.

**Check:** Inspect the referenced implementation and compare it with tests or runtime observations.

**Prompt:** Trace the checkout request from HTTP handler to persistence. Cite file paths and symbols, and identify uncertain steps.

**Review record to retain (team recommendation):** Code-path explanation with repository revision and source references.

Official documentation references: S16, S22


### C10 — Scoped features and bug fixes

**Claim:** Kiro supports iterative code changes and structured feature/bugfix specifications with requirements, design, and implementation tasks.

**Availability:** GA Kiro IDE; documented capability

**Delivery:** Native chat/spec workflow

**Setup:** Provide repository access, acceptance criteria, project conventions, and an appropriate tool-permission policy.

**Limit:** A generated plan or completed task does not establish acceptance, correctness, or production readiness.

**Check:** Review scope and behavior, run tests, and keep the normal pull-request and CI process.

**Prompt:** Add request-ID propagation to checkout only. Propose a plan, implement the bounded change, and show the diff and test results.

**Review record to retain (team recommendation):** Reviewable code diff, scoped acceptance tests, and reviewer disposition.

Official documentation references: S16, S17


### C11 — Unit-test creation

**Claim:** Kiro can generate tests; its documentation includes configured hooks that create unit tests when the agent changes source files.

**Availability:** GA Kiro IDE; documented capability

**Delivery:** Native generation; optional hooks

**Setup:** Supply the test framework, fixtures, dependencies, and existing test conventions. Hooks are optional.

**Limit:** Generated assertions and edge cases still require review. Hook automation must be configured, and tests must run in a suitable toolchain.

**Check:** Run the tests, inspect assertions, and confirm the new cases fail when the relevant defect is reintroduced.

**Prompt:** Add tests for checkout retry limits, timeouts, and empty inputs using the existing framework. Do not weaken assertions to make tests pass.

**Review record to retain (team recommendation):** Generated test changes, execution results, and any failing assertions.

Official documentation references: S18, S19


### C12 — IaC drafting and explanation

**Claim:** File editing and coding assistance can be applied to Terraform, CDK, or CloudFormation work. Kiro also documents an optional Terraform MCP integration.

**Availability:** GA coding tools; workflow-specific setup

**Delivery:** General assistance; optional integration

**Setup:** Supply the IaC files and relevant tooling. Configure additional integrations explicitly when needed.

**Limit:** The reviewed documentation does not substantiate a single built-in validator guaranteeing destructive-change detection and least-privilege analysis across all three IaC frameworks.

**Check:** Use the actual framework’s validation/plan/diff tooling, independent policy checks, and change approval.

**Prompt:** Explain this IaC diff and flag suspected destructive changes or broad permissions. Distinguish observations from assumptions; do not apply it.

**Review record to retain (team recommendation):** IaC diff with relevant plan, validation, or synthesis results produced by the team.

Official documentation references: S20, S21


### C13 — CI build-log diagnosis

**Claim:** Kiro’s file, shell, and debugging capabilities can be used to inspect available build logs and propose a patch.

**Availability:** GA coding tools; workflow-specific setup

**Delivery:** Supplied logs or explicit integration

**Setup:** Provide the failing logs and build context, or configure authorized tooling that can retrieve them.

**Limit:** This is not evidence of an automatically connected, continuously monitoring CI diagnostic feature. Repository access alone does not supply remote pipeline logs.

**Check:** Reproduce the failure and rerun the same pipeline and environment after the change.

**Prompt:** Analyze the supplied CI log. Find the earliest causal failure, propose a minimal patch, and list what still needs reproduction.

**Review record to retain (team recommendation):** Build-log excerpts, stated failure hypothesis, and reproducible local or CI check.

Official documentation references: S20, S19


### C14 — README and runbook drafting

**Claim:** Kiro can edit repository files; configured hooks can generate companion documentation. A runbook is a practical use of those capabilities.

**Availability:** GA coding tools; workflow-specific setup

**Delivery:** General drafting; optional hooks

**Setup:** Provide repository context, existing operational standards, and verified deployment/rollback information.

**Limit:** A generated runbook is not a verified operational procedure. Repository context may omit production configuration or recovery dependencies.

**Check:** Have a service owner validate commands, permissions, prerequisites, rollback safety, and recovery checks in a safe environment.

**Prompt:** Draft a checkout deployment and rollback runbook from these inputs. Mark every command or assumption that needs operator confirmation.

**Review record to retain (team recommendation):** Documentation diff with technical-owner review and a reproducible procedure.

Official documentation references: S18, S20


### C15 — AWS guidance and resource troubleshooting

**Claim:** Amazon Q Developer answers AWS implementation questions. AWS Console resource troubleshooting is separately documented and permission-dependent.

**Availability:** Documented; interface/permissions apply

**Delivery:** Native guidance; scoped resource access

**Setup:** Choose the supported interface. For account-specific troubleshooting, grant the documented permissions and provide the relevant resource/error context.

**Limit:** General AWS advice is not automatically based on your account’s effective IAM policies, organization controls, or live configuration.

**Check:** Check effective permissions, resource policy, relevant organization controls, and the original error.

**Prompt:** Explain this S3 access-denied error. State which policies and resource facts you actually inspected and what remains unverified.

**Review record to retain (team recommendation):** AWS implementation guidance with documentation references or scoped resource diagnostics.

Official documentation references: S23, S33


### C16 — IDE security and quality review

**Claim:** Amazon Q Developer reviews code for security and quality findings, with review scope and supported-language restrictions.

**Availability:** Documented · IDE support ends 30 Apr 2027

**Delivery:** Native review; IDE/language limits

**Setup:** Use a supported IDE/language combination and account entitlement; review quotas and the plugin lifecycle notice.

**Limit:** The guide describes filtering out unsupported languages, test code, and open-source code. Review findings are not a security certification; available features vary by IDE.

**Check:** Reproduce findings, review fixes, and retain independent scanners and security review.

**Prompt:** Review this change for security and correctness. Identify what was actually scanned, excluded, and left unresolved.

**Review record to retain (team recommendation):** Code finding records with severity, affected lines, and reviewer disposition.

Official documentation references: S24, S31


### C17 — GitHub pull-request review

**Claim:** Amazon Q Developer can automatically review newly opened or reopened pull requests. Later commits do not automatically trigger another review.

**Availability:** Preview

**Delivery:** GitHub app integration

**Setup:** Install the GitHub app, authorize selected repositories, and confirm an eligible repository role and review configuration.

**Limit:** Use /q review in a new pull-request comment to request a subsequent review. This is a preview integration with usage and repository-role restrictions.

**Check:** Check the reviewed commit/diff, validate findings, and rerun required CI checks before merging.

**Prompt:** /q review

**Review record to retain (team recommendation):** PR review comments, changed-file context, and any explicitly requested re-review.

Official documentation references: S25, S26


### C18 — GitHub issue-to-pull-request development

**Claim:** The development label or /q dev in an issue can initiate code generation and a pull request using the issue and repository as context.

**Availability:** Preview

**Delivery:** GitHub app integration

**Setup:** Install and authorize the app; provide a specific issue title, description, and acceptance criteria.

**Limit:** An opened pull request is not an accepted or deployed change. The integration is preview and subject to usage limits.

**Check:** Review the proposed diff, test acceptance criteria, and approve through the normal merge process.

**Prompt:** /q dev

**Review record to retain (team recommendation):** Issue-linked pull request with diff, test output, and CI/review status.

Official documentation references: S25, S27


### C19 — Supported Java and .NET transformations

**Claim:** Java transformation supports documented version pairs and Maven projects in supported IDEs. .NET transformation is a separate C# workflow in Visual Studio.

**Availability:** Documented · project/IDE constraints

**Delivery:** Specialized transformation workflow

**Setup:** Validate the exact source/target, successful baseline build, supported IDE, dependencies, quotas, and network prerequisites. Review the IDE support end date.

**Limit:** Java supports 8/11 to 17 or 21, 17 to 17 or 21, and 21 to 21. .NET has project/dependency restrictions and excludes UI layers such as Razor/WebForms.

**Check:** Review diffs and the readiness summary, then run integration and regression tests in the target runtime.

**Prompt:** Check this project against the documented transformation prerequisites before proposing an upgrade. List unsupported components and manual steps.

**Review record to retain (team recommendation):** Transformation diff, compatibility checklist, and independent build/test results.

Official documentation references: S28, S29, S30, S31


## Illustrative handoff

```yaml

work_item: INC-DEMO-001
service: checkout-api
environment: staging
revision: DEMO-A
evidence: [incident-window, telemetry-links, deployed-diff]
allowed_effects: [read-evidence, propose-code-change]
prohibited_effects: [production-deployment]
owner: service-owner
done: reviewed-change-and-independent-verification

```


## Readiness checklist

- [ ] One owned workload and UTC time window are recorded.

- [ ] A deployed revision and material telemetry are available.

- [ ] Out-of-scope access is denied at the actual integration layer.

- [ ] Hypotheses and missing evidence are separated.

- [ ] Any change has its own authorization, rollback and verifier.

- [ ] Active release tests use an approved non-production target.


## Sources

- S01: [About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)

- S02: [Production operations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-production-operations-index.html)

- S03: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

- S04: [Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

- S05: [On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)

- S06: [Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

- S07: [Accessing DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html)

- S08: [Connecting to the DevOps Agent MCP server](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-connecting-to-the-devops-agent-mcp-server.html)

- S09: [Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)

- S10: [Release readiness code reviews](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html)

- S11: [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

- S12: [Working with DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent.html)

- S13: [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

- S14: [AWS DevOps Agent is now generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-devops-agent-generally-available/)

- S15: [Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

- S16: [Kiro IDE chat](https://kiro.dev/docs/ide/chat/)

- S17: [Kiro specs](https://kiro.dev/docs/specs/)

- S18: [Kiro hooks](https://kiro.dev/docs/hooks/)

- S19: [Kiro Java development guide](https://kiro.dev/docs/guides/languages-and-frameworks/java-guide/)

- S20: [Kiro built-in tools](https://kiro.dev/docs/tools/)

- S21: [Kiro MCP server directory](https://kiro.dev/docs/mcp/servers/)

- S22: [Kiro is generally available](https://kiro.dev/blog/general-availability/)

- S23: [What is Amazon Q Developer?](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/what-is.html)

- S24: [Reviewing code with Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-reviews.html)

- S25: [Amazon Q Developer GitHub quickstart](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/github-quickstart.html)

- S26: [Reviewing code in GitHub](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/github-code-reviews.html)

- S27: [Developing features in GitHub](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/github-feature-development.html)

- S28: [Upgrading Java versions](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-transformation.html)

- S29: [Transforming .NET applications](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/transform-dotnet-IDE.html)

- S30: [Porting a .NET application in Visual Studio](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/port-dotnet-application.html)

- S31: [Amazon Q Developer IDE plugins end of support](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-developer-ide-end-of-support.html)

- S32: [Migrating from Amazon Q Developer to Kiro](https://kiro.dev/docs/upgrade-guides/migrating-from-q-developer/)

- S33: [Asking Amazon Q to troubleshoot resources](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/chat-actions-troubleshooting.html)

- S34: [Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

- S35: [Kiro permissions](https://kiro.dev/docs/permissions/)

- S36: [Kiro data protection](https://kiro.dev/docs/privacy-and-security/data-protection/)


## Validation boundary

Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.


## Mechanisms and enablement extension

See the [detailed source-linked setup and verification guide](../mechanisms/devops.md). It contains 10 records, a proposed six-step exercise and lifecycle controls. Existing presentation timing is unchanged.
