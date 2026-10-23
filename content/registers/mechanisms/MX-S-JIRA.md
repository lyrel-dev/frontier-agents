---
id: record-mechanisms-MX-S-JIRA
kind: record
collection: mechanisms
product: security
title: Finding publication to Jira
order: 28
frozen: true
data:
  id: MX-S-JIRA
  platform: security
  title: Finding publication to Jira
  features:
  - FT-S-JIRA
  sections:
  - S-09
  - S-M07
  trigger: Reviewed finding selected for tracking
  state: Connection, project and finding relationship
  process:
    $markdown: field-0001
  effect: External publication
  verification: Inspect actual project audience and original finding linkage.
  on_failure: Keep the finding owned locally while resolving publication failure.
  review:
    primary_section: S-09
    kind: Finding-publication mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Register
      - Integrations → Add integration → Jira; authorize the Forge app and registration.
      - Site authorization
    - - Bind
      - Within Agent Space select project and allowed create/comment actions.
      - Project-specific effects
    - - Publish
      - Select finding(s) and create issues in a project permitting the Task type.
      - One issue per selected finding
    lifecycle:
    - - Finding selected
      - Create Jira issue
      - External record and finding relationship created.
    - - Linked finding revalidated
      - Supported result comment
      - External history updated when permitted.
    - - Integration removed
      - Future publication attempted
      - No further action through that integration; existing issues remain.
    controls:
      $markdown: field-0005
    observable_output: Actual issue/comment in the intended project and preserved finding link.
    undocumented:
      $markdown: field-0006
    test:
    - Use a restricted test project and a non-sensitive finding fixture.
    - Check audience, issue type and finding link.
    - $markdown: field-0007
    claims:
    - source: SS415
      section: Connecting projects to an Agent Space
      assertion: Create and comment actions are selected per project.
    - source: SS416
      section: Creating issues for findings
      assertion: The selected project must allow Task and receives one issue per selected finding.
    - source: SS417
      section: Prerequisites for removal
      assertion: Previously created issues are not deleted with the integration.
---

<!-- block: b-a37be5fb5fdd5346a24a -->
## process

<!-- block: b-1232e25004475e98ace7 -->
<!-- field: field-0001 -->
Publish supported issue or comment content to the configured project.
<!-- /field -->

<!-- block: b-f165780491765d71bd61 -->
## review / inputs

<!-- block: b-32f597a3c6a057bb864d -->
<!-- field: field-0002 -->
Connected Jira Cloud site, permitted project/actions, selected finding and reviewed disclosure scope.
<!-- /field -->

<!-- block: b-7936ccff32555c6fbaef -->
## review / narrative / 0

<!-- block: b-1bd89b4422b95cfe8931 -->
<!-- field: field-0003 -->
A site registration supplies authorization; a project connection chooses where the Agent Space can create issues or comments. Creating an issue publishes a finding into an external system with its own audience and lifecycle.
<!-- /field -->

<!-- block: b-9f93edb21574555a8f60 -->
## review / narrative / 1

<!-- block: b-f11d5fede49d50babd50 -->
<!-- field: field-0004 -->
The link matters later: remediation proposals and revalidation outcomes can be attached to the same issue through supported behavior. Removing the integration stops future actions but does not remove tickets already created.
<!-- /field -->

<!-- block: b-4e1d7ac4c0ef5563a257 -->
## review / controls

<!-- block: b-fe62869b6acf558f8bb4 -->
<!-- field: field-0005 -->
Issue creation and comment permission are separate. Do not import FinOps approval behavior into Security Agent.
<!-- /field -->

<!-- block: b-adcb70ff28b150babdb7 -->
## review / undocumented

<!-- block: b-97f4a0bfcf3c5034803f -->
<!-- field: field-0006 -->
Automatic duplicate suppression and transactional rollback across AWS and Jira are not established.
<!-- /field -->

<!-- block: b-8b84c6502659562d9f0f -->
## review / test / 2

<!-- block: b-3347bfff70d55b408fd0 -->
<!-- field: field-0007 -->
Revoke comment permission; distinguish publication failure from assessment failure and avoid blind duplicate retries.
<!-- /field -->
