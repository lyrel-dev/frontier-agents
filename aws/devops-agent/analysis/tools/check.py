#!/usr/bin/env python3
"""Check report/diagram integrity and the self-contained application package."""
from __future__ import annotations

import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.external_dependencies = []
        self.inline_scripts = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"])
        if tag == "script" and not values.get("src"):
            self.inline_scripts += 1
        resource = values.get("src") if tag in {"script", "img", "iframe"} else None
        if tag == "link" and values.get("rel") == "stylesheet":
            resource = values.get("href")
        if resource and not resource.startswith("data:"):
            self.external_dependencies.append(resource)


def mask_markdown_code(text):
    """Keep code examples out of link checks without joining surrounding text."""
    blank = lambda value: re.sub(r"[^\r\n]", " ", value)
    lines = []
    fence = None
    for line in text.splitlines(keepends=True):
        if fence:
            lines.append(blank(line))
            character, length = fence
            closing = rf" {{0,3}}{re.escape(character)}{{{length},}}[ \t]*(?:\r?\n)?"
            if re.fullmatch(closing, line):
                fence = None
            continue
        opening = re.match(r" {0,3}(`{3,}|~{3,})([^\r\n]*)", line)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = (opening[1][0], len(opening[1]))
            lines.append(blank(line))
        else:
            lines.append(line)

    text = "".join(lines)
    masked = list(text)
    position = 0
    while position < len(text):
        if text[position] != "`":
            position += 1
            continue
        slash = position - 1
        while slash >= 0 and text[slash] == "\\":
            slash -= 1
        if (position - slash - 1) % 2:
            position += 1
            continue
        end = position + 1
        while end < len(text) and text[end] == "`":
            end += 1
        length = end - position
        paragraph_end = re.search(r"\n[ \t]*\n", text[end:])
        limit = end + paragraph_end.start() if paragraph_end else len(text)
        search = end
        found = False
        while search < limit:
            closing_start = text.find("`", search, limit)
            if closing_start < 0:
                break
            closing_end = closing_start + 1
            while closing_end < limit and text[closing_end] == "`":
                closing_end += 1
            if closing_end - closing_start == length:
                masked[position:closing_end] = blank(text[position:closing_end])
                position = closing_end
                found = True
                break
            search = closing_end
        if not found:
            position = end
    return "".join(masked)


def main():
    manifest = json.loads((ROOT / "diagrams/manifest.json").read_text())
    figures = manifest["diagrams"]
    assert len(figures) == 9, "The reviewed model must retain all nine diagrams"
    assert len({d["id"] for d in figures}) == len(figures), "Duplicate diagram ID"
    report = (ROOT / "report.md").read_text()
    fences = re.findall(r"```mermaid\s*\n(.*?)\n```", report, re.S)
    normalized = lambda s: "\n".join(line.rstrip() for line in s.strip().splitlines())
    assert len(fences) == 9, "report.md must contain all nine editable Mermaid diagrams"
    records = {d["id"]: d for d in json.loads((ROOT / "qa/diagram-render.json").read_text())["diagrams"]}
    for diagram in figures:
        source = (ROOT / diagram["filename"]).read_text()
        assert normalized(source) in [normalized(f) for f in fences], f"Report/source mismatch: {diagram['id']}"
        svg = (ROOT / diagram["rendered"]).read_bytes()
        root = ET.fromstring(svg)
        assert root.tag.endswith("svg"), diagram["rendered"]
        assert root.attrib.get("aria-labelledby"), f"Missing accessible title: {diagram['id']}"
        assert root.find("{http://www.w3.org/2000/svg}title") is not None
        assert float(root.attrib["width"]) > 0 and float(root.attrib["height"]) > 0
        assert records[diagram["id"]]["sourceSha256"] == hashlib.sha256(source.encode()).hexdigest()
        assert records[diagram["id"]]["svgSha256"] == hashlib.sha256(svg).hexdigest()

    checked_links = 0
    for path in sorted(ROOT.rglob("*.md")):
        if "node_modules" in path.parts:
            continue
        body = path.read_text()
        assert body.startswith("---\n"), f"Missing YAML front matter: {path.relative_to(ROOT)}"
        assert "\n---\n" in body[4:], f"Unclosed YAML front matter: {path.relative_to(ROOT)}"
        link_body = mask_markdown_code(body)
        for target in re.findall(r"\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", link_body):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            resolved = path.parent / unquote(url.path)
            assert resolved.exists(), f"Broken local link in {path.relative_to(ROOT)}: {target}"
            checked_links += 1
        assert not re.search(r"\[\[[^\]]+\]\]", link_body), f"Unresolved wiki link: {path.relative_to(ROOT)}"

    html = (ROOT / "index.html").read_text()
    page = Page()
    page.feed(html)
    assert not page.external_dependencies, f"Runtime file dependencies: {page.external_dependencies}"
    assert len(page.ids) == len(set(page.ids)), "Duplicate IDs in static application shell"
    assert page.inline_scripts == 4, "Expected data, model, diagrams and UI inline scripts"
    assert "/*__" not in html, "Unfilled build placeholder"
    assert "globalThis.LensDiagrams" in html, "Missing embedded diagrams"
    assert "Mock data" in html, "Missing fictional-data disclosure"
    print(f"PASS: nine report/source/SVG diagram pairs; {checked_links} local Markdown links; YAML boundaries; offline HTML shell.")


if __name__ == "__main__":
    main()
