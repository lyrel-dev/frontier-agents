---
id: mechanism-security-replay
kind: diagram
title: 'Finding revalidation: evidence and result boundaries'
refs:
- S-M05
- S-05
---

<!-- block: b-885b2fbbfb5c5cbdb670 -->
Revalidation creates a separate job for selected existing findings. Non-reproduction must be interpreted under the identity and path actually reached; it is not broad new discovery. Green/AWS: documented service concept. Blue/DOC: our verification procedure. Orange/EXT: engineering-owned source. Stages are logical explanations, not API status enum values.

<!-- block: b-d2873ad8a2645b399fd1 -->
```dot
rankdir=TB;
node [shape=box,style="rounded,filled",fillcolor="#D9F2E5",color="#348761",fontcolor="#164D35"];
edge [color="#526474",fontcolor="#344454"];

finding [label="AWS · Original finding\nValidation steps and history"];
repair [label="EXT · Deployed repair\nApproved target revision",fillcolor="#FCE8D5",color="#C78335",fontcolor="#6D431A"];
auth [label="AWS · Current test credentials\nAuthenticated role and route"];
job [label="AWS · Revalidation job\nRepeat selected validation steps"];
active [label="AWS · Active\nIssue reproduced"];
resolved [label="AWS · Resolved\nIssue not reproduced in this replay"];
accept [label="DOC · Acceptance check\nVerify target, role and completed path",fillcolor="#DCEBFF",color="#447AC2",fontcolor="#183B69"];
finding -> job [label="selected finding"];
repair -> job [label="current deployment"];
auth -> job [label="current identity"];
job -> active;
job -> resolved;
active -> accept [style=dashed];
resolved -> accept [label="not sufficient alone",style=dashed];
{rank=same;finding;repair;auth}
{rank=same;active;resolved}
```
