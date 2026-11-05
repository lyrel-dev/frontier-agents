---
title: AWS DevOps Agent — diagram atlas
id: obsidian-devops-diagram-atlas
aliases: []
tags:
- aws/devops-agent
- agents
- devops
- diagrams
type: diagrams
created: '2026-10-31'
updated: '2026-11-05'
source_cutoff: '2026-10-31'
api_addendum_source_cutoff: '2026-11-05'
status: documentation-vetted
related:
- '[[AWS_DevOps_Agent_Presentation]]'
- '[[AWS_DevOps_Agent_Framework]]'
kind: obsidian-note
product: devops
---

<!-- block: obsidian-devops-diagram-atlas-body -->
# Diagram atlas

All diagrams are editable Mermaid source. Captions identify the relationship shown and its evidence boundary. The presentation uses P01–P19; deeper conceptual diagrams remain embedded in the framework chapters. Use [[Validation_and_Use]] for rendering and review scope.

## Investigation API and UI model addendum

The original presentation figures below retain their 31 October 2026 evidence cutoff. The separately reviewed **5 November 2026** addendum adds six ER diagrams in [[Investigation_Data_Model]] and an approval ER diagram, synchronization sequence and historical-capture flow in [[Investigation_UI_Contract]]. They show proposed logical models with explicit native-versus-derived boundaries. See [[Investigation_API_Sources]] for their source pins and rendering review.

## P01 — The agent loop

```mermaid
flowchart LR
  O["Observe"] --> D{"Choose next step"}
  D -->|Need evidence| T["Use permitted tool"]
  T --> O
  D -->|Enough evidence| R["Return result"]
```

*General concept. A conceptual model/tool loop. The runtime executes tools, supplies their results and enforces stop conditions. This is not an AWS internal implementation diagram.*

