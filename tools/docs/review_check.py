#!/usr/bin/env python3
"""Regression checks for source mapping, review behavior and guarded patching."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
import hashlib
import ast
import json
import subprocess
import tempfile
import threading
import traceback
from bs4 import BeautifulSoup
import markdown_sources as ms
import review_patch as guard

ROOT=Path(__file__).resolve().parents[2]
BASELINE='4a34aaadc5f9fd0e4dbb492c36aa152730c8ba5a'


def source_checks():
    repo=ms.Repository();results=[]
    for name,value in repo.registers().items():
        expected=json.loads(subprocess.check_output(['git','show',BASELINE+':catalog/'+name+'.json'],cwd=ROOT))
        assert value==expected,'Frozen register changed: '+name
    results.append('all registry values equal the approved baseline')
    mapped=0
    for path in [ROOT/'index.html',*(ROOT/'guides').glob('*.html'),*(ROOT/'catalog').glob('*.html'),*(ROOT/'presentations').glob('*.html')]:
        page=BeautifulSoup(path.read_text(),'html.parser');node=page.find(id='review-source-map')
        assert node is not None,path.as_posix()
        data=json.loads(node.string)
        for bid,target in data['targets'].items():
            raw=(ROOT/target['path']).read_text()
            assert ms.digest(raw)==target['file_sha256']
            assert raw[target['start_char']:target['end_char']]==target['markdown']
            assert raw.encode()[target['start_byte']:target['end_byte']].decode()==target['markdown']
            assert ms.digest(target['markdown'])==target['block_sha256']
            assert bid in repo.targets
            mapped+=1
    results.append(f'{mapped} rendered source targets match exact Unicode and UTF-8 source ranges')
    # Reject literal deck payloads in Python without matching this assertion's own text.
    for script in (ROOT/'tools/docs').glob('*.py'):
        if script.name == 'migrate_markdown_once.py':
            continue
        for stmt in ast.walk(ast.parse(script.read_text(encoding='utf-8'))):
            if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
                targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
                if any(isinstance(t, ast.Name) and t.id == 'DECKS' for t in targets) and isinstance(stmt.value, (ast.Dict, ast.List)):
                    raise AssertionError('Literal presentation content remains in '+script.name)
    assert len(repo.select('slide'))==52
    assert len(repo.select('section'))>=111
    return results


def guard_checks():
    outcomes=[]
    original=(ms.ROOT,ms.CONTENT,guard.ROOT,guard.CONTENT)
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);content=root/'content';content.mkdir()
        ms.ROOT=root;ms.CONTENT=content;guard.ROOT=root;guard.CONTENT=content
        try:
            path=content/'example.md'
            raw='---\nid: example\nkind: section\ntitle: Example\n---\n\n<!-- block: example-one -->\nFirst paragraph with café and an emoji 🧭.\n\n<!-- block: example-two -->\nSecond paragraph must remain unchanged.\n'
            path.write_text(raw)
            target=ms.Repository().targets['example-one']
            review={'schema':'frontier-review/v1','review_id':'review-test','comments':[{'id':'comment-1','status':'open','scope':'blocks','targets':[target]}]}
            edit={'comment_id':'comment-1','path':'content/example.md','block_id':'example-one',
                  'expected_file_sha256':target['file_sha256'],'expected_block_sha256':target['block_sha256'],
                  'before':target['markdown'],'after':target['markdown'].replace('First','Reviewed')}
            patch={'schema':'frontier-source-patch/v1','review_id':'review-test','edits':[edit]}
            changes,_=guard.plan(review,patch)
            assert path.read_text()==raw,'Dry-run modified a source'
            guard.apply_plan(changes)
            assert 'Reviewed paragraph' in path.read_text() and 'Second paragraph must remain unchanged.' in path.read_text()
            assert path.read_text().count('<!-- block:')==2
            path.write_text(raw);outcomes.append('dry-run and exact Unicode block replacement')
            def reject(label,packet=review,proposal=patch):
                snapshot=path.read_bytes()
                try:guard.plan(packet,proposal)
                except (ValueError,KeyError,TypeError):pass
                else:raise AssertionError('Accepted invalid patch: '+label)
                assert path.read_bytes()==snapshot,'Rejected patch wrote bytes'
                outcomes.append(label)
            bad=deepcopy(patch);bad['review_id']='another';reject('review identity mismatch',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['path']='../outside.md';reject('path traversal',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['path']='guides/devops.html';reject('generated output target',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['block_id']='example-two';reject('unselected source block',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['before']='approximate';reject('nonexact source excerpt',proposal=bad)
            bad=deepcopy(patch);bad['edits'][0]['after']+='\n<!-- block: forged -->\n';reject('block identity insertion',proposal=bad)
            bad=deepcopy(patch);bad['edits'].append(deepcopy(edit));reject('duplicate edits',proposal=bad)
            bad=deepcopy(review);bad['comments'][0]['status']='resolved';reject('resolved comment',packet=bad)
            path.write_text(raw+'\nAn unrelated newer edit.\n');reject('stale file even when selected block is unchanged');path.write_text(raw)
            protected=content/'registers';protected.mkdir();locked=protected/'locked.md'
            locked.write_text('---\nid: locked\nkind: record\ncollection: use-cases\n---\n<!-- block: frozen-one -->\nApproved objective.\n')
            frozen=ms.Repository().targets['frozen-one'];frozen['protected']=False
            bad=deepcopy(review);bad['comments'][0]['targets']=[frozen]
            proposal=deepcopy(patch);proposal['edits']=[{**edit,'path':'content/registers/locked.md','block_id':'frozen-one','before':frozen['markdown'],'after':'Changed objective.','expected_file_sha256':frozen['file_sha256'],'expected_block_sha256':frozen['block_sha256']}]
            reject('frozen record despite forged protection flag',packet=bad,proposal=proposal)
            link=content/'link.md';link.symlink_to(path)
            bad=deepcopy(patch);bad['edits'][0]['path']='content/link.md'
            packet=deepcopy(review);packet['comments'][0]['targets'][0]['path']='content/link.md'
            reject('symlink source',packet=packet,proposal=bad);link.unlink()
            # All files are checked before the first file is replaced.
            second=content/'second.md';second.write_text(raw.replace('id: example','id: second').replace('example-one','second-one').replace('example-two','second-two'))
            second_target=ms.Repository().targets['second-one']
            packet=deepcopy(review);packet['comments'][0]['targets'].append(second_target)
            proposal=deepcopy(patch);proposal['edits'].append({**edit,'path':'content/second.md','block_id':'second-one',
                'expected_file_sha256':second_target['file_sha256'],'expected_block_sha256':second_target['block_sha256']})
            changes,_=guard.plan(packet,proposal);second.write_text(second.read_text()+'\nConcurrent edit.\n')
            try:guard.apply_plan(changes)
            except ValueError:pass
            else:raise AssertionError('Batch accepted concurrent change')
            assert path.read_text()==raw
            outcomes.append('batch preflight prevents partial application')
        finally:
            ms.ROOT,ms.CONTENT,guard.ROOT,guard.CONTENT=original
    return outcomes


def browser_checks():
    from playwright.sync_api import sync_playwright
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(ROOT)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    reports=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width in (390,1440):
                context=browser.new_context(viewport={'width':width,'height':1000})
                page=context.new_page();errors=[];external=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('request',lambda r:external.append(r.url) if not r.url.startswith(base) else None)
                page.goto(base+'/guides/devops.html');page.wait_for_function('!!window.FrontierReview')
                page.locator('#review-toggle').click()
                block=page.locator('.report-section:visible p[data-review-block]').first
                block.locator('> .review-block-handle').click()
                page.locator('#review-comment').click()
                page.locator('#review-text').fill('Clarify this definition without changing its scope.')
                page.locator('#review-save').click()
                packet=page.evaluate('FrontierReview.exportPacket()');assert len(packet['comments'])==1
                note=packet['comments'][0];assert note['targets'][0]['path'].endswith('.md')
                assert note['targets'][0]['start_byte']>=note['targets'][0]['start_char']
                page.reload();page.wait_for_function('!!window.FrontierReview')
                assert len(page.evaluate('FrontierReview.exportPacket().comments'))==1
                page.locator('#review-search-open').click();page.locator('#review-global-search').fill('memory')
                assert page.locator('#review-search-results li').count()>0
                page.locator('#review-search-dialog button').click()
                page.locator('#review-toggle').click()
                # Consecutive block handles implement Shift range selection.
                candidates=page.locator('.report-section:visible [data-review-block]')
                candidates.nth(0).locator('> .review-block-handle').click()
                candidates.nth(2).locator('> .review-block-handle').click(modifiers=['Shift'])
                assert page.locator('.review-selected').count()>=3
                page.locator('#review-comment').click();page.locator('#review-text').fill('Review these adjacent source blocks together.');page.locator('#review-save').click()
                assert len(page.evaluate('FrontierReview.exportPacket().comments').pop()['targets'])>=3
                page.locator('#review-document-note').click();page.locator('#review-text').fill('Document-level review note.');page.locator('#review-save').click()
                assert page.evaluate('FrontierReview.exportPacket().comments').pop()['scope']=='document'
                # Native text selection is exported separately from exact Markdown coordinates.
                page.locator('#review-drawer .review-panel-heading button').click()
                block=page.locator('.report-section:visible p[data-review-block]').first
                block.evaluate('''el=>{const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const t=w.nextNode();const r=document.createRange();r.setStart(t,0);r.setEnd(t,Math.min(18,t.length));const s=getSelection();s.removeAllRanges();s.addRange(r);el.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));}''')
                assert page.locator('#review-text-comment').is_visible()
                page.locator('#review-text-comment').click();page.locator('#review-text').fill('Clarify the selected wording.');page.locator('#review-save').click()
                assert page.evaluate('FrontierReview.exportPacket().comments').pop()['selector']['exact']
                # Source mappings are also present on the actual presentation slide.
                page.goto(base+'/presentations/devops.html');page.wait_for_function('!!window.FrontierReview');page.locator('#review-toggle').click()
                slide=page.locator('.slide:visible');slide.locator('h1 > .review-block-handle').click()
                page.locator('#review-comment').click();page.locator('#review-text').fill('Slide-title comment.');page.locator('#review-save').click()
                assert '/presentations/devops/' in page.evaluate('FrontierReview.exportPacket().comments').pop()['targets'][0]['path']
                # Import is text-only, and forged/stale hashes are visibly flagged.
                incoming=page.evaluate('FrontierReview.exportPacket()');item=deepcopy(incoming['comments'][-1]);item['id']='import-test';item['body']='<img src=x onerror=alert(1)>';item['targets'][0]['file_sha256']='0'*64;incoming['comments']=[item]
                page.locator('#review-import').set_input_files({'name':'review.json','mimeType':'application/json','buffer':json.dumps(incoming).encode()})
                assert page.locator('.review-warning').count()>0
                assert page.locator('#review-drawer img').count()==0
                with page.expect_download() as download:
                    page.locator('#review-export').click()
                downloaded=json.loads(Path(download.value.path()).read_text())
                assert downloaded['schema']=='frontier-review/v1'
                page.goto(base+'/catalog/UC-D02.html');page.wait_for_function('!!window.FrontierReview')
                assert page.locator('.case-narrative [data-review-block]').count()>0
                assert not external,external
                assert not errors,errors
                reports.append({'viewport':width,'block_range_text_and_document_comments':'passed','local_persistence_and_cross_page_notes':'passed',
                    'global_search':'passed','slide_source_selection':'passed','export_import_and_stale_warning':'passed','external_requests':external,'javascript_errors':errors})
                context.close()
            # File URL mode is retained; no fetch of the index is required.
            page=browser.new_page();page.goto((ROOT/'guides/devops.html').as_uri());page.wait_for_function('!!window.FrontierReview')
            page.locator('#review-search-open').click();page.locator('#review-global-search').fill('memory');assert page.locator('#review-search-results li').count()>0
            reports.append({'file_url_search':'passed'})
            browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
    return reports

if __name__=='__main__':
    result={'schema':'frontier-authoring-validation/v1','errors':[]}
    try:
        result['source_mapping']=source_checks();result['patch_guards']=guard_checks();result['browser']=browser_checks()
    except Exception:
        result['errors'].append(traceback.format_exc())
    (ROOT/'qa/authoring-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if result['errors']:raise SystemExit(1)
