# Rebuild the report and diagrams

The canonical prose is [report.md](../report.md). Each diagram's entities, attributes, cardinalities, title, description, and ownership labels live in its editable `.mmd` file under [diagrams](../diagrams/). The Python renderer keeps only presentation coordinates and connector routes in code.

From this analysis directory, with Python 3.10 or newer:

```bash
python3 -m pip install -r tools/requirements.txt
python3 tools/build_report.py
```

The build regenerates all four accessible SVGs and `report.pdf`. The script locates its inputs relative to its own path, so it can also be run from another directory. It uses no network access, browser, Node package, or external Mermaid rendering service. An alternate PDF destination can be supplied with `--output /path/to/report.pdf`.

To regenerate only the SVGs, using the Python standard library:

```bash
python3 tools/render_diagrams.py
```

## Supported source format

The report builder intentionally supports the small Markdown subset used by this report: headings, paragraphs, bold text, inline code, links, numeric source references, lists, pipe tables, local SVG figures, and `<!-- pagebreak -->` comments. It rejects unsupported fenced blocks. The PDF renders the generated SVGs as vector geometry and text; it is not a screenshot of the Markdown. Hyperlinks and the full official-source index remain in the PDF.

The diagram renderer supports Mermaid `erDiagram`, `direction TB`, typed entity fields with optional `PK`/`FK` flags, and the cardinality/relationship forms present in the four sources. Metadata comments carry the figure title, description, and ownership category. Changes to entity or relationship sets require updating the corresponding presentation layout; the renderer checks that the two agree and fails if they differ. It is a small report-specific renderer, not a general Mermaid implementation. Mermaid-aware tools can render the `.mmd` files directly.

Each SVG includes a document title and description, entity and relationship labels, a textual ownership legend, and explicit cardinalities. AWS facts, local abstractions, and external context have separate colors as a visual aid; their meaning is also stated in text.

## Reproducibility

The checked-in PDF was generated with Python 3 and ReportLab 4.4.9. DejaVu Sans is embedded when available in standard font locations; PDF standard fonts are the fallback. ReportLab invariant mode removes build-time metadata variation. Identical source, font, Python, and dependency environments produce repeatable output; a font fallback can change pagination. No customer AWS connection or credentials are needed to build the documentation.
