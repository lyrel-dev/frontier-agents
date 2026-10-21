# Validation console: application design and delivery boundary

**Version:** 0.1.0 · **Review date:** 21 October 2026  
**Status:** runnable read-only baseline; live-environment acceptance pending.

## 1. Goal, context and reanchored progress

Build a standalone console that can answer a narrow, evidence-backed question: **under a specified workload and a controlled incident, did this deployment meet its agreed customer-impact, detection, response, recovery and data-correctness requirements?**

The system under test includes EC2/Auto Scaling, EKS on EC2, EKS on Fargate, ECS on EC2, ECS on Fargate and Lambda. Shared data stores, networks, queues and operational processes remain part of scenario scope. Docker, Podman or local Kubernetes provides the local control workspace and can also be inspected as a target environment. Those are separate roles: a workspace running in Docker may inspect AWS and a Kubernetes context without implying that either is hosted in that Docker engine.

The previous report established a catalogue and candidate tooling. It did not inspect an account, prove permissions, execute a failure or measure recovery. This delivery changes the baseline as follows:

| Workstream | Previous state | Delivered now | Evidence still needed |
|---|---|---|---|
| Scenario research | 36 scenario descriptions; six FIS template examples | 36 versioned draft definitions, searchable by deployment | Service-specific targets, limits, evidence queries and approval |
| Account/runtime connection | Described, not implemented | Configured read-only collectors and identity/coverage records | Actual account and runtime compatibility acceptance |
| Local workspace | Downloadable report files | SQLite records, imports, exports, backup and audit | Deployment-specific volume and restore drill |
| Validation | Illustrative criteria | Deterministic scalar evaluator with input hashes | Trusted incident measurements and independent reconstruction |
| Reporting | Narrative and synthetic examples | Linked, immutable validation reports | Approved evidence sufficient for a real service decision |
| Execution | FIS examples only | Explicitly absent | Separate executor, durable state, independent stop and cleanup proof |

No completion percentage is assigned. The first release gate is **accepted inspection and persistence**, not a claim of operational readiness.

## 2. Product boundary

The console stores scenario definitions, execution records, evidence, validation runs and reports. It can load each record type in a versioned JSON bundle. It also collects inventory snapshots from administrator-configured connections. The interface does not accept AWS access keys, arbitrary endpoints, socket paths, kubeconfig uploads, shell scripts or executable assertion expressions.

The delivered backend reads metadata and evaluates provided scalar values. It does not generate application traffic, query CloudWatch metric history, run Prometheus queries, observe incident acknowledgements, reconcile database transactions or invoke FIS. Those operations need additional connectors and controls, not merely interface buttons.

A standalone HTML file provides the complete interface as a preview. A local service is required for operating-system sockets, SDK credentials and durable storage. The preview is not a browser-based AWS administration client.

## 3. Architecture and trust boundaries

The local service has four responsibilities: serve the single-page interface, enforce the interchange contract, perform bounded inspections and evaluate saved records. A single process owns the SQLite database. There is no cloud-hosted control plane or hosted application database.

| Component | Location | Authority and persistence |
|---|---|---|
| Browser | Operator workstation | Token in memory; display/import/export; no cloud keys; preview records only in memory |
| API and evaluator | Local Python process or container | Authenticate local requests; schema/ref checks; deterministic evaluation; local writes |
| AWS inspector | Backend process | SDK profile/credential chain; expected-account check; configured read operations |
| Docker/Podman inspector | Backend process | Four fixed GET routes through configured Unix socket; socket authority remains a significant risk |
| Kubernetes inspector | Backend process | Trusted explicit context or in-cluster service account; namespaced metadata reads |
| Record store | Local directory or persistent volume | SQLite database containing records, origin metadata, hashes and audit events |
| Export/backup files | Operator-selected local destination | Sensitive portable copies; operator controls encryption and retention |

