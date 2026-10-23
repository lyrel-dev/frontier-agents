#!/usr/bin/env python3
"""One-time, verified source-format migration. Removed after successful publication."""
from __future__ import annotations
import ast
import copy
import hashlib
import json
import re
from pathlib import Path
import yaml
import md_source as md

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
BASE='4a34aaadc5f9fd0e4dbb492c36aa152730c8ba5a'
REV='2026-10-23-markdown-review'

def write_doc(path,meta,body=''):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text('---\n'+yaml.safe_dump(meta,sort_keys=False,allow_unicode=True,width=110)+'---\n'+body.rstrip()+'\n')

def block(ident,raw):return '<!-- block: '+ident+' -->\n'+str(raw)+'\n<!-- /block -->\n'

def dump_format(raw,data):
    for indent in (2,4,None):
        for ascii_mode in (False,True):
            for sort in (False,True):
                for newline in (True,False):
                    fmt={'indent':indent,'ensure_ascii':ascii_mode,'sort_keys':sort}
                    if json.dumps(data,**fmt)+('\n' if newline else '')==raw:return {**fmt,'newline':newline}
    raise RuntimeError('Unrecognized JSON serialization; do not change frozen projection bytes')

def md_table(rows):
    def cell(v):return str(v).replace('|','&#124;').replace('\n','<br>')
    return '\n'.join(['| '+' | '.join(map(cell,rows[0]))+' |','| '+' | '.join('---' for _ in rows[0])+' |']+['| '+' | '.join(map(cell,r))+' |' for r in rows[1:]])

def patch_method(path,classname,name,replacement):
    text=path.read_text();tree=ast.parse(text)
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==classname)
    f=next(n for n in cls.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name==name)
    lines=text.splitlines(True);lines[f.lineno-1:f.end_lineno]=[replacement.rstrip()+'\n'];path.write_text(''.join(lines))

if (ROOT/'content/compiler-settings.md').exists():
    raise SystemExit('Migration already applied; remove this temporary script rather than replay it')

# Import the existing authoring data before replacing the data modules with adapters.
import build as old
import structure
import presentation
import diagrams
import teaching_diagrams
import reader
old_guides=copy.deepcopy(old.load_guides())
old_chapters=copy.deepcopy(structure.CHAPTERS)
old_decks=copy.deepcopy(presentation.DECKS)
old_groups=copy.deepcopy(structure.DECK_CHAPTERS)
old_registers={n:(ROOT/f'catalog/{n}.json').read_text() for n in md.REGISTRIES}
old_diagrams=copy.deepcopy(diagrams.DIAGRAMS)

write_doc('content/compiler-settings.md',{'id':'compiler-settings','kind':'compiler-settings','title':'Documentation compiler configuration',
    'revision':REV,'baseline':structure.BASELINE,'types':structure.TYPES,'labels':structure.LABELS,
    'frozen_baseline':BASE})
write_doc('content/site-settings.md',{'id':'site-settings','kind':'site-settings','title':'Collection navigation','names':reader.NAMES})
write_doc('content/diagram-layout.md',{'id':'diagram-layout','kind':'diagram-layout','title':'Teaching diagram coordinates','boxes':teaching_diagrams.BOXES})

for product,g in old_guides.items():
    write_doc(f'content/guides/{product}/_book.md',{'id':'guide-'+product,'kind':'guide','product':product,'title':reader.NAMES[product]},md.stamp_text(g['intro']))
    write_doc(f'content/guides/{product}/_references.md',{'id':'references-'+product,'kind':'references','product':product,'title':'Official references — '+reader.NAMES[product]},block('references',g['definitions']))
    for i,ch in enumerate(old_chapters[product],1):
        cid='chapter-'+product+'-'+ch['slug']
        extra={k:v for k,v in ch.items() if k not in ('slug','title','purpose','sections')}
        write_doc(f'content/guides/{product}/chapters/{i:02d}-{ch["slug"]}.md',{'id':cid,'kind':'chapter','product':product,'order':i,'slug':ch['slug'],'title':ch['title'],**extra},block('purpose',ch['purpose']))
        for j,sid in enumerate(ch['sections'],1):
            sec=g['sections'][sid]
            write_doc(f'content/guides/{product}/sections/{sid}.md',{'id':sid,'kind':'section','product':product,'chapter':cid,'order':j,'title':sec['title']},md.stamp_text(sec['body']))

