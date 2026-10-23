---
id: record-mechanisms-MX-F-COMPACT
kind: record
collection: mechanisms
product: finops
title: Conversation compaction
order: 32
frozen: true
data:
  id: MX-F-COMPACT
  platform: finops
  title: Conversation compaction
  features:
  - FT-F-CONTEXT
  sections:
  - F-M04
  trigger: Conversation approaches its context limit
  state: Summary of older material and recent full messages
  process:
    $markdown: field-0001
  effect: Session context change
  verification: Restate the current query basis and unresolved questions.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: F-M04
    kind: Session-context compaction mechanism
    inputs: Growing conversation approaching the model context window.
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Enablement
      - $markdown: field-0005
      - Service-managed context handling
    - - Operational practice
      - Restate critical query constraints and reference authoritative outputs.
      - Team verification procedure
    lifecycle:
    - - Context grows
      - Approaches context limit
      - Older portions summarized.
    - - Compacted context
      - Conversation continues
      - Recent messages and summary guide subsequent work.
    - - Detail missing
      - Reconstruct from authoritative record
      - Do not infer verbatim recall from a fluent answer.
    controls:
      $markdown: field-0006
    observable_output:
      $markdown: field-0007
    undocumented: Thresholds, summary-selection rules and lossless retention are not documented.
    test:
    - Use a non-sensitive long conversation with a recorded query contract.
    - Check whether later analysis retains the period and metric.
    - $markdown: field-0008
    claims:
    - source: FS402
      section: Long conversation handling
      assertion: Automatic summarization replaces older context while recent messages remain in full.
---

<!-- block: b-77452f6439925186979c -->
## process

<!-- block: b-82cb44083cd85787a19f -->
<!-- field: field-0001 -->
Summarize older context while continuing the conversation.
<!-- /field -->

<!-- block: b-3fb1c6feb01251b4adb0 -->
## on failure

<!-- block: b-bce237e51a3f58748c0e -->
<!-- field: field-0002 -->
Reconstruct critical constraints from authoritative records instead of assuming verbatim recall.
<!-- /field -->

<!-- block: b-bd8fb2eb7c2555e28a08 -->
## review / narrative / 0

<!-- block: b-bebce4bff934557293b5 -->
<!-- field: field-0003 -->
Compaction changes the context supplied to continued conversation. Older material is summarized while recent messages remain in full. It preserves a working representation of key decisions, not a verbatim copy of every earlier turn.
<!-- /field -->

<!-- block: b-45be90c4bcaa5357a595 -->
## review / narrative / 1

<!-- block: b-b4298ab31e23581394e2 -->
<!-- field: field-0004 -->
Keep a material cost question explicit after a long exchange: period, metric, filters and unresolved assumptions. Restating those choices is an engineering safeguard, not a control that changes the undocumented compaction algorithm.
<!-- /field -->

<!-- block: b-b609bdbc9c5f551cb03d -->
## review / configuration / 0 / 1

<!-- block: b-245a0b6f55805c11a137 -->
<!-- field: field-0005 -->
Automatic; no administrator threshold or manual compaction switch is established by the cited guide.
<!-- /field -->

<!-- block: b-10b643c61173568c892c -->
## review / controls

<!-- block: b-8cbc89a3554859d2a6a5 -->
<!-- field: field-0006 -->
Compaction is not durable preference management or deletion of stored conversation history.
<!-- /field -->

<!-- block: b-6d297ebc80715c09a3af -->
## review / observable output

<!-- block: b-e65956c38a4551b89226 -->
<!-- field: field-0007 -->
Continued conversation and the constraints it actually applies; a direct compaction event may not be exposed.
<!-- /field -->

<!-- block: b-93e5631a4dbf5aac9c9e -->
## review / test / 2

<!-- block: b-131e0247aec85541a615 -->
<!-- field: field-0008 -->
Where detail is missing, restore it explicitly and label compaction itself unobserved if no service signal exists.
<!-- /field -->
