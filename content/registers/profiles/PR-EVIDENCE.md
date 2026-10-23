---
id: record-profiles-PR-EVIDENCE
kind: record
collection: profiles
product: ''
title: Cross-tool evidence reconciliation
order: 11
frozen: true
data:
  id: PR-EVIDENCE
  title: Cross-tool evidence reconciliation
  platforms:
  - devops
  mechanisms:
  - MX-D-READ
  - MX-D-TOPOLOGY
  parameters:
  - - Identity mapping
    - Service, resource and revision relationships across tools
    - Reviewed application-to-deployment mapping
  - - Observation window
    - Common UTC period
    - Explicit incident interval
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

<!-- block: b-19a5fea48e8a5e73b6fc -->
## setup / 0

<!-- block: b-06aaef6b45275bcaaea3 -->
<!-- field: field-0001 -->
Read source identifiers instead of matching only titles.
<!-- /field -->

<!-- block: b-42633fa58ef45ebab038 -->
## setup / 1

<!-- block: b-95000a7ee38853b885a5 -->
<!-- field: field-0002 -->
Join observations using reviewed service and revision mappings.
<!-- /field -->

<!-- block: b-ac73814a84e250899412 -->
## setup / 2

<!-- block: b-a28af57c0763524eb72b -->
<!-- field: field-0003 -->
Retain unmatched records and contradictory evidence.
<!-- /field -->

<!-- block: b-aceec6091d7c5d2eb18c -->
## tests / 0

<!-- block: b-f8eb94705b195ad58cb4 -->
<!-- field: field-0004 -->
Similar timestamps alone do not establish causality.
<!-- /field -->

<!-- block: b-6c1510855d4453d49d09 -->
## tests / 1

<!-- block: b-f7c9a9ffce3456b18e1d -->
<!-- field: field-0005 -->
An observation for the wrong account or revision is rejected.
<!-- /field -->

<!-- block: b-134bc024f73d5ff7929c -->
## stop behavior

<!-- block: b-555f3b01cbaa52b8a938 -->
<!-- field: field-0006 -->
Continue only with supported relationships and assign gaps to an owner. This is a team procedure, not a universal native correlation feature.
<!-- /field -->
