---
schema_version: "1.0"
document_type: "workstream_handoff"
workstream_id: "aws-fis-devops-agent-validation-console"
title: "AWS FIS / AWS DevOps Agent Operational Validation Console"
as_of_date: "2026-10-23"
repository:
  full_name: "lyrel-dev/frontier-agents"
  branch: "feat/aws-fis-console-delivery"
  application_directory: "applications/aws-validation-console/agent_lab"
  documentation_path: "applications/aws-validation-console/agent_lab/WORKSTREAM.md"
  verified_implementation_commit: "f9cb84f9ade33fbe1f15ff33d661969b828d7fe9"
  verified_ci_run_id: 39911813772
  verified_ci_url: "https://github.com/lyrel-dev/frontier-agents/actions/runs/39911813772"
  default_branch_affected: false
release:
  version: "0.5.2-dev"
  stage: "development"
  software_ci: "passed_for_implementation_commit"
  aws_live_acceptance: "not_run"
  full_definition_of_done: "open"
  starts_with_aws_writes_enabled: false
  starts_with_seeded_customer_or_synthetic_results: false
objective: "Measure whether an AWS DevOps Agent Space detects, investigates, diagnoses, contributes to recovery from, and helps prevent incidents in authorized services when exposed to controlled AWS FIS experiments; retain independently verifiable evidence and uncertainty."
product_roles:
  primary_fault_executor: "AWS Fault Injection Service"
  subject_under_test: "AWS DevOps Agent in its existing Agent Space"
  orchestration_and_evaluation: "Local API, durable worker, evidence evaluator and benchmark"
  persistence: "Local SQLite with immutable source-pinned records"
  observability: "CloudWatch, independent HTTP probes, optional existing incident logs, Prometheus/Grafana outputs"
environment_scope:
  agent_account: "Operator-configured Agent Space account (account A or another reviewed account)"
  orchestrator_account: "Operator-configured FIS template owner/orchestrator account"
  workload_accounts: "Explicitly approved target accounts (one or more; account B and optionally others)"
  regions: "Explicitly configured AWS Regions; native multi-account FIS stays within a template Region"
  execution_environment: "Authorized, non-production workload initially"
  credentials: "Locally managed SDK/SSO profiles; never browser-entered AWS keys"
current_capabilities:
  - id: "CAP-01"
    name: "Versioned multi-account onboarding and qualification"
    status: "implemented_ci_verified"
  - id: "CAP-02"
    name: "Paginated FIS template, target-account and execution-history discovery"
    status: "implemented_ci_verified"
  - id: "CAP-03"
    name: "Approved skip-all target previews and native single/multi-account execution"
    status: "implemented_ci_verified_not_live"
  - id: "CAP-04"
    name: "Durable campaigns, original provider identity, cancellation and cleanup gates"
    status: "implemented_ci_verified_not_live"
  - id: "CAP-05"
    name: "Native incident correlation, agent evidence and human-grounded diagnosis review"
    status: "implemented_ci_verified_not_live"
  - id: "CAP-06"
    name: "Separated business/data/collateral, response and recovery verdicts"
    status: "implemented_ci_verified_not_live"
  - id: "CAP-07"
    name: "Recommendation, version-pinned implementation and comparable replay"
    status: "implemented_ci_verified_not_live"
  - id: "CAP-08"
    name: "Interactive metrics, evidence exports, authenticated Prometheus/Grafana contract"
    status: "implemented_ci_verified"
next_milestones:
  - id: "M1"
    priority: "P0"
    status: "blocked_external_authorization"
    goal: "Qualify real account set, IAM roles, selected Agent Space, incident route, recovery and measurement producers"
    evidence_gate: "G01"
  - id: "M2"
    priority: "P0"
    status: "not_run"
    goal: "Complete one approved real native FIS exposure and validate effect, stop and cleanup"
    evidence_gate: "G02"
  - id: "M3"
    priority: "P0"
    status: "not_run"
    goal: "Prove actual incident delivery and assess agent response and diagnosis without manual triggering"
    evidence_gate: "G03"
  - id: "M4"
    priority: "P1"
    status: "not_run"
    goal: "Exercise one real multi-account template with per-account effect and restoration evidence"
    evidence_gate: "G04"
  - id: "M5"
    priority: "P1"
    status: "not_run"
    goal: "Validate business correctness, metrics and evidence provenance against independent producers"
    evidence_gate: "G05"
  - id: "M6"
    priority: "P1"
    status: "not_run"
    goal: "Demonstrate a real recommendation, approved change, verified state and qualified replay"
    evidence_gate: "G06"
  - id: "M7"
    priority: "P2"
    status: "partially_verified"
    goal: "Accept intended host, credential renewal, backup/restore, stopping and host-failure recovery"
    evidence_gate: "G07"
  - id: "M8"
    priority: "P2"
    status: "not_run"
    goal: "Complete independent security/operations review and sign off the bounded product DoD"
    evidence_gate: "G08"
