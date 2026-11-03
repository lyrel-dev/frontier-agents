---
title: AWS DevOps Agent — presenter notes
id: obsidian-devops-presentation-notes
aliases: []
tags:
- aws/devops-agent
- agents
- devops
- speaker-notes
type: speaker-notes
created: '2026-10-31'
updated: '2026-10-31'
source_cutoff: '2026-10-31'
status: documentation-vetted
related:
- '[[AWS_DevOps_Agent_Presentation]]'
- '[[Source_Index]]'
kind: obsidian-note
product: devops
---

<!-- block: obsidian-devops-presentation-notes-body -->
# Presenter notes

The slide note contains concise projected content. This companion holds explanations, evidence boundaries and teaching prompts. Numbers match the presentation exactly. Open [[AWS_DevOps_Agent_Presentation]] in a second pane.

## 01 · AWS DevOps Agent: from foundations to operations

**Section:** Orientation

Start with the definition of an agent before introducing product names. The audience should leave able to distinguish model behavior, runtime controls and the business process that accepts an outcome. The full reference notes retain service administration, interface and lifecycle detail.

## 02 · The questions this presentation answers

**Section:** Orientation

This is the teaching order requested for the dossier. The framework is conceptual where labeled, documentation-based where describing AWS, and illustrative where designing customer orchestration. These three evidence levels remain explicit throughout.

## 03 · An agent combines a model with an execution system

**Section:** Primer

Avoid anthropomorphic claims. The model output alone does not perform a change. The runtime handles actual calls, results and stopping conditions. Product language varies, so assess the actual decision and execution behavior rather than the label.

