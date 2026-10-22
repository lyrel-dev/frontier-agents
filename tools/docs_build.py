#!/usr/bin/env python3
"""Generate grouped engineering reports and standalone HTML presentations."""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from markdown_it import MarkdownIt
from lesson_plan import DECKS
from docs_structure import CHAPTERS, DECK_CHAPTERS, LABELS, REVISION, section_type

ROOT = Path(__file__).resolve().parents[1]
MD = MarkdownIt('commonmark', {'html': False}).enable('table')
SID = r'[DSFA]-(?:M|U)?\d+'
SECTION = re.compile(r'^(#{2,3})\s+('+SID+r')\s+[—-]\s+(.+)$')
REF = re.compile(r'^\[([DSFA]S\d+)\]:\s+(https://\S+).*$', re.M)
CHAPTER_HEADING = re.compile(r'^## \d{2}\. ')
HISTORY_BOUNDARY = 'Product statements retain their existing official references. This revision changes organization and HTML delivery; it does not constitute a new product-documentation audit or live AWS test.'

def h(value): return html.escape(str(value), quote=True)
def write(rel, text):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
def stamp(seconds): return f'{int(seconds)//60:02d}:{int(seconds)%60:02d}'
def ordered_ids(key): return [sid for c in CHAPTERS[key] for sid in c['sections']]
def timeline(deck):
    elapsed = 0
    result = []
    for slide in deck['slides']:
        result.append((elapsed, elapsed + slide['seconds']))
        elapsed += slide['seconds']
    return result

def parse_source(raw):
    """Parse canonical sections at either heading depth; ignore fenced examples."""
    refs = dict(REF.findall(raw))
    definitions = '\n'.join(m.group(0) for m in REF.finditer(raw))
    content = REF.sub('', raw)
    lines = content.splitlines()
    starts = []
    fence = None
    for i,line in enumerate(lines):
        match = re.match(r'^\s*(`{3,}|~{3,})', line)
        if match:
            marker = match[1][0]
            if fence is None: fence = marker
            elif marker == fence: fence = None
            continue
        if fence: continue
        section = SECTION.match(line)
        if section: starts.append((i, section[2], section[3], len(section[1])))
        elif CHAPTER_HEADING.match(line): starts.append((i, None, None, 2))
    if not any(x[1] for x in starts): raise ValueError('No canonical sections found')
    intro_end = starts[0][0]
    sections = {}
    for j,(pos,sid,title,level) in enumerate(starts):
        if not sid: continue
        if sid in sections: raise ValueError('Duplicate canonical section '+sid)
        end = starts[j+1][0] if j+1<len(starts) else len(lines)
        body = '\n'.join(lines[pos+1:end]).strip()
        sections[sid] = {'id':sid, 'title':title, 'body':body, 'level':level}
    return {'intro':'\n'.join(lines[:intro_end]).strip(), 'sections':sections, 'refs':refs, 'definitions':definitions}

def normalize_body(body, level):
    out=[]; fence=None
    for line in body.splitlines():
        match=re.match(r'^\s*(`{3,}|~{3,})',line)
        if match:
            marker=match[1][0]
            if fence is None:fence=marker
            elif fence==marker:fence=None
        elif not fence and level==2 and re.match(r'^#{3,5} ',line): line='#'+line
        out.append(line)
    return '\n'.join(out)

def semantic_hash(section, definitions):
    rendered=MD.render(section['body']+'\n\n'+definitions)
    text=BeautifulSoup(rendered,'html.parser').get_text(' ',strip=True)
    return hashlib.sha256(re.sub(r'\s+',' ',text).encode()).hexdigest()

