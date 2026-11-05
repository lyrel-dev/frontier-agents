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

The schema dialect is JSON Schema 2020-12. A schema containing `#/$defs/Name` is resolved by attaching `contract.shapes` as `$defs`. Fields listed in `required` must be present even when their value may be null. Unknown object properties are rejected unless explicitly permitted. Timestamp fields contain numeric epoch seconds with at most millisecond precision. The `x-precision` extension is an assertion enforced by the runtime; a generic JSON Schema validator treats it as an annotation, so structural schema validation alone does not verify timestamp ordering. The runtime validator covers the keywords used by this contract; it is not a general-purpose JSON Schema implementation.

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
- [NormalizationDiagnostic](#normalizationdiagnostic)
- [PermissionModelObservation](#permissionmodelobservation)
- [DisasterRecoveryObservation](#disasterrecoveryobservation)
- [DataRecoveryObservation](#datarecoveryobservation)
- [AttentionReason](#attentionreason)
- [AssessmentCoverage](#assessmentcoverage)
- [EffectiveTarget](#effectivetarget)
- [EffectiveTargetObservation](#effectivetargetobservation)
- [CapturedAssociation](#capturedassociation)
- [PolicyAssignmentEvidence](#policyassignmentevidence)
- [PolicyContextCapture](#policycontextcapture)
- [EffectivePolicyEvidence](#effectivepolicyevidence)
- [FindingCapture](#findingcapture)
- [FindingObservation](#findingobservation)
- [FindingCoverage](#findingcoverage)
- [HealthObservation](#healthobservation)
- [PostureObservation](#postureobservation)
- [SelectedObservations](#selectedobservations)
- [EventSubject](#eventsubject)

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
| `systemArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `userJourneyIds` | No | Array of `string` | Items 0–20 |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
| `reportOutputs` | Yes | Array of `object` | Items 1–1 |

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
                "maxLength": 512,
                "pattern": "^(s3://)?[a-z0-9][a-z0-9.-]{1,61}[a-z0-9](/.*)?$"
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
      "maxItems": 1,
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
| `namespaces` | Yes | Array of `string` | Items 1–10 |
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
        "maxLength": 63,
        "pattern": "^[a-z0-9]([-a-z0-9]*[a-z0-9])?$"
      },
      "minItems": 1,
      "maxItems": 10,
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
            "maxLength": 317,
            "pattern": "^([a-z0-9]([-a-z0-9.]*[a-z0-9])?/)?[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?$"
          },
          "additionalProperties": {
            "type": "string",
            "minLength": 0,
            "maxLength": 63,
            "pattern": "^([A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?)?$"
          },
          "maxProperties": 20
        },
        "matchExpressions": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "minLength": 1,
                "maxLength": 317,
                "pattern": "^([a-z0-9]([-a-z0-9.]*[a-z0-9])?/)?[A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?$"
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
                  "maxLength": 63,
                  "pattern": "^([A-Za-z0-9]([-A-Za-z0-9_.]*[A-Za-z0-9])?)?$"
                },
                "minItems": 0,
                "maxItems": 20,
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
          "maxItems": 20,
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
| `resourceTags` | No | Array of `object` | Items 1–10 |
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
            "maxLength": 128,
            "pattern": "^[^\\x00-\\x1f\\x22]+$"
          },
          "values": {
            "type": "array",
            "items": {
              "type": "string",
              "minLength": 0,
              "maxLength": 256,
              "pattern": "^[^\\x00-\\x1f\\x22]*$"
            },
            "minItems": 0,
            "maxItems": 10,
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
      "maxItems": 10,
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
| `status` | Yes | `string` | `ENABLED`, `DISABLED`, `INITIALIZING`, `UNKNOWN` |
| `eligibleResourceCount` | Yes | `integer` or `null` | See full schema |
| `message` | Yes | `string` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `requestedStatus` | No | `string` | `ENABLED`, `DISABLED` |
| `rawStatus` | Yes | `string` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "ENABLED",
        "DISABLED",
        "INITIALIZING",
        "UNKNOWN"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
    },
    "rawStatus": {
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
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    }
  },
  "required": [
    "status",
    "eligibleResourceCount",
    "message",
    "updatedAt",
    "rawStatus",
    "normalizationDiagnostics"
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
| `rawStatus` | Yes | `string` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
    },
    "rawStatus": {
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
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    }
  },
  "required": [
    "status",
    "lastRunAt",
    "errorCode",
    "errorMessage",
    "rawStatus",
    "normalizationDiagnostics"
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
| `observedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `expiresAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
    },
    "expiresAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
| `rawState` | Yes | `string` or `null` | See full schema |
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
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
| `rawState` | Yes | `string` or `null` | See full schema |

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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
    },
    "rawState": {
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
    "state",
    "achievability",
    "observedAt",
    "stale",
    "assessmentId",
    "observationId",
    "ruleVersion",
    "provenance",
    "evaluatedProviderRevision",
    "policyContextCaptureId",
    "rawState"
  ],
  "additionalProperties": false
}
```

## InputSourceEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `inputSourceId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `type` | Yes | `string` | `CFN_STACK`, `TAGS`, `TERRAFORM`, `EKS`, `DESIGN_FILE`, `MONITORING`, `UNKNOWN` |
| `createdAt` | Yes | `number` or `null` | See full schema |
| `resourceConfiguration` | Yes | [ResourceConfiguration](shapes.md#resourceconfiguration) or `null` | See full schema |
| `displayName` | Yes | `string` | Length 0–256 |
| `status` | Yes | `string` | Length 1–2048 |
| `version` | Yes | `integer` | Minimum 1 |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |
| `rawType` | Yes | `string` or `null` | See full schema |
| `localCreatedAt` | Yes | `number` or `null` | See full schema |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

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
        "MONITORING",
        "UNKNOWN"
      ]
    },
    "createdAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
    "rawType": {
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
    "localCreatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "rawType",
    "localCreatedAt",
    "localUpdatedAt",
    "normalizationDiagnostics"
  ],
  "additionalProperties": false
}
```

## SystemEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `systemArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `systemId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `description` | Yes | `string` | Length 0–2048 |
| `createdAt` | Yes | `number` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `sharingEnabled` | Yes | `boolean` or `null` | See full schema |
| `kmsKeyId` | Yes | `string` or `null` | See full schema |
| `tags` | Yes | Map of `string` or `null` | See full schema |
| `displayName` | Yes | `string` | Length 0–256 |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "sharingEnabled": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ]
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
      "anyOf": [
        {
          "type": "object",
          "propertyNames": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
            "pattern": "^[^\\x00-\\x1f\\x22]+$"
          },
          "additionalProperties": {
            "type": "string",
            "minLength": 0,
            "maxLength": 256,
            "pattern": "^[^\\x00-\\x1f\\x22]*$"
          },
          "maxProperties": 50
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
    "version": {
      "type": "integer",
      "minimum": 1
    },
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "localUpdatedAt",
    "normalizationDiagnostics"
  ],
  "additionalProperties": false
}
```

## UserJourneyEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `systemArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `userJourneyId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9 _-]{1,59}$` |
| `description` | Yes | `string` | Length 0–2048 |
| `policyArn` | Yes | `string` or `null` | See full schema |
| `serviceArns` | Yes | Array of `string` | Items 0–unbounded |
| `createdAt` | Yes | `number` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
          "minLength": 31,
          "maxLength": 2048,
          "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
        "minLength": 31,
        "maxLength": 2048,
        "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
      },
      "minItems": 0,
      "uniqueItems": false
    },
    "createdAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
    },
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "localUpdatedAt",
    "normalizationDiagnostics"
  ],
  "additionalProperties": false
}
```

## ServiceEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `description` | Yes | `string` | Length 0–2048 |
| `displayName` | Yes | `string` | Length 0–256 |
| `createdAt` | Yes | `number` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `associatedSystems` | Yes | Array of [AssociatedSystem](shapes.md#associatedsystem) | Items 0–20 |
| `policyArn` | Yes | `string` or `null` | See full schema |
| `regions` | Yes | Array of `string` or `null` | See full schema |
| `permissionModel` | Yes | [PermissionModelObservation](shapes.md#permissionmodelobservation) or `null` | See full schema |
| `dependencyDiscovery` | Yes | [DependencyDiscoveryConfig](shapes.md#dependencydiscoveryconfig) | See shared shape or field semantics. |
| `resourceDiscovery` | Yes | [ResourceDiscovery](shapes.md#resourcediscovery) | See shared shape or field semantics. |
| `achievability` | Yes | [Achievability](shapes.md#achievability) | See shared shape or field semantics. |
| `assessmentStatus` | Yes | `string` | `NOT_STARTED`, `PENDING`, `IN_PROGRESS`, `SUCCESS`, `FAILED`, `UNKNOWN` |
| `inputSourceIds` | Yes | Array of `string` | Items 0–unbounded |
| `resourceCount` | Yes | `integer` or `null` | See full schema |
| `reportConfiguration` | Yes | [ReportConfiguration](shapes.md#reportconfiguration) or `null` | See full schema |
| `devOpsAgentConfiguration` | Yes | [DevOpsAgentConfiguration](shapes.md#devopsagentconfiguration) or `null` | See full schema |
| `tags` | Yes | Map of `string` or `null` | See full schema |
| `kmsKeyId` | Yes | `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `refreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `provenance` | Yes | `string` | Length 1–2048 |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |
| `rawAssessmentStatus` | Yes | `string` or `null` | See full schema |
| `projectionVersion` | Yes | `integer` | Minimum 1 |
| `policyContextRefreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `reassessmentRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `rerunAssessment` | Yes | `boolean` or `null` | See full schema |
| `effectivePolicyEvidence` | Yes | [EffectivePolicyEvidence](shapes.md#effectivepolicyevidence) | See shared shape or field semantics. |

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
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
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
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "maxLength": 64
          },
          "minItems": 0,
          "maxItems": 5,
          "uniqueItems": false
        },
        {
          "type": "null"
        }
      ]
    },
    "permissionModel": {
      "anyOf": [
        {
          "$ref": "#/$defs/PermissionModelObservation"
        },
        {
          "type": "null"
        }
      ]
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
      "enum": [
        "NOT_STARTED",
        "PENDING",
        "IN_PROGRESS",
        "SUCCESS",
        "FAILED",
        "UNKNOWN"
      ]
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
      "anyOf": [
        {
          "type": "object",
          "propertyNames": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
            "pattern": "^[^\\x00-\\x1f\\x22]+$"
          },
          "additionalProperties": {
            "type": "string",
            "minLength": 0,
            "maxLength": 256,
            "pattern": "^[^\\x00-\\x1f\\x22]*$"
          },
          "maxProperties": 50
        },
        {
          "type": "null"
        }
      ]
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
    },
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "rawAssessmentStatus": {
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
    "projectionVersion": {
      "type": "integer",
      "minimum": 1
    },
    "policyContextRefreshRequired": {
      "type": "boolean"
    },
    "reassessmentRequired": {
      "type": "boolean"
    },
    "rerunAssessment": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ]
    },
    "effectivePolicyEvidence": {
      "$ref": "#/$defs/EffectivePolicyEvidence"
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
    "provenance",
    "localUpdatedAt",
    "normalizationDiagnostics",
    "rawAssessmentStatus",
    "projectionVersion",
    "policyContextRefreshRequired",
    "reassessmentRequired",
    "rerunAssessment",
    "effectivePolicyEvidence"
  ],
  "additionalProperties": false
}
```

## ResiliencePolicyEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `policyArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `name` | Yes | `string` | Length 2–60; Pattern `^[A-Za-z0-9][A-Za-z0-9_-]{1,59}$` |
| `displayName` | Yes | `string` | Length 0–256 |
| `description` | Yes | `string` | Length 0–2048 |
| `availabilitySlo` | No | [AvailabilitySlo](shapes.md#availabilityslo) or `null` | See full schema |
| `multiAz` | No | [DisasterRecoveryObservation](shapes.md#disasterrecoveryobservation) or `null` | See full schema |
| `multiRegion` | No | [DisasterRecoveryObservation](shapes.md#disasterrecoveryobservation) or `null` | See full schema |
| `dataRecovery` | No | [DataRecoveryObservation](shapes.md#datarecoveryobservation) or `null` | See full schema |
| `createdAt` | Yes | `number` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `sharingEnabled` | Yes | `boolean` or `null` | See full schema |
| `kmsKeyId` | Yes | `string` or `null` | See full schema |
| `tags` | Yes | Map of `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

```json
{
  "type": "object",
  "properties": {
    "policyArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
      "anyOf": [
        {
          "$ref": "#/$defs/AvailabilitySlo"
        },
        {
          "type": "null"
        }
      ]
    },
    "multiAz": {
      "anyOf": [
        {
          "$ref": "#/$defs/DisasterRecoveryObservation"
        },
        {
          "type": "null"
        }
      ]
    },
    "multiRegion": {
      "anyOf": [
        {
          "$ref": "#/$defs/DisasterRecoveryObservation"
        },
        {
          "type": "null"
        }
      ]
    },
    "dataRecovery": {
      "anyOf": [
        {
          "$ref": "#/$defs/DataRecoveryObservation"
        },
        {
          "type": "null"
        }
      ]
    },
    "createdAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "sharingEnabled": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ]
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
      "anyOf": [
        {
          "type": "object",
          "propertyNames": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128,
            "pattern": "^[^\\x00-\\x1f\\x22]+$"
          },
          "additionalProperties": {
            "type": "string",
            "minLength": 0,
            "maxLength": 256,
            "pattern": "^[^\\x00-\\x1f\\x22]*$"
          },
          "maxProperties": 50
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
    },
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "localUpdatedAt",
    "normalizationDiagnostics"
  ],
  "additionalProperties": false
}
```

## AssessmentEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `assessmentId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `status` | Yes | `string` | `NOT_STARTED`, `PENDING`, `IN_PROGRESS`, `SUCCESS`, `FAILED`, `UNKNOWN` |
| `startedAt` | Yes | `number` or `null` | See full schema |
| `endedAt` | Yes | `number` or `null` | See full schema |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `failureModeFindingsCount` | Yes | `integer` or `null` | See full schema |
| `achievability` | Yes | [Achievability](shapes.md#achievability) | See shared shape or field semantics. |
| `errorCode` | Yes | `string` or `null` | See full schema |
| `errorMessage` | Yes | `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `rawStatus` | Yes | `string` or `null` | See full schema |
| `assessmentCost` | Yes | `object` or `null` | See full schema |
| `assessmentStep` | Yes | `string` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

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
        "FAILED",
        "UNKNOWN"
      ]
    },
    "startedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "endedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
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
    },
    "rawStatus": {
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
    "assessmentCost": {
      "anyOf": [
        {
          "type": "object",
          "properties": {
            "amount": {
              "type": "number",
              "minimum": 0
            },
            "currency": {
              "type": "string",
              "minLength": 3,
              "maxLength": 3
            }
          },
          "required": [
            "amount",
            "currency"
          ],
          "additionalProperties": false
        },
        {
          "type": "null"
        }
      ]
    },
    "assessmentStep": {
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
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "rawStatus",
    "assessmentCost",
    "assessmentStep",
    "normalizationDiagnostics"
  ],
  "additionalProperties": false
}
```

## FindingEntity

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `findingId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `name` | Yes | `string` | Length 1–2048 |
| `description` | Yes | `string` | Length 0–2048 |
| `reasoning` | Yes | `string` | Length 0–2048 |
| `severity` | Yes | `string` | `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN` |
| `status` | Yes | `string` | `OPEN`, `RESOLVED`, `IRRELEVANT`, `UNKNOWN` |
| `failureCategory` | Yes | `string` | Length 1–2048 |
| `policyComponent` | Yes | `string` | Length 1–2048 |
| `serviceFunctions` | Yes | Array of `string` | Items 0–1000 |
| `comment` | Yes | `string` | Length 0–2048 |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `detailObservedAt` | Yes | `number` or `null` | See full schema |
| `observationId` | Yes | `string` or `null` | See full schema |
| `captureId` | Yes | `string` or `null` | See full schema |
| `representation` | Yes | `string` | `DETAIL`, `SUMMARY`, `UNKNOWN` |
| `recommendationIds` | Yes | Array of `string` or `null` | See full schema |
| `verification` | Yes | `string` | Length 1–2048 |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `rawSeverity` | Yes | `string` or `null` | See full schema |
| `rawStatus` | Yes | `string` or `null` | See full schema |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `recommendationPresence` | Yes | `string` | `PRESENT`, `EMPTY`, `OMITTED`, `NULL`, `NOT_FETCHED`, `UNKNOWN` |
| `recommendationFields` | Yes | `object` or `null` | See full schema |
| `findingCapture` | Yes | [FindingCapture](shapes.md#findingcapture) or `null` | See full schema |
| `findingObservation` | Yes | [FindingObservation](shapes.md#findingobservation) or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

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
        "LOW",
        "UNKNOWN"
      ]
    },
    "status": {
      "type": "string",
      "enum": [
        "OPEN",
        "RESOLVED",
        "IRRELEVANT",
        "UNKNOWN"
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
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "detailObservedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
    "captureId": {
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
    "representation": {
      "type": "string",
      "enum": [
        "DETAIL",
        "SUMMARY",
        "UNKNOWN"
      ]
    },
    "recommendationIds": {
      "anyOf": [
        {
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
        {
          "type": "null"
        }
      ]
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
    },
    "rawSeverity": {
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
    "rawStatus": {
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
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "recommendationPresence": {
      "type": "string",
      "enum": [
        "PRESENT",
        "EMPTY",
        "OMITTED",
        "NULL",
        "NOT_FETCHED",
        "UNKNOWN"
      ]
    },
    "recommendationFields": {
      "anyOf": [
        {
          "type": "object",
          "properties": {
            "infrastructureAndCodeRecommendations": {
              "type": "string",
              "enum": [
                "PRESENT",
                "EMPTY",
                "OMITTED",
                "NULL",
                "NOT_FETCHED",
                "UNKNOWN"
              ]
            },
            "observabilityRecommendations": {
              "type": "string",
              "enum": [
                "PRESENT",
                "EMPTY",
                "OMITTED",
                "NULL",
                "NOT_FETCHED",
                "UNKNOWN"
              ]
            },
            "testingRecommendations": {
              "type": "string",
              "enum": [
                "PRESENT",
                "EMPTY",
                "OMITTED",
                "NULL",
                "NOT_FETCHED",
                "UNKNOWN"
              ]
            }
          },
          "required": [
            "infrastructureAndCodeRecommendations",
            "observabilityRecommendations",
            "testingRecommendations"
          ],
          "additionalProperties": false
        },
        {
          "type": "null"
        }
      ]
    },
    "findingCapture": {
      "anyOf": [
        {
          "$ref": "#/$defs/FindingCapture"
        },
        {
          "type": "null"
        }
      ]
    },
    "findingObservation": {
      "anyOf": [
        {
          "$ref": "#/$defs/FindingObservation"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "rawSeverity",
    "rawStatus",
    "localUpdatedAt",
    "recommendationPresence",
    "recommendationFields",
    "findingCapture",
    "findingObservation",
    "normalizationDiagnostics"
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
| `estimatedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
| `updatedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `findingId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `findingObservationId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `category` | Yes | `string` | `INFRASTRUCTURE_AND_CODE`, `OBSERVABILITY`, `TESTING` |
| `sourceArrayOrdinal` | Yes | `integer` | Minimum 0 |
| `suggestedChanges` | Yes | Array of `string` | Items 0–1000 |
| `capturedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `dependencyId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `dependencyName` | Yes | `string` | Length 1–2048 |
| `dnsName` | Yes | `string` or `null` | See full schema |
| `location` | Yes | `string` | Length 1–2048 |
| `criticality` | Yes | `string` | `HARD`, `SOFT`, `UNKNOWN` |
| `comment` | Yes | `string` | Length 0–2048 |
| `provider` | Yes | `string` | Length 1–2048 |
| `sourceRegions` | Yes | Array of `string` | Items 0–1000 |
| `lastDetectedTime` | Yes | `number` or `null` | See full schema |
| `updatedAt` | Yes | `number` or `null` | See full schema |
| `governance` | Yes | `object` | Unknown members rejected |
| `resolvedServiceArn` | Yes | `string` or `null` | See full schema |
| `version` | Yes | `integer` | Minimum 1 |
| `provenance` | Yes | `string` | Length 1–2048 |
| `localUpdatedAt` | Yes | `number` or `null` | See full schema |
| `rawCriticality` | Yes | `string` or `null` | See full schema |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "minLength": 31,
          "maxLength": 2048,
          "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
    },
    "localUpdatedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "rawCriticality": {
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
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "localUpdatedAt",
    "rawCriticality",
    "normalizationDiagnostics"
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
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `topologyId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `capturedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `captureStartedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `captureEndedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `sourceObservedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
    },
    "captureStartedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
    },
    "captureEndedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
    },
    "sourceObservedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
| `occurredAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `receivedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `linkage` | Yes | `string` | `ASSERTED`, `INFERRED` |
| `refreshStatus` | Yes | `string` | Length 1–2048 |
| `sequence` | Yes | `integer` | Minimum 1 |
| `mock` | Yes | `boolean` | See shared shape or field semantics. |
| `producerPrincipalId` | Yes | `string` or `null` | See full schema |
| `trustedSource` | Yes | `boolean` | See shared shape or field semantics. |
| `subjects` | Yes | Array of [EventSubject](shapes.md#eventsubject) | Items 0–unbounded |
| `rawEvent` | Yes | `object` or `null` | See full schema |
| `correlationIds` | Yes | Array of `string` | Items 0–32 |

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
          "minLength": 31,
          "maxLength": 2048,
          "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
    },
    "receivedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
    },
    "subjects": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/EventSubject"
      },
      "minItems": 0,
      "uniqueItems": false
    },
    "rawEvent": {
      "anyOf": [
        {
          "type": "object",
          "additionalProperties": true
        },
        {
          "type": "null"
        }
      ]
    },
    "correlationIds": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 1,
        "maxLength": 256
      },
      "minItems": 0,
      "maxItems": 32,
      "uniqueItems": false
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
    "trustedSource",
    "subjects",
    "rawEvent",
    "correlationIds"
  ],
  "additionalProperties": false
}
```

## ServiceStatus

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `health` | Yes | [HealthProjection](shapes.md#healthprojection) | See shared shape or field semantics. |
| `posture` | Yes | [PostureProjection](shapes.md#postureprojection) | See shared shape or field semantics. |
| `assessmentStatus` | Yes | `string` | `NOT_STARTED`, `PENDING`, `IN_PROGRESS`, `SUCCESS`, `FAILED`, `UNKNOWN` |
| `dependencyDiscovery` | Yes | [DependencyDiscoveryConfig](shapes.md#dependencydiscoveryconfig) | See shared shape or field semantics. |
| `resourceDiscovery` | Yes | [ResourceDiscovery](shapes.md#resourcediscovery) | See shared shape or field semantics. |
| `needsAttention` | Yes | `boolean` | See shared shape or field semantics. |
| `openFindingsCount` | Yes | `integer` or `null` | See full schema |
| `computedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `version` | Yes | `integer` | Minimum 1 |
| `refreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `provenance` | Yes | `string` | Length 1–2048 |
| `rawAssessmentStatus` | Yes | `string` or `null` | See full schema |
| `projectionVersion` | Yes | `integer` | Minimum 1 |
| `policyContextRefreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `reassessmentRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `rerunAssessment` | Yes | `boolean` or `null` | See full schema |
| `effectivePolicyEvidence` | Yes | [EffectivePolicyEvidence](shapes.md#effectivepolicyevidence) | See shared shape or field semantics. |
| `findingCoverage` | Yes | [FindingCoverage](shapes.md#findingcoverage) | See shared shape or field semantics. |
| `assessmentCoverage` | Yes | [AssessmentCoverage](shapes.md#assessmentcoverage) | See shared shape or field semantics. |
| `attentionReasons` | Yes | Array of [AttentionReason](shapes.md#attentionreason) | Items 0–1000 |
| `selectedObservations` | Yes | [SelectedObservations](shapes.md#selectedobservations) | See shared shape or field semantics. |
| `normalizationDiagnostics` | Yes | Array of [NormalizationDiagnostic](shapes.md#normalizationdiagnostic) | Items 0–1000 |

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
    "health": {
      "$ref": "#/$defs/HealthProjection"
    },
    "posture": {
      "$ref": "#/$defs/PostureProjection"
    },
    "assessmentStatus": {
      "type": "string",
      "enum": [
        "NOT_STARTED",
        "PENDING",
        "IN_PROGRESS",
        "SUCCESS",
        "FAILED",
        "UNKNOWN"
      ]
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
    "computedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
    },
    "rawAssessmentStatus": {
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
    "projectionVersion": {
      "type": "integer",
      "minimum": 1
    },
    "policyContextRefreshRequired": {
      "type": "boolean"
    },
    "reassessmentRequired": {
      "type": "boolean"
    },
    "rerunAssessment": {
      "anyOf": [
        {
          "type": "boolean"
        },
        {
          "type": "null"
        }
      ]
    },
    "effectivePolicyEvidence": {
      "$ref": "#/$defs/EffectivePolicyEvidence"
    },
    "findingCoverage": {
      "$ref": "#/$defs/FindingCoverage"
    },
    "assessmentCoverage": {
      "$ref": "#/$defs/AssessmentCoverage"
    },
    "attentionReasons": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/AttentionReason"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "selectedObservations": {
      "$ref": "#/$defs/SelectedObservations"
    },
    "normalizationDiagnostics": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/NormalizationDiagnostic"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance",
    "rawAssessmentStatus",
    "projectionVersion",
    "policyContextRefreshRequired",
    "reassessmentRequired",
    "rerunAssessment",
    "effectivePolicyEvidence",
    "findingCoverage",
    "assessmentCoverage",
    "attentionReasons",
    "selectedObservations",
    "normalizationDiagnostics"
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
| `openFindingCount` | Yes | `integer` or `null` | See full schema |
| `contributorServiceArns` | Yes | Array of `string` | Items 0–unbounded |
| `computedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `aggregationRule` | Yes | `string` | Length 1–2048 |
| `interpretation` | Yes | `string` | Length 1–2048 |
| `projectionVersion` | Yes | `integer` | Minimum 1 |
| `currentAssessedCount` | Yes | `integer` | Minimum 0 |
| `lastKnownAssessedCount` | Yes | `integer` | Minimum 0 |
| `currentAssessmentCoverage` | Yes | `number` or `null` | See full schema |
| `lastKnownAssessmentCoverage` | Yes | `number` or `null` | See full schema |
| `partialAssessmentCount` | Yes | `integer` | Minimum 0 |
| `inaccessibleAssessmentCount` | Yes | `integer` | Minimum 0 |
| `unassessedCount` | Yes | `integer` | Minimum 0 |
| `observedOpenFindingCount` | Yes | `integer` | Minimum 0 |
| `incompleteFindingServiceCount` | Yes | `integer` | Minimum 0 |
| `attentionByDimension` | Yes | Map of `integer` | See shared shape or field semantics. |
| `membershipContext` | Yes | Array of `object` | Items 0–unbounded |
| `evidenceRuleVersion` | Yes | `string` | Length 1–2048 |

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
    "contributorServiceArns": {
      "type": "array",
      "items": {
        "type": "string",
        "minLength": 31,
        "maxLength": 2048,
        "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
      },
      "minItems": 0,
      "uniqueItems": false
    },
    "computedAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
    },
    "projectionVersion": {
      "type": "integer",
      "minimum": 1
    },
    "currentAssessedCount": {
      "type": "integer",
      "minimum": 0
    },
    "lastKnownAssessedCount": {
      "type": "integer",
      "minimum": 0
    },
    "currentAssessmentCoverage": {
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
    "lastKnownAssessmentCoverage": {
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
    "partialAssessmentCount": {
      "type": "integer",
      "minimum": 0
    },
    "inaccessibleAssessmentCount": {
      "type": "integer",
      "minimum": 0
    },
    "unassessedCount": {
      "type": "integer",
      "minimum": 0
    },
    "observedOpenFindingCount": {
      "type": "integer",
      "minimum": 0
    },
    "incompleteFindingServiceCount": {
      "type": "integer",
      "minimum": 0
    },
    "attentionByDimension": {
      "type": "object",
      "additionalProperties": {
        "type": "integer",
        "minimum": 0
      }
    },
    "membershipContext": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "serviceArn": {
            "type": "string",
            "minLength": 31,
            "maxLength": 2048,
            "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
          },
          "associatedSystems": {
            "type": "array",
            "items": {
              "$ref": "#/$defs/AssociatedSystem"
            },
            "minItems": 0,
            "maxItems": 20,
            "uniqueItems": false
          }
        },
        "required": [
          "serviceArn",
          "associatedSystems"
        ],
        "additionalProperties": false
      },
      "minItems": 0,
      "uniqueItems": false
    },
    "evidenceRuleVersion": {
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
    "interpretation",
    "projectionVersion",
    "currentAssessedCount",
    "lastKnownAssessedCount",
    "currentAssessmentCoverage",
    "lastKnownAssessmentCoverage",
    "partialAssessmentCount",
    "inaccessibleAssessmentCount",
    "unassessedCount",
    "observedOpenFindingCount",
    "incompleteFindingServiceCount",
    "attentionByDimension",
    "membershipContext",
    "evidenceRuleVersion"
  ],
  "additionalProperties": false
}
```

## PageSnapshot

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `snapshotId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `createdAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
| `expiresAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
    },
    "expiresAt": {
      "type": "number",
      "minimum": 0,
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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
| `deletedAt` | Yes | `number` | Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.; Minimum 0; Maximum 253402300799; Runtime precision assertion: `milliseconds` |
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
      "maximum": 253402300799,
      "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
      "x-precision": "milliseconds"
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

## NormalizationDiagnostic

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `path` | Yes | `string` | Length 1–2048 |
| `rawValue` | Yes | `string` or `null` | See full schema |
| `normalizedValue` | Yes | `string` or `null` | See full schema |
| `reason` | Yes | `string` | `MISSING`, `UNKNOWN_ENUM`, `INVALID_VALUE` |

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "rawValue": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ]
    },
    "normalizedValue": {
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
    "reason": {
      "type": "string",
      "enum": [
        "MISSING",
        "UNKNOWN_ENUM",
        "INVALID_VALUE"
      ]
    }
  },
  "required": [
    "path",
    "rawValue",
    "normalizedValue",
    "reason"
  ],
  "additionalProperties": false
}
```

## PermissionModelObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `invokerRoleName` | Yes | `string` or `null` | See full schema |
| `crossAccountRoles` | Yes | Array of `object` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "invokerRoleName": {
      "anyOf": [
        {
          "type": "string",
          "minLength": 0,
          "maxLength": 64
        },
        {
          "type": "null"
        }
      ]
    },
    "crossAccountRoles": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "crossAccountRoleArn": {
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
              "externalId": {
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
              "crossAccountRoleArn",
              "externalId"
            ],
            "additionalProperties": false
          },
          "minItems": 0,
          "maxItems": 5,
          "uniqueItems": false
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "invokerRoleName",
    "crossAccountRoles"
  ],
  "additionalProperties": false
}
```

## DisasterRecoveryObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `rtoInMinutes` | Yes | `integer` or `null` | See full schema |
| `rpoInMinutes` | Yes | `integer` or `null` | See full schema |
| `disasterRecoveryApproach` | Yes | `string` or `null` | See full schema |
| `rawDisasterRecoveryApproach` | Yes | `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "rtoInMinutes": {
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
    "rpoInMinutes": {
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
    "disasterRecoveryApproach": {
      "anyOf": [
        {
          "type": "string",
          "enum": [
            "ACTIVE_ACTIVE",
            "HOT_STANDBY",
            "WARM_STANDBY",
            "PILOT_LIGHT",
            "BACKUP_AND_RESTORE",
            "UNKNOWN"
          ]
        },
        {
          "type": "null"
        }
      ]
    },
    "rawDisasterRecoveryApproach": {
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
    "rtoInMinutes",
    "rpoInMinutes",
    "disasterRecoveryApproach",
    "rawDisasterRecoveryApproach"
  ],
  "additionalProperties": false
}
```

## DataRecoveryObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `timeBetweenBackupsInMinutes` | Yes | `integer` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "timeBetweenBackupsInMinutes": {
      "anyOf": [
        {
          "type": "integer",
          "minimum": 0
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "timeBetweenBackupsInMinutes"
  ],
  "additionalProperties": false
}
```

## AttentionReason

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `code` | Yes | `string` | Length 1–128 |
| `dimension` | Yes | `string` | Length 1–64 |
| `severity` | Yes | `string` | `INFO`, `WARNING`, `ERROR` |
| `message` | Yes | `string` | Length 0–2048 |
| `observedAt` | Yes | `number` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "code": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128
    },
    "dimension": {
      "type": "string",
      "minLength": 1,
      "maxLength": 64
    },
    "severity": {
      "type": "string",
      "enum": [
        "INFO",
        "WARNING",
        "ERROR"
      ]
    },
    "message": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "code",
    "dimension",
    "severity",
    "message",
    "observedAt"
  ],
  "additionalProperties": false
}
```

## AssessmentCoverage

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `status` | Yes | `string` | `CURRENT`, `STALE`, `PARTIAL`, `UNASSESSED`, `INACCESSIBLE` |
| `lastKnown` | Yes | `boolean` | See shared shape or field semantics. |
| `current` | Yes | `boolean` | See shared shape or field semantics. |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `stale` | Yes | `boolean` | See shared shape or field semantics. |
| `partial` | Yes | `boolean` | See shared shape or field semantics. |
| `inaccessible` | Yes | `boolean` | See shared shape or field semantics. |
| `contextRefreshRequired` | Yes | `boolean` | See shared shape or field semantics. |
| `policyContextKnown` | Yes | `boolean` | See shared shape or field semantics. |
| `expectedComponents` | Yes | Array of `string` or `null` | See full schema |
| `ruleVersion` | Yes | `string` | Length 1–2048 |
| `reason` | Yes | `string` | Length 0–2048 |

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "CURRENT",
        "STALE",
        "PARTIAL",
        "UNASSESSED",
        "INACCESSIBLE"
      ]
    },
    "lastKnown": {
      "type": "boolean"
    },
    "current": {
      "type": "boolean"
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "stale": {
      "type": "boolean"
    },
    "partial": {
      "type": "boolean"
    },
    "inaccessible": {
      "type": "boolean"
    },
    "contextRefreshRequired": {
      "type": "boolean"
    },
    "policyContextKnown": {
      "type": "boolean"
    },
    "expectedComponents": {
      "anyOf": [
        {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
          },
          "minItems": 0,
          "maxItems": 1000,
          "uniqueItems": false
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
    "reason": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    }
  },
  "required": [
    "status",
    "lastKnown",
    "current",
    "observedAt",
    "stale",
    "partial",
    "inaccessible",
    "contextRefreshRequired",
    "policyContextKnown",
    "expectedComponents",
    "ruleVersion",
    "reason"
  ],
  "additionalProperties": false
}
```

## EffectiveTarget

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `metric` | Yes | `string` | Length 1–128 |
| `label` | Yes | `string` | Length 0–256 |
| `value` | Yes | `number` or `string` or `null` | See full schema |
| `unit` | Yes | `string` | Length 0–64 |
| `policyName` | Yes | `string` or `null` | See full schema |
| `ownership` | Yes | `string` | `SELF`, `CROSS_ACCOUNT`, `UNKNOWN` |
| `rawOwnership` | Yes | `string` or `null` | See full schema |
| `assignment` | Yes | `string` | `DIRECT`, `INHERITED`, `UNKNOWN` |
| `systemArn` | Yes | `string` or `null` | See full schema |
| `userJourneyId` | Yes | `string` or `null` | See full schema |
| `resolvedPolicyArn` | Yes | `string` or `null` | See full schema |
| `resolutionEvidence` | Yes | `string` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "metric": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128
    },
    "label": {
      "type": "string",
      "minLength": 0,
      "maxLength": 256
    },
    "value": {
      "anyOf": [
        {
          "type": "number"
        },
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
    "unit": {
      "type": "string",
      "minLength": 0,
      "maxLength": 64
    },
    "policyName": {
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
    "ownership": {
      "type": "string",
      "enum": [
        "SELF",
        "CROSS_ACCOUNT",
        "UNKNOWN"
      ]
    },
    "rawOwnership": {
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
    "assignment": {
      "type": "string",
      "enum": [
        "DIRECT",
        "INHERITED",
        "UNKNOWN"
      ]
    },
    "systemArn": {
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
    "userJourneyId": {
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
    "resolvedPolicyArn": {
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
    "resolutionEvidence": {
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
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "metric",
    "label",
    "value",
    "unit",
    "policyName",
    "ownership",
    "rawOwnership",
    "assignment",
    "systemArn",
    "userJourneyId",
    "resolvedPolicyArn",
    "resolutionEvidence",
    "provenance"
  ],
  "additionalProperties": false
}
```

## EffectiveTargetObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `effectiveTargetObservationId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `targets` | Yes | Array of [EffectiveTarget](shapes.md#effectivetarget) | Items 0–1000 |
| `evaluatedProviderRevision` | Yes | `string` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "effectiveTargetObservationId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "targets": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/EffectiveTarget"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
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
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "effectiveTargetObservationId",
    "serviceArn",
    "observedAt",
    "targets",
    "evaluatedProviderRevision",
    "provenance"
  ],
  "additionalProperties": false
}
```

## CapturedAssociation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `systemArn` | Yes | `string` or `null` | See full schema |
| `userJourneyIds` | Yes | Array of `string` | Items 0–1000 |
| `localSystemReference` | Yes | `string` | Length 1–2048 |
| `identityResolution` | Yes | `string` | `LOCAL_REFERENCE`, `UNRESOLVED` |

```json
{
  "type": "object",
  "properties": {
    "systemArn": {
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
    "userJourneyIds": {
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
    "localSystemReference": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "identityResolution": {
      "type": "string",
      "enum": [
        "LOCAL_REFERENCE",
        "UNRESOLVED"
      ]
    }
  },
  "required": [
    "systemArn",
    "userJourneyIds",
    "localSystemReference",
    "identityResolution"
  ],
  "additionalProperties": false
}
```

## PolicyAssignmentEvidence

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `policyArn` | Yes | `string` or `null` | See full schema |
| `assignment` | Yes | `string` | `DIRECT`, `INHERITED`, `UNKNOWN` |
| `systemArn` | Yes | `string` or `null` | See full schema |
| `userJourneyId` | Yes | `string` or `null` | See full schema |
| `localPolicyReference` | Yes | `string` or `null` | See full schema |
| `identityResolution` | Yes | `string` | `LOCAL_REFERENCE`, `UNRESOLVED` |

```json
{
  "type": "object",
  "properties": {
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
    "assignment": {
      "type": "string",
      "enum": [
        "DIRECT",
        "INHERITED",
        "UNKNOWN"
      ]
    },
    "systemArn": {
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
    "userJourneyId": {
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
    "localPolicyReference": {
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
    "identityResolution": {
      "type": "string",
      "enum": [
        "LOCAL_REFERENCE",
        "UNRESOLVED"
      ]
    }
  },
  "required": [
    "policyArn",
    "assignment",
    "systemArn",
    "userJourneyId",
    "localPolicyReference",
    "identityResolution"
  ],
  "additionalProperties": false
}
```

## PolicyContextCapture

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `policyContextCaptureId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `associations` | Yes | Array of [CapturedAssociation](shapes.md#capturedassociation) | Items 0–1000 |
| `applicablePolicies` | Yes | Array of [PolicyAssignmentEvidence](shapes.md#policyassignmentevidence) | Items 0–1000 |
| `effectiveTargetObservationId` | Yes | `string` or `null` | See full schema |
| `assessedProviderRevision` | Yes | `string` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |

```json
{
  "type": "object",
  "properties": {
    "policyContextCaptureId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "associations": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/CapturedAssociation"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "applicablePolicies": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/PolicyAssignmentEvidence"
      },
      "minItems": 0,
      "maxItems": 1000,
      "uniqueItems": false
    },
    "effectiveTargetObservationId": {
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
    "assessedProviderRevision": {
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
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    }
  },
  "required": [
    "policyContextCaptureId",
    "serviceArn",
    "observedAt",
    "associations",
    "applicablePolicies",
    "effectiveTargetObservationId",
    "assessedProviderRevision",
    "provenance"
  ],
  "additionalProperties": false
}
```

## EffectivePolicyEvidence

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `effectiveTargetObservation` | Yes | [EffectiveTargetObservation](shapes.md#effectivetargetobservation) or `null` | See full schema |
| `policyContextCapture` | Yes | [PolicyContextCapture](shapes.md#policycontextcapture) or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "effectiveTargetObservation": {
      "anyOf": [
        {
          "$ref": "#/$defs/EffectiveTargetObservation"
        },
        {
          "type": "null"
        }
      ]
    },
    "policyContextCapture": {
      "anyOf": [
        {
          "$ref": "#/$defs/PolicyContextCapture"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "effectiveTargetObservation",
    "policyContextCapture"
  ],
  "additionalProperties": false
}
```

## FindingCapture

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `captureId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `captureStartedAt` | Yes | `number` or `null` | See full schema |
| `captureEndedAt` | Yes | `number` or `null` | See full schema |
| `collectionStatus` | Yes | `string` | `COMPLETE`, `PARTIAL`, `FAILED`, `UNKNOWN` |
| `listCoverage` | Yes | `object` | Unknown members rejected |
| `detailCoverage` | Yes | `object` | Unknown members rejected |
| `relatedAssessmentId` | Yes | `string` or `null` | See full schema |
| `correlationBasis` | Yes | `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "captureId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "captureStartedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "captureEndedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "collectionStatus": {
      "type": "string",
      "enum": [
        "COMPLETE",
        "PARTIAL",
        "FAILED",
        "UNKNOWN"
      ]
    },
    "listCoverage": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": [
            "COMPLETE",
            "PARTIAL",
            "FAILED",
            "UNKNOWN"
          ]
        },
        "pages": {
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
        "filters": {
          "type": "object",
          "additionalProperties": true
        },
        "findingsReturned": {
          "anyOf": [
            {
              "type": "integer",
              "minimum": 0
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "status",
        "pages",
        "filters",
        "findingsReturned"
      ],
      "additionalProperties": false
    },
    "detailCoverage": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "enum": [
            "COMPLETE",
            "PARTIAL",
            "FAILED",
            "UNKNOWN"
          ]
        },
        "requested": {
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
        "hydrated": {
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
        "failed": {
          "anyOf": [
            {
              "type": "integer",
              "minimum": 0
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "required": [
        "status",
        "requested",
        "hydrated",
        "failed"
      ],
      "additionalProperties": false
    },
    "relatedAssessmentId": {
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
    "correlationBasis": {
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
    "captureId",
    "serviceArn",
    "captureStartedAt",
    "captureEndedAt",
    "collectionStatus",
    "listCoverage",
    "detailCoverage",
    "relatedAssessmentId",
    "correlationBasis"
  ],
  "additionalProperties": false
}
```

## FindingObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `observationId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `captureId` | Yes | `string` or `null` | See full schema |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `findingId` | Yes | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `representation` | Yes | `string` | `DETAIL`, `SUMMARY`, `UNKNOWN` |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `name` | Yes | `string` or `null` | See full schema |
| `severity` | Yes | `string` | `HIGH`, `MEDIUM`, `LOW`, `UNKNOWN` |
| `status` | Yes | `string` | `OPEN`, `RESOLVED`, `IRRELEVANT`, `UNKNOWN` |
| `recommendationPresence` | Yes | `string` | `PRESENT`, `EMPTY`, `OMITTED`, `NULL`, `NOT_FETCHED`, `UNKNOWN` |
| `recommendationFields` | Yes | `object` or `null` | See full schema |
| `recommendationIds` | Yes | Array of `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "observationId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "captureId": {
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
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "findingId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "representation": {
      "type": "string",
      "enum": [
        "DETAIL",
        "SUMMARY",
        "UNKNOWN"
      ]
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "name": {
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
    "severity": {
      "type": "string",
      "enum": [
        "HIGH",
        "MEDIUM",
        "LOW",
        "UNKNOWN"
      ]
    },
    "status": {
      "type": "string",
      "enum": [
        "OPEN",
        "RESOLVED",
        "IRRELEVANT",
        "UNKNOWN"
      ]
    },
    "recommendationPresence": {
      "type": "string",
      "enum": [
        "PRESENT",
        "EMPTY",
        "OMITTED",
        "NULL",
        "NOT_FETCHED",
        "UNKNOWN"
      ]
    },
    "recommendationFields": {
      "anyOf": [
        {
          "type": "object",
          "properties": {
            "infrastructureAndCodeRecommendations": {
              "type": "string",
              "enum": [
                "PRESENT",
                "EMPTY",
                "OMITTED",
                "NULL",
                "NOT_FETCHED",
                "UNKNOWN"
              ]
            },
            "observabilityRecommendations": {
              "type": "string",
              "enum": [
                "PRESENT",
                "EMPTY",
                "OMITTED",
                "NULL",
                "NOT_FETCHED",
                "UNKNOWN"
              ]
            },
            "testingRecommendations": {
              "type": "string",
              "enum": [
                "PRESENT",
                "EMPTY",
                "OMITTED",
                "NULL",
                "NOT_FETCHED",
                "UNKNOWN"
              ]
            }
          },
          "required": [
            "infrastructureAndCodeRecommendations",
            "observabilityRecommendations",
            "testingRecommendations"
          ],
          "additionalProperties": false
        },
        {
          "type": "null"
        }
      ]
    },
    "recommendationIds": {
      "anyOf": [
        {
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
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "observationId",
    "captureId",
    "serviceArn",
    "findingId",
    "representation",
    "observedAt",
    "name",
    "severity",
    "status",
    "recommendationPresence",
    "recommendationFields",
    "recommendationIds"
  ],
  "additionalProperties": false
}
```

## FindingCoverage

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `status` | Yes | `string` | `COMPLETE`, `PARTIAL`, `STALE`, `UNASSESSED`, `UNKNOWN` |
| `observedCount` | Yes | `integer` | Minimum 0 |
| `observedOpenCount` | Yes | `integer` | Minimum 0 |
| `unknownStatusCount` | Yes | `integer` | Minimum 0 |
| `exactOpenCount` | Yes | `integer` or `null` | See full schema |
| `countMeaning` | Yes | `string` | `COMPLETE_CAPTURE`, `OBSERVED_SUBSET`, `STALE_CAPTURE`, `NO_CAPTURE` |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `latestCapture` | Yes | [FindingCapture](shapes.md#findingcapture) or `null` | See full schema |
| `stale` | Yes | `boolean` | See shared shape or field semantics. |
| `reason` | Yes | `string` | Length 0–2048 |

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string",
      "enum": [
        "COMPLETE",
        "PARTIAL",
        "STALE",
        "UNASSESSED",
        "UNKNOWN"
      ]
    },
    "observedCount": {
      "type": "integer",
      "minimum": 0
    },
    "observedOpenCount": {
      "type": "integer",
      "minimum": 0
    },
    "unknownStatusCount": {
      "type": "integer",
      "minimum": 0
    },
    "exactOpenCount": {
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
    "countMeaning": {
      "type": "string",
      "enum": [
        "COMPLETE_CAPTURE",
        "OBSERVED_SUBSET",
        "STALE_CAPTURE",
        "NO_CAPTURE"
      ]
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "latestCapture": {
      "anyOf": [
        {
          "$ref": "#/$defs/FindingCapture"
        },
        {
          "type": "null"
        }
      ]
    },
    "stale": {
      "type": "boolean"
    },
    "reason": {
      "type": "string",
      "minLength": 0,
      "maxLength": 2048
    }
  },
  "required": [
    "status",
    "observedCount",
    "observedOpenCount",
    "unknownStatusCount",
    "exactOpenCount",
    "countMeaning",
    "observedAt",
    "latestCapture",
    "stale",
    "reason"
  ],
  "additionalProperties": false
}
```

## HealthObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `observationId` | Yes | `string` or `null` | See full schema |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `state` | Yes | `string` | `HEALTHY`, `DEGRADED`, `UNAVAILABLE`, `UNKNOWN` |
| `rawState` | Yes | `string` or `null` | See full schema |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `expiresAt` | Yes | `number` or `null` | See full schema |
| `source` | Yes | `string` or `null` | See full schema |
| `reason` | Yes | `string` or `null` | See full schema |
| `ruleVersion` | Yes | `string` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |
| `latencyMs` | Yes | `number` or `null` | See full schema |
| `errorRate` | Yes | `number` or `null` | See full schema |
| `windowMinutes` | Yes | `number` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
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
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
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
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
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
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "source": {
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
    "reason": {
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
    "ruleVersion": {
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
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
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
    "observationId",
    "serviceArn",
    "state",
    "rawState",
    "observedAt",
    "expiresAt",
    "source",
    "reason",
    "ruleVersion",
    "provenance",
    "latencyMs",
    "errorRate",
    "windowMinutes"
  ],
  "additionalProperties": false
}
```

## PostureObservation

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `observationId` | Yes | `string` or `null` | See full schema |
| `serviceArn` | Yes | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `state` | Yes | `string` | `ACHIEVABLE`, `NOT_ACHIEVABLE`, `UNKNOWN` |
| `rawState` | Yes | `string` or `null` | See full schema |
| `achievability` | Yes | [Achievability](shapes.md#achievability) | See shared shape or field semantics. |
| `observedAt` | Yes | `number` or `null` | See full schema |
| `source` | Yes | `string` or `null` | See full schema |
| `ruleVersion` | Yes | `string` or `null` | See full schema |
| `provenance` | Yes | `string` | Length 1–2048 |
| `assessmentId` | Yes | `string` or `null` | See full schema |
| `assessmentLinkage` | Yes | `string` | Length 1–2048 |
| `assessmentCorrelationBasis` | Yes | `string` or `null` | See full schema |
| `policyContextCaptureId` | Yes | `string` or `null` | See full schema |
| `evaluatedProviderRevision` | Yes | `string` or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
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
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "state": {
      "type": "string",
      "enum": [
        "ACHIEVABLE",
        "NOT_ACHIEVABLE",
        "UNKNOWN"
      ]
    },
    "rawState": {
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
    "achievability": {
      "$ref": "#/$defs/Achievability"
    },
    "observedAt": {
      "anyOf": [
        {
          "type": "number",
          "minimum": 0,
          "maximum": 253402300799,
          "description": "Unix epoch seconds with at most millisecond precision. Sub-millisecond inputs are rejected before ordering or storage.",
          "x-precision": "milliseconds"
        },
        {
          "type": "null"
        }
      ]
    },
    "source": {
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
    "ruleVersion": {
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
    "provenance": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
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
    "assessmentLinkage": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "assessmentCorrelationBasis": {
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
    }
  },
  "required": [
    "observationId",
    "serviceArn",
    "state",
    "rawState",
    "achievability",
    "observedAt",
    "source",
    "ruleVersion",
    "provenance",
    "assessmentId",
    "assessmentLinkage",
    "assessmentCorrelationBasis",
    "policyContextCaptureId",
    "evaluatedProviderRevision"
  ],
  "additionalProperties": false
}
```

## SelectedObservations

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `health` | Yes | [HealthObservation](shapes.md#healthobservation) or `null` | See full schema |
| `posture` | Yes | [PostureObservation](shapes.md#postureobservation) or `null` | See full schema |

```json
{
  "type": "object",
  "properties": {
    "health": {
      "anyOf": [
        {
          "$ref": "#/$defs/HealthObservation"
        },
        {
          "type": "null"
        }
      ]
    },
    "posture": {
      "anyOf": [
        {
          "$ref": "#/$defs/PostureObservation"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "health",
    "posture"
  ],
  "additionalProperties": false
}
```

## EventSubject

| Member | Required | Type | Constraints |
| --- | --- | --- | --- |
| `entityType` | Yes | `string` | `System`, `UserJourney`, `Service`, `Policy`, `Assessment`, `Finding`, `InputSource`, `Dependency`, `Recommendation`, `TopologySnapshot`, `UNKNOWN` |
| `entityId` | Yes | `string` | Length 1–2048 |
| `serviceArn` | No | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `systemArn` | No | `string` | Length 31–2048; Pattern `^arn:(aws\|aws-cn\|aws-iso\|aws-iso-[a-z]\|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system\|service\|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$` |
| `findingId` | No | `string` | Length 1–256; Pattern `^[A-Za-z0-9][A-Za-z0-9._:-]*$` |
| `relationship` | Yes | `string` | `SUBJECT`, `RELATED` |

```json
{
  "type": "object",
  "properties": {
    "entityType": {
      "type": "string",
      "enum": [
        "System",
        "UserJourney",
        "Service",
        "Policy",
        "Assessment",
        "Finding",
        "InputSource",
        "Dependency",
        "Recommendation",
        "TopologySnapshot",
        "UNKNOWN"
      ]
    },
    "entityId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "serviceArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "systemArn": {
      "type": "string",
      "minLength": 31,
      "maxLength": 2048,
      "pattern": "^arn:(aws|aws-cn|aws-iso|aws-iso-[a-z]|aws-us-gov):resiliencehub:[a-z0-9-]+:[0-9]{12}:(system|service|policy)/[A-Za-z0-9][A-Za-z0-9:_/+.-]{0,1023}$"
    },
    "findingId": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256,
      "pattern": "^[A-Za-z0-9][A-Za-z0-9._:-]*$"
    },
    "relationship": {
      "type": "string",
      "enum": [
        "SUBJECT",
        "RELATED"
      ]
    }
  },
  "required": [
    "entityType",
    "entityId",
    "relationship"
  ],
  "additionalProperties": false
}
```
