---
id: er-security-scope
kind: diagram
title: 'Security Agent: shared configuration and application scope'
refs:
- S-01
- S-10
---

<!-- block: b-e426f72d3a5154c99000 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-a5cff8f146115969b63b -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"S-Tenant" [label="[AWS] Shared service scope\ndocumented scope",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Space" [label="[AWS] Agent Space\nservice resource",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Registration" [label="[AWS] Integration registration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Connection" [label="[AWS] Agent Space source\nconnection\nconfiguration association",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Repository" [label="[EXT] Repository or design source\nsource artifact",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Pack" [label="[AWS] Security requirement pack\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Requirement" [label="[AWS] Security requirement\nconfiguration item",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Pentest" [label="[AWS] Penetration-test\nconfiguration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Tenant" -> "S-Space" [label="organizes application scopes\n1 : 0..*",style="dashed"];
"S-Registration" -> "S-Connection" [label="authorizes selection\n? : 0..*",style="solid"];
"S-Space" -> "S-Connection" [label="selects sources\n1 : 0..*",style="solid"];
"S-Connection" -> "S-Repository" [label="references source\n0..* : ?",style="solid"];
"S-Tenant" -> "S-Pack" [label="shares criteria\n1 : 0..*",style="solid"];
"S-Pack" -> "S-Requirement" [label="contains\n1 : 0..*",style="solid"];
"S-Space" -> "S-Pentest" [label="contains configuration\n1 : 0..*",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
