# Common architectural patterns

Share the work contract. Keep authority local.


Revision: 21 October 2026. Independent engineering field guide.


**Audience:** Platform architects, engineering leads, security governance and service owners

**Availability:** Team-level synthesis of documented mechanisms. Not an AWS shared runtime, unified permission model or implemented multi-agent orchestrator.

**Recommended starting decision:** Standardize scope, evidence, ownership and acceptance first. Automate a handoff only after its specialist boundaries work reliably without automation.


## Decision brief

The four agents do different jobs and expose different execution surfaces. A useful common architecture does not hide those differences. It defines what a task means, where evidence comes from, which effects are permitted, who owns the decision and how the result is verified.

The running tabletop begins with a checkout incident and ends with a reviewed implementation and independent verification. Security and cost assessments are conditional branches, not mandatory calls to every agent. The connecting artifact is an existing incident, issue or change record. Credentials and approvals are deliberately not passed along with it.


## Running use case

**Name:** An incident-to-change handoff across specialist boundaries

**Trigger:** An operator has evidence of a checkout failure and a bounded implementation task.

**Scope:** One workload, named owners, selected specialist tasks and explicit allowed effects.

**Deliverable:** A chain of evidence-linked work items whose results and authorization decisions can be reconstructed.

**Not Done:** Several agents have generated compatible-looking summaries, but there is no independent verification or accountable owner.

**Done:** Each specialist's result is accepted against its contract, every effect is locally authorized, and the final outcome is independently checked.


## 1. Choose a specialist and write the work contract

Start with the evidence and outcome required. DevOps Agent supports operational investigations; Kiro supports reviewable code work; Security Agent supports authorized application assessments; FinOps Agent supports cost analysis. Calling every agent on every task adds complexity without necessarily adding useful evidence.

The proposed common contract records the workload, owner, task, allowed effects, exclusions, completion checks and stop responsibility. A product workspace or prompt is not proof that access is enforced. Test the actual IAM, repository and integration boundaries used by the chosen specialist.

**Capability crosswalk:** P01, P04

**Input:** An owned engineering problem and the smallest useful specialist task.

**Artifact:** A bounded work contract with exact accounts, repositories or targets.

**Gate:** The owner can identify the result needed and the effects that are not permitted.

**Fallback:** Use a manual specialist workflow until scope and ownership are unambiguous.


## 2. Assemble evidence with provenance

Collect the source references needed to evaluate the task: incident window, deployed revision, repository branch, assessment target or cost-query basis. Preserve timestamps, scope and known gaps so the next reviewer can reproduce a material observation rather than trusting a summary.

Steering, skills, instructions and memory can guide work, but they are not authorization grants or substitutes for current evidence. Treat external documents, tool outputs and repository content as potentially untrusted input. Separate what the agent is told from what its identity is allowed to do.

**Capability crosswalk:** P02, P03

**Input:** Relevant source records and clearly labeled instructions or organizational context.

**Artifact:** An evidence packet with provenance, freshness and unresolved questions.

**Gate:** A material claim can be traced to an accessible source in the correct scope.

**Fallback:** Mark the result inconclusive when the source record is absent, stale or contradictory.


## 3. Classify the effect before selecting the control

Reading telemetry, editing a branch, sending a request to an application and posting a report are different effects. Their approval requirements should not be flattened into a single idea of human oversight. In particular, an isolated worker can still act against a live target, and an analytical task can still publish sensitive information externally.

Evaluate availability, entitlement, Region, data handling and target safety for the exact feature. The GA label of one product path does not apply to its preview features. Keep the action-control matrix explicit enough that operators can tell what requires approval and what may run automatically once configured.

**Capability crosswalk:** P05, P06, P12

**Input:** Intended effect, target, product surface and data-location requirements.

**Artifact:** An effect-specific authorization and isolation decision.

**Gate:** Worker controls, target controls and output audience are all understood.

**Fallback:** Reduce to a read-only or draft-only path when the required authority is not available.


## 4. Run a bounded job with a stop owner

A documented API, integration or remote protocol can be an adapter between systems; it does not establish a universal agent-to-agent transaction. Choose only the interfaces needed for the task and retain each product's access model. Manual handoff is a valid first implementation.