AWS authentication uses the backend's SDK credential provider. It checks STS identity rather than trusting a profile label. STS identity success is not proof of access to the requested services; each collection scope records its own outcome. [S1–S2]

One inspection is allowed at a time in this process. It is a synchronous request, not a durable job. A process crash during collection can lose the unfinished snapshot; completed snapshots are transactional. The interface's last-snapshot timestamp is not a continuously checked connection-health claim.

## 4. Application views and operator workflow

| View | Decision it supports | Controls and explicit failure states |
|---|---|---|
| Overview | What evidence exists, and what prevents the next gate? | Counts, latest snapshots, deployment coverage, findings, audit; no composite readiness score |
| Connections | Which identity and scope will be inspected? | Configured accounts/Regions or local context; inspection confirmation; identity mismatch, missing credential and access-denial errors |
| Inventory | What was actually read? | Snapshot selector, model/search filters, resources and coverage; denied/error/truncated scopes remain visible |
| Scenarios | What behavior is being tested, for which models? | Draft/specified status, assertions, procedure, recovery, sources, JSON revision editor |
| Execution records | What happened during this attempt? | Scenario and snapshot references, scope, targets, state, interval, evidence; evaluate but not execute |
| Validation runs | Which assertions passed, failed or lack usable evidence? | Per-check reason, gates, evaluator version and input hashes; re-evaluation makes a new record |
| Reports | What conclusion can be shared without losing limitations? | Frozen result, linked validation, JSON dependency export and escaped HTML |
| Goal & roadmap | What is delivered and what has highest next value? | Ranked increments with exit evidence and dependencies |
| Data & security | How is data loaded, protected and recovered? | Import preview/commit, JSON export, SQLite backup, configuration guidance, sources and audit |

Normal live workflow: configure a connection outside the browser; unlock the workspace; inspect; review gaps; create an observation run from a snapshot; evaluate collection coverage; save a report. That report says whether the selected inventory collection was complete, **not** whether the application survived an incident.

The incident workflow begins with imported execution and evidence records. The operator selects the run, reviews evidence provenance, evaluates its pinned scenario, then creates a report. Imported validations are not silently recalculated or promoted to trusted results. Re-evaluation produces a distinct local validation and still identifies imported inputs.

The preview uses clearly marked examples to exercise the same navigation. A backend failure never loads synthetic resources as a fallback. Empty live views are empty; they do not display invented progress.

## 5. Record model and interchange

Every record has `kind`, stable `id`, positive `revision`, `title`, `simulated` and typed `data`. Its reference is `kind:id@revision`. Revisions are immutable: identical re-import is idempotent; changed content under an existing reference fails. Editing creates a new revision rather than changing historical evidence.

| Kind | Meaning | Required relationship |
|---|---|---|
| `scenario` | Hypothesis, applicability labels, procedure, evidence requirements, recovery checks and scalar assertions | Standalone definition |
| `snapshot` | Observed identity, requested scope, coverage, whitelisted resource summaries and collection interval | Standalone observation |
| `execution_run` | A particular collection or externally executed incident attempt | One exact scenario revision; optional exact snapshot |
| `evidence` | A measured scalar with unit, source, sample count, scope and time window | One exact execution run |
| `validation_run` | Evaluation of an execution record against its pinned assertions | Exact run/scenario, check results, gates and content hashes |
| `report` | A frozen conclusion and limitations | Normally a validation reference; unlinked imported reports allowed but unverified |

The API, not the imported file, assigns origin metadata. A record can be catalogue, collected, imported, locally evaluated or derived from an import. Synthetic status remains visible. A supplied verdict does not acquire authority because its JSON is valid.

Bundles are JSON only, version `1.0`, with at most 5,000 records and a 5 MiB upload limit. YAML, archives, raw FIS templates and older report-data files are not accepted as interchangeable formats. The supplied catalogue is the explicit migration of the earlier 36 scenarios. No arbitrary code, HTML component or query is executed from an import.

