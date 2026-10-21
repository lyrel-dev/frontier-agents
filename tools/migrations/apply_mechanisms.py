#!/usr/bin/env python3
"""Import the reviewed mechanism documentation once, verifying all source bytes."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

ROOT = Path(__file__).resolve().parents[2]
REVISION = '2026-10-21-mechanisms-v1'
PAYLOAD_SHA256 = '4750eab49ad88ff3a70699dbad6c6acbe9c18883b3faa48e3616eb932e1c5fee'
ALLOWED = {
    'content/mechanisms.json',
    'tools/build_mechanisms.py',
    'tools/build_suite.py',
    'tools/qa_mechanisms_browser.py',
    'qa/mechanism-browser-validation.json',
    'qa/mechanism-render-validation.json',
}


def apply() -> None:
    marker = ROOT / 'content/mechanisms-import.json'
    if marker.exists():
        recorded = json.loads(marker.read_text(encoding='utf-8'))
        if recorded.get('revision') == REVISION and recorded.get('payload_sha256') == PAYLOAD_SHA256:
            return
        raise ValueError('Unexpected mechanism import marker; review before updating.')
    encoded = ''.join((ROOT / f'tools/migrations/mechanisms-{i:02d}.b64').read_text(encoding='ascii').strip() for i in range(1, 8))
    payload = lzma.decompress(base64.b64decode(encoded, validate=True))
    if hashlib.sha256(payload).hexdigest() != PAYLOAD_SHA256:
        raise ValueError('Mechanism source payload integrity failure')
    patch = json.loads(payload)
    if set(patch) != ALLOWED:
        raise ValueError('Unexpected source path in mechanism import')
    changes = {}
    for name, record in patch.items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or name.startswith('.github/'):
            raise ValueError('Disallowed import path')
        before = path.read_bytes() if path.exists() else b''
        digest = hashlib.sha256(before).hexdigest()
        if digest == record['after']:
            continue
        if digest != record['before']:
            raise ValueError(f'Concurrent edit or unexpected input: {name}')
        text = before.decode('utf-8')
        for start, stop, replacement in reversed(record['edits']):
            text = text[:start] + replacement + text[stop:]
        after = text.encode('utf-8')
        if hashlib.sha256(after).hexdigest() != record['after']:
            raise ValueError(f'Output integrity failure: {name}')
        changes[path] = after
    for path, data in changes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    marker.write_text(json.dumps({'revision': REVISION, 'payload_sha256': PAYLOAD_SHA256, 'workflow_files_changed': False}, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(changes)} reviewed mechanism source files; workflows unchanged.')


if __name__ == '__main__':
    apply()
