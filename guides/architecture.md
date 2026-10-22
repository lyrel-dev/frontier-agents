# Shared architecture — three distinct control systems

Engineering comparison • documentation reviewed 22 October 2026

This document compares AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent. It is not an AWS reference architecture or a claim that the services share a runtime, memory implementation, authorization model or orchestrator. Product statements are sourced; proposed team-level interfaces are labeled as engineering design.

## A-01 — Compare resources before comparing workflows

| Layer | DevOps Agent | Security Agent | FinOps Agent |
|---|---|---|---|
| Scope | Agent Space with account/provider associations | Application Agent Space plus shared account resources | Agent instance with its own data and connections |
| Reusable configuration | Managed/custom agents, selected tools, knowledge, triggers | Assessment configurations, requirements, sources, credentials | Context files, memories, integrations and automations |
| Execution | Investigation, chat, evaluation, custom invocation | Assessment run or one-off design review; revalidation job | Conversation, queued task, report generation |
| Reviewable state | Tool results, investigation evidence, knowledge versions | Findings, test context, model/review results, lineage | Source queries, task results, report artifacts |

The terms differ because the objects differ. A common UI label does not make all Agent Spaces identical. In Security Agent, requirements can be shared across applications; in DevOps Agent, a topology graph is not the complete access boundary; in FinOps Agent, an instance's context can be visible to everyone with access to that instance. [AS01] [AS02] [AS03]

**Engineering design:** record the platform, account/Region, configuration ID and execution ID separately. Do not put one ambiguous `agent_id` in every downstream ticket and expect it to identify all four concepts.

## A-02 — Separate knowledge producers from consumers

| Retained material | Producer | Consumer and lifecycle | Do not infer |
|---|---|---|---|
| DevOps monitor history | Managed learning over investigations | Selective memory retrieval; bounded refresh/retention | A permanent incident archive or trained model weights |
| DevOps correction | Operator feedback; reflection knowledge | Later relevant investigation context | That feedback instantly changed every derived record |
| Security login skill | Successful authentication navigation | Reuse on later logins; toggle controls reuse | General-purpose vulnerability or incident memory |
| FinOps reference file | Operator upload | Readable contextual source; soft-delete/restore | Conversational edits rewriting the file |
| FinOps memory | Conversation/task-derived context | Instance-persistent preferences/corrections | Verbatim retention of all old conversation messages |

These mechanisms are documented separately in the canonical guides: D-M01, D-M02, D-M07, S-M02, F-M02 and F-M03. Their lifecycle cannot be replaced by a single generic “learning enabled” checkbox. [AS04] [AS05] [AS06] [AS07]

**Engineering verification:** separate five questions: was relevant input available, was retained content produced, was it accessible to this execution, was its use observable, and was the resulting conclusion correct? The final answer alone cannot resolve all five.

## A-03 — Connectivity, authentication and authorization are different layers

A private connection supplies a route. Authentication establishes an identity. Authorization determines allowed operations. Prompt instructions describe desired behavior. A successful connection test demonstrates only the layers it actually exercised.

For DevOps MCP, provider registration and Agent Space tool selection are distinct from private routing and tool-effect classification. Security testing separately resolves credentials and applies them to the application; retrieval may succeed while login fails. FinOps registers an account integration and then binds a destination to an agent. [AS08] [AS06] [AS09]

**Engineering test matrix:**

| Test | Evidence needed | Failure interpretation |
|---|---|---|
| Intended read | Correct identity, resource, time window and result | Inspect source access before evaluating the answer |
| Unselected operation | Operation unavailable or rejected | Do not accept a verbal promise as enforcement evidence |
| Authentication | Actual application role reached | A fetched secret is insufficient |
| External publication | Correct destination and action record | Connected integration is insufficient |
| Configuration update | Saved identifiers and current values | A success message may omit replacement/default consequences |

Use a non-production target and non-sensitive fixture. These are proposed tests, not recorded service outcomes.

## A-04 — Authorization must follow the effect

| Effect | Product control to inspect | Important exception |
|---|---|---|
| AWS-resource mutation through DevOps | Directed-action opt-in, target role and operation-specific approval | Programmatically unclassified external tools can default to read-only classification |
| Active application testing | Target/network/credential configuration and assessment authorization | Application writes can occur without infrastructure-write access |
| Source remediation | Repository connection and supported proposed-change path | Proposed patch does not mean deployed repair |
| Jira publishing through FinOps | Invocation-specific approval | Automations pre-authorize actions that would prompt interactively |
| Slack publishing through FinOps | Destination configuration | Posting has no per-message approval prompt in reviewed guidance |

The common rule is to examine the actual effect, not to label every agent “read-only” or “human-approved.” AWS documents different controls for different paths. [AS10] [AS11] [AS12]

