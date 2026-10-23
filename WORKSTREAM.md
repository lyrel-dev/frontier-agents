---
schema: frontier-workstream/v1
id: aws-operational-agents-documentation
kind: workstream-handoff
title: AWS operational agents — documentation and source-linked review
status: active
document_version: 4
last_reviewed: '2026-10-23'
repository:
  full_name: lyrel-dev/frontier-agents
  target_branch: main
  implementation_branch: docs/hierarchical-selection
  implementation_baseline: 516ad5d14b05cc732600efd5ae1b51e41994168b
  validated_output_before_handoff: 2bf7ac9771f0a3e2d511f2c8cf5589bf9e48f956
  handoff_path: WORKSTREAM.md
  handoff_role: Operational metadata, not an HTML compiler input
objective:
  primary: >-
    Maintain factual, educational AWS DevOps, Security and FinOps Agent guides,
    the approved searchable use-case catalog, diagrams and HTML presentations.
    Author published components in Markdown/YAML. Support contextual annotations
    of meaningful document elements and complete structural units, with exact
    source snapshots and independently guarded LLM edits.
  success_criteria:
    - One canonical Markdown/YAML source per published component.
    - Agent-first explanations followed by documented workflows and configuration.
    - Approved model and thirty use cases preserved without separate authorization.
    - Reader selection hierarchy independent of source-file and edit boundaries.
    - Hover/focus annotation, note-only popups and no mandatory Review mode.
    - Global annotation menu and automatic local persistence without a Save prerequisite.
    - Immutable source membership, exact hash checks and explicitly reviewed patches.
    - Repeatable generation and tested desktop, mobile and touch interaction.
scope:
  included:
    - Canonical documentation, compiler, generated HTML, selection trees and source maps.
    - Search, contextual notes, local persistence, exports and source-patch validation.
    - Optional authenticated host adapter for explicit backend saving.
    - Documentation CI, factual review and instructional quality.
  excluded:
    - Independent applications/ code and its workflow.
    - Live AWS operations or claims of service acceptance.
    - Unauthorized changes to frozen model and use-case records.
    - Automatic LLM transmission or model-provider credentials.
    - Deployment of authentication, shared storage or collaborative editing services.
    - General rich-text editing or reordering published content.
