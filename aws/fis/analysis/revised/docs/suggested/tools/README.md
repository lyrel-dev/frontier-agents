---
id: aws-fis-revised-docs-suggested-tools-readme
title: Assessment workflow diagram rendering
type: tooling
service: aws-fis
status: reviewed
version: '0.2'
created: '2026-11-05'
updated: '2026-11-05'
tags:
- aws
- fis
- analysis
- revised
- tooling
aliases:
- Assessment workflow diagram rendering
related:
- ../model.md
- ../../../diagrams/suggested/README.md
source_commit: 1b5ae1bd11fc61a2701d74ea89ccce2721889ef0
source_path: aws/fis/analysis/workflow/tools/README.md
---

# Workflow diagram rendering

The three Mermaid sources in `../../../diagrams/suggested/` match the three embedded blocks in `../model.md`. The class diagrams cover all six core entities and their owned values. The lifecycle diagram shows local orchestration phases.

```bash
cd aws/fis/analysis/revised/docs/suggested/tools
npm ci
npm run diagrams
```

The renderer uses Pele 1.6.0 on Node.js 20 or later. It parses the maintained Mermaid, rejects embedded-source mismatches and produces standalone SVG with titles/descriptions. `../../../diagrams/suggested/manifest.json` records source, renderer and output hashes. It does not modify the Markdown or Mermaid sources. If a source changes, update its embedded block, regenerate and inspect the SVG.

These diagrams belong to the generalized proposal. They are deliberately separate from the five provider ER diagrams and the FIS PDF renderer.

The standalone Obsidian notes also embed the exact Mermaid source. Package validation checks their parity separately from this rendering command. The five initial FIS SVGs are preserved byte-for-byte from their reviewed baseline; their historical renderer is not duplicated here.
