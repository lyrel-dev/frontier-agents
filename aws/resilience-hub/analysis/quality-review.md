---
id: "aws-resilience-hub-adversarial-quality-review"
title: "Adversarial quality review of the model, API and operator UI"
type: "review"
service: "aws-resilience-hub"
status: "reviewed"
created: "2026-11-05"
updated: "2026-11-05"
tags:
  - "aws"
  - "resilience-hub"
  - "quality-review"
  - "domain-model"
  - "api"
aliases:
  - "Resilience Hub quality challenge"
related:
  - "README.md"
  - "report.md"
  - "review.md"
  - "validation.md"
  - "api/index.md"
  - "api/protocol.md"
  - "api/entities.md"
  - "api/aws-mapping.md"
---

# Adversarial quality review of the model, API and operator UI

**Baseline reviewed:** commit `973685d8f45e0321f5bf87912f6693e217f2a26b`, the previously delivered 44-operation facade and operator prototype. The review covers the report, all five ER diagrams, API schemas and generated operation notes, runtime, browser model, UI, fixtures, documentation tooling and tests.

The previous 39 passing tests did not establish that the implementation preserved the model's operator meaning. This review reproduced failures from an isolated copy of the committed baseline, challenged domain invariants across multiple operations, checked source fidelity against current official AWS documentation, and assigned corrections across the shared model, API and UI.

The user's earlier-interaction lookup was unavailable during this review. The review criteria below therefore come from the visible task: official API analysis, a coherent abstract model, an operator UI for status/health/posture as events occur, corresponding RPC operations, and complete Obsidian documentation. They are not presented as recalled preferences from unseen conversations.

## Questions the deliverable must answer

| Reviewer question | Required quality bar |
| --- | --- |
| Can an operator make a service appear resilient by changing a finding label? | No. Disposition, independent assessment evidence and remediation verification must have separate authority. |
| What evidence supports this badge? | The API must expose the selected observation, its source time, coverage and applicable policy context. An unresolvable capture ID is insufficient. |
| Which requirement was assessed, and is it still representative? | Retain observed effective targets and policy/membership context. Distinguish a provider rerun signal, a local context invalidation and a pending refresh. |
| Does the absence of information look like success? | Unknown, omitted, null, empty, zero, disabled, inaccessible and stale must retain their different meanings. |
| What exactly does a portfolio percentage count? | Define the denominator, freshness and coverage rule, retain contributor identities, and distinguish current evidence from historical evidence. |
| Can normal telemetry prevent an operator from editing configuration? | Configuration concurrency and observational projection changes require distinct revisions. |
| Can an event explain what changed without pretending to be authoritative state? | Retain raw evidence and typed scoped subjects, deduplicate delivery, then request an authoritative refresh. |
| Can the published API express the model shown in the UI? | Required operator evidence must be available through documented read models, with implementation gaps declared explicitly. |
| Do the tests challenge the implementation's assumptions? | Include multi-step, negative, cross-surface and source-shaped cases whose expected outcome comes from a domain invariant. |

## Reproduced defects in the delivered baseline

P1 means the defect can mislead an operator about state/evidence or prevents an essential model/API use case. P2 means a significant consistency, interaction or traceability defect. These priorities describe this prototype's design risk; they are not claims of production incidents.