frozen_contract:
  approved_primary_use_cases: 30
  former_identifiers_mapped: 54
  protected_registers: [use-cases, mechanisms, features, profiles, aliases, resource-models]
  authored_records: content/registers/**/*.md
  generated_projections: catalog/*.json
  rule: Preserve identities, semantics, relationships, variants and acceptance criteria.
source_contract:
  canonical_root: content/
  format: UTF-8 Markdown with YAML front matter, LF endings and stable block IDs
  compiled_outputs: [guides/, catalog/, presentations/, assets/]
  validation_records: qa/
  handoff_exception: WORKSTREAM.md is authored operational metadata at repository root.
selection_contract:
  schema: frontier-selection/v1
  application_model_only: true
  approved_aws_model_changes: false
  independent_concepts:
    - presentation scope selected by the reader
    - immutable source-membership snapshot
    - explicitly permitted edit validated independently
  levels: [text, element, group, subsection, section, chapter, slide, presenter-notes, document]
  heading_policy: A heading is distinct from its containing section or slide.
  container_membership: All mapped descendants, including collapsed and filtered content.
  controls: Parent button, Selection scope chooser, keyboard expansion and existing pointer/touch actions.
  normalization: Ancestors subsume selected descendants; source targets deduplicate in reading order.
  range_boundary: Include complete selected endpoints and fully covered intermediate scopes; never partially covered ancestors.
  snapshot: Root identities, document, content revision, ordered target IDs, contextual IDs and membership digests.
  immutability: Saved notes never acquire newly added descendants or silently reattach to another scope.
  marker_policy: Mark selected rendered roots, not every child and not unrelated occurrences of shared sources.
  unmapped_policy: Annotation-only; containing source context is not permission to edit that source.
  shared_source_policy: A canonical source edit may affect multiple compiled occurrences; review all affected output.
  stale_policy: Canonical content revision changes invalidate structural edit authorization until renewed review.
  guard_policy: Check root snapshots, exact member lists, current canonical ranges, hashes and frozen restrictions.
  compatibility: Legacy frontier-review/v1 block and quote annotations keep their exact-source guards.
contextual_annotation_contract:
  version: contextual-v4
  user_requirement: >-
    Annotate elements and complete sections during normal reading. Keep the
    popup limited to its note/thread. Put collection actions in a global menu.
    Save all note changes locally automatically.
  supersedes: Flat source-block-only selection, mandatory Review mode and global actions inside note popups.
  popup: Note text, replies and note-level actions; no export, source-path or scope-selection controls.
  global_controls:
    - Document notes and collection browsing.
    - JSON export, LLM-request export/copy and import.
    - Explicit connected-user backend saving.
    - Confirmed clear for this document or all local annotations.
  input_methods: [pointer_hover, pointer_drag_selection, keyboard, touch_tap]
  drag_effect: Selection only; never document reordering.
  local_persistence: On note/reply input and every annotation mutation; Done only closes the editor.
  storage: Existing browser localStorage keys retained, per origin.
  storage_failure: Report failure and preserve the in-memory export; never claim a failed write succeeded.
  clear_scope: Local only; previously saved backend copies are not deleted.
  rendering: Portalled controls do not contaminate source text or quote offsets.
  export_schema: frontier-review/v1
  patch_schema: frontier-source-patch/v1
  direct_llm_submission: false
  frozen_record_edits: forbidden
  human_acceptance: pending
backend_contract:
  availability: Optional host integration; no backend deployed by this repository.
  registration: FrontierReview.setBackend(adapter) or window.FrontierReviewBackend
  session: getSession({signal}) returns null or a user with a nonempty string id.
  persistence: saveReview(packet, {signal}) confirms persistence with saved=true and a nonempty id.
  enablement: Adapter and authenticated connected user required; session checked before saving.
  transmission: Explicit Save to backend only; typing never triggers a remote write.
  failure: Preserve local notes and report missing confirmation or failure.
  host_responsibility: Authentication, authorization, ownership, CSRF/TLS where applicable, limits and retention.
  production_backend_tested: false
implementation_snapshot:
  markdown_sources: 457
  guides: 4
  guide_sections: 111
  primary_use_cases: 30
  slides: 52
  diagram_definitions: 48
  source_mapped_html_pages: 42
  verified_source_targets: 2184
  generated_selection_nodes: 12451
  count_boundary: Inspected build inventory, not a measure of instructional quality.
validation_snapshot:
  branch_run: https://github.com/lyrel-dev/frontier-agents/actions/runs/39977311557
  conclusion: success
  browser_widths_px: [390, 1440]
  source_mapping_errors: 0
  existing_patch_guard_cases: 15
  additional_structural_guard_cases: 9
  hierarchical_browser_paths: passed
  hidden_membership_and_ancestor_normalization: passed
  persistent_container_markers_and_exact_export: passed
  prior_contextual_and_menu_regressions: passed
  repeated_build: passed
  preserved_frozen_registers: true
  backend_tests: Controlled adapter mocks, not a deployed service.
  local_additional_test: Synthetic range fixture verified partial-table exclusion, complete-table inclusion and immutable snapshots.
  visual_boundary: Automated browser checks; no claim of manual acceptance of every page.
  live_aws_execution: false
  records:
    - qa/checks.json
    - qa/authoring-review.json
    - qa/source-map.json
    - qa/educational-checks.json
    - qa/relationships.json
    - qa/resource-models.json
milestones:
  - {id: M01, status: done, name: Consolidate 54 prior entries into thirty approved outcomes}
  - {id: M02, status: done, name: Approve entity model and specialize native AWS product resources}
  - {id: M03, status: done, name: Review selected lifecycle claims and editorial distinctions}
  - {id: M04, status: done, name: Establish agent-first teaching and prioritized workflows}
  - {id: M05, status: done, name: Migrate published components to Markdown/YAML}
  - id: M06
    status: done
    name: Source mapping, local search, exports and guarded editing
    qualification: Original toggle-based UX was rejected; its source infrastructure was retained.
  - {id: M07, status: done, name: Validate source integrity and Markdown CI}
  - id: M08
    status: implemented_and_automated_tests_passed
    name: Contextual hover annotations and anchored threads
  - id: M09
    status: implemented_and_automated_tests_passed
    name: Note-only popups, global operations and automatic local persistence
    qualification: Backend adapter tested with mocks only.
  - id: M10
    status: implemented_and_automated_tests_passed
    name: Hierarchical reader selection, immutable source snapshots and edit-authority separation
    qualification: Human UX and editorial acceptance remain open.
roadmap:
  - id: N01
    priority: P0
    status: pending_human_review
    name: Technical and instructional acceptance
    tasks:
      - Read agent definitions, coordination, workspace and prioritized workflows end to end.
      - Remove redundant, ambiguous or promotional wording without changing frozen semantics.
      - Review slides, notes and diagrams together, not only structural counts.
    done_when: Technical reviewers accept terminology, narrative and traceability.
  - id: N02
    priority: P0
    status: pending_human_review
    name: Current official-source audit
    tasks:
      - Recheck material AWS availability, identity, access, lifecycle and retention claims.
      - Distinguish documented behavior from inference, team procedures and synthetic examples.
      - Preserve citations and qualify conflicting source representations.
    done_when: Material claims have current, reviewable, product-specific evidence.
  - id: N03
    priority: P0
    status: automated_checks_passed_human_acceptance_pending
    name: Hierarchical review-to-source acceptance
    tasks:
      - Demonstrate heading versus complete section, chapter, slide and document selection.
      - Inspect hidden membership, ancestor normalization and one marker per selected root.
      - Verify note-only popups, global actions and autosave without Done.
      - Export a review, validate a proposed patch, approve it explicitly and inspect rebuilt output.
      - Reject stale, expanded, protected, ambiguous and context-only edit requests.
      - Review the effects of changing shared canonical sources across compiled occurrences.
    done_when: A reviewer accepts the interaction and observes only authorized source changes.
  - id: N04
    priority: P1
    status: planned
    name: Compiler, accessibility and performance hardening
    tasks:
      - Exercise source moves, deletion, title changes, metadata errors and stable anchors.
      - Extend nested ranges, table-cell, mixed-mapping, touch and keyboard tests.
      - Test long-document storage limits, repeated sources, nearby markers and filtering.
      - Consider finer-grained exact source maps only without broadening edit permission.
    done_when: Authoring and review failures are actionable and navigation remains reliable.
  - id: N05
    priority: P1
    status: planned
    name: Review security and release controls
    tasks:
      - Expand adversarial packet, path, Unicode, hash and source-membership tests.
      - Preserve dry-run approval, frozen restrictions and optional trusted review digests.
      - Avoid concurrent branch edits during generated-output publication.
    done_when: Invalid edits cannot bypass guards and releases preserve repository scope.
  - id: N06
    priority: P1
    status: host_integration_required_for_backend
    name: Production backend integration
    tasks:
      - Connect only to an authorized host session and storage service.
      - Verify server-side ownership, authorization, CSRF protection, failure handling and retention.
      - Scope collaboration and direct LLM submission separately before implementation.
    done_when: An explicitly connected real backend passes its own acceptance tests.
  - id: N07
    priority: P1
    status: planned
    name: Final quality and repository hygiene
    tasks:
      - Remove superseded generators and navigation, not Git history.
      - Keep one canonical content source and preserve the independent application.
      - Refresh QA and handoff while distinguishing evidence gaps from passing builds.
    done_when: Required automated checks and human technical acceptance are complete.
operating_rules:
  - Edit content/**/*.md, not generated HTML, JSON, SVG or assembled guides.
  - Do not treat source-file boundaries as reader-selection boundaries.
  - Do not turn a selected container into whole-file or wildcard edit permission.
  - Never infer hidden or new targets into an existing review snapshot.
  - Keep context-only and protected content annotatable without editable grants.
  - Keep popup note-only, collection operations global and local persistence automatic.
  - Preserve frozen AWS model/use cases, source block IDs and exact patch constraints.
  - Do not automatically transmit comments or source excerpts to any provider.
  - Do not claim live AWS, backend or human acceptance from documentation tests.
  - Use Git history; no manual archives, parallel editions or forced publication over conflicts.
