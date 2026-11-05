# Report and diagram renderer

The canonical report is [`../report.md`](../report.md). The five canonical ER models are the `.mmd` files in [`../diagrams/`](../diagrams/). Their actual Mermaid code is also embedded in the report, so the Markdown remains self-contained.

## Regenerate

From the repository root:

```bash
python3 aws/fis/analysis/tools/render_report.py
```

The command writes five SVGs in `diagrams/`, the reviewed `aws_fis_experiment_action_model.pdf`, and `tools/render-manifest.json`. Use `--svg-only` to regenerate only diagram assets. The command does not access AWS or use the network.

Requirements: Python 3.10 or newer and ReportLab. The committed output was generated with ReportLab 4.4.9 and DejaVu Sans / DejaVu Sans Mono fonts. The renderer discovers DejaVu fonts at the paths listed in `register_fonts()` and falls back to PDF base fonts if none are available. Use the same fonts and ReportLab version for identical output bytes.

## Model fidelity

The renderer parses entity names, attributes, primary/foreign-key annotations, relationship labels, and cardinalities from the canonical Mermaid. It uses a reviewed layout for each of these five diagrams. It fails if entities or relationships differ from that layout, if embedded Mermaid differs from its source file, or if report source references differ from `sources.json`.

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

The reviewed build produced a 27-page PDF, 14 report sections, 5 vector diagrams, and 53 official source references. Validation checked:

- Byte equality of the five embedded Mermaid blocks and standalone sources.
- Exact agreement between Markdown source definitions and `sources.json`, with unique source IDs and URLs.
- Successful XML parsing of all five SVGs.
- Entity/relationship counts of `5/5`, `10/12`, `8/7`, `11/12`, and `7/7` across diagrams 1 through 5.
- PDF text extraction, all section headings, all five figure titles, and all source URLs.
- Page renders of all 27 pages, contact-sheet review, and detailed visual inspection of all five diagram pages plus the Experiment field table.

The render manifest records SHA-256 hashes for the source report, canonical diagrams, generated SVGs, and PDF. PDF generation is configured for deterministic metadata. Layout verification used Poppler (`pdftoppm`); no live AWS request was made.
