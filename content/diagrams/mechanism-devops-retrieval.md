---
id: mechanism-devops-retrieval
kind: diagram
title: 'Incident memory: production, availability and retrieval'
refs:
- D-M01
- D-M02
- D-M07
---

<!-- block: b-28118e00d4175b729a77 -->
Producing context does not prove a later execution selected it. Activation and applicable attachments control availability; current evidence controls interpretation. Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.

<!-- block: b-947699f1568c5edcbcc4 -->
```dot
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];

history [label="AWS · Prior investigations\nRecorded evidence and conclusions"];
feedback [label="AWS · Investigation feedback\nOperator-supplied correction"];
store [label="AWS · Retained entry\nDescription, content and version"];
available [label="AWS · Available context\nActive state; applicable attachment"];
select [label="AWS · Select and read\nStore then entry descriptions"];
current [label="EXT · Current observations\nNew incident time window",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
review [label="DOC · Memory verification\nEntry identity, observed access, current evidence",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
history -> store [label="managed synthesis"];
feedback -> store [label="corrective context"];
{rank=same;history;feedback}
store -> available [label="activation and scope"];
available -> select [label="relevant description"];
select -> review [label="selected history",style=dashed];
current -> review [label="supports or contradicts",style=dashed];
{rank=same;select;current}
```