for product,deck in old_decks.items():
    write_doc(f'content/presentations/{product}/_deck.md',{'id':'deck-'+product,'kind':'deck','product':product,
        **{k:v for k,v in deck.items() if k!='slides'}})
    group_by={idx:title for title,indices in old_groups[product] for idx in indices}
    for i,s in enumerate(deck['slides'],1):
        meta={k:v for k,v in s.items() if k not in ('title','kind','seconds','data','message','explain','diagram')}
        kind=s['kind']
        if kind=='diagram':body='!['+old_diagrams[s['diagram']][0]+'](../assets/diagrams/'+s['diagram']+'.svg)'
        elif kind in ('table','demo'):
            rows=s['data'] if kind=='table' else [['Time','Action','Prepared evidence'],*s['data']]
            body=md_table(rows)
        else:body='\n\n'.join('### '+str(a)+'\n\n'+str(b) for a,b in s['data'])
        chunks=block('slide-content',body)
        if s.get('explain'):chunks+='\n'+block('reading-steps','\n'.join(str(j)+'. '+text for j,text in enumerate(s['explain'],1)))
        chunks+='\n'+block('speaker-notes',s['message'])
        write_doc(f'content/presentations/{product}/{i:02d}.md',{'id':'slide-'+product+'-'+f'{i:02d}','kind':'slide','product':product,
            'title':s['title'],'order':i,'chapter':group_by[i-1],'duration_seconds':s['seconds'],'layout':kind,**meta},chunks)

# Each frozen register record has one Markdown source; prose leaves are anchored
# Markdown body fields, while identity and relationship structure remain YAML.
for registry,raw in old_registers.items():
    data=json.loads(raw);created=set()
    def save_record(value,record_id,product=None,index=False):
        doc_id='registry-'+registry if index else registry+'--'+record_id
        if doc_id in created:raise RuntimeError('Duplicate record identity '+doc_id)
        created.add(doc_id);chunks=[];counter=[0]
        title=value.get('title',value.get('name',record_id)) if isinstance(value,dict) else record_id
        if not isinstance(title,str):title=record_id
        def convert(item,trail=(),root=False,p=product):
            if isinstance(item,dict):
                if not root and isinstance(item.get('id'),str):
                    child_id=item['id'];save_record(item,child_id,item.get('platform',p),False)
                    return {'__md_document__':registry+'--'+child_id}
                out={}
                for k,v in item.items():
                    np=k if trail and trail[-1]=='products' and k in ('devops','security','finops') else p
                    if root and k=='title' and v==title:out[k]={'__md_frontmatter__':'title'}
                    else:out[k]=convert(v,trail+(k,),False,np)
                return out
            if isinstance(item,list):return [convert(v,trail+(str(i),),False,p) for i,v in enumerate(item)]
            if isinstance(item,str) and not item.startswith(('https://','http://')) and ('\n' in item or len(item)>55 or (len(item)>20 and ' ' in item)):
                counter[0]+=1;bid='field-'+str(counter[0]).zfill(4)
                heading=' / '.join(trail)
                chunks.append(block('label-'+str(counter[0]).zfill(4),'## '+heading))
                chunks.append(block(bid,item));return {'__md_block__':bid}
            return item
        converted=convert(value,root=True)
        meta={'id':doc_id,'kind':'registry' if index else 'record','registry':registry,'record_id':record_id,
              'title':title,'frozen':True}
        if product:meta['product']=product
        if index:meta['json_format']=dump_format(raw,data)
        meta['data']=converted
        filename='_index' if index else record_id.replace(':','-')
        write_doc(f'content/catalog/{registry}/{filename}.md',meta,'\n'.join(chunks))
    save_record(data,registry,index=True)

# SVG is editable, fenced source in Markdown. It is not an opaque binary or an archive.
for key,(title,description,refs,_) in old_diagrams.items():
    path=ROOT/f'assets/diagrams/{key}.svg'
    write_doc(f'content/diagrams/{key}.md',{'id':key,'kind':'diagram','title':title,'refs':refs},
              block('description',description)+'\n'+block('definition','```svg\n'+path.read_text().rstrip('\n')+'\n```'))

