---
id: "aws-resilience-hub-model-review"
title: "Model review and implementation decisions"
type: "review"
service: "aws-resilience-hub"
status: "reviewed"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "review"
  - "data-model"
aliases:
  - "Resilience Hub model review"
related:
  - "report.md"
  - "api/index.md"
  - "quality-review.md"
  - "validation.md"
---

# Model review and implementation decisions

**Reviewed:** 2026-11-05

**Scope:** the original AWS Resilience Hub operator UI data-model report, all five ER diagrams, the 44-operation workspace RPC extension, and the mapping to the detailed `resiliencehubv2` contracts.

**Disposition:** the initial prototype review below is retained as an engineering record. The subsequent [adversarial quality review](quality-review.md) supersedes its broad approval: it reproduced substantive semantic defects despite the original passing tests, corrected the implemented slice, and makes the remaining delivery gaps explicit. The package is a reviewed mock and design reference, not a production integration approval.

The reviewed analysis is [report.md](report.md), with [API operations](api/index.md) and five linked diagram notes. The original report's detailed API analysis and all 48 official source URLs have been retained. This review does not claim live-account validation.

## RPC extension review

The implemented extension contains 44 operations: 30 native-backed adapters, nine composed reads, three local commands and two ingestion operations. Each operation has an Obsidian Markdown note with YAML properties, exact schemas, executable examples, roles, errors and lifecycle effects. The [AWS mapping](api/aws-mapping.md) retains the original 34 official sources and now has 38 after the follow-up review. The [protocol](api/protocol.md) explicitly owns the RPC namespace, local revisions, replay window, signed snapshot pagination and guarded deletion rules.

| Review finding | Correction or explicit boundary |
| --- | --- |
| The requested AWS RPC presentation differs from native Resilience Hub v2 transport. | Use the product namespace `ResilienceWorkspace_20261105`, root POST and `X-Amz-Target`; document the native operation-specific routes separately. |
| Native input shapes had several easy-to-confuse names and unions. | Use `crossAccountRoleArn`, four exact achievability keys, `errorMessage`, resource-tag arrays, structured EKS selectors and `reportOutputs[].s3`. Review all native input bounds against the source mapping. |
| A first contract draft included sample ARN strings where schema objects were required. | Replace those properties with schemas; independently validate the shared definitions and all 88 operation request/response schemas. |
| Some composed operations were initially labelled with nonexistent native names. | Map topology acquisition to `ListResources` and `ListServiceTopologyEdges`; map event acquisition to the native entity-event collections. Keep composed get operations visibly application-owned. |
| A seeded event-key collision could previously append new health evidence under an already retained event identity. | Reject the collision before mutation; regression tests verify that existing health and audit evidence remain unchanged. |
| Recommendation list defaults could mix current and historical evidence. | Document the `findingObservationId` filter for current detail recommendations; preserve all historical instances and their observation identities. |
| Current detail DTOs do not represent every partial native summary. | Identify the required-ARN System DTO as the complete mock case. A production adapter needs a partial reference/coverage representation for limited-visibility native system summaries. |
| HTTP errors, default role and diagram messages needed exact implementation alignment. | Document the HTTP 405 transport variant, default `demo` role, and response routing through the API. |

The original extension passed 39 tests and exercised all 44 generated examples and HTTP handlers. That established execution and structural checks; it did not establish correct operator meaning. The later review found missing attention reasons, stale evidence counted as current coverage, missing evidence DTOs, manufactured timestamps, unsafe timestamp ordering and a disposition-dependent assessment simulator. Current corrections and test totals are in [quality-review.md](quality-review.md) and [validation.md](validation.md). The browser and RPC server remain separate mock states; live integration, a background reconciliation worker and production authentication remain delivery work.

## Corrections made before implementation

| Priority | Finding | Applied correction |
| --- | --- | --- |
| P1 | The earlier finding-observation diagram used a composite key, while recommendation prose referenced an undefined observation ID. | `FindingObservation.observationId` is now an explicit local primary key. `Recommendation.observationId` references it. The capture, scoped finding identity, representation and uniqueness rule are explicit. |
| P1 | An abbreviated assessment reference could permit cross-service correlation. | Any optional capture correlation uses `(serviceArn, relatedAssessmentId)` against the composite assessment key. It remains labelled local correlation and does not assert an immutable assessment finding set. |
| P1 | Capture completeness did not distinguish list pagination from fetching detailed findings and recommendation arrays. | Captures have separate list and detail coverage. Observations identify `SUMMARY` or `DETAIL`, source operation, observation time and field presence. Recommendations reference detail observations only. Missing data never becomes a known empty array. |
| P1 | Topology endpoint foreign keys were not visibly constrained to the same snapshot. | Each edge endpoint references `(topologyId, localNodeId)` in its own snapshot. Unresolved endpoints remain stubs. `COMPLETE` still means collector completion, not an atomic AWS snapshot. |
| P1 | The temporal diagram labelled the current projection with `observedAt`, while the accompanying table used `computedAt`. | Projection assembly uses `computedAt`; evidence retains its own observed, measured, provider-update, occurrence and receipt timestamps. |
| P1 | A generic posture subject could blur native service evidence with a system/journey conclusion. | `AWS_SERVICE` posture and `DERIVED_ATTENTION` summaries are distinct observation kinds. Derived summaries retain membership context, contributor identities, evidence references, coverage and a rule version. |
| P2 | Generic snapshot terminology could conflate effective targets, observed policy content and the exact context evaluated by an assessment. | The effective-target observation has a named identity. A policy-context capture is a separate local evidence bundle. No observed hash or local revision is presented as an AWS evaluated policy revision. |
| P2 | Shared-service aggregation was stated at a high level but lacked an implementable denominator and deduplication rule. | System and journey service sets use distinct service ARNs. Finding counts use `(serviceArn, findingId)`. A system includes associated services without journeys. Overlapping attention reasons are combined by service-set union. |
| P2 | “Category” could ambiguously mean a finding failure category or a recommendation group. | API mapping retains the actual `Finding.failureCategory` field. Recommendation category identifies its source array and has separate local enum values. |
| P2 | The five diagrams were not all available as editable standalone sources and SVGs. | Each diagram now has an Obsidian Markdown note with YAML front matter, fenced Mermaid source and an SVG asset generated by the deterministic local renderer. |

