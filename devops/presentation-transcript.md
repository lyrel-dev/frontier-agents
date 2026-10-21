# AWS DevOps Agent — presentation transcript

35 minutes including 12 minutes of demonstrations. Questions and breaks are additional. Demo budgets are walkthrough allocations, not agent completion guarantees.


## 01. AWS DevOps Agent

**00:00–01:00 · 01:00 allocated**

**Takeaway:** Investigations produce hypotheses and evidence for operational review.

Open with the operational job, not a claim of full autonomy. A checkout service is failing after a deployment. We want a coherent investigation, a defensible mitigation decision, and a follow-up item that prevents recurrence. Production operations are generally available; release-management features are preview. The examples in this deck are proposed exercises. The demo slots include the operator walkthrough and a prepared-result fallback, not a promise that an agent run completes within the allotted minutes.

[D01 — About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)

[D14 — AWS DevOps Agent is now generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-devops-agent-generally-available/)

[D15 — Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


## 02. Define the incident scope and evidence window

**01:00–02:30 · 01:30 allocated**

**Takeaway:** A time window, a service boundary, and a change reference make the question answerable.

Use the checkout incident as the thread through this presentation. Supply an incident window and the deployment identity before asking for a cause. A production symptom, an agent hypothesis, a mitigation plan, and a verified recovery are different artifacts. The example does not assert that a real incident occurred. The on-call engineer remains responsible for triage and for comparing conclusions with the source systems.

[D02 — Production operations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-production-operations-index.html)

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)


## 03. Operational capability groups and their dependencies

**02:30–04:00 · 01:30 allocated**

**Takeaway:** Choose an operational job first; enable its data and action paths second.

The capability map separates incident work, on-demand operational questions, prevention, configured recurring tasks, and release validation. They share application context but differ in invocation and output. A daily summary is a custom-agent configuration, not an automatically provisioned SRE dashboard. Release management is a separate preview track and should not inherit the availability label of production operations.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D04 — Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

[D05 — On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)

[D06 — Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

[D09 — Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)


## 04. Configure Agent Space data access and scope

**04:00–05:30 · 01:30 allocated**

**Takeaway:** Acceptance: one known resource is visible; an out-of-scope test resource is denied.

An Agent Space groups the context and integrations used for operational work. It is not an authorization boundary merely because it has a service name. IAM roles and integration permissions establish actual access. For the initial pilot, connect one service and inspect whether its deployment events, logs, and metrics can be read. Do not grant broad writes to compensate for missing read evidence. Private integrations need an explicit network connection; they are not reachable simply because a repository or tool is named in chat.

[D01 — About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)

[D02 — Production operations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-production-operations-index.html)

[D34 — Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

[D39 — Private connections for integrations](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html)


## 05. Investigate a service incident and review hypotheses

**05:30–07:00 · 01:30 allocated**

**Takeaway:** Acceptance: distinguish observed facts, hypotheses, and missing telemetry.

The agent can start from a manual request or a configured external trigger. As evidence arrives, the operator can steer the investigation toward a hypothesis or data source. That is useful when a dashboard and a deployment suggest different explanations. Ask for the evidence behind a conclusion and for alternatives that remain unresolved. A confident root-cause statement is not sufficient to close an incident.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D05 — On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)


## 06. Demo 1 · investigate checkout 5xx errors

**07:00–14:00 · 07:00 allocated**

**Takeaway:** Use a controlled incident snapshot; keep the investigation read-focused.

This seven-minute slot demonstrates the investigation workflow and the engineer’s judgment. It does not measure incident-response speed. Start a fresh request only if the environment is ready. The completed-run fallback must contain genuine, sanitized evidence from an authorized rehearsal; a schematic illustration must be labeled as such. No production mutation is required for this demo.

**Preflight:** Prepare a sanitized incident snapshot, read access and a completed investigation before presenting.

```text

Investigate the checkout 5xx increase in the supplied UTC window after the deployment. Cite telemetry and the deployed diff. Separate observed facts, competing hypotheses, and missing data. Propose a mitigation; do not change resources.

```

- 01:00 — **Confirm scope:** Open the Agent Space, incident window and deployment reference.

- 01:30 — **Inspect the investigation:** Start or open a pre-run investigation; check source coverage.

- 02:00 — **Challenge the leading hypothesis:** Compare two source observations and inspect a competing explanation.

- 01:30 — **Review mitigation:** Check blast radius, rollback assumptions and missing evidence.

- 01:00 — **Record the handoff:** Capture owner, evidence links, next action and verification check.

**Success:** One source-backed hypothesis and one reviewable next action—not an asserted diagnosis.

**Fallback:** After 60 seconds without usable output, use the completed run and inspect its evidence; do not wait for a fresh run.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D05 — On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)


