---
id: mechanism-finops-context
kind: diagram
title: 'FinOps context: three independent lifecycle operations'
refs:
- F-M02
- F-M03
- F-M04
---

<!-- block: b-17829473f3da5b409537 -->
File restoration, memory updates and conversation compaction operate on different representations. Their controls do not remove copies held in other representations. Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.

<!-- block: b-a471cbd45351547980c3 -->
```dot
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];

file [label="AWS · Active uploaded file\nOperator-maintained reference"];
deleted [label="AWS · Soft-deleted file\nNot active context"];
memory [label="AWS · Retained memory\nPreference or correction"];
updated [label="AWS · Updated memory\nRemember, update or forget"];
conversation [label="AWS · Conversation context\nOlder and recent messages"];
summary [label="AWS · Compacted context\nOlder summary + recent full messages"];
check [label="DOC · Context verification\nCheck file state, retained preference and query constraints",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
file -> deleted [label="delete"];
deleted -> file [label="restore"];
memory -> updated [label="conversational request"];
conversation -> summary [label="context approaches limit"];
file -> check [style=dashed];
updated -> check [style=dashed];
summary -> check [style=dashed];
{rank=same;file;memory;conversation}
{rank=same;deleted;updated;summary}
```
