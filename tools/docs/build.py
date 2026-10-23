#!/usr/bin/env python3
"""Compile canonical Markdown into the existing HTML documents and review maps."""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from markdown_sources import repository, digest
from source_views import prepare, publish_pages

prepare()
import renderer
from renderer import *
import source_review

_original_markdown=renderer.render_markdown

def load_guides():
    return repository().guides()

def render_markdown(text,definitions,links,prefix):
    return source_review.render(text,definitions,links,prefix,_original_markdown)

def slide_body(slide,prefix):
    return source_review.slide(slide,prefix,_original_markdown)

renderer.load_guides=load_guides
renderer.render_markdown=render_markdown
renderer.slide_body=slide_body

def build():
    before={p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in (ROOT/'content').rglob('*.md')}
    renderer.build()
    publish_pages()
    source_review.finish()
    after={p.relative_to(ROOT).as_posix():digest(p.read_bytes()) for p in (ROOT/'content').rglob('*.md')}
    if before!=after:
        raise RuntimeError('The compiler modified an authored source')
    print(json.dumps({'canonical_markdown_files':len(before),'content_revision':repository().revision,'source_unchanged':True},indent=2))

def commit():
    allowed={'content','guides','catalog','presentations','assets','examples','tools','qa'}
    roots={'README.md','CHANGELOG.md','MANIFEST.json','VALIDATION.md','PUBLISHING.md','AUTHORING.md','EDITORIAL_STANDARD.md','SCOPE.md','index.html','documentation-build.json','markdown-build.json'}
    raw=subprocess.check_output(['git','status','--porcelain=v1','-z','--untracked-files=all'],cwd=ROOT)
    paths=[]
    for row in raw.split(b'\0'):
        if not row:continue
        status=row[:2].decode();path=row[3:].decode()
        if 'R' in status or 'C' in status:raise RuntimeError('Review rename separately: '+path)
        if Path(path).parts[0] not in allowed and path not in roots:raise RuntimeError('Unexpected output: '+path)
        paths.append(path)
    for path in sorted(set(paths)):
        subprocess.run(['git','add','--',path],cwd=ROOT,check=True)
        subprocess.run(['git','commit','-m','docs: compile '+path],cwd=ROOT,check=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--commit',action='store_true')
    args=parser.parse_args()
    commit() if args.commit else build()
