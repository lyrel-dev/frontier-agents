---
id: aws-fis-revised-diagrams-initial-05-assessments
title: Criteria and workload evidence
type: diagram
service: aws-fis
status: reviewed
version: '1.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- diagram
aliases:
- Criteria and workload evidence
related:
- README.md
- 05_assessments.mmd
- 05_assessments.svg
- ../../docs/initial/report.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/diagrams/05_assessments.mmd
---

# Criteria and workload evidence

**Caption:** These are proposed application evaluation entities. A run can bind several telemetry queries and assessments. Every assessment retains its criterion revision, immutable input snapshot, evidence window and observation cutoff; changing a policy or query later does not silently rewrite a historical verdict.

**Ownership and interpretation:** These assessment concepts are application-owned extensions, not native AWS FIS result fields. Criteria define acceptance, observations provide evidence and an assessment pins the exact interpretation used for its historical verdict.

[Model and invariants](../../docs/initial/report.md#9-workload-assessment-model) · [Editable Mermaid](05_assessments.mmd) · [Standalone SVG](05_assessments.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
erDiagram
    direction TB
    EXPERIMENT_RUN ||--o{ EXPERIMENT_METRIC_BINDING : binds
    METRIC_BINDING ||--o{ EXPERIMENT_METRIC_BINDING : used_by
    METRIC_BINDING ||--o{ METRIC_OBSERVATION : supplies
    EXPERIMENT_RUN ||--o{ RESILIENCE_ASSESSMENT : assessed_by
    ASSESSMENT_CRITERION ||--o{ RESILIENCE_ASSESSMENT : evaluates
    RESILIENCE_ASSESSMENT ||--o{ ASSESSMENT_EVIDENCE : cites
    METRIC_OBSERVATION ||--o{ ASSESSMENT_EVIDENCE : supports
    RESILIENCE_ASSESSMENT {
        string assessmentKey PK
        string experimentKey FK
        string criterionRevision FK
        string verdict
        string missingDataPolicy
        datetime evaluatedAt
        json evidenceWindow
        datetime evidenceCutoffAt
        json inputSnapshot
    }
```

## Portable rendering

![Criteria and workload evidence](05_assessments.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