Import checks include schema, bounded values, timestamps, duplicate JSON property names, duplicate references, changed revisions, missing dependencies, dependency kinds and optional content-hash manifest. All records commit together or none do. Dependencies may be in the existing workspace or the same bundle, regardless of bundle order. The schema is generated from the same Pydantic models used by the API.

Numeric values must be finite and in the JavaScript-safe integer range. Unit labels are matched literally, not converted. SHA-256 hashes cover canonical record content; they are integrity checks, not digital signatures. A local administrator can alter the database and audit history. Signed provenance and independent retention are later production requirements.

## 6. Validation semantics

This release evaluates `lte`, `gte` and `eq` comparisons against numeric or boolean values. Boolean comparisons allow only `eq`. It does not infer a metric from logs or run user-provided formulas. Each assertion declares its metric, threshold, unit, category, required/optional status, minimum sample count and maximum collection lag.

Evidence must refer to the selected run and match its exact scope, simulation flag, unit and value type. Its measurement window must equal the run interval; this deliberately simple first-release contract does not model separate baseline, impairment and stable-recovery windows. Collection must occur after the window ends, within the assertion's lag allowance and not in the future. Historical evidence is not invalid merely because the run happened months ago; the original collection lag remains the check.

Multiple evidence records for the same metric are ambiguous unless the caller selects an explicit evidence set. There is no implicit average, deduplication or “latest wins.” A selected set with missing metrics remains incomplete.

Evaluation has two levels:

1. **Execution gates:** a terminal completed run, specified scenario with assertions, consistent simulation flags and, for a fault scenario, explicit confirmation that the fault occurred. Invalid gates make the overall result inconclusive while retaining individual check findings.
2. **Assertion outcomes:** with valid gates, any failed required assertion makes the result fail. Otherwise missing or unsuitable required evidence makes it inconclusive. Only all required assertions passing yields pass. Optional checks do not determine the overall outcome. No required assertions cannot produce pass.

A known failure is not erased because another check is missing. Equally, absence of a detected failure is not evidence of success. Reports include the evaluator version, exact input hashes and limitations. `fault_confirmed` is still an input claim until an independent fault-event collector exists. A source string and a sample count are not independently authenticated in this release.

Current evidence values can represent latency, error fractions, recovery duration or response timing, but the evaluator cannot establish whether those values were correctly derived. Next-stage collectors must retain numerator, denominator, sampling interval, missing samples, query, raw values and a separate business-transaction reconciliation result.

## 7. Deployment coverage and limits

The inspector intentionally preserves distinctions rather than labelling every container as equivalent.

| Deployment model | Delivered inventory evidence | Not established by that evidence | Next applicable incident family |
|---|---|---|---|
| EC2 / Auto Scaling | Instance state/type/AZ/lifecycle; ASG capacity, membership count and zones | Healthy target routing, replacement timing, spare capacity or application health | Single instance loss, replacement under load, selected capacity shortage |
| EKS on EC2 | EKS cluster plus managed node-group metadata | Self-managed node membership, actual pod placement, PDB behavior or injector readiness | Worker loss, pod disruption, selected dependency failures after prerequisites are proven |
| EKS on Fargate | Fargate profile configuration, distinct from node groups | Actual scheduled pods or support for an EC2-style host/injector action | Supported application/dependency actions; reject node/privilege assumptions |
| ECS on EC2 | Service capacity configuration and explicit running-task launch type | Host-to-task dependency, task fault sidecar or graceful draining behavior | Task loss separately from EC2 host loss; qualified task-level stress |
| ECS on Fargate | Explicit launch type or all-Fargate service strategy; task summaries | Task-action opt-in/sidecar/network prerequisites or any access to the managed host | Task loss or supported task fault; no EC2 host action assumption |
| Lambda | Function metadata including runtime/package, memory, timeout and version | Layer/extension readiness, event-source behavior, idempotency or downstream correctness | Qualified delay/error experiments and business side-effect checks |
| Docker / Podman | Engine version, containers, volumes and networks | Workload health, volume contents, recovery automation or API write isolation | Local process/network faults only after a separately approved worker exists |
| Kubernetes | Namespaced pods, deployments, StatefulSets, DaemonSets, Services and PVCs | Cluster-wide placement, storage durability, secrets, logs or fault-controller permissions | Namespace-scoped workload incidents after eligibility checks |

