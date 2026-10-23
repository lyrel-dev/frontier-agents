---
id: guide-architecture
kind: guide
product: architecture
title: Cross-service architecture
output: guides/architecture.html
references:
  AS01: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-what-is-a-devops-agent-topology.html
  AS02: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  AS03: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
  AS04: https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent-devops-agent-memories.html
  AS05: https://docs.aws.amazon.com/devopsagent/latest/userguide/whats-new.html
  AS06: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
  AS07: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  AS08: https://docs.aws.amazon.com/devopsagent/latest/userguide/configuring-integrations-and-knowledge-connecting-mcp-servers.html
  AS09: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
  AS10: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-working-with-directed-actions.html
  AS11: https://docs.aws.amazon.com/securityagent/latest/userguide/perform-penetration-test.html
  AS12: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
  AS13: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
  AS14: https://docs.aws.amazon.com/securityagent/latest/userguide/revalidate-findings.html
  AS30: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
  AS31: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  AS32: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  AS401: https://docs.aws.amazon.com/securityagent/latest/userguide/review-penetration-findings.html
  AS50: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
  AS501: https://docs.aws.amazon.com/devopsagent/latest/userguide/custom-agents-executing-custom-agents.html
  AS502: https://docs.aws.amazon.com/securityagent/latest/userguide/provide-testing-credentials.html
  AS503: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
  AS51: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  AS52: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  AS53: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
  AS701: https://docs.aws.amazon.com/devopsagent/latest/userguide/working-with-devops-agent-custom-agents-index.html
  AS702: https://docs.aws.amazon.com/securityagent/latest/userguide/understand-lifecycle.html
  AS703: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
---

<!-- block: b-18cf6fc17784595f8fef -->
# Architecture of AWS operational agents

<!-- block: b-59b5ab725d225b35b6bf -->
Concept ownership, product resources, execution, and evidence

<!-- block: b-2bae2c1b9cbe5a059e29 -->
AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent expose different configuration resources, execution records, and retained state. This guide defines the concepts used by the documentation and maps them to the product-specific models. It does not define a common AWS resource schema or cross-service runtime. [AS30] [AS31] [AS32]

<!-- block: b-03adbd5f0ce15fef8217 -->
Start with entity ownership and resource identity. The following chapters compare integrations, retained context, authorization, execution lifecycle, and evidence handoffs. The operational-review example combines reviewed outputs while retaining each service's configuration and permissions.

<!-- block: b-f7fe2bd1e4455cac8ea8 -->
**Reading conventions.** Product statements link to official AWS documentation. Configuration recommendations and verification procedures are team guidance; the proposed tests and synthetic examples have not been executed against AWS. Lifecycle tables describe service behavior and operator actions, not an API status enumeration unless explicitly cited. DOC (blue), AWS (green), and EXT (orange) identify concept ownership. Source-review dates and qualifications are recorded in the source registers.

<!-- block: b-87efebb519035fd6a0d9 -->
Start with the agent overview and workflow walkthroughs. Use the subsequent capability chapters for detailed setup, lifecycle behavior and troubleshooting. The use-case catalog remains separate and unchanged.
