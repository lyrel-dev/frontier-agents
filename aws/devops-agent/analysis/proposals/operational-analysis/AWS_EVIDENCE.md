---
title: AWS evidence acquisition and operational assertion examples
date: '2026-11-05'
type: proposal-annex
status: proposed
tags:
  - operational-analysis
  - evidence
  - assertions
  - aws
---

# AWS evidence acquisition and operational assertions

This annex applies the proposed **Subject, Analysis, Assertion, QueryRun, Evidence, Assessment and Review** model to AWS operational evidence. `QuerySpec`, `Coverage`, `AssertionResult` and `RunReceipt` are owned values. Provider-specific adapters implement acquisition; they do not introduce a different domain entity for each AWS API.

The contracts below were reviewed on **5 November 2026**. No AWS account was queried or modified. The worked service, identifiers, observations and timings are fictional. Consumer receipt/processing records are explicitly application-defined examples, not AWS payload schemas.

## 1. Query adapters and their evidence boundaries

| Adapter | Native surface | Evidence and limits |
| --- | --- | --- |
| Logs Insights | `StartQuery`, `GetQueryResults` | Queries selected log groups/data sources over a specified interval. Running queries can return partial results. Preserve query ID, language, native status, pages, statistics and exact resolved query. |
| Alarm configuration | `DescribeAlarms` | Current alarm configuration and state. A current configuration read does not establish the configuration at an earlier transition. Retain its observation time. |
| Alarm history | `DescribeAlarmHistory` | State, configuration and action history, with pagination and date/type filters. `HistoryData` is a JSON string; the public envelope does not supply a complete typed schema for every embedded action payload. |
| Recent CloudTrail events | `LookupEvents` | Captured management or Insights events in a Region within the past 90 days. This source does not cover SNS publish data events. |
| Recorded CloudTrail events | Configured CloudWatch ingestion/query, S3/Athena, or existing CloudTrail Lake | Searchable evidence depends on the accounts, Regions, event selectors, ingestion and retention actually configured. The adapter must identify its backend and scope. |
| SNS delivery evidence | Queries over configured delivery logs; retained notifications and endpoint records | Correlates a notification with a particular destination. Publication, endpoint handoff and application processing are separate assertions. |

Official contracts: [Logs StartQuery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_StartQuery.html), [Logs GetQueryResults](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetQueryResults.html), [DescribeAlarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarms.html), [DescribeAlarmHistory](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarmHistory.html), [AlarmHistoryItem](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_AlarmHistoryItem.html), [LookupEvents](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_LookupEvents.html).

### Logs Insights: completion and retrieval are separate

The current `GetQueryResults` contract supports up to **100,000** results, with at most **10,000 per page**. `nextToken`/`maxItems` pagination applies to **Logs Insights QL (`CWLI`)**, not SQL or PPL; tokens expire after one hour. `Running` results are partial. Preserve provider states such as `Complete`, `Failed`, `Timeout` and `Unknown` without turning them into assertion verdicts. Returned rows contain field/value pairs; `@ptr`, when available, identifies a log record retrievable with `GetLogRecord`. [GetQueryResults](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetQueryResults.html)

`StartQuery` time bounds are inclusive epoch seconds. A platform using half-open intervals must define its adapter translation and retain both semantic and native bounds. Bindings in `QuerySpec` are application features: the adapter records the resolved query string instead of claiming native general-purpose parameter binding. [StartQuery](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_StartQuery.html)

An exhausted page chain establishes retrieval of the available selected result, subject to query semantics and limits. It does not prove that every relevant source event was logged. Aggregate queries legitimately return fewer rows than matched source records, so comparing row count with `recordsMatched` is not a general truncation test.

### Alarms and CloudTrail: declare the population searched

Omitting `AlarmTypes` returns metric alarms by default; current APIs also support composite and log alarms. CloudWatch retains alarm history for **30 days** and can record repeated notifications for one state transition. Preserve the transition identity separately from observations of notification attempts. [DescribeAlarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_DescribeAlarms.html) · [Alarm history guidance](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Alarms.html)

`LookupEvents` accepts one lookup attribute, returns at most 50 events per page, and is limited to two requests per second per account/Region. Reuse its continuation token with the same parameters. Unsupported event categories, denied reads or missing retention produce collection limitations, not a successful proof of absence. [LookupEvents](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_LookupEvents.html)

