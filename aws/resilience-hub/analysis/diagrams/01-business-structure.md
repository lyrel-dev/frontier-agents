---
id: "aws-resilience-hub-diagram-01-business-structure"
title: "Systems, services and user journeys"
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
  - "Systems, services and user journeys ERD"
related:
  - "../report.md"
  - "../review.md"
  - "../api/index.md"
---

# Systems, services and user journeys

Membership is many-to-many and constrained through the same system.

This note is the editable semantic source. Obsidian renders the Mermaid block below; the [SVG rendering](01-business-structure.svg) provides the layout used by the application and report.

## Entity relationships

```mermaid
%% Reviewed 2026-11-05. Official sources: report S03-S07, S47.
%% Join records normalize Service.associatedSystems; they are not AWS resources.
%% Journey membership references BOTH the matching SystemService and UserJourney.
erDiagram
    direction TB
    SYSTEM {
        string systemKey PK "Local identity in verified source scope"
        string systemId "Provider identifier"
        string systemArn "Nullable in partial summaries"
        string name
    }
    SYSTEM_SERVICE {
        string systemKey PK, FK
        string serviceArn PK, FK
    }
    SERVICE {
        string serviceArn PK
        string name
        json permissionModel
        json regions
    }
    USER_JOURNEY {
        string systemKey PK, FK
        string userJourneyId PK
        string name
    }
    JOURNEY_SERVICE {
        string systemKey PK, FK
        string userJourneyId PK, FK
        string serviceArn PK, FK
    }
    SYSTEM ||--o{ SYSTEM_SERVICE : associates
    SERVICE ||--o{ SYSTEM_SERVICE : participates
    SYSTEM ||--o{ USER_JOURNEY : owns
    USER_JOURNEY ||--o{ JOURNEY_SERVICE : includes
    SYSTEM_SERVICE ||--o{ JOURNEY_SERVICE : constrains
```

## Relationship constraints

- JourneyService must reference both (systemKey, serviceArn) and (systemKey, userJourneyId).
- A service may belong to a system without a journey. Membership does not establish execution order.

The SVG uses navy for AWS-backed identities and values, and teal for local relationships, captures or observations. These colors describe ownership of the model element, not operational status.

## Related notes

- [Reviewed data-model report](../report.md)
- [Model review decisions](../review.md)
- [API operation reference](../api/index.md)

## Official sources

- [S03 — System](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_System.html)
- [S04 — SystemSummary](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_SystemSummary.html)
- [S05 — AssociatedSystem and nested journey membership](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_AssociatedSystem.html)
- [S06 — Service and GetService response](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetService.html)
- [S07 — CreateService and required configuration](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html)
- [S47 — UserJourney](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UserJourney.html)
