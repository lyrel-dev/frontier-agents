---
id: record-profiles-PR-F-PUBLICATION
kind: record
collection: profiles
product: ''
title: FinOps destination and authorization configuration
order: 9
frozen: true
data:
  id: PR-F-PUBLICATION
  title: FinOps destination and authorization configuration
  platforms:
  - finops
  mechanisms:
  - MX-F-JIRA
  - MX-F-SLACK
  parameters:
  - - Destination
    - Configured Jira project or Slack channel
    - Reviewed internal test destination
  - - Invocation
    - Interactive, on-demand, scheduled or event-driven
    - Specify the path explicitly
  - - Content scope
    - Approved data and audience
    - Non-sensitive summary and evidence references
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

<!-- block: b-6a2eeafd12da5ff4be80 -->
## setup / 0

<!-- block: b-dfca8f0b627c51399be3 -->
<!-- field: field-0001 -->
Register the provider and bind the agent connection to its destination.
<!-- /field -->

<!-- block: b-5d793326c8285aa98874 -->
## setup / 1

<!-- block: b-61f7b4ae816253a3837f -->
<!-- field: field-0002 -->
Review audience and message scope before invocation.
<!-- /field -->

<!-- block: b-d705122bea2f52cabcf0 -->
## setup / 2

<!-- block: b-5deb82e635545d798c28 -->
<!-- field: field-0003 -->
For Jira, use invocation-specific approval; for Slack, do not expect a confirmation prompt.
<!-- /field -->

<!-- block: b-b90cb503554e5c9bb18c -->
## setup / 3

<!-- block: b-2ce4ae4b58455ac0902a -->
<!-- field: field-0004 -->
Inspect actual destination and task history.
<!-- /field -->

<!-- block: b-7fdb5eb0fee75ce78711 -->
## tests / 0

<!-- block: b-c3eaff7a0b8d5c5c967b -->
<!-- field: field-0005 -->
Interactive or on-demand Jira approval is observed where applicable.
<!-- /field -->

<!-- block: b-ba817a611fb3574d9b1e -->
## tests / 1

<!-- block: b-93d9579d53a45bf2a2e4 -->
<!-- field: field-0006 -->
Automated Jira authorization is reviewed at setup.
<!-- /field -->

<!-- block: b-90144ed22539529fb065 -->
## tests / 2

<!-- block: b-34894a8e46675d5d83c0 -->
<!-- field: field-0007 -->
Slack is treated as direct publication, not as approval-protected.
<!-- /field -->

<!-- block: b-d820d86b5c1d51d3afb5 -->
## stop behavior

<!-- block: b-a3ac131cb71e5e57bb03 -->
<!-- field: field-0008 -->
Disable future publication or its automation. Disconnecting a destination does not delete already published records.
<!-- /field -->
