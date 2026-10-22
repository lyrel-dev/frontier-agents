# Guided onboarding: real accounts to executable trials

The AWS workspace's **Guided setup** view is part of the same SPA and shares its in-memory operator session. `/setup` exposes the same components independently. Configuration is versioned in local SQLite, not written to AWS. Account IDs, operational descriptions and captured source responses are sensitive: protect the volume and exports.

## 1. Install credentials outside the console

Install the required SDK profiles on the host or carefully scoped container filesystem. Authenticate SSO/role profiles with your organization's normal tools. The browser can select only profile names reported by the local SDK; it accepts no access key, secret, session token, arbitrary credential path or custom AWS endpoint.

Keep the Agent Space's own AWS service access role separate from console access. Use distinct observer, FIS executor, Automation executor and optional task-creator profiles. A local operator can possess both console tokens; this is not enterprise separation of duties.

## 2. Connect the account set

In **Accounts**, enter a stable local connection ID, display name, expected 12-digit account ID and explicit Regions. Select the observer profile. On the template-owner account, select a separate FIS execution profile. Save a proposal, inspect its exact configuration and approve with the local approval token.

**Test reads** verifies STS before service reads and returns each attempted FIS/Agent Space read with a bounded error code and guidance. A workload account need not host an Agent Space; its Agent Space read may be unavailable while its FIS reads succeed. No test claims write permission. Wrong account or root identity prevents further reads.

Changes use optimistic revision checks and a database transaction. They are rejected while queued/running/READY work, uncertain operations or restoration work could be affected. Existing trials retain a frozen binding. API and worker load an approved revision from the same database; no process-specific manual JSON edit is necessary.

The global AWS-write switch is an explicit, separately approved configuration change. Enabling it does not approve a preview, exposure, evaluation or runbook. Keep it off during initial read setup.

## 3. Discover the agent and its account relationships

Choose the agent account and Region, then **Discover Agent Spaces**. The backend reads actual spaces and AWS-account associations. Select the space that monitors the service and the association for the primary workload account. For a multi-account template, select an observer connection and the corresponding existing association for every additional target account.

These selections are reverified at qualification. A visible association is configuration evidence, not proof of incident delivery or successful investigation. The console does not onboard those accounts into DevOps Agent on your behalf.

## 4. Discover FIS definitions and preview targets

Run **Discover all configured accounts**. The worker enumerates templates and execution summaries with resumable pagination. Inspect account/Region coverage before relying on the catalogue; denied or truncated scopes are not empty inventories.

Select a captured definition. Review its actions, target selectors, role, stop conditions and target-account configuration. Approve **Target preview** with its exact digest and confirmation. This starts an AWS `skip-all` experiment through the selected executor profile, records its provider ID and captures the returned target identities. No fault actions execute in that mode. The job can be cancelled; uncertain dispatch remains subject to reconciliation.

Only a complete successful preview can prepare a native execution contract. No-target, malformed or wrong-account results remain blocked. AWS changes after the preview require revalidation. The preview may incur service/telemetry costs; it is not an offline simulation.

## 5. Prepare the measurement plan in forms

**Service and scope:** name the real monitored service and deployment model; select the agent, primary target account and all additional account observers. The template-owner/orchestrator may be different from all workload accounts.

**Exposure:** choose exact target matching or an explicitly approved subset of the captured preview; specify the minimum population, runtime deadline, independent recovery procedure and action-specific safety review. This does not broaden the preview into every resource that might later match a tag. New targets require new qualification.

**Business path:** enter the approved HTTPS GET URL and CIDRs, expected status/JSON predicate, request rate and timeout. DNS and TLS remain checked. This probe is controlled traffic, not a production-scale load engine; external real workload metrics may also be collected.

**Resource checks:** choose the observer account, AWS service and allowlisted read operation. The form creates typed parameters from the installed SDK schema, including structures, lists and maps. Select a result expression, comparison and expected state. Assign check IDs to baseline, applied-effect and cleanup phases. Test a read to inspect its actual result before using it. Every target account must be represented in all three phases. A lifecycle label or static parameter claiming success is not a sufficient recovery verifier.

**Incident route:** name the existing workload alarm and the exact external reference system/reference-ID rule used by its current incident integration. Optional receipt mapping uses a JMESPath expression over a real sender log event. Supply the real log-group names. Correlation does not rely on approximate timestamp overlap. The console does not synthesize successful delivery receipts or create a fallback investigation in native mode.

**Business and collateral requirements:** add actual CloudWatch metric namespaces, names, dimensions, units, statistics, account scope and period. Define maximum/minimum/sum/last across complete closed buckets, comparator, limit, minimum sample count and interpretation. A data-loss metric must come from a separately verified reconciliation process; its name alone does not prove correctness. Choose aggregation appropriate to the metric's semantics—do not sum a cumulative gauge or average percentiles.

**Diagnosis and response:** register the hypothesis, ground-truth resource identities/mechanism, required independent check IDs, response deadline, traffic/error/latency limits and stable-recovery duration. Previews use actual returned resource identities; non-ARN target information remains explicit rather than inventing an ARN.

**Changes and prevention:** optionally select the requester/change profiles and read an existing Automation document by actual ARN and numeric version. Review its content/hash, fixed parameters, implementation artifact/diff, before/after checks and rollback reference. The execution adapter accepts restricted linear documents, not arbitrary scripts or text from agent findings. Registration is not execution approval.

## 6. Review, activate and operate

Review the proposal's account map, exact FIS content fingerprint, preview envelope, measurement contract and safety requirements. Approve local activation. The binding and immutable experiment revision are committed atomically. No fault is sent by activation.

Return to **FIS library** without leaving the SPA. Select the newly mapped template/Agent Space contract; register repetitions, comparison tolerances and history/carryover notes. Activate the queue. Each child qualifies and waits for its own exact exposure approval. The worker performs a new skip-all preview before the run-all operation and rechecks actual scope during execution.

Use **Response / prevention** to inspect captured journals, adjudicate a diagnosis with exact source quotations, propose approved changes, request an actual evaluation, select a recommendation version and compare a verified replay. The agent's output never becomes an unrestricted command.

## CLI and review exports

The CLI is optional; it uses the same persisted configuration as the SPA. After choosing an actual experiment record in the UI:

```sh
python acceptance.py preflight --data data \
  --experiment-ref 'experiment:YOUR_ID@YOUR_REVISION' --read-aws \
  --output local-acceptance/read-checks.json

python acceptance.py audit --data data --trial "$BASELINE_TRIAL_ID" \
  --campaign "$CAMPAIGN_ID" --output local-acceptance/evidence-audit.json
```

Use the actual references from your workspace. Preflight is not a start token. Audit reads a consistent database copy, preserves failed conclusions and cannot certify producer authenticity. Protect all exports; do not upload credentials or real operational captures to the source repository.
