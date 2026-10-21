# Publication review — 0.2.1

Scope: application code, contracts, evaluation, persistence, read-only inspectors, graph rendering/exports, Grafana generation, deployment, tests and documentation. Baseline: `9383a159eb1578aa5d69f095cec34a6477c44114`.

Reproduced and corrected: normalized in-cluster context failed snapshot validation; aggregate chart extrema overflowed the JavaScript argument stack; snapshot series combined distinct scopes and simulation labels; HTML reports omitted provenance; execution gates masked established requirement failures; Grafana legends omitted environment/scenario labels. Deployment versions and the recovery-point-loss definition were also corrected.

Publication requires backend/generator, baseline browser, native publication browser, HTTP, container-persistence and Grafana import/readback checks. Measured counts, tested server version, workflow URL and reviewed source hashes are in `validation/publication-review.json`. No existing account, runtime, database or incident data is used.

This is a read-only local validation workspace and graph viewer, not a fault runner or readiness certificate. Live AWS/runtime inspection, credential refresh, telemetry collection, PromQL execution, production datasource provisioning, fault injection, disaster recovery, supply-chain certification and independent security review remain outside acceptance. The Grafana version is a compatibility-test target, not a production upgrade recommendation.
