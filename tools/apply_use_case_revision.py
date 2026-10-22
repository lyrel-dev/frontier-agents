#!/usr/bin/env python3
"""One-time source migration for the structured use-case catalog revision."""
from pathlib import Path
import base64
import io
import zipfile

ROOT = Path(__file__).resolve().parents[1]
chunks = [ROOT / f"tools/.usecase-payload-{i:02d}" for i in range(7)]
payload = "".join(path.read_text(encoding="utf-8").strip() for path in chunks)
with zipfile.ZipFile(io.BytesIO(base64.b64decode(payload))) as archive:
    for name in archive.namelist():
        target = ROOT / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.read(name))
for path in chunks:
    path.unlink()
Path(__file__).unlink()
