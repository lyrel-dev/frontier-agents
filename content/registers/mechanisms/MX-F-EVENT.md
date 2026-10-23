---
id: record-mechanisms-MX-F-EVENT
kind: record
collection: mechanisms
product: finops
title: Anomaly-event matching and task creation
order: 35
frozen: true
data:
  id: MX-F-EVENT
  platform: finops
  title: Anomaly-event matching and task creation
  features:
  - FT-F-AUTOMATIONS
  - FT-F-TASKS
  sections:
  - F-M05
  trigger: Matching Cost Anomaly Detection event
  state: Managed rule, automation and queued task
  process:
    $markdown: field-0001
  effect: Task creation; publication is a separate configured step
  verification: Trace event, automation, task, analysis and destination result independently.
  on_failure: Inspect monitor conditions and rule permissions before changing the analytical prompt.
  review:
    primary_section: F-M05
    kind: Anomaly-event matching mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Prerequisites
      - Configure a monitor and the agent-role EventBridge permissions.
      - Event source and managed-rule authority
    - - Automation
      - Describe monitor/scope, threshold and desired response in Chat.
      - COST_ANOMALY trigger and prompt
    - - Verification
      - $markdown: field-0005
      - End-to-end observation
    lifecycle:
    - - Matching event arrives
      - Automation matches
      - Task created in the queue.
    - - Task completes
      - Optional publication
      - Delivery has its own outcome.
    - - Automation disabled/deleted
      - Future event arrives
      - No future task from that automation; old records remain.
    controls:
      $markdown: field-0006
    observable_output: Monitor/event identity, automation, task, source analysis and any actual message.
    undocumented:
      $markdown: field-0007
    test:
    - Use a controlled event fixture for tabletop tracing; do not manufacture production spend.
    - Verify all chain identities against available service records during an authorized test.
    - $markdown: field-0008
    claims:
    - source: FS405
      section: Prerequisites; Verify and manage the automation
      assertion:
        $markdown: field-0009
    - source: FS404
      section: Event-based tasks
      assertion: The supported preview trigger is a cost-anomaly event.
    diagram: mechanism-finops-publication
---

<!-- block: b-ba50f29c23d05c3b9fe6 -->
## process

<!-- block: b-114484baa3a65f0fbe4f -->
<!-- field: field-0001 -->
Match the supported event to its configured response prompt.
<!-- /field -->

<!-- block: b-73f2b462790753319e44 -->
## review / inputs

<!-- block: b-a8e4b80d2998507a8d59 -->
<!-- field: field-0002 -->
Cost Anomaly Detection monitor, required managed EventBridge permissions, condition, response prompt and optional destination.
<!-- /field -->

<!-- block: b-2fbcfa94e94e5772889c -->
## review / narrative / 0

<!-- block: b-5b4bfb3d0180566ab4ff -->
<!-- field: field-0003 -->
The event path begins in Cost Anomaly Detection. The service creates a managed rule, matches the configured condition and creates a task using the saved prompt. Analysis and delivery occur after task creation; they are not evidence that matching itself was correct.
<!-- /field -->

<!-- block: b-2ec124845e7059d0aabe -->
## review / narrative / 1

<!-- block: b-1625e79c26b55605af9f -->
<!-- field: field-0004 -->
Trace the chain one object at a time. A monitor event with no task points toward rule or condition configuration. A completed analysis with no message points toward destination publication. Changing the analytical prompt does not repair an absent event subscription.
<!-- /field -->

<!-- block: b-97bc2850002b56febc04 -->
## review / configuration / 2 / 1

<!-- block: b-5b4a81586018564dbccf -->
<!-- field: field-0005 -->
Inspect automation status, last-triggered information, created task and destination result.
<!-- /field -->

<!-- block: b-3af1e8ec39ff5fc2854a -->
## review / controls

<!-- block: b-9730d45632bb5825a571 -->
<!-- field: field-0006 -->
The documented preview event source is Cost Anomaly Detection, not arbitrary events. External publication requires its configured destination.
<!-- /field -->

<!-- block: b-a25b094b72305d32b8b9 -->
## review / undocumented

<!-- block: b-c11f07bbefaf57cf8b56 -->
<!-- field: field-0007 -->
Event deduplication keys, ordering and universal delivery/retry guarantees are not established.
<!-- /field -->

<!-- block: b-0c0c8ed03c1850ddb21e -->
## review / test / 2

<!-- block: b-ca92c1bc591d58edb783 -->
<!-- field: field-0008 -->
A missing message must be localized to absent task, failed analysis or failed delivery rather than reported as one undifferentiated error.
<!-- /field -->

<!-- block: b-37905651a4165d59b1ad -->
## review / claims / 0 / assertion

<!-- block: b-62c4c9ecbce853628f84 -->
<!-- field: field-0009 -->
Monitor, managed-rule permissions and saved condition create a traceable automation/task path.
<!-- /field -->
