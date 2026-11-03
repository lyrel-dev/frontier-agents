---
title: Agent mechanism catalogue
id: obsidian-devops-mechanism-catalog
aliases: []
tags:
- aws/devops-agent
- agents
- devops
- concept-catalogue
type: concept-catalogue
created: '2026-10-31'
updated: '2026-10-31'
source_cutoff: '2026-10-31'
status: documentation-vetted
related:
- '[[00_Start_Here]]'
- '[[Source_Index]]'
- '[[Agent_Foundations]]'
- '[[Platform_Capabilities]]'
kind: obsidian-note
product: devops
---

<!-- block: obsidian-devops-mechanism-catalog-body -->
# Agent mechanism catalogue

This catalogue expands the seven functional families used by the primer. It is a coverage checklist for analyzing agent systems, not a claim that every agent implements every mechanism or that AWS DevOps Agent exposes every underlying option. Framework-specific names and algorithms change; the responsibility each mechanism serves is the stable organizing principle.

## 1. Reasoning, planning and run state

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Model inference and structured decisions | Produce a response, classification, plan or tool request | Can the consumer validate the expected result shape? |
| Instructions and task constraints | State objective, scope, standards and stop conditions | What counts as success or an escalation? |
| Planning and decomposition | Identify work and dependencies | Which steps require new evidence before selection? |
| State and checkpoints | Record actual progress and support continuation | Which calls ran; which results or decisions are pending? |
| Context-window management | Select, summarize or move working material | What would be lost or distorted during continuation? |

Planning is intended work; state records actual work. A checkpoint and long-term memory serve different purposes. [F07](https://strandsagents.com/docs/user-guide/sdk/agents/agent-loop/) [F10](https://strandsagents.com/docs/user-guide/sdk/agents/) [F04](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)

## 2. Tools, integrations, protocols and execution

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Tool schema and description | Advertise inputs, result and effects | Is the operation narrowly and accurately described? |
| API / adapter | Implement a service operation | Does it preserve errors and stable identifiers? |
| MCP integration | Exchange available tool and context capabilities | Which supported features and tool scope are enabled? |
| Agent delegation interface | Assign a bounded task to another agent | What are its task, status, evidence and cancellation contracts? |
| Browser / HTTP interaction | Exercise a user interface or API | Which application identity and data may be changed? |
| Code execution environment | Compute over information or run verification | What filesystem, network, credentials and limits apply? |
| Network and provider connection | Reach and authenticate to an external system | Is failure connectivity, identity, permission or tool behavior? |

Tool correctness and integration availability must be evaluated separately. Document the operation's effect rather than assuming all tool calls are reads. AWS exposes distinct MCP, A2A, release-testing and investigation-Sandbox paths. [F05](https://www.anthropic.com/research/writing-tools-for-agents) [F03](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) [S043](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S093](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html)

## 3. Context, retrieval, skills and memory

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Current context | Supply material used for the next model decision | Is the necessary evidence present and attributable? |
| Knowledge source | Hold reference facts, code, runbooks or topology | Who owns accuracy and freshness? |
| Retrieval and selection | Find relevant information from larger stores | Is important contrary evidence omitted? |
| Procedural skill | Supply steps and supporting references for a task | When does it apply, and how is completion judged? |
| Persistent memory | Retain information for subsequent tasks | What was saved, when was it true, and who may edit it? |
| Provenance and versioning | Preserve source and revision context | Can a stale or disputed fact be traced and replaced? |

Retrieval can use different indexing and selection methods; this dossier does not claim an undocumented embedding, ranking or knowledge-graph implementation inside AWS. The observable concern is whether relevant, current information reaches the task. [F04](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

## 4. Identity, authority and execution controls

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Authentication | Establish client or service identity | Which identity is actually making the call? |
| Authorization | Permit operations on resources | What does the effective policy allow? |
| Credential handling | Supply scoped access material | Where are credentials stored, rotated and applied? |
| Guardrail and argument checks | Constrain eligible behavior | What is prevented, and what remains the owner's responsibility? |
| Human approval | Accept a specific proposed action | Which operation, resource, duration and execution does it cover? |
| Isolation and limits | Bound execution resources and effects | What can the runtime reach, and what ends a run? |

These controls are not interchangeable. A prompt is guidance; a permission is an authorization rule; an approval is a scoped decision. [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S093](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html)

## 5. Orchestration and collaboration

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Sequence / graph | Encode required dependencies | Which transitions are deterministic? |
| Routing | Select the relevant worker or workflow | What input and fallback decide the route? |
| Parallel execution | Run independent tasks concurrently | Who combines results and resolves disagreement? |
| Delegation / handoff | Assign a bounded subtask or transfer control | Which context, tools and result contract cross the boundary? |
| Durable controller / ledger | Preserve cross-system process state | Can work reconcile after a restart or long delay? |
| Retry / timeout / cancellation | Handle incomplete or failed work | Could repetition duplicate an external effect? |
| Human decision gate | Accept consequential transitions | Who is accountable for the decision and exceptions? |

The controller and ledger described here are design responsibilities. They are not asserted as a configurable AWS DevOps Agent workflow engine. [F08](https://strandsagents.com/docs/user-guide/sdk/multi-agent/multi-agent-patterns/) [F09](https://www.anthropic.com/research/multi-agent-research-system)

## 6. Triggers, outputs and effects

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Manual request | Start a task with explicit intent | Is scope sufficiently clear? |
| Schedule | Start recurring work | Are overlap, staleness and capacity handled? |
| Event / webhook | Start or inform work from a change | Is the event authenticated, filtered and correlated? |
| Stream / status API | Expose ongoing and terminal state | Which interface's vocabulary is being interpreted? |
| Artifact / structured result | Preserve a work product | Does the result meet the consumer's schema and evidence contract? |
| Recommendation | Propose subsequent work | Who decides and implements it? |
| Notification | Inform a person or system | What does receipt prove, and what must still be verified? |
| External mutation | Change a target system | Is there observed evidence of the actual effect? |

Invocation, completion, output availability and business acceptance are distinct events. [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S069](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html)

## 7. Evaluation, feedback and improvement

| Mechanism | Responsibility | Operational question |
| --- | --- | --- |
| Execution trace and audit | Show actions, data and decisions | Can the conclusion be traced to observations? |
| Usage and capacity metrics | Observe cost, volume and limits | Is the workload operating within its budget and quotas? |
| Representative test cases | Exercise realistic successes and failures | What environment state demonstrates correctness? |
| Grading and outcome checks | Assess the record and observed result | Are criteria explicit, and can the grader be wrong? |
| Feedback | Correct a particular interpretation or behavior | What changes after the correction? |
| Knowledge / configuration improvement | Improve future task execution | Which prompt, skill, memory or integration revision changed? |
| Engineering improvement | Change the underlying service | Did the deployed control reduce the operational problem? |

Evaluate the model plus runtime plus integrations and acceptance process. A better final explanation does not necessarily imply a better operational outcome. [F06](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S102](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-vended-logs-and-metrics.html)
