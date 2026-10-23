---
id: record-mechanisms-MX-D-INSTRUCTIONS
kind: record
collection: mechanisms
product: devops
title: Standing instruction loading
order: 4
frozen: true
data:
  id: MX-D-INSTRUCTIONS
  platform: devops
  title: Standing instruction loading
  features:
  - FT-D-INSTRUCTIONS
  sections:
  - D-M03
  trigger: New applicable session
  state: Saved global or agent-specific guidance
  process:
    $markdown: field-0001
  effect: Session context
  verification: Test a new session against the saved instruction version.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-M03
    kind: Session-initialization mechanism
    inputs: Saved global and applicable agent-specific AGENTS.md text and a newly starting session.
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Scope
      - $markdown: field-0005
      - Applicable AGENTS.md content
    - - Propagation
      - Save, then start a new session.
      - Startup-loaded content
    - - UI version
      - $markdown: field-0006
      - Navigation qualification
    lifecycle:
    - - Saved guidance
      - Start session
      - Applicable content is loaded.
    - - Session active
      - Edit saved guidance
      - Active session retains its startup content.
    - - Updated guidance
      - Start another session
      - New content becomes applicable.
    controls:
      $markdown: field-0007
    observable_output: Saved instruction content and observable behavior in a newly started session.
    undocumented:
      $markdown: field-0008
    test:
    - Add a test-only required heading to a scoped test instruction.
    - Compare a new session with one started before the change.
    - A denied tool must remain denied even when the instruction asks to use it.
    claims:
    - source: DS405
      section: How agent instructions work; Agent type scoping
      assertion: Instructions are loaded at session start; existing sessions retain the original content.
---

<!-- block: b-e54d0ae249fd518fa946 -->
## process

<!-- block: b-b905f4da465f5b73a113 -->
<!-- field: field-0001 -->
Load standing instructions at session start.
<!-- /field -->

<!-- block: b-f88edd2841bf5ff18cd6 -->
## on failure

<!-- block: b-317b5c7a716c5383826f -->
<!-- field: field-0002 -->
Inspect scope and session start time rather than assuming existing sessions received updates.
<!-- /field -->

<!-- block: b-fe3262c6cbc05f10bd72 -->
## review / narrative / 0

<!-- block: b-6d62e78a0b4c5d48b69c -->
<!-- field: field-0003 -->
Standing instructions are loaded at session initialization. The service includes applicable global and agent-specific content without relying on task-relevance selection. Saving a change affects newly started sessions, not the content already loaded by an existing session.
<!-- /field -->

<!-- block: b-91f63666011359c5ae9d -->
## review / narrative / 1

<!-- block: b-05059680c7eb514bb8b7 -->
<!-- field: field-0004 -->
This makes instructions suitable for persistent reporting conventions. It does not make their content an IAM policy. Use an ordinary output convention as a propagation test and verify actual permissions separately.
<!-- /field -->

<!-- block: b-ff7d0618c7b65035b795 -->
## review / configuration / 0 / 1

<!-- block: b-99d5b4cb0f975861b379 -->
<!-- field: field-0005 -->
Edit global or relevant managed-agent instructions using the instruction editor exposed by the operator app.
<!-- /field -->

<!-- block: b-72ce5f60b5c5531c9b6f -->
## review / configuration / 2 / 1

<!-- block: b-d5e28000ba1954d28e16 -->
<!-- field: field-0006 -->
Retrieved guidance shows both Knowledge → Instructions and Agents → Managed agents → Agent definition. Use the editor present in the deployed interface.
<!-- /field -->

<!-- block: b-c99ad6bb1b255a79b44a -->
## review / controls

<!-- block: b-c0b0bccf09195fbcbf70 -->
<!-- field: field-0007 -->
An instruction cannot grant a tool, change a trust policy or substitute for action approval.
<!-- /field -->

<!-- block: b-a7e8ee57eb615713b412 -->
## review / undocumented

<!-- block: b-84d57e82613f5a73a6cc -->
<!-- field: field-0008 -->
Conflict precedence for contradictory global, agent-specific and task instructions is not fully specified; do not assume a precedence order.
<!-- /field -->
