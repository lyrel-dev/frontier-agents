"""Read-only onboarding checks. Never starts a trial, task, fault or runbook."""
from __future__ import annotations
from datetime import timedelta
from pathlib import Path
import hashlib
from .aws import AWS
from .models import Configuration, Experiment
from .probe import request as probe_request
from .util import Blocked, digest, error_code, iso, normal, uid, utcnow


class ReadOnlyAWS(AWS):
    def client(self, side, service, write=False):
        if write:
            raise Blocked('Preflight cannot create a write client')
        return super().client(side, service)

    def write(self, *args, **kwargs):
        raise Blocked('Preflight has no AWS write capability')

    def safety_lever(self):
        self.identity('fault')
        at = iso()
        try:
            response = self.client('fault', 'fis').get_safety_lever(id='default')
            body = normal(response)
            record = self.store.put_record('aws', self.owner, {
                'side': 'fault', 'account_id': self.b.workload.account_id,
                'region': self.b.workload.region, 'service': 'fis',
                'operation': 'get_safety_lever', 'parameters': {'id': 'default'},
                'requested_at': at, 'received_at': iso(),
                'request_id': response.get('ResponseMetadata', {}).get('RequestId'),
                'response': body, 'response_sha256': digest(body)})
            lever = body.get('safetyLever', {})
            if lever.get('id') != 'default':
                raise Blocked('Unexpected FIS safety lever identity')
            return {'status': lever.get('state', {}).get('status'), 'source': record['id']}
        except Exception as exc:
            self.store.put_record('collection_error', self.owner, {
                'side': 'fault', 'service': 'fis', 'operation': 'get_safety_lever',
                'at': at, 'code': error_code(exc)})
            raise


def source_fingerprint():
    root = Path(__file__).resolve().parents[1]
    files = [*sorted((root / 'lab').glob('*.py')), root / 'requirements.txt']
    return digest({p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in files})


