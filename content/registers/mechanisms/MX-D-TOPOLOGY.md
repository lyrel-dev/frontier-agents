---
id: record-mechanisms-MX-D-TOPOLOGY
kind: record
collection: mechanisms
product: devops
title: Environment-knowledge construction and refresh
order: 1
frozen: true
data:
  id: MX-D-TOPOLOGY
  platform: devops
  title: Environment-knowledge construction and refresh
  features:
  - FT-D-TOPOLOGY
  - FT-D-MEMORY
  sections:
  - D-05
  - D-M08
  trigger: Discovery or applicable managed refresh
  state: Learned relationships and retained context versions
  process:
    $markdown: field-0001
  effect: Retained context update
  verification: Check a known changed resource and relationship in the resulting version.
  on_failure:
    $markdown: field-0002
  review:
    primary_section: D-M08
    kind: Knowledge-production mechanism
    inputs:
      $markdown: field-0003
    narrative:
    - $markdown: field-0004
    - $markdown: field-0005
    configuration:
    - - Discovery
      - $markdown: field-0006
      - Resource and relationship inputs
    - - Refresh
      - Use Topology → Regenerate or request the supported update through Chat.
      - Managed learning request
    - - Inspection
      - Inspect the resulting environment memory and summary/topology representation.
      - Version and changed relationships
    lifecycle:
    - - Source changed
      - Run applicable managed refresh
      - New derived understanding may be written.
    - - Refresh requested
      - Observe completion and inspect a known changed relationship
      - Request acceptance is not completion.
    - - Derived view stale
      - Correct source/discovery configuration and refresh
      - The graph is not repaired by granting unrelated write access.
    controls:
      $markdown: field-0007
    observable_output: Updated context version and a reviewed topology/summary with known changed relationships.
    undocumented:
      $markdown: field-0008
    test:
    - Identify a harmless staging dependency change with authoritative before/after evidence.
    - Find that change in the refreshed representation and record the version.
    - $markdown: field-0009
    claims:
    - source: DS403
      section: How topology graphs are created; Resource discovery; Investigation scope beyond topology
      assertion:
        $markdown: field-0010
    - source: DS402
      section: How memory is built and refreshed
      assertion: Managed stores have distinct refresh conditions and can be inspected after regeneration.
---

<!-- block: b-5d1deb9bc70655088c00 -->
## process

<!-- block: b-578b15f39c7554abb230 -->
<!-- field: field-0001 -->
Synthesize environment evidence into service, dependency and delivery context for subsequent work.
<!-- /field -->

<!-- block: b-ab66cd553561559f9c3f -->
## on failure

<!-- block: b-bd6e8e791bda539487d1 -->
<!-- field: field-0002 -->
Mark stale or inferred relationships; do not substitute the graph for current configuration.
<!-- /field -->

<!-- block: b-4329f67b07d151469bf5 -->
## review / inputs

<!-- block: b-60a18968b78c5d9da810 -->
<!-- field: field-0003 -->
Discovered resources, configuration and observability relationships, connected repository/pipeline context and completed operational work.
<!-- /field -->

<!-- block: b-3382fe7694ab580b946a -->
## review / narrative / 0

<!-- block: b-d7fe1b2b23e25263b89f -->
<!-- field: field-0004 -->
Environment learning turns source evidence into a retained representation. Discovery identifies resources; relationship analysis connects them; learned context describes services and request paths for later work. These products are derived information. They neither replace the deployed configuration nor widen the permission boundary.
<!-- /field -->

<!-- block: b-bc1e2d787e245aa3a348 -->
## review / narrative / 1

<!-- block: b-cef73508fd3e587b9e34 -->
<!-- field: field-0005 -->
Environment understanding, tool-use guidance and monitor history have different refresh conditions. The current memory guide is authoritative for those conditions; the older topology page still uses learned-skill terminology. Requesting regeneration is therefore followed by inspecting the learning result and its version, not by assuming that every dependent view has already changed.
<!-- /field -->

<!-- block: b-cc1b30a423c45e0a8d8d -->
## review / configuration / 0 / 1

<!-- block: b-5b5e3dc1db0352378ead -->
<!-- field: field-0006 -->
Connect the relevant accounts and sources; enable Resource Explorer for its documented discovery path.
<!-- /field -->

<!-- block: b-54f9be6618db5cc99b0b -->
## review / controls

<!-- block: b-f5b22869c226572daf4b -->
<!-- field: field-0007 -->
Authorization belongs to account roles and tool access. A graph omission does not prove a resource is unreadable, and a graph edge does not prove source completeness.
<!-- /field -->

<!-- block: b-86659e4615a351b4aaa2 -->
## review / undocumented

<!-- block: b-dcef5727d6f4514c95a4 -->
<!-- field: field-0008 -->
No universal freshness SLA, complete relationship-detection algorithm or consistency guarantee across all derived views is documented.
<!-- /field -->

<!-- block: b-879442d161ec52e89042 -->
## review / test / 2

<!-- block: b-0f3fdc5a867d570e8b95 -->
<!-- field: field-0009 -->
Leave an input unavailable; require the resulting missing or inferred relationship to remain qualified.
<!-- /field -->

<!-- block: b-8c02ca9c28885afc9761 -->
## review / claims / 0 / assertion

<!-- block: b-f99a728d6e40594fb768 -->
<!-- field: field-0010 -->
Discovery and relationship inference produce a representation that does not bound investigation permissions.
<!-- /field -->
