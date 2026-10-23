#!/usr/bin/env python3
"""Source fidelity, annotation integration and adversarial patch tests."""
from __future__ import annotations
import argparse
import copy
import functools
import http.server
import json
import tempfile
import threading
from pathlib import Path
from bs4 import BeautifulSoup
import md_source as source
from review_patch import apply, REPOSITORY

ROOT=source.ROOT


def patch_tests():
    tests=[]
    with tempfile.TemporaryDirectory() as directory:
        root=Path(directory);(root/'content').mkdir()
        path=root/'content/test.md'
        original='---\nid: fixture\nkind: section\ntitle: Test\n---\n<!-- block: first -->\nCafé and 🚀.\n<!-- /block -->\n\n<!-- block: second -->\nUnchanged paragraph.\n<!-- /block -->\n'
        path.write_text(original)
        d=source.Document(path,root);target=d.target('first')
        bundle={'schema':'frontier.review.v1','repository':REPOSITORY,'annotations':[{'id':'comment-1','type':'comment','status':'open','targets':[target]}]}
        edit={'annotation_id':'comment-1','source_path':'content/test.md','document_id':'fixture','block_id':'first',
              'expected_file_sha256':d.sha,'expected_block_sha256':target['block_sha256'],'old_text':target['markdown'],'new_text':'Café and 🚀, clarified.'}
        patch={'schema':'frontier.patch.v1','repository':REPOSITORY,'edits':[edit]}
        result=apply(bundle,patch,False,root)
        assert path.read_text()==original and not result['written'];tests.append('dry run preserves source')
        apply(bundle,patch,True,root)
        assert path.read_text()==original.replace('Café and 🚀.','Café and 🚀, clarified.')
        tests.append('UTF-8 byte-accurate selected-block edit')
        def rejected(b,p,label):
            before=path.read_bytes()
            try:apply(b,p,True,root)
            except (source.SourceError,ValueError,KeyError,OSError):pass
            else:raise AssertionError('Unsafe patch accepted: '+label)
            assert path.read_bytes()==before,'Partial write on rejected patch: '+label
            tests.append(label)
        rejected(bundle,patch,'stale snapshot rejected')
        path.write_text(original)
        for field,value,label in [('source_path','../README.md','path traversal rejected'),('source_path','guides/devops.html','generated file rejected'),('block_id','unknown','unknown block rejected'),('new_text','Text\n<!-- /block -->','anchor injection rejected'),('expected_file_sha256','0'*64,'wrong file hash rejected'),('old_text','rendered substitute','inexact old text rejected')]:
            bad=copy.deepcopy(patch);bad['edits'][0][field]=value;rejected(bundle,bad,label)
        bad=copy.deepcopy(patch);bad['edits'].append(copy.deepcopy(edit));rejected(bundle,bad,'duplicate edit rejected')
        bad_bundle=copy.deepcopy(bundle);bad_bundle['annotations'][0]['targets'][0]['start_byte']+=1;rejected(bad_bundle,patch,'tampered source span rejected')
        bad_bundle=copy.deepcopy(bundle);bad_bundle['annotations'][0]['status']='resolved';rejected(bad_bundle,patch,'resolved comment rejected')
        doc_target=d.target('@document');both=copy.deepcopy(bundle);both['annotations'][0]['targets'].append(doc_target)
        broad={**edit,'block_id':'@document','old_text':doc_target['markdown'],'new_text':doc_target['markdown'],'expected_block_sha256':doc_target['block_sha256']}
        bad={**patch,'edits':[edit,broad]};rejected(both,bad,'overlapping document and block edits rejected')
        symlink=root/'content/link.md';symlink.symlink_to(path)
        malicious=copy.deepcopy(bundle);malicious['annotations'][0]['targets'][0]['source_path']='content/link.md'
        bad=copy.deepcopy(patch);bad['edits'][0]['source_path']='content/link.md';rejected(malicious,bad,'symlink rejected')
        path.write_text(original.replace('kind: section','kind: section\nfrozen: true'))
        frozen=source.Document(path,root);ft=frozen.target('first')
        fb=copy.deepcopy(bundle);fb['annotations'][0]['targets']=[ft]
        fp=copy.deepcopy(patch);fp['edits'][0]['expected_file_sha256']=frozen.sha
        rejected(fb,fp,'frozen definition rejected')
        # A valid first edit followed by an invalid second edit must change neither.
        path.write_text(original)
        invalid={**edit,'block_id':'missing'}
        rejected(bundle,{**patch,'edits':[edit,invalid]},'transaction prevalidation prevents partial writes')
    return tests


