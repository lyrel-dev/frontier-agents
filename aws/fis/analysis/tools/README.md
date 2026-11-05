# Report and diagram renderer

The canonical report is [`../report.md`](../report.md). The five canonical ER models are the `.mmd` files in [`../diagrams/`](../diagrams/). Their actual Mermaid code is also embedded in the report, so the Markdown remains self-contained.

## Regenerate

From the repository root:

```bash
python3 aws/fis/analysis/tools/render_report.py
```

The command writes five SVGs in `diagrams/`, the reviewed `aws_fis_experiment_action_model.pdf`, and `tools/render-manifest.json`. It validates the canonical inputs before writing outputs. The command does not access AWS or use the network.

Use `--svg-only` to regenerate diagram assets and update the manifest while preserving the existing PDF and its original build record. If any report input changed, the manifest marks that PDF `stale`; generating new diagrams cannot make an old PDF current. A complete render is required to clear that state.

Validate the existing committed artifacts without rebuilding or changing files:

```bash
python3 aws/fis/analysis/tools/render_report.py --check
```

The check rejects changed canonical inputs, mismatched SVG content, missing or changed PDF bytes, stale PDF build inputs, and divergent metadata. It does not regenerate an artifact before checking it.

Requirements: Python 3.10 or newer and ReportLab. The committed output was generated with ReportLab 4.4.9 and DejaVu Sans / DejaVu Sans Mono fonts. The renderer discovers DejaVu fonts at the paths listed in `register_fonts()` and falls back to PDF base fonts if none are available. Use the same fonts and ReportLab version for identical output bytes.

## Model fidelity

The renderer parses entity names, attributes, primary/foreign-key annotations, relationship labels, and cardinalities from the canonical Mermaid. It uses a reviewed layout for each of these five diagrams. It fails if entities or relationships differ from that layout, if embedded Mermaid differs from its source file, or if report source references differ from `sources.json`. Source IDs and URLs must be unique, every citation must resolve, and each canonical diagram must appear exactly once. Both full and SVG-only builds apply those checks.

The report edition and review date come from Markdown front matter. Section headings that open a diagram stay with that diagram; conditional page breaks and paragraph widow/orphan rules avoid isolated headings and nearly empty continuation pages.

SVG and PDF figures share the same vector scene. SVGs include a title, description, and selectable text. Numeric endpoint labels are a direct rendering of the Mermaid multiplicities:

| Mermaid endpoint | Rendered multiplicity |
| --- | --- |
| `||` | `1` |
| `o|` | `0..1` |
| `|{` | `1..N` |
| `o{` | `0..N` |

These are logical domain relationships. Unloaded cache records do not change them. Teal entities represent FIS data or account/Region scope, amber entities represent proposed application records, and blue entities represent external resources or observations. Full names and field inventories remain in the report; the diagrams present the corresponding relationships.

This script is a bounded renderer for this report's Markdown and Mermaid subset. It is not a general Markdown or Mermaid engine. A model change can require updating the explicit node positions and routes in `LAYOUTS`. Reinspect the generated figures after any such change.

## Verification performed

The reviewed edition 1.2 build produced a 24-page PDF, 14 report sections, 5 vector diagrams, and 53 official source references. Validation checked:

- Byte equality of the five embedded Mermaid blocks and standalone sources.
- Exact agreement between Markdown source definitions and `sources.json`, with unique source IDs and URLs.
- Successful XML parsing of all five SVGs.
- Entity/relationship counts of `5/5`, `10/12`, `8/7`, `11/12`, and `7/7` across diagrams 1 through 5.
- PDF text extraction, all section headings, all five figure titles, and all source URLs.
- Page renders of all 24 pages, contact-sheet review, and detailed visual inspection of all five diagram pages plus the Experiment field table.

The v2 render manifest records SHA-256 hashes for the source report, source register, renderer, canonical diagrams, generated SVGs, and PDF. It keeps the PDF's original input hashes distinct from the latest diagram build. The PDF build environment records Python, ReportLab, and font-file versions/hashes. PDF generation uses deterministic metadata; the authoritative review date is the report's front matter and printed text, not the fixed PDF creation timestamp. Layout verification used Poppler (`pdftoppm`); no live AWS request was made.

Seven regression tests use isolated temporary copies to verify non-mutating checks, stale-PDF detection after an SVG-only build, input validation before writes, duplicate URL and unknown citation rejection, changed PDF bytes, and changed renderer provenance:

```bash
python3 -m unittest discover -s aws/fis/analysis/tools -p 'test_*.py' -v
```

These checks establish artifact consistency and build provenance. They do not establish AWS API correctness, figure legibility, or application behavior; those require the source review, visual review, and application checks recorded in the package.