next_action: N01 and N03 human acceptance using the published contextual-v4 interface.
---

# Workstream handoff

## Objective and current status

Maintain technically sourced, educational documentation for **AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent**: four guides including shared architecture, the approved searchable use-case catalog, resource/workflow diagrams and HTML presentations. Published material is authored in Markdown with YAML front matter. The rendered documents support contextual annotations whose exports identify exact canonical source ranges for guarded editing.

The current interface is **contextual-v4**. The implementation and automated tests for hierarchical selection are complete on the branch identified above. The cited run passed source preservation, existing reader/menu behavior, new structural selection paths, patch guards and repeatable generation. Human editorial and interaction acceptance remain open. Counts in the header describe the inspected build, not the quality of the explanation or live AWS behavior.

The original implementation baseline was `516ad5d14b05cc732600efd5ae1b51e41994168b`; the validated output before this handoff is `2bf7ac9771f0a3e2d511f2c8cf5589bf9e48f956`. These are evidence references. Future contributors must start from the current branch, not reset to an old snapshot.

## Product context and frozen decisions

The original 54 overlapping entries were consolidated into **30 approved operational outcomes**. Former identifiers remain navigation metadata. The conceptual entity model was approved and specialized for the three products without assuming identical native agent, knowledge, execution, networking or permission models. The six registers remain frozen. UI, compiler or editorial changes do not authorize rewriting their IDs, objectives, variants, relationships or completion criteria.

