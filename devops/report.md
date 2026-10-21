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


## 6. Hand off an operational work item and verify closure

The proposed team handoff turns an accepted investigation into an owned engineering work item. Include the incident window, affected service and revision, evidence references, remaining uncertainty and the required recovery check. Preparing a code or configuration change is a responsibility of the receiving engineering team; it is not an additional DevOps Agent capability claimed here.

Use the existing review and delivery process for any change. The service owner checks current telemetry after deployment, records whether the symptom recovered and reopens the investigation when the evidence does not support closure. A generated recommendation alone is not a completed incident.

**Capability crosswalk:** C01, C02, C04

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

- S34: [Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)


## Validation boundary

Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.


## Mechanisms and enablement extension

See the [detailed source-linked setup and verification guide](../mechanisms/devops.md). It contains 10 records, a proposed six-step exercise and lifecycle controls. Existing presentation timing is unchanged.
