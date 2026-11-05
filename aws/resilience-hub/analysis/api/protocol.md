---
id: "resilience-workspace-rpc-protocol"
title: "Resilience Workspace RPC protocol"
type: "api-design"
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
  - "Resilience Workspace wire contract"
related:
  - "index.md"
  - "aws-mapping.md"
  - "shapes.md"
  - "errors.md"
  - "workflows.md"
---

# Resilience Workspace RPC protocol

This is the application-owned API for the proposed operator workspace. It presents the reviewed model through a consistent RPC interface, backed in this repository by a deterministic, in-memory mock. Operation notes and schemas describe the interface that is implemented here. A production AWS adapter is a separate integration step.

## Transport and identity

| Item | Contract |
| --- | --- |
| Method and path | `POST /` |
| Request and response media type | `application/x-amz-json-1.1` |
| Operation selector | `X-Amz-Target: ResilienceWorkspace_20261105.<Operation>` |
| API version | `2026-11-05` |
| Operation names | PascalCase, for example `GetService` |
| JSON members | lowerCamelCase, for example `serviceArn` |
| Timestamps | Finite numbers containing seconds since the Unix epoch; fractional seconds are allowed |
| Successful response | HTTP `200` and the operation-specific JSON response |
| Failed response | Non-2xx HTTP status, a typed JSON error, `x-amzn-ErrorType` and `x-amzn-RequestId` |
| Correlation | A fresh server request ID for each HTTP attempt; idempotency tokens identify a logical mutation |
| Maximum request body | 1 MiB in the mock server |

