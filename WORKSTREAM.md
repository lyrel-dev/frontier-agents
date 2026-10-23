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
  validated_output_before_handoff: f2272fd0659d3eb803e702730e55de664f64306f
  handoff_path: WORKSTREAM.md
  handoff_role: Operational metadata, not an HTML compiler input
objective:
  primary: >-
    Maintain factual, educational AWS DevOps, Security and FinOps Agent guides,
    an approved searchable use-case catalog, diagrams and HTML presentations.
    Author published components in Markdown/YAML, provide contextual notes during
    normal reading, and export exact source references for guarded LLM edits.
  success_criteria:
    - One canonical Markdown/YAML source per published component.
    - Agent-first explanations followed by documented workflows and configuration.
    - Approved model and thirty use cases preserved without separate change authorization.
    - Hover/focus annotation controls with a note-only popup and no Review mode.
    - Automatic local persistence of note text, edits, replies and annotation mutations.
    - Global annotation menu for export/import, connected-user backend save and confirmed clear.
    - Exact source hashes, explicit edit scope, dry-run review and guarded application.
    - Repeatable generation and tested desktop, mobile and touch interaction.
scope:
  included:
    - Canonical documentation, compiler, generated HTML and source maps.
    - Search, contextual notes, local persistence, export and source patch validation.
    - Optional authenticated host adapter for explicit backend saving.
    - Documentation CI, technical review and educational quality.
  excluded:
    - Independent applications/ code and its workflow.
    - Live AWS operations or claims of service acceptance.
    - Unauthorized changes to frozen case/model records.
    - Automatic LLM transmission or model-provider credentials.
    - Deployment of an authentication service, shared note database or collaboration server.
    - General rich-text editing or reordering of published document blocks.
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
contextual_annotation_contract:
  version: contextual-v3
  user_requirement: >-
    Annotate document elements during normal reading. Show only the relevant note
    in its popup; put collection operations in a global menu. Save locally automatically.
  supersedes: Mandatory Review toggle, bottom toolbar and global operations inside the note popup.
  hover_and_focus: Left-gutter selection handle and direct comment action.
  selection: Floating action for text quotes, ranges and additive block selections.
  popup: Note text, replies and note-level editing actions only; no source paths or quoted source context.
  global_controls:
    - Add document note and browse the annotation collection.
    - Export JSON, export or copy an LLM request, and import annotations.
    - Save an explicit snapshot to a backend for a connected user.
    - Confirm clearing this document or all local notes, comments and replies.
  input_methods: [pointer_hover, pointer_drag_selection, keyboard, touch_tap]
  drag_effect: Selection only; no document reordering.
  rendering: Controls outside source text; source coordinates are not contaminated.
  local_persistence: On note/reply input and every annotation mutation; Done only closes the editor.
  storage: Existing browser localStorage keys retained, per origin.
  clear_scope: Local only; saved backend copies are not deleted.
  storage_failure: Warn visibly and retain the in-memory export instead of claiming successful persistence.
  export_schema: frontier-review/v1
  patch_schema: frontier-source-patch/v1
  direct_llm_submission: false
  frozen_record_edits: forbidden
  user_acceptance: pending
backend_contract:
  availability: Optional host integration; no backend is deployed by this repository.
  registration: FrontierReview.setBackend(adapter) or window.FrontierReviewBackend
  session_method: getSession({signal}) returns null or a user with a nonempty string id.
  save_method: saveReview(packet, {signal}) confirms persistence with saved=true and a nonempty id.
  enablement: Adapter and connected user required; session is rechecked before saving.
  transmission: Explicit Save to backend only; typing never triggers a remote write.
  failure_behavior: Keep local annotations and report failure or missing confirmation.
  server_responsibility: Authentication, ownership, authorization, CSRF/TLS where applicable, limits and retention.
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
  scope_of_counts: Inspected content inventory; current generated QA remains authoritative.
validation_snapshot:
  branch_run: https://github.com/lyrel-dev/frontier-agents/actions/runs/39966489147
  branch_conclusion: success
  browser_widths_px: [390, 1440]
  touch_tap_test: passed
  automatic_local_persistence_tests: passed
  backend_adapter_tests: Mocked connected-user, success, failure, expiry and unconfirmed response.
  local_clear_confirmation_tests: passed
  storage_failure_export_test: passed
  source_mapping_errors: 0
  patch_guard_regressions: 15
  preserved_frozen_registers: true
  repeated_build: passed
  visual_boundary: Automated rendered-browser checks; no new manual screenshot acceptance is claimed.
  live_aws_execution: false
  records:
    - qa/checks.json
    - qa/authoring-review.json
    - qa/source-map.json
    - qa/educational-checks.json
    - qa/relationships.json
    - qa/resource-models.json
