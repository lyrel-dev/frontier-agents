"""Fail-closed FIS start guard. This module can read, never change, the lever."""
from __future__ import annotations

from .util import Blocked, digest, error_code, iso, normal


def read_safety_lever(aws):
    """Capture the default lever from the verified workload fault identity."""
    aws.identity('fault')
    at = iso()
    try:
        response = aws.client('fault', 'fis').get_safety_lever(id='default')
        body = normal(response)
        record = aws.store.put_record('aws', aws.owner, {
            'side': 'fault', 'account_id': (getattr(aws.b,'orchestrator',None) or aws.b.workload).account_id,
            'region': (getattr(aws.b,'orchestrator',None) or aws.b.workload).region, 'service': 'fis',
            'operation': 'get_safety_lever', 'parameters': {'id': 'default'},
            'requested_at': at, 'received_at': iso(),
            'request_id': response.get('ResponseMetadata', {}).get('RequestId'),
            'response': body, 'response_sha256': digest(body)})
        lever = body.get('safetyLever', {})
        if lever.get('id') != 'default':
            raise Blocked('Unexpected FIS safety lever identity')
        status = lever.get('state', {}).get('status')
        if status not in {'disengaged', 'engaging', 'engaged'}:
            raise Blocked('Unknown FIS safety lever state')
        return {'status': status, 'source': record['id']}
    except Exception as exc:
        aws.store.put_record('collection_error', aws.owner, {
            'side': 'fault', 'service': 'fis', 'operation': 'get_safety_lever',
            'at': at, 'code': error_code(exc)})
        raise
