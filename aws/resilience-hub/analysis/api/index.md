---
id: "resilience-workspace-api-index"
title: "Resilience Workspace API reference"
type: "api-reference"
service: "aws-resilience-hub"
status: "implemented-mock"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "api"
  - "rpc"
aliases:
  - "Resilience Workspace API reference"
related:
  - "protocol.md"
  - "aws-mapping.md"
  - "entities.md"
  - "shapes.md"
  - "errors.md"
  - "workflows.md"
  - "../report.md"
  - "../quality-review.md"
  - "../validation.md"
---



# Resilience Workspace API reference

An executable mock API for the reviewed AWS Resilience Hub operator model. **44 operations** cover the ten requested entities, input sources, status projections and event ingestion. Every operation has an Obsidian Markdown note with YAML properties, request and response schemas, generated examples, access roles, errors and lifecycle effects.

> This is a product-owned RPC facade. The mock makes no AWS calls. Its AWS-shaped transport is a design choice; native Resilience Hub v2 has its own HTTP routes and SDK contract. The existing browser UI and this HTTP server currently maintain separate local mock states.

## Start here

| Note | Contents |
| --- | --- |
| [Protocol](protocol.md) | Transport, identities, authorization, idempotency, versions, pagination and freshness. |
| [AWS mapping](aws-mapping.md) | Operation-by-operation native evidence, adapter boundaries and reviewed field corrections. |
| [Entity mapping](entities.md) | How the ten requested concepts and ER relationships map to RPC operations. |
| [Shared schemas](shapes.md) | Canonical reusable DTO definitions generated from the executable contract. |
| [Errors](errors.md) | Typed errors, status codes and client recovery behavior. |
| [Workflows](workflows.md) | UI tasks, command lifecycle, event reconciliation and sequence diagrams. |
| [Reviewed model](../report.md) | Source-backed analysis and the five ER diagram notes. |
| [Adversarial review](../quality-review.md) | Reproduced semantic failures, corrective changes and remaining delivery gaps. |
| [Validation](../validation.md) | Checks completed and explicit integration boundaries. |

## Run locally

From `aws/resilience-hub/analysis` with Node.js 18 or later:

```bash
node api/server.cjs
# Optional: node api/server.cjs --port 8788 --role reader
```

The default endpoint is `http://127.0.0.1:8787/`. The server binds to loopback, stores mutations only in memory, and uses a trusted demo principal configured at startup. Restarting resets its state. The default `demo` context includes all four application roles; read-only mode uses `--role reader`. No AWS credentials are required.

```bash
curl --silent --show-error http://127.0.0.1:8787/ \
  -H 'Content-Type: application/x-amz-json-1.1' \
  -H 'X-Amz-Target: ResilienceWorkspace_20261105.ListSystems' \
  --data '{"maxResults":20}'
```

Successful responses use HTTP 200 and operation-specific JSON. See [protocol](protocol.md) for the full envelope and [errors](errors.md) for non-2xx responses. Timestamps on the wire are numeric epoch seconds with at most millisecond precision; sub-millisecond inputs are rejected before ordering or storage. The fixture clock starts at 2026-11-05T10:24:00Z and advances with elapsed process time; generated examples and tests inject a fixed clock.

The included [Node client](client.cjs) handles the RPC headers and exposes the server request ID. With the server running:

```bash
node api/client.cjs ListSystems '{"maxResults":20}'
node api/client.cjs GetWorkspaceSummary '{}'
```

## Operation catalogue

The provenance column refers to the facade implementation. Native-backed operations still add local guarantees; composed operations do not invent new AWS endpoints. Integration operations require an ingestor or administrator context. The [mapping note](aws-mapping.md) explains each classification.

### Systems

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [CreateSystem](operations/CreateSystem.md) | Mutation | `NATIVE_ADAPTER` | Creates a system with a provider-compatible name and local version. |
| [GetSystem](operations/GetSystem.md) | Read | `NATIVE_ADAPTER` | Reads one active system. |
| [ListSystems](operations/ListSystems.md) | Read | `NATIVE_ADAPTER` | Lists active systems from a stable local pagination snapshot. |
| [UpdateSystem](operations/UpdateSystem.md) | Mutation | `NATIVE_ADAPTER` | Updates the description or sharing configuration; names are immutable. |
| [DeleteSystem](operations/DeleteSystem.md) | Mutation | `NATIVE_ADAPTER` | Tombstones an empty system and retains history. |

