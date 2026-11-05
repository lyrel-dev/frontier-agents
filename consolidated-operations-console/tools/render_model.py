#!/usr/bin/env python3
"""Synchronize schema text while preserving the editable Draw.io atlas layout.

model/schema.json owns entity/relationship contracts. diagrams/model.drawio owns
geometry and styling. The pinned official Draw.io engine renders SVGs; Inkscape
rasterizes those SVGs for visual inspection. --check is offline and does not write.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
from pathlib import Path
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
import zlib

ROOT=Path(__file__).resolve().parents[1]
SCHEMA=ROOT/'model/schema.json'
ATLAS=ROOT/'diagrams/model.drawio'
MANIFEST=ROOT/'diagrams/manifest.json'

def digest(data):return hashlib.sha256(data).hexdigest()
def typename(spec):
    if '$ref' in spec:return spec['$ref'].split('/')[-1]
    if 'oneOf' in spec:return ' | '.join(typename(x) for x in spec['oneOf'])
    if 'anyOf' in spec:return ' | '.join(typename(x) for x in spec['anyOf'])
    if 'allOf' in spec:return ' & '.join(typename(x) for x in spec['allOf'])
    if 'enum' in spec:return 'enum'
    if 'const' in spec:return str(spec['const'])
    if spec.get('type')=='array':return 'List['+typename(spec['items'])+']'
    return spec.get('type','JsonValue')

def display_type(spec):
    if '$ref' in spec:return spec['$ref'].split('/')[-1]
    if 'oneOf' in spec:return ' | '.join(display_type(x) for x in spec['oneOf'])
    if 'anyOf' in spec:
        nonnull=[x for x in spec['anyOf'] if x.get('type')!='null']
        return display_type(nonnull[0])+'?' if len(nonnull)==1 else ' | '.join(display_type(x) for x in spec['anyOf'])
    if 'allOf' in spec:return ' & '.join(display_type(x) for x in spec['allOf'])
    if 'enum' in spec:return 'Enum'
    if 'const' in spec:return str(spec['const'])
    if spec.get('type')=='array':return display_type(spec['items'])+'[]'
    return spec.get('type','JsonValue').capitalize()

def reference(schema):
    defs=schema['$defs'];entities=schema['x-entities'];contract=schema['x-versionContract']
    out=['# Entity and value reference','',
         'Generated from [schema.json](schema.json). Edit the schema, then run `python tools/render_model.py` from this package. The editable layout is [model.drawio](../diagrams/model.drawio); generation preserves its geometry and waypoints. [MODEL.md](../MODEL.md) defines the invariants and ownership rules that JSON Schema cannot express.','',
         f'The model contains **{len(entities)} entities**. Every entity carries `version`, `createdAt` and `updatedAt`. Every entity except Workspace also carries `workspaceId`. A stable entity identity and its retained versions belong to the same entity type.','',
         '## Common version contract','',
         '| Property | Contract |','| --- | --- |',
         f'| First version | `{contract["versionStart"]}` |',
         f'| Next version | Current version plus `{contract["increment"]}` |',
         f'| Writes | {contract["writeRule"]} |',
         f'| Exact historical reference | `{contract["exactReference"]}` |',
         f'| Live identity reference | `{contract["identityReference"]}` |',
         f'| Provider version | {contract["nativeVersion"]} |','',
         'Write authority determines who may append the next version. Sealing rules constrain an entity lifecycle; they do not create an exception to immutable retained versions. An entity remains versioned even when it is normally created once or has already reached a terminal state.','',
         '## Entity index','','| Module | Entity | Write authority | Identity |','| --- | --- | --- | --- |']
    for name in entities:
        d=defs[name];out.append(f'| {d["x-module"]} | [{name}](#{name.lower()}) | `{d["x-writeAuthority"]}` | `{d["x-identity"]}` |')
    out+=['','## Entities','']
    for name in entities:
        d=defs[name];out += [f'### {name}','',d['description'],'',
         f'**Owner:** {d["x-owner"]}. **Module:** {d["x-module"]}. **Identity:** `{d["x-identity"]}`.','',
         f'**Write authority:** `{d["x-writeAuthority"]}`. **Sealing rule:** {d["x-sealingRule"]}','',
         '| Field | Type | Required |','| --- | --- | --- |']
        for field,spec in d['properties'].items():out.append(f'| `{field}` | `{typename(spec).replace(" | "," or ")}` | {"Yes" if field in d.get("required",[]) else "No"} |')
        out.append('')
    out+=['## Owned values and scalar contracts','',
          'Owned values have no independent lifecycle or version stream. `EntityRef` is an exact reference value, not an entity. `EntityIdentity` explicitly means a live identity. A field carrying a historical input uses the exact reference contract.','',
          '| Shape | Meaning |','| --- | --- |']
    for name,d in defs.items():
        if name not in entities:out.append(f'| `{name}` | {d.get("description",typename(d)).replace("|","/")} |')
    out+=['','## Relationship register','',
          'All multiplicities describe the logical model; a partial cache can contain unresolved references. The [complete Draw.io atlas](../diagrams/model.drawio) distributes every association over readable detailed sheets. The [overview](../diagrams/complete-model.svg) contains all entities and a selected subset of associations.','',
          '| From | Cardinality | To | Cardinality | Meaning |','| --- | --- | --- | --- | --- |']
    for r in schema['x-relationships']:out.append(f'| {r["from"]} | {r["fromCardinality"]} | {r["to"]} | {r["toCardinality"]} | {r["label"]} |')
    return '\n'.join(out)+'\n'

def read_atlas():
    tree=ET.parse(ATLAS);root=tree.getroot()
    if root.tag!='mxfile':raise ValueError('Expected a native Draw.io mxfile.')
    for page in root.findall('diagram'):
        if page.find('mxGraphModel') is None:
            if not (page.text or '').strip():raise ValueError('Draw.io page is empty: '+page.get('id',''))
            decoded=urllib.parse.unquote(zlib.decompress(base64.b64decode(page.text),-15).decode())
            page.text=None;page.append(ET.fromstring(decoded))
    root.set('compressed','false')
    return root

def serialize(root):
    ET.indent(root,space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n'+ET.tostring(root,encoding='unicode')+'\n'

def synchronize(schema):
    root=read_atlas();root.set('schemaSha256',digest(SCHEMA.read_bytes()))
    for page in root.findall('diagram'):
        modelroot=page.find('./mxGraphModel/root')
        for obj in modelroot.findall('object'):
            name=obj.get('entity')
            if name:
                if name not in schema['x-entities']:raise ValueError('Unknown diagram entity '+name)
                spec=schema['$defs'][name];fields=obj.get('displayFields','').split(',')
                if 'version' not in fields:raise ValueError('Class omits version: '+name)
                if any(field not in spec['properties'] for field in fields):raise ValueError('Stale selected field on '+name)
                obj.set('label',name);obj.set('module',spec['x-module']);obj.set('tooltip',spec['description'])
                body=modelroot.find(f'./mxCell[@id="{obj.get("id")}-fields"]')
                if body is None:raise ValueError('Missing class attribute compartment for '+name)
                body_style=dict(part.split('=',1) for part in body.get('style','').split(';') if '=' in part)
                available=float(body.find('mxGeometry').get('width'))
                font_size=float(body_style.get('fontSize',13))
                limit=math.floor(available/(font_size*.62))
                lines=[]
                for field in fields:
                    field_type=display_type(spec['properties'][field]);line=f'{field}: {field_type}'
                    if len(line)<=limit:lines.append(line)
                    else:lines.extend([field+':','  '+field_type])
                body.set('value','\n'.join(lines))
            if obj.get('relationshipIndex') is not None:
                index=int(obj.get('relationshipIndex'));r=schema['x-relationships'][index]
                if (obj.get('fromEntity'),obj.get('toEntity'))!=(r['from'],r['to']):raise ValueError('Relationship index changed; review Draw.io layout: '+str(index))
                obj.set('label','' if obj.get('compact')=='1' else r['label'])
                obj.set('tooltip',f'{r["from"]} {r["fromCardinality"]} → {r["to"]} {r["toCardinality"]}: {r["label"]}')
                for suffix,key in [('from','fromCardinality'),('to','toCardinality')]:
                    label=modelroot.find(f'./mxCell[@id="{obj.get("id")}-{suffix}"]')
                    if label is None:raise ValueError('Missing relationship cardinality '+str(index))
                    label.set('value',r[key])
    return root

def inspect_atlas(root,schema):
    pages=[];primary_coverage=set();relationship_coverage=set()
    for page in root.findall('diagram'):
        modelroot=page.find('./mxGraphModel/root');model=page.find('mxGraphModel')
        objects=modelroot.findall('object');nodes=[o for o in objects if o.get('entity')]
        entities=[o.get('entity') for o in nodes]
        if len(entities)!=len(set(entities)):raise ValueError('Duplicate entity on page '+page.get('id'))
        declared=page.get('entities','').split(',')
        if declared!=entities:raise ValueError('Page entity metadata differs from actual cells')
        primary=[o.get('entity') for o in nodes if o.get('boundary')!='1']
        if set(primary)!=set(page.get('primaryEntities','').split(',')):raise ValueError('Primary entity metadata differs from actual cells')
        if page.get('kind')=='overview':
            if set(entities)!=set(schema['x-entities']):raise ValueError('Overview must show every entity')
        else:primary_coverage.update(primary)
        rel_ids=[]
        for obj in objects:
            if obj.get('relationshipIndex') is None:continue
            i=int(obj.get('relationshipIndex'));rel_ids.append(i);r=schema['x-relationships'][i]
            cell=obj.find('mxCell')
            if cell.get('source')!='class-'+r['from'] or cell.get('target')!='class-'+r['to']:raise ValueError('Wrong edge endpoint for relationship '+str(i))
            if r['from'] not in entities or r['to'] not in entities:raise ValueError('Missing edge endpoint class')
        if rel_ids!=[int(x) for x in page.get('relationshipIds','').split(',') if x]:raise ValueError('Page relationship metadata differs from actual cells')
        if page.get('kind')!='overview':relationship_coverage.update(rel_ids)
        pages.append({'id':page.get('id'),'title':page.get('name'),'kind':page.get('kind'),
                      'entities':entities,'primaryEntities':primary,'relationshipIds':rel_ids,
                      'pageSize':{'width':int(model.get('pageWidth')),'height':int(model.get('pageHeight'))}})
    if primary_coverage!=set(schema['x-entities']):raise ValueError('Detailed sheets do not cover all primary entities')
    if relationship_coverage!=set(range(len(schema['x-relationships']))):raise ValueError('Detailed sheets do not cover all relationships')
    return pages

def file_info(relative):
    p=ROOT/relative
    return {'path':relative,'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size}

def check(schema,root,pages):
    errors=[]
    expected_reference=reference(schema)
    if (ROOT/'model/REFERENCE.md').read_text()!=expected_reference:errors.append('Stale model/REFERENCE.md')
    if ATLAS.read_text()!=serialize(root):errors.append('Stale Draw.io schema text; run the generator')
    if not MANIFEST.exists():raise SystemExit('Missing Draw.io manifest')
    manifest=json.loads(MANIFEST.read_text())
    if manifest.get('format')!='drawio-atlas/1':errors.append('Unexpected diagram manifest format')
    if manifest.get('schemaSha256')!=digest(SCHEMA.read_bytes()):errors.append('Stale diagram schema provenance')
    if len(manifest.get('diagrams',[]))!=len(pages):errors.append('Diagram page count differs from atlas')
    for entry in [manifest.get('drawio',{}),manifest.get('reference',{}),manifest.get('renderReport',{})]:
        p=ROOT/entry.get('path','__missing__')
        if not p.is_file() or digest(p.read_bytes())!=entry.get('sha256'):errors.append('Stale/missing '+str(p.relative_to(ROOT)))
    for actual,expected in zip(manifest.get('diagrams',[]),pages):
        for key in ['id','title','kind','entities','primaryEntities','relationshipIds','pageSize']:
            if actual.get(key)!=expected[key]:errors.append('Stale page metadata: '+expected['id']+' '+key)
        for ext in ['svg','png']:
            info=actual.get(ext,{});p=ROOT/info.get('path','__missing__')
            if not p.is_file() or digest(p.read_bytes())!=info.get('sha256'):errors.append('Stale/missing '+str(p.relative_to(ROOT)))
    for suffix in ['*.mmd','*.dot']:
        if list((ROOT/'diagrams').glob(suffix)):errors.append('Superseded non-Draw.io source remains: '+suffix)
    report=json.loads((ROOT/'diagrams/render-report.json').read_text())
    for page in report['pages']:
        if page['classOverlaps'] or page['connectorIntrusions'] or page['labelIntrusions'] or page.get('textOverflows'):errors.append('Unresolved layout collision: '+page['id'])
        if not page.get('nativeCodecRoundTrip',{}).get('metadataPreserved'):errors.append('Missing native Draw.io codec verification: '+page['id'])
    if errors:raise SystemExit('\n'.join(errors))
    print(f'Draw.io atlas, {len(pages)} SVG/PNG exports and reference match; {len(schema["x-entities"])} entities and {len(schema["x-relationships"])} relationships covered.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--sync-only',action='store_true');args=ap.parse_args()
    schema=json.loads(SCHEMA.read_text());root=synchronize(schema);pages=inspect_atlas(root,schema)
    if args.check:return check(schema,root,pages)
    ATLAS.write_text(serialize(root));(ROOT/'model/REFERENCE.md').write_text(reference(schema))
    if args.sync_only:
        print('Synchronized schema text and reference; SVG/PNG regeneration still required.');return
    subprocess.run(['node',str(ROOT/'tools/render_drawio.mjs')],check=True)
    report=json.loads((ROOT/'diagrams/render-report.json').read_text())
    for page in pages:
        stem='diagrams/'+page['id']
        subprocess.run(['inkscape',str(ROOT/(stem+'.svg')),'--export-type=png','--export-filename='+str(ROOT/(stem+'.png'))],capture_output=True,text=True,check=True)
        page['svg']=file_info(stem+'.svg');page['png']=file_info(stem+'.png')
    manifest={'format':'drawio-atlas/1','schemaSha256':digest(SCHEMA.read_bytes()),
              'drawio':file_info('diagrams/model.drawio'),'reference':file_info('model/REFERENCE.md'),
              'renderer':report['renderer'],'rasterizer':subprocess.run(['inkscape','--version'],capture_output=True,text=True,check=True).stdout.strip(),
              'renderReport':file_info('diagrams/render-report.json'),
              'summary':{'entities':len(schema['x-entities']),'relationships':len(schema['x-relationships']),'pages':len(pages),
                         'allEntitiesOnOverview':True,'allEntitiesOnDetailedSheets':True,'allRelationshipsOnDetailedSheets':True},
              'diagrams':pages}
    MANIFEST.write_text(json.dumps(manifest,indent=2)+'\n')
    check(schema,root,pages)

if __name__=='__main__':main()
