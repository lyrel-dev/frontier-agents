"""Final scope-boundary correction; no concept or case record is modified."""
from pathlib import Path
import json
here=Path(__file__).resolve().parent
p=here/'teaching_diagrams.py';s=p.read_text()
s=s.replace('viewBox="0 0 1400 825"','viewBox="0 0 1440 825"')
s=s.replace('<rect x="240" y="35" width="900" height="580"','<rect data-scope-boundary="true" x="240" y="35" width="1160" height="580"')
s=s.replace('M1385 350 H1393 V705 H1385','M1385 350 H1420 V705 H1385')
s=s.replace('Question, incident or configured start','Question, signal or trigger')
s=s.replace('Findings, proposals, artifacts and history','Findings, plans, artifacts and history')
p.write_text(s)
p=here/'teaching_check.py';s=p.read_text()
needle="        geometry[key]={'fixed_layout':root.get('data-layout'),'components':len(positions)}"
replacement='''        scope=next((n for n in root.iter() if n.get('data-scope-boundary')=='true'),None)
        if scope is not None:
            sx,sy,sw,sh=(float(scope.get(a)) for a in ('x','y','width','height'))
            for node in (n for n in root.iter() if 'data-node' in n.attrib):
                x,y,w,h=map(float,node.get('data-box').split(','))
                inside=x>=sx and y>=sy and x+w<=sx+sw and y+h<=sy+sh
                if node.get('data-node')=='result' and not inside:errors.append(key+': execution record shown outside scope')
                if node.get('data-owner')=='external' and inside:errors.append(key+': external source or actor placed inside scope')
        geometry[key]={'fixed_layout':root.get('data-layout'),'components':len(positions),'scope_boundary_checked':scope is not None}'''
if needle not in s:raise ValueError('Expected geometry record not found')
p.write_text(s.replace(needle,replacement,1))
p=here.parents[1]/'qa/educational-review.json';r=json.loads(p.read_text())
r['visual_review']['amended_asset_review']={'path':'assets/diagrams/teaching-devops-coordination.svg','git_blob_sha':'eefb3804e01a5cad7d87957acf2708e3d5d94acb','method':'Copied the fetched SVG bytes, verified the Git blob hash, rendered locally and visually inspected the amended role, label and connector layout.'}
r['visual_review']['corrections'].append('Extend the visible workspace boundary around its execution results; external actors, sources and publication destinations remain outside.')
p.write_text(json.dumps(r,indent=2)+'\n')
Path(__file__).unlink()
