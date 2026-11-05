"""Non-mutating validation of the self-contained revised FIS package."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PROPERTIES = {"id", "title", "type", "service", "status", "version", "created", "updated", "tags", "aliases", "related"}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def within(path):
    return path.is_relative_to(ROOT)


def validate():
    errors = []
    notes = sorted(ROOT.rglob("*.md"))
    notes = [path for path in notes if "node_modules" not in path.parts]
    identifiers = {}
    markdown_by_path = {}

    def local_link(source, target):
        target = target.strip().strip("<>")
        if not target or target.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target):
            return
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            return
        destination = (source.parent / target).resolve()
        if not within(destination):
            errors.append(f"{source.relative_to(ROOT)}: link leaves revised package: {target}")
        elif not destination.exists():
            errors.append(f"{source.relative_to(ROOT)}: missing local link: {target}")

    for note in notes:
        text = note.read_text(encoding="utf-8")
        match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not match:
            errors.append(f"{note.relative_to(ROOT)}: missing YAML front matter")
            continue
        try:
            properties = yaml.safe_load(match.group(1))
        except yaml.YAMLError as error:
            errors.append(f"{note.relative_to(ROOT)}: invalid YAML: {error}")
            continue
        if not isinstance(properties, dict):
            errors.append(f"{note.relative_to(ROOT)}: YAML properties must be a mapping")
            continue
        missing = REQUIRED_PROPERTIES - set(properties)
        if missing:
            errors.append(f"{note.relative_to(ROOT)}: missing properties {sorted(missing)}")
        identifier = properties.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            errors.append(f"{note.relative_to(ROOT)}: id must be a nonempty string")
        elif identifier in identifiers:
            errors.append(f"duplicate id {identifier}: {note.relative_to(ROOT)} and {identifiers[identifier]}")
        else:
            identifiers[identifier] = str(note.relative_to(ROOT))
        for field in ("tags", "aliases", "related"):
            if not isinstance(properties.get(field), list):
                errors.append(f"{note.relative_to(ROOT)}: {field} must be a list")
        for target in properties.get("related", []):
            if isinstance(target, str):
                local_link(note, target)
        body = text[match.end():]
        markdown_by_path[note] = body
        prose = re.sub(r"```.*?```", "", body, flags=re.S)
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", prose):
            local_link(note, target)
        for target in re.findall(r"!?\[\[([^\]]+)\]\]", prose):
            name = target.split("|", 1)[0].split("#", 1)[0]
            if name:
                local_link(note, name if Path(name).suffix else name + ".md")

    # Diagram notes are the Obsidian-readable documents; .mmd/.svg are editable/rendered assets.
    diagrams = sorted((ROOT / "diagrams").rglob("*.mmd"))
    if len(diagrams) != 8:
        errors.append(f"expected 8 canonical diagrams, found {len(diagrams)}")
    for source in diagrams:
        svg_path, note_path = source.with_suffix(".svg"), source.with_suffix(".md")
        if not svg_path.exists() or not note_path.exists():
            errors.append(f"missing SVG or Obsidian note for {source.relative_to(ROOT)}")
            continue
        canonical = source.read_text().strip()
        note_blocks = re.findall(r"```mermaid\n(.*?)\n```", note_path.read_text(), re.S)
        if [block.strip() for block in note_blocks] != [canonical]:
            errors.append(f"diagram note differs from source: {note_path.relative_to(ROOT)}")
        try:
            svg = ET.parse(svg_path).getroot()
            if svg.tag != "{http://www.w3.org/2000/svg}svg" or any(svg.find("{http://www.w3.org/2000/svg}" + tag) is None for tag in ("title", "desc")):
                errors.append(f"missing SVG root/title/description: {svg_path.relative_to(ROOT)}")
        except ET.ParseError as error:
            errors.append(f"invalid SVG {svg_path.relative_to(ROOT)}: {error}")
    for document, directory, count in (("docs/initial/report.md", "initial", 5), ("docs/suggested/model.md", "suggested", 3)):
        path = ROOT / document
        if not path.exists():
            errors.append(f"missing reviewed model: {document}")
            continue
        blocks = re.findall(r"```mermaid\n(.*?)\n```", path.read_text(), re.S)
        expected = [(p.read_text().strip()) for p in sorted((ROOT / "diagrams" / directory).glob("*.mmd"))]
        if len(blocks) != count or [block.strip() for block in blocks] != expected:
            errors.append(f"embedded diagrams differ in {document}")

    # Original interface code is retained; only report/diagram navigation is adapted.
    initial_manifest = json.loads((ROOT / "initial/source-manifest.json").read_text())
    for item in initial_manifest["files"]:
        target = ROOT / "initial" / item["path"]
        if sha256(target) != item["packagedSha256"]:
            errors.append(f"preserved interface changed after packaging: {item['path']}")
        if item["adaptation"] == "none" and item["sourceSha256"] != item["packagedSha256"]:
            errors.append(f"unexpected baseline-code modification: {item['path']}")

    sources = json.loads((ROOT / "docs/initial/sources.json").read_text())["sources"]
    ids = [item["id"] for item in sources]
    urls = [item["url"] for item in sources]
    if len(ids) != len(set(ids)) or len(urls) != len(set(urls)):
        errors.append("duplicate initial source ID or URL")
    report = (ROOT / "docs/initial/report.md").read_text()
    if set(re.findall(r"\[(S\d+)\]", report)) != set(ids):
        errors.append("initial report citation set differs from source register")

    documentation_manifest = json.loads((ROOT / "docs/manifest.json").read_text())
    declared_files = {item["path"] for item in documentation_manifest["files"]}
    actual_files = {
        str(path.relative_to(ROOT))
        for folder in (ROOT / "docs", ROOT / "diagrams")
        for path in folder.rglob("*")
        if path.is_file() and path != ROOT / "docs/manifest.json"
        and not any(part in {"node_modules", "__pycache__"} for part in path.parts)
    }
    if declared_files != actual_files:
        errors.append("documentation manifest inventory differs from packaged docs/diagrams")
    for item in documentation_manifest["files"]:
        path = ROOT / item["path"]
        if not path.exists() or sha256(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            errors.append(f"documentation manifest hash/size mismatch: {item['path']}")
    for item in documentation_manifest["imports"]:
        path = ROOT / item["targetPath"]
        if not path.exists() or sha256(path) != item["targetSha256"]:
            errors.append(f"imported artifact hash mismatch: {item['targetPath']}")

    # Verify literal local application assets and links. Dynamic links receive browser checks.
    for path in (ROOT / "index.html", ROOT / "initial/index.html", ROOT / "suggested/index.html"):
        if not path.exists():
            errors.append(f"missing interface: {path.relative_to(ROOT)}")
            continue
        for target in re.findall(r'(?:href|src|data-src)="([^"]+)"', path.read_text()):
            local_link(path, target)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(json.dumps({"status": "valid", "markdownNotes": len(notes), "canonicalDiagrams": len(diagrams), "officialFisSources": len(sources), "preservedInitialFiles": len(initial_manifest["files"]), "documentationFilesHashed": len(declared_files), "importsVerified": len(documentation_manifest["imports"]), "filesChanged": 0}, indent=2))


if __name__ == "__main__":
    validate()
