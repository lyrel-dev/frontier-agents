---
schema: frontier-workstream/v1
id: aws-operational-agents-documentation
kind: workstream-handoff
title: AWS operational agents — documentation and source-linked review
status: active
document_version: 3
last_reviewed: '2026-10-23'
repository:
  full_name: lyrel-dev/frontier-agents
  target_branch: main
  implementation_branch: docs/annotation-menu-autosave
  implementation_baseline: c9db501798470a2dbfc3961eafaef9fd431f52c0
  validated_output_before_handoff: cfdf280e98e6d4ef78bb0131c6140f167a50e629
  handoff_path: WORKSTREAM.md
  handoff_role: Operational metadata, not an HTML compiler input
objective:
  primary: Maintain factual, educational AWS DevOps, Security and FinOps Agent guides,
    a searchable approved use-case catalog, diagrams and HTML presentations. Author
    published components in Markdown/YAML, provide contextual annotation during normal
    reading, and export exact source references for guarded LLM edits.
  success_criteria:
  - One canonical Markdown/YAML source per published component.
  - Agent-first explanations followed by documented workflows and configuration.
  - Approved model and thirty use cases unchanged without separate authorization.
  - Hover/focus controls and text-selection comments without a Review mode.
  - Persistent source-linked comment markers and element-scoped threads.
  - Exact source hashes, explicit edit scope, dry-run review and guarded application.
  - Deterministic generation and tested desktop, mobile and touch interaction.
scope:
  included:
  - Canonical documentation, compiler, generated HTML and source maps.
  - Search, local contextual comments, export and source patch validation.
  - Documentation CI, technical review and educational quality.
  excluded:
  - Independent applications/ code and its workflow.
  - Live AWS operations or claims of service acceptance.
  - Unauthorized changes to frozen case/model records.
  - Automatic LLM transmission, provider credentials or shared annotation backend.
  - General rich-text editing or reordering published document blocks.
