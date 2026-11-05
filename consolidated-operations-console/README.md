# Consolidated Operations Console

**Phase 1: a modular consolidated data model and AWS RPC style API contracts.**

This package consolidates the work under `aws/<service-name>/analysis/**` on `main`, pinned to `d926a81c584b6b69f41bfb9641532c4f8f2d7cb3` on 5 November 2026. It introduces a common model for scope, evidence, collection, projections, snapshots, local work and commands, with typed workload, Health, resilience, investigation, workflow and FIS modules.

The source inventory contains **226 active files**. The proposed model contains **37 entities**: 11 in the shared foundation and 26 in the domain modules, exposed through **101 typed RPC operations**. It is a model/contract package with offline validation; a live application, scheduler, persistence layer and AWS adapters belong to later phases.

## Start here

| Question | Document |
| --- | --- |
| What previous work exists on main? | [Complete inventory](INVENTORY.md) · [Machine-readable file manifest](inventory.json) |
| What application are we defining, and what is in this first step? | [Context and scope](CONTEXT_AND_SCOPE.md) |
| Which earlier design conventions are retained? | [Design principles and repository evidence](DESIGN_PRINCIPLES.md) |
| What is the consolidated model? | [Model decisions and invariants](MODEL.md) · [Every entity/field/value](model/REFERENCE.md) |
| Where does every source-model concept go? | [Source-to-target crosswalk](MAPPING.md) · [Typed adapter/profile registry](model/adapter-profiles.json) |
| What does the full class diagram look like? | [All 37 entities, SVG](diagrams/complete-model.svg) · [Editable Mermaid](diagrams/complete-model.mmd) |
| How do the API operations work? | [Wire and command protocol](api/PROTOCOL.md) · [Operation catalog](api/OPERATIONS.md) |
| What are the machine-readable contracts? | [Data model](model/schema.json) · [RPC inputs/outputs](api/rpc.schema.json) · [Operation metadata](api/operations.json) |
| Can I inspect a connected example? | [Worked model records](model/examples.json) · [Per-operation requests/responses](api/examples.json) |
| How do we consolidate incrementally? | [Consolidation path and acceptance gates](CONSOLIDATION_PLAN.md) |
| What was reviewed and checked? | [Review](REVIEW.md) · [Validation evidence and limits](VALIDATION.md) |

## Model at a glance

| Module | Entity count | Responsibility |
| --- | ---: | --- |
| Foundation | 11 | Workspace/access scope, resource identity, reads, immutable evidence/interpretation, capture, work and command intent |
| Workload | 4 | System, UserJourney, Service and service-scoped Dependency |
| Health | 6 | Event/context/impact, communication assembly, lifecycle catalog and observed component deployment |
| Resilience | 4 | Policy, native assessment, service finding and observation-scoped recommendation |
| Investigation | 6 | AgentSpace, Task-based investigation, execution, journal, approval and versioned assets |
| Workflow | 5 | Scenario/draft, immutable revision, admitted run, step lifecycle and attempt facts |
| FIS | 1 | Native experiment with owned action/target/report detail |

The repeated evidence infrastructure is consolidated. Provider state, execution outcome, acceptance verdict, cleanup, current coverage and local operator disposition retain their independent meaning. A source payload revision is different from seeing that payload again; a projection is different from either. These boundaries are the basis for a trustworthy common console.

## API style

```http
POST / HTTP/1.1
Host: console.example
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ConsolidatedOperationsConsole_20261105.GetService

{"serviceId":"svc-checkout"}
```

Operation names use PascalCase and JSON fields use lowerCamelCase. The authenticated session supplies Workspace and acting-principal scope; request bodies cannot choose them. Lists use bounded `maxResults`/`nextToken`. Mutations use `clientToken`; edits use the version of the local owner, and provider changes use explicit durable command contracts. The namespace and operations belong to this application. Native AWS calls keep their own documented transports behind adapters.

## Regenerate and validate

From this directory:

```sh
python tools/render_model.py
python api/generate.py
python tools/validate.py
python tools/render_model.py --check
python api/generate.py --check
```

`model/schema.json` is the authoritative model. The renderer derives `model/REFERENCE.md` and seven complete/focused class-diagram sources and SVGs from it. It uses Graphviz for SVG output; the accompanying Mermaid is editable, and no identical rendering across engines is claimed. `api/generate.py` authors the operation registry and schemas from its explicit definitions plus the model, and derives documented/examples output. The validator checks offline contracts and selected semantic risks; it is not a service runtime.

See [VALIDATION.md](VALIDATION.md) for dependencies, actual check results, reproducibility and the remaining production gates. Existing source packages and root documentation are left as their original work products.
