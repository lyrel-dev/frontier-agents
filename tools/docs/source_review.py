"""Add source identity without making the published reader a content editor."""
from pathlib import Path
from html import escape
import json
import re
from collections import defaultdict
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from markdown_sources import repository, ROOT, FIELD

HERE = Path(__file__).resolve().parent
MD = MarkdownIt('commonmark', {'html': False}).enable('table')


def normalized(text):
    return ' '.join(text.split())


def attach(node, target):
    node['data-review-block'] = target['block_id']
    node['data-review-source'] = target['source_id']
    node['data-review-protected'] = 'true' if target['protected'] else 'false'


def body_html(source, renderer, definitions='', links=None, prefix='', role=None):
    pieces = []
    in_notes = False
    for target in source.targets():
        if target['field']:
            continue
        text = target['markdown']
        if text.strip() == '## Presenter notes':
            in_notes = True
            if role == 'slide':
                break
            continue
        if role == 'notes' and not in_notes:
            continue
        if role == 'slide' and in_notes:
            continue
        rendered = renderer(text, definitions, links or {}, prefix+'-'+target['block_id'])
        soup = BeautifulSoup(rendered, 'html.parser')
        node = soup.find(True)
        if node:
            attach(node, target)
        pieces.append(str(soup))
    return ''.join(pieces)


def render(text, definitions, links, prefix, renderer):
    repo = repository()
    source = None
    for product in ('devops','security','finops','architecture'):
        if prefix == product+'-intro':
            source = repo.by_id.get('guide-'+product)
    if source is None:
        sid = re.search(r'-([DSFA]-(?:M|U)?\d+)$', prefix)
        if sid:
            source = repo.by_id.get(sid[1])
    if source is None or source.body.strip() != text.strip():
        return renderer(text, definitions, links, prefix)
    return body_html(source, renderer, definitions, links, prefix)


def slide(data, prefix, renderer):
    source = repository().by_id[data['_source']]
    value = body_html(source, renderer, prefix=prefix, role='slide')
    soup = BeautifulSoup(value, 'html.parser')
    if data['kind'] == 'diagram':
        for node in soup.find_all('ol', recursive=False):
            node['class'] = 'diagram-steps'
    elif data['kind'] not in ('table','demo'):
        outer = soup.new_tag('div', attrs={'class':'flow' if data['kind']=='flow' else 'columns'})
        group = None
        for node in list(soup.contents):
            if getattr(node, 'name', None) == 'h2' or group is None:
                group = soup.new_tag('section', attrs={'class':'content-unit'})
                outer.append(group)
            group.append(node.extract())
        soup.append(outer)
    return str(soup)


def plain(target):
    value = target['markdown']
    if target.get('field') == 'title':
        return target['title']
    if target.get('rendered_text'):
        return target['rendered_text']
    value = re.sub(r'<!--.*?-->', '', value, flags=re.S)
    if value.lstrip().startswith('```svg'):
        tree = BeautifulSoup(value[6:].rsplit('```',1)[0], 'xml')
        return ' '.join(n.get_text() for n in tree.find_all('text'))
    return normalized(BeautifulSoup(MD.render(value), 'html.parser').get_text(' ', strip=True))


def target_for_title(source):
    return next((t for t in source.targets() if t['field']=='title'), None)


def annotate_titles(soup, current, repo):
    product = Path(current).stem
    if current.startswith('guides/') and product in ('devops','security','finops','architecture'):
        source = repo.by_id['guide-'+product]
        node = soup.select_one('main h1')
        if node is not None and target_for_title(source):
            attach(node, target_for_title(source))
        for section in soup.select('.report-section'):
            source = repo.by_id.get(section.get('id'))
            if source and section.find('h3') and target_for_title(source):
                attach(section.find('h3'), target_for_title(source))
        for chapter in soup.select('[data-reader-chapter]'):
            source = repo.by_id.get('chapter-'+product+'-'+chapter['id'].removeprefix('chapter-'))
            if source:
                if chapter.find('h2') and target_for_title(source):
                    attach(chapter.find('h2'), target_for_title(source))
                first = chapter.select_one('header p:not(.chapter-label)')
                targets = [t for t in source.targets() if not t['field']]
                if first and targets:
                    attach(first, targets[0])
    if current.startswith('presentations/') and product in ('devops','security','finops','architecture'):
        sources = repo.select('slide', product)
        for node, source in zip(soup.select('.slide'), sources):
            if target_for_title(source):
                attach(node.h1, target_for_title(source))
            notes = [t for t in source.targets() if not t['field'] and t['markdown'].strip() != '## Presenter notes']
            if notes and node.select_one('.slide-explanation'):
                attach(node.select_one('.slide-explanation'), notes[-1])


