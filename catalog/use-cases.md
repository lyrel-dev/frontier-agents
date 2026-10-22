# Day-to-Day Use Case Catalog

Day-to-day use cases for AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent. Delivery mode distinguishes built-in functions, configured workflows, controlled actions and team-composed procedures.

Delivery mode distinguishes native functions, configured workflows, controlled actions and team-composed procedures.

## AWS DevOps Agent

### Incident operations

#### D-UC01 — Incident signal triage

Classify an incoming alert or ticket as linked to existing work, skipped by an approved rule, or eligible for a new investigation.

**Delivery:** Built-in function. **Cadence:** Event-driven. **Availability:** GA production operations.

**Inputs and prerequisites:** Incident identity, correlation evidence, skip criteria and active investigations.

**Reviewable output:** Triage decision, reason and resulting investigation linkage.

**Constraint:** A triage decision is not a diagnosis. Incorrect linking or skipping requires a routing correction.

**Example request:** Explain why this alert was linked, skipped or scheduled for a new investigation.

**Canonical sections:** [D-06](../guides/devops.html#D-06)

**Official sources:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

#### D-UC02 — Root-cause investigation

Correlate available metrics, logs, traces, code changes, deployment history and topology for a scoped production incident.

**Delivery:** Built-in function. **Cadence:** Event-driven or on demand. **Availability:** GA production operations.

**Inputs and prerequisites:** Incident signal, service scope, UTC window, connected telemetry and deployment context.

**Reviewable output:** Investigation record with observations, hypotheses, root-cause versions and evidence.

**Constraint:** The output remains an investigation result to verify against current source data.

**Example request:** Investigate the checkout 5xx increase for the stated service and UTC window; separate observations, hypotheses and missing data.

**Canonical sections:** [D-01](../guides/devops.html#D-01), [D-06](../guides/devops.html#D-06)

**Official sources:** [DS01](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html), [DS02](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html), [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html), [DS18](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

#### D-UC03 — Investigation steering and hypothesis review

Provide contrary evidence or missing context during an active investigation and obtain a revised analysis.

**Delivery:** Built-in function. **Cadence:** On demand. **Availability:** GA production operations.

**Inputs and prerequisites:** Active investigation, operator question, new evidence or rejected hypothesis.

**Reviewable output:** Updated investigation or root-cause version that records the steering input.

**Constraint:** Steering changes analysis; it does not authorize a production action.

**Example request:** The database pool is healthy. Re-evaluate the upstream dependency hypothesis and cite the current evidence.

**Canonical sections:** [D-06](../guides/devops.html#D-06)

**Official sources:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

#### D-UC04 — Mitigation plan preparation

Produce a reviewable mitigation candidate with target, expected effect, risks, rollback and verification steps.

**Delivery:** Built-in function. **Cadence:** On demand. **Availability:** GA production operations.

**Inputs and prerequisites:** Reviewed incident evidence and a specific operational objective.

**Reviewable output:** Mitigation proposal suitable for operator approval or normal runbook execution.

**Constraint:** A proposal is not permission to execute. Unsupported or high-risk actions remain outside the action path.

**Example request:** Propose the lowest-risk mitigation, including blast radius, rollback and recovery checks.

**Canonical sections:** [D-06](../guides/devops.html#D-06), [D-M06](../guides/devops.html#D-M06)

**Official sources:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html), [DS16](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

#### D-UC05 — Approved directed mitigation

Execute an eligible state-changing AWS or connected-tool operation after layered enablement and exact operator approval.

**Delivery:** Controlled action. **Cadence:** On demand. **Availability:** GA operations; directed actions require opt-in.

**Inputs and prerequisites:** Directed-action enablement, eligible role or integration, correct tool classification and exact operation/resource approval.

**Reviewable output:** Attributed action record and independently checked resulting state.

**Constraint:** Approval is scoped to a particular operation and resource. Tool misclassification can change expected approval behavior.

**Example request:** After showing the exact target and parameters, request approval for the narrowly scoped change.

**Canonical sections:** [D-M06](../guides/devops.html#D-M06)

**Official sources:** [DS16](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

### Health reporting and reviews

#### D-UC06 — On-demand service health query

Answer a scoped operational question using current and historical telemetry, alarms, deployments and incident context.

**Delivery:** Built-in function. **Cadence:** On demand. **Availability:** GA production operations.

**Inputs and prerequisites:** Service identity, reporting window and connected metrics/logs/alarms/deployment sources.

**Reviewable output:** Timestamped health answer with source scope and missing signals.

**Constraint:** A conversational health answer does not replace monitoring or prove complete signal coverage.

**Example request:** Summarize checkout health for the previous 60 minutes and state every unavailable signal.

**Canonical sections:** [D-01](../guides/devops.html#D-01), [D-05](../guides/devops.html#D-05)

**Official sources:** [DS01](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html), [DS02](https://docs.aws.amazon.com/devopsagent/latest/userguide/getting-started-with-aws-devops-agent-creating-an-agent-space.html), [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html), [DS18](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

#### D-UC07 — Minute-by-minute incident status report

Generate a concise rolling update for an active incident from current logs, metrics and investigation state.

**Delivery:** Configured custom agent. **Cadence:** On demand or short schedule. **Availability:** GA custom agents.

**Inputs and prerequisites:** Custom agent, selected telemetry and incident tools, explicit five- or ten-minute window and output contract.

**Reviewable output:** Delta-focused status update: changed observations, open hypotheses, owner and next check.

**Constraint:** This is a configured workflow, not a native fixed-cadence report. Schedule cadence and data window are separate.

**Example request:** Every five minutes, report only what changed in the active checkout incident and name the next verification step.

**Canonical sections:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07)

**Official sources:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

#### D-UC08 — Daily or weekly service health report

Produce a recurring report covering service health, incidents, deployments, trends and missing data.

**Delivery:** Configured custom agent. **Cadence:** Scheduled. **Availability:** GA custom agents.

**Inputs and prerequisites:** Named services, reporting period, selected tools, reporting standard and recipients.

**Reviewable output:** Structured health report or artifact with evidence links and data-quality notes.

**Constraint:** The agent can report only from attached memory and selected tools. A schedule does not define report scope by itself.

**Example request:** Generate the weekly payments health report for complete UTC days, including error, latency, incidents, deployments and data gaps.

**Canonical sections:** [D-07](../guides/devops.html#D-07), [D-M07](../guides/devops.html#D-M07)

**Official sources:** [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

#### D-UC09 — Deployment and change activity report

Summarize deployments, failed releases, rollback events and affected services over a defined period.

**Delivery:** Configured custom agent. **Cadence:** On demand or scheduled. **Availability:** GA custom agents.

**Inputs and prerequisites:** CI/CD integration, service ownership, revision identifiers and complete reporting window.

**Reviewable output:** Deployment report with revisions, outcomes, affected services and unresolved follow-up.

**Constraint:** Requires connected pipeline tools and explicit interpretation of deployment states.

**Example request:** List production deployments in the last seven complete days, including failed changes and linked incidents.

**Canonical sections:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07)

**Official sources:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

#### D-UC10 — Operational review pack

Assemble a weekly or monthly review combining service health, incident trends, prevention work, deployments and action owners.

**Delivery:** Configured custom agent. **Cadence:** Scheduled. **Availability:** GA custom agents.

**Inputs and prerequisites:** Review template, selected data sources, attached reporting context and named audience.

**Reviewable output:** Review agenda, evidence summary, decisions required and owned follow-up.

**Constraint:** This is a team-defined workflow. The report contract, recipients and stop owner must be configured.

**Example request:** Prepare the weekly operational review pack with health, incidents, improvements, deployments, decisions and owners.

**Canonical sections:** [D-07](../guides/devops.html#D-07), [D-M07](../guides/devops.html#D-M07)

**Official sources:** [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS10](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

### Pattern analysis and improvement

#### D-UC11 — Incident pattern identification

Analyze investigation history to identify recurring causes, similar incidents and systemic operational themes.

**Delivery:** Built-in function. **Cadence:** Periodic or on demand. **Availability:** GA production operations.

**Inputs and prerequisites:** Recent investigation history and managed learning context.

**Reviewable output:** Pattern summary, recurring-cause context and candidate prevention themes.

**Constraint:** Historical similarity does not establish the cause of a new incident.

**Example request:** Identify recurring checkout incident patterns and cite the investigations that support each pattern.

**Canonical sections:** [D-M01](../guides/devops.html#D-M01), [D-06](../guides/devops.html#D-06)

**Official sources:** [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html), [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

#### D-UC12 — Prevention recommendation backlog

Review, prioritize and track recommendations across observability, infrastructure, governance and code optimization.

**Delivery:** Built-in function. **Cadence:** Weekly or on demand. **Availability:** GA production operations.

**Inputs and prerequisites:** Multiple incident investigations, team priorities and recommendation evaluation.

**Reviewable output:** Ranked recommendations with source incidents, expected effect and backlog state.

**Constraint:** Recommendations are not automatically implemented and may age out when not kept or implemented.

**Example request:** Run a prevention evaluation and return the highest-priority recommendations with affected incidents and owners.

**Canonical sections:** [D-06](../guides/devops.html#D-06)

**Official sources:** [DS08](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html), [DS15](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

### Knowledge and documentation

#### D-UC13 — Recurring root-cause recall

Use monitor-specific memory from previous investigations as contextual evidence in a later incident.

**Delivery:** Built-in mechanism. **Cadence:** Event-driven. **Availability:** GA managed memory.

**Inputs and prerequisites:** Prior completed investigations, active monitor memory and current incident evidence.

**Reviewable output:** Retrieved historical context considered alongside current telemetry.

**Constraint:** Memory existence, retrieval and diagnostic correctness are separate observations.

**Example request:** Compare this alarm with relevant prior causes, then list the current evidence that supports or contradicts each one.

**Canonical sections:** [D-M01](../guides/devops.html#D-M01)

**Official sources:** [DS07](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

#### D-UC14 — SOP consolidation into reusable skills

Convert an approved operational procedure into a targeted skill with applicability rules and supporting references.

**Delivery:** Composed workflow. **Cadence:** On demand. **Availability:** GA skills.

**Inputs and prerequisites:** Reviewed SOP, target agent types, actual tool names and expected evidence.

**Reviewable output:** Version-controlled SKILL.md bundle and a matching/nonmatching selection test.

**Constraint:** Consolidation and review are team work. A skill supplies procedure; it does not grant tools or permissions.

**Example request:** Create a skill from the approved checkout timeout SOP and state when it should and should not load.

**Canonical sections:** [D-M04](../guides/devops.html#D-M04)

**Official sources:** [DS11](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

#### D-UC15 — Standing operational policy

Apply always-on guidance such as evidence formatting, escalation or safety rules to new sessions.

**Delivery:** Configured knowledge. **Cadence:** Per session. **Availability:** GA instructions.

**Inputs and prerequisites:** Reviewed global or agent-specific AGENTS.md content.

**Reviewable output:** New sessions that include the standing guidance.

**Constraint:** Instructions guide behavior but do not enforce IAM authorization. Existing sessions retain their startup content.

**Example request:** Apply the evidence-output contract to new incident RCA sessions and compare with an existing session.

**Canonical sections:** [D-M03](../guides/devops.html#D-M03)

**Official sources:** [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS09](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html)

#### D-UC16 — Topology documentation and dependency map

Use discovered resources and inferred relationships to document service, repository, pipeline and dependency context.

**Delivery:** Built-in function with composed documentation. **Cadence:** On demand or refreshed. **Availability:** GA production operations.

**Inputs and prerequisites:** Connected accounts, discovery, Resource Explorer where applicable and relevant integrations.

**Reviewable output:** Topology view and environment summary that can support architecture documentation.

**Constraint:** Topology is a representation, not an authorization boundary or guaranteed complete inventory.

**Example request:** Document the payments service containers, downstream dependencies, repositories and deployment boundaries; mark inferred relationships.

**Canonical sections:** [D-05](../guides/devops.html#D-05)

**Official sources:** [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

#### D-UC17 — Environment summary and topology refresh

Refresh learned environment understanding after integration or infrastructure changes and inspect the new version.

**Delivery:** Built-in mechanism. **Cadence:** On demand or platform-managed. **Availability:** GA production operations.

**Inputs and prerequisites:** Changed resources or integrations and managed learning capability.

**Reviewable output:** Updated environment summary, topology and versioned knowledge.

**Constraint:** A refresh request is not completion evidence. Managed learning schedules are platform-owned.

**Example request:** Refresh the environment understanding after the new inventory integration and report the resulting version and changed relationships.

**Canonical sections:** [D-05](../guides/devops.html#D-05)

**Official sources:** [DS04](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html), [DS06](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html), [DS19](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

### Custom operational work

#### D-UC18 — Configuration audit

Periodically compare selected resource configurations with organizational standards and produce findings.

**Delivery:** Configured custom agent. **Cadence:** Scheduled. **Availability:** GA custom agents.

**Inputs and prerequisites:** Read-only configuration tools, approved standard, selected resource scope and report format.

**Reviewable output:** Audit findings with resource identifiers, rule and observed value.

**Constraint:** Requires explicit tools and standards. It is not a built-in universal compliance engine.

**Example request:** Audit staging security-group and logging settings against the attached operations standard; do not change resources.

**Canonical sections:** [D-07](../guides/devops.html#D-07), [D-M04](../guides/devops.html#D-M04)

**Official sources:** [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html), [DS11](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

#### D-UC19 — Metrics and error trend analysis

Analyze a defined time series for trend, seasonality, error-pattern or capacity changes.

**Delivery:** Configured custom agent. **Cadence:** On demand or scheduled. **Availability:** GA custom agents.

**Inputs and prerequisites:** Selected metric/log tools, complete time range, aggregation and comparison basis.

**Reviewable output:** Trend report with material changes, possible explanations and missing evidence.

**Constraint:** The workflow must define aggregation and avoid treating correlation as cause.

**Example request:** Analyze checkout latency and error trends for the last four complete weeks and identify material changes.

**Canonical sections:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07)

**Official sources:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

#### D-UC20 — Cross-tool operational correlation

Combine observability, deployment, ticketing and AWS resource data to answer a bounded operational question.

**Delivery:** Configured custom agent. **Cadence:** On demand. **Availability:** GA custom agents.

**Inputs and prerequisites:** Selected tools from multiple providers, shared identifiers and explicit question.

**Reviewable output:** Evidence table linking signals across systems and unresolved mismatches.

**Constraint:** Tool availability and identity mapping must be explicit; similar timestamps do not prove causality.

**Example request:** Correlate the error increase with deployments, alerts and tickets using service and revision identifiers.

**Canonical sections:** [D-03](../guides/devops.html#D-03), [D-07](../guides/devops.html#D-07)

**Official sources:** [DS03](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html), [DS12](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html), [DS13](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

### Release and change assurance

#### D-UC21 — Release readiness review

Review a proposed code change, dependencies and operational risk before release.

**Delivery:** Preview function. **Cadence:** On demand or repository-triggered. **Availability:** Preview; feature and repository eligibility specific.

**Inputs and prerequisites:** Candidate revision, repositories, topology and release context.

**Reviewable output:** Readiness findings, risk explanations and recommended actions.

**Constraint:** Do not apply production-operations GA status to this preview path.

**Example request:** Review the retry-policy change for dependency, IAM, resilience and operational risks.

**Canonical sections:** [D-09](../guides/devops.html#D-09)

**Official sources:** [DS20](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html), [DS21](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

#### D-UC22 — Active release testing

Exercise a deployed web application or API in an authorized test environment and record observed behavior.

**Delivery:** Preview function. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Disposable staging target, test identities, disabled external effects and explicit allowed operations.

**Reviewable output:** Test results, reproduction detail and residual risk.

**Constraint:** Requests can create, modify or delete application data. Infrastructure write controls do not make application testing read-only.

**Example request:** Test the staging checkout API with synthetic data; avoid production endpoints and external notifications.

**Canonical sections:** [D-09](../guides/devops.html#D-09)

**Official sources:** [DS20](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html), [DS21](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

## AWS Security Agent

### Application assessment

#### S-UC01 — On-demand application penetration test

Run an authorized application-focused penetration test against configured non-production targets.

**Delivery:** Native assessment. **Cadence:** On demand. **Availability:** GA on-demand penetration testing.

**Inputs and prerequisites:** Agent Space, verified target, written authority, test data and stop owner.

**Reviewable output:** Assessment run with findings, evidence and coverage record.

**Constraint:** Testing sends real requests and can change application state. Domain verification is not sufficient authorization.

**Example request:** Run the authorized staging penetration test with the stated target, exclusions and test identities.

**Canonical sections:** [S-01](../guides/security.html#S-01), [S-03](../guides/security.html#S-03), [S-04](../guides/security.html#S-04)

**Official sources:** [SS01](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html), [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS06](https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html), [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS10](https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html), [SS11](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

#### S-UC02 — Authenticated workflow assessment

Assess protected application routes using representative test identities and current login instructions.

**Delivery:** Configured assessment. **Cadence:** On demand. **Availability:** GA penetration testing.

**Inputs and prerequisites:** Credential strategy, login instructions, protected routes and representative roles.

**Reviewable output:** Findings and coverage tied to the actual authenticated identity.

**Constraint:** Credential retrieval and application authentication are separate steps.

**Example request:** Assess the invoice workflow as the test customer role and record the identity and routes reached.

**Canonical sections:** [S-M01](../guides/security.html#S-M01), [S-03](../guides/security.html#S-03)

**Official sources:** [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html), [SS06](https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html), [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html)

#### S-UC03 — Private application assessment

Assess an authorized application reachable only through configured VPC connectivity.

**Delivery:** Configured assessment. **Cadence:** On demand. **Availability:** GA penetration testing.

**Inputs and prerequisites:** Target rules, VPC route, DNS, security groups and application credentials.

**Reviewable output:** Reachability record and assessment findings for the private target.

**Constraint:** Private reachability does not broaden the authorized target list or credential scope.

**Example request:** Assess the private staging endpoint and confirm that the production callback remains out of scope.

**Canonical sections:** [S-03](../guides/security.html#S-03), [S-M01](../guides/security.html#S-M01)

**Official sources:** [SS06](https://docs.aws.amazon.com/securityagent/latest/userguide/troubleshooting.html), [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

#### S-UC04 — Recurring penetration test

Run the same saved penetration-test configuration on a recurring schedule to obtain separate assessment runs.

**Delivery:** Configured assessment. **Cadence:** Scheduled. **Availability:** Feature-specific; verify current availability.

**Inputs and prerequisites:** Stable saved configuration, current test credentials, authorized target and schedule.

**Reviewable output:** Separate scheduled run records and findings.

**Constraint:** Each run reflects the then-current target and credentials; a schedule does not guarantee successful authentication.

**Example request:** Schedule the staging penetration test weekly and retain each run as a separate evidence record.

**Canonical sections:** [S-04](../guides/security.html#S-04)

**Official sources:** [SS07](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-penetration-test.html), [SS08](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html), [SS10](https://docs.aws.amazon.com/securityagent/latest/userguide/quotas.html), [SS11](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

### Authentication and access

#### S-UC05 — Login procedure reuse

Reuse a previously successful authentication navigation workflow in later test sessions and runs.

**Delivery:** Native mechanism. **Cadence:** Per session/run. **Availability:** GA penetration testing.

**Inputs and prerequisites:** At least one successful login, saved penetration-test configuration and Login Optimization enabled.

**Reviewable output:** Reused login skill and observed authenticated identity.

**Constraint:** The learned procedure concerns login navigation, not general vulnerability learning.

**Example request:** Compare first-run and later login behavior, then verify the actual application role.

**Canonical sections:** [S-M02](../guides/security.html#S-M02)

**Official sources:** [SS09](https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html)

### Findings and remediation

#### S-UC06 — Finding review and prioritization

Review impact, confidence, reproduction steps, affected data and business context before disposition.

**Delivery:** Native operation. **Cadence:** On demand. **Availability:** Feature-specific.

**Inputs and prerequisites:** Completed assessment findings and application-owner context.

**Reviewable output:** Prioritized finding with owner, disposition and remediation plan.

**Constraint:** Finding count or severity alone is not an adequate risk decision.

**Example request:** Prioritize the findings using impact, confidence, affected role and reproduction evidence.

**Canonical sections:** [S-05](../guides/security.html#S-05)

**Official sources:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS12](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html)

#### S-UC07 — Jira remediation tracking

Create a Jira issue for an accepted finding and keep remediation and revalidation updates linked.

**Delivery:** Configured integration. **Cadence:** On demand. **Availability:** Feature-specific.

**Inputs and prerequisites:** Finding, connected Jira project and approved disclosure scope.

**Reviewable output:** Jira issue linked to the finding, with later revalidation comments when supported.

**Constraint:** Sensitive assessment details should not be published to an inappropriate project or audience.

**Example request:** Create a Jira issue for this accepted finding with the evidence, affected revision and acceptance test.

**Canonical sections:** [S-05](../guides/security.html#S-05)

**Official sources:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS12](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html)

#### S-UC08 — Proposed code remediation

Generate a repository change proposal for an accepted finding and send it through normal engineering review.

**Delivery:** Configured remediation. **Cadence:** On demand. **Availability:** Feature-specific; provider support applies.

**Inputs and prerequisites:** Accepted finding, repository access and remediation configuration.

**Reviewable output:** Patch or pull request linked to the finding.

**Constraint:** A proposed patch is not a reviewed, deployed or verified repair.

**Example request:** Prepare a remediation change for the authorization finding and include tests; do not merge automatically.

**Canonical sections:** [S-05](../guides/security.html#S-05)

**Official sources:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS12](https://docs.aws.amazon.com/securityagent/latest/userguide/remediate-finding.html)

#### S-UC09 — Finding revalidation

Retest selected existing findings after the repair is deployed to the original authorized target.

**Delivery:** Native operation. **Cadence:** On demand. **Availability:** GA penetration testing.

**Inputs and prerequisites:** Completed original finding, deployed repair and current authentication configuration.

**Reviewable output:** Separate revalidation job linked to the original finding with Active or Resolved result.

**Constraint:** Revalidation does not rediscover unrelated vulnerabilities or establish whole-application security.

**Example request:** Revalidate the selected finding against the deployed revision and record the actual test identity.

**Canonical sections:** [S-M05](../guides/security.html#S-M05)

**Official sources:** [SS13](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

### Shift-left review

#### S-UC10 — Repository code review

Analyze a configured repository or supported source package for vulnerabilities and enabled security requirements.

**Delivery:** Preview assessment. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Connected repository or S3 source, review mode and applicable requirement packs.

**Reviewable output:** Code findings with evidence, location and possible remediation.

**Constraint:** Provider, source and availability limits apply. Completed review is not complete application coverage.

**Example request:** Review the repository for vulnerability findings and the enabled authorization requirements.

**Canonical sections:** [S-06](../guides/security.html#S-06), [S-M03](../guides/security.html#S-M03)

**Official sources:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

#### S-UC11 — Change-focused code review

Assess a pull request, merge request or differential source so findings are tied to a specific change.

**Delivery:** Preview assessment. **Cadence:** Event-triggered or on demand. **Availability:** Preview.

**Inputs and prerequisites:** Supported change event or differential source, repository context and criteria.

**Reviewable output:** Revision-specific findings and optional remediation path.

**Constraint:** Subsequent changes may require a new review; support differs by provider and trigger path.

**Example request:** Review this change for security findings and enabled requirements; identify the exact revision.

**Canonical sections:** [S-06](../guides/security.html#S-06)

**Official sources:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

#### S-UC12 — Security requirement evaluation

Evaluate design or code evidence against reviewed applicability and compliance criteria.

**Delivery:** Configured criteria. **Cadence:** On demand. **Availability:** Preview workflows.

**Inputs and prerequisites:** Enabled requirement pack and eligible assessment configured for requirement evaluation.

**Reviewable output:** Requirement-level compliant, violating or inapplicable result.

**Constraint:** A framework or generated pack is not a compliance certification.

**Example request:** Evaluate the ownership-check requirement and show why it is applicable, compliant or violated.

**Canonical sections:** [S-M03](../guides/security.html#S-M03)

**Official sources:** [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

#### S-UC13 — Security requirement consolidation

Generate or consolidate a requirement pack from authoritative policy documents and review the replacement before enablement.

**Delivery:** Composed workflow. **Cadence:** On demand. **Availability:** Preview workflows.

**Inputs and prerequisites:** Governed policy sources, existing pack and reviewer.

**Reviewable output:** Reviewed replacement requirement pack and external change record.

**Constraint:** Regeneration replaces existing requirements, including manual entries. Keep the authoritative source outside the generated pack.

**Example request:** Regenerate the pack from the approved policy documents and identify which existing requirements would be replaced.

**Canonical sections:** [S-M04](../guides/security.html#S-M04)

**Official sources:** [SS14](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html), [SS15](https://docs.aws.amazon.com/securityagent/latest/userguide/import-security-requirements.html)

#### S-UC14 — Design review

Assess a design document against security requirements before implementation or release.

**Delivery:** Preview assessment. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Current design material, application context and enabled requirement packs.

**Reviewable output:** Design findings and reviewed assumptions.

**Constraint:** Design review uses a different one-off lifecycle from reusable run configurations.

**Example request:** Review the new payment design against the enabled security requirements and list unsupported assumptions.

**Canonical sections:** [S-06](../guides/security.html#S-06)

**Official sources:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

#### S-UC15 — Threat modeling

Build and review a threat model from connected architecture and scope material.

**Delivery:** Preview assessment. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Architecture documents, code/context sources and explicit system boundary.

**Reviewable output:** Assets, trust boundaries, flows, threats and model findings.

**Constraint:** Inferred system context requires review; the model is not a complete guarantee of threat coverage.

**Example request:** Create a threat model for the checkout service and mark inferred flows that require owner confirmation.

**Canonical sections:** [S-06](../guides/security.html#S-06)

**Official sources:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

### Program operations

#### S-UC16 — CI/CD assessment integration

Start a previously configured assessment from a delivery workflow and record the server-side job result.

**Delivery:** Configured integration. **Cadence:** Pipeline-triggered. **Availability:** Preview.

**Inputs and prerequisites:** Saved assessment configuration, pipeline credentials and explicit pass/fail policy.

**Reviewable output:** Assessment job and auditable delivery decision.

**Constraint:** The pipeline runner is not the assessment engine. Missing or inconclusive evidence needs an explicit gate policy.

**Example request:** Start the configured staging assessment from the release pipeline and fail safely on missing evidence.

**Canonical sections:** [S-06](../guides/security.html#S-06)

**Official sources:** [SS03](https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html), [SS05](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-code-review.html), [SS16](https://docs.aws.amazon.com/securityagent/latest/userguide/quickstart-threat-model.html), [SS17](https://docs.aws.amazon.com/securityagent/latest/userguide/review-code-findings-github.html)

## AWS FinOps Agent

### Cost inquiry and reporting

#### F-UC01 — Natural-language cost inquiry

Ask a bounded cost question in plain language using authorized cost and usage data.

**Delivery:** Native function. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Dates, cost metric, currency, account scope and requested dimension.

**Reviewable output:** Answer with figures, filters and source context.

**Constraint:** A fluent answer is not a substitute for a reproducible source query.

**Example request:** Show production storage cost for the last complete week by account and Region; state the metric and filters.

**Canonical sections:** [F-M01](../guides/finops.html#F-M01)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html)

#### F-UC02 — Cost variance decomposition

Compare complete periods and quantify the service, usage or rate components contributing to the change.

**Delivery:** Native function. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Comparable windows, same cost basis, grouping dimensions and source permissions.

**Reviewable output:** Reconciled delta and ranked contributors.

**Constraint:** Contribution arithmetic does not by itself establish the operational cause.

**Example request:** Compare the last two complete weeks and decompose the cost delta into usage and rate changes.

**Canonical sections:** [F-M01](../guides/finops.html#F-M01), [F-U01](../guides/finops.html#F-U01)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html)

#### F-UC03 — Cost breakdown by ownership dimension

Group cost by account, service, Region, tag or organization-specific owner mapping.

**Delivery:** Native function with context. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Authorized cost data, grouping dimension and optional context file mapping.

**Reviewable output:** Dimensioned totals and unmapped items.

**Constraint:** Owner mappings require maintained context; tags and account metadata may be incomplete.

**Example request:** Break down this cost by service owner and list every unmapped account or tag.

**Canonical sections:** [F-M01](../guides/finops.html#F-M01), [F-M02](../guides/finops.html#F-M02)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html), [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html)

#### F-UC04 — Forecast and commitment coverage review

Review forecasts or commitment coverage as separate analytical questions from historical cost.

**Delivery:** Native function. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Forecast horizon, commitment scope and relevant upstream source.

**Reviewable output:** Forecast or coverage summary with assumptions.

**Constraint:** Forecast and recommendation values are not observed spend and should not be combined without qualification.

**Example request:** Summarize the next-month forecast and current commitment coverage; separate observed and projected values.

**Canonical sections:** [F-M01](../guides/finops.html#F-M01)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html)

#### F-UC05 — Daily, weekly or monthly cost report

Generate a recurring cost report with a fixed basis, sections, audience and downloadable artifact.

**Delivery:** Configured recurring task. **Cadence:** Scheduled. **Availability:** Preview.

**Inputs and prerequisites:** Report contract, schedule, source scope, context and recipients.

**Reviewable output:** HTML, PDF or editable presentation artifact.

**Constraint:** Schedule, source window and audience are separate settings. Report values still require reconciliation.

**Example request:** Create a weekly cost report with service totals, anomalies, recommendations, owners and unresolved gaps.

**Canonical sections:** [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04)

**Official sources:** [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS11](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)

#### F-UC06 — FinOps operational review pack

Assemble a cross-functional review of cost movement, anomalies, recommendations, decisions and measured outcomes.

**Delivery:** Composed workflow. **Cadence:** Scheduled. **Availability:** Preview.

**Inputs and prerequisites:** Recurring report, owner mappings, recommendation status and review template.

**Reviewable output:** Review agenda, decision log and owner/action table.

**Constraint:** The review process and acceptance criteria are team-defined, not a separate native feature.

**Example request:** Prepare the monthly FinOps review pack with decisions required, owners and prior action outcomes.

**Canonical sections:** [F-03](../guides/finops.html#F-03), [F-04](../guides/finops.html#F-04), [F-M02](../guides/finops.html#F-M02)

**Official sources:** [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS11](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html), [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

### Anomaly and optimization

#### F-UC07 — On-demand cost anomaly investigation

Investigate a detected cost anomaly and rank root causes by cost impact.

**Delivery:** Native function. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Cost Anomaly Detection record, Cost Explorer access and optional CloudTrail permission.

**Reviewable output:** Anomaly explanation with affected services, usage/rate analysis and correlated changes.

**Constraint:** CloudTrail events are correlated activity, not automatic proof of cause.

**Example request:** Investigate the MemoryDB anomaly and separate usage, rate and correlated change evidence.

**Canonical sections:** [F-M01](../guides/finops.html#F-M01)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html)

#### F-UC08 — Event-triggered anomaly response

Automatically create a task when a matching cost anomaly event occurs and publish or retain the result.

**Delivery:** Configured automation. **Cadence:** Event-driven. **Availability:** Preview.

**Inputs and prerequisites:** Anomaly monitor, event-rule permission, automation condition and optional destination.

**Reviewable output:** Task history, investigation result and delivery status.

**Constraint:** The documented event source is Cost Anomaly Detection. Removing the automation stops future tasks, not existing records.

**Example request:** When a production anomaly exceeds the threshold, investigate it and post the result to the approved channel.

**Canonical sections:** [F-M05](../guides/finops.html#F-M05), [F-03](../guides/finops.html#F-03)

**Official sources:** [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS07](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

#### F-UC09 — Optimization recommendation triage

Review upstream optimization recommendations against service constraints and overlapping estimates.

**Delivery:** Native function with team review. **Cadence:** On demand. **Availability:** Preview.

**Inputs and prerequisites:** Cost Optimization Hub or Compute Optimizer recommendation, workload evidence and owner constraints.

**Reviewable output:** Prioritized candidate, rejected/deferred reason and accepted next step.

**Constraint:** The agent contextualizes upstream recommendations; it does not independently calculate or authorize the change.

**Example request:** Review the storage recommendations, identify overlapping savings and list the reliability constraints.

**Canonical sections:** [F-M01](../guides/finops.html#F-M01)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html)

#### F-UC10 — Post-change savings measurement

Measure an independently authorized change using comparable cost and service-health windows.

**Delivery:** Composed workflow. **Cadence:** Periodic after change. **Availability:** Preview service; team process.

**Inputs and prerequisites:** Implemented change record, comparable periods and service indicators.

**Reviewable output:** Measured outcome with attribution limits.

**Constraint:** A lower bill does not prove the change caused the decrease; traffic, prices and allocation may differ.

**Example request:** Compare the post-change period with a matched baseline and state what cannot be attributed to the change.

**Canonical sections:** [F-U01](../guides/finops.html#F-U01), [F-M01](../guides/finops.html#F-M01)

**Official sources:** [FS01](https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html), [FS03](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS14](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html)

### Context and governance

#### F-UC11 — Cost ownership and allocation context

Provide account-to-team mappings, reporting basis and organizational conventions through maintained reference files.

**Delivery:** Configured context. **Cadence:** As needed. **Availability:** Preview.

**Inputs and prerequisites:** Supported context file with non-sensitive ownership and allocation data.

**Reviewable output:** Context available to relevant tasks and conversations.

**Constraint:** Files are visible to agent users, cannot be conversationally rewritten and have file/total size limits.

**Example request:** Use the approved account-owner mapping and list every cost item that lacks an owner.

**Canonical sections:** [F-M02](../guides/finops.html#F-M02)

**Official sources:** [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html)

#### F-UC12 — Persistent reporting preferences

Retain non-sensitive preferences, corrections and owner details across conversations.

**Delivery:** Native memory. **Cadence:** Across sessions. **Availability:** Preview.

**Inputs and prerequisites:** Explicit remember, update or forget request.

**Reviewable output:** Agent-instance memory applied in later sessions.

**Constraint:** Memory is distinct from reference files and should be tested independently.

**Example request:** Remember that executive reports use amortized cost and update the preference when the policy changes.

**Canonical sections:** [F-M03](../guides/finops.html#F-M03)

**Official sources:** [FS04](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

### Automation and collaboration

#### F-UC13 — Scheduled recurring task

Create a schedule that produces a new queued task at each interval.

**Delivery:** Configured automation. **Cadence:** Scheduled. **Availability:** Preview.

**Inputs and prerequisites:** Prompt, schedule, tools/data permissions and output expectations.

**Reviewable output:** Automation record and separate task history.

**Constraint:** Deleting an automation stops future starts but does not delete existing tasks or messages.

**Example request:** Run the weekly optimization review every Monday at the stated UTC time.

**Canonical sections:** [F-03](../guides/finops.html#F-03)

**Official sources:** [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html)

#### F-UC14 — Jira follow-up creation

Create an issue or comment that turns a reviewed cost analysis into owned follow-up.

**Delivery:** Configured integration. **Cadence:** On demand or automated. **Availability:** Preview.

**Inputs and prerequisites:** Connected Jira project, reviewed content and owner.

**Reviewable output:** Jira issue/comment and task history.

**Constraint:** Interactive and on-demand Jira actions require approval; automation actions are pre-authorized at setup.

**Example request:** Create a Jira issue for the accepted storage optimization with evidence, owner and acceptance criteria.

**Canonical sections:** [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06)

**Official sources:** [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html), [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

#### F-UC15 — Slack publication

Post a reviewed cost or anomaly summary to a configured Slack channel.

**Delivery:** Configured integration. **Cadence:** On demand or automated. **Availability:** Preview.

**Inputs and prerequisites:** Registered workspace, agent connection, channel and reviewed message scope.

**Reviewable output:** Slack post and delivery result.

**Constraint:** Slack posting has no approval prompt, including interactive use; channel membership and sensitive content must be reviewed.

**Example request:** Post the approved anomaly summary to the FinOps incident channel.

**Canonical sections:** [F-05](../guides/finops.html#F-05), [F-M06](../guides/finops.html#F-M06)

**Official sources:** [FS12](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html), [FS13](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html), [FS05](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html), [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

#### F-UC16 — Downloadable report artifact

Generate, revise and retain a report artifact for review or distribution.

**Delivery:** Native output. **Cadence:** On demand or scheduled. **Availability:** Preview.

**Inputs and prerequisites:** Source query, report instructions and desired format.

**Reviewable output:** HTML, PDF or editable presentation artifact.

**Constraint:** Formatting quality does not establish numerical or causal accuracy; external copies have their own lifecycle.

**Example request:** Generate an editable monthly cost report and include the query basis for every chart.

**Canonical sections:** [F-04](../guides/finops.html#F-04)

**Official sources:** [FS06](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html), [FS08](https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html), [FS10](https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html), [FS11](https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html)