def browser_tests():
    from playwright.sync_api import sync_playwright
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    handler=functools.partial(Quiet,directory=str(ROOT))
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base='http://127.0.0.1:'+str(server.server_port)
    results=[]
    try:
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for width in (390,1440):
                context=br.new_context(viewport={'width':width,'height':1000},accept_downloads=True)
                page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/guides/devops.html');page.wait_for_function('!!window.FrontierReview')
                assert page.evaluate('window.FRONTIER_SEARCH.length')>100
                page.locator('#review-search-open').click();page.locator('#review-search-input').fill('AGENTS.md')
                assert page.locator('#review-search-results a').count()>0
                page.locator('#review-search-close').click()
                page.locator('#review-enable').click()
                node=page.locator('[data-source-key^="D-90::b-"]').filter(has=page.locator('p')).first
                node.locator(':scope > .review-handle').click()
                key=node.get_attribute('data-source-key')
                page.locator('#review-body').fill('Clarify this paragraph without changing the approved model.')
                page.locator('#review-form button[type="submit"]').click()
                assert page.locator('.review-thread').count()==1
                assert page.locator('#review-status').inner_text().startswith('Saved')
                page.locator('#review-kind').select_option('note');page.locator('#review-body').fill('<img src=x onerror=alert(1)> This is review text, not HTML.')
                page.locator('#review-form button[type="submit"]').click()
                assert page.locator('.review-thread').count()==2
                assert page.locator('.review-thread img').count()==0
                bundle=page.evaluate('window.FrontierReview.bundle()')
                t=bundle['annotations'][0]['targets'][0]
                assert t['key']==key and t['markdown'] and t['offset_encoding']=='utf-8'
                actual=(ROOT/t['source_path']).read_bytes()[t['start_byte']:t['end_byte']].decode()
                assert actual==t['markdown']
                page.reload();page.locator('#review-open').click();assert page.locator('.review-thread').count()==2
                # Thread operations and local cross-document persistence.
                first=page.locator('.review-thread').first
                first.get_by_role('button',name='Reply',exact=True).click()
                first.locator('textarea').fill('Keep source references intact.')
                first.get_by_role('button',name='Save reply',exact=True).click()
                first.get_by_role('button',name='Resolve',exact=True).click()
                assert 'resolved' in page.locator('.review-thread h3').first.inner_text()
                first.get_by_role('button',name='Reopen',exact=True).click()
                with page.expect_download() as dl:
                    page.locator('#review-export').click()
                exported=json.loads(Path(dl.value.path()).read_text())
                assert len(exported['annotations'])==2
                assert exported['annotations'][0]['replies'][0]['body']=='Keep source references intact.'
                with page.expect_download() as packet:
                    page.locator('#review-llm').click()
                text=Path(packet.value.path()).read_text()
                assert 'frontier.patch.v1' in text and t['source_path'] in text and t['block_sha256'] in text
                page.goto(base+'/catalog/UC-D06.html');page.locator('#review-open').click()
                assert page.locator('.review-thread').count()==2
                page.goto(base+'/presentations/devops.html');page.locator('#review-enable').click();page.locator('#review-section').click()
                selected=page.locator('#review-targets').inner_text()
                assert 'content/presentations/devops/01.md' in selected
                page.locator('#review-body').fill('Comment on the slide definition, not generated HTML.')
                page.locator('#review-form button[type="submit"]').click()
                assert len(page.evaluate('window.FrontierReview.bundle().annotations'))==3
                # Independent browser import and malformed input rejection.
                other=br.new_context(viewport={'width':width,'height':1000});p=other.new_page();p.goto(base+'/guides/devops.html');p.locator('#review-open').click()
                p.locator('#review-import-file').set_input_files({'name':'review.json','mimeType':'application/json','buffer':json.dumps(exported).encode()})
                p.wait_for_function('window.FrontierReview.bundle().annotations.length===2')
                assert p.locator('.review-thread').count()==2
                bad={**exported,'repository':'another/repository'}
                p.locator('#review-import-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':json.dumps(bad).encode()})
                p.wait_for_function('document.querySelector("#review-status").textContent.includes("rejected")')
                assert len(p.evaluate('window.FrontierReview.bundle().annotations'))==2
                other.close()
                assert not errors,errors
                results.append({'width':width,'search':'passed','source_selection':'passed','notes_comments_and_replies':'passed',
                    'reload_and_cross_document_storage':'passed','export_and_import':'passed','llm_packet':'passed','html_injection':'rejected','javascript_errors':errors})
                context.close()
            # Local-file reading and global search must not depend on fetch or a server.
            page=br.new_page();page.goto((ROOT/'guides/devops.html').as_uri());page.wait_for_function('!!window.FrontierReview')
            assert page.evaluate('window.FRONTIER_SEARCH.length')>100
            page.locator('#review-search-open').click();page.locator('#review-search-input').fill('memory')
            assert page.locator('#review-search-results a').count()>0
            results.append({'file_url_search':'passed'});page.close();br.close()
    finally:server.shutdown();server.server_close()
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--browser',action='store_true');args=parser.parse_args()
    errors=[];tests=[];browser=[]
    try:
        docs=source.documents();index=json.loads((ROOT/'assets/source-map.json').read_text())
        for key,target in index['targets'].items():
            d=docs[target['document_id']];actual=d.target(target['block_id'])
            assert actual==target,'Incorrect source target: '+key
            raw=d.bytes[target['start_byte']:target['end_byte']]
            assert raw.decode()==target['markdown'] and source.digest(raw)==target['block_sha256']
        for product,text in source.assembled_guides().items():assert (ROOT/f'guides/{product}.md').read_text()==text
        for registry in source.REGISTRIES:
            assert json.loads((ROOT/f'catalog/{registry}.json').read_text())==source.registry(registry)
        for path,record in index['pages'].items():
            soup=BeautifulSoup((ROOT/path).read_text(),'html.parser')
            payload=json.loads(soup.find(id='review-source-data').string)
            for node in soup.select('[data-source-key]'):assert node['data-source-key'] in payload['targets']
            assert len(soup.select('#review-source-data'))==1
        tests=patch_tests()
        if args.browser:browser=browser_tests()
    except Exception as exc:
        import traceback;errors.append(str(exc));print(traceback.format_exc())
    result={'schema':'frontier.markdown-validation.v1','revision':source.source_revision(),
            'source_documents':len(source.documents()),'exact_source_spans':'passed' if not errors else 'see errors',
            'patch_tests':tests,'browser':browser,'errors':errors,
            'boundary':'Source preservation, browser interactions and patch safety tests; not live AWS execution or real-time collaboration.'}
    (ROOT/'qa/markdown-review-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    raise SystemExit(1 if errors else 0)

if __name__=='__main__':main()