Bound the job's time, spend, retries and concurrency where the product provides controls, and add team procedures where it does not. A recurring schedule needs a recipient, duplicate-work policy and stop owner. Record partial and failed outcomes rather than treating lack of a response as success.

**Capability crosswalk:** P07, P09

**Input:** Authorized task, explicit adapter and operational limits.

**Artifact:** A run record with status, owner, effect log and stop or retry decision.

**Gate:** Operators can interrupt work and identify incomplete results.

**Fallback:** Use a prepared, labeled example for presentations and the established engineering process for real work.


## 5. Transfer a reviewable artifact—not inherited privileges

For an incident-to-fix handoff, the next specialist receives the affected repository, observed failure, evidence references and regression-test expectations. It does not receive production credentials or a blanket instruction to implement every mitigation. A security finding or cost recommendation follows the same artifact principle.

Keep work-item IDs, source revisions and reviewer decisions stable across systems of record. The receiving specialist establishes its own authorized access and acceptance criteria. That preserves accountability even when the handoff is automated later.

**Capability crosswalk:** P08, P11

**Input:** Accepted specialist output with scope, evidence and unresolved limitations.

**Artifact:** A linked implementation, assessment or optimization task with a new accountable owner.

**Gate:** The recipient can evaluate the result without inheriting the sender's approval authority.

**Fallback:** Reject an incomplete handoff and request missing evidence instead of filling gaps with assumptions.


## 6. Verify independently before widening the system

Verification must be independent of the claim being accepted. Compare an incident conclusion with telemetry, a code change with meaningful tests and review, a repaired finding with revalidation, and a cost recommendation with a consistent post-change measurement. Agent agreement alone is not independent verification.

Pilot one workflow before building a broad orchestrator. Measure acceptance, rework, boundary failures, time spent reviewing and the quality of retained evidence. Expand only where the operating process is understood and the chosen interfaces and feature availability support it.

**Capability crosswalk:** P10, P11, P12

**Input:** Specialist output and an independent acceptance method.

**Artifact:** An owner-approved outcome and evidence-based expansion decision.

**Gate:** The final decision can be reconstructed from sources, controls and verification records.

**Fallback:** Keep the workflow manual or narrow its scope when evidence or control reliability is inadequate.


## Detailed capability reference


### P01 — Bounded workspaces and accountable owners

**Rule:** Define a service, repository set, or account group before delegating work. Give that boundary a named platform owner and a separate operational owner.

**Setup:** Create a boundary record with application ID, environment, accounts, repositories, targets, authorized operators, and output destinations. Start with one team-owned workload.

**Boundary:** A workspace name, topology view, or prompt is not proof of an enforced security boundary. Test the underlying role and integration scope.

**Check:** Attempt a harmless read of an explicitly out-of-scope test resource. Confirm denial at the actual integration or identity layer, not merely a refusal in chat.

**Anti:** One organization-wide identity and a prompt saying “only touch checkout.”

Evidence: D01, D05, K02, K03, S02, S03, F01, F02


### P02 — Source-grounded context, with provenance

**Rule:** Supply a minimum evidence packet: exact code or deployment version, relevant time window, authoritative source links, and known gaps. Separate observations from inferred explanations.

**Setup:** Record a source owner, revision or timestamp, classification, and refresh rule for every context input. Keep one canonical owner map outside the agent.

**Boundary:** Connected data is not necessarily complete or current. A missing signal must remain missing rather than being filled in with a plausible narrative.

**Check:** Reproduce one material claim in the source system. Check the commit, application version, observation period, filters, and whether data was actually accessible.

**Anti:** A copied chat summary becomes the authoritative incident, security, or billing record.

Evidence: D02, K11, K02, S03, F09, F04


### P03 — Instructions and memory are not authorization

**Rule:** Version explicit team instructions and review learned context separately. Enforce access, network reach, and execution authority in the controls that actually govern the chosen interface.

**Setup:** Maintain approved runbooks, conventions, and owner mappings with review dates. Treat repository text, tool responses, and generated memory as inputs that can be wrong or untrusted.