Do not reinstate the rejected taxonomy-as-document structure. Use cases describe operational objectives; features identify concrete product facilities; mechanisms explain documented processes. Historical implementation-profile records represent authored configuration recipes, not native AWS resources or a separate reader-facing feature catalog. They support traceability without dictating repetitive chapter prose.

The teaching sequence starts with the agent: instructions, procedures/skills, retained informational context, tools and a particular execution. It then explains coordinated responsibilities and workspace scope before applying the same diagrams to workflows. DevOps prioritizes incident operations, health/change reporting, reliability improvement, SOP/topology knowledge, configuration/release assurance and operational reviews. Security follows assessment and finding lineage. FinOps follows instance context, source-backed analysis, tasks, automations and publication. This is an editorial sequence, not an AWS ranking.

The ten capability dimensions remain a detailed reference after the introduction. DOC blue, AWS green and EXT orange distinguish concept ownership in diagrams; they do not depict undisclosed service internals. Presentations remain HTML-only. Exercise budgets do not imply live-agent completion times.

## Corrected selection strategy

The prior implementation conflated the smallest addressable source block with the largest object a reader may annotate. That caused headings to be selectable without their sections, and allowed flat-block tests to pass while whole sections and slides were unsupported. The correction establishes three independent layers:

| Layer | Meaning | Constraint |
|---|---|---|
| Presentation scope | Text, element, subsection, section, chapter, complete slide, notes group or document selected by the reader | Uses document structure, not Markdown file boundaries |
| Source-membership snapshot | Ordered, deduplicated exact source targets captured for that scope | Includes mapped hidden descendants; does not change after the note is saved |
| Permitted edit | Particular replacement proposed against an explicitly captured target | Subject to hashes, exact prior text, source boundaries, frozen restrictions and human approval |

Hover or focus content, then use **Parent** or **Selection scope** to select the enclosing unit. A heading means the heading text; a section means the heading and all its contents. A selected boundary and summary appear before commenting. Keyboard users can focus a handle, use Alt+Up to expand and Alt+Down to return through that expansion path. Directly choosing another scope resets the path.

Selecting a container includes its mapped descendants even when filtering, collapse or chapter navigation hides them. The summary identifies hidden and protected targets. Ancestor/descendant overlap is normalized; canonical source targets deduplicate in reading order. A range includes complete endpoints and fully covered intermediate scopes, not a partially covered ancestor. Selecting through a table cell therefore does not silently authorize its entire table.

Meaningful generated content and nested elements without independent exact Markdown ranges remain **annotation-only**. The containing source block is context, not editable authority. A table-cell note cannot silently grant whole-table editing rights. A reviewer may explicitly select the mapped table for a wider edit. Text quotes continue to require a unique verbatim source occurrence before automated replacement.

A comment remains anchored to its selected rendered root, not duplicated across every descendant or unrelated occurrence of shared content. The source snapshot records document identity, root IDs, content revision, target IDs, contextual IDs and membership digests. Newly added descendants do not enter an old review automatically. Missing or changed roots are stale, not silently reassigned.

