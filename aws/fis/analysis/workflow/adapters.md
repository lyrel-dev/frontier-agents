---
id: assessment-workflow-adapters
title: Observation and execution adapter contracts
status: reviewed-proposal
version: "0.2"
updated: "2026-11-05"
---

# Observation and execution adapter contracts

Provider operations use one core invocation contract, but their guarantees stay specific. “Query complete,” “alarm entered ALARM,” “SNS accepted publication,” “endpoint received a message” and “application processed it” are different claims. The model must preserve that distinction through collection, assertion and display.

All operation names below belong to the proposed product. They are not new AWS API names. The synthetic [catalogue](operation-catalog.json) and [examples](examples/) make their input/output shapes reviewable; no adapters are implemented here.

## 1. Common adapter contract

An adapter declares its immutable code and schema identity, trusted effect classification, permission scope, execution budget, retry policy, resume checkpoint schema and cancellation/reconciliation capabilities. Operationally consuming an SQS message is not a side-effect-free read. Catalogue capabilities must describe such effects even when the adapter's assessment purpose is observation.

The runtime interface is `start(resolvedInput, context, dispatchKey)`, `resume(checkpoint, context)` and `cancel(intent, checkpoint, context)`. Start/resume return either a durable pending checkpoint or a terminal execution result. Cancel returns a cancellation observation; it does not itself prove a terminal remote state. Resuming or polling does not allocate a new StepAttempt.

The server authenticates provider context, validates output schemas and applies its own assessment reducer. A plugin cannot write the Run verdict, alter the criterion denominator, change a pinned predicate or bypass a scope hold. Adapter errors include category and retry eligibility. The catalogue classifies `observe`, `mutate` and `compensate`; it also declares specific side effects such as consuming a dedicated queue or starting a billed query.

An `Observation` contains `value`, `evidenceIds`, `collection`, `coverage`, `scope`, `window`, `observedAt` and `source`. `value` is absent when collection is unavailable, not a fabricated empty array. A completed empty result is explicit. Raw provider records are retained or referenced, while normalized values declare their conversion and schema.

## 2. AWS FIS

`aws/fis.start` accepts an authorized connection binding and a template ID. It records its dispatch intent and calls native StartExperiment with a stable token where supported. The output identifies the experiment and its known source timestamps. Local submission time, provider start time and observation time are separate; `submittedAt` is not renamed `startedAt`.

`aws/fis.ensure-stopped` accepts a **StepRef** (`runId`, `stepKey`), not only a successful start's output. It inspects that step's attempt and intent facts, including a zero-attempt case, and can therefore reconcile an ambiguous start whose response was lost. It uses retained intent/native identity, requests native stop where necessary and polls until a terminal provider state is observed. Missing identity after an ambiguous dispatch is unknown. A proven zero-dispatch result uses `remoteDisposition: none`, the StepRef and `reasonCode: NOT_DISPATCHED`; it needs no invented effect key. Terminal/unknown remote observations require the real `originEffectKey`. Reissuing Start after cancellation is forbidden. If a safe lookup cannot resolve the ambiguity, finalization is incomplete.

