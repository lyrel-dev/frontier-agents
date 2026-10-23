---
id: er-finops-work
kind: diagram
title: 'FinOps Agent: conversation, automation and task records'
refs:
- F-09
- F-03
---

<!-- block: b-2fdf6b4c60305b6b974d -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-96d848267fa95c10aff4 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"F-Agent" [label="[AWS] FinOps agent instance\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Conversation" [label="[AWS] Conversation\ninteraction record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Automation" [label="[AWS] Automation\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Rule" [label="[AWS] EventBridge managed rule\ncross-service resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Task" [label="[AWS] Task\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Artifact" [label="[AWS] Report artifact\noutput record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Source" [label="[DOC] AWS cost and operational\nevidence\nnormalized evidence family",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Agent" -> "F-Conversation" [label="retains\n1 : 0..*",style="solid"];
"F-Agent" -> "F-Task" [label="queues and retains\n1 : 0..*",style="solid"];
"F-Agent" -> "F-Automation" [label="contains future-work rules\n1 : 0..*",style="solid"];
"F-Automation" -> "F-Task" [label="creates on each match\n0..1 : 0..*",style="dashed"];
"F-Conversation" -> "F-Task" [label="may explicitly request\n? : 0..*",style="solid"];
"F-Rule" -> "F-Automation" [label="delivers supported events\n? : ?",style="solid"];
"F-Task" -> "F-Artifact" [label="can produce reports\n? : 0..*",style="dashed"];
"F-Task" -> "F-Source" [label="queries authorized evidence\n? : ?",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
