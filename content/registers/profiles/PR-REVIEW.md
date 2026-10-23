---
id: record-profiles-PR-REVIEW
kind: record
collection: profiles
product: ''
title: Team-managed operational review
order: 10
frozen: true
data:
  id: PR-REVIEW
  title: Team-managed operational review
  platforms:
  - devops
  - finops
  - architecture
  mechanisms:
  - MX-D-CUSTOM
  - MX-F-TASK
  parameters:
  - - Profile
    - Reliability, cost-management or combined meeting
    - Reliability review
  - - Inputs
    - Reviewed reports with period and execution identity
    - Health and incident results OR reconciled cost and anomaly results
  - - Decision owners
    - Humans accountable for priorities and closure
    - Service owner and review chair
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

<!-- block: b-77e7f8f8535c57bd919d -->
## setup / 0

<!-- block: b-676c10ee0efc5fca9bcc -->
<!-- field: field-0001 -->
Select reviewed inputs for the chosen profile.
<!-- /field -->

<!-- block: b-29c49c4d7a4e576ea420 -->
## setup / 1

<!-- block: b-a0b99e72bad25c35ab9a -->
<!-- field: field-0002 -->
Preserve source and execution identities in the meeting material.
<!-- /field -->

<!-- block: b-b08553e5b8a65bc89494 -->
## setup / 2

<!-- block: b-e84f4e5a270151b98c01 -->
<!-- field: field-0003 -->
Have owners confirm decisions, progress and acceptance.
<!-- /field -->

<!-- block: b-f8f1cafbcbef5518bb48 -->
## tests / 0

<!-- block: b-7cf475a81451577fb6d4 -->
<!-- field: field-0004 -->
Estimated benefit is not recorded as measured outcome.
<!-- /field -->

<!-- block: b-5f91433281785ff2a459 -->
## tests / 1

<!-- block: b-d5d2670daf8857f69886 -->
<!-- field: field-0005 -->
Unverified work is not marked complete.
<!-- /field -->

<!-- block: b-e3a63b3f54c25198b306 -->
## tests / 2

<!-- block: b-ebfa16473df752098f40 -->
<!-- field: field-0006 -->
A handoff transfers neither credentials nor approval authority.
<!-- /field -->

<!-- block: b-4ecb5d8665b35d11bbe9 -->
## stop behavior

<!-- block: b-40b31768c3965f63abd6 -->
<!-- field: field-0007 -->
Stop disclosure to an inappropriate audience. Each underlying service retains its own execution and retention controls.
<!-- /field -->
