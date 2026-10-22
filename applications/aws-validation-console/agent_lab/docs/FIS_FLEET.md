# AWS FIS account catalogue and agent-response campaigns

Version 0.5.1-dev makes the AWS/FIS view the default console. It discovers existing AWS definitions, registers bounded measured-response campaigns, and dispatches qualified trials through the existing FIS executor. It does not create or modify experiment templates, grant IAM permissions, or supply artificial incidents or measurements.

## Connect the account set

Use Guided setup to propose and separately approve `fis_accounts` in the persisted workspace configuration. Local JSON remains an optional bootstrap method. Each entry has a stable local ID, expected 12-digit account ID, SDK profile and explicit Region list. The same account/Region cannot appear twice. Profile-based role assumption and SSO remain SDK/host configuration; no access key, profile path, endpoint override or role session is accepted from the browser. Account IDs and sanitized scope are visible only after local authentication.

The default GUI path requires no JSON editing; select installed SDK profiles and review the exact proposal. `config/fis-accounts.template.json` remains available only for optional bootstrap automation. An explicit account set can exist without any executable agent/workload binding. If `fis_accounts` is empty, the console derives the unique account/Region scopes from its existing agent/workload bindings. The distributed configuration contains neither accounts nor bindings.

Start the durable worker and API with `python run.py --config config.local.json --with-worker`. Open the loopback URL and unlock with the operator token. `/` is the AWS view; `/response` retains detailed diagnosis, intervention and prevention controls. The worker must remain running for discovery and campaign progression.

## Discover definitions, not alleged readiness

**Discover all configured accounts** queues a resumable read job. For each account/Region the backend verifies STS identity before FIS access, enumerates all `ListExperimentTemplates` pages, reads each definition with `GetExperimentTemplate`, and enumerates target-account configurations for multi-account templates. It also enumerates `ListExperiments` history pages. Historical execution summaries are inventory, not automatically benchmarked evidence.

Each scope retains its cursor, source responses, request identifiers when supplied by AWS, content hashes and errors. A worker restart reuses the cursor and verifies identity again. One denied account does not hide successfully read accounts. Deleted/unreadable definitions remain visible as incomplete rows. Requests are paginated up to the configurable `fis_discovery_max_pages` budget per scope; the default is 1,000 pages, not 1,000 templates. Budget exhaustion, repeated tokens, failed detail reads and denied requests produce explicit partial/error coverage, never a fabricated empty success. Discovery is a sequence of reads, not an atomic AWS snapshot. The library shows the latest requested discovery; prior captures remain immutable in local storage.

The coverage claim is **all returned definitions in successfully enumerated configured accounts/Regions**. It is not an Organizations-wide inventory or a claim about Regions the administrator did not include. Discovery does not mutate AWS and yields to active trials, intervention and restoration work so bulk reads cannot delay the executor's observation/stopping loop.

## From a discovered template to an executable contract

Select **Inspect AWS definition**, then **Guided setup**. The form-based workflow selects actual Agent Space associations, approves a target preview, builds typed account-scoped verifiers, probe/incident/measurement requirements and reviewed runbooks, then commits the binding and immutable contract atomically. The older raw-contract attachment remains an advanced API compatibility path, not an operator prerequisite.

Guided native contracts support AWS-resolved dynamic selectors and multi-account definitions. Account-role maps, target envelopes, independent per-account checks and fresh dispatch previews are mandatory. See [ONBOARDING.md](ONBOARDING.md) and [NATIVE_FIS.md](NATIVE_FIS.md) for exact semantics. Legacy contracts retain their original explicit-target finite-action checks. The AWS template is not rewritten by either path.

## Orchestrate a campaign

Select template/agent-contract pairs in the library, register repetitions, actual-exposure comparability tolerance, pause-on-failure policy and a note about Agent Space history/carryover. At most 100 physical trials are enumerated. The plan pins definitions, bindings and source hashes before any trial begins.

**Activate queue** allows the durable worker to register and qualify the next child. It does not grant mutation authority. Each child waits at READY until a holder of the separate approval credential approves the exact action/target digest. The worker then runs the existing baseline, fresh FIS safety-lever guard, idempotent `StartExperiment`, resolved-target/effect checks, native incident correlation, independent probes and restoration. A fresh skip-all preview is checked before the separate run-all operation. Both provider IDs are retained; the actual fault-execution ID is shown in the queue.

