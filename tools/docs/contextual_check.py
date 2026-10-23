"""Browser acceptance for normal-reading, source-anchored annotations."""
from __future__ import annotations
from copy import deepcopy
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import threading
from playwright.sync_api import sync_playwright, expect


def browser_checks(root: Path):
    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args): pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    reports = []
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            for width in (390, 1440):
                context = browser.new_context(viewport={'width': width, 'height': 1000})
                page = context.new_page(); errors = []; external = []
                page.on('pageerror', lambda e: errors.append(str(e)))
                page.on('request', lambda r: external.append(r.url) if not r.url.startswith(base) else None)
                page.goto(base+'/guides/devops.html')
                page.wait_for_function('window.FrontierReview?.interaction === "contextual-v2"')
                assert page.locator('#review-toggle,#review-toolbar').count() == 0
                expect(page.locator('#review-block-controls')).to_be_hidden()
                para = page.locator('.report-section:visible p[data-review-block]').first
                original = para.text_content(); bid = para.get_attribute('data-review-block')
                para.hover()
                expect(page.locator('#review-block-controls')).to_have_attribute('data-block-id', bid)
                page.locator('#review-block-comment').click()
                expect(page.locator('#review-drawer')).to_have_attribute('data-context', 'element')
                page.locator('#review-text').fill('Clarify this definition without changing its scope.')
                page.locator('#review-save').click()
                packet = page.evaluate('FrontierReview.exportPacket()')
                assert len(packet['comments']) == 1
                assert packet['comments'][0]['targets'][0]['block_id'] == bid
                assert packet['comments'][0]['targets'][0]['path'].endswith('.md')
                assert packet['review_id'] == page.evaluate('FrontierReview.exportPacket().review_id')
                assert '"review_id": "'+packet['review_id']+'"' in page.evaluate('FrontierReview.exportPrompt()')
                page.locator('#review-drawer .review-panel-heading button').click()
                badge = page.locator(f'.review-comment-marker[data-block-id="{bid}"]:visible').first
                expect(badge).to_be_visible(); badge.click()
                expect(page.locator('#review-note-filter')).to_have_value('anchor')
                assert page.locator('.review-thread').count() == 1
                page.get_by_role('button', name='Reply', exact=True).click()
                page.locator('#review-text').fill('Retain the AWS/source ownership distinction.')
                page.locator('#review-save').click()
                assert page.evaluate('FrontierReview.exportPacket().comments[0].replies.length') == 1
                page.get_by_role('button', name='Resolve', exact=True).click()
                assert page.evaluate('FrontierReview.exportPacket().comments[0].status') == 'resolved'
                page.get_by_role('button', name='Reopen', exact=True).click()
                page.locator('#review-drawer .review-panel-heading button').click()
                assert para.text_content() == original, 'Controls contaminated rendered source text'
                assert page.locator('[data-review-block] [data-review-ui]').count() == 0
                page.reload(); page.wait_for_function('!!window.FrontierReview')
                assert page.evaluate('FrontierReview.exportPacket().review_id') == packet['review_id']
                assert len(page.evaluate('FrontierReview.exportPacket().comments')) == 1
                expect(page.locator(f'.review-comment-marker[data-block-id="{bid}"]:visible').first).to_be_visible()

                para = page.locator('.report-section:visible p[data-review-block]').first
                para.evaluate('''el=>{el.focus();const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);const t=w.nextNode();const r=document.createRange();r.setStart(t,0);r.setEnd(t,Math.min(18,t.length));const s=getSelection();s.removeAllRanges();s.addRange(r);el.dispatchEvent(new MouseEvent('mouseup',{bubbles:true}));}''')
                expect(page.locator('#review-text-comment')).to_be_visible()
                page.locator('#review-text-comment').click(); page.locator('#review-text').fill('Clarify the quoted wording.')
                page.locator('#review-save').click()
                quote = page.evaluate('FrontierReview.exportPacket().comments').pop()
                assert quote['scope'] == 'text' and quote['selector']['exact']
                assert quote['selector']['position']['unit'].startswith('UTF-16')
                page.locator('#review-drawer .review-panel-heading button').click()
                page.evaluate('getSelection().removeAllRanges()');page.wait_for_timeout(90)

                candidates = page.locator('.report-section:visible [data-review-block]')
                ids = candidates.evaluate_all('(els)=>els.map(el=>el.dataset.reviewBlock)')
                candidates.nth(0).hover(); page.locator('#review-block-select').click()
                candidates.nth(2).hover(); page.locator('#review-block-select').click(modifiers=['Shift'])
                assert page.locator('.review-selected').count() >= 3
                page.locator('#review-text-comment').click();page.locator('#review-text').fill('Review the selected adjacent blocks together.');page.locator('#review-save').click()
                assert len(page.evaluate('FrontierReview.exportPacket().comments').pop()['targets']) >= 3
                page.locator('#review-drawer .review-panel-heading button').click()
                candidates.nth(0).hover();page.locator('#review-block-select').click()
                candidates.nth(2).hover();page.locator('#review-block-select').click(modifiers=['Control'])
                assert page.locator('.review-selected').count() == 2
                page.locator('#review-clear-selection').click()
                assert candidates.evaluate_all('(els)=>els.map(el=>el.dataset.reviewBlock)') == ids

                candidates.nth(0).focus();page.keyboard.press('Control+Alt+m')
                expect(page.locator('#review-text')).to_be_focused()
                page.locator('#review-text').fill('Keyboard-accessible source comment.');page.locator('#review-save').click()
                page.locator('#review-drawer .review-panel-heading button').click()
                candidates.nth(0).hover();handle=page.locator('#review-block-select').bounding_box()
                destination=candidates.nth(2).bounding_box()
                page.mouse.move(handle['x']+handle['width']/2,handle['y']+handle['height']/2)
                page.mouse.down();page.mouse.move(destination['x']+10,destination['y']+8,steps=8);page.mouse.up()
                assert page.locator('.review-selected').count() >= 3
                assert candidates.evaluate_all('(els)=>els.map(el=>el.dataset.reviewBlock)') == ids
                page.locator('#review-clear-selection').click()

                page.locator('#review-document-note').click();page.locator('#review-text').fill('Document-level observation.');page.locator('#review-save').click()
                assert page.evaluate('FrontierReview.exportPacket().comments').pop()['scope'] == 'document'
                page.locator('#review-drawer .review-panel-heading button').click()
                page.locator('#review-search-open').click();page.locator('#review-global-search').fill('memory')
                assert page.locator('#review-search-results li').count()>0
                page.locator('#review-search-dialog button').click()

                for tag, selector in [('heading','h3[data-review-block]'),('list','ul[data-review-block],ol[data-review-block]'),('table','.table-wrap[data-review-block],table[data-review-block]'),('diagram','figure[data-review-block]')]:
                    target=page.locator(selector).first
                    assert target.count(), 'No source-backed '+tag
                    ident=target.get_attribute('id');target_id=target.get_attribute('data-review-block')
                    page.goto(base+'/guides/devops.html?annotation-kind='+tag+'#'+ident)
                    page.wait_for_function('!!window.FrontierReview')
                    target=page.locator('[id="'+ident+'"]')
                    expect(target).to_be_visible();target.hover()
                    if tag=='diagram':target.focus()
                    expect(page.locator('#review-block-controls')).to_have_attribute('data-block-id',target_id)
                    page.locator('#review-block-comment').click()
                    expect(page.locator('#review-text')).to_be_visible()
                    page.locator('#review-drawer .review-panel-heading button').click()
                    bounds=page.locator('#review-block-controls').bounding_box()
                    assert bounds is None or bounds['x']>=0 and bounds['x']+bounds['width']<=width+1

                page.goto(base+'/presentations/devops.html');page.wait_for_function('!!window.FrontierReview')
                title=page.locator('.slide:visible h1[data-review-block]');title.hover();page.locator('#review-block-comment').click()
                page.locator('#review-text').fill('Slide-title comment.');page.locator('#review-save').click()
                assert '/presentations/devops/' in page.evaluate('FrontierReview.exportPacket().comments').pop()['targets'][0]['path']
                page.locator('#review-drawer .review-panel-heading button').click();page.locator('#notes-button').click()
                speaker=page.locator('.note-block:visible .talk-track > p[data-review-block]').first
                speaker.focus();page.keyboard.press('Control+Alt+m');page.locator('#review-text').fill('Presenter note comment.');page.locator('#review-save').click()
                assert '/presentations/devops/' in page.evaluate('FrontierReview.exportPacket().comments').pop()['targets'][0]['path']
                page.locator('#review-drawer .review-panel-heading button').click()
                page.locator('#review-notes-open').click();page.locator('.review-io summary').click()
                incoming=page.evaluate('FrontierReview.exportPacket()');item=deepcopy(incoming['comments'][-1])
                item['id']='import-test';item['body']='<img src=x onerror=alert(1)>';item['targets'][0]['file_sha256']='0'*64;incoming['comments']=[item]
                page.locator('#review-import').set_input_files({'name':'review.json','mimeType':'application/json','buffer':json.dumps(incoming).encode()})
                expect(page.locator('.review-warning').first).to_be_visible()
                assert page.locator('#review-drawer img').count()==0
                with page.expect_download() as dl:page.locator('#review-export').click()
                downloaded=json.loads(Path(dl.value.path()).read_text())
                assert downloaded['schema']=='frontier-review/v1' and downloaded['review_id']==packet['review_id']
                page.emulate_media(media='print');expect(page.locator('#review-drawer')).to_be_hidden();page.emulate_media(media='screen')
                page.goto(base+'/catalog/UC-D02.html');page.wait_for_function('!!window.FrontierReview')
                assert page.locator('.case-narrative [data-review-block]').count()>0
                assert not external,external
                assert not errors,errors
                reports.append({'viewport':width,'mode_switch_absent':'passed','hover_and_element_threads':'passed','persistent_markers_reply_resolve_reopen':'passed',
                    'quote_range_additive_drag_and_keyboard_selection':'passed','source_text_and_block_order_preserved':'passed',
                    'heading_list_table_diagram_slide_and_notes':'passed','global_search':'passed','export_import_stale_hash_and_inert_comment_html':'passed',
                    'print_controls_hidden':'passed','external_requests':external,'javascript_errors':errors})
                context.close()
            context=browser.new_context(viewport={'width':390,'height':900},is_mobile=True,has_touch=True)
            page=context.new_page();page.goto(base+'/guides/devops.html');page.wait_for_function('!!window.FrontierReview')
            target=page.locator('.report-section:visible p[data-review-block]').first;target.tap()
            expect(page.locator('#review-block-comment')).to_be_visible();page.locator('#review-block-comment').tap()
            page.locator('#review-text').fill('Touch annotation.');page.locator('#review-save').tap()
            assert len(page.evaluate('FrontierReview.exportPacket().comments'))==1
            reports.append({'touch_tap_annotation':'passed'});context.close()
            page=browser.new_page();page.goto((root/'guides/devops.html').as_uri());page.wait_for_function('!!window.FrontierReview')
            page.locator('#review-search-open').click();page.locator('#review-global-search').fill('memory');assert page.locator('#review-search-results li').count()>0
            reports.append({'file_url_search':'passed'});browser.close()
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
    return reports
