---
id: record-profiles-PR-F-AUTOMATION
kind: record
collection: profiles
product: ''
title: Recurring or anomaly-triggered FinOps work
order: 8
frozen: true
data:
  id: PR-F-AUTOMATION
  title: Recurring or anomaly-triggered FinOps work
  platforms:
  - finops
  mechanisms:
  - MX-F-SCHEDULE
  - MX-F-EVENT
  - MX-F-TASK
  - MX-F-QUERY
  - MX-F-ARTIFACT
  parameters:
  - - Trigger
    - Schedule or supported anomaly event
    - Explicit schedule OR selected Cost Anomaly Detection monitor
  - - Observation window
    - Period independent of execution time
    - Previous complete calendar week
  - - Destination
    - Optional and separately reviewed
    - No external publication by default
  setup:
  - $markdown: field-0001
  - $markdown: field-0002
  - $markdown: field-0003
  tests:
  - $markdown: field-0004
  - $markdown: field-0005
  - $markdown: field-0006
  stop_behavior:
    $markdown: field-0007
---

<!-- block: b-f6c68259d383565c8222 -->
## setup / 0

<!-- block: b-f49474f2b6c45fffb85a -->
<!-- field: field-0001 -->
Verify trigger permissions and source monitor where event-driven.
<!-- /field -->

<!-- block: b-3b602bd88b0252b39487 -->
## setup / 1

<!-- block: b-bb0f36368af651938326 -->
<!-- field: field-0002 -->
Inspect the stored automation rather than rely on conversational acknowledgement.
<!-- /field -->

<!-- block: b-d42508796f285e38872e -->
## setup / 2

<!-- block: b-589180bf3ea059389d04 -->
<!-- field: field-0003 -->
Trace an actual task to its analysis and optional delivery.
<!-- /field -->

<!-- block: b-146c468b1fc0589dbe5b -->
## tests / 0

<!-- block: b-104195ac9f5d5e229d0d -->
<!-- field: field-0004 -->
A nonmatching event creates no expected task.
<!-- /field -->

<!-- block: b-5a79dbba54da5fc7b485 -->
## tests / 1

<!-- block: b-493719eb077c505a9e35 -->
<!-- field: field-0005 -->
Queue, analysis and publication failures remain distinguishable.
<!-- /field -->

<!-- block: b-a5d60a062b5d50b29f76 -->
## tests / 2

<!-- block: b-7c1762be25a65a1bbd95 -->
<!-- field: field-0006 -->
Disabling automation stops future starts, not deletion of old tasks.
<!-- /field -->

<!-- block: b-ba5cb3d1e7d059078515 -->
## stop behavior

<!-- block: b-9a25f7d0300d57c2803f -->
<!-- field: field-0007 -->
Disable the automation and control existing tasks separately. Manage external records at their destination.
<!-- /field -->
