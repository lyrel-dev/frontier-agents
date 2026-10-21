# Local API and interchange contract

The service runs at `http://127.0.0.1:8787` by default. API requests require `Authorization: Bearer <console-token>`. No AWS key belongs in that header. Browser requests are same-origin; no CORS is enabled. There is no public OpenAPI/Swagger endpoint. The authenticated schema endpoint returns the record interchange schema, not a command-execution specification.

## Endpoints

| Method/path | Body | Effect |
|---|---|---|
| `GET /` | — | Serve the single-file interface. |
| `GET /healthz` | — | Process health; no authentication required, no sensitive metadata. |
| `GET /api/workspace` | — | Records, server origin/hash metadata and recent audit entries. |
| `GET /api/config` | — | Sanitized connection names, expected identity and selected scope; no raw socket/kubeconfig paths. |
| `GET /api/schema` | — | Version 1 bundle JSON schema. |
| `POST /api/import/preview` | Raw bundle JSON | Validate and show proposed additions/conflicts; no write. |
| `POST /api/import` | Raw bundle JSON | Validate again, then atomically add records; origin is imported. |
| `GET /api/export` | — | Complete record bundle with hash manifest. |
| `POST /api/inspect` | `{"connection_id":"aws-staging"}` | Read configured metadata and save a snapshot. One inspection at a time. |
| `POST /api/observe` | `{"snapshot_ref":"snapshot:ID@1"}` | Create a collection-observation run and incomplete-scope scalar from a non-synthetic snapshot. |
| `POST /api/evaluate` | `{"run_ref":"execution_run:ID@1","evidence_refs":null}` | Create a new validation from linked evidence. An explicit list resolves ambiguity; `[]` selects none. |
| `POST /api/reports` | `{"validation_ref":"validation_run:ID@1"}` | Create a frozen report. |
| `GET /api/report-html?reference=report:ID@1` | — | Download escaped, inert standalone report HTML. |
| `GET /api/backup` | — | Download a consistent SQLite backup. |

There are no start-fault, stop-fault, arbitrary-shell, invoke-Lambda, container-exec, delete-record or restore-database endpoints. A scenario's `action` field is descriptive text, not an executable instruction.

## Bundle envelope

```json
{
  "schema_version": "1.0",
  "kind": "validation_bundle",
  "records": [],
  "manifest": null
}
```

The empty array above illustrates the envelope only; imports require at least one record. Use `examples/catalogue.json` or `examples/synthetic-workflow.json` for complete valid data. Maximum: 5 MiB, 5,000 records. `manifest` is optional and maps record references to canonical SHA-256 values.

The six record kinds are `scenario`, `snapshot`, `execution_run`, `evidence`, `validation_run`, `report`. All have `id`, positive integer `revision`, `title`, strict boolean `simulated`, and typed `data`. The generated JSON schema specifies required fields, limits, time formats and enums. Do not rely on the browser preview as a substitute for server validation.

## Import transaction rules

A reference is `kind:id@revision`. Same reference/same normalized content is a no-op. Same reference/changed content is a conflict. A new revision is an addition, not an overwrite. Dependencies must exist in the workspace or bundle and have the correct kind. A conflict or broken dependency aborts the entire import. Origin metadata is assigned by the service and cannot be supplied through the bundle.

A standalone report can have no validation link, but its imported conclusion remains unverified. An imported validation may retain an external verdict; local re-evaluation creates another record and preserves limitations about the supplied evidence. Importing a report is never evidence that a test ran here.

## Evaluation contract

The scenario must be specified and contain at least one required assertion to pass. Runs must be completed, not merely planned, and their time interval must not end in the future. Fault scenarios need explicit fault confirmation. Evidence must reference the run, match its scope and exact interval, use the declared unit and value type, meet the sample minimum and be collected within the allowed lag. Multiple records for one metric require explicit selection. Missing or invalid evidence is inconclusive, not zero and not success.

With valid execution gates, a known required failure yields fail even if another metric is absent. If no required check fails but any lacks usable evidence, the result is inconclusive. All required checks passing yields pass only for those checks. See `DESIGN.md` for the complete boundary.

## Error handling

Authentication errors reject the request before workspace access. Unknown connections and records, schema failures, conflict/import errors and busy inspection return non-success HTTP responses with a bounded explanation. Raw credential fields and SDK error messages are not echoed in normal validation/inspection errors. Service-side details should remain in protected logs. Clients must check HTTP status rather than interpreting an error body as an empty result.

Record timestamps are timezone-aware; the UI displays UTC. Do not use binary floating-point equality for approximate measurements without first choosing an appropriate evidence representation. No unit conversion, percentile recomputation or query evaluation is implicit.