# Correct the source loader to support scalar metadata bindings and cache clearing.
p=HERE/'md_source.py';text=p.read_text()
text=text.replace("    diagram_definitions.cache_clear()\n",'')
text=text.replace("    if isinstance(value,dict):\n", "    if isinstance(value,dict):\n        if set(value)=={'__md_frontmatter__'}:\n            return owner.meta[value['__md_frontmatter__']]\n",1)
p.write_text(text);import importlib;md=importlib.reload(md)

# Replace content-bearing Python modules with small compiler adapters.
(HERE/'structure.py').write_text('''"""Chapter membership and labels compiled from frontmatter Markdown."""
from md_source import structures, decks
_data=structures()
REVISION=_data['revision']
BASELINE=_data['baseline']
CHAPTERS=_data['chapters']
TYPES=_data['types']
LABELS=_data['labels']
DECK_CHAPTERS={p:d['_groups'] for p,d in decks().items()}
def section_type(sid):
    return 'example' if '-U' in sid else 'mechanism' if '-M' in sid else TYPES[sid]
''')
(HERE/'presentation.py').write_text('''"""Presentation content is authored in content/presentations/**/*.md."""
from md_source import decks
DECKS=decks()
''')
(HERE/'diagrams.py').write_text('''"""Diagram definitions are fenced SVG or DOT in frontmatter Markdown."""
from md_source import ROOT, diagram_definitions, build_diagrams
DIAGRAMS=diagram_definitions()
def build():
    return build_diagrams()
if __name__=='__main__':
    print(build())
''')
(HERE/'teaching_diagrams.py').write_text('''"""Compatibility for geometry checks; no authored diagram labels live in Python."""
from md_source import documents, diagram_definitions
BOXES=documents()['diagram-layout'].meta['boxes']
PRODUCTS={}
DIAGRAMS={k:v for k,v in diagram_definitions().items() if k.startswith('teaching-')}
''')
(HERE/'mechanism_figures.py').unlink(missing_ok=True)
# Resource rendering consumes the Markdown register rather than a JSON authoring file.
p=HERE/'resource_model.py';s=p.read_text().replace('    return json.loads(SOURCE.read_text(encoding=\'utf-8\'))','    from md_source import registry\n    return registry(\'resource-models\')')
a=s.index('def diagram_definitions():');b=s.index('\n\nCSS =',a)
s=s[:a]+"def diagram_definitions():\n    from md_source import diagram_definitions as definitions\n    return {k:v for k,v in definitions().items() if k.startswith('er-')}\n"+s[b:]
p.write_text(s)

# Render from the same assembled data model, preserving established URLs and controls.
p=HERE/'build.py';s=p.read_text()
s=s.replace('import mechanism_detail','import mechanism_detail\nimport md_source\nimport review_build')
s=s.replace('def render_markdown(text,definitions,links,prefix):','def _render_unmapped(text,definitions,links,prefix):',1)
where=s.index('\ndef links_for(')
s=s[:where]+'''\ndef render_markdown(text,definitions,links,prefix):
    return md_source.render_fragment(text,definitions,links,prefix,_render_unmapped)

'''+s[where:]
s=s.replace('def slide_body(s,prefix):','''def slide_body(s,prefix):
    if s.get('_source_id') and s['kind'] != 'diagram':
        content=_render_unmapped(s['_markdown'],'',{},prefix)
        if s['kind'] in ('columns','flow'):
            soup=BeautifulSoup(content,'html.parser');groups=[]
            for heading in list(soup.find_all('h3',recursive=False)):
                unit=soup.new_tag('section',attrs={'class':'content-unit'})
                following=[]
                for node in heading.next_siblings:
                    if getattr(node,'name',None)=='h3': break
                    following.append(node)
                heading.name='h2';unit.append(heading.extract())
                for node in following: unit.append(node.extract())
                groups.append(str(unit))
            content='<div class="'+('flow' if s['kind']=='flow' else 'columns')+'">'+''.join(groups)+'</div>'
        return content
''',1)
s=s.replace("    build_diagrams();guides=load_guides();catalog=load_catalog()", "    md_source.assemble()\n    build_diagrams();guides=load_guides();catalog=load_catalog()")
s=s.replace("    reader.render(guides,render_markdown,write)","    reader.render(guides,render_markdown,write)\n    md_source.assemble()\n    author=md_source.documents()['authoring']\n    write('authoring.html',reader.Reader(guides,render_markdown,write).page('Authoring and source review','<main id=\"main\" class=\"directory-main\">'+render_markdown(author.clean,'',{},'authoring')+'</main>','authoring.html','guides','authoring'))\n    review_build.build()")
s=s.replace("allowed={'guides'", "allowed={'content','guides'")
s=s.replace("'index.html','documentation-build.json'}", "'index.html','authoring.html','AUTHORING.md','documentation-build.json'}")
# Generated contributor docs are sourced from Markdown, not Python string literals.
s=re.sub(r"^    write\('PUBLISHING.md',.*\)\n",'',s,flags=re.M)
p.write_text(s)
patch_method(HERE/'reader.py','Reader','readme', '''    def readme(self):
        from md_source import documents
        self.write('README.md', documents()['page-readme'].clean)
''')