### User journeys

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [CreateUserJourney](operations/CreateUserJourney.md) | Mutation | `NATIVE_ADAPTER` | Creates a user journey scoped to one system. |
| [GetUserJourney](operations/GetUserJourney.md) | Read | `NATIVE_ADAPTER` | Reads a journey and its projected service memberships. |
| [ListUserJourneys](operations/ListUserJourneys.md) | Read | `NATIVE_ADAPTER` | Lists the journeys of one system. |
| [UpdateUserJourney](operations/UpdateUserJourney.md) | Mutation | `NATIVE_ADAPTER` | Changes a journey name, description, or policy; membership changes use UpdateService. |
| [DeleteUserJourney](operations/DeleteUserJourney.md) | Mutation | `NATIVE_ADAPTER` | Tombstones an unassigned journey; services must be detached first. |

### Services

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [CreateService](operations/CreateService.md) | Mutation | `NATIVE_ADAPTER` | Creates a service with validated same-system journey memberships. |
| [GetService](operations/GetService.md) | Read | `NATIVE_ADAPTER` | Reads native-like service fields plus explicitly local display, version, and freshness metadata. |
| [ListServices](operations/ListServices.md) | Read | `NATIVE_ADAPTER` | Lists distinct services, optionally scoped by system and user journey. |
| [UpdateService](operations/UpdateService.md) | Mutation | `NATIVE_ADAPTER` | Updates service configuration; effective-policy observations are marked for refresh without rewriting historical posture. |
| [DeleteService](operations/DeleteService.md) | Mutation | `NATIVE_ADAPTER` | Tombstones a service only when it has no active assessment; observations and captures remain retained. |

### Policies

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [CreatePolicy](operations/CreatePolicy.md) | Mutation | `NATIVE_ADAPTER` | Creates a policy with top-level native availability and recovery components. |
| [GetPolicy](operations/GetPolicy.md) | Read | `NATIVE_ADAPTER` | Reads one resilience policy. |
| [ListPolicies](operations/ListPolicies.md) | Read | `NATIVE_ADAPTER` | Lists the policies visible in the fixed mock workspace. |
| [UpdatePolicy](operations/UpdatePolicy.md) | Mutation | `NATIVE_ADAPTER` | Updates objectives and marks affected service policy contexts for a future refresh. |
| [DeletePolicy](operations/DeletePolicy.md) | Mutation | `NATIVE_ADAPTER` | Tombstones a policy only when no active service or journey is assigned to it. |

### Input sources

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [CreateInputSource](operations/CreateInputSource.md) | Mutation | `NATIVE_ADAPTER` | Registers exactly one supported resource configuration and requests a later discovery refresh. |
| [ListInputSources](operations/ListInputSources.md) | Read | `NATIVE_ADAPTER` | Lists registered sources, preserving missing historical source configuration as null. |
| [DeleteInputSource](operations/DeleteInputSource.md) | Mutation | `NATIVE_ADAPTER` | Tombstones a registered input source without erasing its observations. |

### Assessments

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [StartFailureModeAssessment](operations/StartFailureModeAssessment.md) | Mutation | `NATIVE_ADAPTER` | Queues one mock assessment; health and the last successful posture remain independent. |
| [GetFailureModeAssessment](operations/GetFailureModeAssessment.md) | Read | `COMPOSED_READ` | Reads one retained assessment from the local observation store. |
| [ListFailureModeAssessments](operations/ListFailureModeAssessments.md) | Read | `NATIVE_ADAPTER` | Lists retained assessment runs for a service. |

