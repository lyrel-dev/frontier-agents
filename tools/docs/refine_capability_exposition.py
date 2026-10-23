"""Finalize contextual references and remove stale exposition notes; no registry writes."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
p=HERE/'reader.py';text=p.read_text()
needle='    def feature_detail(self, feature, current):'
helper='''    @staticmethod
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

'''
if needle not in text:raise ValueError('Missing reader feature method')
text=text.replace(needle,helper+needle)
text=text.replace("                explanation_sections = {'MX-D-QUERY':'D-21','MX-D-CUSTOM':'D-19','MX-S-PERSONALIZE':'S-13'}\n                mechanisms = [m for m in self.mechanisms.values() if m['platform']==product and explanation_sections.get(m['id'],m['review']['primary_section'])==sid]", "                mechanisms = [m for m in self.mechanisms.values() if m['platform']==product and self.mechanism_section(m)==sid]")
text=text.replace("f['sections'][0]==sid", "self.feature_section(f)==sid")
text=text.replace("sid in self.mechanisms[s['mechanism']]['sections']", "sid==self.mechanism_section(self.mechanisms[s['mechanism']])")
text=text.replace("self.section_link(s,current) for s in feature['sections']", "self.section_link(s,current) for s in dict.fromkeys([self.feature_section(feature),*feature['sections']])")
text=text.replace("        refs = list(dict.fromkeys(s for s in case['sections']))", "        refs = list(dict.fromkeys([*(self.mechanism_section(self.mechanisms[step['mechanism']]) for step in case['workflow'] if step['mechanism'] in self.mechanisms),*case['sections']]))")
# A shared case can use product-specific recipes. Its existing shared sources are still resolved in its own guide;
# only same-product workflow steps add source identifiers to the case's per-product reference register.
text=text.replace("source_ids = sorted({r for s in refs for r in g['sections'][s]['sources']})", "source_ids = sorted({r for s in refs if s in g['sections'] for r in g['sections'][s]['sources']})")
p.write_text(text)
p=ROOT/'guides/devops.md';text=p.read_text()
text=text.replace('Newer documentation moves learned topology, dependency, pipeline and tool-use knowledge into memory; older pages still call these learned skills.', 'The August 27 changelog records the move of learned topology, dependency, pipeline, and tool-use knowledge into memory. Some retrieved pages retain the earlier learned-skills terminology.')
text=text.replace('**Source-version decisions:** older cached pages and newer indexed AWS content differed for instruction navigation, custom-store attachment and learned-knowledge storage. This edition uses the newer indexed managed-agent, memory, asset and dated-change guidance for those points. The Region table was not reproduced as a complete regional inventory. A retrieval date is not a claim that AWS published the page on that date.', '**Source-version qualifications:** retrieved representations differ for instruction navigation, asset types, trigger coverage, custom-store access, and learned-knowledge storage. The dated change entries and topic-specific procedures support the selected descriptions; the differing representations are recorded in `qa/exposition-review.json`. The guide does not infer publication order from retrieval order or provide a complete regional inventory.')
text=text.replace('New integration and scheduling material and selected knowledge mechanisms were rechecked on 22 October 2026. Other retained explanations keep their existing sources and review boundaries.', 'The capability exposition follows the supplied outline. Agent definitions, triggers, assets, integration directions, release authentication, and selected knowledge behavior were checked for the 23 October 2026 revision. Retained procedures keep their existing references and review boundaries.')
text=text.replace('| Managed/custom execution | Routing, manual runs, schedules, cancellation, observation | Not every external incident provider reproduced |', '| Managed/custom execution | Definitions, routing, on-demand/scheduled/event invocation, continuation, cancellation | Provider-specific event payloads and full protocol schemas remain linked |')
text=text.replace('| Sandbox/release preview | Configuration and effect boundaries | Full release-profile authoring is deferred |', '| Sandbox/release preview | Runtime scope, test-profile fields, authentication, and effect boundaries | Complete environment and deployment procedures remain linked |')
text=text.replace('Newer indexed content used.', 'Retrieved-source qualifications are recorded in the review notes.')
for product in ('devops','security','finops'):
    target=ROOT/f'guides/{product}.md'
    s=text if product=='devops' else target.read_text()
    s=s.replace('## 11. Worked example and reference material','## 11. Appendix: worked example and reference material')
    target.write_text(s)
# These checks document freeze and rendering, not editorial success. Add the current review rather than imply
# that preservation alone validated the old mechanism names as a product taxonomy.
p=HERE/'check.py';text=p.read_text()
text=text.replace("'# Documentation validation\\n\\nStage 3 adds", "'# Documentation validation\\n\\nThe current [capability-exposition review](qa/exposition-review.json) follows the supplied ten-part outline. [Exposition checks](qa/exposition-checks.json) verify the chapter distinctions and frozen semantic sources. The previous dependency records remain traceability inputs, not a claim that every record is a native platform mechanism.\\n\\nStage 3 adds")
p.write_text(text)
p=HERE/'mechanism_detail.py';text=p.read_text()
start=text.find('"""');end=text.find('"""',start+3)
if start==0 and end>0:
    text='"""Validate the frozen dependency registry and retained claim mappings.\n\nAuthored guide prose explains the actual product capabilities and processes.\nThe registry provides compatibility identifiers; it is not a product taxonomy.\n"""'+text[end+3:]
p.write_text(text)
p=ROOT/'qa/exposition-review.json';d=json.loads(p.read_text())
d['link_review']='References to previously combined remote/release sections now resolve to the authored managed-workflow explanations; custom definition and invocation references are distinguished without rewriting frozen records.'
d['source_qualification_review']='Removed unsupported newer/older wording in retained DevOps notes; dated changes and retrieval discrepancies remain explicit.'
p.write_text(json.dumps(d,indent=2)+'\n')
Path(__file__).unlink()