milestones:
  - {id: M01, status: done, name: Consolidate prior entries into thirty approved outcomes}
  - {id: M02, status: done, name: Approve concept model and specialize AWS product resources}
  - {id: M03, status: done, name: Review selected lifecycles and factual/editorial distinctions}
  - {id: M04, status: done, name: Establish agent-first teaching and prioritized workflows}
  - {id: M05, status: done, name: Migrate published components to Markdown/YAML}
  - id: M06
    status: done
    name: Source mapping, local search, exports and guarded patching
    qualification: The original toggle-based annotation UX was rejected and superseded.
  - {id: M07, status: done, name: Validate source integrity and Markdown CI}
  - id: M08
    status: implemented_and_automated_tests_passed
    name: Contextual hover annotations and anchored threads
    qualification: Human acceptance remains open; no claim of rich-text-editor feature parity.
  - id: M09
    status: implemented_and_automated_tests_passed
    name: Note-only popup, global annotation menu and automatic local persistence
    qualification: Backend tested through adapter mocks, not a deployed authenticated service.
roadmap:
  - id: N01
    priority: P0
    status: pending_human_review
    name: Editorial and instructional acceptance
    tasks:
      - Review agent composition, coordinated work, workspace and prioritized workflows.
      - Remove redundant, ambiguous or promotional wording without changing frozen semantics.
      - Read guides and slides together; inspect diagram clarity and explanation.
    done_when: Technical reviewers accept terminology, narrative and workflow traceability.
  - id: N02
    priority: P0
    status: pending_human_review
    name: Current official-source accuracy audit
    tasks:
      - Recheck material AWS behavior, availability, identity, permission and lifecycle claims.
      - Distinguish documented behavior from team procedures, inference and synthetic evidence.
      - Preserve citations and qualify conflicting documentation representations.
    done_when: Material product claims have current, reviewable, product-specific support.
  - id: N03
    priority: P0
    status: automated_checks_passed_human_acceptance_pending
    name: Contextual annotation and source-edit acceptance
    tasks:
      - Demonstrate note-only hover/focus/tap popups and global annotation operations.
      - Verify local persistence without Done, after closing and after reload.
      - Export precise review JSON and LLM request with stable identities.
      - Review, validate and explicitly apply an authorized source correction, then rebuild.
      - Reject stale, frozen, ambiguous and out-of-scope edit proposals.
    done_when: A reviewer accepts the interaction and observes only authorized source changes.
  - id: N04
    priority: P1
    status: planned
    name: Compiler, search and accessibility hardening
    tasks:
      - Exercise source additions, moves, deletion, metadata failures and stable anchors.
      - Test nested elements, tables, adjacent annotations and narrow layouts.
      - Evaluate keyboard focus, search relevance, performance and printing.
    done_when: Authoring failures are actionable and source navigation remains reliable.
  - id: N05
    priority: P1
    status: planned
    name: Review security and release controls
    tasks:
      - Expand adversarial packet, path, Unicode, hash and exact-edit boundary tests.
      - Preserve dry-run approval and independent protection of frozen records.
      - Avoid concurrent edits while CI commits generated outputs.
    done_when: Invalid edits cannot bypass guards and releases preserve repository scope.
  - id: N06
    priority: P1
    status: host_integration_required_for_backend
    name: Production backend integration and optional collaboration
    tasks:
      - Connect the adapter to an authorized host session and storage endpoint when available.
      - Validate server-side ownership, authorization, CSRF protection, failures and retention.
      - Treat collaborative storage and direct LLM submission as separately scoped future work.
    done_when: A real authenticated backend is explicitly connected and its boundaries are verified.
  - id: N07
    priority: P1
    status: planned
    name: Final quality and repository hygiene
    tasks:
      - Remove superseded generators and navigation, not Git history.
      - Preserve one canonical source and independent application code.
      - Refresh QA and handoff while keeping evidence gaps distinct from build status.
    done_when: Mandatory automated checks and human technical acceptance are complete.
