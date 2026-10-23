---
id: er-security-lineage
kind: diagram
title: 'Security Agent: finding, repair and revalidation lineage'
refs:
- S-11
- S-M05
---

<!-- block: b-8509dc38f4ec52c6abb6 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-103d7cbf2a4c5f2ab807 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"S-Run" [label="[AWS] Penetration-test run\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Finding" [label="[AWS] Penetration-test finding\nresult record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Revalidation" [label="[AWS] Revalidation job\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-SelectedResult" [label="[DOC] Finding-to-revalidation\nresult\nnormalized association",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Remediation" [label="[AWS] Remediation attempt\noperation record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Patch" [label="[EXT] Patch or pull request\nchange artifact",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Target" [label="[EXT] Deployed test application\ncustomer workload",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Issue" [label="[EXT] Jira issue\nexternal work record",fillcolor="#FCE8D5",color="#C78335",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Run" -> "S-Finding" [label="produces evidence\n1 : 0..*",style="solid"];
"S-Finding" -> "S-SelectedResult" [label="is evaluated in\n1 : 0..*",style="dashed"];
"S-Revalidation" -> "S-SelectedResult" [label="reports selected results\n1 : 1..*",style="dashed"];
"S-Finding" -> "S-Remediation" [label="initiates proposal work\n? : ?",style="solid"];
"S-Remediation" -> "S-Patch" [label="produces proposed change\n? : ?",style="solid"];
"S-Run" -> "S-Target" [label="assesses running system\n0..* : ?",style="solid"];
"S-Revalidation" -> "S-Target" [label="retests selected evidence\n0..* : ?",style="solid"];
"S-Finding" -> "S-Issue" [label="may be linked\n? : ?",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
