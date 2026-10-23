# 0.5.2-dev — preview cancellation and recovery

Source baseline: `cfc9b6b76843b208dc4a605cc2a81bf80f0e15ef` on
`feat/aws-fis-console-delivery`. This follows the published 0.5.1 integration,
native-browser, container, and monitoring acceptance; it is not a migration from
an uncommitted package. No live AWS result is claimed.

## Correctness changes

Preview cancellation and first dispatch now share a SQLite transaction boundary.
The broker rechecks the queued owner, unmodified approval subject, unexpired
approval, pending intent and skip-all request while reserving dispatch. A cancel
that wins before that reservation prevents StartExperiment. A cancel after it
records a stop request; it does not assert that the request was never sent. The
original provider identity and idempotency token remain authoritative.

The guard runs after the safety-lever read. Approval expiry or cancellation while
that read is outstanding cannot be ignored by a stale worker snapshot. An
approval is expired at its exact expiration timestamp, not just afterward.

When AWS has accepted a preview but local attachment of its identity fails, the
worker recovers the provider ID and original intent timestamp. The timestamp is
explicitly labelled as a timeout basis, not an actual AWS execution start. This
prevents an endless STOPPING loop caused by missing local timing metadata.

Disabling new AWS writes does not prevent reconciliation or stopping a known
preview. STOPPING cannot be promoted to a successful preview merely because AWS
then reports natural completion. An unexpected actions mode requests a stop of
the owned operation and never supplies an admissible preview result.

The admissible preview result and terminal entity are also committed in one
transaction. Cancellation observed before this commit cannot be overwritten by
late result publication; failed publication leaves no orphan approval envelope.

These are local-controller guarantees. The reservation transaction does not make
an AWS request transactional, freeze resource selectors, prove action permissions,
or establish cloud-side fault recovery. Restrictive IAM roles and independent
stop/restoration controls remain required.

## Reproducible regression checks

`tests/test_preview_lifecycle.py` adds 19 fixture-only regressions covering cancel
before/after reservation; stale worker state; exact expiry and expiry during a
read; interrupted provider attachment; stop with writes disabled; unexpected
mode; malformed authority; independent database readers; API authentication; cancellation during terminal verification; and atomic result publication rollback.
The fixtures make no AWS requests and are not included in the runtime image.

Run the full required workflow for this exact commit, not the parent revision.
The workflow includes native response/FIS/setup/typed-form browser checks,
measured loopback worker checks, actual Docker hosting and actual authenticated
Prometheus/Grafana integration. Source and generated acceptance evidence are
retained separately by CI. A test infrastructure failure must fail the job.

## Scope and live acceptance

The account onboarding, native single-/multi-account FIS execution, guided
measurement setup, response benchmark and recommendation/change/replay workflows
remain present. The application still starts empty with new AWS writes disabled.
The full live product DoD remains open until authorized account/incident trials,
action permissions, native delivery, diagnosis quality, independent business
measurement producers and prevention efficacy have been assessed.

Official FIS semantics used in review:
- https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_GetExperiment.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_StopExperiment.html
