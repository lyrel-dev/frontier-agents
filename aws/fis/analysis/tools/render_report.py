#!/usr/bin/env python3
"""Render the reviewed Markdown and canonical Mermaid ERDs without a browser.

Run from any directory:
    python3 aws/fis/analysis/tools/render_report.py

Dependencies: reportlab. Optional verification: pypdf, pdfplumber, Poppler.

The five small diagrams have explicit, reviewed orthogonal layouts. Entity names,
attributes, relationship labels, and endpoint cardinalities are parsed from the
canonical .mmd files; a layout/schema mismatch fails the build. The same vector
scene is used for standalone accessible SVG and embedded PDF figures. Markdown
is the prose source of truth. This is a deliberately bounded renderer for this
report's Markdown subset, not a general Mermaid or Markdown implementation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import platform
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    CondPageBreak, Flowable, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
    Table, TableStyle,
)

BASE = Path(__file__).resolve().parents[1]
INK = '#183346'
MUTED = '#586E7C'
EDGE = '#8A9CA8'
BORDER = '#CCD9E0'
PALE = '#F2F6F8'
TEAL = '#007E83'
AMBER = '#A66B1B'
BLUE = '#2A6B9B'
WHITE = '#FFFFFF'
PAGE_W, PAGE_H = A4
MARGIN = 36
CONTENT_W = PAGE_W - 2 * MARGIN
REPOSITORY = 'https://github.com/lyrel-dev/frontier-agents'
REPO_PATH = 'aws/fis/analysis'
FONT = 'Helvetica'
BOLD = 'Helvetica-Bold'
MONO = 'Courier'
FONT_FILES: dict[str, str] = {}


def register_fonts() -> None:
    global FONT, BOLD, MONO, FONT_FILES
    candidates = [
        Path('/usr/share/fonts/truetype/dejavu'),
        Path('/opt/codex/runtimes/codex-primary-runtime/dependencies/native/'
             'libreoffice-headless/libreoffice/share/fonts/truetype'),
    ]
    for directory in candidates:
        if all((directory / n).is_file() for n in (
            'DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSansMono.ttf'
        )):
            pdfmetrics.registerFont(TTFont('FISBody', str(directory / 'DejaVuSans.ttf')))
            pdfmetrics.registerFont(TTFont('FISBold', str(directory / 'DejaVuSans-Bold.ttf')))
            pdfmetrics.registerFont(TTFont('FISMono', str(directory / 'DejaVuSansMono.ttf')))
            pdfmetrics.registerFontFamily('FISBody', normal='FISBody', bold='FISBold',
                                          italic='FISBody', boldItalic='FISBold')
            FONT, BOLD, MONO = 'FISBody', 'FISBold', 'FISMono'
            FONT_FILES = {name: digest(directory / name) for name in (
                'DejaVuSans.ttf', 'DejaVuSans-Bold.ttf', 'DejaVuSansMono.ttf'
            )}
            return


@dataclass
class Entity:
    name: str
    attributes: list[tuple[str, str, str]] = field(default_factory=list)


@dataclass
class Relation:
    left: str
    left_card: str
    right_card: str
    right: str
    label: str

    @property
    def key(self) -> str:
        return f'{self.left}|{self.label}|{self.right}'


CARD = {'||': '1', 'o|': '0..1', '|{': '1..N', 'o{': '0..N'}


def parse_mermaid(path: Path) -> tuple[dict[str, Entity], list[Relation]]:
    entities: dict[str, Entity] = {}
    relations: list[Relation] = []
    active: Entity | None = None
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped in ('erDiagram', 'direction TB') or stripped.startswith('%%'):
            continue
        match = re.fullmatch(r'(\w+)\s+([|o{}]+)--([|o{}]+)\s+(\w+)\s*:\s*(\w+)', stripped)
        if match:
            left, lc, rc, right, label = match.groups()
            if lc not in CARD or rc not in CARD:
                raise ValueError(f'Unsupported cardinality in {path.name}: {stripped}')
            entities.setdefault(left, Entity(left))
            entities.setdefault(right, Entity(right))
            relations.append(Relation(left, lc, rc, right, label))
            continue
        match = re.fullmatch(r'(\w+)\s*\{', stripped)
        if match:
            active = entities.setdefault(match.group(1), Entity(match.group(1)))
            continue
        if stripped == '}':
            active = None
            continue
        if active:
            parts = stripped.split(maxsplit=2)
            if len(parts) < 2:
                raise ValueError(f'Invalid attribute in {path.name}: {stripped}')
            active.attributes.append((parts[0], parts[1], parts[2] if len(parts) == 3 else ''))
            continue
        raise ValueError(f'Unsupported Mermaid statement in {path.name}: {stripped}')
    if len({r.key for r in relations}) != len(relations):
        raise ValueError(f'Duplicate relationship key in {path.name}')
    return entities, relations


APP_ENTITIES = {
    'ACTION_DEPENDENCY', 'TEMPLATE_DEPENDENCY', 'TEMPLATE_BINDING',
    'ACTION_TARGET_BINDING', 'RESOLVED_TARGET_MEMBERSHIP', 'RESOURCE_IDENTITY',
    'TARGET_RESOLUTION_OBSERVATION', 'EXECUTION_EVIDENCE', 'STATE_OBSERVATION',
    'METRIC_BINDING', 'EXPERIMENT_METRIC_BINDING', 'RESILIENCE_ASSESSMENT',
    'ASSESSMENT_CRITERION', 'ASSESSMENT_EVIDENCE',
}
EXTERNAL_ENTITIES = {'CLOUDWATCH_ALARM', 'ALARM_OBSERVATION', 'METRIC_OBSERVATION'}


def kind_for(name: str) -> tuple[str, str]:
    if name in APP_ENTITIES:
        return 'Application model', AMBER
    if name in EXTERNAL_ENTITIES:
        return 'External evidence / resource', BLUE
    if name == 'AWS_SCOPE':
        return 'Account and Region context', TEAL
    return 'AWS FIS data', TEAL


def display_name(name: str) -> str:
    return {
        'AWS_SCOPE': 'AWS scope',
        'CATALOG_ACTION': 'Catalog action',
        'ACTION_PARAMETER_DEFINITION': 'Action parameter definition',
        'EXPERIMENT_TARGET_ACCOUNT': 'Experiment target account',
        'EXPERIMENT_METRIC_BINDING': 'Experiment metric binding',
        'TARGET_RESOLUTION_OBSERVATION': 'Target resolution observation',
    }.get(name, name.replace('_', ' ').capitalize())


def node_height(entity: Entity) -> float:
    return 82 + 28 * len(entity.attributes)


class Scene:
    def __init__(self, width: float, height: float, title: str, description: str):
        self.width, self.height = width, height
        self.title, self.description = title, description
        self.ops: list[dict[str, Any]] = []

    def rect(self, x: float, y: float, w: float, h: float, fill: str,
             stroke: str | None = None, radius: float = 0, sw: float = 1) -> None:
        self.ops.append(dict(kind='rect', x=x, y=y, w=w, h=h, fill=fill,
                             stroke=stroke, radius=radius, sw=sw))

    def line(self, points: list[tuple[float, float]], stroke: str = EDGE,
             width: float = 2) -> None:
        self.ops.append(dict(kind='line', points=points, stroke=stroke, sw=width))

    def text(self, x: float, y: float, value: str, size: float = 20,
             color: str = INK, weight: str = 'normal', align: str = 'left',
             angle: float = 0, mono: bool = False) -> None:
        self.ops.append(dict(kind='text', x=x, y=y, value=value, size=size,
                             color=color, weight=weight, align=align, angle=angle, mono=mono))

    def label(self, x: float, y: float, value: str, size: float = 17,
              color: str = MUTED, angle: float = 0) -> None:
        # White backgrounds make crossings distinct and preserve label legibility.
        w = pdfmetrics.stringWidth(value, FONT, size) + 12
        if angle == 0:
            self.rect(x - w / 2, y - size + 1, w, size + 6, WHITE, radius=3)
        self.text(x, y, value, size, color, align='center', angle=angle)

    def svg(self) -> str:
        out = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width:g}" height="{self.height:g}" '
            f'viewBox="0 0 {self.width:g} {self.height:g}" role="img" aria-labelledby="title description">',
            f'<title id="title">{escape(self.title)}</title>',
            f'<desc id="description">{escape(self.description)}</desc>',
            '<style>text{font-family:"DejaVu Sans",Arial,sans-serif} '
            '.mono{font-family:"DejaVu Sans Mono",monospace}</style>',
        ]
        for o in self.ops:
            if o['kind'] == 'rect':
                out.append(f'<rect x="{o["x"]:g}" y="{o["y"]:g}" width="{o["w"]:g}" '
                           f'height="{o["h"]:g}" rx="{o["radius"]:g}" fill="{o["fill"]}" '
                           f'stroke="{o["stroke"] or "none"}" stroke-width="{o["sw"]:g}"/>')
            elif o['kind'] == 'line':
                points = ' '.join(f'{x:g},{y:g}' for x, y in o['points'])
                out.append(f'<polyline points="{points}" fill="none" stroke="{o["stroke"]}" '
                           f'stroke-width="{o["sw"]:g}" stroke-linejoin="round"/>')
            elif o['kind'] == 'text':
                anchor = {'left': 'start', 'center': 'middle', 'right': 'end'}[o['align']]
                transform = f' transform="rotate({o["angle"]:g} {o["x"]:g} {o["y"]:g})"' if o['angle'] else ''
                cls = ' class="mono"' if o['mono'] else ''
                out.append(f'<text x="{o["x"]:g}" y="{o["y"]:g}" font-size="{o["size"]:g}" '
                           f'font-weight="{o["weight"]}" text-anchor="{anchor}" fill="{o["color"]}"'
                           f'{transform}{cls}>{escape(o["value"])}</text>')
        out.append('</svg>')
        return '\n'.join(out) + '\n'

    def draw_pdf(self, c: canvas.Canvas, width: float) -> float:
        scale = width / self.width
        c.saveState()
        c.scale(scale, scale)
        for o in self.ops:
            if o['kind'] == 'rect':
                c.setFillColor(colors.HexColor(o['fill']))
                if o['stroke']:
                    c.setStrokeColor(colors.HexColor(o['stroke']))
                    c.setLineWidth(o['sw'])
                c.roundRect(o['x'], self.height - o['y'] - o['h'], o['w'], o['h'],
                            o['radius'], fill=1, stroke=bool(o['stroke']))
            elif o['kind'] == 'line':
                c.setStrokeColor(colors.HexColor(o['stroke']))
                c.setLineWidth(o['sw'])
                path = c.beginPath()
                path.moveTo(o['points'][0][0], self.height - o['points'][0][1])
                for x, y in o['points'][1:]:
                    path.lineTo(x, self.height - y)
                c.drawPath(path)
            elif o['kind'] == 'text':
                c.saveState()
                c.setFillColor(colors.HexColor(o['color']))
                font = MONO if o['mono'] else BOLD if o['weight'] == 'bold' else FONT
                c.setFont(font, o['size'])
                c.translate(o['x'], self.height - o['y'])
                c.rotate(-o['angle'])
                fn = {'left': c.drawString, 'center': c.drawCentredString, 'right': c.drawRightString}[o['align']]
                fn(0, 0, o['value'])
                c.restoreState()
        c.restoreState()
        return self.height * scale


def r(left: str, label: str, right: str) -> str:
    return f'{left}|{label}|{right}'


# Layout positions are x, y, width; node heights follow canonical attribute count.
# Routes are endpoint-to-endpoint polylines plus a relation-label location.
LAYOUTS = {
    '01_execution': {
        'height': 1070,
        'title': '01 / Run identity and action dependencies',
        'nodes': {
            'EXPERIMENT_TEMPLATE': (60, 125, 420), 'CATALOG_ACTION': (770, 125, 420),
            'EXPERIMENT_RUN': (60, 360, 420), 'ACTION_EXECUTION': (770, 360, 420),
            'ACTION_DEPENDENCY': (770, 815, 420),
        },
        'routes': {
            r('EXPERIMENT_TEMPLATE', 'source', 'EXPERIMENT_RUN'): ([(270,207),(270,360)], (270,291)),
            r('EXPERIMENT_RUN', 'contains', 'ACTION_EXECUTION'): ([(480,510),(770,510)], (625,492)),
            r('CATALOG_ACTION', 'identifies', 'ACTION_EXECUTION'): ([(980,207),(980,360)], (980,291)),
            r('ACTION_EXECUTION', 'predecessor', 'ACTION_DEPENDENCY'): ([(890,666),(890,815)], (890,727)),
            r('ACTION_EXECUTION', 'successor', 'ACTION_DEPENDENCY'): ([(1070,666),(1070,815)], (1070,767)),
        },
    },
    '02_catalog_templates': {
        'height': 1120,
        'title': '02 / Templates and catalog definitions',
        'nodes': {
            'CATALOG_ACTION': (80,125,310), 'EXPERIMENT_TEMPLATE': (470,125,310),
            'RESOURCE_TYPE': (860,125,310), 'ACTION_PARAMETER_DEFINITION': (80,360,310),
            'TEMPLATE_ACTION': (470,360,310), 'TEMPLATE_TARGET': (860,360,310),
            'ACTION_TARGET_SLOT': (80,655,310), 'TEMPLATE_DEPENDENCY': (470,655,310),
            'TEMPLATE_BINDING': (860,655,310), 'TEMPLATE_TARGET_ACCOUNT': (470,940,310),
        },
        'routes': {
            r('EXPERIMENT_TEMPLATE','contains','TEMPLATE_ACTION'): ([(625,207),(625,360)],(625,290)),
            r('EXPERIMENT_TEMPLATE','defines','TEMPLATE_TARGET'): ([(780,166),(825,166),(825,401),(860,401)],(825,285)),
            r('CATALOG_ACTION','configures','TEMPLATE_ACTION'): ([(390,166),(430,166),(430,401),(470,401)],(430,280)),
            r('CATALOG_ACTION','describes','ACTION_PARAMETER_DEFINITION'): ([(235,207),(235,360)],(235,290)),
            r('CATALOG_ACTION','supports','ACTION_TARGET_SLOT'): ([(80,166),(35,166),(35,696),(80,696)],(53,540,-90)),
            r('RESOURCE_TYPE','accepted_by','ACTION_TARGET_SLOT'): ([(1170,166),(1215,166),(1215,845),(235,845),(235,737)],(760,830)),
            r('RESOURCE_TYPE','selects','TEMPLATE_TARGET'): ([(1015,207),(1015,360)],(1015,290)),
            r('TEMPLATE_ACTION','binds','TEMPLATE_BINDING'): ([(780,401),(810,401),(810,696),(860,696)],(810,550)),
            r('TEMPLATE_TARGET','referenced_by','TEMPLATE_BINDING'): ([(1015,442),(1015,655)],(1015,557)),
            r('TEMPLATE_ACTION','predecessor','TEMPLATE_DEPENDENCY'): ([(575,442),(575,655)],(575,525)),
            r('TEMPLATE_ACTION','successor','TEMPLATE_DEPENDENCY'): ([(675,442),(675,655)],(675,590)),
            r('EXPERIMENT_TEMPLATE','configures','TEMPLATE_TARGET_ACCOUNT'): ([(505,207),(450,235),(450,981),(470,981)],(450,850,-90)),
        },
    },
    '03_targeting': {
        'height': 1370,
        'title': '03 / Target selectors and selected memberships',
        'nodes': {
            'EXPERIMENT_RUN': (60,125,420), 'EXPERIMENT_TARGET_ACCOUNT': (770,125,420),
            'TARGET_SELECTION': (60,390,420), 'ACTION_EXECUTION': (770,330,420),
            'ACTION_TARGET_BINDING': (770,570,420),
            'RESOLVED_TARGET_MEMBERSHIP': (60,880,420), 'RESOURCE_IDENTITY': (770,910,420),
            'TARGET_RESOLUTION_OBSERVATION': (60,1190,420),
        },
        'routes': {
            r('EXPERIMENT_RUN','defines','TARGET_SELECTION'): ([(270,207),(270,390)],(270,306)),
            r('EXPERIMENT_RUN','configures','EXPERIMENT_TARGET_ACCOUNT'): ([(480,166),(770,166)],(625,148)),
            r('ACTION_EXECUTION','binds','ACTION_TARGET_BINDING'): ([(980,412),(980,570)],(980,498)),
            r('TARGET_SELECTION','referenced_by','ACTION_TARGET_BINDING'): ([(480,470),(625,470),(625,650),(770,650)],(625,553)),
            r('TARGET_SELECTION','resolves_to','RESOLVED_TARGET_MEMBERSHIP'): ([(270,612),(270,880)],(270,753)),
            r('RESOURCE_IDENTITY','identifies','RESOLVED_TARGET_MEMBERSHIP'): ([(770,951),(480,951)],(625,932)),
            r('TARGET_SELECTION','observed_by','TARGET_RESOLUTION_OBSERVATION'): ([(60,501),(25,501),(25,1231),(60,1231)],(45,785,-90)),
        },
    },
    '04_evidence_reports': {
        'height': 1500,
        'title': '04 / Evidence, reports and safety observations',
        'nodes': {
            'AWS_SCOPE': (60,125,350), 'SAFETY_LEVER': (850,125,350),
            'EXPERIMENT_RUN': (60,350,350), 'ACTION_EXECUTION': (850,350,350),
            'EXECUTION_EVIDENCE': (60,650,350), 'STATE_OBSERVATION': (850,650,350),
            'EXPERIMENT_REPORT': (480,990,350),
            'STOP_CONDITION': (60,1170,350), 'CLOUDWATCH_ALARM': (850,1170,350),
            'REPORT_ARTIFACT': (480,1320,350), 'ALARM_OBSERVATION': (850,1320,350),
        },
        'routes': {
            r('EXPERIMENT_RUN','accumulates','EXECUTION_EVIDENCE'): ([(150,432),(150,650)],(150,550)),
            r('EXPERIMENT_RUN','observed_by','STATE_OBSERVATION'): ([(410,391),(620,391),(620,490),(825,490),(825,680),(850,680)],(620,474)),
            r('ACTION_EXECUTION','optionally_identifies','EXECUTION_EVIDENCE'): ([(850,391),(780,391),(780,550),(325,550),(325,650)],(545,535)),
            r('ACTION_EXECUTION','optionally_identifies','STATE_OBSERVATION'): ([(1025,432),(1025,650)],(1025,550)),
            r('EXECUTION_EVIDENCE','may_support','STATE_OBSERVATION'): ([(410,710),(850,710)],(630,693)),
            r('EXPERIMENT_RUN','generates','EXPERIMENT_REPORT'): ([(345,432),(445,460),(445,1031),(480,1031)],(461,830,-90)),
            r('EXPERIMENT_REPORT','contains','REPORT_ARTIFACT'): ([(655,1072),(655,1320)],(655,1265)),
            r('EXPERIMENT_RUN','configures','STOP_CONDITION'): ([(60,391),(25,391),(25,1211),(60,1211)],(44,1040,-90)),
            r('CLOUDWATCH_ALARM','referenced_by','STOP_CONDITION'): ([(850,1211),(410,1211)],(630,1193)),
            r('CLOUDWATCH_ALARM','observed_by','ALARM_OBSERVATION'): ([(1025,1252),(1025,1320)],(1130,1293)),
            r('AWS_SCOPE','owns','EXPERIMENT_RUN'): ([(235,207),(235,350)],(235,286)),
            r('AWS_SCOPE','has','SAFETY_LEVER'): ([(410,166),(850,166)],(630,148)),
        },
    },
    '05_assessments': {
        'height': 1240,
        'title': '05 / Workload criteria and assessment evidence',
        'nodes': {
            'EXPERIMENT_RUN': (60,125,350), 'METRIC_BINDING': (850,125,350),
            'EXPERIMENT_METRIC_BINDING': (470,390,350),
            'ASSESSMENT_CRITERION': (60,675,310), 'RESILIENCE_ASSESSMENT': (470,675,350),
            'METRIC_OBSERVATION': (850,675,350), 'ASSESSMENT_EVIDENCE': (470,1075,350),
        },
        'routes': {
            r('EXPERIMENT_RUN','binds','EXPERIMENT_METRIC_BINDING'): ([(410,166),(445,166),(445,431),(470,431)],(445,301)),
            r('METRIC_BINDING','used_by','EXPERIMENT_METRIC_BINDING'): ([(850,166),(830,166),(830,431),(820,431)],(830,300)),
            r('METRIC_BINDING','supplies','METRIC_OBSERVATION'): ([(1025,207),(1025,675)],(1025,447)),
            r('EXPERIMENT_RUN','assessed_by','RESILIENCE_ASSESSMENT'): ([(150,207),(150,570),(420,570),(420,805),(470,805)],(280,554)),
            r('ASSESSMENT_CRITERION','evaluates','RESILIENCE_ASSESSMENT'): ([(370,716),(470,716)],(420,698)),
            r('RESILIENCE_ASSESSMENT','cites','ASSESSMENT_EVIDENCE'): ([(645,1009),(645,1075)],(740,1045)),
            r('METRIC_OBSERVATION','supports','ASSESSMENT_EVIDENCE'): ([(1025,757),(1025,1116),(820,1116)],(1025,950)),
        },
    },
}


def cardinality_label(scene: Scene, point: tuple[float, float], toward: tuple[float, float], value: str) -> None:
    x, y = point
    dx, dy = toward[0] - x, toward[1] - y
    length = math.hypot(dx, dy)
    if not length:
        raise ValueError('Zero-length edge endpoint')
    ux, uy = dx / length, dy / length
    if abs(dx) > abs(dy):
        scene.label(x + ux * 24, y + 18, value, 15)
    else:
        scene.label(x + 29, y + uy * 23 + 5, value, 15)


def make_scene(stem: str, entities: dict[str, Entity], relations: list[Relation]) -> Scene:
    layout = LAYOUTS[stem]
    if set(entities) != set(layout['nodes']):
        raise ValueError(f'Entity/layout mismatch for {stem}: {set(entities) ^ set(layout["nodes"])}')
    if {r.key for r in relations} != set(layout['routes']):
        raise ValueError(f'Relationship/layout mismatch for {stem}')
    description = 'Logical ER model. Cardinalities are counts at each endpoint. ' + '; '.join(
        f'{r.left} ({CARD[r.left_card]}) {r.label.replace("_", " ")} '
        f'{r.right} ({CARD[r.right_card]})' for r in relations
    )
    scene = Scene(1250, layout['height'], layout['title'], description)
    scene.rect(0, 0, scene.width, scene.height, WHITE)
    scene.rect(50, 30, 42, 5, TEAL)
    scene.text(50, 76, layout['title'], 30, INK, 'bold')
    scene.text(50, 101, 'Logical model | Endpoint labels show multiplicity | Source: canonical Mermaid', 15, MUTED)
    # All connector strokes precede cards and labels.
    for rel in relations:
        points, _ = layout['routes'][rel.key]
        scene.line(points, WHITE, 6)
        scene.line(points)
    for name, entity in entities.items():
        x, y, w = layout['nodes'][name]
        h = node_height(entity)
        if x < 0 or y < 0 or x + w > scene.width or y + h > scene.height - 60:
            raise ValueError(f'Node outside figure bounds: {stem}/{name}')
        kind, color = kind_for(name)
        scene.rect(x, y, w, h, WHITE, BORDER, 8, 1.3)
        scene.rect(x, y, w, 42, color, radius=8)
        scene.rect(x, y + 28, w, 14, color)
        title = display_name(name)
        font_size = min(23, (w - 32) / pdfmetrics.stringWidth(title, BOLD, 1))
        scene.text(x + 16, y + 29, title, font_size, WHITE, 'bold')
        scene.text(x + 16, y + 65, kind, 14, MUTED)
        for index, (datatype, attr, keys) in enumerate(entity.attributes):
            baseline = y + 98 + index * 28
            if index % 2 == 0:
                scene.rect(x + 1, baseline - 21, w - 2, 28, '#F4F7F9')
            key_text = keys.replace(', ', ' ')
            if key_text:
                scene.text(x + 16, baseline, key_text, 12, color, 'bold')
            size = min(19.5, (w - 146) / pdfmetrics.stringWidth(attr, FONT, 1))
            scene.text(x + 80, baseline, attr, size)
            scene.text(x + w - 14, baseline, datatype, 12.5, MUTED, align='right', mono=True)
    for rel in relations:
        points, label = layout['routes'][rel.key]
        lx, ly = label[:2]
        angle = label[2] if len(label) == 3 else 0
        scene.label(lx, ly, rel.label.replace('_', ' '), angle=angle)
        cardinality_label(scene, points[0], points[1], CARD[rel.left_card])
        cardinality_label(scene, points[-1], points[-2], CARD[rel.right_card])
    foot_y = scene.height - 30
    for x, color, label in [(50,TEAL,'AWS FIS data / scope'),(420,AMBER,'Application model'),(830,BLUE,'External evidence / resource')]:
        scene.rect(x, foot_y - 13, 15, 15, color, radius=3)
        scene.text(x + 25, foot_y, label, 16, MUTED)
    return scene


class SceneFlowable(Flowable):
    def __init__(self, scene: Scene):
        super().__init__()
        self.scene = scene
        self.width = CONTENT_W
        self.height = scene.height * self.width / scene.width

    def draw(self) -> None:
        self.scene.draw_pdf(self.canv, self.width)


def styles() -> dict[str, ParagraphStyle]:
    common = dict(fontName=FONT, textColor=colors.HexColor(INK), splitLongWords=True,
                  allowWidows=False, allowOrphans=False)
    def style(name: str, **kwargs: Any) -> ParagraphStyle:
        return ParagraphStyle(name, **(common | kwargs))
    return {
        'title': style('title', fontSize=26, leading=32, spaceAfter=10, fontName=BOLD),
        'h2': style('h2', fontSize=18, leading=23, spaceAfter=12, fontName=BOLD, keepWithNext=True),
        'h3': style('h3', fontSize=12, leading=17, spaceBefore=11, spaceAfter=7, fontName=BOLD, keepWithNext=True),
        'body': style('body', fontSize=9.25, leading=14, spaceAfter=8),
        'small': style('small', fontSize=8.1, leading=12, spaceAfter=8, textColor=colors.HexColor(MUTED)),
        'cell': style('cell', fontSize=8.0, leading=11.8),
        'head': style('head', fontSize=8.2, leading=11.8, textColor=colors.white, fontName=BOLD),
        'bullet': style('bullet', fontSize=9.25, leading=14, spaceAfter=6, leftIndent=13, firstLineIndent=-10),
        'source': style('source', fontSize=8.1, leading=12.3, spaceAfter=8),
    }


def inline(text: str, refs: dict[str, str]) -> str:
    tokens: list[str] = []
    def save(value: str) -> str:
        tokens.append(value)
        return f'ZZTOKEN{len(tokens)-1}ZZ'
    text = re.sub(r'`([^`]+)`', lambda m: save(f'<font name="{MONO}" size="8">{escape(m.group(1))}</font>'), text)
    def link_match(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        if not re.match(r'https?://', url):
            route = 'tree' if url.endswith('/') else 'blob'
            url = f'{REPOSITORY}/{route}/main/{REPO_PATH}/{url}'
        return save(f'<link href="{escape(url, {chr(34): "&quot;"})}" color="{BLUE}">{escape(label)}</link>')
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link_match, text)
    text = re.sub(r'\[(S\d+)\]', lambda m: save(f'<link href="{refs[m.group(1)]}" color="{BLUE}">[{m.group(1)}]</link>'), text)
    text = escape(text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    for i, token in enumerate(tokens):
        text = text.replace(f'ZZTOKEN{i}ZZ', token)
    return text


def split_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip('|').split('|')]


class ReportDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable: Flowable) -> None:
        if isinstance(flowable, Paragraph) and flowable.style.name == 'h2':
            title = flowable.getPlainText()
            key = 'section-' + re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title, key, level=0, closed=False)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_sources(report: Path) -> tuple[str, dict[str, str], dict[str, str]]:
    """Validate canonical inputs before any rendering or output mutation."""
    text = report.read_text()
    if re.search(r'\{\{(?:DIAGRAM:|SOURCE_REGISTER)', text):
        raise ValueError('The canonical report must not contain unexpanded placeholders')
    front_matter = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not front_matter:
        raise ValueError('Report metadata is missing')
    metadata: dict[str, str] = {}
    for line in front_matter.group(1).splitlines():
        key, separator, value = line.partition(':')
        if not separator or key in metadata:
            raise ValueError(f'Unsupported or duplicate report metadata: {line}')
        metadata[key] = value.strip().strip('"')
    if any(not metadata.get(key) for key in ('title', 'version', 'review_date')):
        raise ValueError('Report metadata requires title, version, and review_date')
    dt.date.fromisoformat(metadata['review_date'])
    reference_items = re.findall(r'^\[(S\d+)\]:\s+(\S+)\s*$', text, re.M)
    refs = dict(reference_items)
    if len(refs) != len(reference_items):
        raise ValueError('Markdown source IDs must be unique')
    source_records = json.loads((BASE / 'sources.json').read_text())['sources']
    source_refs = {source['id']: source['url'] for source in source_records}
    if len(source_refs) != len(source_records) or refs != source_refs:
        raise ValueError('Markdown references must exactly match the source register')
    if len(set(source_refs.values())) != len(source_refs):
        raise ValueError('Source URLs must be unique')
    for token in re.findall(r'\[(S\d+(?:-S\d+)?)\]', text):
        if '-' in token:
            start, end = (int(part[1:]) for part in token.split('-'))
            if start > end or end - start > len(refs):
                raise ValueError(f'Invalid source range: {token}')
            ids = [f'S{number:02d}' for number in range(start, end + 1)]
        else:
            ids = [token]
        if any(source_id not in refs for source_id in ids):
            raise ValueError(f'Unknown source citation: {token}')
    diagram_blocks = re.findall(r'<!-- diagram-source: diagrams/(\S+) -->\n```mermaid\n(.*?)\n```', text, re.S)
    expected_files = {f'{stem}.mmd' for stem in LAYOUTS}
    if (len(diagram_blocks) != len(expected_files)
            or {filename for filename, _ in diagram_blocks} != expected_files
            or len(re.findall(r'^```mermaid$', text, re.M)) != len(expected_files)):
        raise ValueError('Expected each canonical embedded diagram exactly once')
    for filename, block in diagram_blocks:
        if block + '\n' != (BASE / 'diagrams' / filename).read_text():
            raise ValueError(f'Markdown/Mermaid content mismatch: {filename}')
    return text, refs, metadata


def input_hashes() -> dict[str, str]:
    paths = ['report.md', 'sources.json', 'tools/render_report.py']
    paths += [f'diagrams/{stem}.mmd' for stem in LAYOUTS]
    return {path: digest(BASE / path) for path in paths}


def report_is_current(report: dict[str, Any], inputs: dict[str, str]) -> bool:
    output = BASE / 'aws_fis_experiment_action_model.pdf'
    return bool(report and report.get('inputHashes') == inputs
                and report.get('output') == output.name and output.is_file()
                and report.get('bytes') == output.stat().st_size
                and report.get('sha256') == digest(output))


def check_artifacts(manifest: dict[str, Any], scenes: dict[str, Scene],
                    inputs: dict[str, str], metadata: dict[str, str]) -> None:
    """Check existing artifacts; never regenerate or update their attestations."""
    if manifest.get('schema') != 'frontier-fis-render/v2':
        raise ValueError('Render manifest requires a full build with schema v2')
    if manifest.get('inputHashes') != inputs:
        raise ValueError('Manifest inputs are stale; regenerate the complete report')
    records = manifest.get('diagrams', [])
    if len(records) != len(scenes):
        raise ValueError('Manifest diagram count does not match the canonical model')
    by_source = {record['source']: record for record in records}
    if len(by_source) != len(records):
        raise ValueError('Manifest contains duplicate diagram records')
    for stem, scene in scenes.items():
        source_path = f'diagrams/{stem}.mmd'
        output_path = f'diagrams/{stem}.svg'
        record = by_source.get(source_path, {})
        output = BASE / output_path
        if not output.is_file() or output.read_text() != scene.svg():
            raise ValueError(f'SVG is stale or missing: {output_path}')
        if (record.get('output') != output_path
                or record.get('sourceSha256') != inputs[source_path]
                or record.get('outputSha256') != digest(output)):
            raise ValueError(f'Diagram manifest mismatch: {output_path}')
    report = manifest.get('report', {})
    if report.get('status') != 'current' or not report_is_current(report, inputs):
        raise ValueError('PDF is stale or missing; --svg-only does not rebuild or validate the PDF')
    if report.get('version') != metadata['version'] or report.get('reviewDate') != metadata['review_date']:
        raise ValueError('PDF metadata differs from the canonical report')


def make_pdf(report: Path, scenes: dict[str, Scene], output: Path) -> dict[str, Any]:
    text, refs, metadata = validate_sources(report)
    reviewed = dt.date.fromisoformat(metadata['review_date'])
    review_label = f'{reviewed.day} {reviewed:%B %Y}'
    text = re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.S)
    lines = text.splitlines()
    st = styles()
    story: list[Flowable] = []
    section_titles: list[str] = []
    figure_names: list[str] = []
    pending_diagram: str | None = None
    i = 0
    section_count = 0
    def p(raw: str, name: str = 'body') -> Paragraph:
        return Paragraph(inline(raw, refs), st[name])
    while i < len(lines):
        line = lines[i].strip()
        if not line or re.match(r'^\[S\d+\]:', line):
            i += 1
            continue
        match = re.match(r'<!-- diagram-source: diagrams/(\S+) -->', line)
        if match:
            pending_diagram = Path(match.group(1)).stem
            i += 1
            continue
        if line.startswith('<!--'):
            i += 1
            continue
        if line == '```mermaid':
            if not pending_diagram:
                raise ValueError('Mermaid fence is missing source annotation')
            i += 1
            while i < len(lines) and lines[i].strip() != '```':
                i += 1
            i += 1
            items: list[Flowable] = []
            if story and isinstance(story[-1], Paragraph) and story[-1].style.name == 'h3':
                items.append(story.pop())
            if story and isinstance(story[-1], Paragraph) and story[-1].style.name == 'h2':
                items.insert(0, story.pop())
                # A section that opens with a diagram belongs to the same block.
                # Leaving a conditional break/spacer before it can create a blank
                # page when the grouped figure nearly fills a fresh frame.
                if story and isinstance(story[-1], Spacer):
                    story.pop()
                if story and isinstance(story[-1], CondPageBreak):
                    story.pop()
            items.append(SceneFlowable(scenes[pending_diagram]))
            while i < len(lines) and not lines[i].strip():
                i += 1
            if i < len(lines) and lines[i].strip().startswith('**Caption:**'):
                items.append(p(lines[i].strip(), 'small'))
                i += 1
            story.append(KeepTogether(items))
            story.append(Spacer(1,10))
            figure_names.append(pending_diagram)
            pending_diagram = None
            continue
        if line.startswith('# '):
            story.append(p(line[2:], 'title'))
            story.append(p(f'Reviewed edition {metadata["version"]} | {review_label} | AWS primary documentation', 'small'))
            i += 1
            continue
        if line.startswith('## '):
            title = line[3:]
            if section_count:
                if title == '14. Official sources':
                    story.append(PageBreak())
                else:
                    story.extend([CondPageBreak(150), Spacer(1, 15)])
            section_count += 1
            section_titles.append(title)
            story.append(p(title, 'h2'))
            i += 1
            continue
        if line.startswith('### '):
            story.append(p(line[4:], 'h3'))
            i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = split_cells(lines[i])
                if not all(re.fullmatch(r':?-+:?', cell.replace(' ','')) for cell in cells):
                    rows.append(cells)
                i += 1
            n = len(rows[0])
            if any(len(row) != n for row in rows):
                raise ValueError(f'Unbalanced Markdown table near {i}')
            # Content-aware fixed widths keep labels legible and explanatory cells roomy.
            if n == 2:
                fractions = [0.31,0.69]
            elif n == 3:
                fractions = [0.23,0.35,0.42]
            else:
                fractions = [1/n]*n
            data = [[p(cell,'head' if j == 0 else 'cell') for cell in row] for j,row in enumerate(rows)]
            table = Table(data, colWidths=[CONTENT_W*f for f in fractions], repeatRows=1, hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor(INK)),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
                ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor(PALE)]),
                ('LINEBELOW',(0,0),(-1,-1),.35,colors.HexColor(BORDER)),
            ]))
            story.extend([table,Spacer(1,10)])
            continue
        source = re.match(r'- \*\*\[(S\d+)\]\*\* (.+)', line)
        if source:
            key, title = source.groups()
            url = refs[key]
            story.append(Paragraph(f'<b>[{key}] {escape(title)}</b><br/>'
                                   f'<link href="{url}" color="{BLUE}">{escape(url)}</link>', st['source']))
            i += 1
            continue
        bullet = re.match(r'(?:- |(\d+)\. )(.+)', line)
        if bullet:
            number, body = bullet.groups()
            prefix = f'{number}. ' if number else '- '
            story.append(p(prefix + body, 'bullet'))
            i += 1
            continue
        parts = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith(('#','|','<!--','```','- ','[')) or re.match(r'^\d+\. ',nxt):
                break
            parts.append(nxt)
            i += 1
        story.append(p(' '.join(parts)))
    source_hash = hashlib.sha256(report.read_bytes()).hexdigest()
    def footer(c: canvas.Canvas, doc: SimpleDocTemplate) -> None:
        c.setStrokeColor(colors.HexColor(BORDER));c.setLineWidth(.5)
        c.line(MARGIN,38,PAGE_W-MARGIN,38)
        c.setFont(FONT,7.1);c.setFillColor(colors.HexColor(MUTED))
        c.drawString(MARGIN,25,f'AWS FIS | Reviewed experiment and action model | {reviewed.day} {reviewed:%b %Y}')
        c.drawRightString(PAGE_W-MARGIN,25,str(doc.page))
        if doc.page > 1:
            c.setFillColor(colors.HexColor(TEAL));c.rect(MARGIN,PAGE_H-23,25,3,fill=1,stroke=0)
    doc = ReportDoc(str(output),pagesize=A4,leftMargin=MARGIN,rightMargin=MARGIN,
                    topMargin=34,bottomMargin=52,title='AWS FIS experiment and action model - reviewed edition',
                    author='Frontier Agents',subject='Reviewed API model, ER diagrams, derived data and operator UI')
    doc.build(story,onFirstPage=footer,onLaterPages=footer,
              canvasmaker=lambda *a,**k: canvas.Canvas(*a,**(k | {'invariant':1})))
    return dict(reportSha256=source_hash, version=metadata['version'],
                reviewDate=metadata['review_date'], sections=section_titles, figures=figure_names)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--svg-only', action='store_true', help='Regenerate diagrams; preserve the PDF build record and mark it stale when needed')
    mode.add_argument('--check', action='store_true', help='Validate existing sources, SVGs, manifest and PDF hashes without changing files')
    args = parser.parse_args()
    _, _, metadata = validate_sources(BASE / 'report.md')
    register_fonts()
    scenes = {}
    inputs = input_hashes()
    manifest: dict[str, Any] = {'schema':'frontier-fis-render/v2','source':'report.md',
                                'inputHashes':inputs,'diagrams':[]}
    for stem in LAYOUTS:
        source = BASE / 'diagrams' / f'{stem}.mmd'
        entities, relations = parse_mermaid(source)
        scene = make_scene(stem,entities,relations)
        scenes[stem] = scene
        target = source.with_suffix('.svg')
        manifest['diagrams'].append(dict(source=str(source.relative_to(BASE)),
                                        output=str(target.relative_to(BASE)),entities=len(entities),
                                        relationships=len(relations),sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                                        outputSha256=hashlib.sha256(scene.svg().encode()).hexdigest()))
    manifest_path = BASE / 'tools/render-manifest.json'
    if args.check:
        check_artifacts(json.loads(manifest_path.read_text()), scenes, inputs, metadata)
        print(json.dumps({'status':'valid','svgFiles':len(scenes),
                          'reportVersion':metadata['version'],'filesChanged':0}))
        return
    for stem, scene in scenes.items():
        (BASE / 'diagrams' / f'{stem}.svg').write_text(scene.svg())
    if not args.svg_only:
        output = BASE / 'aws_fis_experiment_action_model.pdf'
        manifest['report'] = make_pdf(BASE/'report.md',scenes,output)
        manifest['report'].update(output=output.name,bytes=output.stat().st_size,
                                  sha256=digest(output),inputHashes=inputs,status='current',
                                  buildEnvironment={'python':platform.python_version(),
                                                    'reportlab':reportlab.Version,
                                                    'fontFiles':FONT_FILES})
    elif manifest_path.is_file():
        previous = json.loads(manifest_path.read_text()).get('report')
        if previous:
            manifest['report'] = previous
            previous['status'] = 'current' if report_is_current(previous, inputs) else 'stale'
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'svgFiles':len(scenes),'pdf':manifest.get('report',{}).get('output'),
                      'pdfBytes':manifest.get('report',{}).get('bytes'),
                      'pdfStatus':manifest.get('report',{}).get('status','not_built'),
                      'manifest':'tools/render-manifest.json'}))


if __name__ == '__main__':
    main()
