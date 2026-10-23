---
id: record-profiles-PR-D-PROCEDURE
kind: record
collection: profiles
product: ''
title: Reviewed runbook-skill configuration
order: 13
frozen: true
data:
  id: PR-D-PROCEDURE
  title: Reviewed runbook-skill configuration
  platforms:
  - devops
  mechanisms:
  - MX-D-SKILL
  - MX-D-INSTRUCTIONS
  parameters:
  - - Procedure source
    - One approved SOP after conflict resolution
    - Reviewed source in Git
  - - Applicability
    - Symptoms, services and agent scope
    - Specific operational situation
  - - Tool references
    - Real tool names used by the procedure
    - Selected supported operations
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

<!-- block: b-f2b33ba22a7b521bb0f0 -->
## setup / 0

<!-- block: b-9bd2fdfd0c415e87a9fc -->
<!-- field: field-0001 -->
Reconcile conflicting SOPs and obtain an accountable review.
<!-- /field -->

<!-- block: b-02d67bc75cb950b383ae -->
## setup / 1

<!-- block: b-d3f89ca1b42a5852bc48 -->
<!-- field: field-0002 -->
Package the approved procedure as a skill with its applicability description.
<!-- /field -->

<!-- block: b-485b973aeb26503fb215 -->
## setup / 2

<!-- block: b-26d3de3781df5f8fb49c -->
<!-- field: field-0003 -->
Keep broadly applicable reporting conventions in standing instructions only where appropriate.
<!-- /field -->

<!-- block: b-58e29d8e305c5a4e80fa -->
## setup / 3

<!-- block: b-aeecdc5042e15b0980ad -->
<!-- field: field-0004 -->
Test a matching and a nonmatching request using non-sensitive evidence.
<!-- /field -->

<!-- block: b-136b1e559203554b8cba -->
## tests / 0

<!-- block: b-e2ab662f988253a1b4a0 -->
<!-- field: field-0005 -->
Irrelevant tasks do not require the skill.
<!-- /field -->

<!-- block: b-fee6456729f35efea51c -->
## tests / 1

<!-- block: b-6bcc7f03e3f05ed1bea4 -->
<!-- field: field-0006 -->
Required tools exist and unsupported steps stop explicitly.
<!-- /field -->

<!-- block: b-4e46b6aab8c85a01bb25 -->
## tests / 2

<!-- block: b-6b00b687fac8534caf6f -->
<!-- field: field-0007 -->
Changes to standing instructions are tested in a new applicable session.
<!-- /field -->

<!-- block: b-79963b8d84c2513dbdf5 -->
## stop behavior

<!-- block: b-56080784783d5b14b3ee -->
<!-- field: field-0008 -->
Deactivate or revise the relevant procedural configuration using the supported controls. Changing a skill does not undo past actions or grant new access.
<!-- /field -->
