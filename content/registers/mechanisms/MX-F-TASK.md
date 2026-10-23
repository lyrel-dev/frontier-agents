---
id: record-mechanisms-MX-F-TASK
kind: record
collection: mechanisms
product: finops
title: Queued task execution and observation
order: 33
frozen: true
data:
  id: MX-F-TASK
  platform: finops
  title: Queued task execution and observation
  features:
  - FT-F-TASKS
  sections:
  - F-03
  trigger: Explicit task request or automation
  state: Task status, source results and outputs
  process:
    $markdown: field-0001
  effect: Execution and output
  verification: Match completed results to task identity and requested scope.
  on_failure: Distinguish absent, queued and failed tasks before retrying.
  review:
    primary_section: F-03
    kind: Explicit request-to-task mechanism
    inputs: Explicit task request or automation invocation, prompt and permitted data/context.
    narrative:
    - $markdown: field-0002
    - $markdown: field-0003
    configuration:
    - - Create
      - Ask explicitly to create a task, or Tasks → Create tasks.
      - Separate execution record
    - - Observe
      - Inspect Tasks/history and actual tool results.
      - Work status and evidence
    - - Stop
      - Use supported cancellation for current work; control recurring automation separately.
      - Execution versus definition
    lifecycle:
    - - Task requested
      - Create record
      - Work enters the shared queue.
    - - Queued work
      - Execute
      - Tool results and output accumulate.
    - - Task cancelled
      - Inspect retained record
      - Cancellation does not delete task history.
    controls: Cancelling work is not rollback of prior external publication.
    observable_output: Task identity, execution status, source calls, outputs and separate delivery outcome.
    undocumented:
      $markdown: field-0004
    test:
    - Create a report task using non-sensitive inputs with an explicit date range.
    - Trace its identity from request to resulting output.
    - Cancel controlled work and distinguish preserved history from a deleted task.
    claims:
    - source: FS404
      section: On-demand tasks
      assertion: Tasks are explicit and run through a shared queue rather than blocking the conversation.
    - source: FS403
      section: Managing your data
      assertion: Cancellation and record removal are different lifecycle operations.
---

<!-- block: b-0a66a25191035d2bb24e -->
## process

<!-- block: b-276fc3ade219535e9e36 -->
<!-- field: field-0001 -->
Run queued work and retain its separate execution evidence.
<!-- /field -->

<!-- block: b-0967a7ba13a15bb7a555 -->
## review / narrative / 0

<!-- block: b-67fc67813a905f6c9bc3 -->
<!-- field: field-0002 -->
An ordinary question can be answered in the conversation. A task is created when explicitly requested or through an automation. The task has its own queue position, execution and output, so a chat acknowledgement is not completion evidence.
<!-- /field -->

<!-- block: b-3b9bd54b61335555b594 -->
## review / narrative / 1

<!-- block: b-9f22ea953e9752108049 -->
<!-- field: field-0003 -->
All documented task types share a queue. Inspect whether work was never created, remains queued, failed during analysis or completed but failed to publish. Those failures require different actions.
<!-- /field -->

<!-- block: b-55cdefb636ab58b0bba7 -->
## review / undocumented

<!-- block: b-bc4a0d2035855c10acc0 -->
<!-- field: field-0004 -->
Queue order, fairness, exactly-once processing and guaranteed cancellation of every in-flight action are not specified.
<!-- /field -->
