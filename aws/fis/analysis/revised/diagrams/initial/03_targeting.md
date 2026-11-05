---
id: aws-fis-revised-diagrams-initial-03-targeting
title: Selected target scope
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
- Selected target scope
related:
- README.md
- 03_targeting.mmd
- 03_targeting.svg
- ../../docs/initial/report.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/diagrams/03_targeting.mmd
---

# Selected target scope

**Caption:** Selectors describe intended selection; memberships describe resources resolved for the run. ResourceIdentity is optional application normalization. A selector can feed several actions, and a resource can appear in several selectors. Action effects are a separate evidence layer.

**Ownership and interpretation:** Target selections and account configurations belong to one experiment. Membership is scoped to the run, selector and account. An observed membership is not proof that a fault was applied or recovery occurred; unidentified membership is retained without inventing resource identity.

[Model and invariants](../../docs/initial/report.md#5-target-selectors-resolved-memberships-and-accounts) · [Editable Mermaid](03_targeting.mmd) · [Standalone SVG](03_targeting.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
erDiagram
    direction TB
    EXPERIMENT_RUN ||--o{ TARGET_SELECTION : defines
    EXPERIMENT_RUN ||--o{ EXPERIMENT_TARGET_ACCOUNT : configures
    ACTION_EXECUTION ||--o{ ACTION_TARGET_BINDING : binds
    TARGET_SELECTION ||--o{ ACTION_TARGET_BINDING : referenced_by
    TARGET_SELECTION ||--o{ RESOLVED_TARGET_MEMBERSHIP : resolves_to
    RESOURCE_IDENTITY o|--o{ RESOLVED_TARGET_MEMBERSHIP : identifies
    TARGET_SELECTION ||--o{ TARGET_RESOLUTION_OBSERVATION : observed_by
    ACTION_TARGET_BINDING {
        string experimentKey PK, FK
        string actionName PK, FK
        string slotName PK
        string targetName FK
    }
    TARGET_SELECTION {
        string experimentKey PK, FK
        string targetName PK
        string resourceType
        string selectionMode
        json selectorSnapshot
    }
    RESOLVED_TARGET_MEMBERSHIP {
        string membershipKey PK
        string experimentKey FK
        string targetName FK
        json targetInformation
        string optionalResourceKey FK
    }
```

## Portable rendering

![Selected target scope](03_targeting.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