operating_rules:
  - Edit content/**/*.md, not generated HTML, JSON, SVG or assembled guides.
  - Keep global export/backend/clear controls out of note popups.
  - Preserve automatic local persistence and do not require a Save click.
  - Do not reinstate a mandatory Review mode or contaminate source text with controls.
  - Preserve frozen model/cases, stable block IDs and exact patch authorization.
  - Do not automatically transmit annotations or source excerpts to any provider.
  - Do not equate documentation tests with live AWS, production-backend or human acceptance.
  - Use Git history; do not create manual archives or parallel editions.
next_action: N01/N03 human acceptance; connect and test the backend adapter only with an authorized host.
---

# Workstream handoff

## Objective and status

Maintain factual, educational documentation for **AWS DevOps Agent, AWS Security Agent and AWS FinOps Agent**: guides, the approved use-case catalog, resource and workflow diagrams, and HTML presentations. Published content is authored in Markdown with YAML front matter. Rendered elements remain linked to precise source blocks so reviewers can annotate material and request tightly scoped edits from an LLM.

The current revision is **contextual-v3**. It implements the latest user clarification: the anchored popup shows only the relevant note and its thread actions; export, backend saving, collection management and clearing belong in a global menu; and note text, edits and replies are saved locally automatically. The branch validation linked above passed. Human editorial and interaction acceptance remain open.

The inspected implementation baseline was `c9db501798470a2dbfc3961eafaef9fd431f52c0`. Validated output before this handoff was `f2272fd0659d3eb803e702730e55de664f64306f`. These are evidence references, not instructions to work from an old checkout. Future contributors must begin from the current branch.

## Context and frozen decisions

The original 54 overlapping catalog records were consolidated into **30 approved operational outcomes**. Former identifiers remain navigation metadata. The conceptual entity model was approved and then specialized for the three products without assuming common native agent, memory, permission or execution models. The six registers remain frozen. A review comment or UI revision does not authorize changes to their identities, relationships, objectives, variants or completion criteria.

Do not repeat the rejected taxonomy-as-document approach. Use cases state operational objectives; features identify concrete product facilities; mechanisms explain documented behavior. Historical implementation-profile records are authored configuration recipes, not an AWS-native resource or another reader-facing feature taxonomy. They remain for traceability but must not generate repetitive, interchangeable prose.

The instructional sequence begins with an agent's instructions, procedures/skills, informational context, tools and execution, then adds coordinated responsibilities and the workspace boundary. Workflows reuse that visual vocabulary. DevOps prioritizes incident operations, reporting, reliability improvement, operational knowledge, configuration/release assurance and operational reviews. Security follows assessment and finding lineage. FinOps follows instance context, source-backed analysis, tasks, automation and publication. This teaching priority is editorial, not an AWS ranking.

The ten capability dimensions remain a detailed reference after the introduction. DOC blue, AWS green and EXT orange identify ownership in diagrams; they do not reveal private AWS implementation. Presentations remain HTML-only. Their allocated exercise time must not be presented as measured live-agent completion time.

## Annotation interaction contract

Hover or focus a source-backed paragraph, heading, list, table, figure, slide element or presenter note. The nearby gutter exposes a block handle and direct comment action. Touch users tap the element. Text selection exposes a floating comment action. Shift selects a range, Ctrl/Command toggles blocks, and dragging selects blocks without reordering the document. No Review mode is required.

The anchored popup contains **note text, replies and note-level actions**. It does not contain source paths, copied source excerpts, author/type forms, collection filters, exports or backend controls. Persistent markers reopen the relevant thread. Source metadata is retained in exported review records, not removed from the editing contract.

The document header has **Search all** and **Annotations**. The Annotations menu provides the note collection, document-level notes, filtering, JSON and LLM-request export, import, explicit backend saving, and confirmed local clearing. Clearing one document or all local annotations removes their notes, comments and replies from browser storage; it does not delete previously saved backend copies.

Text and replies are persisted to localStorage on input, with stable note/reply IDs across subsequent edits. **Done closes the editor; it is not a save prerequisite.** Closing or reloading does not require another save action. Other mutations, including resolution, reopening, imports and clearing, also update localStorage automatically. Storage failures are reported visibly, while the current in-memory notes remain exportable. Browser storage is finite and may be unavailable; never display a successful local-save claim after a failed write.

The interface is a standalone, read-only contextual annotation implementation, not a licensed Tiptap Notion editor or collaborative rich-text application. Controls are rendered outside source-backed text, preserving quote offsets and table content. Existing storage keys and export schemas remain compatible with prior notes.

## Backend saving

