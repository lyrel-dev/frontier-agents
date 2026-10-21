# Roadmap ordered by value

**Goal:** demonstrate how the deployment and its operators respond to controlled incidents, using attributable measurements rather than resource-state inference.

**Reanchored baseline:** the earlier 36 research scenarios remain drafts. This delivery adds a runnable read-only console, local record storage, import/export, scalar evaluation and reports. It does not add fault execution or live incident telemetry. No account or runtime has been accepted in the delivery environment.

The order reflects dependency and reduction of decision risk, not a fabricated numerical ROI. Independent work on responder evidence may proceed alongside telemetry.

## 1. Prove inspection and local persistence

**Value:** Establish which account and runtime were actually read, what was missed, and whether evidence survives restart.

**Deliverable:** Accept the shipped read-only collectors against one real AWS account and one local runtime; test the storage and restore path.

**Exit evidence:** Account mismatch blocks collection; denied and truncated reads remain visible; a snapshot survives service restart; a SQLite backup restores the same record hashes.

**Current status:** Code delivered · live acceptance pending.

**Dependency:** Administrator-provided identity, namespace/socket access and persistent storage.

## 2. Turn catalogue entries into scoped test definitions

**Value:** Prevent a plausible scenario description from being treated as an executable or applicable test.

**Deliverable:** A scenario editor and applicability engine with six AWS deployment profiles, exact targets, dependency proof, concrete limits and evidence queries.

**Exit evidence:** Unresolved limits, incompatible actions, empty target sets and stale snapshots block planning. The 36 research scenarios remain drafts until specified.

**Current status:** Schema delivered · applicability engine next.

**Dependency:** Accepted inventory and workload ownership.

## 3. Collect incident evidence under a known workload

**Value:** Measure customer impact and recovery instead of inferring them from resource state.

**Deliverable:** Bounded k6/Locust traffic, CloudWatch/Prometheus collectors, UTC incident events, transaction reconciliation and local raw-evidence retention.

**Exit evidence:** Baseline, impairment and recovery windows are reproducible; denominators and missing samples are explicit; evidence links to one run and exact target scope.

**Current status:** Scalar evaluation delivered · collectors planned.

**Dependency:** Specified scenarios and approved observation endpoints.

## 4. Execute one supervised non-production fault

**Value:** Close the loop from approved plan to observed incident without creating an uncontrolled executor.

**Deliverable:** A separate write-capable FIS worker with durable run state, idempotency, target-hash approval, independent stop monitoring and cleanup verification.

**Exit evidence:** A single approved low-blast-radius test completes; retries do not duplicate the fault; losing this console does not remove the stop path; incomplete cleanup blocks closure.

**Current status:** Not implemented.

**Dependency:** Evidence collectors, least-privilege execution role and tested recovery procedure.

## 5. Validate responder actions and business recovery

**Value:** Distinguish infrastructure restoration from a resolved operational incident.

**Deliverable:** Alert-delivery and acknowledgement events, runbook evidence, escalation timestamps, business-transaction checks and repeat-test comparison.

**Exit evidence:** Detection, acknowledgement, mitigation, stable recovery and data correctness each have attributable evidence or an explicit inconclusive result.

**Current status:** Designed · not integrated.

**Dependency:** An approved incident drill and access to the incident system.

## 6. Run repeatable campaigns and compare regressions

**Value:** Show whether releases improve or weaken the same tested behavior.

**Deliverable:** Persisted campaign schedules, workload/version pinning, trend views and release gates based on matched scenarios and complete evidence.

**Exit evidence:** A campaign resumes after restart without duplicate execution; comparisons reject mismatched scope or scenario revisions; missing evidence cannot satisfy a release gate.

**Current status:** Planned.

**Dependency:** Reliable single-run execution and reproducible evidence.

## 7. Qualify production and multi-account use

**Value:** Expand only after identity, failure containment and operational controls have been demonstrated.

**Deliverable:** Separate inspection/execution identities, multi-user approvals, signed evidence, retention policy, restore drills and account/Region-specific safety controls.

**Exit evidence:** A security review and production game-day acceptance approve each account, Region and fault class; no approval is inherited merely from a non-production pass.

**Current status:** Not authorized by this release.

**Dependency:** Non-production acceptance and organization change approval.

## First implementation backlog

The immediate backlog is deliberately narrower than the full product:

| Item | Owner role | Acceptance artifact |
|---|---|---|
| Approve one AWS inspection identity and one local scope | Account/runtime administrator | Effective identity, scoped permission review and configuration with no secrets |
| Exercise each intended connector against known resources | Platform engineer | Snapshot, expected-versus-observed comparison, explicit coverage gaps and actual versions |
| Demonstrate persistence and restore | Workspace operator | Before/after record-hash manifests and integrity check |
| Select one service and specify one incident | Service owner | Exact scenario revision, targets, workload, limits, recovery procedure and evidence queries |
| Add a read-only telemetry collector | Application/SRE engineer | Raw measurement provenance, complete windows, known-value tests and missing-sample behavior |

Do not add a fault-start control until the executor has its own accepted safety and recovery design. Do not mark the collection milestone as operational-readiness validation.