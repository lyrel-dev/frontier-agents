"""Publish a terminal trial and its assessment in one local transaction.

Captured inputs can be committed earlier. A crash while computing the result
leaves FINALIZING recoverable; readers never see a new closed trial without its
assessment. This does not combine AWS writes with the local SQLite transaction.
"""
from __future__ import annotations
import json
from .util import Blocked, canonical, digest, iso, uid


def finalize_trial(store, trial_id, assessment, *, expected_revision, state, closed_at):
    if state not in {'CLOSED', 'CLOSED_ABORTED'}:
        raise Blocked('Unsupported terminal trial state')
    if assessment.get('trial_id') != trial_id or assessment.get('lifecycle') != state:
        raise Blocked('Final assessment identity or lifecycle mismatch')
    identifier = uid('assessment')
    at, sha = iso(), digest(assessment)
    with store.transaction() as db:
        row = db.execute('SELECT * FROM entities WHERE id=?', (trial_id,)).fetchone()
        if not row or row['kind'] != 'trial' or row['state'] != 'FINALIZING':
            raise Blocked('Trial is not awaiting finalization')
        if row['revision'] != expected_revision:
            raise Blocked('Trial changed while its assessment was computed; retry finalization')
        data = json.loads(row['data'])
        expected_state = 'CLOSED_ABORTED' if data.get('aborted') else 'CLOSED'
        if state != expected_state or data.get('cleanup_verified') is not True:
            raise Blocked('Final state or restoration verification mismatch')
        capture_id = assessment.get('probe_capture_id')
        capture = db.execute('SELECT kind,owner,sha256 FROM records WHERE id=?', (capture_id,)).fetchone()
        if (not capture or capture['kind'] != 'probe_capture' or capture['owner'] != trial_id
                or assessment.get('input_hashes', {}).get(capture_id) != capture['sha256']):
            raise Blocked('Final assessment must pin this trial\'s probe capture')
        db.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',
                   (identifier, 'assessment', trial_id, at, sha, canonical(assessment)))
        store._event(db, trial_id, 'record.saved', {'id':identifier,'kind':'assessment','sha256':sha})
        changes = {'closed_at':closed_at,'assessment_id':identifier}
        data.update(changes)
        db.execute('UPDATE entities SET state=?,revision=revision+1,updated_at=?,data=? WHERE id=?',
                   (state, at, canonical(data), trial_id))
        store._event(db, trial_id, 'trial.closed', {'from':'FINALIZING','to':state,'changes':changes})
        store._event(db, trial_id, 'trial.assessed', {'assessment_id':identifier})
    return store.record(identifier)
