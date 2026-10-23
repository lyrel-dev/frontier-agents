---
id: record-profiles-PR-D-REPORT
kind: record
collection: profiles
product: ''
title: Custom operational reporting configuration
order: 1
frozen: true
data:
  id: PR-D-REPORT
  title: Custom operational reporting configuration
  platforms:
  - devops
  mechanisms:
  - MX-D-READ
  - MX-D-CUSTOM
  - MX-D-SKILL
  - MX-D-RECALL
  - MX-D-INSTRUCTIONS
  - MX-D-SCHEDULE
  - MX-D-TOPOLOGY
  parameters:
  - - Resource scope
    - Actual service and resource identifiers
    - Approved service list
  - - Tool selection
    - Exact operations available in the Agent Space
    - Selected telemetry, incident or deployment read tools
  - - Reporting basis
    - Period, dimensions, aggregation, comparison and failed-read treatment
    - Previous complete UTC day with declared percentile and error-rate basis
  - - Context
    - Only the relevant procedure and mapping
    - Reviewed report skill and explicitly selected store
  - - Schedule
    - Optional timing separate from observation window
    - Disabled until a trial invocation passes
  - - Publication
    - Separate destination-specific effect
    - No external destination by default
  setup:
  - $markdown: field-0001
  - $markdown: field-0002
  - $markdown: field-0003
  - $markdown: field-0004
  tests:
  - $markdown: field-0005
  - $markdown: field-0006
  - $markdown: field-0007
  stop_behavior:
    $markdown: field-0008
---

<!-- block: b-b23e1a637f2e51d19caa -->
## setup / 0

<!-- block: b-184feef260b05ef2b74b -->
<!-- field: field-0001 -->
Create the custom definition with explicit objective, output and source limits.
<!-- /field -->

<!-- block: b-4f4ba161d85e59e295d5 -->
## setup / 1

<!-- block: b-8f6db214d0dd5f3ab5e3 -->
<!-- field: field-0002 -->
Select actual tools and inspect applicable skills and store access using the current guide.
<!-- /field -->

<!-- block: b-73381d983e365203ada0 -->
## setup / 2

<!-- block: b-6d79edabc0ef51a28477 -->
<!-- field: field-0003 -->
Run once, inspect the invocation and reconcile material measurements.
<!-- /field -->

<!-- block: b-21cd5b88119b5145b6a2 -->
## setup / 3

<!-- block: b-996520a549e65dad8cec -->
<!-- field: field-0004 -->
Enable recurrence only when schedule variability and concurrency suit the requirement.
<!-- /field -->

<!-- block: b-cacddfad4f5e5824ab19 -->
## tests / 0

<!-- block: b-14e4ea99a72b5b44afa6 -->
<!-- field: field-0005 -->
Unavailable telemetry is missing evidence, not a healthy result.
<!-- /field -->

<!-- block: b-a5ee09e3699b55b699ec -->
## tests / 1

<!-- block: b-9d1a06ee9c235da3b78a -->
<!-- field: field-0006 -->
A known mapping is interpreted from the intended context.
<!-- /field -->

<!-- block: b-5a1ad055d17b56d29b60 -->
## tests / 2

<!-- block: b-d6628596d5ea51088c9a -->
<!-- field: field-0007 -->
A delayed invocation exposes both observation time and generation time.
<!-- /field -->

<!-- block: b-e29bf37f3b4b5abab054 -->
## stop behavior

<!-- block: b-ede78f54a5a85cb09ad5 -->
<!-- field: field-0008 -->
Pause future triggers and cancel current work separately. Do not claim guaranteed minute-by-minute delivery from a flexible schedule.
<!-- /field -->