# Authoring documentation is part of the same searchable, selectable source collection.
authoring='''# Authoring, search, and source review

## Source layout

All maintained documentation content is authored under `content/` in UTF-8 Markdown with a YAML header. Guides, chapter introductions, slide content, speaker notes, approved catalog records, diagrams, and contributor documents use the same source loader. Files under `guides/`, `presentations/`, `catalog/`, and `assets/` are compiled projections; do not edit them directly.

A guide section is one file. Its header contains `id`, `kind: section`, `product`, `chapter`, `order`, and `title`. The chapter value references a chapter document. A slide file has `kind: slide`, `product`, `order`, `chapter`, `title`, `duration_seconds`, `layout`, and guide `refs`. Its body holds the slide's Markdown, reading steps where applicable, and speaker notes. Duration includes the exercise when the layout is `demo`.

The approved entity model and use-case semantics are unchanged. Complex reference records retain their identities and relationships as YAML; longer prose is held in named Markdown body blocks. The YAML references those blocks rather than duplicating their text. Generated registry JSON is an interchange projection, not a second authoring source.

## Block identities

Every editable body block has explicit, persistent comment markers. For example:

    <!-- block: explanation-01 -->
    The paragraph being explained and reviewed.
    <!-- /block -->

Keep the document ID and block ID when editing text. Moving or reordering a block does not require changing its ID. New blocks need new IDs; copied blocks must not retain an existing ID in the same file. The build rejects duplicate document IDs, duplicate block IDs, duplicate YAML keys, and unanchored prose. For a new, entirely unanchored file, run `python tools/docs/md_source.py stamp content/path/to/file.md` once. The compiler itself never inserts IDs or rewrites source files.

A whole table, code fence, or diagram definition can be one block. A selected phrase within that block is retained as a rendered quotation, but the exact Markdown block remains the editing boundary. This prevents an HTML character offset from being mistaken for a source position.

## Build and validate

Install `tools/docs/requirements.txt`, then run:

    python tools/docs/build.py
    python tools/docs/check.py --browser
    python tools/docs/md_check.py --browser

Use `python -m http.server 8000 --bind 127.0.0.1` from the repository root for review across pages. Open the local collection in a browser. Reading and search also work from file URLs; browser storage isolation for file URLs varies, so use export/import to transfer notes when not serving the collection. No external server or API account is required.

The existing guide, use-case, resource-model, and presentation URLs are retained. Timings, workflow groupings, and the approved records are not redefined by this source-format migration. JSON, SVG, HTML, search data, and source maps are generated from Markdown.

## Search the collection

Choose **Search all**, or press **Ctrl/Cmd+K**. Search includes guide explanations, slide content, use-case articles, and resource definitions. Filter by content type; quoted phrases are supported. Results link to the containing chapter or slide and the exact rendered block. Each guide retains its existing local search.

## Select content and annotate

Choose **Review** to display block handles. Click a handle to select a block; Shift-click extends a range; Ctrl/Cmd-click toggles additional blocks. Drag across handles to select a contiguous range. Shift with the up/down arrow extends keyboard selection, and Ctrl/Cmd+A selects visible blocks while review mode is active and focus is outside a text field. Ordinary text selection retains an excerpt and its surrounding text. **Select section / slide** and **Select document** target larger source units.

These are independently implemented, read-only, Notion-style selection interactions. This is not the Tiptap commercial Notion template, a WYSIWYG document editor, drag-to-reorder authoring, or a collaborative editor. Rendered content cannot be edited in the browser. Tiptap's published template requires a production subscription; no license-dependent code is bundled here.

A note records context; a comment requests or discusses a change. Both can have replies, be edited, resolved, reopened, and exported. Storage is local to the browser and origin, not GitHub. A storage failure is reported and export remains available. Imports preserve conflicting review entries rather than silently overwriting them. There is no server-side multiuser synchronization or authentication service.

## Export a review for an LLM

**Export JSON** creates `frontier.review.v1`: comments, statuses, replies, source IDs, exact Markdown snapshots, file and block SHA-256 hashes, source revision, byte ranges, line numbers, and optional rendered quotations. **Export LLM request** produces a Markdown instruction packet with the same review bundle. **Copy LLM request** places it on the clipboard when permitted. Neither action sends data to an external service. Review the packet before submitting it to an LLM; selected text and whole-document selections can include substantial source content.

The editing LLM must return `frontier.patch.v1`. Every edit identifies one open comment and an explicitly selected source document/block, supplies both expected hashes and exact old text, and replaces only that source span. Rendered text selectors express the reviewer's intent; they are never used as source byte offsets. Line numbers are navigation aids. UTF-8 byte offsets are zero-based with an exclusive end.

## Apply proposed source edits

First inspect a dry-run diff:

    python tools/docs/review_patch.py documentation-review.json proposed-edits.json

Only after reviewing it, write the validated changes:

    python tools/docs/review_patch.py documentation-review.json proposed-edits.json --write

The patch tool accepts only `content/**/*.md`, rejects stale or altered snapshots, unknown IDs, edits outside the selected span, overlapping edits, generated-file destinations, symlinks, and path traversal. It checks every edit before writing any file. It preserves document identity and existing block IDs. Frozen reference definitions cannot be changed through this tool without a separate approved policy change. Rebuild, run validation, review the rendered result and Git diff, then commit the source changes and regenerated outputs.

When source changes invalidate a comment's snapshot, the UI marks it stale. It does not silently search for similar text and claim a match. Export preserves the original reviewed snapshot; obtain a current selection before applying a replacement. Comments are review data, not instructions to bypass source policy or edit unselected files.

## Technical references

- [Obsidian properties and YAML frontmatter](https://help.obsidian.md/properties)
- [Tiptap Notion-like template and license requirements](https://tiptap.dev/docs/ui-components/templates/notion-like-editor)
- [Tiptap stable node identities](https://tiptap.dev/docs/editor/extensions/functionality/uniqueid)
- [W3C Web Annotation selectors](https://www.w3.org/TR/annotation-model/)

The review schema uses explicit source selectors and a rendered TextQuoteSelector-inspired field. It is a repository-specific interchange format, not a claim of complete W3C JSON-LD conformance.
'''
write_doc('content/authoring/authoring.md',{'id':'authoring','kind':'page','title':'Authoring and source review','output':'AUTHORING.md'},md.stamp_text(authoring))
readme=(ROOT/'README.md').read_text()
readme=readme.replace('## Source ownership and build', '## Markdown sources and review\n\nAuthor documentation in `content/**/*.md`. The compiler preserves the existing HTML routes and generates local search and source-aware review controls. Read [Authoring and source review](AUTHORING.md) for file schemas, selection, comment export, and guarded LLM patch application.\n\n## Source ownership and build')
a=readme.index('The six JSON registers');b=readme.index('```text',a)
readme=readme[:a]+'The approved records are frozen semantically. Their canonical source is now Markdown with YAML frontmatter. The JSON files are generated interchange projections and remain identical to the approved baseline. Guide and slide prose, speaker notes, and diagram definitions are authored in Markdown. The renderer does not introduce a new product taxonomy.\n\n'+readme[b:]
readme=readme.replace('guides/          Canonical guide prose and HTML books','content/         Canonical Markdown with YAML frontmatter\nguides/          Compiled Markdown and HTML books').replace('catalog/         Frozen records, use-case pages, and resource reference','catalog/         Compiled frozen records, use cases, and resource reference').replace('python tools/docs/check.py --browser','python tools/docs/check.py --browser\npython tools/docs/md_check.py --browser')
write_doc('content/authoring/readme.md',{'id':'page-readme','kind':'page','title':'Repository README','output':'README.md'},md.stamp_text(readme))
publishing='''# Publishing documentation

Canonical documentation sources are frontmatter Markdown under `content/`. Edit those files, not compiled guide Markdown, HTML, registry JSON, search data, source maps, or SVG output. The approved use-case and entity-model definitions remain frozen. Their projections must match the approved baseline.

Run `python tools/docs/build.py`, `python tools/docs/check.py --browser`, and `python tools/docs/md_check.py --browser`. Review source changes and generated output. The publication workflow runs for Markdown and compiler changes as well as explicit build requests. It validates before committing each generated document separately.

Review comments are local user data. Export them deliberately, inspect the LLM request, and validate proposed source-only edits with `review_patch.py` before writing. No review action automatically calls an LLM, publishes comments, or commits source changes.

Keep the independent application unchanged. Git retains prior versions; do not maintain manual archives or duplicate guide editions. Publishing files to the repository does not by itself deploy a website. See [AUTHORING.md](AUTHORING.md) for the authoring and review contract.
'''
write_doc('content/authoring/publishing.md',{'id':'page-publishing','kind':'page','title':'Publishing documentation','output':'PUBLISHING.md'},md.stamp_text(publishing))
# Existing contributor/editorial documents are preserved as Markdown sources too.
for name in ('EDITORIAL_STANDARD.md','CHANGELOG.md','SCOPE.md','VALIDATION.md'):
    if (ROOT/name).exists():
        write_doc('content/authoring/'+name.lower(),{'id':'page-'+name[:-3].lower().replace('_','-'),'kind':'page','title':name[:-3].replace('_',' ').title(),'output':name},md.stamp_text((ROOT/name).read_text()))
