---
id: assessment-workflow-design
title: Assessment workflow design
status: reviewed-proposal
version: "0.2"
updated: "2026-11-05"
---

# Assessment workflow design

This is the reviewed successor to the generalized model proposed in the conversation. It describes an application-owned assessment workflow, with AWS FIS as one possible execution adapter. It does not change the native FIS model in [the API analysis](../report.md).

**Implementation status:** design proposal with executable contract checks, synthetic examples and rendered diagrams. The FIS Observatory application remains a provider-focused mock. There is no generalized workflow scheduler, API server, CEL evaluator, AWS adapter or live assessment engine in this package.

| Document | Purpose |
| --- | --- |
| [Model](model.md) | Six identity-bearing concepts, ownership, complete class diagram, state and verdict rules, cancellation, finalization and evidence semantics. |
| [API](api.md) | Explicit commands, writable DTOs, one proposed HTTP binding, concurrency, idempotency, pagination and errors. |
| [Adapter contracts](adapters.md) | FIS, Logs Insights, alarm observations, CloudTrail and notification receipt; exactly what each can establish. |
| [Scenario schema](scenario.schema.json) | Structural schema for the authoring document. Semantic validation is a separate stage. |
| [Operation catalogue](operation-catalog.json) | Synthetic adapter contracts, current aliases and retained digest-addressed revisions. Implementation digests identify unimplemented example labels, not executable code. These operation names are proposed product names. |
| [Examples](examples/) | Alarm notification verification and a Logs Insights error budget, including explicit bindings and criterion inputs. |
| [Contract checks](contract.py) | A small reference validator and verdict reducer for the documented decisions. It does not execute scenarios. |
| [Tests](tests/test_contract.py) | Counterexamples for cycles, reference scope, floating dependencies, skipped criteria, partial evidence and cancellation semantics. |
| [Diagrams](diagrams/) | Editable Mermaid class and lifecycle diagrams with accessible SVG renderings. |

The reviewed design keeps the authoring surface small: named steps, `uses`, typed `with`, `needs`, conditions, bounded execution policies and a finalization graph. Queries and assertions use the same operation contract as commands. Provider-specific payloads remain typed evidence; they do not become universal core entities.

## Validate the proposal

With Python 3.10 or later, `jsonschema` and `PyYAML` installed:

```bash
python3 aws/fis/analysis/workflow/contract.py
python3 -m unittest discover -s aws/fis/analysis/workflow/tests -v
```

The first command checks both complete examples, their operation locks, declared input references, dependency scope, finalizer ordering, and embedded diagram parity. Each `.lock.json` pins its companion YAML's program and the retained synthetic contracts. The tests exercise selected semantic counterexamples, including alias rotation without changing old published locks. Neither command compiles CEL, resolves real deployment bindings, proves IAM permissions, verifies a notification receiver or runs an HTTP server. The exact validation scope is recorded in [the package validation record](../VALIDATION.md).

## Design boundaries

Repository guidance requires explicit entity kinds, scoped identities, qualified cardinalities, and separation of configuration, execution, evidence and acceptance. Those are concrete recorded principles in [EDITORIAL_STANDARD.md](../../../../EDITORIAL_STANDARD.md). The neighboring [Resilience Workspace API](../../../resilience-hub/analysis/api/protocol.md) also makes writable fields, local versions, idempotency, pagination and provenance explicit. Its RPC transport is a neighboring design choice, not evidence of a universal user preference.

This proposal adds no independent Job, Stage, Query, Alarm, Assertion, Report, Approval, Trigger or Scheduler aggregate. A reusable scenario invocation, schedule service, independent reassessment history or operator remediation workflow can be designed later when its identity and lifecycle justify it. Required runtime behavior is specified here; optional product features are not disguised as already implemented capabilities.
