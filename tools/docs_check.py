#!/usr/bin/env python3
"""Check content preservation, grouped navigation and native HTML presentations."""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from decimal import Decimal
import yaml
from pathlib import Path
from urllib.parse import unquote, urlsplit
from bs4 import BeautifulSoup
from docs_build import ROOT, DECKS, load_guides, parse_source, semantic_hash, ordered_ids, write, REVISION, MD
from docs_structure import CHAPTERS, DECK_CHAPTERS, BASELINE


def git(*args): return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()

def check(browser=False):
    guides=load_guides();errors=[];links=0;preserved=0;browser_results=[]
    for key,g in guides.items():
        old=parse_source(git('show',f'{BASELINE}:guides/{key}.md'))
        if g['refs'] != old['refs']:errors.append(key+': source register changed')
        if set(g['sections']) != set(old['sections']):errors.append(key+': section set changed')
        for sid,s in g['sections'].items():
            if sid not in old['sections'] or s['title']!=old['sections'][sid]['title'] or semantic_hash(s,g['definitions'])!=semantic_hash(old['sections'][sid],old['definitions']):
                errors.append(sid+': canonical content changed')
            else:preserved+=1
        soup=BeautifulSoup((ROOT/f'guides/{key}.html').read_text(),'html.parser')
        if [s['id'] for s in soup.select('.report-section')] != ordered_ids(key):errors.append(key+': section order')
        if len(soup.select('.chapter')) != len(CHAPTERS[key]):errors.append(key+': chapter count mismatch')
        expected_toc = len(CHAPTERS[key]) + (1 if key in {'devops','security','finops'} else 0)
        if len(soup.select('.toc details')) != expected_toc:errors.append(key+': chapter navigation mismatch')
        if len(soup.select('.toc a[data-section]')) != len(g['sections']):errors.append(key+': incomplete table of contents')
        deck=BeautifulSoup((ROOT/f'presentations/{key}.html').read_text(),'html.parser')
        if len(deck.select('.slide')) != len(DECKS[key]['slides']):errors.append(key+': slide count')
        if len(deck.select('.note-block')) != len(DECKS[key]['slides']):errors.append(key+': missing notes')
        if len(deck.select('.chapter-strip button')) != len(DECK_CHAPTERS[key]):errors.append(key+': missing presentation chapters')
        for actual,expected in zip(deck.select('.slide'),DECKS[key]['slides']):
            if int(actual['data-seconds'])!=expected['seconds']:errors.append(key+': timing changed')
            if actual.h1.get_text()!=expected['title']:errors.append(key+': slide title changed')
            for ref in expected['refs']:
                if ref not in g['sections']:errors.append(key+': invalid slide reference '+ref)
    for key,deck_definition in DECKS.items():
        titles=[slide['title'] for slide in deck_definition['slides']]
        if len(titles)!=len(set(titles)):errors.append(key+': duplicate slide title')
        if any(len(slide.get('data',[]))<3 for slide in deck_definition['slides'] if slide['kind']!='demo'):errors.append(key+': sparse slide outline')
    if list((ROOT/'presentations').glob('*.pptx')):errors.append('Binary presentation outputs remain')
    for folder in ['archive','dist']:
        if (ROOT/folder).exists():errors.append('Manual distribution/history directory: '+folder)
    html_files=[p for p in ROOT.rglob('*.html') if 'applications' not in p.relative_to(ROOT).parts and '.git' not in p.parts]
    for p in html_files:
        soup=BeautifulSoup(p.read_text(),'html.parser');ids=[t['id'] for t in soup.select('[id]')]
        if len(ids)!=len(set(ids)):errors.append(str(p.relative_to(ROOT))+': duplicate IDs')
        for tag in soup.select('a[href]'):
            u=urlsplit(tag['href'])
            if u.scheme or u.netloc:continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            links+=1
            if target.suffix=='.pptx':errors.append('Binary presentation link: '+str(p.relative_to(ROOT)))
            if not target.exists():errors.append('Broken link: '+str(p.relative_to(ROOT))+' -> '+tag['href'])
            elif u.fragment and target.suffix=='.html' and not BeautifulSoup(target.read_text(),'html.parser').find(id=unquote(u.fragment)):errors.append('Broken anchor: '+tag['href'])
    changed=git('diff','--name-only',BASELINE,'--','applications','.github/workflows/validation-console.yml')
    if changed:errors.append('Unrelated application changes: '+changed)
    fixture_results=[]
    evidence=json.loads((ROOT/'examples/prepared-evidence.json').read_text())
    f=evidence['finops'];assert f['rates_are_not_aws_prices'] and f['same_account_service_and_cost_basis']
    baseline=comparison=Decimal('0')
    for row in f['rows']:
        assert Decimal(row['baseline_quantity'])*Decimal(row['unit_rate'])==Decimal(row['baseline_cost'])
        assert Decimal(row['comparison_quantity'])*Decimal(row['unit_rate'])==Decimal(row['comparison_cost'])
        baseline+=Decimal(row['baseline_cost']);comparison+=Decimal(row['comparison_cost'])
    assert (baseline,comparison,comparison-baseline,(comparison-baseline)/baseline*100)==tuple(Decimal(f[a]) for a in ('expected_baseline','expected_comparison','expected_delta','expected_percent_change'))
    assert Decimal(f['prepared_job_log_additional_transfer_units'])*Decimal(f['rows'][2]['unit_rate'])==Decimal('274')
    rendered=BeautifulSoup(MD.render((ROOT/'guides/finops.md').read_text()),'html.parser')
    table=next(t for t in rendered.select('table') if t.select_one('th') and t.select_one('th').get_text()=='Component')
    for tr,row in zip(table.select('tbody tr')[:3],f['rows']):
        assert [td.get_text().replace(',','').strip() for td in tr.select('td')]==[row[a] for a in ('component','baseline_quantity','comparison_quantity','unit_rate','baseline_cost','comparison_cost')]
    fixture_results.append('FinOps quantity/rate arithmetic and guide-table consistency')
    dv=evidence['devops'];assert dv['prior']['database_connections']==dv['prior']['database_limit'];assert dv['current']['database_connections']<dv['current']['database_limit'];assert dv['current']['inventory_p95_ms']>dv['prior']['inventory_p95_ms'];assert dv['current']['database_query_p95_ms']<dv['prior']['database_query_p95_ms']
    fixture_results.append('DevOps contradictory current evidence')
    se=evidence['security'];assert se['proposed_revision']==se['deployed_revision'];assert se['test_identity']==se['prepared_revalidation_identity'];assert se['original_revision']!=se['deployed_revision']
    fixture_results.append('Security revision and identity consistency')
    for key in guides:
        raw=(ROOT/f'guides/{key}.md').read_text()
        for token in MD.parse(raw):
            if token.type=='fence' and token.info.strip()=='yaml':yaml.safe_load(token.content)
            if token.type=='fence' and token.content.startswith('---\nname:'):yaml.safe_load(token.content.split('---',2)[1])
    prior='c1c810b48e2349d3fb2479402c767a2834c76b9a'
    old=json.loads(git('show',prior+':content/narratives.json'))['agents']
    terms={v['title'].casefold() for k,v in old.items() if k not in DECKS}
    olde=json.loads(git('show',prior+':content/devops-evidence.json'))
    for cap in olde.get('capabilities',[]):
        product=cap.get('product','')
        if product and product not in {'AWS DevOps Agent','AWS Security Agent','AWS FinOps Agent'}:terms.update([product.casefold(),product.removesuffix(' Developer').casefold()])
    scope_hits=[]
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(x in path.parts for x in ('applications','.git','__pycache__')):continue
        rel=path.relative_to(ROOT).as_posix()
        if path.suffix in {'.zip','.bundle','.b64','.gz','.tar'}:errors.append('Stored distribution: '+rel)
        try:text=path.read_text()
        except UnicodeDecodeError:continue
        if any(t and t in (rel+' '+text).casefold() for t in terms):scope_hits.append(rel)
    errors.extend('Excluded scope: '+x for x in scope_hits)
    if browser:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for key,g in guides.items():
                for width in (390,1440):
                    page=br.new_page(viewport={'width':width,'height':1000});js_errors=[]
                    page.on('pageerror',lambda e:js_errors.append(str(e)))
                    page.goto((ROOT/f'guides/{key}.html').as_uri(),wait_until='load')
                    n=len(g['sections'])
                    assert page.locator('.report-section:visible').count()==n
                    page.locator('#search').fill('unmatchable-zz867');assert page.locator('.report-section:visible').count()==0
                    assert page.locator('#empty-results').is_visible()
                    page.locator('#reset').click()
                    first=CHAPTERS[key][0]
                    page.locator('#chapter').select_option(first['slug']);assert page.locator('.report-section:visible').count()==len(first['sections'])
                    page.locator('#reset').click();page.locator('#type').select_option('mechanism');assert page.locator('.report-section:visible').count()>0
                    page.emulate_media(media='print');assert page.locator('.report-section:visible').count()==n
                    page.emulate_media(media='screen');assert page.locator('.report-section:visible').count()<n
                    page.locator('#nav-collapse').click();assert page.locator('.toc details[open]').count()==0
                    sid=ordered_ids(key)[0];page.evaluate('(id)=>location.hash=id',sid);page.wait_for_timeout(150)
                    assert page.locator('#'+sid).is_visible();assert page.locator('.toc details[open]').count()>0
                    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                    page.locator('#reset').click()
                    page.locator('a[href="../presentations/'+key+'.html"]').first.click();page.wait_for_load_state('load')
                    assert page.locator('.slide:visible').count()==1
                    for i in range(len(DECKS[key]['slides'])):
                        page.locator('#slide-select').select_option(str(i))
                        assert page.locator('.slide:visible').count()==1
                        assert page.locator('.slide:visible h1').inner_text()==DECKS[key]['slides'][i]['title']
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),(key,width,i)
                    page.locator('#agenda-open').click();assert page.locator('#agenda').is_visible()
                    page.locator('#agenda [data-slide="0"]').click();assert not page.locator('#agenda').is_visible()
                    assert page.locator('#slide-select').input_value()=='0'
                    page.locator('#next').focus();page.keyboard.press('ArrowRight');assert page.locator('#slide-select').input_value()=='1'
                    page.locator('.chapter-strip button').nth(2).click();assert page.locator('#slide-select').input_value()==str(DECK_CHAPTERS[key][2][1][0])
                    page.locator('#notes-button').click();assert page.locator('.note-block:visible').count()==1
                    page.locator('#speaker-notes summary').click()
                    page.locator('#timer-toggle').click();page.wait_for_function("!document.querySelector('#session-time').textContent.startsWith('00:00')",timeout=5000)
                    page.locator('#timer-toggle').click();paused=page.locator('#session-time').inner_text();page.wait_for_timeout(450);assert page.locator('#session-time').inner_text()==paused
                    page.locator('#timer-reset').click();assert page.locator('#session-time').inner_text().startswith('00:00')
                    current=page.locator('#slide-select').input_value();page.reload();assert page.locator('#slide-select').input_value()==current
                    page.emulate_media(media='print');assert page.locator('.slide:visible').count()==len(DECKS[key]['slides']);assert not page.locator('.deck-toolbar').first.is_visible()
                    page.emulate_media(media='screen');assert page.locator('.slide:visible').count()==1
                    errors.extend(js_errors);browser_results.append({'subject':key,'width':width,'report_chapters':len(CHAPTERS[key]),'slide_count':len(DECKS[key]['slides']),'javascript_errors':js_errors,'search_chapter_type_deeplinks_notes_timers_print':'passed'})
                    page.close()
            for rel in ['index.html','presentations/index.html']:
                for width in (390,1440):
                    page=br.new_page(viewport={'width':width,'height':1000});page.goto((ROOT/rel).as_uri());assert page.locator('.index-card').count()==5;assert page.locator('#use-case-catalog-card').count()==1
                    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2');page.close()
            br.close()
    results={'revision':REVISION,'baseline':BASELINE,'reports':4,'report_chapters':sum(len(c) for c in CHAPTERS.values()),'canonical_sections_preserved':preserved,'canonical_content_and_sources_unchanged':not any('content changed' in e or 'source register changed' in e for e in errors),'html_presentations':4,'timed_slides':sum(len(d['slides']) for d in DECKS.values()),'programme_minutes':sum(s['seconds'] for d in DECKS.values() for s in d['slides'])//60,'exercise_minutes':sum(s['seconds'] for d in DECKS.values() for s in d['slides'] if s['kind']=='demo')//60,'html_files_checked':len(html_files),'local_links_checked':links,'binary_presentations_remaining':len(list((ROOT/'presentations').glob('*.pptx'))),'browser_checks':browser_results,'synthetic_fixture_checks':fixture_results,'excluded_scope_hits':scope_hits,'application_changes':changed.splitlines(),'errors':errors,'boundary':'Organization, preserved source content, HTML behavior and timing checks only. No new external product audit or live AWS execution.'}
    write('qa/checks.json',json.dumps(results,indent=2)+'\n')
    if errors:raise SystemExit(json.dumps(results,indent=2))
    write('VALIDATION.md','# Structured HTML validation\n\nResults are in [qa/checks.json](qa/checks.json). The checks compare every canonical section body and official source register with the pinned previous publication, check chapter membership, nested navigation, links, speaker notes and slide budgets, and verify that no binary presentation outputs remain.\n\nBrowser tests use real local HTML navigation at 390 and 1440 pixels. They exercise search, chapter and type filters, chapter expansion, section links, all slides, agendas, keyboard navigation, notes, paused/reset timers, persistent slide links and print-state restoration. These tests do not establish product-documentation correctness or successful AWS operation.\n\nThe separate application and its workflow are checked for unchanged content. The current presentation duration and prepared-result exercise allocation are recorded in `qa/checks.json`. Git holds prior revisions; no manual archives are created.\n')
    files={}
    roots=['guides','presentations','tools','qa','examples','devops','security','finops','architecture','mechanisms','platforms']
    paths=[ROOT/n for n in ['README.md','CHANGELOG.md','VALIDATION.md','PUBLISHING.md','EDITORIAL_STANDARD.md','SCOPE.md','index.html','documentation-build.json','.github/workflows/document-suite.yml']]
    for folder in roots: paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    for p in sorted(set(paths)):
        if p.is_file():files[p.relative_to(ROOT).as_posix()]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    write('MANIFEST.json',json.dumps({'revision':REVISION,'files':files,'excluded':['MANIFEST.json itself','applications/','.git/','__pycache__/']},indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--browser',action='store_true');a=p.parse_args();check(a.browser)
