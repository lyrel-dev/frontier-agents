"""Attach precise Markdown provenance and local review controls to rendered pages."""
from __future__ import annotations
from collections import defaultdict
from html import escape
from pathlib import Path
import hashlib
import json
import re
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
import md_source as source

ROOT=source.ROOT
HERE=Path(__file__).resolve().parent
SCHEMA='frontier.review.v1'


def normal(value):
    return re.sub(r'\s+',' ',str(value)).strip()


def visible(raw):
    return normal(BeautifulSoup(source.MD.render(raw),'html.parser').get_text(' ',strip=True))


def pack(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')


def target_maps():
    result={}
    for d in source.documents().values():
        result[d.id+'::@document']=d.target('@document')
        for bid in d.blocks:result[d.id+'::'+bid]=d.target(bid)
    return result


def doc_route(d):
    p=d.meta.get('product')
    if d.kind=='section':return 'guides/'+p+'.html#'+d.id
    if d.kind=='guide':return 'guides/'+p+'.html'
    if d.kind=='chapter':return 'guides/'+p+'.html#chapter-'+d.meta['slug']
    if d.kind=='slide':return 'presentations/'+p+'.html#slide-'+f'{d.meta["order"]:02d}'
    if d.kind=='deck':return 'presentations/'+p+'.html'
    if d.kind=='record' and d.meta.get('registry')=='use-cases':return 'catalog/'+d.meta['record_id']+'.html#'+d.meta['record_id']
    if d.kind=='diagram':return 'assets/diagrams/'+d.id+'.svg'
    if d.kind=='page' and d.meta.get('output')=='AUTHORING.md':return 'authoring.html'
    if d.kind=='record' and d.meta.get('registry')=='resource-models':return 'catalog/resource-models.html#'+d.meta['record_id']
    return None


def scopes(current):
    docs=source.documents();ids=set()
    if current.startswith('guides/'):
        p=Path(current).stem
        ids={d.id for d in docs.values() if d.meta.get('product')==p}
    elif current.startswith('presentations/') and Path(current).stem!='index':
        p=Path(current).stem
        ids={d.id for d in docs.values() if d.meta.get('product')==p}
    elif current.startswith('catalog/UC-'):
        cid=Path(current).stem
        case=next(c for c in source.registry('use-cases')['entries'] if c['id']==cid)
        needed={cid,*case.get('profiles',[])}
        needed.update(s['mechanism'] for s in case['workflow'])
        needed.update(f for s in case['workflow'] for f in s['configuration_features'])
        ids={d.id for d in docs.values() if d.meta.get('record_id') in needed}
    elif current=='catalog/resource-models.html':
        ids={d.id for d in docs.values() if d.meta.get('registry')=='resource-models'}
    elif current=='catalog/index.html':
        ids={d.id for d in docs.values() if d.meta.get('registry')=='use-cases'}
    elif current=='authoring.html':ids={'authoring'}
    else:ids={d.id for d in docs.values() if d.kind in ('guide','chapter','deck')}
    return ids


def page_documents(current):
    docs=source.documents()
    if current.startswith('guides/'):
        p=Path(current).stem
        return [d.id for d in docs.values() if d.meta.get('product')==p and d.kind in ('guide','chapter','section','references')]
    if current.startswith('presentations/') and Path(current).stem!='index':
        p=Path(current).stem
        return [d.id for d in docs.values() if d.meta.get('product')==p and d.kind in ('deck','slide')]
    if current.startswith('catalog/UC-'):
        return [d.id for d in docs.values() if d.meta.get('record_id')==Path(current).stem and d.meta.get('registry')=='use-cases']
    if current=='catalog/resource-models.html':return [d.id for d in docs.values() if d.meta.get('registry')=='resource-models']
    if current=='authoring.html':return ['authoring']
    return sorted(scopes(current))


def annotate(soup,current,targets):
    """Use explicit source IDs where possible. Never guess an ambiguous text match."""
    docs=source.documents();candidates=scopes(current);by_text=defaultdict(list)
    for did in candidates:
        d=docs[did]
        for bid,raw in d.blocks.items():
            if bid.startswith('@'):continue
            text=normal(raw)
            if len(text)>=12:by_text[text].append(did+'::'+bid)
            rendered=visible(raw)
            if rendered!=text and len(rendered)>=12:by_text[rendered].append(did+'::'+bid)
    # Headers and complete sections receive explicit source-document selectors.
    if current.startswith('guides/'):
        product=Path(current).stem
        for section in soup.select('.report-section[id]'):
            if section['id'] in docs:
                section['data-source-document']=section['id']
                h=section.find(['h2','h3'],recursive=False)
                if h and '@title' in docs[section['id']].blocks:h['data-source-key']=section['id']+'::@title'
        for ch in source.by_kind('chapter',product):
            el=soup.find(id='chapter-'+ch.meta['slug'])
            if el:
                el['data-source-document']=ch.id
                h=el.select_one('header h2')
                if h:h['data-source-key']=ch.id+'::@title'
    if current.startswith('presentations/'):
        product=Path(current).stem
        slides=source.by_kind('slide',product)
        for node,d in zip(soup.select('.slide'),slides):
            node['data-source-document']=d.id
            node['data-source-key']=d.id+'::@document'
            if node.h1:node.h1['data-source-key']=d.id+'::@title'
            message=node.select_one('.slide-explanation')
            if message:message['data-source-key']=d.id+'::speaker-notes'
            content=node.select_one('.slide-body')
            if content:content['data-source-key']=d.id+'::slide-content'
            steps=node.select_one('.diagram-steps')
            if steps and 'reading-steps' in d.blocks:steps['data-source-key']=d.id+'::reading-steps'
        for i,n in enumerate(soup.select('.note-block')):
            if i<len(slides):
                p=n.select_one('.talk-track p')
                if p:p['data-source-key']=slides[i].id+'::speaker-notes'
    # Explicit record identity for catalog/model sections; body values are bound below.
    for node in soup.select('.model-record[id], .configuration-recipe[id], main > header[id]'):
        matches=[d for d in docs.values() if d.meta.get('record_id')==node['id']]
        if len(matches)==1:
            node['data-source-document']=matches[0].id
            h=node.find(['h1','h2','h3'])
            if h and '@title' in matches[0].blocks:h['data-source-key']=matches[0].id+'::@title'
    for n in soup.select('main p, main li, main td, main dd, main h3, main h4'):
        if n.get('data-source-key') or n.find_parent(attrs={'data-source-key':True}) or n.find_parent(['svg','nav']):continue
        text=normal(n.get_text(' ',strip=True))
        keys=set(by_text.get(text,[]))
        if not keys:
            # Fixed labels such as "Failure handling." are renderer chrome.
            label=n.find('strong',recursive=False)
            if label:
                without=text[len(normal(label.get_text(' ',strip=True))):].strip()
                keys=set(by_text.get(without,[]))
        if len(keys)==1:n['data-source-key']=keys.pop()
    for fig in soup.select('figure[data-diagram-key]'):
        did=fig['data-diagram-key']
        if did in docs:
            fig['data-source-key']=did+'::definition'
            fig['data-source-document']=did
            cap=fig.find('figcaption')
            if cap and 'description' in docs[did].blocks:cap['data-source-key']=did+'::description'
    # Stable render anchors are distinct from source IDs when a source is reused.
    counts=defaultdict(int)
    for node in soup.select('[data-source-key]'):
        key=node['data-source-key']
        if key not in targets:raise source.SourceError('Unknown render target '+key)
        counts[key]+=1
        if not node.get('id'):
            suffix='' if counts[key]==1 else '-'+str(counts[key])
            node['id']='src-'+hashlib.sha256(key.encode()).hexdigest()[:16]+suffix
    return soup


def build():
    targets=target_maps();revision=source.source_revision();search=[];page_records={}
    css=(HERE/'review_ui.css').read_text();js=(HERE/'review_ui.js').read_text()
    # Search data is a local script rather than fetch(JSON), so file:// remains supported.
    paths=[ROOT/'index.html',ROOT/'authoring.html']
    paths += sorted((ROOT/'guides').glob('*.html'))+sorted((ROOT/'presentations').glob('*.html'))+sorted((ROOT/'catalog').glob('*.html'))
    for path in paths:
        if not path.exists():continue
        current=path.relative_to(ROOT).as_posix()
        soup=BeautifulSoup(path.read_text(),'html.parser')
        for old in soup.select('[data-review-generated]'):old.decompose()
        annotate(soup,current,targets)
        keys={n['data-source-key'] for n in soup.select('[data-source-key]')}
        for n in soup.select('[data-source-document]'):keys.add(n['data-source-document']+'::@document')
        page_ids=page_documents(current)
        keys.update(d+'::@document' for d in page_ids)
        chosen={k:targets[k] for k in sorted(keys)}
        info={'schema':SCHEMA,'repository':'lyrel-dev/frontier-agents','revision':revision,
              'page':current,'title':soup.title.get_text() if soup.title else current,
              'document_sources':page_ids,'targets':chosen}
        data=soup.new_tag('script',id='review-source-data',type='application/json')
        data['data-review-generated']='data';data.string=pack(info);soup.body.append(data)
        style=soup.new_tag('style');style['data-review-generated']='style';style.string=css;soup.head.append(style)
        idx=soup.new_tag('script',src=('../' if '/' in current else '')+'assets/search-index.js')
        idx['data-review-generated']='search';soup.body.append(idx)
        script=soup.new_tag('script');script['data-review-generated']='runtime';script.string=js;soup.body.append(script)
        path.write_text(str(soup)+'\n',encoding='utf-8')
        page_records[current]={'targets':sorted(keys),'documents':page_ids}
        # One primary occurrence per source and page; notes repeats are not search duplicates.
        seen=set()
        for node in soup.select('[data-source-key]'):
            key=node['data-source-key'];t=targets[key]
            if key in seen or t['block_id']=='@document' or node.find_parent(class_='note-block'):continue
            seen.add(key)
            text=normal(node.get_text(' ',strip=True))
            if not text:continue
            article=node.find_parent(class_='slide')
            slide=article.get('id') if article else None
            search.append({'key':key,'path':current,'anchor':node['id'],'slide':slide,
                           'title':t['title'],'kind':t['kind'],'text':text,'source_path':t['source_path']})
    # Exact source index is build output; it is never an editing destination.
    index={'schema':'frontier.source-map.v1','repository':'lyrel-dev/frontier-agents','revision':revision,
           'targets':targets,'pages':page_records}
    (ROOT/'assets/source-map.json').write_text(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n')
    (ROOT/'assets/search-index.js').write_text('window.FRONTIER_SEARCH='+pack(search)+';\n')
    report={'source_documents':len(source.documents()),'source_targets':len(targets),'annotated_pages':len(page_records),
            'search_entries':len(search),'revision':revision}
    (ROOT/'qa/markdown-build.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
