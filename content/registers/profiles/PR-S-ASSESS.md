---
id: record-profiles-PR-S-ASSESS
kind: record
collection: profiles
product: ''
title: Running-application assessment configuration
order: 4
frozen: true
data:
  id: PR-S-ASSESS
  title: Running-application assessment configuration
  platforms:
  - security
  mechanisms:
  - MX-S-CONTEXT
  - MX-S-ACCESS
  - MX-S-AUTH
  - MX-S-LOGIN
  - MX-S-RUN
  - MX-S-REVALIDATE
  parameters:
  - - Target
    - Authorized application and deployed revision
    - Staging application / demo-r2
  - - Network
    - Public or private route and explicit exclusions
    - Separate attack targets from login support paths
  - - Identity
    - Representative test roles and credential strategy
    - Test customer role; no production credential
  - - Run limits
    - Configured work limits and responsible owner
    - Owner-approved limit, not assumed wall-clock duration
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

<!-- block: b-a0931de45ae455bb851b -->
## setup / 0

<!-- block: b-4873cc5c37c05f3e9d4a -->
<!-- field: field-0001 -->
Review the saved scope before starting execution.
<!-- /field -->

<!-- block: b-29d689dd8c755877b597 -->
## setup / 1

<!-- block: b-e16963373a3350278f57 -->
<!-- field: field-0002 -->
Test target reachability and actual application identity.
<!-- /field -->

<!-- block: b-3c95a32f9c035b71b56d -->
## setup / 2

<!-- block: b-f9f42bc57cee51929348 -->
<!-- field: field-0003 -->
Start a separate run and retain excluded or incomplete paths.
<!-- /field -->

<!-- block: b-a3a8cbc5b62257aeb9a0 -->
## setup / 3

<!-- block: b-240481a04fff54299333 -->
<!-- field: field-0004 -->
For revalidation, confirm the deployed repair and select original findings rather than run broad discovery.
<!-- /field -->

<!-- block: b-4365a7a0bc39515b8a9d -->
## tests / 0

<!-- block: b-1f54eb4ab82f51d8888d -->
<!-- field: field-0005 -->
Failed authentication leaves protected paths unassessed.
<!-- /field -->

<!-- block: b-4e9772489b595060b537 -->
## tests / 1

<!-- block: b-3d71fa614dfc5337a1e4 -->
<!-- field: field-0006 -->
Each run identifies the actual target revision and roles.
<!-- /field -->

<!-- block: b-0946c8a8607b58608243 -->
## tests / 2

<!-- block: b-d61f31e754995253b1d7 -->
<!-- field: field-0007 -->
Revalidation retains the original finding and separate job.
<!-- /field -->

<!-- block: b-3ff2a98179da5cc9b109 -->
## stop behavior

<!-- block: b-38a7db4f952e5717865d -->
<!-- field: field-0008 -->
Stop unexpected effects. Control future schedules separately from current jobs, findings and external tickets.
<!-- /field -->
