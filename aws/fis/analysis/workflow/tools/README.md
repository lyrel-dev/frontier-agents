# Workflow diagram rendering

The three Mermaid sources in `../diagrams/` match the three embedded blocks in `../model.md`. The class diagrams cover all six core entities and their owned values. The lifecycle diagram shows local orchestration phases.

```bash
cd aws/fis/analysis/workflow/tools
npm ci
npm run diagrams
```

The renderer uses Pele 1.6.0 on Node.js 20 or later. It parses the maintained Mermaid, rejects embedded-source mismatches and produces standalone SVG with titles/descriptions. `../diagrams/manifest.json` records source, renderer and output hashes. It does not modify the Markdown or Mermaid sources. If a source changes, update its embedded block, regenerate and inspect the SVG.

These diagrams belong to the generalized proposal. They are deliberately separate from the five provider ER diagrams and the FIS PDF renderer.