acceptance_gates:
  - id: "G01"
    status: "open"
    owner_role: "AWS/platform administrator"
    evidence: "Actual identities, associations, permissions, source availability, reviewed targets and independent stop/recovery plan"
  - id: "G02"
    status: "open"
    owner_role: "Resilience experiment operator"
    evidence: "FIS preview and run IDs, actual targets, workload degradation, stop/cleanup and restoration evidence"
  - id: "G03"
    status: "open"
    owner_role: "Incident operations and independent reviewer"
    evidence: "Correlated delivery receipt, real Agent Space task/journal, independently supported or refuted diagnosis, timing and impact"
  - id: "G04"
    status: "open"
    owner_role: "Multi-account platform owner"
    evidence: "Target-account role map, per-account observer/effect/cleanup proof, drift and failure handling"
  - id: "G05"
    status: "open"
    owner_role: "Service owner and SRE"
    evidence: "Approved business probes, validated metric denominators/reconciliation and required application/data/collateral results"
  - id: "G06"
    status: "open"
    owner_role: "Change owner and resilience reviewer"
    evidence: "Actual versioned recommendation, approved implementation, independently verified state, comparable replay and controls"
  - id: "G07"
    status: "open"
    owner_role: "Runtime/platform operator"
    evidence: "Intended host deployment, SSO/role refresh, restart/backup/restore, independent stopping and failure drills"
  - id: "G08"
    status: "open"
    owner_role: "Security and acceptance authority"
    evidence: "Reviewed IAM/trust, blast-radius bounds, private data handling, risk register and signed scope-limited decision"
limitations:
  - "Software and CI tests used AWS provider fixtures; no user AWS account or live Agent Space was tested"
  - "FIS skip-all preview is a real AWS API operation; it does not lock targets or prove action permissions"
  - "Actual target drift detection is detective; IAM execution roles must prevent unauthorized blast radius"
  - "FIS stop does not reverse prior resource changes; independent restoration must work without this console"
  - "No Organizations-wide enrollment, arbitrary-partition support, single cross-Region FIS experiment or parallel fault campaigns"
  - "GET business probes do not replace a full load tool or validated transaction reconciliation"
  - "A correct diagnosis needs source-grounded assessment; summary presence alone is not success"
  - "Small sequential agent cohorts with shared history cannot prove causal superiority"
documentation_sources:
  - "README.md"
  - "docs/ONBOARDING.md"
  - "docs/NATIVE_FIS.md"
  - "docs/FIS_FLEET.md"
  - "docs/BENCHMARK_CONTRACT.md"
  - "docs/DELIVERY_ACCEPTANCE.md"
  - "docs/RELEASE_0_5_2.md"
  - "validation/acceptance-traceability.json"
---
# Workstream handoff — AWS FIS / DevOps Agent validation console

## 1. Mission and acceptance target

Build and qualify an **AWS-centric, local-first operational validation console** that connects to an administrator-approved set of AWS accounts, discovers their existing AWS Fault Injection Service (FIS) templates and execution history, and orchestrates controlled experiments to **measure the response and prevention capability of an AWS DevOps Agent Space** monitoring services in other accounts.

The application is not the fault engine: **FIS owns fault injection**; **AWS DevOps Agent is the subject under test**. The console owns experiment scope, approvals, durable scheduling, independent observation, source-pinned evidence, evaluation and benchmarks. It must answer separately: Was a fault actually applied? Did it affect the business service? Did the normal incident integration deliver it? Did the agent investigate within the requirement? Was the diagnosis correct? Did an approved intervention help? Was the service restored safely? Did a subsequently implemented recommendation improve outcomes under a comparable replay?

