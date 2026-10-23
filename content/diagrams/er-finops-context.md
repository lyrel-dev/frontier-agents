---
id: er-finops-context
kind: diagram
title: 'FinOps Agent: retained inputs and session context'
refs:
- F-10
- F-M02
- F-M03
- F-M04
---

<!-- block: b-ab0254f4df355eeda24a -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-1f37ad6632dc5db28588 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"F-Agent" [label="[AWS] FinOps agent instance\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-File" [label="[AWS] Context file\nretained input",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Memory" [label="[AWS] Persistent memory\nmanaged retained state",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Conversation" [label="[AWS] Conversation\ninteraction record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Summary" [label="[AWS] Conversation summary\nderived context",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Runtime" [label="[AWS] Session runtime\nephemeral execution component",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"F-Agent" -> "F-Conversation" [label="retains\n1 : 0..*",style="solid"];
"F-Agent" -> "F-File" [label="retains reference inputs\n1 : 0..*",style="solid"];
"F-Agent" -> "F-Memory" [label="retains contextual state\n1 : ?",style="solid"];
"F-File" -> "F-Runtime" [label="is loaded for a session\n? : ?",style="solid"];
"F-Memory" -> "F-Runtime" [label="is loaded for a session\n? : ?",style="solid"];
"F-Conversation" -> "F-Summary" [label="compacts older messages\n1 : ?",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
