---
id: "aws-resilience-hub-diagram-03-assessments-findings"
title: "Assessments, finding captures and recommendations"
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
  - "Assessments, finding captures and recommendations ERD"
related:
  - "../report.md"
  - "../review.md"
  - "../api/index.md"
---

# Assessments, finding captures and recommendations

Findings are service-scoped. Captures preserve observation history without inventing run ownership.

This note is the editable semantic source. Obsidian renders the Mermaid block below; the [SVG rendering](03-assessments-findings.svg) provides the layout used by the application and report.

## Entity relationships

```mermaid
%% Reviewed 2026-11-05. Official sources: report S16-S22, S45-S48.
%% Finding observations have a real surrogate key, used by recommendations.
%% Capture correlation must use (serviceArn, relatedAssessmentId).
%% Unique observation: (captureId, serviceArn, findingId, representation).
erDiagram
    direction TB
    SERVICE {
        string serviceArn PK
    }
    ASSESSMENT {
        string serviceArn PK, FK
        string assessmentId PK
        string assessmentStatus
        int totalFindings "Run result; not current backlog"
    }
    FINDING {
        string serviceArn PK, FK
        string findingId PK
        string status
        string failureCategory
        string severity
    }
    FINDING_CAPTURE {
        string captureId PK
        string serviceArn FK
        datetime captureStartedAt
        datetime captureCompletedAt
        json listCoverage
        json detailCoverage
        string relatedAssessmentId FK "Optional same-service correlation"
    }
    FINDING_OBSERVATION {
        string observationId PK
        string captureId FK
        string serviceArn FK
        string findingId FK
        string representation "SUMMARY or DETAIL"
        datetime observedAt
        datetime sourceUpdatedAt "Optional provider timestamp"
    }
    RECOMMENDATION {
        string recommendationId PK "Local, observation-scoped identity"
        string observationId FK "DETAIL observation only"
        string category "Source recommendation array"
        int sourceArrayOrdinal
        json suggestedChanges
    }
    SERVICE ||--o{ ASSESSMENT : owns
    SERVICE ||--o{ FINDING : contains
    SERVICE ||--o{ FINDING_CAPTURE : scopes
    ASSESSMENT o|..o{ FINDING_CAPTURE : local_correlation
    FINDING ||--o{ FINDING_OBSERVATION : observed_as
    FINDING_CAPTURE ||--o{ FINDING_OBSERVATION : collects
    FINDING_OBSERVATION ||--o{ RECOMMENDATION : owns
```

## Relationship constraints

- Observation uniqueness: (captureId, serviceArn, findingId, representation). Recommendations require DETAIL.
- relatedAssessmentId joins with the capture serviceArn. It records correlation, not an authoritative result set.
- List coverage and detail hydration coverage are independent. Missing recommendation data is not an empty set.

The SVG uses navy for AWS-backed identities and values, and teal for local relationships, captures or observations. These colors describe ownership of the model element, not operational status.

## Related notes

- [Reviewed data-model report](../report.md)
- [Model review decisions](../review.md)
- [API operation reference](../api/index.md)

## Official sources

- [S16 — AssessmentSummary](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_AssessmentSummary.html)
- [S17 — Finding](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_Finding.html)
- [S19 — ListFailureModeFindings](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeFindings.html)
- [S20 — GetFailureModeFinding](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetFailureModeFinding.html)
- [S21 — Viewing findings and managing disposition](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-viewing-findings.html)
- [S22 — InfrastructureAndCodeRecommendation](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_InfrastructureAndCodeRecommendation.html)
- [S45 — StartFailureModeAssessment](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_StartFailureModeAssessment.html)
- [S46 — UpdateFailureModeFinding](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_UpdateFailureModeFinding.html)
- [S48 — ListFailureModeAssessments](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeAssessments.html)
