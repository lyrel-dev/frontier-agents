---
id: er-devops-knowledge
kind: diagram
title: 'DevOps Agent: stored knowledge and configuration references'
refs:
- D-13
- D-M07
---

<!-- block: b-4b9d465b21f5550aa4f8 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-d1bd6f05d83950b3bb95 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"D-Space" [label="[AWS] Agent Space\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Custom" [label="[AWS] Custom-agent definition\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Skill" [label="[AWS] Skill\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Store" [label="[AWS] Memory store\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Memory" [label="[AWS] Memory entry\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Version" [label="[AWS] Memory content version\nversion record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Investigation" [label="[AWS] Investigation\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Space" -> "D-Custom" [label="stores\n1 : 0..*",style="solid"];
"D-Custom" -> "D-Skill" [label="references asset IDs\n0..* : 0..*",style="solid"];
"D-Custom" -> "D-Store" [label="attaches asset IDs\n0..* : 0..*",style="solid"];
"D-Space" -> "D-Store" [label="scopes\n1 : 0..*",style="solid"];
"D-Store" -> "D-Memory" [label="groups\n1 : 0..*",style="solid"];
"D-Memory" -> "D-Version" [label="has content versions\n1 : 1..*",style="solid"];
"D-Investigation" -> "D-Memory" [label="informs later synthesis\n? : ?",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
