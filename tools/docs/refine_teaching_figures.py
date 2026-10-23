"""One-time visual and semantic refinement before the first build."""
from pathlib import Path
p=Path(__file__).resolve().parent/'teaching_diagrams.py'
s=p.read_text()
s=s.replace("        if ident not in active:\n            fill='#f4f6f8';stroke='#9aa7b2'\n",'')
s=s.replace("weight='3' if ident in active else '1.3'","weight='4' if ident in active else '1'")
for old,new in [('205, 116','205, 140'),('260, 118','260, 140'),('840, 130','840, 140'),('350, 112','350, 140'),('235, 112','235, 140'),('215, 116','215, 140'),('205, 112','205, 140')]:
 s=s.replace(old,new)
s=s.replace('width=max(18,int((w-24)/10.6))','width=max(14,int((w-24)/11.2))')
s=s.replace("        out.append(f'<path data-edge=\"{a}-{b}\" class=\"{cls}\" d=\"{d}\"/>')", "        reverse=' marker-start=\"url(#arrow)\"' if (a,b) in (('execution','connections'),('connections','sources')) else ''\n        out.append(f'<path data-edge=\"{a}-{b}\" class=\"{cls}\" d=\"{d}\"{reverse}/>')")
s=s.replace('font-size:18px}.tag','font-size:17px}.tag')
needle="    for ident,(x,y,w,h) in BOXES.items():"
extra='''    if view in ('review','mitigation','repair','optimization'):
        out.append('<path class="edge-soft" data-edge="result-operator" d="M1275 420 V625 H118 V610"/>')
        out.append('<text x="250" y="643" font-size="16">team review / acceptance</text>')
    if product == 'devops' and view == 'learning':
        out.append('<path class="edge-soft" data-edge="operator-feedback" d="M118 610 V632 H855 V540 H875"/>')
        out.append('<text x="245" y="625" font-size="16">verified correction</text>')
    if product == 'devops' and view == 'knowledge':
        out.append('<path class="edge-soft" data-edge="operator-skill" d="M118 470 V242 H690 V222"/>')
        out.append('<text x="285" y="237" font-size="16">reviewed procedure</text>')
'''
if needle not in s:raise ValueError('Diagram node loop not found')
s=s.replace(needle,extra+needle,1)
p.write_text(s)
g=p.parents[2]/'guides/security.md'
t=g.read_text();needle='The capability chapters below retain the detailed configuration procedures'
if needle in t:t=t.replace(needle,'![Specific retained state and its consumer](../assets/diagrams/teaching-security-context.svg)\n\n'+needle,1)
g.write_text(t)
Path(__file__).unlink()