EKS control planes and unresolved/mixed ECS capacity strategies remain shared/unclassified. An EKS Fargate profile is configuration, not proof that a particular pod uses it. ECS task records retain their own launch type. AWS documents action-specific EKS, ECS and Lambda prerequisites; the future applicability engine must evaluate these rather than map a model label directly to an executable action. [S3–S6]

Shared AWS reads currently cover RDS instance/cluster metadata, load balancer metadata, CloudWatch metric alarms, and FIS action definitions/template summaries. They do not fetch actual metric series, alarm delivery, target health, all managed-service dependencies or regional failover readiness. Other services from the research catalogue remain scenarios without corresponding inventory collectors in this release.

Collection is bounded: one to three Regions per configured AWS connection; five pages or 1,000 items per list operation; 20,000 resources per snapshot; a cooperative 120-second deadline. An in-flight SDK call can complete after the deadline. Nested listing structures and client response limits mean “complete” means complete for the configured bounded read, not a universal account census. Inaccessible or capped scopes are recorded, not converted to empty-success results.

Docker/Podman uses four fixed unversioned compatibility GET routes; real engine-version acceptance is pending. Kubernetes uses at most ten configured namespaces, bounded pagination and TLS verification. A named Kubernetes context can still refer to a remote cluster; the administrator must prove that it is the intended local environment.

## 8. Storage and recovery design

The authoritative store is `workspace.sqlite3` under `CONSOLE_DATA`. It contains normalized record JSON, hashes, origin metadata and local audit events. The process uses one database writer with transaction locking and rollback journaling. There is no Redis, external SQL server or cloud storage requirement. The database file is created with mode 0600; host/volume access, snapshots and backups remain administrator responsibilities.

Docker/Podman uses a named volume; Kubernetes uses a PVC with one replica and Recreate rollout. A PVC's name does not prove that its backing storage is local or suitable for SQLite: verify the provisioner, filesystem semantics, node-loss behavior and backup method. [S13]

The backup endpoint uses SQLite's backup API to produce a consistent database copy. Restore is an operator-controlled offline procedure; the API does not accept an uploaded database file. [S14] JSON exports are portable record sets, not full audit/config backups. Configuration and external credentials must be restored separately. There is no automatic retention or encryption. Raw attachments, trace files and large metric series require a future content-addressed local evidence store rather than expansion of the JSON scalar contract.

If the console shares the failure domain being tested, local control and evidence can disappear together. That is acceptable only for read-only setup checks. Before executing faults, keep the controller, backup and stop path outside the selected target set. “All data local” must not be interpreted as permission to destroy the only evidence copy in the experiment.

## 9. Future execution design — specified, not implemented

A future run has separate planning and execution states: `draft → preflight → blocked | awaiting_approval → approved → baseline → fault_active → recovery_observation → validating → closed`. Any active phase can transition to `stop_requested → cleanup → closed` or `cleanup_required`. These states require a versioned schema migration; they are not silently accepted by the current five-state execution record contract.

Before approval, resolve immutable resource identifiers from a recent snapshot; verify action support, ownership, prerequisites, limits, workload profile, recovery procedure and evidence queries. Hash the complete plan and resolved targets. An approval applies to that hash and expires; a changed target list invalidates it. The inspector role must never acquire execution permissions as a side effect of planning.

A separate worker obtains a restricted execution identity and persists the external experiment ID before retrying. Use idempotent start semantics and reconcile unknown outcomes before any second start. Store every transition and remote event. A browser disconnect does not cancel or restart a fault implicitly.

