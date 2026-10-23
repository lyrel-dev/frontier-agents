"""Correct inline SVG CSS references and verify actual rendered arrowheads."""
from pathlib import Path
import json
here=Path(__file__).resolve().parent
p=here/'build.py';s=p.read_text()
old="    svg.attrs.pop('width',None);svg.attrs.pop('height',None)\n    return str(svg)"
new='''    # Inline diagrams share a document: namespace both attribute references
    # and CSS fragment URLs, then scope selectors to this SVG instance.
    styles = svg.find_all('style')
    if styles:
        svg['id'] = prefix+'-svg-root'
        for style in styles:
            css = style.get_text()
            css = re.sub(r'url\\(#([^)]*)\\)', lambda m: 'url(#'+mapping.get(m[1],m[1])+')', css)
            def scope_rule(match):
                selectors = ','.join('#'+svg['id']+' '+part.strip() for part in match[2].split(','))
                return match[1]+selectors+'{'
            css = re.sub(r'(^|})([^{}]+)\\{', scope_rule, css)
            style.string = css
    svg.attrs.pop('width',None);svg.attrs.pop('height',None)
    return str(svg)'''
if old not in s:raise ValueError('Inline SVG renderer changed')
p.write_text(s.replace(old,new,1))
p=here/'teaching_check.py';s=p.read_text()
old="                                if clipped:raise AssertionError(s['diagram']+': clipped node text '+json.dumps(clipped))"
new=old+'''
                                bad_markers=page.locator('.slide:visible').evaluate("""root=>[...root.querySelectorAll('svg[data-layout]')].flatMap(svg=>{const marker=svg.querySelector('marker');return [...svg.querySelectorAll('path[data-edge]')].filter(p=>!getComputedStyle(p).markerEnd.includes('#'+marker.id)).map(p=>p.dataset.edge)})""")
                                if bad_markers:raise AssertionError(s['diagram']+': missing scoped arrowheads '+str(bad_markers))'''
if old not in s:raise ValueError('Teaching geometry check changed')
s=s.replace(old,new,1).replace("'diagram_text_bounds':'passed'", "'diagram_text_bounds':'passed','scoped_arrowheads':'passed'")
p.write_text(s)
p=here.parents[1]/'qa/educational-review.json';r=json.loads(p.read_text())
r['visual_review']['corrections'].append('Namespace CSS marker URLs and scope SVG styles per inline diagram; test computed marker references in the HTML presentation.')
r['last_source_retrieval']={'custom_agents':'Direct official page confirms prompt, selected tools, assigned skills and invocation; its representation omits some retained-context material present in the supplied source and earlier indexed review.','agent_spaces':'Direct official page confirms account, integration, user and history isolation.','managed_agents':'Final direct re-fetch returned a cache miss; retain the supplied source and earlier reviewed evidence rather than claim every source was freshly retrieved.'}
p.write_text(json.dumps(r,indent=2)+'\n')
Path(__file__).unlink()
