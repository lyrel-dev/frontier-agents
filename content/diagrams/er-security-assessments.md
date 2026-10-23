---
id: er-security-assessments
kind: diagram
title: 'Security Agent: assessment configurations and executions'
refs:
- S-10
- S-06
---

<!-- block: b-69d7d85cfce353caa3f5 -->
Colors identify concept ownership; labels distinguish resources, configuration members and derived state. An edge shows source-count : target-count; ? means unspecified. Dashed edges are logical or editorial relationships, not asserted service foreign keys. See the relationship register for qualifications.

<!-- block: b-7b298352cf185a1d8a76 -->
```dot
rankdir=TB; nodesep=0.28; ranksep=0.48; node [fontsize=11.5,margin="0.12,0.08"]; edge [fontsize=10];
"S-Pentest" [label="[AWS] Penetration-test\nconfiguration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Run" [label="[AWS] Penetration-test run\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-CodeConfig" [label="[AWS] Full-code review\nconfiguration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-CodeRun" [label="[AWS] Code review\nexecution record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Design" [label="[AWS] Design review\none-off assessment",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-ThreatConfig" [label="[AWS] Threat-model configuration\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-ThreatRun" [label="[AWS] Threat-model run\nexecution and result record",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Pack" [label="[AWS] Security requirement pack\nservice configuration",fillcolor="#D9F2E5",color="#348761",fontcolor="#152636",style="rounded,filled",shape=box];
"S-Pentest" -> "S-Run" [label="is executed as\n1 : 0..*",style="solid"];
"S-CodeConfig" -> "S-CodeRun" [label="starts full-source scans\n? : 0..*",style="solid"];
"S-Design" -> "S-Design" [label="clones to a new review\n0..1 : 0..*",style="dashed"];
"S-ThreatConfig" -> "S-ThreatRun" [label="is executed as\n1 : 0..*",style="solid"];
"S-Pack" -> "S-CodeRun" [label="supplies enabled criteria\n? : ?",style="solid"];
"S-Pack" -> "S-Design" [label="supplies enabled criteria\n? : ?",style="solid"];
subgraph cluster_ownership {label="Ownership of the definition (not availability)";style="rounded";color="#b5c2cc";rank=same;
legend_0 [label="DOC · Documentation-defined",fillcolor="#DCEBFF",color="#447AC2",style=filled,fontsize=10];
legend_1 [label="AWS · AWS-defined",fillcolor="#D9F2E5",color="#348761",style=filled,fontsize=10];
legend_2 [label="EXT · External / engineering-owned",fillcolor="#FCE8D5",color="#C78335",style=filled,fontsize=10];
legend_0 -> legend_1 -> legend_2 [style=invis];}
```
