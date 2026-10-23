---
id: record-profiles-PR-D-RELEASE
kind: record
collection: profiles
product: ''
title: Release-assurance configuration
order: 3
frozen: true
data:
  id: PR-D-RELEASE
  title: Release-assurance configuration
  platforms:
  - devops
  mechanisms:
  - MX-D-READINESS
  - MX-D-TEST
  parameters:
  - - Mode
    - Source readiness analysis or active application testing
    - Choose the intended output, not interchangeable modes
  - - Revision
    - Candidate source or actually deployed revision
    - demo-r2
  - - Allowed effects
    - Application operations for the active test
    - Disposable data and disabled external notifications
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

<!-- block: b-391ed3a6d7135463b524 -->
## setup / 0

<!-- block: b-b4289d766877525ab8d5 -->
<!-- field: field-0001 -->
Check feature, provider and Region eligibility.
<!-- /field -->

<!-- block: b-9a4ab581c5a651199f12 -->
## setup / 1

<!-- block: b-bac40c778d105e2a8c44 -->
<!-- field: field-0002 -->
Select candidate source for readiness analysis or explicitly authorize the deployed target for testing.
<!-- /field -->

<!-- block: b-386be6096b8b5259b5f8 -->
## setup / 2

<!-- block: b-ab399a843f545133a505 -->
<!-- field: field-0003 -->
Inspect the resulting task and unresolved limitations.
<!-- /field -->

<!-- block: b-42d5189a8ce9566cac60 -->
## tests / 0

<!-- block: b-f4e3ca12e6015a299d99 -->
<!-- field: field-0004 -->
Source review is not represented as deployed-target verification.
<!-- /field -->

<!-- block: b-b3dc399b35f35e6eb91f -->
## tests / 1

<!-- block: b-29b441b538d05633bbfd -->
<!-- field: field-0005 -->
Unexpected application effects stop active testing.
<!-- /field -->

<!-- block: b-52fea72d0e915b64a38f -->
## stop behavior

<!-- block: b-a358f441de995678a13b -->
<!-- field: field-0006 -->
Disable future execution and stop active work through the supported path; preserve incomplete coverage.
<!-- /field -->
