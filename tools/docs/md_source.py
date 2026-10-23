"""Markdown is the authoring format; HTML and JSON are compiled projections.

No source file is modified by a build. Explicit block markers preserve identity
across edits. Positions are UTF-8 byte offsets, never browser string offsets.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import re
import subprocess
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import yaml
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / 'content'
MARKER = re.compile(r'^<!-- block: ([A-Za-z0-9_.:-]+) -->\n(.*?)\n<!-- /block -->[ \t]*$', re.M | re.S)
SAFE_ID = re.compile(r'^[A-Za-z0-9][A-Za-z0-9_.:-]*$')
MD = MarkdownIt('commonmark', {'html': False}).enable('table')
REGISTRIES = ('use-cases','mechanisms','features','profiles','aliases','resource-models')

class SourceError(ValueError):
    pass

class UniqueLoader(yaml.SafeLoader):
    pass

def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str) or key in result:
            raise SourceError('YAML keys must be unique strings: '+repr(key))
        result[key] = loader.construct_object(value_node, deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)

def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode('utf-8')).hexdigest()

def safe_path(value, root=ROOT):
    p = Path(value)
    if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != 'content' or p.suffix != '.md':
        raise SourceError('Only content/*.md source paths are allowed: '+str(value))
    out = root / p
    for candidate in (out, *out.parents):
        if candidate == root:
            break
        if candidate.is_symlink():
            raise SourceError('Symlink source paths are forbidden')
    if not out.resolve().is_relative_to((root/'content').resolve()):
        raise SourceError('Source path escapes content/')
    return out

class Document:
    def __init__(self, path, root=ROOT):
        self.path = Path(path)
        self.relative = self.path.relative_to(root).as_posix()
        self.bytes = self.path.read_bytes()
        self.text = self.bytes.decode('utf-8')
        if '\r' in self.text:
            raise SourceError(self.relative+': use UTF-8 and LF newlines')
        if not self.text.startswith('---\n'):
            raise SourceError(self.relative+': YAML frontmatter is required')
        end = self.text.find('\n---\n', 4)
        if end < 0:
            raise SourceError(self.relative+': frontmatter closing delimiter is missing')
        self.header_end = end+5
        self.header = self.text[4:end]
        self.meta = yaml.load(self.header, Loader=UniqueLoader)
        if not isinstance(self.meta, dict):
            raise SourceError(self.relative+': frontmatter must be a mapping')
        self.id = self.meta.get('id','')
        if not isinstance(self.id, str) or not SAFE_ID.fullmatch(self.id):
            raise SourceError(self.relative+': invalid document id')
        self.kind = self.meta.get('kind')
        if not isinstance(self.kind,str) or not self.kind:
            raise SourceError(self.relative+': kind is required')
        self.body = self.text[self.header_end:]
        self.clean = MARKER.sub(lambda m:m[2], self.body).strip()
        self.sha = digest(self.bytes)
        self.blocks = {}
        self.spans = {}
        last = 0
        for match in MARKER.finditer(self.body):
            ident = match[1]
            if ident in self.blocks:
                raise SourceError(self.relative+': duplicate block '+ident)
            if self.body[last:match.start()].strip():
                raise SourceError(self.relative+': unanchored prose before '+ident)
            self.blocks[ident] = match[2]
            self.spans[ident] = (self.header_end+match.start(2),self.header_end+match.end(2))
            last = match.end()
        if self.body[last:].strip():
            raise SourceError(self.relative+': unanchored content; run md_source.py stamp')
        # Frontmatter values are distinct selectable source spans, not inferred text matches.
        node = yaml.compose(self.header, Loader=UniqueLoader)
        for key, value in node.value:
            if key.value in ('title','subtitle','duration_seconds','order'):
                ident = '@'+key.value
                a,b = 4+value.start_mark.index,4+value.end_mark.index
                self.blocks[ident] = self.text[a:b]
                self.spans[ident] = (a,b)

    def target(self, block):
        if block == '@document':
            a,b = 0,len(self.text)
        else:
            a,b = self.spans[block]
        raw = self.text[a:b]
        return {'key':self.id+'::'+block, 'document_id':self.id,'block_id':block,
                'source_path':self.relative,'file_sha256':self.sha,'block_sha256':digest(raw),
                'start_byte':len(self.text[:a].encode('utf-8')),'end_byte':len(self.text[:b].encode('utf-8')),
                'start_line':self.text.count('\n',0,a)+1,'end_line':self.text.count('\n',0,max(a,b-1))+1,
                'offset_encoding':'utf-8','end_exclusive':True,'markdown':raw,
                'kind':self.kind,'title':self.meta.get('title',self.id),
                'frozen':bool(self.meta.get('frozen',False))}

@lru_cache(maxsize=1)
def documents():
    result = {}
    for path in sorted(CONTENT.rglob('*.md')):
        doc = Document(path)
        if doc.id in result:
            raise SourceError('Duplicate document id: '+doc.id)
        result[doc.id] = doc
    if not result:
        raise SourceError('No Markdown sources found in content/')
    return result

def refresh():
    documents.cache_clear()
    structures.cache_clear()
    decks.cache_clear()
    diagram_definitions.cache_clear()
    body_lookup.cache_clear()


def by_kind(kind, product=None):
    return sorted((d for d in documents().values() if d.kind==kind and (product is None or d.meta.get('product')==product)),
                  key=lambda d:(d.meta.get('order',0),d.id))

def decode(value, owner):
    if isinstance(value,dict):
        if set(value)=={'__md_block__'}:
            ident=value['__md_block__']
            if ident not in owner.blocks:
                raise SourceError(owner.relative+': unresolved block '+ident)
            return owner.blocks[ident]
        if set(value)=={'__md_document__'}:
            ident=value['__md_document__']
            if ident not in documents():
                raise SourceError(owner.relative+': unresolved document '+ident)
            doc=documents()[ident]
            return decode(doc.meta['data'],doc)
        return {k:decode(v,owner) for k,v in value.items()}
    if isinstance(value,list):
        return [decode(v,owner) for v in value]
    return value

def registry(name):
    doc=documents()['registry-'+name]
    return decode(doc.meta['data'],doc)

@lru_cache(maxsize=1)
def structures():
    config=documents()['compiler-settings'].meta
    chapters={}
    for book in by_kind('guide'):
        p=book.meta['product'];chapters[p]=[]
        for ch in by_kind('chapter',p):
            sections=[d.id for d in by_kind('section',p) if d.meta['chapter']==ch.id]
            chapters[p].append({'slug':ch.meta['slug'],'title':ch.meta['title'],'purpose':ch.clean,
                               'sections':sections,**({'appendix':True} if ch.meta.get('appendix') else {})})
    return {'chapters':chapters,'types':config['types'],'labels':config['labels'],
            'baseline':config['baseline'],'revision':config['revision']}


def strip_markers(value):
    return MARKER.sub(lambda m:m[2],value).strip()


def table_rows(markdown):
    rows=[];row=None
    for token in MD.parse(markdown):
        if token.type=='tr_open':row=[]
        elif token.type=='inline' and row is not None:row.append(html.unescape(token.content).replace('\\|','|').replace('<br>','\n'))
        elif token.type=='tr_close':rows.append(row);row=None
    return rows

@lru_cache(maxsize=1)
def decks():
    result={}
    for deck in by_kind('deck'):
        p=deck.meta['product'];slides=[];groups=[]
        for d in by_kind('slide',p):
            meta=d.meta
            content=d.blocks.get('slide-content','')
            notes=d.blocks.get('speaker-notes','')
            # Layout is metadata; the actual slide and its notes are Markdown.
            kind=meta['layout']
            if kind in ('table','demo'):
                data=table_rows(content)
                if kind=='demo':data=data[1:]
            elif kind in ('columns','flow'):
                parts=re.split(r'^### (.+)\n',content,flags=re.M)
                data=[[parts[i],parts[i+1].strip()] for i in range(1,len(parts),2)]
            else:data=[]
            s={k:v for k,v in meta.items() if k not in ('id','kind','product','order','chapter','layout','duration_seconds','frozen')}
            s.update({'kind':kind,'seconds':meta['duration_seconds'],'data':data,'message':notes,
                      '_source_id':d.id,'_markdown':content})
            if 'reading-steps' in d.blocks:
                s['explain']=[t.content for t in MD.parse(d.blocks['reading-steps']) if t.type=='inline']
            if kind=='diagram':
                match=re.search(r'\]\([^)]*/([^/)]+)\.svg\)',content)
                if not match:raise SourceError(d.relative+': diagram slide must link a diagram SVG')
                s['diagram']=match[1]
            chapter=meta['chapter']
            if not groups or groups[-1][0]!=chapter:groups.append((chapter,[]))
            groups[-1][1].append(len(slides));slides.append(s)
        result[p]={'title':deck.meta['title'],'subtitle':deck.meta.get('subtitle',''),
                   'prefix':deck.meta['prefix'],'slides':slides,'_groups':groups}
    return result


def diagram_definitions():
    result={}
    for d in by_kind('diagram'):
        result[d.id]=(d.meta['title'],d.blocks.get('description',''),d.meta.get('refs',[]),d.blocks['definition'])
    return result


def build_diagrams():
    from xml.etree import ElementTree as ET
    out=ROOT/'assets/diagrams';out.mkdir(parents=True,exist_ok=True)
    for d in by_kind('diagram'):
        raw=d.blocks['definition']
        match=re.fullmatch(r'```(svg|dot)\n(.*)\n```',raw,re.S)
        if not match:raise SourceError(d.relative+': expected fenced svg or dot definition')
        language,payload=match.groups()
        if language=='dot':
            payload=subprocess.run(['dot','-Tsvg'],input=payload,text=True,capture_output=True,check=True).stdout
        node=ET.fromstring(payload)
        if node.tag.split('}')[-1]!='svg':raise SourceError('Diagram must produce SVG')
        for element in node.iter():
            if element.tag.split('}')[-1].lower() in ('script','foreignobject'):
                raise SourceError('Executable SVG content is not allowed')
            for key,value in element.attrib.items():
                if key.lower().startswith('on') or (key.split('}')[-1] in ('href','src') and not value.startswith('#')):
                    raise SourceError('External or executable SVG reference is not allowed')
        (out/(d.id+'.svg')).write_text(payload,encoding='utf-8')
    return len(by_kind('diagram'))


def assembled_guides():
    result={}
    for book in by_kind('guide'):
        p=book.meta['product'];parts=[book.clean]
        for ch in by_kind('chapter',p):
            parts += ['## '+f'{ch.meta["order"]:02d}'+'. '+ch.meta['title'],ch.clean]
            for sec in by_kind('section',p):
                if sec.meta['chapter']==ch.id:
                    parts += ['### '+sec.id+' — '+sec.meta['title'],sec.clean]
        refs=by_kind('references',p)
        parts += [d.clean for d in refs]
        result[p]='\n\n'.join(parts).rstrip()+'\n'
    return result


def assemble():
    """Emit compatibility projections. No JSON or Python definition is an input."""
    for name in REGISTRIES:
        d=documents()['registry-'+name]
        fmt=d.meta['json_format'];params={k:v for k,v in fmt.items() if k!='newline'}
        if 'separators' in params:params['separators']=tuple(params['separators'])
        raw=json.dumps(registry(name),**params)+('\n' if fmt.get('newline') else '')
        (ROOT/f'catalog/{name}.json').write_text(raw,encoding='utf-8')
    for p,text in assembled_guides().items():
        (ROOT/f'guides/{p}.md').write_text(text,encoding='utf-8')
    for doc in by_kind('page'):
        path=doc.meta['output']
        if Path(path).is_absolute() or '..' in Path(path).parts:raise SourceError('Invalid page output')
        (ROOT/path).write_text(doc.clean.rstrip()+'\n',encoding='utf-8')

@lru_cache(maxsize=1)
def body_lookup():
    result=defaultdict(list)
    for d in documents().values():
        if d.kind in ('section','guide','chapter','page'):
            result[d.clean].append(d)
    return result


def render_fragment(text,definitions,links,prefix,legacy):
    candidates=body_lookup().get(text.strip(),[])
    if not candidates:
        return legacy(text,definitions,links,prefix)
    d=next((x for x in candidates if x.id in prefix),candidates[0])
    chunks=[]
    for i,(bid,raw) in enumerate(d.blocks.items()):
        if bid.startswith('@'):continue
        rendered=legacy(raw,definitions,links,prefix+'-b'+str(i))
        chunks.append('<div class="source-block" data-source-key="'+html.escape(d.id+'::'+bid,quote=True)+'">'+rendered+'</div>')
    return '\n'.join(chunks)


def source_revision():
    files={d.relative:d.sha for d in documents().values()}
    revision=digest(json.dumps(files,sort_keys=True,separators=(',',':')))
    try:
        commit=subprocess.check_output(['git','log','-1','--format=%H','--','content'],cwd=ROOT,text=True).strip() or None
        dirty=bool(subprocess.check_output(['git','status','--porcelain','--','content'],cwd=ROOT,text=True).strip())
    except subprocess.CalledProcessError:commit=None;dirty=True
    return {'content_sha256':revision,'source_commit':commit,'uncommitted_sources':dirty}


def stamp_text(text, prefix='b'):
    """Assign persisted IDs once, without rewriting authored Markdown content."""
    if '<!-- block:' in text:return text
    lines=text.splitlines(keepends=True);ranges=[];end=0
    for t in MD.parse(text):
        if t.map and t.level==0 and t.map[0]>=end:
            a,b=t.map
            if a>end and ''.join(lines[end:a]).strip():ranges.append((end,a))
            ranges.append((a,b));end=b
    if ''.join(lines[end:]).strip():ranges.append((end,len(lines)))
    if not ranges and text.strip():ranges=[(0,len(lines))]
    chunks=[]
    for i,(a,b) in enumerate(ranges,1):
        raw=''.join(lines[a:b]).rstrip('\n')
        ident=prefix+'-'+f'{i:04d}'+'-'+digest(raw)[:8]
        chunks.append('<!-- block: '+ident+' -->\n'+raw+'\n<!-- /block -->')
    return '\n\n'.join(chunks)+'\n' if chunks else ''


def stamp(path):
    p=safe_path(path);text=p.read_text();end=text.find('\n---\n',4)+5
    if not text.startswith('---\n') or end<5:raise SourceError('Frontmatter required')
    if '<!-- block:' in text[end:]:raise SourceError('Already anchored. Add new named blocks explicitly; existing IDs must not be reassigned.')
    p.write_text(text[:end]+stamp_text(text[end:]))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    s=sub.add_parser('stamp');s.add_argument('source')
    sub.add_parser('validate')
    args=parser.parse_args()
    if args.command=='stamp':stamp(args.source)
    else:print(json.dumps({'documents':len(documents()),'revision':source_revision()},indent=2))
