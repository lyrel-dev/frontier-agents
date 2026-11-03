---
title: Platform capabilities and functions
id: obsidian-devops-platform-capabilities
aliases: []
tags:
- aws/devops-agent
- agents
- devops
- reference
type: reference
created: '2026-10-31'
updated: '2026-10-31'
source_cutoff: '2026-10-31'
status: documentation-vetted
related:
- '[[00_Start_Here]]'
- '[[Source_Index]]'
- '[[Orchestration_and_Use_Cases]]'
kind: obsidian-note
product: devops
---

<!-- block: obsidian-devops-platform-capabilities-body -->
# Platform capabilities and their operational functions

An agent role names a responsibility. A platform capability supplies something that makes the responsibility possible: scope, evidence, execution, knowledge, a result surface, or a control. Design from both directions. A cause-analysis role without the relevant telemetry cannot establish a well-supported cause; an integration with no defined task or owner adds a connection without an operational purpose.

## Scope and access

The Agent Space organizes the permitted operational environment, users, integrations and knowledge. Provider registration establishes a connection at account level; an association exposes selected provider capabilities or resources to a space. The exact selection controls depend on the provider. Topology helps agents and operators navigate relationships, while effective IAM and provider permissions determine access. [S104](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html) [S029](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html) [S105](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html)

Human entry and resource inspection have distinct identities. Operator access can use the supported console or identity-provider paths. Investigation roles provide account access; elevated roles participate in the approved-action path. Each connected account has its own investigation role. A human's access to the operator app does not by itself grant every downstream permission. [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S074](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html)

## Capability traceability

| Platform capability | Function and consuming workflow | Evidence of useful operation |
| --- | --- | --- |
| Agent Space | Establish a coherent application and operating scope | Correct accounts, associations and authorized operators |
| Topology | Orient investigation and environmental understanding | Relevant dependencies linked to current evidence |
| Integration toolbox | Query telemetry, code, incidents and specialist context | Successful scoped calls with source and time information |
| Identity and IAM | Authorize people, service calls and supported actions | Effective permissions match intended resources |
| Instructions | Apply standing guidance at session start | New session follows the reviewed guidance |
| Skills | Supply task-specific procedures | Relevant diagnostic procedure is selected and applied |
| Memory | Retain and retrieve contextual information | Referenced knowledge is current and relevant |
| Investigation records | Expose hypotheses, calls, findings and interaction | Operator can inspect the evidence supporting a conclusion |
| Custom trajectory and outputs | Expose run activity, artifacts and recommendations | Requested output exists and meets the task contract |
| Review / prevention | Assess quality and generate improvements | Criteria results or actionable recommendations |
| Directed-action controls | Scope eligible operator-requested mutations | Correct proposal, approval, execution and verification |
| Release evidence | Assess proposed code and deployed behavior | Findings match the commit and application assessed |
| Metrics / quotas / audit | Observe usage, activity and capacity | Limits and failures are visible to the operating team |
| Assets / IaC | Manage reusable configuration and changes | Versioned assets and supported deployment configuration |

The first column uses documented capability families. The third column proposes customer acceptance evidence; it is not a list of AWS-enforced completion criteria. Sources: [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S102](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-vended-logs-and-metrics.html) [S078](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html).

## Execution environments are capability-specific

An environment that executes analysis code is different from the application being tested. Keep that distinction visible in access reviews and demonstrations.

| Environment | Task | Boundary |
| --- | --- | --- |
| Investigation Sandbox | Compute on evidence during an investigation | Optional ephemeral environment with read-only AWS proxy and network controls |
| Managed readiness verification | Build and test proposed code | Separate managed verification environment and readiness guardrails |
| Deployed test application | UI interaction and API behavior checks | Real application requests, including writes, under test credentials |
| External integration | Retrieve evidence or perform a permitted operation | Provider authorization, tool scope and connectivity |

These are different product paths. Investigation Sandbox is not the runtime for every Chat or custom invocation. Readiness guardrails should not be used to describe the effects of application testing. [S093](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html) [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

## Connect platform operation to a named owner

The following ownership assignment is recommended practice. A platform administrator owns space and provider configuration. An identity owner governs operator and service permissions. A responder owns incident interpretation and recovery acceptance. An engineering owner implements prevention recommendations. A release owner accepts versioned release evidence. A custom-agent owner maintains the task definition, trigger and output contract.

This ownership model resolves a common ambiguity: an agent can produce the work product while a different person or workflow owns the consequential operational decision. Record both responsibilities in the task contract.

## Implementation reference

- [[Reference_Agent_Spaces_and_Access]] — setup, roles, identity, topology, provider association, EKS/Azure and retirement.
- [[Reference_Network_Security_and_Regions]] — private paths, availability, encryption, inference geography and audit.
- [[Reference_Integrations_and_Events]] — provider surfaces, webhooks, MCP, A2A, EventBridge and summaries.
- [[Reference_Prevention_and_Operations]] — prevention, Sandbox, assets, IaC, price, metrics and complete quota tables.
