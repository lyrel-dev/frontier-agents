---
id: record-profiles-PR-D-INCIDENT
kind: record
collection: profiles
product: ''
title: Incident and prevention configuration
order: 0
frozen: true
data:
  id: PR-D-INCIDENT
  title: Incident and prevention configuration
  platforms:
  - devops
  mechanisms:
  - MX-D-READ
  - MX-D-TRIAGE
  - MX-D-INVESTIGATE
  - MX-D-RECALL
  - MX-D-FEEDBACK
  - MX-D-PREVENT
  parameters:
  - - Operation
    - Investigation, routing, feedback or prevention evaluation
    - Select the operation matching the objective
  - - Agent Space
    - Authorized space and account scope
    - Approved staging space
  - - Incident subject
    - Service identity and actual UTC observation interval
    - Checkout service and supplied incident window
  - - Historical context
    - Relevant active monitor or service context
    - Optional; never a substitute for current evidence
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

<!-- block: b-b6f6a8a70c1a58f19cad -->
## setup / 0

<!-- block: b-dca1e94ac6cb5a4991d2 -->
<!-- field: field-0001 -->
Verify operator access independently from resource and tool access.
<!-- /field -->

<!-- block: b-2a26f0855c285cd2a863 -->
## setup / 1

<!-- block: b-4e31f304d7235e75b5dc -->
<!-- field: field-0002 -->
For incident work, start from a signal or scoped manual investigation. For prevention work, inspect a manual or scheduled evaluation over existing investigation evidence.
<!-- /field -->

<!-- block: b-1a9d19d0a47755e3a9f3 -->
## setup / 2

<!-- block: b-edd940c2e8735108a434 -->
<!-- field: field-0003 -->
Inspect triage, current evidence and any observable historical-context retrieval separately.
<!-- /field -->

<!-- block: b-81965222f9f2537fafe0 -->
## tests / 0

<!-- block: b-61f81da8c0fe5bc1ac1f -->
<!-- field: field-0004 -->
Current observations contradict a prior cause: the conclusion must follow current evidence.
<!-- /field -->

<!-- block: b-220f9e23a20754698db4 -->
## tests / 1

<!-- block: b-81b95cc1eb46578a81e8 -->
<!-- field: field-0005 -->
A missing source produces an explicit evidence gap.
<!-- /field -->

<!-- block: b-a832d971a8e451c08838 -->
## tests / 2

<!-- block: b-77fca903581558b1a702 -->
<!-- field: field-0006 -->
Correcting routing changes linkage, not production resource state.
<!-- /field -->

<!-- block: b-8f36748b73ca5ad2914f -->
## stop behavior

<!-- block: b-02b71853b5c75576b703 -->
<!-- field: field-0007 -->
Use supported investigation controls. Steering and feedback do not grant mutation authority.
<!-- /field -->
