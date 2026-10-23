#!/usr/bin/env python3
"""Validate source-scoped LLM edits. Dry-run is default; no model/network calls.

Usage:
  python tools/docs/review_patch.py validate review.json patch.json
  python tools/docs/review_patch.py apply review.json patch.json --write
"""
from __future__ import annotations
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import yaml
from markdown_sources import ROOT, CONTENT, Repository, Source, FRONT, UniqueLoader, digest

MAX_BYTES = 20_000_000

class ReviewError(ValueError):
    pass

def load_json(path):
    path=Path(path)
    if path.stat().st_size>MAX_BYTES:
        raise ReviewError('Input exceeds 20 MB')
    def unique(pairs):
        out={}
        for k,v in pairs:
            if k in out: raise ReviewError('Duplicate JSON property: '+k)
            out[k]=v
        return out
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique)

def checked_path(value):
    if not isinstance(value,str) or not re.fullmatch(r'content/[A-Za-z0-9_./-]+\.md',value) or '..' in Path(value).parts:
        raise ReviewError('Not an allowed Markdown source path: '+str(value))
    path=ROOT/value
    if not path.is_file() or path.is_symlink() or any(p.is_symlink() for p in path.parents if p!=ROOT):
        raise ReviewError('Source is missing or uses a symlink: '+value)
    if not path.resolve().is_relative_to(CONTENT.resolve()):
        raise ReviewError('Source escapes content/: '+value)
    return path

def plan(review,patch):
    if not isinstance(review,dict) or review.get('schema')!='frontier-review/v1':
        raise ReviewError('Unsupported review schema')
    if not isinstance(patch,dict) or patch.get('schema')!='frontier-source-patch/v1':
        raise ReviewError('Unsupported patch schema')
    if not review.get('review_id') or patch.get('review_id')!=review['review_id']:
        raise ReviewError('Patch does not identify the supplied review')
    comments=review.get('comments')
    if not isinstance(comments,list) or len(comments)>2000:
        raise ReviewError('Invalid review comments')
    by_id={}
    for comment in comments:
        if not isinstance(comment,dict) or not isinstance(comment.get('id'),str) or comment['id'] in by_id:
            raise ReviewError('Invalid or duplicate comment identifier')
        by_id[comment['id']]=comment
    edits=patch.get('edits')
    if not isinstance(edits,list) or not edits or len(edits)>2000:
        raise ReviewError('Patch must contain 1–2000 explicit edits')
    repo=Repository()
    from selection_model import validate_structure
    files={};used=set();authorized=[]
    for edit in edits:
        required={'comment_id','path','block_id','expected_file_sha256','expected_block_sha256','before','after'}
        if not isinstance(edit,dict) or set(edit)!=required or not all(isinstance(edit[k],str) for k in required):
            raise ReviewError('Edit requires exactly: '+', '.join(sorted(required)))
        comment=by_id.get(edit['comment_id'])
        if comment is None or comment.get('status')!='open':
            raise ReviewError('Edit must reference an open review comment')
        validate_structure(comment,repo,ROOT)
        choices=[t for t in comment.get('targets',[]) if isinstance(t,dict) and t.get('block_id')==edit['block_id'] and t.get('path')==edit['path']]
        if len(choices)!=1:
            raise ReviewError('Edit is outside the comment selection or is ambiguous')
        supplied=choices[0]
        path=checked_path(edit['path'])
        source=Source.read(path)
        # Protection is derived from current source and directory, never from the packet.
        if source.protected or path.is_relative_to(CONTENT/'registers'):
            raise ReviewError('Approved record is frozen: '+edit['path'])
        current=repo.targets.get(edit['block_id'])
        if current is None or current['path']!=edit['path']:
            raise ReviewError('Block no longer exists at the selected source')
        for field,key in [('file_sha256','expected_file_sha256'),('block_sha256','expected_block_sha256')]:
            if current[field]!=supplied.get(field) or current[field]!=edit[key]:
                raise ReviewError('Stale '+field+'; re-review the current source: '+edit['path'])
        if edit['before']!=current['markdown'] or supplied.get('markdown')!=current['markdown']:
            raise ReviewError('Source excerpt differs; fuzzy replacement is not permitted')
        # A selected text quote is narrower than its enclosing Markdown block.
        # Only exact, unique source text can authorize an automated sub-block edit;
        # rendered selections spanning markup/multiple blocks require explicit block review.
        if comment.get('scope')=='text':
            selector=comment.get('selector')
            quote=selector.get('exact') if isinstance(selector,dict) else None
            if not isinstance(quote,str) or not quote.strip():
                raise ReviewError('Text-scoped edit requires an exact selected quote')
            before=edit['before']
            if before.count(quote)!=1:
                raise ReviewError('Selected rendered text cannot be uniquely mapped to source Markdown; select a block')
            at=before.index(quote)
            prefix,suffix=before[:at],before[at+len(quote):]
            if not edit['after'].startswith(prefix) or not edit['after'].endswith(suffix):
                raise ReviewError('Text-scoped edit changed Markdown outside the selected quote')
        if '\x00' in edit['after'] or '\r' in edit['after'] or len(edit['after'].encode())>1_000_000:
            raise ReviewError('Invalid replacement text or replacement exceeds 1 MB')
        if re.search(r'^<!-- block:',edit['after'],re.M):
            raise ReviewError('Replacement cannot add or replace block markers')
        if edit['block_id'] in used:
            raise ReviewError('Duplicate edit for a source block')
        used.add(edit['block_id'])
        files.setdefault(path,{'source':source,'changes':[]})['changes'].append((current,edit['after']))
        authorized.append({'comment_id':edit['comment_id'],'path':edit['path'],'block_id':edit['block_id']})
    result={}
    for path,item in files.items():
        source=item['source'];text=source.raw
        ranges=sorted(item['changes'],key=lambda pair:pair[0]['start_char'])
        if any(a[0]['end_char']>b[0]['start_char'] for a,b in zip(ranges,ranges[1:])):
            raise ReviewError('Overlapping edit ranges')
        for target,replacement in reversed(ranges):
            text=text[:target['start_char']]+replacement+text[target['end_char']:]
        match=FRONT.match(text)
        if not match: raise ReviewError('Patch removed YAML front matter')
        metadata=yaml.load(match[1],Loader=UniqueLoader)
        if not isinstance(metadata,dict):raise ReviewError('Invalid YAML metadata')
        old_meta={k:v for k,v in source.meta.items() if k!='title'}
        new_meta={k:v for k,v in metadata.items() if k!='title'}
        if old_meta!=new_meta:
            raise ReviewError('Patch changed configuration/identity metadata outside the editable title')
        if 'title' in metadata and not isinstance(metadata['title'],str):
            raise ReviewError('Title must remain a string')
        candidate=Source(path,text,metadata,match.end())
        if [t['block_id'] for t in candidate.targets()]!=[t['block_id'] for t in source.targets()]:
            raise ReviewError('Patch changed block identities; split/merge operations require a separate authoring change')
        # Exact scope assertion: every difference is accounted for by the selected ranges.
        result[path]={'before':source.raw,'after':text,'sha256':digest(source.raw)}
    return result,authorized

