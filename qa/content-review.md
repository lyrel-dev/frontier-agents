# Content review — canonical engineering guides

Review date: 22 October 2026. This is an editorial/source review, not an independent service certification or a live AWS execution record.

## Corrections implemented

| Audit defect | Correction | Location |
|---|---|---|
| Competing scenario, mechanism and platform editions | One maintained Markdown guide per platform; generated HTML and slides derive from it. Old HTML entry points contain only navigation links. | guides/; README; documentation builder |
| Reused identifiers | Global D-, S-, F- and A- section namespaces; one meaning per identifier. | Canonical guide headings and slide references |
| Fixed four-stage/three-step template | Removed. Procedures, matrices and explanations have lengths determined by the subject. | Editorial standard and new renderer |
| Capabilities confused with applications | Product functions are connected to supporting resource/control capabilities before use cases. | D-01; S-01; F-01 |
| Configuration compressed to generic verbs | Added authentication fields, role responsibilities, configuration choices, confirmation points and diagnostic paths. | D-02 through D-04; S-02 through S-04; F-02 and F-05 |
| Combined memory mechanisms | Separated production, feedback, attachment/lifecycle, standing instructions and selected procedures; separated FinOps files, memory and compaction. | D-M01 through D-M07; F-M02 through F-M04 |
| Requirement generation mixed with evaluation | Evaluation/applicability and destructive regeneration are separate mechanisms. | S-M03; S-M04 |
| Encryption reduced to a label | Added documented key hierarchy, calling identities, context and lifecycle implications. | S-M06 |
| Synthetic totals could not support attribution | Added quantities/rates, component decomposition and limited corroborating change evidence. | F-U01; examples/prepared-evidence.json |
| Narrative lacked observable state | Added triage states, run/configuration distinction, finding lineage, event-to-task trace and object-specific lifecycle. | D-06; S-04/S-M05; F-M05/F-M07 |
| Automated checks presented as content assurance | Separate machine checks, source review, layout review and live-runtime limitations. | VALIDATION.md; qa/checks.json |

## Source-version decisions

Official AWS pages were read for the revision using available full-page content and indexed extracts. Some cached full pages were older than the indexed version of the same URL. The guide source registers identify the affected subjects rather than claiming a single perfectly synchronized documentation snapshot.

- DevOps instructions: newer managed-agent and instruction guidance uses the Agents / Managed agents / Agent definition route; older cached text uses Knowledge / Instructions.
- DevOps knowledge: newer memory, custom-agent, asset and dated-change guidance documents custom-store attachment, learned-knowledge migration and corrective reflections. These are not inferred from older generic descriptions of learning.
- Security authentication: newer indexed guidance includes email MFA and credential testing. Older cached authentication content excludes email MFA.
- Security network configuration: newer task-specific wizard documents explicit nonstandard ports and target/access/exclusion classes. The older troubleshooting page's 80/443-only restriction is not carried forward.
- Quotas and default behaviors: selected values are attributed to the reviewed quota/configuration pages; the guides direct users to effective current limits before deployment.

The source registers name the reviewed official sections near their claims. The generated coverage map links those identifiers to canonical sections. It does not claim exhaustive coverage of all AWS user guides or a numerical completeness score.

## Explicit remaining boundaries

- DevOps: full remote-protocol client setup, complete release-profile authoring and all incident-provider variations remain linked reference scope. The guide explains their place and effect boundaries without inventing configuration schemas.
- Security: complete provider compatibility/CI/CD matrices, full design-review tutorial and GenAI-specific exception authoring are not reproduced. The included procedures address the application-assessment platform and ordinary operational prerequisites.
- FinOps: the guide does not enumerate every supported cost dimension or reproduce full account-specific IAM policies. Query contracts, source provenance and role responsibilities are explained; official API/policy references remain authoritative.
- The architecture comparison is an engineering synthesis, not an AWS-provided common runtime or cross-agent permission model.

## Verification scope

The worked examples contain deliberately invented data, not results collected from the services. The executable fixture checks establish arithmetic or record consistency only. Proposed service-side acceptance tests remain proposed. No credentials, live targets, external messages or infrastructure changes were exercised.

All four curated deck layouts were rendered locally. Representative flow, table and exercise slides were inspected. The published build adds complete canonical reference text and source URLs to notes; automated layout bounds and note checks are separate from visual inspection. This is not a pixel-level review of every rendering in every presentation application.

Git history retains previous editions. No manual snapshot directory, encoded import package or distribution archive is part of this revision.