The static documentation has no deployed authentication or storage backend. The user has authorized the **save option for a connected user**, implemented through a host adapter rather than an invented login service.

Register an adapter with `FrontierReview.setBackend(adapter)` after the reader loads, or assign `window.FrontierReviewBackend` beforehand. `getSession({signal})` returns `null` or an authenticated host user's nonempty string ID and optional display name. `saveReview(packet, {signal})` returns `{saved: true, id}` only after successful server persistence. The UI disables saving without the adapter and connected user, rechecks the session before saving, and requires a confirmation receipt before reporting success. Timeout, failure, missing confirmation or user changes do not discard local notes.

Backend saving is an **explicit snapshot operation**. Typing saves only locally and never triggers a remote write. A backend copy may be older than subsequent local edits. Clearing local annotations does not erase server copies.

The host/server must provide authentication, authorization, note ownership, CSRF protection where needed, TLS, limits and retention. It must derive identity from the actual session rather than trust a user ID inside review JSON. Do not place credentials in generated HTML or annotation localStorage. Adapter tests use controlled mocks; no production backend or server authorization was tested in this revision.

## Canonical source and tooling layout

| Location | Responsibility |
|---|---|
| `content/guides/<product>/index.md` | Guide introductions and official references |
| `content/guides/<product>/chapters/` | Chapter order, membership and introductory prose |
| `content/guides/<product>/sections/` | Technical explanation and procedures |
| `content/presentations/<product>/` | Slide Markdown, notes, timing and deck metadata |
| `content/diagrams/` | DOT/SVG source fences and captions |
| `content/registers/` | Frozen records and relationships in YAML/Markdown |
| `content/configuration/` | Rendering metadata |
| `content/site/` | Authored README, editorial, authoring and publishing instructions |
| `tools/docs/markdown_sources.py` | Parsing, source identities, relationships and coordinates |
| `tools/docs/build.py`, `renderer.py`, `source_views.py` | Compilation and compatibility projections |
| `tools/docs/source_review.py` | Source-map attachment and collection search index |
| `tools/docs/review.js`, `review.css` | Contextual popups, global menu, local persistence and backend adapter |
| `tools/docs/review_patch.py` | Exact-scope source patch validation/application |
| `tools/docs/contextual_check.py` | Existing contextual-selection and source-integrity browser journeys |
| `tools/docs/annotation_menu_check.py` | Note-only popup, automatic persistence, clear and backend-adapter checks |
| `tools/docs/review_check.py` | Source guards and combined annotation acceptance |
| `.github/workflows/document-suite.yml` | Build, browser checks, repeatability and generated commits |

Each source has YAML `id` and `kind`. Stable `<!-- block: identifier -->` markers identify selectable source blocks independently of their titles or filenames. Preserve these markers through ordinary prose edits. Source splits, merges or new IDs are explicit authoring changes, not automatic side effects of a comment.

Generated HTML, assembled guide Markdown, `catalog/*.json`, SVG files, search data and source maps are outputs, not alternate authoring locations. This root `WORKSTREAM.md` is operational handoff metadata, not a compiled product document. The independent `applications/` tree and its workflow remain outside scope.

## Source-scoped LLM correction contract

Annotations store their original document, source path, source/block IDs, exact Markdown excerpt, file and block SHA-256, Unicode code-point and UTF-8 byte intervals, and line ranges. Rendered text quotations separately use UTF-16 DOM coordinates. Do not conflate those units.

An editing model must return `frontier-source-patch/v1` bound to an open comment and stable review ID. Each edit names the authorized source, exact previous text and hashes. Text-scoped edits may alter only a unique verbatim quote in the selected Markdown block, preserving its prefix and suffix. Formatted, repeated or cross-block selections that cannot be mapped uniquely require an explicit block-level review. Fuzzy replacement and silent re-anchoring are prohibited.

The guard rejects stale versions, frozen records, generated paths, unrelated targets, symlinks, traversal, duplicate or overlapping edits and changed block identities. Validation is a dry run; application requires `--write` after a human has reviewed the diff. Comments and quoted material are untrusted data, not permission to execute commands or modify other files. LLM submission remains manual and separate from backend note saving.

## Completed work and evidence

M01–M02 established and froze the outcome catalog and product resource models. M03–M04 reviewed selected operating lifecycles and replaced generic cards with agent-first teaching and stable workflow diagrams. M05 moved published content to Markdown/YAML. M06–M07 added source mapping, review export, patch guards and CI. M08 replaced the rejected Review-toggle UI with contextual annotation. M09 now separates the note popup from global operations and adds input-time local persistence plus an optional connected-user save adapter.

