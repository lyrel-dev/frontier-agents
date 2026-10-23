---
id: record-mechanisms-MX-F-FILES
kind: record
collection: mechanisms
product: finops
title: Uploaded reference-file use
order: 30
frozen: true
data:
  id: MX-F-FILES
  platform: finops
  title: Uploaded reference-file use
  features:
  - FT-F-FILES
  sections:
  - F-M02
  trigger: Task needs organizational context
  state: Active uploaded reference
  process:
    $markdown: field-0001
  effect: Context read
  verification: Verify a known mapping and expose unmapped records.
  on_failure: Keep unassigned values visible and update the authoritative file deliberately.
  review:
    primary_section: F-M02
    kind: Reference-file loading mechanism
    inputs:
      $markdown: field-0002
    narrative:
    - $markdown: field-0003
    - $markdown: field-0004
    configuration:
    - - Upload
      - $markdown: field-0005
      - Instance-visible reference
    - - Maintain
      - Update the governed source and intentionally replace the active uploaded representation.
      - Team-managed content
    - - Deactivate/restore
      - Delete soft-deletes; Restore reactivates.
      - File availability
    lifecycle:
    - - Active file
      - Delete
      - Soft-deleted; removed from active context.
    - - Soft-deleted file
      - Restore
      - Available again.
    - - Similar fact retained in memory
      - Edit file
      - Memory is a separate representation and may need separate correction.
    controls:
      $markdown: field-0006
    observable_output: File state and correct application of a known identifier mapping.
    undocumented: File-versus-memory precedence and exact internal retrieval ranking are not specified.
    test:
    - Upload a harmless mapping for a fictitious account label.
    - Ask a question requiring that mapping and inspect attribution.
    - $markdown: field-0007
    claims:
    - source: FS402
      section: Supported file types; Manage context files
      assertion: Files are agent-read-only, size-limited and support soft deletion/restoration.
    - source: FS403
      section: Managing your data
      assertion: File removal and other object lifecycles differ.
    diagram: mechanism-finops-context
---

<!-- block: b-6229a8196aab5d918b40 -->
## process

<!-- block: b-80b5db1479415b60ba8d -->
<!-- field: field-0001 -->
Read the maintained mapping or reporting convention during relevant work.
<!-- /field -->

<!-- block: b-f0ff20997f8e59258655 -->
## review / inputs

<!-- block: b-3c32efc527c25764af3a -->
<!-- field: field-0002 -->
Approved non-sensitive organization mapping or report convention in a supported active file.
<!-- /field -->

<!-- block: b-c2a5aee1e39354bb98f6 -->
## review / narrative / 0

<!-- block: b-40dd8e0821f25f338d9c -->
<!-- field: field-0003 -->
Uploaded context is maintained outside the conversation. The agent can read the file but cannot rewrite or delete it by conversational instruction. A request to forget a preference therefore does not modify a conflicting account-owner mapping in an uploaded file.
<!-- /field -->

<!-- block: b-ccbb78b537f257cc96e9 -->
## review / narrative / 1

<!-- block: b-e5ab7aa2387c52a7a305 -->
<!-- field: field-0004 -->
Soft deletion removes a file from active context and Restore makes it active again. This is a documented reversible lifecycle for files, not a claim that every other retained object supports restoration.
<!-- /field -->

<!-- block: b-82b5e987693b563bbe13 -->
## review / configuration / 0 / 1

<!-- block: b-9e9402c507a2583c8170 -->
<!-- field: field-0005 -->
Context files workspace: upload TXT, CSV, JSON, Markdown, HTML or YAML within documented size limits.
<!-- /field -->

<!-- block: b-364e7d083465559e82e2 -->
## review / controls

<!-- block: b-3b46f109cf515f4a8d5b -->
<!-- field: field-0006 -->
Files are visible to users with access to the agent. Do not upload credentials or sensitive personal information.
<!-- /field -->

<!-- block: b-103bdff41d3d55f88ce3 -->
## review / test / 2

<!-- block: b-01068924f8f85547b602 -->
<!-- field: field-0007 -->
Soft-delete it and test again; restoring the file is distinct from remembering a new preference.
<!-- /field -->