### Findings

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [GetFailureModeFinding](operations/GetFailureModeFinding.md) | Read | `NATIVE_ADAPTER` | Reads the current detailed finding observation and disposition. |
| [ListFailureModeFindings](operations/ListFailureModeFindings.md) | Read | `NATIVE_ADAPTER` | Lists detailed local finding projections; their capture provenance is retained. |
| [UpdateFailureModeFinding](operations/UpdateFailureModeFinding.md) | Mutation | `NATIVE_ADAPTER` | Changes disposition and comment; resolving a finding does not prove a healthy or compliant service. |

### Recommendations

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [GetRecommendation](operations/GetRecommendation.md) | Read | `COMPOSED_READ` | Reads one immutable recommendation observation and its separately versioned local enrichment. |
| [ListRecommendations](operations/ListRecommendations.md) | Read | `COMPOSED_READ` | Lists retained recommendation instances, optionally from one finding observation. |
| [UpdateRecommendationEnrichment](operations/UpdateRecommendationEnrichment.md) | Mutation | `LOCAL` | Updates local title, explanation, or estimate without mutating provider recommendation evidence. |

### Dependencies

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [GetDependency](operations/GetDependency.md) | Read | `COMPOSED_READ` | Reads a dependency observation, plus its separately managed local governance classification. |
| [ListDependencies](operations/ListDependencies.md) | Read | `NATIVE_ADAPTER` | Lists discovered dependencies scoped to a service. |
| [UpdateDependency](operations/UpdateDependency.md) | Mutation | `NATIVE_ADAPTER` | Updates native-like criticality and comment; allowed status remains local governance. |
| [UpdateDependencyGovernance](operations/UpdateDependencyGovernance.md) | Mutation | `LOCAL` | Updates local allowed status with an independent governance version. |

### Topology

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [CaptureTopologySnapshot](operations/CaptureTopologySnapshot.md) | Mutation | `LOCAL` | Copies the latest stored representative fixture graph into an immutable local capture, retaining original observation time and scope. |
| [GetTopologySnapshot](operations/GetTopologySnapshot.md) | Read | `COMPOSED_READ` | Reads a retained topology capture in its service scope. |
| [ListTopologySnapshots](operations/ListTopologySnapshots.md) | Read | `COMPOSED_READ` | Lists stored local captures, not provider topology entities. |

### Operator projections

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [GetServiceStatus](operations/GetServiceStatus.md) | Read | `COMPOSED_READ` | Projects independent runtime health, assessment lifecycle, assessed posture, and discovery status with freshness. |
| [GetWorkspaceSummary](operations/GetWorkspaceSummary.md) | Read | `COMPOSED_READ` | Aggregates distinct services in a validated business scope; it does not claim end-to-end journey compliance. |

### Events

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [ListEvents](operations/ListEvents.md) | Read | `COMPOSED_READ` | Lists retained event envelopes and typed subjects across distinct source channels with stable pagination. |

### Ingestion

| Operation | Mode | Provenance | Purpose |
| --- | --- | --- | --- |
| [PutHealthObservation](operations/PutHealthObservation.md) | Mutation | `INGEST` | Ingests a source-keyed health observation; late observations stay historical and expiry makes current health unknown. |
| [IngestEvent](operations/IngestEvent.md) | Mutation | `INGEST` | Retains the raw event, typed subjects and correlation IDs as evidence and requests a refresh; no event body patches authoritative state. |

## Maintain the contract and notes

Edit [contract.cjs](contract.cjs) and the runtime together, then regenerate the operation notes and shared schemas. Generated notes carry stable IDs and relative links suitable for an Obsidian vault. The hand-authored protocol, mapping, entity and workflow notes explain intent and native boundaries.

```bash
node scripts/generate_api_docs.cjs
node scripts/generate_api_docs.cjs --check
node --test tests/*.test.cjs
python scripts/check_notes.py
```

The generator executes every documented example against a fresh runtime. Setup commands in delete examples create disposable entities. Request and response JSON schemas resolve `#/$defs/<Shape>` through the definitions in [shapes.md](shapes.md) or `contract.shapes`. [contract.cjs](contract.cjs), [runtime.cjs](runtime.cjs) and [server.cjs](server.cjs) are source code; all human-readable documents and diagrams are Markdown notes with YAML headers.
