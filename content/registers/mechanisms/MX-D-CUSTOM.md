---
id: record-mechanisms-MX-D-CUSTOM
kind: record
collection: mechanisms
product: devops
title: Configured custom-agent invocation
order: 8
frozen: true
data:
  id: MX-D-CUSTOM
  platform: devops
  title: Configured custom-agent invocation
  features:
  - FT-D-CUSTOM
  - FT-D-HISTORY
  sections:
  - D-07
  trigger: Manual invocation or configured trigger
  state: Definition, invocation and tool results
  process:
    $markdown: field-0001
  effect: Execution and output
  verification: Inspect tool arguments, failures and output against the task scope.
  on_failure: Mark incomplete output and resolve the failed prerequisite before repeating the run.
  review:
    primary_section: D-07
    kind: Definition-to-execution mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Define
      - Agents → Custom Agents → Create agent; provide goal, approach, constraints and output.
      - Reusable definition
    - - Select
      - Assign actual tools through the supported configuration path and applicable skills/stores.
      - Scoped execution resources
    - - Run
      - Run Now or Run with prompt; open the invocation in History.
      - Independent execution
    lifecycle:
    - - Definition saved
      - Run Now
      - An invocation starts or is pending.
    - - Invocation active
      - Cancel in trajectory or Chat
      - Completed evidence is retained; in-flight calls may still finish.
    - - No invocation active
      - Invoke again
      - A new record is created; do not assume prior transient context is inherited.
    controls:
      $markdown: field-0005
    observable_output: Invocation identity, status, tool arguments/results/errors and requested output.
    undocumented: Exactly-once effects and universal rollback after cancellation are not documented.
    test:
    - Create a harmless read-only report over a known staging signal.
    - Inspect the actual arguments and reconcile a figure in the output.
    - $markdown: field-0006
    claims:
    - source: DS407
      section: How custom agents work
      assertion: Prompt, selected tools and assigned skills are loaded per invocation.
    - source: DS408
      section: Running; Canceling an invocation; Tool call results
      assertion:
        $markdown: field-0007
    - source: DS414
      section: Creating a custom agent using the form
      assertion: Creation and tool assignment are separate setup concerns.
    diagram: mechanism-devops-cancellation
---

<!-- block: b-da729e5d4470584aa550 -->
## process

<!-- block: b-053b485c19e7520e9bc7 -->
<!-- field: field-0001 -->
Execute the selected operational work and retain its invocation trajectory.
<!-- /field -->

<!-- block: b-747f7c93be6552389447 -->
## review / inputs

<!-- block: b-ac68061e389159429e3c -->
<!-- field: field-0002 -->
Custom definition with system prompt, selected tools, assigned skills and applicable memory access; optional per-run prompt.
<!-- /field -->

<!-- block: b-ef3cfe307e635ad88704 -->
## review / narrative / 0

<!-- block: b-cbfd2835bcee57d785e9 -->
<!-- field: field-0003 -->
A custom definition persists across executions. Run Now creates a new invocation; an additional prompt supplies context for that run without replacing the system prompt. The execution loads its configured resources, calls available tools and records results in a trajectory.
<!-- /field -->

<!-- block: b-3562eff35ccb58e7ac23 -->
## review / narrative / 1

<!-- block: b-f672c2c82c30506880cf -->
<!-- field: field-0004 -->
A definition is not a running job. Likewise, an output artifact is not the invocation itself. Diagnose these objects separately when a report is missing: was an invocation created, did its tools complete, and was the requested output produced?
<!-- /field -->

<!-- block: b-c2a1015988aa591485c0 -->
## review / controls

<!-- block: b-0d2f67a4ca1f587298c4 -->
<!-- field: field-0005 -->
Only assigned tools are available. The documented execution page permits one invocation at a time per custom agent.
<!-- /field -->

<!-- block: b-f5d2aeb78bdb53a4aebd -->
## review / test / 2

<!-- block: b-4449a3f92ef55679b494 -->
<!-- field: field-0006 -->
Cancel a controlled long read; distinguish cancellation from completion of an already-started external call.
<!-- /field -->

<!-- block: b-a8def8a300f954609729 -->
## review / claims / 1 / assertion

<!-- block: b-a1b691cab93e5157b7e7 -->
<!-- field: field-0007 -->
Runs have history; cancellation preserves completed evidence and may not interrupt in-flight calls.
<!-- /field -->
