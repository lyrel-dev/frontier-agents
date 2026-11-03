---
title: AWS DevOps Agent — start here
id: obsidian-devops-00-start-here
aliases:
- AWS DevOps Agent overview
tags:
- aws/devops-agent
- agents
- devops
- index
type: index
created: '2026-10-31'
updated: '2026-10-31'
source_cutoff: '2026-10-31'
status: documentation-vetted
related:
- '[[AWS_DevOps_Agent_Presentation]]'
- '[[AWS_DevOps_Agent_Framework]]'
kind: obsidian-note
product: devops
---

<!-- block: obsidian-devops-00-start-here-body -->
# Start here

This Markdown dossier begins with an agent primer, develops a mechanism taxonomy, maps DevOps roles to AWS platform capabilities, and then explains orchestration through operational cases and custom extensions.

## Choose a reading route

| Goal | Open |
| --- | --- |
| Present the material | [[AWS_DevOps_Agent_Presentation]] |
| Prepare the talk | [[Presentation_Notes]] |
| Read the complete narrative | [[AWS_DevOps_Agent_Framework]] |
| Study the mechanism taxonomy | [[Agent_Foundations]] and [[Mechanism_Catalog]] |
| Compare agent roles and controls | [[Agent_Roles_and_Capabilities]] and [[Platform_Capabilities]] |
| Implement operational patterns | [[Orchestration_and_Use_Cases]] |
| Reuse a diagram | [[Diagram_Atlas]] |
| Resolve a source or interface question | [[Source_Index]] and [[Reference_Evidence_Gaps_and_Demo]] |

## Present in Obsidian

Extract the folder and open it as a vault, or copy its Markdown notes into an existing vault. Enable Obsidian's core **Slides** plugin, open the presentation note, then choose **Start presentation** from the command palette or note menu. Slide boundaries are Markdown horizontal rules. YAML properties remain at the start of every note. Mermaid diagrams are fenced code blocks; internal navigation uses wikilinks. No community plugin or custom theme is required. [O01](https://obsidian.md/help/properties) [O02](https://obsidian.md/help/Plugins/Slides) [O03](https://obsidian.md/help/Advanced+formatting+syntax)

The full presentation has **44 slides**, designed for approximately **60–75 minutes plus discussion**. The presenter notes contain explanations and caveats that would otherwise crowd the projected content. Timing is an editorial estimate.

For a shorter briefing, use slides **01, 03, 04, 07, 14, 15, 16, 17, 21, 24, 25, 29, 31, 32, 33, 34, 35, 37, 38, 39, 43, 44**. Keep the primer before the AWS role catalogue and the orchestration explanation before the custom examples.

## Contents and evidence

The core framework has seven mechanism families, the nine named managed-agent roles in the reviewed AWS reference, three operational cases and three custom-agent extensions. The established payments system is fictional and clearly marked as an illustrative customer design. Source-specific implementation detail is preserved in the reference notes below.

| Reference note | Topic chapters |
| --- | --- |
| [[Reference_Agent_Spaces_and_Access]] | Service scope and operating model; Agent Space boundaries and account access; Creating and validating an Agent Space; IAM roles and effective permissions; Operator identity and access lifecycle; Topology discovery and investigation context; Provider registration and scoped associations; Kubernetes and Azure resource access; Migration maintenance and retirement |
| [[Reference_Network_Security_and_Regions]] | Capability status and service boundaries; Private tool connectivity; Private service ingress and connection validation; Regional availability and processing geography; Encryption audit and evidence quality |
| [[Reference_Incident_Response_and_Actions]] | Incident intake and automatic triage; Evidence findings and operator visibility; Feedback review forks and human support; From mitigation proposal to approved change; Action eligibility and approval API |
| [[Reference_Integrations_and_Events]] | Telemetry and operational evidence sources; Tickets collaboration and repository context; Webhook delivery and payload validation; Client access and outbound tool calls; Protocol contracts and authentication boundaries; Lifecycle events and status vocabulary; Retrieving the summary behind a completion event |
| [[Reference_Knowledge_and_Custom_Agents]] | Managed agents and standing instructions; Skills and the knowledge model; Memory stores and continuous learning; Create and scope a custom agent; Invoke custom agents and configure triggers; Custom agent outputs and lifecycle |
| [[Reference_Prevention_and_Operations]] | Evaluate incidents and prevent recurrence; Rank recommendations and prepare implementation; Sandbox computation during investigations; Manage assets and deploy configuration as code; Price usage and observe the service; Platform quotas and operating capacity; Custom agent quotas and adoption practice |
| [[Reference_Release_Management]] | Release readiness workflow; Release reports and trigger controls; Release testing workflow; Test profiles authentication and delivery integration; Execution environments and mutation boundaries |
| [[Reference_Evidence_Gaps_and_Demo]] | Source conflicts and current interpretation; Feature and interface differences to preserve; Demonstration and adoption rehearsal |
| [[Glossary]] | Concept glossary for presenters |

## Validation and maintenance

See [[Validation_and_Use]] for the precise review scope and known limits. Source cutoff: **31 October 2026**. The examples have not been deployed into your environment. Before implementation, confirm current feature availability, integration behavior and acceptance evidence for your own accounts and systems.
