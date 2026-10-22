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