The initial structural-edit policy is deliberately conservative: **any canonical content-revision change requires renewed structural review before automated editing**. Legacy block/quote records retain their existing exact-hash behavior. Any future relaxation must prove unchanged membership and must not replace the original authorized target set with a newly computed one.

A canonical target may be rendered in several documents. Highlighting and comments stay on the selected instance, but editing that canonical target may update all its occurrences. Inspect affected outputs before accepting a patch; do not fork source content to hide shared effects.

This selection hierarchy is an application-level documentation model. It does not modify the approved AWS concept model or the frozen use cases.

## Annotation and storage behavior retained

Annotation is available during normal reading; no Review mode exists. Hover/focus/tap controls expose a handle and comment action. Native text selection provides a floating comment action. Shift, Ctrl/Command and handle dragging provide range/additive selection; dragging never rearranges the document.

The anchored popup contains **only the note, replies and note-level actions**. It does not contain source paths, copied document excerpts, source-selection controls, exports, collection filters or backend tools. The document-level **Annotations** menu owns collection browsing, document notes, export/import, explicit backend save and confirmed clearing. Search remains a separate document-wide command.

Note text, edits and replies save to browser localStorage on input. Resolution, reopening, import and clearing also persist automatically. **Done closes the editor; it is not required for saving.** Browser storage keys and existing note schemas are retained. Storage failures are reported visibly and the in-memory export is retained; never show success after a failed write. Clearing local notes does not delete backend copies.

Use one localhost origin for reliable cross-page storage. Direct-file persistence is browser-specific. There is no shared reviewer database or collaborative editing service. Export before clearing browser data or moving devices. Controls are portalled outside content so labels do not contaminate source text or quote offsets.

## Export, source patch and backend contracts

An annotation export uses `frontier-review/v1`. Exact targets include source path and ID, block ID, file/block SHA-256, Markdown excerpt, line range, Unicode code-point offsets and UTF-8 byte offsets. Rendered text quotations have separate UTF-16 DOM positions. These coordinate systems are not interchangeable.

New semantic selections add `selection.schema: frontier-selection/v1` and root-membership snapshots. Root labels or CSS structure are not whole-file instructions. The patch tool independently compares the captured roots and target list with the current compiled map and canonical sources. The LLM prompt explicitly forbids expanding into contextual IDs or new descendants.

Model proposals use `frontier-source-patch/v1`, bound to a stable review ID and open comment. The tool rejects stale or changed membership, omitted/reordered members, duplicate or ancestor/descendant roots, unsafe document/source paths, symlinks, frozen targets, unrelated ranges, ambiguous quotes and changes to block identities. An annotation-only scope grants no source edits. A valid section review can authorize one exact member replacement; it never requires rewriting the section's whole file.

The guard defaults to a dry run. Inspect its diff before using `--write`. The optional trusted review digest can pin the original reviewer packet. Comments, source quotes and model text are untrusted data, not permission to execute commands. No export is sent to an LLM automatically.

Backend saving remains an optional host adapter, not an authentication service supplied by this repository. Register `FrontierReview.setBackend(adapter)` or `window.FrontierReviewBackend`. The adapter supplies `getSession({signal})` and `saveReview(packet, {signal})`; the latter must confirm actual persistence with `{saved: true, id}`. The reader requires a connected user and rechecks the session. Typing remains local-only; **Save to backend** sends an explicit snapshot. Failures preserve local annotations. Server-side authentication, ownership, authorization, CSRF/TLS where applicable, limits and retention belong to the host. Tests use controlled mocks, not a deployed production backend.

## Source layout and module responsibilities

| Location | Responsibility |
|---|---|
| `content/guides/<product>/` | Introductions, chapter membership, technical sections and official references |
| `content/presentations/<product>/` | Markdown slide bodies, notes, timing and deck metadata |
| `content/diagrams/` | DOT/SVG fences and explanatory captions |
| `content/registers/` | Frozen definitions and relationships in YAML/Markdown |
| `content/configuration/` | Rendering metadata |
| `content/site/` | README, authoring, editorial and publishing instructions |
| `tools/docs/markdown_sources.py` | Parsing, stable source IDs, reference resolution and exact coordinates |
| `tools/docs/build.py`, `renderer.py`, `source_views.py` | Compilation and generated compatibility views |
| `tools/docs/source_review.py` | Rendered source anchors, selection metadata and search index |
| `tools/docs/selection_model.py` | Semantic tree construction and independent structural-patch validation |
| `tools/docs/selection_model.js` | Client hierarchy, normalized roots, immutable snapshots and range boundaries |
| `tools/docs/review.js`, `review.css` | Contextual controls, selected scopes, comments, markers, menus and persistence |
| `tools/docs/review_patch.py` | Existing exact-source guards plus structural snapshot validation |
| `tools/docs/hierarchy_check.py` | Tree, source-authority and whole-container browser regressions |
| `tools/docs/contextual_check.py`, `annotation_menu_check.py` | Preserved contextual and global-menu/autosave behavior |
| `.github/workflows/document-suite.yml` | Build, browser checks, repeatability and generated-file publication |

