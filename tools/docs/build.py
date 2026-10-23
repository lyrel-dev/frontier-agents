#!/usr/bin/env python3
"""Build the maintained narrative guides, use-case catalog, and HTML presentations.

Canonical prose lives in guides/*.md; catalog narratives live in JSON. This
renderer preserves authored capability explanations; frozen registries supply links, not chapter prose. Diagrams and presentations have their
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
import reader
import resource_model
import mechanism_detail

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
    return f'<figure class="diagram" data-diagram-key="{key}"><div class="diagram-viewport">{inline_svg(key,prefix)}</div><figcaption><strong>{esc(title)}.</strong> {esc(description)} <span class="diagram-scope">Logical model. Entity ownership and relationship qualifications are defined in the resource register.</span> <a href="../assets/diagrams/{key}.svg" target="_blank" rel="noopener">Open full-size SVG</a></figcaption></figure>'

def render_markdown(text,definitions,links,prefix):
    text=re.sub(r'^<!-- mechanism-review:(?:start|end) [^>]+ -->\s*$', '', text, flags=re.M)
    soup=BeautifulSoup(MD.render(text+'\n\n'+definitions),'html.parser')
    for heading in soup.find_all('h4'):
        match=re.match(r'(MX-[A-Z]-[A-Z]+)\s+[—-]\s+',heading.get_text())
        if match:heading['id']=(prefix+'-'+match[1]) if '-note' in prefix else match[1]
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



def metadata(guides,catalog):
    coverage=['# Guide and source coverage','The source map below identifies the references attached to each maintained section. It is not a claim that every upstream page was freshly audited. Product-specific resource identities and relationships retain the 22 October review. The capability exposition and targeted October 23 source checks are recorded in [exposition review](../qa/exposition-review.json); other retained sections keep their earlier references. See [the product-model source record](../qa/product-source-review.json) and [the earlier source-review record](../qa/source-review.json).']
    for key,g in guides.items():
        coverage+=['## '+DECKS[key]['title'],'| Section | Subject | Official references |','|---|---|---|']
        for sid in ordered_ids(key):
            s=g['sections'][sid];coverage.append(f'| [{sid}]({key}.html#{sid}) | {s["title"]} | '+', '.join(f'[{r}]({g["refs"][r]})' for r in s['sources'])+' |')
    coverage+=['## Diagram scope','Figures are logical models of documented resource relationships or explicitly labeled documentation dependencies, not descriptions of undisclosed infrastructure. Dashed cross-product handoffs are team-composed.','| Figure | Detailed guide |','|---|---|']
    for key,(title,description,refs,dot) in DIAGRAMS.items():coverage.append(f'| [{title}](../assets/diagrams/{key}.svg) | '+', '.join(refs)+' |')
    write('guides/coverage.md','\n'.join(coverage))

    write('PUBLISHING.md','# Publishing documentation\n\nThe six catalog JSON registers (use-cases, mechanisms, features, profiles, aliases, resource-models) are frozen at dace05a3ce6aaae02470a817584b8ca3a4cc95be. Do not change their definitions, identifiers, relationships, or use-case semantics during reader revisions.\n\nProduct capability explanations and official references are authored in guides/*.md. Frozen registers supply identifiers and relationships; they do not generate chapter prose or define a homogeneous product taxonomy. Chapter membership remains in tools/docs/structure.py; reader layout is in reader.py, reading.css, and reading.js; presentation content remains in presentation.py. Keep the supplied capability dimensions, detailed product explanations, and separate use-case catalog. Do not replace explanation with registry-field cards or add another parallel guide.\n\nRun python tools/docs/build.py and python tools/docs/check.py --browser. The reading checks compare frozen records byte-for-byte and test complete task-to-procedure reading journeys. Trigger the existing workflow through documentation-build.json and publish only after validation.\n\nGit retains previous versions. Do not create manual archives, migration copies, or forwarding editions. Preserve the independent application and its workflow. Repository publication does not deploy a website.\n')


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
    for key,g in guides.items():presentation(key,g,guides)
    metadata(guides,catalog)
    resource_model.resource_index(guides,frame,write,figure)
    reader.render(guides,render_markdown,write)
    print(json.dumps({'guides':len(guides),'sections':sum(len(g['sections']) for g in guides.values()),'diagrams':len(DIAGRAMS),'use_cases':len(catalog['entries']),'slides':sum(len(d['slides']) for d in DECKS.values())},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--commit',action='store_true');a=p.parse_args()
    commit() if a.commit else build()
