---
id: aws-fis-revised-diagrams-suggested-03-lifecycle
title: Local run lifecycle
type: diagram
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
- diagram
aliases:
- Local run lifecycle
related:
- README.md
- 03_lifecycle.mmd
- 03_lifecycle.svg
- ../../docs/suggested/model.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/workflow/diagrams/03_lifecycle.mmd
---

# Local run lifecycle

**Caption:** The lifecycle describes local orchestration phases. Execution outcome, assessment verdict/finality and remote-effect/finalization disposition remain separate; a terminal local phase does not prove remote work has ceased.

**Ownership and interpretation:** The Run owns orchestration phase and monotonic cancellation intent. Sealed attempt facts are not rewritten by later reconciliation; new evidence can update the projection of the originating remote effect. Finalizers inspect original step intents even when no provider handle was returned.

[Model and invariants](../../docs/suggested/model.md#4-execution-and-assessment-are-separate-facts) · [Editable Mermaid](03_lifecycle.mmd) · [Standalone SVG](03_lifecycle.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
stateDiagram-v2
[*] --> Queued
Queued --> Running : admitted and eligible
Queued --> Finalizing : cancel or admission expiry
Running --> Finalizing : settled, cancel, or deadline
Finalizing --> Finished : cleanup settled or deadline
Finished --> [*]
note right of Finalizing
Remote disposition is tracked separately.
An accepted stop is not proof of cleanup.
end note
```

## Portable rendering

![Local run lifecycle](03_lifecycle.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
