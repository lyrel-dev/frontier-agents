# Local API

All `/api/*` requests require `Authorization: Bearer <local token>`. Approval routes require the **separate approval token**; it is not an AWS key. The operator token cannot approve execution. The UI keeps tokens in memory, not persistent browser storage. API writes reject other origins. Bind to loopback or use authenticated port forwarding; this is not a multi-user internet service.

| Method and route | Operation |
|---|---|
| GET `/api/workspace`, `/api/config` | Projections, immutable definition summaries, worker heartbeat and sanitized instrument names. |
| GET `/api/schema/{kind}` | configuration, experiment, campaign, diagnosis or change schema. |
| POST `/api/experiments` | Register immutable strict definition; targets/credentials/actions must reference administrator instruments. |
| POST `/api/trials` | `experiment_ref`, optional `campaign_id`, `arm` baseline/treatment/benign. No task ID or outcomes accepted. |
| POST `/api/trials/{id}/qualify` | Queue read qualification. |
| GET `/api/entities/{id}/approval/{purpose}` | Exact subject, digest and typed account/space confirmation. |
| POST `/api/entities/{id}/approve/{purpose}` | `expected_digest`, `confirmation`, `approver`, `rationale`. Separate approval token. Purpose: start/evaluation/change/rollback. |
| POST `/api/trials/{id}/start` | Begin approved trial; requires heartbeat, unexpired matching approval and exclusive environment slot. |
| POST `/api/trials/{id}/abort` | Persist abort intent; worker owns stop/cleanup. |
| POST `/api/trials/{id}/retry-cleanup` | Retry original restoration after resolving a RESTORE_REQUIRED state. |
| POST `/api/trials/{id}/diagnosis` | Attributed structured extraction with exact finding quote and independent verifier citations. |
| POST `/api/trials/{id}/assess` | New assessment from captured probes/source records, never overwrites previous assessment. |
| POST `/api/campaigns` | Pre-register experiment reference, comparison claim, tolerances, minimum pairs and history note. |
| POST `/api/campaigns/{id}/pin` | Select an actually collected `record_id` for one recommendation version. |
| POST `/api/entities/{id}/changes` | Map source quotation to registered `runbook_id`, with proposer/rationale. No arbitrary command or parameters. |
| POST `/api/entities/{id}/reconcile` | Read and verify `operation_id` + `provider_id` against the original uncertain intent. Does not resend it. |
| POST `/api/campaigns/{id}/compare` | Create a new matched evidence comparison with failed/excluded/unpaired attempts. |
| GET `/api/entities/{id}` | Projection, source records, events, operations and recorded probes. |
| GET `/api/records/{id}` | Immutable source/assessment record and content hash. |
| GET `/api/entities/{id}/export` | Dependency-inclusive evidence bundle; no executable result import. |
| GET `/api/entities/{id}/report` | Standalone interactive report, with pinned input hashes/probe capture and no network calls. |
| GET `/api/backup` | Consistent SQLite backup. |
| GET `/api/metrics`, `/api/grafana` | Measured Prometheus export and dashboard JSON. |

Definitions use `experiment:<id>@<revision>` references. Reusing an identical reference/content is idempotent; changed content at the same revision is rejected. Trial, recommendation, approval, operation and assessment IDs are generated independently.

A known prerequisite failure is HTTP 409, unknown record 404, bad schema 422, and missing authorization 401. A request failure is not a zero-data measurement. The server does not expose Swagger, arbitrary filesystem paths, AWS profile editing, raw command execution or cloud credentials.

The local projection is mutable and revisioned; source records, event entries and probe captures are append-only. Frozen reports check hashes but do not authenticate the original producer. Scoped exports may refer to earlier global hash-chain entries; use the database backup for full-chain inspection.
