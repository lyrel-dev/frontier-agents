"""Serialize preview cancellation with first dispatch in the local journal.

Only the local PENDING -> DISPATCHING transition is atomic. After reservation,
remote outcome/stop reconciliation is necessary; AWS is not in this transaction.
"""
import json
from .util import Blocked, canonical, digest, dt, iso, uid, utcnow


def reserve_dispatch(store, operation, clock=utcnow):
    """Called by Broker immediately before its first remote preview request."""
    with store.transaction() as db:
        op = db.execute('SELECT * FROM operations WHERE id=?', (operation['id'],)).fetchone()
        if not op or op['state'] != 'PENDING' or op['request_sha256'] != digest(operation['request']):
            raise Blocked('Preview intent is no longer pending or its request changed')
        owner = db.execute('SELECT * FROM entities WHERE id=?', (op['owner'],)).fetchone()
        if not owner or owner['kind'] != 'fis_preview':
            raise Blocked('Preview operation has no valid owner')
        data = json.loads(owner['data'])
        if owner['state'] != 'QUEUED' or data.get('abort_requested'):
            raise Blocked('Preview cancelled or no longer queued; no start dispatched')
        if dt(data['expires_at']) <= clock():
            raise Blocked('Preview approval expired before dispatch')
        if digest(data['subject']) != data['digest']:
            raise Blocked('Preview approval subject is inconsistent')
        request = json.loads(op['request'])
        if (request.get('side'), request.get('service'), request.get('operation')) != ('fault','fis','start_experiment'):
            raise Blocked('Only the approved FIS preview can reserve this operation')
        if request.get('parameters', {}).get('experimentOptions', {}).get('actionsMode') != 'skip-all':
            raise Blocked('Preview reservation cannot authorize fault injection')
        db.execute('UPDATE operations SET state=?,updated_at=? WHERE id=?', ('DISPATCHING',iso(clock()),op['id']))
        store._event(db,op['owner'],'operation.dispatching',{'id':op['id'],'name':op['name'],
            'reservation':'preview approval and cancellation checked atomically'})
    return store.operation(operation['owner'],operation['name'])


def cancel(store, identifier):
    """A pre-reservation cancel forbids dispatch; a later cancel requests stop."""
    with store.transaction() as db:
        owner = db.execute('SELECT * FROM entities WHERE id=?', (identifier,)).fetchone()
        if not owner or owner['kind'] != 'fis_preview':
            raise Blocked('Not a preview job')
        if owner['state'] in {'COMPLETE','BLOCKED'}:
            return store.entity(identifier)
        op = db.execute("SELECT * FROM operations WHERE owner=? AND name='target-preview'", (identifier,)).fetchone()
        data = json.loads(owner['data']); data['abort_requested'] = True
        if not op or op['state'] in {'PENDING','FAILED'}:
            state='BLOCKED';data['reason']='Cancelled before preview dispatch'
            if op and op['state']=='PENDING':
                db.execute('UPDATE operations SET state=?,response=?,updated_at=? WHERE id=?',
                           ('FAILED',canonical({'code':'CancelledBeforeDispatch'}),iso(),op['id']))
                store._event(db,identifier,'operation.failed',{'id':op['id'],'name':op['name'],'code':'CancelledBeforeDispatch'})
        else:
            state=owner['state'];data['reason']='Stop requested; reconcile the reserved remote operation first'
        db.execute('UPDATE entities SET state=?,revision=revision+1,updated_at=?,data=? WHERE id=?',
                   (state,iso(),canonical(data),identifier))
        store._event(db,identifier,'preview.cancel_requested',{'from':owner['state'],'to':state,
                     'dispatch_reserved':bool(op and op['state'] in {'DISPATCHING','UNKNOWN','CONFIRMED'})})
    return store.entity(identifier)


def complete(store, identifier, result, clock=utcnow):
    """Publish the admissible preview and terminal entity atomically with cancel."""
    record_id = uid('fis_preview_result')
    at, sha = iso(clock()), digest(result)
    with store.transaction() as db:
        owner = db.execute('SELECT * FROM entities WHERE id=?', (identifier,)).fetchone()
        if not owner or owner['kind'] != 'fis_preview' or owner['state'] != 'RUNNING':
            raise Blocked('Preview no longer eligible for successful completion')
        data = json.loads(owner['data'])
        if data.get('abort_requested') or not data.get('remote_terminal') or data.get('remote_state') != 'completed':
            raise Blocked('Cancelled or unconfirmed preview cannot supply an approval target envelope')
        op = db.execute("SELECT * FROM operations WHERE owner=? AND name='target-preview'", (identifier,)).fetchone()
        if (not op or op['state'] != 'CONFIRMED' or op['provider_id'] != result.get('provider_id')
                or any(result.get(key) != value for key, value in data['subject'].items())):
            raise Blocked('Preview result does not match its approved operation')
        db.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',
                   (record_id,'fis_preview_result',identifier,at,sha,canonical(result)))
        store._event(db,identifier,'record.saved',{'id':record_id,'kind':'fis_preview_result','sha256':sha})
        data.update(result_id=record_id,finished_at=at)
        db.execute('UPDATE entities SET state=?,revision=revision+1,updated_at=?,data=? WHERE id=?',
                   ('COMPLETE',at,canonical(data),identifier))
        store._event(db,identifier,'preview.completed',{'result_id':record_id})
    return store.record(record_id)
