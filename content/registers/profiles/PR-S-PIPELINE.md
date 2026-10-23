---
id: record-profiles-PR-S-PIPELINE
kind: record
collection: profiles
product: ''
title: Pipeline assessment and delivery decision
order: 6
frozen: true
data:
  id: PR-S-PIPELINE
  title: Pipeline assessment and delivery decision
  platforms:
  - security
  mechanisms:
  - MX-S-PIPELINE
  - MX-S-RUN
  parameters:
  - - Assessment
    - Saved authorized configuration
    - Actual assessment configuration identifier
  - - Pipeline identity
    - Scoped invocation access
    - Approved CI identity
  - - Gate policy
    - Errors, incomplete results and accepted findings
    - Block or escalate; never a missing-result pass
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

<!-- block: b-55b14246d3cc5656b932 -->
## setup / 0

<!-- block: b-4e244cb963db5b988030 -->
<!-- field: field-0001 -->
Verify eligibility and bind the pipeline to the saved assessment.
<!-- /field -->

<!-- block: b-f232cd1dc0ac56fca309 -->
## setup / 1

<!-- block: b-ab17e30d460a5eb0834b -->
<!-- field: field-0002 -->
Invoke and observe the server-side job, retaining revision and run identity.
<!-- /field -->

<!-- block: b-9498ea88272858808137 -->
## setup / 2

<!-- block: b-50574550371d57339729 -->
<!-- field: field-0003 -->
Apply the team gate only after interpreting actual scope and coverage.
<!-- /field -->

<!-- block: b-14cfd63ec63852d78a82 -->
## tests / 0

<!-- block: b-f04334cb84635ba5b346 -->
<!-- field: field-0004 -->
Invocation failure is not successful assessment.
<!-- /field -->

<!-- block: b-13d40efe80c25e0dae5f -->
## tests / 1

<!-- block: b-df658286257a5fa0bc65 -->
<!-- field: field-0005 -->
An observation timeout does not imply that the underlying job stopped.
<!-- /field -->

<!-- block: b-9b9e70ced48159409566 -->
## tests / 2

<!-- block: b-9917861d998d5e02bd1a -->
<!-- field: field-0006 -->
A new deployed revision requires matching assessment evidence.
<!-- /field -->

<!-- block: b-48215fc393ae53798280 -->
## stop behavior

<!-- block: b-979490d3639e54bda5fa -->
<!-- field: field-0007 -->
Stop the actual assessment using supported controls; stopping the pipeline runner is not assumed to cancel it.
<!-- /field -->
