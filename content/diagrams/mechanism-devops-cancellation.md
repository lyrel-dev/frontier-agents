---
id: mechanism-devops-cancellation
kind: diagram
title: 'Custom work: future triggers and current invocations'
refs:
- D-07
---

<!-- block: b-c26bc6c577235d74b657 -->
Pausing a schedule stops future starts. Cancelling an invocation preserves completed evidence and may not interrupt a tool call already in progress. The scheduling window is not a delivery SLA. Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.

<!-- block: b-1909bc7d18975b8da01c -->
```dot
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];

definition [label="AWS · Custom definition\nPrompt, tools, skills, store access"];
trigger [label="AWS · Schedule trigger\nActive or paused"];
run [label="AWS · Invocation\nSeparate execution and trajectory"];
call [label="EXT · Tool operation\nAlready-started external work",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
record [label="AWS · Retained trajectory\nCompleted calls and outputs"];
check [label="DOC · Stop verification\nFuture starts and in-flight effects",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
definition -> run [label="loads configuration"];
trigger -> run [label="eligible future occurrence"];
run -> call [label="invokes"];
run -> record [label="cancel retains completed work"];
call -> check [label="may complete after cancellation",style=dashed];
record -> check [label="inspect actual outcome",style=dashed];
{rank=same;definition;trigger}
{rank=same;call;record}
```
