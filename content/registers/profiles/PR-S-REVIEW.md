---
id: record-profiles-PR-S-REVIEW
kind: record
collection: profiles
product: ''
title: Source, design and finding-review configuration
order: 5
frozen: true
data:
  id: PR-S-REVIEW
  title: Source, design and finding-review configuration
  platforms:
  - security
  mechanisms:
  - MX-S-CONTEXT
  - MX-S-CODE
  - MX-S-DESIGN
  - MX-S-THREAT
  - MX-S-CRITERIA
  - MX-S-GENERATE
  - MX-S-FINDING
  - MX-S-FIX
  - MX-S-JIRA
  parameters:
  - - Assessment mode
    - One supported assessment with its own resource lifecycle
    - Code baseline, code change, design or threat model
  - - Evidence revision
    - Source or design matching the subject
    - Immutable revision identifier
  - - Criteria
    - Reviewed applicable requirements
    - Selected enabled pack
  - - Write features
    - Optional comment, repair proposal or ticket
    - Disabled until provider and audience review
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

<!-- block: b-7ae602106d70519b9807 -->
## setup / 0

<!-- block: b-e691eacbd1b351bcb992 -->
<!-- field: field-0001 -->
Choose the actual mode rather than assume a shared configuration schema.
<!-- /field -->

<!-- block: b-8100938aa26a5a41abbc -->
## setup / 1

<!-- block: b-4f5a794ccedf560abfb5 -->
<!-- field: field-0002 -->
Connect matching evidence and enable the intended review criteria.
<!-- /field -->

<!-- block: b-7adcc430c06c5ce39e63 -->
## setup / 2

<!-- block: b-801fe81299ec5d869e21 -->
<!-- field: field-0003 -->
Inspect preflight and completed results separately.
<!-- /field -->

<!-- block: b-049b187a1bab5775b560 -->
## setup / 3

<!-- block: b-cbae68b7cf2c565eb3b8 -->
<!-- field: field-0004 -->
Review repair proposals through ordinary tests and deployment before revalidation.
<!-- /field -->

<!-- block: b-28edae466b0a5529b012 -->
## tests / 0

<!-- block: b-c9a480d4a14e51c1b8dc -->
<!-- field: field-0005 -->
A new source revision cannot silently reuse stale acceptance.
<!-- /field -->

<!-- block: b-5fbf099ef2805797ad54 -->
## tests / 1

<!-- block: b-9c24bad2843d5d399617 -->
<!-- field: field-0006 -->
A requirement may be inapplicable rather than compliant.
<!-- /field -->

<!-- block: b-14e6fc13a87e55a3a80b -->
## tests / 2

<!-- block: b-d4938a31d31b5991a790 -->
<!-- field: field-0007 -->
Regenerating a pack is reviewed as replacement.
<!-- /field -->

<!-- block: b-6364244b677d5d66a685 -->
## stop behavior

<!-- block: b-08e72154e46d5493bd0d -->
<!-- field: field-0008 -->
Retain unfinished findings. Disable optional writes without discarding their source evidence.
<!-- /field -->
