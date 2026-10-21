"""Local, immutable records with atomic imports. Hashes detect content changes, not authorship."""
from __future__ import annotations
import hashlib, json, sqlite3, threading, os
from datetime import datetime, timezone
from pathlib import Path
from .models import Bundle

def now():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

def canonical(record):
    def normalize(value):
        if isinstance(value, dict):
            return {k: normalize(v) for k, v in value.items()}
        if isinstance(value, list):
            return [normalize(v) for v in value]
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
    return json.dumps(normalize(record), sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)

def digest(record):
    return hashlib.sha256(canonical(record).encode()).hexdigest()

def ref(record):
    return f"{record['kind']}:{record['id']}@{record['revision']}"

def strict_json(text):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError(f'Duplicate JSON key: {k}')
            result[k] = v
        return result
    def invalid(value):
        raise ValueError(f'Non-finite JSON number: {value}')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)

class Conflict(ValueError):
    pass

class Store:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / 'workspace.sqlite3'
        self.lock = threading.RLock()
        with self.connect() as con:
            # A single-process local application does not need WAL or a network filesystem.
            con.execute('PRAGMA journal_mode=DELETE')
            con.execute('CREATE TABLE IF NOT EXISTS records (ref TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL, sha256 TEXT NOT NULL, origin TEXT NOT NULL, created_at TEXT NOT NULL)')
            con.execute('CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT NOT NULL, action TEXT NOT NULL, detail TEXT NOT NULL)')
            con.execute('PRAGMA user_version=1')
        try:
            os.chmod(self.path, 0o600)
        except OSError:
            pass

    def connect(self):
        con = sqlite3.connect(self.path, timeout=15)
        con.row_factory = sqlite3.Row
        con.execute('PRAGMA busy_timeout=15000')
        return con

    def all(self):
        with self.connect() as con:
            return [self.unpack(r) for r in con.execute('SELECT * FROM records ORDER BY created_at, ref')]

    @staticmethod
    def unpack(row):
        return {'record': json.loads(row['payload']), 'meta': {'ref': row['ref'], 'sha256': row['sha256'], 'origin': row['origin'], 'created_at': row['created_at']}}

    def get(self, reference):
        with self.connect() as con:
            row = con.execute('SELECT * FROM records WHERE ref=?', (reference,)).fetchone()
        if row is None:
            raise KeyError(reference)
        return self.unpack(row)

    def audit(self, action, detail):
        with self.lock, self.connect() as con:
            con.execute('INSERT INTO audit(at,action,detail) VALUES (?,?,?)', (now(), action, canonical(detail)))

    def audit_entries(self):
        with self.connect() as con:
            return [{'seq': r['seq'], 'at': r['at'], 'action': r['action'], 'detail': json.loads(r['detail'])} for r in con.execute('SELECT * FROM audit ORDER BY seq DESC LIMIT 200')]

    def prepare(self, raw):
        validated = Bundle.model_validate(raw).model_dump(mode='json')
        records = validated['records']
        keys = [ref(r) for r in records]
        if len(keys) != len(set(keys)):
            raise ValueError('Bundle repeats an immutable record reference')
        manifest = validated.get('manifest')
        if manifest is not None:
            if set(manifest) != set(keys):
                raise ValueError('Manifest must cover every record and no other records')
            for record in records:
                if manifest[ref(record)] != digest(record):
                    raise ValueError('Manifest hash mismatch: ' + ref(record))
        with self.connect() as con:
            existing = {r['ref']: r['sha256'] for r in con.execute('SELECT ref,sha256 FROM records')}
        all_keys = set(existing) | set(keys)
        decisions = []
        for r in records:
            key = ref(r)
            if key in existing and existing[key] != digest(r):
                raise Conflict(f'{key} already exists with different content; assign a new revision')
            d = r['data']
            expected = {'scenario_ref': 'scenario', 'snapshot_ref': 'snapshot', 'run_ref': 'execution_run', 'validation_ref': 'validation_run'}
            for field, kind in expected.items():
                value = d.get(field)
                if value is not None:
                    if not value.startswith(kind + ':'):
                        raise ValueError(f'{key}: {field} must reference a {kind}')
                    if value not in all_keys:
                        raise ValueError(f'{key}: missing dependency {value}; include it in this bundle or import it first')
            decisions.append({'ref': key, 'action': 'unchanged' if key in existing else 'create', 'sha256': digest(r)})
        return records, decisions

    def import_bundle(self, raw, origin='imported', dry_run=False):
        with self.lock:
            records, decisions = self.prepare(raw)
            if dry_run:
                return {'decisions': decisions, 'created': sum(d['action'] == 'create' for d in decisions), 'committed': False}
            at = now()
            with self.connect() as con:
                for record, decision in zip(records, decisions):
                    if decision['action'] == 'create':
                        con.execute('INSERT INTO records VALUES (?,?,?,?,?,?)', (ref(record), record['kind'], canonical(record), digest(record), origin, at))
                con.execute('INSERT INTO audit(at,action,detail) VALUES (?,?,?)', (at, 'import' if origin == 'imported' else origin, canonical({'records': decisions})))
            return {'decisions': decisions, 'created': sum(d['action'] == 'create' for d in decisions), 'committed': True}

    def export(self):
        entries = self.all()
        return {'schema_version': '1.0', 'kind': 'validation_bundle', 'records': [e['record'] for e in entries], 'manifest': {e['meta']['ref']: e['meta']['sha256'] for e in entries}}

    def backup(self, target):
        with self.lock, self.connect() as source, sqlite3.connect(target) as dest:
            source.backup(dest)
