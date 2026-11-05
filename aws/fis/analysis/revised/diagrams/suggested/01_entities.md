---
id: aws-fis-revised-diagrams-suggested-01-entities
title: All assessment workflow entities
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
- All assessment workflow entities
related:
- README.md
- 01_entities.mmd
- 01_entities.svg
- ../../docs/suggested/model.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/workflow/diagrams/01_entities.mmd
---

# All assessment workflow entities

**Caption:** All six identity-bearing concepts are included: Scenario, ScenarioRevision, Run, StepRun, StepAttempt and Evidence. Scenario and Run are aggregate roots; StepRun and StepAttempt are owned execution children. The model does not imply six independently writable CRUD APIs.

**Ownership and interpretation:** Scenario owns published ScenarioRevisions. A Run executes one revision and owns its StepRuns and attempts. Evidence is immutable and retained for one Run, with an optional producer attempt and explicit consumption references. The workspace is supplied by authenticated server context.

[Model and invariants](../../docs/suggested/model.md#1-entities-ownership-and-identity) · [Editable Mermaid](01_entities.mmd) · [Standalone SVG](01_entities.svg) · [Diagram index](README.md)

## Mermaid

```mermaid
classDiagram
direction TB
class Scenario {
  +scenarioId : Id
  +version : Integer
  +defaultRevisionId : Id
}
class ScenarioRevision {
  +scenarioRevisionId : Id
  +scenarioId : Id
  +digest : Digest
  +publishedAt : Instant
}
class Run {
  +runId : Id
  +scenarioRevisionId : Id
  +projectionVersion : Integer
  +phase : RunPhase
  +outcome : RunOutcome
}
class StepRun {
  +runId : Id
  +stepKey : Key
  +selectedAttemptNo : Integer
  +skipReason : Code
}
class StepAttempt {
  +attemptNo : Integer
  +dispatchKey : Id
  +outcome : AttemptOutcome
  +remoteDisposition : Disposition
}
class Evidence {
  +evidenceId : Id
  +runId : Id
  +schemaRef : Digest
  +observedAt : Instant
  +contentDigest : Digest
}
Scenario "1" *-- "0..*" ScenarioRevision : publishes
ScenarioRevision "1" <-- "0..*" Run : executes
Run "1" *-- "1..*" StepRun : owns
StepRun "1" *-- "0..*" StepAttempt : records
Run "1" o-- "0..*" Evidence : retains
Evidence "0..*" --> "0..1" StepAttempt : produced by
Evidence "0..*" <-- "0..*" StepAttempt : consumes
```

## Portable rendering

![All assessment workflow entities](01_entities.svg)

The Mermaid block above is identical to the canonical `.mmd` source. The SVG is provided for viewers that do not render Mermaid and carries an accessible title and description. Read the linked model for identity scope, logical cardinalities, conditional relationships and missing-data rules.
