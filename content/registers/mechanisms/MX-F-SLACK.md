---
id: record-mechanisms-MX-F-SLACK
kind: record
collection: mechanisms
product: finops
title: Direct Slack publication
order: 38
frozen: true
data:
  id: MX-F-SLACK
  platform: finops
  title: Direct Slack publication
  features:
  - FT-F-SLACK
  sections:
  - F-05
  - F-M06
  trigger: Supported message request
  state: Workspace, channel connection and membership
  process:
    $markdown: field-0001
  effect: External publication
  verification: Review audience before invocation and inspect delivery afterward.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: F-M06
    kind: One-way destination-publication mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Register
      - Authorize the workspace integration.
      - Account-level registration
    - - Connect
      - $markdown: field-0006
      - Instance-specific destination
    - - Publish
      - Use the reviewed destination and verify the resulting post.
      - External effect
    lifecycle:
    - - Connection active
      - Post requested
      - Message may be sent without an approval prompt.
    - - App absent from channel
      - Post attempted
      - Delivery fails despite registration.
    - - Connection removed
      - Future request
      - Future access changes; existing posts remain externally managed.
    controls:
      $markdown: field-0007
    observable_output: Actual channel post and recorded action/delivery result.
    undocumented:
      $markdown: field-0008
    test:
    - Use a restricted test channel containing the installed app.
    - Verify destination and content without expecting a confirmation prompt.
    - $markdown: field-0009
    claims:
    - source: FS409
      section: Integration and connection model; Capabilities
      assertion: Connections are per-instance/channel and one-way; membership is required.
    - source: FS407
      section: Slack messages
      assertion: Posting does not prompt for approval even in interactive invocation.
---

<!-- block: b-af12960bcfec5f2f8da5 -->
## process

<!-- block: b-939926fa4905589282ec -->
<!-- field: field-0001 -->
Post to the configured channel without a per-message approval prompt.
<!-- /field -->

<!-- block: b-8406fbcaf9e95eb5b967 -->
## on failure

<!-- block: b-e9a4c18218a451149f11 -->
<!-- field: field-0002 -->
Keep analysis completion separate from delivery failure; posting does not establish channel-reading capability.
<!-- /field -->

<!-- block: b-2637a4df1fd8594ba46c -->
## review / inputs

<!-- block: b-57d5ef820681507a85ec -->
<!-- field: field-0003 -->
Account workspace registration, instance channel connection, app membership and reviewed message/artifact.
<!-- /field -->

<!-- block: b-a44b4fe40fd75bc38999 -->
## review / narrative / 0

<!-- block: b-ad64ac8479825a638822 -->
<!-- field: field-0004 -->
Slack publication is one-way in the documented preview. Registration authorizes the workspace; the instance connection selects a channel; channel membership permits delivery. Posting does not establish channel reading, command handling or thread interaction.
<!-- /field -->

<!-- block: b-b20aafc5813a5167ae12 -->
## review / narrative / 1

<!-- block: b-f0fd9edfdf4c509cb742 -->
<!-- field: field-0005 -->
There is no per-message approval prompt, including interactive requests. Review the intended channel and content before invocation, then inspect actual delivery. Disconnecting the channel is not a mechanism for deleting previously posted messages.
<!-- /field -->

<!-- block: b-331c7c1874be5ab6934c -->
## review / configuration / 1 / 1

<!-- block: b-4001aea144e25143974b -->
<!-- field: field-0006 -->
Add the app to the channel; instance → Add connection → Slack; select integration and channel ID.
<!-- /field -->

<!-- block: b-c217e1c4a82350bfb80a -->
## review / controls

<!-- block: b-935039b5750c563490f5 -->
<!-- field: field-0007 -->
Review audience before sending. The integration does not provide general edit/delete, channel administration or conversation reading.
<!-- /field -->

<!-- block: b-7927d3e0f8ac585da484 -->
## review / undocumented

<!-- block: b-2730412d66525cf9b500 -->
<!-- field: field-0008 -->
Deduplicated retries, universal rollback and guaranteed post deletion are not provided by the documented interface.
<!-- /field -->

<!-- block: b-a6647d44f1225521a356 -->
## review / test / 2

<!-- block: b-19cdebd5cb625ed5af3f -->
<!-- field: field-0009 -->
Remove app membership for an authorized negative test and distinguish delivery failure from task failure.
<!-- /field -->
