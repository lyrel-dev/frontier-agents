---
id: er-devops-scope
kind: diagram
title: 'DevOps Agent: scope, providers and execution'
refs:
- D-01
- D-13
---

<!-- block: b-0f43f6c17f6d520298a1 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-3383fb432f8c5ef29e50 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"D-Space" [label="[AWS] Agent Space\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Registration" [label="[AWS] Provider registration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Association" [label="[AWS] Service association\nAPI resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Tool" [label="[AWS] Selected tool\nconfiguration member",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Custom" [label="[AWS] Custom-agent definition\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Trigger" [label="[AWS] Custom-agent trigger\nschedule configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Invocation" [label="[AWS] Custom-agent invocation\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Source" [label="[EXT] Telemetry or repository\nsource\nsource system",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Space" -> "D-Association" [label="contains\n1 : 0..*",style="solid"];
"D-Registration" -> "D-Association" [label="is associated through\n1 : 0..*",style="solid"];
"D-Association" -> "D-Tool" [label="selects\n? : 0..*",style="solid"];
"D-Space" -> "D-Custom" [label="stores\n1 : 0..*",style="solid"];
"D-Custom" -> "D-Tool" [label="selects subset\n? : 0..*",style="solid"];
"D-Custom" -> "D-Invocation" [label="is executed as\n1 : 0..*",style="solid"];
"D-Custom" -> "D-Trigger" [label="has schedules\n1 : 0..*",style="solid"];
"D-Trigger" -> "D-Invocation" [label="initiates\n0..1 : 0..*",style="dashed"];
"D-Tool" -> "D-Source" [label="reads authorized evidence\n? : ?",style="dashed"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
