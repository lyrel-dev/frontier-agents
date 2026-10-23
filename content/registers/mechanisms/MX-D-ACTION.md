---
id: record-mechanisms-MX-D-ACTION
kind: record
collection: mechanisms
product: devops
title: Operation-specific directed authorization
order: 11
frozen: true
data:
  id: MX-D-ACTION
  platform: devops
  title: Operation-specific directed authorization
  features:
  - FT-D-ACTIONS
  sections:
  - D-M06
  trigger: Operator requests an eligible state-changing operation
  state: Opt-in, role, category and approval
  process:
    $markdown: field-0001
  effect: Resource or external-tool mutation
  verification: Inspect exact approval, attribution and resulting resource state.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-M06
    kind: Effect-specific authorization mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Enable
      - $markdown: field-0006
      - Primary opt-in
    - - Authorize account
      - $markdown: field-0007
      - Permission ceiling
    - - Review exact action
      - Inspect target and parameters in Chat approval; reject or narrow as needed.
      - Specific execution grant
    lifecycle:
    - - Disabled
      - Enable and configure eligible access
      - Requests can reach the approval path.
    - - Proposal awaiting decision
      - Approve exact operation
      - Scoped execution is permitted.
    - - Approval granted
      - Different target or operation requested
      - Previous approval is not reusable.
    - - Action executed
      - Inspect resource and service signals
      - Action success and recovery are separate observations.
    controls:
      $markdown: field-0008
    observable_output: Approval details, execution attribution and independently inspected resulting state.
    undocumented:
      $markdown: field-0009
    test:
    - Use an eligible reversible staging operation under narrow permissions.
    - Match approval, attribution and target state.
    - Request a different target or denied operation; it must not inherit the earlier approval.
    claims:
    - source: DS411
      section: Enabling; Registering elevated role; Categorizing tools; Approving directed actions
      assertion:
        $markdown: field-0010
---

<!-- block: b-fb34dc9b18b75cb0a4eb -->
## process

<!-- block: b-b3538f535be756e8ba5a -->
<!-- field: field-0001 -->
Execute the specific approved operation through its configured authorization path.
<!-- /field -->

<!-- block: b-f0b0a0eca8c85d8094ac -->
## on failure

<!-- block: b-849ca140c9ea5b0f8da0 -->
<!-- field: field-0002 -->
Stop on a failed authorization gate; use the normal approved engineering process rather than bypassing it.
<!-- /field -->

<!-- block: b-b14b68a36c745bbca19f -->
## review / inputs

<!-- block: b-a2bf443d6a2a5279be48 -->
<!-- field: field-0003 -->
Eligible exact operation and resource; Agent Space opt-in; target-account elevated role or selected classified tool; operator approval.
<!-- /field -->

<!-- block: b-702ac6e77ccb5762a718 -->
## review / narrative / 0

<!-- block: b-614a90584f02560c9584 -->
<!-- field: field-0004 -->
The requested effect passes several gates. Enabling directed actions opens the capability; the target role supplies a permission ceiling; the approval constrains the specific operation and resource. For AWS calls, the service uses scoped credentials and records attribution. None of these steps is replaced by a mitigation recommendation.
<!-- /field -->

<!-- block: b-e58e2e24b6ed5b87a577 -->
## review / narrative / 1

<!-- block: b-1bf66b4e44f75b839579 -->
<!-- field: field-0005 -->
External-tool classification is part of the control boundary. A tool marked read-only but implemented as mutating can defeat the intended approval path. Review classification against its real effects and permissions rather than its display name.
<!-- /field -->

<!-- block: b-4f4329455dda5af68c67 -->
## review / configuration / 0 / 1

<!-- block: b-57f6e20aeb78555c8ab6 -->
<!-- field: field-0006 -->
Agent Space settings: enable directed actions; preserve the full preferences map when updating through the API.
<!-- /field -->

<!-- block: b-c1e9bf4fbee05149b4bb -->
## review / configuration / 1 / 1

<!-- block: b-378e0e95984a5294baf9 -->
<!-- field: field-0007 -->
Register the elevated role with documented trust including source-identity/session tagging support.
<!-- /field -->

<!-- block: b-d0c18724256c55ae8918 -->
## review / controls

<!-- block: b-047a05607b155ab3bf8a -->
<!-- field: field-0008 -->
API preference replacement can reset omitted settings. IAM and service guardrails still apply after approval; tool effects require correct classification.
<!-- /field -->

<!-- block: b-4d8e7450942e518d9501 -->
## review / undocumented

<!-- block: b-c3509e9d65a1587087fc -->
<!-- field: field-0009 -->
No universal transactional rollback is documented; approved calls can have effects that outlive the conversation.
<!-- /field -->

<!-- block: b-8d7dad54c6845c7bb963 -->
## review / claims / 0 / assertion

<!-- block: b-bbb8879f92da5cac9661 -->
<!-- field: field-0010 -->
Independent opt-ins, operation-specific approval, preference replacement and classification govern mutation.
<!-- /field -->