**Boundary:** Do not assume one shared memory store, instruction format, or permission configuration across the portfolio. A policy written in a document is not an IAM policy.

**Check:** Change a non-sensitive convention in a test workspace and check its effect. Separately verify that instructions cannot grant a denied operation or broaden repository access.

**Anti:** “Never change production” in a steering file is the only safeguard protecting production credentials.

Evidence: D03, K07, K08, K04, S09, S13, S02, F04


### P04 — Explicit task contracts and trigger ownership

**Rule:** Wrap every interactive, scheduled, or event-driven request in a bounded task: objective, inputs, allowed effects, owner, expected output, and completion criteria.

**Setup:** Prove an on-demand task first. Then add only a supported trigger, one owner, a deduplication key, an escalation destination, and a way to disable recurrence.

**Boundary:** “Event-driven” does not mean every event type is supported. A schedule, webhook, issue trigger, and local IDE hook are different integration paths.

**Check:** Replay the same sample event twice in a test setup. Ensure your team process or adapter prevents duplicate actionable work; no universal native deduplication is assumed.

**Anti:** Every alert automatically starts every agent, with no owner, suppression window, or action boundary.

Evidence: D02, D03, K09, K02, S03, S11, F05, F08


### P05 — Authorize effects, not product labels

**Rule:** Classify each proposed effect as observation, repository change, external publication, application testing, or infrastructure mutation. Apply the destination’s native gate to that exact effect.

**Setup:** Maintain an action register with initiator, tool, target, permissions, approval behavior, output visibility, and revocation owner. Classify custom tools before enabling them.

**Boundary:** No portfolio-wide “human approval” switch exists in this design. The ability to generate a recommendation never transfers permission to execute it.

**Check:** Test one permitted action and one denied action for each configured path. Verify the identity, target, parameters, and whether approval is per call or pre-authorized.

**Anti:** A reviewer approves an investigation summary and the integration treats it as authorization for arbitrary changes.

Evidence: D04, D05, K04, S03, S04, F03, F05


### P06 — Isolate both execution and its targets

**Rule:** Constrain the worker environment and every system it can reach. Use disposable test data, narrow credentials, limited egress, and explicit non-production targets for active testing.

**Setup:** Inventory egress, environment variables, test identities, external callbacks, and data-reset procedures. Remove live payment, email, and production-data paths from the test environment.

**Boundary:** An isolated runner is not a guarantee that reachable databases, APIs, payment endpoints, or communication channels are isolated. Secrets can escape through permitted outputs.

**Check:** In a controlled test, confirm an out-of-scope endpoint is blocked and a non-production write can be reset. Review logs and generated diffs for accidental secret disclosure.

**Anti:** A sandbox is given production credentials and unrestricted network access, then treated as harmless.

Evidence: D08, D09, K03, K05, K06, S04, F01, F03


### P07 — Integrate through explicit adapters

**Rule:** Use documented product interfaces with their own authentication and scope. Keep the shared contract agent-neutral; put provider-specific request and response handling in small adapters.

**Setup:** For each proposed connection, record client, server, protocol, authentication, enabled tools, data transferred, feature status, and failure behavior. A manual artifact handoff is a valid first implementation.

**Boundary:** MCP compatibility is not a shared authorization domain. This report does not establish a generic FinOps MCP endpoint, common cross-agent API, or built-in four-agent orchestration service.

**Check:** Demonstrate one permitted call with a narrow identity. Remove the connection and verify access stops without breaking unrelated agents.

**Anti:** One universal connector forwards every tool and credential to every agent.

Evidence: D06, D07, K10, S08, S13, F10, F11


### P08 — Artifact-first handoff between specialists

**Rule:** Pass a small, reviewable evidence packet rather than raw conversation history: finding, affected scope, evidence links, proposed change, owner, acceptance tests, and expiry.

**Setup:** Use the existing issue, pull request, or change record as the durable handoff. Give linked agent runs the same work-item ID and keep sensitive findings in approved locations.

**Boundary:** The handoff contract below is a team convention, not an AWS schema. It carries context and provenance—not credentials, delegated authority, or transferable approvals.

**Check:** Ask the receiving engineer to reconstruct the problem without reading the original chat. Reject packets with unresolved source access, missing versions, or no accountable owner.

