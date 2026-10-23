---
id: devops-knowledge
kind: diagram
title: Environment-knowledge consolidation
refs:
- D-M08
- D-05
---

<!-- block: b-09322c8a4c325cfda877 -->
Discovery, connected evidence, and completed investigations feed distinct retained knowledge. A later execution selects the relevant context; it still reads current source evidence.

<!-- block: b-8d74484407675059bfe8 -->
```dot
rankdir=TB;
sources [label="Environment evidence\nResources, repositories, pipelines, telemetry"];
history [label="Completed investigations\nObserved tool use and outcomes"];
learning [label="Managed learning\nSynthesis and refresh"];
map [label="Environment understanding\nServices, components, request paths"];
deps [label="Dependencies and pipelines\nRelationships and delivery stages"];
tools [label="Tool-use guidance\nQuery patterns and recurring errors"];
selection [label="Later execution\nSelect relevant stored context"];
sources -> learning [label="environment inputs"];
history -> learning [label="operational experience"];
learning -> map;
learning -> deps;
learning -> tools;
map -> selection [label="relevant descriptions"];
deps -> selection;
tools -> selection;
```
