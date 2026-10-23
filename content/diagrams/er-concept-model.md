---
id: er-concept-model
kind: diagram
title: The documentation model and its AWS resource bindings
refs:
- A-10
- A-11
---

<!-- block: b-86f11e758683547daf9c -->
The blue entities are the approved explanatory vocabulary. Green examples are named product configurations, not equivalent resources. Orange nodes retain the external evidence and review boundary. Product diagrams refine this model.

<!-- block: b-d4b609a5e9aa5310940e -->
```dot
rankdir=TB; nodesep=0.25; ranksep=0.4; node [fontsize=11,margin="0.10,0.07"]; edge [fontsize=10];
"C-USECASE" [label="[DOC] Use case\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-VARIANT" [label="[DOC] Use-case variant\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-WORKFLOW" [label="[DOC] Workflow\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-STEP" [label="[DOC] Workflow step\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-CAPABILITY" [label="[DOC] Capability group\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-MECHANISM" [label="[DOC] Mechanism explanation\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-FEATURE" [label="[DOC] Feature reference\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-PROFILE" [label="[DOC] Implementation profile\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"C-BINDING" [label="[DOC] Resource binding\ndocumentation concept",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"X-EVIDENCE" [label="[EXT] Source evidence\nexternal evidence or process",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"X-REVIEW" [label="[EXT] Engineering review\nexternal evidence or process",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"C-USECASE" -> "C-VARIANT" [label="has optional variants",style=dashed];
"C-USECASE" -> "C-WORKFLOW" [label="is achieved through",style=dashed];
"C-WORKFLOW" -> "C-STEP" [label="orders",style=dashed];
"C-STEP" -> "C-MECHANISM" [label="uses conditionally",style=dashed];
"C-CAPABILITY" -> "C-MECHANISM" [label="groups explanations",style=dashed];
"C-MECHANISM" -> "C-FEATURE" [label="uses documented facilities",style=dashed];
"C-PROFILE" -> "C-USECASE" [label="implements selected variant",style=dashed];
"C-PROFILE" -> "C-BINDING" [label="specifies configuration",style=dashed];
"C-FEATURE" -> "C-BINDING" [label="maps to actual types",style=dashed];
"X-EVIDENCE" -> "C-STEP" [label="supplies observations",style=dashed];
"C-STEP" -> "X-REVIEW" [label="provides result for acceptance",style=dashed];
"D-Custom" [label="[AWS] Custom-agent definition\nasset subtype",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"C-BINDING" -> "D-Custom" [label="product-specific example",style=dashed];
"S-Pentest" [label="[AWS] Penetration-test\nconfiguration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"C-BINDING" -> "S-Pentest" [label="product-specific example",style=dashed];
"F-Automation" [label="[AWS] Automation\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"C-BINDING" -> "F-Automation" [label="product-specific example",style=dashed];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