**Anti:** A generated narrative is sent to another agent with “implement everything,” including unverified assumptions.

Evidence: D10, K12, K11, S05, S07, F07, F10


### P09 — Bounded asynchronous work and stop responsibility

**Rule:** Track every run as a job with a lifecycle, an owner, a work budget, and a stop procedure. Reconcile completed, partial, failed, cancelled, and waiting-for-input states explicitly.

**Setup:** Set team-level concurrency and retry limits; use native caps where available. Record run identifiers, last observed state, budget consumption, and the operator who can stop the job.

**Boundary:** Client timeout is not proof that server work stopped. Product quotas, elapsed time, billable work, and spending caps are different concepts.

**Check:** Exercise cancellation on a safe task and confirm the server reaches a terminal state. Check partial outputs and duplicate retries before closing the work item.

**Anti:** A CI job is cancelled, so everyone assumes the billable agent job has also ended.

Evidence: D03, K12, K02, S03, S10, S13, F05


### P10 — Independent verification before promotion

**Rule:** Define acceptance criteria before a run and verify the result with evidence independent of the generated narrative. Keep merge, deployment, security acceptance, and financial decisions with accountable owners.

**Setup:** Write separate checks for code behavior, operational recovery, finding reproduction, and billing reconciliation. Use ordinary CI and source dashboards wherever possible.

**Boundary:** Completed is not correct; a passing gate is not complete coverage; an estimate is not realized savings. Confidence and scope must remain attached to the result.

**Check:** Re-run the relevant test against the exact proposed commit or deployed version. Document unresolved coverage and compare cost results with matched periods and dimensions.

**Anti:** A fluent root-cause explanation, green job, or projected saving becomes a production approval.

Evidence: D11, K01, K02, S04, S06, F03, F07, F09


### P11 — Evidence lineage and separate systems of record

**Rule:** Correlate request, run, source version, evidence, approval, change, and observed outcome in a durable work record. Store evidence under the access and retention policy appropriate to its sensitivity.

**Setup:** Use one correlation ID across links; retain minimal structured metadata and source references. Define access to evidence separately from access to the generated executive summary.

**Boundary:** There is no common portfolio-wide audit trail asserted here. A chat log does not replace Git history, cloud audit events, security evidence, or billing records.

**Check:** Sample a completed work item. Reconstruct who requested it, what it read, what it changed or published, who authorized the effect, and how the result was verified.

**Anti:** Store only the final summary and lose the source version, tool call, and approval history.

Evidence: D04, D03, K12, K02, S05, S06, F05, F09


### P12 — Feature-level availability and data-location gates

**Rule:** Approve the exact combination of feature, interface, Region, inference route, data classification, and integration destination. Recheck it when the configuration or product changes.

**Setup:** Keep a feature register with status, storage Region, processing geography, eligible users/plans, source links, owner, and review date. Treat preview use as an explicit exception decision.

**Boundary:** Availability in a Region does not establish end-to-end data residency. Source location, service storage, model inference, and third-party output destinations are separate boundaries.

**Check:** Trace one representative artifact from source through service processing to PR, ticket, or channel. Confirm each destination is approved before providing sensitive data.

**Anti:** “It runs on AWS” is used as proof that all data stays in the workload’s Region.

Evidence: D09, K01, S12, F06


## Illustrative handoff

```yaml

work_item: INC-DEMO-001
kind: illustrative-team-contract
owner: checkout-service-owner
scope: {service: checkout-api, environment: staging, revision: DEMO-A}
evidence: [source-observation, affected-diff]
allowed_effects: [read-evidence, propose-branch-change]
exclusions: [production-write, credential-transfer]
receiver_authorization: establish-separately
acceptance: independent-test-and-owner-review
stop_owner: named-operator

```


## Readiness checklist

- [ ] Every task has a workload owner, scope and completion check.

- [ ] Evidence retains timestamps, revision and provenance.

- [ ] Instructions and memory are not treated as access grants.

- [ ] Approval is specific to the effect, target and interface.

- [ ] Jobs have limits, stop ownership and an incomplete-result path.

- [ ] Handoffs transfer artifacts rather than credentials or inherited approval.