def load_guides():
    result={}
    for key in DECKS:
        g=parse_source((ROOT/f'guides/{key}.md').read_text(encoding='utf-8'))
        expected=ordered_ids(key)
        if set(g['sections'])!=set(expected) or len(expected)!=len(set(expected)):
            raise ValueError(f'{key}: section map does not match canonical content')
        for sid,sec in g['sections'].items():
            sec['body']=normalize_body(sec['body'],sec['level']);sec['level']=3
            sec['html']=MD.render(sec['body']+'\n\n'+g['definitions'])
            sec['sources']=sorted(set(re.findall(r'\b[DSFA]S\d+\b',sec['body'])) & set(g['refs']))
        result[key]=g
    return result

def group_markdown(key,g):
    parts=[g['intro']]
    for number,c in enumerate(CHAPTERS[key],1):
        parts.extend([f'## {number:02d}. {c["title"]}',c['purpose']])
        for sid in c['sections']:
            s=g['sections'][sid]
            parts.extend([f'### {sid} — {s["title"]}',s['body']])
    parts.append(g['definitions'])
    return '\n\n'.join(parts).strip()+'\n'

def decorate(markup, urls):
    soup=BeautifulSoup(markup,'html.parser')
    for node in list(soup.find_all(string=True)):
        if node.parent.name in {'a','code','pre','script','style'} or node.find_parent(['pre','code','a']):continue
        text=str(node);matches=list(re.finditer(r'\b'+SID+r'\b',text))
        if not matches:continue
        pieces=[];cursor=0
        for m in matches:
            pieces.append(NavigableString(text[cursor:m.start()]))
            if m[0] in urls:
                a=soup.new_tag('a',href=urls[m[0]]);a.string=m[0];pieces.append(a)
            else:pieces.append(NavigableString(m[0]))
            cursor=m.end()
        pieces.append(NavigableString(text[cursor:]))
        for p in pieces:node.insert_before(p)
        node.extract()
    for table in list(soup.find_all('table')):
        wrapper=soup.new_tag('div',attrs={'class':'table-wrap','tabindex':'0','role':'region','aria-label':'Scrollable reference table'})
        table.wrap(wrapper)
    for p in soup.find_all('p'):
        first=p.find('strong',recursive=False)
        if first and p.get_text().startswith(first.get_text()) and any(x in first.get_text().lower() for x in ('procedure','verification','proposed','original example')):p['class']='callout'
    return str(soup)

