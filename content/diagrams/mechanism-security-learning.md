---
id: mechanism-security-learning
kind: diagram
title: 'Security reuse: login navigation and finding preferences'
refs:
- S-M02
- S-05
---

<!-- block: b-5a21852300ea56e2a99b -->
The two retained processes have different producers and effects. Disabling reuse or personalization preserves learned material; neither operation repairs the application. Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.

<!-- block: b-65bd88b00689500a81d5 -->
```dot
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];

login [label="AWS · Successful login\nCurrent credential and navigation"];
procedure [label="AWS · Login procedure\nLogin Optimization setting"];
nextlogin [label="AWS · Later login\nAuthenticated application session"];
edit [label="AWS · Eligible finding edits\nMost recent completed test run"];
preference [label="AWS · Finding preferences\nPersonalization enabled at test start"];
nextfinding [label="AWS · Later similar finding\nOriginal and personalized attributes"];
review [label="DOC · Engineering verification\nConfirm session identity and finding changes",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
login -> procedure [label="learns navigation"];
procedure -> nextlogin [label="reuse when enabled"];
edit -> preference [label="learns eligible changes"];
preference -> nextfinding [label="apply to similar finding"];
nextlogin -> review [style=dashed];
nextfinding -> review [style=dashed];
{rank=same;login;edit}
{rank=same;procedure;preference}
{rank=same;nextlogin;nextfinding}
```