frozen_contract:
  approved_primary_use_cases: 30
  former_identifiers_mapped: 54
  protected_registers:
  - use-cases
  - mechanisms
  - features
  - profiles
  - aliases
  - resource-models
  authored_records: content/registers/**/*.md
  generated_projections: catalog/*.json
  rule: Preserve identities, semantics, relationships, variants and acceptance criteria.
source_contract:
  canonical_root: content/
  format: UTF-8 Markdown with YAML front matter, LF endings and stable block IDs
  compiled_outputs:
  - guides/
  - catalog/
  - presentations/
  - assets/
  validation_records: qa/
  handoff_exception: WORKSTREAM.md is authored operational metadata at repository
    root.
contextual_annotation_contract:
  version: contextual-v3
  user_requirement: Annotation controls appear on document elements during normal
    reading.
  supersedes: Mandatory Review toggle, fixed bottom toolbar and unfiltered primary
    drawer.
  hover_and_focus: Left-gutter block selection handle and direct comment action.
  selection: Floating action for text quotes, ranges and additive block selections.
  persisted_comments: Margin markers reopen element-scoped threads and source context.
  input_methods:
  - pointer_hover
  - pointer_drag_selection
  - keyboard
  - touch_tap
  drag_effect: Selection only; no document reordering.
  global_controls: 'Annotations menu: export/import, connected-user backend save,
    confirmed clear and collection browsing'
  rendering: Controls outside source text; no source-coordinate contamination.
  storage: Existing browser localStorage keys retained, per origin.
  export_schema: frontier-review/v1
  patch_schema: frontier-source-patch/v1
  direct_llm_submission: false
  frozen_record_edits: forbidden
  user_acceptance: pending
  popup: Note/thread and note-level editing actions only
  local_persistence: Automatic on note/reply input and every annotation mutation
  backend_save: Explicit host adapter call for an authenticated connected user; no
    deployed backend included
implementation_snapshot:
  markdown_sources: 457
  guides: 4
  guide_sections: 111
  primary_use_cases: 30
  slides: 52
  diagram_definitions: 48
  source_mapped_html_pages: 42
  verified_source_targets: 2184
  scope_of_counts: Existing content inventory; consult current generated QA for derived
    counts.
validation_snapshot:
  branch_run: https://github.com/lyrel-dev/frontier-agents/actions/runs/39950131103
  branch_conclusion: success
  browser_widths_px:
  - 390
  - 1440
  touch_tap_test: passed
  contextual_browser_errors: 0
  patch_guard_regressions: 15
  preserved_frozen_registers: true
  repeated_build: passed
  local_visual_review: Representative fixture at desktop and mobile widths, not all
    published pages.
  live_aws_execution: false
  records:
  - qa/checks.json
  - qa/authoring-review.json
  - qa/source-map.json
  - qa/educational-checks.json
  - qa/relationships.json
  - qa/resource-models.json
  status: This revision requires the current CI run; prior run links are historical.
milestones:
- id: M01
  status: done
  name: Consolidate prior entries into 30 approved outcomes
- id: M02
  status: done
  name: Approve concept model and specialize AWS product resources
- id: M03
  status: done
  name: Review selected lifecycles and factual/editorial distinctions
- id: M04
  status: done
  name: Establish agent-first teaching and prioritized workflows
- id: M05
  status: done
  name: Migrate published components to Markdown/YAML
- id: M06
  status: done
  name: Source mapping, local search, annotation exports and guarded patching
  qualification: The original toggle-based annotation UX was rejected and is superseded
    by M08.
- id: M07
  status: done
  name: Validate source integrity and Markdown CI
- id: M08
  status: implemented_and_automated_tests_passed
  name: Contextual hover annotations and source-anchored threads
  qualification: Human acceptance remains open; no claim of full editor feature parity.
- id: M09
  status: implementation_pending_validation
  name: Minimal note popup, global annotation menu and automatic local persistence
roadmap:
- id: N01
  priority: P0
  status: pending_human_review
  name: Editorial and instructional acceptance
  tasks:
  - Review agent composition, coordinated work, workspace and prioritized workflows.
  - Eliminate redundant, ambiguous or promotional wording without changing frozen
    semantics.
  - Read guides and slides together and inspect diagram legibility and explanation.
  done_when: Technical reviewers accept the terminology, narrative and workflow traceability.
- id: N02
  priority: P0
  status: pending_human_review
  name: Current official-source accuracy audit
  tasks:
  - Recheck high-impact AWS behavior, availability, identity, permission and lifecycle
    claims.
  - Distinguish documented behavior from team procedures, inference and synthetic
    evidence.
  - Preserve references and explicitly qualify differing documentation representations.
  done_when: Material product claims have current, reviewable and product-specific
    support.
- id: N03
  priority: P0
  status: automated_checks_passed_human_acceptance_pending
  name: Contextual review-to-source edit round trip
  tasks:
  - Demonstrate hover/focus/tap comments and persistent element-scoped threads.
  - Export matching JSON and LLM requests with stable identities and exact source
    targets.
  - Review, validate and explicitly apply a proposed source correction, then inspect
    rebuilt output.
  - Reject stale, protected, ambiguous and out-of-scope proposals.
  done_when: A reviewer accepts the contextual interaction and observes only authorized
    source changes.
- id: N04
  priority: P1
  status: planned
  name: Compiler, search and accessibility hardening
  tasks:
  - Exercise source additions, moves, deletion, metadata/reference failures and stable
    anchors.
  - Test nested elements, table cells, nearby comments and narrow/mobile viewports.
  - Evaluate keyboard focus, search relevance, large-document performance and print.
  done_when: Authoring failures are actionable and context/source navigation remains
    reliable.
- id: N05
  priority: P1
  status: planned
  name: Review security and release controls
  tasks:
  - Extend adversarial packet, path, Unicode, hash and exact-edit boundary tests.
  - Preserve dry-run review and independent protection of frozen records.
  - Avoid concurrent branch edits while CI commits generated outputs.
  done_when: Invalid or unrelated edits cannot bypass source guards and release checks
    preserve scope.
- id: N06
  priority: P2
  status: optional_not_authorized
  name: Direct provider submission or shared annotations
  tasks:
  - Seek explicit scope and authorization before adding external transmission or shared
    storage.
  - Define consent, identity, secrets, retention, access, audit and conflict controls.
  done_when: Any new external service is explicitly authorized and its boundaries
    are tested.
- id: N07
  priority: P1
  status: planned
  name: Final quality and repository hygiene
  tasks:
  - Remove superseded navigation/generators, not historical Git records.
  - Preserve one canonical content source and independent application code.
  - Refresh QA and handoff while keeping evidence gaps separate from build status.
  done_when: Both mandatory automated checks and human technical acceptance are complete.
operating_rules:
- Edit content/**/*.md, not generated HTML, JSON, SVG or assembled guides.
- Do not reinstate a mandatory Review mode or controls that contaminate source text.
- Preserve frozen model/cases, block IDs and exact patch authorization.
- Do not auto-send comments or source excerpts to any provider.
- Do not treat passing documentation tests as live AWS or human editorial acceptance.
- Keep Git history; no manual archives or parallel editions.
next_action: Validate contextual-v3 behavior and backend adapter boundaries, then
  complete N01/N03 human acceptance.
