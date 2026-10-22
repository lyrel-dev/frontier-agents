# AWS operational agents

Open `index.html` from a repository checkout. The guides, catalog, and presentations work locally; GitHub source preview does not execute HTML controls.

| Subject | Guide | HTML presentation | Duration |
|---|---|---|---|
| AWS DevOps Agent | [HTML](guides/devops.html) / [Markdown](guides/devops.md) | [Slides](presentations/devops.html) / [Notes](presentations/devops-notes.md) | 58 min including 8 min exercise |
| AWS Security Agent | [HTML](guides/security.html) / [Markdown](guides/security.md) | [Slides](presentations/security.html) / [Notes](presentations/security-notes.md) | 56 min including 8 min exercise |
| AWS FinOps Agent | [HTML](guides/finops.html) / [Markdown](guides/finops.md) | [Slides](presentations/finops.html) / [Notes](presentations/finops-notes.md) | 49 min including 8 min exercise |
| Shared Architecture | [HTML](guides/architecture.html) / [Markdown](guides/architecture.md) | [Slides](presentations/architecture.html) / [Notes](presentations/architecture-notes.md) | 26 min including 4 min exercise |

The programme is **189 minutes including 28 minutes of prepared-result exercises**. Questions and breaks are additional.

## Operational use cases

[Read and search the catalog](catalog/index.html). All 54 workflows are narrated in prose and grouped by operational purpose. The catalog is an application layer, not a competing definition of platform capabilities.

## Repository layout

```text
guides/          Maintained Markdown guides and generated HTML
catalog/         Maintained narrative JSON; generated HTML and Markdown
presentations/   Generated HTML decks and presenter notes
assets/diagrams/ Generated, accessible SVG figures
examples/        Synthetic evidence used in worked examples
tools/docs/      Rendering, diagrams, presentation outline, and checks
qa/              Current validation and source-review records
applications/    Independently maintained readiness-console application
```

Each guide introduces the agent and its resource model, describes supported integrations, explains knowledge production and retrieval, and then follows operational workflows. Stable identifiers connect use cases, mechanisms, diagrams, and presentation references. Superseded entry-point directories and generators are removed; Git retains history.

## Build and validate

Install Graphviz (`dot`) and Python dependencies, then run:

```sh
python -m pip install -r tools/docs/requirements.txt
python -m playwright install chromium
python tools/docs/build.py
python tools/docs/check.py --browser
```

See [publishing](PUBLISHING.md), [editorial rules](EDITORIAL_STANDARD.md), [source coverage](guides/coverage.md), and [validation](VALIDATION.md). No live AWS operation is represented by the synthetic examples or document checks.
