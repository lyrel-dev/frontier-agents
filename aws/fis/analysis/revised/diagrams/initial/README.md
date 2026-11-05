---
id: aws-fis-revised-diagrams-initial-readme
title: Initial FIS entity relationship diagrams
type: diagram-index
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
- diagram-index
aliases:
- Initial FIS entity relationship diagrams
related:
- ../README.md
- ../../docs/initial/report.md
- 01_execution.md
- 02_catalog_templates.md
- 03_targeting.md
- 04_evidence_reports.md
- 05_assessments.md
---

# Initial FIS entity relationship diagrams

These five views describe the native FIS contract and explicitly identified application extensions. The reviewed source and SVG bytes are preserved from report edition 1.2. Each Obsidian note includes ownership, a caption, the canonical Mermaid and a portable SVG.

| View | Source | Rendering |
| --- | --- | --- |
| [Run identity and action dependencies](01_execution.md) | [Mermaid](01_execution.mmd) | [SVG](01_execution.svg) |
| [Definitions, catalogue and templates](02_catalog_templates.md) | [Mermaid](02_catalog_templates.mmd) | [SVG](02_catalog_templates.svg) |
| [Selected target scope](03_targeting.md) | [Mermaid](03_targeting.mmd) | [SVG](03_targeting.svg) |
| [Evidence, reports and safety observations](04_evidence_reports.md) | [Mermaid](04_evidence_reports.mmd) | [SVG](04_evidence_reports.svg) |
| [Criteria and workload evidence](05_assessments.md) | [Mermaid](05_assessments.mmd) | [SVG](05_assessments.svg) |

Read the [complete model](../../docs/initial/report.md) for fields, qualified cardinalities and invariants. Return to [all diagrams](../README.md) or the [reading guide](../../docs/README.md).

The initial diagrams are preserved alongside the suggested diagrams so that the native provider model remains visible. The generalized model does not rename FIS action children into independently controllable workflow resources.
