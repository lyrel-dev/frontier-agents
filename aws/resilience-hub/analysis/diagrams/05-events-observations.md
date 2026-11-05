---
id: "aws-resilience-hub-diagram-05-events-observations"
title: "Events, observations and the current operator view"
type: "entity-relationship-diagram"
service: "aws-resilience-hub"
status: "reviewed"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "data-model"
  - "erd"
aliases:
  - "Events, observations and the current operator view ERD"
related:
  - "../report.md"
  - "../review.md"
  - "../quality-review.md"
  - "../api/index.md"
---

# Events, observations and the current operator view

Proposed application model: provider events trigger hydration; projections select qualified evidence.

This note is the editable semantic source. Obsidian renders the Mermaid block below; the [SVG rendering](05-events-observations.svg) provides the layout used by the application and report.

## Entity relationships

```mermaid
%% Reviewed 2026-11-05. Proposed local temporal model; official context S32-S44.
%% Event uniqueness includes source channel, stream scope and provider event ID.
%% Native service posture and derived aggregate summaries have different kinds.
%% Projection computedAt is distinct from evidence observation timestamps.
erDiagram
    direction TB
    ENTITY_REF {
        string entityKey PK
        string entityType
        string providerScope
        string providerKey
        string visibilityState "Includes tombstones and unresolved refs"
    }
    EVENT_SUBJECT {
        string eventKey PK, FK
        string entityKey PK, FK
        string role
        json linkageEvidence
    }
    EVENT {
        string eventKey PK
        string sourceChannel
        string streamScope
        string sourceEventId
        string eventType
        datetime occurredAt
        datetime receivedAt
        json rawEvent "Original channel envelope and detail"
    }
    POSTURE_OBSERVATION {
        string observationId PK
        string entityKey FK
        string observationKind "AWS_SERVICE or DERIVED_ATTENTION"
        string assessmentRef "Optional scoped correlation"
        string policyContextRef "Observed context; not evaluated revision"
        json contributorEvidence
        string aggregationRuleVersion "Required for derived summaries"
    }
    HEALTH_OBSERVATION {
        string observationId PK
        string entityKey FK
        string sourceSignal
        datetime measuredAt
        datetime expiresAt
        string state
        json evidence
    }
    CURRENT_PROJECTION {
        string entityKey PK, FK
        string dimension PK
        json selectedObservationRefs
        int projectionRevision
        datetime computedAt
        json freshnessAndCoverage
    }
    ENTITY_REF ||--o{ EVENT_SUBJECT : linked_by
    EVENT ||--o{ EVENT_SUBJECT : subjects
    ENTITY_REF ||--o{ POSTURE_OBSERVATION : observed_as
    ENTITY_REF ||--o{ HEALTH_OBSERVATION : observed_as
    ENTITY_REF ||--o{ CURRENT_PROJECTION : projects
    CURRENT_PROJECTION }o..o{ POSTURE_OBSERVATION : selects_evidence
    CURRENT_PROJECTION }o..o{ HEALTH_OBSERVATION : selects_evidence
```

## Relationship constraints

- Event uniqueness: (sourceChannel, streamScope, sourceEventId). Subjects retain type, provider scope and key.
- Aggregate attention summaries retain distinct contributor identities, membership context and rule version.
- computedAt belongs to the projection. occurredAt, receivedAt and observation timestamps remain separate.
- Preserve the original channel payload and typed scoped subjects together. Local create events reference the generated entity identity; request IDs are supplementary correlation data.
- A configuration version changes with editable configuration; the projection revision can advance independently when evidence arrives.

## Implementation boundary

The mock exposes typed event subjects and retained envelopes, mutation timelines, selected health/posture observations, and separately expiring projections. The logical Event maps to the API's EventEntity envelope; EventSubject maps to its nested `subjects[]`, and `sourceChannel`/`streamScope` map to `channel`/`streamOwner`. Generalized historical entity references, complete membership replay, live provider hydration and durable storage remain the broader temporal design. `GetServiceStatus.selectedObservations` makes the selected evidence retrievable inline; an accepted event is still not proof that an asynchronous provider workflow completed. See the [traceability matrix](../report.md#1-implementation-traceability).

The SVG uses navy for AWS-backed identities and values, and teal for local relationships, captures or observations. These colors describe ownership of the model element, not operational status.

## Related notes

- [Reviewed data-model report](../report.md)
- [Model review decisions](../review.md)
- [API operation reference](../api/index.md)

## Official sources

- [S32 — Native EventBridge notification support and delivery](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-notifications.html)
- [S33 — Assessment completed event](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-assessment-completed.html)
- [S34 — Assessment failed event](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-assessment-failed.html)
- [S35 — Assessment queued event](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-assessment-queued.html)
- [S36 — Finding resolved or irrelevant event](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-finding-resolved.html)
- [S37 — Dependency discovered event and stabilization](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-dependency-discovered.html)
- [S38 — ListServiceEvents](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListServiceEvents.html)
- [S39 — ListSystemEvents](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListSystemEvents.html)
- [S40 — ListPolicyEvents](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListPolicyEvents.html)
- [S41 — CloudTrail logging](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-cloudtrail-events.html)
- [S42 — Achievability](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_Achievability.html)
- [S43 — CloudWatch achievability metrics emission](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-cloudwatch-metrics.html)
- [S44 — Dependency discovery and operational observability](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-discovery-vs-observability.html)
