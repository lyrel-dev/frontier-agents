#!/usr/bin/env python3
"""Check the final published tree and refresh hashes after all report changes."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import hashlib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]

def main():
    raw=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=ROOT)
    names=sorted(set(x.decode() for x in raw.split(b'\0') if x))
    names=[n for n in names if (ROOT/n).is_file() and '__pycache__' not in n and '/mechanism-screens/' not in n]
    errors=[];links=0;cache={}
    for name in names:
        p=ROOT/name
        if p.suffix!='.html':continue
        soup=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
        for tag in soup.select('a[href]'):
            u=urlsplit(tag['href'])
            if u.scheme or u.netloc:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
            links+=1
            if not target.is_file():errors.append({'file':name,'href':tag['href'],'reason':'missing target'});continue
            if u.fragment and target.suffix=='.html':
                if target not in cache:cache[target]={x.get('id') for x in BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser').select('[id]')}
                if unquote(u.fragment) not in cache[target]:errors.append({'file':name,'href':tag['href'],'reason':'missing anchor'})
    report={'revision':'2026-10-21-platform-reference-1','html_files':sum(Path(n).suffix=='.html' for n in names),'local_links_checked':links,'errors':errors,'live_aws_execution':False,'scope':'Final local links across the complete working tree; source content and browser behavior have separate validation records.'}
    out=ROOT/'qa/platform-publication-validation.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    if errors:print(json.dumps(report,indent=2));raise SystemExit(1)
    names=sorted(set(names+['qa/platform-publication-validation.json']))
    files={}
    for name in names:
        if name=='MANIFEST.json':continue
        p=ROOT/name
        if p.is_file():
            content=p.read_bytes();files[name]={'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest()}
    manifest={'revision':'2026-10-21-platform-reference-1','files':files,'boundary':'File hashes identify this working-tree publication. They do not establish external documentation accuracy or runtime product behavior.'}
    (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2));print('Manifest entries:',len(files))

if __name__=='__main__':main()
