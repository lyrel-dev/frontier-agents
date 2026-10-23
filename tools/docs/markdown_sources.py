"""Canonical Markdown/YAML sources and deterministic compatibility projections.

Only content/**/*.md is authored. HTML, assembled Markdown and catalog JSON are
outputs. Coordinates use Unicode code points, UTF-8 bytes and 1-based lines.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import re
import subprocess
from xml.etree import ElementTree as ET
import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'content'
FROZEN = {'use-cases', 'mechanisms', 'features', 'profiles', 'aliases', 'resource-models'}
MARKER = re.compile(r'^<!-- block: ([A-Za-z0-9_.:-]+) -->\s*$')
FIELD = re.compile(r'<!-- field: ([A-Za-z0-9_.:-]+) -->\n(.*?)\n<!-- /field -->', re.S)
FRONT = re.compile(r'\A---\n(.*?)\n---(?:\n|\Z)', re.S)
MD = MarkdownIt('commonmark', {'html': False}).enable('table')

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for k, v in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in result:
            raise ValueError(f'Duplicate YAML property: {key}')
        result[key] = loader.construct_object(v, deep=deep)
    return result

UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def digest(value):
    return hashlib.sha256(value.encode('utf-8') if isinstance(value, str) else value).hexdigest()

def strip_blocks(text):
    return re.sub(r'^<!-- block: [A-Za-z0-9_.:-]+ -->\n', '', text, flags=re.M).strip('\n')

def split_body(raw, offset):
    """Recognize markers outside code fences, never markers inside examples."""
    marks = []
    position = offset
    fence = None
    for line in raw[offset:].splitlines(keepends=True):
        fm = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fm:
            token = fm[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
        match = MARKER.match(line.rstrip('\n')) if fence is None else None
        if match:
            marks.append((position, position + len(line), match[1]))
        position += len(line)
    result = []
    for i, (_, start, bid) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(raw)
        while start < end and raw[start] == '\n':
            start += 1
        while end > start and raw[end - 1] == '\n':
            end -= 1
        result.append((bid, start, end))
    return result

@dataclass
class Source:
    path: Path
    raw: str
    meta: dict
    body_start: int

    @classmethod
    def read(cls, path):
        path = Path(path)
        if path.is_symlink() or not path.resolve().is_relative_to(CONTENT.resolve()):
            raise ValueError('Source must be a regular file inside content/: ' + str(path))
        raw = path.read_text(encoding='utf-8')
        if '\r' in raw:
            raise ValueError('Use UTF-8 with LF line endings: ' + str(path))
        match = FRONT.match(raw)
        if not match:
            raise ValueError('Missing YAML front matter: ' + str(path))
        meta = yaml.load(match[1], Loader=UniqueLoader)
        if not isinstance(meta, dict) or not all(isinstance(meta.get(k), str) and meta[k] for k in ('id', 'kind')):
            raise ValueError('Front matter requires nonempty id and kind: ' + str(path))
        return cls(path, raw, meta, match.end())

    @property
    def id(self):
        return self.meta['id']

    @property
    def body(self):
        return strip_blocks(self.raw[self.body_start:])

    @property
    def protected(self):
        return self.meta.get('collection') in FROZEN or self.meta.get('frozen') is True

    def target(self, bid, start, end, field=None):
        raw = self.raw
        return {'source_id': self.id, 'path': self.path.relative_to(ROOT).as_posix(),
                'block_id': bid, 'source_kind': self.meta['kind'],
                'product': self.meta.get('product', ''), 'title': self.meta.get('title', self.id),
                'file_sha256': digest(raw), 'block_sha256': digest(raw[start:end]),
                'start_char': start, 'end_char': end,
                'start_byte': len(raw[:start].encode()), 'end_byte': len(raw[:end].encode()),
                'start_line': raw.count('\n', 0, start) + 1,
                'end_line': raw.count('\n', 0, max(start, end - 1)) + 1,
                'markdown': raw[start:end], 'protected': self.protected,
                'field': field}

    def targets(self):
        result = [self.target(bid, start, end) for bid, start, end in split_body(self.raw, self.body_start)]
        # The title is editable at its exact YAML scalar, not through a whole-header replacement.
        match = FRONT.match(self.raw)
        tree = yaml.compose(match[1], Loader=UniqueLoader)
        if isinstance(tree, yaml.MappingNode):
            for key, value in tree.value:
                if key.value == 'title' and isinstance(value, yaml.ScalarNode):
                    result.append(self.target(self.id + '::title', match.start(1) + value.start_mark.index,
                                              match.start(1) + value.end_mark.index, 'title'))
        return result

    def fields(self):
        return {key: text for key, text in FIELD.findall(self.body)}

class Repository:
    def __init__(self):
        self.sources = [Source.read(p) for p in sorted(CONTENT.rglob('*.md'))]
        self.by_id = {}
        self.targets = {}
        for source in self.sources:
            if source.id in self.by_id:
                raise ValueError('Duplicate source id: ' + source.id)
            self.by_id[source.id] = source
            for target in source.targets():
                if target['block_id'] in self.targets:
                    raise ValueError('Duplicate block id: ' + target['block_id'])
                self.targets[target['block_id']] = target
        self.revision = digest('\n'.join(s.path.relative_to(ROOT).as_posix() + ':' + digest(s.raw) for s in self.sources))

    def select(self, kind, product=None):
        values = [s for s in self.sources if s.meta['kind'] == kind and (product is None or s.meta.get('product') == product)]
        return sorted(values, key=lambda s: (s.meta.get('order', 0), s.id))

    def decode(self, source):
        fields = source.fields()
        visiting = set()
        def walk(value):
            if isinstance(value, dict):
                if set(value) == {'$markdown'}:
                    return fields[value['$markdown']]
                if set(value) == {'$record'}:
                    ident = value['$record']
                    if ident in visiting:
                        raise ValueError('Cyclic record reference: ' + ident)
                    visiting.add(ident)
                    decoded = self.decode(self.by_id[ident])
                    visiting.remove(ident)
                    return decoded
                return {k: walk(v) for k, v in value.items()}
            if isinstance(value, list):
                return [walk(v) for v in value]
            return value
        return walk(source.meta.get('data', {}))

    def registers(self):
        return {s.meta['collection']: self.decode(s) for s in self.select('register')}

    def chapters(self):
        result = {}
        for source in self.select('chapter'):
            item = dict(source.meta['definition'])
            item['purpose'] = source.body
            result.setdefault(source.meta['product'], []).append(item)
        return result

    def guides(self):
        result = {}
        chapters = self.chapters()
        for doc in self.select('guide'):
            product = doc.meta['product']
            refs = doc.meta['references']
            sections = {}
            for source in self.select('section', product):
                body = source.body
                sources = sorted(set(re.findall(r'\b[DSFA]S\d+\b', body)))
                if set(sources) - set(refs):
                    raise ValueError(source.id + ': missing source references')
                sections[source.id] = {'id': source.id, 'title': source.meta['title'], 'body': body,
                                       'sources': sources, '_source': source.id}
            order = [sid for c in chapters[product] for sid in c['sections']]
            if set(order) != set(sections) or len(order) != len(set(order)):
                raise ValueError(product + ': chapter membership mismatch')
            result[product] = {'intro': doc.body, 'sections': {sid: sections[sid] for sid in order},
                               'refs': refs, 'definitions': '\n'.join(f'[{k}]: {v}' for k, v in refs.items()),
                               '_source': doc.id}
        return result

    def decks(self):
        result = {}
        for deck in self.select('deck'):
            product = deck.meta['product']
            data = dict(deck.meta['definition'])
            data['subtitle'] = deck.body
            slides = []
            for source in self.select('slide', product):
                meta = source.meta
                body, separator, notes = source.body.partition('\n## Presenter notes\n')
                if not separator:
                    raise ValueError(source.id + ': Presenter notes section missing')
                item = dict(meta['definition'])
                item['title'] = meta['title']
                item['message'] = notes.strip()
                item['_source'] = source.id
                item['_markdown'] = body.strip()
                item['data'] = []
                if item['kind'] in ('table', 'demo'):
                    from bs4 import BeautifulSoup
                    table = BeautifulSoup(MD.render(body), 'html.parser').find('table')
                    if table is None:
                        raise ValueError(source.id + ': expected Markdown table')
                    rows = [[c.get_text() for c in row.find_all(['th', 'td'])] for row in table.find_all('tr')]
                    item['data'] = rows[1:] if item['kind'] == 'demo' else rows
                elif item['kind'] == 'diagram':
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(MD.render(body), 'html.parser')
                    item['explain'] = [n.get_text() for n in soup.select('ol > li')]
                else:
                    parts = re.split(r'^## (.+)\n', body, flags=re.M)
                    item['data'] = [[parts[i], parts[i + 1].strip()] for i in range(1, len(parts), 2)]
                slides.append(item)
            data['slides'] = slides
            result[product] = data
        return result

    def diagrams(self):
        result = {}
        for source in self.select('diagram'):
            match = re.search(r'^```(dot|svg)\n(.*?)\n```\s*$', source.body, re.M | re.S)
            if not match:
                raise ValueError(source.id + ': diagram needs a dot or svg fenced block')
            description = source.body[:match.start()].strip()
            result[source.id] = (source.meta['title'], description, source.meta['refs'],
                                 match[2] if match[1] == 'dot' else '')
        return result

@lru_cache(maxsize=1)
def repository():
    return Repository()

def settings(name):
    return repository().by_id['settings-' + name].meta['data']

def materialize():
    """Regenerate read-only JSON and assembled Markdown; never write content/."""
    repo = repository()
    for name, value in repo.registers().items():
        source = next(s for s in repo.select('register') if s.meta['collection'] == name)
        fmt = source.meta.get('json_format', {'indent': 2, 'ensure_ascii': True, 'newline': True})
        text = json.dumps(value, indent=fmt['indent'], ensure_ascii=fmt['ensure_ascii']) + ('\n' if fmt['newline'] else '')
        (ROOT / 'catalog' / (name + '.json')).write_text(text, encoding='utf-8')
    for product, guide in repo.guides().items():
        lines = [guide['intro'], '']
        for number, chapter in enumerate(repo.chapters()[product], 1):
            lines += [f'## {number:02d}. {chapter["title"]}', '', chapter['purpose'], '']
            for sid in chapter['sections']:
                section = guide['sections'][sid]
                lines += [f'### {sid} — {section["title"]}', '', section['body'], '']
        lines += [guide['definitions'], '']
        (ROOT / 'guides' / (product + '.md')).write_text('\n'.join(lines), encoding='utf-8')
    return repo

def build_diagrams():
    repo = repository()
    ns = '{http://www.w3.org/2000/svg}'
    for source in repo.select('diagram'):
        match = re.search(r'^```(dot|svg)\n(.*?)\n```\s*$', source.body, re.M | re.S)
        if match[1] == 'svg':
            value = match[2]
        else:
            defaults = settings('diagram-defaults')['graph_prefix']
            value = subprocess.run(['dot', '-Tsvg'], input=defaults + match[2] + '\n}', text=True,
                                   capture_output=True, check=True).stdout
        root = ET.fromstring(value)
        for element in root.iter():
            if element.tag.split('}')[-1].lower() in ('script', 'foreignobject'):
                raise ValueError('Executable SVG element: ' + source.id)
            for attr, val in element.attrib.items():
                if attr.lower().startswith('on') or (attr.split('}')[-1] in ('href', 'src') and not val.startswith('#')):
                    raise ValueError('External or executable SVG attribute: ' + source.id)
        for child in list(root):
            if child.tag in (ns + 'title', ns + 'desc'):
                root.remove(child)
        title = ET.Element(ns + 'title', {'id': source.id + '-title'}); title.text = source.meta['title']
        desc = ET.Element(ns + 'desc', {'id': source.id + '-desc'}); desc.text = source.body[:match.start()].strip()
        root.insert(0, title); root.insert(1, desc)
        root.set('role', 'img'); root.set('aria-labelledby', source.id + '-title ' + source.id + '-desc')
        root.set('data-diagram', source.id)
        ET.register_namespace('', ns[1:-1]); ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
        (ROOT / 'assets/diagrams' / (source.id + '.svg')).write_text(ET.tostring(root, encoding='unicode'), encoding='utf-8')
    return len(repo.select('diagram'))