FIS experiment actions remain provider-owned children keyed by experiment identity and action name. The adapter cannot independently retry or stop one of them. A workflow retry around FIS Start can create another complete experiment and therefore requires an explicit adapter-safe policy. The existing [FIS report](../report.md) contains the native operation and field inventory, including stop behavior, preview limits and the lack of generic per-resource fault results. [StartExperiment](https://docs.aws.amazon.com/fis/latest/APIReference/API_StartExperiment.html) · [StopExperiment](https://docs.aws.amazon.com/fis/latest/APIReference/API_StopExperiment.html)

## 3. CloudWatch Logs Insights

`aws/cloudwatch.logs.query` starts a bounded query, persists the native query ID, polls its status and retrieves all applicable result pages within the configured limits. A `Running` result is partial. `Complete` does not establish that the adapter has consumed all returned pages. Current Logs Insights QL results support pagination; language-specific behavior belongs in the adapter, not the generic workflow core. [GetQueryResults](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetQueryResults.html)

The evidence records exact query text, language, account/Region, log groups, time window, query ID, scan statistics, result limit, pages consumed, truncation and observation cutoff. Query completion does not prove that every source emitted/ingested all relevant records. Missing logging configuration, ingestion lag, dropped source records or sampling can make a negative assertion inconclusive.

The [error-budget example](examples/logs-error-budget.yaml) requests a typed count and asserts against it. Normalization requires exactly one parseable numeric aggregate row. A missing/malformed count is unavailable/schema-error evidence unless the adapter has a documented query-specific empty-result normalization rule. It is not silently zero. The example does not claim to prove a global error budget from arbitrary application logging.

## 4. CloudWatch alarms and notification receipt

An alarm's current state does not identify which transition caused a notification. The experiment should verify an OK precondition, arm the observation source, trigger the perturbation, collect a transition and a receiver receipt, then evaluate them as separate required criteria.

CloudWatch alarm notifications provide identifying fields such as alarm ARN, old/new state and state-change time. CloudWatch documents notification publication to configured SNS topics, with possible out-of-order publication even for FIFO topics. A workflow run ID is not automatically injected into that payload. Correlation must use actual alarm/transition/topic/receiver facts plus a bounded isolated window. [Alarm notification schema and behavior](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Notify_Users_Alarm_Changes.html)

| Claim | Evidence needed | What is insufficient |
| --- | --- | --- |
| Alarm entered ALARM | A specific alarm transition within the required window | A later current state without transition context |
| Publication to a topic was recorded | Relevant publication audit or producer observation in the correct scope | A receipt from a different alarm or topic |
| SNS handed off to the endpoint | Endpoint-specific delivery evidence | A successful alarm evaluation alone |
| The selected receiver received the notification within 60 seconds | A trusted receiver receipt timestamp correlated to the exact transition/topic/receiver | The payload's alarm timestamp or an SQS receipt handle alone |
| The application processed the notification | Application acknowledgement or durable business-effect evidence | Endpoint delivery or queue receive alone |

SNS delivery status logs can establish endpoint response and handoff timing for supported endpoint types. They do not, by themselves, prove a downstream application's business processing. Logging configuration and sampling remain part of coverage. [SNS delivery status](https://docs.aws.amazon.com/sns/latest/dg/sns-topic-attributes.html)

### Complete notification example

The [alarm-delivery scenario](examples/alarm-delivery.yaml) declares every input and connection binding. `capture.open` establishes a bounded, durable observation session before injection and returns only when ready. It records receiver identity, subscription/topic identity, start cursor, coverage capabilities and lease expiry. Its output handle is an operational reference retained by the attempt, not a seventh public domain aggregate. A production implementation must persist and recover that session; naming it a handle is not an implementation of durability.

The capture session is specifically **the receiver being assessed**. A dedicated SNS-to-SQS probe subscription proves delivery to that probe, not to an existing production Lambda, email address or HTTP endpoint. To claim production receiver delivery or processing, instrument that exact receiver and bind its evidence source. The observer must never compete with the production consumer by draining its queue.

SQS ReceiveMessage changes visibility and may return no messages even when some exist. An empty poll is not proof of absence. Capture may acknowledge only its dedicated queue under explicit adapter policy, after evidence is durably stored. Dedupe uses durable message/source identities, not receive receipt handles. [ReceiveMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html)

`capture.collect-alarm` returns typed observations for two claims: a transition occurred within 180 seconds after the provider-established execution boundary, and the selected receiver received the matching notification within 60 seconds of that transition. It collects from the previously armed session, so a receipt arriving before the collect step starts is still included. It waits through the applicable decision window plus a declared collection grace period, without treating that grace as a source completeness guarantee.

The adapter must distinguish clocks: `occurredAt` for the alarm transition, `receivedAt` assigned by the trusted receiver, and `observedAt` when this workflow ingests the receipt. A late-ingested record with an on-time trusted `receivedAt` can satisfy the deadline if collected before the sealed cutoff. A record received after the deadline cannot. Clock uncertainty is retained; if it crosses the deadline boundary the time-based conclusion is inconclusive.

Each claim includes normalized matching `records` and its own coverage. No transition within a closed, adequately covered window produces a conclusive failure for the **transition** criterion. It makes the conditional delivery claim unavailable/inconclusive because there was no identified transition to assess. An observation outage makes the affected claim inconclusive. Both required criteria remain visible. A generic adapter timeout does not silently replace this domain distinction.

The finalizer graph orders `ensure-stopped` before `capture.close`. Close uses settled dependency semantics so it still runs after a stop failure, preserving its last cursor, coverage gaps and unresolved effect references. Cancellation may interrupt collection; it must not fabricate a closed, adequately covered window.

## 5. CloudTrail audit queries

CloudTrail evidence answers an audit question about recorded API activity. The chosen backend and event selectors must cover the event category, account, Region and window. LookupEvents provides recent regional management/Insights history, not an arbitrary data-event query. SNS Publish/PublishBatch are data events that require appropriate recording configuration; they are not present in default Event history. [LookupEvents](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_LookupEvents.html) · [SNS CloudTrail logging](https://docs.aws.amazon.com/sns/latest/dg/logging-using-cloudtrail.html)

Do not make CloudTrail Lake the mandatory backend for a new product: AWS closed it to new customers from 31 May 2026. Existing-customer scope has its own conditions. The generic query contract can use an authorized trail-backed query service or another supported collection, with explicit provenance and coverage. [CloudTrail Lake availability change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html)

Repeated CloudTrail queries over the same event interval can return different results as late records arrive. A query completion time is not an event-source watermark. A failed absence check needs adequate source coverage and a declared cutoff; otherwise it is inconclusive. [CloudTrail query results](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/query-results.html)

A recorded Publish call is publication evidence. It is not proof of receiver delivery, application processing or complete notification coverage. Query language/backend differences remain adapter concerns; assessment predicates consume a typed observation with explicit claim scope.

## 6. Assertions and temporal checks

`core/assert` consumes one immutable observation and emits a CheckResult plus assessment evidence. `proof: complete` uses a typed CEL `expect` expression and requires complete collection with sufficient coverage. `proof: witness` uses `operator: exists` over matching records, enabling a positive result from a trustworthy witness even if other records are missing. It cannot be used for “exactly one,” “no errors,” a maximum, or an arbitrary predicate whose truth can change when more rows arrive.

The adapter returns verdict, reason code, input evidence IDs and evaluation cutoff. The server builds the immutable CheckResult by adding the operation/predicate/evaluator digests and check key from the pinned revision and trusted attempt context; the adapter cannot overwrite those provenance fields. False is an assessment result; an expression type error is an execution failure. No generic retry policy reevaluates false assertions until they pass.

`core/check` is a proposed reusable observation-and-assertion operation for temporal sampling. Its mode, window, sample cadence, allowed gaps, maximum attempts/records and final cutoff must be pinned. Its internal observation requests belong to the same StepAttempt and append evidence; they are not undocumented child StepRuns. The first release can implement it as a trusted library adapter without a separate Check entity or nested scheduler.

This initial package provides no temporal evaluator or trustworthy source-coverage detector. The schemas and static checks make the required contracts explicit so a future implementation cannot claim that syntax validation established those behaviors.
