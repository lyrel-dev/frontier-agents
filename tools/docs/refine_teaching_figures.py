"""One-time visual and semantic refinement before the first build."""
from pathlib import Path
p=Path(__file__).resolve().parent/'teaching_diagrams.py'
s=p.read_text()
# Keep all color meanings unchanged even when a workflow is not emphasizing a node.
s=s.replace("        if ident not in active:\n            fill='#f4f6f8';stroke='#9aa7b2'\n",'')
s=s.replace("weight='3' if ident in active else '1.3'","weight='4' if ident in active else '1'")
for old,new in [('205, 116','205, 140'),('260, 118','260, 140'),('840, 130','840, 140'),('350, 112','350, 140'),('235, 112','235, 140'),('215, 116','215, 140'),('205, 112','205, 140')]:
 s=s.replace(old,new)
s=s.replace("        out.append(f'<path data-edge=\"{a}-{b}\" class=\"{cls}\" d=\"{d}\"/>')", "        reverse=' marker-start=\"url(#arrow)\"' if (a,b) in (('execution','connections'),('connections','sources')) else ''\n        out.append(f'<path data-edge=\"{a}-{b}\" class=\"{cls}\" d=\"{d}\"{reverse}/>')")
# Source access has a return observation; input/context relations remain one-way.
s=s.replace('font-size:18px}.tag','font-size:17px}.tag')
p.write_text(s)
# Show the same narrowly scoped Security reuse view in the guide as well.
g=p.parents[2]/'guides/security.md'
t=g.read_text();needle='The capability chapters below retain the detailed configuration procedures'
if needle in t:t=t.replace(needle,'![Specific retained state and its consumer](../assets/diagrams/teaching-security-context.svg)\n\n'+needle,1)
g.write_text(t)
Path(__file__).unlink()
