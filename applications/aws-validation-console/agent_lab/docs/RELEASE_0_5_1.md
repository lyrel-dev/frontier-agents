# 0.5.1-dev — integration and publication review

This revision includes the previously local-only 0.5.0 account onboarding, guided measurement-plan preparation, native FIS selector/multi-account execution, and business-requirement validation. It adds these review corrections:

* Configuration activation is blocked while a preview is stopping and while any pending or uncertain provider intent exists, even if its entity state is stale.
* A persisted but undispatched preview intent rechecks approval expiry. Cancelling it cannot dispatch a new preview. Known remote previews remain tracked after local attachment errors.
* Native trials compare the actual FIS execution snapshot with the approved action parameters, dependency graph, target definition, role, stop conditions, and account-targeting options. Mismatch requests stopping/restoration of the owned operation. The comparison is detective; it is not a preventive IAM boundary.
* Target-account evidence comes from the experiment's account configurations, not from a later mutable template read.
* A complete, proven no-response failure remains auditable without demanding nonexistent task/journal records or inventing a correct diagnosis. Missing delivery, ambiguous correlation and unavailable evidence still block that interpretation.

The first native repository run exposed a setup-test wait helper that requested JavaScript string evaluation under CSP. The helper now polls through the browser protocol, as the existing response test does. The application Content Security Policy is unchanged; native acceptance still fails rather than falling back to DOM injection.

## Reproducible acceptance

Run the existing Python, native-browser, worker HTTP and Docker checks. The additional `tests/observability_acceptance.py` starts the actual empty application, Prometheus 3.15.1 and Grafana 13.2.4 in a disposable, isolated Docker network namespace. It checks authenticated scraping, executes all baseline panel queries in Prometheus and through Grafana, imports/reads back the generated dashboard, and verifies that no incident measurements were created. It is not a test of real AWS metric content.

The workflow records native browser results and the precise built image IDs. A required dependency that is unavailable fails the job; no check is silently skipped. Provider responses in unit/workflow tests remain isolated fixtures. No credentials or real account bindings are included.

## Definition of Done

Software and hosting acceptance do not establish a working production incident route, action permissions, correct Agent Space diagnosis, transaction reconciliation or prevention effectiveness. Authorized live-account trials and independent evidence review are still required. An absent live trial is not replaced by an empty dashboard or a passing fixture test. The full live product DoD remains open.

Official contracts used for the execution check:

- https://docs.aws.amazon.com/fis/latest/APIReference/API_GetExperiment.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_Experiment.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentTargetAccountConfigurations.html
- https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html
- https://prometheus.io/docs/prometheus/latest/querying/api/
- https://grafana.com/docs/grafana/latest/developer-resources/api-reference/http-api/
