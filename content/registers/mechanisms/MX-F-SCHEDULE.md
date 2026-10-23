---
id: record-mechanisms-MX-F-SCHEDULE
kind: record
collection: mechanisms
product: finops
title: Scheduled task creation
order: 34
frozen: true
data:
  id: MX-F-SCHEDULE
  platform: finops
  title: Scheduled task creation
  features:
  - FT-F-AUTOMATIONS
  - FT-F-TASKS
  sections:
  - F-03
  trigger: Saved recurring schedule
  state: Automation and independently retained tasks
  process:
    $markdown: field-0001
  effect: Future tasks
  verification: Inspect trigger and the actual task's reporting window separately.
  on_failure: Disable future starts and control already-created work separately.
  review:
    primary_section: F-03
    kind: Automation-to-task mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Create
      - Describe the recurring work and schedule in conversation.
      - Saved automation
    - - Inspect
      - Open Automations and confirm the actual saved schedule and prompt.
      - Configuration confirmation
    - - Disable/delete
      - Stop future occurrences through the automation control.
      - Not cancellation/deletion of prior tasks
    lifecycle:
    - - Automation active
      - Scheduled occurrence
      - A new task is created.
    - - Automation active
      - Disable
      - Future starts stop.
    - - Automation deleted
      - Inspect existing tasks/artifacts
      - Historical work remains independently retained.
    controls:
      $markdown: field-0005
    observable_output: Automation configuration and individual task histories with their queried periods.
    undocumented:
      $markdown: field-0006
    test:
    - Create a non-sensitive recurring report only after an on-demand trial.
    - Inspect saved timing and the first task observation window.
    - $markdown: field-0007
    claims:
    - source: FS404
      section: Scheduled tasks
      assertion: Schedules create automations and new tasks; disabling/deleting stops recurring work.
    - source: FS403
      section: Managing your data
      assertion: Automations and task records have distinct lifecycles.
---

<!-- block: b-326fb87d15115fdda39f -->
## process

<!-- block: b-1649f54dde8f54e18edc -->
<!-- field: field-0001 -->
Create a new task on each applicable scheduled occurrence.
<!-- /field -->

<!-- block: b-64be26b620a059caa450 -->
## review / inputs

<!-- block: b-246defe93f6d5fa9bf68 -->
<!-- field: field-0002 -->
Recurring prompt, explicit schedule and timezone, observation-window rule and optional destination.
<!-- /field -->

<!-- block: b-f93ecae074675513a18f -->
## review / narrative / 0

<!-- block: b-c409702b80915c09b25f -->
<!-- field: field-0003 -->
A recurring request creates an automation. Each eligible occurrence creates separate work; the automation is not the historical report. Keep the schedule and reporting basis distinct so a delayed task still queries the intended complete period.
<!-- /field -->

<!-- block: b-91e20bc2ead254c19654 -->
## review / narrative / 1

<!-- block: b-1e615f1a65595ef599eb -->
<!-- field: field-0004 -->
Disabling an automation controls future starts. Existing tasks and distributed artifacts retain their own lifecycle. When replacing recurring work, inspect old automations to avoid running both definitions unintentionally.
<!-- /field -->

<!-- block: b-7ad84749bb9852a1b2bf -->
## review / controls

<!-- block: b-e7d3d94a28595256b721 -->
<!-- field: field-0005 -->
Unattended publication has destination-specific authorization; recurrence is not a universal approval bypass for unrelated actions.
<!-- /field -->

<!-- block: b-99f1f41757ee50ac85bb -->
## review / undocumented

<!-- block: b-cf0da8df64175289847d -->
<!-- field: field-0006 -->
Exact missed-run and timezone-resolution behavior must be inspected; the guide does not establish a universal timing SLA.
<!-- /field -->

<!-- block: b-502117683cc85847807e -->
## review / test / 2

<!-- block: b-ea82e0ffb37c5d2ea89a -->
<!-- field: field-0007 -->
Disable the automation and confirm future creation stops without assuming prior artifacts disappear.
<!-- /field -->
