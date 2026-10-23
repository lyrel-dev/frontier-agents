# 0.5.1-dev — operational acceptance and telemetry boundaries

- Publish the pending guided onboarding/native FIS components on a separate branch.
- Add a scrape-only credential, exact internal-host allowlist and worker-aware readiness.
- Pin the account/Agent Space binding directly in new assessments. Scope-sensitive
  telemetry rejects wrong-owner or unpinned assessments; historical records are not rewritten.
- Retain workload/agent/template/assessment identity in Prometheus and Grafana.
- Exercise local configuration activation and persistence in actual containers.
- Add real Prometheus scrape, Grafana import/readback and PromQL execution acceptance.
- Pin botocore to the matching tested boto3 version; this is not a full dependency lock.
- Retain live AWS gates separately from source/hosting/software checks.

# 0.5.0-dev — guided preparation and native AWS FIS execution

- Added integrated form-based account/Region/profile onboarding, Agent Space association discovery, immutable configuration proposals and separate activation approval.
- Added real skip-all preview lifecycle, native dynamic/multi-account target envelopes, fresh dispatch preview, exact account-role checks and per-account effect/restoration validation.
- Prevented an in-flight catalogue refresh from restoring private records after the operator locks the SPA; added delayed-response regression coverage.
- Added typed SDK verifier forms and guided probe/route/metric/ground-truth/runbook preparation; no raw application JSON is required by the guided operator path.
- Added configured business/data/collateral checks to response, prevention, benchmarks, graphs and exports. Missing evidence is inconclusive; unconfigured requirements are not assessed.
- Added native multi-account SDK and workflow regressions, guided browser workflow and current component acceptance traceability. Updated CI requests native navigation for all UI surfaces.
- Runtime remains empty, non-production and write-disabled by default. No real AWS account/incident was tested; no remote commit/push was performed in this delivery.

# 0.4.0-rc1 — AWS FIS account catalogue and benchmark campaigns

- Added resumable, account-verified paginated template/history discovery with target-account configuration reads and explicit per-scope gaps.
- Added an AWS-first default SPA: accounts, FIS library, guarded campaign queues and frozen response benchmarks.
- Reused the existing FIS executor and per-exposure approval/recovery controls; no blanket execution of discovered templates.
- Added deterministic child registration, transactional queue ownership/pause enforcement, failure retention and restart-safe progression.
- Added cohort/agent-separated statistics, actual-exposure comparability, missing/censored counts, interactive graphs and all-attempt exports.
- Multi-account and selector-based templates are visible but remain execution-blocked until their adapters are qualified.
- No live AWS or agent outcome is asserted by this increment.

# Runtime safeguards and hosting gate — 22 October 2026

- Require a fresh, verified FIS safety-lever read before first fault dispatch. Block engaged, engaging, unknown and unreadable states. Preserve uncertain-operation reconciliation and owned-experiment stopping.
- Acquire worker ownership before serving the combined API; fail startup if another worker owns the workspace.
- Supervise engine and probe-scheduler failures, stop the combined HTTP service on worker failure, and drain probes before releasing the lock.
- Add 23 runtime regression tests and a credential-free Docker acceptance harness covering isolation, authentication, persistence and shutdown. CI retains measured hosting results rather than treating a test definition as a pass.
- No live AWS account, fault, agent task or prevention campaign is exercised by this increment. See docs/RUNTIME_ACCEPTANCE.md.

# Acceptance tooling follow-up — 22 October 2026

- Added `acceptance.py preflight`: offline by default; optional read-only AWS qualification and an explicitly requested single business-path GET. It cannot start a fault, agent task or runbook.
- Added FIS safety-lever observation and complete configured-metric checks. Missing or partial data blocks read qualification.
- Added `acceptance.py audit`: checks a consistent copy of captured evidence, pinned hashes, source scope, native-response obligations and optional prevention lineage. Reviewable evidence is not a passing agent result or authenticated AWS proof.
- Fixed the native-browser test's unlock/workspace loading race and added delayed-response coverage without weakening CSP or falling back to a bridge.
- Excluded local environment definitions and acceptance exports from Git and Docker build contexts.
- The executable baseline is committed on `feat/devops-agent-response-lab`. Live AWS acceptance is still pending; no real account or target was supplied.

# 0.3.0-rc1 — executable replacement, not a migration of historical claims

- Added a persistent experiment worker, real bounded HTTP probes, FIS execution/target confirmation, independent cleanup and restart/unknown-write handling.
- Added native incident discovery without a pre-entered task ID; explicit delivery acceptance/rejection, collection gaps and assisted mode are distinct.
- Added grounded structured diagnosis review, exact approved Automation interventions and conservative recovery attribution.
- Added actual evaluation requests, version-pinned recommendation reads, implementation verification, replay and preregistered comparison.
- Added empty operational SPA, interactive measured graphs, immutable evidence exports, pinned offline reports and an actual Prometheus exporter/Grafana dashboard.
- Restricted the initial executor to explicit-ARN finite FIS templates and linear pinned Automation documents. Unsupported deployment/fault paths are blocked rather than advertised as qualified.
- Corrected a partial optional CreateBacklogTask reference discovered by SDK contract tests; no invented reference identifiers are sent.
- No runtime fixture dataset, seed operation, ready-made success or credentials are included. Test fixtures are isolated under tests.

Live AWS execution, native incident routing, agent behavior, deployed prevention efficacy, container/runtime hosting and Grafana server acceptance remain pending. See validation/review.json and docs/LIVE_ACCEPTANCE.md.
