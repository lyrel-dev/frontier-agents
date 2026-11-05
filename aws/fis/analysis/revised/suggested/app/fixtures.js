/* Synthetic assessment fixtures. No credentials, AWS calls or executable adapters.
 * Revisions pin the reviewed example contracts. Future trace events are simulator
 * instructions; AssessmentModel.projectRun never exposes them in a snapshot. */
(function (root, factory) {
  const value = factory();
  if (typeof module === 'object' && module.exports) module.exports = value;
  else root.AssessmentFixtures = value;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const revisions = {
  "alarm": {
    "scenarioRevisionId": "scnrev_alarm_delivery_002",
    "scenarioId": "scn_application_alarm_delivery",
    "version": 2,
    "digest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
    "programDigest": "sha256:aa22e7c3b5abb1000a0f4e57e076a93ed8fcd98f2474925740370bc271d4e660",
    "publishedAt": "2026-11-04T15:16:00Z",
    "expressionContract": "cel/assessment-v0.2",
    "reducerVersion": "assessment-reducer/0.2",
    "synthetic": true,
    "yaml": "apiVersion: assessment/v0.2\nname: Checkout alarm notification delivery\ndescription: Verify an alarm transition and timely receipt by the explicitly bound probe receiver.\ninputs:\n  type: object\n  additionalProperties: false\n  required: [templateId, alarmArn, topicArn, receiverId]\n  properties:\n    templateId: {type: string, minLength: 1}\n    alarmArn: {type: string, minLength: 1}\n    topicArn: {type: string, minLength: 1}\n    receiverId: {type: string, minLength: 1}\nbindings:\n  aws: {kind: connection, capability: aws_assessment_scope}\n  receiver: {kind: connection, capability: dedicated_notification_receiver}\npolicies:\n  timeoutSeconds: 600\n  finalizationTimeoutSeconds: 180\n  concurrency: queue_per_deployment\nsteps:\n  capture:\n    uses: events/capture.open@1\n    timeoutSeconds: 30\n    with:\n      connection: \"${{ bindings.receiver }}\"\n      receiverId: \"${{ inputs.receiverId }}\"\n      topicArn: \"${{ inputs.topicArn }}\"\n      leaseSeconds: 900\n  baseline:\n    uses: aws/cloudwatch.alarm.read@1\n    timeoutSeconds: 30\n    with:\n      connection: \"${{ bindings.aws }}\"\n      alarmArn: \"${{ inputs.alarmArn }}\"\n  baseline_ok:\n    needs: [baseline]\n    uses: core/assert@1\n    assessmentRole: precondition\n    timeoutSeconds: 5\n    with:\n      observation: \"${{ steps.baseline.outputs.observation }}\"\n      proof: complete\n      expect: value.state == \"OK\"\n  inject:\n    needs: [capture, baseline_ok]\n    uses: aws/fis.start@1\n    timeoutSeconds: 45\n    with:\n      connection: \"${{ bindings.aws }}\"\n      templateId: \"${{ inputs.templateId }}\"\n  collect:\n    needs: [inject]\n    after: settled\n    uses: events/capture.collect-alarm@1\n    timeoutSeconds: 300\n    with:\n      captureStep: \"${{ steps.capture.ref }}\"\n      injectionStep: \"${{ steps.inject.ref }}\"\n      alarmArn: \"${{ inputs.alarmArn }}\"\n      topicArn: \"${{ inputs.topicArn }}\"\n      receiverId: \"${{ inputs.receiverId }}\"\n      transitionWindowSeconds: 180\n      receiptDeadlineSeconds: 60\n      collectionGraceSeconds: 30\n  alarm_transition:\n    needs: [collect]\n    after: settled\n    uses: core/assert@1\n    assessmentRole: criterion\n    timeoutSeconds: 5\n    with:\n      observation: \"${{ steps.collect.outputs.transition }}\"\n      proof: witness\n      operator: exists\n  notification_received:\n    needs: [collect]\n    after: settled\n    uses: core/assert@1\n    assessmentRole: criterion\n    timeoutSeconds: 5\n    with:\n      observation: \"${{ steps.collect.outputs.receipt }}\"\n      proof: witness\n      operator: exists\nfinally:\n  stop_injection:\n    uses: aws/fis.ensure-stopped@1\n    after: settled\n    timeoutSeconds: 120\n    with:\n      connection: \"${{ bindings.aws }}\"\n      step: \"${{ steps.inject.ref }}\"\n  close_capture:\n    needs: [stop_injection]\n    after: settled\n    uses: events/capture.close@1\n    timeoutSeconds: 30\n    with:\n      step: \"${{ steps.capture.ref }}\"\n",
    "operations": [
      {
        "uses": "aws/cloudwatch.alarm.read@1",
        "implementationDigest": "sha256:15aeee396852b974ec89e28b8be11cb2684a9bbf58364b8e7b35b49d095d919a",
        "inputSchemaDigest": "sha256:18280675361c2fe029ee88e649de35aeb6afe5912d7ca003cf3231e593c679e2",
        "outputSchemaDigest": "sha256:913e0d44e3496e83d0c24ec6f90fedb4a77c5d80f83e514bfa35975e0f68d529",
        "capabilityDigest": "sha256:6878329e05d9007ab65cbc767b415c32a8c06d053385b868886da0e409255b1f"
      },
      {
        "uses": "aws/fis.ensure-stopped@1",
        "implementationDigest": "sha256:19c4397346bd16bb1ad3079d293c9e4fa4afaa1ecf216bd240b7f63b720bb749",
        "inputSchemaDigest": "sha256:5af9b48250df00e8be6af6e80e9af8a5f3d042a6d30e7ac2be784eb607949080",
        "outputSchemaDigest": "sha256:c7891f2b30439e590722d5b1f6fd21af5ac20092c9fdd38e7bae83ac1b4fe12b",
        "capabilityDigest": "sha256:c4457bd924d9f766979b15c1ed340d0f816001989ea131cd61199242bd12263e"
      },
      {
        "uses": "aws/fis.start@1",
        "implementationDigest": "sha256:c9da508312034cf67c78f808e0d8cd1142710c340e725dd3f5bea8fbd34af962",
        "inputSchemaDigest": "sha256:028f3ccc53e1d231e3dc2fa26482cf3b3d3033738cf79065b5f1800dc387aabc",
        "outputSchemaDigest": "sha256:87cca2452fb8708f566d83b63e4fa10d669554714f44286936c6d4fd4beee5a3",
        "capabilityDigest": "sha256:6a03b7fa1cde0a91f491f1cd996be54b480cb17cc0afec79225681bb4e0dcb64"
      },
      {
        "uses": "core/assert@1",
        "implementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
        "inputSchemaDigest": "sha256:eaf72e914af5b51d6f6876884f5125a297877262e06287419440d271e66fa6eb",
        "outputSchemaDigest": "sha256:83b8884d26c9f61f6c5e9367d0b538d8b76c5131831751febb4be36be61f4360",
        "capabilityDigest": "sha256:37d19947ad488d900870d0b6af60bfd78f76deb8d0eb92c9a9bb634a5e6e6357"
      },
      {
        "uses": "events/capture.close@1",
        "implementationDigest": "sha256:e18024914b8b2a0ba7903beb20b6a175d0e47415a3ee34fe106c6ea88878c5d8",
        "inputSchemaDigest": "sha256:02c1ee2b6e5916916e1490f926fbceb11515b1b51381b3827ae454e3ca9a64fe",
        "outputSchemaDigest": "sha256:c7891f2b30439e590722d5b1f6fd21af5ac20092c9fdd38e7bae83ac1b4fe12b",
        "capabilityDigest": "sha256:943ce9cf012bb22c812c005c0c1790a0a001a691f9e05e3f1203fd1a97afda9c"
      },
      {
        "uses": "events/capture.collect-alarm@1",
        "implementationDigest": "sha256:14be817dfbc74e2a83f61f09b53db5c176e368ae644cb56a9c4d01fbe3418cad",
        "inputSchemaDigest": "sha256:14ec1ea16f88b9d3bfa9ff67dd6065514bd2d43d7411ae46d85585029ecdeb9f",
        "outputSchemaDigest": "sha256:b13301fbd978595c4ff943f5e6a2da3d8a59203d8cdcebe911d19ca1c5d5ccd6",
        "capabilityDigest": "sha256:7764ccfeaffd1798feaaada7f814b22fe435649d71e1c7ac77fc65c2fdc8e3ef"
      },
      {
        "uses": "events/capture.open@1",
        "implementationDigest": "sha256:e8713789d1e5012d13fd53294b913cff408f8d583c83e46beca258d4ed97b25d",
        "inputSchemaDigest": "sha256:8a7b2121b0ed151ee26d1c985321961dd2ea1adc16bc32cfe5659fc04dd12073",
        "outputSchemaDigest": "sha256:dcc62945d10446450685adcca42cdb4865ad7f80c949fcb04377b438ddb43fa4",
        "capabilityDigest": "sha256:031668ac071d974bf4bdfa1bb104ffe77d6a1c5c4972b7ff8e474b0187ebd6b5"
      }
    ],
    "definitions": [
      {
        "stepKey": "capture",
        "label": "Arm receiver capture",
        "description": "A dedicated, durable probe session is ready before injection.",
        "graph": "main",
        "uses": "events/capture.open@1",
        "needs": [],
        "after": "success",
        "assessmentRole": null,
        "timeoutSeconds": 30,
        "with": {
          "connection": "${{ bindings.receiver }}",
          "receiverId": "${{ inputs.receiverId }}",
          "topicArn": "${{ inputs.topicArn }}",
          "leaseSeconds": 900
        }
      },
      {
        "stepKey": "baseline",
        "label": "Read alarm baseline",
        "description": "Observe the bound alarm before any infrastructure mutation.",
        "graph": "main",
        "uses": "aws/cloudwatch.alarm.read@1",
        "needs": [],
        "after": "success",
        "assessmentRole": null,
        "timeoutSeconds": 30,
        "with": {
          "connection": "${{ bindings.aws }}",
          "alarmArn": "${{ inputs.alarmArn }}"
        }
      },
      {
        "stepKey": "baseline_ok",
        "label": "Check safe starting state",
        "description": "Require an observed OK alarm state before perturbing the service.",
        "graph": "main",
        "uses": "core/assert@1",
        "needs": [
          "baseline"
        ],
        "after": "success",
        "assessmentRole": "precondition",
        "timeoutSeconds": 5,
        "with": {
          "observation": "${{ steps.baseline.outputs.observation }}",
          "proof": "complete",
          "expect": "value.state == \"OK\""
        }
      },
      {
        "stepKey": "inject",
        "label": "Start fault experiment",
        "description": "Dispatch the scoped FIS experiment once; retain the original intent.",
        "graph": "main",
        "uses": "aws/fis.start@1",
        "needs": [
          "capture",
          "baseline_ok"
        ],
        "after": "success",
        "assessmentRole": null,
        "timeoutSeconds": 45,
        "with": {
          "connection": "${{ bindings.aws }}",
          "templateId": "${{ inputs.templateId }}"
        }
      },
      {
        "stepKey": "collect",
        "label": "Collect transition and receipt",
        "description": "Correlate the alarm transition with a receipt from the bound receiver.",
        "graph": "main",
        "uses": "events/capture.collect-alarm@1",
        "needs": [
          "inject"
        ],
        "after": "settled",
        "assessmentRole": null,
        "timeoutSeconds": 300,
        "with": {
          "captureStep": "${{ steps.capture.ref }}",
          "injectionStep": "${{ steps.inject.ref }}",
          "alarmArn": "${{ inputs.alarmArn }}",
          "topicArn": "${{ inputs.topicArn }}",
          "receiverId": "${{ inputs.receiverId }}",
          "transitionWindowSeconds": 180,
          "receiptDeadlineSeconds": 60,
          "collectionGraceSeconds": 30
        }
      },
      {
        "stepKey": "alarm_transition",
        "label": "Alarm transitions in time",
        "description": "The alarm enters ALARM within 180 seconds of the execution boundary.",
        "graph": "main",
        "uses": "core/assert@1",
        "needs": [
          "collect"
        ],
        "after": "settled",
        "assessmentRole": "criterion",
        "timeoutSeconds": 5,
        "with": {
          "observation": "${{ steps.collect.outputs.transition }}",
          "proof": "witness",
          "operator": "exists"
        }
      },
      {
        "stepKey": "notification_received",
        "label": "Receiver gets the notification",
        "description": "The bound probe receives the correlated notification within 60 seconds.",
        "graph": "main",
        "uses": "core/assert@1",
        "needs": [
          "collect"
        ],
        "after": "settled",
        "assessmentRole": "criterion",
        "timeoutSeconds": 5,
        "with": {
          "observation": "${{ steps.collect.outputs.receipt }}",
          "proof": "witness",
          "operator": "exists"
        }
      },
      {
        "stepKey": "stop_injection",
        "label": "Reconcile and stop experiment",
        "description": "Inspect the original StepRef, including an uncertain start response.",
        "graph": "finalizer",
        "uses": "aws/fis.ensure-stopped@1",
        "needs": [],
        "after": "settled",
        "assessmentRole": null,
        "timeoutSeconds": 120,
        "with": {
          "connection": "${{ bindings.aws }}",
          "step": "${{ steps.inject.ref }}"
        }
      },
      {
        "stepKey": "close_capture",
        "label": "Close receiver capture",
        "description": "Close after stop reconciliation settles, even if it fails.",
        "graph": "finalizer",
        "uses": "events/capture.close@1",
        "needs": [
          "stop_injection"
        ],
        "after": "settled",
        "assessmentRole": null,
        "timeoutSeconds": 30,
        "with": {
          "step": "${{ steps.capture.ref }}"
        }
      }
    ],
    "policies": {
      "timeoutSeconds": 600,
      "finalizationTimeoutSeconds": 180,
      "concurrency": "queue_per_deployment"
    }
  },
  "logs": {
    "scenarioRevisionId": "scnrev_logs_budget_003",
    "scenarioId": "scn_application_log_budget",
    "version": 3,
    "digest": "sha256:ce0f0a5721384a2c242f283d7e19c6e8ee14be75b54e51c246018f56d4709211",
    "programDigest": "sha256:c786e65326cd76184bffa5bebcdbbe056a0570cd40d4c5219fdc5e83049fcc90",
    "publishedAt": "2026-11-04T15:16:00Z",
    "expressionContract": "cel/assessment-v0.2",
    "reducerVersion": "assessment-reducer/0.2",
    "synthetic": true,
    "yaml": "apiVersion: assessment/v0.2\nname: Checkout logged error count\ndescription: Assess a declared application log scope and fixed event-time window, subject to evidence coverage.\ninputs:\n  type: object\n  additionalProperties: false\n  required: [logGroups, windowStart, windowEnd, maximumErrors]\n  properties:\n    logGroups:\n      type: array\n      minItems: 1\n      uniqueItems: true\n      items: {type: string, minLength: 1}\n    windowStart: {type: string, format: date-time}\n    windowEnd: {type: string, format: date-time}\n    maximumErrors: {type: integer, minimum: 0}\nbindings:\n  aws: {kind: connection, capability: cloudwatch_logs_query_scope}\npolicies:\n  timeoutSeconds: 300\n  finalizationTimeoutSeconds: 60\n  concurrency: queue_per_deployment\nsteps:\n  query_errors:\n    uses: aws/cloudwatch.logs.query@1\n    timeoutSeconds: 240\n    with:\n      connection: \"${{ bindings.aws }}\"\n      logGroups: \"${{ inputs.logGroups }}\"\n      windowStart: \"${{ inputs.windowStart }}\"\n      windowEnd: \"${{ inputs.windowEnd }}\"\n      language: CWLI\n      resultShape: single_numeric_count\n      query: |\n        fields @timestamp, level\n        | filter level = \"ERROR\"\n        | stats count(*) as count\n  error_budget:\n    needs: [query_errors]\n    after: settled\n    uses: core/assert@1\n    assessmentRole: criterion\n    timeoutSeconds: 5\n    with:\n      observation: \"${{ steps.query_errors.outputs.observation }}\"\n      proof: complete\n      expect: value.count <= inputs.maximumErrors\nfinally:\n  stop_query:\n    uses: aws/cloudwatch.logs.ensure-stopped@1\n    after: settled\n    timeoutSeconds: 45\n    with:\n      connection: \"${{ bindings.aws }}\"\n      step: \"${{ steps.query_errors.ref }}\"\n",
    "operations": [
      {
        "uses": "aws/cloudwatch.logs.ensure-stopped@1",
        "implementationDigest": "sha256:9ec71d5c6593270faeda036f9f243765a6a71c3fbe4a58dd0d44ccb9f1f2745b",
        "inputSchemaDigest": "sha256:5af9b48250df00e8be6af6e80e9af8a5f3d042a6d30e7ac2be784eb607949080",
        "outputSchemaDigest": "sha256:c7891f2b30439e590722d5b1f6fd21af5ac20092c9fdd38e7bae83ac1b4fe12b",
        "capabilityDigest": "sha256:00ecf9eaab85c3dd5258792b628afb706f758a169de64b563c6a8acbf418e1bf"
      },
      {
        "uses": "aws/cloudwatch.logs.query@1",
        "implementationDigest": "sha256:36895dedff9ffaf2876e407b66f37f526f74f3f8aa19f7c250255ae372c91156",
        "inputSchemaDigest": "sha256:5b82f30420638c3bb79183d859eed5d9dc8b5279d7131ec76fab14596b4a45b4",
        "outputSchemaDigest": "sha256:78319cbba7f27e627eaa7727cccc24a2c04b901e2812de79f675a9b4c89f07aa",
        "capabilityDigest": "sha256:896aae071e8331c82e44963aed678c000dc187ab82f03324c632178336b78854"
      },
      {
        "uses": "core/assert@1",
        "implementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
        "inputSchemaDigest": "sha256:eaf72e914af5b51d6f6876884f5125a297877262e06287419440d271e66fa6eb",
        "outputSchemaDigest": "sha256:83b8884d26c9f61f6c5e9367d0b538d8b76c5131831751febb4be36be61f4360",
        "capabilityDigest": "sha256:37d19947ad488d900870d0b6af60bfd78f76deb8d0eb92c9a9bb634a5e6e6357"
      }
    ],
    "definitions": [
      {
        "stepKey": "query_errors",
        "label": "Query application error count",
        "description": "Run a bounded Logs Insights query and collect its result pages.",
        "graph": "main",
        "uses": "aws/cloudwatch.logs.query@1",
        "needs": [],
        "after": "success",
        "assessmentRole": null,
        "timeoutSeconds": 240,
        "with": {
          "connection": "${{ bindings.aws }}",
          "logGroups": "${{ inputs.logGroups }}",
          "windowStart": "${{ inputs.windowStart }}",
          "windowEnd": "${{ inputs.windowEnd }}",
          "language": "CWLI",
          "resultShape": "single_numeric_count",
          "query": "fields @timestamp, level\n| filter level = \"ERROR\"\n| stats count(*) as count\n"
        }
      },
      {
        "stepKey": "error_budget",
        "label": "Verify logged error budget",
        "description": "Evaluate a typed count only when the source coverage supports the claim.",
        "graph": "main",
        "uses": "core/assert@1",
        "needs": [
          "query_errors"
        ],
        "after": "settled",
        "assessmentRole": "criterion",
        "timeoutSeconds": 5,
        "with": {
          "observation": "${{ steps.query_errors.outputs.observation }}",
          "proof": "complete",
          "expect": "value.count <= inputs.maximumErrors"
        }
      },
      {
        "stepKey": "stop_query",
        "label": "Reconcile query completion",
        "description": "Confirm the original query is terminal; never start a replacement.",
        "graph": "finalizer",
        "uses": "aws/cloudwatch.logs.ensure-stopped@1",
        "needs": [],
        "after": "settled",
        "assessmentRole": null,
        "timeoutSeconds": 45,
        "with": {
          "connection": "${{ bindings.aws }}",
          "step": "${{ steps.query_errors.ref }}"
        }
      }
    ],
    "policies": {
      "timeoutSeconds": 300,
      "finalizationTimeoutSeconds": 60,
      "concurrency": "queue_per_deployment"
    }
  }
};
  const runs = [
  {
    "key": "alarm-live",
    "runId": "run_demo_alarm_live_20261105",
    "title": "Checkout · alarm notification",
    "description": "Assess the declared scope with explicit evidence and independent execution, criterion and cleanup outcomes.",
    "service": "Checkout",
    "environment": "Production EU",
    "region": "eu-central-1",
    "accounts": [
      "444455556666"
    ],
    "owner": "Platform Resilience",
    "createdAt": "2026-11-05T09:00:00Z",
    "initialCursorSeconds": 110,
    "durationSeconds": 240,
    "synthetic": true,
    "revisionKey": "alarm",
    "scenario": {
      "scenarioId": "scn_application_alarm_delivery",
      "displayName": "Alarm-to-receiver assessment"
    },
    "admission": {
      "admittedAt": "2026-11-05T09:00:00Z",
      "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
      "inputsDigest": "sha256:9754caea3fd4de160c94831b305ef2c2cad37c38f485d1102e6c7e7bf11e8498",
      "subject": {
        "deploymentRef": "deployment_checkout_prod_euc1",
        "expectedDeploymentRevision": "release_2026_11_05.3",
        "service": "Checkout",
        "environment": "production",
        "accountIds": [
          "444455556666"
        ],
        "region": "eu-central-1"
      },
      "inputs": {
        "templateId": "EXTc412542ec0d9a06fb",
        "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
        "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
        "receiverId": "checkout-alarm-probe"
      },
      "bindings": {
        "aws": {
          "connectionId": "connection_checkout_assessment",
          "capabilities": [
            "aws_assessment_scope"
          ]
        },
        "receiver": {
          "connectionId": "connection_checkout_dedicated_probe",
          "capabilities": [
            "dedicated_notification_receiver"
          ]
        }
      },
      "requiredCriteria": [
        "alarm_transition",
        "notification_received"
      ],
      "policies": {
        "timeoutSeconds": 600,
        "finalizationTimeoutSeconds": 180,
        "concurrency": "queue_per_deployment"
      },
      "bindingObservedAt": "2026-11-05T09:00:00Z"
    },
    "_events": [
      {
        "at": 0,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_01",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "admission",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "admission",
          "title": "Revision and deployment bound",
          "summary": "The exact published revision, input values and trusted connection references were fixed before dispatch.",
          "occurredAt": "2026-11-05T09:00:00Z",
          "observedAt": "2026-11-05T09:00:00Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/admission/1",
          "schemaRef": "sha256:a9a9546dd44dfa0d6a0940f9829b98d45ffba2c3a6c511adb4b6da8ddc1e54d3",
          "value": {
            "scenarioRevisionId": "scnrev_alarm_delivery_002",
            "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
            "requiredCriteria": [
              "alarm_transition",
              "notification_received"
            ]
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f4083e81379f421b5790829832e61c7c3989f68ba341e34b5a975e2b53118b8f"
        }
      },
      {
        "at": 1,
        "kind": "run_phase",
        "phase": "running",
        "reason": "Main workflow admitted with a fixed criterion denominator.",
        "termination": null
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:capture:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_checkout_dedicated_probe",
            "capabilities": [
              "dedicated_notification_receiver"
            ]
          },
          "receiverId": "checkout-alarm-probe",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
          "leaseSeconds": 900
        },
        "resolvedInputsDigest": "sha256:b0ce5ef900e6fd694546f57c476a23494e4492cb0c09e0527de675a4842fd994",
        "checkpoint": null
      },
      {
        "at": 2,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "opening",
          "observedAt": "2026-11-05T09:00:02Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A local capture intent exists; readiness is not yet established.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "baseline",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:baseline:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_checkout_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability"
        },
        "resolvedInputsDigest": "sha256:f611be4fa473b397490d748af35bb7a03625392795a383b1e2b807cb5e3a103b",
        "checkpoint": null
      },
      {
        "at": 5,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_02",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "baseline",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "observation",
          "title": "Alarm baseline observed",
          "summary": "The alarm is OK at the starting observation.",
          "occurredAt": "2026-11-05T09:00:04Z",
          "observedAt": "2026-11-05T09:00:05Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/baseline/2",
          "schemaRef": "sha256:3a57c20e4754fe8b5157afec9259195d1cb99d9074b946f6b2aa2c8a6b3c53d9",
          "value": {
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "state": "OK",
            "stateUpdatedAt": "2026-11-05T08:58:00Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f733fa13e74d5f10f76b733af198a319a0691278221571be9bee42b3cd971a74"
        }
      },
      {
        "at": 5,
        "kind": "step_finish",
        "stepKey": "baseline",
        "outcome": "succeeded",
        "outputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_alarm-live_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T09:00:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 6,
        "kind": "step_start",
        "stepKey": "baseline_ok",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:baseline_ok:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_alarm-live_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T09:00:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
              "authenticated": true
            }
          },
          "proof": "complete",
          "expect": "value.state == \"OK\""
        },
        "resolvedInputsDigest": "sha256:4ea9e184f37114082e921bebd7ce8231503756ab5b1da06e918ffade0e67cd0a",
        "checkpoint": null
      },
      {
        "at": 7,
        "kind": "check_result",
        "stepKey": "baseline_ok",
        "check": {
          "verdict": "passed",
          "summary": "The mutation precondition is satisfied.",
          "expected": "Alarm state is OK",
          "actual": "OK",
          "reasonCode": "PREDICATE_TRUE",
          "evidenceIds": [
            "ev_alarm-live_02"
          ],
          "evaluatedThrough": "2026-11-05T09:00:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "proof": "complete",
          "window": null,
          "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 7,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_03",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "baseline_ok",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The mutation precondition is satisfied.",
          "occurredAt": "2026-11-05T09:00:07Z",
          "observedAt": "2026-11-05T09:00:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/baseline_ok/3",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "The mutation precondition is satisfied.",
            "expected": "Alarm state is OK",
            "actual": "OK",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_alarm-live_02"
            ],
            "evaluatedThrough": "2026-11-05T09:00:07Z",
            "collection": "complete",
            "coverage": "sufficient",
            "proof": "complete",
            "window": null,
            "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:81e5dba0a25e8fe139b17db9b46caaf8caa6d47aca20907937fcbcb266e9d42f"
        }
      },
      {
        "at": 7,
        "kind": "step_finish",
        "stepKey": "baseline_ok",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_alarm-live_02"
            ],
            "evaluatedThrough": "2026-11-05T09:00:07Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 8,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_04",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "capture",
          "source": "Receiver capture",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Dedicated receiver capture ready",
          "summary": "The probe session is active before injection. This proves readiness of the bound probe, not a production subscriber.",
          "occurredAt": "2026-11-05T09:00:08Z",
          "observedAt": "2026-11-05T09:00:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/capture/4",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_f9a281b5fb",
            "receiverId": "checkout-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
            "queueArn": "arn:aws:sqs:eu-central-1:444455556666:checkout-assessment-probe",
            "readyAt": "2026-11-05T09:00:08Z",
            "leaseExpiresAt": "2026-11-05T09:15:02Z",
            "coveragePolicy": "dedicated-receiver/v1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:d8dfc7fccedb351a6d462587e39f2db1cfea2df3a08272c77f3a71e8039d4393"
        }
      },
      {
        "at": 8,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_f9a281b5fb",
          "disposition": "active",
          "providerState": null,
          "localState": "ready",
          "observedAt": "2026-11-05T09:00:08Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A dedicated probe is collecting only its own subscription.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 8,
        "kind": "step_finish",
        "stepKey": "capture",
        "outcome": "succeeded",
        "outputs": {
          "capture": {
            "captureId": "capture_f9a281b5fb",
            "readyAt": "2026-11-05T09:00:08Z",
            "leaseExpiresAt": "2026-11-05T09:15:02Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 10,
        "kind": "step_start",
        "stepKey": "inject",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:inject:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_checkout_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "templateId": "EXTc412542ec0d9a06fb"
        },
        "resolvedInputsDigest": "sha256:983aac9257ee879e10b23113e719d4a4e057b362af2186641ad45961294b5b6a",
        "checkpoint": {
          "providerClientToken": "dispatch_alarm-live_inject_1"
        }
      },
      {
        "at": 10,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "awaiting_response",
          "observedAt": "2026-11-05T09:00:10Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "Dispatch intent is durable. No provider identity has been observed yet.",
          "actions": []
        },
        "observedByStepKey": "inject",
        "sourceKind": "runtime"
      },
      {
        "at": 13,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_05",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "inject",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-execution",
          "title": "FIS experiment started",
          "summary": "The provider returned an experiment identity. Workflow start succeeded while the external experiment remains active.",
          "occurredAt": "2026-11-05T09:00:11Z",
          "observedAt": "2026-11-05T09:00:13Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/inject/5",
          "schemaRef": "sha256:c0c3c85379702f81d2d9b5a14ef3c6ecbe5a452faf3c9c0745c228c3e18bbd7e",
          "value": {
            "experimentId": "EXPf9a281b5fbd4a8436",
            "experimentTemplateId": "EXTc412542ec0d9a06fb",
            "state": "running",
            "startTime": "2026-11-05T09:00:11Z",
            "selectedScope": {
              "resourceType": "aws:ec2:subnet",
              "uniqueResources": 3,
              "membershipCount": 3,
              "accountId": "444455556666"
            }
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:5a39d3df150461356d98f218a0911f036240d9462b0a4c8ceade0836c3e945a1"
        }
      },
      {
        "at": 13,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXPf9a281b5fbd4a8436",
          "disposition": "active",
          "providerState": "running",
          "localState": null,
          "observedAt": "2026-11-05T09:00:13Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The Start step completed; the FIS experiment is independently running.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "initiating",
              "startTime": "2026-11-05T09:00:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "pending"
            }
          ]
        },
        "observedByStepKey": "inject",
        "sourceKind": "provider"
      },
      {
        "at": 13,
        "kind": "step_finish",
        "stepKey": "inject",
        "outcome": "succeeded",
        "outputs": {
          "experiment": {
            "provider": "aws/fis",
            "nativeId": "EXPf9a281b5fbd4a8436",
            "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
            "accountId": "444455556666",
            "region": "eu-central-1"
          },
          "submittedAt": "2026-11-05T09:00:10Z",
          "providerStartedAt": "2026-11-05T09:00:11Z"
        },
        "error": null,
        "reason": null
      },
      {
        "at": 14,
        "kind": "step_start",
        "stepKey": "collect",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:collect:1",
        "resolvedInputs": {
          "captureStep": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "capture"
          },
          "injectionStep": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject"
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
          "receiverId": "checkout-alarm-probe",
          "transitionWindowSeconds": 180,
          "receiptDeadlineSeconds": 60,
          "collectionGraceSeconds": 30
        },
        "resolvedInputsDigest": "sha256:722bf5e86daf774cffbf8028f4a0465e9d03288206399aa3b902c3c6dae2e435",
        "checkpoint": {
          "captureId": "capture_f9a281b5fb",
          "cursor": "alarm-live/ready",
          "providerStartedAt": "2026-11-05T09:00:11Z",
          "transitionDeadline": "2026-11-05T09:03:11Z"
        }
      },
      {
        "at": 51,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_06",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "inject",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-action",
          "title": "Availability Zone isolation active",
          "summary": "The named provider action is running. Selected resources are not a generic per-resource fault-result record.",
          "occurredAt": "2026-11-05T09:00:49Z",
          "observedAt": "2026-11-05T09:00:51Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/inject/6",
          "schemaRef": "sha256:eea4c43d9319e91de68a1cef58e7d9c64752111c878cb1bdb9efac44f0594a34",
          "value": {
            "experimentId": "EXPf9a281b5fbd4a8436",
            "actionName": "isolateZone",
            "actionId": "aws:network:disrupt-connectivity",
            "state": "running"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:7923ce5d8cd4cdf67e60b9c3f6287ff2de37586d776a10e0981d6784b70041ed"
        }
      },
      {
        "at": 51,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXPf9a281b5fbd4a8436",
          "disposition": "active",
          "providerState": "running",
          "localState": null,
          "observedAt": "2026-11-05T09:00:51Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The latest provider action observation confirms isolation is running.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "running",
              "startTime": "2026-11-05T09:00:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "pending"
            }
          ]
        },
        "observedByStepKey": "inject",
        "sourceKind": "provider"
      },
      {
        "at": 78,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_07",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "collect",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "alarm-transition",
          "title": "Alarm entered ALARM",
          "summary": "A specific OK → ALARM transition is correlated by alarm ARN and state-change time.",
          "occurredAt": "2026-11-05T09:01:16Z",
          "observedAt": "2026-11-05T09:01:18Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/collect/7",
          "schemaRef": "sha256:7765857a2fdcfdf96f7b6c346bd721ca6dc9b88a531bf84b658334fff2cc8925",
          "value": {
            "AlarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "OldStateValue": "OK",
            "NewStateValue": "ALARM",
            "StateChangeTime": "2026-11-05T09:01:16Z",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:7d09ee26b4a490128987748b283ec7eb33a7c250c16693af387dc3dfc6af3410"
        }
      },
      {
        "at": 128,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_08",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "collect",
          "source": "SNS probe receiver",
          "sourceKind": "provider",
          "kind": "notification-receipt",
          "title": "Probe notification received",
          "summary": "The dedicated probe received the matching notification 48 seconds after the alarm transition.",
          "occurredAt": "2026-11-05T09:02:04Z",
          "observedAt": "2026-11-05T09:02:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/collect/8",
          "schemaRef": "sha256:fc7c7fdf46ee4ec8996ae4aa3f93162684efb89e10db6785f94e08890b8e4819",
          "value": {
            "receiverId": "checkout-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "state": "ALARM",
            "stateChangeTime": "2026-11-05T09:01:16Z",
            "messageId": "demo-sns-alarm-live-01",
            "receivedAt": "2026-11-05T09:02:04Z",
            "ingestedAt": "2026-11-05T09:02:08Z",
            "latencySeconds": 48,
            "deadlineSeconds": 60,
            "clockUncertaintyMs": 250,
            "clockBasis": "receiver_ingress_utc",
            "clockBoundSynthetic": true,
            "claim": "receipt_by_dedicated_probe"
          },
          "scope": {
            "receiverId": "checkout-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:checkout-alerts",
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:fa7a7f622781515f777001b9c124a858eebed9794264da580d3a011750d5c040"
        }
      },
      {
        "at": 129,
        "kind": "step_finish",
        "stepKey": "collect",
        "outcome": "succeeded",
        "outputs": {
          "transition": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-live/collect/7",
                  "occurredAt": "2026-11-05T09:01:16Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-live_07"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T09:02:09Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "window": {
              "start": "2026-11-05T09:00:11Z",
              "end": "2026-11-05T09:03:11Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
              "authenticated": true
            }
          },
          "receipt": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-live/collect/8",
                  "occurredAt": "2026-11-05T09:02:04Z",
                  "receivedAt": "2026-11-05T09:02:04Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-live_07",
              "ev_alarm-live_08"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T09:02:09Z",
            "scope": "checkout-alarm-probe",
            "window": {
              "start": "2026-11-05T09:01:16Z",
              "end": "2026-11-05T09:02:16Z"
            },
            "source": {
              "namespace": "events/receiver",
              "identity": "checkout-alarm-probe",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 130,
        "kind": "step_start",
        "stepKey": "alarm_transition",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:alarm_transition:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-live/collect/7",
                  "occurredAt": "2026-11-05T09:01:16Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-live_07"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T09:02:09Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
            "window": {
              "start": "2026-11-05T09:00:11Z",
              "end": "2026-11-05T09:03:11Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:checkout-availability",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:0ea31e5eb4bccdbc8401692cff9143e8fe1709093673d8451bb7a03f9d00b32c",
        "checkpoint": null
      },
      {
        "at": 130,
        "kind": "step_start",
        "stepKey": "notification_received",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:notification_received:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-live/collect/8",
                  "occurredAt": "2026-11-05T09:02:04Z",
                  "receivedAt": "2026-11-05T09:02:04Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-live_07",
              "ev_alarm-live_08"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T09:02:09Z",
            "scope": "checkout-alarm-probe",
            "window": {
              "start": "2026-11-05T09:01:16Z",
              "end": "2026-11-05T09:02:16Z"
            },
            "source": {
              "namespace": "events/receiver",
              "identity": "checkout-alarm-probe",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:14ff67c42475d4e5add2095fbe4e99a8dff7151953e9be726e3f5a05a37ccd3e",
        "checkpoint": null
      },
      {
        "at": 131,
        "kind": "check_result",
        "stepKey": "alarm_transition",
        "check": {
          "verdict": "passed",
          "summary": "A qualifying transition occurred inside the declared 180-second window.",
          "expected": "ALARM transition within 180 s",
          "actual": "65 s",
          "reasonCode": "QUALIFYING_WITNESS",
          "evidenceIds": [
            "ev_alarm-live_07"
          ],
          "evaluatedThrough": "2026-11-05T09:02:11Z",
          "collection": "partial",
          "coverage": "sufficient",
          "proof": "witness",
          "window": {
            "start": "2026-11-05T09:00:11Z",
            "end": "2026-11-05T09:03:11Z"
          },
          "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 131,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_09",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "alarm_transition",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "A qualifying transition occurred inside the declared 180-second window.",
          "occurredAt": "2026-11-05T09:02:11Z",
          "observedAt": "2026-11-05T09:02:11Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/alarm_transition/9",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "A qualifying transition occurred inside the declared 180-second window.",
            "expected": "ALARM transition within 180 s",
            "actual": "65 s",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-live_07"
            ],
            "evaluatedThrough": "2026-11-05T09:02:11Z",
            "collection": "partial",
            "coverage": "sufficient",
            "proof": "witness",
            "window": {
              "start": "2026-11-05T09:00:11Z",
              "end": "2026-11-05T09:03:11Z"
            },
            "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T09:00:11Z",
            "end": "2026-11-05T09:03:11Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:6796ebfe6bc825b4a3efee8af0039daa6229b6bc41786798d77375a6eacb3823"
        }
      },
      {
        "at": 131,
        "kind": "step_finish",
        "stepKey": "alarm_transition",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-live_07"
            ],
            "evaluatedThrough": "2026-11-05T09:02:11Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 131,
        "kind": "check_result",
        "stepKey": "notification_received",
        "check": {
          "verdict": "passed",
          "summary": "The dedicated probe received the correlated notification within its deadline.",
          "expected": "Probe receipt within 60 s of the transition",
          "actual": "48 s",
          "reasonCode": "QUALIFYING_WITNESS",
          "evidenceIds": [
            "ev_alarm-live_07",
            "ev_alarm-live_08"
          ],
          "evaluatedThrough": "2026-11-05T09:02:11Z",
          "collection": "partial",
          "coverage": "sufficient",
          "proof": "witness",
          "window": {
            "start": "2026-11-05T09:01:16Z",
            "end": "2026-11-05T09:02:16Z"
          },
          "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 131,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_10",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "notification_received",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The dedicated probe received the correlated notification within its deadline.",
          "occurredAt": "2026-11-05T09:02:11Z",
          "observedAt": "2026-11-05T09:02:11Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/notification_received/10",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "The dedicated probe received the correlated notification within its deadline.",
            "expected": "Probe receipt within 60 s of the transition",
            "actual": "48 s",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-live_07",
              "ev_alarm-live_08"
            ],
            "evaluatedThrough": "2026-11-05T09:02:11Z",
            "collection": "partial",
            "coverage": "sufficient",
            "proof": "witness",
            "window": {
              "start": "2026-11-05T09:01:16Z",
              "end": "2026-11-05T09:02:16Z"
            },
            "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T09:01:16Z",
            "end": "2026-11-05T09:02:16Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:eb33a9c8afe2d008fb652c34d5e2456c492c0b16d9a84fb029412b9dd2fbb553"
        }
      },
      {
        "at": 131,
        "kind": "step_finish",
        "stepKey": "notification_received",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-live_07",
              "ev_alarm-live_08"
            ],
            "evaluatedThrough": "2026-11-05T09:02:11Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 132,
        "kind": "run_phase",
        "phase": "finalizing",
        "reason": "Main checks settled. Required cleanup is still running.",
        "termination": null
      },
      {
        "at": 132,
        "kind": "step_start",
        "stepKey": "stop_injection",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:stop_injection:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_checkout_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "step": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject"
          }
        },
        "resolvedInputsDigest": "sha256:1e156612cbbe21bca396d04d96167c78ab85be4066f7c288696a8f98a22dd90e",
        "checkpoint": null
      },
      {
        "at": 133,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXPf9a281b5fbd4a8436",
          "disposition": "active",
          "providerState": "stopping",
          "localState": null,
          "observedAt": "2026-11-05T09:02:13Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "A stop request was accepted; cessation has not yet been confirmed.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "stopping",
              "startTime": "2026-11-05T09:00:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "cancelled"
            }
          ]
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "provider"
      },
      {
        "at": 160,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_11",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "stop_injection",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-execution",
          "title": "External experiment is terminal",
          "summary": "A provider observation confirms stopped. This establishes cleanup of the tracked experiment, not workload recovery.",
          "occurredAt": "2026-11-05T09:02:38Z",
          "observedAt": "2026-11-05T09:02:40Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/stop_injection/11",
          "schemaRef": "sha256:c0c3c85379702f81d2d9b5a14ef3c6ecbe5a452faf3c9c0745c228c3e18bbd7e",
          "value": {
            "experimentId": "EXPf9a281b5fbd4a8436",
            "state": "stopped",
            "endTime": "2026-11-05T09:02:38Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:79500b156b15321ad1ae5339b46acbdbcbdab94d5a4c0c263e9a19719730ebe4"
        }
      },
      {
        "at": 160,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXPf9a281b5fbd4a8436",
          "disposition": "terminal",
          "providerState": "stopped",
          "localState": null,
          "observedAt": "2026-11-05T09:02:40Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The original external experiment is confirmed terminal.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "stopped",
              "startTime": "2026-11-05T09:00:11Z",
              "endTime": "2026-11-05T09:02:38Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "cancelled"
            }
          ]
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "provider"
      },
      {
        "at": 160,
        "kind": "step_finish",
        "stepKey": "stop_injection",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_alarm_live_20261105:inject:1:effect",
          "evidenceIds": [
            "ev_alarm-live_11"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 161,
        "kind": "step_start",
        "stepKey": "close_capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_live_20261105:close_capture:1",
        "resolvedInputs": {
          "step": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "capture"
          }
        },
        "resolvedInputsDigest": "sha256:1c5c124abb2562037141b4499ccc9904d496265b43e4daa57c3ae3fa398a2e03",
        "checkpoint": null
      },
      {
        "at": 162,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_12",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "close_capture",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Receiver capture closed",
          "summary": "Capture closed after experiment reconciliation settled; retained messages and their receipt times remain inspectable.",
          "occurredAt": "2026-11-05T09:02:42Z",
          "observedAt": "2026-11-05T09:02:42Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/close_capture/12",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_f9a281b5fb",
            "state": "closed",
            "lastCursor": "alarm-live/receipt/1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_checkout_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:444733878071fdf2e4c6b742b22548203c50ad0888e45612038f09c6727e8ff5"
        }
      },
      {
        "at": 162,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_live_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_live_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_f9a281b5fb",
          "disposition": "terminal",
          "providerState": null,
          "localState": "closed",
          "observedAt": "2026-11-05T09:02:42Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "The local probe session is closed.",
          "actions": []
        },
        "observedByStepKey": "close_capture",
        "sourceKind": "runtime"
      },
      {
        "at": 162,
        "kind": "step_finish",
        "stepKey": "close_capture",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_alarm_live_20261105:capture:1:effect",
          "evidenceIds": [
            "ev_alarm-live_12"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 163,
        "kind": "run_phase",
        "phase": "finished",
        "reason": "All required workflow operations and cleanup settled.",
        "termination": null
      },
      {
        "at": 190,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-live_13",
          "runId": "run_demo_alarm_live_20261105",
          "stepKey": "stop_injection",
          "source": "FIS report",
          "sourceKind": "provider",
          "kind": "artifact",
          "title": "Provider report reference available",
          "summary": "An independently generated FIS report is retained as an artifact reference. It does not change the sealed assessment.",
          "occurredAt": "2026-11-05T09:03:10Z",
          "observedAt": "2026-11-05T09:03:10Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-live/stop_injection/13",
          "schemaRef": "sha256:10c5a18eeec568b1687d444f7b622e284d03d6148794484f04f8f6ce2ab20758",
          "value": {
            "artifact": {
              "store": "s3",
              "arn": "arn:aws:s3:::synthetic-assessment-reports/alarm-live/experiment-report.pdf",
              "mediaType": "application/pdf",
              "synthetic": true
            },
            "reportState": "completed"
          },
          "scope": {
            "experimentId": "EXPf9a281b5fbd4a8436",
            "accountId": "444455556666",
            "region": "eu-central-1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:7b61f684f8ac1caf7815ac51a079d240a0390ec9a2dd8e2052ca2e76cc88439b"
        }
      }
    ]
  },
  {
    "key": "alarm-passed",
    "runId": "run_demo_alarm_passed_20261105",
    "title": "Orders · alarm notification",
    "description": "Assess the declared scope with explicit evidence and independent execution, criterion and cleanup outcomes.",
    "service": "Orders",
    "environment": "Production EU",
    "region": "eu-central-1",
    "accounts": [
      "444455556666"
    ],
    "owner": "Platform Resilience",
    "createdAt": "2026-11-05T08:30:00Z",
    "initialCursorSeconds": 200,
    "durationSeconds": 240,
    "synthetic": true,
    "revisionKey": "alarm",
    "scenario": {
      "scenarioId": "scn_application_alarm_delivery",
      "displayName": "Alarm-to-receiver assessment"
    },
    "admission": {
      "admittedAt": "2026-11-05T08:30:00Z",
      "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
      "inputsDigest": "sha256:aa97530aff7310a86f44371b4b99d4f701592943a565417e3d7a3d03abd9efed",
      "subject": {
        "deploymentRef": "deployment_orders_prod_euc1",
        "expectedDeploymentRevision": "release_2026_11_05.3",
        "service": "Orders",
        "environment": "production",
        "accountIds": [
          "444455556666"
        ],
        "region": "eu-central-1"
      },
      "inputs": {
        "templateId": "EXTc7da9fa6a2392b9f9",
        "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
        "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts",
        "receiverId": "orders-alarm-probe"
      },
      "bindings": {
        "aws": {
          "connectionId": "connection_orders_assessment",
          "capabilities": [
            "aws_assessment_scope"
          ]
        },
        "receiver": {
          "connectionId": "connection_orders_dedicated_probe",
          "capabilities": [
            "dedicated_notification_receiver"
          ]
        }
      },
      "requiredCriteria": [
        "alarm_transition",
        "notification_received"
      ],
      "policies": {
        "timeoutSeconds": 600,
        "finalizationTimeoutSeconds": 180,
        "concurrency": "queue_per_deployment"
      },
      "bindingObservedAt": "2026-11-05T08:30:00Z"
    },
    "_events": [
      {
        "at": 0,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_01",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "admission",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "admission",
          "title": "Revision and deployment bound",
          "summary": "The exact published revision, input values and trusted connection references were fixed before dispatch.",
          "occurredAt": "2026-11-05T08:30:00Z",
          "observedAt": "2026-11-05T08:30:00Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/admission/1",
          "schemaRef": "sha256:a9a9546dd44dfa0d6a0940f9829b98d45ffba2c3a6c511adb4b6da8ddc1e54d3",
          "value": {
            "scenarioRevisionId": "scnrev_alarm_delivery_002",
            "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
            "requiredCriteria": [
              "alarm_transition",
              "notification_received"
            ]
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f4083e81379f421b5790829832e61c7c3989f68ba341e34b5a975e2b53118b8f"
        }
      },
      {
        "at": 1,
        "kind": "run_phase",
        "phase": "running",
        "reason": "Main workflow admitted with a fixed criterion denominator.",
        "termination": null
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:capture:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_orders_dedicated_probe",
            "capabilities": [
              "dedicated_notification_receiver"
            ]
          },
          "receiverId": "orders-alarm-probe",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts",
          "leaseSeconds": 900
        },
        "resolvedInputsDigest": "sha256:e11f1bca83c46ecbf6c366d75e76bf1801bb585f38841c45ada166a5a401711e",
        "checkpoint": null
      },
      {
        "at": 2,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "opening",
          "observedAt": "2026-11-05T08:30:02Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A local capture intent exists; readiness is not yet established.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "baseline",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:baseline:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_orders_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability"
        },
        "resolvedInputsDigest": "sha256:41170ab630ec7992fcf4c9476f2c81aa07ef8f6c3e8cd07c07bc814254e5603a",
        "checkpoint": null
      },
      {
        "at": 5,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_02",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "baseline",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "observation",
          "title": "Alarm baseline observed",
          "summary": "The alarm is OK at the starting observation.",
          "occurredAt": "2026-11-05T08:30:04Z",
          "observedAt": "2026-11-05T08:30:05Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/baseline/2",
          "schemaRef": "sha256:3a57c20e4754fe8b5157afec9259195d1cb99d9074b946f6b2aa2c8a6b3c53d9",
          "value": {
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "state": "OK",
            "stateUpdatedAt": "2026-11-05T08:28:00Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f2b6d8463e4de6462df94955af33b96fc249117bdd0a38bab952edddb5a1e8f5"
        }
      },
      {
        "at": 5,
        "kind": "step_finish",
        "stepKey": "baseline",
        "outcome": "succeeded",
        "outputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_alarm-passed_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T08:30:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 6,
        "kind": "step_start",
        "stepKey": "baseline_ok",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:baseline_ok:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_alarm-passed_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T08:30:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
              "authenticated": true
            }
          },
          "proof": "complete",
          "expect": "value.state == \"OK\""
        },
        "resolvedInputsDigest": "sha256:7a8895d875981144bd8f856e17c0364eb5817596b0988df018de7fc1add01a36",
        "checkpoint": null
      },
      {
        "at": 7,
        "kind": "check_result",
        "stepKey": "baseline_ok",
        "check": {
          "verdict": "passed",
          "summary": "The mutation precondition is satisfied.",
          "expected": "Alarm state is OK",
          "actual": "OK",
          "reasonCode": "PREDICATE_TRUE",
          "evidenceIds": [
            "ev_alarm-passed_02"
          ],
          "evaluatedThrough": "2026-11-05T08:30:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "proof": "complete",
          "window": null,
          "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 7,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_03",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "baseline_ok",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The mutation precondition is satisfied.",
          "occurredAt": "2026-11-05T08:30:07Z",
          "observedAt": "2026-11-05T08:30:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/baseline_ok/3",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "The mutation precondition is satisfied.",
            "expected": "Alarm state is OK",
            "actual": "OK",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_alarm-passed_02"
            ],
            "evaluatedThrough": "2026-11-05T08:30:07Z",
            "collection": "complete",
            "coverage": "sufficient",
            "proof": "complete",
            "window": null,
            "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:25631f76f4b312517f9081dd92aafefaa445409f3a392429be79218cecc67193"
        }
      },
      {
        "at": 7,
        "kind": "step_finish",
        "stepKey": "baseline_ok",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_alarm-passed_02"
            ],
            "evaluatedThrough": "2026-11-05T08:30:07Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 8,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_04",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "capture",
          "source": "Receiver capture",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Dedicated receiver capture ready",
          "summary": "The probe session is active before injection. This proves readiness of the bound probe, not a production subscriber.",
          "occurredAt": "2026-11-05T08:30:08Z",
          "observedAt": "2026-11-05T08:30:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/capture/4",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_0979860488",
            "receiverId": "orders-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts",
            "queueArn": "arn:aws:sqs:eu-central-1:444455556666:orders-assessment-probe",
            "readyAt": "2026-11-05T08:30:08Z",
            "leaseExpiresAt": "2026-11-05T08:45:02Z",
            "coveragePolicy": "dedicated-receiver/v1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:1067c086e3c2666983e97fc2c7dc3342f2cf795dc07d88528cea8c00487d0f5b"
        }
      },
      {
        "at": 8,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_0979860488",
          "disposition": "active",
          "providerState": null,
          "localState": "ready",
          "observedAt": "2026-11-05T08:30:08Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A dedicated probe is collecting only its own subscription.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 8,
        "kind": "step_finish",
        "stepKey": "capture",
        "outcome": "succeeded",
        "outputs": {
          "capture": {
            "captureId": "capture_0979860488",
            "readyAt": "2026-11-05T08:30:08Z",
            "leaseExpiresAt": "2026-11-05T08:45:02Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 10,
        "kind": "step_start",
        "stepKey": "inject",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:inject:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_orders_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "templateId": "EXTc7da9fa6a2392b9f9"
        },
        "resolvedInputsDigest": "sha256:cfaf857f0bb801265fb9e99024bd2043cef99973efc70d88c1af688437089c82",
        "checkpoint": {
          "providerClientToken": "dispatch_alarm-passed_inject_1"
        }
      },
      {
        "at": 10,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "awaiting_response",
          "observedAt": "2026-11-05T08:30:10Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "Dispatch intent is durable. No provider identity has been observed yet.",
          "actions": []
        },
        "observedByStepKey": "inject",
        "sourceKind": "runtime"
      },
      {
        "at": 13,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_05",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "inject",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-execution",
          "title": "FIS experiment started",
          "summary": "The provider returned an experiment identity. Workflow start succeeded while the external experiment remains active.",
          "occurredAt": "2026-11-05T08:30:11Z",
          "observedAt": "2026-11-05T08:30:13Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/inject/5",
          "schemaRef": "sha256:c0c3c85379702f81d2d9b5a14ef3c6ecbe5a452faf3c9c0745c228c3e18bbd7e",
          "value": {
            "experimentId": "EXP097986048835c3da5",
            "experimentTemplateId": "EXTc7da9fa6a2392b9f9",
            "state": "running",
            "startTime": "2026-11-05T08:30:11Z",
            "selectedScope": {
              "resourceType": "aws:ec2:subnet",
              "uniqueResources": 3,
              "membershipCount": 3,
              "accountId": "444455556666"
            }
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:87ee6ddd4a5f8ff07ef12f81a460e1a446a0f26a00c69be17d0f191711bf1ae5"
        }
      },
      {
        "at": 13,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP097986048835c3da5",
          "disposition": "active",
          "providerState": "running",
          "localState": null,
          "observedAt": "2026-11-05T08:30:13Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The Start step completed; the FIS experiment is independently running.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "initiating",
              "startTime": "2026-11-05T08:30:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "pending"
            }
          ]
        },
        "observedByStepKey": "inject",
        "sourceKind": "provider"
      },
      {
        "at": 13,
        "kind": "step_finish",
        "stepKey": "inject",
        "outcome": "succeeded",
        "outputs": {
          "experiment": {
            "provider": "aws/fis",
            "nativeId": "EXP097986048835c3da5",
            "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
            "accountId": "444455556666",
            "region": "eu-central-1"
          },
          "submittedAt": "2026-11-05T08:30:10Z",
          "providerStartedAt": "2026-11-05T08:30:11Z"
        },
        "error": null,
        "reason": null
      },
      {
        "at": 14,
        "kind": "step_start",
        "stepKey": "collect",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:collect:1",
        "resolvedInputs": {
          "captureStep": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "capture"
          },
          "injectionStep": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject"
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts",
          "receiverId": "orders-alarm-probe",
          "transitionWindowSeconds": 180,
          "receiptDeadlineSeconds": 60,
          "collectionGraceSeconds": 30
        },
        "resolvedInputsDigest": "sha256:c09fc90768fdc661628fabe3f320e5c0cf04272729ce893a274db75f9831e99d",
        "checkpoint": {
          "captureId": "capture_0979860488",
          "cursor": "alarm-passed/ready",
          "providerStartedAt": "2026-11-05T08:30:11Z",
          "transitionDeadline": "2026-11-05T08:33:11Z"
        }
      },
      {
        "at": 51,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_06",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "inject",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-action",
          "title": "Availability Zone isolation active",
          "summary": "The named provider action is running. Selected resources are not a generic per-resource fault-result record.",
          "occurredAt": "2026-11-05T08:30:49Z",
          "observedAt": "2026-11-05T08:30:51Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/inject/6",
          "schemaRef": "sha256:eea4c43d9319e91de68a1cef58e7d9c64752111c878cb1bdb9efac44f0594a34",
          "value": {
            "experimentId": "EXP097986048835c3da5",
            "actionName": "isolateZone",
            "actionId": "aws:network:disrupt-connectivity",
            "state": "running"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:50ec5606764500cebc1397c946b7131b6c3571258fc7cae99ff58cec56878bee"
        }
      },
      {
        "at": 51,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP097986048835c3da5",
          "disposition": "active",
          "providerState": "running",
          "localState": null,
          "observedAt": "2026-11-05T08:30:51Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The latest provider action observation confirms isolation is running.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "running",
              "startTime": "2026-11-05T08:30:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "pending"
            }
          ]
        },
        "observedByStepKey": "inject",
        "sourceKind": "provider"
      },
      {
        "at": 78,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_07",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "collect",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "alarm-transition",
          "title": "Alarm entered ALARM",
          "summary": "A specific OK → ALARM transition is correlated by alarm ARN and state-change time.",
          "occurredAt": "2026-11-05T08:31:16Z",
          "observedAt": "2026-11-05T08:31:18Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/collect/7",
          "schemaRef": "sha256:7765857a2fdcfdf96f7b6c346bd721ca6dc9b88a531bf84b658334fff2cc8925",
          "value": {
            "AlarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "OldStateValue": "OK",
            "NewStateValue": "ALARM",
            "StateChangeTime": "2026-11-05T08:31:16Z",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:43126df0f6a55ed56b30f92a59d74081ca91267a28b09dcddbb882e2a9dfa1de"
        }
      },
      {
        "at": 128,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_08",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "collect",
          "source": "SNS probe receiver",
          "sourceKind": "provider",
          "kind": "notification-receipt",
          "title": "Probe notification received",
          "summary": "The dedicated probe received the matching notification 48 seconds after the alarm transition.",
          "occurredAt": "2026-11-05T08:32:04Z",
          "observedAt": "2026-11-05T08:32:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/collect/8",
          "schemaRef": "sha256:fc7c7fdf46ee4ec8996ae4aa3f93162684efb89e10db6785f94e08890b8e4819",
          "value": {
            "receiverId": "orders-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts",
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "state": "ALARM",
            "stateChangeTime": "2026-11-05T08:31:16Z",
            "messageId": "demo-sns-alarm-passed-01",
            "receivedAt": "2026-11-05T08:32:04Z",
            "ingestedAt": "2026-11-05T08:32:08Z",
            "latencySeconds": 48,
            "deadlineSeconds": 60,
            "clockUncertaintyMs": 250,
            "clockBasis": "receiver_ingress_utc",
            "clockBoundSynthetic": true,
            "claim": "receipt_by_dedicated_probe"
          },
          "scope": {
            "receiverId": "orders-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:orders-alerts",
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:5722a61f8585a3e987be975db4f2c1f6756edab588fd7137bab593a83f69dfc8"
        }
      },
      {
        "at": 129,
        "kind": "step_finish",
        "stepKey": "collect",
        "outcome": "succeeded",
        "outputs": {
          "transition": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-passed/collect/7",
                  "occurredAt": "2026-11-05T08:31:16Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-passed_07"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T08:32:09Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "window": {
              "start": "2026-11-05T08:30:11Z",
              "end": "2026-11-05T08:33:11Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
              "authenticated": true
            }
          },
          "receipt": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-passed/collect/8",
                  "occurredAt": "2026-11-05T08:32:04Z",
                  "receivedAt": "2026-11-05T08:32:04Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-passed_07",
              "ev_alarm-passed_08"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T08:32:09Z",
            "scope": "orders-alarm-probe",
            "window": {
              "start": "2026-11-05T08:31:16Z",
              "end": "2026-11-05T08:32:16Z"
            },
            "source": {
              "namespace": "events/receiver",
              "identity": "orders-alarm-probe",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 130,
        "kind": "step_start",
        "stepKey": "alarm_transition",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:alarm_transition:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-passed/collect/7",
                  "occurredAt": "2026-11-05T08:31:16Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-passed_07"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T08:32:09Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
            "window": {
              "start": "2026-11-05T08:30:11Z",
              "end": "2026-11-05T08:33:11Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:orders-availability",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:9848c08b40a63d06162ce60d61513bbc1cc51e2313cf4dbb6b9e925b83f19df4",
        "checkpoint": null
      },
      {
        "at": 130,
        "kind": "step_start",
        "stepKey": "notification_received",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:notification_received:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-passed/collect/8",
                  "occurredAt": "2026-11-05T08:32:04Z",
                  "receivedAt": "2026-11-05T08:32:04Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-passed_07",
              "ev_alarm-passed_08"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T08:32:09Z",
            "scope": "orders-alarm-probe",
            "window": {
              "start": "2026-11-05T08:31:16Z",
              "end": "2026-11-05T08:32:16Z"
            },
            "source": {
              "namespace": "events/receiver",
              "identity": "orders-alarm-probe",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:9f69c5d9df1189d639797f2b4638b95f352bf71bc29f4289b5cf6b46d6ea43d5",
        "checkpoint": null
      },
      {
        "at": 131,
        "kind": "check_result",
        "stepKey": "alarm_transition",
        "check": {
          "verdict": "passed",
          "summary": "A qualifying transition occurred inside the declared 180-second window.",
          "expected": "ALARM transition within 180 s",
          "actual": "65 s",
          "reasonCode": "QUALIFYING_WITNESS",
          "evidenceIds": [
            "ev_alarm-passed_07"
          ],
          "evaluatedThrough": "2026-11-05T08:32:11Z",
          "collection": "partial",
          "coverage": "sufficient",
          "proof": "witness",
          "window": {
            "start": "2026-11-05T08:30:11Z",
            "end": "2026-11-05T08:33:11Z"
          },
          "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 131,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_09",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "alarm_transition",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "A qualifying transition occurred inside the declared 180-second window.",
          "occurredAt": "2026-11-05T08:32:11Z",
          "observedAt": "2026-11-05T08:32:11Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/alarm_transition/9",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "A qualifying transition occurred inside the declared 180-second window.",
            "expected": "ALARM transition within 180 s",
            "actual": "65 s",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-passed_07"
            ],
            "evaluatedThrough": "2026-11-05T08:32:11Z",
            "collection": "partial",
            "coverage": "sufficient",
            "proof": "witness",
            "window": {
              "start": "2026-11-05T08:30:11Z",
              "end": "2026-11-05T08:33:11Z"
            },
            "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T08:30:11Z",
            "end": "2026-11-05T08:33:11Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:973c011b814ccbc2ab4859938e5dc4dfce2ebcc6b4b93fc03a3a7eceb2481857"
        }
      },
      {
        "at": 131,
        "kind": "step_finish",
        "stepKey": "alarm_transition",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-passed_07"
            ],
            "evaluatedThrough": "2026-11-05T08:32:11Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 131,
        "kind": "check_result",
        "stepKey": "notification_received",
        "check": {
          "verdict": "passed",
          "summary": "The dedicated probe received the correlated notification within its deadline.",
          "expected": "Probe receipt within 60 s of the transition",
          "actual": "48 s",
          "reasonCode": "QUALIFYING_WITNESS",
          "evidenceIds": [
            "ev_alarm-passed_07",
            "ev_alarm-passed_08"
          ],
          "evaluatedThrough": "2026-11-05T08:32:11Z",
          "collection": "partial",
          "coverage": "sufficient",
          "proof": "witness",
          "window": {
            "start": "2026-11-05T08:31:16Z",
            "end": "2026-11-05T08:32:16Z"
          },
          "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 131,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_10",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "notification_received",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The dedicated probe received the correlated notification within its deadline.",
          "occurredAt": "2026-11-05T08:32:11Z",
          "observedAt": "2026-11-05T08:32:11Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/notification_received/10",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "The dedicated probe received the correlated notification within its deadline.",
            "expected": "Probe receipt within 60 s of the transition",
            "actual": "48 s",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-passed_07",
              "ev_alarm-passed_08"
            ],
            "evaluatedThrough": "2026-11-05T08:32:11Z",
            "collection": "partial",
            "coverage": "sufficient",
            "proof": "witness",
            "window": {
              "start": "2026-11-05T08:31:16Z",
              "end": "2026-11-05T08:32:16Z"
            },
            "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T08:31:16Z",
            "end": "2026-11-05T08:32:16Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:c7fe0a3e649f4666c7662ca61a99b10d18e4cebda2e617b2c00d19ce58c0a54f"
        }
      },
      {
        "at": 131,
        "kind": "step_finish",
        "stepKey": "notification_received",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-passed_07",
              "ev_alarm-passed_08"
            ],
            "evaluatedThrough": "2026-11-05T08:32:11Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 132,
        "kind": "run_phase",
        "phase": "finalizing",
        "reason": "Main checks settled. Required cleanup is still running.",
        "termination": null
      },
      {
        "at": 132,
        "kind": "step_start",
        "stepKey": "stop_injection",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:stop_injection:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_orders_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "step": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject"
          }
        },
        "resolvedInputsDigest": "sha256:01321899d54e48953cf46a062a0012d0caec706f54a707157e33fa3a53850883",
        "checkpoint": null
      },
      {
        "at": 133,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP097986048835c3da5",
          "disposition": "active",
          "providerState": "stopping",
          "localState": null,
          "observedAt": "2026-11-05T08:32:13Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "A stop request was accepted; cessation has not yet been confirmed.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "stopping",
              "startTime": "2026-11-05T08:30:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "cancelled"
            }
          ]
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "provider"
      },
      {
        "at": 160,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_11",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "stop_injection",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-execution",
          "title": "External experiment is terminal",
          "summary": "A provider observation confirms stopped. This establishes cleanup of the tracked experiment, not workload recovery.",
          "occurredAt": "2026-11-05T08:32:38Z",
          "observedAt": "2026-11-05T08:32:40Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/stop_injection/11",
          "schemaRef": "sha256:c0c3c85379702f81d2d9b5a14ef3c6ecbe5a452faf3c9c0745c228c3e18bbd7e",
          "value": {
            "experimentId": "EXP097986048835c3da5",
            "state": "stopped",
            "endTime": "2026-11-05T08:32:38Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:39fd3fb4bb8de543f0c79bc2ec76c1f1cdbba1ba0700269c33529517d3cd0232"
        }
      },
      {
        "at": 160,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP097986048835c3da5",
          "disposition": "terminal",
          "providerState": "stopped",
          "localState": null,
          "observedAt": "2026-11-05T08:32:40Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The original external experiment is confirmed terminal.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "stopped",
              "startTime": "2026-11-05T08:30:11Z",
              "endTime": "2026-11-05T08:32:38Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "cancelled"
            }
          ]
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "provider"
      },
      {
        "at": 160,
        "kind": "step_finish",
        "stepKey": "stop_injection",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_alarm_passed_20261105:inject:1:effect",
          "evidenceIds": [
            "ev_alarm-passed_11"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 161,
        "kind": "step_start",
        "stepKey": "close_capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_passed_20261105:close_capture:1",
        "resolvedInputs": {
          "step": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "capture"
          }
        },
        "resolvedInputsDigest": "sha256:18b35dcf6837781951e791564a11cc18539653c6bca26596cf711fc0365a9920",
        "checkpoint": null
      },
      {
        "at": 162,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_12",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "close_capture",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Receiver capture closed",
          "summary": "Capture closed after experiment reconciliation settled; retained messages and their receipt times remain inspectable.",
          "occurredAt": "2026-11-05T08:32:42Z",
          "observedAt": "2026-11-05T08:32:42Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/close_capture/12",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_0979860488",
            "state": "closed",
            "lastCursor": "alarm-passed/receipt/1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_orders_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:6fd48087d1ea29e1c08dcd6ac492bc8c657b6510e83d3c2980c8f2a6c575d9a4"
        }
      },
      {
        "at": 162,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_passed_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_passed_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_0979860488",
          "disposition": "terminal",
          "providerState": null,
          "localState": "closed",
          "observedAt": "2026-11-05T08:32:42Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "The local probe session is closed.",
          "actions": []
        },
        "observedByStepKey": "close_capture",
        "sourceKind": "runtime"
      },
      {
        "at": 162,
        "kind": "step_finish",
        "stepKey": "close_capture",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_alarm_passed_20261105:capture:1:effect",
          "evidenceIds": [
            "ev_alarm-passed_12"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 163,
        "kind": "run_phase",
        "phase": "finished",
        "reason": "All required workflow operations and cleanup settled.",
        "termination": null
      },
      {
        "at": 190,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-passed_13",
          "runId": "run_demo_alarm_passed_20261105",
          "stepKey": "stop_injection",
          "source": "FIS report",
          "sourceKind": "provider",
          "kind": "artifact",
          "title": "Provider report reference available",
          "summary": "An independently generated FIS report is retained as an artifact reference. It does not change the sealed assessment.",
          "occurredAt": "2026-11-05T08:33:10Z",
          "observedAt": "2026-11-05T08:33:10Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-passed/stop_injection/13",
          "schemaRef": "sha256:10c5a18eeec568b1687d444f7b622e284d03d6148794484f04f8f6ce2ab20758",
          "value": {
            "artifact": {
              "store": "s3",
              "arn": "arn:aws:s3:::synthetic-assessment-reports/alarm-passed/experiment-report.pdf",
              "mediaType": "application/pdf",
              "synthetic": true
            },
            "reportState": "completed"
          },
          "scope": {
            "experimentId": "EXP097986048835c3da5",
            "accountId": "444455556666",
            "region": "eu-central-1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:c01cc716af54c677ae82f669a5c8f9aa41d8a41058d159478d4d1bca995f96da"
        }
      }
    ]
  },
  {
    "key": "alarm-late",
    "runId": "run_demo_alarm_late_20261105",
    "title": "Payments · alarm notification",
    "description": "Assess the declared scope with explicit evidence and independent execution, criterion and cleanup outcomes.",
    "service": "Payments",
    "environment": "Production EU",
    "region": "eu-central-1",
    "accounts": [
      "444455556666"
    ],
    "owner": "Platform Resilience",
    "createdAt": "2026-11-05T08:00:00Z",
    "initialCursorSeconds": 260,
    "durationSeconds": 300,
    "synthetic": true,
    "revisionKey": "alarm",
    "scenario": {
      "scenarioId": "scn_application_alarm_delivery",
      "displayName": "Alarm-to-receiver assessment"
    },
    "admission": {
      "admittedAt": "2026-11-05T08:00:00Z",
      "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
      "inputsDigest": "sha256:9cd06484ab441769ab5c87be914df9cbf69a9856493ed93cccf8a2eda9b8d334",
      "subject": {
        "deploymentRef": "deployment_payments_prod_euc1",
        "expectedDeploymentRevision": "release_2026_11_05.3",
        "service": "Payments",
        "environment": "production",
        "accountIds": [
          "444455556666"
        ],
        "region": "eu-central-1"
      },
      "inputs": {
        "templateId": "EXTea99cca84ccb4af41",
        "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
        "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts",
        "receiverId": "payments-alarm-probe"
      },
      "bindings": {
        "aws": {
          "connectionId": "connection_payments_assessment",
          "capabilities": [
            "aws_assessment_scope"
          ]
        },
        "receiver": {
          "connectionId": "connection_payments_dedicated_probe",
          "capabilities": [
            "dedicated_notification_receiver"
          ]
        }
      },
      "requiredCriteria": [
        "alarm_transition",
        "notification_received"
      ],
      "policies": {
        "timeoutSeconds": 600,
        "finalizationTimeoutSeconds": 180,
        "concurrency": "queue_per_deployment"
      },
      "bindingObservedAt": "2026-11-05T08:00:00Z"
    },
    "_events": [
      {
        "at": 0,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_01",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "admission",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "admission",
          "title": "Revision and deployment bound",
          "summary": "The exact published revision, input values and trusted connection references were fixed before dispatch.",
          "occurredAt": "2026-11-05T08:00:00Z",
          "observedAt": "2026-11-05T08:00:00Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/admission/1",
          "schemaRef": "sha256:a9a9546dd44dfa0d6a0940f9829b98d45ffba2c3a6c511adb4b6da8ddc1e54d3",
          "value": {
            "scenarioRevisionId": "scnrev_alarm_delivery_002",
            "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
            "requiredCriteria": [
              "alarm_transition",
              "notification_received"
            ]
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f4083e81379f421b5790829832e61c7c3989f68ba341e34b5a975e2b53118b8f"
        }
      },
      {
        "at": 1,
        "kind": "run_phase",
        "phase": "running",
        "reason": "Main workflow admitted with a fixed criterion denominator.",
        "termination": null
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:capture:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_payments_dedicated_probe",
            "capabilities": [
              "dedicated_notification_receiver"
            ]
          },
          "receiverId": "payments-alarm-probe",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts",
          "leaseSeconds": 900
        },
        "resolvedInputsDigest": "sha256:9a6870a8fb86331806b889e44fa2dc2f38f599b751168c2f53470681c679d994",
        "checkpoint": null
      },
      {
        "at": 2,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "opening",
          "observedAt": "2026-11-05T08:00:02Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A local capture intent exists; readiness is not yet established.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "baseline",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:baseline:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_payments_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability"
        },
        "resolvedInputsDigest": "sha256:25313f6220b9acab96754d1a518a5c26e92b2615052f2ff94f9f85b01a215f56",
        "checkpoint": null
      },
      {
        "at": 5,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_02",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "baseline",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "observation",
          "title": "Alarm baseline observed",
          "summary": "The alarm is OK at the starting observation.",
          "occurredAt": "2026-11-05T08:00:04Z",
          "observedAt": "2026-11-05T08:00:05Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/baseline/2",
          "schemaRef": "sha256:3a57c20e4754fe8b5157afec9259195d1cb99d9074b946f6b2aa2c8a6b3c53d9",
          "value": {
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "state": "OK",
            "stateUpdatedAt": "2026-11-05T07:58:00Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:455b01f52f54bf99b5add8737ededac120919e3fadc55954a3e02f5b8c5016f4"
        }
      },
      {
        "at": 5,
        "kind": "step_finish",
        "stepKey": "baseline",
        "outcome": "succeeded",
        "outputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_alarm-late_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T08:00:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 6,
        "kind": "step_start",
        "stepKey": "baseline_ok",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:baseline_ok:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_alarm-late_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T08:00:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
              "authenticated": true
            }
          },
          "proof": "complete",
          "expect": "value.state == \"OK\""
        },
        "resolvedInputsDigest": "sha256:bb99e967260a7de3b2665eef18792e087e8c8b40bba1cdba29ea01cc631b6137",
        "checkpoint": null
      },
      {
        "at": 7,
        "kind": "check_result",
        "stepKey": "baseline_ok",
        "check": {
          "verdict": "passed",
          "summary": "The mutation precondition is satisfied.",
          "expected": "Alarm state is OK",
          "actual": "OK",
          "reasonCode": "PREDICATE_TRUE",
          "evidenceIds": [
            "ev_alarm-late_02"
          ],
          "evaluatedThrough": "2026-11-05T08:00:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "proof": "complete",
          "window": null,
          "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 7,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_03",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "baseline_ok",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The mutation precondition is satisfied.",
          "occurredAt": "2026-11-05T08:00:07Z",
          "observedAt": "2026-11-05T08:00:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/baseline_ok/3",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "The mutation precondition is satisfied.",
            "expected": "Alarm state is OK",
            "actual": "OK",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_alarm-late_02"
            ],
            "evaluatedThrough": "2026-11-05T08:00:07Z",
            "collection": "complete",
            "coverage": "sufficient",
            "proof": "complete",
            "window": null,
            "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:52240311b94705b6a4a14a59f9bb947c661531e4a79e5c4d844ec7cf541c112b"
        }
      },
      {
        "at": 7,
        "kind": "step_finish",
        "stepKey": "baseline_ok",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_alarm-late_02"
            ],
            "evaluatedThrough": "2026-11-05T08:00:07Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 8,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_04",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "capture",
          "source": "Receiver capture",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Dedicated receiver capture ready",
          "summary": "The probe session is active before injection. This proves readiness of the bound probe, not a production subscriber.",
          "occurredAt": "2026-11-05T08:00:08Z",
          "observedAt": "2026-11-05T08:00:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/capture/4",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_8ddbf3cc5c",
            "receiverId": "payments-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts",
            "queueArn": "arn:aws:sqs:eu-central-1:444455556666:payments-assessment-probe",
            "readyAt": "2026-11-05T08:00:08Z",
            "leaseExpiresAt": "2026-11-05T08:15:02Z",
            "coveragePolicy": "dedicated-receiver/v1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:1050a7014a47e7dbab504a11c558cd3c7998bdac70b3815ecc1b80d274f0a15b"
        }
      },
      {
        "at": 8,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_8ddbf3cc5c",
          "disposition": "active",
          "providerState": null,
          "localState": "ready",
          "observedAt": "2026-11-05T08:00:08Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A dedicated probe is collecting only its own subscription.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 8,
        "kind": "step_finish",
        "stepKey": "capture",
        "outcome": "succeeded",
        "outputs": {
          "capture": {
            "captureId": "capture_8ddbf3cc5c",
            "readyAt": "2026-11-05T08:00:08Z",
            "leaseExpiresAt": "2026-11-05T08:15:02Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 10,
        "kind": "step_start",
        "stepKey": "inject",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:inject:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_payments_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "templateId": "EXTea99cca84ccb4af41"
        },
        "resolvedInputsDigest": "sha256:8ce17bbad52844871508740e91b8bc8ad34cc601bc5cf6711607c1f295cb928c",
        "checkpoint": {
          "providerClientToken": "dispatch_alarm-late_inject_1"
        }
      },
      {
        "at": 10,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "awaiting_response",
          "observedAt": "2026-11-05T08:00:10Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "Dispatch intent is durable. No provider identity has been observed yet.",
          "actions": []
        },
        "observedByStepKey": "inject",
        "sourceKind": "runtime"
      },
      {
        "at": 13,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_05",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "inject",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-execution",
          "title": "FIS experiment started",
          "summary": "The provider returned an experiment identity. Workflow start succeeded while the external experiment remains active.",
          "occurredAt": "2026-11-05T08:00:11Z",
          "observedAt": "2026-11-05T08:00:13Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/inject/5",
          "schemaRef": "sha256:c0c3c85379702f81d2d9b5a14ef3c6ecbe5a452faf3c9c0745c228c3e18bbd7e",
          "value": {
            "experimentId": "EXP8ddbf3cc5ca77fdfb",
            "experimentTemplateId": "EXTea99cca84ccb4af41",
            "state": "running",
            "startTime": "2026-11-05T08:00:11Z",
            "selectedScope": {
              "resourceType": "aws:ec2:subnet",
              "uniqueResources": 3,
              "membershipCount": 3,
              "accountId": "444455556666"
            }
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:51fd69ec179dfb426e1c9974e4b38cb89f9fc26b5076d9d4cf4261b06dea1f92"
        }
      },
      {
        "at": 13,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP8ddbf3cc5ca77fdfb",
          "disposition": "active",
          "providerState": "running",
          "localState": null,
          "observedAt": "2026-11-05T08:00:13Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The Start step completed; the FIS experiment is independently running.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "initiating",
              "startTime": "2026-11-05T08:00:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "pending"
            }
          ]
        },
        "observedByStepKey": "inject",
        "sourceKind": "provider"
      },
      {
        "at": 13,
        "kind": "step_finish",
        "stepKey": "inject",
        "outcome": "succeeded",
        "outputs": {
          "experiment": {
            "provider": "aws/fis",
            "nativeId": "EXP8ddbf3cc5ca77fdfb",
            "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
            "accountId": "444455556666",
            "region": "eu-central-1"
          },
          "submittedAt": "2026-11-05T08:00:10Z",
          "providerStartedAt": "2026-11-05T08:00:11Z"
        },
        "error": null,
        "reason": null
      },
      {
        "at": 14,
        "kind": "step_start",
        "stepKey": "collect",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:collect:1",
        "resolvedInputs": {
          "captureStep": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "capture"
          },
          "injectionStep": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject"
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts",
          "receiverId": "payments-alarm-probe",
          "transitionWindowSeconds": 180,
          "receiptDeadlineSeconds": 60,
          "collectionGraceSeconds": 30
        },
        "resolvedInputsDigest": "sha256:59767fef7da4d8c18f122fa934aae2a2740d7f9e72569bb13d1332df8251e67f",
        "checkpoint": {
          "captureId": "capture_8ddbf3cc5c",
          "cursor": "alarm-late/ready",
          "providerStartedAt": "2026-11-05T08:00:11Z",
          "transitionDeadline": "2026-11-05T08:03:11Z"
        }
      },
      {
        "at": 51,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_06",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "inject",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-action",
          "title": "Availability Zone isolation active",
          "summary": "The named provider action is running. Selected resources are not a generic per-resource fault-result record.",
          "occurredAt": "2026-11-05T08:00:49Z",
          "observedAt": "2026-11-05T08:00:51Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/inject/6",
          "schemaRef": "sha256:eea4c43d9319e91de68a1cef58e7d9c64752111c878cb1bdb9efac44f0594a34",
          "value": {
            "experimentId": "EXP8ddbf3cc5ca77fdfb",
            "actionName": "isolateZone",
            "actionId": "aws:network:disrupt-connectivity",
            "state": "running"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:7d5171034097df45c6f8495374019b475a4a7006e4a4e8353b95b62d164f7619"
        }
      },
      {
        "at": 51,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP8ddbf3cc5ca77fdfb",
          "disposition": "active",
          "providerState": "running",
          "localState": null,
          "observedAt": "2026-11-05T08:00:51Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The latest provider action observation confirms isolation is running.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "running",
              "startTime": "2026-11-05T08:00:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "pending"
            }
          ]
        },
        "observedByStepKey": "inject",
        "sourceKind": "provider"
      },
      {
        "at": 78,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_07",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "collect",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "alarm-transition",
          "title": "Alarm entered ALARM",
          "summary": "A specific OK → ALARM transition is correlated by alarm ARN and state-change time.",
          "occurredAt": "2026-11-05T08:01:16Z",
          "observedAt": "2026-11-05T08:01:18Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/collect/7",
          "schemaRef": "sha256:7765857a2fdcfdf96f7b6c346bd721ca6dc9b88a531bf84b658334fff2cc8925",
          "value": {
            "AlarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "OldStateValue": "OK",
            "NewStateValue": "ALARM",
            "StateChangeTime": "2026-11-05T08:01:16Z",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:1f02de24809275d6457d25ae5d082efe3120da63557aa4810237364ea6974a7a"
        }
      },
      {
        "at": 155,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_08",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "collect",
          "source": "SNS probe receiver",
          "sourceKind": "provider",
          "kind": "notification-receipt",
          "title": "Probe notification received",
          "summary": "The dedicated probe received the matching notification 15 seconds after its deadline.",
          "occurredAt": "2026-11-05T08:02:31Z",
          "observedAt": "2026-11-05T08:02:35Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/collect/8",
          "schemaRef": "sha256:fc7c7fdf46ee4ec8996ae4aa3f93162684efb89e10db6785f94e08890b8e4819",
          "value": {
            "receiverId": "payments-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts",
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "state": "ALARM",
            "stateChangeTime": "2026-11-05T08:01:16Z",
            "messageId": "demo-sns-alarm-late-01",
            "receivedAt": "2026-11-05T08:02:31Z",
            "ingestedAt": "2026-11-05T08:02:35Z",
            "latencySeconds": 75,
            "deadlineSeconds": 60,
            "clockUncertaintyMs": 250,
            "clockBasis": "receiver_ingress_utc",
            "clockBoundSynthetic": true,
            "claim": "receipt_by_dedicated_probe"
          },
          "scope": {
            "receiverId": "payments-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:payments-alerts",
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:3f88d27ecce141f1b6023980bc2e38d070d0c72fa359449afddbbbd4d9cea95f"
        }
      },
      {
        "at": 170,
        "kind": "step_finish",
        "stepKey": "collect",
        "outcome": "succeeded",
        "outputs": {
          "transition": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-late/collect/7",
                  "occurredAt": "2026-11-05T08:01:16Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-late_07"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T08:02:50Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "window": {
              "start": "2026-11-05T08:00:11Z",
              "end": "2026-11-05T08:03:11Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
              "authenticated": true
            }
          },
          "receipt": {
            "value": {
              "records": []
            },
            "evidenceIds": [
              "ev_alarm-late_07",
              "ev_alarm-late_08"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T08:02:50Z",
            "scope": "payments-alarm-probe",
            "window": {
              "start": "2026-11-05T08:01:16Z",
              "end": "2026-11-05T08:02:16Z"
            },
            "source": {
              "namespace": "events/receiver",
              "identity": "payments-alarm-probe",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 171,
        "kind": "step_start",
        "stepKey": "alarm_transition",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:alarm_transition:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "records": [
                {
                  "sourceRecordId": "demo/alarm-late/collect/7",
                  "occurredAt": "2026-11-05T08:01:16Z"
                }
              ]
            },
            "evidenceIds": [
              "ev_alarm-late_07"
            ],
            "collection": "partial",
            "coverage": "sufficient",
            "windowClosed": false,
            "observedAt": "2026-11-05T08:02:50Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
            "window": {
              "start": "2026-11-05T08:00:11Z",
              "end": "2026-11-05T08:03:11Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:payments-availability",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:9c82de9cae837fcd1b2c70ebe4c562883aaaadcca3ec8c44a2736bf9e505bff1",
        "checkpoint": null
      },
      {
        "at": 171,
        "kind": "step_start",
        "stepKey": "notification_received",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:notification_received:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "records": []
            },
            "evidenceIds": [
              "ev_alarm-late_07",
              "ev_alarm-late_08"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T08:02:50Z",
            "scope": "payments-alarm-probe",
            "window": {
              "start": "2026-11-05T08:01:16Z",
              "end": "2026-11-05T08:02:16Z"
            },
            "source": {
              "namespace": "events/receiver",
              "identity": "payments-alarm-probe",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:6f19321450013b3f084e10d3f1e0aadefd6c0402236fe2dfc5e2c348c2a90a2d",
        "checkpoint": null
      },
      {
        "at": 172,
        "kind": "check_result",
        "stepKey": "alarm_transition",
        "check": {
          "verdict": "passed",
          "summary": "A qualifying transition occurred inside the declared 180-second window.",
          "expected": "ALARM transition within 180 s",
          "actual": "65 s",
          "reasonCode": "QUALIFYING_WITNESS",
          "evidenceIds": [
            "ev_alarm-late_07"
          ],
          "evaluatedThrough": "2026-11-05T08:02:52Z",
          "collection": "partial",
          "coverage": "sufficient",
          "proof": "witness",
          "window": {
            "start": "2026-11-05T08:00:11Z",
            "end": "2026-11-05T08:03:11Z"
          },
          "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 172,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_09",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "alarm_transition",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "A qualifying transition occurred inside the declared 180-second window.",
          "occurredAt": "2026-11-05T08:02:52Z",
          "observedAt": "2026-11-05T08:02:52Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/alarm_transition/9",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "A qualifying transition occurred inside the declared 180-second window.",
            "expected": "ALARM transition within 180 s",
            "actual": "65 s",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-late_07"
            ],
            "evaluatedThrough": "2026-11-05T08:02:52Z",
            "collection": "partial",
            "coverage": "sufficient",
            "proof": "witness",
            "window": {
              "start": "2026-11-05T08:00:11Z",
              "end": "2026-11-05T08:03:11Z"
            },
            "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T08:00:11Z",
            "end": "2026-11-05T08:03:11Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:6872b78b44303a497f30d3c65a71052e266bda5e465b1df51c006be020777050"
        }
      },
      {
        "at": 172,
        "kind": "step_finish",
        "stepKey": "alarm_transition",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "QUALIFYING_WITNESS",
            "evidenceIds": [
              "ev_alarm-late_07"
            ],
            "evaluatedThrough": "2026-11-05T08:02:52Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 172,
        "kind": "check_result",
        "stepKey": "notification_received",
        "check": {
          "verdict": "failed",
          "summary": "The matching receipt arrived 15 seconds after the allowed deadline.",
          "expected": "Probe receipt within 60 s of the transition",
          "actual": "75 s",
          "reasonCode": "NO_WITNESS_IN_COVERED_WINDOW",
          "evidenceIds": [
            "ev_alarm-late_07",
            "ev_alarm-late_08"
          ],
          "evaluatedThrough": "2026-11-05T08:02:52Z",
          "collection": "complete",
          "coverage": "sufficient",
          "proof": "witness",
          "window": {
            "start": "2026-11-05T08:01:16Z",
            "end": "2026-11-05T08:02:16Z"
          },
          "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 172,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_10",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "notification_received",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The matching receipt arrived 15 seconds after the allowed deadline.",
          "occurredAt": "2026-11-05T08:02:52Z",
          "observedAt": "2026-11-05T08:02:52Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/notification_received/10",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "failed",
            "summary": "The matching receipt arrived 15 seconds after the allowed deadline.",
            "expected": "Probe receipt within 60 s of the transition",
            "actual": "75 s",
            "reasonCode": "NO_WITNESS_IN_COVERED_WINDOW",
            "evidenceIds": [
              "ev_alarm-late_07",
              "ev_alarm-late_08"
            ],
            "evaluatedThrough": "2026-11-05T08:02:52Z",
            "collection": "complete",
            "coverage": "sufficient",
            "proof": "witness",
            "window": {
              "start": "2026-11-05T08:01:16Z",
              "end": "2026-11-05T08:02:16Z"
            },
            "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T08:01:16Z",
            "end": "2026-11-05T08:02:16Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:cec2443b9276f275a48cb1782947cc637a07b451c52ff7d0a703a3cf653291ec"
        }
      },
      {
        "at": 172,
        "kind": "step_finish",
        "stepKey": "notification_received",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "failed",
            "reasonCode": "NO_WITNESS_IN_COVERED_WINDOW",
            "evidenceIds": [
              "ev_alarm-late_07",
              "ev_alarm-late_08"
            ],
            "evaluatedThrough": "2026-11-05T08:02:52Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 173,
        "kind": "run_phase",
        "phase": "finalizing",
        "reason": "Main checks settled. Required cleanup is still running.",
        "termination": null
      },
      {
        "at": 173,
        "kind": "step_start",
        "stepKey": "stop_injection",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:stop_injection:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_payments_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "step": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject"
          }
        },
        "resolvedInputsDigest": "sha256:72865567394d7be76146a3652b2c76ab76cb026a8fac4e86c895b75aff2a981f",
        "checkpoint": null
      },
      {
        "at": 174,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP8ddbf3cc5ca77fdfb",
          "disposition": "active",
          "providerState": "stopping",
          "localState": null,
          "observedAt": "2026-11-05T08:02:54Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "A stop request was accepted; cessation has not yet been confirmed.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "stopping",
              "startTime": "2026-11-05T08:00:11Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "cancelled"
            }
          ]
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "provider"
      },
      {
        "at": 200,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_11",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "stop_injection",
          "source": "AWS FIS",
          "sourceKind": "provider",
          "kind": "provider-execution",
          "title": "External experiment is terminal",
          "summary": "A provider observation confirms stopped. This establishes cleanup of the tracked experiment, not workload recovery.",
          "occurredAt": "2026-11-05T08:03:18Z",
          "observedAt": "2026-11-05T08:03:20Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/stop_injection/11",
          "schemaRef": "sha256:c0c3c85379702f81d2d9b5a14ef3c6ecbe5a452faf3c9c0745c228c3e18bbd7e",
          "value": {
            "experimentId": "EXP8ddbf3cc5ca77fdfb",
            "state": "stopped",
            "endTime": "2026-11-05T08:03:18Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:0284b057de42e6b93bb3f9c3fc74059c20cbd97eebbe30ffa421ddad9218a749"
        }
      },
      {
        "at": 200,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": "EXP8ddbf3cc5ca77fdfb",
          "disposition": "terminal",
          "providerState": "stopped",
          "localState": null,
          "observedAt": "2026-11-05T08:03:20Z",
          "observationKind": "provider",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "The original external experiment is confirmed terminal.",
          "actions": [
            {
              "name": "isolateZone",
              "actionId": "aws:network:disrupt-connectivity",
              "status": "stopped",
              "startTime": "2026-11-05T08:00:11Z",
              "endTime": "2026-11-05T08:03:18Z"
            },
            {
              "name": "recoveryWait",
              "actionId": "aws:fis:wait",
              "status": "cancelled"
            }
          ]
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "provider"
      },
      {
        "at": 200,
        "kind": "step_finish",
        "stepKey": "stop_injection",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_alarm_late_20261105:inject:1:effect",
          "evidenceIds": [
            "ev_alarm-late_11"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 201,
        "kind": "step_start",
        "stepKey": "close_capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_alarm_late_20261105:close_capture:1",
        "resolvedInputs": {
          "step": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "capture"
          }
        },
        "resolvedInputsDigest": "sha256:f4ada52ec7bc0d960ed0c0ef3e2953ae228146eb37dec15bfcaff94050c3c0a3",
        "checkpoint": null
      },
      {
        "at": 202,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_12",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "close_capture",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Receiver capture closed",
          "summary": "Capture closed after experiment reconciliation settled; retained messages and their receipt times remain inspectable.",
          "occurredAt": "2026-11-05T08:03:22Z",
          "observedAt": "2026-11-05T08:03:22Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/close_capture/12",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_8ddbf3cc5c",
            "state": "closed",
            "lastCursor": "alarm-late/receipt/1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_payments_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:e2c3e226a4ba75c712358859ac391fd9f0b0f8802e0c98dd7d51e97ca8852e40"
        }
      },
      {
        "at": 202,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_alarm_late_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_alarm_late_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_8ddbf3cc5c",
          "disposition": "terminal",
          "providerState": null,
          "localState": "closed",
          "observedAt": "2026-11-05T08:03:22Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "The local probe session is closed.",
          "actions": []
        },
        "observedByStepKey": "close_capture",
        "sourceKind": "runtime"
      },
      {
        "at": 202,
        "kind": "step_finish",
        "stepKey": "close_capture",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_alarm_late_20261105:capture:1:effect",
          "evidenceIds": [
            "ev_alarm-late_12"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 203,
        "kind": "run_phase",
        "phase": "finished",
        "reason": "All required workflow operations and cleanup settled.",
        "termination": null
      },
      {
        "at": 230,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_alarm-late_13",
          "runId": "run_demo_alarm_late_20261105",
          "stepKey": "stop_injection",
          "source": "FIS report",
          "sourceKind": "provider",
          "kind": "artifact",
          "title": "Provider report reference available",
          "summary": "An independently generated FIS report is retained as an artifact reference. It does not change the sealed assessment.",
          "occurredAt": "2026-11-05T08:03:50Z",
          "observedAt": "2026-11-05T08:03:50Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/alarm-late/stop_injection/13",
          "schemaRef": "sha256:10c5a18eeec568b1687d444f7b622e284d03d6148794484f04f8f6ce2ab20758",
          "value": {
            "artifact": {
              "store": "s3",
              "arn": "arn:aws:s3:::synthetic-assessment-reports/alarm-late/experiment-report.pdf",
              "mediaType": "application/pdf",
              "synthetic": true
            },
            "reportState": "completed"
          },
          "scope": {
            "experimentId": "EXP8ddbf3cc5ca77fdfb",
            "accountId": "444455556666",
            "region": "eu-central-1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:accd90584b1d20990683413d9705d08ca76b08380bb98d1c5a605c8f7a4e01fc"
        }
      }
    ]
  },
  {
    "key": "start-ambiguous",
    "runId": "run_demo_start_ambiguous_20261105",
    "title": "Inventory · alarm notification",
    "description": "Assess the declared scope with explicit evidence and independent execution, criterion and cleanup outcomes.",
    "service": "Inventory",
    "environment": "Production EU",
    "region": "eu-central-1",
    "accounts": [
      "444455556666"
    ],
    "owner": "Platform Resilience",
    "createdAt": "2026-11-05T09:30:00Z",
    "initialCursorSeconds": 230,
    "durationSeconds": 280,
    "synthetic": true,
    "revisionKey": "alarm",
    "scenario": {
      "scenarioId": "scn_application_alarm_delivery",
      "displayName": "Alarm-to-receiver assessment"
    },
    "admission": {
      "admittedAt": "2026-11-05T09:30:00Z",
      "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
      "inputsDigest": "sha256:e095742122a8a0aab3db092d4864353d96943b5f521ae404a8183fd2a7b4ea55",
      "subject": {
        "deploymentRef": "deployment_inventory_prod_euc1",
        "expectedDeploymentRevision": "release_2026_11_05.3",
        "service": "Inventory",
        "environment": "production",
        "accountIds": [
          "444455556666"
        ],
        "region": "eu-central-1"
      },
      "inputs": {
        "templateId": "EXTd9f9f0988d7f69aee",
        "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
        "topicArn": "arn:aws:sns:eu-central-1:444455556666:inventory-alerts",
        "receiverId": "inventory-alarm-probe"
      },
      "bindings": {
        "aws": {
          "connectionId": "connection_inventory_assessment",
          "capabilities": [
            "aws_assessment_scope"
          ]
        },
        "receiver": {
          "connectionId": "connection_inventory_dedicated_probe",
          "capabilities": [
            "dedicated_notification_receiver"
          ]
        }
      },
      "requiredCriteria": [
        "alarm_transition",
        "notification_received"
      ],
      "policies": {
        "timeoutSeconds": 600,
        "finalizationTimeoutSeconds": 180,
        "concurrency": "queue_per_deployment"
      },
      "bindingObservedAt": "2026-11-05T09:30:00Z"
    },
    "_events": [
      {
        "at": 0,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_01",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "admission",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "admission",
          "title": "Revision and deployment bound",
          "summary": "The exact published revision, input values and trusted connection references were fixed before dispatch.",
          "occurredAt": "2026-11-05T09:30:00Z",
          "observedAt": "2026-11-05T09:30:00Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/start-ambiguous/admission/1",
          "schemaRef": "sha256:a9a9546dd44dfa0d6a0940f9829b98d45ffba2c3a6c511adb4b6da8ddc1e54d3",
          "value": {
            "scenarioRevisionId": "scnrev_alarm_delivery_002",
            "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
            "requiredCriteria": [
              "alarm_transition",
              "notification_received"
            ]
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f4083e81379f421b5790829832e61c7c3989f68ba341e34b5a975e2b53118b8f"
        }
      },
      {
        "at": 1,
        "kind": "run_phase",
        "phase": "running",
        "reason": "Main workflow admitted with a fixed criterion denominator.",
        "termination": null
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:capture:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_inventory_dedicated_probe",
            "capabilities": [
              "dedicated_notification_receiver"
            ]
          },
          "receiverId": "inventory-alarm-probe",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:inventory-alerts",
          "leaseSeconds": 900
        },
        "resolvedInputsDigest": "sha256:c9a094836a8ddab03a744b6ec5ca81dc9ff7e1613eca36b683b821e8760b06fa",
        "checkpoint": null
      },
      {
        "at": 2,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_start_ambiguous_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "opening",
          "observedAt": "2026-11-05T09:30:02Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A local capture intent exists; readiness is not yet established.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "baseline",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:baseline:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_inventory_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability"
        },
        "resolvedInputsDigest": "sha256:6844ee35cd6b004395d97360a7c8d97a4790e7b99ecec1991e164a81d7263b3b",
        "checkpoint": null
      },
      {
        "at": 5,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_02",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "baseline",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "observation",
          "title": "Alarm baseline observed",
          "summary": "The alarm is OK at the starting observation.",
          "occurredAt": "2026-11-05T09:30:04Z",
          "observedAt": "2026-11-05T09:30:05Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/start-ambiguous/baseline/2",
          "schemaRef": "sha256:3a57c20e4754fe8b5157afec9259195d1cb99d9074b946f6b2aa2c8a6b3c53d9",
          "value": {
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
            "state": "OK",
            "stateUpdatedAt": "2026-11-05T09:28:00Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:ee2f41db2feeedbc8fdab457ea9da5656da524c5466c3b077d2d8e282462de7e"
        }
      },
      {
        "at": 5,
        "kind": "step_finish",
        "stepKey": "baseline",
        "outcome": "succeeded",
        "outputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_start-ambiguous_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T09:30:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 6,
        "kind": "step_start",
        "stepKey": "baseline_ok",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:baseline_ok:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
              "state": "OK"
            },
            "evidenceIds": [
              "ev_start-ambiguous_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T09:30:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
              "authenticated": true
            }
          },
          "proof": "complete",
          "expect": "value.state == \"OK\""
        },
        "resolvedInputsDigest": "sha256:d8360b6f425ffe65ab105845bc02478b22dfc43a3b174c4bad7b4bbba9f95f31",
        "checkpoint": null
      },
      {
        "at": 7,
        "kind": "check_result",
        "stepKey": "baseline_ok",
        "check": {
          "verdict": "passed",
          "summary": "The mutation precondition is satisfied.",
          "expected": "Alarm state is OK",
          "actual": "OK",
          "reasonCode": "PREDICATE_TRUE",
          "evidenceIds": [
            "ev_start-ambiguous_02"
          ],
          "evaluatedThrough": "2026-11-05T09:30:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "proof": "complete",
          "window": null,
          "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 7,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_03",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "baseline_ok",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The mutation precondition is satisfied.",
          "occurredAt": "2026-11-05T09:30:07Z",
          "observedAt": "2026-11-05T09:30:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/start-ambiguous/baseline_ok/3",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "passed",
            "summary": "The mutation precondition is satisfied.",
            "expected": "Alarm state is OK",
            "actual": "OK",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_start-ambiguous_02"
            ],
            "evaluatedThrough": "2026-11-05T09:30:07Z",
            "collection": "complete",
            "coverage": "sufficient",
            "proof": "complete",
            "window": null,
            "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:9f8c1f49f60e62ac6e9b2a09267834badc944b756b6080663b7855d13c9b084d"
        }
      },
      {
        "at": 7,
        "kind": "step_finish",
        "stepKey": "baseline_ok",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "passed",
            "reasonCode": "PREDICATE_TRUE",
            "evidenceIds": [
              "ev_start-ambiguous_02"
            ],
            "evaluatedThrough": "2026-11-05T09:30:07Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 8,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_04",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "capture",
          "source": "Receiver capture",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Dedicated receiver capture ready",
          "summary": "The probe session is active before injection. This proves readiness of the bound probe, not a production subscriber.",
          "occurredAt": "2026-11-05T09:30:08Z",
          "observedAt": "2026-11-05T09:30:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/start-ambiguous/capture/4",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_8808b07d3c",
            "receiverId": "inventory-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:inventory-alerts",
            "queueArn": "arn:aws:sqs:eu-central-1:444455556666:inventory-assessment-probe",
            "readyAt": "2026-11-05T09:30:08Z",
            "leaseExpiresAt": "2026-11-05T09:45:02Z",
            "coveragePolicy": "dedicated-receiver/v1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:80fd6915a7a32c62e66d534a41181cbfeb5cfcc2dc217f1e3679b99dd819c091"
        }
      },
      {
        "at": 8,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_start_ambiguous_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_8808b07d3c",
          "disposition": "active",
          "providerState": null,
          "localState": "ready",
          "observedAt": "2026-11-05T09:30:08Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A dedicated probe is collecting only its own subscription.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 8,
        "kind": "step_finish",
        "stepKey": "capture",
        "outcome": "succeeded",
        "outputs": {
          "capture": {
            "captureId": "capture_8808b07d3c",
            "readyAt": "2026-11-05T09:30:08Z",
            "leaseExpiresAt": "2026-11-05T09:45:02Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 10,
        "kind": "step_start",
        "stepKey": "inject",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:inject:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_inventory_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "templateId": "EXTd9f9f0988d7f69aee"
        },
        "resolvedInputsDigest": "sha256:11677c5f5998fe1e1cf5e29a4d41eef600eee5f9a2d06c416cc551a10b345181",
        "checkpoint": {
          "providerClientToken": "dispatch_start-ambiguous_inject_1"
        }
      },
      {
        "at": 10,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_start_ambiguous_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "awaiting_response",
          "observedAt": "2026-11-05T09:30:10Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "Dispatch intent is durable. No provider identity has been observed yet.",
          "actions": []
        },
        "observedByStepKey": "inject",
        "sourceKind": "runtime"
      },
      {
        "at": 20,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_05",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "inject",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "execution-error",
          "title": "Start response was lost",
          "summary": "Dispatch was persisted, but the response did not establish a provider identity. A new Start call could create work and is forbidden after cancellation.",
          "occurredAt": "2026-11-05T09:30:20Z",
          "observedAt": "2026-11-05T09:30:20Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/start-ambiguous/inject/5",
          "schemaRef": "sha256:9ec3510442048e4e90b18b3c8cc7a46abcc212a2d541aeb687c647639ea0dce0",
          "value": {
            "code": "START_OUTCOME_UNKNOWN",
            "providerIdentityKnown": false,
            "dispatchKey": "run_demo_start_ambiguous_20261105:inject:1",
            "retryCreatesNewIntent": false
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:e4504aaf4894ef5f5125e7439d999dca64d60a22c927560338020cb977383d36"
        }
      },
      {
        "at": 20,
        "kind": "step_finish",
        "stepKey": "inject",
        "outcome": "failed",
        "outputs": {},
        "error": {
          "code": "START_OUTCOME_UNKNOWN",
          "category": "transport",
          "message": "The provider outcome is unknown; no safe creating retry is allowed.",
          "retryable": false
        },
        "reason": null
      },
      {
        "at": 21,
        "kind": "step_start",
        "stepKey": "collect",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:collect:1",
        "resolvedInputs": {
          "captureStep": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "capture"
          },
          "injectionStep": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "inject"
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:inventory-availability",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:inventory-alerts",
          "receiverId": "inventory-alarm-probe",
          "transitionWindowSeconds": 180,
          "receiptDeadlineSeconds": 60,
          "collectionGraceSeconds": 30
        },
        "resolvedInputsDigest": "sha256:47e2f767d22668df9e48dbedba6b8d8599411800cf9b58bc74933f95056ca433",
        "checkpoint": null
      },
      {
        "at": 22,
        "kind": "cancellation",
        "intent": {
          "commandId": "cmd_start-ambiguous_cancel",
          "clientToken": "cancel_start-ambiguous_intent",
          "reason": "Stop after the uncertain provider response.",
          "acceptedAt": "2026-11-05T09:30:22Z",
          "principal": "synthetic/operator",
          "source": "recorded mock trace",
          "receipt": {
            "accepted": true,
            "httpStatus": 202,
            "acceptedAt": "2026-11-05T09:30:22Z",
            "commandId": "cmd_start-ambiguous_cancel",
            "runId": "run_demo_start_ambiguous_20261105"
          }
        }
      },
      {
        "at": 22,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_06",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "inject",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "control",
          "title": "Cancellation accepted",
          "summary": "New main-step dispatch is fenced. Accepted cancellation does not establish that the FIS experiment stopped.",
          "occurredAt": "2026-11-05T09:30:22Z",
          "observedAt": "2026-11-05T09:30:22Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/start-ambiguous/inject/6",
          "schemaRef": "sha256:092d3ae28eea3c47f1f38e13b52db2e600693979483e1e57b6a8df5230314b45",
          "value": {
            "accepted": true,
            "reason": "Uncertain provider start response"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:33502664e81abc5f11bfaffc35c0ab670ab5a5fd67e798d6063f6d3974080119"
        }
      },
      {
        "at": 22,
        "kind": "step_skip",
        "stepKey": "alarm_transition",
        "reasonCode": "RUN_CANCELLED"
      },
      {
        "at": 22,
        "kind": "step_skip",
        "stepKey": "notification_received",
        "reasonCode": "RUN_CANCELLED"
      },
      {
        "at": 23,
        "kind": "step_finish",
        "stepKey": "collect",
        "outcome": "cancelled",
        "outputs": {},
        "error": null,
        "reason": "Cancellation interrupted observation before a provider execution boundary was established."
      },
      {
        "at": 24,
        "kind": "run_phase",
        "phase": "finalizing",
        "reason": "Cancellation was accepted; the external effect still needs non-creating reconciliation.",
        "termination": null
      },
      {
        "at": 25,
        "kind": "step_start",
        "stepKey": "stop_injection",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:stop_injection:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_inventory_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "step": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "inject"
          }
        },
        "resolvedInputsDigest": "sha256:c9ba99a0068b50f919159f93da2ff44e5c087ce21a05aaece3cabdce31437f3b",
        "checkpoint": {
          "originEffectKey": "run_demo_start_ambiguous_20261105:inject:1:effect",
          "nativeId": null,
          "strategy": "non-creating-reconciliation"
        }
      },
      {
        "at": 110,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_start-ambiguous_07",
          "runId": "run_demo_start_ambiguous_20261105",
          "stepKey": "stop_injection",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "reconciliation",
          "title": "External outcome remains unknown",
          "summary": "The retained intent cannot be safely resolved to a provider identity. No replacement experiment was created. The deployment hold remains.",
          "occurredAt": "2026-11-05T09:31:50Z",
          "observedAt": "2026-11-05T09:31:50Z",
          "collection": "unavailable",
          "coverage": "unknown",
          "sourceRecordId": "demo/start-ambiguous/stop_injection/7",
          "schemaRef": "sha256:42de469c495ace93ae4ff79102428f61cd503018bce7548789380010ac0daf7b",
          "value": {
            "originEffectKey": "run_demo_start_ambiguous_20261105:inject:1:effect",
            "nativeId": null,
            "remoteDisposition": "unknown",
            "scopeHold": "retained"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:671ddc4867af4b685a308c5011743cb9d188be73fbf840010b94fbd46bd381d7"
        }
      },
      {
        "at": 110,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_start_ambiguous_20261105:inject:1:effect",
          "originAttempt": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "inject",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "inject",
          "provider": "aws/fis",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "unconfirmed",
          "observedAt": "2026-11-05T09:31:50Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": true,
          "requiresFinalization": true,
          "detail": "Neither remote creation nor cessation can be established from the retained evidence.",
          "actions": []
        },
        "observedByStepKey": "stop_injection",
        "sourceKind": "runtime"
      },
      {
        "at": 110,
        "kind": "step_finish",
        "stepKey": "stop_injection",
        "outcome": "failed",
        "outputs": {
          "remoteDisposition": "unknown",
          "originEffectKey": "run_demo_start_ambiguous_20261105:inject:1:effect",
          "evidenceIds": [
            "ev_start-ambiguous_07"
          ]
        },
        "error": {
          "code": "EXTERNAL_STATE_UNCONFIRMED",
          "category": "reconciliation",
          "message": "The original effect remains unresolved. Keep the protective deployment hold.",
          "retryable": false
        },
        "reason": null
      },
      {
        "at": 111,
        "kind": "step_start",
        "stepKey": "close_capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_start_ambiguous_20261105:close_capture:1",
        "resolvedInputs": {
          "step": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "capture"
          }
        },
        "resolvedInputsDigest": "sha256:8884dfbfe01f4afee0ef026bbbb1439ecad563232172ac935917d23ac057ac01",
        "checkpoint": null
      },
      {
        "at": 113,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_start_ambiguous_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_start_ambiguous_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_8808b07d3c",
          "disposition": "terminal",
          "providerState": null,
          "localState": "closed",
          "observedAt": "2026-11-05T09:31:53Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "Capture closed after failed stop reconciliation settled.",
          "actions": []
        },
        "observedByStepKey": "close_capture",
        "sourceKind": "runtime"
      },
      {
        "at": 113,
        "kind": "step_finish",
        "stepKey": "close_capture",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_start_ambiguous_20261105:capture:1:effect",
          "evidenceIds": []
        },
        "error": null,
        "reason": null
      },
      {
        "at": 115,
        "kind": "run_phase",
        "phase": "finished",
        "reason": "Local orchestration finished; the remote effect remains unresolved.",
        "termination": null
      }
    ]
  },
  {
    "key": "logs-inconclusive",
    "runId": "run_demo_logs_inconclusive_20261105",
    "title": "Inventory · logged error budget",
    "description": "Assess the declared scope with explicit evidence and independent execution, criterion and cleanup outcomes.",
    "service": "Inventory",
    "environment": "Production EU",
    "region": "eu-central-1",
    "accounts": [
      "777788889999"
    ],
    "owner": "Platform Resilience",
    "createdAt": "2026-11-05T10:20:00Z",
    "initialCursorSeconds": 100,
    "durationSeconds": 150,
    "synthetic": true,
    "revisionKey": "logs",
    "scenario": {
      "scenarioId": "scn_application_log_budget",
      "displayName": "Application logged error budget"
    },
    "admission": {
      "admittedAt": "2026-11-05T10:20:00Z",
      "revisionDigest": "sha256:ce0f0a5721384a2c242f283d7e19c6e8ee14be75b54e51c246018f56d4709211",
      "inputsDigest": "sha256:af1ceb90a7801297eb42d7ce0adb64dc03d68652a28e6a38795f615c7bdb467b",
      "subject": {
        "deploymentRef": "deployment_inventory_prod_euc1",
        "expectedDeploymentRevision": "release_2026_11_05.3",
        "service": "Inventory",
        "environment": "production",
        "accountIds": [
          "777788889999"
        ],
        "region": "eu-central-1"
      },
      "inputs": {
        "logGroups": [
          "/aws/ecs/inventory/api"
        ],
        "windowStart": "2026-11-05T09:50:00Z",
        "windowEnd": "2026-11-05T10:00:00Z",
        "maximumErrors": 5
      },
      "bindings": {
        "aws": {
          "connectionId": "connection_inventory_assessment",
          "capabilities": [
            "cloudwatch_logs_query_scope"
          ]
        }
      },
      "requiredCriteria": [
        "error_budget"
      ],
      "policies": {
        "timeoutSeconds": 300,
        "finalizationTimeoutSeconds": 60,
        "concurrency": "queue_per_deployment"
      },
      "bindingObservedAt": "2026-11-05T10:20:00Z"
    },
    "_events": [
      {
        "at": 0,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_logs-inconclusive_01",
          "runId": "run_demo_logs_inconclusive_20261105",
          "stepKey": "admission",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "admission",
          "title": "Revision and deployment bound",
          "summary": "The exact published revision, input values and trusted connection references were fixed before dispatch.",
          "occurredAt": "2026-11-05T10:20:00Z",
          "observedAt": "2026-11-05T10:20:00Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/logs-inconclusive/admission/1",
          "schemaRef": "sha256:a9a9546dd44dfa0d6a0940f9829b98d45ffba2c3a6c511adb4b6da8ddc1e54d3",
          "value": {
            "scenarioRevisionId": "scnrev_logs_budget_003",
            "revisionDigest": "sha256:ce0f0a5721384a2c242f283d7e19c6e8ee14be75b54e51c246018f56d4709211",
            "requiredCriteria": [
              "error_budget"
            ]
          },
          "scope": {
            "accountId": "777788889999",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:eebeb3ff79502a2e2fa0e0165e39ba526b1d091f0166ef68445a714dd93634b8"
        }
      },
      {
        "at": 1,
        "kind": "run_phase",
        "phase": "running",
        "reason": "Main workflow admitted with a fixed criterion denominator.",
        "termination": null
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "query_errors",
        "attemptNo": 1,
        "dispatchKey": "run_demo_logs_inconclusive_20261105:query_errors:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_inventory_assessment",
            "capabilities": [
              "cloudwatch_logs_query_scope"
            ]
          },
          "logGroups": [
            "/aws/ecs/inventory/api"
          ],
          "windowStart": "2026-11-05T09:50:00Z",
          "windowEnd": "2026-11-05T10:00:00Z",
          "language": "CWLI",
          "resultShape": "single_numeric_count",
          "query": "fields @timestamp, level\n| filter level = \"ERROR\"\n| stats count(*) as count\n"
        },
        "resolvedInputsDigest": "sha256:4f0fdf6ba8fab0739fe3ddb0ae1f9df4df0df2ac9e858ffa030b9fdd53c4b345",
        "checkpoint": null
      },
      {
        "at": 2,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_logs_inconclusive_20261105:query_errors:1:effect",
          "originAttempt": {
            "runId": "run_demo_logs_inconclusive_20261105",
            "stepKey": "query_errors",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "query_errors",
          "provider": "aws/cloudwatch.logs",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "starting",
          "observedAt": "2026-11-05T10:20:02Z",
          "observationKind": "local",
          "accountId": "777788889999",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "Query dispatch is persisted; no response has been observed yet.",
          "actions": []
        },
        "observedByStepKey": "query_errors",
        "sourceKind": "runtime"
      },
      {
        "at": 4,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_logs_inconclusive_20261105:query_errors:1:effect",
          "originAttempt": {
            "runId": "run_demo_logs_inconclusive_20261105",
            "stepKey": "query_errors",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "query_errors",
          "provider": "aws/cloudwatch.logs",
          "nativeId": "b125a640-demo-4d17-9000-logsquery0001",
          "disposition": "active",
          "providerState": "Scheduled",
          "localState": null,
          "observedAt": "2026-11-05T10:20:04Z",
          "observationKind": "provider",
          "accountId": "777788889999",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "The provider query is scheduled. No final result is available.",
          "actions": []
        },
        "observedByStepKey": "query_errors",
        "sourceKind": "provider"
      },
      {
        "at": 30,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_logs-inconclusive_02",
          "runId": "run_demo_logs_inconclusive_20261105",
          "stepKey": "query_errors",
          "source": "CloudWatch Logs Insights",
          "sourceKind": "provider",
          "kind": "query-progress",
          "title": "Query still running",
          "summary": "A running GetQueryResults response is partial; its empty current rows are not a final zero count.",
          "occurredAt": "2026-11-05T10:20:30Z",
          "observedAt": "2026-11-05T10:20:30Z",
          "collection": "partial",
          "coverage": "unknown",
          "sourceRecordId": "demo/logs-inconclusive/query_errors/2",
          "schemaRef": "sha256:f987aa862c0cf375f735a6d5f7b786fe5ba0b756187175443ff2aaa14a060988",
          "value": {
            "queryId": "b125a640-demo-4d17-9000-logsquery0001",
            "status": "Running",
            "rows": []
          },
          "scope": {
            "accountId": "777788889999",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:87385e7eb32412309b3a84d6e9f108dc09e426192b04f13872bada4630dd1d40"
        }
      },
      {
        "at": 52,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_logs-inconclusive_03",
          "runId": "run_demo_logs_inconclusive_20261105",
          "stepKey": "query_errors",
          "source": "CloudWatch Logs Insights",
          "sourceKind": "provider",
          "kind": "query-result",
          "title": "Query complete; pages exhausted",
          "summary": "The typed result returned zero recorded errors. This establishes the query result, not complete application logging coverage.",
          "occurredAt": "2026-11-05T10:20:52Z",
          "observedAt": "2026-11-05T10:20:52Z",
          "collection": "complete",
          "coverage": "unknown",
          "sourceRecordId": "demo/logs-inconclusive/query_errors/3",
          "schemaRef": "sha256:0ba1e5e3ea7949db11199c9cc0855d582b0e463d5b0093500f5f001d07662c56",
          "value": {
            "queryId": "b125a640-demo-4d17-9000-logsquery0001",
            "status": "Complete",
            "language": "CWLI",
            "rows": [
              {
                "count": 0
              }
            ],
            "pagesCollected": 1,
            "nextToken": null,
            "statistics": {
              "recordsScanned": 28416,
              "bytesScanned": 9021440
            },
            "query": "fields @timestamp, level\n| filter level = \"ERROR\"\n| stats count(*) as count\n"
          },
          "scope": {
            "accountId": "777788889999",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T09:50:00Z",
            "end": "2026-11-05T10:00:00Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:7edbd91fd94c6a28eb342b5946ec164fec3c43dac3355474963e829f6abad123"
        }
      },
      {
        "at": 54,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_logs-inconclusive_04",
          "runId": "run_demo_logs_inconclusive_20261105",
          "stepKey": "query_errors",
          "source": "Log pipeline observation",
          "sourceKind": "provider",
          "kind": "coverage",
          "title": "Source coverage is incomplete",
          "summary": "The logging collector has a 125-second delivery gap inside the assessed window. No generic query completion watermark repairs that gap.",
          "occurredAt": "2026-11-05T10:20:54Z",
          "observedAt": "2026-11-05T10:20:54Z",
          "collection": "complete",
          "coverage": "unknown",
          "sourceRecordId": "demo/logs-inconclusive/query_errors/4",
          "schemaRef": "sha256:310342ec84374fe6486c2309ce00e95f3a25f5454ca4be4f24332aec59330247",
          "value": {
            "logGroup": "/aws/ecs/inventory/api",
            "gapStart": "2026-11-05T09:54:00Z",
            "gapEnd": "2026-11-05T09:56:05Z",
            "gapSeconds": 125,
            "coveragePolicy": "application-logging/v2",
            "state": "unknown"
          },
          "scope": {
            "accountId": "777788889999",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:53f929e9cdca114edcccd1d5e5133e406d06be9173ac22661891fd8679072146"
        }
      },
      {
        "at": 54,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_logs_inconclusive_20261105:query_errors:1:effect",
          "originAttempt": {
            "runId": "run_demo_logs_inconclusive_20261105",
            "stepKey": "query_errors",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "query_errors",
          "provider": "aws/cloudwatch.logs",
          "nativeId": "b125a640-demo-4d17-9000-logsquery0001",
          "disposition": "terminal",
          "providerState": "Complete",
          "localState": null,
          "observedAt": "2026-11-05T10:20:54Z",
          "observationKind": "provider",
          "accountId": "777788889999",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "The query is complete; source coverage remains a separate fact.",
          "actions": []
        },
        "observedByStepKey": "query_errors",
        "sourceKind": "provider"
      },
      {
        "at": 55,
        "kind": "step_finish",
        "stepKey": "query_errors",
        "outcome": "succeeded",
        "outputs": {
          "observation": {
            "value": {
              "count": 0
            },
            "evidenceIds": [
              "ev_logs-inconclusive_03",
              "ev_logs-inconclusive_04"
            ],
            "collection": "complete",
            "coverage": "unknown",
            "windowClosed": true,
            "observedAt": "2026-11-05T10:20:55Z",
            "scope": "/aws/ecs/inventory/api",
            "window": {
              "start": "2026-11-05T09:50:00Z",
              "end": "2026-11-05T10:00:00Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.logs",
              "identity": "/aws/ecs/inventory/api",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 56,
        "kind": "step_start",
        "stepKey": "error_budget",
        "attemptNo": 1,
        "dispatchKey": "run_demo_logs_inconclusive_20261105:error_budget:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "count": 0
            },
            "evidenceIds": [
              "ev_logs-inconclusive_03",
              "ev_logs-inconclusive_04"
            ],
            "collection": "complete",
            "coverage": "unknown",
            "windowClosed": true,
            "observedAt": "2026-11-05T10:20:55Z",
            "scope": "/aws/ecs/inventory/api",
            "window": {
              "start": "2026-11-05T09:50:00Z",
              "end": "2026-11-05T10:00:00Z"
            },
            "source": {
              "namespace": "aws/cloudwatch.logs",
              "identity": "/aws/ecs/inventory/api",
              "authenticated": true
            }
          },
          "proof": "complete",
          "expect": "value.count <= inputs.maximumErrors"
        },
        "resolvedInputsDigest": "sha256:5fcaed82d301f8b1f48cfea64ff1a3c433de5cc3b32b7a4bf669509452adb285",
        "checkpoint": null
      },
      {
        "at": 57,
        "kind": "check_result",
        "stepKey": "error_budget",
        "check": {
          "verdict": "inconclusive",
          "summary": "Zero errors were returned, but the logging gap prevents a conclusive budget assessment.",
          "expected": "At most 5 recorded errors; sufficient source coverage",
          "actual": "0 returned · coverage unknown",
          "reasonCode": "INSUFFICIENT_EVIDENCE",
          "evidenceIds": [
            "ev_logs-inconclusive_03",
            "ev_logs-inconclusive_04"
          ],
          "evaluatedThrough": "2026-11-05T10:20:57Z",
          "collection": "complete",
          "coverage": "unknown",
          "proof": "complete",
          "window": {
            "start": "2026-11-05T09:50:00Z",
            "end": "2026-11-05T10:00:00Z"
          },
          "predicateDigest": "sha256:79588d0dbde01f926f6fc4d1d79ca0a7b409ce8e6a29ebaa1d7bed23dcb1e76c",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 57,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_logs-inconclusive_05",
          "runId": "run_demo_logs_inconclusive_20261105",
          "stepKey": "error_budget",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "Zero errors were returned, but the logging gap prevents a conclusive budget assessment.",
          "occurredAt": "2026-11-05T10:20:57Z",
          "observedAt": "2026-11-05T10:20:57Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/logs-inconclusive/error_budget/5",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "inconclusive",
            "summary": "Zero errors were returned, but the logging gap prevents a conclusive budget assessment.",
            "expected": "At most 5 recorded errors; sufficient source coverage",
            "actual": "0 returned · coverage unknown",
            "reasonCode": "INSUFFICIENT_EVIDENCE",
            "evidenceIds": [
              "ev_logs-inconclusive_03",
              "ev_logs-inconclusive_04"
            ],
            "evaluatedThrough": "2026-11-05T10:20:57Z",
            "collection": "complete",
            "coverage": "unknown",
            "proof": "complete",
            "window": {
              "start": "2026-11-05T09:50:00Z",
              "end": "2026-11-05T10:00:00Z"
            },
            "predicateDigest": "sha256:79588d0dbde01f926f6fc4d1d79ca0a7b409ce8e6a29ebaa1d7bed23dcb1e76c",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "777788889999",
            "region": "eu-central-1",
            "deploymentRef": "deployment_inventory_prod_euc1"
          },
          "window": {
            "start": "2026-11-05T09:50:00Z",
            "end": "2026-11-05T10:00:00Z"
          },
          "synthetic": true,
          "contentDigest": "sha256:6dc948a72edf3f69934fb6bff7e459fef6e3dff5c0ee6c7152dd43833423512b"
        }
      },
      {
        "at": 57,
        "kind": "step_finish",
        "stepKey": "error_budget",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "inconclusive",
            "reasonCode": "INSUFFICIENT_EVIDENCE",
            "evidenceIds": [
              "ev_logs-inconclusive_03",
              "ev_logs-inconclusive_04"
            ],
            "evaluatedThrough": "2026-11-05T10:20:57Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 58,
        "kind": "run_phase",
        "phase": "finalizing",
        "reason": "The query is complete; confirm its external lifecycle before sealing.",
        "termination": null
      },
      {
        "at": 59,
        "kind": "step_start",
        "stepKey": "stop_query",
        "attemptNo": 1,
        "dispatchKey": "run_demo_logs_inconclusive_20261105:stop_query:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_inventory_assessment",
            "capabilities": [
              "cloudwatch_logs_query_scope"
            ]
          },
          "step": {
            "runId": "run_demo_logs_inconclusive_20261105",
            "stepKey": "query_errors"
          }
        },
        "resolvedInputsDigest": "sha256:402a53b54fb8e345ea8dc4847bcdaba15e07607d7a12fa073d44f34c1d846f4f",
        "checkpoint": null
      },
      {
        "at": 61,
        "kind": "step_finish",
        "stepKey": "stop_query",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_logs_inconclusive_20261105:query_errors:1:effect",
          "evidenceIds": [
            "ev_logs-inconclusive_03"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 62,
        "kind": "run_phase",
        "phase": "finished",
        "reason": "Execution succeeded; the assessment is inconclusive because source coverage is unknown.",
        "termination": null
      }
    ]
  },
  {
    "key": "baseline-blocked",
    "runId": "run_demo_baseline_blocked_20261105",
    "title": "Fulfillment · alarm notification",
    "description": "Assess the declared scope with explicit evidence and independent execution, criterion and cleanup outcomes.",
    "service": "Fulfillment",
    "environment": "Production EU",
    "region": "eu-central-1",
    "accounts": [
      "444455556666"
    ],
    "owner": "Platform Resilience",
    "createdAt": "2026-11-05T10:40:00Z",
    "initialCursorSeconds": 40,
    "durationSeconds": 70,
    "synthetic": true,
    "revisionKey": "alarm",
    "scenario": {
      "scenarioId": "scn_application_alarm_delivery",
      "displayName": "Alarm-to-receiver assessment"
    },
    "admission": {
      "admittedAt": "2026-11-05T10:40:00Z",
      "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
      "inputsDigest": "sha256:cbfe1545d0a504b1e1f9f73b554de7f3181e8b6edb536f53d126e670ebbd63e8",
      "subject": {
        "deploymentRef": "deployment_fulfillment_prod_euc1",
        "expectedDeploymentRevision": "release_2026_11_05.3",
        "service": "Fulfillment",
        "environment": "production",
        "accountIds": [
          "444455556666"
        ],
        "region": "eu-central-1"
      },
      "inputs": {
        "templateId": "EXT4be90ef5a6994d5b2",
        "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
        "topicArn": "arn:aws:sns:eu-central-1:444455556666:fulfillment-alerts",
        "receiverId": "fulfillment-alarm-probe"
      },
      "bindings": {
        "aws": {
          "connectionId": "connection_fulfillment_assessment",
          "capabilities": [
            "aws_assessment_scope"
          ]
        },
        "receiver": {
          "connectionId": "connection_fulfillment_dedicated_probe",
          "capabilities": [
            "dedicated_notification_receiver"
          ]
        }
      },
      "requiredCriteria": [
        "alarm_transition",
        "notification_received"
      ],
      "policies": {
        "timeoutSeconds": 600,
        "finalizationTimeoutSeconds": 180,
        "concurrency": "queue_per_deployment"
      },
      "bindingObservedAt": "2026-11-05T10:40:00Z"
    },
    "_events": [
      {
        "at": 0,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_01",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "admission",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "admission",
          "title": "Revision and deployment bound",
          "summary": "The exact published revision, input values and trusted connection references were fixed before dispatch.",
          "occurredAt": "2026-11-05T10:40:00Z",
          "observedAt": "2026-11-05T10:40:00Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/admission/1",
          "schemaRef": "sha256:a9a9546dd44dfa0d6a0940f9829b98d45ffba2c3a6c511adb4b6da8ddc1e54d3",
          "value": {
            "scenarioRevisionId": "scnrev_alarm_delivery_002",
            "revisionDigest": "sha256:95ca9ceda54a845b9e7dc2696be47d82b97cd9dabdb9d8f7d7a0a92432d2a5c7",
            "requiredCriteria": [
              "alarm_transition",
              "notification_received"
            ]
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:f4083e81379f421b5790829832e61c7c3989f68ba341e34b5a975e2b53118b8f"
        }
      },
      {
        "at": 1,
        "kind": "run_phase",
        "phase": "running",
        "reason": "Main workflow admitted with a fixed criterion denominator.",
        "termination": null
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:capture:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_fulfillment_dedicated_probe",
            "capabilities": [
              "dedicated_notification_receiver"
            ]
          },
          "receiverId": "fulfillment-alarm-probe",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:fulfillment-alerts",
          "leaseSeconds": 900
        },
        "resolvedInputsDigest": "sha256:6bd716d598e5427d5e91e2b27327eb0c4d71792066fb03fc603c9e5cf042524e",
        "checkpoint": null
      },
      {
        "at": 2,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_baseline_blocked_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": null,
          "disposition": "unknown",
          "providerState": null,
          "localState": "opening",
          "observedAt": "2026-11-05T10:40:02Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A local capture intent exists; readiness is not yet established.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 2,
        "kind": "step_start",
        "stepKey": "baseline",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:baseline:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_fulfillment_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability"
        },
        "resolvedInputsDigest": "sha256:003abe334512bbe5bc06bbd83ea56d9d464a98a93f9e0862da40289a1b29f5c6",
        "checkpoint": null
      },
      {
        "at": 5,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_02",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "baseline",
          "source": "CloudWatch alarms",
          "sourceKind": "provider",
          "kind": "observation",
          "title": "Alarm baseline observed",
          "summary": "The alarm is ALARM at the starting observation.",
          "occurredAt": "2026-11-05T10:40:04Z",
          "observedAt": "2026-11-05T10:40:05Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/baseline/2",
          "schemaRef": "sha256:3a57c20e4754fe8b5157afec9259195d1cb99d9074b946f6b2aa2c8a6b3c53d9",
          "value": {
            "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
            "state": "ALARM",
            "stateUpdatedAt": "2026-11-05T10:38:00Z"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:7f905d4e3c1a804da0908ae9d57a2e5d1cd1f04dd68db16eaabe5d7d8b64dfb1"
        }
      },
      {
        "at": 5,
        "kind": "step_finish",
        "stepKey": "baseline",
        "outcome": "succeeded",
        "outputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
              "state": "ALARM"
            },
            "evidenceIds": [
              "ev_baseline-blocked_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T10:40:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 6,
        "kind": "step_start",
        "stepKey": "baseline_ok",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:baseline_ok:1",
        "resolvedInputs": {
          "observation": {
            "value": {
              "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
              "state": "ALARM"
            },
            "evidenceIds": [
              "ev_baseline-blocked_02"
            ],
            "collection": "complete",
            "coverage": "sufficient",
            "windowClosed": true,
            "observedAt": "2026-11-05T10:40:05Z",
            "scope": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
            "source": {
              "namespace": "aws/cloudwatch.alarm",
              "identity": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
              "authenticated": true
            }
          },
          "proof": "complete",
          "expect": "value.state == \"OK\""
        },
        "resolvedInputsDigest": "sha256:abb09b668eff6266021308bed49e7ca7ca86f5724a2538143f853fb3a5dfa2bf",
        "checkpoint": null
      },
      {
        "at": 7,
        "kind": "check_result",
        "stepKey": "baseline_ok",
        "check": {
          "verdict": "failed",
          "summary": "The alarm is already ALARM; fault injection is blocked.",
          "expected": "Alarm state is OK",
          "actual": "ALARM",
          "reasonCode": "PREDICATE_FALSE",
          "evidenceIds": [
            "ev_baseline-blocked_02"
          ],
          "evaluatedThrough": "2026-11-05T10:40:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "proof": "complete",
          "window": null,
          "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 7,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_03",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "baseline_ok",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "The alarm is already ALARM; fault injection is blocked.",
          "occurredAt": "2026-11-05T10:40:07Z",
          "observedAt": "2026-11-05T10:40:07Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/baseline_ok/3",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "failed",
            "summary": "The alarm is already ALARM; fault injection is blocked.",
            "expected": "Alarm state is OK",
            "actual": "ALARM",
            "reasonCode": "PREDICATE_FALSE",
            "evidenceIds": [
              "ev_baseline-blocked_02"
            ],
            "evaluatedThrough": "2026-11-05T10:40:07Z",
            "collection": "complete",
            "coverage": "sufficient",
            "proof": "complete",
            "window": null,
            "predicateDigest": "sha256:7fdbd37f7de005db7f3214cc8c237b5e91ca66c34ea8fe544ec39f2dfb4ffaf9",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:2ec517304e779f0326d928865902180c181829814e9a7fb50b82d89fb5a2926a"
        }
      },
      {
        "at": 7,
        "kind": "step_finish",
        "stepKey": "baseline_ok",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "failed",
            "reasonCode": "PREDICATE_FALSE",
            "evidenceIds": [
              "ev_baseline-blocked_02"
            ],
            "evaluatedThrough": "2026-11-05T10:40:07Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 8,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_04",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "capture",
          "source": "Receiver capture",
          "sourceKind": "runtime",
          "kind": "capture",
          "title": "Dedicated receiver capture ready",
          "summary": "The probe session is active before injection. This proves readiness of the bound probe, not a production subscriber.",
          "occurredAt": "2026-11-05T10:40:08Z",
          "observedAt": "2026-11-05T10:40:08Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/capture/4",
          "schemaRef": "sha256:fdb03bb64a625f90a4de35e0170856588841f15c180fd8a79d47354f382fecf2",
          "value": {
            "captureId": "capture_fb38303b3e",
            "receiverId": "fulfillment-alarm-probe",
            "topicArn": "arn:aws:sns:eu-central-1:444455556666:fulfillment-alerts",
            "queueArn": "arn:aws:sqs:eu-central-1:444455556666:fulfillment-assessment-probe",
            "readyAt": "2026-11-05T10:40:08Z",
            "leaseExpiresAt": "2026-11-05T10:55:02Z",
            "coveragePolicy": "dedicated-receiver/v1"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:1c0fae8bd0e542441e1bca931a761396541f3f519854ac9e721c840d2f302000"
        }
      },
      {
        "at": 8,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_baseline_blocked_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_fb38303b3e",
          "disposition": "active",
          "providerState": null,
          "localState": "ready",
          "observedAt": "2026-11-05T10:40:08Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "A dedicated probe is collecting only its own subscription.",
          "actions": []
        },
        "observedByStepKey": "capture",
        "sourceKind": "runtime"
      },
      {
        "at": 8,
        "kind": "step_finish",
        "stepKey": "capture",
        "outcome": "succeeded",
        "outputs": {
          "capture": {
            "captureId": "capture_fb38303b3e",
            "readyAt": "2026-11-05T10:40:08Z",
            "leaseExpiresAt": "2026-11-05T10:55:02Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 9,
        "kind": "step_skip",
        "stepKey": "inject",
        "reasonCode": "PRECONDITION_NOT_PASSED"
      },
      {
        "at": 10,
        "kind": "step_start",
        "stepKey": "collect",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:collect:1",
        "resolvedInputs": {
          "captureStep": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "capture"
          },
          "injectionStep": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "inject"
          },
          "alarmArn": "arn:aws:cloudwatch:eu-central-1:444455556666:alarm:fulfillment-availability",
          "topicArn": "arn:aws:sns:eu-central-1:444455556666:fulfillment-alerts",
          "receiverId": "fulfillment-alarm-probe",
          "transitionWindowSeconds": 180,
          "receiptDeadlineSeconds": 60,
          "collectionGraceSeconds": 30
        },
        "resolvedInputsDigest": "sha256:eab3810f332c07ed2f6f5a5c8e7f90fbcca72d713b2e8ee1114f85d6ee397db0",
        "checkpoint": null
      },
      {
        "at": 11,
        "kind": "step_finish",
        "stepKey": "collect",
        "outcome": "succeeded",
        "outputs": {
          "transition": {
            "evidenceIds": [],
            "collection": "unavailable",
            "coverage": "unknown",
            "windowClosed": false,
            "observedAt": "2026-11-05T10:40:11Z",
            "scope": "fulfillment-alarm-probe",
            "reasonCode": "INJECTION_NOT_DISPATCHED",
            "source": {
              "namespace": "events/receiver",
              "identity": "fulfillment-alarm-probe",
              "authenticated": true
            }
          },
          "receipt": {
            "evidenceIds": [],
            "collection": "unavailable",
            "coverage": "unknown",
            "windowClosed": false,
            "observedAt": "2026-11-05T10:40:11Z",
            "scope": "fulfillment-alarm-probe",
            "reasonCode": "INJECTION_NOT_DISPATCHED",
            "source": {
              "namespace": "events/receiver",
              "identity": "fulfillment-alarm-probe",
              "authenticated": true
            }
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 12,
        "kind": "step_start",
        "stepKey": "alarm_transition",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:alarm_transition:1",
        "resolvedInputs": {
          "observation": {
            "evidenceIds": [],
            "collection": "unavailable",
            "coverage": "unknown",
            "windowClosed": false,
            "observedAt": "2026-11-05T10:40:11Z",
            "scope": "fulfillment-alarm-probe",
            "reasonCode": "INJECTION_NOT_DISPATCHED",
            "source": {
              "namespace": "events/receiver",
              "identity": "fulfillment-alarm-probe",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:84bf77e75c238130caa9a4fd828b70e407f61b0c9cf72b3f5108444170e4a994",
        "checkpoint": null
      },
      {
        "at": 12,
        "kind": "step_start",
        "stepKey": "notification_received",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:notification_received:1",
        "resolvedInputs": {
          "observation": {
            "evidenceIds": [],
            "collection": "unavailable",
            "coverage": "unknown",
            "windowClosed": false,
            "observedAt": "2026-11-05T10:40:11Z",
            "scope": "fulfillment-alarm-probe",
            "reasonCode": "INJECTION_NOT_DISPATCHED",
            "source": {
              "namespace": "events/receiver",
              "identity": "fulfillment-alarm-probe",
              "authenticated": true
            }
          },
          "proof": "witness",
          "operator": "exists"
        },
        "resolvedInputsDigest": "sha256:84bf77e75c238130caa9a4fd828b70e407f61b0c9cf72b3f5108444170e4a994",
        "checkpoint": null
      },
      {
        "at": 13,
        "kind": "check_result",
        "stepKey": "alarm_transition",
        "check": {
          "verdict": "inconclusive",
          "summary": "No perturbation was dispatched because the baseline precondition failed.",
          "expected": "ALARM transition within 180 s",
          "actual": null,
          "reasonCode": "PRECONDITION_BLOCKED",
          "evidenceIds": [],
          "evaluatedThrough": "2026-11-05T10:40:13Z",
          "collection": "unavailable",
          "coverage": "unknown",
          "proof": "witness",
          "window": null,
          "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 13,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_05",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "alarm_transition",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "No perturbation was dispatched because the baseline precondition failed.",
          "occurredAt": "2026-11-05T10:40:13Z",
          "observedAt": "2026-11-05T10:40:13Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/alarm_transition/5",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "inconclusive",
            "summary": "No perturbation was dispatched because the baseline precondition failed.",
            "expected": "ALARM transition within 180 s",
            "actual": null,
            "reasonCode": "PRECONDITION_BLOCKED",
            "evidenceIds": [],
            "evaluatedThrough": "2026-11-05T10:40:13Z",
            "collection": "unavailable",
            "coverage": "unknown",
            "proof": "witness",
            "window": null,
            "predicateDigest": "sha256:fd35a23d0bc30c180ba5e7af91183098f419a53c23a787d86d02583a62d17e94",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:c5c777e2440b3a9f37b8669a70ccc2190eee17b159479f90e958c3d0fde2bd72"
        }
      },
      {
        "at": 13,
        "kind": "step_finish",
        "stepKey": "alarm_transition",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "inconclusive",
            "reasonCode": "PRECONDITION_BLOCKED",
            "evidenceIds": [],
            "evaluatedThrough": "2026-11-05T10:40:13Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 13,
        "kind": "check_result",
        "stepKey": "notification_received",
        "check": {
          "verdict": "inconclusive",
          "summary": "No perturbation was dispatched because the baseline precondition failed.",
          "expected": "Probe receipt within 60 s of the transition",
          "actual": null,
          "reasonCode": "PRECONDITION_BLOCKED",
          "evidenceIds": [],
          "evaluatedThrough": "2026-11-05T10:40:13Z",
          "collection": "unavailable",
          "coverage": "unknown",
          "proof": "witness",
          "window": null,
          "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
          "evaluatorVersion": "cel/assessment-v0.2",
          "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
          "synthetic": true
        }
      },
      {
        "at": 13,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_06",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "notification_received",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "check-result",
          "title": "Check evaluated",
          "summary": "No perturbation was dispatched because the baseline precondition failed.",
          "occurredAt": "2026-11-05T10:40:13Z",
          "observedAt": "2026-11-05T10:40:13Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/notification_received/6",
          "schemaRef": "sha256:8da958451339177026d5047c299a73f0e940ec3c19a6dc88ae48ff933760b0c1",
          "value": {
            "verdict": "inconclusive",
            "summary": "No perturbation was dispatched because the baseline precondition failed.",
            "expected": "Probe receipt within 60 s of the transition",
            "actual": null,
            "reasonCode": "PRECONDITION_BLOCKED",
            "evidenceIds": [],
            "evaluatedThrough": "2026-11-05T10:40:13Z",
            "collection": "unavailable",
            "coverage": "unknown",
            "proof": "witness",
            "window": null,
            "predicateDigest": "sha256:ad35864b3dc274ad44972de7cbf4c79035d0ce355bea4d5c73cf918cf980db73",
            "evaluatorVersion": "cel/assessment-v0.2",
            "evaluatorImplementationDigest": "sha256:98a28efdafe544e3ce570380013c87094829fbd67bf9bd59c64d6b68c478eeeb",
            "synthetic": true
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:6c71c6f97c3e69a482b909a3bfde43edcdf63b57d8bfe33446134a196bd985c7"
        }
      },
      {
        "at": 13,
        "kind": "step_finish",
        "stepKey": "notification_received",
        "outcome": "succeeded",
        "outputs": {
          "check": {
            "verdict": "inconclusive",
            "reasonCode": "PRECONDITION_BLOCKED",
            "evidenceIds": [],
            "evaluatedThrough": "2026-11-05T10:40:13Z"
          }
        },
        "error": null,
        "reason": null
      },
      {
        "at": 14,
        "kind": "run_phase",
        "phase": "finalizing",
        "reason": "The guard prevented mutation. Finalizers inspect the actual dispatch facts.",
        "termination": null
      },
      {
        "at": 15,
        "kind": "step_start",
        "stepKey": "stop_injection",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:stop_injection:1",
        "resolvedInputs": {
          "connection": {
            "connectionId": "connection_fulfillment_assessment",
            "capabilities": [
              "aws_assessment_scope"
            ]
          },
          "step": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "inject"
          }
        },
        "resolvedInputsDigest": "sha256:2ed1172676bcd856c0548d24d3019c4e859d7f0e236650a8f1b9798434a82b1a",
        "checkpoint": null
      },
      {
        "at": 16,
        "kind": "evidence",
        "record": {
          "evidenceId": "ev_baseline-blocked_07",
          "runId": "run_demo_baseline_blocked_20261105",
          "stepKey": "stop_injection",
          "source": "Assessment runtime",
          "sourceKind": "runtime",
          "kind": "reconciliation",
          "title": "No experiment was dispatched",
          "summary": "The injection StepRun has zero attempts. Cleanup is a proven no-op; no effect identity is invented.",
          "occurredAt": "2026-11-05T10:40:16Z",
          "observedAt": "2026-11-05T10:40:16Z",
          "collection": "complete",
          "coverage": "sufficient",
          "sourceRecordId": "demo/baseline-blocked/stop_injection/7",
          "schemaRef": "sha256:42de469c495ace93ae4ff79102428f61cd503018bce7548789380010ac0daf7b",
          "value": {
            "step": {
              "runId": "run_demo_baseline_blocked_20261105",
              "stepKey": "inject"
            },
            "attemptCount": 0,
            "remoteDisposition": "none",
            "reasonCode": "NOT_DISPATCHED"
          },
          "scope": {
            "accountId": "444455556666",
            "region": "eu-central-1",
            "deploymentRef": "deployment_fulfillment_prod_euc1"
          },
          "window": null,
          "synthetic": true,
          "contentDigest": "sha256:c74967f7d04cba1e2e8423775378950025c2772652e149b2f73e8762a898e8a6"
        }
      },
      {
        "at": 16,
        "kind": "step_finish",
        "stepKey": "stop_injection",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "none",
          "step": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "inject"
          },
          "reasonCode": "NOT_DISPATCHED",
          "evidenceIds": [
            "ev_baseline-blocked_07"
          ]
        },
        "error": null,
        "reason": null
      },
      {
        "at": 17,
        "kind": "step_start",
        "stepKey": "close_capture",
        "attemptNo": 1,
        "dispatchKey": "run_demo_baseline_blocked_20261105:close_capture:1",
        "resolvedInputs": {
          "step": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "capture"
          }
        },
        "resolvedInputsDigest": "sha256:7b56d261a6fd6ef34a22d0cd2d1e3bd68e02f0191fe69deb4ad7bc9692bbb602",
        "checkpoint": null
      },
      {
        "at": 18,
        "kind": "effect",
        "record": {
          "originEffectKey": "run_demo_baseline_blocked_20261105:capture:1:effect",
          "originAttempt": {
            "runId": "run_demo_baseline_blocked_20261105",
            "stepKey": "capture",
            "attemptNo": 1
          },
          "effectOrdinal": 1,
          "stepKey": "capture",
          "provider": "events/capture",
          "nativeId": "capture_fb38303b3e",
          "disposition": "terminal",
          "providerState": null,
          "localState": "closed",
          "observedAt": "2026-11-05T10:40:18Z",
          "observationKind": "local",
          "accountId": "444455556666",
          "region": "eu-central-1",
          "requiresHold": false,
          "requiresFinalization": true,
          "detail": "Capture closed after the proven no-op fault cleanup.",
          "actions": []
        },
        "observedByStepKey": "close_capture",
        "sourceKind": "runtime"
      },
      {
        "at": 18,
        "kind": "step_finish",
        "stepKey": "close_capture",
        "outcome": "succeeded",
        "outputs": {
          "remoteDisposition": "terminal",
          "originEffectKey": "run_demo_baseline_blocked_20261105:capture:1:effect",
          "evidenceIds": []
        },
        "error": null,
        "reason": null
      },
      {
        "at": 19,
        "kind": "run_phase",
        "phase": "finished",
        "reason": "A failed starting precondition prevented the infrastructure mutation.",
        "termination": null
      }
    ]
  }
];
  runs.forEach(run => { run.revision = revisions[run.revisionKey]; });
  return { schemaVersion: "assessment-fixtures/1", synthetic: true, revisions, runs };
}));
