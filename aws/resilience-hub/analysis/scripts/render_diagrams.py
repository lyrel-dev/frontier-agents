#!/usr/bin/env python3
"""Render the five editable Mermaid ER models with deterministic SVG layouts.

The .mmd files hold entity fields and relationships. diagram-layouts.json only
holds presentation coordinates, labels, and explanatory notes. This renderer
supports the small erDiagram subset used here; it does not require Mermaid,
a browser, a CDN, or network access. Run from any working directory.
"""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "diagrams"
INK, MUTED, BORDER = "#16304a", "#53677c", "#cbd8e3"
AWS, LOCAL = "#183750", "#087f83"


def parse_mermaid(path):
    entities, relations = {}, []
    current = None
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("%%") or line in ("erDiagram", "direction TB"):
            continue
        if re.fullmatch(r"[A-Z_]+\s*\{", line):
            current = line.split()[0]
            entities[current] = []
        elif line == "}":
            current = None
        elif current:
            match = re.fullmatch(r'(\w+)\s+(\w+)(?:\s+([A-Z, ]+?))?(?:\s+"([^"]*)")?', line)
            if not match:
                raise ValueError(f"Unsupported field in {path}: {line}")
            kind, name, keys, comment = match.groups()
            entities[current].append((kind, name, (keys or "").strip(), comment or ""))
        else:
            match = re.fullmatch(r'([A-Z_]+)\s+([|o{}]+)(--|\.\.)([|o{}]+)\s+([A-Z_]+)\s*:\s*"?([^\"]+)"?', line)
            if not match:
                raise ValueError(f"Unsupported relationship in {path}: {line}")
            a, ca, style, cb, b, label = match.groups()
            if a not in entities or b not in entities:
                # Relationship declarations may precede their entity blocks.
                pass
            relations.append((a, ca, style, cb, b, label.strip()))
    return entities, relations


def esc(value):
    return html.escape(str(value), quote=True)


def render(name, spec):
    entities, relations = parse_mermaid(DIR / f"{name}.mmd")
    width, height = spec["size"]
    output = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
              f'<title id="title">{esc(spec["title"])}</title>',
              '<desc id="desc">Entity relationship diagram. Navy entities are AWS-backed; teal entities are local records. Cardinalities are printed on relationship lines. See the accompanying Mermaid source and report for constraints.</desc>',
              '<style>text{font-family:Inter,Arial,sans-serif}.entity{font-size:17px;font-weight:700}.field{font-size:16px}.meta{font-size:13px}.link{font-size:14px}.note{font-size:16px}</style>',
              f'<rect width="{width}" height="{height}" rx="18" fill="#f8fbfd"/>',
              f'<text x="32" y="42" fill="{INK}" font-size="25" font-weight="700">{esc(spec["title"])}</text>',
              f'<text x="32" y="69" fill="{MUTED}" font-size="16">{esc(spec["subtitle"])}</text>']
    if len(relations) != len(spec["routes"]):
        raise ValueError(f"{name}: expected a route for every Mermaid relationship")
    cardinality = {"||": "1", "o|": "0..1", "|o": "0..1", "o{": "0..*", "}o": "0..*", "|{": "1..*", "}|": "1..*"}
    for relation, route in zip(relations, spec["routes"]):
        a, ca, style, cb, b, label = relation
        if a not in entities or b not in entities:
            raise ValueError(f"{name}: relationship has unknown entity")
        points = route["points"]
        dash = ' stroke-dasharray="7 5"' if style == ".." else ""
        output.append(f'<polyline points="{" ".join(f"{x},{y}" for x,y in points)}" fill="none" stroke="#6e8397" stroke-width="1.8"{dash}/>')
        for text, position in ((cardinality[ca], route["a"]), (cardinality[cb], route["b"]), (route.get("label", label), route["labelAt"])):
            x, y = position
            output.append(f'<text x="{x}" y="{y}" text-anchor="middle" class="link" font-size="14" fill="{MUTED}">{esc(text)}</text>')
    for entity, fields in entities.items():
        x, y, w, h = spec["boxes"][entity]
        header = LOCAL if entity in spec.get("local", []) else AWS
        output.extend([f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="white" stroke="{BORDER}"/>',
                       f'<path d="M{x+9},{y} H{x+w-9} Q{x+w},{y} {x+w},{y+9} V{y+43} H{x} V{y+9} Q{x},{y} {x+9},{y} Z" fill="{header}"/>',
                       f'<text x="{x+15}" y="{y+28}" fill="white" class="entity" font-size="17" font-weight="700">{esc(entity)}</text>'])
        yy = y + 68
        for kind, field, keys, comment in fields:
            output.append(f'<text x="{x+15}" y="{yy}" fill="{INK}" class="field" font-size="16">{esc(field)}{f"  [{esc(keys)}]" if keys else ""}</text>')
            yy += 22
            if comment:
                output.append(f'<text x="{x+15}" y="{yy-2}" fill="{MUTED}" class="meta" font-size="13">{esc(comment)}</text>')
                yy += 18
        if yy > y + h + 3:
            raise ValueError(f"{name}: {entity} fields exceed its box ({yy} > {y+h})")
    ly = spec["legendY"]
    for x, color, label in ((32, AWS, "AWS-backed identity or value"), (335, LOCAL, "Local normalization or evidence")):
        output.append(f'<rect x="{x}" y="{ly-12}" width="13" height="13" rx="3" fill="{color}"/><text x="{x+22}" y="{ly}" fill="{MUTED}" class="link" font-size="14">{label}</text>')
    for i, note in enumerate(spec.get("notes", [])):
        output.append(f'<text x="32" y="{ly+32+i*24}" fill="{MUTED}" class="note" font-size="16">{esc(note)}</text>')
    output.append('</svg>')
    target = DIR / f"{name}.svg"
    target.write_text(("\n".join(output) + "\n").replace("<text ", '<text font-family="sans-serif" '))
    return target


if __name__ == "__main__":
    layouts = json.loads((DIR / "diagram-layouts.json").read_text())
    for name, spec in layouts.items():
        print(render(name, spec).relative_to(ROOT))