- [ ] An independent check supports each accepted result.

- [ ] Feature availability and data location are reviewed separately.


## Sources

- X01: [AWS frontier agents](https://aws.amazon.com/ai/frontier-agents/)

- D01: [About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)

- D02: [Production operations](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-production-operations-index.html)

- D03: [Custom Agents](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

- D04: [Working with directed actions](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

- D05: [Limiting Agent Access in an AWS Account](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

- D06: [Accessing DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-accessing-devops-agent-index.html)

- D07: [Connecting to the DevOps Agent MCP server](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-connecting-to-the-devops-agent-mcp-server.html)

- D08: [Release testing](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

- D09: [Supported Regions](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

- D10: [Proactive incident prevention](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

- D11: [Autonomous incident response](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

- K01: [Kiro Web](https://kiro.dev/docs/web/)

- K02: [GitHub integration](https://kiro.dev/docs/web/github/)

- K03: [Cloud sandbox](https://kiro.dev/docs/web/sandbox/)

- K04: [Permissions](https://kiro.dev/docs/permissions/)

- K05: [Sandbox internet access](https://kiro.dev/docs/web/sandbox/internet-access/)

- K06: [Sandbox environment variables and secrets](https://kiro.dev/docs/web/sandbox/environment-variables/)

- K07: [Steering](https://kiro.dev/docs/steering/)

- K08: [Memory](https://kiro.dev/docs/memory/)

- K09: [Automations](https://kiro.dev/docs/web/automations/)

- K10: [Model Context Protocol](https://kiro.dev/docs/mcp/)

- K11: [Specifications](https://kiro.dev/docs/specs/)

- K12: [Autonomous mode](https://kiro.dev/docs/web/autonomous-mode/)

- S01: [What is AWS Security Agent (now part of AWS Continuum)?](https://docs.aws.amazon.com/securityagent/latest/userguide/what-is.html)

- S02: [Set up AWS Security Agent](https://docs.aws.amazon.com/securityagent/latest/userguide/setup-security-agent.html)

- S03: [Create a penetration test](https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html)

- S04: [Security best practices](https://docs.aws.amazon.com/securityagent/latest/userguide/security-best-practices.html)

- S05: [Review penetration-test findings](https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html)

- S06: [Revalidate findings](https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html)

- S07: [Enable finding remediation](https://docs.aws.amazon.com/securityagent/latest/userguide/enable-remediate-findings.html)

- S08: [Run code security scans from your IDE](https://docs.aws.amazon.com/securityagent/latest/userguide/code-review-ide-integration.html)

- S09: [Manage security requirements](https://docs.aws.amazon.com/securityagent/latest/userguide/security-requirements.html)

- S10: [Run penetration tests from CI/CD](https://docs.aws.amazon.com/securityagent/latest/userguide/cicd-pentest.html)

- S11: [Scoped-pentest GitHub Actions tutorial](https://docs.aws.amazon.com/securityagent/latest/userguide/sample-cicd-github.html)

- S12: [Resilience and regional availability](https://docs.aws.amazon.com/securityagent/latest/userguide/resilience.html)

- S13: [Pricing and billing](https://docs.aws.amazon.com/securityagent/latest/userguide/pricing.html)

- S14: [On-demand penetration testing is generally available](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-security-agent-ondemand-penetration/)

- F01: [Creating an agent](https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html)

- F02: [IAM setup guide](https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html)

- F03: [Agent guardrail controls](https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html)

- F04: [Context files and memory](https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html)

- F05: [Task management](https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html)

- F06: [Cross-region inference](https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html)

- F07: [Optimization recommendations](https://docs.aws.amazon.com/finops-agent/latest/userguide/optimization-recommendations.html)

- F08: [Event-triggered cost anomaly investigation](https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html)

- F09: [Asking about costs](https://docs.aws.amazon.com/finops-agent/latest/userguide/cost-inquiry.html)

- F10: [Jira integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html)

- F11: [Slack integration](https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html)


## Validation boundary

Documentation synthesis and proposed workflows only. No live AWS execution or measured engineering outcome. The original audit snapshot and the selected narrative rechecks are distinct.
