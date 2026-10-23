"""Validate the reading architecture without changing the approved concepts."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
import hashlib
import json
import subprocess
from bs4 import BeautifulSoup
from reader import BASELINE, RETIRED, Reader, NAMES
from structure import CHAPTERS

ROOT=Path(__file__).resolve().parents[2]
FROZEN=('use-cases','mechanisms','features','profiles','aliases','resource-models')


def validate(guides,browser=False):
    errors=[];protected={};results=[]
    for name in FROZEN:
        rel='catalog/'+name+'.json'
        old=subprocess.check_output(['git','show',BASELINE+':'+rel],cwd=ROOT)
        now=(ROOT/rel).read_bytes()
        protected[rel]={'unchanged':old==now,'sha256':hashlib.sha256(now).hexdigest()}
        if old!=now:errors.append('Frozen source changed: '+rel)
    r=Reader(guides,None,None)
    for path in RETIRED:
        if (ROOT/path).exists():errors.append('Retired reader page remains: '+path)
    for path in (ROOT/'tools/docs').glob('apply_*'):
        errors.append('Temporary migration source remains: '+path.name)
    pages=[ROOT/'index.html',ROOT/'catalog/index.html',ROOT/'catalog/resource-models.html',ROOT/'presentations/index.html']
    pages += [ROOT/f'guides/{p}.html' for p in guides]
    pages += [ROOT/f'catalog/{c["id"]}.html' for c in r.cases]
    for path in pages:
        soup=BeautifulSoup(path.read_text(),'html.parser')
        if len(soup.select('main'))!=1 or len(soup.select('h1'))!=1:errors.append(str(path)+': expected one main and one page heading')
        nav=soup.select_one('nav[aria-label="Main navigation"]')
        if not nav or [a.get_text() for a in nav.select('a')]!=['Guides','Use cases','Resource model','Presentations']:errors.append(str(path)+': reader navigation is inconsistent')
        for a in soup.select('a[href]'):
            if any(a['href'].split('#')[0].endswith(p.split('/')[-1]) for p in RETIRED):errors.append(str(path)+': link to retired record page '+a['href'])
    for p,g in guides.items():
        page=BeautifulSoup((ROOT/f'guides/{p}.html').read_text(),'html.parser')
        if page.select('.usecase-entry,[data-usecase-catalog],.embedded-catalog'):errors.append(p+': full duplicate catalog remains')
        if len(page.select('input[type="search"]'))!=1:errors.append(p+': competing searches remain')
        if len(page.select('[data-reader-chapter]'))!=len(CHAPTERS[p]):errors.append(p+': missing chapter')
        for m in r.mechanisms.values():
            if m['platform']==p and not page.find(id=m['id']):errors.append('Missing mechanism destination '+m['id'])
        for f in r.features.values():
            if f['platform']==p and not page.find(id=f['id']):errors.append('Missing feature destination '+f['id'])
    for case in r.cases:
        page=BeautifulSoup((ROOT/f'catalog/{case["id"]}.html').read_text(),'html.parser')
        if [p.get_text() for p in page.select('.case-narrative p')]!=case['narrative']:errors.append(case['id']+': approved narrative changed in presentation')
        steps=page.select('.workflow-steps>li')
        if len(steps)!=len(case['workflow']):errors.append(case['id']+': workflow step missing')
        for expected,actual in zip(case['workflow'],steps):
            if actual.h3.get_text()!=expected['title']:errors.append(case['id']+': workflow order changed')
            for field in ('purpose','condition','effect','verification','on_failure'):
                if expected[field] not in actual.get_text(' ',strip=True):errors.append(case['id']+': hidden workflow requirement '+field)
        for pid in case['profiles']:
            node=page.find(id=pid)
            if not node:errors.append(case['id']+': configuration missing '+pid);continue
            p=r.profiles[pid]
            for text in p['setup']+p['tests']+[p['stop_behavior']]:
                if text not in node.get_text(' ',strip=True):errors.append(case['id']+': configuration content omitted')
        if set(x['id'] for x in page.select('main>section'))!={'context','workflow','configuration','verification','references'}:errors.append(case['id']+': broken article hierarchy')
    if browser and not errors:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for width in (390,1440):
                page=br.new_page(viewport={'width':width,'height':1000});js=[]
                page.on('pageerror',lambda e:js.append(str(e)))
                try:
                    for p,g in guides.items():
                        page.goto((ROOT/f'guides/{p}.html').as_uri())
                        assert page.locator('.chapter:visible').count()==1,'Guide must start with one chapter'
                        assert page.locator('.report-section:visible').count()==len(CHAPTERS[p][0]['sections'])
                        page.locator('#next-chapter').click()
                        page.wait_for_function('(id)=>document.querySelector(".chapter:not([hidden])").id===id',arg='chapter-'+CHAPTERS[p][1]['slug'])
                        assert page.locator('.chapter:visible').get_attribute('id')=='chapter-'+CHAPTERS[p][1]['slug']
                        page.locator('#previous-chapter').click()
                        page.wait_for_function('(id)=>document.querySelector(".chapter:not([hidden])").id===id',arg='chapter-'+CHAPTERS[p][0]['slug'])
                        page.locator('#read-all').check();assert page.locator('.chapter:visible').count()==len(CHAPTERS[p])
                        page.locator('#read-all').uncheck()
                        page.locator('#guide-search').fill('nonexistent-zz928');assert page.locator('.report-section:visible').count()==0
                        assert page.locator('#guide-empty').is_visible()
                        mid=next((m['id'] for m in r.mechanisms.values() if m['platform']==p),None)
                        dest=mid or list(g['sections'])[-1]
                        page.evaluate('(id)=>location.hash=id',dest)
                        page.wait_for_function('(id)=>{const n=document.getElementById(id);return n&&!n.closest(".chapter").hidden}',arg=dest)
                        assert page.locator('#'+dest).is_visible(),'Deep link must clear search and reveal chapter'
                        assert page.locator('#guide-search').input_value()==''
                        page.reload();assert page.locator('#'+dest).is_visible(),'Reload must preserve deep link'
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                        page.emulate_media(media='print');assert page.locator('.report-section:visible').count()==len(g['sections'])
                        page.emulate_media(media='screen');assert page.locator('.chapter:visible').count()==1
                    page.goto((ROOT/'catalog/index.html').as_uri())
                    assert page.locator('.case-index-entry:visible').count()==30
                    page.locator('#case-product').select_option('devops');assert page.locator('.case-index-entry:visible').count()==15
                    page.locator('#case-search').fill('SOP');assert page.locator('.case-index-entry:visible').count()>0
                    page.locator('#case-search').fill('nonexistent-zz928');assert page.locator('#case-empty').is_visible()
                    page.locator('.catalog-search button').click();assert page.locator('.case-index-entry:visible').count()==30
                    page.goto((ROOT/'catalog/index.html').as_uri()+'#D-UC03');page.wait_for_url('**/UC-D02.html#UC-D02')
                    assert page.locator('h1').inner_text()==next(c['title'] for c in r.cases if c['id']=='UC-D02')
                    page.goto((ROOT/'catalog/index.html').as_uri()+'#F-UC04')
                    assert page.locator('#F-UC04').is_visible() and page.locator('#F-UC04 a').count()==2
                    # Complete reading journey: task -> configuration -> mechanism -> product chapter -> task.
                    page.goto((ROOT/'catalog/UC-D06.html').as_uri())
                    page.locator('#workflow a[href="../guides/devops.html#MX-D-RECALL"]').click()
                    assert page.locator('#MX-D-RECALL').is_visible()
                    page.goto((ROOT/'guides/devops.html').as_uri()+'#FT-D-MEMORY')
                    assert page.locator('#FT-D-MEMORY').get_attribute('open') is not None
                    page.locator('#FT-D-MEMORY a[href="../catalog/UC-D06.html#UC-D06"]').click()
                    assert page.locator('#configuration').is_visible()
                    for case in r.cases:
                        page.goto((ROOT/f'catalog/{case["id"]}.html').as_uri())
                        assert page.locator('.case-narrative p').count()==len(case['narrative'])
                        assert page.locator('.workflow-steps>li').count()==len(case['workflow'])
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2'),case['id']+' horizontal overflow'
                        for pid in case['profiles']:assert page.locator('#'+pid).is_visible()
                    assert not js,js
                    results.append({'width':width,'guide_chapters_search_deep_links_reload_print':'passed','case_search_grouping_and_legacy_choices':'passed','workflow_configuration_procedure_return_journey':'passed','all_30_case_pages':'passed','javascript_errors':js})
                except Exception as exc:
                    import traceback
                    errors.append('Reading journey '+str(width)+' at '+page.url+': '+str(exc)+'; JavaScript='+str(js)+'; '+traceback.format_exc(limit=2))
                finally:page.close()
            br.close()
    result={'revision':'2026-10-23-reading-structure','baseline':BASELINE,'scope':'Navigation and reader composition only; concept definitions and use-case semantics remain frozen.',
            'frozen_sources':protected,'reader_pages_checked':len(pages),'use_case_pages':len(r.cases),'guide_chapters':sum(len(c) for c in CHAPTERS.values()),
            'retired_reader_pages':list(RETIRED),'browser':results,'errors':errors,
            'boundary':'Structural, preservation and browser checks do not establish content completeness or live AWS execution.'}
    (ROOT/'qa/reading-structure.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