**Product-level DoD:** An operator can use the UI to configure approved accounts and measured workloads; discover and qualify an existing FIS template; run an authorized native-response campaign; capture independently corroborated FIS, incident, agent and workload evidence; assess distinct response and recovery dimensions; and complete an approved recommendation-to-change-to-replay prevention trial. All failed, missing, excluded and unsafe attempts must remain visible. Software CI is necessary but **not sufficient**.

**Current state:** The 0.5.2-dev development source was verified by GitHub Actions on implementation commit f9cb84f9ade33fbe1f15ff33d661969b828d7fe9. **No real customer/account A/B incident or agent performance test has run; full DoD is open.** Do not turn a passing software check, a successful FIS API call, a healthy endpoint, or an agent summary into a readiness certificate.

## 2. Why this project exists

The effort began with research into open-source chaos engineering, load generators, AWS FIS and incident-response measures. An initial 0.2.x local workspace could inspect AWS and Docker/Podman/Kubernetes metadata and evaluate *supplied* evidence; it could not challenge an agent. This was explicitly rejected as insufficient. The 0.3.x response lab added a durable worker, actual local probes, an FIS adapter, native-incident correlation, diagnosis reviews, intervention handling and prevention replay. Version 0.4.x made FIS account/template discovery and agent-response campaigns the primary UI. Version 0.5.0 introduced guided onboarding and native, AWS-resolved, single-/multi-account FIS execution. Version 0.5.1 hardened UI loading, SDK-shaped forms, finalization, and real Prometheus/Grafana CI. Version 0.5.2 corrected preview cancellation, expiry, uncertain provider IDs, stop reconciliation and atomic publication.

The **legacy 0.2.1 workbench is separate** at applications/aws-validation-console; do not import its historical records or upgrade them to agent-response or prevention proof. This workstream lives at applications/aws-validation-console/agent_lab. Keep unrelated repository presentations, agents and content unchanged.

## 3. Architecture and identity boundaries

| Layer | Responsibility | Authority and constraints |
|---|---|---|
| AWS account set | Explicit expected 12-digit account IDs, Regions, profiles and enrollment coverage | STS identity checked; SDK/SSO credentials provisioned externally; no browser-entered AWS secrets |
| FIS orchestrator account | Owns authoritative templates and a native experiment | Template and target-account roles remain AWS-defined; UI never rewrites a template into a fake local fault |
| FIS target accounts | Hosts affected service resources; may be multiple accounts within one experiment Region | Each needs observer access, approved FIS role boundaries, independent baseline/effect/cleanup checks |
| Agent account / Agent Space | Monitors target service accounts through existing associations and incident routing | Existing service access role and route are separate from console observation/execution roles |
| Local console API and single durable worker | Guided setup, discovery, plan approval, queue, FIS operations, observation, evaluation | Private bearer/approval tokens, SQLite operation intents, one worker owner, no arbitrary shell or agent-prose execution |
| Evidence and monitoring | AWS source reads, CloudWatch, permitted HTTPS GET probes, task/journals, receipts, reports, Prometheus/Grafana | Preserve timestamps, source scope, query, coverage gaps, hashes and absent samples |

Account A (agent), Account B (monitored workload) and the FIS template owner may be different. Do not assume the Agent Space is in the FIS orchestrator account. AWS FIS multi-account experiments are bounded to the FIS template's Region; the Agent Space can reside in its configured Region. Access to an AWS account is *not* permission to inject a fault into it.

**Execution path:** approve a versioned plan → measured baseline → separately approved FIS skip-all target preview → verify exact/subset approved envelope, target-account role map and configuration fingerprint → fresh safety and approval checks → second preview just before dispatch → separately journaled run-all experiment → verify actual target information, action states and independent effect → observe the existing incident path, agent task and journals → verify service impact, business requirements and restoration → freeze distinct evaluation dimensions. Stop/reconciliation remains available when starting new experiments is disabled.

**Prevention path:** register comparison before baseline → obtain actual Agent Space EVALUATION and versioned recommendation → approve a fixed reviewed Automation implementation → independently verify changed state → repeat a comparable challenge and fault-free control when required → measure recurrence, impact or time-to-investigation *separately*. A recommendation merely marked implemented, or a PR merged, is not proof of prevention.

## 4. Non-negotiable invariants

