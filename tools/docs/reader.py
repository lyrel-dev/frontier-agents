"""Reader-facing information architecture over frozen documentation records.

This module renders books and workflow pages. It never writes catalog JSON or
changes guide prose. Mechanisms and features are reached within their product
guide; configuration recipes are read in the use case that needs them.
"""
from __future__ import annotations
from collections import defaultdict
from html import escape
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import posixpath
import re
from bs4 import BeautifulSoup
from structure import CHAPTERS
from presentation import DECKS

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASELINE = 'dace05a3ce6aaae02470a817584b8ca3a4cc95be'
NAMES = {'devops':'AWS DevOps Agent', 'security':'AWS Security Agent',
         'finops':'AWS FinOps Agent', 'architecture':'Cross-service architecture'}
RETIRED = ('catalog/mechanisms.html','catalog/features.html','catalog/profiles.html','catalog/migration.md')


def esc(value):
    return escape(str(value), quote=True)


def records(name):
    return json.loads((ROOT / f'catalog/{name}.json').read_text())['entries']


def paragraph(value, cls=''):
    return '<p'+(' class="'+cls+'"' if cls else '')+'>'+esc(value)+'</p>'


def listing(items, ordered=False):
    tag = 'ol' if ordered else 'ul'
    return '<'+tag+'>'+''.join('<li>'+esc(x)+'</li>' for x in items)+'</'+tag+'>'


def table(headers, rows):
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="Configuration table"><table><thead><tr>'+''.join('<th scope="col">'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows)+'</tbody></table></div>'


def relative(target, current):
    path, sep, fragment = target.partition('#')
    result = posixpath.relpath(path, posixpath.dirname(current) or '.')
    if path == current:
        result = ''
    return result + (sep+fragment if sep else '')


def anchor(target, label, current, attrs=''):
    return '<a href="'+esc(relative(target,current))+'"'+attrs+'>'+esc(label)+'</a>'


