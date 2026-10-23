#!/usr/bin/env python3
"""Validate LLM edits against an exported review. Dry run unless --write is given."""
from __future__ import annotations
import argparse
import difflib
import json
import os
from pathlib import Path
import tempfile
from md_source import Document, SourceError, ROOT, digest, safe_path

REPOSITORY='lyrel-dev/frontier-agents'


def read_json(path):
    p=Path(path)
    if p.stat().st_size>30*1024*1024:raise SourceError('Input exceeds 30 MB')
    return json.loads(p.read_text(encoding='utf-8'))


def plan(bundle,patch,root=ROOT):
    if bundle.get('schema')!='frontier.review.v1' or bundle.get('repository')!=REPOSITORY:
        raise SourceError('Wrong review schema or repository')
    if patch.get('schema')!='frontier.patch.v1' or patch.get('repository')!=REPOSITORY:
        raise SourceError('Wrong patch schema or repository')
    annotations={a['id']:a for a in bundle.get('annotations',[])}
    edits=patch.get('edits')
    if not isinstance(edits,list) or not edits or len(edits)>500:
        raise SourceError('Patch must contain 1–500 edits')
    grouped={};seen=set();documents={}
    required={'annotation_id','source_path','document_id','block_id','expected_file_sha256','expected_block_sha256','old_text','new_text'}
    for edit in edits:
        if not isinstance(edit,dict) or not required<=set(edit) or any(not isinstance(edit[k],str) for k in required):
            raise SourceError('Every edit must contain the documented string fields')
        annotation=annotations.get(edit['annotation_id'])
        if not annotation or annotation.get('status')!='open' or annotation.get('type')!='comment' or annotation.get('deleted'):
            raise SourceError('Edit is not linked to an open change-request comment')
        matches=[t for t in annotation.get('targets',[]) if t.get('source_path')==edit['source_path'] and t.get('document_id')==edit['document_id'] and t.get('block_id')==edit['block_id']]
        if len(matches)!=1:raise SourceError('Edit is outside the comment selection or ambiguous')
        selected=matches[0]
        path=safe_path(edit['source_path'],root)
        doc=documents.setdefault(path,Document(path,root))
        if doc.id!=edit['document_id']:raise SourceError('Document identity mismatch')
        if doc.meta.get('frozen'):
            raise SourceError('Frozen model/catalog definition requires separate explicit approval: '+doc.id)
        bid=edit['block_id']
        if bid!='@document' and bid not in doc.blocks:raise SourceError('Selected block no longer exists')
        current=doc.target(bid)
        for key in ('source_path','document_id','block_id','file_sha256','block_sha256','start_byte','end_byte','offset_encoding','end_exclusive'):
            if selected.get(key)!=current[key]:raise SourceError('Stale or altered review selector: '+key+' in '+doc.relative)
        if edit['expected_file_sha256']!=doc.sha or edit['expected_block_sha256']!=current['block_sha256']:
            raise SourceError('Expected hashes do not match the current source')
        if edit['old_text']!=current['markdown'] or selected.get('markdown')!=current['markdown']:
            raise SourceError('Exact source text does not match; rendered text is not an edit range')
        if '\r' in edit['new_text'] or '\x00' in edit['new_text']:
            raise SourceError('Replacement must be UTF-8 text with LF newlines')
        if len(edit['new_text'].encode('utf-8'))>4*1024*1024:raise SourceError('Replacement is too large')
        if bid!='@document' and ('<!-- block:' in edit['new_text'] or '<!-- /block -->' in edit['new_text']):
            raise SourceError('A block edit cannot alter anchor delimiters')
        identity=(path,bid)
        if identity in seen:raise SourceError('Multiple edits address the same block')
        seen.add(identity)
        grouped.setdefault(path,[]).append((current['start_byte'],current['end_byte'],edit['new_text'].encode('utf-8')))
    output={}
    for path,changes in grouped.items():
        doc=documents[path];ordered=sorted(changes)
        for prior,nxt in zip(ordered,ordered[1:]):
            if nxt[0]<prior[1]:raise SourceError('Overlapping edits, including document/block overlap, are not allowed')
        raw=doc.bytes
        for a,b,new in reversed(ordered):raw=raw[:a]+new+raw[b:]
        # Parse a candidate before touching any source; preserve identities and routing metadata.
        with tempfile.NamedTemporaryFile(dir=path.parent,suffix='.md',delete=False) as handle:
            staging=Path(handle.name);handle.write(raw)
        try:
            candidate=Document(staging,root)
            for field in ('id','kind','product','output','registry','record_id','frozen'):
                if candidate.meta.get(field)!=doc.meta.get(field):raise SourceError('Identity, output routing or freeze policy may not change: '+field)
            if not set(doc.blocks)<=set(candidate.blocks):raise SourceError('Existing block IDs may not be deleted or renamed')
        finally:staging.unlink(missing_ok=True)
        output[path]=(doc.bytes,raw)
    return output


def apply(bundle,patch,write=False,root=ROOT):
    changes=plan(bundle,patch,root)
    diffs=[]
    for path,(old,new) in changes.items():
        name=path.relative_to(root).as_posix()
        diffs.append(''.join(difflib.unified_diff(old.decode().splitlines(True),new.decode().splitlines(True),fromfile=name,tofile=name)))
    if write:
        temporary={};replaced=[]
        try:
            # Check all source files again immediately before staging; no partial validation.
            for path,(old,new) in changes.items():
                if path.read_bytes()!=old:raise SourceError('Source changed while validating: '+str(path))
                with tempfile.NamedTemporaryFile(dir=path.parent,delete=False) as handle:
                    handle.write(new);handle.flush();os.fsync(handle.fileno());temporary[path]=Path(handle.name)
            for path,temp in temporary.items():
                os.replace(temp,path);replaced.append(path)
        except Exception:
            for path in reversed(replaced):path.write_bytes(changes[path][0])
            raise
        finally:
            for temp in temporary.values():temp.unlink(missing_ok=True)
    return {'written':write,'files':[p.relative_to(root).as_posix() for p in changes],'diff':'\n'.join(diffs)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('review',help='Exported documentation-review.json')
    parser.add_argument('patch',help='LLM-produced frontier.patch.v1 JSON')
    parser.add_argument('--write',action='store_true',help='Write validated source edits; default is a dry-run diff')
    args=parser.parse_args()
    try:
        result=apply(read_json(args.review),read_json(args.patch),args.write)
        print(result['diff'])
        print(('Applied' if result['written'] else 'DRY RUN — no files written')+': '+', '.join(result['files']))
        print('Rebuild and review generated output before committing. No generated file was edited by this command.')
    except (SourceError,ValueError,KeyError,OSError) as error:
        parser.exit(2,'Patch rejected: '+str(error)+'\n')

if __name__=='__main__':main()