The root POST, target selector, media type and numeric timestamps follow the conventions described in the [Smithy AWS JSON 1.1 specification](https://smithy.io/2.0/aws/protocols/aws-json-1_1-protocol.html). The selected namespace, operation set and DTOs belong to this product. This repository does not supply a generated Smithy SDK, a SigV4 implementation, protocol compliance certification or an AWS endpoint.

The native Resilience Hub v2 API has its own HTTP contract. For example, AWS documents `CreateService` as `POST /v2/create-service` with `application/json`, and `GetService` as `GET /v2/get-service?serviceArn=...`. A production adapter must use those native operations or the official SDK. See [CreateService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html), [GetService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetService.html) and the [AWS mapping](aws-mapping.md).

```http
POST / HTTP/1.1
Host: 127.0.0.1:8787
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ResilienceWorkspace_20261105.ListSystems

{"maxResults":20}
```

All operation notes contain executable request examples and responses generated from the same runtime and fixtures as the server. The [catalogue](index.md) links to those notes and their exact input and output schemas. A request with no parameters uses `{}`. The server rejects unsupported methods, paths, media types, malformed JSON and unknown targets with the [documented errors](errors.md).

## Operation provenance

| Kind | Meaning | Example |
| --- | --- | --- |
| `NATIVE_ADAPTER` | A corresponding AWS operation exists; the facade validates, scopes, maps and may hydrate its response. Its extra local fields and guarantees still belong to the facade. | `CreateService`, `UpdateFailureModeFinding` |
| `COMPOSED_READ` | The product assembles a read view from native list/detail observations and its own store. | `GetFailureModeAssessment`, `GetWorkspaceSummary` |
| `LOCAL` | The product manages its own captures, recommendation enrichment or governance decisions. | `CaptureTopologySnapshot`, `UpdateRecommendationEnrichment` |
| `INGEST` | A trusted integration supplies health observations or event envelopes to the product. | `PutHealthObservation`, `IngestEvent` |

Reusing a native operation name does not mean the request and response are byte-for-byte native payloads. The per-operation provenance and [mapping](aws-mapping.md) identify the boundary. In particular, RPC `List*` responses use the facade's documented shape; AWS often returns a narrower summary representation.

## Identities, references and field presence

Provider ARNs and scoped provider IDs are the primary external keys. A user journey is addressed by `(systemArn, userJourneyId)`. Assessments, findings, input sources and dependencies are addressed within their service scope. A topology edge can reference only nodes in its own capture. Friendly names, browser fixture IDs and list ordinals are never substitutes for these identities.

`displayName`, local entity `version`, recommendation identity, cost estimates, governance decisions, captures, health observations and derived attention are product data. They must not be forwarded unmodified to AWS. Provider names for systems, services and policies are constrained identifiers; a separate local display name preserves human-friendly labels. User journey names have their own native constraints and may contain spaces. The [entity mapping](entities.md) distinguishes native fields from local additions.

Inputs accept only the writable properties defined by the schema. A read-only response object is not a valid update request. Omitted update members preserve existing values. Supplied arrays replace the corresponding local array after reference validation; this is a facade rule. Null is accepted only where explicitly allowed by the shape. An absent optional property, explicit null, a known empty collection and a known zero remain different values. No generic `fieldsToClear` command or arbitrary object patch is supported.

Names, timestamps, enums and resource configuration unions are validated before mutation. `CreateInputSource.resourceConfiguration` has exactly one configuration member, matching the native tagged-union model. A discovery request sets `ENABLED` or `DISABLED`; `INITIALIZING` is provider-managed output. Permission models use `crossAccountRoleArn` within `crossAccountRoles`. See [CreateInputSource](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/create_input_source.html) and [CreateService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html).

## Mutation lifecycle

Every mutation is explicit about its scope and writable fields. Local versions let the client detect a concurrent edit before replacing the product's current record. An update or guarded delete supplies the current `expectedVersion`; a mismatch returns a conflict and leaves the state unchanged. The client should fetch again, show the intervening changes and obtain a new user decision before retrying a different write.

The version is an application revision, not an AWS revision or ETag. A successful local comparison cannot prevent an administrator from changing AWS directly. A production adapter needs reconciliation and a durable command record around the remote call; it must not claim transactional compare-and-swap across AWS and the product database.

The mock conservatively rejects deletion when referenced entities or active work would be orphaned. It retains local historical observations and a deletion record rather than rewriting historical captures. These guards are product decisions, not assertions of undocumented AWS cascade behavior. The corresponding delete note states the guards applied to each entity.

Starting an assessment acknowledges a run and returns its identity and initial status. It does not promise completion, an achievable policy, zero findings or healthy runtime behavior. The last observed posture remains visible while a newer assessment is pending or has failed. The mock does not automatically complete the run or contact AWS.

## Idempotency and retries

Mutations use a required `clientToken` in this facade. The runtime scopes replay to the trusted principal, operation and token, and compares the canonical request payload. An identical replay returns the previously recorded response without repeating side effects. Reuse of a token with a different payload returns `ConflictException`. Replay is checked before applying an optimistic version comparison, so a successful write can be retried using the original version and token.

The mock retains idempotency results for 24 hours of its runtime clock. The store is in memory and is lost when the server restarts. This limit is a local design choice; AWS documentation for the mapped operations does not establish an equivalent general token retention guarantee. A production implementation must persist successful results and in-flight reservations and resolve uncertain remote outcomes before declaring a retry safe.

For network failures, retry the exact same mutation with the same token. A changed user intent needs a new token. Do not automatically retry validation, authorization or version conflicts as if they were transport failures. Operation error notes distinguish retryable service failures from a request that must change. No mock response establishes that a real AWS write occurred.

## Pagination and consistency

List operations accept `maxResults` from 1 through 100, defaulting to 20, and an opaque `nextToken`. The first request freezes a local result set for that traversal. Tokens are signed, expire after 15 minutes of the runtime clock, and are bound to the operation, principal, filters and snapshot. The next request must preserve its scope and filters. Invalid, expired, tampered or cross-scope tokens fail rather than silently starting a different traversal.

An absent `nextToken` ends a traversal. A new first-page request starts a new local snapshot and may see intervening writes. Snapshot consistency here concerns the product's collected in-memory records; it is not an atomic multi-operation snapshot of AWS resources. AWS list pagination must be exhausted separately, with collection and detail-hydration coverage recorded. Native summary omissions must not erase already hydrated fields. See [ListServices](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListServices.html) and [ListFailureModeAssessments](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeAssessments.html).

## Authorization boundary

The operation catalogue assigns allowed application roles: `reader`, `operator`, `admin` and `ingestor`. The runtime receives its trusted principal through server-side context. The JSON body does not choose a tenant, role or identity, and browser headers do not grant privileges. A role is an application permission, not an AWS IAM action. The eventual adapter must separately obtain the appropriate AWS credentials and enforce allowed account/resource scopes.

The runnable demo binds to loopback and uses an explicitly configured mock principal. It does not implement authentication, SigV4 verification, multi-tenant identity federation or a durable audit store. Application authorization tests exercise the runtime context; they do not establish production authentication. Keep the mock as a local development process.

## Event processing and freshness

`IngestEvent` records an event envelope and produces a refresh intent. It does not apply an event body as an authoritative patch to a service or complete an AWS refresh. Dedupe uses channel, stream owner and source event ID so identifiers from different delivery surfaces do not collide. Event occurrence time, ingestion time and entity observation time remain separate.

`PutHealthObservation` accepts a monitoring observation with its own source, measured time and expiry. Older evidence is retained without replacing a newer current health projection. Expired evidence becomes unknown according to the local rule, while its last raw state remains inspectable. A health signal does not rewrite resilience achievability.

`CaptureTopologySnapshot` freezes a copy of the available mock graph. It records the local capture time while retaining the source observation time and partial coverage. Capturing an old graph cannot turn it into fresh provider evidence. A production collector must reconcile `ListResources` and `ListServiceTopologyEdges` and document missing or unresolved endpoints.

The [event workflow](workflows.md) describes the production refresh sequence. AWS documents native EventBridge notifications as best effort, so periodic reconciliation is needed even when a stream appears quiet. See [EventBridge notifications](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-notifications.html). The demo's event store, health projection and aggregate rule are application-owned.

## Versioning and implementation scope

The namespace makes the initial API revision explicit. Adding optional response properties can be compatible for tolerant clients. Renaming a field, changing identity scope, redefining status meaning or making a formerly optional request member mandatory requires a new contract revision. Input validation is intentionally strict, so new writable members also need a coordinated client/server release.

The machine-readable [contract](contract.cjs), [runtime](runtime.cjs) and [HTTP server](server.cjs) are executable source code. Their corresponding Markdown notes are generated by [generate_api_docs.cjs](../scripts/generate_api_docs.cjs). Run the generator's check mode after contract changes to detect documentation drift. The [validation record](../validation.md) distinguishes executable mock tests from the production integration work that remains.