**Engineering design:** carry a requested effect and intended target in a work item, but never carry credentials or substitute a ticket approval for the receiving service's native authorization.

## A-05 — Configuration, execution and derived artifacts need separate lifecycles

Pause an automation to stop future starts; cancel a current run using its supported operation; remove or deactivate context using its own controls; delete an artifact only when the artifact itself is the intended target. These are different transitions. In-flight calls or retained execution history may remain after a stop action. [AS13] [AS07]

Security revalidation deliberately creates a new job linked to the original finding rather than silently rewriting the original assessment. DevOps memories keep immutable versions. FinOps task records and uploaded files have different retention/deletion semantics. [AS14] [AS04] [AS07]

**Engineering design:** retain version identifiers and source revisions in accepted work records. Keep maintained configuration source in Git. Do not create dated snapshot directories or compressed manual distributions as a substitute for version control. The product's own runtime retention is independent of this repository's history policy.

## A-06 — A handoff is an artifact, not transferred execution authority

The following is an original team interface, not an AWS schema:

```yaml
schema: engineering-handoff-v1
origin:
  platform: aws-devops-agent
  configuration_id: example-space
  execution_id: example-investigation
  observed_window_utc: "2026-10-22T10:00Z/2026-10-22T10:15Z"
subject:
  service: checkout-staging
  revision: demo-r2
request:
  owner: service-team
  question: Verify the inventory dependency latency explanation
  allowed_effect: review-only
  excluded_effects: [production-deployment, external-publication]
evidence:
  - reference: authorized-internal-record
    observation: inventory p95 increased while database latency remained low
    classification: synthetic-training-fixture
completion:
  required: current evidence supports or rejects the proposed explanation
  unresolved: [upstream-log-access]
```

The receiving engineer resolves the internal evidence link, validates the resource/revision, obtains their own access and decides which product operation is appropriate. There is no implied cross-agent shared session, credential forwarding or automatic trust in the originating conclusion.

**Failure branch:** a task naming “the latest deployment” without an immutable revision cannot establish which change was assessed. Return the work item for clarification rather than letting each product silently choose a different latest revision.

## A-U01 — Worked comparison: one symptom, three different jobs

**Synthetic tabletop.** A staging release produces elevated request retries, an authorization finding and increased transfer volume. Those observations are distinct; one is not proof of the others.

| Specialist question | Product evidence | Acceptance boundary |
|---|---|---|
| Where did the latency increase originate? | DevOps current telemetry, historical context and investigation output | Explain the supported dependency direction; identify missing upstream evidence |
| Does the repaired account boundary hold? | Security finding, deployed revision, actual role and revalidation job | Verify the selected authorization path, not overall application security |
| Which cost components increased? | FinOps matched queries, quantity/rate decomposition, change evidence | Reconcile the delta; distinguish numerical contribution from causal attribution |

**Four-minute exercise:** spend one minute identifying each product's required input, two minutes checking revision/window/identity consistency across the prepared records, and one minute assigning unresolved questions to owners. A purported single root cause is rejected unless evidence actually connects the observations. No live agents or shared runtime are assumed.

## A-07 — Coverage, evidence and unresolved implementation details

This comparison covers resource scoping, retained context, access layers, effects, lifecycle and handoffs. It does not propose a universal agent framework or reproduce complete IAM policies. The three platform guides carry the detailed procedures and explicit per-product coverage tables.

The public sources do not justify specifying a shared vector database, embedding strategy, memory-ranking algorithm, foundation-model training pipeline or cross-product identity fabric. Where an implementation detail is not documented, the guide says so rather than completing an attractive architecture diagram with invented components.

### Official sources and reviewed scope

- [AS01] DevOps topology versus investigation access scope.
- [AS02] Security account and application resource hierarchy.
- [AS03] FinOps creation and instance connections.
- [AS04] DevOps stored knowledge, retrieval and versioning; newer indexed memory guidance.
- [AS05] Dated DevOps correction-memory change.
- [AS06] Security credential resolution and learned login; newer indexed guidance.
- [AS07] FinOps persistent/runtime state and deletion semantics.
- [AS08] DevOps MCP registration, selection and authentication.
- [AS09] FinOps integration registration and binding.
- [AS10] DevOps directed-action controls and classification.
- [AS11] Security active-target configuration and run boundaries; newer indexed guidance.
- [AS12] FinOps action-specific approval.
- [AS13] Custom-agent trigger versus invocation cancellation.
- [AS14] Security revalidation lineage.

[AS01]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
[AS02]: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
[AS03]: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
[AS04]: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
[AS05]: https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html
[AS06]: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
[AS07]: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
[AS08]: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
[AS09]: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
[AS10]: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
[AS11]: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
[AS12]: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
[AS13]: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
[AS14]: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
