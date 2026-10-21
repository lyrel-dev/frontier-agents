#!/usr/bin/env python3
"""Validate the three-agent publication, including text inside presentation files.

Removed names are derived from the prior Git revision, never stored in this tree.
An existing input package can supply the baseline for an offline local check.
This program does not create compressed distributions or historical snapshots.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from urllib.parse import urlparse
from zipfile import ZipFile
from pptx import Presentation

ROOT=Path(__file__).resolve().parents[1]
REPORTS={'devops','security','finops','architecture'}
AGENTS=REPORTS-{'architecture'}
BASE='c1c810b48e2349d3fb2479402c767a2834c76b9a'

def load(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--baseline-package');args=parser.parse_args()
    def baseline(path):
        if args.baseline_package:
            with ZipFile(args.baseline_package) as z:return json.loads(z.read(path))
        return json.loads(subprocess.check_output(['git','-C',str(ROOT),'show',f'{BASE}:{path}']))
    old=baseline('content/narratives.json')['agents']
    names={v['title'] for k,v in old.items() if k not in REPORTS}
    existing_products={c.get('product','') for k in AGENTS for c in load(f'content/{k}-evidence.json')['capabilities']}
    for k in AGENTS:
        names.update(c.get('product','') for c in baseline(f'content/{k}-evidence.json').get('capabilities',[]) if c.get('product','') not in existing_products)
    terms={v.casefold() for n in names for v in [n,n.removesuffix(' Developer')] if v}
    known_hosts={urlparse(s['url']).netloc for k in REPORTS for s in load(f'content/{k}-evidence.json')['sources']}
    for k in REPORTS:
        new_urls={s['url'] for s in load(f'content/{k}-evidence.json')['sources']}
        for s in baseline(f'content/{k}-evidence.json')['sources']:
            u=urlparse(s['url'])
            if u.netloc not in known_hosts:terms.add(u.netloc.casefold())
            if s['url'] not in new_urls and '/latest/' in u.path:
                current_roots={urlparse(a).path.split('/')[1] for a in new_urls if '/latest/' in a}
                root=u.path.split('/')[1]
                if root not in current_roots:
                    terms.add(root.casefold())
                    terms.update(x.casefold() for x in u.path.split('/') if x.endswith('-ug'))
    errors=[];files=0;parts=0;decks=[]
    for forbidden in ['archive','dist','tools/migrations']:
        if (ROOT/forbidden).exists():errors.append('Unsupported retained directory: '+forbidden)
    if {p.stem for p in (ROOT/'content/narratives').glob('*.json')}!=REPORTS:errors.append('Narrative catalog outside approved scope')
    if set(load('content/narratives.json')['agents'])!=REPORTS:errors.append('Assembled narrative scope differs')
    m=load('content/mechanisms.json')
    if set(m['agents'])!=AGENTS:errors.append('Mechanism catalog outside approved scope')
    if {p.stem for p in (ROOT/'content/platforms').glob('*.json')}!=AGENTS:errors.append('Platform reference catalog outside approved scope')
    expected_pptx={
        'aws-devops-agent-presentation.pptx','aws-security-agent-presentation.pptx',
        'aws-finops-agent-presentation.pptx','aws-frontier-agents-common-architecture-presentation.pptx',
        'devops-mechanisms-reference.pptx','security-mechanisms-reference.pptx',
        'finops-mechanisms-reference.pptx','overview-mechanisms-reference.pptx',
        'devops-platform-reference.pptx','security-platform-reference.pptx','finops-platform-reference.pptx'
    }
    if {p.name for p in (ROOT/'presentations').glob('*.pptx')}!=expected_pptx:errors.append('Presentation catalog outside approved scope')
    def check(text,location):
        if any(t in text.casefold() for t in terms):errors.append('Excluded-scope text: '+location)
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file() or any(x in p.parts for x in ['.git','__pycache__']):continue
        rel=p.relative_to(ROOT).as_posix();files+=1;check(rel,rel+' (path)')
        if p.suffix in {'.zip','.b64','.bundle','.tar','.gz'}:errors.append('Unsupported stored package: '+rel)
        if p.suffix=='.pptx':
            with ZipFile(p) as z:
                for n in z.namelist():
                    if n.endswith(('.xml','.rels')):parts+=1;check(z.read(n).decode('utf-8'),rel+':'+n)
            prs=Presentation(p);bad=[]
            for i,s in enumerate(prs.slides,1):
                if not s.notes_slide.notes_text_frame.text.strip():bad.append(f'{i}: empty notes')
                for shape in s.shapes:
                    if min(shape.left,shape.top)<-30000 or shape.left+shape.width>prs.slide_width+30000 or shape.top+shape.height>prs.slide_height+30000:bad.append(f'{i}: shape out of bounds')
            errors.extend(rel+': '+x for x in bad);decks.append({'file':rel,'slides':len(prs.slides),'errors':bad})
        else:
            try:check(p.read_text(encoding='utf-8'),rel)
            except UnicodeDecodeError:pass
    counts={k:len(load(f'content/{k}-evidence.json').get('capabilities',load(f'content/{k}-evidence.json').get('patterns',[]))) for k in sorted(REPORTS)}
    platform_counts={k:{'capabilities':len(load(f'content/platforms/{k}.json')['capabilities']),'mechanisms':len(load(f'content/platforms/{k}.json')['mechanisms'])} for k in sorted(AGENTS)}
    report={'revision':load('documentation-build.json')['revision'],'scope':['AWS DevOps Agent','AWS Security Agent','AWS FinOps Agent'],'shared_architecture':True,'baseline_commit':BASE,'text_files_and_presentations_checked':files,'presentation_xml_parts_checked':parts,'capability_and_pattern_counts':counts,'platform_reference_counts':platform_counts,'mechanism_records':sum(len(a['records']) for a in m['agents'].values()),'mechanism_source_references':len(m['sources']),'core_minutes':sum(load(f'content/{k}-presentation.json')['minutes'] for k in REPORTS),'core_demo_minutes':sum(load(f'content/{k}-presentation.json')['demo'] for k in REPORTS),'presentations':decks,'removed_scope_matches':sum(e.startswith('Excluded-scope') for e in errors),'errors':errors,'boundary':'Content, links, timing, notes and shape bounds are checked separately from runtime product behavior. Platform-reference counts are separate from the retained scenario-edition records. No new external documentation audit or live AWS run.'}
    (ROOT/'qa/scope-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    if errors:raise SystemExit(json.dumps(report,indent=2))
    manifest={}
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and not any(x in p.parts for x in ['.git','__pycache__']) and p.name!='MANIFEST.json':
            manifest[p.relative_to(ROOT).as_posix()]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    (ROOT/'MANIFEST.json').write_text(json.dumps({'revision':report['revision'],'files':manifest,'excluded':['MANIFEST.json itself','.git/','__pycache__/'],'history_policy':'Git history; no manually retained snapshots or compressed distributions'},indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
