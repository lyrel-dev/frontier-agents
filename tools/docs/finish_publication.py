#!/usr/bin/env python3
"""Complete publication metadata once; retain source files rather than stale templates."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
build=ROOT/'tools/docs/build.py'
text=build.read_text()
lines=text.splitlines(True)
removed=[line for line in lines if line.startswith("    write('CHANGELOG.md',") or line.startswith("    write('EDITORIAL_STANDARD.md',")]
assert len(removed)==2
text=''.join(line for line in lines if line not in removed)
needle='<h2>Reading order</h2>'
assert needle in text
text=text.replace(needle,'<h2>Implementation references</h2><p>Follow a workflow into its <a href="catalog/mechanisms.html">mechanisms</a>, inspect the <a href="catalog/features.html">features and affected outcomes</a>, and choose a <a href="catalog/profiles.html">configuration profile</a>. The <a href="catalog/migration.md">consolidation map</a> explains where every former record now belongs.</p>'+needle)
compile(text,str(build),'exec');build.write_text(text)
editorial=ROOT/'EDITORIAL_STANDARD.md'
current=editorial.read_text()
addition='''## Outcomes and implementation relationships

Maintain each operational objective once. Every primary case has a responsible actor, completion criteria and connected narrative. Preserve separate cases when the result, decision or authorization boundary differs. Treat cadence, network route, identity and format as variants when the operational objective remains the same.

Workflow steps identify purpose, responsible actor, required/optional/conditional mechanism, its condition, concrete feature configuration, effect, acceptance evidence and failure handling. Human review is labeled as a team procedure rather than invented native behavior. A feature is a concrete service facility; its mechanism explains a documented process. The guide remains the detailed technical authority.

An implementation profile supplies reusable configuration choices and proposed acceptance exercises. It is not a deployable AWS schema or a claim that products share permissions, runtime or memory. Product-specific publication and mutation controls remain attached to the selected variant after consolidation.

Keep old identifiers and titles as aliases to the maintained successor. A split record offers all relevant successors rather than choosing silently. Alias data is navigation metadata, not an archived copy of superseded prose. Preserve searchable supporting references without counting them as primary outcomes.

Validate both directions: case to mechanism to feature, and feature to affected cases. Required dependencies may block the selected implementation; optional dependencies change its available context; conditional dependencies apply only to the declared profile. These modeled relationships do not constitute live account-readiness evidence.

'''
assert '## Outcomes and implementation relationships' not in current
current=current.replace('## Diagrams\n',addition+'## Diagrams\n')
editorial.write_text(current)
(ROOT/'CHANGELOG.md').write_text('''# Documentation changes

## 22 October 2026 — linked operational-outcome catalog

Consolidated 54 former records into 30 primary outcomes: 14 DevOps, eight Security, seven FinOps and one shared operational review. Preserved legitimate variants and reclassified 13 records as supporting mechanisms or configuration procedures. Forecasting and commitment coverage are now separate outcomes.

Each case contains an actor, objective, completion criteria and a workflow linked to mechanisms and concrete feature configuration. Dependency records distinguish required, optional and conditional behavior, effects, proposed verification and failure handling. Mechanism, feature and implementation-profile reading indexes support forward and reverse navigation.

Former identifiers remain searchable aliases. The combined forecasting/coverage identifier offers both successors. The shared review is counted once and appears in each applicable platform filter. Native operational inquiry is distinct from configured custom-agent reporting.

Updated the HTML reports, source-linked presentation sequence and relationship diagram. Added regression tests for unresolved mechanisms, missing failure handling, ambiguous split aliases and unqualified cross-product configuration. Browser checks cover navigation, filtering, aliases, print restoration and presentation behavior. No live AWS work or measured benefit is claimed.

Editorial rules and this change record are maintained source files rather than overwritten templates. Temporary migration inputs and scripts are removed after application. No manual archives or binary presentations are produced; Git retains earlier revisions. The independent application and its workflow remain unchanged.
''')
Path(__file__).unlink()
