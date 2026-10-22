# Next target: live two-account acceptance

Current source is the 0.5.1-dev implementation based on `feat/aws-fis-agent-benchmark` at b9dc5393. See DELIVERY_ACCEPTANCE.md for publication and live acceptance status. The previous workbench and its results remain separate.

## Gate 1 — read qualification

Use the actual account A / Agent Space and account B / service configuration. No account IDs, credentials, experiment definition or measurements are included. Keep local configuration and acceptance exports out of Git.

```sh
# Offline: validates the chosen configuration and definition, but makes no AWS request.
python acceptance.py preflight --config config.local.json \
  --experiment experiment.local.json --data data --output local-acceptance/plan.json

# Operator-initiated AWS reads; still no fault, runbook or agent-task creation.
python acceptance.py preflight --config config.local.json \
  --experiment experiment.local.json --data data --read-aws \
  --output local-acceptance/read-checks.json

# Optional: also send exactly one configured business-path GET, not a load test.
python acceptance.py preflight --config config.local.json \
  --experiment experiment.local.json --data data --read-aws --probe \
  --output local-acceptance/read-and-path-checks.json
```

For GUI-created plans, use `--experiment-ref experiment:ID@REVISION` instead of `--experiment`; the CLI loads the active approved workspace configuration. The optional experiment file uses the existing `Experiment` contract (generate `schemas/experiment.schema.json` with `python build_assets.py`). It must name configured fault/probe IDs, actual resource ARNs, a diagnosis oracle and service-owned limits. Registration can also be performed in the console; preflight does not register or start a trial.

The read check verifies both STS identities; the existing association; pinned native FIS/target-account configuration (or legacy duration-bounded FIS) and required Automation documents; baseline resource checks; incident and stop alarms; the FIS safety lever; and bounded reads of the configured incident sources and metrics. Configured metric windows with missing/partial data block the check. A native delivery receipt source is required: an alarm alone cannot establish accepted incident delivery.

`fis:GetSafetyLever` is an additional read permission for the workload fault profile. The command only reads the `default` lever; it never disengages it. `engaged`, `engaging`, denied or unknown states block qualification. An administrator must decide whether an engaged lever should remain engaged. Do not change it merely to satisfy a test.

Read profiles can incur the normal AWS read/telemetry costs. This is an application-level read-only path, not an IAM permission boundary. Use least-privilege profiles. Read success does not establish write permission, safety of fault effects, credential refresh or the incident route's behavior under failure.

Reports have configuration, experiment and source-code hashes, collected source references, a timestamp and a fifteen-minute expiry. They are **not approval tokens**. The trial's existing qualification and exact approval still run independently; an expired or successful preflight cannot bypass them.

Exit status 0 means the requested read checks completed. Status 2 means blocked/incomplete. Offline plans intentionally return 2 because AWS was not checked. No output file is overwritten. Reports are created with mode 0600. The distributed empty configuration produces a truthful blocked report without constructing an AWS client.

## Gate 2 — authorized native-response trial

After independent review of IAM, emergency stopping and cleanup, run one bounded non-production trial through the console. Preserve actual delivery receipts, resolved targets, independent fault-effect checks, native task/journal responses, probe observations, diagnosis adjudication and verified restoration. Do not replace missing evidence with manual values or an assisted investigation.

No account binding or target authorization was supplied in the development session. This gate has not been executed against AWS. CI uses fixtures only and cannot close it.

## Gate 3 — recommendation, verified change and comparable replay

Register the campaign before baseline. Obtain an actual agent evaluation, pin a recommendation version, deploy an exact approved implementation, verify changed state, and run the qualified replay. Retain the independent intervention actor and all aborted, failed and excluded attempts. A failed prevention result is a result, not a reason to omit the attempt.

## Gate 4 — audit the retained evidence

```sh
python acceptance.py audit --data data --trial "$BASELINE_TRIAL_ID" \
  --campaign "$CAMPAIGN_ID" --output local-acceptance/evidence-audit.json
```

`--campaign` is optional for a response-only audit. The command takes a consistent SQLite copy through a read-only source connection, checks pinned hashes, source-account/request metadata, response dimensions, restoration and uncertain provider operations. It never runs the evaluator again, queries AWS or rewrites the workspace.

`reviewable` means that the checked local evidence is present and consistent; it does **not** mean that the agent passed, that records were independently authenticated, or that live acceptance is certified. Assessed response and prevention failures remain failures in the output. Unassessed diagnosis, unproved native delivery, missing hashes, mismatched inputs and unqualified comparisons remain blocked. Source IDs and hashes are not signatures: an independent reviewer must verify provenance against AWS and approve the final scope-limited conclusion.

## Known boundaries

No native incident, agent diagnosis, runbook intervention or prevention replay was executed against the user's AWS accounts during development. Credential refresh, external emergency recovery and production IAM efficacy remain operator acceptance obligations. The current adapters are intentionally limited; see [COVERAGE.md](COVERAGE.md).

Official API contracts reviewed for this addition:

- https://docs.aws.amazon.com/devopsagent/latest/APIReference/API_GetAssociation.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_GetSafetyLever.html
- https://docs.aws.amazon.com/fis/latest/userguide/safety-lever.html
- https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_MetricDataResult.html
