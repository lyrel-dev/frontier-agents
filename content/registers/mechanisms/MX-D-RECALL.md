---
id: record-mechanisms-MX-D-RECALL
kind: record
collection: mechanisms
product: devops
title: Selective incident-context retrieval
order: 2
frozen: true
data:
  id: MX-D-RECALL
  platform: devops
  title: Selective incident-context retrieval
  features:
  - FT-D-MEMORY
  sections:
  - D-M01
  - D-M07
  trigger: A task identifies relevant available store descriptions
  state: Active stores, entry descriptions, versions and applicable attachments
  process:
    $markdown: field-0001
  effect: Context read
  verification:
    $markdown: field-0002
  on_failure:
    $markdown: field-0003
  review:
    primary_section: D-M01
    kind: Knowledge-retrieval mechanism
    inputs:
      $markdown: field-0004
    narrative:
    - $markdown: field-0005
    - $markdown: field-0006
    configuration:
    - - Content
      - Knowledge → Memories → select store → View entry; inspect description and version.
      - Stored informational context
    - - Availability
      - Inspect store and entry activation; inspect custom-agent attachments where applicable.
      - Access to retained material
    - - Description maintenance
      - Refine the store/entry description and retest a relevant request.
      - Retrieval metadata, not permissions
    lifecycle:
    - - Entry retained
      - Deactivate entry or store
      - Content remains but active retrieval is suppressed.
    - - Entry edited
      - Save updated content
      - A new immutable version is created.
    - - Custom store deleted in console
      - Confirm deletion
      - Store contents are removed; the documented deletion is not reversible.
    controls:
      $markdown: field-0007
    observable_output:
      $markdown: field-0008
    undocumented:
      $markdown: field-0009
    test:
    - $markdown: field-0010
    - Record existence, observable retrieval and supported conclusion separately.
    - $markdown: field-0011
    claims:
    - source: DS402
      section: How memories work; Activating and deactivating; Deleting a memory store
      assertion:
        $markdown: field-0012
    diagram: mechanism-devops-retrieval
---

<!-- block: b-a09e4047257e5ac8b9b1 -->
## process

<!-- block: b-36bf8df8281556a78280 -->
<!-- field: field-0001 -->
Select a relevant store, inspect its entries and read the content needed by the current task.
<!-- /field -->

<!-- block: b-018303189cbd5543b3a1 -->
## verification

<!-- block: b-9519748f226c5997887f -->
<!-- field: field-0002 -->
Distinguish entry existence, observable retrieval and correctness against current evidence.
<!-- /field -->

<!-- block: b-37e57bc267a354aba909 -->
## on failure

<!-- block: b-a18a6f3a813b5642a783 -->
<!-- field: field-0003 -->
Continue without history when current evidence suffices. Do not infer retrieval merely from answer wording.
<!-- /field -->

<!-- block: b-a1401b4ca4125127a899 -->
## review / inputs

<!-- block: b-0e28a7696ae954eba62c -->
<!-- field: field-0004 -->
Current task; available store and entry descriptions; active memory content; applicable custom-agent store attachment.
<!-- /field -->

<!-- block: b-41881f036c8855f2bb83 -->
## review / narrative / 0

<!-- block: b-8f70e78ef27e59588f2d -->
<!-- field: field-0005 -->
Retrieval is a selection process, not automatic loading of all history. The agent first sees available store descriptions, then inspects a relevant store and selects entries before reading their content. A useful description exposes the subject and conditions under which an entry matters. A relevant fact hidden behind an unrelated description may never be read.
<!-- /field -->

<!-- block: b-57f917bcc9525ac88746 -->
## review / narrative / 1

<!-- block: b-e25b71d34a115db28d29 -->
<!-- field: field-0006 -->
Operationally, distinguish content production, availability to this execution, selection and diagnostic influence. A previous cause is contextual evidence for a new incident. Current measurements can contradict it. Viewing an old version is also different from restoring a deleted store; the current guide does not establish a general backup or undelete service.
<!-- /field -->

<!-- block: b-5de90bd91b185380a023 -->
## review / controls

<!-- block: b-2a26634abce15aa49a77 -->
<!-- field: field-0007 -->
Keep raw incident evidence in its source system. Store access, relevance and answer correctness are separate; memory is not a same-investigation raw-tool cache.
<!-- /field -->

<!-- block: b-3dd10ad8ab81512e9587 -->
## review / observable output

<!-- block: b-df94fc893fce540bbf19 -->
<!-- field: field-0008 -->
Entry content/version and, where exposed, a memory read in execution evidence. Output similarity alone does not establish retrieval.
<!-- /field -->

<!-- block: b-46a4fff11e8e5b11897c -->
## review / undocumented

<!-- block: b-c9a771ac411056d0ad34 -->
<!-- field: field-0009 -->
Embedding model, ranking thresholds, hidden selection policy and model-weight training are not documented by this mechanism.
<!-- /field -->

<!-- block: b-992dfe07e3ea538b8699 -->
## review / test / 0

<!-- block: b-b49285b166805b50ab64 -->
<!-- field: field-0010 -->
Prepare a harmless known fact and a current observation that contradicts a historical cause.
<!-- /field -->

<!-- block: b-19f1af3ee8035428834e -->
## review / test / 2

<!-- block: b-762e8ff57abd57f5b7e8 -->
<!-- field: field-0011 -->
Deactivate the entry or remove the applicable attachment and verify that unsupported historical claims are not asserted.
<!-- /field -->

<!-- block: b-90a2a2feea085afc8014 -->
## review / claims / 0 / assertion

<!-- block: b-55f75f96bfdc5f9888c7 -->
<!-- field: field-0012 -->
Description-led retrieval, immutable versions and activation differ from irreversible custom-store deletion.
<!-- /field -->
