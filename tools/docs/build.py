#!/usr/bin/env python3
"""Build the maintained narrative guides, use-case catalog, and HTML presentations.

Canonical prose lives in guides/*.md; catalog narratives live in JSON. This
renderer does not modify either source. Diagrams and presentations have their
own maintained definitions beside this file. No external runtime assets are used.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import html
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from markdown_it import MarkdownIt
from structure import CHAPTERS, DECK_CHAPTERS, LABELS, REVISION, section_type
from presentation import DECKS
from diagrams import DIAGRAMS, build as build_diagrams
import catalog as catalogue

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path(__file__).resolve().parent
MD=MarkdownIt('commonmark',{'html':False}).enable('table')
SID=r'[DSFA]-(?:M|U)?\d+'
HEADING=re.compile(r'^(#{2,3})\s+('+SID+r')\s+[—-]\s+(.+)$')
REF=re.compile(r'^\[([DSFA]S\d+)\]:\s+(https://\S+).*$',re.M)
PLATFORMS={'devops':'AWS DevOps Agent','security':'AWS Security Agent','finops':'AWS FinOps Agent','architecture':'Shared operational practice'}
PLATFORM_ORDER=tuple(PLATFORMS)


def esc(value): return html.escape(str(value),quote=True)
def write(path,text):
    dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(text.rstrip()+'\n',encoding='utf-8')
def stamp(seconds): return f'{int(seconds)//60:02d}:{int(seconds)%60:02d}'
def ordered_ids(key): return [sid for c in CHAPTERS[key] for sid in c['sections']]
def slug(text):return re.sub('[^a-z0-9]+','-',text.lower()).strip('-')
def totals(deck):
    return sum(s['seconds'] for s in deck['slides']),sum(s['seconds'] for s in deck['slides'] if s['kind']=='demo')

def parse_source(raw):
    refs=dict(REF.findall(raw));definitions='\n'.join(m[0] for m in REF.finditer(raw))
    lines=REF.sub('',raw).splitlines();starts=[];fence=None
    for i,line in enumerate(lines):
        marker=re.match(r'^\s*(`{3,}|~{3,})',line)
        if marker:
            char=marker[1][0];fence=char if fence is None else None if fence==char else fence
            continue
        if fence:continue
        m=HEADING.match(line)
        if m:starts.append((i,m[2],m[3]))
        elif re.match(r'^## \d{2}\. ',line):starts.append((i,None,None))
    if not starts:raise ValueError('Guide has no chapters or sections')
    sections={}
    for j,(i,sid,title) in enumerate(starts):
        if not sid:continue
        if sid in sections:raise ValueError('Duplicate section '+sid)
        end=starts[j+1][0] if j+1<len(starts) else len(lines)
        body='\n'.join(lines[i+1:end]).strip()
        sources=sorted(set(re.findall(r'\b[DSFA]S\d+\b',body)))
        missing=set(sources)-set(refs)
        if missing:raise ValueError(f'{sid}: undefined references {missing}')
        sections[sid]={'id':sid,'title':title,'body':body,'sources':sources}
    return {'intro':'\n'.join(lines[:starts[0][0]]).strip(),'sections':sections,'refs':refs,'definitions':definitions}

def load_guides():
    guides={}
    for key in DECKS:
        g=parse_source((ROOT/f'guides/{key}.md').read_text())
        if set(g['sections'])!=set(ordered_ids(key)):raise ValueError(key+': chapter membership differs from guide source')
        guides[key]=g
    return guides

def load_catalog():return json.loads((ROOT/'catalog/use-cases.json').read_text())

def inline_svg(key,prefix):
    path=ROOT/f'assets/diagrams/{key}.svg'
    soup=BeautifulSoup(path.read_text(),'html.parser');svg=soup.find('svg')
    if svg is None:raise ValueError('Missing SVG '+key)
    mapping={n['id']:prefix+'-'+n['id'] for n in svg.select('[id]')}
    for node in [svg,*svg.find_all(True)]:
        if node.has_attr('id'):node['id']=mapping[node['id']]
        for attr,value in list(node.attrs.items()):
            if not isinstance(value,str):continue
            if attr in ('aria-labelledby','aria-describedby'):node[attr]=' '.join(mapping.get(x,x) for x in value.split())
            elif attr in ('href','xlink:href') and value.startswith('#'):node[attr]='#'+mapping.get(value[1:],value[1:])
            elif 'url(#' in value:
                node[attr]=re.sub(r'url\(#([^)]*)\)',lambda m:'url(#'+mapping.get(m[1],m[1])+')',value)
    svg.attrs.pop('width',None);svg.attrs.pop('height',None)
    return str(svg)

def figure(key,prefix):
    title,description,refs,_=DIAGRAMS[key]
    return f'<figure class="diagram" data-diagram-key="{key}"><div class="diagram-viewport">{inline_svg(key,prefix)}</div><figcaption><strong>{esc(title)}.</strong> {esc(description)} <span class="diagram-scope">Logical model; arrows show documented relationships, not AWS internal deployment.</span></figcaption></figure>'

def render_markdown(text,definitions,links,prefix):
    soup=BeautifulSoup(MD.render(text+'\n\n'+definitions),'html.parser')
    for index,img in enumerate(list(soup.find_all('img'))):
        key=Path(img.get('src','')).stem
        if key in DIAGRAMS:
            fig=BeautifulSoup(figure(key,prefix+'-fig'+str(index)),'html.parser').figure
            parent=img.parent
            if parent.name=='p' and len(parent.find_all(recursive=False))==1:parent.replace_with(fig)
            else:img.replace_with(fig)
    for node in list(soup.find_all(string=True)):
        if node.find_parent(['a','pre','code','svg','script','style']):continue
        text=str(node);matches=list(re.finditer(r'\b'+SID+r'\b',text))
        if not matches:continue
        chunks=[];pos=0
        for m in matches:
            chunks.append(NavigableString(text[pos:m.start()]))
            if m[0] in links:
                a=soup.new_tag('a',href=links[m[0]]);a.string=m[0];chunks.append(a)
            else:chunks.append(NavigableString(m[0]))
            pos=m.end()
        chunks.append(NavigableString(text[pos:]))
        for piece in chunks:node.insert_before(piece)
        node.extract()
    for table in list(soup.find_all('table')):
        wrapper=soup.new_tag('div',attrs={'class':'table-wrap','tabindex':'0','role':'region','aria-label':'Scrollable reference table'});table.wrap(wrapper)
        for th in table.find_all('th'):th['scope']='col'
    return str(soup)

def links_for(guides,current=None):
    return {sid:(('#'+sid) if key==current else key+'.html#'+sid) for key,g in guides.items() for sid in g['sections']}

def frame(title,body,view,key='',total=0,depth=1):
    prefix='../' if depth else ''
    css=(SOURCE/'styles.css').read_text();css+=('\n@media print{@page{size:A4 landscape;margin:12mm}}' if view=='presentation' else '');js=(SOURCE/'interactions.js').read_text()
    nav=f'<a href="{prefix}index.html">Contents</a><a href="{prefix}catalog/index.html">Use cases</a><a href="{prefix}presentations/index.html">Presentations</a><a href="{prefix}guides/coverage.md">Sources and coverage</a>'
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><style>{css}</style></head><body class="{view}-page" data-view="{view}" data-key="{esc(key)}" data-total="{total}"><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="{prefix}index.html">AWS operational agents</a><nav aria-label="Collection">{nav}</nav></header>{body}<script>{js}</script></body></html>'

def options(values,label):return '<option value="">'+esc(label)+'</option>'+''.join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in sorted(values))

def catalog_sources(e,guides):return catalogue.sources(e,guides)
def catalog_controls(entries,platform=False):return catalogue.controls(entries,platform)
def catalog_entry(e,guides,embedded=False):return catalogue.entry(e,guides,embedded)
def catalog_content(catalog,guides,key=None):return catalogue.content(catalog,guides,key)

def report(key,g,guides,catalog):
    links=links_for(guides,key);deck=DECKS[key];minutes,exercise=totals(deck)
    toc=[];chapters=[];flat=ordered_ids(key)
    for number,c in enumerate(CHAPTERS[key],1):
        nav=[];content=[]
        for j,sid in enumerate(c['sections'],1):
            s=g['sections'][sid];n=f'{number}.{j}'
            nav.append(f'<li><a href="#{sid}" data-section="{sid}"><span>{n}</span> {esc(s["title"])}</a></li>')
            content.append(f'<section class="report-section" id="{sid}" data-kind="{section_type(sid)}" data-chapter="{c["slug"]}"><div class="section-meta">{n} · {sid} · {esc(LABELS[section_type(sid)])}</div><h3><a href="#{sid}">{esc(s["title"])}</a></h3>{render_markdown(s["body"],g["definitions"],links,key+"-"+sid)}</section>')
        toc.append(f'<details open><summary>{number:02d}. {esc(c["title"])}</summary><ol>{"".join(nav)}</ol></details>')
        chapters.append(f'<section class="chapter" id="chapter-{c["slug"]}" data-chapter="{c["slug"]}"><header class="chapter-heading"><span class="chapter-number">Chapter {number:02d}</span><h2>{esc(c["title"])}</h2><p>{esc(c["purpose"])}</p></header>{"".join(content)}</section>')
    intro=BeautifulSoup(render_markdown(g['intro'],g['definitions'],links,key+'-intro'),'html.parser')
    if intro.h1:intro.h1.decompose()
    chapter_options=''.join(f'<option value="{c["slug"]}">{i:02d}. {esc(c["title"])}</option>' for i,c in enumerate(CHAPTERS[key],1))
    kinds=dict.fromkeys(section_type(s) for s in flat)
    type_options=''.join(f'<option value="{t}">{esc(LABELS[t])}</option>' for t in kinds)
    catalog_panel=''
    if key in PLATFORMS:
        cases=[e for e in catalog['entries'] if catalogue.includes(e,key)]
        toc.append(f'<details open data-usecase-toc><summary>{len(CHAPTERS[key])+1:02d}. Operational use cases</summary><ol><li><a href="#use-case-catalog">Search and read {len(cases)} workflows</a></li></ol></details>')
        catalog_panel=f'<section id="use-case-catalog" class="embedded-catalog" data-usecase-catalog><header class="chapter-heading"><span class="chapter-number">Chapter {len(CHAPTERS[key])+1:02d}</span><h2>Operational use cases</h2><p>The preceding chapters explain configuration and mechanisms. These workflows apply them to recurring engineering tasks. Read the situation, execution, and interpretation before using the reference fields.</p></header>{catalog_content(catalog,guides,key)}</section>'
    body=f'''<div class="book-layout"><aside class="toc" aria-label="Table of contents"><p class="toc-title">{esc(deck['title'])}</p><div class="toc-actions"><button id="nav-expand">Expand</button><button id="nav-collapse">Collapse</button></div>{''.join(toc)}</aside><main id="main" class="book"><header class="book-title"><p class="eyebrow">Engineering guide</p><h1>{esc(deck['title'])}</h1>{intro}<div class="reading-links"><a href="../presentations/{key}.html">HTML presentation</a><a href="{key}.md">Markdown source</a><a href="../catalog/index.html{'?platform='+key if key in PLATFORMS else ''}">Use-case catalog</a></div></header><div class="filter-bar"><input id="search" type="search" aria-label="Search guide" placeholder="Search the technical chapters"><select id="chapter" aria-label="Chapter"><option value="">All chapters</option>{chapter_options}</select><select id="type" aria-label="Section type"><option value="">All section types</option>{type_options}</select><button id="reset">Reset</button><button data-print>Print</button></div><p id="search-status" class="result-count" aria-live="polite"></p><p id="empty-results" hidden>No technical sections match. The operational catalog has its own search below.</p>{''.join(chapters)}{catalog_panel}<footer>Logical diagrams and authored workflows are explanatory material. Source links support product behavior; no live AWS execution or measured improvement is claimed.</footer></main></div>'''
    write(f'guides/{key}.html',catalogue.decorate(frame(deck['title']+' — guide',body,'report',key)))

def table(rows):
    return '<div class="table-wrap" tabindex="0"><table><thead><tr>'+''.join('<th scope="col">'+esc(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in r)+'</tr>' for r in rows[1:])+'</tbody></table></div>'

def slide_body(s,prefix):
    if s['kind']=='diagram':return figure(s['diagram'],prefix)
    if s['kind'] in ('table','demo'):
        rows=s['data'] if s['kind']=='table' else [['Time','Action','Prepared evidence'],*s['data']]
        return table(rows)
    cls='flow' if s['kind']=='flow' else 'columns'
    return '<div class="'+cls+'">'+''.join('<section class="content-unit"><h2>'+esc(label)+'</h2><p>'+esc(text)+'</p></section>' for label,text in s['data'])+'</div>'

def presentation(key,g,guides):
    d=DECKS[key];total,exercise=totals(d);groups=DECK_CHAPTERS[key]
    assert [i for _,items in groups for i in items]==list(range(len(d['slides'])))
    group_by={i:(j,title) for j,(title,items) in enumerate(groups) for i in items}
    links={sid:f'../guides/{k}.html#{sid}' for k,v in guides.items() for sid in v['sections']}
    slides=[];notes=[];transcript=[f'# {d["title"]}: presentation notes','',f'Presentation: {total//60} minutes, including {exercise//60} minutes of prepared-result exercises. Questions and breaks are additional.','']
    elapsed=0
    for i,s in enumerate(d['slides']):
        start=elapsed;elapsed+=s['seconds'];gi,group=group_by[i];ident=f'slide-{i+1:02d}'
        refs=' · '.join(f'<a href="../guides/{key}.html#{sid}">{esc(g["sections"][sid]["title"])}</a>' for sid in s['refs'])
        slides.append(f'<article class="slide" id="{ident}" data-seconds="{s["seconds"]}" data-group="{gi}" data-kind="{s["kind"]}"><header class="slide-top"><span>{esc(d["title"])} · {gi+1:02d}. {esc(group)}</span><span>{i+1}/{len(d["slides"])} · {stamp(start)}–{stamp(elapsed)}</span></header><h1>{esc(s["title"])}</h1><div class="slide-body">{slide_body(s,key+"-slide"+str(i))}</div><p class="slide-explanation">{esc(s["message"])}</p><footer class="slide-foot">Guide: {refs}</footer></article>')
        note_parts=[f'<div class="talk-track"><p>{esc(s["message"])}</p><p>Allocated time: {stamp(s["seconds"])}. '+('Use the supplied synthetic evidence; do not imply live service execution.' if s['kind']=='demo' else 'Use the detailed section references below for configuration and limitations.')+'</p></div>']
        transcript.extend([f'## {i+1:02d}. {s["title"]}',f'{stamp(start)}–{stamp(elapsed)} · {group}',s['message'],''])
        if s['kind']=='diagram':transcript.append(f'![{DIAGRAMS[s["diagram"]][0]}](../assets/diagrams/{s["diagram"]}.svg)\n')
        else:
            for row in s['data']:transcript.append(' | '.join(str(x) for x in row))
        for sid in s['refs']:
            sec=g['sections'][sid]
            note_parts.append('<section class="note-reference"><h3>'+esc(sec['title'])+'</h3>'+render_markdown(sec['body'],g['definitions'],links,key+'-note'+str(i)+'-'+sid)+'</section>')
            transcript.append(f'\nDetailed reference: [{sec["title"]}](../guides/{key}.html#{sid})\n')
        notes.append(f'<section class="note-block" data-note="{i}"><h2>{esc(s["title"])}</h2>{"".join(note_parts)}</section>')
    select=''.join(f'<option value="{i}">{i+1:02d}. {esc(s["title"])}</option>' for i,s in enumerate(d['slides']))
    chapters=''.join(f'<button data-slide="{items[0]}" data-chapter-button="{j}"><span>{j+1:02d}</span> {esc(title)}</button>' for j,(title,items) in enumerate(groups))
    agenda=''.join('<section><h3>'+esc(title)+'</h3>'+''.join(f'<button data-slide="{i}">{i+1:02d}. {esc(d["slides"][i]["title"])} <small>{stamp(d["slides"][i]["seconds"])}</small></button>' for i in items)+'</section>' for title,items in groups)
    body=f'''<main id="main" class="deck-main"><div class="deck-toolbar"><button id="previous" aria-label="Previous slide">←</button><button id="next" aria-label="Next slide">→</button><select id="slide-select" aria-label="Slide">{select}</select><button id="agenda-open">Contents</button><button id="notes-button" aria-expanded="false">Notes</button><button id="fullscreen">Fullscreen</button><button data-print>Print slides</button></div><nav class="chapter-strip" aria-label="Presentation chapters">{chapters}</nav><div class="timer-bar"><button id="timer-toggle">Start timer</button><button id="timer-reset">Reset timer</button><span>Session <output id="session-time">00:00</output> / {stamp(total)}</span><span>Slide <output id="slide-time">00:00</output></span><span>{exercise//60} min exercise included</span></div>{''.join(slides)}<details id="speaker-notes" class="notes"><summary>Presenter notes and detailed references</summary>{''.join(notes)}</details><p class="deck-links"><a href="../guides/{key}.html">Read the guide</a> · <a href="../catalog/index.html{'?platform='+key if key in PLATFORMS else ''}">Read the use cases</a> · <a href="{key}-notes.md">Notes in Markdown</a></p><dialog id="agenda"><div class="dialog-heading"><h2>Presentation contents</h2><button id="agenda-close">Close</button></div>{agenda}</dialog></main>'''
    write(f'presentations/{key}.html',frame(d['title']+' — presentation',body,'presentation',key,total))
    write(f'presentations/{key}-notes.md','\n\n'.join(transcript))

def build_catalog(catalog,guides):
    catalogue.build_pages(catalog,guides,frame,write)

def indexes(catalog):
    rows=[]
    for key,d in DECKS.items():
        total,exercise=totals(d)
        rows.append(f'<tr><th scope="row">{esc(d["title"])}</th><td><a href="guides/{key}.html">Guide</a></td><td><a href="presentations/{key}.html">HTML presentation</a></td><td>{total//60} min, including {exercise//60} min exercise</td></tr>')
    programme=sum(totals(d)[0] for d in DECKS.values())//60;exercises=sum(totals(d)[1] for d in DECKS.values())//60
    body=f'<main id="main" class="index-main"><header class="book-title"><p class="eyebrow">Engineering reference</p><h1>AWS operational agents</h1><p>Read the service architecture, supported integrations, knowledge mechanisms, and operating workflows for three AWS services. The guides explain the platforms; the use-case catalog applies them to daily engineering work; the HTML presentations provide a timed teaching sequence.</p></header><h2>Guides and presentations</h2><div class="table-wrap"><table><thead><tr><th>Subject</th><th>Reference</th><th>Teaching edition</th><th>Delivery budget</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div><h2>Operational use cases</h2><p><a href="catalog/index.html">Browse the grouped and searchable catalog</a>. Its {len(catalog["entries"])} narratives explain situations, evidence-gathering work, and the resulting decisions. Reference fields and official sources are available alongside the prose.</p><h2>Implementation references</h2><p>Follow a workflow into its <a href="catalog/mechanisms.html">mechanisms</a>, inspect the <a href="catalog/features.html">features and affected outcomes</a>, and choose a <a href="catalog/profiles.html">configuration profile</a>. The <a href="catalog/migration.md">consolidation map</a> explains where every former record now belongs.</p><h2>Reading order</h2><p>Start with <a href="guides/architecture.html#A-00">Agents, tools, context, and executions</a>. Then select a product guide, follow its integration and knowledge chapters, and use the catalog to find the relevant workflow. All presentations are HTML; no server or external script library is required.</p><p>The full programme is {programme} minutes, including {exercises} minutes of prepared-result exercises. Questions and breaks are additional. These budgets do not promise live agent completion within the exercise time.</p><footer><a href="VALIDATION.md">Validation boundary</a> · <a href="guides/coverage.md">Coverage and source mapping</a> · <a href="applications/aws-validation-console/README.md">Separate readiness-console application</a></footer></main>'
    write('index.html',frame('AWS operational agents',body,'index',depth=0))
    presbody=body.replace('href="guides/','href="../guides/').replace('href="catalog/','href="../catalog/').replace('href="presentations/','href="').replace('href="VALIDATION.md','href="../VALIDATION.md').replace('href="applications/','href="../applications/')
    write('presentations/index.html',frame('HTML presentation collection',presbody,'index',depth=1))

def metadata(guides,catalog):
    total=sum(totals(d)[0] for d in DECKS.values())//60;exercise=sum(totals(d)[1] for d in DECKS.values())//60
    rows=['| Subject | Guide | HTML presentation | Duration |','|---|---|---|---|']
    for key,d in DECKS.items():
        t,e=totals(d);rows.append(f'| {d["title"]} | [HTML](guides/{key}.html) / [Markdown](guides/{key}.md) | [Slides](presentations/{key}.html) / [Notes](presentations/{key}-notes.md) | {t//60} min including {e//60} min exercise |')
    write('README.md','# AWS operational agents\n\nOpen `index.html` from a repository checkout. The guides, catalog, and presentations work locally; GitHub source preview does not execute HTML controls.\n\n'+'\n'.join(rows)+f'\n\nThe programme is **{total} minutes including {exercise} minutes of prepared-result exercises**. Questions and breaks are additional.\n\n## Operational use cases\n\n[Read and search the catalog](catalog/index.html). All {len(catalog["entries"])} workflows are narrated in prose and grouped by operational purpose. Workflow steps link to shared mechanisms, concrete feature configuration and implementation profiles. Browse the [mechanism index](catalog/mechanisms.html), [feature impact index](catalog/features.html), [profiles](catalog/profiles.html) and [consolidation map](catalog/migration.md).\n\n## Repository layout\n\n```text\nguides/          Maintained Markdown guides and generated HTML\ncatalog/         Canonical cases, mechanisms, features, profiles and alias data; generated reading indexes\npresentations/   Generated HTML decks and presenter notes\nassets/diagrams/ Generated, accessible SVG figures\nexamples/        Synthetic evidence used in worked examples\ntools/docs/      Rendering, diagrams, presentation outline, and checks\nqa/              Current validation and source-review records\napplications/    Independently maintained readiness-console application\n```\n\nEach guide introduces the agent and its resource model, describes supported integrations, explains knowledge production and retrieval, and then follows operational workflows. Stable identifiers connect use cases, mechanisms, diagrams, and presentation references. Superseded entry-point directories and generators are removed; Git retains history.\n\n## Build and validate\n\nInstall Graphviz (`dot`) and Python dependencies, then run:\n\n```sh\npython -m pip install -r tools/docs/requirements.txt\npython -m playwright install chromium\npython tools/docs/build.py\npython tools/docs/check.py --browser\n```\n\nSee [publishing](PUBLISHING.md), [editorial rules](EDITORIAL_STANDARD.md), [source coverage](guides/coverage.md), and [validation](VALIDATION.md). No live AWS operation is represented by the synthetic examples or document checks.\n')
    coverage=['# Guide and source coverage','The source map below identifies the references attached to each maintained section. It is not a claim that every upstream page was freshly audited. New integration and scheduling material and selected knowledge mechanisms were reviewed on 22 October 2026; retained sections keep their earlier references. See [the source-review record](../qa/source-review.json).']
    for key,g in guides.items():
        coverage+=['## '+DECKS[key]['title'],'| Section | Subject | Official references |','|---|---|---|']
        for sid in ordered_ids(key):
            s=g['sections'][sid];coverage.append(f'| [{sid}]({key}.html#{sid}) | {s["title"]} | '+', '.join(f'[{r}]({g["refs"][r]})' for r in s['sources'])+' |')
    coverage+=['## Diagram scope','Figures are logical models of documented resource relationships or explicitly labeled documentation dependencies, not descriptions of undisclosed infrastructure. Dashed cross-product handoffs are team-composed.','| Figure | Detailed guide |','|---|---|']
    for key,(title,description,refs,dot) in DIAGRAMS.items():coverage.append(f'| [{title}](../assets/diagrams/{key}.svg) | '+', '.join(refs)+' |')
    write('guides/coverage.md','\n'.join(coverage))
    write('PUBLISHING.md','# Publishing documentation\n\nEdit guide prose in `guides/*.md`, cases in `catalog/use-cases.json`, mechanism and feature relationships in `catalog/mechanisms.json` and `catalog/features.json`, and recipes in `catalog/profiles.json`, chapter membership in `tools/docs/structure.py`, slide content in `tools/docs/presentation.py`, and figures in `tools/docs/diagrams.py`.\n\nRun `python tools/docs/build.py` and `python tools/docs/check.py --browser`. Inspect rendered prose, diagrams, and slides as well as the recorded checks. Trigger the documentation workflow through `documentation-build.json`; generated documentation changes are committed separately on the checked-out branch. Promote a tested branch without overwriting intervening changes.\n\nDo not maintain compressed distributions, historical copies, old forwarding pages, or alternate renderers. Git is the revision history. Preserve `applications/` and its workflow. Repository publication is not website hosting.\n')

def commit():
    allowed={'guides','catalog','presentations','assets','examples','tools','qa','devops','security','finops','architecture','mechanisms','platforms'}
    roots={'README.md','CHANGELOG.md','MANIFEST.json','VALIDATION.md','PUBLISHING.md','EDITORIAL_STANDARD.md','SCOPE.md','index.html','documentation-build.json'}
    raw=subprocess.check_output(['git','-C',str(ROOT),'status','--porcelain=v1','-z','--untracked-files=all'])
    paths=[]
    for record in raw.split(b'\0'):
        if not record:continue
        status=record[:2].decode();path=record[3:].decode()
        if 'R' in status or 'C' in status:raise RuntimeError('Inspect staged rename before publishing')
        if path.split('/')[0] not in allowed and path not in roots:raise RuntimeError('Unexpected change: '+path)
        paths.append(path)
    for path in sorted(set(paths)):
        subprocess.run(['git','add','--',path],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m','docs: publish '+path],cwd=ROOT,check=True)

def build():
    build_diagrams();guides=load_guides();catalog=load_catalog()
    for key,g in guides.items():report(key,g,guides,catalog);presentation(key,g,guides)
    build_catalog(catalog,guides);indexes(catalog);metadata(guides,catalog)
    print(json.dumps({'guides':len(guides),'sections':sum(len(g['sections']) for g in guides.values()),'diagrams':len(DIAGRAMS),'use_cases':len(catalog['entries']),'slides':sum(len(d['slides']) for d in DECKS.values())},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--commit',action='store_true');a=p.parse_args()
    commit() if a.commit else build()
