# 0.5.1-dev — integration and publication review

This revision includes the previously local-only 0.5.0 account onboarding, guided measurement-plan preparation, native FIS selector/multi-account execution, and business-requirement validation. It adds these review corrections:

* Configuration activation is blocked while a preview is stopping and while any pending or uncertain provider intent exists, even if its entity state is stale.
* A persisted but undispatched preview intent rechecks approval expiry. Cancelling it cannot dispatch a new preview. Known remote previews remain tracked after local attachment errors.
* Native trials compare the actual FIS execution snapshot with the approved action parameters, dependency graph, target definition, role, stop conditions, and account-targeting options. Mismatch requests stopping/restoration of the owned operation. The comparison is detective; it is not a preventive IAM boundary.
* Target-account evidence comes from the experiment's account configurations, not from a later mutable template read.
* A complete, proven no-response failure remains auditable without demanding nonexistent task/journal records or inventing a correct diagnosis. Missing delivery, ambiguous correlation and unavailable evidence still block that interpretation.

The first native repository run exposed a setup-test wait helper that requested JavaScript string evaluation under CSP. The helper now polls through the browser protocol, as the existing response test does. The application Content Security Policy is unchanged; native acceptance still fails rather than falling back to DOM injection.

## Guided setup navigation correction

Native browser acceptance exposed a race in the setup view: navigation kept the previous form editable while configuration reads were outstanding. The completed read then replaced that form, discarding input entered in the meantime. The view now removes obsolete controls immediately, marks loading explicitly, and ignores responses for superseded navigation. Locking invalidates outstanding navigation and pending API responses as well. A successful response arriving after lock cannot restore account proposals or private setup state. Approval dialogs remain open until the updated configuration is loaded, so a refresh cannot discard new input.

The guided browser suite delays real HTTP reads and completes them out of order. It checks that controls become available only after the current stage has loaded and that a late older response cannot erase newer input. It still uses the served Content Security Policy in native mode. Test diagnostics retain bounded errors and field-validity metadata, not credential field values.

## Complete resource-parameter forms

The add-check control remains disabled until the read-operation catalogue is available. Failed catalogue reads can be retried without discarding the plan. Changing a service or operation clears the old parameter editor; delayed schema responses cannot attach fields for a previously selected operation.

The SDK input descriptor no longer silently truncates nested structures at five levels. It preserves the full supported input shape, including CloudWatch metric-query dimensions. A recursive or over-budget shape is rejected explicitly instead of becoming an incomplete form. Model checks cover every allowlisted read operation, and a separate native-browser check edits nested CloudWatch dimension fields through the served application.

## Atomic trial finalization

The real-worker acceptance run exposed a terminal-state race: CLOSED was committed before the evaluator attached the assessment. A concurrent reader could see a closed trial without its result, and a process interruption in that interval could strand the result permanently. Finalization now computes against the intended terminal state and commits the assessment, its pinned probe capture reference, the terminal state and journal events in one local transaction. The revision and verified cleanup are rechecked before commit. An interruption before that commit leaves FINALIZING for the replacement worker; no second FIS start is issued.

Tests inspect the database through a separate reader before commit, inject a failure inside the transaction, reject stale/mismatched inputs, and restart finalization after an interrupted evaluation. The local transaction does not make AWS mutations transactional or replace provider-operation reconciliation.

## Reproducible acceptance

Run the Python suite and the native-browser checks, including `python tests/sdk_form_browser_checks.py --native`, followed by worker HTTP and Docker acceptance. The additional `tests/observability_acceptance.py` starts the actual empty application, Prometheus 3.15.1 and Grafana 13.2.4 in a disposable, isolated Docker network namespace. It checks authenticated scraping, executes all baseline panel queries in Prometheus and through Grafana, imports/reads back the generated dashboard, and verifies that no incident measurements were created. It is not a test of real AWS metric content.

The workflow records native browser results and the precise built image IDs. A required dependency that is unavailable fails the job; no check is silently skipped. Provider responses in unit/workflow tests remain isolated fixtures. No credentials or real account bindings are included.

## Definition of Done

Software and hosting acceptance do not establish a working production incident route, action permissions, correct Agent Space diagnosis, transaction reconciliation or prevention effectiveness. Authorized live-account trials and independent evidence review are still required. An absent live trial is not replaced by an empty dashboard or a passing fixture test. The full live product DoD remains open.

Official contracts used for the execution check:

- https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_GetExperiment.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_Experiment.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentTargetAccountConfigurations.html
- https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html
- https://prometheus.io/docs/prometheus/latest/querying/api/
- https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/

## Catalogue refresh and monitoring transport

The catalogue now preserves search and account/Region filters in authenticated in-memory view state. A delayed return-from-setup refresh or periodic refresh cannot clear those inputs; locking clears them. Native acceptance explicitly delays the catalogue response while the operator changes the search.

Monitoring acceptance no longer assumes host NAT mappings exist on Docker's internal bridge. The application, Prometheus and Grafana share an internal network namespace with no published host ports. Fixed Python HTTP assertions run inside that namespace; the request credentials travel through stdin, not process arguments or error logs. The test still exercises real authentication, scraping, every baseline PromQL expression, Grafana dashboard import/readback, and Grafana datasource queries. Thirteen transport checks cover allowed endpoints, actual HTTP authentication, retryable unavailability, malformed results and credential-safe errors.
