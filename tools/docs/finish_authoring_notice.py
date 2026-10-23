"""One-time correction of the maintained authoring notice."""
from pathlib import Path
p=Path(__file__).resolve().parent/'build.py'
text=p.read_text()
old='Authored product prose lives in guides/*.md. Detailed mechanism blocks are generated from the frozen register.'
new='Product capability explanations and official references are authored in guides/*.md. Frozen registers supply identifiers and relationships; they do not generate chapter prose or define a homogeneous product taxonomy.'
if old not in text:raise ValueError('Obsolete authoring notice not found')
text=text.replace(old,new)
text=text.replace('Update rendered navigation without introducing another parallel guide or record-type index.', 'Keep the supplied capability dimensions, detailed product explanations, and separate use-case catalog. Do not replace explanation with registry-field cards or add another parallel guide.')
text=text.replace('Product-specific resource identities and relationships were reviewed on 22 October 2026; retained sections keep their earlier references.', 'Product-specific resource identities and relationships retain the 22 October review. The capability exposition and targeted October 23 source checks are recorded in [exposition review](../qa/exposition-review.json); other retained sections keep their earlier references.')
p.write_text(text)
Path(__file__).unlink()
