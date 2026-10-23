---
id: record-profiles-PR-D-QUERY
kind: record
collection: profiles
product: ''
title: Native operational-query configuration
order: 12
frozen: true
data:
  id: PR-D-QUERY
  title: Native operational-query configuration
  platforms:
  - devops
  mechanisms:
  - MX-D-QUERY
  - MX-D-READ
  parameters:
  - - Agent Space
    - Operator and data access for the relevant environment
    - Approved space
  - - Question scope
    - Actual service, UTC interval and dimensions
    - Declared recent observation period
  setup:
  - $markdown: field-0001
  - $markdown: field-0002
  - $markdown: field-0003
  tests:
  - $markdown: field-0004
  - $markdown: field-0005
  stop_behavior:
    $markdown: field-0006
---

<!-- block: b-1531fe3411bb52819ef7 -->
## setup / 0

<!-- block: b-4f8c1578224456abb1ee -->
<!-- field: field-0001 -->
Verify access to the sources needed for this question.
<!-- /field -->

<!-- block: b-658419c62dab5f189eb7 -->
## setup / 1

<!-- block: b-85874d362b35522c8ee4 -->
<!-- field: field-0002 -->
Ask through the built-in query path, stating service and observation scope.
<!-- /field -->

<!-- block: b-43773bf7c50254889bd9 -->
## setup / 2

<!-- block: b-2c65665984275bd1889b -->
<!-- field: field-0003 -->
Inspect returned evidence and reconcile a material observation.
<!-- /field -->

<!-- block: b-8a056e85a324538d8f0f -->
## tests / 0

<!-- block: b-bdff501ec9745ff0a17c -->
<!-- field: field-0004 -->
A missing signal is disclosed rather than interpreted as healthy.
<!-- /field -->

<!-- block: b-fa22d820966f51118c99 -->
## tests / 1

<!-- block: b-a25169c3fdbb54239dde -->
<!-- field: field-0005 -->
The answer uses the requested window and dimensions.
<!-- /field -->

<!-- block: b-1fb2ffa0378551e4b499 -->
## stop behavior

<!-- block: b-5cc92b6a9ec25e3ea7c8 -->
<!-- field: field-0006 -->
End or redirect an unsupported inquiry. No custom-agent schedule or external publication is implied.
<!-- /field -->