**Primary references:** [F01](https://www.anthropic.com/research/building-effective-agents) [F07](https://strandsagents.com/docs/user-guide/sdk/agents/agent-loop/)

## 04 · The observation loop makes actions testable

**Section:** Primer

Read the loop aloud using a failed checkout as an example: observe errors, choose a query, execute it, inspect the result, then decide again. A claim of success is an output; an observed restored service is an outcome. Errors and missing permissions must become explicit results.

**Diagram P01:** A conceptual model/tool loop. The runtime executes tools, supplies their results and enforces stop conditions. This is not an AWS internal implementation diagram. See [[Diagram_Atlas#P01 — The agent loop]].

**Primary references:** [F07](https://strandsagents.com/docs/user-guide/sdk/agents/agent-loop/)

## 05 · Model, workflow, agent and service are different layers

**Section:** Primer

A predefined workflow can contain model calls and agent-led stages. A fixed path does not guarantee identical model outputs. A managed service can contain multiple agent roles without revealing its physical runtime topology.

**Primary references:** [F01](https://www.anthropic.com/research/building-effective-agents) [F10](https://strandsagents.com/docs/user-guide/sdk/agents/) [S001](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)

## 06 · Autonomy and authority are separate

**Section:** Primer

An investigator can have freedom to select queries while having no production change authority. Define the goal, available evidence, action scope, approval boundary and stopping condition separately. AWS directed actions illustrate this separation.

**Primary references:** [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [F07](https://strandsagents.com/docs/user-guide/sdk/agents/agent-loop/)

## 07 · Seven families of agent mechanisms

**Section:** Mechanisms

This seven-part taxonomy is an original teaching framework, not a universal standard or AWS product taxonomy. The dossier expands each family into concrete mechanisms, examples and failure modes.

## 08 · A tool is an operation; an integration makes it usable

**Section:** Mechanisms

Use one example: a deployment-history tool, an authenticated GitHub integration, a protocol exchange and the API implementation. Protocol compatibility alone says nothing about authorization, tool quality or whether the retrieved data answers the question.

**Primary references:** [F03](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) [F05](https://www.anthropic.com/research/writing-tools-for-agents) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html)

## 09 · Protocol exchange sits inside a larger tool contract

**Section:** Mechanisms

This conceptual sequence separates the host, MCP server, tool implementation and external service. Real deployments may combine layers. Authentication, resource permissions and network reachability remain necessary; this is not a universal MCP server implementation.

**Diagram P02:** Conceptual request/result layering. MCP does not grant the downstream permissions or define the host reasoning process. See [[Diagram_Atlas#P02 — Tools and protocol exchange]].

**Primary references:** [F03](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) [F05](https://www.anthropic.com/research/writing-tools-for-agents)

## 10 · Context, skill, memory and state serve different purposes

**Section:** Mechanisms

Continuity is maintained by the application through context and persistence. Saving a memory does not by itself retrain the model. A skill is procedural, while environmental knowledge is informational. Neither grants permission to use a tool.

**Primary references:** [F04](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) [F10](https://strandsagents.com/docs/user-guide/sdk/agents/) [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

## 11 · Relevant context is assembled for each decision

**Section:** Mechanisms

Explain the loop between an action and fresh evidence. An earlier incident memory can guide the first query but should not settle the new cause. Retrieval selects useful material from a potentially much larger knowledge base.

**Diagram P03:** Context is selected for a current decision. The runtime, a tool or an external event supplies each new observation; the decision requests it. Memory is stored information; saving it is not itself model retraining. See [[Diagram_Atlas#P03 — Assembling useful context]].

**Primary references:** [F04](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

## 12 · Controls, lifecycle and evaluation complete the system

**Section:** Mechanisms

A notification is not completion proof. A completion flag is not proof that a business objective was met. Evaluate the execution record and observed state against acceptance criteria. Diagnose network, credential, permission and approval failures separately.

**Primary references:** [F06](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

## 13 · Orchestration patterns are choices, not maturity levels

**Section:** Mechanisms

Use deterministic code for invariants and model judgment for evidence-dependent choices. Parallelism is useful only when branches can work independently. Preserve worker evidence and assign one owner for the final decision. These generic patterns do not reveal AWS internal orchestration.

**Primary references:** [F08](https://strandsagents.com/docs/user-guide/sdk/multi-agent/multi-agent-patterns/) [F09](https://www.anthropic.com/research/multi-agent-research-system)

## 14 · DevOps agent types begin as responsibilities

**Section:** Roles

These are role families used to reason about DevOps work. They are not a list of separately shipped AWS products. The next slides move from these functional descriptions to the documented AWS names.

## 15 · AWS DevOps Agent supplies workflows within an Agent Space

**Section:** AWS platform

Explain accounts, integrations, operator access, topology and knowledge as Agent Space context. Topology helps navigate relationships but is not an authorization policy. Managed and custom agents use the capabilities made available to the space.

**Diagram P04:** The Agent Space supplies scope and context. Boxes describe public concepts, not physical hosting or an internal scheduler. See [[Diagram_Atlas#P04 — AWS operating model]].

**Primary references:** [S104](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html) [S105](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html) [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

## 16 · Named managed agents: conversation and incident work

**Section:** Roles

Names are exact product labels. These managed components run inside product workflows; they are not independent Run Now definitions. Incident UI is an output-generation responsibility, not a user-defined presentation agent.

**Primary references:** [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) [S083](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-on-demand-devops-tasks.html)

## 17 · Named managed agents: assurance, tests and knowledge

**Section:** Roles

The managed-agent guide describes Evaluation as performance/policy assessment, while the Skills guide labels Evaluation as proactive recommendations. Record this naming inconsistency. Grader powers Review. Release readiness is documented but is not separately named in the current roster. Availability follows capability-specific guidance, not a blanket inference from a page badge.

**Primary references:** [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

## 18 · Managed and custom agents expose different control surfaces

**Section:** Roles

Managed guidance is editable through AGENTS.md. New sessions receive saved instructions; existing sessions retain their initial guidance. Custom memory access starts empty until stores are attached. Learning schedules are platform-owned and distinct from custom triggers.

**Primary references:** [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S052](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

## 19 · Platform capabilities provide context and execution

**Section:** AWS platform

A memory store, webhook or IAM role is not another reasoning agent. The detailed traceability table connects capabilities to configuration and evidence surfaces. Platform capability and agent job are different dimensions.

**Primary references:** [S104](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html) [S105](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html) [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html)

## 20 · Platform capabilities also support acceptance and operation

**Section:** AWS platform

Investigation Sandbox is a separate optional computation environment, covered in the technical reference. Usage metrics do not measure business success on their own. Connect completion records to recovery, implementation or release acceptance evidence.

**Primary references:** [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S102](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-vended-logs-and-metrics.html) [S086](https://docs.aws.amazon.com/devopsagent/latest/userguide/quotas.html) [S093](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html)

## 21 · Permissions remain separate from agent roles

**Section:** AWS platform

Human access, investigation access and elevated-action access are separate. Each account role is assumed directly. Agent Space topology is not a complete authorization inventory. A prompt cannot create a permission or a private network route.

**Diagram P05:** Each connected account supplies its own investigation role. Operator access and the elevated action path are separate. The elevated role is registered on the target account association. This is not role chaining through a primary investigation role. See [[Diagram_Atlas#P05 — Access has separate boundaries]].

**Primary references:** [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S074](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

## 22 · Incident workflow: triage controls intake

**Section:** Built-in workflows

Use a duplicate paging event as the example. A linked event joins existing work. A skipped event has not proved the service is healthy. Operators can unlink or unskip to start an independent investigation. Record the relationship to the external incident.

**Diagram P06:** Linked, Skipped and Proceed are distinct triage outcomes. Operators can correct a link or skip; a skip is not a health verdict. See [[Diagram_Atlas#P06 — Incident triage]].

**Primary references:** [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

## 23 · Incident workflow: evidence drives the cause assessment

**Section:** Built-in workflows

Explain timeline inspection, evidence, operator steering, feedback and forks. A fork can begin from a timeline user or agent message; it is not limited to completed investigations. Missing telemetry must be represented as uncertainty.

**Diagram P07:** Conceptual evidence workflow. The actual investigation can use parallel work; the drawing is not an exhaustive API state machine. See [[Diagram_Atlas#P07 — Investigation evidence loop]].

**Primary references:** [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

## 24 · A mitigation proposal is followed by explicit action controls

**Section:** Built-in workflows

Eligibility includes opt-in, supported operations, guardrails and role permissions. Destructive classified operations are blocked. Chat approval is scoped; API clients separately record approval and resume execution. Verification is the customer operating step after execution.

**Diagram P08:** Eligibility includes feature opt-in, supported operation, guardrails and effective permissions. Only the operator-directed chat path produces these action approvals. Outcome verification is recommended customer practice. See [[Diagram_Atlas#P08 — Directed action gates]].

**Primary references:** [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S099](https://docs.aws.amazon.com/boto3/latest/reference/services/devops-agent/client/update_approval_action.html) [S092](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContext.html)

## 25 · Review, prevention and Learning answer different questions

**Section:** Built-in workflows

Review grades completed work. Prevention proposes engineering improvements. Learning maintains reusable managed context. Corrective feedback is another learning path. These branches can consume common records without forming one mandatory automatic chain.

**Diagram P09:** These are separate consumers of incident information. There is no asserted automatic Review-to-prevention-to-Learning chain, and Evaluation naming differs between the managed-agent and Skills guides. The diagram therefore uses the prevention workflow label. See [[Diagram_Atlas#P09 — Three uses of incident history]].

**Primary references:** [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html)

## 26 · Release readiness and release testing produce different evidence

**Section:** Built-in workflows

The optional readiness verification environment builds and tests code. UI/API testing targets a deployment and can write application data. Their results should be tied to the code and environment assessed. Release management is preview in us-east-1 at the source cutoff.

**Diagram P10:** Readiness and deployed-application testing provide different evidence. Their combination at a team release gate is a proposed customer policy. Tests may modify application data. See [[Diagram_Atlas#P10 — Two release evidence paths]].

**Primary references:** [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S097](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html)

## 27 · Integration direction determines the contract

**Section:** Orchestration

Hosted MCP and A2A serve external clients. Outbound MCP exposes tools; outbound A2A delegates to remote agents. Each path has its own identity, protocol and scope. ACP is documented through a sample adapter over service APIs, not a native hosted ACP endpoint.

**Diagram P11:** Inbound service access and outbound integrations are different configuration and authorization paths. The remote specialist is not an AWS continuation subagent. See [[Diagram_Atlas#P11 — Integration direction]].

**Primary references:** [S070](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) [S043](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html) [S049](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-connecting-to-the-devops-agent-mcp-server.html) [S011](https://github.com/aws-samples/sample-aws-devops-agent-acp-mcp)

## 28 · Private connectivity has two separate paths

**Section:** Orchestration

PrivateLink is private ingress to the service. VPC Lattice underpins the private tool-connection path. Shared VPCs need the documented self-managed arrangement. DNS, routes, security controls, credentials and provider scope must all be validated.

**Diagram P12:** PrivateLink serves private client ingress. The private connection and VPC Lattice path reach a private tool. These are separate paths with their own setup. See [[Diagram_Atlas#P12 — Private paths are directional]].

**Primary references:** [S103](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-vpc-endpoints-aws-privatelink.html) [S048](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html)

## 29 · Three owners coordinate a complete process

**Section:** Orchestration

AWS documents continuation subagents with the same tools and skills near a context limit. That behavior does not establish a user-authored DAG, independent child schedules or distributed transactions. The customer retains the business process ledger.

**Primary references:** [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) [S043](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html) [S070](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html)

## 30 · The customer process observes and reconciles results

**Section:** Orchestration

Agent completion and business acceptance are different states. The customer controller records intent, returned task/execution IDs and output references. On restart or timeout it reconciles authoritative state before repeating side effects.

**Diagram P13:** This example shows an investigation. The customer workflow and ledger are proposed architecture. The optional remote A2A branch represents documented investigation delegation, not an asserted custom-agent tool path. Continuation inside a custom run does not supply this durable customer process. See [[Diagram_Atlas#P13 — Orchestration ownership]].

**Primary references:** [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) [S069](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html) [S051](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html)

## 31 · Example environment: extend what already exists

**Section:** Operational cases

The example organization is fictional. PagerDuty pages, ServiceNow records incidents/changes, GitHub holds code and CloudWatch/Datadog supply evidence. Internal MCP supplies scoped ownership and deployment context. Existing integrations do not imply automatic cross-system synchronization.

**Diagram P19:** Illustrative existing environment: CloudWatch/Datadog supply telemetry, GitHub/ServiceNow supply change context, and internal MCP supplies ownership and deployment data. The customer workflow keeps a ledger. Provider scope, identity and network access must be configured; no automatic cross-provider synchronization is implied. See [[Diagram_Atlas#P19 — Established system extension]].

**Primary references:** [S029](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html) [S024](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-aws-eks-access-setup.html) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) [S045](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-ticketing-and-chat-connecting-slack.html)

## 32 · Case 1: incident to verified recovery

**Section:** Operational cases

Triage precedes this accepted-incident diagram. Correlate the failure with the actual deployment. The responder may approve an eligible action, use the existing rollback process or hold. A hold remains unresolved; closure requires recovery evidence. Preserve feedback and optionally request Review.

**Diagram P14:** Customer operating pattern. The eligible action path uses documented directed-action controls; the manual path uses the established change process. Holding cannot itself close the incident. See [[Diagram_Atlas#P14 — Incident recovery case]].

**Primary references:** [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html)

## 33 · Case 2: recurring incidents to an implemented improvement

**Section:** Operational cases

A kept recommendation becomes normal engineering work with an owner. A merged PR alone does not prove deployment; fewer incidents alone do not prove a new control exists. Verify the implementation and then observe impact. EventBridge does not supply a documented prevention-completed event.

**Diagram P15:** The service proposes improvements. Implementation ownership, deployment proof and recurrence observation belong to the illustrated customer process. See [[Diagram_Atlas#P15 — Prevention implementation case]].

**Primary references:** [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S087](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Recommendation.html) [S069](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html)

## 34 · Case 3: candidate change to a human release gate

**Section:** Operational cases

The customer process combines readiness, optional managed verification and application tests. The AWS-maintained action is aws-actions/devops-agent-qa@v1. Missing or mismatched evidence holds the release. Existing delivery controls remain responsible for deployment.

**Diagram P16:** The sequencing and human gate are customer policy. Keep the commit and tested deployment identities attached to every result. See [[Diagram_Atlas#P16 — Release evidence case]].

**Primary references:** [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S021](https://github.com/aws-actions/devops-agent-qa)

## 35 · Custom agents package a task within selected scope

**Section:** Custom extensions

Custom agents combine a prompt, selected tools, skills and attached stores. They start without memory access; managed stores are read-only and attached custom stores can be written. Inspect a manual run before recurring automation. Output acceptance remains a customer design decision.

**Diagram P17:** Assigned integration tools and attached stores define task scope; built-in artifact and recommendation tools are also available. Notifications need a destination and instructions; the customer acceptance step is a proposed operating practice. See [[Diagram_Atlas#P17 — Custom agent invocation]].

**Primary references:** [S052](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)

## 36 · Triggers and outputs need explicit contracts

**Section:** Custom extensions

JMESPath filters can reject or project payloads. A true result passes the original event, while another truthy result supplies the projection. Do not invent a provider payload field. Custom event support in the console does not imply equivalent CloudFormation support; Trigger currently documents TIME_BASED.

**Primary references:** [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S026](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-devopsagent-trigger.html)

## 37 · Extension A: incident context assembler

**Section:** Custom extensions

This is an illustrative specialization, not a built-in named managed agent. It assembles commit, owner, approved change and runbook context. The ledger associates its output with the incident investigation. A Slack update is optional and requires the configured destination plus instructions.

**Primary references:** [S052](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)

## 38 · Extension B: recurrence implementation auditor

**Section:** Custom extensions

The output categories here are customer report categories, not AWS enums. Memory is context; the work system and ledger remain authoritative for commitments. Updates to business records require a reviewer or separately authorized customer integration.

**Primary references:** [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html)

## 39 · Extension C: release evidence coordinator

**Section:** Custom extensions

AWS documents custom Release Manager tools for creating, listing, retrieving and canceling tasks and analyzing readiness reports. The example combines those with pipeline test evidence. The customer controller invokes any optional remote A2A specialist independently and merges its evidence; this does not assert native custom-agent A2A tool support. It does not invent a new managed roster entry or assume a multi-day process fits in one session.

**Primary references:** [S052](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) [S043](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html)

## 40 · A durable controller handles incomplete evidence

**Section:** Operating the system

Investigation and mitigation events can omit summary_record_id. When present, call ListJournalRecords with agentSpaceId, executionId and the correct recordType, paginate and match recordId. Never substitute task_id. Custom and prevention lifecycle events are outside this documented EventBridge family.

**Diagram P18:** Use Agent Space ID, execution ID and the relevant summary record type. A task ID is not an execution ID. These are investigation/mitigation events; custom and prevention runs are excluded. EventBridge does not carry the summary body; absence of the ID is valid. Validation and missing-result handling are customer practice. See [[Diagram_Atlas#P18 — Completion evidence retrieval]].

**Primary references:** [S069](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html) [S075](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html)

## 41 · Retries, cancellation and approval need separate handling

**Section:** Operating the system

CreateBacklogTask offers clientToken for idempotent task creation; it does not make all external side effects idempotent. Deleting a custom definition does not cancel its running invocation. Recording an action approval and resuming execution are separate API steps.

**Primary references:** [S051](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_CreateBacklogTask.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S079](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-managing-custom-agents.html) [S099](https://docs.aws.amazon.com/boto3/latest/reference/services/devops-agent/client/update_approval_action.html) [S092](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_SendMessageContext.html)

## 42 · Operate within current feature and capacity boundaries

**Section:** Operating the system

Availability and quotas are time-sensitive. Investigations default to three concurrent runs and prevention to one; the detailed quota table contains the full published set. Billing is cumulative active agent time rather than incident wall-clock duration.

**Primary references:** [S019](https://aws.amazon.com/about-aws/whats-new/2026/03/aws-devops-agent-generally-available/) [S097](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html) [S086](https://docs.aws.amazon.com/devopsagent/latest/userguide/quotas.html) [S093](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html) [S020](https://aws.amazon.com/devops-agent/pricing/)

## 43 · Validate the whole operational contract

**Section:** Operating the system

These are recommended customer adoption checks. The dossier diagrams were documentation-reviewed and rendered, but no live customer environment was deployed. Define business outcomes before enabling recurring invocation. Test the whole system rather than only the prose quality of the final answer.

**Primary references:** [F06](https://www.anthropic.com/research/demystifying-evals-for-ai-agents)

## 44 · Use one contract from primer to advanced system

**Section:** Close

Close by revisiting a single case through all four layers. The practical design artifact is the task contract plus an explicit acceptance owner. For questions, use the role matrix, integration contracts, diagram atlas and source-conflict note.
