---
id: er-devops-incidents
kind: diagram
title: 'DevOps Agent: incident records and directed-action boundary'
refs:
- D-14
- D-06
- D-M06
---

<!-- block: b-938c0eaee135524190f3 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-abe184d93abd5567b51d -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"D-Signal" [label="[AWS] Incident signal\noperational record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Investigation" [label="[AWS] Investigation\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Feedback" [label="[AWS] Investigation feedback\noperational record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Memory" [label="[AWS] Memory entry\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Chat" [label="[AWS] Chat conversation\ninteraction record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Approval" [label="[AWS] Directed-action approval\nauthorization event",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Role" [label="[AWS] Resource and operator IAM\nroles\ncross-service resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"D-Signal" -> "D-Investigation" [label="links or starts\n0..* : 0..1",style="dashed"];
"D-Investigation" -> "D-Feedback" [label="receives correction\n1 : ?",style="solid"];
"D-Investigation" -> "D-Memory" [label="informs later synthesis\n? : ?",style="solid"];
"D-Chat" -> "D-Approval" [label="requests action authorization\n? : 0..*",style="solid"];
"D-Approval" -> "D-Role" [label="permits scoped use\n? : ?",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
