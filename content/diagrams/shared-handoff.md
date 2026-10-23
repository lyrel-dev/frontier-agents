---
id: shared-handoff
kind: diagram
title: Team-managed evidence handoff
refs:
- A-08
- A-06
---

<!-- block: b-1e3d05605a455dcea84b -->
An operational finding can become input to separate security and cost work. Each receiving service uses its own configuration and authorization; only identifiers, evidence references, and decisions are handed over.

<!-- block: b-521a59e834605142b2a9 -->
```dot
rankdir=TB;
incident [label="Operational investigation\nService, time window, revision"];
handoff [label="Reviewed handoff\nEvidence references and open questions"];
security [label="Security assessment\nIts own application scope and identity"];
finops [label="Cost investigation\nIts own query basis and data role"];
owner [label="Engineering owners\nReview results and authorize changes"];
verification [label="Independent verification\nSource measurements and scoped tests"];
incident -> handoff [label="team review"];
handoff -> security [label="application evidence",style=dashed];
handoff -> finops [label="service and period",style=dashed];
security -> owner [label="finding evidence"];
finops -> owner [label="cost evidence"];
owner -> verification [label="controlled follow-up"];
```