1. A fresh install has **zero accounts, incidents, measurements, seeded results or passing badges**, and AWS writes disabled.
2. Browsers receive sanitized account metadata and local token authorization, **never AWS access keys**, arbitrary credential paths or unrestricted commands.
3. STS identity, exact account/Agent Space association, allowlisted instrumentation, required alarms and per-exposure approval are checked before cloud mutation.
4. FIS **skip-all preview is a real StartExperiment** and therefore requires approval, an idempotency token, a retained provider ID and stop/reconciliation handling. It is not an offline dry run or proof that run-all can execute actions.
5. Preview targets may drift before run-all. A fresh preview and subsequent actual-target checks are required; post-start detection cannot prevent first impact. Use restrictive IAM and independent cloud-side stopping to bound risk.
6. Persist intent before a provider write. A timeout or crash has an **unknown remote state** until reconciled; do not issue a second start solely because a local response is missing.
7. Cancellation, expiry and result publication are state transitions with explicit transaction boundaries. A stopping preview cannot later become an admissible successful preview merely from provider completion.
8. Pause/cancel stops **future** dispatch and requests stopping owned operations; stopping FIS does not reverse already completed effects. Unverified restoration blocks later unrelated experiments.
9. Native trials **must not create a manual INVESTIGATION task** to hide absent automatic delivery. Accepted delivery + complete observations + expired deadline may prove a no-response failure; missing delivery/collector evidence is not agent silence.
10. Keep **delivery, fault validity, business impact, response, diagnosis, intervention, attribution, data correctness, collateral effects, recovery and cleanup** separate. Missing required evidence is inconclusive; unconfigured dimensions are not assessed.
11. Reports preserve **every** scheduled and attempted trial, qualified and excluded denominators, actual FIS IDs, account/Region/target identities, evidence sources, evaluator version and source hashes. Hashes establish local consistency, not AWS-source authenticity.
12. Independent workload checks and cleanup apply **per affected target account**. A successful CloudWatch read or FIS terminal state is insufficient for a resilience pass.
13. No false causal ranking: experiments are sequential, agent history persists, cohort sample sizes may be small, and unrelated automatic recovery must not be credited to the agent.

## 5. Completed work versus accepted behavior

| Area | Committed implementation (software verification) | Still required to accept the product |
|---|---|---|
| Account onboarding | UI-selected local SDK profiles, expected accounts/Regions, Agent Spaces and secondary-account associations; versioned activation and read diagnostics | Real profiles/SSO refresh, role trust and least-privilege verification across every intended account |
| FIS catalogue | Per-account/Region paginated template definitions, target-account configs, execution summaries, resumable coverage and immutable source provenance | Real template enumeration and independent completeness check in the authorized account set |
| FIS native plan/execution | Approved previews, dynamic target information, same-Region multi-account definition support, fresh drift checks, original run-all provider identity, stop/reconcile gates | Live action-type prerequisites, execution-role efficacy, actual targets/effects, cloud emergency recovery and cleanup |
| Durable campaigns | Sequential owned queue, exact child approval, restart-safe intents and failure retention | Real interrupted-execution drill, recovery verification and complete attempted-denominator accounting |
| Agent response | Exact native incident correlation, task/journal reads, separated delivery/response/diagnosis/attribution | Prove the configured incident route really reaches the agent; adjudicate actual diagnosis against independent ground truth |
| Business and prevention | Configured closed-window metrics; application/data/collateral checks; evaluation/recommendation/change/replay workflows | Validate metric producers and transactions, execute reviewed change and qualified real replay plus benign controls |
| Interactive evidence | SQLite snapshots, graphical series with gaps, immutable exports, authenticated Prometheus contract and Grafana dashboard | Operational retention/backup and independent source reconciliation on target deployment |
| Runtime and CI | Python, native Chromium UI, loopback worker, actual Docker hosting and real empty Prometheus/Grafana server integration | Live AWS acceptance; Podman and Kubernetes hosting and managed credential refresh remain separately unverified |

