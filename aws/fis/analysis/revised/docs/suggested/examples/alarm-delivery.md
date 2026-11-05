---
id: aws-fis-revised-docs-suggested-examples-alarm-delivery
title: Alarm transition and probe receipt scenario
type: example
service: aws-fis
status: reviewed-proposal
version: '0.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- example
aliases:
- Alarm transition and probe receipt scenario
related:
- README.md
- ../model.md
- ../adapters.md
- alarm-delivery.yaml
- alarm-delivery.lock.json
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/workflow/examples/alarm-delivery.yaml
---

# Alarm transition and probe receipt scenario

The program opens the dedicated receiver capture before injection, reads the alarm baseline, gates mutation on the baseline precondition, starts one FIS experiment, and collects transition/receipt evidence. Two required criteria assess the alarm transition and the explicitly bound probe receiver separately. The stop finalizer precedes capture closure.

**Claim boundary:** A received probe message proves receipt by that probe. It does not establish production-consumer receipt or business processing. A positive witness may settle a restricted existential criterion; missing data requires a closed, sufficiently covered scope before it can establish absence. The complete source-backed interpretation is in [adapter contracts](../adapters.md); the [model](../model.md) defines evidence completeness, assessment and finalization.

[Canonical YAML](alarm-delivery.yaml) · [Synthetic publication lock](alarm-delivery.lock.json) · [Example index](README.md)

## Complete authoring document

```yaml
apiVersion: assessment/v0.2
name: Checkout alarm notification delivery
description: Verify an alarm transition and timely receipt by the explicitly bound probe receiver.
inputs:
  type: object
  additionalProperties: false
  required: [templateId, alarmArn, topicArn, receiverId]
  properties:
    templateId: {type: string, minLength: 1}
    alarmArn: {type: string, minLength: 1}
    topicArn: {type: string, minLength: 1}
    receiverId: {type: string, minLength: 1}
bindings:
  aws: {kind: connection, capability: aws_assessment_scope}
  receiver: {kind: connection, capability: dedicated_notification_receiver}
policies:
  timeoutSeconds: 600
  finalizationTimeoutSeconds: 180
  concurrency: queue_per_deployment
steps:
  capture:
    uses: events/capture.open@1
    timeoutSeconds: 30
    with:
      connection: "${{ bindings.receiver }}"
      receiverId: "${{ inputs.receiverId }}"
      topicArn: "${{ inputs.topicArn }}"
      leaseSeconds: 900
  baseline:
    uses: aws/cloudwatch.alarm.read@1
    timeoutSeconds: 30
    with:
      connection: "${{ bindings.aws }}"
      alarmArn: "${{ inputs.alarmArn }}"
  baseline_ok:
    needs: [baseline]
    uses: core/assert@1
    assessmentRole: precondition
    timeoutSeconds: 5
    with:
      observation: "${{ steps.baseline.outputs.observation }}"
      proof: complete
      expect: value.state == "OK"
  inject:
    needs: [capture, baseline_ok]
    uses: aws/fis.start@1
    timeoutSeconds: 45
    with:
      connection: "${{ bindings.aws }}"
      templateId: "${{ inputs.templateId }}"
  collect:
    needs: [inject]
    after: settled
    uses: events/capture.collect-alarm@1
    timeoutSeconds: 300
    with:
      captureStep: "${{ steps.capture.ref }}"
      injectionStep: "${{ steps.inject.ref }}"
      alarmArn: "${{ inputs.alarmArn }}"
      topicArn: "${{ inputs.topicArn }}"
      receiverId: "${{ inputs.receiverId }}"
      transitionWindowSeconds: 180
      receiptDeadlineSeconds: 60
      collectionGraceSeconds: 30
  alarm_transition:
    needs: [collect]
    after: settled
    uses: core/assert@1
    assessmentRole: criterion
    timeoutSeconds: 5
    with:
      observation: "${{ steps.collect.outputs.transition }}"
      proof: witness
      operator: exists
  notification_received:
    needs: [collect]
    after: settled
    uses: core/assert@1
    assessmentRole: criterion
    timeoutSeconds: 5
    with:
      observation: "${{ steps.collect.outputs.receipt }}"
      proof: witness
      operator: exists
finally:
  stop_injection:
    uses: aws/fis.ensure-stopped@1
    after: settled
    timeoutSeconds: 120
    with:
      connection: "${{ bindings.aws }}"
      step: "${{ steps.inject.ref }}"
  close_capture:
    needs: [stop_injection]
    after: settled
    uses: events/capture.close@1
    timeoutSeconds: 30
    with:
      step: "${{ steps.capture.ref }}"
```

## Publication and execution boundary

Publishing resolves the declared operation aliases to retained implementation and schema digests. Admission uses that fixed lock, not whichever contract an alias points to later. The lock in this example pins synthetic labels for contract review. No workflow or cloud action is executed by this Markdown or the accompanying static validator.
