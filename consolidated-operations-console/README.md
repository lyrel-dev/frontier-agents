# Consolidated Operations Console

**Phase 1 · contract revision 2 · uniformly versioned entities and Draw.io diagrams.**

This package consolidates the work under `aws/<service-name>/analysis/**` on `main`, pinned to `d926a81c584b6b69f41bfb9641532c4f8f2d7cb3` on 5 November 2026. The source inventory contains **226 active files**. The application model contains **36 entities**: 11 in the foundation and 25 in the workload, Health, resilience, investigation, workflow and FIS modules.

Every entity carries **`version`, `createdAt` and `updatedAt`**. Identity stays stable across versions; history is another representation of the same entity. A Source, Projection or Scenario has versions without a separate revision class. Exact historical references identify the entity and its version. This revision applies the user's correction to the first consolidation, published at [`db142c8`](https://github.com/lyrel-dev/frontier-agents/commit/db142c84bcfd691d5c71071681731cac81a52c7b).

The deliverable is a data model and **108 typed AWS RPC style operation contracts: 74 reads and 34 mutations**, with offline checks. Collectors, persistence, authorization enforcement, command dispatch, workflow execution and the console UI are subsequent implementation phases.

## Start here

| Question | Document |
| --- | --- |
| What previous work exists on main? | [Complete inventory](INVENTORY.md) · [File manifest](inventory.json) |
| What is the application and this phase's scope? | [Context and scope](CONTEXT_AND_SCOPE.md) |
| Which design rules govern this revision? | [Design principles and their provenance](DESIGN_PRINCIPLES.md) |
| How are all entities versioned? | [Model and invariants](MODEL.md) · [Every entity, field and value](model/REFERENCE.md) |
| Where does each earlier concept go? | [Consolidation map](MAPPING.md) · [Adapter/profile registry](model/adapter-profiles.json) |
| Where are the editable diagrams? | [Draw.io model atlas](diagrams/model.drawio) · [All-entity overview](diagrams/complete-model.svg) |
| How do the API operations work? | [RPC protocol](api/PROTOCOL.md) · [Operation catalog](api/OPERATIONS.md) |
| What are the machine-readable contracts? | [Model schema](model/schema.json) · [RPC schemas](api/rpc.schema.json) · [Operation metadata](api/operations.json) |
| What do connected examples look like? | [Model examples](model/examples.json) · [RPC examples](api/examples.json) |
| How does implementation proceed? | [Consolidation path and acceptance gates](CONSOLIDATION_PLAN.md) |
| What changed and what was verified? | [Review findings and corrections](REVIEW.md) · [Validation evidence](VALIDATION.md) |

## Model at a glance

| Module | Entities | Responsibility |
| --- | ---: | --- |
| Foundation | 11 | Workspace/access, resource identity, collection, source evidence, observation, derivation, capture, operator work and command intent |
| Workload | 4 | System, UserJourney, Service and Dependency |
| Health | 6 | Event/context/impact, communication, lifecycle catalogue and component deployment |
| Resilience | 4 | Policy, assessment, finding and recommendation |
| Investigation | 6 | AgentSpace, Investigation, Execution, JournalRecord, ApprovalRequest and Asset |
| Workflow | 4 | Scenario, Run, StepRun and StepAttempt |
| FIS | 1 | Experiment, with owned actions, selected targets and report values |

Source evidence, observing that evidence and deriving a conclusion remain different concepts. They now use the same entity-version mechanism. Provider state, collection coverage, technical execution, acceptance, cleanup and local operator disposition retain their own meanings.

## Draw.io diagrams

Open [model.drawio](diagrams/model.drawio) in Draw.io to edit the eight-page atlas. The overview shows all 36 entities. Focused pages show foundation identity/commands, evidence/history, workload, Health, resilience, investigation, and workflow/FIS relationships with readable spacing and explicit boundary references. SVG exports are available in [diagrams/](diagrams/).

The all-entity overview intentionally shows a selected relationship set; the detailed pages cover the model's relationships. The class fields are selected for reading. [The generated reference](model/REFERENCE.md) is the complete field contract.

## API style

```http
POST / HTTP/1.1
Host: console.example.invalid
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ConsolidatedOperationsConsole_20261105V2.GetService

{"serviceId":"svc-checkout","version":1}
```

A typed getter can select an exact `version`; omitting it selects the current authorized representation. Responses contain the entity's actual version. Writes use the owning entity's `expectedVersion` and an idempotency `clientToken`. Trusted ingestion and lifecycle transitions publish entity versions under their owning authority. A native provider version remains separate metadata and does not substitute for the application version.

The authenticated context supplies Workspace and actor scope. Provider commands use explicit contracts and durable receipts. [The protocol](api/PROTOCOL.md) defines historical reads, reference resolution, pagination, concurrency, replay, errors and the compatibility break from revision 1.

## Regeneration and validation

`model/schema.json` is the authoritative logical contract. The reference, diagram atlas and API artifacts are kept consistent with it. [VALIDATION.md](VALIDATION.md) records the exact reproduction commands, renderer versions, executed checks and evidence limits.

The revision preserves the original service analyses and frozen source inventory. Changes are confined to `consolidated-operations-console/`.