def apply_plan(changes):
    """Preflight all files before writing; restore original bytes on local failure."""
    for path,item in changes.items():
        checked_path(path.relative_to(ROOT).as_posix())
        if digest(path.read_bytes())!=item['sha256']:
            raise ReviewError('Source changed after validation; no files were written')
    pending=[];written=[]
    try:
        for path,item in changes.items():
            fd,temp=tempfile.mkstemp(prefix='.review-',suffix='.tmp',dir=path.parent)
            with os.fdopen(fd,'w',encoding='utf-8',newline='\n') as handle:
                handle.write(item['after']);handle.flush();os.fsync(handle.fileno())
            pending.append((path,Path(temp)))
        for path,temp in pending:
            if digest(path.read_bytes())!=changes[path]['sha256']:
                raise ReviewError('Concurrent source modification; restoring this patch batch')
            os.replace(temp,path);written.append(path)
    except Exception:
        for path in written:
            path.write_text(changes[path]['before'],encoding='utf-8')
        raise
    finally:
        for _,temp in pending:
            temp.unlink(missing_ok=True)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','apply'])
    parser.add_argument('review');parser.add_argument('patch')
    parser.add_argument('--write',action='store_true',help='Apply only after all exact-scope checks pass')
    parser.add_argument('--review-sha256',help='Optional trusted SHA-256 of the original reviewer export')
    args=parser.parse_args()
    try:
        if args.review_sha256 and digest(Path(args.review).read_bytes())!=args.review_sha256:
            raise ReviewError('Reviewer export digest differs from the trusted value')
        changes,edits=plan(load_json(args.review),load_json(args.patch))
        for path,item in changes.items():
            rel=path.relative_to(ROOT).as_posix()
            print(''.join(difflib.unified_diff(item['before'].splitlines(True),item['after'].splitlines(True),fromfile=rel,tofile=rel)),end='')
        if args.write:
            if args.command!='apply':raise ReviewError('--write requires the apply command')
            apply_plan(changes)
        print(json.dumps({'valid':True,'applied':args.write,'files':len(changes),'edits':edits},indent=2))
    except (ValueError,KeyError,TypeError,OSError,yaml.YAMLError) as exc:
        raise SystemExit('REJECTED: '+str(exc))

if __name__=='__main__':main()
