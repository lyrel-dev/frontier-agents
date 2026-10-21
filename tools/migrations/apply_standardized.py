#!/usr/bin/env python3
"""Apply the reviewed editorial source revision; leave workflow permissions unchanged."""
from pathlib import Path
import base64, hashlib, json, lzma
ROOT = Path(__file__).resolve().parents[2]
def main():
    parts = sorted((ROOT/'tools/migrations').glob('editorial-*.b64'))
    payload = lzma.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts)))
    patch = json.loads(payload)
    changes = {}
    for name, record in patch.items():
        if name.startswith('.github/'):
            print(f'Preserving existing workflow: {name}')
            continue
        path = (ROOT/name).resolve()
        if not path.is_relative_to(ROOT): raise ValueError('Unsafe path')
        before = path.read_bytes() if path.exists() else b''
        digest = hashlib.sha256(before).hexdigest()
        if digest == record['after']: continue
        if digest != record['before']: raise ValueError(f'Concurrent edit or unexpected input: {name}')
        if 'json_edits' in record:
            obj = json.loads(before)
            for edit in record['json_edits']:
                keys, value = edit[:2]
                if not keys: obj=value; continue
                parent=obj
                for key in keys[:-1]: parent=parent[key]
                if len(edit)>2: del parent[keys[-1]]
                else: parent[keys[-1]]=value
            after=(json.dumps(obj, ensure_ascii=False, indent=2)+'\n').encode()
        else:
            text=before.decode()
            for start,stop,value in reversed(record['edits']): text=text[:start]+value+text[stop:]
            after=text.encode()
        if hashlib.sha256(after).hexdigest()!=record['after']: raise ValueError(f'Output integrity failure: {name}')
        changes[path]=after
    for path, data in changes.items():
        path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    print(f'Applied {len(changes)} source files with before/after SHA-256 verification.')
if __name__=='__main__': main()
