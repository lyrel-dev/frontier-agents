"""Educational and visual checks; not a substitute for content or service testing."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
BASELINE='1a62b5686ec361d1b4ab894df0a0ab249cfe1d78'
FROZEN=('use-cases','mechanisms','features','profiles','aliases','resource-models')


def validate(guides,browser=False):
    from presentation import DECKS
    from structure import CHAPTERS, DECK_CHAPTERS
    from teaching_diagrams import DIAGRAMS, BOXES, PRODUCTS
    errors=[];frozen={};coverage={};geometry={};screens=[]
    cases=json.loads((ROOT/'catalog/use-cases.json').read_text())['entries']
    for name in FROZEN:
        path=f'catalog/{name}.json';actual=(ROOT/path).read_bytes()
        prior=subprocess.check_output(['git','show',BASELINE+':'+path],cwd=ROOT)
        frozen[path]={'unchanged':prior==actual,'sha256':hashlib.sha256(actual).hexdigest()}
        if prior!=actual:errors.append('Frozen source changed: '+path)
    for p,d in DECKS.items():
        available={c['id'] for c in cases if p in c.get('platforms',[c['platform']])}
        covered={c for s in d['slides'] for c in s.get('cases',[])}
        if p!='architecture' and not available<=covered:errors.append(p+': missing use-case teaching coverage '+str(sorted(available-covered)))
        if not covered<={c['id'] for c in cases}:errors.append(p+': invented use-case identifier')
        if CHAPTERS[p][0]['slug']!='agent-overview':errors.append(p+': guide does not begin with the agent')
        if p!='architecture':
            opening=d['slides'][:5]
            keys=[s.get('diagram','') for s in opening]
            expected=[f'teaching-{p}-{v}' for v in ('agent','coordination','space')]
            if not all(k in keys for k in expected):errors.append(p+': opening lacks composition/coordination/scope')
            if [keys.index(k) for k in expected]!=sorted(keys.index(k) for k in expected):errors.append(p+': teaching expansion order')
            if d['slides'][0].get('diagram')!=expected[0]:errors.append(p+': first slide is not the agent composition diagram')
        for s in d['slides']:
            if s.get('diagram','').startswith('teaching-') and len(s.get('explain',[]))!=3:errors.append(p+': missing diagram walkthrough '+s['title'])
            if not set(s['refs'])<=set(guides[p]['sections']):errors.append(p+': unknown guide reference '+s['title'])
        coverage[p]={'slides':len(d['slides']),'minutes':sum(s['seconds'] for s in d['slides'])/60,
                     'exercise_minutes':sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')/60,
                     'use_cases':sorted(covered),'chapter_order':[t for t,_ in DECK_CHAPTERS[p]]}
    for key in DIAGRAMS:
        path=ROOT/f'assets/diagrams/{key}.svg';root=ET.parse(path).getroot()
        positions={n.attrib['data-node']:n.attrib['data-box'] for n in root.iter() if 'data-node' in n.attrib}
        for ident,position in positions.items():
            expected=','.join(str(x) for x in BOXES[ident])
            if position!=expected:errors.append(key+': moved component '+ident)
        if root.get('role')!='img':errors.append(key+': missing accessible diagram role')
        scope=next((n for n in root.iter() if n.get('data-scope-boundary')=='true'),None)
        if scope is not None:
            sx,sy,sw,sh=(float(scope.get(a)) for a in ('x','y','width','height'))
            for node in (n for n in root.iter() if 'data-node' in n.attrib):
                x,y,w,h=map(float,node.get('data-box').split(','))
                inside=x>=sx and y>=sy and x+w<=sx+sw and y+h<=sy+sh
                if node.get('data-node')=='result' and not inside:errors.append(key+': execution record shown outside scope')
                if node.get('data-owner')=='external' and inside:errors.append(key+': external source or actor placed inside scope')
        geometry[key]={'fixed_layout':root.get('data-layout'),'components':len(positions),'scope_boundary_checked':scope is not None}
    # The teaching view must not turn Security login reuse into an application-source write.
    sec=(ROOT/'assets/diagrams/teaching-security-context.svg').read_text()
    if 'data-edge="learning-knowledge"' in sec:errors.append('Security reuse incorrectly writes application context')
    if browser and not errors:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for p,d in DECKS.items():
                for width in (390,1440):
                    page=br.new_page(viewport={'width':width,'height':1000});js=[]
                    page.on('pageerror',lambda e:js.append(str(e)))
                    try:
                        page.goto((ROOT/f'presentations/{p}.html').as_uri())
                        if page.locator('.slide:visible').count()!=1:raise AssertionError('one visible teaching slide expected')
                        for i,s in enumerate(d['slides']):
                            page.locator('#slide-select').select_option(str(i))
                            if page.locator('.slide:visible h1').inner_text()!=s['title']:raise AssertionError('wrong slide title')
                            if page.evaluate('document.documentElement.scrollWidth>innerWidth+2'):raise AssertionError('horizontal page overflow')
                            if width==1440:
                                h=page.locator('.slide:visible').bounding_box()['height']
                                if h>1050:raise AssertionError(s['title']+': height '+str(h))
                            if s.get('diagram','').startswith('teaching-'):
                                clipped=page.locator('.slide:visible').evaluate('''root=>[...root.querySelectorAll('g[data-node]')].flatMap(g=>{const b=g.querySelector('rect').getBBox();return [...g.querySelectorAll('text')].filter(t=>{const x=t.getBBox();return x.x<b.x-1||x.y<b.y-1||x.x+x.width>b.x+b.width+2||x.y+x.height>b.y+b.height+2}).map(t=>({node:g.dataset.node,text:t.textContent}))})''')
                                if clipped:raise AssertionError(s['diagram']+': clipped node text '+json.dumps(clipped))
                                bad_markers=page.locator('.slide:visible').evaluate("""root=>[...root.querySelectorAll('svg[data-layout]')].flatMap(svg=>{const marker=svg.querySelector('marker');return [...svg.querySelectorAll('path[data-edge]')].filter(p=>!getComputedStyle(p).markerEnd.includes('#'+marker.id)).map(p=>p.dataset.edge)})""")
                                if bad_markers:raise AssertionError(s['diagram']+': missing scoped arrowheads '+str(bad_markers))
                        if js:raise AssertionError(str(js))
                        screens.append({'product':p,'width':width,'slides_checked':len(d['slides']),'diagram_text_bounds':'passed','scoped_arrowheads':'passed','page_overflow':'passed','javascript_errors':js})
                    except Exception as exc:errors.append(p+' at '+str(width)+': '+str(exc))
                    finally:page.close()
            br.close()
    result={'revision':'2026-10-23-educational-sequence','baseline':BASELINE,'frozen_sources':frozen,
            'presentation_sequences':coverage,'diagram_views':geometry,'browser':screens,'errors':errors,
            'boundary':'Teaching order, frozen content, case coverage and geometry checks. Not live AWS execution, complete fact verification or a claim that automated tests establish educational quality.'}
    (ROOT/'qa/educational-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
