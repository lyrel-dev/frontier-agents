---
id: "resilience-workspace-operation-update-service"
title: "UpdateService"
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
  - "UpdateService"
related:
  - "../index.md"
  - "../protocol.md"
  - "../aws-mapping.md"
  - "../shapes.md"
  - "../errors.md"
operation: "UpdateService"
api_version: "2026-11-05"
provenance: "NATIVE_ADAPTER"
mutating: true
native_operations:
  - "UpdateService"
---



# UpdateService

Updates service configuration; effective-policy observations are marked for refresh without rewriting historical posture.

| Property | Value |
| --- | --- |
| Target | `ResilienceWorkspace_20261105.UpdateService` |
| Transport | `POST /`; `application/x-amz-json-1.1` |
| Operation kind | Mutation against the local mock store |
| Provenance | `NATIVE_ADAPTER` — Native-backed facade with local validation, versions, idempotency and response normalization. |
| Allowed application roles | `operator`, `admin` |
| Native adapter basis | [UpdateService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UpdateService.html) |

Native names above identify the intended adapter basis, not HTTP calls made by this mock. Any local versions, tokens, display metadata, hydration and projections follow the [facade protocol](../protocol.md). See [AWS mapping](../aws-mapping.md) for supported native fields and limitations.

## Request

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `description` | No | `string` | Length 0–615 |
| `associatedSystems` | No | Array of [AssociatedSystem](../shapes.md#associatedsystem) | Items 0–20 |
| `policyArn` | No | `string` or `null` | See full schema |
| `regions` | No | Array of `string` | Items 1–5 |
| `permissionModel` | No | [PermissionModel](../shapes.md#permissionmodel) | See shared shape or field semantics. |
| `dependencyDiscovery` | No | `string` | `ENABLED`, `DISABLED` |
| `reportConfiguration` | No | [ReportConfiguration](../shapes.md#reportconfiguration) or `null` | See full schema |
| `devOpsAgentConfiguration` | No | [DevOpsAgentConfiguration](../shapes.md#devopsagentconfiguration) or `null` | See full schema |
| `expectedVersion` | Yes | `integer` | Minimum 1 |
| `clientToken` | Yes | `string` | Length 1–63; Pattern `^[A-Za-z0-9_.-]+$` |

### HTTP example

```http
POST / HTTP/1.1
Host: 127.0.0.1:8787
Content-Type: application/x-amz-json-1.1
X-Amz-Target: ResilienceWorkspace_20261105.UpdateService

{
  "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/71000000-0000-4000-8000-000000000403",
  "dependencyDiscovery": "DISABLED",
  "expectedVersion": 1,
  "clientToken": "example-update-service"
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
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
          "minLength": 31,
          "maxLength": 2048,
          "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
        "minLength": 6,
        "maxLength": 64,
        "pattern": "^[a-z]{2}-((iso[a-z]?|gov)-)?[a-z]+-[0-9]$"
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
    "expectedVersion": {
      "type": "integer",
      "minimum": 1
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
    "expectedVersion",
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
    "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/71000000-0000-4000-8000-000000000403",
    "name": "checkout",
    "displayName": "Checkout orchestration",
    "description": "Basket validation, checkout workflow and idempotent order submission.",
    "createdAt": 1786523400,
    "updatedAt": 1793873940,
    "localUpdatedAt": 1793874240,
    "observedAt": 1793874120,
    "associatedSystems": [
      {
        "systemArn": "arn:aws:resiliencehub:eu-west-1:111122223333:system/71000000-0000-4000-8000-000000000101",
        "userJourneyIds": [
          "71000000-0000-4000-8000-000000000302"
        ]
      }
    ],
    "policyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
    "regions": [
      "eu-west-1"
    ],
    "permissionModel": {
      "invokerRoleName": "NorthstarResilienceHubInvoker",
      "crossAccountRoles": []
    },
    "dependencyDiscovery": {
      "status": "DISABLED",
      "rawStatus": "DISABLED",
      "eligibleResourceCount": 16,
      "message": "Discovery disabled; historical dependencies are retained.",
      "updatedAt": 1793874240,
      "requestedStatus": "DISABLED",
      "normalizationDiagnostics": []
    },
    "resourceDiscovery": {
      "status": "SUCCEEDED",
      "rawStatus": "SUCCEEDED",
      "lastRunAt": 1793873160,
      "errorCode": null,
      "errorMessage": null,
      "normalizationDiagnostics": []
    },
    "achievability": {
      "availabilitySlo": "NOT_ACHIEVABLE",
      "multiAzRtoRpo": "NOT_ACHIEVABLE",
      "multiRegionRtoRpo": "ACHIEVABLE",
      "dataRecoveryTimeBetweenBackups": "ACHIEVABLE"
    },
    "assessmentStatus": "SUCCESS",
    "rawAssessmentStatus": "SUCCESS",
    "inputSourceIds": [
      "71000000-0000-4000-8000-000000000502",
      "71000000-0000-4000-8000-000000000552"
    ],
    "resourceCount": 34,
    "reportConfiguration": null,
    "devOpsAgentConfiguration": null,
    "tags": {
      "Environment": "production",
      "Team": "Commerce SRE",
      "Application": "checkout"
    },
    "kmsKeyId": null,
    "version": 2,
    "projectionVersion": 2,
    "refreshRequired": true,
    "policyContextRefreshRequired": false,
    "reassessmentRequired": true,
    "rerunAssessment": null,
    "effectivePolicyEvidence": {
      "effectiveTargetObservation": {
        "effectiveTargetObservationId": "targets-checkout-initial",
        "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/71000000-0000-4000-8000-000000000403",
        "observedAt": 1793869560,
        "targets": [
          {
            "metric": "availabilitySlo",
            "label": "Availability SLO",
            "value": 99.95,
            "unit": "%",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "dataRecoveryTimeBetweenBackups",
            "label": "Backup interval",
            "value": 60,
            "unit": "min",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "multiAzRto",
            "label": "Multi-AZ RTO",
            "value": 5,
            "unit": "min",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "multiAzRpo",
            "label": "Multi-AZ RPO",
            "value": 0,
            "unit": "min",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "multiAzDrApproach",
            "label": "Multi-AZ approach",
            "value": "ACTIVE_ACTIVE",
            "unit": "",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "multiRegionRto",
            "label": "Multi-Region RTO",
            "value": 60,
            "unit": "min",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "multiRegionRpo",
            "label": "Multi-Region RPO",
            "value": 15,
            "unit": "min",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          },
          {
            "metric": "multiRegionDrApproach",
            "label": "Multi-Region approach",
            "value": "WARM_STANDBY",
            "unit": "",
            "policyName": "Tier 1 · Critical commerce",
            "ownership": "SELF",
            "rawOwnership": "SELF",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "resolvedPolicyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "resolutionEvidence": "Verified mock policy membership and unique policy identity",
            "provenance": "MOCK_GET_SERVICE_EFFECTIVE_VALUES"
          }
        ],
        "evaluatedProviderRevision": null,
        "provenance": "LOCAL_CAPTURE_OF_EFFECTIVE_TARGETS"
      },
      "policyContextCapture": {
        "policyContextCaptureId": "policy-context-checkout-initial",
        "serviceArn": "arn:aws:resiliencehub:eu-west-1:111122223333:service/71000000-0000-4000-8000-000000000403",
        "observedAt": 1793869560,
        "associations": [
          {
            "systemArn": "arn:aws:resiliencehub:eu-west-1:111122223333:system/71000000-0000-4000-8000-000000000101",
            "userJourneyIds": [
              "71000000-0000-4000-8000-000000000302"
            ],
            "localSystemReference": "commerce",
            "identityResolution": "LOCAL_REFERENCE"
          }
        ],
        "applicablePolicies": [
          {
            "policyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "assignment": "DIRECT",
            "systemArn": null,
            "userJourneyId": null,
            "localPolicyReference": "critical",
            "identityResolution": "LOCAL_REFERENCE"
          },
          {
            "policyArn": "arn:aws:resiliencehub:eu-west-1:111122223333:policy/71000000-0000-4000-8000-000000000201",
            "assignment": "INHERITED",
            "systemArn": "arn:aws:resiliencehub:eu-west-1:111122223333:system/71000000-0000-4000-8000-000000000101",
            "userJourneyId": "71000000-0000-4000-8000-000000000302",
            "localPolicyReference": "critical",
            "identityResolution": "LOCAL_REFERENCE"
          }
        ],
        "effectiveTargetObservationId": "targets-checkout-initial",
        "assessedProviderRevision": null,
        "provenance": "LOCAL_CAPTURE"
      }
    },
    "normalizationDiagnostics": [],
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

Use the latest `service.version` as `expectedVersion`. This is the service configuration revision; telemetry and observation refreshes use a separate projection revision. A conflict requires a fresh read and a decision about the intervening change. The revision belongs to the product store; it is not an AWS conditional-write token.

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
