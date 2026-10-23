# AWS operational agents

Open `index.html` from a repository checkout. HTML files work locally without a server. GitHub file preview shows source rather than running the controls.

## Reading paths

| Read | Location |
|---|---|
| Learn the model and operating procedures | [Guides](index.html) |
| Apply an operational workflow | [Use cases](catalog/index.html) |
| Look up product objects and relationships | [Resource model](catalog/resource-models.html) |
| Present the material | [HTML presentations](presentations/index.html) |

Guides distinguish workspace organization, definition, context, invocation, integrations, network connectivity, execution controls, managed functions, outputs, and administration. They have chapter navigation and one search. Each use case has a dedicated page with its narrative, workflow, configuration recipes, verification criteria, and technical references. The product guides explain concrete platform facilities and their operating mechanisms by capability dimension. The frozen dependency registers supply references, not a product taxonomy.

## Product editions

| Subject | Guide | Markdown | Presentation | Duration |
|---|---|---|---|---|
| AWS DevOps Agent | [Read](guides/devops.html) | [Source](guides/devops.md) | [Slides](presentations/devops.html) | 80 min, including 8 min exercise |
| AWS Security Agent | [Read](guides/security.html) | [Source](guides/security.md) | [Slides](presentations/security.html) | 67 min, including 8 min exercise |
| AWS FinOps Agent | [Read](guides/finops.html) | [Source](guides/finops.md) | [Slides](presentations/finops.html) | 63 min, including 8 min exercise |
| Cross-service architecture | [Read](guides/architecture.html) | [Source](guides/architecture.md) | [Slides](presentations/architecture.html) | 38 min, including 4 min exercise |

## Source ownership and build

The six JSON registers in `catalog/` are frozen at `dace05a3ce6aaae02470a817584b8ca3a4cc95be`. Reader navigation and page composition are maintained in `tools/docs/reader.py`, `reading.css`, and `reading.js`. This revision preserves the model, case selection, and workflow semantics. Product exposition follows the supplied capability outline; targeted source qualifications are recorded in qa/exposition-review.json. Former identifiers remain lookup metadata in `catalog/aliases.json`; they are not a reader-facing chapter.

```text
guides/          Canonical guide prose and HTML books
catalog/         Frozen records, use-case pages, and resource reference
presentations/   HTML decks and notes
assets/diagrams/ Source-linked SVG diagrams
tools/docs/      One renderer and validation toolchain
qa/              Review and validation records
examples/        Synthetic worked evidence
applications/    Independent application; not modified
```

```sh
python -m pip install -r tools/docs/requirements.txt
python -m playwright install chromium
python tools/docs/build.py
python tools/docs/check.py --browser
```

Graphviz (`dot`) is also required. [Validation scope](VALIDATION.md), [source coverage](guides/coverage.md), and [publishing instructions](PUBLISHING.md) distinguish document checks from live service testing. Git retains previous versions; no manual archives are maintained.