---

# Workstream handoff

## Purpose and status

Maintain an educational, technically sourced collection for **AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent**, consisting of guides, a searchable use-case catalog, resource/workflow diagrams, and HTML presentations. Published document components are authored in Markdown with YAML front matter. Reviewers annotate the rendered material and export comments that identify the exact Markdown source to be changed.

The latest work corrects the interaction requirement: **annotation is part of normal reading, not a separate Review mode**. The original implementation had usable source mapping and patch safeguards, but its mandatory toggle, fixed bottom toolbar, and general-purpose drawer did not meet the user's Notion-style interaction request. Those controls have been replaced by element hover/focus controls, a selection toolbar, persistent source-linked comment markers, and element-scoped threads. The JSON export and guarded-edit contracts remain unchanged.

Implementation validation and human acceptance are different. Automated tests establish the recorded behaviors and preservation checks. They do not establish that every guide is well explained, every AWS statement is current, or that the interaction has received final user acceptance. Technical and educational review remains open.

## Non-negotiable decisions and context

The catalog was consolidated from **54 overlapping entries to 30 approved operational outcomes**. Former identifiers remain navigation metadata. The conceptual entity relationship model was approved and specialized for DevOps, Security, and FinOps without suggesting identical memory, runtime, permission, or execution models. The model and the six canonical registers remain frozen; an annotation does not authorize changing them.

Do not reinstate the rejected taxonomy-as-document design. A use case expresses an operational objective; a feature is a concrete product facility; a mechanism explains documented behavior. The historical “implementation profile” records are authored configuration recipes, not a native AWS resource or a parallel reader-facing product taxonomy. Their identities and relations are retained, but they must not dictate generic, repetitive chapter prose.

The instructional sequence begins with an agent's instructions, skills/procedures, informational context, tools, and execution; then explains coordination and workspace scope; then traces the prioritized workflows using stable diagrams. For DevOps, the priority remains incident operations, operational reporting, reliability improvement, operational knowledge, configuration/release assurance, and operational reviews. Security follows assessment and finding lineage. FinOps follows instance context, source-backed analysis, tasks, automation, and publication. This ordering is editorial, not an AWS ranking.

The ten capability dimensions remain a configuration reference after the introduction. Diagrams use DOC blue, AWS green, and EXT orange for concept ownership. They are logical explanations, not undisclosed service call graphs. Presentations are HTML-only, and their budgets include explicitly allocated exercises. No live AWS execution or measured accuracy/productivity/security/savings result has been established.

## Current interaction contract

1. Hover over a source-backed paragraph, heading, list, table, diagram, slide element, or presenter note. A handle and comment action appear beside the element, ordinarily in the left gutter. No Review switch exists.
2. Click its comment control to open an element-anchored note editor without source-path or excerpt metadata. The controls also appear on keyboard focus; touch users tap the element.
3. Select text to reveal the nearby floating comment action. Use handle clicks, Shift ranges, Ctrl/Command toggling, or handle dragging to select blocks. Dragging selects; it never reorders authored content.
4. Saved annotations retain visible margin markers. Clicking a marker opens threads for that element, rather than requiring a search through unrelated document notes. Replies, resolution and reopening remain available.
5. The document header exposes Search all and the global Annotations menu. That menu contains document notes, collection browsing, export/import, explicit connected-user backend saving, and confirmed local clearing. The note popup contains no global actions.
6. Controls are portalled outside source text; they do not insert button labels inside paragraphs, tables, or source excerpts. Keyboard and touch alternatives remain available, comments are rendered as text, and annotation controls disappear when printing.

The component is a standalone read-only contextual annotation implementation. It is not the licensed Tiptap Notion editor, a full content editor, or a collaborative server. Those are not current requirements. Existing browser storage keys and `frontier-review/v1` exports are retained to avoid discarding previous notes.

## Source and compiler layout

