---
title: Glossary for presenters
id: obsidian-devops-glossary
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

<!-- block: obsidian-devops-glossary-body -->
# Glossary for presenters

This reference supplements the primer and operational framework. It preserves source-specific setup and interface detail. Related: [[AWS_DevOps_Agent_Framework]] · [[Source_Index]].

## Concept glossary for presenters

Agent Space: the logical operational and access context. Primary account: the AWS account owning the space. Secondary account: an associated source of workload evidence. Association: the selected relationship between a space and a registered capability. Provider or Service: the account-level registration for an external integration.

Sources: [S104](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-are-devops-agent-spaces.html) [S040](https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-multiple-aws-accounts.html) [S023](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_devopsagent-readme.html)

Topology: the discovered and learned resource relationship view. Investigation: a formal operational inquiry. Triage: the decision to link, skip, or proceed for an incoming incident. Execution: an individual run of agent work. Journal: its recorded messages, evidence, and tool activity. Mitigation proposal: suggested corrective action requiring separate implementation.

Sources: [S105](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html) [S010](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-autonomous-incident-response.html) [S075](https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_ListJournalRecords.html)

Directed action: an explicitly requested operation under configured controls. Elevated role: additional AWS credentials available to approved eligible actions. Approval pattern: the operation and arguments a human authorizes. Review: a separate assessment of a completed investigation by the Grader. Prevention evaluation: analysis of incident history to generate improvements.

Sources: [S108](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html) [S099](https://docs.aws.amazon.com/boto3/latest/reference/services/devops-agent/client/update_approval_action.html) [S091](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-reviewing-investigations.html) [S084](https://docs.aws.amazon.com/devopsagent/latest/userguide/production-operations-proactive-incident-prevention.html)

Instructions: guidance loaded at session start. Skill: a reusable task procedure. Memory store: a named collection of informational records. Reflection: a corrective lesson from investigation feedback. Learning agent: the managed capability that refreshes environment understanding. Custom agent: a user-defined prompt and selected tools, skills, and memory.

Sources: [S004](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-agent-instructions.html) [S060](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-skills.html) [S059](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html) [S077](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-managed-agents.html) [S056](https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html)

Asset: a versioned service resource for knowledge or configuration content. Trigger: a scheduled or event-based invocation rule, with interface-specific support. Trajectory: a custom invocation's activity record. Artifact: persisted output such as a report. Recommendation: a tracked improvement item. Test profile: reusable release-test target and configuration.

Sources: [S078](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-managing-assets.html) [S063](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html) [S055](https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-custom-agent-outputs.html) [S090](https://docs.aws.amazon.com/devopsagent/latest/userguide/release-management-release-testing.html)