md.refresh()

# Semantic preservation is tested before any publication: the compiler roundtrips every register.
checks={}
for name,raw in old_registers.items():
    doc=md.documents()['registry-'+name];fmt=doc.meta['json_format'];params={k:v for k,v in fmt.items() if k!='newline'}
    rendered=json.dumps(md.registry(name),**params)+('\n' if fmt['newline'] else '')
    if rendered!=raw:raise RuntimeError('Frozen register did not roundtrip: '+name)
    checks[name]={'identical_projection':True,'sha256':md.digest(raw)}
for p,g in old_guides.items():
    new=old.parse_source(md.assembled_guides()[p])
    if new['sections']!=g['sections'] or new['intro']!=g['intro'] or new['refs']!=g['refs']:
        raise RuntimeError('Guide prose changed during migration: '+p)
for p,d in old_decks.items():
    new=md.decks()[p]
    for prior,current in zip(d['slides'],new['slides']):
        for key,value in prior.items():
            if current.get(key)!=value:raise RuntimeError('Slide roundtrip mismatch: '+p+' / '+prior['title']+' / '+key)
(ROOT/'qa/markdown-migration.json').write_text(json.dumps({'baseline':BASE,'frozen_projections':checks,
    'guide_prose_preserved':True,'slide_content_notes_timings_preserved':True,'source_documents':len(md.documents()),
    'source_policy':'Markdown is authoritative; compatibility outputs are generated; no new operational concepts or use cases.'},indent=2)+'\n')
# Add content to the manifest; generated JSON remains a deterministic interchange format.
p=HERE/'check.py';s=p.read_text().replace("roots=('guides'","roots=('content','guides'")
p.write_text(s)
md.assemble()
print('Markdown migration passed: '+str(len(md.documents()))+' source documents; approved content preserved.')
Path(__file__).unlink()
