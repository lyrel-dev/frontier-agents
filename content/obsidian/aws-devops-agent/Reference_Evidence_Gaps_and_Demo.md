---
title: Source conflicts, evidence gaps and demonstration
id: obsidian-devops-reference-evidence-gaps-and-demo
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
- '[[AWS_DevOps_Agent_Framework]]'
- '[[Source_Index]]'
kind: obsidian-note
product: devops
---

<!-- block: obsidian-devops-reference-evidence-gaps-and-demo-body -->
# Source conflicts, evidence gaps and demonstration

This reference supplements the primer and operational framework. It preserves source-specific setup and interface detail. Related: [[AWS_DevOps_Agent_Framework]] · [[Source_Index]].

## Source conflicts and current interpretation

A documented discrepancy is a limit on the claim, not a reason to silently select the most convenient version. The following differences affect diagrams or deployment decisions.

| Topic | Difference in official sources | Dossier treatment |
| --- | --- | --- |
| Availability | Some setup introductions say six Regions; dedicated current page lists fifteen. | Use the Regions page and feature-specific preview rows. |
| IAM console-link session | Security and web-app pages say ten minutes; identity setup says thirty. | Omit a universal duration and validate the target environment. |
| At-rest keys | General security text says AWS-managed keys; encryption guide specifies AWS-owned default and optional customer-managed keys. | Use the specialized encryption guide. |
| Workload mutation | Older pages broadly describe reads; directed-actions guide documents guarded writes. | Separate default investigation access from approved chat actions. |
| Grafana writes | Connection guide disables writes; directed-action guide includes mutable Grafana examples. | Show telemetry and triggers; qualify write support pending validation. |
| Datadog authentication | Retrieved connection body emphasizes OAuth; 27 October notes add key and token options. | Cite the dated update; inspect current registration choices before implementation. |

Sources: [S097](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-supported-regions.html) [S095](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-setting-up-iam-identity-center-authentication.html) [S106](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-web-app.html) [S022](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security.html) [S062](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-encryption-at-rest-for-devops-agent.html) [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S037](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-telemetry-sources-connecting-grafana.html) [S033](https://docs.aws.amazon.com/devopsagent/latest/userguide/connecting-telemetry-sources-connecting-datadog.html) [S107](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

## Feature and interface differences to preserve

| Topic | Difference or evidence gap | Dossier treatment |
| --- | --- | --- |
| Learned knowledge | Older pages describe learned skills; current memory guide documents migration. | Use current managed stores and explain the transition. |
| Agent instructions | Older screenshots use Knowledge; October guidance uses managed Agents pages. | Use the newer navigation. |
| Custom triggers | Overview omits events; execution guide supports webhooks. CloudFormation Trigger lists TIME_BASED. | Describe UI support and IaC support separately. |
| Skill executable files | Sandbox note allows code while an older ZIP restriction rejects scripts. | Qualify code execution by Sandbox and verify upload behavior. |
| Release action name | User-guide prose names devops-agent-release-testing; example and AWS repository use devops-agent-qa. | Use the AWS-maintained action repository. |
| Constellation | An AWS managed policy names Agent Space Constellation; complete public workflow is absent. | Record the concept as an evidence gap. Do not imply default sharing. |

Sources: [S073](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-learned-skills.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S026](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-devopsagent-trigger.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) [S093](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-sandbox.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html) [S021](https://github.com/aws-actions/devops-agent-qa) [S007](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AIDevOpsConstellationAccessPolicy.html)

Additional interface distinctions remain explicit throughout the dossier: recommendation UI verbs do not establish an API enum mapping; MCP tool-name limits differ between guide and API schema; current managed policy references can differ from copied tutorial JSON. Release readiness output labels changed after the launch article. Use current operation-specific references for automation.

Sources: [S087](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_Recommendation.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html) [S038](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html) [S081](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_MCPToolDetail.html) [S008](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AIDevOpsOperatorAppAccessPolicy.html) [S058](https://docs.aws.amazon.com/devopsagent/latest/userguide/aws-devops-agent-security-devops-agent-iam-permissions.html) [S089](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-readiness-code-review.html) [S107](https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html)

## Demonstration and adoption rehearsal

The following is a recommended rehearsal plan. It translates the documented features into observable acceptance criteria for a customer environment. It is separate from documentation review.

| Rehearsal | Evidence to capture | Decision supported |
| --- | --- | --- |
| Scope and access | A permitted resource query succeeds and an intentionally excluded query fails. | IAM and provider scope are understood. |
| Synthetic incident | Known fault, input event, triage outcome, timeline and cause assessment. | The investigation explains the known failure with relevant evidence. |
| Steering and review | A message changes the inquiry; fork and Review remain distinguishable. | Operators can guide work and assess quality. |
| Notification and event export | Delivery per destination; summary retrieval with and without a summary ID. | Operational integrations behave as designed. |
| Directed action if enabled | Named request, displayed approval, scoped execution record and recovery check. | Approval, attribution and rollback process are usable. |
| Release preview | Review report, staging test evidence and explicit release-gate behavior. | Delivery teams understand coverage and side effects. |

Begin with one owned workload and representative incident history. Establish who accepts a cause assessment, who approves changes, who owns provider credentials, and who triages recommendations. Measure correctness and evidence quality as well as elapsed resolution time. The AWS AI Service Card describes limitations and does not provide a confidence score that can replace those checks.

Sources: [S014](https://docs.aws.amazon.com/ai/responsible-ai/aws-aidevops-agent/overview.html)

For a shorter presentation, prioritize the service boundary, permission roles, triage, evidence loop, directed actions, knowledge, release execution boundaries, and operational costs. Use provider matrices and API details as appendix material. For an engineering workshop, add the setup, protocol, EventBridge, and rehearsal sections.

## Evaluation naming differs between current guides

The managed-agent roster describes Evaluation as performance scoring and policy compliance checks. The Skills guide labels the Evaluation skill target as proactive recommendations. This is an explicit documentation naming inconsistency. The presentation uses the prevention workflow label and keeps Grader Review distinct, without inventing another agent type. [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html)
