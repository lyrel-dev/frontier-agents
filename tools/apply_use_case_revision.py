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
old = "assert page.locator('.index-card').count()==4"
new = "assert page.locator('.index-card').count()==5;assert page.locator('#use-case-catalog-card').count()==1"
if old not in check_text:
    raise RuntimeError("Expected collection-card assertion was not found")
check_path.write_text(check_text.replace(old, new), encoding="utf-8")
for path in (ROOT / "tools").glob(".usecase-payload-*"):
    path.unlink()
Path(__file__).unlink()
