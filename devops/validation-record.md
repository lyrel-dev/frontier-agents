# AWS agents in daily engineering — validated report — capability evidence record

Scope revision: 2026-10-21-three-agent-scope. This is a filtered record of the previously reviewed official evidence, not a new external documentation audit. Earlier editions are available through Git history.

## Current capability records

## C01 · Incident triage and root-cause investigation

**Documented function:** Correlates accessible metrics, logs, traces, code changes, and deployment history using application topology.

**Availability:** GA production operations

**Prerequisites:** Create an Agent Space, connect relevant accounts and telemetry, and grant operator access. Configure alert/ticket triggers for automatic initiation.

**Limitations:** A proposed root cause remains an investigation result to verify, not a guarantee of diagnostic accuracy or complete data coverage.

**Proposed verification:** Compare timestamps, resource identities, telemetry, and the deployed diff with the investigation evidence.

- [S02 · Production operations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-production-operations-index.html)

- [S03 · Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

## C02 · Mitigation recommendations and approved actions

**Documented function:** Incident investigations can present mitigation proposals. Resource-changing directed actions are a separate, explicitly enabled execution path.

**Availability:** GA operations; actions need opt-in

**Prerequisites:** Recommendations need investigation context. Execution additionally needs Agent Space opt-in, scoped elevated access or integration configuration, and an authorized approver. Runbooks improve context but are not a universal prerequisite.

**Limitations:** Do not equate a suggested rollback with permission to execute it. Directed actions require layered enablement and per-action approval; unsupported operations remain excluded.

**Proposed verification:** Approve only a specific change after checking affected resources and recovery criteria.

- [S03 · Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

- [S13 · Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

## C03 · On-demand service health

**Documented function:** Chat supports resource questions, historical/current health metrics, alarm status, deployment history, and incident insights.

**Availability:** GA production operations

**Prerequisites:** Use an enabled Agent Space web app with the needed data. Older Agent Spaces may require updated chat permissions.

**Limitations:** Answers depend on accessible telemetry and the selected Agent Space. A health summary is not a replacement for monitoring.

**Proposed verification:** Check the reporting window and compare figures with the source dashboards.

- [S05 · On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)

## C04 · Recurring incident prevention

**Documented function:** Analyzes investigation history to suggest improvements to observability, infrastructure, governance, and application code.

**Availability:** GA production operations

**Prerequisites:** Provide relevant investigation history. Review the Improvements page; assign owners to accepted work.

**Limitations:** Recommendations do not automatically implement fixes or guarantee non-recurrence. The documented default evaluation cadence is weekly; manual evaluation is available.

**Proposed verification:** Confirm the evidence, assign ownership, and measure whether the incident pattern declines.

- [S04 · Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

## C05 · Scheduled SRE health summaries

**Documented function:** Custom agents can generate recurring operational reports using a tailored prompt, selected MCP tools, skills, and attached memory stores.

**Availability:** Documented; setup-dependent

**Prerequisites:** Configure the agent and schedule, select read-only tools for the pilot, and supply the needed skills and context.

**Limitations:** A daily database report or slow-query check is a configured workflow, not an automatic built-in dashboard. Necessary database/log evidence must be accessible.

**Proposed verification:** Review an initial run, data completeness, thresholds, tool calls, and unexpected findings before scheduling.

- [S06 · Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

## C06 · Production context from a coding environment

**Documented function:** MCP-compatible clients can connect to DevOps Agent for operational queries and investigations. A2A is documented separately for agent-to-agent communication.

**Availability:** Documented; setup-dependent

**Prerequisites:** Configure a supported client, the remote endpoint, authentication, Agent Space access, and required integrations.

**Limitations:** MCP, A2A, and ACP are distinct interfaces. A coding assistant does not gain production visibility merely because it is installed.

**Proposed verification:** Confirm identity, account/Agent Space scope, source evidence, and permitted operations.

- [S07 · Accessing DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html)

- [S08 · Connecting to the DevOps Agent MCP server](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-connecting-to-the-devops-agent-mcp-server.html)

## C07 · Release risk and readiness review

**Documented function:** Reviews changes for internal standards, cross-repository dependency risk, and access-control issues. Managed verification can also build, run, and test changes when enabled.

**Availability:** Preview · us-east-1

**Prerequisites:** Use an Agent Space in us-east-1, connect GitHub/GitLab repositories, enable the relevant repository capabilities, and supply standards as needed.

**Limitations:** This is preview, not a GA release gate. A review recommendation is not proof that a deployment is safe.

**Proposed verification:** Retain CI, policy checks, peer review, and release authorization.

- [S09 · Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)

- [S10 · Release readiness code reviews](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html)

- [S12 · Working with DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent.html)

- [S15 · Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

## C08 · Release QA and integration testing

**Documented function:** Generates and executes exploratory UAT/regression plans against deployed web applications and REST APIs.

**Availability:** Preview · us-east-1

**Prerequisites:** Configure a deployed test target and test profile, necessary authentication/access, safe test data, and any pipeline trigger. Release management preview requires us-east-1.

**Limitations:** Tests can send real write requests and create, modify, or delete application data. This differs from managed code-review verification; it is not a blanket guarantee of coverage.

**Proposed verification:** Review target safety, test intent, side effects, results, coverage gaps, and cleanup.

- [S11 · Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

- [S15 · Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

## Boundary

No live AWS account, workflow, penetration test or cost action was exercised in this scope revision.
