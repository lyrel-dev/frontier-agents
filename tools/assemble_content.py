#!/usr/bin/env python3
"""Assemble modular narratives and validate presentation source before building."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
KEYS = ('devops', 'kiro', 'security', 'finops', 'architecture')


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main() -> None:
    agents = {}
    results = []
    # Correct transcription errors in the initial source import. Once the
    # canonical JSON is committed, these exact-match repairs are no-ops.
    repairs = {
        'security': [ ('"headers":[Workflow"', '"headers":["Workflow"') ],
        'architecture': [ ('"F11"],],"caps"', '"F11"],"caps"') ],
    }
    for key in KEYS:
        narrative = json.loads((ROOT/'content'/'narratives'/f'{key}.json').read_text(encoding='utf-8'))
        assert len(narrative['stages']) == 6, key
        assert all(len(s['paragraphs']) >= 2 and s['gate'] and s['fallback'] for s in narrative['stages']), key
        agents[key] = narrative
        path = ROOT/'content'/f'{key}-presentation.json'
        raw = path.read_text(encoding='utf-8')
        for old, new in repairs.get(key, []):
            raw = raw.replace(old, new)
        deck = json.loads(raw)
        for slide in deck['slides']:
            if slide['takeaway'] == 'Pilot success is less verified work—not more generated text.':
                slide['takeaway'] = 'Pilot success is less effort per verified outcome—not more generated text.'
            # One-time editorial repair after rendered-slide review. The detailed
            # reconciliation limits remain in the speaker notes and report.
            if key == 'finops' and slide['kind'] == 'demo' and slide['prompt'].startswith('For authorized real data, compare storage costs'):
                slide['prompt'] = 'Reconcile synthetic totals of $1,400 and $1,974 (41% higher). This fixture cannot establish drivers. For authorized real data, match periods and cost basis before testing usage, rate and change hypotheses. Do not modify infrastructure.'
                slide['steps'][1][2] = 'Reconcile the fixture totals; require source breakdowns for any driver claim.'
            assert slide['notes'].strip(), (key, slide['title'])
            assert all(ref in deck['sources'] for ref in slide.get('refs', [])), (key, slide['title'])
            if slide['kind'] == 'demo':
                assert sum(step[0] for step in slide['steps']) == slide['seconds'], (key, slide['title'])
        assert sum(s['seconds'] for s in deck['slides']) == deck['minutes'] * 60, key
        assert sum(s['seconds'] for s in deck['slides'] if s['kind'] == 'demo') == deck['demo'] * 60, key
        write_json(path, deck)
        results.append({'agent': key, 'stages': len(narrative['stages']), 'slides': len(deck['slides']), 'minutes': deck['minutes'], 'demo_minutes': deck['demo'], 'source_references_valid': True})
    write_json(ROOT/'content/narratives.json', {
        'revision': '2026-10-21-editorial-v2',
        'scope': 'Independent engineering field guides; documented product behavior, proposed team workflows, and illustrative examples are labeled separately. No live AWS execution or measured benefit is claimed.',
        'agents': agents,
    })
    write_json(ROOT/'qa/source-validation.json', {
        'revision': '2026-10-21-editorial-v2',
        'checks': results,
        'boundary': 'Structural and timing validation of source files, not verification of external source content or live AWS behavior.'
    })
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
