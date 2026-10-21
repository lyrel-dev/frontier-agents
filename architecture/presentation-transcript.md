# Common architectural patterns — presentation transcript

36 minutes including 8 minutes of demonstrations. Questions and breaks are additional. Demo budgets are walkthrough allocations, not agent completion guarantees.


## 01. Common architectural patterns

**00:00–01:00 · 01:00 allocated**

**Takeaway:** Standardize the work and evidence—not the agent privileges.

This is a team-level reference design assembled from the documented behavior of four products. It is not an AWS internal architecture or a shared four-agent runtime. The common unit is a bounded engineering work item with an owner, evidence, allowed effects and completion checks. Each product retains its own identity, execution and approval model. The demo is a tabletop handoff walkthrough, not an implemented orchestrator.

[D01 — About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[S04 — What is AWS Security Agent?](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

[F03 — Create an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)


## 02. One operating model; four specialist roles

**01:00–02:30 · 01:30 allocated**

**Takeaway:** Assign work by the evidence and result needed, not by a generic “agent” label.

DevOps Agent is the operational investigator, Kiro produces repository work, Security Agent supplies application-security assessment evidence, and FinOps Agent explains and routes cost work. These roles can overlap, but their output artifacts are different. A shared work-item schema makes the handoff legible without claiming shared sessions or permissions. The table is a recommended allocation of responsibility based on documented capabilities.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[F07 — Cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-anomaly-detection.html)


## 03. Use a work contract as the unit of delegation

**02:30–04:00 · 01:30 allocated**

**Takeaway:** A task is ready when its owner, scope, allowed effects and done condition are explicit.

The contract is a team artifact, not a product-specific API. Start with the service, environment and question. Add exact evidence identifiers, allowed effects and non-goals. Name the person who can stop the work and the person who can accept its output. This prevents a vague request such as “fix checkout” from becoming an unlimited mandate. A contract carries intent; underlying product controls still enforce access.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K08 — Specifications](https://kiro.dev/docs/specs/)

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 04. Four handoffs cover most first-pass team needs

**04:00–06:00 · 02:00 allocated**

**Takeaway:** Compose only the specialists needed by the actual job.

An incident can lead to a code change, a security finding to a repair, or a cost anomaly to an infrastructure work item. The daily review aggregates accepted evidence into an owned backlog. Do not force all four agents into every task. Manual artifact handoffs are often sufficient to prove the operating model before building automation. Each row is a proposed team workflow, not a turnkey integration supplied by AWS.

[D04 — Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 05. P01 · bind the workspace to accountable ownership

**06:00–08:00 · 02:00 allocated**

**Takeaway:** A product workspace is not automatically an enforced security boundary.

Use a service-oriented boundary record: accounts, repositories, targets, operators and output destinations. The name of a workspace does not prove that access outside it is denied. Test the actual role, repository integration or target configuration. Keep operator accountability visible even when a service role executes the work. Start with one team-owned workload so failures in the boundary model can be detected before wider adoption.

[D34 — Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

[K06 — GitHub integration](https://kiro.dev/docs/web/github/)

[S08 — Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

[F03 — Create an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)


## 06. P02 · retain provenance with every conclusion

**08:00–09:30 · 01:30 allocated**

**Takeaway:** An answer must carry enough context to be checked after it leaves the original interface.

A source link alone can be insufficient when the source changes. Record the revision or time interval, resource identity and relevant filters along with the conclusion. Distinguish observed evidence from an agent inference and a human decision. This is especially important in cost reports, where a different basis or date range can produce a different number, and in code work, where a later commit can invalidate an earlier check.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K03 — Working with the agent](https://kiro.dev/docs/web/using-the-agent/)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)


## 07. P03 · keep instructions separate from authorization

**09:30–11:00 · 01:30 allocated**

**Takeaway:** Guidance changes behavior; credentials and technical controls determine possible effects.

Steering, skills, memory and context files improve relevance. They must not be treated as permission boundaries or proof of policy enforcement. Treat source content as evidence, not as authority to ignore the task’s restrictions. Keep secrets out of context artifacts unless the approved workflow specifically requires them. When stable policy and learned context conflict, verify current policy and correct the context.

[K13 — Steering](https://kiro.dev/docs/steering/)

[K14 — Memory](https://kiro.dev/docs/memory/)

[D06 — Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

[F12 — Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)


## 08. P05 · classify the effect before selecting the gate

**11:00–13:00 · 02:00 allocated**

**Takeaway:** Approval is product- and entry-point-specific.

A single “human in the loop” box hides important differences. DevOps directed actions require explicit enablement and approval. Active release tests can mutate a target through application requests. Kiro’s output reaches a reviewable branch, with merging under team control. FinOps collaboration writes have trigger-dependent approval rules. Model the real effect and apply the correct gate; do not assume a prompt before every mutation.

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

[D11 — Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 09. P06 · isolate the worker and the target

**13:00–14:30 · 01:30 allocated**

**Takeaway:** An isolated execution environment can still affect systems it can reach.

Worker isolation reduces some risks, but it does not neutralize network side effects. A test may submit a form that charges a payment or sends a notification, and a sandbox command can use injected credentials. Design the target as carefully as the worker: synthetic data, disposable credentials, allowed endpoints, disabled business side effects and independent health checks. These are recommended controls around the documented execution paths.

[K10 — Cloud sandbox](https://kiro.dev/docs/web/sandbox/)

[K19 — Sandbox internet access](https://kiro.dev/docs/web/sandbox/internet-access/)

[K20 — Environment variables and secrets](https://kiro.dev/docs/web/sandbox/environment-variables/)

[D11 — Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)


## 10. P07 · integrate through explicit adapters

**14:30–16:00 · 01:30 allocated**

**Takeaway:** A protocol or connector is a building block—not a common permission model.

MCP and the documented DevOps remote protocols can expose useful capabilities to clients. Repository and collaboration integrations provide other handoff paths. They still require their own identities, scopes and supported actions. There is no basis here to claim an out-of-the-box orchestrator across all four products. Start with a link or exported artifact, and automate only a documented interface whose failure modes the team can operate.

[D37 — DevOps Agent remote servers](https://docs.aws.amazon.com/devopsagent/latest/userguide/accessing-devops-agent-connecting-to-devops-agent-remote-servers-index.html)

[D38 — Accessing DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html)

[K15 — Model Context Protocol](https://kiro.dev/docs/mcp/)

[S26 — Code review from an IDE](https://docs.aws.amazon.com/securityagent/latest/userguide/code-review-ide-integration.html)

[F13 — Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

[F14 — Slack integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)


## 11. P08 · hand off artifacts, not inherited authority

**16:00–18:00 · 02:00 allocated**

**Takeaway:** The next specialist receives evidence and scope—not credentials or another agent’s approval.

The sample handoff is deliberately product-neutral. Keep the work-item ID, owner and original evidence references stable. Include the exact allowed effects and exclusions for the receiving task. The receiver must establish its own authorized access; a previous operator approval cannot be carried forward as permission to perform a different action. Capture missing evidence explicitly so the next specialist does not fill gaps with invented facts.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K08 — Specifications](https://kiro.dev/docs/specs/)

[S12 — Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)


## 12. P09 · bound jobs, retries, schedules and stop ownership

**18:00–19:30 · 01:30 allocated**

**Takeaway:** Client completion and service-side termination are different events.

Asynchronous work needs an owner even when no one is watching the interface. Record retry or work limits and where to inspect the run state. A stopped client or CI job may not mean the server-side job has stopped, so verify termination and consumption. Review scheduled tasks periodically and disable those whose context or purpose has expired. The eight-minute demo is an exercise budget, not a promise about any job’s execution time.

[D06 — Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

[K24 — Workflows](https://kiro.dev/docs/workflows/)

[S28 — Run penetration tests from CI/CD](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 13. P10 · verify using evidence independent of the claim

**19:30–21:30 · 02:00 allocated**

**Takeaway:** The same agent saying “done” is not a release or closure criterion.

Independent verification does not always require another AI agent. It may be a source-system query, a known test, a human code review or a monitored deployment. Match the check to the promised result. A proposed root cause should explain source observations; code must pass relevant checks on the reviewed revision; a security fix must be deployed before revalidation; a cost explanation must reconcile to the same data scope. The team decides which checks are required for promotion.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K09 — Built-in tools](https://kiro.dev/docs/tools/)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[F06 — Cost inquiry](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)


## 14. P11 · preserve evidence across systems of record

**21:30–23:00 · 01:30 allocated**

**Takeaway:** Do not replace incident, repository, security or cost records with a single chat summary.

Keep authoritative records where their owners maintain them. The handoff links those records rather than flattening them into one untraceable narrative. Redact sensitive data before copying it to a wider audience, and retain version or time information. A summary may be useful for daily coordination, but reviewers should still be able to open the original investigation, commit, finding or cost query.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K06 — GitHub integration](https://kiro.dev/docs/web/github/)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[F11 — Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)


## 15. P12 · gate availability and data location per feature

**23:00–24:30 · 01:30 allocated**

**Takeaway:** Hosting Region, source location and inference routing are separate questions.

The team should record the product surface, feature maturity, service Region, inference behavior, retention and output destinations for the workflow it actually deploys. DevOps release preview has a more limited Region footprint than production operations. Kiro client capabilities and account rollout differ. Security capability maturity is mixed. FinOps remains preview with its documented US storage and inference boundaries. Do not use an organization-wide “AWS approved” label as a substitute for this feature-level review.

[D15 — Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[S05 — Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

[S30 — Resilience and regional availability](https://docs.aws.amazon.com/securityagent/latest/userguide/resilience.html)

[F16 — Cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)


## 16. Tabletop demo · incident to verified handoff

**24:30–32:30 · 08:00 allocated**

**Takeaway:** Trace one work item through specialist artifacts without transferring authority.

The exercise tests the team’s operating model. Ask participants to identify the owner and stop condition at each handoff. Then introduce missing evidence or a request to expand scope and see whether the receiver stops. Security and cost work are conditional; not every incident needs all specialists. The final artifact is an accepted or rejected next action, not a claim that a new orchestrator has been built.

**Preflight:** Use the supplied illustrative handoff template and labeled rehearsal artifacts. No live cross-agent orchestration is required.

```text

For the illustrative checkout incident, assemble an evidence-linked handoff with scope, owner, exact revision, allowed effects, exclusions and completion checks. Route code work to a reviewer-controlled PR. Add Security or FinOps assessment only when the issue requires it. Do not deploy or share credentials.

```

- 01:00 — **Open the work contract:** Confirm service, environment, evidence and owner.

- 02:00 — **Review operational evidence:** Separate facts, candidate cause and missing data.

- 02:00 — **Inspect the coding handoff:** Show the task contract, scoped diff and independent checks.

- 02:00 — **Choose conditional assurance:** Add targeted security or cost work only when justified.

- 01:00 — **Record the decision:** Name the release owner and required post-change verification.

**Success:** Every transition carries evidence and a new task boundary; no transition carries implicit approval.

**Fallback:** This tabletop is the default mode. A prepared recording may illustrate a real integration, but must be identified as replay.

[D03 — Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

[K04 — Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

[S14 — Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

[F09 — Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)


## 17. Prove the process before building orchestration

**32:30–34:30 · 02:00 allocated**

**Takeaway:** Manual handoffs make authority and evidence defects visible early.

Start with a manual evidence handoff and a small set of representative tasks. Verify actual denial of out-of-scope access and inspect failure recovery. Automate a connector only when the manual process has a clear owner and useful output. Measure accepted handoffs, missing evidence, approval violations, rework, consumption and closure quality. These are proposed operating metrics, not measured benefits from this documentation exercise.

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

[K06 — GitHub integration](https://kiro.dev/docs/web/github/)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)


## 18. Share the work contract; keep authority local

**34:30–36:00 · 01:30 allocated**

**Takeaway:** The common architecture is an accountable engineering process.

Close with the architecture decision: standardize scope, evidence, handoff and verification, but keep product-specific controls explicit. There is no need to invent a shared memory or privilege layer to gain value from specialist tools. Adopt only the integrations the team can observe and stop. The detailed report below preserves all twelve patterns, the action matrix and the proposed workflow material for implementation planning.

[D13 — Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

[K02 — Kiro Web](https://kiro.dev/docs/web/)

[S10 — Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

[F15 — Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)
