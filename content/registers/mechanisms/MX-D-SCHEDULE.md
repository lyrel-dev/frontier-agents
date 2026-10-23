---
id: record-mechanisms-MX-D-SCHEDULE
kind: record
collection: mechanisms
product: devops
title: Schedule-to-invocation creation
order: 9
frozen: true
data:
  id: MX-D-SCHEDULE
  platform: devops
  title: Schedule-to-invocation creation
  features:
  - FT-D-SCHEDULE
  - FT-D-HISTORY
  sections:
  - D-07
  trigger: Configured schedule becomes due
  state: Trigger and independently managed invocation
  process:
    $markdown: field-0001
  effect: Future invocation
  verification: Inspect saved timing and actual start; record the observation window independently.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-07
    kind: Trigger-to-execution mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Create
      - Agents → selected custom agent → Triggers → create; enter a valid rate or cron expression.
      - Recurring trigger
    - - Inspect
      - Confirm saved expression, next run and actual start.
      - Timing evidence
    - - Stop
      - Pause/delete trigger and, if needed, cancel the current invocation separately.
      - Future versus current work
    lifecycle:
    - - Trigger active
      - Schedule due
      - Eligible future invocation under timing/concurrency constraints.
    - - Trigger active
      - Pause
      - Future starts disabled until resumed.
    - - Trigger paused
      - Resume
      - Future schedule becomes active.
    - - Trigger exists
      - Delete
      - Trigger is removed; existing execution evidence is separate.
    controls:
      $markdown: field-0006
    observable_output: Trigger configuration plus actual invocation timing and observation interval.
    undocumented:
      $markdown: field-0007
    test:
    - Choose a non-time-critical test report and explicit UTC reporting period.
    - Compare due time, actual start and the period queried.
    - $markdown: field-0008
    claims:
    - source: DS408
      section: Scheduling custom agents; Managing triggers
      assertion: Rate/cron triggers can be paused or deleted separately from invocations.
    - source: DS409
      section: CronSchedule
      assertion: The schedule anchors a flexible window of up to 30 minutes.
---

<!-- block: b-8f4c038b0ad55da79ba5 -->
## process

<!-- block: b-82e03514e4b250b99e15 -->
<!-- field: field-0001 -->
Create future work under the supported scheduling and concurrency constraints.
<!-- /field -->

<!-- block: b-897712d11d0a5c7b9ebe -->
## on failure

<!-- block: b-15c900a9a07f5ab49f8a -->
<!-- field: field-0002 -->
Use explicit invocation when timing is critical. Pausing future starts does not cancel current work.
<!-- /field -->

<!-- block: b-1d9db7eb7c8a5873969c -->
## review / inputs

<!-- block: b-482d873cde545eb99107 -->
<!-- field: field-0003 -->
Saved custom agent and valid rate/cron trigger; explicit reporting-window rules in task instructions.
<!-- /field -->

<!-- block: b-4a8138ae457053ea8658 -->
## review / narrative / 0

<!-- block: b-c288ffd2851f5518bfa3 -->
<!-- field: field-0004 -->
A trigger schedules future invocation opportunities. It does not specify the observation interval used by a report. The API reference further qualifies the timing: custom-agent schedules use a flexible start window of up to 30 minutes. An expression therefore cannot be presented as an exact delivery deadline.
<!-- /field -->

<!-- block: b-1de309b50dc35b6088fe -->
## review / narrative / 1

<!-- block: b-5ef1708474aa58cc8141 -->
<!-- field: field-0005 -->
Pausing the trigger prevents subsequent starts but does not cancel a running invocation. These are two independent control operations and should be inspected separately when retiring recurring work.
<!-- /field -->

<!-- block: b-5011a9afca5e510eb566 -->
## review / controls

<!-- block: b-d65a890beaf25f5899af -->
<!-- field: field-0006 -->
Schedule variability, one-at-a-time custom execution and external-call completion are independent constraints.
<!-- /field -->

<!-- block: b-86933dc02fa157798a9c -->
## review / undocumented

<!-- block: b-91c1e15470b753838448 -->
<!-- field: field-0007 -->
Missed-occurrence, overlap queueing and exactly-once delivery behavior are not established by the cited schedule pages.
<!-- /field -->

<!-- block: b-aff7e5ef01c052d28262 -->
## review / test / 2

<!-- block: b-e147784c75695390a1ff -->
<!-- field: field-0008 -->
Run longer than the interval in an approved test and record actual behavior rather than assuming queued catch-up.
<!-- /field -->
