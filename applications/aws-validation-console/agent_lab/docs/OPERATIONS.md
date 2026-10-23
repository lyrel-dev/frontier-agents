# Current preparation path

Use [Guided onboarding](ONBOARDING.md) for accounts, native previews and the measurement plan. [Native FIS](NATIVE_FIS.md) specifies selector and multi-account scope; legacy direct contracts remain isolated.

# Operator procedure and state meanings

## Before enabling execution

Confirm ownership of the non-production service, target resources and traffic path. Select a representative GET business operation that is safe to repeat; an HTTP 200 from a static health page does not establish business recovery. A JSON predicate can validate a returned business property. The initial workload adapter is a bounded single-path GET probe (maximum 5 requests/second), not a production-scale load generator, write/reconciliation harness or arbitrary script runner.

Runbook state checks must interrogate the deployed resource state, not rely only on a successful Automation status. Store the reviewed source/deployment artifact and diff digest in the runbook contract. The worker executes only fixed parameters and numeric document versions. Add a separately reviewed rollback instrument for effects requiring rollback.

The local machine must reach the workload's approved CIDRs, the AWS endpoints and its own local volume. DNS answers are checked and the socket is pinned to an approved address. TLS still checks the original hostname. Redirects, proxies from environment, metadata/link-local addresses, raw response-body storage, are not supported. Guided probe URLs and CIDRs require an exact separately approved configuration; an unapproved URL is never probed.

## Response sequence

`DRAFT → QUALIFYING → READY → BASELINING → EXPOSING → OBSERVING → CLEANING → SETTLING → FINALIZING → CLOSED`

Qualification captures account/association reads, exact template content, approved target policy and native runtime budget, stop alarms, baseline resource checks, incident-alarm enablement and registered document hashes. It is not an IAM simulator and cannot establish the result of a future AWS write.

The baseline must satisfy the registered error/latency limits and delivered-request minimum for every bucket. A missing or late probe slot is not silently backfilled. The worker qualifies the template again before starting the fault. The actual FIS experiment ID and resolved resources are retained. A changed target set, failed/skipped required action or worker gap prevents a successful completed exposure.

The incident clock uses the first qualifying selected alarm transition after exposure. Native task candidates must match the configured reference exactly and be created in the relevant interval. Multiple candidates are ambiguous. A manual task-ID form is deliberately absent. Linked investigations retain their original task and effective-task lineage; findings older than the new incident task are not treated as a newly published response.

The configured delivery receipt is **sender evidence**, not AWS-signed proof. The optional `integration/delivery_receipt.py` helper formats a receipt only after the existing sender has an actual acceptance response. It does not send an incident or alter delivery. Do not insert a successful receipt to compensate for a failed integration.

No-task response failure requires an independently correlated acceptance receipt, a complete final source collection, no observation gaps, and expiry of the full response deadline measured from acceptance. An incident accepted near the observation boundary is inconclusive until its deadline is observable. Exactly correlated tasks without a receipt may support task timing but cannot prove the full delivery path.

If you use assisted mode, the worker creates an INVESTIGATION task with a unique trial-marked title and the original persisted client token. Expected cause/rubric are not sent. Assisted mode is labelled separately and cannot establish automatic incident triggering.

## Stopping and unresolved state

- **ABORTING / CLEANING:** stop the owned FIS experiment if still active, settle concurrent interventions, run only originally approved cleanup, and verify actual restoration. FIS StopExperiment is not a rollback guarantee.
- **UNKNOWN_REMOTE_STATE:** a write may have been accepted. Do not re-create the operation. The worker reconciles discoverable FIS/task identities. For an uncertain Automation, obtain the actual execution ID independently; the console verifies pinned document/version/parameters and the operation's tags before resuming. A missing ID is not proof that no action occurred.
- **RESTORE_REQUIRED:** new trials are blocked. Use independent cloud-side recovery and any approved rollback. After verification, request **Recheck restoration**. This reuses the original stop/cleanup authorization, not an arbitrary new command.
- **CLOSED_ABORTED / CLOSED_BLOCKED:** retain the attempt. A numerical chart does not upgrade a blocked or aborted lifecycle into a qualified prevention pair.

If the local host disappears, use the pre-established cloud-side stop alarms and FIS controls. Action durations, where present, do not prove restoration. A native operator deadline cannot constrain lasting or one-shot effects when the local host is absent. Stop/cancel only your owned experiment/execution unless the account-level emergency procedure explicitly calls for the broader FIS safety lever. Test this procedure before relying on the console.

## Diagnosis and intervention

The oracle is frozen before the exposure, including expected affected resources, causal mechanism code, independent read verifiers and review rubric. Fault effect must be verified independently before a diagnosis verdict is available. The reviewer quotes what the agent actually claimed and the relevant independent response. The system checks citations, resource/cause equality and declared unsupported claims. It does not understand all natural-language nuance or provide independent expert review.

An implementation proposal cites actual agent output and maps it to a fixed registered instrument. The approval shows document/version/content hash, parameters, implementation artifact/diff and rollback. An operator-controlled SSM Automation implementation is **agent-assisted**, not autonomous agent execution. Interrupted Automation is not assumed rolled back; unresolved effects block the environment.

## Prevention

The campaign plan is frozen before baseline attempts. Evaluation uses actual baseline investigation task IDs, not seeded history. AWS may return no recommendation; that remains observable rather than generating a local substitute. Recommendations are retrieved by exact returned version and checked against the evaluation task and Agent Space ARN.

A change must be independently verified before replay and still present after replay. Comparison checks exact target equality; a replacement resource is not automatically comparable. Changing a parameter that incidentally removes the original target does not establish prevention. Review a new design when the architecture changes target identity.

All attempts are retained. Chronological baseline/replay pairing is deterministic; unpaired attempts and disqualified trials are reported. No statistical confidence is manufactured from one pair. Use more pairs and an appropriate external design for causal or generalization claims. Agent history is not reset; disclose carryover.

## Storage, restart and backup

SQLite uses a local filesystem and WAL. API and one worker share the same directory; the worker holds an OS file lock. Do not use multiple workers on network filesystems. Keep the workspace directory private and encrypt the underlying host/volume if needed. The application does not itself encrypt SQLite.

Use **Download SQLite backup** for a consistent online backup. To restore: stop API and worker, preserve the current workspace, replace the database with a verified backup, remove stale WAL/SHM only while all processes are stopped, fix ownership/mode, then start one worker. Reconcile every previously active/uncertain provider operation before starting new work. Restoration of the local DB does not revert AWS.

JSON exports are evidence exports, not executable imports or a database-restore endpoint. Definitions can be imported through their strict schema. No measured-result import path can silently award an agent outcome.
