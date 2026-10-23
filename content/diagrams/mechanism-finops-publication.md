---
id: mechanism-finops-publication
kind: diagram
title: FinOps tasks and destination-specific authorization
refs:
- F-03
- F-M05
- F-M06
---

<!-- block: b-5d600b942c1b54ebbccf -->
Conversations can request publication directly; explicit tasks and automations use the task queue. Jira confirmation depends on invocation mode. Slack has no per-message approval prompt. Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.

<!-- block: b-5c768c3f94505f79b1f1 -->
```dot
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];

manual [label="AWS · On-demand task request"];
chat [label="AWS · Conversation analysis\nDirect answer or action request"];
auto [label="AWS · Schedule / anomaly automation"];
task [label="AWS · Queued task and analysis\nSource reads and result"];
jira [label="AWS · Jira action\nInteractive: confirm\nAutomation: setup authorization"];
slack [label="AWS · Slack action\nNo per-message approval prompt"];
external [label="EXT · Project / channel record\nExternal audience and retention",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
check [label="DOC · Delivery verification\nInspect actual destination before retry",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
manual -> task [label="explicit task request"];
chat -> jira [label="direct requested action"];
chat -> slack [label="direct requested action"];
auto -> task [label="eligible occurrence"];
task -> jira [label="configured action"];
task -> slack [label="configured action"];
jira -> external;
slack -> external;
external -> check [style=dashed];
{rank=same;manual;auto;chat}
{rank=same;jira;slack}
```