**Verified implementation baseline:** branch feat/aws-fis-console-delivery, commit f9cb84f9ade33fbe1f15ff33d661969b828d7fe9; [GitHub Actions run 39911813772](https://github.com/lyrel-dev/frontier-agents/actions/runs/39911813772) completed successfully. That run recorded **288 Python tests, 31 response-browser, 43 FIS-browser, 33 guided-setup-browser, four typed-form-browser, nine actual local HTTP/worker, 15 Docker, and ten authenticated Prometheus/Grafana checks**. Browser checks used native HTTP navigation; cloud providers in unit tests were isolated fixtures. The monitoring tests deliberately used an empty exporter (not AWS telemetry). A later documentation-only commit requires its own CI to be reviewed; do not reuse this run as a test of a different code revision.

## 6. Roadmap ordered by value and prerequisites

| Order | Priority / gate | Next deliverable and execution plan | Exit evidence |
|---|---|---|---|
| 1 | **P0 / G01** | Obtain explicit approval for a non-production target, installed local SDK/SSO observer and FIS-execution profiles, account/Region list, Agent Space ID and its real cross-account association. Review separate recovery operator, IAM policies/trust, blast radius and existing native incident route. Use Guided setup and read-only preflight first. | STS/association provenance; exact template and account coverage; approved actions, stop alarm, restoration plan, verified metric/receipt sources. No write experiment yet. |
| 2 | **P0 / G02** | With separate approval, test skip-all preview cancellation, expiry, target/drift handling and independent stopping on the actual template. Then run **one bounded native-response fault** while maintaining real controlled traffic, preserve run-all FIS ID, actual resources and each target-account effect, and verify restoration. | Actual FIS action/target records, independent fault impact, complete probes and recovery proof; no unresolved operations or RESTORE_REQUIRED. |
| 3 | **P0 / G03** | Observe the **existing** incident route end to end without creating a substitute task. Capture sender receipt or rejection, exact reference, Agent Space task/journal, diagnosis claims, operator intervention and application state. Include one proven-no-response or impaired-delivery control when safe. | Attribution to actual source IDs; first detection/delivery/task/summary/correct-finding timestamps; accepted/failed/inconclusive reasons and independent ground truth review. |
| 4 | **P1 / G04** | Qualify a real same-Region multi-account template and repeat the above with every target role/observer/check; deliberately reject out-of-envelope targets in a non-disruptive test. | Target-account configuration identity, per-account effect and cleanup, drift and partial-account-access outcomes. |
| 5 | **P1 / G05** | Validate request populations, sampling periods, CloudWatch queries, business correctness/transaction reconciliation and collateral regressions; ensure missing buckets cannot pass. | Reviewed signal design and independent producer checks with closed-window data, sample counts and explicit outcomes. |
| 6 | **P1 / G06** | Register prevention campaign before first baseline. Retrieve a real versioned recommendation, review implementation/rollback, deploy with separate approval, verify state, replay matched exposure and execute benign control as applicable. | Source-pinned recommendation ID/version, change artifact/actor, before-and-after results with comparability and confounders retained; no unwarranted causal claim. |
| 7 | **P2 / G07** | Accept the selected local/container host, credentials refresh, backup/restore, worker crash/resume and cloud-side stop/cleanup if the local controller disappears. Add Podman/Kubernetes qualification only when they are selected deployment requirements. | Recorded host/restart/credential tests, restored database/evidence hashes, independent emergency-stopping procedure proven. |
| 8 | **P2 / G08** | Conduct security and operational acceptance, review unsupported AWS partitions/deployment modes, settle retention and audit policy, identify residual risks and sign an exact-scope release decision. | Independent review, complete G01–G07 evidence links, no critical unresolved restoration, documented exceptions and signed acceptance. |

These are **proposed ordered acceptance milestones**, not promised dates or evidence already obtained. Until G01 is satisfied, **do not dispatch** a real fault merely to make the dashboard non-empty. Later acceptance findings can create additional software defects; fix them with regression coverage and rerun all relevant suites.

## 7. Immediate next-operator checklist

- Review the current implementation commit and CI for the branch; compare its changed files with this handoff. Consult docs/RELEASE_0_5_2.md and docs/DELIVERY_ACCEPTANCE.md before declaring any gate closed.
- Launch the empty console locally. Add real, authorized SDK profiles on the host (or scoped container mount) and use **Guided setup** to select account IDs, Regions, real Agent Space associations and FIS template. Never commit profile files, account secrets, operational data or exported investigations.
- Keep AWS writes disabled while conducting role/identity reads. Validate current FIS definition, explicit target role map, workload behavior, sources for incident-receipt correlation and cloud stop condition. Supply service-owned limits and independent verifiers before approving an experiment.
- Prepare one approved **non-production** native-response trial. Ensure emergency recovery remains usable without this process. Obtain the separate preview and exposure approvals, record exact provider IDs and reconcile any ambiguous outcomes.
- Run a frozen evidence audit after cleanup; compare important events and measurements against AWS source systems. Produce a response verdict that preserves absent or contradictory evidence. Register the prevention comparison before any intervention/replay.
- Update this handoff's YAML milestone/gate states only when the corresponding **independent evidence** exists; name the source/ID/date of each closure. A green CI or “reviewable” hash audit is not sufficient.

## 8. Reproducing the baseline

From the repository root:

~~~sh
git fetch origin
git switch feat/aws-fis-console-delivery
git pull --ff-only origin feat/aws-fis-console-delivery
cd applications/aws-validation-console/agent_lab
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python build_assets.py
python -m pytest -q
python tests/browser_checks.py --native
python tests/fis_browser_checks.py --native
python tests/native_setup_diagnostics.py
python tests/sdk_form_browser_checks.py --native
python tests/worker_http_acceptance.py
# The following require a Docker engine and do not use AWS credentials:
python tests/container_runtime_acceptance.py
python tests/observability_acceptance.py
~~~

To run the empty application (no AWS calls with distributed configuration):

~~~sh
python run.py --with-worker
~~~

Open http://127.0.0.1:8787 and unlock with the private local operator token. Approval uses a separate token. Do not enable live writes until the P0 prerequisites, independent controls and explicit approvals are in place.

## 9. Source map and handoff evidence

| Path | Read it for |
|---|---|
| README.md | Default application behavior and minimal startup |
| docs/ONBOARDING.md | Account/profile/association selection, previews and form-based measurement contracts |
| docs/NATIVE_FIS.md | Native FIS target identities, multi-account roles, preview semantics, safety boundaries |
| docs/FIS_FLEET.md | Catalogue coverage, campaign queue and benchmark rules |
| docs/BENCHMARK_CONTRACT.md | Denominators, correctness metrics, missing-data behavior and prevention comparisons |
| docs/SAFETY.md and docs/PERMISSIONS.md | Execution roles, independent stop/recovery and credential authority |
| docs/DELIVERY_ACCEPTANCE.md and docs/ACCEPTANCE_GATE.md | Live DoD obligations and read-only qualification/audit commands |
| docs/RELEASE_0_5_1.md and docs/RELEASE_0_5_2.md | Latest corrections, scope and regression rationale |
| lab/ and tests/ | Runtime control-plane implementation and credential-free regressions |
| validation/acceptance-traceability.json | Detailed requirement IDs P01–P30; check live gate status before closure |
| .github/workflows/aws-fis-agent-benchmark.yml (repository root) | Exact CI checks for application-branch changes |

**Status vocabulary:** *implemented* = code exists; *CI verified* = named tests passed for the pinned code revision; *read-qualified* = configuration/source checks completed; *live-tested* = an authorized actual cloud experiment executed; *reviewable* = sufficient local evidence for independent audit, not a passing agent assessment; *accepted* = signed, scope-limited business and safety DoD with all required live evidence.

**Open risks and decisions:** Dynamic selectors may select new resources after preview; limit blast radius with IAM and stop alarms. A timed-out AWS call cannot be atomically combined with SQLite; preserve intents and reconcile original IDs. Self-healing, fault expiry and parallel responders confound causal attribution. Data-correctness assertions need trustworthy producer logic, not only metric names. Agent history and sequential trial order confound comparisons. Protect SQLite, logs and exports; hashes are not signatures. Stop/cleanup and proof of actual recovered business state are distinct.

**Do not silently claim:** universal AWS FIS action compatibility; Organizations-wide enrollment; every Region/partition; one multi-Region FIS experiment; concurrent randomized agent benchmarking; production load generation from a GET probe; automated semantic proof of diagnosis; causal agent-attributable recovery; permanent prevention from one replay; or closure of live acceptance from a passing CI run.

The next owner should advance **G01 (real safe account qualification)** first, preserve evidence and failed outcomes, and keep the full DoD open until explicit acceptance. No user AWS account identifiers, access keys or incident material belong in this source document.

