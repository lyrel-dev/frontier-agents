#!/usr/bin/env python3
"""Validate and assemble the supported documentation source."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
KEYS=('devops','security','finops','architecture')
def main():
    agents={};checks=[]
    for key in KEYS:
        n=json.loads((ROOT/f'content/narratives/{key}.json').read_text())
        assert len(n['stages'])==6
        d=json.loads((ROOT/f'content/{key}-presentation.json').read_text())
        e=json.loads((ROOT/f'content/{key}-evidence.json').read_text())
        caps={x['id'] for x in e.get('capabilities',e.get('patterns',[]))}
        for s in d['slides']:
            assert s['notes'].strip()
            assert set(s.get('refs',[]))<=set(d['sources'])
            assert set(s.get('caps',[]))<=caps
            if s['kind']=='demo':assert sum(x[0] for x in s['steps'])==s['seconds']
        assert sum(x['seconds'] for x in d['slides'])==60*d['minutes']
        assert sum(x['seconds'] for x in d['slides'] if x['kind']=='demo')==60*d['demo']
        agents[key]=n;checks.append({'report':key,'slides':len(d['slides']),'minutes':d['minutes'],'demo_minutes':d['demo'],'source_references_valid':True})
    revision=json.loads((ROOT/'documentation-build.json').read_text())['revision']
    (ROOT/'content/narratives.json').write_text(json.dumps({'revision':revision,'scope':'Three AWS agents and proposed shared operating patterns; no live execution or measured benefit.','agents':agents},ensure_ascii=False,indent=2)+'\n')
    (ROOT/'qa').mkdir(exist_ok=True)
    (ROOT/'qa/source-validation.json').write_text(json.dumps({'revision':revision,'checks':checks,'boundary':'Structural and timing validation, not live product testing.'},indent=2)+'\n')
if __name__=='__main__':main()
