# AWS Health model review

**Review date:** 5 November 2026

**Reviewed revision:** 1.1

**Scope:** API inventory, abstract entities and relationships, state ownership, provenance, counters, lifecycle matching, and the documentation package.

## Outcome

The review found no material contradiction in the retained API inventory or core model. The recommended operational core remains `HealthEvent → EventContext → EntityImpact`. Revision 1.1 makes implementation invariants explicit so the showcase can demonstrate public exposure, account-specific impact, source history, derived lifecycle posture, and operator work without conflating them.

This was a documentation and semantic review. It did not inspect a customer AWS environment, execute Health operations, or validate a production database. The reviewed report retains 40 official AWS source mappings and distinguishes documented provider behavior from proposed application behavior. See [report.md](report.md) for claim-level citations and the full API analysis.

## Findings and incorporated changes

| Finding | Risk to an operator application | Incorporated clarification |
|---|---|---|
| Context identity needed a non-null key and conditional references | Duplicate public contexts or accidental cross-account overwrites, especially with database NULL uniqueness behavior | Use tenant-scoped `(eventArn, contextKind, contextKey)` uniqueness. PUBLIC has no account/organization FK; ACCOUNT has exactly one account; ORG_SUMMARY has exactly one organization and no account. |
| Account-specific entities needed a routing invariant | Entities could be counted under organization summaries or a mismatched account | ACCOUNT impact records must agree with any supplied `awsAccountId`. ORG_SUMMARY owns no impacts. Unresolved associations remain raw observations until reconciled. |
| The original local communication key could be confused with AWS `communicationId` | Delivery deduplication could collapse updates, pages, or distinct notification contexts | Name the local grouping key `communicationRecordId`; preserve AWS `detail.communicationId` as `rawCommunicationId` on the logical page. Page and delivery identity remain distinct. |
| Entity freshness needed to be visible independently of parent-event freshness | A newer event fetch could falsely imply current entity evidence | Keep `EntityRevision.providerUpdatedAt`, event-update time, transport time, and local observation time separate. Preserve payload kind and field presence. |
| Realistic demonstration data needed explicit provenance and a stable time basis | Fictional incidents or dates could look like a live AWS status report; aging would make the demo inconsistent | Label all organization/account/resource/incident/milestone records as fictional and show a fixed scenario clock. Simulated AWS updates and local actions remain separate transitions. |
| Status ownership and metric populations needed an executable definition | Local completion could clear provider pending state; deliveries could inflate event totals; entity counts could be mislabeled resources | Count distinct event ARNs, verified account contexts, event-relative impacts, and inventory resources in their own units. Local completion does not rewrite AWS state or clear exposure without new evidence. Missing/ambiguous catalog matching remains unknown. |

## Important constraints retained from the original analysis

- The current 15-operation API inventory has 13 reads and two organization integration controls. Health exposes no acknowledgement, assignment, manual-close, or remediation-execution operation.
- Public visibility and notification receipt do not establish account-specific impact. Affected-account lookups for public events return an empty account list.
- A Health entity can represent a resource, group, or broader construct. Its identity and count are not automatically inventory-resource identity and count.
- Source events, source entities, local workflow, derived posture, and collection coverage have separate states. Missing actionability does not become informational.
- EventBridge delivery requires idempotency, logical page assembly, raw identity preservation, and explicit incomplete/conflicting evidence. Provider timestamps and arrival time have different meanings.
- The lifecycle catalog supplies service/version and milestone facts without stable provider entry IDs or a direct resource/Health-event foreign key. Applicability comes from an explicit join to independently observed deployments.
- Pagination, per-item failures, optional organization aggregate breakdowns, retention differences, regional routing, and integration readiness must remain visible in coverage.

## Documentation verification

The documentation package contains canonical Markdown, four editable Mermaid ERDs, four standalone SVGs, and a PDF containing all four diagrams and the complete source index. The report-specific generator reads Markdown and derives SVG semantic content from the Mermaid sources. This avoids maintaining a second independent copy of the report or diagram entities in a PDF-only generator.

The completed checks were:

- Rebuilt all SVGs and the PDF from repository-relative sources with the provided Python tools.
- Parsed the four SVGs as XML; checked document titles/descriptions, ownership legends, entity sets, relationship sets, and cardinality mapping.
- Examined rendered PDF pages for all four ERDs, tables, typography, and legible relationship labels; adjusted short-link cardinality placement and paragraph/page boundaries.
- Extracted PDF text to confirm the presence of all 14 report sections, all four figure titles, and all 40 official source URLs; checked that the PDF includes clickable links.
- Checked report-relative file references against the documentation package and retained all six review clarifications in prose and diagrams where relevant.

The SVGs are accessible standalone documents with textual metadata and labels. This does not claim a fully tagged PDF or a comprehensive accessibility certification.

## Application validation

See [README.md](README.md) for application behavior, execution instructions, and its validation record. Application testing is recorded there separately from this document/model review.

## Remaining design boundary

This is an abstract model and a demonstrator contract, not a production physical schema or collector implementation. A production integration still needs concrete authentication and entitlements, persistence and tenancy controls, source-specific reconciliation, inventory connectors, matching rules, and operational monitoring. Those choices can be made without changing the reviewed ownership and identity boundaries.

Rebuild instructions and the intentionally supported source format are documented in [tools/README.md](tools/README.md).
