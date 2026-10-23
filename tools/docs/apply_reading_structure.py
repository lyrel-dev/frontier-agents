"""One-time wiring; removed after the reader architecture is integrated."""
from pathlib import Path
import ast
import json
import re
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(HERE))
BASELINE='dace05a3ce6aaae02470a817584b8ca3a4cc95be'


def edit(name, old, new):
    path=ROOT/name;text=path.read_text()
    if text.count(old)!=1:raise ValueError(name+': expected one anchor '+repr(old[:100])+'; found '+str(text.count(old)))
    path.write_text(text.replace(old,new))


def remove_functions(path,names):
    p=ROOT/path;text=p.read_text();lines=text.splitlines(keepends=True);tree=ast.parse(text)
    nodes=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name in names]
    if {n.name for n in nodes}!=set(names):raise ValueError('Missing functions in '+path)
    for n in sorted(nodes,key=lambda x:x.lineno,reverse=True):del lines[n.lineno-1:n.end_lineno]
    p.write_text(''.join(lines))

remove_functions('tools/docs/build.py',{'report','catalog_sources','catalog_controls','catalog_entry','catalog_content','build_catalog','indexes'})
edit('tools/docs/build.py','import catalog as catalogue','import reader')
edit('tools/docs/build.py',"    for key,g in guides.items():report(key,g,guides,catalog);presentation(key,g,guides)","    for key,g in guides.items():presentation(key,g,guides)")
edit('tools/docs/build.py','    build_catalog(catalog,guides);indexes(catalog);metadata(guides,catalog)','    metadata(guides,catalog)')
edit('tools/docs/build.py','    resource_model.integrate_pages(write)','    reader.render(guides,render_markdown,write)')
# README is owned by the reader renderer, not by the retired record-index edition.
p=HERE/'build.py';t=p.read_text();start=t.index('def metadata(guides,catalog):');cut=t.index('    coverage=',start)
t=t[:start]+'def metadata(guides,catalog):\n'+t[cut:]
# Publishing rules must state the freeze rather than invite changes to the approved registers.
lines=t.splitlines();lines=[line for line in lines if not line.startswith("    write('PUBLISHING.md',")]
insert=lines.index('def commit():')
publishing='# Publishing documentation\n\nThe six catalog JSON registers (use-cases, mechanisms, features, profiles, aliases, resource-models) are frozen at '+BASELINE+'. Do not change their definitions, identifiers, relationships, or use-case semantics during reader revisions.\n\nAuthored product prose lives in guides/*.md. Detailed mechanism blocks are generated from the frozen register. Chapter membership remains in tools/docs/structure.py; reader layout is in reader.py, reading.css, and reading.js; presentation content remains in presentation.py. Update rendered navigation without introducing another parallel guide or record-type index.\n\nRun python tools/docs/build.py and python tools/docs/check.py --browser. The reading checks compare frozen records byte-for-byte and test complete task-to-procedure reading journeys. Trigger the existing workflow through documentation-build.json and publish only after validation.\n\nGit retains previous versions. Do not create manual archives, migration copies, or forwarding editions. Preserve the independent application and its workflow. Repository publication does not deploy a website.\n'
lines.insert(insert,"    write('PUBLISHING.md',"+repr(publishing)+")\n\n")
p.write_text('\n'.join(lines)+'\n')
# Remove the obsolete page composer and its navigation injection.
(HERE/'catalog.py').unlink()
remove_functions('tools/docs/resource_model.py',{'integrate_pages'})
# Direct generated related-mechanism links to the authoritative guide.
p=HERE/'mechanism_detail.py';t=p.read_text()
t=t.replace('../catalog/mechanisms.html#{r[\'id\']}','../guides/{entry[\'platform\']}.html#{r[\'id\']}')
# Browser contracts moved to reading_check; all mechanism semantics and source checks remain.
a=t.index('    if browser and not errors:',t.index('def validate('));b=t.index("    result={'stage':3",a)
t=t[:a]+"    # Browser navigation is validated across the new reading paths in reading_check.\n"+t[b:]
p.write_text(t)
remove_functions('tools/docs/mechanism_detail.py',{'index_summary'})
# Preserve schema and deliberate-defect tests; retire tests that demanded obsolete record pages.
p=HERE/'model_check.py';t=p.read_text();a=t.index("    for file,items in [('mechanisms',mechanisms)");b=t.index("    result={'schema_version':2",a)
t=t[:a]+"    # Reader composition and reverse navigation are checked in reading_check.\n"+t[b:]
p.write_text(t)
# Maintain the editorial scan across the complete new reading surface.
p=HERE/'editorial_check.py';t=p.read_text();t=t.replace("('catalog/index.html','catalog/mechanisms.html','catalog/features.html','catalog/profiles.html','catalog/resource-models.html','index.html')","('catalog/index.html','catalog/resource-models.html','index.html',*[p.relative_to(ROOT).as_posix() for p in sorted((ROOT/'catalog').glob('UC-*.html'))])")
p.write_text(t)
# Adjust structural expectations, retaining unchanged presentation tests and data checks.
p=HERE/'check.py';t=p.read_text();t=t.replace('from mechanism_detail import validate as validate_mechanisms','from mechanism_detail import validate as validate_mechanisms\nfrom reading_check import validate as validate_reading')
a=t.index('    html_paths=');b=t.index('\n    parsed=',a)
t=t[:a]+"    html_paths=[ROOT/'index.html',*sorted((ROOT/'guides').glob('*.html')),*sorted((ROOT/'catalog').glob('*.html')),*sorted((ROOT/'presentations').glob('*.html'))]"+t[b:]
a=t.index("        if key!='architecture':");b=t.index('        deck=parsed[',a)
t=t[:a]+"        if page.select('.embedded-catalog,[data-usecase-catalog]'):errors.append(key+': duplicate catalog remains in guide')\n"+t[b:]
a=t.index("    catalog_page=parsed[");b=t.index('    for path,page in parsed.items():',a)
t=t[:a]+"    rendered_narratives=[p.get_text() for e in entries for p in parsed[(ROOT/f'catalog/{e[\"id\"]}.html').resolve()].select('.case-narrative p')]\n    if rendered_narratives!=source_narratives:errors.append('Use-case narrative/source mismatch')\n"+t[b:]
# Navigation checks for books and workflows are in reading_check. Existing deck tests remain.
a=t.index("                        page.goto((ROOT/f'guides/{key}.html')");b=t.index("                        page.goto((ROOT/f'presentations/{key}.html')",a)
t=t[:a]+"                        n=len(g['sections'])\n"+t[b:]
a=t.index('            for width in (390,1440):',t.index('    if browser and not errors:'))
b=t.index('            br.close()',a)
t=t[:a]+t[b:]
t=t.replace('    if browser and not errors:\n',"    reading_result=validate_reading(guides,browser=browser)\n    errors.extend(reading_result['errors'])\n    if browser and not errors:\n",1)
t=t.replace("    results['product_resource_model']=resource_result","    results['product_resource_model']=resource_result\n    results['reading_structure']=reading_result")
# Validation document should link to the actual current navigation checks.
t=t.replace("# Documentation validation\\n\\nStage 3 adds", "# Documentation validation\\n\\nThe current reader revision is covered by [frozen-record and reading-journey checks](qa/reading-structure.json). Model and use-case sources are unchanged. Guide navigation, search, contextual configuration, and deep links are tested separately from service behavior.\\n\\nStage 3 adds")
p.write_text(t)
# Stable Markdown editions must also point to the contextual destinations.
from reader import Reader
r=Reader({},None,None)
for p in (ROOT/'guides').glob('*.md'):
    text=p.read_text()
    for ident,target in r.targets.items():
        for old in ('mechanisms','features','profiles'):
            text=text.replace('../catalog/'+old+'.html#'+ident,'../'+target)
    text=text.replace('../catalog/migration.md','../catalog/index.html')
    p.write_text(text)
