---
id: guide-finops
kind: guide
product: finops
title: AWS FinOps Agent
output: guides/finops.html
references:
  FS01: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
  FS02: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
  FS03: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
  FS04: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
  FS05: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
  FS06: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
  FS07: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
  FS08: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  FS09: https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html
  FS10: https://docs.aws.amazon.com/finops-agent/latest/userguide/quotas.html
  FS11: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
  FS12: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
  FS13: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
  FS14: https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_GetCostAndUsage.html
  FS401: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
  FS402: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
  FS403: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  FS404: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
  FS405: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
  FS406: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
  FS407: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
  FS408: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
  FS409: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
  FS50: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
  FS501: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
  FS502: https://docs.aws.amazon.com/finops-agent/latest/userguide/creating-an-agent.html
  FS503: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
  FS504: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
  FS505: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  FS506: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
  FS507: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
  FS508: https://docs.aws.amazon.com/finops-agent/latest/userguide/cross-region-inference.html
  FS509: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
  FS51: https://docs.aws.amazon.com/finops-agent/latest/userguide/setting-up.html
  FS510: https://docs.aws.amazon.com/finops-agent/latest/userguide/automated-anomaly-response.html
  FS52: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
  FS53: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
  FS54: https://docs.aws.amazon.com/finops-agent/latest/userguide/data-protection.html
  FS55: https://docs.aws.amazon.com/finops-agent/latest/userguide/jira-integration.html
  FS56: https://docs.aws.amazon.com/finops-agent/latest/userguide/slack-integration.html
  FS57: https://docs.aws.amazon.com/finops-agent/latest/userguide/agent-guardrail-control.html
  FS58: https://docs.aws.amazon.com/finops-agent/latest/userguide/custom-cost-reporting.html
  FS701: https://docs.aws.amazon.com/finops-agent/latest/userguide/what-is.html
  FS702: https://docs.aws.amazon.com/finops-agent/latest/userguide/task-management.html
  FS703: https://docs.aws.amazon.com/finops-agent/latest/userguide/context-files-and-memory.html
---

<!-- block: b-6e58f88427285dcca2a5 -->
# AWS FinOps Agent

<!-- block: b-4e1c81491ffb5a829f26 -->
Instance configuration, cost analysis, context, and automation

<!-- block: b-2da99b4fefe851119b14 -->
AWS FinOps Agent is documented as a preview service for cost inquiry, reporting, anomaly investigation, and interpretation of upstream recommendations. Its instance retains organizational context and contains task automations and destination connections. A conversation, a queued task, and an automation are different objects. [FS501] [FS502] [FS503]

<!-- block: b-25e2a2d5b35054d38da1 -->
This guide separates those configuration facilities from their mechanisms: contextual reuse, conversation compaction, scheduled task creation, anomaly-event matching, and publication authorization. It then describes the managed analytical functions and their outputs. The use-case catalog supplies the approved operational objectives rather than another list of platform features.

<!-- block: b-8a008757ba46527ba6a3 -->
**Reading conventions.** The dimensions below organize documented FinOps facilities; they do not imply a DevOps-style custom-agent API, arbitrary MCP tool registry, or shared cross-service memory. Official sources support product behavior. DOC/AWS/EXT colors identify ownership. Financial examples use synthetic values; verification procedures are proposed, not live account results.

<!-- block: b-f1da201b26be5043a299 -->
Start with the agent overview and workflow walkthroughs. Use the subsequent capability chapters for detailed setup, lifecycle behavior and troubleshooting. The use-case catalog remains separate and unchanged.
