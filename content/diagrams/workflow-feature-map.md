---
id: workflow-feature-map
kind: diagram
title: Outcome, workflow, mechanism, and feature relationships
refs:
- A-09
---

<!-- block: b-3e43550e0ea457a78822 -->
An authored documentation model: each workflow step declares a dependency on a documented mechanism and concrete feature configuration. Reverse links support impact review. This is not an AWS runtime design.

<!-- block: b-d50c720e4539501fb5ea -->
```dot
rankdir=TB;
outcome [label="Operational objective\nActor and completion criteria"];
variant [label="Variant\nScope, trigger, network, format"];
step [label="Workflow step\nPurpose and responsible actor"];
mechanism [label="Documented mechanism\nTrigger, state, process, effect"];
feature [label="Platform feature\nResources and supported operations"];
recipe [label="Implementation profile\nValues, permissions, checks, failure handling"];
evidence [label="Verification evidence\nObservable result and limitations"];
outcome -> step [label="is carried out through"];
variant -> step [label="conditions a dependency"];
step -> mechanism [label="requires / optionally uses"];
mechanism -> feature [label="implemented with"];
recipe -> feature [label="configures"];
recipe -> step [label="binds to environment"];
step -> evidence [label="accepted using"];
```
