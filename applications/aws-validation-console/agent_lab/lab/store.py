"""Local single-worker durable journal and rebuildable projections.

WAL is for a local disk, not a shared network filesystem. Records, events and
operation intents are committed before AWS writes. This is not a distributed
transaction and does not claim exactly-once provider execution.
"""
from __future__ import annotations
from contextlib import contextmanager
import json
import os
from pathlib import Path
import sqlite3
import threading
import uuid
from .util import canonical, digest, iso, uid, Blocked

TERMINAL = {'CLOSED','CLOSED_ABORTED','CLOSED_BLOCKED','BLOCKED'}


class Store:
    def __init__(self, directory: str | Path):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path = self.directory / 'experiments.sqlite3'
        self.lock = threading.RLock()
        with self.connect() as db:
            db.executescript('''
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY, kind TEXT NOT NULL, owner TEXT NOT NULL,
                created_at TEXT NOT NULL, sha256 TEXT NOT NULL, data TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS record_owner ON records(owner,kind);
            CREATE TABLE IF NOT EXISTS entities (
                id TEXT PRIMARY KEY, kind TEXT NOT NULL, state TEXT NOT NULL,
                revision INTEGER NOT NULL, updated_at TEXT NOT NULL, data TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL,
                at TEXT NOT NULL, type TEXT NOT NULL, previous_hash TEXT NOT NULL,
                sha256 TEXT NOT NULL, data TEXT NOT NULL);
            CREATE INDEX IF NOT EXISTS event_owner ON events(owner,sequence);
            CREATE TABLE IF NOT EXISTS operations (
                id TEXT PRIMARY KEY, owner TEXT NOT NULL, name TEXT NOT NULL,
                token TEXT NOT NULL, state TEXT NOT NULL, request TEXT NOT NULL,
                request_sha256 TEXT NOT NULL, provider_id TEXT, response TEXT,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                UNIQUE(owner,name));
            CREATE TABLE IF NOT EXISTS probes (
                sequence INTEGER PRIMARY KEY AUTOINCREMENT, owner TEXT NOT NULL,
                scheduled_at TEXT NOT NULL, at TEXT NOT NULL, data TEXT NOT NULL,
                UNIQUE(owner,scheduled_at));
            CREATE INDEX IF NOT EXISTS probe_owner ON probes(owner,sequence);
            CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, data TEXT NOT NULL);
            CREATE TRIGGER IF NOT EXISTS records_no_update BEFORE UPDATE ON records BEGIN SELECT RAISE(ABORT,'Immutable record'); END;
            CREATE TRIGGER IF NOT EXISTS records_no_delete BEFORE DELETE ON records BEGIN SELECT RAISE(ABORT,'Immutable record'); END;
            CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT,'Immutable event'); END;
            CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT,'Immutable event'); END;
            CREATE TRIGGER IF NOT EXISTS probes_no_update BEFORE UPDATE ON probes BEGIN SELECT RAISE(ABORT,'Immutable probe'); END;
            CREATE TRIGGER IF NOT EXISTS probes_no_delete BEFORE DELETE ON probes BEGIN SELECT RAISE(ABORT,'Immutable probe'); END;
            ''')
        os.chmod(self.path, 0o600)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        db.execute('PRAGMA busy_timeout=15000')
        return db

    @contextmanager
    def transaction(self):
        with self.lock, self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()

    @staticmethod
    def _event(db, owner, event_type, data):
        previous = db.execute('SELECT sha256 FROM events ORDER BY sequence DESC LIMIT 1').fetchone()
        at = iso()
        obj = {'owner':owner,'at':at,'type':event_type,'previous_hash':previous[0] if previous else '', 'data':data}
        db.execute('INSERT INTO events(owner,at,type,previous_hash,sha256,data) VALUES(?,?,?,?,?,?)',
                   (owner,at,event_type,obj['previous_hash'],digest(obj),canonical(data)))

    def event(self, owner, event_type, data):
        with self.transaction() as db:
            self._event(db,owner,event_type,data)

    def put_record(self, kind, owner, data, record_id=None):
        record_id = record_id or uid(kind)
        at, sha = iso(), digest(data)
        with self.transaction() as db:
            old = db.execute('SELECT sha256 FROM records WHERE id=?',(record_id,)).fetchone()
            if old:
                if old['sha256'] != sha:
                    raise Blocked('Immutable record conflicts with existing content')
                return self.record(record_id)
            db.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',(record_id,kind,owner,at,sha,canonical(data)))
            self._event(db,owner,'record.saved',{'id':record_id,'kind':kind,'sha256':sha})
        return self.record(record_id)

    def record(self, record_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM records WHERE id=?',(record_id,)).fetchone()
        if not row:
            raise KeyError(record_id)
        out = dict(row); out['data'] = json.loads(out['data'])
        if digest(out['data']) != out['sha256']:
            raise Blocked('Stored record digest mismatch')
        return out

    def records(self, owner=None, kind=None):
        query, args = 'SELECT id FROM records WHERE 1=1', []
        if owner is not None:
            query += ' AND owner=?'; args.append(owner)
        if kind is not None:
            query += ' AND kind=?'; args.append(kind)
        with self.connect() as db:
            ids = [r[0] for r in db.execute(query+' ORDER BY rowid',args)]
        return [self.record(i) for i in ids]

    def create(self, kind, state, data, entity_id=None):
        entity_id = entity_id or uid(kind)
        with self.transaction() as db:
            db.execute('INSERT INTO entities VALUES(?,?,?,?,?,?)',(entity_id,kind,state,1,iso(),canonical(data)))
            self._event(db,entity_id,'entity.created',{'kind':kind,'state':state,'data':data})
        return self.entity(entity_id)

    def entity(self, entity_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM entities WHERE id=?',(entity_id,)).fetchone()
        if not row:
            raise KeyError(entity_id)
        out = dict(row); out['data'] = json.loads(out['data']); return out

    def entities(self, kind=None):
        with self.connect() as db:
            rows = db.execute('SELECT id FROM entities'+(' WHERE kind=?' if kind else '')+' ORDER BY rowid DESC', (kind,) if kind else ()).fetchall()
        return [self.entity(r[0]) for r in rows]

    def update(self, entity_id, *, state=None, changes=None, expected_revision=None, event='entity.updated'):
        with self.transaction() as db:
            row = db.execute('SELECT * FROM entities WHERE id=?',(entity_id,)).fetchone()
            if not row:
                raise KeyError(entity_id)
            if expected_revision is not None and row['revision'] != expected_revision:
                raise Blocked('Concurrent modification; reload the current record')
            data = json.loads(row['data']); data.update(changes or {})
            new_state = state or row['state']
            db.execute('UPDATE entities SET state=?, revision=revision+1, updated_at=?, data=? WHERE id=?',
                       (new_state,iso(),canonical(data),entity_id))
            self._event(db,entity_id,event,{'from':row['state'],'to':new_state,'changes':changes or {}})
        return self.entity(entity_id)

    def start_trial(self, entity_id, approval, *, started_at=None):
        """Reserve the environment atomically. Abort/block cannot race this check."""
        with self.transaction() as db:
            row = db.execute('SELECT * FROM entities WHERE id=?',(entity_id,)).fetchone()
            if not row or row['kind'] != 'trial' or row['state'] != 'READY':
                raise Blocked('Trial is not ready')
            active = [r for r in db.execute("SELECT id,state FROM entities WHERE kind='trial'")
                      if r['state'] not in TERMINAL | {'DRAFT','READY'} and r['id'] != entity_id]
            changes = [r for r in db.execute("SELECT id,state FROM entities WHERE kind='change'")
                       if r['state'] in {'APPROVED','RUNNING','UNKNOWN_REMOTE_STATE','ROLLBACK_APPROVED','ROLLING_BACK','RESTORE_REQUIRED'}]
            if active or changes:
                raise Blocked('Only one active workload experiment or change is permitted')
            data = json.loads(row['data'])
            if data.get('fis_campaign_id'):
                fleet = db.execute('SELECT kind,state,data FROM entities WHERE id=?', (data['fis_campaign_id'],)).fetchone()
                if (not fleet or fleet['kind'] != 'fis_campaign' or fleet['state'] != 'RUNNING'
                        or json.loads(fleet['data']).get('active_trial_id') != entity_id):
                    raise Blocked('The fleet queue is paused, cancelled or no longer owns this trial')
            data['approval_id'] = approval['id']; data['started_at'] = started_at or iso()
            db.execute('UPDATE entities SET state=?, revision=revision+1,updated_at=?,data=? WHERE id=?',
                       ('BASELINING',iso(),canonical(data),entity_id))
            self._event(db,entity_id,'trial.started',{'approval_id':approval['id'],'started_at':data['started_at']})
        return self.entity(entity_id)

    def reserve_change(self, entity_id, approval, *, rollback=False):
        """Atomically reserve one change slot; a compromised approval cannot race a trial."""
        with self.transaction() as db:
            row=db.execute('SELECT * FROM entities WHERE id=?',(entity_id,)).fetchone()
            allowed={'VERIFIED','RESTORE_REQUIRED'} if rollback else {'PROPOSED'}
            if not row or row['kind']!='change' or row['state'] not in allowed:
                raise Blocked('Change state changed before approval')
            data=json.loads(row['data'])
            for other in db.execute("SELECT * FROM entities WHERE kind='change'"):
                if other['id']!=entity_id and other['state'] in {'APPROVED','RUNNING','UNKNOWN_REMOTE_STATE','ROLLBACK_APPROVED','ROLLING_BACK','RESTORE_REQUIRED'}:
                    raise Blocked('Another change owns the execution slot')
            for trial in db.execute("SELECT * FROM entities WHERE kind='trial'"):
                if trial['state'] not in TERMINAL|{'DRAFT','READY'}:
                    if data.get('trial_id')!=trial['id']:
                        raise Blocked('Another workload trial owns the environment')
                    if not rollback and (trial['state']!='OBSERVING' or json.loads(trial['data']).get('abort_requested')):
                        raise Blocked('Trial no longer accepts mitigation execution')
            state='ROLLBACK_APPROVED' if rollback else 'APPROVED'
            data['rollback_approval_id' if rollback else 'approval_id']=approval['id']
            db.execute('UPDATE entities SET state=?,revision=revision+1,updated_at=?,data=? WHERE id=?',
                       (state,iso(),canonical(data),entity_id))
            self._event(db,entity_id,'change.approved',{'state':state,'approval_id':approval['id']})
        return self.entity(entity_id)

    def operation(self, owner, name):
        with self.connect() as db:
            row = db.execute('SELECT * FROM operations WHERE owner=? AND name=?',(owner,name)).fetchone()
        if not row:
            return None
        out = dict(row); out['request'] = json.loads(out['request'])
        if digest(out['request']) != out['request_sha256']:
            raise Blocked('Stored operation request digest mismatch')
        out['response'] = json.loads(out['response']) if out['response'] else None
        return out

    def intent(self, owner, name, request):
        with self.transaction() as db:
            row = db.execute('SELECT * FROM operations WHERE owner=? AND name=?',(owner,name)).fetchone()
            if row:
                if row['request_sha256'] != digest(request):
                    raise Blocked('Operation request changed after durable intent')
            else:
                identifier, token, at = uid('op'), str(uuid.uuid4()), iso()
                db.execute('INSERT INTO operations VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                           (identifier,owner,name,token,'PENDING',canonical(request),digest(request),None,None,at,at))
                self._event(db,owner,'operation.intent',{'id':identifier,'name':name,'request_sha256':digest(request)})
        return self.operation(owner,name)

    def operation_state(self, op, state, provider_id=None, response=None):
        with self.transaction() as db:
            row = db.execute('SELECT state FROM operations WHERE id=?',(op['id'],)).fetchone()
            if not row:
                raise KeyError(op['id'])
            db.execute('UPDATE operations SET state=?,provider_id=COALESCE(?,provider_id),response=COALESCE(?,response),updated_at=? WHERE id=?',
                       (state,provider_id,canonical(response) if response is not None else None,iso(),op['id']))
            self._event(db,op['owner'],'operation.'+state.lower(),{'id':op['id'],'name':op['name'],'provider_id':provider_id})
        return self.operation(op['owner'],op['name'])

    def operations(self, owner=None):
        with self.connect() as db:
            rows=db.execute('SELECT owner,name FROM operations'+(' WHERE owner=?' if owner else ''),(owner,) if owner else ()).fetchall()
        return [self.operation(r[0],r[1]) for r in rows]

    def probe(self, owner, data):
        with self.transaction() as db:
            db.execute('INSERT OR IGNORE INTO probes(owner,scheduled_at,at,data) VALUES(?,?,?,?)',
                       (owner,data['scheduled_at'],data['at'],canonical(data)))

    def probes(self, owner):
        with self.connect() as db:
            return [json.loads(r[0]) for r in db.execute('SELECT data FROM probes WHERE owner=? ORDER BY scheduled_at',(owner,))]

    def events(self, owner=None):
        with self.connect() as db:
            rows = db.execute('SELECT * FROM events'+(' WHERE owner=?' if owner else '')+' ORDER BY sequence',(owner,) if owner else ()).fetchall()
        return [{**dict(r),'data':json.loads(r['data'])} for r in rows]

    def meta(self, key, value=None):
        with self.transaction() as db:
            if value is not None:
                db.execute('INSERT INTO metadata VALUES(?,?) ON CONFLICT(key) DO UPDATE SET data=excluded.data',(key,canonical(value)))
            row = db.execute('SELECT data FROM metadata WHERE key=?',(key,)).fetchone()
        return json.loads(row[0]) if row else None

    def backup(self, path):
        with self.lock, self.connect() as source, sqlite3.connect(path) as target:
            source.backup(target)
        os.chmod(path,0o600)

    def export(self, owner):
        """Dependency-inclusive export; record IDs refer to content, not latest revisions."""
        root=self.entity(owner)
        entity_map={e['id']:e for e in self.entities()}
        record_map={r['id']:r for r in self.records()}
        owners={owner}; selected=set(); processed=set()
        def strings(value):
            if isinstance(value,str):yield value
            elif isinstance(value,dict):
                for k,v in value.items():
                    yield k
                    yield from strings(v)
            elif isinstance(value,list):
                for item in value:yield from strings(item)
        while True:
            before=(len(owners),len(selected))
            for identifier in list(owners):
                entity=entity_map[identifier]
                for ref in strings(entity['data']):
                    if ref in record_map:selected.add(ref)
                for key in ('campaign_id','change_id','trial_id'):
                    linked=entity['data'].get(key)
                    if linked in entity_map:owners.add(linked)
                for other in entity_map.values():
                    if other['data'].get('campaign_id')==identifier or other['data'].get('trial_id')==identifier:owners.add(other['id'])
                selected.update(r['id'] for r in record_map.values() if r['owner']==identifier)
            for identifier in list(selected-processed):
                selected.update(v for v in strings(record_map[identifier]['data']) if v in record_map)
                processed.add(identifier)
            if before==(len(owners),len(selected)):break
        records=[record_map[r] for r in sorted(selected)]
        return {'schema_version':'1.0','kind':'agent_experiment_export','entity':root,
                'entities':[entity_map[o] for o in sorted(owners)],'records':records,
                'manifest':{r['id']:r['sha256'] for r in records},
                'events':[e for e in self.events() if e['owner'] in owners],
                'operations':[o for o in self.operations() if o['owner'] in owners],
                'probes':self.probes(owner),'producer':'local-console','authenticity':'unsigned',
                'limitations':['Scoped event exports may reference earlier global-chain events not included here. Use the full backup to inspect the complete journal.'],
                'exported_at':iso()}