| Location | Responsibility |
|---|---|
| `content/guides/<product>/index.md` | Guide introduction and official references |
| `content/guides/<product>/chapters/` | Chapter order, membership, and introductions |
| `content/guides/<product>/sections/` | Authored technical explanations and procedures |
| `content/presentations/<product>/` | Markdown slide bodies, notes, timings, and deck metadata |
| `content/diagrams/` | DOT/SVG fences and captions |
| `content/registers/` | Frozen records and relationships represented in YAML/Markdown |
| `content/configuration/` | Rendering metadata |
| `content/site/` | README, authoring, editorial, and publication instructions |
| `tools/docs/markdown_sources.py` | Parser, stable IDs, record resolution, and source coordinates |
| `tools/docs/build.py`, `renderer.py`, `source_views.py` | Compiler and compatibility projections |
| `tools/docs/source_review.py` | Rendered source anchors and collection search index |
| `tools/docs/review.js`, `review.css` | Contextual selection, comments, markers, search, and export |
| `tools/docs/review_patch.py` | Guarded exact-source patch validation/application |
| `tools/docs/review_check.py` | Source integrity and patch regression checks |
| `tools/docs/contextual_check.py` | Generated-document contextual interaction acceptance tests |
| `.github/workflows/document-suite.yml` | Source validation, build, browser checks, repeatability, generated commits |

Every compiled source has YAML `id` and `kind` fields. Block markers of the form `<!-- block: identifier -->` provide stable source identity independent of the title or filename. Do not regenerate IDs during ordinary prose edits. The compiler must not change authored `content/` files.

`guides/`, `presentations/`, `catalog/*.json`, generated catalog HTML, SVG output, search data, and source maps are outputs. Do not edit them as alternative sources. `WORKSTREAM.md` is a standalone root handoff with machine-readable metadata, not a compiled product document. No manual archives or secondary editions should be created; Git preserves history.

## Review storage and LLM edit contract

Comments are stored in browser `localStorage`, per origin. Localhost gives predictable cross-page behavior; direct file URLs have browser-specific persistence behavior. Clearing storage removes local notes. Export is the current backup and portability mechanism. There is no user-account service, synchronization, or shared reviewer database.

An export identifies the original document, source path, source ID and block ID; exact Markdown text; full-file and block SHA-256; Unicode code-point and UTF-8 byte intervals; and line ranges. Rendered text selection separately records a quote and UTF-16 DOM positions. These units must not be confused or converted by assuming they are identical.

The editing model returns `frontier-source-patch/v1` JSON bound to an open comment and the stable `review_id`. Every edit must identify the permitted source and exact previous text and hashes. Text-scoped edits can replace only a unique verbatim source quote, preserving the rest of the block. Formatting, repeated text, or cross-block selections that make that mapping ambiguous require explicit block-level review. Never introduce fuzzy matching or silent re-anchoring.

The patch tool rejects generated paths, traversal, symlinks, frozen records, unrelated targets, stale file/block versions, duplicate or overlapping changes, and changed block identities. It defaults to a dry run. Applying a patch requires `--write` after a human reviews the diff. Comments and source quotations are untrusted data, not instructions to run commands or grant permissions.

No comment is transmitted to an LLM automatically. Export JSON and Export/Copy LLM request are manual handoff operations. Direct provider submission or shared annotation storage requires a separately approved security/privacy design and is not part of this release.

## Completed roadmap and correction history

- M01–M02: consolidate and freeze the 30 operational outcomes; approve the conceptual entity model and document native AWS product-resource differences.
- M03–M04: review selected operating lifecycles and source claims; replace repetitive taxonomy cards with agent-first teaching, stable diagrams and prioritized workflow exposition.
- M05: migrate published components to Markdown/YAML; preserve generated routes, identifiers, 52 slides, and the approved records.
- M06–M07: implement source mapping, local search/comments, export, and guarded edits; establish source, browser and CI validation. The original interaction design was subsequently rejected; these milestones did not constitute approval of the toggle-based UX.
- M08: replace the mandatory Review mode with contextual controls and anchored threads; update the browser suite, authoring instructions and this handoff. The current QA record specifies what was tested. M09 further separates global operations from note popups and adds automatic local persistence. Human acceptance is still pending.

The pre-correction snapshot contained 457 Markdown sources, 111 guide sections, 48 diagrams, 52 slides, 42 mapped HTML pages, 2,184 verified rendered targets and 1,455 indexed entries. Those counts describe the inspected baseline, not an immutable quality criterion; consult generated QA for the current output. The independent `applications/` code and its workflow remain outside this workstream.

## Remaining roadmap

### N01 — Technical and educational acceptance (P0)

Read the guides from beginning to end and review the presentations as a first-time technical audience would. Verify the agent definition, instructions/skills/knowledge/tool distinctions, coordinated responsibilities, and Agent Space before operational workflows. Remove redundancy and promotional phrasing. Ensure diagram arrows, ownership colors, source accesses, outputs, approvals, and human decisions are explained in prose. Automated structural checks alone cannot close this stage.

### N02 — Current official-source audit (P0)

