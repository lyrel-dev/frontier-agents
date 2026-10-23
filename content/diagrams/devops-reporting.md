---
id: devops-reporting
kind: diagram
title: Configured operational-report workflow
refs:
- D-07
---

<!-- block: b-493545674d8351079b4d -->
The team defines the report period and selected evidence. An invocation queries sources, produces a report, and exposes results for review. Schedule timing and the reporting window are separate configuration decisions.

<!-- block: b-edd319b33c665e97b004 -->
```dot
rankdir=TB;
contract [label="Report specification\nService, window, aggregation, audience"];
definition [label="Custom-agent definition\nPrompt, tools, skills, memory"];
trigger [label="On-demand or scheduled start\nFlexible schedule window applies"];
query [label="Invocation\nQuery selected logs and metrics"];
report [label="Report\nMeasured changes and missing signals"];
review [label="Engineering review\nReproduce a material observation"];
publication [label="Approved destination\nOnly when separately configured"];
contract -> definition [label="defines the task"];
definition -> query [label="supplies configuration"];
trigger -> query [label="starts work"];
query -> report [label="synthesizes evidence"];
report -> review [label="checked"];
review -> publication [label="team publication path",style=dashed];
```
