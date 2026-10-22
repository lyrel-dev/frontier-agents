"""Audit frozen local evidence for the live gate; never manufactures an assessment."""
from __future__ import annotations
from .util import Blocked, digest, iso


def audit(store, trial_id, campaign_id=None):
    checks = []
    pinned = {}

    def require(name, ok, detail):
        checks.append({'check': name, 'status': 'pass' if ok else 'blocked', 'detail': detail})

    def verify(reference, expected=None):
        record = store.record(reference)
        if expected and record['sha256'] != expected:
            raise Blocked('Pinned input mismatch: ' + reference)
        if reference in pinned:
            return record
        if len(pinned) >= 10000:
            raise Blocked('Acceptance dependency limit exceeded')
        pinned[reference] = record['sha256']
        for child, sha in record['data'].get('input_hashes', {}).items():
            verify(child, sha)
        return record

    trial = store.entity(trial_id)
    if trial['kind'] != 'trial':
        raise Blocked('Select a response trial, not a scenario or imported report')
    d = trial['data']
    spec = verify(d['experiment_ref'])['data']
    binding = verify(d['binding_record_id'])['data']
    require('closed_native_response', trial['state'] == 'CLOSED' and spec['mode'] == 'native'
            and d.get('arm') != 'benign', 'A closed native response trial is required.')
    require('measured_fault', bool(d.get('fis_id') and d.get('fault_confirmed') and d.get('resolved_target_arns')),
            'An owned provider experiment, actual targets and independent effect confirmation must exist.')
    require('cleanup', d.get('cleanup_verified') is True, 'Restoration must be verified independently.')
    assessment = verify(d['assessment_id']) if d.get('assessment_id') else None
    dimensions = assessment['data'].get('dimensions', {}) if assessment else {}
    require('assessment_identity', bool(assessment and assessment['kind'] == 'assessment'
            and assessment['owner'] == trial_id and assessment['data'].get('trial_id') == trial_id),
            'The selected frozen assessment must belong to this trial.')
    for name in ('challenge', 'measurement', 'delivery', 'cleanup'):
        require(name, dimensions.get(name, {}).get('outcome') == 'pass',
                'Required captured evidence must be qualified: ' + name)
    for name in ('response', 'diagnosis'):
        require(name, dimensions.get(name, {}).get('outcome') in ('pass', 'fail'),
                'An assessed failure is reviewable; missing or not-assessed evidence is not.')
    # Require retained AWS read provenance, not only manually entered IDs.
    sources = [store.record(rid) for rid in list(pinned)
               if store.record(rid)['kind'] == 'aws' and store.record(rid)['owner'] == trial_id]
    expected_accounts = {'agent': binding['agent']['account_id'], 'requester': binding['agent']['account_id'],
                         'workload': binding['workload']['account_id'], 'fault': binding['workload']['account_id'],
                         'change': binding['workload']['account_id']}
    require('source_account_scope', bool(sources) and all(
        r['data'].get('side') in expected_accounts
        and r['data'].get('account_id') == expected_accounts[r['data']['side']]
        and r['data'].get('region') == binding['agent' if r['data']['side'] in ('agent', 'requester') else 'workload']['region']
        and r['data'].get('request_id')
        and r['data'].get('response_sha256') == digest(r['data'].get('response')) for r in sources),
        'Captured AWS reads must retain account scope, request IDs and matching response hashes.')
    operations = {(r['data'].get('service'), r['data'].get('operation')) for r in sources}
    require('source_operations', {('fis', 'get_experiment'), ('fis', 'list_experiment_resolved_targets'),
                                 ('devops-agent', 'get_backlog_task'), ('devops-agent', 'list_journal_records')} <= operations,
            'Retain fault, resolved-target, task and journal source responses.')
    scoped_owners = {trial_id}
    campaign = None
    comparison = None
    if campaign_id:
        campaign = store.entity(campaign_id)
        if campaign['kind'] != 'campaign':
            raise Blocked('Select a prevention campaign')
        c = campaign['data']
        require('baseline_link', d.get('campaign_id') == campaign_id and d.get('arm') == 'baseline',
                'The selected response trial must be an untreated baseline in this campaign.')
        comparison = verify(c['comparison_id']) if c.get('comparison_id') else None
        require('comparison_identity', bool(comparison and comparison['kind'] == 'comparison'
                and comparison['owner'] == campaign_id and comparison['data'].get('campaign_id') == campaign_id),
                'A frozen comparison must belong to the selected campaign.')
        require('paired_prevention_assessed', bool(comparison and comparison['data'].get('pairs')
                and comparison['data'].get('outcome') in ('pass', 'fail') and not comparison['data'].get('blockers')),
                'A matched assessed replay is required; it may show that prevention failed.')
        if c.get('recommendation_record_id'):
            recommendation = verify(c['recommendation_record_id'])
            require('recommendation_pin', recommendation['kind'] == 'recommendation', 'Use the pinned agent recommendation.')
        else:
            require('recommendation_pin', False, 'No recommendation is pinned.')
        change = store.entity(c['change_id']) if c.get('change_id') else None
        require('verified_change', bool(change and change['kind'] == 'change' and change['state'] == 'VERIFIED'),
                'The agent-linked implementation must have an actual verified deployment.')
        scoped_owners.add(campaign_id)
        if change:
            scoped_owners.add(change['id'])
        if comparison:
            for pair in comparison['data'].get('pairs', []):
                scoped_owners.update([pair['baseline_trial'], pair['replay_trial']])
    # Include changes owned by selected trials, and surface every unresolved operation.
    for change in store.entities('change'):
        if change['data'].get('trial_id') in scoped_owners or change['data'].get('campaign_id') in scoped_owners:
            scoped_owners.add(change['id'])
    unresolved = [op['id'] for op in store.operations() if op['owner'] in scoped_owners
                  and op['state'] in ('PENDING', 'DISPATCHING', 'UNKNOWN')]
    require('no_uncertain_operations', not unresolved, 'Unresolved provider intents: ' + ', '.join(unresolved))
    require('restoration_clear', not any(e['state'] == 'RESTORE_REQUIRED' for e in store.entities()),
            'An outstanding restoration prevents acceptance promotion.')
    blocked = [r['check'] for r in checks if r['status'] != 'pass']
    return {'schema': 'agent-lab.acceptance-audit/v1', 'at': iso(), 'trial_id': trial_id,
            'campaign_id': campaign_id, 'status': 'blocked' if blocked else 'reviewable',
            'blocking_checks': blocked, 'checks': checks, 'input_hashes': pinned,
            'entity_snapshots': [store.entity(owner) for owner in sorted(scoped_owners)],
            'response_outcomes': {k: v.get('outcome') for k, v in dimensions.items()},
            'prevention_outcome': comparison['data']['outcome'] if comparison else 'not_assessed',
            'live_acceptance_certified': False,
            'limits': ['Local completeness and hash audit, not independent verification of the AWS producer.',
                       'Reviewable does not mean the agent passed; failed response/prevention outcomes are retained.',
                       'An authorized live run and independent review remain necessary. No cloud calls were made by this audit.']}
