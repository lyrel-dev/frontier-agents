---
id: er-finops-scope
kind: diagram
title: 'FinOps Agent: instance access and integration connections'
refs:
- F-01
- F-09
---

<!-- block: b-07addc53cc9255de9814 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-9939234491ce540aadf0 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"F-Agent" [label="[AWS] FinOps agent instance\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-DataRole" [label="[AWS] Agent data role\ncross-service resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-OperatorRole" [label="[AWS] Operator role\ncross-service resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Integration" [label="[AWS] Integration registration\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Connection" [label="[AWS] Agent connection\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Destination" [label="[EXT] Jira project or Slack\nchannel\nexternal destination",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Agent" -> "F-DataRole" [label="uses data access role\n? : 1",style="solid"];
"F-Agent" -> "F-OperatorRole" [label="uses operator role\n? : 1",style="solid"];
"F-Agent" -> "F-Connection" [label="has destination connections\n1 : 0..*",style="solid"];
"F-Integration" -> "F-Connection" [label="authorizes connections\n1 : 0..*",style="solid"];
"F-Connection" -> "F-Destination" [label="selects destination\n? : 1",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
