---
id: record-mechanisms-MX-F-MEMORY
kind: record
collection: mechanisms
product: finops
title: Cross-session preference retention
order: 31
frozen: true
data:
  id: MX-F-MEMORY
  platform: finops
  title: Cross-session preference retention
  features:
  - FT-F-MEMORY
  sections:
  - F-M03
  trigger:
    $markdown: field-0001
  state: Instance-local retained preference
  process:
    $markdown: field-0002
  effect: Retained context update and read
  verification: Test a later conversation separately from reference-file retrieval.
  on_failure: State material query choices explicitly when retention is uncertain.
  review:
    primary_section: F-M03
    kind: Cross-session retained-context mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Write/update
      - Ask the agent to remember or update one non-sensitive preference.
      - Persistent conversational context
    - - Remove
      - Ask it to forget the specific retained fact.
      - Memory update, not history deletion
    - - Verify
      - Use a later session without restating the test fact.
      - Cross-session behavior
    lifecycle:
    - - Preference supplied
      - Remember/update
      - Retained context can influence later work.
    - - Preference retained
      - Forget
      - Memory is updated in place.
    - - Session ends
      - Start later session
      - Persistent instance data is separate from ephemeral runtime.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented:
      $markdown: field-0008
    test:
    - Use a fictitious reporting preference absent from uploaded files.
    - Test a later session, then change the preference and test again.
    - Forget it; do not claim that earlier reports or conversation history were erased.
    claims:
    - source: FS402
      section: Agent memory across sessions
      assertion: Remember, update and forget govern retained preferences/corrections.
    - source: FS403
      section: Data isolation; Managing your data
      assertion: Instance isolation and memory updates differ from conversation retention.
---

<!-- block: b-fff8bd14c3f05b778698 -->
## trigger

<!-- block: b-781a144168f559309ce5 -->
<!-- field: field-0001 -->
Conversation preferences, corrections or task outcomes; explicit remember, update or forget requests
<!-- /field -->

<!-- block: b-55c2a3cb806c566bb8c6 -->
## process

<!-- block: b-a260d289b863562089d9 -->
<!-- field: field-0002 -->
Apply retained preferences to subsequent sessions.
<!-- /field -->

<!-- block: b-671be83fce0353d9a024 -->
## review / inputs

<!-- block: b-3703d6050dff530c8093 -->
<!-- field: field-0003 -->
Conversation preferences, corrections, task outcomes, and explicit requests to remember, update or forget information within the instance.
<!-- /field -->

<!-- block: b-5b4517f7e8f05e088436 -->
## review / narrative / 0

<!-- block: b-e2e3d31843c05b0e90ec -->
<!-- field: field-0004 -->
Conversational memory retains preferences and corrections for later work in the same instance. It is not the current conversation transcript and is not an uploaded file. An explicit remember, update or forget instruction targets this retained representation.
<!-- /field -->

<!-- block: b-496b0c46c7e75283be37 -->
## review / narrative / 1

<!-- block: b-b43db3e8b2b35557b195 -->
<!-- field: field-0005 -->
Test it across sessions rather than immediately repeating the fact in the same conversation. Also inspect whether an active reference file supplies the same information; otherwise successful file use can be mistaken for memory recall.
<!-- /field -->

<!-- block: b-2892f5237f37552fb1c6 -->
## review / controls

<!-- block: b-afcfc07e50b25bdd8fa0 -->
<!-- field: field-0006 -->
Each instance isolates its retained content; no shared organization-wide memory is inferred.
<!-- /field -->

<!-- block: b-d597b9bf862454dd8adb -->
## review / observable output

<!-- block: b-2886520da59a51dea999 -->
<!-- field: field-0007 -->
Observed later use of a controlled fact, qualified when no direct memory-inspection evidence is exposed.
<!-- /field -->

<!-- block: b-e879385750275373a4ac -->
## review / undocumented

<!-- block: b-bcd18d705e065812a8ef -->
<!-- field: field-0008 -->
Internal schema, selection precedence and complete deletion of historical conversation occurrences are not established by a forget request.
<!-- /field -->
