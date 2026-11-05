#!/usr/bin/env python3
"""Build the self-contained Lens demo using the Python standard library.

All source files and reviewed SVGs are bundled into index.html. The output has
no runtime dependencies and makes no network calls. Relative report/source
links remain available when the adjacent analysis package is retained.
"""
from pathlib import Path
import json
import re

APP = Path(__file__).resolve().parent
ANALYSIS = APP.parent
SRC = APP / "src"


def render_page():
    """Return the deterministic page and diagram count without changing files."""
    content = (SRC / "shell.html").read_text(encoding="utf-8")
    for token, filename in [("STYLES", "styles.css"), ("DATA", "mock-data.js"),
                            ("MODEL", "model.js"), ("APP", "app.js")]:
        value = (SRC / filename).read_text(encoding="utf-8")
        if token != "STYLES":
            value = re.sub(r"</script", r"<\\/script", value, flags=re.I)
        marker = "/*__" + token + "__*/"
        if content.count(marker) != 1:
            raise SystemExit("Expected exactly one bundle marker: " + marker)
        content = content.replace(marker, value)

    manifest_path = ANALYSIS / "diagrams" / "manifest.json"
    raw = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
    entries = raw if isinstance(raw, list) else raw.get("diagrams", [])
    diagrams = []
    for entry in entries:
        source = entry.get("filename") or entry.get("source_file") or entry.get("file") or entry["id"] + ".mmd"
        source_path = ANALYSIS / "diagrams" / Path(source).name
        svg_path = source_path.with_suffix(".svg")
        if not source_path.exists() or not svg_path.exists():
            raise SystemExit("Build reviewed diagrams first; missing " + str(svg_path))
        svg = svg_path.read_text(encoding="utf-8")
        start = svg.find("<svg")
        if start < 0:
            raise SystemExit("Missing SVG root: " + str(svg_path))
        svg = svg[start:]
        diagrams.append({**entry, "id": entry["id"], "title": entry.get("title", entry["id"]),
                         "sourcePath": "diagrams/" + source_path.name,
                         "svgPath": "diagrams/" + svg_path.name,
                         "source": source_path.read_text(encoding="utf-8"), "svg": svg})
    diagram_js = "globalThis.LensDiagrams = " + json.dumps(diagrams, ensure_ascii=False).replace("</", "<\\/") + ";"
    if content.count("/*__DIAGRAMS__*/") != 1:
        raise SystemExit("Expected exactly one diagram bundle marker")
    content = content.replace("/*__DIAGRAMS__*/", diagram_js)
    if "/*__" in content:
        raise SystemExit("Unfilled bundle marker")
    return content, len(diagrams)


def main():
    content, diagram_count = render_page()
    output = ANALYSIS / "index.html"
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    print(f"Built {output.name}: {len(content.encode('utf-8')):,} bytes; {diagram_count} embedded diagrams; offline runtime.")


if __name__ == "__main__":
    main()
