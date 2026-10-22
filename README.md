<!-- USE-CASE-CATALOG -->
## Day-to-day use case catalog

[Open the grouped and searchable catalog](catalog/index.html). It contains **54** use cases: 22 for AWS DevOps Agent, 16 for AWS Security Agent, and 16 for AWS FinOps Agent. Each record identifies delivery mode, cadence, availability, inputs, reviewable output, constraints, canonical guide sections and official sources.
<!-- /USE-CASE-CATALOG -->

# AWS agent engineering guides

Open `index.html` after cloning the repository. Reports and presentations are separate, self-contained HTML pages; GitHub source previews do not execute their controls.

| Subject | Structured report | Presentation | Timing |
|---|---|---|---|
| AWS DevOps Agent | [Report](guides/devops.html) / [Markdown](guides/devops.md) | [HTML presentation](presentations/devops.html) / [Notes](presentations/devops-notes.md) | 44 min / 8 min exercise |
| AWS Security Agent | [Report](guides/security.html) / [Markdown](guides/security.md) | [HTML presentation](presentations/security.html) / [Notes](presentations/security-notes.md) | 44 min / 8 min exercise |
| AWS FinOps Agent | [Report](guides/finops.html) / [Markdown](guides/finops.md) | [HTML presentation](presentations/finops.html) / [Notes](presentations/finops-notes.md) | 39 min / 8 min exercise |
| Shared Architecture | [Report](guides/architecture.html) / [Markdown](guides/architecture.md) | [HTML presentation](presentations/architecture.html) / [Notes](presentations/architecture-notes.md) | 22 min / 4 min exercise |

The programme remains **124 minutes including 28 minutes of prepared-result exercises**. Questions and breaks are additional.

## Reading and presentation structure

Reports have numbered chapters, a nested table of contents, a chapter map, chapter/type filters, stable section links and links to the relevant slides. Chapter groups distinguish platform overview and capabilities, access and integrations, mechanisms, operations, worked examples, troubleshooting, and evidence. The shared architecture guide uses corresponding comparison groups.

Standalone HTML decks include chapter navigation, an agenda, slide selection, keyboard controls, fullscreen, speaker notes, session and slide timers, source links and slide-only printing. They open directly as presentations.

## Maintained sources

- `guides/*.md`: canonical descriptive content, with explicit chapter and section headings.
- `tools/docs_structure.py`: chapter membership and presentation chapter boundaries.
- `tools/lesson_plan.py`: curated slide content and delivery budgets.
- `tools/docs_build.py`: HTML generation; no binary presentation output.

No competing capability catalog or historical copy is retained. Prior editions are available through Git. The [readiness-console application](applications/aws-validation-console/README.md) and its workflow are outside the documentation build.

## Build and check

```sh
python -m pip install -r tools/docs-requirements.txt
python -m playwright install chromium
python tools/docs_build.py
python tools/docs_check.py --browser
```

See [coverage](guides/coverage.md), [validation](VALIDATION.md), [editorial rules](EDITORIAL_STANDARD.md) and [publishing](PUBLISHING.md). This organization-only revision retains existing product references; no new AWS source audit or live execution is claimed.