Sources: [F01](https://www.anthropic.com/research/building-effective-agents) [F07](https://strandsagents.com/docs/user-guide/sdk/agents/agent-loop/)

## P02 — Tools and protocol exchange

```mermaid
sequenceDiagram
  participant H as Agent host
  participant M as MCP server
  participant T as Tool
  participant E as Service
  H->>M: Tool request
  M->>T: Invoke within scope
  T->>E: API request
  E-->>T: Observed result
  T-->>M: Tool result
  M-->>H: Evidence for next step
```

*General concept. Conceptual request/result layering. MCP does not grant the downstream permissions or define the host reasoning process.*

Sources: [F03](https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture) [F05](https://www.anthropic.com/research/writing-tools-for-agents)

## P03 — Assembling useful context

```mermaid
flowchart LR
  I["Instructions"] --> C["Current context"]
  K["Skills and knowledge"] --> R["Select relevant material"]
  M["Stored memories"] --> R
  R --> C
  O["Current observations"] --> C
  C --> A["Agent decision"]
  A -->|Request observation| O
```

*General concept. Context is selected for a current decision. The runtime, a tool or an external event supplies each new observation; the decision requests it. Memory is stored information; saving it is not itself model retraining.*

Sources: [F04](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

## P04 — AWS operating model

```mermaid
flowchart LR
  U["Operator or client"] --> W["Product workflow"]
  W --> M["Managed agents"]
  W --> C["Custom agents"]
  M --> E["Permitted evidence and tools"]
  C --> E
  S["Agent Space configuration"] --> W
  S --> E
```

*Documented relationship. The Agent Space supplies scope and context. Boxes describe public concepts, not physical hosting or an internal scheduler.*

Sources: [S001](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html) [S104](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html) [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

## P05 — Access has separate boundaries

```mermaid
flowchart LR
  H["Human identity"] --> O["Operator app access"]
  O --> S["Agent Space"]
  S --> A["Account A role"]
  S --> B["Account B role"]
  S --> E["Target account elevated role"]
  A --> R["Permitted resource reads"]
  B --> R
  E --> G["Scoped approved action"]
```

*Documented relationship. Each connected account supplies its own investigation role. Operator access and the elevated action path are separate. The elevated role is registered on the target account association. This is not role chaining through a primary investigation role.*

Sources: [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S074](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-limiting-agent-access-in-an-aws-account.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

## P06 — Incident triage

```mermaid
flowchart LR
  E["Incident event"] --> T{"Triage"}
  T -->|Related| L["Link to investigation"]
  T -->|Skip rule| S["Skip"]
  T -->|Proceed| I["Independent investigation"]
  L -.->|Operator unlinks| I
  S -.->|Operator unskips| I
```

*Documented relationship. Linked, Skipped and Proceed are distinct triage outcomes. Operators can correct a link or skip; a skip is not a health verdict.*

Sources: [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

## P07 — Investigation evidence loop

```mermaid
flowchart LR
  I["Incident scope"] --> H["Working hypothesis"]
  H --> T["Query connected evidence"]
  T --> J{"Evidence sufficient?"}
  J -->|Specific gap| H
  J -->|Yes| F["Findings and proposal"]
  O["Operator context"] --> H
```

*Documented relationship. Conceptual evidence workflow. The actual investigation can use parallel work; the drawing is not an exhaustive API state machine.*

Sources: [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html)

## P08 — Directed action gates

```mermaid
flowchart LR
  C["Operator asks in chat"] --> G{"Eligible and permitted?"}
  G -->|No| H["Hold or revise"]
  G -->|Yes| A{"Scoped approval"}
  A -->|Rejected| H
  A -->|Approved| X["Execute eligible action"]
  X --> V["Verify outcome"]
```

*Documented controls with customer verification. Eligibility includes feature opt-in, supported operation, guardrails and effective permissions. Only the operator-directed chat path produces these action approvals. Outcome verification is recommended customer practice.*

Sources: [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html)

## P09 — Three uses of incident history

```mermaid
flowchart LR
  I["Investigation records"] -->|Completed only| G["Requested Review"]
  G --> Q["Quality verdict"]
  I --> P["Prevention evaluation"]
  P --> R["Improvement backlog"]
  I --> L["Learning"]
  L --> M["Reusable managed context"]
```

*Documented relationship. These are separate consumers of incident information. There is no asserted automatic Review-to-prevention-to-Learning chain, and Evaluation naming differs between the managed-agent and Skills guides. The diagram therefore uses the prevention workflow label.*

Sources: [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html)

## P10 — Two release evidence paths

```mermaid
flowchart LR
  C["Proposed change"] --> R["Readiness review"]
  R --> B["Optional build verification"]
  R --> D["Release decision"]
  B --> D
  A["Deployed application"] --> T["UI or API tests"]
  T --> D
```

*Documented capabilities with customer decision. Readiness and deployed-application testing provide different evidence. Their combination at a team release gate is a proposed customer policy. Tests may modify application data.*

Sources: [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)

## P11 — Integration direction

```mermaid
flowchart LR
  C["External client"] -->|Hosted MCP or A2A| A["AWS DevOps Agent"]
  A -->|Configured MCP| T["External tools"]
  A -->|Configured A2A| R["Remote specialist"]
  T --> E["Operational systems"]
  R --> E
```

*Documented relationship. Inbound service access and outbound integrations are different configuration and authorization paths. The remote specialist is not an AWS continuation subagent.*

Sources: [S070](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) [S043](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html) [S049](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-connecting-to-the-devops-agent-mcp-server.html)

## P12 — Private paths are directional

```mermaid
sequenceDiagram
  participant C as Private client
  participant A as DevOps Agent
  participant L as VPC Lattice path
  participant T as Private tool
  C->>A: Service request via PrivateLink
  A->>L: Use configured private connection
  L->>T: Reach permitted endpoint
  T-->>L: Tool response
  L-->>A: Evidence
  A-->>C: Service result
```

*Documented network relationship. PrivateLink serves private client ingress. The private connection and VPC Lattice path reach a private tool. These are separate paths with their own setup.*

Sources: [S103](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-vpc-endpoints-aws-privatelink.html) [S048](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-to-privately-hosted-tools.html)

## P13 — Orchestration ownership

```mermaid
flowchart LR
  C["Customer workflow"] --> A["AWS investigation"]
  A --> T["Assigned tools"]
  A -.-> R["Remote A2A agent"]
  T --> O["Evidence and outputs"]
  R --> O
  O --> L["Customer ledger"]
  L -->|Reconcile| C
```

*Customer architecture using documented interfaces. This example shows an investigation. The customer workflow and ledger are proposed architecture. The optional remote A2A branch represents documented investigation delegation, not an asserted custom-agent tool path. Continuation inside a custom run does not supply this durable customer process.*

Sources: [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html) [S043](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-remote-a2a-agents.html) [S070](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-devops-agent-remote-servers-integrating-with-the-devops-agent-a2a-server.html)

## P14 — Incident recovery case

```mermaid
flowchart LR
  A["Investigate"] --> D{"Decision"}
  D -->|Approved| C["Execute change"]
  D -->|Hold| H["Hold and monitor"]
  C --> V{"Recovered?"}
  V -->|No| A
  V -->|Yes| R["Accept recovery"]
```

*Customer operating pattern. Customer operating pattern. The eligible action path uses documented directed-action controls; the manual path uses the established change process. Holding cannot itself close the incident.*

Sources: [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html)

## P15 — Prevention implementation case

```mermaid
flowchart LR
  R["Recommendation"] --> D{"Keep?"}
  D -->|Defer or discard| H["Record reason"]
  D -->|Keep| I["Implement and deploy"]
  I --> V["Verify implementation"]
  V --> O["Observe impact"]
```

*Customer operating pattern. The service proposes improvements. Implementation ownership, deployment proof and recurrence observation belong to the illustrated customer process.*

Sources: [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S087](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Recommendation.html)

## P16 — Release evidence case

```mermaid
flowchart LR
  C["Pinned candidate"] --> R["Readiness and verification"]
  C --> T["Test candidate deployment"]
  R --> E["Versioned evidence bundle"]
  T --> E
  E --> G{"Human release gate"}
  G -->|Accepted| P["Established delivery"]
  G -->|Not accepted| H["Hold"]
```

*Customer operating pattern. The sequencing and human gate are customer policy. Keep the commit and tested deployment identities attached to every result.*

Sources: [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S021](https://github.com/aws-actions/devops-agent-qa)

## P17 — Custom agent invocation

```mermaid
flowchart LR
  T["Manual schedule or event"] --> A["Custom invocation"]
  C["Prompt tools skills memory"] --> A
  A --> E["Assigned integration tools"]
  E -->|Evidence| A
  A --> O["Trajectory and outputs"]
  O --> R["Customer acceptance"]
```

*Documented relationship. Assigned integration tools and attached stores define task scope; built-in artifact and recommendation tools are also available. Notifications need a destination and instructions; the customer acceptance step is a proposed operating practice.*

Sources: [S052](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-creating-a-custom-agent.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html)

## P18 — Completion evidence retrieval

```mermaid
flowchart LR
  E["Completed event"] --> Q{"Summary ID present?"}
  Q -->|No| H["Record missing summary"]
  Q -->|Yes| L["ListJournalRecords"]
  L --> M["Page and match record ID"]
  M --> V["Validate usable evidence"]
```

*Documented relationship. Use Agent Space ID, execution ID and the relevant summary record type. A task ID is not an execution ID. These are investigation/mitigation events; custom and prevention runs are excluded. EventBridge does not carry the summary body; absence of the ID is valid. Validation and missing-result handling are customer practice.*

Sources: [S069](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-integrating-devops-agent-into-event-driven-applications-using-amazon-eventbridge-index.html) [S075](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html)

## P19 — Established system extension

```mermaid
flowchart LR
  P["Incident intake"] --> W["Customer workflow"]
  W --> A["Agent Space"]
  A --> E["Connected tools"]
  E -->|Evidence| A
  A --> O["Sourced outputs"]
  O --> W
  W --> H["Human gate"]
```

*Illustrative customer architecture. Illustrative existing environment: CloudWatch/Datadog supply telemetry, GitHub/ServiceNow supply change context, and internal MCP supplies ownership and deployment data. The customer workflow keeps a ledger. Provider scope, identity and network access must be configured; no automatic cross-provider synchronization is implied.*

Sources: [S029](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge.html) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) [S045](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-to-ticketing-and-chat-connecting-slack.html)
