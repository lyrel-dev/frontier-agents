---
title: "Operational analysis proposal: validation record"
type: documentation-validation
date: '2026-11-05'
status: checked
implementation_tests: not-executed
tags:
  - operational-analysis
  - review
  - diagrams
---

# Validation record

## Scope

This record covers the proposed model, RPC contract, AWS evidence annex and complete class diagram. It does not establish a running application, deployed API, evaluator correctness or live AWS integration. The [16 adversarial acceptance cases](../DESIGN_REVIEW.md) remain explicitly **not executed**.

The proposal was reconciled with the latest committed [consolidated design principles](../../../../../../consolidated-operations-console/DESIGN_PRINCIPLES.md): every entity is versioned, a version is not another entity, owned values inherit their owner's version, and the editable presentation diagram uses Draw.io. The seven entities remain a separate analysis bounded context.

## Executed document and diagram checks

From `aws/devops-agent/analysis`:

```bash
python3 tools/render-proposal-drawio.py --check
python3 tools/check.py
```

The proposal checker validates all seven classes, their visible common version metadata, immutable-fact policies, all eight association endpoints and cardinalities, accessible SVG metadata, and hash bindings for the source, SVG, PNG, render report, wrapper, renderer and runtime pin. The package checker verifies YAML front matter and local links, declared diagram publications and source/render hashes. It also confirms that the existing native-model application's deterministic bundle still matches its unchanged sources.

The [API proposal](../API.md) contains six JSON examples checked for JSON syntax. These examples are illustrative requests and responses; parsing them does not prove an API implementation. The model/API review checked entity ownership, immutable versions, input selection, receipt coverage, assertion-instance completeness, predicate-specific adequacy, evidence reuse, operator decisions and the separation of collection from interpretation.

## Actual Draw.io rendering

The canonical source is [OA01-domain-classes.drawio](../diagrams/OA01-domain-classes.drawio). The exported [SVG](../diagrams/OA01-domain-classes.svg) and [PNG](../diagrams/OA01-domain-classes.png) have a **1200 × 1410** canvas. Draw.io **32.6.10**, pinned to source commit `c72c9a98b7a6ce392556ed04c05e0ff19f43f5c3`, decoded and rendered the source through its native SVG engine. JSDOM **26.1.0** and `@napi-rs/canvas` **0.1.100** supplied DOM primitives and font metrics. Inkscape **1.4** rasterized the exported SVG.

The [render report](../diagrams/render-report.json) records:

- Seven classes and eight associations retained through a native Draw.io codec round trip.
- Zero class overlaps, connector intrusions, label intrusions or text overflows.
- Passing deliberate geometry controls for overlapping classes, a connector through a class and separated geometry.
- Source and SVG hashes tied to the actual render.

Independent SVG exports were byte-identical after the same numeric-dimension normalization. The [manifest](../diagrams/manifest.json) retains artifact and tool hashes. The SVG SHA-256 reviewed here is `5de3c19f0d653ef5edc5344c68000c817f2cfb6480f46cdd2f632d4f0961ee87`.

## Visual review

The complete PNG was inspected directly after rendering. All seven class names, common version fields, selected domain fields, eight relationship labels and sixteen endpoint multiplicities are visible. The layout has at most three entity boxes across, readable spacing, no crossing connectors and no clipped labels. Owned values and immutable version-1 facts are explained on the canvas. Arrows are explicitly described as references/ownership rather than delete cascades.

This was raster inspection of the actual Draw.io SVG export. No browser or installed Draw.io desktop inspection is claimed. The superseded Mermaid draft and its earlier render evidence were removed, leaving one authoritative editable figure.

## Regeneration

Use the pinned runtime and dependencies documented in the [consolidated diagram instructions](../../../../../../consolidated-operations-console/diagrams/README.md). From the parent analysis directory:

```bash
DRAWIO_RUNTIME=/path/to/pinned-drawio \
CONSOLE_DIAGRAM_NODE_MODULES=/path/to/node_modules \
python3 tools/render-proposal-drawio.py --write
```

Then repeat the two checks above and inspect the PNG. Regeneration updates the artifact and tool hash bindings; visual review must correspond to those outputs. Offline `--check` validates retained evidence and does not rerun the Draw.io engine.

## Remaining acceptance work

Formal payload/evaluator schemas, adapter conformance, atomic persistence/publication, cloud captures, authorization enforcement and operator usability still require implementation evidence. A readable, structurally consistent class diagram does not prove those behaviors. The existing Lens prototype's earlier tests also do not validate this new proposal.
