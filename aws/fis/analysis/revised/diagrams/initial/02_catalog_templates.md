---
id: aws-fis-revised-diagrams-initial-02-catalog-templates
title: Definitions, catalogue and templates
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
- Definitions, catalogue and templates
related:
- README.md
- 02_catalog_templates.mmd
- 02_catalog_templates.svg
- ../../docs/initial/report.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/diagrams/02_catalog_templates.mmd
---

# Definitions, catalogue and templates

**Caption:** A template contains named steps, selectors and eligible account configurations. Target-slot bindings and predecessor edges are normalized relations. Catalogue metadata describes supported inputs and resource types; an unavailable metadata lookup should not prevent display of a recorded run.

**Ownership and interpretation:** TemplateAction and TemplateTarget are template-owned named members. Catalogue action and resource-type metadata describe capabilities, not executions. A target slot and an action map key are different identifiers.

[Model and invariants](../../docs/initial/report.md#3-definitions-catalog-metadata-and-templates) · [Editable Mermaid](02_catalog_templates.mmd) · [Standalone SVG](02_catalog_templates.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
erDiagram
    direction TB
    EXPERIMENT_TEMPLATE ||--|{ TEMPLATE_ACTION : contains
    EXPERIMENT_TEMPLATE ||--o{ TEMPLATE_TARGET : defines
    CATALOG_ACTION ||--o{ TEMPLATE_ACTION : configures
    CATALOG_ACTION ||--o{ ACTION_PARAMETER_DEFINITION : describes
    CATALOG_ACTION ||--o{ ACTION_TARGET_SLOT : supports
    RESOURCE_TYPE ||--o{ ACTION_TARGET_SLOT : accepted_by
    RESOURCE_TYPE ||--o{ TEMPLATE_TARGET : selects
    TEMPLATE_ACTION ||--o{ TEMPLATE_BINDING : binds
    TEMPLATE_TARGET ||--o{ TEMPLATE_BINDING : referenced_by
    TEMPLATE_ACTION ||--o{ TEMPLATE_DEPENDENCY : predecessor
    TEMPLATE_ACTION ||--o{ TEMPLATE_DEPENDENCY : successor
    EXPERIMENT_TEMPLATE ||--o{ TEMPLATE_TARGET_ACCOUNT : configures
```

## Portable rendering

![Definitions, catalogue and templates](02_catalog_templates.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