The successful branch run `39966489147` covers document generation, frozen-record preservation, existing browser journeys, the added menu/autosave tests, and repeatable output. `qa/authoring-review.json` records zero errors, 2,184 verified source targets, all 15 patch-guard regression cases, mobile/desktop contextual checks, touch input, and the new menu tests. The new cases test note/reply/edit persistence without Done, stable IDs, export precision, clear confirmation/cancellation, backend session and save outcomes, and localStorage failure reporting.

These tests establish the recorded behavior, not editorial quality, current truth of every AWS claim, successful live AWS operation or production backend security. Human acceptance and a real host/backend integration test remain open.

## Remaining roadmap

**N01 — Technical and educational acceptance (P0).** Read guides end to end and review their slides as a first-time technical audience would. Verify the agent definition, instructions/skills/knowledge/tools distinctions, coordinated responsibilities and workspace before workflows. Remove repetition, ambiguous wording and promotional phrasing. Explain diagram arrows, ownership, outputs, authorizations and human decisions in surrounding prose. Automated checks alone cannot close this stage.

**N02 — Official-source accuracy audit (P0).** Recheck high-impact AWS claims: availability, account/Region constraints, permissions, retained state, trigger/cancellation behavior, publication and revalidation. Distinguish AWS behavior from authored procedures, synthetic evidence and inference. Preserve claim-level citations and qualify differing retrieved versions. Do not infer undisclosed internal algorithms or shared runtimes from similar naming.

**N03 — Human review/edit acceptance (P0).** Demonstrate a hover/touch/focus note, text/range annotation, persistent marker, automatic local reload, global export and clear, and an approved source edit. Inspect matching JSON/LLM exports and precise source targets, validate a model patch, review its diff, apply explicitly, rebuild and inspect the result. Rejection of stale, frozen and ambiguous proposals is part of acceptance. No UI screenshot or automated test substitutes for the user's approval of the experience.

**N04 — Compiler, accessibility and search hardening (P1).** Exercise source additions, moves, renaming/deletion, nested blocks and tables, narrow layouts, nearby annotations, keyboard focus, search relevance, large-document performance and printing. Maintain stable source identity and actionable errors. Check existing notes remain accessible across rendered representations.

**N05 — Security and release controls (P1).** Expand adversarial import/patch cases, including malformed packets, stale/missing targets, Unicode offsets, path traversal, frozen records, overlaps and prompt-injection text. Preserve manual diff review. Ensure the branch validated is the branch published; avoid concurrent contributor changes during generated-output pushes. Never force-push to hide a conflict.

**N06 — Production backend integration (P1 when a host is available).** Connect the documented adapter to the actual authenticated session and persistence API. Test server-derived ownership, authorization, CSRF, response/error semantics and retention. Shared multi-user editing and direct LLM submission remain separately scoped; they are not delivered by this adapter.

**N07 — Final quality and repository hygiene (P1).** Keep one canonical content source, remove superseded generators and stale navigation, and maintain current QA and handoff records. Preserve the independent application and Git history. Do not declare complete editorial acceptance while substantive review remains open.

## Working procedure

Start from current `main` and read this handoff, `AUTHORING.md`, `PUBLISHING.md` and the current QA. For substantive changes, create a documentation branch. Edit canonical Markdown or the relevant UI/tooling source; preserve all frozen semantics and block IDs. Do not put export, backend or clear controls back inside the note popup and do not introduce a Save prerequisite for local persistence.

Run the following after installing Graphviz and the documented Python/Chromium dependencies:

    python tools/docs/build.py
    python tools/docs/check.py --browser
    python tools/docs/review_check.py

Inspect the affected generated pages as well as test records. A second build must preserve authored bytes and reproduce outputs in the same environment. Source review and browser rendering are distinct checks. For a model-produced correction:

    python tools/docs/review_patch.py validate review.json patch.json
    python tools/docs/review_patch.py apply review.json patch.json --write

Review the dry-run diff before the second command. Rebuild and rerun acceptance after applying it. Keep private review exports local unless their publication is explicitly authorized. Commit the maintained source and generated outputs through Git; do not create ZIP archives or parallel editions.

The immediate next steps are N01/N03 human acceptance and, only with an authorized host available, a real backend-adapter integration test. The approved model and use-case catalog are not being redesigned.
