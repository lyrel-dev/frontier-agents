# Measured Grafana dashboard

`grafana/agent-validation.json` is the empty-workspace baseline with twelve time-series panels: eleven derived trial measurements and source-observation age. It queries the implemented authenticated `GET /api/metrics` endpoint after a Prometheus scrape. These `agent_validation_*` names are local normalized **gauges**, not native AWS metrics. The empty workspace emits declarations but no invented observation values.

Import the JSON into your Grafana installation and select its Prometheus datasource variable. Select actual trial IDs. No automatic Grafana installation, AWS connection or measurement generation occurs during import. CloudWatch observations remain available in console trial graphs; the supplied Grafana JSON focuses on derived accepted/pending assessments, not arbitrary native service namespaces.

The example Prometheus configuration uses a bearer-token file. Supply a protected token file and an address reachable from the scraper, using a private/local tunnel consistent with the API's Host restrictions. The application is not designed for broad unauthenticated scraping. Do not put the token into a URL, dashboard, Git file or public container environment. For a separate Prometheus container, host-loopback routing and Host validation require an explicit reviewed deployment; the placeholder address is not a working auto-discovery feature.

Each trial is labeled with trial ID, campaign and arm. Values are the latest selected assessment, not live samples streamed from AWS. Source-observation age detects old observations still being scraped. Never apply `rate()` to the gauges or infer a success from missing data. Complete context, eligibility, missing evidence and verdict dimensions remain in the console's pinned report. A Grafana curve alone cannot prove a valid trial or agent-attributable recovery.

Bound active campaign retention and time-series cardinality. Long-term evidence belongs in the local workspace/approved backup rather than unbounded Prometheus labels. Dashboard JSON structure and query mapping are checked locally; no Grafana or Prometheus server was run for this delivery.

## Configured business requirements

After assessments contain configured business checks, the authenticated `/api/grafana` response adds a panel for each distinct requirement/category/unit. `/api/metrics` exports `agent_validation_business_value` with those labels and the trial/campaign/arm. Missing aggregate observations are absent, not zero. Panels and labels retain the registered units. The offline baseline intentionally cannot know the future account-specific requirement set. Re-export the runtime dashboard after adding such evidence.

## Scrape-only access and scope (0.5.1)

Use `LAB_METRICS_TOKEN` or a private `LAB_METRICS_TOKEN_FILE`, distinct from the
operator and approval tokens. Configure Prometheus `authorization.credentials_file`
with that scrape-only value. It is never saved in the workspace or exported.
Use explicit `LAB_ALLOWED_HOSTS` for an internal service name; no wildcard hosts.

Exported summaries include workload account/Region/service, Agent Space,
FIS template revision and assessment identity. They are frozen outcomes repeatedly
exposed to the scraper, not live workload samples. Inspect observation age and the
pinned result; recent scrapes do not make an old experiment fresh. Empty values
remain absent. Business series preserve their measurement-account and unit labels.

`tests/observability_acceptance.py` verifies the actual scrape, dashboard import,
readback and generated PromQL against isolated servers. It uses test-only metadata,
not user AWS evidence. Review that exact revision's CI artifact for measured results.
