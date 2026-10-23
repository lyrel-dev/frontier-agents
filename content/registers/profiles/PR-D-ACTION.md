---
id: record-profiles-PR-D-ACTION
kind: record
collection: profiles
product: ''
title: Directed mitigation configuration
order: 2
frozen: true
data:
  id: PR-D-ACTION
  title: Directed mitigation configuration
  platforms:
  - devops
  mechanisms:
  - MX-D-ACTION
  - MX-D-READ
  parameters:
  - - Target
    - Explicit resource and eligible operation
    - Approved staging resource
  - - Authorization
    - Opt-in, role, tool category and exact approval
    - Record configuration and approval identifiers
  - - Recovery
    - Post-change measurements and rollback conditions
    - Declared latency and error acceptance
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

<!-- block: b-e23c8e0bce8a5921a154 -->
## setup / 0

<!-- block: b-18980da885845a2186de -->
<!-- field: field-0001 -->
Inspect each authorization layer without broadening scope.
<!-- /field -->

<!-- block: b-748226abe9e65609a3ef -->
## setup / 1

<!-- block: b-3e48e8f933fa58baa4f5 -->
<!-- field: field-0002 -->
Review the exact parameters and obtain the documented operator approval.
<!-- /field -->

<!-- block: b-fd88cfeb23b859dbb53d -->
## setup / 2

<!-- block: b-9a7fc763d5b05581a592 -->
<!-- field: field-0003 -->
Compare resulting resource state with service recovery measurements.
<!-- /field -->

<!-- block: b-b121562449815bc098df -->
## tests / 0

<!-- block: b-661d16ecf49350be9224 -->
<!-- field: field-0004 -->
An operation outside the approval remains rejected.
<!-- /field -->

<!-- block: b-63cd6a610cfd5d48a8e9 -->
## tests / 1

<!-- block: b-f751053fe40159e3bdff -->
<!-- field: field-0005 -->
The action record matches the approved operation and target.
<!-- /field -->

<!-- block: b-9ed469b4811358cfa68a -->
## tests / 2

<!-- block: b-c4fd890f80c65f6f9101 -->
<!-- field: field-0006 -->
Unsuccessful recovery follows the declared rollback or escalation decision.
<!-- /field -->

<!-- block: b-cb940e3c31ad5ca581da -->
## stop behavior

<!-- block: b-ad9eb2d63844563ebcd6 -->
<!-- field: field-0007 -->
Stop when a gate fails. An unconditional elevated-role workaround is not part of this recipe.
<!-- /field -->
