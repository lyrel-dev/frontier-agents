---
id: aws-fis-revised-diagrams-suggested-02-owned-values
title: Owned workflow values and references
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
- Owned workflow values and references
related:
- README.md
- 02_owned_values.mmd
- 02_owned_values.svg
- ../../docs/suggested/model.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/workflow/diagrams/02_owned_values.mmd
---

# Owned workflow values and references

**Caption:** Step definitions, immutable operation locks, admission snapshots, check results and external operation references are owned values. The diagram shares entity boundaries with the all-entity view and does not introduce extra aggregate roots.

**Ownership and interpretation:** Definitions and locks belong to the published revision. Admission freezes the run meaning, bindings and criterion denominator. Check results and provider handles belong to attempts. Their scoped references and cited evidence must resolve within the owning revision or run.

[Model and invariants](../../docs/suggested/model.md#owned-values-and-external-references) · [Editable Mermaid](02_owned_values.mmd) · [Standalone SVG](02_owned_values.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
classDiagram
direction TB
class ScenarioRevision
class StepDefinition {
  +stepKey : Key
  +phase : MainOrFinalizer
  +uses : OperationAlias
  +checkRole : CheckRole
}
class OperationLock {
  +implementationDigest : Digest
  +inputSchemaDigest : Digest
  +outputSchemaDigest : Digest
}
class Run
class AdmissionSnapshot {
  +revisionDigest : Digest
  +requiredCriteria : KeySet
  +bindingsObservedAt : Instant
}
class StepAttempt
class CheckResult {
  +verdict : Verdict
  +evidenceIds : IdSet
  +evaluatedThrough : Instant
}
class ExternalOperationRef {
  +provider : Namespace
  +nativeId : String
  +observedAt : Instant
}
class Evidence
ScenarioRevision "1" *-- "1..*" StepDefinition : defines
ScenarioRevision "1" *-- "1..*" OperationLock : pins
StepDefinition "0..*" --> "1" OperationLock : invokes
StepDefinition "0..*" --> "0..*" StepDefinition : needs
Run "1" *-- "1" AdmissionSnapshot : binds
StepAttempt "1" *-- "0..1" CheckResult : evaluates
StepAttempt "1" *-- "0..*" ExternalOperationRef : tracks
CheckResult "0..*" --> "0..*" Evidence : cites
```

## Portable rendering

![Owned workflow values and references](02_owned_values.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
