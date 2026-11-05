#!/usr/bin/env python3
"""Render or verify the operational-analysis proposal's canonical Draw.io source.

The existing consolidated-console tool loads the pinned official Draw.io engine.
This wrapper checks the proposal contract, exports SVG/PNG, and binds outputs to
source, renderer, and runtime-pin hashes. --check is read-only and offline.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ANALYSIS = Path(__file__).resolve().parents[1]
PROPOSAL = ANALYSIS / 'proposals/operational-analysis'
DIAGRAMS = PROPOSAL / 'diagrams'
CONSOLE = ANALYSIS.parents[2] / 'consolidated-operations-console'
RENDERER = CONSOLE / 'tools/render_drawio.mjs'
PIN = CONSOLE / 'tools/drawio-runtime.json'
SOURCE = DIAGRAMS / 'OA01-domain-classes.drawio'
SVG = SOURCE.with_suffix('.svg')
PNG = SOURCE.with_suffix('.png')
REPORT = DIAGRAMS / 'render-report.json'
MANIFEST = DIAGRAMS / 'manifest.json'
ENTITIES = ['Subject', 'Analysis', 'Assertion', 'QueryRun', 'Evidence', 'Assessment', 'Review']
RELATIONSHIPS = [
    ('Analysis', '0..*', 'Subject', '1..*', 'targets'),
    ('Analysis', '1', 'Assertion', '0..*', 'owns'),
    ('Analysis', '1', 'QueryRun', '0..*', 'owns'),
    ('Analysis', '1', 'Assessment', '0..*', 'retains'),
    ('QueryRun', '0..1', 'Evidence', '0..*', 'acquires'),
    ('Assessment', '0..*', 'Assertion', '1..*', 'pins'),
    ('Assessment', '0..*', 'Evidence', '0..*', 'cites'),
    ('Review', '0..*', 'Assessment', '1', 'reviews'),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def info(path):
    return {'path': str(path.relative_to(PROPOSAL)), 'sha256': digest(path), 'bytes': path.stat().st_size}


def source_contract():
    xml = SOURCE.read_text()
    root = ET.fromstring(xml)
    pages = root.findall('diagram')
    require(len(pages) == 1, 'Expected one complete seven-entity Draw.io page')
    page = pages[0]
    require(page.get('id') == 'oa01-domain-classes', 'Unexpected native page id')
    classes = page.findall('.//object[@entity]')
    require(Counter(c.get('entity') for c in classes) == Counter(ENTITIES), 'Entity inventory differs from the seven-entity model')
    cells = {c.get('id'): c for c in page.findall('.//mxCell[@id]')}
    for cls in classes:
        name = cls.get('entity')
        fields = cells[cls.get('id') + '-fields'].get('value').splitlines()
        for value in ['id: Id', 'version: Integer', 'createdAt: Instant', 'updatedAt: Instant']:
            require(value in fields, f'{name} lacks common field {value}')
        require(set(('id', 'version', 'createdAt', 'updatedAt')) <= set(cls.get('displayFields').split(',')), f'{name} lacks common field metadata')
        immutable = name in ('Evidence', 'Assessment', 'Review')
        require(cls.get('versionPolicy') == ('immutable-version-1' if immutable else 'append-only-versions'), f'{name} version policy differs')
    require('revision' not in xml and 'resultEpoch' not in xml, 'Superseded version counter in Draw.io source')
    edges = page.findall('.//object[@relationshipIndex]')
    require(len(edges) == len(RELATIONSHIPS), 'Expected all eight associations')
    require({int(e.get('relationshipIndex')) for e in edges} == set(range(8)), 'Association indices are incomplete')
    for edge in edges:
        expected = RELATIONSHIPS[int(edge.get('relationshipIndex'))]
        actual = tuple(edge.get(k) for k in ['fromEntity', 'fromCardinality', 'toEntity', 'toCardinality', 'label'])
        require(actual == expected, f'Association metadata differs: {edge.get("id")}')
        cell = edge.find('mxCell')
        require((cell.get('source'), cell.get('target')) == ('class-' + expected[0], 'class-' + expected[2]), 'Association endpoints differ')
        for suffix, value in [('from', expected[1]), ('to', expected[3])]:
            require(cells[edge.get('id') + '-' + suffix].get('value') == value, 'Visible cardinality differs from metadata')
    model = page.find('mxGraphModel')
    return {'id': page.get('id'), 'entities': ENTITIES, 'relationships': len(edges), 'width': int(model.get('pageWidth')), 'height': int(model.get('pageHeight'))}


def renderer_bindings():
    return {'wrapperSha256': digest(Path(__file__)), 'rendererSha256': digest(RENDERER), 'runtimePinSha256': digest(PIN)}


def validate_exports():
    svg = ET.parse(SVG).getroot()
    ns = {'s': 'http://www.w3.org/2000/svg'}
    require(svg.get('role') == 'img' and svg.get('aria-labelledby'), 'SVG lacks accessible image metadata')
    title = svg.find('s:title', ns)
    require(title is not None and title.get('id') in svg.get('aria-labelledby').split(), 'SVG accessible title is not bound')
    for dimension in ['width', 'height']:
        require(float(svg.get(dimension)) > 0, 'SVG dimensions must be positive numeric values')
    require(svg.find('.//s:foreignObject', ns) is None, 'SVG must use portable SVG text')
    report = json.loads(REPORT.read_text())
    require(report.get('sourceSha256') == digest(SOURCE), 'Render report source provenance is stale')
    require(len(report['pages']) == 1, 'Render report page count differs')
    page = report['pages'][0]
    require(page['svgSha256'] == digest(SVG), 'Render report SVG provenance is stale')
    for key in ['classOverlaps', 'connectorIntrusions', 'labelIntrusions', 'textOverflows']:
        require(page.get(key) == [], 'Unresolved diagram geometry issue: ' + key)
    require(page['nativeCodecRoundTrip'] == {'entities': 7, 'relationships': 8, 'metadataPreserved': True}, 'Missing native Draw.io codec verification')
    require(report['geometryControls'] == {'overlappingClassesRejected': True, 'connectorThroughClassRejected': True, 'separatedGeometryAccepted': True}, 'Missing geometry negative controls')
    require(PNG.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), 'Missing raster preview')
    return report


def check():
    source_contract()
    report = validate_exports()
    manifest = json.loads(MANIFEST.read_text())
    require(manifest.get('kind') == 'proposal-diagram-registry', 'Unexpected registry kind')
    require(manifest.get('entities') == ENTITIES, 'Registry entity inventory differs')
    require(manifest.get('renderBindings') == renderer_bindings(), 'Renderer or runtime pin changed; regenerate outputs')
    for key, path in [('drawio', SOURCE), ('svg', SVG), ('png', PNG), ('renderReport', REPORT)]:
        require(manifest.get(key) == info(path), 'Stale artifact provenance: ' + key)
    require(manifest.get('renderer') == report['renderer'], 'Renderer provenance differs')
    entry = manifest.get('diagrams', [None])[0]
    require(len(manifest.get('diagrams', [])) == 1 and entry == {
        'id': 'OA01', 'title': 'Seven entities for operational analysis',
        'filename': 'diagrams/OA01-domain-classes.drawio', 'rendered': 'diagrams/OA01-domain-classes.svg',
        'source': 'README.md', 'type': 'class', 'format': 'drawio',
    }, 'Registry diagram contract differs')
    require(not list(DIAGRAMS.glob('*.mmd')), 'Superseded Mermaid source remains')
    print('Proposal Draw.io source and SVG/PNG hashes match: 7 versioned entities, 8 associations; native codec and geometry checks pass.')


def render():
    source_contract()
    with tempfile.TemporaryDirectory(prefix='oa-drawio-') as temporary:
        subprocess.run(['node', str(RENDERER), '--input', str(SOURCE), '--output', temporary], check=True)
        exported = Path(temporary)
        svg_text = (exported / 'oa01-domain-classes.svg').read_text()
        for dimension in ('width', 'height'):
            svg_text = re.sub(r'(?<= ' + dimension + r'=")([0-9.]+)px(?=")', r'\1', svg_text, count=1)
        SVG.write_text(svg_text)
        report = json.loads((exported / 'render-report.json').read_text())
        report['pages'][0]['svgSha256'] = digest(SVG)
        report['pages'][0]['svgBytes'] = SVG.stat().st_size
        report['svgMetadataNormalization'] = 'Root width and height are numeric pixels; geometry is unchanged.'
    report['sourceSha256'] = digest(SOURCE)
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    result = subprocess.run(['inkscape', str(SVG), '--export-type=png', '--export-filename=' + str(PNG)], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('Inkscape raster export failed: ' + result.stderr)
    rasterizer = subprocess.run(['inkscape', '--version'], capture_output=True, text=True, check=True).stdout.strip()
    manifest = {
        'schemaVersion': 1, 'kind': 'proposal-diagram-registry', 'proposal': 'operational-analysis',
        'entities': ENTITIES, 'renderer': report['renderer'], 'rasterizer': rasterizer,
        'drawio': info(SOURCE), 'svg': info(SVG), 'png': info(PNG), 'renderReport': info(REPORT),
        'renderBindings': renderer_bindings(),
        'diagrams': [{'id': 'OA01', 'title': 'Seven entities for operational analysis',
                      'filename': 'diagrams/OA01-domain-classes.drawio', 'rendered': 'diagrams/OA01-domain-classes.svg',
                      'source': 'README.md', 'type': 'class', 'format': 'drawio'}],
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + '\n')
    obsolete = SOURCE.with_suffix('.mmd')
    if obsolete.exists():
        obsolete.unlink()
    check()
    print('Exported with pinned Draw.io 32.6.10 SVG engine; PNG rasterized with ' + rasterizer + '.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify retained source, output and renderer hashes without rendering')
    parser.add_argument('--write', action='store_true', help='Regenerate SVG, PNG, manifest and render report (default)')
    args = parser.parse_args()
    if args.check and args.write:
        parser.error('--check and --write are mutually exclusive')
    try:
        check() if args.check else render()
    except (ValueError, KeyError, ET.ParseError) as error:
        raise SystemExit(str(error))