| ID | Priority | Reproduction and observed failure | Required correction |
| --- | --- | --- | --- |
| Q01 | P1 | Checkout assessment completion returned `NOT_ACHIEVABLE` on the control fixture. Changing only its two high findings to `RESOLVED`, then completing an assessment, returned `ACHIEVABLE` and marked both findings `CONFIRMED_AFTER_REASSESSMENT`. `IRRELEVANT` dispositions could also turn posture green. | Drive simulated assessment outcomes from independent explicit response evidence. Never infer repair verification from a disposition or its readback. |
| Q02 | P1 | Storefront edge had an open finding but `needsAttention` returned false. Resource discovery changed to `FAILED` could also remain outside attention. A stricter policy edit set a refresh flag without affecting the attention total. | One named, shared attention rule with explicit reasons covering findings, resource/discovery gaps, health, posture, execution failure and context invalidation. |
| Q03 | P1 | Advancing the clock by 48 hours made all seven retained posture records stale, while the portfolio still reported 88% assessment coverage. | Separate current usable evidence coverage from last-known historical evidence. Expose stale, partial, inaccessible and unassessed categories. |
| Q04 | P1 | The edge fixture retained eight effective targets. `GetService` returned none of them. `GetServiceStatus` returned `policy-context-edge-initial`, but no operation could resolve that evidence. Finding capture references had similar omissions. | Return the selected effective-target observation, policy context and finding coverage/evidence inline in the relevant read models. |
| Q05 | P1 | A health observation at `1793874240.0009` selected `HEALTHY`; an older observation at `1793874240.0001` then selected `UNAVAILABLE`. Both stored times had been truncated to `1793874240`. | Align accepted timestamp precision, comparison precision and storage precision. Equal-time or older evidence must not replace a newer selected observation. |
| Q06 | P1 | Input sources without a creation time returned `createdAt` copied from `observedAt`. Policies without update times returned `updatedAt` copied from creation time. Missing dependency discovery became `DISABLED`. | Preserve unknown provider facts and explicit presence/normalization information; keep local mutation time separate from provider update time. |
| Q07 | P1 | The official example ARN `arn:aws:resiliencehub:us-east-1:111122223333:service/my-service:abc123` failed facade validation because the resource suffix allowed only fixture-style characters. | Accept the documented opaque provider identity shape; do not let fixture ID conventions define the integration boundary. |
| Q08 | P2 | `CreateService` followed by `ListEvents` for the new ARN returned zero events. The creation audit event targeted `northstar` instead of the created service. Ingested native correlation details could not be retained. | Derive typed subjects from command inputs and results; retain raw event evidence and scoped correlation metadata. |
| Q09 | P2 | A new telemetry observation increased `Service.version`, causing a configuration edit based on the prior version to conflict even though configuration had not changed. | Reserve configuration versions for configuration writes and use a separate projection revision for observations. |
| Q10 | P2 | Browser and RPC health selection disagreed on equal timestamps. Null recommendation arrays could crash an inspector, while omitted recommendations and missing DNS windows were displayed as known zeroes. | Use consistent selection semantics and explicit missing/empty rendering, with focused browser/model tests. |
| Q11 | P2 | Generated examples validated against the same schemas as the implementation, while the report's coverage and evidence requirements remained unimplemented. The earlier review status overstated semantic completeness. | Maintain a model-to-implementation coverage matrix, executable invariant regressions and a bounded readiness verdict. |
| Q12 | P2 | The facade's native-backed write bounds diverged from the official inputs: multiple report outputs were accepted, resource-tag and EKS collections were too large, and an allowed empty tag-value selector was rejected. The same permission shape was used for writes and nullable provider readbacks. | Align writable bounds with official input contracts and use a separate permissive observation shape for reads. Preserve unknown provider members through diagnostics rather than weakening write validation. |

The native identity example is documented in [Failure Mode Assessment Completed](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-eventbridge-assessment-completed.html); the generic ARN syntax is documented in [GetService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_GetService.html). Native finding updates change disposition and optional comment, while native assessment and service responses supply separate assessment/posture information. See [UpdateFailureModeFinding](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/update_failure_mode_finding.html), [ListFailureModeAssessments](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_ListFailureModeAssessments.html) and [GetService](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/get_service.html).