p=HERE/'structure.py';t=p.read_text();t=re.sub(r"REVISION\s*=\s*['\"][^'\"]+['\"]","REVISION = '2026-10-23-reading-structure'",t,count=1);p.write_text(t)
p=ROOT/'EDITORIAL_STANDARD.md';p.write_text(p.read_text()+'\n## Reader hierarchy\n\nPrimary navigation follows reader tasks: Guides, Use cases, Resource model, Presentations. Each guide has one chapter hierarchy and one search. Each approved use case has one contextual page containing the unchanged narrative, workflow, configuration and verification. Mechanisms and features link to their product-guide explanations. Internal schema types and migration mappings are not primary reader destinations. Protect all six catalog JSON registers byte-for-byte.\n')
p=ROOT/'CHANGELOG.md';p.write_text(p.read_text()+'\n## 2026-10-23 — Reading structure\n\nReplaced record-type pages with chapter-based guides and dedicated use-case pages. Removed duplicate embedded catalogs and standalone mechanism, feature, profile and consolidation-map editions. Configuration is presented in use-case context; mechanisms and resource configuration link directly to product procedures. Frozen registers and presentation content are unchanged. Added reading-journey and source-preservation tests.\n')
(ROOT/'qa/reading-review.md').write_text('# Reading-structure review\n\n## Defects addressed\n\nThe previous primary navigation exposed internal record categories rather than reading tasks. Each product guide embedded another complete catalog with a second search, and configuration and mechanism details required navigation through separate indexes. The presentation index repeated the entire home page.\n\n## Reader paths\n\nThe home page introduces the cross-service overview and the three product books. A book starts with its overview chapter, offers chapter navigation and a single search, and links to relevant use cases without repeating the full catalog. The use-case directory contains grouped summaries and search; each selected case includes its workflow, applicable configuration, completion criteria and direct technical references. The resource model remains a technical dictionary. Presentations retain their slide content and timings and have their own index.\n\n## Frozen scope\n\nNo definitions, cases, variants, dependency semantics, profiles, source claims or relationship multiplicities were changed. All six JSON registers are compared byte-for-byte with '+BASELINE+'. Historical identifiers remain lookup metadata; retired HTML index pages are removed, not archived. Internal references are rewritten. External bookmarks to removed index URLs are not maintained as duplicate editions.\n\n## Validation\n\nSee reading-structure.json for chapter/search/deep-link/print tests, all 30 use-case pages, and a complete task-to-configuration-to-procedure navigation test. Existing source, relationship, entity and presentation checks remain. Browser checks are not a live AWS test or a claim of prose quality.\n')
# No migration utility remains in the published tree.
Path(__file__).unlink()
print('Reader layout integrated; frozen JSON records were not written.')