## API conclusions retained after review

The following conclusions in the original report were correct and remain central to the UI:

- **Use the next-generation contract.** The requested conceptual `*Entity` names map to v2 shapes and operations. Do not mix in the older application-centric API. Detailed operation and SDK contracts take precedence over overview naming. [Official SDK inventory](https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-resiliencehubv2-2026-02-17.html)
- **Four optional policy component types.** The current shape supports availability SLO, backup interval, Multi-AZ recovery and Multi-Region recovery targets; a policy need not configure every component. Coverage must compare results with captured applicable targets. The shape has no native performance component for latency or error-rate objectives. Effective targets expose eight metrics. [GetPolicy](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetPolicy.html) · [EffectivePolicyValues](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_EffectivePolicyValues.html)
- **Ownership is not inheritance.** `SELF` and `CROSS_ACCOUNT` describe account ownership; a returned policy name is not a policy ARN. Identity resolution must be evidenced and optional. [SloSource](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_SloSource.html)
- **No mandatory Assessment-to-Finding foreign key.** Current findings are service-scoped; the list operation has no assessment ID filter. Local captures can be correlated to a run without claiming exact historical run membership. [ListFailureModeFindings](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeFindings.html) · [GetFailureModeFinding](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetFailureModeFinding.html)
- **Recommendations are nested suggested-change groups.** They do not provide native identity, implementation cost, complexity or a standalone mutation lifecycle. Those UI values are local enrichment, with provenance. Assessment execution cost is a different concept. [Finding](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_Finding.html) · [InfrastructureAndCodeRecommendation](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_InfrastructureAndCodeRecommendation.html)
- **Discovery is not health.** Enabled discovery, positive eligibility, DNS query activity and dependency criticality do not establish that a service is currently healthy. Live health requires additional monitoring evidence and expiry rules. [Discovery versus observability](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-discovery-vs-observability.html)
- **Events require reconciliation.** Native EventBridge delivery is best effort. Event history, entity timelines and CloudTrail have different semantics and IDs; an API invocation is not asynchronous completion. [EventBridge notifications](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-notifications.html) · [CloudTrail events](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-cloudtrail-events.html)

## Prototype behavior required by this review

The prototype should label all data as fictional. It may simulate event arrival, a hydrated assessment result, a finding disposition change and a telemetry change, provided it preserves these model boundaries:

1. A successful assessment can coexist with unmet resilience objectives, open findings or degraded runtime health.
2. An old event appears in the timeline without reverting newer authoritative observations.
3. A failed new assessment preserves the previous successful posture and displays its age.
4. A finding marked `IRRELEVANT` remains suppressed rather than becoming a verified repair. A `RESOLVED` disposition still needs subsequent verification evidence.
5. A shared service or finding is counted once in a system/portfolio total, even if it appears in several journeys.
6. Expired telemetry becomes unknown or stale according to the labelled local rule.
7. A partial capture keeps earlier evidence with its original timestamp and communicates the gap.
8. A service failing its strict combined objective does not establish that every looser journey policy failed.
9. A subsequent assessment completion cannot infer remediation or achievability from operator finding dispositions. It needs independent result evidence.
10. The current coverage denominator uses distinct services and captured expected policy components; retained, stale, incomplete and inaccessible evidence remain explicit.

## Validation performed on the report package

- Reviewed entity identities, relation scopes and ownership against the detailed source mappings.
- Preserved all 48 official URLs and verified that every report citation has a definition.
- Generated all five SVGs from the Mermaid blocks in the Markdown diagram notes and their local presentation layouts. The renderer checks unknown entities, missing routes and field overflow.
- Converted prose and diagram sources to Markdown notes with YAML properties. The prior PDF export and its PDF-only build dependencies have been removed from the current package.
- Checked that native `failureCategory`, policy component names, observation identity and `computedAt` terminology remain consistent across the package.

These checks establish internal consistency of the documentation package. They are not live AWS integration tests. Exact association-array replacement, detachment, clearing, authorization, pagination and concurrent-edit behavior must be verified with the chosen SDK and controlled account responses before production editing is enabled.

The follow-up review also makes `PolicyContextCapture`, `RecommendationEnrichment` and `DependencyGovernance` explicit in the ER diagrams, adds event-envelope preservation, and connects diagram concepts to the implemented API. Refer to [quality-review.md](quality-review.md) for the corrected acceptance bar and the baseline reproductions that motivated it.
