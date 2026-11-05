---
id: fis-revised-package
title: AWS FIS revised analysis and interface comparison
type: package-index
service: aws-fis
status: reviewed-mock-package
version: "1.0"
created: "2026-11-05"
updated: "2026-11-05"
tags: [aws, fis, analysis, assessment, ui, obsidian]
aliases: [FIS revised analysis, FIS initial and suggested interfaces]
related: [docs/README.md, initial/README.md, suggested/README.md, REVIEW.md, VALIDATION.md]
---

# AWS FIS revised analysis and interface comparison

This self-contained package preserves the initial FIS operator interface and adds a suggested interface for the reviewed generalized assessment model. The comparison presents **Initial** first and **Suggested** second. Both interfaces use deterministic synthetic data; neither contacts AWS or runs infrastructure operations.

## Open the interfaces

Open [index.html](index.html) to switch between the two interfaces without discarding either view's current state. The initial FIS interface is selected by default. The same page can open directly to [the suggested interface](index.html#suggested).

| Interface | Purpose | Standalone entry point |
| --- | --- | --- |
| **01 · Initial** | Inspect native FIS experiments, named actions, selected resources, telemetry and evidence. This is the preserved, reviewed FIS Observatory. | [initial/index.html](initial/index.html) |
| **02 · Suggested** | Inspect a service assessment containing workflow steps, attempts, checks, evidence and independent cleanup. | [suggested/index.html](suggested/index.html) |

The interfaces are buildless HTML, CSS and JavaScript. Keep the package directories together. For local HTTP serving from the repository root:

```bash
python3 -m http.server 8080 --directory aws/fis/analysis/revised
```

Then open `http://localhost:8080/`. All scenario times are explicitly UTC. Replay uses a fixed synthetic clock. Controls labelled as simulation affect browser memory only; reload restores the fixtures.

## Read the notes in Obsidian

Open `revised` as a vault, or place this directory inside an existing vault. Start with [docs/README.md](docs/README.md). Every Markdown document has YAML properties, a stable note ID and local navigation. Relative Markdown links work in both Obsidian and repository viewers.

The sequence keeps the reviewed native model before the suggested generalization:

1. [Initial FIS analysis](docs/initial/report.md): official API entities, relationships, mutation boundaries and derived-data limits.
2. [Suggested assessment model](docs/suggested/model.md): six core entities, ownership, execution/assessment semantics and finalization.
3. [Suggested API](docs/suggested/api.md) and [adapter contracts](docs/suggested/adapters.md): writable boundaries, idempotency, evidence claims and provider integration requirements.
4. [Diagram index](diagrams/README.md): all five FIS ER diagrams and all three generalized model/lifecycle diagrams.
5. [Current review](REVIEW.md) and [current validation](VALIDATION.md): what this package implements and what was actually verified.

Diagram documents contain YAML properties, a caption, a rendered SVG and the maintained Mermaid block. Machine-readable JSON schemas/catalogues and YAML scenario examples are supporting code artifacts; their documentation is provided as Obsidian notes. The revised reports are Markdown documents. The earlier PDF remains part of the prior baseline, with its provenance recorded in the baseline review notes.

## Scope and provenance

The initial interface comes from reviewed commit `1b5ae1bd11fc61a2701d74ea89ccce2721889ef0`. Its source manifest identifies preserved bytes and documentation-path adaptations. The existing `aws/fis/analysis` deliverables remain intact; the new package lives entirely under `analysis/revised`.

The generalized model is an application proposal. Its query/capture/cleanup operation names are not AWS API names. The suggested UI demonstrates that proposal through recorded synthetic observations; it does not provide a scheduler, live API server, CEL evaluator, authenticated receiver or AWS adapter.

## Verify

Checks require Node.js, Python 3.10 or later, `PyYAML` and `jsonschema`. The browser interfaces have no runtime dependencies. From the repository root:

```bash
python3 aws/fis/analysis/revised/tools/check_package.py
node --test aws/fis/analysis/revised/initial/app/tests/model.test.cjs
node --test aws/fis/analysis/revised/suggested/app/tests/model.test.cjs
```

See [VALIDATION.md](VALIDATION.md) for current results, browser checks and limitations. No validation result in this package establishes real fault behavior or production readiness.
