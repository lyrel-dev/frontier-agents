#!/usr/bin/env python3
"""Check the package's deliberately flat YAML subset and local Markdown links.

Uses only the standard library. Front matter is constrained to JSON-quoted
scalars, booleans, numbers and lists, all of which are valid YAML. This checker
does not claim to parse arbitrary YAML or arbitrary Markdown extensions.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"id", "title", "type", "service", "status", "created", "updated", "tags", "aliases", "related"}
LINK = re.compile(r"!?\[[^\]\n]+\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)")
DEFINITION = re.compile(r"^\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
FENCE = re.compile(r"^```[^\n]*\n.*?^```\s*$", re.MULTILINE | re.DOTALL)


def read_note(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing opening YAML delimiter")
    boundary = text.find("\n---\n", 4)
    if boundary < 0:
        raise ValueError("missing closing YAML delimiter")
    properties: dict = {}
    list_key = None
    for line in text[4:boundary].splitlines():
        if not line.strip():
            continue
        if line.startswith("  - "):
            if list_key is None:
                raise ValueError("list member has no property")
            properties[list_key].append(json.loads(line[4:]))
            continue
        match = re.fullmatch(r"([a-z][a-z0-9_]*):\s*(.*)", line)
        if not match:
            raise ValueError("front matter is outside the supported flat YAML subset: " + line)
        key, value = match.groups()
        if key in properties:
            raise ValueError("duplicate YAML property: " + key)
        list_key = key if not value else None
        properties[key] = [] if not value else json.loads(value)
    missing = REQUIRED - properties.keys()
    if missing:
        raise ValueError("missing YAML properties: " + ", ".join(sorted(missing)))
    for key in ("id", "title", "type", "service", "status", "created", "updated"):
        if not isinstance(properties[key], str) or not properties[key]:
            raise ValueError(key + " must be a nonempty string")
    for key in ("tags", "aliases", "related"):
        if not isinstance(properties[key], list) or not all(isinstance(value, str) for value in properties[key]):
            raise ValueError(key + " must be a list of strings")
    for key in ("created", "updated"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", properties[key]):
            raise ValueError(key + " must be an ISO date")
    return properties, text[boundary + 5:]


def heading_anchors(text: str) -> set[str]:
    result = set()
    repeated: dict[str, int] = {}
    for heading in re.findall(r"^#{1,6}\s+(.+)$", FENCE.sub("", text), re.MULTILINE):
        heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
        key = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
        ordinal = repeated.get(key, 0)
        repeated[key] = ordinal + 1
        result.add(key + ("-" + str(ordinal) if ordinal else ""))
    return result


def check_link(source: Path, destination: str) -> None:
    if re.match(r"^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|//)", destination):
        return
    file_name, _, fragment = destination.partition("#")
    if "?" in file_name:
        file_name = file_name.split("?", 1)[0]
    target = (source.parent / file_name).resolve() if file_name else source
    if not target.is_relative_to(ROOT):
        raise ValueError("local link escapes package: " + destination)
    if not target.exists():
        raise ValueError("broken local link: " + destination)
    if fragment and target.suffix == ".md":
        _, body = read_note(target)
        if fragment not in heading_anchors(body):
            raise ValueError("missing heading anchor: " + destination)


def main() -> int:
    notes = sorted(ROOT.rglob("*.md"))
    ids: dict[str, Path] = {}
    errors = []
    link_count = 0
    mermaid_count = 0
    for note in notes:
        try:
            properties, body = read_note(note)
            if properties["id"] in ids:
                raise ValueError("duplicate note id also used by " + str(ids[properties["id"]].relative_to(ROOT)))
            ids[properties["id"]] = note
            if properties["service"] != "aws-resilience-hub":
                raise ValueError("wrong service property")
            if len(re.findall(r"^```", body, re.MULTILINE)) % 2:
                raise ValueError("unclosed Markdown fence")
            diagrams = re.findall(r"^```mermaid\s*\n", body, re.MULTILINE)
            mermaid_count += len(diagrams)
            if note.parent.name == "diagrams" and len(diagrams) != 1:
                raise ValueError("diagram note must have exactly one Mermaid block")
            destinations = [*properties["related"], *LINK.findall(FENCE.sub("", body)), *DEFINITION.findall(body)]
            for destination in destinations:
                check_link(note, destination)
                link_count += 1
        except (ValueError, OSError) as error:
            errors.append(str(note.relative_to(ROOT)) + ": " + str(error))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Verified {len(notes)} Markdown notes, unique YAML identities, {link_count} links/properties and {mermaid_count} Mermaid blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