def frame(title,body,view,key='',total=0):
    css=(ROOT/'tools/docs_styles.css').read_text()
    js=(ROOT/'tools/docs_interactions.js').read_text()
    prefix='../' if view!='index' else ''
    nav=f'<a href="{prefix}index.html">Collection</a><a href="{prefix}presentations/index.html">HTML presentations</a><a href="{prefix}guides/coverage.md">Coverage</a>'
    print_css='@media print{@page{size:A4 landscape}}' if view=='presentation' else '@media print{@page{size:A4 portrait}}'
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{h(title)}</title><style>{css}\n{print_css}</style></head><body class="{view}-page" data-view="{view}" data-key="{h(key)}" data-total="{total}"><a href="#main" class="skip">Skip to content</a><header class="site-header"><div class="brand">AWS agent engineering guides</div><nav aria-label="Collection navigation">{nav}</nav></header>{body}<script>{js}</script></body></html>'''

def slide_body(s):
    if s['kind'] in ('table','demo'):
        rows=s['data'] if s['kind']=='table' else [['Time','Action','Prepared evidence'],*s['data']]
        return '<div class="table-wrap" tabindex="0" role="region" aria-label="Slide table"><table><thead><tr>'+''.join('<th scope="col">'+h(x)+'</th>' for x in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+h(x)+'</td>' for x in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>'
    klass='flow' if s['kind']=='flow' else 'columns';node='node' if klass=='flow' else 'column'
    return '<div class="'+klass+'">'+''.join('<div class="'+node+'"><strong>'+h(label)+'</strong><p>'+h(text)+'</p></div>' for label,text in s['data'])+'</div>'

def slide_map(key):
    mapping={}
    for i,s in enumerate(DECKS[key]['slides']):
        for ref in s['refs']:mapping.setdefault(ref,i)
    return mapping

def report(key,g,all_guides):
    d=DECKS[key];mapping=slide_map(key)
    urls={sid:(f'#{sid}' if k==key else f'{k}.html#{sid}') for k,v in all_guides.items() for sid in v['sections']}
    total=sum(s['seconds'] for s in d['slides'])//60;demo=sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')//60
    toc=[];cards=[];chapters=[];flat=ordered_ids(key)
    for number,c in enumerate(CHAPTERS[key],1):
        toc_items=[];sections=[]
        for j,sid in enumerate(c['sections'],1):
            s=g['sections'][sid];label=f'{number}.{j}';typ=section_type(sid)
            toc_items.append(f'<li><a href="#{sid}" data-section="{sid}">{label} {h(s["title"])}<small>{sid} · {h(LABELS[typ])}</small></a></li>')
            link=f'<a href="../presentations/{key}.html#slide-{mapping[sid]+1:02d}">Related slide {mapping[sid]+1} →</a>' if sid in mapping else ''
            pos=flat.index(sid)
            previous=f'<a href="#{flat[pos-1]}">← {h(g["sections"][flat[pos-1]]["title"])}</a>' if pos else '<span></span>'
            following=f'<a href="#{flat[pos+1]}">{h(g["sections"][flat[pos+1]]["title"])} →</a>' if pos+1<len(flat) else '<a href="#main">Back to overview ↑</a>'
            section=f'<section class="report-section" id="{sid}" data-kind="{typ}" data-chapter="{c["slug"]}" data-path="{h(c["title"]+" / "+s["title"])}"><div class="section-meta"><span>{label}</span><span>{h(LABELS[typ])}</span><code>{sid}</code>{link}</div><h3><a href="#{sid}">{h(s["title"])}</a></h3>{decorate(s["html"],urls)}<nav class="section-nav" aria-label="Adjacent sections">{previous}{following}</nav></section>'
            sections.append(section)
        toc.append(f'<details open><summary>{number:02d}. {h(c["title"])}</summary><ul>{"".join(toc_items)}</ul></details>')
        cards.append(f'<a class="map-link" href="#chapter-{c["slug"]}"><span class="ordinal">{number:02d} · {len(c["sections"])} sections</span><strong>{h(c["title"])}</strong><p>{h(c["purpose"])}</p></a>')
        chapters.append(f'<section class="chapter" id="chapter-{c["slug"]}" data-chapter="{c["slug"]}"><header class="chapter-heading"><span class="ordinal">CHAPTER {number:02d}</span><h2>{h(c["title"])}</h2><p>{h(c["purpose"])}</p></header>{"".join(sections)}</section>')
    intro_soup=BeautifulSoup(MD.render(g['intro']+'\n\n'+g['definitions']),'html.parser')
    if intro_soup.h1:intro_soup.h1.decompose()
    intro=decorate(str(intro_soup),urls)
    options=''.join(f'<option value="{c["slug"]}">{i:02d}. {h(c["title"])}</option>' for i,c in enumerate(CHAPTERS[key],1))
    types=''.join(f'<option value="{t}">{h(LABELS[t])}</option>' for t in dict.fromkeys(section_type(s) for s in flat))
    body=f'''<div class="report-shell"><aside class="toc" aria-label="Grouped table of contents"><div class="toc-label">{h(d['title'])}</div><a class="button-link" href="../presentations/{key}.html">Open HTML presentation</a><div class="toc-actions"><button id="nav-expand">Expand contents</button><button id="nav-collapse">Collapse contents</button></div>{''.join(toc)}</aside><main id="main" class="content"><div class="hero"><div class="eyebrow">Engineering report · structured edition</div><h1>{h(d['title'])}</h1><div class="intro">{intro}</div><div class="actions"><a class="button-link primary" href="../presentations/{key}.html">Open HTML presentation</a><a href="{key}.md">Markdown guide</a><a href="../presentations/{key}-notes.md">Presenter reference</a></div><div class="meta-row"><span>{len(CHAPTERS[key])} chapters</span><span>{len(flat)} canonical sections</span><span>Presentation: {total} min, including {demo} min exercise</span></div></div><h2 style="margin-top:30px">Report structure</h2><div class="chapter-map">{''.join(cards)}</div><div class="filter-bar"><input id="search" type="search" aria-label="Search guide" placeholder="Search sections · / to focus"><select id="chapter" aria-label="Chapter"><option value="">All chapters</option>{options}</select><select id="type" aria-label="Section type"><option value="">All section types</option>{types}</select><button id="reset">Reset</button><button data-print>Print report</button></div><p id="search-status" class="search-status" aria-live="polite"></p><p id="reading-location" class="reading-breadcrumb">Report overview</p><p id="empty-results" class="empty" hidden>No sections match. Clear the search or choose a different chapter or section type.</p>{''.join(chapters)}<footer>{h(HISTORY_BOUNDARY)}</footer></main></div>'''
    write(f'guides/{key}.html',frame(d['title']+' — engineering report',body,'report',key))

def presentation(key,g,all_guides):
    d=DECKS[key];times=timeline(d);groups=DECK_CHAPTERS[key]
    covered=[i for _,items in groups for i in items]
    if covered!=list(range(len(d['slides']))):raise ValueError('Invalid slide chapter ordering: '+key)
    group_by={i:(j,title) for j,(title,items) in enumerate(groups) for i in items}
    urls={sid:f'../guides/{k}.html#{sid}' for k,v in all_guides.items() for sid in v['sections']}
    sections=[];notes=[];transcript=[f'# {d["title"]} — HTML presentation reference', '', f'Open [{key}.html]({key}.html). The timing includes prepared-result exercises, not live service completion. Questions and breaks are additional.']
    for i,(s,(start,end)) in enumerate(zip(d['slides'],times)):
        group,title=group_by[i];id_=f'slide-{i+1:02d}'
        refs=''.join(f'<a href="../guides/{key}.html#{r}">{h(r)}</a>' for r in s['refs'])
        sections.append(f'<article class="slide" id="{id_}" data-seconds="{s["seconds"]}" data-kind="{s["kind"]}" data-group="{group}" data-chapter="{h(title)}" aria-label="Slide {i+1}"'+(' hidden' if i else '')+f'><div class="slide-top"><span>{h(d["title"])} · {group+1:02d} / {len(groups):02d} {h(title)}</span><span>{"Prepared-result exercise" if s["kind"]=="demo" else "Presentation"}</span></div><h1>{h(s["title"])}</h1><div class="slide-body">{slide_body(s)}</div><div class="takeaway">{h(s["message"])}</div><div class="slide-foot"><span>{i+1:02d} / {len(d["slides"]):02d} · {stamp(start)}–{stamp(end)} · {stamp(s["seconds"])} planned</span><span>Guide sections: {refs}</span></div></article>')
        refs_html=[];source_ids=[]
        for sid in s['refs']:
            sec=g['sections'][sid];source_ids.extend(sec['sources'])
            refs_html.append(f'<section class="note-reference"><h3><a href="../guides/{key}.html#{sid}">{sid} — {h(sec["title"])}</a></h3>{decorate(sec["html"],urls)}</section>')
        official=''.join(f'<li><a href="{h(g["refs"][r])}">{r} — {h(g["refs"][r].rsplit("/",1)[-1])}</a></li>' for r in sorted(set(source_ids)))
        notes.append(f'<div class="note-block"'+(' hidden' if i else '')+f'><h2>{i+1}. {h(s["title"])}</h2><p class="small">Budget {stamp(s["seconds"])} · cumulative {stamp(start)}–{stamp(end)}.</p><div class="talk-track"><strong>Speaking focus</strong><p>{h(s["message"])}</p><p class="small">Use the visual as the outline. The linked reference below is supporting detail, not a required verbatim script.</p></div>{"".join(refs_html)}<h3>Official documentation for this slide</h3><ul>{official or "<li>Synthetic or team-composed example; see the linked guide for its stated boundaries.</li>"}</ul></div>')
        transcript.extend(['',f'## {i+1}. {s["title"]}',f'**Chapter:** {title}. **Schedule:** {stamp(start)}–{stamp(end)}. **Slide budget:** {stamp(s["seconds"])}.',s['message'],'',*[' | '.join(row) for row in s['data']],'','**Guide:** '+', '.join(f'[{r}](../guides/{key}.html#{r})' for r in s['refs'])])
    strip=[];agenda=[]
    for j,(title,items) in enumerate(groups):
        budget=sum(d['slides'][i]['seconds'] for i in items)
        strip.append(f'<button data-start="{items[0]}" data-group="{j}" aria-current="false"><span>{j+1:02d} · {stamp(budget)}</span>{h(title)}</button>')
        buttons=''.join(f'<button data-slide="{i}">{i+1:02d}. {h(d["slides"][i]["title"])}<small>{stamp(times[i][0])}–{stamp(times[i][1])} · {stamp(d["slides"][i]["seconds"])} planned</small></button>' for i in items)
        agenda.append(f'<section class="agenda-group"><h3>{j+1:02d}. {h(title)} · {stamp(budget)}</h3>{buttons}</section>')
    total=times[-1][1];demo=sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')
    opts=''.join(f'<option value="{i}">{i+1:02d}. {h(s["title"])}</option>' for i,s in enumerate(d['slides']))
    sources=''.join(f'<li><a href="{h(url)}">{r} — {h(url.rsplit("/",1)[-1])}</a></li>' for r,url in g['refs'].items())
    body=f'''<main id="main" class="deck-main"><div class="deck-toolbar"><a class="button-link" href="../guides/{key}.html">Read structured report</a><button id="agenda-open">Agenda</button><button id="previous">Previous</button><select id="slide-select" aria-label="Select slide">{opts}</select><button id="next">Next</button><button id="notes-button">Speaker notes</button><button id="fullscreen">Fullscreen</button><button data-print>Print slides</button></div><nav class="chapter-strip" aria-label="Presentation chapters">{''.join(strip)}</nav><div class="deck-toolbar"><button id="timer-toggle" aria-pressed="false">Start timer</button><button id="timer-reset">Reset timer</button><span class="timer" id="session-clock">Session <b id="session-time">00:00 / {stamp(total)}</b></span><span class="timer" id="slide-clock">Slide <b id="slide-time">00:00</b></span><span class="small">{total//60} min including {demo//60} min prepared-result exercise</span></div>{''.join(sections)}<div class="deck-status"><span id="slide-position"></span><progress id="slide-progress" max="{len(d['slides'])}" value="1" aria-label="Slide progress"></progress><span>← → navigate · N notes · T timer · F fullscreen</span></div><span id="slide-announcement" aria-live="polite" style="position:absolute;left:-10000px;width:1px;height:1px;overflow:hidden"></span><details id="speaker-notes" class="notes"><summary>Speaker notes and canonical reference</summary>{''.join(notes)}</details><details class="evidence"><summary>Official source register · untimed reference</summary><p class="small">{h(HISTORY_BOUNDARY)}</p><ol>{sources}</ol></details><footer>No live service completion or measured outcome is implied by the walkthrough budgets. <a href="{key}-notes.md">Presenter reference</a>.</footer></main><dialog id="agenda" aria-labelledby="agenda-title"><div class="dialog-top"><h2 id="agenda-title">{h(d['title'])} — agenda</h2><button id="agenda-close">Close</button></div><p>{total//60} minutes including {demo//60} minutes of prepared-result exercise. Select a slide or use the chapter buttons.</p>{''.join(agenda)}</dialog>'''
    write(f'presentations/{key}.html',frame(d['title']+' — HTML presentation',body,'presentation',key,total))
    write(f'presentations/{key}-notes.md','\n\n'.join(transcript)+'\n')

def indexes():
    total=sum(s['seconds'] for d in DECKS.values() for s in d['slides'])//60
    demo=sum(s['seconds'] for d in DECKS.values() for s in d['slides'] if s['kind']=='demo')//60
    for presentation_index in (False,True):
        prefix='../' if presentation_index else '';cards=[]
        for k,d in DECKS.items():
            minutes=sum(s['seconds'] for s in d['slides'])//60;exercise=sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')//60
            deck_url=f'{k}.html' if presentation_index else f'presentations/{k}.html'
            purpose=' · '.join(c['title'] for c in CHAPTERS[k][:3])
            cards.append(f'<section class="index-card"><div class="eyebrow">{len(CHAPTERS[k])} report chapters · {len(d["slides"])} slides</div><h2>{h(d["title"])}</h2><p>{h(d["subtitle"])}</p><p class="small">{h(purpose)}; operations, worked examples and evidence.</p><p><strong>{minutes} minutes</strong>, including {exercise} minutes of prepared-result exercise.</p><div class="actions"><a class="button-link primary" href="{deck_url}">Open HTML presentation</a><a href="{prefix}guides/{k}.html">Read structured report</a></div></section>')
        title='HTML presentations' if presentation_index else 'Structured reports and HTML presentations'
        body=f'<main id="main" class="index-main"><div class="eyebrow">Three AWS agents · one shared comparison</div><h1>{title}</h1><p class="intro">Read the grouped report for configuration and mechanism detail. Use the separate HTML presentation for chapter-based delivery, timed exercises, speaker notes and source links. Both views use the same canonical guide sections.</p><div class="programme"><strong>{total}-minute programme</strong>, including {demo} minutes of prepared-result exercises. Questions and breaks are additional. Each deck opens directly in presentation mode.</div><div class="index-grid">{"".join(cards)}</div><footer>Open these files locally or on a static website. No server, remote JavaScript or presentation application is required. {h(HISTORY_BOUNDARY)}</footer></main>'
        out=frame(title,body,'index')
        if presentation_index:
            out=out.replace('href="index.html">Collection','href="../index.html">Collection').replace('href="presentations/index.html">HTML presentations','href="index.html">HTML presentations').replace('href="guides/coverage.md">Coverage','href="../guides/coverage.md">Coverage')
        write('presentations/index.html' if presentation_index else 'index.html',out)

def metadata(guides):
    rows=[]
    for k,d in DECKS.items():
        minutes=sum(s['seconds'] for s in d['slides'])//60;exercise=sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')//60
        rows.append(f'| {d["title"]} | [Report](guides/{k}.html) / [Markdown](guides/{k}.md) | [HTML presentation](presentations/{k}.html) / [Notes](presentations/{k}-notes.md) | {minutes} min / {exercise} min exercise |')
    write('README.md','# AWS agent engineering guides\n\nOpen `index.html` after cloning the repository. Reports and presentations are separate, self-contained HTML pages; GitHub source previews do not execute their controls.\n\n| Subject | Structured report | Presentation | Timing |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n\nThe programme remains **124 minutes including 28 minutes of prepared-result exercises**. Questions and breaks are additional.\n\n## Reading and presentation structure\n\nReports have numbered chapters, a nested table of contents, a chapter map, chapter/type filters, stable section links and links to the relevant slides. Chapter groups distinguish platform overview and capabilities, access and integrations, mechanisms, operations, worked examples, troubleshooting, and evidence. The shared architecture guide uses corresponding comparison groups.\n\nStandalone HTML decks include chapter navigation, an agenda, slide selection, keyboard controls, fullscreen, speaker notes, session and slide timers, source links and slide-only printing. They open directly as presentations.\n\n## Maintained sources\n\n- `guides/*.md`: canonical descriptive content, with explicit chapter and section headings.\n- `tools/docs_structure.py`: chapter membership and presentation chapter boundaries.\n- `tools/lesson_plan.py`: curated slide content and delivery budgets.\n- `tools/docs_build.py`: HTML generation; no binary presentation output.\n\nNo competing capability catalog or historical copy is retained. Prior editions are available through Git. The [readiness-console application](applications/aws-validation-console/README.md) and its workflow are outside the documentation build.\n\n## Build and check\n\n```sh\npython -m pip install -r tools/docs-requirements.txt\npython -m playwright install chromium\npython tools/docs_build.py\npython tools/docs_check.py --browser\n```\n\nSee [coverage](guides/coverage.md), [validation](VALIDATION.md), [editorial rules](EDITORIAL_STANDARD.md) and [publishing](PUBLISHING.md). This organization-only revision retains existing product references; no new AWS source audit or live execution is claimed.\n')
    coverage=['# Coverage and claim-to-source map','','Canonical sections retain their existing references and review boundaries. The chapter structure below is editorial navigation, not a new product classification or external audit.']
    for k,g in guides.items():
        coverage.append('\n## '+DECKS[k]['title'])
        for i,c in enumerate(CHAPTERS[k],1):
            coverage.extend([f'\n### {i:02d}. {c["title"]}','| Section | Subject | Type | Source identifiers |','|---|---|---|---|'])
            for sid in c['sections']:
                s=g['sections'][sid];coverage.append(f'| [{sid}]({k}.html#{sid}) | {s["title"]} | {LABELS[section_type(sid)]} | '+', '.join(s['sources'])+' |')
    write('guides/coverage.md','\n'.join(coverage)+'\n')
    write('PUBLISHING.md','# Publishing documentation\n\nEdit the canonical guide, chapter map or lesson plan, rebuild, then run `python tools/docs_check.py --browser`. Review the generated HTML before committing. The documentation workflow is triggered by `documentation-build.json`; it validates before committing each changed documentation file separately.\n\nThe report and presentation are both HTML. No compressed distributions or retained historical document copies are produced. Git holds prior revisions. The separate application and its workflow must remain unchanged. Repository publication is not website hosting.\n')
    write('CHANGELOG.md','# Documentation changes\n\n## 22 October 2026 — structured HTML edition\n\nRestored explicit chapters and nested section navigation in every report. Added standalone HTML presentations with chapter agendas, source-linked notes, session/slide timers and printing. Removed generated binary decks and their build dependencies. Preserved all canonical section bodies and the existing 124-minute schedule. Git retains earlier versions; no manual archives are produced.\n')

def build():
    guides=load_guides()
    for key,g in guides.items():write(f'guides/{key}.md',group_markdown(key,g))
    for key,g in guides.items():report(key,g,guides);presentation(key,g,guides)
    for path in (ROOT/'presentations').glob('*.pptx'):path.unlink()
    indexes();metadata(guides)
    print(json.dumps({'revision':REVISION,'reports':len(guides),'sections':sum(len(g['sections']) for g in guides.values()),'html_presentations':len(DECKS),'slides':sum(len(d['slides']) for d in DECKS.values())},indent=2))

def commit():
    allowed={'tools','guides','presentations','qa','examples','devops','security','finops','architecture','mechanisms','platforms'}
    root_files={'README.md','CHANGELOG.md','MANIFEST.json','VALIDATION.md','PUBLISHING.md','EDITORIAL_STANDARD.md','SCOPE.md','index.html','documentation-build.json'}
    raw=subprocess.check_output(['git','status','--porcelain=v1','-z','--untracked-files=all'],cwd=ROOT)
    paths=[]
    for record in raw.split(b'\0'):
        if not record:continue
        status=record[:2].decode();path=record[3:].decode()
        if 'R' in status or 'C' in status:raise RuntimeError('Inspect rename before publishing')
        if path.split('/')[0] not in allowed and path not in root_files:raise RuntimeError('Unexpected change outside documentation: '+path)
        paths.append(path)
    for path in sorted(set(paths)):
        subprocess.run(['git','add','--',path],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m','docs: publish '+path],cwd=ROOT,check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--commit',action='store_true');args=p.parse_args()
    commit() if args.commit else build()