## 07. Daily service-health and incident queries

**14:00–15:15 · 01:15 allocated**

**Takeaway:** Acceptance: inspect one cited alarm or resource before sharing the summary.

Not every operational task is an incident. The on-demand interface can answer focused questions about service health, resource configuration, recent alarms and investigation history. Ask for a specific period rather than “is everything healthy.” The value is an evidence-linked summary that reduces console navigation. Where a source is unavailable, the answer should state the gap rather than imply coverage.

[D05 — On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)


## 08. Create prevention tasks from investigation history

**15:15–16:30 · 01:15 allocated**

**Takeaway:** Acceptance: an owner and a measurable recurrence or detection check accompany each accepted item.

Prevention analyzes investigation history and produces recommendations. It is not a guarantee that failures will disappear. Keep recommendations separate from accepted engineering work: a team must assess relevance, assign ownership and decide how to validate an improvement. Use a known repeat incident to show how the suggested change would make detection earlier or the service more resilient.

[D04 — Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)


## 09. Configure scheduled operational reports

**16:30–17:45 · 01:15 allocated**

**Takeaway:** Acceptance: the selected tools—not the prompt alone—bound access and side effects.

A custom agent is a configured workflow. For example, a team can define a daily summary that reads alarms and recent investigations and returns an actionable report. Select only the tools needed for that job. A prompt that says “read only” does not neutralize a write-capable integration. Review the output and invocation record before enabling a recurring schedule.

[D06 — Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)


## 10. Mitigation recommendations and action authorization

**17:45–19:45 · 02:00 allocated**

**Takeaway:** Directed actions have their own enablement, role, tool and approval path.

Keep the read-oriented investigation path separate from directed actions. Directed actions are disabled by default. Enabling them is only one layer: the relevant account role or third-party tool configuration must also permit the operation, and the operator must approve the concrete action. Review the target, parameters, blast radius and rollback plan. The release-testing write path is a different mechanism; do not assume this approval model protects application endpoints exercised by a test.

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

[D34 — Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)


## 11. Release-review and deployed-application testing differ

**19:45–21:45 · 02:00 allocated**

**Takeaway:** Managed code verification is not the same as active testing against a deployed application.

Readiness review evaluates a change and can build and test it in a managed verification environment. Active release testing sends traffic to a running application and may perform POST, PUT and DELETE requests. Those operations can trigger real business effects. Use a disposable staging deployment, test identities and disabled external side effects. Both features remain a preview track in the documented Region. A positive review is evidence for the release owner, not a production deployment authorization.

[D09 — Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)

[D10 — Release readiness code reviews](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html)

