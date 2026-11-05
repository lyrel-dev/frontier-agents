#!/usr/bin/env python3
"""Bundle the offline single-page demo. Python standard library only."""
from pathlib import Path
import json

APP = Path(__file__).resolve().parent
ANALYSIS = APP.parent
SRC = APP / 'src'
DIAGRAM_IDS = ['01-core-model', '02-history-delivery', '03-lifecycle-posture', '04-operator-workflow']

def main():
    content = (SRC / 'shell.html').read_text(encoding='utf-8')
    for token, filename in [('STYLES','styles.css'),('DATA','mock-data.js'),('MODEL','model.js'),('APP','app.js')]:
        text = (SRC / filename).read_text(encoding='utf-8')
        if token != 'STYLES':
            text = text.replace('</script', '<\\/script')
        content = content.replace('/*__' + token + '__*/', text)
    diagrams = {}
    for diagram_id in DIAGRAM_IDS:
        path = ANALYSIS / 'diagrams' / (diagram_id + '.svg')
        if not path.exists():
            raise SystemExit('Build reviewed diagrams first: missing ' + str(path))
        svg = path.read_text(encoding='utf-8')
        start = svg.find('<svg')
        diagrams[diagram_id] = svg[start:] if start >= 0 else svg
    diagram_js = 'globalThis.HealthDemoDiagrams = ' + json.dumps(diagrams, ensure_ascii=False).replace('</', '<\\/') + ';'
    content = content.replace('/*__DIAGRAMS__*/', diagram_js)
    assert '/*__' not in content, 'Unfilled bundle placeholder'
    output = ANALYSIS / 'index.html'
    output.write_text(content, encoding='utf-8')
    print(f'Built {output.name}: {len(content.encode("utf-8")):,} bytes; no runtime dependencies.')

if __name__ == '__main__':
    main()
