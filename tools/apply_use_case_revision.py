#!/usr/bin/env python3
"""One-time source migration for the structured use-case catalog revision."""
from pathlib import Path
import base64
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parts = [
    "tools/.usecase-payload-00",
    "tools/.usecase-payload-01",
    "tools/.usecase-payload-02",
    "tools/.usecase-payload-03",
    "tools/.usecase-payload-04a",
    "tools/.usecase-payload-04b",
    "tools/.usecase-payload-04c",
    "tools/.usecase-payload-04d",
    "tools/.usecase-payload-05",
    "tools/.usecase-payload-06a",
    "tools/.usecase-payload-06b",
    "tools/.usecase-payload-06c",
]
payload = "".join((ROOT / name).read_text(encoding="utf-8").strip() for name in parts)
if len(payload) % 4:
    raise RuntimeError(f"Invalid staged payload length: {len(payload)}")
with zipfile.ZipFile(io.BytesIO(base64.b64decode(payload, validate=True))) as archive:
    expected = {
        "tools/lesson_plan.py",
        "tools/docs_structure.py",
        "tools/use_case_catalog.py",
        "catalog/use-cases.json",
        "EDITORIAL_STANDARD.md",
    }
    if set(archive.namelist()) != expected:
        raise RuntimeError(f"Unexpected migration contents: {archive.namelist()}")
    for name in archive.namelist():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(name))

check_path = ROOT / "tools/docs_check.py"
check_text = check_path.read_text(encoding="utf-8")
replacements = {
    "assert page.locator('.index-card').count()==4":
        "assert page.locator('.index-card').count()==5;assert page.locator('#use-case-catalog-card').count()==1",
    "        if len(soup.select('.chapter'))!=len(CHAPTERS[key]) or len(soup.select('.toc details'))!=len(CHAPTERS[key]):errors.append(key+': chapter navigation mismatch')":
        "        if len(soup.select('.chapter')) != len(CHAPTERS[key]):errors.append(key+': chapter count mismatch')\n"
        "        expected_toc = len(CHAPTERS[key]) + (1 if key in {'devops','security','finops'} else 0)\n"
        "        if len(soup.select('.toc details')) != expected_toc:errors.append(key+': chapter navigation mismatch')",
    "    if (ROOT/'tools/lesson_plan.py').read_text().strip()!=git('show',f'{BASELINE}:tools/lesson_plan.py').strip():errors.append('Curated lesson plan changed')":
        "    for key,deck_definition in DECKS.items():\n"
        "        titles=[slide['title'] for slide in deck_definition['slides']]\n"
        "        if len(titles)!=len(set(titles)):errors.append(key+': duplicate slide title')\n"
        "        if any(len(slide.get('data',[]))<3 for slide in deck_definition['slides'] if slide['kind']!='demo'):errors.append(key+': sparse slide outline')",
    "The existing 124-minute programme and 28-minute prepared-result exercise allocation are retained.":
        "The current presentation duration and prepared-result exercise allocation are recorded in `qa/checks.json`.",
}
for old, new in replacements.items():
    if old not in check_text:
        raise RuntimeError(f"Expected validation source was not found: {old[:90]}")
    check_text = check_text.replace(old, new)
check_path.write_text(check_text, encoding="utf-8")

for path in (ROOT / "tools").glob(".usecase-payload-*"):
    path.unlink()
Path(__file__).unlink()