Published HTML, compiled guide Markdown, catalog JSON, SVG, search data and source maps are generated outputs. Edit canonical `content/**/*.md` instead. Keep explicit block IDs stable through ordinary edits. `WORKSTREAM.md` is a root operational handoff, not a compiler input. Preserve the independent `applications/` code and its workflow.

## Completed milestones and remaining roadmap

M01–M05 established the approved catalog/model, selected factual review, agent-first educational flow and Markdown/YAML authoring. M06–M07 supplied precise source mappings, search, exported reviews, patch guards and CI. The original toggle-based interaction was rejected; M08 replaced it with contextual controls. M09 separated note popups from global operations and made local saving automatic. **M10 now separates hierarchical reader scope from immutable source membership and edit authority.** Automated implementation tests pass; that does not constitute final user acceptance.

The next priorities are **N01 technical/instructional review** and **N03 a human-observed hierarchical review-to-source correction**. Read whole guides and presentations together. Demonstrate a heading, section, chapter, complete slide and document selection; inspect hidden membership and a container's single thread marker; export a review; validate and explicitly approve one source correction; rebuild and inspect all affected output. Do not close this milestone solely because a browser script passes.

N02 remains the current official-source audit. Verify important AWS availability, permission, lifecycle, retention and execution claims against their actual product documentation, distinguishing native behavior, team procedures, inference and synthetic evidence. No new live AWS execution was performed by this UI work.

N04/N05 cover maintenance, accessibility, performance and security hardening. Test source moves/deletions, mixed mapping, repeated content, narrow layouts, nested ranges, storage limits, hostile imports, stale and forged packets, Unicode and exact edit boundaries. Finer-grained source mapping must never be implemented by giving a small selection broader implicit authority. Do not silently relax snapshot revision checks.

N06 requires a separately connected and authorized real backend. Shared review storage, collaboration and direct provider submission are separate designs. N07 requires final editorial acceptance, current QA/handoff, one canonical source and removal of superseded generators—not archives of earlier editions.

## Working and publication procedure

Start from current `main`, then read this handoff, `AUTHORING.md`, `EDITORIAL_STANDARD.md`, `PUBLISHING.md` and the current QA. Use a documentation branch for substantive changes. Preserve all six frozen registers and the independent application. For content changes edit the appropriate Markdown source and retain block IDs; for selection/UI changes update the maintained modules and relevant semantic tests, not just rendered CSS.

Install Graphviz and the documented Python/Chromium dependencies, then run:

    python tools/docs/build.py
    python tools/docs/check.py --browser
    python tools/docs/review_check.py

A second build must produce identical generated output in the same environment and leave authored Markdown unchanged. Inspect source and generated diffs. The current run validates 42 page selection trees, 2,184 exact source targets, the original 15 patch-guard cases, nine additional structural guard cases, and desktop/mobile whole-container reading paths. Existing popup/menu/autosave, keyboard/touch, import/export, search and adapter checks remain active. Counts alone are not acceptance criteria.

For model-proposed edits:

    python tools/docs/review_patch.py validate review.json patch.json
    python tools/docs/review_patch.py apply review.json patch.json --write

The second command requires human approval of the dry-run diff. Rebuild and rerun the checks after application. Never commit private reviewer exports without authorization. Do not force-publish over concurrent branch changes. Remove temporary migration scripts/hooks after validation and keep prior versions only in Git.

The remaining boundary is explicit: automated document, browser and source-authority checks passed for the recorded revision; live AWS tests, real backend acceptance, exhaustive source review and final human UX/editorial acceptance remain separate work.
