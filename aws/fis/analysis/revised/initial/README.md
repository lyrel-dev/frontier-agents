---
id: fis-revised-initial-interface
title: Initial FIS experiment interface
type: interface-reference
service: aws-fis
status: preserved-reviewed-prototype
version: "1.2"
created: "2026-11-05"
updated: "2026-11-05"
tags: [aws, fis, ui, initial, synthetic]
aliases: [Initial FIS Observatory]
related: [../README.md, ../docs/initial/report.md, ../docs/initial/REVIEW.md, ../suggested/README.md]
---

# Initial FIS experiment interface

This is the reviewed FIS Observatory interface preserved from commit `1b5ae1bd11fc61a2701d74ea89ccce2721889ef0`. It remains the first interface in the [comparison workspace](../index.html). The suggested workflow interface is available as the second choice.

The model, fixtures, stylesheet and 27 model tests are preserved byte-for-byte. The HTML and rendering code change only documentation and diagram URLs so the copied interface uses this package's Obsidian Markdown reports and shared diagrams. [source-manifest.json](source-manifest.json) records the original and packaged hashes.

Open [index.html](index.html) directly or use the comparison workspace. The original five synthetic experiments, replay controls, simulated stop, action details, selected resources, evidence filters, diagrams and observed-snapshot export remain available. All operational data is synthetic and no AWS calls are made.

## Verify

```bash
node --test aws/fis/analysis/revised/initial/app/tests/model.test.cjs
```

The prior review and validation are preserved as baseline records in [the initial notes](../docs/initial/README.md). Current package checks belong to [VALIDATION.md](../VALIDATION.md).