The order is repeat-major and selection-order, with one physical exposure at a time across the workspace. Different agent contracts cause separate sequential replays; the console does not claim simultaneous observation or isolate other agents already monitoring the service. Incident routing and any independent agent actions must be controlled and recorded by the operator. Agent history is not reset.

A child ID is deterministic within the plan, so a worker restart between child creation and parent update does not produce a second trial. Dispatch uses the original executor's intent/idempotency/reconciliation logic. Only one campaign may own the queue. Pausing is transactionally checked again when a child starts, including attempts made through the original trial API. Unknown remote outcomes and unresolved restoration block progression.

**Pause future dispatch** does not stop an exposure already running. **Cancel queue** requests abort of the active child and waits for its terminal cleanup state; unresolved restoration cannot be labelled successful cancellation. Pause-on-failure defaults on. Failed and incomplete attempts remain in the campaign and cannot be deleted to improve results.

## Benchmark the agent, not FIS completion

**Freeze benchmark report** creates a new immutable result from the current plan and pinned assessments. It includes every planned slot, including never-started, aborted, blocked, failed and inconclusive attempts. FIS action completion, native response and diagnostic correctness remain separate outcomes.

For latency summaries, a qualified exposure must be closed, the actual FIS execution completed, and its challenge, measurement, native delivery and cleanup requirements passed. A response failure with confirmed delivery remains a qualified failure; its missing task latency is not zero. Actual fault duration and delivered request count must also be present. Within each registered cohort, subsequent qualifying attempts are compared to the first qualifying attempt using the preregistered tolerance; materially different exposure or traffic is excluded with a retained explanation.

Cohorts hash workload account/Region/service, FIS definition content, fault target/check configuration, probe, measurement requirements and native route reference. Different cohorts are not pooled. Agent account/Region/space is a separate grouping key. Same-cohort groups can be inspected side by side, but fixed order and shared history prevent an automatic causal ranking.

The report supplies planned/registered/started/qualified counts, response and diagnosis distributions, response-pass fraction, measured no-response failures, and per-metric sample count, missing count, median and nearest-rank p95. Latency quantiles condition on available observations, not all attempts; counts make that denominator explicit. Small samples do not support a confidence or generalization claim. Interactive graphs retain one point per measured trial; isolated scalar observations are not turned into trends. CSV exports all attempts. JSON includes plan and source hashes plus captured trial projections.

Configured data-correctness, collateral-regression and application requirements retain independent verdicts and metric definitions in the report. Correct diagnosis still requires the existing grounded review. Benchmarks do not convert task creation into correct reasoning, service recovery into agent-attributable remediation, or a response campaign into evidence of prevention. The existing recommendation/change/replay workspace remains available for prevention testing.

## API and IAM

All `/api/fis/*` routes use the existing same-origin bearer-token boundary and body limits. Account configuration remains administrator-controlled. The discovery-policy starter is `deploy/fis-discovery-policy.json`; it grants FIS list/get and STS identity reads only. Execution uses the separately approved fault profile, FIS execution role and existing exact-approval controls. No IAM policy is attached automatically.

Endpoints: `GET /api/fis/accounts`, `POST /api/fis/sync`, `GET /api/fis/catalog`, `POST /api/fis/contracts`, `GET/POST /api/fis/campaigns`, `GET /api/fis/campaigns/{id}`, `POST /api/fis/campaigns/{id}/command/{activate|pause|resume|cancel}`, `POST /api/fis/campaigns/{id}/benchmark`, and `GET /api/fis/benchmarks/{record}/csv`. Records and existing trial approval/evidence endpoints remain available. Generated schemas define the POST contracts.

## Acceptance boundaries

Credential-free tests cover pagination, scope failures, resume, multi-account discovery, explicit execution blockers, approval gates, queue races, original provider-operation identity and benchmark denominators. Browser acceptance reports identify native navigation versus the limited bridge harness. Provider fixtures remain under tests and are excluded from the runtime image.

No user account, Agent Space, incident route, IAM efficacy or real agent performance has been exercised during development. The live acceptance gate still requires authorized account configuration, independent emergency recovery, a controlled native-response trial and review of actual evidence. Software CI is not that acceptance.

## Primary AWS contracts reviewed

- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperimentTemplates.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_GetExperimentTemplate.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListTargetAccountConfigurations.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_ListExperiments.html
- https://docs.aws.amazon.com/fis/latest/APIReference/API_StartExperiment.html
- https://docs.aws.amazon.com/fis/latest/userguide/experiment-options.html