[D11 — Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

[D15 — Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


## 12. Demo 2 · review a risky release

**21:45–26:45 · 05:00 allocated**

**Takeaway:** A proposed retry-policy and database-timeout change must produce inspectable release evidence.

This five-minute walkthrough demonstrates interpretation rather than a fresh end-to-end run. The reviewed revision must match the displayed diff. Build failures caused by missing private dependencies are setup failures, not proof that the proposed application change is unsafe. Conversely, a skipped verification step is not a pass. Keep the production release decision with the existing owner.

**Preflight:** Use a connected test repository and a pre-completed readiness review; do not point a test profile at production.

```text

Review this change for dependency impact, retry amplification, database saturation and rollback viability. Cite affected code and verification evidence. Return risks and missing checks. Do not deploy or promote.

```

- 00:45 — **Select the change:** Show the PR/MR and its exact commit.

- 01:15 — **Start or open review:** Confirm preview Region and enabled review/verification settings.

- 01:15 — **Inspect risk evidence:** Trace a finding to changed code and a dependency.

- 01:00 — **Read verification:** Separate a passed check, an unrun check and a failure.

- 00:45 — **Decide the next step:** Release owner accepts, requests work or blocks promotion.

**Success:** Findings are tied to the exact change, and unexecuted checks are visible.

**Fallback:** Use the prepared review and code diff if the preview or verification environment is unavailable.

[D09 — Release management](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-release-management-index.html)

[D10 — Release readiness code reviews](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html)

[D15 — Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)


## 13. Access operational context from coding clients

**26:45–28:00 · 01:15 allocated**

**Takeaway:** Acceptance: client connectivity does not widen the Agent Space’s permissions.

The documented remote MCP interface brings operational questions into a development environment. This can reduce the copy-and-paste handoff between an on-call engineer and a developer. It does not mean every AWS frontier agent shares one session or identity. Authenticate the client, scope access and preserve links to the original investigation. A2A and other access methods are integration building blocks, not a turnkey four-product orchestrator.

[D37 — DevOps Agent remote servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/accessing-devops-agent-connecting-to-devops-agent-remote-servers-index.html)

[D38 — Accessing DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html)


## 14. Translate investigation findings into owned work

**28:00–29:30 · 01:30 allocated**

**Takeaway:** A proposed engineering handoff does not transfer production authorization.

This is a proposed team procedure using the documented investigation, mitigation and prevention outputs. It is not a native implementation or deployment feature. The receiving engineers decide whether a change is justified and use their existing repository, test and release controls. Preserve the distinction between an observed symptom, a hypothesis, a recommended action and a verified result.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D04 — Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)


## 15. Verify recovery before closing the incident

**29:30–31:00 · 01:30 allocated**

**Takeaway:** Completion is a service-owner decision supported by current telemetry.

Retain a small closure record with the deployed revision, verification window, observed result and owner. These are proposed team acceptance criteria, not guaranteed product-generated fields. When evidence is missing or the symptom persists, keep the incident open and continue the investigation. The walkthrough does not demonstrate an automated code-change workflow.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D04 — Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

[D05 — On Demand DevOps Tasks](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)


## 16. Pilot a single service with scoped read access

**31:00–32:30 · 01:30 allocated**

**Takeaway:** Prove the read path before expanding automated effects.

Treat deployment readiness as a team decision. Record the feature’s availability, Agent Space Region, data-source access, mutation paths and stop responsibility. For the first service, leave directed actions off unless a separately reviewed experiment requires them. Put release-preview work in a different pilot lane. The documentation specifies behavior; this checklist is the recommended operating design for the team.

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

[D15 — Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

[D34 — Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)


## 17. Pilot metrics require verified engineering results

**32:30–34:00 · 01:30 allocated**

**Takeaway:** Measure review effort and rework for independently accepted outcomes.

The scorecard is a proposal, not an AWS performance claim. Use the same small set of representative tasks before and during the pilot. Measure how much time an engineer spends reaching an evidence-supported hypothesis, how often conclusions need correction, and whether recommended prevention work is accepted. Count service and integration consumption as well as human review effort. Do not infer production MTTR improvement from a staged demo.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D04 — Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

[D06 — Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)


## 18. Accept outcomes only after verification and authorization

**34:00–35:00 · 01:00 allocated**

**Takeaway:** Investigate with context. Gate the effect. Close with independent verification.

Close by asking the team to choose one read-heavy operational workflow and its owner. The agent can help connect evidence and produce useful recommendations, but the engineer remains responsible for the decision and its consequences. Release preview, directed actions and active tests should each be evaluated on their own terms. Questions follow the timed close. The detailed inventory below maps every retained capability to the new presentation so no feature disappears during the restructuring.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

[D11 — Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)
