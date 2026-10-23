---
id: authoring-guide
kind: page
title: Markdown authoring and source-scoped review
output: AUTHORING.md
---

<!-- block: authoring-introduction -->
# Markdown authoring and source-scoped review

The authored documentation is in `content/`. Every source is UTF-8 Markdown with YAML front matter. The compiler assembles the existing `guides/`, `catalog/`, and `presentations/` HTML documents. Their URLs, educational order, and approved use cases are retained. Generated Markdown, JSON, SVG, HTML, search data, and source maps are outputs, not editing targets.

<!-- block: authoring-layout -->
## Source layout

| Directory | Authoring responsibility |
|---|---|
| `content/guides/<product>/index.md` | Guide introduction and official-reference definitions |
| `content/guides/<product>/chapters/` | Chapter metadata, membership, ordering, and introductions |
| `content/guides/<product>/sections/` | Technical explanations and operating procedures |
| `content/presentations/<product>/index.md` | Presentation metadata and chapter grouping |
| `content/presentations/<product>/<number>.md` | Slide body, presenter notes, timing, and references |
| `content/diagrams/` | Diagram captions and DOT or SVG fenced source |
| `content/registers/` | Approved records and their relationships, represented in YAML and Markdown |
| `content/configuration/` | Presentation geometry and compiler metadata, not application credentials |
| `content/site/` | Repository authoring and publishing instructions |

The approved records are frozen. Moving their representation from JSON to Markdown is not authorization to rewrite their meaning. The compiler reconstructs the JSON projections and the regression tests compare them with the approved baseline.

<!-- block: authoring-frontmatter -->
## Front matter and blocks

A section has a stable identity independent of its filename or heading:

```yaml
---
id: D-90
kind: section
product: devops
title: An agent, its configuration, and one execution
order: 1
---
```

The body contains ordinary Markdown. An explicit `<!-- block: ... -->` comment precedes each selectable block. These identifiers are not positional: retain them when editing or moving the block. Do not reuse an identifier elsewhere. The compiler does not modify authored sources. Source splitting, merging, or reordering is an explicit authoring operation, not an automatic effect of a review comment.

Small relationship fields remain in YAML. Long prose in approved record files lives in named Markdown fields. The `$markdown` values in their front matter point to these fields; `$record` values connect a register to another source record. They are compiler references, not AWS concepts. Nested metadata can be edited in Obsidian source mode; this is not an Obsidian plugin or a promise of support for all Obsidian extensions.

<!-- block: authoring-slides -->
## Presentation sources

Each slide is a Markdown file. Its YAML identifies its product, title, order, layout, allocation in seconds, guide references, and existing use-case references. Diagram slides use a Markdown image reference to a maintained diagram; table slides use Markdown tables. The `## Presenter notes` section supplies the presenter narrative. Timing remains data in the header; the compiler calculates presentation totals rather than maintaining another total in prose.

For a new slide, add the file and update the presentation chapter membership in its `index.md`. For a new guide section, add its stable section ID to the relevant chapter manifest. The compiler rejects orphan or duplicate section membership. Do not add slide prose to Python dictionaries.

<!-- block: authoring-build -->
## Build and serve

```sh
python -m pip install -r tools/docs/requirements.txt
python -m playwright install chromium
python tools/docs/build.py
python tools/docs/check.py --browser
python tools/docs/review_check.py
python -m http.server 8000 --bind 127.0.0.1
```

Graphviz must be installed for DOT diagrams. Open the local server's `index.html`. Direct file opening still supports reading and search. Use HTTP on a single local origin for predictable cross-page annotation storage; browser behavior for local-file storage is not consistent.

<!-- block: authoring-review -->
## Select and annotate

Select **Review** in the lower toolbar. Each source-backed paragraph, heading, list, table, or figure exposes a block handle. Click selects a block; Shift-click selects a range; Ctrl/Command-click toggles individual blocks. Dragging across handles selects a range. Native text selection provides a comment action for a quote. **Document note** associates a note with the source files contributing to the assembled document.

Use the side panel to add notes, reply, edit, resolve, reopen, or delete a local thread. Notes do not change the published text. The interaction is a standalone, read-only implementation of Notion-style block selection; it does not use Tiptap's licensed Notion template or hosted comments service and is not a general rich-text editor.

**Search all** searches across guides, slides, diagram text, and mapped catalog records. `Ctrl/Command+K` opens the search dialog. A result opens the corresponding chapter or slide. `Ctrl/Command+Alt+M` opens a comment for the current selection.

<!-- block: authoring-storage -->
## Storage and sharing

Annotations are stored in this browser's local storage, under the site's origin. They are not a multi-user server database. Clearing browser data removes them. Export regularly. Import merges note identifiers and timestamps; older source hashes remain unchanged and are shown as stale rather than silently reattached. Keep exported reviews out of the public repository unless you have reviewed their contents.

The reader makes no LLM or analytics requests. **Export JSON** saves the machine-readable packet. **Export LLM request** or **Copy LLM request** provides the instructions and source excerpts to submit to an editing model. No provider token is placed in the HTML, and no comments are sent automatically.

<!-- block: authoring-contract -->
## Review export contract

Each annotation contains its type, author, text, replies, status, document, and selected source targets. Each target includes:

| Field | Meaning |
|---|---|
| `source_id`, `block_id`, `path` | Stable source and block identities and repository-relative Markdown path |
| `file_sha256`, `block_sha256` | Exact version of the file and selected source block |
| `start_char`, `end_char` | Half-open Unicode code-point interval in the source file |
| `start_byte`, `end_byte` | Corresponding half-open UTF-8 byte interval |
| `start_line`, `end_line` | Human-readable 1-based source line range |
| `markdown` | Exact source excerpt, including Markdown syntax |
| `field` | `title` for a selected YAML title scalar; otherwise a body block |
| `protected` | Display hint for an approved/frozen record; the patch guard derives protection independently |

For text selection, a separate quote selector carries the exact rendered text, prefix/suffix context, and UTF-16 positions within the first and last rendered blocks. These DOM offsets are not passed off as Markdown offsets. Inline formatting can make a rendered quote discontinuous in Markdown. The exact source block remains the editing unit; the quote tells the reviewer which portion requires attention.

<!-- block: authoring-patches -->
## Validate a model-produced patch

The editing model must return `frontier-source-patch/v1` JSON with the exported `review_id`. Each edit names an open `comment_id`, source `path`, `block_id`, expected file/block hashes, exact `before` excerpt, and replacement `after` Markdown. Generated documents, unrelated blocks, symlinks, traversal paths, stale versions, duplicate or overlapping edits, and frozen registers are rejected.

```sh
python tools/docs/review_patch.py validate review.json patch.json
python tools/docs/review_patch.py apply review.json patch.json --write
python tools/docs/build.py
python tools/docs/check.py --browser
python tools/docs/review_check.py
```

Validation prints a diff and does not write. Application requires `--write`, preflights every file before replacing any file, and limits replacements to the selected source blocks. The optional `--review-sha256` argument pins a separately trusted reviewer-export digest. A stale anchor requires renewed review; the tool never searches for an approximate replacement. It does not execute commands or instructions contained in review text.

Inspect the diff and the rebuilt result before committing. Source anchoring prevents unrelated edits; it does not establish that the proposed wording is accurate. Changes to an approved model or use case require separate authorization outside this patch path.
