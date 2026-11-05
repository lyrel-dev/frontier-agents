---
id: aws-fis-revised-diagrams-initial-01-execution
title: Run identity and action dependencies
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
- Run identity and action dependencies
related:
- README.md
- 01_execution.mmd
- 01_execution.svg
- ../../docs/initial/report.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/diagrams/01_execution.mmd
---

# Run identity and action dependencies

**Caption:** One run contains one or more logical action executions. A dependency identifies two steps in the same run. The source template can be missing from retained/current catalogue data after deletion; the source ID is still retained.

**Ownership and interpretation:** ExperimentRun and ActionExecution are native execution projections. ActionExecution identity is scoped to the experiment and action map key. ActionDependency is an application normalization of the named predecessor relation; both ends must belong to the same run.

[Model and invariants](../../docs/initial/report.md#2-core-execution-model) · [Editable Mermaid](01_execution.mmd) · [Standalone SVG](01_execution.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
erDiagram
    direction TB
    EXPERIMENT_TEMPLATE o|--o{ EXPERIMENT_RUN : source
    EXPERIMENT_RUN ||--|{ ACTION_EXECUTION : contains
    CATALOG_ACTION ||--o{ ACTION_EXECUTION : identifies
    ACTION_EXECUTION ||--o{ ACTION_DEPENDENCY : predecessor
    ACTION_EXECUTION ||--o{ ACTION_DEPENDENCY : successor
    EXPERIMENT_RUN {
        string experimentKey PK
        string arn
        string sourceTemplateId
        string status
        datetime creationTime
        datetime startTime
        datetime endTime
        json configSnapshot
    }
    ACTION_EXECUTION {
        string experimentKey PK, FK
        string actionName PK
        string actionId FK
        string status
        string reason
        datetime startTime
        datetime endTime
        json parameters
    }
    ACTION_DEPENDENCY {
        string experimentKey PK, FK
        string predecessorActionName PK, FK
        string successorActionName PK, FK
    }
```

## Portable rendering

![Run identity and action dependencies](01_execution.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
