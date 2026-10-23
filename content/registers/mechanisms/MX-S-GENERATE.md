---
id: record-mechanisms-MX-S-GENERATE
kind: record
collection: mechanisms
product: security
title: Requirement-pack regeneration
order: 23
frozen: true
data:
  id: MX-S-GENERATE
  platform: security
  title: Requirement-pack regeneration
  features:
  - FT-S-REQUIREMENTS
  sections:
  - S-M04
  trigger: Policy documents are submitted for requirement generation
  state: Existing custom pack and generated replacement
  process:
    $markdown: field-0001
  effect: Configuration replacement
  verification: Compare with approved policy and prior manually added requirements.
  on_failure: Do not enable an unreviewed replacement; keep authoritative source in Git.
  review:
    primary_section: S-M04
    kind: Requirement-replacement mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Select
      - Security requirements → Custom packs → choose/create the intended pack.
      - Replacement target
    - - Generate
      - $markdown: field-0005
      - Generation operation
    - - Accept
      - Review/edit resulting requirements before enabling the pack for later assessments.
      - Team approval of generated criteria
    lifecycle:
    - - Pack has requirements
      - Regenerate from new documents
      - Existing requirements, including manual ones, are replaced.
    - - Generation in progress
      - Attempt another upload
      - The documented workflow blocks another upload until processing finishes.
    - - Generated criteria
      - Review and enable
      - New eligible reviews use the accepted configuration.
    controls:
      $markdown: field-0006
    observable_output: Generated requirement definitions and prospective pack state.
    undocumented: Automatic merge of old/manual rules and transactional rollback are not documented.
    test:
    - Use a disposable pack containing one manual rule and an approved small policy fixture.
    - Compare resulting criteria with source and prior contents.
    - Confirm replacement behavior without using a production policy pack.
    claims:
    - source: SS409
      section: Generate requirements; Replace requirements with a new upload
      assertion: Generation replaces existing pack contents and requires review before use.
---

<!-- block: b-9e35a588dbf2579ebd72 -->
## process

<!-- block: b-4ac038ea1acd583faa08 -->
<!-- field: field-0001 -->
Replace pack contents from the selected policy documents for subsequent review.
<!-- /field -->

<!-- block: b-83e16c52cd6d547abc9b -->
## review / inputs

<!-- block: b-7b03614e75c1545ea5d9 -->
<!-- field: field-0002 -->
Documents submitted for a custom requirement pack. The team reviews the policy source and replacement before enabling the pack.
<!-- /field -->

<!-- block: b-bfc70c9e2cf95cccb03b -->
## review / narrative / 0

<!-- block: b-49cf23ba3499573f852d -->
<!-- field: field-0003 -->
Generation reads policy documents and constructs structured requirements. Running it again for an existing pack replaces the requirements; it is not an append operation. A successful generation therefore establishes a proposed replacement, not approval of every generated rule.
<!-- /field -->

<!-- block: b-ce90d3b0773d5aab9527 -->
## review / narrative / 1

<!-- block: b-38c3bde6958e54139310 -->
<!-- field: field-0004 -->
Reconcile overlapping policies before submission. Review applicability and technical criteria afterward, and explicitly compare the replacement with any manual entries that existed before the upload.
<!-- /field -->

<!-- block: b-e0153fdf5ba85f1083a4 -->
## review / configuration / 1 / 1

<!-- block: b-792c789cbde958c1b0ca -->
<!-- field: field-0005 -->
Upload supported documents and choose Generate requirements; acknowledge replacement when applicable.
<!-- /field -->

<!-- block: b-367d25c3fa0557f1b76b -->
## review / controls

<!-- block: b-9223eb9473da5eef86e5 -->
<!-- field: field-0006 -->
Keep authoritative policy and reviewed configuration in Git; do not treat a generated pack as the only source of policy.
<!-- /field -->
