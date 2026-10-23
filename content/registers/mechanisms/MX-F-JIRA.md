---
id: record-mechanisms-MX-F-JIRA
kind: record
collection: mechanisms
product: finops
title: Invocation-dependent Jira approval
order: 37
frozen: true
data:
  id: MX-F-JIRA
  platform: finops
  title: Invocation-dependent Jira approval
  features:
  - FT-F-JIRA
  sections:
  - F-05
  - F-M06
  trigger: Supported issue or comment request
  state: Destination and invocation-specific authorization
  process:
    $markdown: field-0001
  effect: External publication
  verification: Inspect invocation type, action details, destination and resulting issue or comment.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: F-M06
    kind: Invocation-dependent publication mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Connect
      - Authorize the Jira Cloud integration, then bind the approved project to this instance.
      - Project scope
    - - Interactive action
      - Review project, issue/comment body and target shown for approval.
      - Per-action decision
    - - Automation action
      - Review action and audience before enabling recurrence/event handling.
      - Setup-time authorization
    lifecycle:
    - - Interactive request
      - Confirm/revise action
      - Supported publication can execute.
    - - Automation configured
      - Matching invocation
      - Publication executes without a per-run approval prompt.
    - - Publication uncertain
      - Inspect destination before retry
      - Avoid assuming an unobserved response means no issue exists.
    controls:
      $markdown: field-0006
    observable_output: Actual issue/comment, intended project and task action history.
    undocumented: Exactly-once external publication and automatic duplicate suppression are not documented.
    test:
    - Use a restricted Jira Cloud test project and non-sensitive payload.
    - Compare interactive approval with a separately reviewed automation test.
    - $markdown: field-0007
    claims:
    - source: FS407
      section: Jira issue creation and comment addition
      assertion: Approval differs between interactive/on-demand and automated invocation.
    - source: FS408
      section: Integration model; Capabilities
      assertion: Project connections and supported actions limit the effect.
---

<!-- block: b-e650535222c053969b0f -->
## process

<!-- block: b-0ad188fa6628577796d6 -->
<!-- field: field-0001 -->
Request approval interactively or on demand; use setup authorization for scheduled or event-driven actions.
<!-- /field -->

<!-- block: b-7133b4d6b9a45a7c95ec -->
## on failure

<!-- block: b-6803fdec1ad25d1fa582 -->
<!-- field: field-0002 -->
Stop incorrect destinations. Do not expect an interactive prompt to protect an unattended automation.
<!-- /field -->

<!-- block: b-985fdee980db55ac9ba1 -->
## review / inputs

<!-- block: b-b472008d6b785586a304 -->
<!-- field: field-0003 -->
Account Jira registration, per-instance project connection, supported action, payload and invocation mode.
<!-- /field -->

<!-- block: b-bbfbb712f40e569895ec -->
## review / narrative / 0

<!-- block: b-bfafc1cf56d3597f8de3 -->
<!-- field: field-0004 -->
Jira approval depends on how the action starts. Chat and on-demand tasks present issue/comment details for confirmation; a scheduled or event automation uses authorization established during setup. The same destination does not imply the same per-run approval behavior.
<!-- /field -->

<!-- block: b-3b5114b94999581ab2dd -->
## review / narrative / 1

<!-- block: b-1201f46d1ca9523bbc21 -->
<!-- field: field-0005 -->
After approval or preauthorization, inspect the actual external record. A successful analysis is not a successful issue creation, and a retry after an uncertain response can create duplicates unless the operator checks the existing project records.
<!-- /field -->

<!-- block: b-ffe01b27380651cc96f2 -->
## review / controls

<!-- block: b-5b62dbde1ded509285db -->
<!-- field: field-0006 -->
Supported actions do not include arbitrary issue-field changes, deletion or Jira workflow management.
<!-- /field -->

<!-- block: b-c985048691fa50468189 -->
## review / test / 2

<!-- block: b-db90f2e13ed05198af5a -->
<!-- field: field-0007 -->
Deny project access and verify a publication failure does not erase or falsely complete the analysis record.
<!-- /field -->
