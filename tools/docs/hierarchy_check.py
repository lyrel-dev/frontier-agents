"""Semantic selection tests; no live AWS execution or editorial-quality claim."""
from copy import deepcopy
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import re
import threading
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, expect
from markdown_sources import Repository
from selection_model import snapshot_keys, validate_structure, ordered_unique
import review_patch


def packet_for(mapping, keys):
    roots=[{k:mapping['selections'][ident][k] for k in snapshot_keys()} for ident in keys]
    ids=ordered_unique(x for node in roots for x in node['target_ids'])
    context=ordered_unique(x for node in roots for x in node['context_ids'])
    return {'id':'hierarchy-comment','kind':'comment','status':'open','scope':'structure',
        'document':mapping['document'],'body':'Clarify the selected section.',
        'targets':[mapping['targets'][bid] for bid in ids],
        'selection':{'schema':'frontier-selection/v1','content_revision':mapping['content_revision'],
                     'roots':roots,'target_ids':ids,'context_ids':context}}


def validate(root: Path):
    repo=Repository(); reports=[]; pages=0; total=0
    paths=[root/'index.html',*(root/'guides').glob('*.html'),*(root/'catalog').glob('*.html'),*(root/'presentations').glob('*.html')]
    for path in paths:
        tree=BeautifulSoup(path.read_text(),'html.parser')
        mapping=json.loads(tree.find(id='review-source-map').string)
        nodes=mapping['selections'];assert nodes,path
        assert sum(n['kind']=='document' for n in nodes.values())==1
        for ident,node in nodes.items():
            element=tree.find(id=node['anchor'])
            assert element is not None and element.get('data-review-scope')==ident
            assert len(node['target_ids'])==len(set(node['target_ids']))
            assert all(bid in mapping['targets'] for bid in node['target_ids'])
            seen={ident};parent=node['parent']
            while parent:
                assert parent in nodes and parent not in seen
                assert set(node['target_ids']).issubset(nodes[parent]['target_ids'])
                seen.add(parent);parent=nodes[parent]['parent']
        pages+=1;total+=len(nodes)
    reports.append({'pages':pages,'selection_nodes':total,'tree_integrity_and_exact_membership':'passed'})
    tree=BeautifulSoup((root/'guides/devops.html').read_text(),'html.parser')
    mapping=json.loads(tree.find(id='review-source-map').string)
    section=next(n for n in mapping['selections'].values() if n['kind']=='section' and len(n['target_ids'])>2)
    comment=packet_for(mapping,[section['id']]);validate_structure(comment,repo,root)
    editable=next(t for t in comment['targets'] if not t['protected'] and not t.get('field'))
    review={'schema':'frontier-review/v1','review_id':'hierarchy-test','comments':[comment]}
    proposal={'schema':'frontier-source-patch/v1','review_id':'hierarchy-test','edits':[{
        'comment_id':comment['id'],'path':editable['path'],'block_id':editable['block_id'],
        'expected_file_sha256':editable['file_sha256'],'expected_block_sha256':editable['block_sha256'],
        'before':editable['markdown'],'after':editable['markdown']+'\n\nReview-only test sentence.'}]}
    changes,_=review_patch.plan(review,proposal)
    assert len(changes)==1
    regressions=['valid section permits one exact member edit without writing']
    def rejected(label, changed):
        try:validate_structure(changed,repo,root)
        except ValueError:regressions.append(label)
        else:raise AssertionError('Unsafe structural selection accepted: '+label)
    bad=deepcopy(comment);bad['targets'].pop();rejected('omitted member rejected',bad)
    bad=deepcopy(comment);bad['selection']['target_ids']=bad['selection']['target_ids'][::-1];rejected('reordered member rejected',bad)
    bad=deepcopy(comment);bad['selection']['content_revision']='0'*64;rejected('stale canonical revision rejected',bad)
    bad=deepcopy(comment);bad['selection']['roots'].append(deepcopy(bad['selection']['roots'][0]));rejected('duplicate roots rejected',bad)
    child=next(n for n in mapping['selections'].values() if n['parent']==section['id'] and n['target_ids'])
    bad=packet_for(mapping,[section['id'],child['id']]);rejected('ancestor descendant duplication rejected',bad)
    bad=deepcopy(comment);bad['selection']['roots'][0]['membership_sha256']='0'*64;rejected('changed scope membership rejected',bad)
    bad=deepcopy(comment);bad['document']='../outside.html';rejected('unsafe generated-document path rejected',bad)
    contextual=next(n for n in mapping['selections'].values() if n['annotation_only'] and n['context_ids'])
    bad=packet_for(mapping,[contextual['id']]);rejected('context-only cell or item cannot authorize edits',bad)
    reports.append({'source_guard_regressions':regressions})
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(root)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            for width in (390,1440):
                context=browser.new_context(viewport={'width':width,'height':1000})
                page=context.new_page();errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.goto(base+'/guides/devops.html');page.wait_for_function('FrontierReview.interaction==="contextual-v4"')
                section_el=page.locator('.report-section:visible').first
                scope_id=section_el.get_attribute('data-review-scope')
                heading=section_el.locator('h3[data-review-block]').first
                title_scope=heading.get_attribute('data-review-scope')
                heading.hover();page.locator('#review-block-select').click()
                expect(page.locator('#review-scope-select')).to_have_value(title_scope)
                page.locator('#review-scope-select').select_option(scope_id)
                expect(section_el).to_have_class(re.compile('review-scope-selected'))
                expected=page.evaluate('(id)=>JSON.parse(document.getElementById("review-source-map").textContent).selections[id].target_ids',scope_id)
                assert len(expected)>1
                assert set(page.locator('.review-selected').evaluate_all('(els)=>els.map(e=>e.dataset.reviewBlock)'))==set(expected)
                section_el.locator('p[data-review-block]').first.evaluate('el=>el.hidden=true')
                page.locator('#review-text-comment').click();page.locator('#review-text').fill('Review this complete section.')
                saved=page.evaluate('FrontierReview.exportPacket().comments[0]')
                assert saved['selection']['target_ids']==expected
                assert [t['block_id'] for t in saved['targets']]==expected
                page.locator('#review-drawer .review-panel-heading button').click()
                badge=page.locator('.review-comment-marker[data-scope-id="'+scope_id+'"]')
                expect(badge).to_be_visible()
                assert page.locator('.review-comment-marker').count()==1,'Container comment duplicated on every child'
                page.reload();page.wait_for_function('!!window.FrontierReview')
                assert page.evaluate('FrontierReview.exportPacket().comments[0].selection.target_ids')==expected
                section_el=page.locator('[data-review-scope="'+scope_id+'"]');heading=section_el.locator('h3[data-review-block]').first
                heading.hover();page.locator('#review-scope-select').select_option(scope_id)
                heading.hover();page.locator('#review-block-select').click(modifiers=['Control'])
                assert page.locator('.review-scope-selected').count()==1,'Ancestor selection was not normalized'
                heading.focus();page.keyboard.press('Enter');page.keyboard.press('Alt+ArrowUp')
                chapter=section_el.locator('xpath=ancestor::section[@data-reader-chapter][1]')
                chapter_scope=chapter.get_attribute('data-review-scope')
                page.locator('#review-scope-select').select_option(chapter_scope)
                expected_chapter=page.evaluate('(id)=>JSON.parse(document.getElementById("review-source-map").textContent).selections[id].target_ids',chapter_scope)
                assert len(expected_chapter)>=len(expected)
                page.locator('#review-text-comment').click();page.locator('#review-text').fill('Review the chapter structure and progression.')
                assert page.evaluate('FrontierReview.exportPacket().comments').pop()['selection']['target_ids']==expected_chapter
                page.locator('#review-drawer .review-panel-heading button').click()
                page.locator('#review-notes-open').click();page.locator('#review-document-note').click()
                page.locator('#review-text').fill('Document-wide review.')
                note=page.evaluate('FrontierReview.exportPacket().comments').pop()
                assert note['scope']=='document' and note['selection']['roots'][0]['kind']=='document'
                assert len(note['targets'])>len(expected_chapter)
                page.locator('#review-drawer .review-panel-heading button').click()
                page.goto(base+'/presentations/devops.html');page.wait_for_function('!!window.FrontierReview')
                slide=page.locator('.slide:visible');title=slide.locator('h1[data-review-block]')
                slide_id=slide.get_attribute('data-review-scope');title.hover()
                page.locator('#review-scope-select').select_option(slide_id)
                page.locator('#review-text-comment').click();page.locator('#review-text').fill('Review the complete slide.')
                note=page.evaluate('FrontierReview.exportPacket().comments').pop()
                assert note['selection']['roots'][0]['kind']=='slide' and len(note['targets'])>1
                assert len(note['targets'])==len({t['block_id'] for t in note['targets']})
                assert page.locator('#review-drawer #review-scope-select,#review-drawer #review-export').count()==0
                assert not errors,errors
                reports.append({'viewport':width,'heading_section_chapter_slide_document':'passed',
                    'hidden_members_snapshotted':'passed','normalized_ancestor_selection':'passed',
                    'one_container_thread_marker':'passed','autosave_reload_exact_export':'passed',
                    'note_popup_remains_note_only':'passed','javascript_errors':errors})
                context.close()
            browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
    return reports
