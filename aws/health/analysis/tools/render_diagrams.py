#!/usr/bin/env python3
"""Render the four reviewed Mermaid ERDs as accessible, dependency-free SVGs.

The .mmd files own entities, attributes, relationships, and ownership labels.
This deliberately small renderer supports the ER syntax used in those files;
LAYOUTS owns only presentation coordinates and connector routes. Mermaid-aware
editors/GitHub can also render the editable sources directly.
"""
from __future__ import annotations

import re
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET

ANALYSIS = Path(__file__).resolve().parents[1]
COLORS = {
    "aws": ("#087884", "#EAF5F6", "AWS"),
    "local": ("#2456A1", "#EDF2FA", "LOCAL"),
    "external": ("#936209", "#FAF5E9", "EXTERNAL"),
}
INK = "#23364A"
LINE = "#CBD6E0"
EDGE = "#687B90"

# Each node tuple is x, y, width. Height follows the editable attribute list.
# Connector tuple: start port, end port, optional waypoints.
LAYOUTS = {
    "01-core-model": {
        "height": 870,
        "subtitle": "Provider identity, conditional evidence contexts, and event-relative impact.",
        "note": "PUBLIC has no account. ACCOUNT has one account. ORG_SUMMARY has one organization and owns no impacts.",
        "nodes": {
            "EVENT_TYPE": (30, 125, 265), "HEALTH_EVENT": (355, 125, 265),
            "ORG_HEALTH_ACCESS": (680, 125, 265), "ACCOUNT": (30, 345, 265),
            "EVENT_CONTEXT": (355, 345, 265), "ORGANIZATION": (680, 345, 265),
            "ORGANIZATION_MEMBERSHIP": (30, 590, 265), "ENTITY_IMPACT": (355, 590, 265),
        },
        "edges": {
            ("EVENT_TYPE", "HEALTH_EVENT"): ("R", "L", []),
            ("HEALTH_EVENT", "EVENT_CONTEXT"): ("B", "T", []),
            ("EVENT_CONTEXT", "ACCOUNT"): ("L0.27", "R", []),
            ("EVENT_CONTEXT", "ORGANIZATION"): ("R0.27", "L", []),
            ("ORGANIZATION", "ORGANIZATION_MEMBERSHIP"): ("B", "B", [(812.5, 805), (162.5, 805)]),
            ("ACCOUNT", "ORGANIZATION_MEMBERSHIP"): ("B", "T", []),
            ("ORGANIZATION", "ORG_HEALTH_ACCESS"): ("T", "B", []),
            ("EVENT_CONTEXT", "ENTITY_IMPACT"): ("B", "T", []),
        },
    },
    "02-history-delivery": {
        "height": 920,
        "subtitle": "Local communication grouping, raw AWS identity, and independent event/entity clocks.",
        "note": "Source observations are immutable. A later collection time does not make the underlying provider evidence newer.",
        "nodes": {
            "SOURCE_OBSERVATION": (30, 125, 265), "EVENT_CONTEXT": (355, 125, 265),
            "COMMUNICATION": (680, 125, 265), "ENTITY_REVISION": (30, 390, 265),
            "EVENT_REVISION": (355, 390, 265), "COMMUNICATION_PAGE": (680, 390, 265),
            "ENTITY_IMPACT": (30, 660, 265), "EVENT_DESCRIPTION": (355, 660, 265),
            "MESSAGE_DELIVERY": (680, 660, 265),
        },
        "edges": {
            ("EVENT_CONTEXT", "EVENT_REVISION"): ("B", "T", []),
            ("EVENT_REVISION", "EVENT_DESCRIPTION"): ("B", "T", []),
            ("EVENT_CONTEXT", "COMMUNICATION"): ("R0.68", "L", []),
            ("COMMUNICATION", "COMMUNICATION_PAGE"): ("B", "T", []),
            ("COMMUNICATION_PAGE", "MESSAGE_DELIVERY"): ("B", "T", []),
            ("ENTITY_IMPACT", "ENTITY_REVISION"): ("T", "B", []),
            ("SOURCE_OBSERVATION", "EVENT_REVISION"): ("R", "L", [(322, 194), (322, 468)]),
            ("SOURCE_OBSERVATION", "ENTITY_REVISION"): ("B", "T", []),
            ("SOURCE_OBSERVATION", "MESSAGE_DELIVERY"): ("T", "R", [(162.5, 108), (966, 108), (966, 747)]),
        },
    },
    "03-lifecycle-posture": {
        "height": 935,
        "subtitle": "Provider lifecycle facts meet independently observed deployments through an explicit assessment.",
        "note": "Catalog IDs are local. AWS supplies no direct catalog-to-resource or catalog-to-Health-event foreign key.",
        "nodes": {
            "SERVICE_LIFECYCLE_ENTRY": (60, 125, 350), "INVENTORY_RESOURCE": (560, 125, 350),
            "LIFECYCLE_MILESTONE": (60, 400, 350), "COMPONENT_DEPLOYMENT": (560, 400, 350),
            "LIFECYCLE_EXPOSURE": (310, 690, 360),
        },
        "edges": {
            ("SERVICE_LIFECYCLE_ENTRY", "LIFECYCLE_MILESTONE"): ("B", "T", []),
            ("INVENTORY_RESOURCE", "COMPONENT_DEPLOYMENT"): ("B", "T", []),
            ("COMPONENT_DEPLOYMENT", "LIFECYCLE_EXPOSURE"): ("B", "T0.75", [(735, 615), (580, 615)]),
            ("LIFECYCLE_MILESTONE", "LIFECYCLE_EXPOSURE"): ("B", "T0.25", [(235, 615), (400, 615)]),
        },
    },
    "04-operator-workflow": {
        "height": 860,
        "subtitle": "Application-owned response work and auditable actions retain their own state.",
        "note": "Exactly one target FK is set per WorkItemTarget. Completing work never rewrites an AWS provider status.",
        "nodes": {
            "WORK_ITEM": (60, 125, 350), "OPERATOR_ACTION": (560, 125, 350),
            "WORK_ITEM_TARGET": (60, 455, 350), "EVENT_CONTEXT": (560, 350, 350),
            "ENTITY_IMPACT": (560, 535, 350), "LIFECYCLE_EXPOSURE": (560, 720, 350),
        },
        "edges": {
            ("WORK_ITEM", "OPERATOR_ACTION"): ("R", "L", []),
            ("WORK_ITEM", "WORK_ITEM_TARGET"): ("B", "T", []),
            ("WORK_ITEM_TARGET", "EVENT_CONTEXT"): ("R", "L", [(470, 524), (470, 383)]),
            ("WORK_ITEM_TARGET", "ENTITY_IMPACT"): ("R", "L", [(470, 524), (470, 568)]),
            ("WORK_ITEM_TARGET", "LIFECYCLE_EXPOSURE"): ("B", "L", [(235, 753)]),
        },
    },
}


