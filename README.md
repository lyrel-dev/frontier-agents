# AWS operational agents

Technical guides, a searchable use-case catalog, resource diagrams, and HTML presentations for AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent. The approved entity model and 30 use cases remain unchanged.

## Read and review

| Material | Entry point |
|---|---|
| Product guides | [Contents](index.html) |
| Operational tasks | [Use cases](catalog/index.html) |
| Entity definitions and relationships | [Resource model](catalog/resource-models.html) |
| Teaching editions | [HTML presentations](presentations/index.html) |
| Authoring, annotations, and source patches | [Authoring guide](AUTHORING.md) |

Open `index.html` from a checkout, or run `python -m http.server 8000 --bind 127.0.0.1`. HTTP on a single local origin is recommended for shared annotation storage across pages. GitHub's HTML preview displays source rather than running the reader.

Use **Search all** to search the collection. Use **Review** to select a block, range of blocks, or text quote and add a comment. **Document note** records a whole-document observation. Export notes as JSON or as an LLM editing request. Nothing is sent to an external model automatically.

## Canonical sources

All maintained document content is authored in Markdown files with YAML front matter under `content/`. Guide sections, chapter ordering, slide bodies and presenter notes, diagram source, and approved record definitions have explicit source identities. HTML, assembled guide Markdown, catalog JSON, SVG, and search indexes are compiler outputs.

```text
content/
  guides/          Introductions, chapter manifests, and technical sections
  presentations/   Slide Markdown, notes, timing, and deck manifests
  diagrams/        DOT/SVG fences and captions
  registers/       Frozen records and relationships in YAML/Markdown
  configuration/   Rendering metadata
  site/            Repository and authoring documentation
tools/docs/        Compiler, review UI, validation, and exact-source patch guard
guides/            Generated guide Markdown and HTML
catalog/           Generated use-case pages and JSON projections
presentations/     Generated HTML decks and presenter notes
assets/            Generated diagrams, review assets, and search index
qa/                Validation evidence
applications/      Independent application; not modified by this migration
```

## Build and validate

```sh
python -m pip install -r tools/docs/requirements.txt
python -m playwright install chromium
python tools/docs/build.py
python tools/docs/check.py --browser
python tools/docs/review_check.py
```

Graphviz (`dot`) must also be installed. Do not edit generated documents. See [AUTHORING.md](AUTHORING.md) for front matter, stable block IDs, source offsets, review exports, and guarded model-produced patches.

## Review boundary

Comments are browser-local annotations, not a collaborative cloud service. JSON exports contain source paths, immutable block IDs, exact source excerpts, file/block hashes, and separate rendered-text quote selectors. The patch tool rejects stale, unrelated, generated-file, and frozen-record edits; it defaults to a dry run.

The UI implements read-only Notion-style selection gestures. It is not a full Tiptap editor, and comments do not directly mutate source files. Published content and browser tests do not establish live AWS behavior. [Validation](VALIDATION.md) records the checks performed. Git history retains previous editions; no manual archives are maintained.