def run_preflight(config: Configuration, spec: Experiment | None, store, *,
                  read_aws=False, probe=False, clock=utcnow, aws_factory=ReadOnlyAWS,
                  request=probe_request):
    """Persist checks and source hashes; a read result never grants execution authority.

    aws_factory/request are injection seams for tests, not API or config fields.
    The shipping CLI always uses the real read-only SDK adapter.
    """
    if probe and not read_aws:
        raise Blocked('A business-path request requires explicit --read-aws and --probe')
    owner = uid('preflight')
    at = clock()
    rows = []

    def check(name, ok, detail, *, required=True):
        rows.append({'check': name, 'status': 'pass' if ok else 'blocked',
                     'required': required, 'detail': detail})

    binding = next((b for b in config.bindings if spec and b.id == spec.binding_id), None)
    check('binding', binding is not None,
          'Selected experiment is bound to a configured environment.' if binding else
          'Provide the real two-account configuration and an experiment definition.')
    fault = next((f for f in binding.faults if spec and f.id == spec.fault_id), None) if binding else None
    workload = next((p for p in binding.probes if spec and p.id == spec.probe_id), None) if binding else None
    if binding:
        valid = (fault is not None and workload is not None
                 and spec.observation_seconds >= fault.max_fault_seconds + spec.stable_seconds
                 and set(spec.oracle.affected_resource_arns) <= set(fault.target_arns)
                 and set(spec.oracle.required_checks) <= {c.id for c in binding.checks}
                 and set(spec.intervention_runbook_ids) <= {b.id for b in binding.runbooks})
        check('experiment_contract', valid, 'Fault, probe, oracle, observation budget and runbooks must resolve exactly.')
        check('native_mode', spec.mode == 'native', 'Live native-response acceptance cannot use assisted task creation.')
        check('receipt_adapter', bool(binding.route.receipt_log_group),
              'A native delivery receipt source is required to separate delivery failure from agent silence.')
        check('lifecycle_source', bool(binding.route.lifecycle_log_group),
              'An optional lifecycle source enables active-investigation timestamps.', required=False)
    locally_valid = all(r['status'] == 'pass' for r in rows if r['required'])
    aws_attempted = False
    observation = None
    if read_aws and locally_valid:
        aws_attempted = True
        aws = aws_factory(binding, store, owner)
        try:
            qualification = aws.qualify(spec)
            store.put_record('preflight_qualification', owner, qualification)
            check('account_and_instrument_reads', True,
                  'Account identities, association, instrument pins, baseline verifiers and alarms were read.')
        except Exception as exc:
            check('account_and_instrument_reads', False, 'Read qualification failed: ' + error_code(exc))
        if rows[-1]['status'] == 'pass':
            try:
                lever = aws.safety_lever()
                check('fis_safety_lever', lever['status'] == 'disengaged',
                      'Observed state: ' + str(lever['status']) + '. The console does not change it.')
            except Exception as exc:
                check('fis_safety_lever', False, 'Safety state is unverified: ' + error_code(exc))
            # Read even when the safety lever is engaged; these are observations, not execution.
            try:
                lookback = max([300, *[m.period_seconds * 3 for m in binding.metrics]])
                observation = aws.observe(iso(at - timedelta(seconds=lookback)), iso(at))
                store.put_record('preflight_observation', owner, observation)
                check('incident_source_reads', observation.get('complete') is True,
                      'Bounded source queries completed. Empty logs do not prove incident delivery.')
                returned = {m['id']: m for m in observation.get('metrics', [])}
                for metric in binding.metrics:
                    m = returned.get(metric.id, {})
                    points = m.get('points', [])
                    ok = (m.get('complete') is True and bool(points) and m.get('missing') == 0
                          and all(p.get('value') is not None for p in points))
                    check('metric:' + metric.id, ok,
                          'Configured closed-window samples must be present and complete; no zero fill.')
            except Exception as exc:
                check('incident_source_reads', False, 'Source read failed: ' + error_code(exc))
            if probe:
                try:
                    sample = request(workload, iso(clock()))
                    store.put_record('preflight_probe', owner, sample)
                    check('business_path', sample.get('attempted') is True and sample.get('success') is True,
                          'Exactly one approved GET was attempted. This is not a workload baseline.')
                except Exception as exc:
                    check('business_path', False, 'Business-path request failed: ' + error_code(exc))
    if not read_aws:
        rows.append({'check': 'aws_reads', 'status': 'not_run', 'required': True,
                     'detail': 'Offline plan only. Use --read-aws locally to query the configured profiles.'})
    if not probe:
        rows.append({'check': 'business_path', 'status': 'not_run', 'required': False,
                     'detail': 'No HTTP probe sent. Add --probe for one explicit request.'})
    blocking = [r['check'] for r in rows if r['required'] and r['status'] != 'pass']
    sources = store.records(owner)
    body = {'schema': 'agent-lab.preflight/v1', 'id': owner, 'checked_at': iso(at),
            'expires_at': iso(at + timedelta(minutes=15)),
            'status': 'blocked' if blocking else 'read_checks_passed',
            'blocking_checks': blocking, 'checks': rows, 'aws_reads_attempted': aws_attempted,
            'aws_write_operations': 0, 'trial_created': False, 'execution_authorized': False,
            'configuration_sha256': digest(config.model_dump(mode='json')),
            'experiment_sha256': digest(spec.model_dump(mode='json')) if spec else None,
            'source_sha256': source_fingerprint(),
            'input_hashes': {r['id']: r['sha256'] for r in sources},
            'limits': ['Read access is not permission to mutate resources.',
                       'No native incident or agent response was exercised by this check.',
                       'IAM efficacy, independent emergency recovery, credential refresh and prevention replay remain live gates.',
                       'This report is not an approval token; trial qualification still runs separately.']}
    return store.put_record('preflight', owner, body)
