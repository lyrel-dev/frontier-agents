---
id: "resilience-workspace-api-shapes"
title: "Shared API schemas"
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
  - "Shared API schemas"
related:
  - "index.md"
  - "entities.md"
  - "protocol.md"
---



# Shared API schemas

Generated from [contract.cjs](contract.cjs). These JSON Schema definitions describe the implemented mock facade, including local enrichments and projections. They are not a transcription of AWS service models. See [AWS mapping](aws-mapping.md) for provider field ownership and [entity mapping](entities.md) for relationship constraints.

The schema dialect is JSON Schema 2020-12. A schema containing `#/$defs/Name` is resolved by attaching `contract.shapes` as `$defs`. Fields listed in `required` must be present even when their value may be null. Unknown object properties are rejected unless explicitly permitted. Timestamp fields contain numeric epoch seconds. The runtime validator covers the keywords used by this contract; it is not a general-purpose JSON Schema implementation.

## Definitions

- [PermissionModel](#permissionmodel)
- [AssociatedSystem](#associatedsystem)
- [AvailabilitySlo](#availabilityslo)
- [DataRecovery](#datarecovery)
- [DisasterRecovery](#disasterrecovery)
- [ReportConfiguration](#reportconfiguration)
- [DevOpsAgentConfiguration](#devopsagentconfiguration)
- [EksConfiguration](#eksconfiguration)
- [ResourceConfiguration](#resourceconfiguration)
- [DependencyDiscoveryConfig](#dependencydiscoveryconfig)
- [ResourceDiscovery](#resourcediscovery)
- [Achievability](#achievability)
- [HealthObservationInput](#healthobservationinput)
- [HealthProjection](#healthprojection)
- [PostureProjection](#postureprojection)
- [InputSourceEntity](#inputsourceentity)
- [SystemEntity](#systementity)
- [UserJourneyEntity](#userjourneyentity)
- [ServiceEntity](#serviceentity)
- [ResiliencePolicyEntity](#resiliencepolicyentity)
- [AssessmentEntity](#assessmententity)
- [FindingEntity](#findingentity)
- [RecommendationEstimate](#recommendationestimate)
- [RecommendationEnrichment](#recommendationenrichment)
- [RecommendationEntity](#recommendationentity)
- [DependencyEntity](#dependencyentity)
- [TopologyNode](#topologynode)
- [TopologyEdge](#topologyedge)
- [TopologyEntity](#topologyentity)
- [EventEntity](#evententity)
- [ServiceStatus](#servicestatus)
- [WorkspaceSummary](#workspacesummary)
- [PageSnapshot](#pagesnapshot)
- [DeletionReceipt](#deletionreceipt)

## PermissionModel

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `invokerRoleName` | Yes | `string` | Length 1–64; Pattern `^[A-Za-z0-9_+=,.@-]+$` |
| `crossAccountRoles` | No | Array of `object` | Items 0–5 |

```json
{
  "type": "object",
  "properties": {
    "invokerRoleName": {
      "type": "string",
      "minLength": 1,
      "maxLength": 64,
      "pattern": "^[A-Za-z0-9_+=,.@-]+$"
    },
    "crossAccountRoles": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "crossAccountRoleArn": {
            "type": "string",
            "minLength": 20,
            "maxLength": 2048,
            "pattern": "^arn:aws[a-z-]*:iam::[0-9]{12}:role/.+$"
          },
          "externalId": {
            "type": "string",
            "minLength": 2,
            "maxLength": 1224
          }
        },
        "required": [
          "crossAccountRoleArn"
        ],
        "additionalProperties": false
      },
      "minItems": 0,
      "maxItems": 5,
      "uniqueItems": false
    }
  },
  "required": [
    "invokerRoleName"
  ],
  "additionalProperties": false
}
```

## AssociatedSystem

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `systemArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `userJourneyIds` | No | Array of `string` | Items 0–20 |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
    },
    "userJourneyIds": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 256,
        "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
      },
      "minItems": 0,
      "maxItems": 20,
      "uniqueItems": false
    }
  },
  "required": [
    "systemArn"
  ],
  "additionalProperties": false
}
```

## AvailabilitySlo

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `target` | Yes | `number` | Minimum 0; Maximum 100 |

```json
{
  "type": "object",
  "properties": {
    "target": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    }
  },
  "required": [
    "target"
  ],
  "additionalProperties": false
}
```

## DataRecovery

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `timeBetweenBackupsInMinutes` | No | `integer` | Minimum 0; Maximum 5256000 |

```json
{
  "type": "object",
  "properties": {
    "timeBetweenBackupsInMinutes": {
      "type": "integer",
      "minimum": 0,
      "maximum": 5256000
    }
  },
  "required": [],
  "additionalProperties": false
}
```

## DisasterRecovery

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `rtoInMinutes` | No | `integer` | Minimum 0; Maximum 5256000 |
| `rpoInMinutes` | No | `integer` | Minimum 0; Maximum 5256000 |
| `disasterRecoveryApproach` | No | `string` | `ACTIVE_ACTIVE`, `HOT_STANDBY`, `WARM_STANDBY`, `PILOT_LIGHT`, `BACKUP_AND_RESTORE` |

```json
{
  "type": "object",
  "properties": {
    "rtoInMinutes": {
      "type": "integer",
      "minimum": 0,
      "maximum": 5256000
    },
    "rpoInMinutes": {
      "type": "integer",
      "minimum": 0,
      "maximum": 5256000
    },
    "disasterRecoveryApproach": {
      "type": "string",
      "enum": [
        "ACTIVE_ACTIVE",
        "HOT_STANDBY",
        "WARM_STANDBY",
        "PILOT_LIGHT",
        "BACKUP_AND_RESTORE"
      ]
    }
  },
  "required": [],
  "additionalProperties": false
}
```

## ReportConfiguration

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `reportOutputs` | Yes | Array of `object` | Items 1–20 |

```json
{
  "type": "object",
  "properties": {
    "reportOutputs": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "s3": {
            "type": "object",
            "properties": {
              "bucketPath": {
                "type": "string",
                "minLength": 3,
                "maxLength": 2048
              },
              "bucketOwner": {
                "type": "string",
                "minLength": 12,
                "maxLength": 12,
                "pattern": "^[0-9]{12}$"
              }
            },
            "required": [
              "bucketPath",
              "bucketOwner"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "s3"
        ],
        "additionalProperties": false
      },
      "minItems": 1,
      "maxItems": 20,
      "uniqueItems": false
    }
  },
  "required": [
    "reportOutputs"
  ],
  "additionalProperties": false
}
```

## DevOpsAgentConfiguration

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `agentSpaceArn` | Yes | `string` | Length 20–2048 |

```json
{
  "type": "object",
  "properties": {
    "agentSpaceArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048
    }
  },
  "required": [
    "agentSpaceArn"
  ],
  "additionalProperties": false
}
```

## EksConfiguration

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `clusterArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:eks:.+:cluster/.+$` |
| `namespaces` | Yes | Array of `string` | Items 1–100 |
| `labelSelector` | No | `object` | Unknown members rejected |

```json
{
  "type": "object",
  "properties": {
    "clusterArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:eks:.+:cluster/.+$"
    },
    "namespaces": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 63
      },
      "minItems": 1,
      "maxItems": 100,
      "uniqueItems": false
    },
    "labelSelector": {
      "type": "object",
      "properties": {
        "matchLabels": {
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
        "matchExpressions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "minLength": 1,
                "maxLength": 128
              },
              "operator": {
                "type": "string",
                "enum": [
                  "IN",
                  "NOT_IN",
                  "EXISTS",
                  "DOES_NOT_EXIST"
                ]
              },
              "values": {
                "type": "array",
                "items": {
                  "type": "string",
                  "minLength": 0,
                  "maxLength": 256
                },
                "minItems": 0,
                "maxItems": 100,
                "uniqueItems": false
              }
            },
            "required": [
              "key",
              "operator"
            ],
            "additionalProperties": false
          },
          "minItems": 0,
          "maxItems": 100,
          "uniqueItems": false
        }
      },
      "required": [],
      "additionalProperties": false
    }
  },
  "required": [
    "clusterArn",
    "namespaces"
  ],
  "additionalProperties": false
}
```

## ResourceConfiguration

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `resourceTags` | No | Array of `object` | Items 1–50 |
| `cfnStackArn` | No | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:cloudformation:.+:stack/.+$` |
| `tfStateFileUrl` | No | `string` | Length 5–2048; Pattern `^s3://.+` |
| `eks` | No | [EksConfiguration](shapes.md#eksconfiguration) | See shared shape or field semantics. |
| `designFileS3Url` | No | `string` | Length 5–2048; Pattern `^s3://.+` |

```json
{
  "type": "object",
  "properties": {
    "resourceTags": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
          },
          "values": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 0,
              "maxLength": 256
            },
            "minItems": 1,
            "maxItems": 100,
            "uniqueItems": false
          }
        },
        "required": [
          "key",
          "values"
        ],
        "additionalProperties": false
      },
      "minItems": 1,
      "maxItems": 50,
      "uniqueItems": false
    },
    "cfnStackArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:cloudformation:.+:stack/.+$"
    },
    "tfStateFileUrl": {
      "type": "string",
      "minLength": 5,
      "maxLength": 2048,
      "pattern": "^s3://.+"
    },
    "eks": {
      "$ref": "#/$defs/EksConfiguration"
    },
    "designFileS3Url": {
      "type": "string",
      "minLength": 5,
      "maxLength": 2048,
      "pattern": "^s3://.+"
    }
  },
  "required": [],
  "additionalProperties": false,
  "minProperties": 1,
  "maxProperties": 1
}
```

## DependencyDiscoveryConfig

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `status` | Yes | `string` | `ENABLED`, `DISABLED`, `INITIALIZING` |
| `eligibleResourceCount` | Yes | `integer` or `null` | See full schema |
| `message` | Yes | `string` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `requestedStatus` | No | `string` | `ENABLED`, `DISABLED` |

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "ENABLED",
        "DISABLED",
        "INITIALIZING"
      ]
    },
    "eligibleResourceCount": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    },
    "message": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 0,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "updatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "requestedStatus": {
      "type": "string",
      "enum": [
        "ENABLED",
        "DISABLED"
      ]
    }
  },
  "required": [
    "status",
    "eligibleResourceCount",
    "message",
    "updatedAt"
  ],
  "additionalProperties": false
}
```

## ResourceDiscovery

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `status` | Yes | `string` | Length 1–2048 |
| `lastRunAt` | Yes | `number` or `null` | See full schema |
| `errorCode` | Yes | `string` or `null` | See full schema |
| `errorMessage` | Yes | `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "lastRunAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "errorCode": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "errorMessage": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 0,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "status",
    "lastRunAt",
    "errorCode",
    "errorMessage"
  ],
  "additionalProperties": false
}
```

## Achievability

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `availabilitySlo` | No | `string` or `null` | See full schema |
| `multiAzRtoRpo` | No | `string` or `null` | See full schema |
| `multiRegionRtoRpo` | No | `string` or `null` | See full schema |
| `dataRecoveryTimeBetweenBackups` | No | `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "availabilitySlo": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "ACHIEVABLE",
            "NOT_ACHIEVABLE",
            "UNKNOWN"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "multiAzRtoRpo": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "ACHIEVABLE",
            "NOT_ACHIEVABLE",
            "UNKNOWN"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "multiRegionRtoRpo": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "ACHIEVABLE",
            "NOT_ACHIEVABLE",
            "UNKNOWN"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "dataRecoveryTimeBetweenBackups": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "ACHIEVABLE",
            "NOT_ACHIEVABLE",
            "UNKNOWN"
          ]
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [],
  "additionalProperties": false
}
```

## HealthObservationInput

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `state` | Yes | `string` | `HEALTHY`, `DEGRADED`, `UNAVAILABLE`, `UNKNOWN` |
| `observedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `expiresAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `source` | Yes | `string` | Length 1–256 |
| `reason` | Yes | `string` | Length 0–2048 |
| `latencyMs` | No | `number` | Minimum 0 |
| `errorRate` | No | `number` | Minimum 0; Maximum 100 |
| `windowMinutes` | No | `number` | Minimum 0.001; Maximum 1440 |
| `ruleVersion` | Yes | `string` | Length 1–128 |

```json
{
  "type": "object",
  "properties": {
    "state": {
      "type": "string",
      "enum": [
        "HEALTHY",
        "DEGRADED",
        "UNAVAILABLE",
        "UNKNOWN"
      ]
    },
    "observedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "expiresAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "source": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "reason": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "latencyMs": {
      "type": "number",
      "minimum": 0
    },
    "errorRate": {
      "type": "number",
      "minimum": 0,
      "maximum": 100
    },
    "windowMinutes": {
      "type": "number",
      "minimum": 0.001,
      "maximum": 1440
    },
    "ruleVersion": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128
    }
  },
  "required": [
    "state",
    "observedAt",
    "expiresAt",
    "source",
    "reason",
    "ruleVersion"
  ],
  "additionalProperties": false
}
```

## HealthProjection

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `state` | Yes | `string` | `HEALTHY`, `DEGRADED`, `UNAVAILABLE`, `UNKNOWN` |
| `rawState` | Yes | `string` | `HEALTHY`, `DEGRADED`, `UNAVAILABLE`, `UNKNOWN` |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `expiresAt` | Yes | `number` or `null` | See full schema |
| `stale` | Yes | `boolean` | See shared shape or field semantics. |
| `source` | Yes | `string` | Length 0–2048 |
| `reason` | Yes | `string` | Length 0–2048 |
| `observationId` | Yes | `string` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |
| `ruleVersion` | Yes | `string` | Length 0–2048 |
| `ageMinutes` | Yes | `number` or `null` | See full schema |
| `latencyMs` | Yes | `number` or `null` | See full schema |
| `errorRate` | Yes | `number` or `null` | See full schema |
| `windowMinutes` | Yes | `number` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "state": {
      "type": "string",
      "enum": [
        "HEALTHY",
        "DEGRADED",
        "UNAVAILABLE",
        "UNKNOWN"
      ]
    },
    "rawState": {
      "type": "string",
      "enum": [
        "HEALTHY",
        "DEGRADED",
        "UNAVAILABLE",
        "UNKNOWN"
      ]
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "expiresAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "stale": {
      "type": "boolean"
    },
    "source": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "reason": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "observationId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
        },
        {
          "type": "null"
        }
      ]
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "ruleVersion": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "ageMinutes": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    },
    "latencyMs": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    },
    "errorRate": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        },
        {
          "type": "null"
        }
      ]
    },
    "windowMinutes": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "state",
    "rawState",
    "observedAt",
    "expiresAt",
    "stale",
    "source",
    "reason",
    "observationId",
    "provenance",
    "ruleVersion",
    "ageMinutes",
    "latencyMs",
    "errorRate",
    "windowMinutes"
  ],
  "additionalProperties": false
}
```

## PostureProjection

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `state` | Yes | `string` | `ACHIEVABLE`, `NOT_ACHIEVABLE`, `UNKNOWN` |
| `achievability` | Yes | [Achievability](shapes.md#achievability) | See shared shape or field semantics. |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `stale` | Yes | `boolean` | See shared shape or field semantics. |
| `assessmentId` | Yes | `string` or `null` | See full schema |
| `observationId` | Yes | `string` or `null` | See full schema |
| `ruleVersion` | Yes | `string` | Length 1–2048 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `evaluatedProviderRevision` | Yes | `string` or `null` | See full schema |
| `policyContextCaptureId` | Yes | `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "state": {
      "type": "string",
      "enum": [
        "ACHIEVABLE",
        "NOT_ACHIEVABLE",
        "UNKNOWN"
      ]
    },
    "achievability": {
      "$ref": "#/$defs/Achievability"
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "stale": {
      "type": "boolean"
    },
    "assessmentId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
        },
        {
          "type": "null"
        }
      ]
    },
    "observationId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
        },
        {
          "type": "null"
        }
      ]
    },
    "ruleVersion": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "evaluatedProviderRevision": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "policyContextCaptureId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 256,
          "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "state",
    "achievability",
    "observedAt",
    "stale",
    "assessmentId",
    "observationId",
    "ruleVersion",
    "provenance",
    "evaluatedProviderRevision",
    "policyContextCaptureId"
  ],
  "additionalProperties": false
}
```

## InputSourceEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `inputSourceId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `type` | Yes | `string` | `CFN_STACK`, `TAGS`, `TERRAFORM`, `EKS`, `DESIGN_FILE`, `MONITORING` |
| `createdAt` | Yes | `number` or `null` | See full schema |
| `resourceConfiguration` | Yes | [ResourceConfiguration](shapes.md#resourceconfiguration) or `null` | See full schema |
| `displayName` | Yes | `string` | Length 0–256 |
| `status` | Yes | `string` | Length 1–2048 |
| `version` | Yes | `integer` | Minimum 1 |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |

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
    "inputSourceId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "type": {
      "type": "string",
      "enum": [
        "CFN_STACK",
        "TAGS",
        "TERRAFORM",
        "EKS",
        "DESIGN_FILE",
        "MONITORING"
      ]
    },
    "createdAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "resourceConfiguration": {
      "anyOf": [
        {
          "$ref": "#/$defs/ResourceConfiguration"
        },
        {
          "type": "null"
        }
      ]
    },
    "displayName": {
      "type": "string",
      "minLength": 0,
      "maxLength": 256
    },
    "status": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceArn",
    "inputSourceId",
    "type",
    "createdAt",
    "resourceConfiguration",
    "displayName",
    "status",
    "version",
    "observedAt",
    "provenance"
  ],
  "additionalProperties": false
}
```

## SystemEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `systemArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `systemId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `description` | Yes | `string` | Length 0–2048 |
| `createdAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `sharingEnabled` | Yes | `boolean` | See shared shape or field semantics. |
| `kmsKeyId` | Yes | `string` or `null` | See full schema |
| `tags` | Yes | Map of `string` | Properties 0–50 |
| `displayName` | Yes | `string` | Length 0–256 |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
    },
    "systemId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 60,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$"
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "createdAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "sharingEnabled": {
      "type": "boolean"
    },
    "kmsKeyId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
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
    "displayName": {
      "type": "string",
      "minLength": 0,
      "maxLength": 256
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "systemArn",
    "systemId",
    "name",
    "description",
    "createdAt",
    "updatedAt",
    "sharingEnabled",
    "kmsKeyId",
    "tags",
    "displayName",
    "version",
    "provenance"
  ],
  "additionalProperties": false
}
```

## UserJourneyEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `systemArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `userJourneyId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9 _-]{1,59}$` |
| `description` | Yes | `string` | Length 0–2048 |
| `policyArn` | Yes | `string` or `null` | See full schema |
| `serviceArns` | Yes | Array of `string` | Items 0–1000 |
| `createdAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
    },
    "userJourneyId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 60,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9 _-]{1,59}$"
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
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
    "serviceArns": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 20,
        "maxLength": 2048,
        "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "createdAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "systemArn",
    "userJourneyId",
    "name",
    "description",
    "policyArn",
    "serviceArns",
    "createdAt",
    "updatedAt",
    "version",
    "provenance"
  ],
  "additionalProperties": false
}
```

## ServiceEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `description` | Yes | `string` | Length 0–2048 |
| `displayName` | Yes | `string` | Length 0–256 |
| `createdAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `observedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `associatedSystems` | Yes | Array of [AssociatedSystem](shapes.md#associatedsystem) | Items 0–20 |
| `policyArn` | Yes | `string` or `null` | See full schema |
| `regions` | Yes | Array of `string` | Items 1–5 |
| `permissionModel` | Yes | [PermissionModel](shapes.md#permissionmodel) | See shared shape or field semantics. |
| `dependencyDiscovery` | Yes | [DependencyDiscoveryConfig](shapes.md#dependencydiscoveryconfig) | See shared shape or field semantics. |
| `resourceDiscovery` | Yes | [ResourceDiscovery](shapes.md#resourcediscovery) | See shared shape or field semantics. |
| `achievability` | Yes | [Achievability](shapes.md#achievability) | See shared shape or field semantics. |
| `assessmentStatus` | Yes | `string` | Length 1–2048 |
| `inputSourceIds` | Yes | Array of `string` | Items 0–1000 |
| `resourceCount` | Yes | `integer` or `null` | See full schema |
| `reportConfiguration` | Yes | [ReportConfiguration](shapes.md#reportconfiguration) or `null` | See full schema |
| `devOpsAgentConfiguration` | Yes | [DevOpsAgentConfiguration](shapes.md#devopsagentconfiguration) or `null` | See full schema |
| `tags` | Yes | Map of `string` | Properties 0–50 |
| `kmsKeyId` | Yes | `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `refreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `provenance` | Yes | `string` | Length 1–2048 |

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
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 60,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$"
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "displayName": {
      "type": "string",
      "minLength": 0,
      "maxLength": 256
    },
    "createdAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "observedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
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
        "maxLength": 64
      },
      "minItems": 1,
      "maxItems": 5,
      "uniqueItems": false
    },
    "permissionModel": {
      "$ref": "#/$defs/PermissionModel"
    },
    "dependencyDiscovery": {
      "$ref": "#/$defs/DependencyDiscoveryConfig"
    },
    "resourceDiscovery": {
      "$ref": "#/$defs/ResourceDiscovery"
    },
    "achievability": {
      "$ref": "#/$defs/Achievability"
    },
    "assessmentStatus": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "inputSourceIds": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 256,
        "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "resourceCount": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0
        },
        {
          "type": "null"
        }
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
    "kmsKeyId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "refreshRequired": {
      "type": "boolean"
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceArn",
    "name",
    "description",
    "displayName",
    "createdAt",
    "updatedAt",
    "observedAt",
    "associatedSystems",
    "policyArn",
    "regions",
    "permissionModel",
    "dependencyDiscovery",
    "resourceDiscovery",
    "achievability",
    "assessmentStatus",
    "inputSourceIds",
    "resourceCount",
    "reportConfiguration",
    "devOpsAgentConfiguration",
    "tags",
    "kmsKeyId",
    "version",
    "refreshRequired",
    "provenance"
  ],
  "additionalProperties": false
}
```

## ResiliencePolicyEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `policyArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `displayName` | Yes | `string` | Length 0–256 |
| `description` | Yes | `string` | Length 0–2048 |
| `availabilitySlo` | No | [AvailabilitySlo](shapes.md#availabilityslo) | See shared shape or field semantics. |
| `multiAz` | No | [DisasterRecovery](shapes.md#disasterrecovery) | See shared shape or field semantics. |
| `multiRegion` | No | [DisasterRecovery](shapes.md#disasterrecovery) | See shared shape or field semantics. |
| `dataRecovery` | No | [DataRecovery](shapes.md#datarecovery) | See shared shape or field semantics. |
| `createdAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `sharingEnabled` | Yes | `boolean` | See shared shape or field semantics. |
| `kmsKeyId` | Yes | `string` or `null` | See full schema |
| `tags` | Yes | Map of `string` | Properties 0–50 |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "policyArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
    },
    "name": {
      "type": "string",
      "minLength": 2,
      "maxLength": 60,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$"
    },
    "displayName": {
      "type": "string",
      "minLength": 0,
      "maxLength": 256
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "availabilitySlo": {
      "$ref": "#/$defs/AvailabilitySlo"
    },
    "multiAz": {
      "$ref": "#/$defs/DisasterRecovery"
    },
    "multiRegion": {
      "$ref": "#/$defs/DisasterRecovery"
    },
    "dataRecovery": {
      "$ref": "#/$defs/DataRecovery"
    },
    "createdAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "sharingEnabled": {
      "type": "boolean"
    },
    "kmsKeyId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
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
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "policyArn",
    "name",
    "displayName",
    "description",
    "createdAt",
    "updatedAt",
    "sharingEnabled",
    "kmsKeyId",
    "tags",
    "version",
    "provenance"
  ],
  "additionalProperties": false
}
```

## AssessmentEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `assessmentId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `status` | Yes | `string` | `NOT_STARTED`, `PENDING`, `IN_PROGRESS`, `SUCCESS`, `FAILED` |
| `startedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `endedAt` | Yes | `number` or `null` | See full schema |
| `observedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `failureModeFindingsCount` | Yes | `integer` or `null` | See full schema |
| `achievability` | Yes | [Achievability](shapes.md#achievability) | See shared shape or field semantics. |
| `errorCode` | Yes | `string` or `null` | See full schema |
| `errorMessage` | Yes | `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |

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
    "assessmentId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "status": {
      "type": "string",
      "enum": [
        "NOT_STARTED",
        "PENDING",
        "IN_PROGRESS",
        "SUCCESS",
        "FAILED"
      ]
    },
    "startedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "endedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "observedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "failureModeFindingsCount": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    },
    "achievability": {
      "$ref": "#/$defs/Achievability"
    },
    "errorCode": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "errorMessage": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 0,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceArn",
    "assessmentId",
    "status",
    "startedAt",
    "endedAt",
    "observedAt",
    "failureModeFindingsCount",
    "achievability",
    "errorCode",
    "errorMessage",
    "version",
    "provenance"
  ],
  "additionalProperties": false
}
```

## FindingEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `findingId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `name` | Yes | `string` | Length 1–2048 |
| `description` | Yes | `string` | Length 0–2048 |
| `reasoning` | Yes | `string` | Length 0–2048 |
| `severity` | Yes | `string` | `HIGH`, `MEDIUM`, `LOW` |
| `status` | Yes | `string` | `OPEN`, `RESOLVED`, `IRRELEVANT` |
| `failureCategory` | Yes | `string` | Length 1–2048 |
| `policyComponent` | Yes | `string` | Length 1–2048 |
| `serviceFunctions` | Yes | Array of `string` | Items 0–1000 |
| `comment` | Yes | `string` | Length 0–2048 |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `detailObservedAt` | Yes | `number` or `null` | See full schema |
| `observationId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `captureId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `representation` | Yes | `string` | `DETAIL`, `SUMMARY` |
| `recommendationIds` | Yes | Array of `string` | Items 0–1000 |
| `verification` | Yes | `string` | Length 1–2048 |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |

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
    "findingId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "reasoning": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "severity": {
      "type": "string",
      "enum": [
        "HIGH",
        "MEDIUM",
        "LOW"
      ]
    },
    "status": {
      "type": "string",
      "enum": [
        "OPEN",
        "RESOLVED",
        "IRRELEVANT"
      ]
    },
    "failureCategory": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "policyComponent": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "serviceFunctions": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2048
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "comment": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "detailObservedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "observationId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "captureId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "representation": {
      "type": "string",
      "enum": [
        "DETAIL",
        "SUMMARY"
      ]
    },
    "recommendationIds": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 256,
        "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "verification": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceArn",
    "findingId",
    "name",
    "description",
    "reasoning",
    "severity",
    "status",
    "failureCategory",
    "policyComponent",
    "serviceFunctions",
    "comment",
    "updatedAt",
    "detailObservedAt",
    "observationId",
    "captureId",
    "representation",
    "recommendationIds",
    "verification",
    "version",
    "provenance"
  ],
  "additionalProperties": false
}
```

## RecommendationEstimate

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `amount` | Yes | `number` or `null` | See full schema |
| `currency` | Yes | `string` | Length 3–3 |
| `basis` | Yes | `string` | Length 1–2048 |
| `complexity` | Yes | `string` | `LOW`, `MEDIUM`, `HIGH`, `UNKNOWN` |
| `source` | Yes | `string` | Length 1–2048 |
| `estimatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `confidence` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "amount": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    },
    "currency": {
      "type": "string",
      "minLength": 3,
      "maxLength": 3
    },
    "basis": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "complexity": {
      "type": "string",
      "enum": [
        "LOW",
        "MEDIUM",
        "HIGH",
        "UNKNOWN"
      ]
    },
    "source": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "estimatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "confidence": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "amount",
    "currency",
    "basis",
    "complexity",
    "source",
    "estimatedAt",
    "confidence"
  ],
  "additionalProperties": false
}
```

## RecommendationEnrichment

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `title` | Yes | `string` | Length 1–256 |
| `description` | Yes | `string` | Length 0–2048 |
| `estimate` | Yes | [RecommendationEstimate](shapes.md#recommendationestimate) or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "description": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "estimate": {
      "anyOf": [
        {
          "$ref": "#/$defs/RecommendationEstimate"
        },
        {
          "type": "null"
        }
      ]
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "title",
    "description",
    "estimate",
    "version",
    "updatedAt",
    "provenance"
  ],
  "additionalProperties": false
}
```

## RecommendationEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `recommendationId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `findingId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `findingObservationId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `category` | Yes | `string` | `INFRASTRUCTURE_AND_CODE`, `OBSERVABILITY`, `TESTING` |
| `sourceArrayOrdinal` | Yes | `integer` | Minimum 0 |
| `suggestedChanges` | Yes | Array of `string` | Items 0–1000 |
| `capturedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `enrichment` | Yes | [RecommendationEnrichment](shapes.md#recommendationenrichment) | See shared shape or field semantics. |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "recommendationId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "serviceArn": {
      "type": "string",
      "minLength": 20,
      "maxLength": 2048,
      "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
    },
    "findingId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "findingObservationId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "category": {
      "type": "string",
      "enum": [
        "INFRASTRUCTURE_AND_CODE",
        "OBSERVABILITY",
        "TESTING"
      ]
    },
    "sourceArrayOrdinal": {
      "type": "integer",
      "minimum": 0
    },
    "suggestedChanges": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2048
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "capturedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "enrichment": {
      "$ref": "#/$defs/RecommendationEnrichment"
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "recommendationId",
    "serviceArn",
    "findingId",
    "findingObservationId",
    "category",
    "sourceArrayOrdinal",
    "suggestedChanges",
    "capturedAt",
    "enrichment",
    "provenance"
  ],
  "additionalProperties": false
}
```

## DependencyEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `dependencyId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `dependencyName` | Yes | `string` | Length 1–2048 |
| `dnsName` | Yes | `string` or `null` | See full schema |
| `location` | Yes | `string` | Length 1–2048 |
| `criticality` | Yes | `string` | `HARD`, `SOFT`, `UNKNOWN` |
| `comment` | Yes | `string` | Length 0–2048 |
| `provider` | Yes | `string` | Length 1–2048 |
| `sourceRegions` | Yes | Array of `string` | Items 0–1000 |
| `lastDetectedTime` | Yes | `number` or `null` | See full schema |
| `updatedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `governance` | Yes | `object` | Unknown members rejected |
| `resolvedServiceArn` | Yes | `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |

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
    "dependencyId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "dependencyName": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "dnsName": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "location": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "criticality": {
      "type": "string",
      "enum": [
        "HARD",
        "SOFT",
        "UNKNOWN"
      ]
    },
    "comment": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "provider": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "sourceRegions": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2048
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "lastDetectedTime": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        {
          "type": "null"
        }
      ]
    },
    "updatedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "governance": {
      "type": "object",
      "properties": {
        "allowedStatus": {
          "type": "string",
          "enum": [
            "ALLOWED",
            "REVIEW",
            "DENIED"
          ]
        },
        "source": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        "observedAt": {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799
        },
        "version": {
          "type": "integer",
          "minimum": 1
        }
      },
      "required": [
        "allowedStatus",
        "source",
        "observedAt",
        "version"
      ],
      "additionalProperties": false
    },
    "resolvedServiceArn": {
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
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceArn",
    "dependencyId",
    "dependencyName",
    "dnsName",
    "location",
    "criticality",
    "comment",
    "provider",
    "sourceRegions",
    "lastDetectedTime",
    "updatedAt",
    "governance",
    "resolvedServiceArn",
    "version",
    "provenance"
  ],
  "additionalProperties": false
}
```

## TopologyNode

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `id` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `resourceIdentifier` | Yes | `string` | Length 1–2048 |
| `name` | Yes | `string` | Length 1–2048 |
| `type` | Yes | `string` | Length 1–2048 |
| `region` | Yes | `string` or `null` | See full schema |
| `accountId` | Yes | `string` or `null` | See full schema |
| `status` | Yes | `string` | `KNOWN`, `UNRESOLVED` |

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "resourceIdentifier": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "type": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "region": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "accountId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "status": {
      "type": "string",
      "enum": [
        "KNOWN",
        "UNRESOLVED"
      ]
    }
  },
  "required": [
    "id",
    "resourceIdentifier",
    "name",
    "type",
    "region",
    "accountId",
    "status"
  ],
  "additionalProperties": false
}
```

## TopologyEdge

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `id` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `source` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `target` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `type` | Yes | `string` | Length 1–2048 |
| `label` | Yes | `string` | Length 0–2048 |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "source": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "target": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "type": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "label": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "id",
    "source",
    "target",
    "type",
    "label",
    "provenance"
  ],
  "additionalProperties": false
}
```

## TopologyEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `topologyId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `capturedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `captureStartedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `captureEndedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `sourceObservedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `collectionStatus` | Yes | `string` | `COMPLETE`, `PARTIAL` |
| `queryScope` | Yes | `object` | See shared shape or field semantics. |
| `resourceCount` | Yes | `integer` | Minimum 0 |
| `totalServiceResourceCount` | Yes | `integer` or `null` | See full schema |
| `edgeCount` | Yes | `integer` | Minimum 0 |
| `unresolvedCount` | Yes | `integer` | Minimum 0 |
| `nodes` | Yes | Array of [TopologyNode](shapes.md#topologynode) | Items 0–1000 |
| `edges` | Yes | Array of [TopologyEdge](shapes.md#topologyedge) | Items 0–1000 |
| `atomicSnapshot` | Yes | `boolean` | See shared shape or field semantics. |
| `provenance` | Yes | `string` | Length 1–2048 |
| `coverageMessage` | Yes | `string` | Length 0–2048 |
| `captureMode` | Yes | `string` | `FIXTURE_CAPTURE`, `LOCAL_COPY` |
| `version` | Yes | `integer` | Minimum 1 |

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
    "topologyId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "capturedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "captureStartedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "captureEndedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "sourceObservedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "collectionStatus": {
      "type": "string",
      "enum": [
        "COMPLETE",
        "PARTIAL"
      ]
    },
    "queryScope": {
      "type": "object",
      "additionalProperties": true
    },
    "resourceCount": {
      "type": "integer",
      "minimum": 0
    },
    "totalServiceResourceCount": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    },
    "edgeCount": {
      "type": "integer",
      "minimum": 0
    },
    "unresolvedCount": {
      "type": "integer",
      "minimum": 0
    },
    "nodes": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/TopologyNode"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "edges": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/TopologyEdge"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "atomicSnapshot": {
      "type": "boolean"
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "coverageMessage": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "captureMode": {
      "type": "string",
      "enum": [
        "FIXTURE_CAPTURE",
        "LOCAL_COPY"
      ]
    },
    "version": {
      "type": "integer",
      "minimum": 1
    }
  },
  "required": [
    "serviceArn",
    "topologyId",
    "capturedAt",
    "captureStartedAt",
    "captureEndedAt",
    "sourceObservedAt",
    "collectionStatus",
    "queryScope",
    "resourceCount",
    "totalServiceResourceCount",
    "edgeCount",
    "unresolvedCount",
    "nodes",
    "edges",
    "atomicSnapshot",
    "provenance",
    "coverageMessage",
    "captureMode",
    "version"
  ],
  "additionalProperties": false
}
```

## EventEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `eventId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `sourceEventId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `eventKey` | Yes | `string` | Length 1–2048 |
| `channel` | Yes | `string` | `TELEMETRY`, `ENTITY_TIMELINE`, `EVENTBRIDGE`, `LOCAL` |
| `streamOwner` | Yes | `string` | Length 1–2048 |
| `source` | Yes | `string` | Length 1–2048 |
| `type` | Yes | `string` | Length 1–2048 |
| `title` | Yes | `string` | Length 1–2048 |
| `message` | Yes | `string` | Length 0–2048 |
| `severity` | Yes | `string` | `INFO`, `WARNING`, `ERROR` |
| `serviceArn` | Yes | `string` or `null` | See full schema |
| `entityType` | Yes | `string` | Length 1–2048 |
| `entityId` | Yes | `string` | Length 1–2048 |
| `occurredAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `receivedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `linkage` | Yes | `string` | `ASSERTED`, `INFERRED` |
| `refreshStatus` | Yes | `string` | Length 1–2048 |
| `sequence` | Yes | `integer` | Minimum 1 |
| `mock` | Yes | `boolean` | See shared shape or field semantics. |
| `producerPrincipalId` | Yes | `string` or `null` | See full schema |
| `trustedSource` | Yes | `boolean` | See shared shape or field semantics. |

```json
{
  "type": "object",
  "properties": {
    "eventId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "sourceEventId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "eventKey": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "channel": {
      "type": "string",
      "enum": [
        "TELEMETRY",
        "ENTITY_TIMELINE",
        "EVENTBRIDGE",
        "LOCAL"
      ]
    },
    "streamOwner": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "source": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "type": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "title": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
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
    "serviceArn": {
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
    "entityType": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "entityId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "occurredAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "receivedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "linkage": {
      "type": "string",
      "enum": [
        "ASSERTED",
        "INFERRED"
      ]
    },
    "refreshStatus": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "sequence": {
      "type": "integer",
      "minimum": 1
    },
    "mock": {
      "type": "boolean"
    },
    "producerPrincipalId": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 1,
          "maxLength": 2048
        },
        {
          "type": "null"
        }
      ]
    },
    "trustedSource": {
      "type": "boolean"
    }
  },
  "required": [
    "eventId",
    "sourceEventId",
    "eventKey",
    "channel",
    "streamOwner",
    "source",
    "type",
    "title",
    "message",
    "severity",
    "serviceArn",
    "entityType",
    "entityId",
    "occurredAt",
    "receivedAt",
    "linkage",
    "refreshStatus",
    "sequence",
    "mock",
    "producerPrincipalId",
    "trustedSource"
  ],
  "additionalProperties": false
}
```

## ServiceStatus

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 20–2048; Pattern `^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9_-]+$` |
| `health` | Yes | [HealthProjection](shapes.md#healthprojection) | See shared shape or field semantics. |
| `posture` | Yes | [PostureProjection](shapes.md#postureprojection) | See shared shape or field semantics. |
| `assessmentStatus` | Yes | `string` | Length 1–2048 |
| `dependencyDiscovery` | Yes | [DependencyDiscoveryConfig](shapes.md#dependencydiscoveryconfig) | See shared shape or field semantics. |
| `resourceDiscovery` | Yes | [ResourceDiscovery](shapes.md#resourcediscovery) | See shared shape or field semantics. |
| `needsAttention` | Yes | `boolean` | See shared shape or field semantics. |
| `openFindingsCount` | Yes | `integer` | Minimum 0 |
| `computedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `version` | Yes | `integer` | Minimum 1 |
| `refreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `provenance` | Yes | `string` | Length 1–2048 |

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
    "health": {
      "$ref": "#/$defs/HealthProjection"
    },
    "posture": {
      "$ref": "#/$defs/PostureProjection"
    },
    "assessmentStatus": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "dependencyDiscovery": {
      "$ref": "#/$defs/DependencyDiscoveryConfig"
    },
    "resourceDiscovery": {
      "$ref": "#/$defs/ResourceDiscovery"
    },
    "needsAttention": {
      "type": "boolean"
    },
    "openFindingsCount": {
      "type": "integer",
      "minimum": 0
    },
    "computedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "refreshRequired": {
      "type": "boolean"
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceArn",
    "health",
    "posture",
    "assessmentStatus",
    "dependencyDiscovery",
    "resourceDiscovery",
    "needsAttention",
    "openFindingsCount",
    "computedAt",
    "version",
    "refreshRequired",
    "provenance"
  ],
  "additionalProperties": false
}
```

## WorkspaceSummary

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceCount` | Yes | `integer` | Minimum 0 |
| `healthyCount` | Yes | `integer` | Minimum 0 |
| `degradedCount` | Yes | `integer` | Minimum 0 |
| `unavailableCount` | Yes | `integer` | Minimum 0 |
| `unknownHealthCount` | Yes | `integer` | Minimum 0 |
| `achievableCount` | Yes | `integer` | Minimum 0 |
| `atRiskCount` | Yes | `integer` | Minimum 0 |
| `unknownPostureCount` | Yes | `integer` | Minimum 0 |
| `stalePostureCount` | Yes | `integer` | Minimum 0 |
| `attentionCount` | Yes | `integer` | Minimum 0 |
| `openFindingCount` | Yes | `integer` | Minimum 0 |
| `contributorServiceArns` | Yes | Array of `string` | Items 0–1000 |
| `computedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `aggregationRule` | Yes | `string` | Length 1–2048 |
| `interpretation` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "serviceCount": {
      "type": "integer",
      "minimum": 0
    },
    "healthyCount": {
      "type": "integer",
      "minimum": 0
    },
    "degradedCount": {
      "type": "integer",
      "minimum": 0
    },
    "unavailableCount": {
      "type": "integer",
      "minimum": 0
    },
    "unknownHealthCount": {
      "type": "integer",
      "minimum": 0
    },
    "achievableCount": {
      "type": "integer",
      "minimum": 0
    },
    "atRiskCount": {
      "type": "integer",
      "minimum": 0
    },
    "unknownPostureCount": {
      "type": "integer",
      "minimum": 0
    },
    "stalePostureCount": {
      "type": "integer",
      "minimum": 0
    },
    "attentionCount": {
      "type": "integer",
      "minimum": 0
    },
    "openFindingCount": {
      "type": "integer",
      "minimum": 0
    },
    "contributorServiceArns": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 20,
        "maxLength": 2048,
        "pattern": "^arn:aws[a-z-]*:resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9_-]+$"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "computedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "aggregationRule": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "interpretation": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "serviceCount",
    "healthyCount",
    "degradedCount",
    "unavailableCount",
    "unknownHealthCount",
    "achievableCount",
    "atRiskCount",
    "unknownPostureCount",
    "stalePostureCount",
    "attentionCount",
    "openFindingCount",
    "contributorServiceArns",
    "computedAt",
    "aggregationRule",
    "interpretation"
  ],
  "additionalProperties": false
}
```

## PageSnapshot

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `snapshotId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `createdAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `expiresAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `totalResults` | Yes | `integer` | Minimum 0 |

```json
{
  "type": "object",
  "properties": {
    "snapshotId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "createdAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "expiresAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "totalResults": {
      "type": "integer",
      "minimum": 0
    }
  },
  "required": [
    "snapshotId",
    "createdAt",
    "expiresAt",
    "totalResults"
  ],
  "additionalProperties": false
}
```

## DeletionReceipt

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `resourceId` | Yes | `string` | Length 1–2048 |
| `deleted` | Yes | `boolean` | Exactly `true` |
| `deletedAt` | Yes | `number` | Minimum 0; Maximum 253402300799 |
| `version` | Yes | `integer` | Minimum 1 |
| `historyRetained` | Yes | `boolean` | Exactly `true` |

```json
{
  "type": "object",
  "properties": {
    "resourceId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "deleted": {
      "const": true,
      "type": "boolean"
    },
    "deletedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799
    },
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "historyRetained": {
      "const": true,
      "type": "boolean"
    }
  },
  "required": [
    "resourceId",
    "deleted",
    "deletedAt",
    "version",
    "historyRetained"
  ],
  "additionalProperties": false
}
```