def parse_mermaid(path: Path) -> dict:
    """Parse exactly the small, auditable Mermaid ER subset used by this report."""
    result = {"title": path.stem, "description": "", "ownership": {}, "entities": {}, "relations": []}
    current = None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("%%"):
            key, sep, value = line[2:].strip().partition(":")
            if sep and key in ("title", "description"):
                result[key] = value.strip()
            elif sep and key == "ownership":
                result[key] = dict(item.split("=", 1) for item in value.split())
            continue
        if line in ("erDiagram", "direction TB"):
            continue
        relation = re.fullmatch(r"([A-Z_]+)\s+([|o{}]+)--([|o{}]+)\s+([A-Z_]+)\s*:\s*([a-z_]+)", line)
        if relation:
            result["relations"].append(relation.groups())
            continue
        entity = re.fullmatch(r"([A-Z_]+)\s*\{", line)
        if entity:
            current = entity.group(1)
            result["entities"][current] = []
            continue
        if line == "}":
            current = None
            continue
        if current:
            field = re.fullmatch(r"([a-z_]+)\s+([A-Za-z][A-Za-z0-9]*)(?:\s+([A-Z,]+))?", line)
            if field:
                result["entities"][current].append(field.groups())
                continue
        raise ValueError(f"Unsupported Mermaid statement at {path.name}:{number}: {line}")
    return result


def cardinality(value: str) -> str:
    return {"||": "1", "|o": "0..1", "o|": "0..1", "o{": "0..n", "}o": "0..n", "|{": "1..n", "}|": "1..n"}[value]


def node_height(attributes: list) -> int:
    return 48 + 18 * len(attributes)


def port(box: tuple, name: str) -> tuple[float, float]:
    x, y, w, h = box
    side = name[0]
    fraction = float(name[1:]) if len(name) > 1 else 0.5
    return {"T": (x + w * fraction, y), "B": (x + w * fraction, y + h),
            "L": (x, y + h * fraction), "R": (x + w, y + h * fraction)}[side]


