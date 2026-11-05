---
id: aws-fis-revised-diagrams-initial-04-evidence-reports
title: Evidence, reports and safety observations
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
- Evidence, reports and safety observations
related:
- README.md
- 04_evidence_reports.mmd
- 04_evidence_reports.svg
- ../../docs/initial/report.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/diagrams/04_evidence_reports.mmd
---

# Evidence, reports and safety observations

**Caption:** ExecutionEvidence and StateObservation are retained application records, with optional named-action correlation. Report state is independent from execution. CloudWatchAlarm is an external identity shared by condition references; its observations remain timestamped external evidence. AWS_SCOPE is the owning account/Region scope, not a target-account child.

**Ownership and interpretation:** FIS report objects are experiment projections. Logs, control intent and retained observations preserve their source and observation times. CloudWatch alarm state belongs to the external alarm, while the safety lever belongs to its owning AWS account/Region scope.

[Model and invariants](../../docs/initial/report.md#8-evidence-and-audit-model) · [Editable Mermaid](04_evidence_reports.mmd) · [Standalone SVG](04_evidence_reports.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
erDiagram
    direction TB
    EXPERIMENT_RUN ||--o{ EXECUTION_EVIDENCE : accumulates
    EXPERIMENT_RUN ||--o{ STATE_OBSERVATION : observed_by
    ACTION_EXECUTION o|--o{ EXECUTION_EVIDENCE : optionally_identifies
    ACTION_EXECUTION o|--o{ STATE_OBSERVATION : optionally_identifies
    EXECUTION_EVIDENCE o|--o{ STATE_OBSERVATION : may_support
    EXPERIMENT_RUN ||--o| EXPERIMENT_REPORT : generates
    EXPERIMENT_REPORT ||--o{ REPORT_ARTIFACT : contains
    EXPERIMENT_RUN ||--o{ STOP_CONDITION : configures
    CLOUDWATCH_ALARM o|--o{ STOP_CONDITION : referenced_by
    CLOUDWATCH_ALARM ||--o{ ALARM_OBSERVATION : observed_by
    AWS_SCOPE ||--o{ EXPERIMENT_RUN : owns
    AWS_SCOPE ||--|| SAFETY_LEVER : has
    EXECUTION_EVIDENCE {
        string evidenceKey PK
        string experimentKey FK
        string source
        string sourceRecordId
        datetime occurredAt
        datetime observedAt
        json rawPayload
    }
```

## Portable rendering

![Evidence, reports and safety observations](04_evidence_reports.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
