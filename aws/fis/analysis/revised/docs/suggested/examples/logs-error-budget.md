---
id: aws-fis-revised-docs-suggested-examples-logs-error-budget
title: Logged error count scenario
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
- Logged error count scenario
related:
- README.md
- ../model.md
- ../adapters.md
- logs-error-budget.yaml
- logs-error-budget.lock.json
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/workflow/examples/logs-error-budget.yaml
---

# Logged error count scenario

The program runs a bounded Logs Insights query over declared log groups and an event-time window, then evaluates the typed numeric count against the configured maximum. Its finalizer inspects the query step and ensures any remote query has stopped.

**Claim boundary:** A missing or malformed aggregate is unavailable/schema-error evidence, not a measured zero. Query completion and consumed result pages are distinct, and the claim is bounded to the declared logging scope and coverage. It does not prove a global service error budget from arbitrary application logs. The complete source-backed interpretation is in [adapter contracts](../adapters.md); the [model](../model.md) defines evidence completeness, assessment and finalization.

[Canonical YAML](logs-error-budget.yaml) · [Synthetic publication lock](logs-error-budget.lock.json) · [Example index](README.md)

## Complete authoring document

```yaml
apiVersion: assessment/v0.2
name: Checkout logged error count
description: Assess a declared application log scope and fixed event-time window, subject to evidence coverage.
inputs:
  type: object
  additionalProperties: false
  required: [logGroups, windowStart, windowEnd, maximumErrors]
  properties:
    logGroups:
      type: array
      minItems: 1
      uniqueItems: true
      items: {type: string, minLength: 1}
    windowStart: {type: string, format: date-time}
    windowEnd: {type: string, format: date-time}
    maximumErrors: {type: integer, minimum: 0}
bindings:
  aws: {kind: connection, capability: cloudwatch_logs_query_scope}
policies:
  timeoutSeconds: 300
  finalizationTimeoutSeconds: 60
  concurrency: queue_per_deployment
steps:
  query_errors:
    uses: aws/cloudwatch.logs.query@1
    timeoutSeconds: 240
    with:
      connection: "${{ bindings.aws }}"
      logGroups: "${{ inputs.logGroups }}"
      windowStart: "${{ inputs.windowStart }}"
      windowEnd: "${{ inputs.windowEnd }}"
      language: CWLI
      resultShape: single_numeric_count
      query: |
        fields @timestamp, level
        | filter level = "ERROR"
        | stats count(*) as count
  error_budget:
    needs: [query_errors]
    after: settled
    uses: core/assert@1
    assessmentRole: criterion
    timeoutSeconds: 5
    with:
      observation: "${{ steps.query_errors.outputs.observation }}"
      proof: complete
      expect: value.count <= inputs.maximumErrors
finally:
  stop_query:
    uses: aws/cloudwatch.logs.ensure-stopped@1
    after: settled
    timeoutSeconds: 45
    with:
      connection: "${{ bindings.aws }}"
      step: "${{ steps.query_errors.ref }}"
```

## Publication and execution boundary

Publishing resolves the declared operation aliases to retained implementation and schema digests. Admission uses that fixed lock, not whichever contract an alias points to later. The lock in this example pins synthetic labels for contract review. No workflow or cloud action is executed by this Markdown or the accompanying static validator.