def render_one(stem: str) -> Path:
    parsed = parse_mermaid(ANALYSIS / "diagrams" / f"{stem}.mmd")
    layout = LAYOUTS[stem]
    if set(parsed["entities"]) != set(layout["nodes"]):
        raise ValueError(f"Update presentation layout for changed entities in {stem}")
    if {(r[0], r[3]) for r in parsed["relations"]} != set(layout["edges"]):
        raise ValueError(f"Update connector routes for changed relationships in {stem}")
    boxes = {key: (*coords, node_height(parsed["entities"][key])) for key, coords in layout["nodes"].items()}
    height = layout["height"]
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="980" height="{height}" viewBox="0 0 980 {height}" role="img" aria-labelledby="{stem}-title {stem}-desc">']
    svg.append(f'<title id="{stem}-title">{escape(parsed["title"])}</title>')
    svg.append(f'<desc id="{stem}-desc">{escape(parsed["description"])} Teal means AWS facts, blue means application model, and amber means external context. Labels 1, 0..1, 0..n, and 1..n give cardinality. {escape(layout["note"])}</desc>')
    svg.append('<rect x="0" y="0" width="980" height="'+str(height)+'" fill="#FFFFFF"/>')
    svg.append(f'<text x="30" y="29" font-family="DejaVu Sans, Arial, sans-serif" font-size="22" font-weight="700" fill="{INK}">{escape(parsed["title"])}</text>')
    svg.append(f'<text x="30" y="53" font-family="DejaVu Sans, Arial, sans-serif" font-size="12.5" fill="#53677B">{escape(layout["subtitle"])}</text>')
    for x, kind, label in [(30, "aws", "AWS facts"), (250, "local", "Application model"), (505, "external", "External context")]:
        color, fill, tag = COLORS[kind]
        svg.append(f'<rect x="{x}" y="76" width="13" height="13" rx="3" fill="{fill}" stroke="{color}"/>')
        svg.append(f'<text x="{x+20}" y="87" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.5" fill="{INK}">{label}</text>')
    svg.append(f'<text x="744" y="87" font-family="DejaVu Sans, Arial, sans-serif" font-size="11" fill="#53677B">Cardinality: minimum..maximum</text>')
    svg.append('<g aria-label="Entity relationships">')
    for a, ca, cb, b, verb in parsed["relations"]:
        start_side, end_side, waypoints = layout["edges"][(a, b)]
        points = [port(boxes[a], start_side), *waypoints, port(boxes[b], end_side)]
        title = f'{a}: {cardinality(ca)}; {verb.replace("_", " ")}; {b}: {cardinality(cb)}'
        svg.append(f'<g role="group" aria-label="{escape(title)}"><title>{escape(title)}</title>')
        path = " ".join(f"{x:g},{y:g}" for x, y in points)
        svg.append(f'<polyline points="{path}" fill="none" stroke="{EDGE}" stroke-width="1.5"/>')
        short_horizontal = len(points) == 2 and abs(points[0][0] - points[1][0]) < 160 and abs(points[0][1] - points[1][1]) < 40
        for endpoint, ((x, y), side, code) in enumerate([(points[0], start_side[0], ca), (points[-1], end_side[0], cb)]):
            dx, dy = {"T": (6, -8), "B": (6, 15), "L": (-7, -7), "R": (7, -7)}[side]
            # Put the second label below short horizontal links so that the
            # two endpoint cardinalities remain distinct at print size.
            if short_horizontal and endpoint == 1 and side in ("L", "R"):
                dy = 16
            anchor = "end" if side == "L" else "start"
            svg.append(f'<text x="{x+dx:g}" y="{y+dy:g}" text-anchor="{anchor}" font-family="DejaVu Sans, Arial, sans-serif" font-size="12" font-weight="700" fill="#4B6075">{cardinality(code)}</text>')
        svg.append('</g>')
    svg.append('</g>')
    for key, attrs in parsed["entities"].items():
        x, y, w, h = boxes[key]
        kind = parsed["ownership"].get(key, "local")
        color, fill, tag = COLORS[kind]
        svg.append(f'<g id="{stem}-{key.lower()}" role="group" aria-label="{key}, {kind}"><title>{key}, {kind}</title>')
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="#FFFFFF" stroke="{LINE}" stroke-width="1.2"/>')
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="34" rx="7" fill="{fill}"/>')
        svg.append(f'<rect x="{x}" y="{y+22}" width="{w}" height="12" fill="{fill}"/>')
        svg.append(f'<text x="{x+11}" y="{y+22}" font-family="DejaVu Sans, Arial, sans-serif" font-size="13.5" font-weight="700" fill="{color}">{key}</text>')
        # Ownership is explicit in accessible labels and the textual legend.
        for i, (datatype, name, flags) in enumerate(attrs):
            label = f"{name} [{flags}]" if flags else name
            svg.append(f'<text x="{x+12}" y="{y+53+i*18}" font-family="DejaVu Sans, Arial, sans-serif" font-size="14" fill="{INK}">{escape(label)}</text>')
        svg.append('</g>')
    svg.append(f'<text x="30" y="{height-22}" font-family="DejaVu Sans, Arial, sans-serif" font-size="11.1" fill="#53677B">{escape(layout["note"])}</text>')
    svg.append('</svg>')
    output = ANALYSIS / "diagrams" / f"{stem}.svg"
    output.write_text("\n".join(svg) + "\n", encoding="utf-8")
    # Syntax validation catches invalid XML in accessible descriptions as well.
    ET.parse(output)
    return output


def main() -> None:
    for stem in LAYOUTS:
        print(render_one(stem).relative_to(ANALYSIS))


if __name__ == "__main__":
    main()