class Reader:
    def __init__(self, guides, render_markdown, write):
        self.guides = guides
        self.markdown = render_markdown
        self.write = write
        self.cases = records('use-cases')
        self.mechanisms = {e['id']:e for e in records('mechanisms')}
        self.features = {e['id']:e for e in records('features')}
        self.profiles = {e['id']:e for e in records('profiles')}
        self.aliases = records('aliases')
        self.model = json.loads((ROOT/'catalog/resource-models.json').read_text())
        self.targets = {e['id']:f'catalog/{e["id"]}.html#{e["id"]}' for e in self.cases}
        for mid, m in self.mechanisms.items():
            self.targets[mid] = f'guides/{m["platform"]}.html#{mid}'
        for fid, f in self.features.items():
            self.targets[fid] = f'guides/{f["platform"]}.html#{fid}'
        for pid in self.profiles:
            consumers = [c for c in self.cases if pid in c['profiles']]
            if not consumers:
                raise ValueError('Configuration has no use case: '+pid)
            self.targets[pid] = f'catalog/{consumers[0]["id"]}.html#{pid}'
        self.section_product = {sid:p for p,g in guides.items() for sid in g['sections']}

    def link(self, ident, label, current):
        return anchor(self.targets[ident], label, current)

    def section_link(self, sid, current):
        p = self.section_product[sid]
        return anchor(f'guides/{p}.html#{sid}', self.guides[p]['sections'][sid]['title'], current)

    def header(self, current, active):
        nav = [('index.html','Guides','guides'),('catalog/index.html','Use cases','cases'),
               ('catalog/resource-models.html','Resource model','model'),
               ('presentations/index.html','Presentations','presentations')]
        return '<a class="skip-link" href="#main">Skip to content</a><header class="reader-header"><a class="reader-brand" href="'+esc(relative('index.html',current))+'">AWS operational agents</a><nav aria-label="Main navigation">'+''.join(anchor(path,label,current,' aria-current="page"' if key==active else '') for path,label,key in nav)+'</nav></header>'

    def page(self, title, body, current, active, kind):
        css = (HERE/'reading.css').read_text()
        js = (HERE/'reading.js').read_text()
        return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' — AWS operational agents</title><style>'+css+'</style></head><body data-reader="'+kind+'">'+self.header(current,active)+body+'<footer class="reader-footer">'+anchor('VALIDATION.md','Validation scope',current)+' · '+anchor('guides/coverage.md','Official sources and coverage',current)+'</footer><script>'+js+'</script></body></html>'

    def rewrite(self, html, current):
        """Resolve old record-index links to their contextual reading destinations."""
        soup = BeautifulSoup(html,'html.parser')
        for a in soup.select('a[href]'):
            u = urlsplit(a['href'])
            if u.scheme or u.netloc:
                continue
            path = posixpath.normpath(posixpath.join(posixpath.dirname(current),unquote(u.path))) if u.path else current
            fragment = unquote(u.fragment)
            if path in RETIRED:
                if fragment in self.targets:
                    a['href'] = relative(self.targets[fragment],current)
                else:
                    a['href'] = relative('index.html',current)
                    a.string = 'Product guides'
            elif path == 'catalog/index.html' and fragment in self.targets:
                a['href'] = relative(self.targets[fragment],current)
        return str(soup)

    @staticmethod
    def mechanism_section(mechanism):
        overrides={'MX-D-QUERY':'D-21','MX-D-CUSTOM':'D-19','MX-S-PERSONALIZE':'S-13'}
        if mechanism['id'] in overrides:
            return overrides[mechanism['id']]
        primary=mechanism['review']['primary_section']
        if mechanism['platform']=='devops' and primary=='D-09':
            return 'D-22'
        return primary

    @staticmethod
    def feature_section(feature):
        if feature['id']=='FT-D-CUSTOM':
            return 'D-16'
        if feature['platform']=='devops' and feature['sections'][0]=='D-09':
            return 'D-22'
        return feature['sections'][0]

    def feature_detail(self, feature, current):
        product=self.model['products'][feature['platform']]
        entities={e['id']:e for e in product['entities']}
        ids=product['feature_bindings'][feature['id']]
        uses=[c for c in self.cases if any(feature['id'] in s['configuration_features'] for s in c['workflow'])]
        result='<details class="feature-reference" id="'+feature['id']+'"><summary>Resource and use-case references: '+esc(feature['title'])+'</summary>'
        result+='<p>Read the configuration explanation in '+ ' · '.join(self.section_link(s,current) for s in dict.fromkeys([self.feature_section(feature),*feature['sections']]))+'.</p>'
        result+='<p>Resource definitions: '+' · '.join(anchor('catalog/resource-models.html#'+i,entities[i]['name'],current) for i in ids)+'</p>'
        if uses:result+='<p>Applicable use cases: '+' · '.join(self.link(c['id'],c['title'],current) for c in uses)+'</p>'
        return result+'</details>'

    def guide(self, product, guide):
        current = 'guides/'+product+'.html'
        links = {sid:relative(f'guides/{p}.html#{sid}',current) for p,g in self.guides.items() for sid in g['sections']}
        intro = BeautifulSoup(self.markdown(guide['intro'],guide['definitions'],links,product+'-intro'),'html.parser')
        if intro.h1:
            intro.h1.decompose()
        nav, chapters = [], []
        for number, chapter in enumerate(CHAPTERS[product],1):
            cid = 'chapter-'+chapter['slug']
            nav_sections, content = [], []
            display_number = 'A' if chapter.get('appendix') else f'{number:02d}'
            for j, sid in enumerate(chapter['sections'],1):
                section = guide['sections'][sid]
                mechanisms = [m for m in self.mechanisms.values() if m['platform']==product and self.mechanism_section(m)==sid]
                subnav = ''
                nav_sections.append('<li><a data-section="'+sid+'" href="#'+sid+'">'+display_number+'.'+str(j)+' '+esc(section['title'])+'</a>'+subnav+'</li>')
                prose = BeautifulSoup(self.markdown(section['body'],guide['definitions'],links,product+'-'+sid),'html.parser')
                # Compatibility anchors resolve frozen workflow references to their technical explanation.
                # They are references, not declarations that every old registry label is a mechanism.
                for m in mechanisms:
                    node=prose.new_tag('span',id=m['id'])
                    node['class']='technical-reference-anchor'
                    node['aria-label']='Technical reference: '+section['title']
                    node.string=''
                    prose.insert(0,node)
                context = ''.join(self.feature_detail(f,current) for f in self.features.values() if f['platform']==product and self.feature_section(f)==sid)
                related = [c for c in self.cases if any(s['mechanism'] in self.mechanisms and sid==self.mechanism_section(self.mechanisms[s['mechanism']]) for s in c['workflow']) and product in c['platforms']]
                if related:
                    context += '<details class="related-reading"><summary>Use cases that apply this section</summary><ul>'+''.join('<li>'+self.link(c['id'],c['title'],current)+'</li>' for c in related)+'</ul></details>'
                content.append('<section class="report-section" id="'+sid+'" data-chapter="'+chapter['slug']+'"><h3><span class="section-number">'+display_number+'.'+str(j)+'</span> '+esc(section['title'])+'</h3>'+str(prose)+context+'</section>')
            nav.append('<li><details open><summary><a href="#'+cid+'">'+display_number+'. '+esc(chapter['title'])+'</a></summary><ol>'+''.join(nav_sections)+'</ol></details></li>')
            chapters.append('<section class="chapter" data-reader-chapter="'+cid+'" id="'+cid+'"><header><p class="chapter-label">'+('Appendix' if chapter.get('appendix') else 'Chapter '+f'{number:02d}')+'</p><h2>'+esc(chapter['title'])+'</h2>'+paragraph(chapter['purpose'])+'</header>'+''.join(content)+'</section>')
        side = '<aside class="reader-sidebar"><details id="reader-contents" open><summary>Contents</summary><nav class="toc" aria-label="Guide chapters"><ol>'+''.join(nav)+'</ol></nav></details></aside>'
        controls = '<form class="reader-search" role="search"><label for="guide-search">Search this guide</label><div><input id="guide-search" type="search" placeholder="Search explanations and procedures"><button type="reset">Clear</button></div><p id="guide-search-status" role="status"></p></form><div class="reading-controls"><label><input type="checkbox" id="read-all"> Read all chapters</label><button type="button" data-print>Print guide</button></div>'
        breadcrumbs = '<nav class="breadcrumbs" aria-label="Breadcrumb">'+anchor('index.html','Guides',current)+'<span>/</span><span>'+esc(NAMES[product])+'</span></nav>'
        contextual = '<p class="edition-links">'+anchor('presentations/'+product+'.html','Open presentation',current)+' · '+anchor('catalog/index.html?platform='+product,'Find a use case',current)+' · '+anchor('guides/'+product+'.md','Markdown edition',current)+'</p>'
        pager = '<nav class="chapter-pager" aria-label="Chapter navigation"><a id="previous-chapter" href="#" hidden>Previous chapter</a><span id="chapter-position" aria-live="polite"></span><a id="next-chapter" href="#">Next chapter</a></nav>'
        body = '<div class="reader-layout">'+side+'<main id="main" class="reader-main">'+breadcrumbs+'<header class="guide-introduction"><h1>'+esc(NAMES[product])+'</h1>'+str(intro)+contextual+'</header>'+controls+'<p id="guide-empty" hidden>No sections match this search. Clear the search or choose a chapter in Contents.</p>'+''.join(chapters)+pager+'</main></div>'
        self.write(current,self.rewrite(self.page(NAMES[product],body,current,'guides','guide'),current))

    def case_page(self, case):
        current = 'catalog/'+case['id']+'.html'
        name = NAMES[case['platform']]
        title = case['title']
        nav = [('context','Purpose and scope'),('workflow','Workflow'),('configuration','Configuration'),('verification','Verification and limits'),('references','Technical references')]
        side = '<aside class="reader-sidebar"><details id="reader-contents" open><summary>On this page</summary><nav aria-label="Use-case contents"><ol>'+''.join('<li><a href="#'+s+'">'+str(i)+'. '+t+'</a></li>' for i,(s,t) in enumerate(nav,1))+'</ol></nav></details><p>'+anchor('catalog/index.html','All use cases',current)+'</p><p>'+anchor('guides/'+case['platform']+'.html','Read '+name,current)+'</p></aside>'
        body = '<div class="reader-layout">'+side+'<main id="main" class="reader-main"><nav class="breadcrumbs" aria-label="Breadcrumb">'+anchor('catalog/index.html','Use cases',current)+'<span>/</span><span>'+esc(case['group'])+'</span></nav><header id="'+case['id']+'"><p class="chapter-label">'+esc(name)+'</p><h1>'+esc(title)+'</h1>'+paragraph(case['objective'],'lead')+'<p class="case-actor"><strong>Responsible actor.</strong> '+esc(case['actor'])+'</p></header>'
        body += '<section id="context"><h2>1. Purpose and scope</h2><div class="case-narrative">'+''.join(paragraph(p) for p in case['narrative'])+'</div><dl class="context-fields"><dt>Inputs</dt><dd>'+esc(case['inputs'])+'</dd><dt>Expected output</dt><dd>'+esc(case['output'])+'</dd><dt>Execution pattern</dt><dd>'+esc(case['cadence'])+'</dd><dt>Delivery mode</dt><dd>'+esc(case['delivery'])+'</dd></dl>'
        if case['variants']:
            body += '<h3>Variants</h3>'
            for variant in case['variants']:
                body += '<section class="case-variant"><h4>'+esc(variant['name'])+'</h4>'+paragraph(variant['changes'])+paragraph(variant['controls'])+'</section>'
        body += '</section><section id="workflow"><h2>2. Workflow</h2>'+paragraph(case['steps_basis'])+'<ol class="workflow-steps">'
        for i, step in enumerate(case['workflow'],1):
            m = self.mechanisms.get(step['mechanism'])
            body += '<li id="step-'+str(i)+'"><h3>'+esc(step['title'])+'</h3>'+paragraph(step['purpose'])+'<p><strong>Responsible actor.</strong> '+esc(step['actor'])+'</p>'
            body += '<p><strong>Dependency.</strong> '+esc(step['dependency'].capitalize())+'. '+esc(step['condition'])+'</p>'
            if m:
                body += '<p><strong>Platform process.</strong> '+self.link(m['id'],m['title'],current)+'. '+esc(m['process'])+'</p>'
                body += '<p><strong>Configuration.</strong> '+' · '.join(self.link(fid,self.features[fid]['title'],current) for fid in step['configuration_features'])+'</p>'
            else:
                body += '<p><strong>Implementation.</strong> Engineering procedure; no native service operation is asserted for this step.</p>'
            body += '<p><strong>Effect.</strong> '+esc(step['effect'])+'</p><p><strong>Verification.</strong> '+esc(step['verification'])+'</p><p class="failure-note"><strong>Failure handling.</strong> '+esc(step['on_failure'])+'</p></li>'
        body += '</ol></section><section id="configuration"><h2>3. Configuration</h2><p>Use the applicable configuration below for the selected workflow. Parameters and checks are engineering guidance, not deployable AWS payloads. Product procedures remain in the linked guide sections.</p>'
        for pid in case['profiles']:
            profile = self.profiles[pid]
            body += '<section class="configuration-recipe" id="'+pid+'"><h3>'+esc(profile['title'])+'</h3>'+table(['Parameter','Configuration decision','Example or constraint'],profile['parameters'])
            body += '<h4>Setup procedure</h4>'+listing(profile['setup'],True)+'<h4>Proposed checks</h4>'+listing(profile['tests'])+'<p><strong>Stop behavior.</strong> '+esc(profile['stop_behavior'])+'</p>'
            # Profiles can be shared by several operations; preserve applicability, do not promote every mechanism to required.
            body += '<details><summary>Supporting procedures for this configuration</summary><p>This recipe is reused by multiple workflows. The required, optional, or conditional dependencies for this use case are specified in its workflow above.</p><ul>'+''.join('<li>'+self.link(mid,self.mechanisms[mid]['title'],current)+'</li>' for mid in profile['mechanisms'])+'</ul></details></section>'
        body += '</section><section id="verification"><h2>4. Verification and limits</h2><h3>Completion criteria</h3>'+listing(case['completion'])+'<h3>Prerequisites and availability</h3>'+paragraph(case['availability'])+'<h3>Limitations</h3>'+paragraph(case['constraints'])+'<h3>Example request</h3><blockquote>'+paragraph(case['example'])+'</blockquote><p>Verification procedures are proposed checks. This documentation does not report a live execution of the workflow.</p></section>'
        refs = list(dict.fromkeys([*(self.mechanism_section(self.mechanisms[step['mechanism']]) for step in case['workflow'] if step['mechanism'] in self.mechanisms),*case['sections']]))
        body += '<section id="references"><h2>5. Technical references</h2><ul>'+''.join('<li>'+self.section_link(s,current)+'</li>' for s in refs)+'</ul>'
        g = self.guides[case['platform']]
        source_ids = sorted({r for s in refs if s in g['sections'] for r in g['sections'][s]['sources']})
        body += '<details><summary>Official documentation linked by these sections</summary><ul>'+''.join('<li><a href="'+esc(g['refs'][r])+'">'+esc(r)+' — '+esc(g['refs'][r].split('/')[-1].replace('.html','').replace('-',' '))+'</a></li>' for r in source_ids)+'</ul></details></section>'
        group = [c for c in self.cases if c['platform']==case['platform'] and c['group']==case['group']]
        body += '<nav class="related-cases" aria-label="Related use cases"><h2>Related use cases</h2><ul>'+''.join('<li>'+self.link(c['id'],c['title'],current)+'</li>' for c in group if c['id']!=case['id'])+'</ul>'+anchor('catalog/index.html','Return to all use cases',current)+'</nav></main></div>'
        self.write(current,self.page(title,body,current,'cases','case'))

    def case_index(self):
        current='catalog/index.html'
        data=json.loads((ROOT/'catalog/use-cases.json').read_text())
        groups=defaultdict(list)
        for c in self.cases:
            groups[(c['platform'],c['group'])].append(c)
        controls='<form class="catalog-search" role="search"><label for="case-search">Search use cases</label><input id="case-search" type="search" placeholder="For example: incident triage, health report, SOP"><div class="search-options"><label>Product<select id="case-product"><option value="">All products</option>'+''.join('<option value="'+p+'">'+esc(n)+'</option>' for p,n in NAMES.items())+'</select></label><label>Group<select id="case-group"><option value="">All groups</option>'+''.join('<option>'+esc(group)+'</option>' for group in dict.fromkeys(c['group'] for c in self.cases))+'</select></label><button type="reset">Clear filters</button></div><p id="case-count" role="status"></p></form>'
        body='<main id="main" class="directory-main"><header><h1>Use cases</h1><p>Choose an operational task. Each use-case page explains the objective, workflow, applicable configuration, and completion criteria. Links lead directly to the corresponding product procedures.</p></header>'+controls+'<p id="case-empty" hidden>No use cases match these filters.</p><nav class="group-navigation" aria-label="Use-case groups"><ul>'
        for i,((p,group),cases) in enumerate(groups.items(),1):
            body+='<li><a href="#group-'+str(i)+'">'+esc(group)+' <span>'+str(len(cases))+'</span></a></li>'
        body+='</ul></nav>'
        for i,((p,group),cases) in enumerate(groups.items(),1):
            body+='<section class="case-group" id="group-'+str(i)+'"><header><p class="chapter-label">'+esc(NAMES[p])+'</p><h2>'+esc(group)+'</h2>'+paragraph(data['group_introductions'][group])+'</header><ul class="case-list">'
            for c in cases:
                body+='<li class="case-index-entry" id="'+c['id']+'" data-products="'+esc(' '.join(c['platforms']))+'" data-group="'+esc(group)+'"><h3>'+self.link(c['id'],c['title'],current)+'</h3>'+paragraph(c['objective'])+'<p class="case-meta">'+esc(c['actor'])+' · '+esc(c['cadence'])+'</p><span hidden class="search-text">'+esc(json.dumps(c,ensure_ascii=False))+'</span></li>'
            body+='</ul></section>'
        aliases=[]
        for old in self.aliases:
            targets=[self.targets[t] for t in old['targets']]
            aliases.append({'id':old['id'],'targets':[relative(t,current) for t in targets]})
            body+='<section class="alias-choice" id="'+old['id']+'" hidden><h2>'+esc(old['title'])+'</h2>'+paragraph(old['disposition'])+'<ul>'+''.join('<li>'+anchor(t,next((c['title'] for c in self.cases if c['id']==ident),ident),current)+'</li>' for ident,t in zip(old['targets'],targets))+'</ul></section>'
        routes={c['id']:relative(self.targets[c['id']],current) for c in self.cases}
        body+='</main><script type="application/json" id="case-routes">'+json.dumps({'aliases':aliases,'cases':routes}).replace('<','\\u003c')+'</script>'
        self.write(current,self.page('Use cases',body,current,'cases','directory'))
        md=['# Use cases','', 'Use the [searchable index](index.html) to browse by product and operational task. Each linked page includes its configuration and direct procedure references.','']
        for (p,group),cases in groups.items():
            md+=['## '+NAMES[p]+' — '+group,'',data['group_introductions'][group],'']
            for c in cases:
                md+=['### ['+c['title']+']('+c['id']+'.html)','',c['objective'],'',*c['narrative'],'']
        self.write('catalog/use-cases.md','\n'.join(md))

    def home(self):
        current='index.html'
        descriptions={'devops':'Resource access, operational evidence, incident investigation, retained knowledge, and controlled execution.',
                      'security':'Application sources, assessment configuration, authentication, findings, and repair verification.',
                      'finops':'Cost-data access, organizational context, task execution, reporting, and publication.',
                      'architecture':'The approved concept model, product-specific resource relationships, and cross-service evidence handoffs.'}
        order=('architecture','devops','security','finops')
        body='<main id="main" class="directory-main"><header><h1>AWS operational agents</h1><p>Technical guides for AWS DevOps Agent, AWS Security Agent, and AWS FinOps Agent. Start with the cross-service overview to understand the model, or select a product guide for configuration and operating procedures.</p></header><section><h2>Guides</h2><ol class="guide-list">'
        for p in order:
            body+='<li><h3>'+anchor('guides/'+p+'.html',NAMES[p],current)+'</h3>'+paragraph(descriptions[p])+'<ol class="chapter-links">'+''.join('<li>'+anchor('guides/'+p+'.html#chapter-'+c['slug'],c['title'],current)+'</li>' for c in CHAPTERS[p])+'</ol></li>'
        body+='</ol></section><section><h2>Find an operational task</h2><p>'+anchor('catalog/index.html','Browse the 30 approved use cases',current)+'. Search by task, product, or use-case group. Configuration recipes and verification steps are included in the selected use case; separate knowledge of the documentation schema is not required.</p></section><section><h2>Reference and presentations</h2><p>'+anchor('catalog/resource-models.html','Resource model',current)+' defines the product objects and ownership labels. '+anchor('presentations/index.html','HTML presentations',current)+' provide the teaching editions of the guides.</p></section></main>'
        self.write(current,self.page('Guides',body,current,'guides','home'))
        current='presentations/index.html'
        rows=[]
        for p,d in DECKS.items():
            seconds=sum(s['seconds'] for s in d['slides']);demo=sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')
            rows.append('<tr><th scope="row">'+anchor('presentations/'+p+'.html',NAMES[p],current)+'</th><td>'+str(len(d['slides']))+'</td><td>'+str(seconds//60)+' min</td><td>'+str(demo//60)+' min, included</td><td>'+anchor('guides/'+p+'.html','Guide',current)+'</td></tr>')
        body='<main id="main" class="directory-main"><h1>HTML presentations</h1><p>Open a presentation to navigate slides, read notes, and use the session timer. Durations include the prepared-result exercise; questions and breaks are additional.</p><div class="table-wrap"><table><thead><tr><th>Presentation</th><th>Slides</th><th>Duration</th><th>Exercise</th><th>Detailed reading</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div></main>'
        self.write(current,self.page('Presentations',body,current,'presentations','presentations'))

    def finish_other_pages(self):
        """Give existing model/deck renderers the same shell without changing content."""
        paths=['catalog/resource-models.html']+['presentations/'+p+'.html' for p in self.guides]
        for current in paths:
            soup=BeautifulSoup(self.rewrite((ROOT/current).read_text(),current),'html.parser')
            for n in soup.select('.site-header,.skip'):
                n.decompose()
            new=BeautifulSoup(self.header(current,'model' if 'resource-models' in current else 'presentations'),'html.parser')
            for node in reversed(list(new.contents)):
                soup.body.insert(0,node)
            style=soup.new_tag('style');style.string=(HERE/'reading.css').read_text();soup.head.append(style)
            if 'resource-models' in current:
                note=soup.select_one('.eyebrow')
                if note:note.decompose()
            self.write(current,str(soup))

    def readme(self):
        lines=['# AWS operational agents','',
               'Open `index.html` from a repository checkout. HTML files work locally without a server. GitHub file preview shows source rather than running the controls.','',
               '## Reading paths','',
               '| Read | Location |','|---|---|',
               '| Learn the model and operating procedures | [Guides](index.html) |',
               '| Apply an operational workflow | [Use cases](catalog/index.html) |',
               '| Look up product objects and relationships | [Resource model](catalog/resource-models.html) |',
               '| Present the material | [HTML presentations](presentations/index.html) |','',
               'Guides distinguish workspace organization, definition, context, invocation, integrations, network connectivity, execution controls, managed functions, outputs, and administration. They have chapter navigation and one search. Each use case has a dedicated page with its narrative, workflow, configuration recipes, verification criteria, and technical references. The product guides explain concrete platform facilities and their operating mechanisms by capability dimension. The frozen dependency registers supply references, not a product taxonomy.','',
               '## Product editions','', '| Subject | Guide | Markdown | Presentation | Duration |','|---|---|---|---|---|']
        for p,d in DECKS.items():
            total=sum(s['seconds'] for s in d['slides'])//60;demo=sum(s['seconds'] for s in d['slides'] if s['kind']=='demo')//60
            lines.append(f'| {NAMES[p]} | [Read](guides/{p}.html) | [Source](guides/{p}.md) | [Slides](presentations/{p}.html) | {total} min, including {demo} min exercise |')
        lines+=['','## Source ownership and build','',
                'The six JSON registers in `catalog/` are frozen at `'+BASELINE+'`. Reader navigation and page composition are maintained in `tools/docs/reader.py`, `reading.css`, and `reading.js`. This revision preserves the model, case selection, and workflow semantics. Product exposition follows the supplied capability outline; targeted source qualifications are recorded in qa/exposition-review.json. Former identifiers remain lookup metadata in `catalog/aliases.json`; they are not a reader-facing chapter.','',
                '```text','guides/          Canonical guide prose and HTML books','catalog/         Frozen records, use-case pages, and resource reference','presentations/   HTML decks and notes','assets/diagrams/ Source-linked SVG diagrams','tools/docs/      One renderer and validation toolchain','qa/              Review and validation records','examples/        Synthetic worked evidence','applications/    Independent application; not modified','```','',
                '```sh','python -m pip install -r tools/docs/requirements.txt','python -m playwright install chromium','python tools/docs/build.py','python tools/docs/check.py --browser','```','',
                'Graphviz (`dot`) is also required. [Validation scope](VALIDATION.md), [source coverage](guides/coverage.md), and [publishing instructions](PUBLISHING.md) distinguish document checks from live service testing. Git retains previous versions; no manual archives are maintained.']
        self.write('README.md','\n'.join(lines))

    def run(self):
        for p,g in self.guides.items():
            self.guide(p,g)
        for case in self.cases:
            self.case_page(case)
        self.case_index();self.home();self.finish_other_pages();self.readme()
        for path in RETIRED:
            (ROOT/path).unlink(missing_ok=True)
        # Keep generated notes navigable after retiring record-type pages.
        for path in (ROOT/'presentations').glob('*-notes.md'):
            text=path.read_text()
            for ident,target in self.targets.items():
                for old in ('mechanisms','features','profiles'):
                    text=text.replace('../catalog/'+old+'.html#'+ident,relative(target,path.relative_to(ROOT).as_posix()))
            self.write(path.relative_to(ROOT),text)


def render(guides, render_markdown, write):
    Reader(guides,render_markdown,write).run()