The stop path must work independently of this UI and local worker. FIS account/Region safety levers can stop running experiments and prevent new starts; they do not replace per-experiment controls or an approved cleanup procedure. [S8] Stopping a fault is not equivalent to restoring service or recreating a deleted resource. Validate post-actions and business recovery before closing the run. [S7]

The first executor acceptance is one supervised, low-blast-radius non-production experiment. Multi-step AZ impairment, destructive storage scenarios, regional failover and unattended campaigns remain blocked until their own recovery and evidence requirements have been accepted.

## 10. Value-ranked delivery sequence

1. Accept real inspection, persistence and restore: without trusted scope, every later conclusion is ambiguous.
2. Convert catalogue drafts into scoped definitions and eligibility checks: prevent unsupported or underspecified plans.
3. Collect workload, incident and data-correctness evidence: establish measurable impact before adding faults.
4. Execute one supervised non-production incident with a separate worker: prove safety and lifecycle correctness.
5. Integrate responder events and stable business recovery: test the operating model, not only infrastructure.
6. Add repeatable campaigns and matched regression comparisons: increase frequency only after reproducibility.
7. Qualify production and multi-account use: security review, separation of duties, signed evidence and account-specific approval.

See `ROADMAP.md` for deliverables and binary exit evidence. Work on responder evidence can start alongside telemetry; fault automation does not need to block importing real supervised drill records.

## 11. Acceptance and nonfunctional limits

The current test suite covers schema and immutable storage, evaluation edge cases, authenticated API flows, escaped reports, backup restoration, selected AWS SDK-stub paths, fixed Unix-socket reads and Kubernetes SDK doubles. Browser checks exercise interface behavior separately. `VALIDATION.json` distinguishes actual tests from mocks and unperformed deployment work.

No AWS account, Docker/Podman daemon or Kubernetes cluster was connected during delivery. Container builds, image pull policies, real credential refresh, actual runtime versions, persistent-volume ownership, performance under large workspaces and recovery during host failure require field acceptance. The Kubernetes client dependency was not installed in the delivery environment; its adapter was exercised with test doubles, not a live SDK connection.

Initial bounds suit a single operator and a bounded account, not an enterprise asset index. The API returns the workspace as a whole; the interface caps initial inventory rendering but this is not server-side paging. Large histories need pagination, indexing, archival and retention before wider rollout. Multi-user authorization, accessibility certification, penetration testing, dependency-vulnerability review and production service-level commitments are not claimed.

## Sources

Primary documentation reviewed on 21 October 2026. These sources establish platform behavior; design choices and implementation boundaries above are specific to this delivery.

- [S1 — Boto3 credential providers](https://docs.aws.amazon.com/boto3/latest/guide/credentials.html)
- [S2 — STS GetCallerIdentity](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetCallerIdentity.html)
- [S3 — FIS action reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html)
- [S4 — FIS EKS pod actions](https://docs.aws.amazon.com/fis/latest/userguide/eks-pod-actions.html)
- [S5 — FIS ECS task actions](https://docs.aws.amazon.com/fis/latest/userguide/ecs-task-actions.html)
- [S6 — FIS Lambda actions](https://docs.aws.amazon.com/fis/latest/userguide/use-lambda-actions.html)
- [S7 — Stopping FIS experiments](https://docs.aws.amazon.com/fis/latest/userguide/stop-experiment.html)
- [S8 — FIS safety levers](https://docs.aws.amazon.com/fis/latest/userguide/safety-lever.html)
- [S9 — Docker daemon protection](https://docs.docker.com/engine/security/protect-access/)
- [S10 — Podman system service](https://docs.podman.io/en/latest/markdown/podman-system-service.1.html)
- [S11 — Kubernetes kubeconfig trust](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
- [S12 — Kubernetes RBAC practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/)
- [S13 — Kubernetes persistent volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [S14 — SQLite backup API](https://www.sqlite.org/backup.html)