def annotate_records(soup, current, repo):
    if not current.startswith('catalog/'):
        return
    candidates = repo.select('record')
    case_id = Path(current).stem
    if case_id.startswith('UC-'):
        root = repo.by_id.get('record-use-cases-'+case_id)
        if not root:
            return
        data = repo.decode(root)
        ids = {root.id}
        ids.update('record-profiles-'+p for p in data.get('profiles', []))
        ids.update('record-mechanisms-'+s['mechanism'] for s in data.get('workflow', []) if s.get('mechanism'))
        candidates = [s for s in candidates if s.id in ids]
        if soup.select_one('main h1') and target_for_title(root):
            attach(soup.select_one('main h1'), target_for_title(root))
    lookup = defaultdict(list)
    for source in candidates:
        for target in source.targets():
            text = plain(target)
            if len(text)>24 and not text.startswith('```'):
                lookup[normalized(text)].append(target)
    # Only exact, unambiguous text matches are mapped. No fuzzy reassignment.
    for node in soup.select('main p,main li,main td,main th,main h2,main h3,main h4'):
        if node.has_attr('data-review-block') or node.find_parent(attrs={'data-review-block':True}) or node.find(['p','li','table']):
            continue
        text = normalized(node.get_text(' ',strip=True))
        choices = lookup.get(text, [])
        if len(choices)==1:
            attach(node, choices[0])


def finish():
    repo = repository()
    pages = [ROOT/'index.html', *sorted((ROOT/'guides').glob('*.html')),
             *sorted((ROOT/'catalog').glob('*.html')), *sorted((ROOT/'presentations').glob('*.html'))]
    search = []
    seen = set()
    mappings = {}
    for path in pages:
        current = path.relative_to(ROOT).as_posix()
        soup = BeautifulSoup(path.read_text(), 'html.parser')
        for old in soup.select('[data-review-ui],#review-source-map'):
            old.decompose()
        annotate_titles(soup, current, repo)
        annotate_records(soup, current, repo)
        for figure in soup.select('figure[data-diagram-key]'):
            source = repo.by_id.get(figure['data-diagram-key'])
            if source:
                targets = source.targets()
                code = next((t for t in targets if t['markdown'].startswith(('```dot','```svg'))),None)
                caption = next((t for t in targets if not t['field'] and not t['markdown'].startswith('```')),None)
                if code:
                    attach(figure, code)
                if caption and figure.find('figcaption'):
                    attach(figure.find('figcaption'), caption)
        local = {}
        counter = defaultdict(int)
        for node in soup.select('[data-review-block]'):
            bid = node['data-review-block']
            if bid not in repo.targets:
                raise ValueError('Rendered block not in source repository: '+bid)
            target = repo.targets[bid]
            counter[bid] += 1
            if not node.get('id'):
                node['id'] = 'review-'+bid.replace(':','-')+'-'+str(counter[bid])
            local[bid] = target
            ident = (bid, current)
            if ident not in seen:
                seen.add(ident)
                text = plain(target)
                if len(text)>1:
                    search.append({'block_id':bid,'title':target['title'],'text':text[:18000],
                                   'kind':target['source_kind'],'product':target['product'],
                                   'source':target['path'],'page':current,'anchor':node['id']})
        packet = {'schema':'frontier-source-map/v1','repository':'lyrel-dev/frontier-agents',
                  'content_revision':repo.revision,'document':current,
                  'title':soup.title.get_text() if soup.title else current,'targets':local,
                  'source_files':sorted({t['path'] for t in local.values()}),
                  'coordinate_contract':'source offsets are Unicode code points and UTF-8 bytes; DOM selectors use UTF-16 code units'}
        node = soup.new_tag('script', attrs={'type':'application/json','id':'review-source-map'})
        node.string = json.dumps(packet,ensure_ascii=False).replace('<','\\u003c')
        soup.body.append(node)
        depth = '../' * (len(Path(current).parts)-1)
        capture=soup.new_tag('script',attrs={'data-review-ui':'true'})
        capture.string='window.__reviewInitialHash=location.hash;'
        soup.head.insert(0,capture)
        css=soup.new_tag('link',attrs={'rel':'stylesheet','href':depth+'assets/review.css','data-review-ui':'true'})
        soup.head.append(css)
        for asset in ('search-index.js','review.js'):
            script=soup.new_tag('script',attrs={'src':depth+'assets/'+asset,'data-review-ui':'true','defer':True})
            soup.body.append(script)
        path.write_text(str(soup)+'\n',encoding='utf-8')
        mappings[current]={'source_files':packet['source_files'],'mapped_blocks':len(local)}
    # Prefer a guide occurrence to a duplicate in speaker notes; preserve slide-only sources.
    rank=lambda item: (0 if item['page'].startswith('guides/') else 1 if item['page'].startswith('catalog/') else 2)
    unique={}
    for item in sorted(search,key=rank):
        unique.setdefault(item['block_id'],item)
    content={'schema':'frontier-search/v1','revision':repo.revision,'entries':list(unique.values())}
    (ROOT/'assets/search-index.js').write_text('window.FRONTIER_SEARCH='+json.dumps(content,ensure_ascii=False).replace('<','\\u003c')+';\n')
    for name in ('review.js','review.css'):
        (ROOT/'assets'/name).write_text((HERE/name).read_text())
    (ROOT/'qa/source-map.json').write_text(json.dumps({'schema':'frontier-source-map-report/v1','content_revision':repo.revision,
         'source_files':len(repo.sources),'search_blocks':len(unique),'pages':mappings},indent=2)+'\n')