The reviewed write bounds are recorded with primary sources in [AWS mapping](api/aws-mapping.md): one report output; 1–10 resource-tag selectors; 0–10 values per selector; and at most 10 EKS namespaces with the documented name/label constraints. See [CreateService](https://docs.aws.amazon.com/resilience-hub/v2/APIReference/API_CreateService.html) and [CreateInputSource](https://docs.aws.amazon.com/botocore/latest/reference/services/resiliencehubv2/client/create_input_source.html). These are native-backed request rules, separate from read normalization of provider observations.

## Baseline evidence

The following values were reproduced from the immutable baseline commit, not inferred from current code comments:

```json
{
  "assessment": {
    "control": "NOT_ACHIEVABLE",
    "operatorOnlyTriage": "ACHIEVABLE",
    "verification": [
      "CONFIRMED_AFTER_REASSESSMENT",
      "CONFIRMED_AFTER_REASSESSMENT"
    ]
  },
  "attention": { "edge": false, "edgeOpenFindings": 1 },
  "coverageAfter48Hours": { "percent": 88, "stalePostures": 7 },
  "precision": {
    "newerSelected": true,
    "olderSelected": true,
    "result": "UNAVAILABLE",
    "observedAt": 1793874240
  },
  "creationTimeline": { "scopedEvents": 0, "eventEntity": "northstar" },
  "evidence": {
    "effectiveTargetsInFixture": 8,
    "apiEffectiveTargetFields": [],
    "policyContextId": "policy-context-edge-initial"
  },
  "fabricatedTimestamp": {
    "fixtureHasCreatedAt": false,
    "reportedCreatedAt": 1793873520,
    "reportedObservedAt": 1793873520
  }
}
```

## Why the earlier tests missed these failures

The existing tests checked many useful properties: scoped references, pagination, command atomicity, transport, rendering and immediate separation of triage from posture. Their gaps were methodological:

1. The triage test stopped before the subsequent assessment completion, where mutable disposition leaked into assessed evidence.
2. Generated request/response examples proved agreement between the runtime and its own schema, not agreement with the report or a real provider identity example.
3. Baseline fixtures usually contained all expected fields, so missing provider timestamps, unknown configuration and future enum values received little pressure.
4. Coverage assertions accepted the implementation's retained-result interpretation without challenging the report's freshness requirement.
5. Health tests used whole-second or millisecond timestamps and did not compare browser and RPC tie behavior.
6. Read-model tests checked that a capture ID existed, but did not ask whether a client could retrieve the evidence needed to explain it.

The correction strategy is to add regressions around those invariants and to keep the initial dataset, aggregate rules, rendered labels, API DTOs and documentation aligned.

## Review acceptance criteria

- Triage alone cannot alter an assessment outcome or create verification evidence, even after a later simulated assessment.
- All reasons that satisfy the documented attention rule are visible, deduplicated and represented in the API.
- Expired or incomplete assessment evidence cannot inflate current coverage; retained evidence remains separately inspectable.
- A client can inspect the selected policy context and finding evidence without private access to the server's in-memory state.
- Unsupported timestamp precision cannot make an older observation win. The browser and RPC agree on ties.
- Read normalization does not fabricate provider dates or disabled states from absence.
- Provider-shaped ARNs with documented opaque resource characters pass syntax validation.
- Creation events resolve to their subjects and appear in the appropriate timeline; raw input events remain evidence rather than state patches.
- Observational updates do not consume a configuration edit's optimistic version.
- Valid optional policy components, absent collection timestamps, incomplete finding captures and material assessment-input changes cannot produce misleading coverage or attention conclusions.
- Legacy browser state containing conclusions generated by the earlier simulator is not silently restored into the corrected demo.
- All maintained notes retain valid YAML and links; generated schemas/examples agree with the implementation after fixes.

## Remaining implementation boundary

This remains a realistic, deterministic operator prototype and a local RPC facade. The browser and HTTP server have separate stores. The facade does not authenticate real users, persist commands across restarts, call AWS, execute a reconciliation worker or certify provider-side concurrency and clearing semantics. Native partially visible system summaries also require a production adapter representation beyond the complete fixture workspace.

Those boundaries are acceptable for the requested mock deliverable when stated explicitly. They do not excuse incorrect operator conclusions inside the mock. The following closure evidence is from the corrected executable package.

## Correction results

The code, contract, UI and documentation corrections for **Q01–Q12 are complete within the stated mock scope**. Their closure is supported by the 61-test suite, independent schema check, generated references and source review recorded in [validation.md](validation.md).

| Review case | Corrected result | Evidence |
| --- | --- | --- |
| Disposition followed by assessment completion | Identical explicit provider-response fixtures produce identical posture for OPEN, RESOLVED and IRRELEVANT variants. A claimed repair remains UNVERIFIED; suppression remains SUPPRESSED. | Paired domain regressions in [model.test.cjs](tests/model.test.cjs). |
| Persisted invalid conclusions | Schema 2 uses a new browser store. Earlier cached state is retained separately and not loaded; a visible notice explains the reviewed fixture. | Legacy-cache regression in [ui-contract.test.cjs](tests/ui-contract.test.cjs). |
| Portfolio attention | Eight distinct services require attention, with the same named reasons in the browser and API. Storefront's open finding is no longer omitted. | [evidence-contract.test.cjs](tests/evidence-contract.test.cjs), plus domain reason tests. |
| Current versus retained coverage | Initial current coverage is 6/8 (75%); retained evidence is 7/8 (88%, rounded). After 48 hours current coverage is 0/8 while retained evidence remains 7/8. An empty scope returns null percentages. | Cross-surface baseline, expiry and empty-scope tests. |
| Optional components and missing context | An availability-only captured policy can qualify. A missing expected outcome, target value or capture cannot. Current policy edits do not rewrite captured applicability. | Domain optional-policy/context regressions. |
| Incomplete finding collection | Ten open findings are observed; exact portfolio open count is null because one service has no finding capture. A newer partial attempt without an end timestamp supersedes the older complete coverage claim, while retained records remain available. | Shared finding-coverage tests and the domain review's partial-attempt reproduction. |
| Inspectable status evidence | Edge reads expose all eight effective targets, a resolving context-to-target reference, and selected health/posture observations. Configuration reads and retained-posture reads resolve their own contexts. | Public-read checks and [rpc-quality.test.cjs](tests/rpc-quality.test.cjs). |
| Timestamp ordering | Unsupported sub-millisecond inputs fail validation before mutation. Supported timestamps round-trip exactly; equal-time/older observations cannot replace current health. | Timestamp regression using the original rollback values and supported millisecond variants. |
| Unknown provider facts | A seed input source with no provider creation time returns null. Missing discovery is explicit UNKNOWN with a missing-source diagnostic. Unknown native enums preserve raw evidence; read permission variants remain representable. | Source-shaped read-normalization regressions. |
| Identity and input fidelity | The official opaque ARN example passes syntax validation. Report/tag/EKS bounds, ISO Region syntax and tag character constraints are tested, while documented local subsets remain explicit. | Native-shaped request regressions and [AWS mapping](api/aws-mapping.md). |
| Event traceability | Creation events appear under their actual typed subject; child operations retain parent scope. Raw envelopes and correlation IDs are inspectable without mutating authoritative service state. | Scoped audit and raw-event regressions. |
| Edit concurrency | Telemetry, events, findings and assessments leave the service configuration revision unchanged. Input-source membership is explicitly part of service configuration. Enrichment and governance use nested versions. | Runtime concurrency tests and generated mutation-version guidance. |
| Same triage command on both surfaces | Transitioning a finding to RESOLVED creates the same local reassessment obligation and partial current coverage. Health/posture remain unchanged and the claimed repair stays unverified. | Cross-surface triage regression. |
| Documentation and diagram fidelity | All 44 operation examples regenerate; 53 reusable shapes and 88 schemas pass an independent validator. The five ER diagrams now show context, enrichment, governance and event-subject records without naming collisions. | [Validation record](validation.md), [API index](api/index.md), diagram notes. |

Additional review pressure caught errors in the first corrective draft: assuming all four policy components were mandatory, selecting targets independently of the retained context, trusting an old complete finding capture over a newer unfinished attempt, and restoring invalid cached conclusions. Those were corrected before the final gate. They illustrate why a coherent contract needs scenario and relationship checks beyond an operation catalogue.

## Readiness verdict and remaining decisions

**Accepted as a corrected, executable mock and a source-backed model/API design reference.** The report's earlier broad approval is superseded. The new validation evidence supports the implemented semantic slice; it does not support a production release or a claim of complete native API coverage. Fresh visual acceptance is still open because the available browser could not access the workspace preview. The obsolete overview screenshot was removed rather than reused as current evidence.

The following delivery gaps remain concrete and visible in the report's implementation matrix:

| Remaining gap | Required completion evidence |
| --- | --- |
| Browser-to-RPC integration | The UI reads and writes the HTTP store, including errors, pagination, idempotent retry and concurrent-edit recovery. Currently the two demonstrations have separate state. |
| Authoritative assessment and reconciliation pipeline | A worker reads native state after events and periodically, captures pagination/detail coverage, completes asynchronous workflows and preserves failures. RPC assessment start currently only queues a mock run. |
| Full history and partial visibility | Native ARN-less system references, historical policy content/membership, full finding detail archives, DNS query series and complete topology descriptors are represented and retrievable. Current evidence and representative topology captures implement only a bounded subset. |
| Real integration guarantees | Controlled AWS-account tests establish provider field presence, permission boundaries, association replacement/detachment, clearing semantics and concurrent/out-of-band writes. Local versions do not create AWS conditional-write support. |
| Production operation | Durable command/audit storage, identity enforcement and scoped tenancy replace the trusted in-memory demo process. |
| Visual acceptance | An accessible browser verifies the revised evidence panel, cache notice, desktop/mobile layout, keyboard focus and snapshot export. In-memory DOM tests do not substitute for that gate. |

Two model limits remain deliberate: a captured context is not proof of an AWS-evaluated policy revision, and service membership is insufficient to calculate end-to-end journey compliance. Those require additional provider evidence or a separately specified composition model; adding a reassuring badge would not resolve them.
