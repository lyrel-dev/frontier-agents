#!/usr/bin/env python3
"""Validate the current documentation, independently of live AWS operation."""
from __future__ import annotations
import argparse
import traceback
import hashlib
import json
import re
import subprocess
from collections import Counter
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote,urlsplit
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
from build import ROOT,DECKS,CHAPTERS,DECK_CHAPTERS,REVISION,load_guides,load_catalog,ordered_ids,parse_source,write,totals
from diagrams import DIAGRAMS
from structure import BASELINE
from model_check import validate_model


def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()

def file_manifest():
    roots=('guides','catalog','presentations','assets','examples','tools/docs','qa')
    paths=[ROOT/p for p in ('README.md','EDITORIAL_STANDARD.md','CHANGELOG.md','PUBLISHING.md','SCOPE.md','VALIDATION.md','index.html','documentation-build.json','.github/workflows/document-suite.yml')]
    for root in roots:paths.extend(p for p in (ROOT/root).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    return {p.relative_to(ROOT).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(paths)) if p.exists()}

def check(browser=False):
    errors=[];guides=load_guides();catalog=load_catalog();entries=catalog['entries'];browser_results=[]
    html_paths=[ROOT/'catalog/mechanisms.html',ROOT/'catalog/features.html',ROOT/'catalog/profiles.html',ROOT/'index.html',ROOT/'catalog/index.html',ROOT/'presentations/index.html',*(ROOT/f'guides/{k}.html' for k in guides),*(ROOT/f'presentations/{k}.html' for k in guides)]
    parsed={p.resolve():BeautifulSoup(p.read_text(),'html.parser') for p in html_paths}
    previous_ids=[];new_ids=[];link_count=0;figures=0
    for key,g in guides.items():
        old=parse_source(git('show',f'{BASELINE}:guides/{key}.md'))
        previous_ids.extend(old['sections']);new_ids.extend(g['sections'])
        if not set(old['sections'])<=set(g['sections']):errors.append(key+': previous stable section identifiers were removed')
        if len(ordered_ids(key))!=len(set(ordered_ids(key))):errors.append(key+': duplicate chapter membership')
        for sid,s in g['sections'].items():
            if not s['body'].strip():errors.append(sid+': empty explanation')
            if not s['sources'] and '-U' not in sid:errors.append(sid+': no official source mapping')
            if s['body'].lstrip().startswith('|'):errors.append(sid+': table precedes conceptual explanation')
        for ref,url in g['refs'].items():
            host=urlsplit(url).hostname or ''
            if not(host=='docs.aws.amazon.com' or host=='aws.amazon.com'):errors.append(ref+': source is not an official AWS page')
        page=parsed[(ROOT/f'guides/{key}.html').resolve()]
        if [n['id'] for n in page.select('.report-section')]!=ordered_ids(key):errors.append(key+': rendered chapter order differs from source')
        if len(page.select('.toc a[data-section]'))!=len(g['sections']):errors.append(key+': incomplete technical contents')
        if key!='architecture':
            expected=sum(key in e.get('platforms',[e['platform']]) for e in entries)
            if len(page.select('.usecase-entry'))!=expected:errors.append(key+': embedded narrative count')
            if str(page).find('id="use-case-catalog"')<str(page).rfind('class="chapter"'):errors.append(key+': catalog interrupts technical chapters')
        deck=parsed[(ROOT/f'presentations/{key}.html').resolve()]
        if len(deck.select('.slide'))!=len(DECKS[key]['slides']):errors.append(key+': slide count mismatch')
        if len(deck.select('.note-block'))!=len(DECKS[key]['slides']):errors.append(key+': missing presenter notes')
        for actual,s in zip(deck.select('.slide'),DECKS[key]['slides']):
            if actual.h1.get_text()!=s['title'] or int(actual['data-seconds'])!=s['seconds']:errors.append(key+': slide source mismatch')
            if not set(s['refs'])<=set(g['sections']):errors.append(key+': invalid detailed reference')
            if s['kind']=='diagram' and not actual.select_one('svg[role=img]'):errors.append(key+': diagram slide has no accessible SVG')
        titles=[s['title'].casefold() for s in DECKS[key]['slides']]
        if len(titles)!=len(set(titles)):errors.append(key+': duplicate slide title')
        if [i for _,items in DECK_CHAPTERS[key] for i in items]!=list(range(len(titles))):errors.append(key+': incomplete presentation chapters')
    if len(new_ids)!=len(set(new_ids)):errors.append('Canonical identifiers are not unique')
    source_narratives=[]
    for e in entries:
        if e['platform'] not in guides:errors.append(e['id']+': unknown product')
        if not set(e['sections'])<=set(guides[e['platform']]['sections']):errors.append(e['id']+': unknown canonical reference')
        if len(e.get('narrative',[]))<2:errors.append(e['id']+': missing connected narrative')
        source_narratives.extend(e.get('narrative',[]))
        if e['group'] not in catalog['group_introductions']:errors.append(e['id']+': group has no introduction')
    if len(source_narratives)!=len(set(source_narratives)):errors.append('Catalog reuses identical narrative paragraphs')
    if len({e['id'] for e in entries})!=len(entries):errors.append('Duplicate use-case identifiers')
    catalog_page=parsed[(ROOT/'catalog/index.html').resolve()]
    if len(catalog_page.select('.narrative p'))!=len(source_narratives):errors.append('Narrative paragraphs missing from catalog HTML')
    for path,page in parsed.items():
        identifiers=[n['id'] for n in page.select('[id]')]
        if len(identifiers)!=len(set(identifiers)):errors.append(str(path.relative_to(ROOT))+': duplicate HTML/SVG identifiers')
        for tag in page.select('a[href],img[src]'):
            address=tag.get('href',tag.get('src'));u=urlsplit(address)
            if u.scheme or u.netloc:continue
            target=(path.parent/unquote(u.path)).resolve() if u.path else path
            link_count+=1
            if not target.exists():errors.append(str(path.relative_to(ROOT))+': missing target '+address);continue
            if u.fragment and target.suffix=='.html':
                target_page=parsed.get(target)
                if target_page is None:target_page=BeautifulSoup(target.read_text(),'html.parser');parsed[target]=target_page
                if not target_page.find(id=unquote(u.fragment)):errors.append(str(path.relative_to(ROOT))+': missing anchor '+address)
        for fig in page.select('figure.diagram'):
            figures+=1;svg=fig.find('svg')
            if not svg or not fig.find('figcaption'):errors.append(str(path.relative_to(ROOT))+': missing diagram or caption');continue
            if svg.get('role')!='img':errors.append('SVG missing image role')
            for ident in svg.get('aria-labelledby','').split():
                if not svg.find(id=ident):errors.append('SVG accessibility identifier does not resolve: '+ident)
    for key in DIAGRAMS:
        try:ET.parse(ROOT/f'assets/diagrams/{key}.svg')
        except Exception as exc:errors.append(key+': invalid standalone SVG '+str(exc))
    for name in ('devops','security','finops','architecture','mechanisms','platforms','archive','dist'):
        if (ROOT/name).exists():errors.append('Superseded directory remains: '+name)
    if list((ROOT/'tools').glob('*.py')):errors.append('Superseded or migration Python file remains in tools root')
    if list((ROOT/'presentations').glob('*.pptx')):errors.append('Binary presentation remains')
    terms=['ki'+'ro','amazon '+'q'];scope_hits=[]
    for path in ROOT.rglob('*'):
        if not path.is_file() or any(p in ('.git','applications','__pycache__') for p in path.relative_to(ROOT).parts):continue
        if path.suffix in ('.zip','.b64','.bundle','.tar','.gz'):errors.append('Stored archive or encoded package: '+str(path.relative_to(ROOT)))
        try:text=path.read_text()
        except UnicodeDecodeError:continue
        if any(term in text.casefold() for term in terms):scope_hits.append(str(path.relative_to(ROOT)))
    errors.extend('Excluded product reference: '+p for p in scope_hits)
    app_changes=git('diff','--name-only',BASELINE,'--','applications','.github/workflows/validation-console.yml').splitlines()
    if app_changes:errors.append('Unrelated application changed')
    evidence=json.loads((ROOT/'examples/prepared-evidence.json').read_text());f=evidence['finops'];baseline=comparison=Decimal('0')
    for row in f['rows']:
        assert Decimal(row['baseline_quantity'])*Decimal(row['unit_rate'])==Decimal(row['baseline_cost'])
        assert Decimal(row['comparison_quantity'])*Decimal(row['unit_rate'])==Decimal(row['comparison_cost'])
        baseline+=Decimal(row['baseline_cost']);comparison+=Decimal(row['comparison_cost'])
    assert (baseline,comparison,comparison-baseline,(comparison-baseline)/baseline*100)==tuple(Decimal(f[a]) for a in ('expected_baseline','expected_comparison','expected_delta','expected_percent_change'))
    d=evidence['devops'];assert d['current']['database_connections']<d['current']['database_limit'];assert d['current']['inventory_p95_ms']>d['prior']['inventory_p95_ms']
    s=evidence['security'];assert s['deployed_revision']==s['proposed_revision'];assert s['test_identity']==s['prepared_revalidation_identity']
    model_result=validate_model(guides, browser=browser)
    errors.extend(model_result["errors"])
    if browser and not errors:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for key,g in guides.items():
                for width in (390,1440):
                    page=br.new_page(viewport={'width':width,'height':1000});js_errors=[]
                    page.on('pageerror',lambda err:js_errors.append(str(err)))
                    try:
                        page.goto((ROOT/f'guides/{key}.html').as_uri(),wait_until='load')
                        n=len(g['sections']);assert page.locator('.report-section:visible').count()==n
                        page.locator('#search').fill('nonexistent-zz928');assert page.locator('.report-section:visible').count()==0
                        assert page.locator('#empty-results').is_visible();page.locator('#reset').click()
                        page.locator('#chapter').select_option(CHAPTERS[key][0]['slug']);assert page.locator('.report-section:visible').count()==len(CHAPTERS[key][0]['sections'])
                        page.locator('#reset').click();page.locator('#type').select_option('mechanism');assert 0<page.locator('.report-section:visible').count()<n
                        page.emulate_media(media='print');assert page.locator('.report-section:visible').count()==n
                        page.emulate_media(media='screen');assert page.locator('.report-section:visible').count()<n
                        page.locator('#nav-collapse').click();assert page.locator('.toc details[open]').count()==0
                        page.evaluate('(id)=>location.hash=id',ordered_ids(key)[0]);page.wait_for_timeout(100)
                        assert page.locator('.toc details[open]').count()>0
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                        assert page.locator('figure.diagram svg').count()>0
                        if key in ('devops','security','finops'):
                            expected=sum(key in e.get('platforms',[e['platform']]) for e in entries)
                            assert page.locator('.usecase-entry:visible').count()==expected
                            page.locator('[data-uc-search]').fill('nonexistent-zz928');assert page.locator('.usecase-entry:visible').count()==0
                            page.locator('[data-uc-reset]').click();assert page.locator('.usecase-entry:visible').count()==expected
                        page.goto((ROOT/f'presentations/{key}.html').as_uri(),wait_until='load')
                        assert page.locator('.slide:visible').count()==1
                        tall=[]
                        for i,slide in enumerate(DECKS[key]['slides']):
                            page.locator('#slide-select').select_option(str(i))
                            assert page.locator('.slide:visible h1').inner_text()==slide['title']
                            assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                            overflow=page.locator('.slide:visible').evaluate('(el)=>el.scrollWidth>el.clientWidth+2')
                            assert not overflow
                            if width==1440:
                                height=page.locator('.slide:visible').bounding_box()['height']
                                if height>1050:tall.append({'slide':i+1,'height':round(height)})
                        page.locator('#agenda-open').click();assert page.locator('#agenda').is_visible()
                        page.locator('#agenda [data-slide="0"]').click();assert not page.locator('#agenda').is_visible()
                        page.locator('#next').focus();page.keyboard.press('ArrowRight');assert page.locator('#slide-select').input_value()=='1'
                        page.locator('#notes-button').click();assert page.locator('.note-block:visible').count()==1
                        page.locator('#notes-button').click();assert not page.locator('.note-block:visible').count()
                        page.locator('#timer-toggle').click();page.wait_for_function("document.querySelector('#session-time').textContent!=='00:00'",timeout=5000)
                        page.locator('#timer-toggle').click();paused=page.locator('#session-time').inner_text();page.wait_for_timeout(300);assert page.locator('#session-time').inner_text()==paused
                        page.locator('#timer-reset').click();assert page.locator('#session-time').inner_text()=='00:00'
                        selected=page.locator('#slide-select').input_value();page.reload();assert page.locator('#slide-select').input_value()==selected
                        page.emulate_media(media='print');assert page.locator('.slide:visible').count()==len(DECKS[key]['slides'])
                        page.emulate_media(media='screen');assert page.locator('.slide:visible').count()==1
                        browser_results.append({'subject':key,'width':width,'technical_sections':n,'slides':len(DECKS[key]['slides']),'javascript_errors':js_errors,'slides_over_1050px':tall,'navigation_filters_hash_notes_timer_print':'passed'})
                        errors.extend(js_errors)
                        if tall:errors.append(key+': desktop slides require layout review '+json.dumps(tall))
                    except Exception as exc:errors.append(f'{key} at {width}px: '+str(exc)+'; '+traceback.format_exc(limit=2))
                    finally:page.close()
            for width in (390,1440):
                page=br.new_page(viewport={'width':width,'height':1000});js_errors=[];page.on('pageerror',lambda err:js_errors.append(str(err)))
                try:
                    page.goto((ROOT/'catalog/index.html').as_uri());assert page.locator('.usecase-entry:visible').count()==len(entries)
                    page.locator('[data-uc-platform]').select_option('devops');assert page.locator('.usecase-entry:visible').count()==15
                    page.locator('[data-uc-search]').fill('flexible');assert page.locator('#UC-D05').is_visible()
                    page.locator('[data-uc-search]').fill('nonexistent-zz928');assert page.locator('.usecase-entry:visible').count()==0
                    page.evaluate("location.hash='UC-S01'");page.wait_for_timeout(100);assert page.locator('#UC-S01').is_visible()
                    page.locator('#UC-S01 summary').click();assert page.locator('#UC-S01 > .case-reference > dl').is_visible()
                    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                    errors.extend(js_errors);browser_results.append({'subject':'catalog','width':width,'narratives':len(entries),'filters_and_cross_product_hash':'passed','javascript_errors':js_errors})
                except Exception as exc:errors.append(f'catalog at {width}px: '+str(exc))
                finally:page.close()
            br.close()
    results={'revision':REVISION,'baseline':BASELINE,'guides':len(guides),'canonical_sections':len(new_ids),'previous_identifiers_retained':len(set(previous_ids)&set(new_ids)),'new_sections':sorted(set(new_ids)-set(previous_ids)),'authored_use_case_narratives':len(entries),'narrative_paragraphs':len(source_narratives),'platform_use_cases':dict(Counter(e['platform'] for e in entries)),'logical_diagrams':len(DIAGRAMS),'rendered_diagram_instances':figures,'html_presentations':len(DECKS),'slides':sum(len(d['slides']) for d in DECKS.values()),'programme_minutes':sum(totals(d)[0] for d in DECKS.values())//60,'exercise_minutes':sum(totals(d)[1] for d in DECKS.values())//60,'local_links_checked':link_count,'browser_checks':browser_results,'application_changes':app_changes,'excluded_scope_hits':scope_hits,'errors':errors,'boundary':'Source mapping, narrative presence/uniqueness, logical SVG accessibility, examples, and HTML behavior were checked. These checks do not establish factual completeness, live AWS operation, agent accuracy, or measured outcomes.'}
    results['relationship_model']=model_result
    write('qa/checks.json',json.dumps(results,indent=2))
    if errors:raise SystemExit(json.dumps(results,indent=2))
    write('VALIDATION.md','# Documentation validation\n\nThe current [machine-readable results](qa/checks.json) distinguish source structure, rendered behavior, and synthetic examples. The [content revision record](qa/content-review.json) identifies cleanup and editorial changes; the [source review record](qa/source-review.json) identifies new and selectively rechecked official material.\n\nThe [relationship checks](qa/relationships.json) additionally validate all 54 former-record mappings, 30 outcome definitions, workflow dependency types, feature configuration references, implementation profiles, reverse impact links and semantic regression cases. These are modeled dependencies, not live availability tests.\n\nChecks cover stable section identifiers, source mapping, use-case narratives, local links, unique SVG identifiers and accessibility descriptions, report and catalog filtering, chapter and slide navigation, notes, timers, hash links, and print-state restoration at desktop and mobile widths. The synthetic cost arithmetic and incident/security evidence relationships are checked separately.\n\nThese are not live AWS tests, an exhaustive upstream-documentation audit, or a claim that passing structural checks alone establishes good technical writing. The diagrams are logical explanatory models. No productivity, accuracy, security coverage, or savings result has been measured.\n\nThe application tree and its workflow are compared with the pinned baseline and must remain unchanged. Superseded document entry points and generators are removed rather than archived.\n')
    write('MANIFEST.json',json.dumps({'revision':REVISION,'files':file_manifest(),'excluded':['MANIFEST.json itself','applications/','.git/','__pycache__/']},indent=2))
    print(json.dumps(results,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--browser',action='store_true');args=parser.parse_args();check(args.browser)