Recheck high-impact AWS claims, including product availability, account/Region limits, identity and permissions, memory production/retrieval, cancellation, publication, and revalidation. Retain exact reference attribution and distinguish AWS behavior, team-authored procedures, synthetic examples, and inference. Resolve or explicitly qualify differing retrieved source versions. No internal routing algorithm or cross-service runtime should be inferred from similar naming.

### N03 — Human review-to-source acceptance (P0)

Demonstrate the actual normal-reading interaction: hover, comment, text selection, multi-block selection, anchored thread reopening, and keyboard/touch access. Export one JSON packet and its LLM request, inspect exact Markdown targets, propose a change, validate it, review the diff, apply with approval, rebuild, and inspect the result. Exercise stale, ambiguous, protected, and out-of-scope rejection paths. Confirm previous notes remain accessible. Mark this complete only after a reviewer accepts the experience, not merely because tests pass.

### N04 — Maintenance, accessibility, and search hardening (P1)

Exercise add/move/rename/delete authoring cases, nested blocks and table cells, narrow viewports, large figures, multiple comments at nearby anchors, keyboard focus, touch selection and print. Evaluate search relevance and source navigation. Extend diagnostics for broken references and metadata. Keep source IDs stable and reject ambiguous patches.

### N05 — Security and release controls (P1)

Continue adversarial testing of imports, malformed packets, stale/missing targets, Unicode offsets, paths, hashes, frozen records, overlapping replacements, and prompt-injection content. Preserve manual diff review. Ensure the CI branch being validated is the branch being published; avoid concurrent edits during the bot's generated-output push. Never force-push to conceal a conflict or overwrite another contributor's change.

### N06 — Optional provider submission or shared comments (P2; not authorized)

Only design direct LLM submission, secrets handling, shared storage or multi-user editing after explicit approval. Define authentication, authorization, consent, confidentiality, retention, conflict handling and audit requirements before implementing. Do not call the current local review interface a collaborative editor.

### N07 — Final quality and repository hygiene (P1)

Remove stale navigation and superseded generators rather than preserving parallel editions. Verify one canonical source per component. Keep current source-review gaps distinct from passing build checks, and refresh the validation/handoff records. Do not declare the whole documentation complete while substantive editorial or product-source review remains open.

## Working procedure for the next contributor

Start from current `main`, read this handoff and `AUTHORING.md`, and inspect the current source and QA records. Create a documentation branch for a substantive change. Edit the relevant `content/**/*.md` file, keeping stable IDs and frozen semantics. For UI work, edit `tools/docs/review.js` and `review.css` and extend `contextual_check.py`; do not restore a mandatory annotation mode or inject controls into source text.

Run:

    python -m pip install -r tools/docs/requirements.txt
    python -m playwright install chromium
    python tools/docs/build.py
    python tools/docs/check.py --browser
    python tools/docs/review_check.py

Graphviz is also required. Review generated pages in a browser. A repeated build must preserve authored Markdown bytes and produce the same generated content in the same environment. The main QA records are `qa/checks.json`, `qa/authoring-review.json`, `qa/source-map.json`, `qa/educational-checks.json`, `qa/relationships.json`, and `qa/resource-models.json`.

For an exported review:

    python tools/docs/review_patch.py validate review.json patch.json
    python tools/docs/review_patch.py apply review.json patch.json --write

Inspect the dry-run diff before the second command. Rebuild and rerun checks after an approved edit. Do not commit private review exports without authorization. Preserve the independent application and use Git history, not ZIPs or archive folders.

The immediate next action remains reviewer-led instructional acceptance (N01) and a human-accepted contextual review/edit round trip (N03), not redesign of the frozen model or catalog.


## Contextual-v3 update: local-first notes and global operations

The user clarified that the anchored popup must show only the note. Export, save-to-backend, and clearing controls belong in a global menu, and all annotations must persist locally automatically. The current revision removes global operations, source excerpts/paths, and author/type forms from the note popup. Note text, edits, and replies save on input; Done is not a save prerequisite. Existing note IDs, storage keys, source mappings and patch safeguards remain unchanged.

The document-level Annotations menu provides collection browsing, export/import, confirmed local clearing, and explicit backend save. Backend save requires an authenticated host adapter; absent a connected user or adapter it is disabled. The compiler does not deploy a backend. No remote write occurs merely because a user types. Server authorization and data ownership must be enforced by the host implementation, independently of the exported source metadata.

The additional acceptance tests cover reload without Done, reply/edit persistence, popup/global-control separation, local clearing/cancellation, export after input, authenticated adapter success/failure/session changes, and storage failures. Human acceptance and live backend validation remain distinct from mocked adapter regression tests. The approved model, use cases, and independent application remain frozen/out of scope.
