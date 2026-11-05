---
id: aws-fis-revised-diagrams-suggested-readme
title: Suggested workflow class and lifecycle diagrams
type: diagram-index
service: aws-fis
status: reviewed-proposal
version: '0.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- diagram-index
aliases:
- Suggested workflow class and lifecycle diagrams
related:
- ../README.md
- ../../docs/suggested/model.md
- 01_entities.md
- 02_owned_values.md
- 03_lifecycle.md
---

# Suggested workflow class and lifecycle diagrams

The complete entity view contains all six core entities. The owned-value view explains subordinate contracts without introducing more aggregates; the lifecycle view separates local orchestration from assessment and remote effects. Each Obsidian note includes ownership, a caption, the canonical Mermaid and a portable SVG.

| View | Source | Rendering |
| --- | --- | --- |
| [All assessment workflow entities](01_entities.md) | [Mermaid](01_entities.mmd) | [SVG](01_entities.svg) |
| [Owned workflow values and references](02_owned_values.md) | [Mermaid](02_owned_values.mmd) | [SVG](02_owned_values.svg) |
| [Local run lifecycle](03_lifecycle.md) | [Mermaid](03_lifecycle.mmd) | [SVG](03_lifecycle.svg) |

Read the [complete model](../../docs/suggested/model.md) for fields, qualified cardinalities and invariants. Return to [all diagrams](../README.md) or the [reading guide](../../docs/README.md).

The initial diagrams are preserved alongside the suggested diagrams so that the native provider model remains visible. The generalized model does not rename FIS action children into independently controllable workflow resources.
