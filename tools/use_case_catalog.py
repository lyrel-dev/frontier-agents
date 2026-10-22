#!/usr/bin/env python3
"""Build and validate the grouped, searchable use-case catalog.

The catalog is a separate structured data set. It is injected into each HTML
report and linked from each standalone HTML presentation. It does not redefine
platform capabilities or mechanisms.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit

from bs4 import BeautifulSoup

from docs_build import ROOT, load_guides
from lesson_plan import DECKS

CATALOG = ROOT / 'catalog' / 'use-cases.json'
PLATFORMS = {
    'devops': 'AWS DevOps Agent',
    'security': 'AWS Security Agent',
    'finops': 'AWS FinOps Agent',
}
PLATFORM_ORDER = ('devops', 'security', 'finops')
BANNED_TITLE = re.compile(
    r'(?i)\b(revolutionary|transformative|game[- ]changing|seamless|effortless|'
    r'best[- ]in[- ]class|cutting[- ]edge|next[- ]generation|unlock|supercharge|'
    r'accelerate|smarter|powerful|future[- ]proof)\b'
)
REQUIRED = {
    'id', 'platform', 'group', 'title', 'summary', 'delivery', 'cadence',
    'availability', 'inputs', 'output', 'sections', 'constraints', 'example',
    'keywords',
}

CATALOG_CSS = r'''
.catalog-page .catalog-main{max-width:1500px;margin:auto;padding:28px}.catalog-hero{background:white;border:1px solid var(--line);border-top:5px solid var(--accent);padding:30px;border-radius:7px}.catalog-hero p{max-width:82ch}.catalog-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:22px 0}.catalog-summary div{background:var(--pale);padding:17px;border-top:3px solid var(--accent)}.catalog-summary strong{display:block;font-size:26px}.catalog-controls,.embedded-catalog-controls{display:flex;gap:9px;flex-wrap:wrap;position:sticky;top:0;z-index:5;background:var(--bg);padding:14px 0}.catalog-controls input,.embedded-catalog-controls input{flex:2;min-width:200px}.catalog-controls select,.embedded-catalog-controls select{flex:1;min-width:145px}.catalog-group{margin:28px 0}.catalog-group>h2,.embedded-usecase-group>h3{border-bottom:2px solid var(--ink);padding-bottom:10px}.catalog-grid,.embedded-usecase-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.usecase-card{background:white;border:1px solid var(--line);border-left:5px solid var(--accent);border-radius:6px;padding:20px;min-width:0}.usecase-card h3,.usecase-card h4{margin:6px 0 11px}.usecase-card h3{font-size:21px}.usecase-card h4{font-size:18px}.usecase-card p{font-size:14px}.usecase-meta{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0 13px}.chip{display:inline-block;border:1px solid var(--line);background:#f7fafb;border-radius:999px;padding:3px 8px;font-size:11px;color:var(--muted)}.usecase-card details{border-top:1px solid var(--line);padding-top:10px;margin-top:12px}.usecase-card summary{cursor:pointer;font-weight:700;font-size:13px}.usecase-fields{display:grid;grid-template-columns:1fr 1fr;gap:12px 18px;margin-top:12px}.usecase-field strong{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin-bottom:3px}.usecase-source{font-size:12px;overflow-wrap:anywhere}.usecase-source a{display:block;margin:5px 0}.catalog-count{font-size:13px;color:var(--muted);min-height:24px}.catalog-empty{padding:22px;background:white;border:1px dashed var(--line)}.embedded-usecase-catalog{margin:28px 0 35px;padding:26px;background:white;border:1px solid var(--line);border-top:5px solid var(--accent);border-radius:7px}.embedded-usecase-catalog>header{display:flex;justify-content:space-between;gap:18px;align-items:flex-start;flex-wrap:wrap}.embedded-usecase-catalog>header p{max-width:72ch}.embedded-usecase-group{margin-top:24px}.catalog-link-row{display:flex;gap:12px;flex-wrap:wrap;align-items:center}.catalog-page footer{max-width:1500px;margin:30px auto;padding:0 28px 35px;color:var(--muted);font-size:13px}
@media(max-width:900px){.catalog-summary{grid-template-columns:1fr 1fr}.catalog-grid,.embedded-usecase-grid{grid-template-columns:1fr}.usecase-fields{grid-template-columns:1fr}.catalog-page .catalog-main{padding:16px}.catalog-controls,.embedded-catalog-controls{position:static}.catalog-controls>* ,.embedded-catalog-controls>*{width:100%;min-width:0!important}.embedded-usecase-catalog{padding:20px}}
@media print{.catalog-controls,.embedded-catalog-controls,.catalog-link-row{display:none!important}.catalog-grid,.embedded-usecase-grid{display:block}.usecase-card{break-inside:avoid;margin:10px 0}.usecase-card details{display:block}.usecase-card details>*{display:block}.catalog-page .catalog-main{padding:0}.catalog-hero{border:0;padding:0}.catalog-summary{grid-template-columns:repeat(4,1fr)}}
'''

CATALOG_JS = r'''
(()=>{
  function setup(root){
    const cards=[...root.querySelectorAll('.usecase-card')];
    const search=root.querySelector('[data-uc-search]');
    const platform=root.querySelector('[data-uc-platform]');
    const group=root.querySelector('[data-uc-group]');
    const delivery=root.querySelector('[data-uc-delivery]');
    const cadence=root.querySelector('[data-uc-cadence]');
    const availability=root.querySelector('[data-uc-availability]');
    const count=root.querySelector('[data-uc-count]');
    const empty=root.querySelector('[data-uc-empty]');
    function run(){
      const q=(search?.value||'').trim().toLowerCase();let shown=0;
      cards.forEach(card=>{
        const ok=(!q||card.textContent.toLowerCase().includes(q))&&
          (!platform?.value||card.dataset.platform===platform.value)&&
          (!group?.value||card.dataset.group===group.value)&&
          (!delivery?.value||card.dataset.delivery===delivery.value)&&
          (!cadence?.value||card.dataset.cadence===cadence.value)&&
          (!availability?.value||card.dataset.availability===availability.value);
        card.hidden=!ok;if(ok)shown++;
      });
      root.querySelectorAll('[data-uc-group-block]').forEach(block=>{
        block.hidden=!block.querySelector('.usecase-card:not([hidden])');
      });
      if(count)count.textContent=shown+' of '+cards.length+' use cases shown';
      if(empty)empty.hidden=shown!==0;
    }
    [search,platform,group,delivery,cadence,availability].filter(Boolean).forEach(x=>x.addEventListener('input',run));
    const reset=root.querySelector('[data-uc-reset]');
    if(reset)reset.addEventListener('click',()=>{[search,platform,group,delivery,cadence,availability].filter(Boolean).forEach(x=>x.value='');run();});
    const params=new URLSearchParams(location.search);
    if(platform&&params.get('platform'))platform.value=params.get('platform');
    if(group&&params.get('group'))group.value=params.get('group');
    run();
  }
  document.querySelectorAll('[data-usecase-catalog]').forEach(setup);
})();
'''


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding='utf-8'))


def source_map(entry: dict, guides: dict) -> list[tuple[str, str]]:
    guide = guides[entry['platform']]
    ids: list[str] = []
    for section_id in entry['sections']:
        ids.extend(guide['sections'][section_id]['sources'])
    seen = set()
    result = []
    for source_id in ids:
        if source_id in seen:
            continue
        seen.add(source_id)
        result.append((source_id, guide['refs'][source_id]))
    return result


def select_options(values, label: str) -> str:
    return '<option value="">All '+esc(label)+'</option>'+''.join(
        '<option value="'+esc(v)+'">'+esc(v)+'</option>' for v in sorted(values)
    )


def controls(entries: list[dict], include_platform: bool, embedded: bool) -> str:
    cls = 'embedded-catalog-controls' if embedded else 'catalog-controls'
    platform = ''
    if include_platform:
        platform = '<select data-uc-platform aria-label="Platform">'+select_options(
            {e['platform'] for e in entries}, 'platforms'
        ).replace('>devops<','>AWS DevOps Agent<').replace('>security<','>AWS Security Agent<').replace('>finops<','>AWS FinOps Agent<')+'</select>'
    return (
        f'<div class="{cls}">'
        '<input data-uc-search type="search" aria-label="Search use cases" placeholder="Search use cases, inputs, outputs and constraints">'
        + platform
        + '<select data-uc-group aria-label="Use case group">'+select_options({e['group'] for e in entries}, 'groups')+'</select>'
        + '<select data-uc-delivery aria-label="Delivery mode">'+select_options({e['delivery'] for e in entries}, 'delivery modes')+'</select>'
        + '<select data-uc-cadence aria-label="Cadence">'+select_options({e['cadence'] for e in entries}, 'cadences')+'</select>'
        + '<select data-uc-availability aria-label="Availability">'+select_options({e['availability'] for e in entries}, 'availability states')+'</select>'
        + '<button data-uc-reset>Reset</button></div>'
        + '<p class="catalog-count" data-uc-count aria-live="polite"></p>'
        + '<p class="catalog-empty" data-uc-empty hidden>No use cases match the current filters.</p>'
    )


def card(entry: dict, guides: dict, report: bool = False) -> str:
    refs = source_map(entry, guides)
    section_links = ''.join(
        f'<a href="{("#" if report else "../guides/"+entry["platform"]+".html#")}{esc(sid)}">{esc(sid)}</a> '
        for sid in entry['sections']
    )
    source_links = ''.join(
        f'<a href="{esc(url)}">{esc(source_id)} · Official AWS documentation</a>'
        for source_id, url in refs
    ) or '<span>No official source identifier is attached to this team-composed example.</span>'
    return f'''<article class="usecase-card" id="{esc(entry['id'])}" data-platform="{esc(entry['platform'])}" data-group="{esc(entry['group'])}" data-delivery="{esc(entry['delivery'])}" data-cadence="{esc(entry['cadence'])}" data-availability="{esc(entry['availability'])}">
<div class="eyebrow">{esc(entry['id'])} · {esc(entry['group'])}</div><h4>{esc(entry['title'])}</h4><p>{esc(entry['summary'])}</p>
<div class="usecase-meta"><span class="chip">{esc(entry['delivery'])}</span><span class="chip">{esc(entry['cadence'])}</span><span class="chip">{esc(entry['availability'])}</span></div>
<details><summary>Inputs, output, controls and references</summary><div class="usecase-fields">
<div class="usecase-field"><strong>Inputs and prerequisites</strong><span>{esc(entry['inputs'])}</span></div>
<div class="usecase-field"><strong>Reviewable output</strong><span>{esc(entry['output'])}</span></div>
<div class="usecase-field"><strong>Constraint</strong><span>{esc(entry['constraints'])}</span></div>
<div class="usecase-field"><strong>Example request</strong><span>{esc(entry['example'])}</span></div>
<div class="usecase-field"><strong>Canonical guide sections</strong><span>{section_links}</span></div>
<div class="usecase-field usecase-source"><strong>Official sources</strong>{source_links}</div>
</div></details></article>'''


def grouped_cards(entries: list[dict], guides: dict, report: bool = False) -> str:
    groups = defaultdict(list)
    for entry in entries:
        groups[(entry['platform'], entry['group'])].append(entry)
    parts = []
    for platform in PLATFORM_ORDER:
        for (p, group), items in groups.items():
            if p != platform:
                continue
            title = group if report else f'{PLATFORMS[platform]} · {group}'
            anchor = re.sub(r'[^a-z0-9]+', '-', (platform+'-'+group).lower()).strip('-')
            parts.append(
                f'<section class="{"embedded-usecase-group" if report else "catalog-group"}" id="usecase-{anchor}" data-uc-group-block>'
                f'<h3>{esc(title)}</h3><div class="{"embedded-usecase-grid" if report else "catalog-grid"}">'
                + ''.join(card(e, guides, report) for e in items)
                + '</div></section>'
            )
    return ''.join(parts)


def catalog_page(catalog: dict, guides: dict) -> str:
    entries = catalog['entries']
    counts = Counter(e['platform'] for e in entries)
    base_css = (ROOT/'tools/docs_styles.css').read_text(encoding='utf-8')
    summary = ''.join(
        f'<div><strong>{counts[p]}</strong><span>{esc(PLATFORMS[p])} use cases</span></div>'
        for p in PLATFORM_ORDER
    ) + f'<div><strong>{len({e["group"] for e in entries})}</strong><span>catalog groups</span></div>'
    body = f'''<a href="#main" class="skip">Skip to content</a><header class="site-header"><div class="brand">AWS agent engineering guides</div><nav><a href="../index.html">Collection</a><a href="../presentations/index.html">HTML presentations</a><a href="../guides/coverage.md">Coverage</a></nav></header><main id="main" class="catalog-main" data-usecase-catalog><section class="catalog-hero"><div class="eyebrow">Structured reference · {esc(catalog['revision'])}</div><h1>Day-to-Day Use Case Catalog</h1><p>{esc(catalog['description'])}</p><p>The catalog classifies each item as a built-in function, configured workflow, controlled action or team-composed procedure. Those labels prevent operational scenarios from being presented as platform capabilities.</p><div class="catalog-summary">{summary}</div></section>{controls(entries,True,False)}{grouped_cards(entries,guides,False)}</main><footer>Product claims are linked to the official sources attached to the canonical guide sections. Example requests and team-composed procedures were not executed.</footer>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Day-to-Day Use Case Catalog</title><style>{base_css}\n{CATALOG_CSS}</style></head><body class="catalog-page">{body}<script>{CATALOG_JS}</script></body></html>'''


def markdown_page(catalog: dict, guides: dict) -> str:
    lines = ['# Day-to-Day Use Case Catalog', '', catalog['description'], '',
             'Delivery mode distinguishes native functions, configured workflows, controlled actions and team-composed procedures.', '']
    for platform in PLATFORM_ORDER:
        lines += ['## '+PLATFORMS[platform], '']
        groups = defaultdict(list)
        for entry in catalog['entries']:
            if entry['platform'] == platform:
                groups[entry['group']].append(entry)
        for group, items in groups.items():
            lines += ['### '+group, '']
            for entry in items:
                lines += [f'#### {entry["id"]} — {entry["title"]}', '', entry['summary'], '',
                          f'**Delivery:** {entry["delivery"]}. **Cadence:** {entry["cadence"]}. **Availability:** {entry["availability"]}.', '',
                          f'**Inputs and prerequisites:** {entry["inputs"]}', '',
                          f'**Reviewable output:** {entry["output"]}', '',
                          f'**Constraint:** {entry["constraints"]}', '',
                          f'**Example request:** {entry["example"]}', '',
                          '**Canonical sections:** '+', '.join(f'[{s}](../guides/{platform}.html#{s})' for s in entry['sections']), '',
                          '**Official sources:** '+', '.join(f'[{sid}]({url})' for sid,url in source_map(entry,guides)), '']
    return '\n'.join(lines).rstrip()+'\n'


def append_style_and_script(soup: BeautifulSoup) -> None:
    style = soup.find('style')
    if style and 'embedded-usecase-catalog' not in style.get_text():
        style.append('\n'+CATALOG_CSS)
    if not soup.find('script', attrs={'data-usecase-script': 'true'}):
        script = soup.new_tag('script')
        script['data-usecase-script'] = 'true'
        script.string = CATALOG_JS
        soup.body.append(script)


def inject_report(key: str, entries: list[dict], guides: dict) -> None:
    path = ROOT/f'guides/{key}.html'
    soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
    old = soup.find(id='use-case-catalog')
    if old:
        old.decompose()
    for old_nav in soup.select('[data-usecase-toc]'):
        old_nav.decompose()
    append_style_and_script(soup)
    nav = soup.select_one('.site-header nav')
    if nav and not nav.find('a', href='../catalog/index.html'):
        a=soup.new_tag('a',href=f'../catalog/index.html?platform={key}');a.string='Use cases';nav.append(a)
    actions = soup.select_one('.hero .actions')
    if actions and not actions.find('a', href=re.compile(r'catalog/index\.html')):
        a=soup.new_tag('a',href=f'../catalog/index.html?platform={key}');a.string='Full use case catalog';actions.append(a)
    chapter_map = soup.select_one('.chapter-map')
    if chapter_map:
        link = BeautifulSoup(
            f'<a class="map-link" href="#use-case-catalog"><span class="ordinal">CATALOG · {len(entries)} use cases</span><strong>Day-to-Day Use Case Catalog</strong><p>Grouped native functions, configured workflows, controlled actions and team-composed procedures.</p></a>',
            'html.parser'
        ).a
        chapter_map.insert(0, link)
    toc = soup.select_one('.toc')
    if toc:
        groups=[]
        for entry in entries:
            if entry['group'] not in groups: groups.append(entry['group'])
        links=''.join(f'<li><a href="#usecase-{re.sub(r"[^a-z0-9]+","-",(key+"-"+g).lower()).strip("-")}">{esc(g)}</a></li>' for g in groups)
        block=BeautifulSoup(f'<details data-usecase-toc open><summary>Use Case Catalog</summary><ul><li><a href="#use-case-catalog">Catalog controls and overview</a></li>{links}</ul></details>','html.parser').details
        label=toc.select_one('.toc-label')
        if label: label.insert_after(block)
        else: toc.insert(0,block)
    panel = BeautifulSoup(
        f'''<section class="embedded-usecase-catalog" id="use-case-catalog" data-usecase-catalog><header><div><div class="eyebrow">Structured use case catalog</div><h2>Day-to-Day Use Cases</h2><p>Use cases are applications of platform functions and mechanisms. Delivery mode identifies whether the work is built in, configured, controlled or composed by the team.</p></div><div class="catalog-link-row"><a class="button-link" href="../catalog/index.html?platform={key}">Open full catalog</a></div></header>{controls(entries,False,True)}{grouped_cards(entries,guides,True)}</section>''',
        'html.parser'
    ).section
    chapter_map = soup.select_one('.chapter-map')
    if chapter_map: chapter_map.insert_after(panel)
    else:
        hero=soup.select_one('.hero')
        if hero: hero.insert_after(panel)
    path.write_text(str(soup),encoding='utf-8')


def inject_presentation(key: str) -> None:
    path=ROOT/f'presentations/{key}.html'
    soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
    nav=soup.select_one('.site-header nav')
    if nav and not nav.find('a',href=re.compile(r'catalog/index\.html')):
        a=soup.new_tag('a',href=f'../catalog/index.html?platform={key}');a.string='Use cases';nav.append(a)
    toolbar=soup.select_one('.deck-toolbar')
    if toolbar and not toolbar.find('a',href=re.compile(r'catalog/index\.html')):
        a=soup.new_tag('a',href=f'../catalog/index.html?platform={key}');a['class']='button-link';a.string='Use case catalog';toolbar.insert(0,a)
    path.write_text(str(soup),encoding='utf-8')


def replace_marker(text: str, start: str, end: str, block: str) -> str:
    pattern=re.compile(re.escape(start)+r'.*?'+re.escape(end),re.S)
    wrapped=start+'\n'+block.rstrip()+'\n'+end
    if pattern.search(text): return pattern.sub(wrapped,text)
    return wrapped+'\n\n'+text


def update_collection_files(catalog: dict) -> None:
    counts=Counter(e['platform'] for e in catalog['entries'])
    readme=ROOT/'README.md'
    block=(
        '## Day-to-day use case catalog\n\n'
        f'[Open the grouped and searchable catalog](catalog/index.html). It contains **{len(catalog["entries"])}** use cases: '
        f'{counts["devops"]} for AWS DevOps Agent, {counts["security"]} for AWS Security Agent, and {counts["finops"]} for AWS FinOps Agent. '
        'Each record identifies delivery mode, cadence, availability, inputs, reviewable output, constraints, canonical guide sections and official sources.\n'
    )
    readme.write_text(replace_marker(readme.read_text(encoding='utf-8'),'<!-- USE-CASE-CATALOG -->','<!-- /USE-CASE-CATALOG -->',block),encoding='utf-8')
    for rel in ('index.html','presentations/index.html'):
        path=ROOT/rel
        soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        nav=soup.select_one('.site-header nav')
        prefix='' if rel=='index.html' else '../'
        if nav and not nav.find('a',href=re.compile(r'catalog/index\.html')):
            a=soup.new_tag('a',href=prefix+'catalog/index.html');a.string='Use cases';nav.append(a)
        grid=soup.select_one('.index-grid')
        if grid and not soup.find(id='use-case-catalog-card'):
            card_html=f'''<article class="index-card" id="use-case-catalog-card"><div class="eyebrow">Structured catalog</div><h2>Day-to-Day Use Cases</h2><p>{len(catalog['entries'])} grouped records covering incident operations, reporting, operational reviews, security assessment, cost analysis, automation and knowledge work.</p><div class="actions"><a class="button-link primary" href="{prefix}catalog/index.html">Open catalog</a><a href="{prefix}catalog/use-cases.md">Markdown</a></div></article>'''
            grid.insert(0,BeautifulSoup(card_html,'html.parser').article)
        path.write_text(str(soup),encoding='utf-8')


def build() -> dict:
    catalog=load_catalog();guides=load_guides();entries=catalog['entries']
    (ROOT/'catalog').mkdir(parents=True,exist_ok=True)
    (ROOT/'catalog/index.html').write_text(catalog_page(catalog,guides),encoding='utf-8')
    (ROOT/'catalog/use-cases.md').write_text(markdown_page(catalog,guides),encoding='utf-8')
    for key in PLATFORM_ORDER:
        platform_entries=[e for e in entries if e['platform']==key]
        inject_report(key,platform_entries,guides)
        inject_presentation(key)
    # Architecture presentation/report link to the cross-platform catalog.
    inject_presentation('architecture')
    arch=ROOT/'guides/architecture.html'
    if arch.exists():
        soup=BeautifulSoup(arch.read_text(encoding='utf-8'),'html.parser')
        nav=soup.select_one('.site-header nav')
        if nav and not nav.find('a',href='../catalog/index.html'):
            a=soup.new_tag('a',href='../catalog/index.html');a.string='Use cases';nav.append(a)
        actions=soup.select_one('.hero .actions')
        if actions and not actions.find('a',href=re.compile(r'catalog/index\.html')):
            a=soup.new_tag('a',href='../catalog/index.html');a.string='Cross-platform use case catalog';actions.append(a)
        arch.write_text(str(soup),encoding='utf-8')
    update_collection_files(catalog)
    return {'entries':len(entries),'platform_counts':Counter(e['platform'] for e in entries)}


def validate(browser: bool=False) -> dict:
    catalog=load_catalog();guides=load_guides();entries=catalog['entries'];errors=[]
    ids=[]
    for entry in entries:
        missing=REQUIRED-set(entry)
        if missing:errors.append(entry.get('id','unknown')+': missing '+','.join(sorted(missing)))
        ids.append(entry['id'])
        if entry['platform'] not in PLATFORMS:errors.append(entry['id']+': invalid platform')
        if not entry['sections']:errors.append(entry['id']+': no canonical sections')
        elif not set(entry['sections'])<=set(guides[entry['platform']]['sections']):errors.append(entry['id']+': invalid canonical section')
        if len(entry['summary'])<45 or len(entry['inputs'])<35 or len(entry['output'])<25:errors.append(entry['id']+': insufficient description')
        if not source_map(entry,guides) and entry['delivery']!='Composed workflow':errors.append(entry['id']+': no official source mapping')
    if len(ids)!=len(set(ids)):errors.append('Duplicate use-case IDs')
    for p in PLATFORM_ORDER:
        if sum(e['platform']==p for e in entries)<12:errors.append(p+': insufficient use-case coverage')
        if len({e['group'] for e in entries if e['platform']==p})<3:errors.append(p+': insufficient grouping')
    for key,deck in DECKS.items():
        titles=[s['title'] for s in deck['slides']]
        if len(titles)!=len(set(titles)):errors.append(key+': duplicate slide title')
        for title in titles:
            if BANNED_TITLE.search(title):errors.append(key+': marketing title '+title)
        for i,slide in enumerate(deck['slides'],1):
            if slide['kind']!='demo' and len(slide['data'])<3:errors.append(f'{key}: slide {i} too sparse')
            if slide['kind']=='table' and len(slide['data'])<5:errors.append(f'{key}: table slide {i} needs more rows')
    for key in PLATFORM_ORDER:
        report=BeautifulSoup((ROOT/f'guides/{key}.html').read_text(encoding='utf-8'),'html.parser')
        expected=sum(e['platform']==key for e in entries)
        if not report.find(id='use-case-catalog'):errors.append(key+': missing embedded catalog')
        if len(report.select('#use-case-catalog .usecase-card'))!=expected:errors.append(key+': embedded catalog count mismatch')
        pres=BeautifulSoup((ROOT/f'presentations/{key}.html').read_text(encoding='utf-8'),'html.parser')
        if not pres.find('a',href=re.compile(r'catalog/index\.html')):errors.append(key+': presentation missing catalog link')
    page=BeautifulSoup((ROOT/'catalog/index.html').read_text(encoding='utf-8'),'html.parser')
    if len(page.select('.usecase-card'))!=len(entries):errors.append('Standalone catalog count mismatch')
    local_links=0
    for path in [ROOT/'catalog/index.html',*(ROOT/f'guides/{k}.html' for k in PLATFORM_ORDER),*(ROOT/f'presentations/{k}.html' for k in (*PLATFORM_ORDER,'architecture'))]:
        soup=BeautifulSoup(path.read_text(encoding='utf-8'),'html.parser')
        for a in soup.select('a[href]'):
            u=urlsplit(a['href'])
            if u.scheme or u.netloc:continue
            local_links+=1
            target=(path.parent/u.path).resolve() if u.path else path
            if not target.exists():errors.append(str(path.relative_to(ROOT))+': missing '+a['href'])
            elif u.fragment and target.suffix=='.html':
                if not BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser').find(id=u.fragment):errors.append(str(path.relative_to(ROOT))+': missing anchor '+a['href'])
    browser_results=[]
    if browser:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser_obj=pw.chromium.launch(headless=True)
            for width in (390,1440):
                page_obj=browser_obj.new_page(viewport={'width':width,'height':1000});js=[];page_obj.on('pageerror',lambda e:js.append(str(e)))
                page_obj.goto((ROOT/'catalog/index.html').as_uri(),wait_until='load')
                total=page_obj.locator('.usecase-card').count();page_obj.locator('[data-uc-search]').fill('minute-by-minute');assert page_obj.locator('.usecase-card:visible').count()==1
                page_obj.locator('[data-uc-reset]').click();assert page_obj.locator('.usecase-card:visible').count()==total
                page_obj.locator('[data-uc-platform]').select_option('devops');assert page_obj.locator('.usecase-card:visible').count()==sum(e['platform']=='devops' for e in entries)
                assert not page_obj.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                browser_results.append({'page':'catalog','width':width,'javascript_errors':js,'filters':'passed'});page_obj.close()
            for key in PLATFORM_ORDER:
                page_obj=browser_obj.new_page(viewport={'width':390,'height':900});js=[];page_obj.on('pageerror',lambda e:js.append(str(e)))
                page_obj.goto((ROOT/f'guides/{key}.html').as_uri(),wait_until='load')
                n=page_obj.locator('#use-case-catalog .usecase-card').count();page_obj.locator('#use-case-catalog [data-uc-search]').fill('zz-no-match');assert page_obj.locator('#use-case-catalog .usecase-card:visible').count()==0
                page_obj.locator('#use-case-catalog [data-uc-reset]').click();assert page_obj.locator('#use-case-catalog .usecase-card:visible').count()==n
                assert not page_obj.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                browser_results.append({'page':key+'-report','width':390,'javascript_errors':js,'embedded_catalog':'passed'});page_obj.close()
            browser_obj.close()
    result={
        'revision':catalog['revision'],
        'use_cases':len(entries),
        'platform_counts':dict(Counter(e['platform'] for e in entries)),
        'group_counts':dict(Counter(e['group'] for e in entries)),
        'delivery_counts':dict(Counter(e['delivery'] for e in entries)),
        'local_links_checked':local_links,
        'browser':browser_results,
        'marketing_title_matches':[],
        'errors':errors,
        'boundary':'Catalog structure, source mapping, local links, HTML controls and slide information density were checked. No live AWS workflow or use-case outcome was executed.',
    }
    (ROOT/'qa/use-case-catalog.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    if errors:raise SystemExit(json.dumps(result,indent=2))
    return result


def finalize(result: dict) -> None:
    checks_path=ROOT/'qa/checks.json'
    if checks_path.exists():
        checks=json.loads(checks_path.read_text(encoding='utf-8'))
        checks['use_case_catalog']={k:v for k,v in result.items() if k not in {'browser','errors'}}
        checks['use_case_catalog']['browser_checks']=len(result['browser'])
        checks_path.write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    validation=ROOT/'VALIDATION.md'
    if validation.exists():
        block=(
            '## Use case catalog and presentation structure\n\n'
            f'The published catalog contains **{result["use_cases"]}** use cases grouped by platform, operational family, delivery mode, cadence and availability. '
            'Browser checks cover the standalone catalog and embedded report catalogs. Presentation titles are checked against the editorial marketing-language list, and non-exercise slides must meet minimum information-density rules. '
            'These checks validate documentation structure and controls, not successful AWS execution.\n'
        )
        text=replace_marker(validation.read_text(encoding='utf-8'),'<!-- USE-CASE-VALIDATION -->','<!-- /USE-CASE-VALIDATION -->',block)
        validation.write_text(text,encoding='utf-8')
    manifest_path=ROOT/'MANIFEST.json'
    if manifest_path.exists():
        manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
        for path in sorted([*(ROOT/'catalog').glob('*'),ROOT/'qa/use-case-catalog.json',ROOT/'tools/use_case_catalog.py']):
            if path.is_file():
                manifest['files'][path.relative_to(ROOT).as_posix()]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        for path in (checks_path,validation):
            if path.exists():manifest['files'][path.relative_to(ROOT).as_posix()]={'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        manifest_path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')


def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--browser',action='store_true');parser.add_argument('--finalize',action='store_true');args=parser.parse_args()
    if not args.check:
        summary=build();print(json.dumps(summary,indent=2,default=dict))
    if args.check or args.finalize:
        result=validate(args.browser);print(json.dumps(result,indent=2,ensure_ascii=False))
        if args.finalize:finalize(result)


if __name__=='__main__':
    main()
