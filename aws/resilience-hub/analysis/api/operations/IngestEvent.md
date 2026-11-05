---
id: "resilience-workspace-operation-ingest-event"
title: "IngestEvent"
type: "api-operation"
service: "aws-resilience-hub"
status: "implemented-mock"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "api"
  - "rpc-operation"
aliases:
  - "IngestEvent"
related:
  - "../index.md"
  - "../protocol.md"
  - "../aws-mapping.md"
  - "../shapes.md"
  - "../errors.md"
operation: "IngestEvent"
api_version: "2026-11-05"
provenance: "INGEST"
mutating: true
native_operations: []
---



# IngestEvent

Records a source event and refresh intent; untrusted payload content cannot replace service state.

| Property | Value |
| --- | --- |
| Target | `ResilienceWorkspace_20261105.IngestEvent` |
| Transport | `POST /`; `application/x-amz-json-1.1` |
| Operation kind | Mutation against the local mock store |
| Provenance | `INGEST` — Trusted integration ingestion into the product observation/event store. |
| Allowed application roles | `ingestor`, `admin` |
| Native adapter basis | Application-owned; no native mutation or read is asserted. |

Native names above identify the intended adapter basis, not HTTP calls made by this mock. Any local versions, tokens, display metadata, hydration and projections follow the [facade protocol](../protocol.md). See [AWS mapping](../aws-mapping.md) for supported native fields and limitations.

## Request

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `sourceEventId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `channel` | Yes | `string` | `EVENTBRIDGE`, `ENTITY_TIMELINE` |
| `streamOwner` | Yes | `string` | Length 1–256 |
| `source` | Yes | `string` | Length 1–256 |
| `type` | Yes | `string` | Length 1–256 |
| `title` | Yes | `string` | Length 1–256 |
| `message` | Yes | `string` | Length 0–2048 |
| `severity` | No | `string` | `INFO`, `WARNING`, `ERROR` |
| `occurredAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `clientToken` | Yes | `string` | Length 1–63; Pattern `^[A-Za-z0-9_.-]+$` |

### HTTP example

```http
POST / HTTP/1.1
Host: 127.0.0.1:8787
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ResilienceWorkspace_20261105.IngestEvent

{
  "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/71000000-0000-4000-8000-000000000403",
  "sourceEventId": "evt-assessment-104",
  "channel": "EVENTBRIDGE",
  "streamOwner": "111122223333/eu-west-1/default",
  "source": "aws.resiliencehub",
  "type": "Resilience Hub Failure Mode Assessment Completed",
  "title": "Assessment completion notification",
  "message": "A provider notification requests a scoped refresh.",
  "occurredAt": 1793874240,
  "clientToken": "example-ingest-event"
}
```

### Request schema

Schema references resolve through the [shared definitions](../shapes.md).

```json
{
  "type": "object",
  "properties": {
    "serviceArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
    },
    "sourceEventId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "channel": {
      "type": "string",
      "enum": [
        "EVENTBRIDGE",
        "ENTITY_TIMELINE"
      ]
    },
    "streamOwner": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "source": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "type": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "message": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "severity": {
      "type": "string",
      "enum": [
        "INFO",
        "WARNING",
        "ERROR"
      ]
    },
    "occurredAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "clientToken": {
      "type": "string",
      "minLength": 1,
      "maxLength": 63,
      "pattern": "^[A-Za-z0-9_.-]+$"
    }
  },
  "required": [
    "serviceArn",
    "sourceEventId",
    "channel",
    "streamOwner",
    "source",
    "type",
    "title",
    "message",
    "occurredAt",
    "clientToken"
  ],
  "additionalProperties": false
}
```

## Response

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `event` | Yes | [EventEntity](../shapes.md#evententity) | See shared shape or field semantics. |
| `duplicate` | Yes | `boolean` | See shared shape or field semantics. |
| `refreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `refreshOperations` | Yes | Array of `string` | Items 0–1000 |

### Successful response example

HTTP 200. This body is generated by executing the request above against a fresh deterministic mock runtime.

```json
{
  "event": {
    "eventId": "event-2001",
    "sourceEventId": "evt-assessment-104",
    "eventKey": "EVENTBRIDGE|111122223333/eu-west-1/default|evt-assessment-104",
    "channel": "EVENTBRIDGE",
    "streamOwner": "111122223333/eu-west-1/default",
    "source": "aws.resiliencehub",
    "type": "Resilience Hub Failure Mode Assessment Completed",
    "title": "Assessment completion notification",
    "message": "A provider notification requests a scoped refresh.",
    "severity": "INFO",
    "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/71000000-0000-4000-8000-000000000403",
    "entityType": "Service",
    "entityId": "checkout",
    "occurredAt": 1793874240,
    "receivedAt": 1793874240,
    "linkage": "ASSERTED",
    "refreshStatus": "REFRESH_REQUIRED",
    "sequence": 7,
    "mock": true,
    "producerPrincipalId": "demo-operator",
    "trustedSource": false
  },
  "duplicate": false,
  "refreshRequired": true,
  "refreshOperations": [
    "GetService",
    "ListFailureModeAssessments",
    "ListFailureModeFindings",
    "ListDependencies"
  ]
}
```

### Response schema

```json
{
  "type": "object",
  "properties": {
    "event": {
      "$ref": "#/$defs/EventEntity"
    },
    "duplicate": {
      "type": "boolean"
    },
    "refreshRequired": {
      "type": "boolean"
    },
    "refreshOperations": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2048
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    }
  },
  "required": [
    "event",
    "duplicate",
    "refreshRequired",
    "refreshOperations"
  ],
  "additionalProperties": false
}
```

## Consistency and lifecycle

Supply one stable `clientToken` for the logical command. Identical retries return the prior result within the local idempotency window; a changed body with the same token conflicts. Authorization uses trusted server-side context. No request makes a real AWS mutation.

- Appends a source envelope with a trusted-principal stamp.
- Marks a service refresh required without replacing its projection.

## Errors

| Error | HTTP | Meaning |
| --- | --- | --- |
| `ValidationException` | 400 | The target, JSON body, request schema, cursor, or domain input is invalid. |
| `AccessDeniedException` | 403 | The trusted server-side principal lacks a required role or workspace scope. |
| `ResourceNotFoundException` | 404 | No active entity exists in the requested parent scope. |
| `ConflictException` | 409 | An optimistic version, idempotency token, uniqueness rule, or reference guard conflicts. |
| `InternalServerException` | 500 | An unexpected local implementation error occurred. |

Transport errors and client recovery guidance are in [RPC errors](../errors.md). Error availability is a common facade envelope; it does not imply that every listed condition occurs on every execution.

## Documentation source

Generated from [contract.cjs](../contract.cjs) and [runtime.cjs](../runtime.cjs) by [generate_api_docs.cjs](../../scripts/generate_api_docs.cjs). Regenerate after editing the executable contract; use `--check` to detect drift. The mock server and browser prototype use separate local state.
