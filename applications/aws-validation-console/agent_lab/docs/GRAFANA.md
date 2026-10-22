# Measured Grafana dashboard

`grafana/agent-validation.json` contains twelve time-series panels: eleven derived trial measurements and source-observation age. It queries the implemented authenticated `GET /api/metrics` endpoint after a Prometheus scrape. These `agent_validation_*` names are local normalized **gauges**, not native AWS metrics. The empty workspace emits declarations but no invented observation values.

Import the JSON into your Grafana installation and select its Prometheus datasource variable. Select actual trial IDs. No automatic Grafana installation, AWS connection or measurement generation occurs during import. CloudWatch observations remain available in console trial graphs; the supplied Grafana JSON focuses on derived accepted/pending assessments, not arbitrary native service namespaces.

The example Prometheus configuration uses a bearer-token file. Supply a protected token file and an address reachable from the scraper, using a private/local tunnel consistent with the API's Host restrictions. The application is not designed for broad unauthenticated scraping. Do not put the token into a URL, dashboard, Git file or public container environment. For a separate Prometheus container, host-loopback routing and Host validation require an explicit reviewed deployment; the placeholder address is not a working auto-discovery feature.

Each trial is labeled with trial ID, campaign and arm. Values are the latest selected assessment, not live samples streamed from AWS. Source-observation age detects old observations still being scraped. Never apply `rate()` to the gauges or infer a success from missing data. Complete context, eligibility, missing evidence and verdict dimensions remain in the console's pinned report. A Grafana curve alone cannot prove a valid trial or agent-attributable recovery.

Bound active campaign retention and time-series cardinality. Long-term evidence belongs in the local workspace/approved backup rather than unbounded Prometheus labels. Dashboard JSON structure and query mapping are checked locally; no Grafana or Prometheus server was run for this delivery.
