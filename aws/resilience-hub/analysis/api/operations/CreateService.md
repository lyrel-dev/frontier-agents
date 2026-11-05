---
id: "resilience-workspace-operation-create-service"
title: "CreateService"
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
  - "CreateService"
related:
  - "../index.md"
  - "../protocol.md"
  - "../aws-mapping.md"
  - "../shapes.md"
  - "../errors.md"
operation: "CreateService"
api_version: "2026-11-05"
provenance: "NATIVE_ADAPTER"
mutating: true
native_operations:
  - "CreateService"
---



# CreateService

Creates a service with validated same-system journey memberships.

| Property | Value |
| --- | --- |
| Target | `ResilienceWorkspace_20261105.CreateService` |
| Transport | `POST /`; `application/x-amz-json-1.1` |
| Operation kind | Mutation against the local mock store |
| Provenance | `NATIVE_ADAPTER` — Native-backed facade with local validation, versions, idempotency and response normalization. |
| Allowed application roles | `operator`, `admin` |
| Native adapter basis | [CreateService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html) |

Native names above identify the intended adapter basis, not HTTP calls made by this mock. Any local versions, tokens, display metadata, hydration and projections follow the [facade protocol](../protocol.md). See [AWS mapping](../aws-mapping.md) for supported native fields and limitations.

## Request

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `description` | No | `string` | Length 0–615 |
| `associatedSystems` | No | Array of [AssociatedSystem](../shapes.md#associatedsystem) | Items 0–20 |
| `policyArn` | No | `string` or `null` | See full schema |
| `regions` | Yes | Array of `string` | Items 1–5 |
| `permissionModel` | Yes | [PermissionModel](../shapes.md#permissionmodel) | See shared shape or field semantics. |
| `dependencyDiscovery` | No | `string` | `ENABLED`, `DISABLED` |
| `reportConfiguration` | No | [ReportConfiguration](../shapes.md#reportconfiguration) or `null` | See full schema |
| `devOpsAgentConfiguration` | No | [DevOpsAgentConfiguration](../shapes.md#devopsagentconfiguration) or `null` | See full schema |
| `kmsKeyId` | No | `string` | Length 1–2048 |
| `tags` | No | Map of `string` | Properties 0–50 |
| `clientToken` | Yes | `string` | Length 1–63; Pattern `^[A-Za-z0-9_.-]+$` |

### HTTP example

```http
POST / HTTP/1.1
Host: 127.0.0.1:8787
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ResilienceWorkspace_20261105.CreateService

{
  "name": "sandbox-service",
  "description": "Isolated API demonstration",
  "permissionModel": {
    "invokerRoleName": "NorthstarResilienceHubInvoker",
    "crossAccountRoles": [
      {
        "crossAccountRoleArn": "arn:aws:iam::111122223333:role/NorthstarResilienceReadOnly"
      }
    ]
  },
  "regions": [
    "eu-west-1"
  ],
  "clientToken": "example-create-service"
}
```

### Request schema

Schema references resolve through the [shared definitions](../shapes.md).

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 60,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$"
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 615
    },
    "associatedSystems": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/AssociatedSystem"
      },
      "minItems": 0,
      "maxItems": 20,
      "uniqueItems": false
    },
    "policyArn": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 20,
          "maxLength": 2048,
          "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
        },
        {
          "type": "null"
        }
      ]
    },
    "regions": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 64,
        "pattern": "^[a-z]{2}(-gov)?-[a-z]+-[0-9]+$"
      },
      "minItems": 1,
      "maxItems": 5,
      "uniqueItems": false
    },
    "permissionModel": {
      "$ref": "#/$defs/PermissionModel"
    },
    "dependencyDiscovery": {
      "type": "string",
      "enum": [
        "ENABLED",
        "DISABLED"
      ]
    },
    "reportConfiguration": {
      "anyOf": [
        {
          "$ref": "#/$defs/ReportConfiguration"
        },
        {
          "type": "null"
        }
      ]
    },
    "devOpsAgentConfiguration": {
      "anyOf": [
        {
          "$ref": "#/$defs/DevOpsAgentConfiguration"
        },
        {
          "type": "null"
        }
      ]
    },
    "kmsKeyId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "tags": {
      "type": "object",
      "propertyNames": {
        "type": "string",
        "minLength": 1,
        "maxLength": 128
      },
      "additionalProperties": {
        "type": "string",
        "minLength": 0,
        "maxLength": 256
      },
      "maxProperties": 50
    },
    "clientToken": {
      "type": "string",
      "minLength": 1,
      "maxLength": 63,
      "pattern": "^[A-Za-z0-9_.-]+$"
    }
  },
  "required": [
    "name",
    "permissionModel",
    "regions",
    "clientToken"
  ],
  "additionalProperties": false
}
```

## Response

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `service` | Yes | [ServiceEntity](../shapes.md#serviceentity) | See shared shape or field semantics. |

### Successful response example

HTTP 200. This body is generated by executing the request above against a fresh deterministic mock runtime.

```json
{
  "service": {
    "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/73000000-0000-4000-8000-000000003001",
    "name": "sandbox-service",
    "displayName": "sandbox-service",
    "description": "Isolated API demonstration",
    "createdAt": 1793874240,
    "updatedAt": 1793874240,
    "observedAt": 1793874240,
    "associatedSystems": [],
    "policyArn": null,
    "regions": [
      "eu-west-1"
    ],
    "permissionModel": {
      "invokerRoleName": "NorthstarResilienceHubInvoker",
      "crossAccountRoles": [
        {
          "crossAccountRoleArn": "arn:aws:iam::111122223333:role/NorthstarResilienceReadOnly"
        }
      ]
    },
    "dependencyDiscovery": {
      "status": "DISABLED",
      "eligibleResourceCount": null,
      "message": "No discovery evidence captured yet.",
      "updatedAt": 1793874240,
      "requestedStatus": "DISABLED"
    },
    "resourceDiscovery": {
      "status": "NOT_STARTED",
      "lastRunAt": null,
      "errorCode": null,
      "errorMessage": null
    },
    "achievability": {},
    "assessmentStatus": "NOT_STARTED",
    "inputSourceIds": [],
    "resourceCount": null,
    "reportConfiguration": null,
    "devOpsAgentConfiguration": null,
    "tags": {},
    "kmsKeyId": null,
    "version": 1,
    "refreshRequired": true,
    "provenance": "MOCK_NATIVE_SERVICE_WITH_LOCAL_METADATA"
  }
}
```

### Response schema

```json
{
  "type": "object",
  "properties": {
    "service": {
      "$ref": "#/$defs/ServiceEntity"
    }
  },
  "required": [
    "service"
  ],
  "additionalProperties": false
}
```

## Consistency and lifecycle

Supply one stable `clientToken` for the logical command. Identical retries return the prior result within the local idempotency window; a changed body with the same token conflicts. Authorization uses trusted server-side context. No request makes a real AWS mutation.

- Commits an atomic local mock-state transaction.
- Records a local audit event; never calls AWS.

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