**CloudTrail Lake is optional.** Its new-customer cutoff was **31 May 2026**; existing customers continue under documented conditions. Do not require it for new installations. AWS identifies CloudWatch as the migration alternative, and Athena can query configured CloudTrail trail files in S3. Existing Lake integrations retain their own query status and pagination contracts. [Lake availability change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html) · [Athena and CloudTrail](https://docs.aws.amazon.com/athena/latest/ug/cloudtrail-logs.html) · [Lake GetQueryResults](https://docs.aws.amazon.com/awscloudtrail/latest/APIReference/API_GetQueryResults.html)

## 2. Worked service assessment: did the alarm reach its consumer?

The fictional `checkout-prod` Subject represents a deployed checkout service. Its resource references identify an alarm, SNS topic and incident receiver. An Analysis targets this subject for `2026-11-05T09:00:00Z`–`09:05:00Z` (10:00–10:05 CET). Its purpose is to validate the alert path, not to declare the whole service healthy.

| Assertion | Fictional retained evidence | Bounded conclusion |
| --- | --- | --- |
| A1: the alarm entered `ALARM` | State-history evidence identifies transition T at 09:00:00Z. | Supports that transition. It says nothing about recovery. |
| A2: the notification for T was published to topic X | A captured SNS envelope identifies message M/topic X; its alarm payload identifies T. A matching publish record may corroborate acceptance. | Supports publication of the correlated notification. |
| A3: M reached the intended HTTPS receiver within 60 seconds of T | Message-specific delivery evidence and a receiver receipt at 09:00:05Z identify M and that endpoint. | Supports this delivery and deadline under stated clock assumptions. |
| A4: the receiver processed M successfully | A custom application processing record at 09:00:08Z identifies M and an explicit processing outcome. | Supports the declared processing step, not human acknowledgement. |

Each query has a retained `QueryRun` and its receipts. All seven entities use the common version contract. The `Assessment` pins exact Assertion, Evidence and QueryRun versions, including the selected result manifests and relevant coverage. The operator's `Review` accepts or challenges that exact assessment version; it does not rewrite the query output or computed verdicts.

### Exact correlation fields

The SNS HTTP envelope supplies **`MessageId`, `TopicArn`, `Timestamp` and `Message`**. The alarm payload inside `Message` supplies **`AlarmArn`, `StateChangeTime`, `NewStateValue` and `OldStateValue`**. Retain the complete owning scope and source references. `Timestamp` is publication time, not endpoint receipt time. Retries reuse the original SNS message ID. [SNS envelope](https://docs.aws.amazon.com/sns/latest/dg/http-notification-json.html) · [Alarm notification schemas](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Notify_Users_Alarm_Changes.html)

Delivery-log profiles can expose **`notification.messageId`**, **`notification.topicArn`**, **`delivery.destination`**, **`delivery.statusCode`**, **`delivery.providerResponse`**, **`delivery.attempts`** and **`status`**. These are documented examples, not a universal required-field schema for all protocols. Match the same message and destination; retain unsuccessful attempts alongside any later successful delivery. [Delivery example](https://docs.aws.amazon.com/sns/latest/dg/sns-message-data-protection-examples.html)

The custom receiver records in this example use `snsMessageId`, `topicArn`, `endpointId`, `receivedAt`, `processedAt` and `processingOutcome`. Their parser/version and outcome meaning belong to the application. If that correlation is unavailable, topic/time proximity is an inferred association and cannot silently become an exact join. Timing assessments retain timestamp precision and clock assumptions; uncertainty crossing the deadline yields `inconclusive`.

### Limits that change the verdict

SNS `Publish`/`PublishBatch` are CloudTrail **data events**, disabled by default and absent from Event history. A documented publish event can expose `responseElements.messageId`, while hiding the message body. It can corroborate publication without independently identifying the embedded alarm transition. [SNS CloudTrail logging](https://docs.aws.amazon.com/sns/latest/dg/logging-using-cloudtrail.html)

Topic delivery-status logging covers Firehose, SQS, Lambda, HTTPS and platform application endpoints. Success logging can be sampled and requires configured logging roles. A missing success record is therefore insufficient to refute delivery. Email delivery or human acknowledgement requires another suitable source. Current logging configuration does not establish historical logging coverage. [Delivery-status scope](https://docs.aws.amazon.com/sns/latest/dg/sns-topic-attributes.html) · [Sampling/configuration](https://docs.aws.amazon.com/sns/latest/dg/topics-attrib.html)

Raw delivery changes or strips the SNS envelope. Record that limitation rather than substituting an unrelated queue identifier for `MessageId`. HTTP collectors should retain the outcome of SNS signature and expected-topic validation. Topic-level delivery metrics provide aggregate context, not proof for message M. [Raw delivery](https://docs.aws.amazon.com/sns/latest/dg/sns-large-payload-raw-message-delivery.html) · [Signature validation](https://docs.aws.amazon.com/sns/latest/dg/sns-verify-signature-of-message.html) · [SNS metrics](https://docs.aws.amazon.com/sns/latest/dg/sns-monitoring-using-cloudwatch.html)

## 3. Positive witnesses and negative absence

| Evaluation situation | Recommended result |
| --- | --- |
| One valid, exactly correlated receipt satisfies an existential delivery assertion. | `supported`, even if unrelated collection remains partial. |
| No receipt is returned, but success logging was sampled, disabled or outside retention. | `inconclusive`, with the specific coverage reason. |
| A required event is absent from a sufficiently covered, closed interval under the assertion's declared evidence policy. | `refuted`, with the query, coverage assumptions and deadline retained. |
| Evidence conflicts or correlation is ambiguous. | `inconclusive`; preserve both sides and the conflict reason. |
| A query times out, fails or is denied. | Acquisition failure; dependent assertions normally become `inconclusive`, not `refuted`. |
| An explicit applicability rule excludes the subject. | `not_applicable`; unsupported adapters alone do not establish this. |

`Coverage` records requested/resolved sources, filters, time bounds, pagination/limits, logging and sampling knowledge, freshness and gaps. Supporting a universal claim such as “every alarm transition reached the receiver” additionally requires a bounded transition population. A positive witness can establish existence, and one reliable counterexample can refute a universal claim. Supporting universality or absence requires adequate population coverage.

Keep domain time, source publication time, collection time and assessment time distinct. Later evidence can produce a new assessment while the previously reviewed assessment remains reproducible. This permits the same compact model to support incident investigation, post-deployment validation, operational readiness and periodic infrastructure analysis.
