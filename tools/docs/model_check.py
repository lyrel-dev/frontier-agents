"""Check the documentation relationship model, not live AWS readiness."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlsplit
import json
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[2]
REQUIRED_CASE={'id','actor','objective','completion','workflow','variants','profiles','narrative','platforms','sections'}
REQUIRED_STEP={'title','actor','purpose','mechanism','dependency','condition','configuration_features','effect','verification','on_failure'}
REQUIRED_MECHANISM={'id','platform','title','features','sections','trigger','state','process','effect','verification','on_failure'}
EXPECTED_FORMER={f'{p}-UC{i:02d}' for p,n in [('D',22),('S',16),('F',16)] for i in range(1,n+1)}

def load(name):return json.loads((ROOT/f'catalog/{name}.json').read_text())['entries']

def schema_errors(cases,mechanisms,features,profiles,aliases,guides):
    errors=[];all_lists=[cases,mechanisms,features,profiles]
    ids=[r['id'] for group in all_lists for r in group]
    if len(ids)!=len(set(ids)):errors.append('Record identifiers are not globally unique')
    C={x['id']:x for x in cases};M={x['id']:x for x in mechanisms};F={x['id']:x for x in features};P={x['id']:x for x in profiles}
    if len(cases)!=30:errors.append('Expected exactly 30 primary outcome records')
    if Counter(c['platform'] for c in cases)!=Counter({'devops':14,'security':8,'finops':7,'architecture':1}):errors.append('Primary outcome distribution differs from the reviewed consolidation')
    if len(aliases)!=54 or {a['id'] for a in aliases}!=EXPECTED_FORMER:errors.append('All 54 former identifiers must be mapped exactly once')
    if len({a['id'] for a in aliases})!=len(aliases):errors.append('Duplicate former identifier')
    for a in aliases:
        if not a.get('title') or not a.get('disposition') or not a.get('targets'):errors.append(a['id']+': incomplete migration rationale')
        for target in a.get('targets',[]):
            if target not in set(ids):errors.append(a['id']+': unresolved successor '+target)
        if a['id']=='F-UC04' and set(a['targets'])!={'UC-F02','UC-F03'}:errors.append('Forecast/coverage alias must present both distinct successors')
    for r in mechanisms+features:
        if r['platform'] not in guides:errors.append(r['id']+': unknown product');continue
        if not r.get('sections'):errors.append(r['id']+': missing canonical explanation')
        for sid in r.get('sections',[]):
            if sid not in guides[r['platform']]['sections']:errors.append(r['id']+': unresolved guide section '+sid)
            elif not guides[r['platform']]['sections'][sid]['sources']:errors.append(r['id']+': guide explanation has no official evidence')
    for m in mechanisms:
        if REQUIRED_MECHANISM-set(m):errors.append(m['id']+': incomplete mechanism record')
        if not m.get('features'):errors.append(m['id']+': no implementation feature')
        for f in m.get('features',[]):
            if f not in F:errors.append(m['id']+': unknown feature '+f)
            elif F[f]['platform']!=m['platform']:errors.append(m['id']+': mechanism incorrectly borrows another product feature')
    for p in profiles:
        for field in ('platforms','parameters','setup','tests','stop_behavior','mechanisms'):
            if not p.get(field):errors.append(p['id']+': missing profile '+field)
        for mid in p.get('mechanisms',[]):
            if mid not in M:errors.append(p['id']+': unknown mechanism '+mid)
            elif M[mid]['platform'] not in p['platforms']:errors.append(p['id']+': unqualified cross-product mechanism')
    objectives=[]
    for c in cases:
        if REQUIRED_CASE-set(c):errors.append(c['id']+': incomplete case')
        objectives.append(c.get('objective','').casefold())
        if len(c.get('completion',[]))<2:errors.append(c['id']+': no reviewable completion conditions')
        if len(c.get('narrative',[]))<2:errors.append(c['id']+': missing connected narrative')
        if not c.get('workflow'):errors.append(c['id']+': no workflow')
        for p in c.get('profiles',[]):
            if p not in P:errors.append(c['id']+': missing profile '+p)
        for s in c.get('workflow',[]):
            if REQUIRED_STEP-set(s):errors.append(c['id']+': incomplete workflow dependency')
            if not s.get('verification') or not s.get('on_failure'):errors.append(c['id']+': no acceptance/failure behavior')
            if s.get('dependency') not in ('required','optional','conditional'):errors.append(c['id']+': invalid dependency kind')
            if s.get('dependency') in ('conditional','optional') and not s.get('condition'):errors.append(c['id']+': missing dependency condition')
            mid=s.get('mechanism')
            if mid is None:
                if s.get('configuration_features'):errors.append(c['id']+': human decision invents a native feature')
                continue
            if mid not in M:errors.append(c['id']+': unknown mechanism '+str(mid));continue
            m=M[mid]
            if set(s.get('configuration_features',[]))!=set(m['features']):errors.append(c['id']+': feature bindings differ from the mechanism')
            if m['platform'] not in c['platforms']:errors.append(c['id']+': unqualified product dependency')
    if len(objectives)!=len(set(objectives)):errors.append('Primary cases share an identical objective')
    consumers={m for c in cases for s in c['workflow'] if (m:=s['mechanism'])}
    consumers.update(m for p in profiles for m in p['mechanisms'])
    for m in M:
        if m not in consumers:errors.append(m+': mechanism has no workflow or profile consumer')
    used_features={f for m in mechanisms for f in m['features']}
    for f in F:
        if f not in used_features:errors.append(f+': feature has no mechanism')
    for pid in P:
        if not any(pid in c['profiles'] for c in cases):errors.append(pid+': profile has no outcome consumer')
    # These preserve material boundaries that a superficial deduplication could remove.
    if C.get('UC-D03',{}).get('completion')==C.get('UC-D04',{}).get('completion'):errors.append('Planning and execution were collapsed')
    if C.get('UC-F02',{}).get('objective')==C.get('UC-F03',{}).get('objective'):errors.append('Forecast and coverage were collapsed')
    if C.get('UC-S01',{}).get('objective')==C.get('UC-S07',{}).get('objective'):errors.append('Assessment and revalidation were collapsed')
    return errors

def validate_model(guides,browser=False):
    cases=load('use-cases');mechanisms=load('mechanisms');features=load('features');profiles=load('profiles');aliases=load('aliases')
    errors=schema_errors(cases,mechanisms,features,profiles,aliases,guides);regression=[];browser_results=[]
    # Deliberately corrupt copies to establish that critical checks actually reject defects.
    bad=deepcopy(cases);bad[0]['workflow'][0]['mechanism']='MX-UNKNOWN'
    assert any('unknown mechanism' in x for x in schema_errors(bad,mechanisms,features,profiles,aliases,guides));regression.append('Unknown mechanism rejected')
    bad=deepcopy(aliases);next(x for x in bad if x['id']=='F-UC04')['targets']=['UC-F02']
    assert any('both distinct successors' in x for x in schema_errors(cases,mechanisms,features,profiles,bad,guides));regression.append('Ambiguous split cannot silently resolve to one outcome')
    bad=deepcopy(cases);bad[0]['workflow'][0]['on_failure']=''
    assert any('acceptance/failure' in x for x in schema_errors(bad,mechanisms,features,profiles,aliases,guides));regression.append('Missing failure handling rejected')
    bad=deepcopy(profiles);bad[0]['platforms']=['security']
    assert any('unqualified cross-product' in x for x in schema_errors(cases,mechanisms,features,bad,aliases,guides));regression.append('Cross-product configuration assumption rejected')
    for file,items in [('mechanisms',mechanisms),('features',features),('profiles',profiles)]:
        page=BeautifulSoup((ROOT/f'catalog/{file}.html').read_text(),'html.parser')
        if {a['id'] for a in page.select('.reference-entry')}!={r['id'] for r in items}:errors.append(file+': reference render/source mismatch')
        for r in items:
            node=page.find(id=r['id'])
            if node and not node.select('a[href*="../catalog/"]'):errors.append(r['id']+': missing dependency navigation')
    feature_page=BeautifulSoup((ROOT/'catalog/features.html').read_text(),'html.parser')
    node=feature_page.find(id='FT-D-MEMORY')
    if not node or not node.find('a',href='../catalog/index.html#UC-D02') or not node.find('a',href='../catalog/index.html#UC-D06'):errors.append('Memory impact index omits incident or health-report consumers')
    if browser and not errors:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            br=pw.chromium.launch(headless=True)
            for width in (390,1440):
                page=br.new_page(viewport={'width':width,'height':1000});js_errors=[];page.on('pageerror',lambda err:js_errors.append(str(err)))
                try:
                    for file,items in [('mechanisms',mechanisms),('features',features),('profiles',profiles)]:
                        page.goto((ROOT/f'catalog/{file}.html').as_uri())
                        assert page.locator('.reference-entry:visible').count()==len(items)
                        page.locator('[data-ref-search]').fill('nonexistent-zz928')
                        assert page.locator('.reference-entry:visible').count()==0
                        assert page.locator('[data-ref-empty]').is_visible()
                        page.locator('[data-ref-reset]').click()
                        page.locator('[data-ref-platform]').select_option('security')
                        expected=sum('security' in r.get('platforms',[r.get('platform')]) for r in items)
                        assert page.locator('.reference-entry:visible').count()==expected
                        assert not page.evaluate('document.documentElement.scrollWidth>innerWidth+2')
                    page.goto((ROOT/'catalog/index.html').as_uri()+'#D-UC03')
                    page.wait_for_function("location.hash==='#UC-D02'")
                    assert page.locator('#UC-D02').is_visible()
                    page.goto((ROOT/'catalog/index.html').as_uri()+'#S-UC05')
                    page.wait_for_url('**/mechanisms.html#MX-S-LOGIN')
                    assert page.locator('#MX-S-LOGIN').is_visible()
                    page.goto((ROOT/'catalog/index.html').as_uri()+'#F-UC04')
                    assert page.locator('#F-UC04').is_visible()
                    assert page.locator('#F-UC04 a').count()==2
                    page.goto((ROOT/'catalog/index.html').as_uri())
                    page.locator('[data-uc-platform]').select_option('devops')
                    assert page.locator('.usecase-entry:visible').count()==15
                    assert page.locator('#UC-G01').is_visible()
                    page.locator('[data-uc-platform]').select_option('finops')
                    assert page.locator('.usecase-entry:visible').count()==8
                    assert page.locator('#UC-G01').is_visible()
                    page.locator('[data-uc-reset]').click();page.locator('[data-uc-search]').fill('Investigation steering')
                    assert page.locator('#UC-D02').is_visible()
                    page.locator('[data-uc-reset]').click();page.locator('[data-uc-search]').fill('Persistent reporting preferences')
                    assert page.locator('[data-supporting-matches]').is_visible()
                    assert page.locator('[data-supporting-matches] a[href="../catalog/mechanisms.html#MX-F-MEMORY"]').is_visible()
                    page.locator('[data-uc-reset]').click();page.locator('#UC-D06 summary').click()
                    assert page.locator('#UC-D06 .workflow-steps > li').count()==len(next(c for c in cases if c['id']=='UC-D06')['workflow'])
                    page.locator('#UC-D06 a[href="../catalog/mechanisms.html#MX-D-RECALL"]').click()
                    assert page.locator('#MX-D-RECALL').is_visible()
                    page.locator('#MX-D-RECALL a[href="../catalog/features.html#FT-D-MEMORY"]').click()
                    assert page.locator('#FT-D-MEMORY').is_visible()
                    page.locator('#FT-D-MEMORY a[href="../catalog/index.html#UC-D06"]').first.click()
                    assert page.locator('#UC-D06').is_visible()
                    errors.extend(js_errors)
                    browser_results.append({'width':width,'reference_filters':'passed','outcome_mechanism_feature_reverse_navigation':'passed','former_case_and_support_aliases':'passed','forecast_coverage_choice':'passed','shared_profile_filters':'passed','javascript_errors':js_errors})
                except Exception as exc:errors.append('Relationship browser check at '+str(width)+': '+str(exc))
                finally:page.close()
            br.close()
    result={'schema_version':2,'primary_cases':len(cases),'primary_distribution':dict(Counter(c['platform'] for c in cases)),'mechanisms':len(mechanisms),'features':len(features),'implementation_profiles':len(profiles),'former_identifiers_mapped':len(aliases),'workflow_steps':sum(len(c['workflow']) for c in cases),'mechanism_bindings':sum(s['mechanism'] is not None for c in cases for s in c['workflow']),'supporting_records_reclassified':sum(a['disposition'].startswith('Supporting') for a in aliases),'regression_checks':regression,'browser':browser_results,'errors':errors,'boundary':'Document dependency and navigation checks. Not a live AWS readiness test, exhaustive source audit or evidence of operational improvement.'}
    (ROOT/'qa/relationships.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
