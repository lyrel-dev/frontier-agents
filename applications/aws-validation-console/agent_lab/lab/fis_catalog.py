"""Resumable, read-only FIS discovery across explicitly configured account/Regions.

One scope step performs one FIS operation. Tokens and pending identifiers are
journaled; a process restart rechecks STS. A bound or error is PARTIAL, not empty.
The catalogue does not authorize execution and never writes an AWS resource.
"""
from __future__ import annotations
import boto3
from botocore.config import Config
from .aws import template_contract
from .models import FISAccount
from .util import Blocked, canonical, digest, error_code, iso, normal, uid

TERMINAL = {'COMPLETE', 'PARTIAL', 'DENIED', 'ERROR', 'CANCELLED'}


def accounts(config):
    if config.fis_accounts:
        return config.fis_accounts
    # Existing bindings remain usable without entering credentials twice.
    found = {}
    for binding in config.bindings:
        for side in ('workload', 'agent'):
            a = getattr(binding, side)
            key = (a.account_id, a.region)
            found.setdefault(key, FISAccount(id='account-' + digest(key)[:16],
                name=a.account_id + ' / ' + a.region, account_id=a.account_id,
                profile=a.profile, regions=[a.region]))
    return list(found.values())


class Catalog:
    def __init__(self, config, store, *, session_factory=None):
        self.config, self.store = config, store
        self.factory = session_factory or (lambda profile: boto3.Session(profile_name=profile))
        self.clients = {}
        self.sdk = Config(connect_timeout=3, read_timeout=8,
                          retries={'total_max_attempts': 2, 'mode': 'standard'},
                          ignore_configured_endpoint_urls=True)

    def request(self, selected=None):
        configured = {a.id: a for a in accounts(self.config)}
        ids = list(configured) if selected is None else selected
        if not ids or len(ids) != len(set(ids)) or not set(ids) <= set(configured):
            raise Blocked('Select distinct configured accounts; no credentials or endpoints are accepted here')
        if any(e['state'] not in TERMINAL for e in self.store.entities('fis_sync')):
            raise Blocked('A discovery job already exists; finish or cancel it first')
        scopes = [{'connection_id': a.id, 'account_id': a.account_id, 'region': region,
                   'configuration_sha256': digest(a.model_dump(mode='json'))}
                  for identifier in ids for a in [configured[identifier]] for region in a.regions]
        return self.store.create('fis_sync', 'QUEUED', {
            'requested_at': iso(), 'scopes': scopes, 'scope_ids': [],
            'max_pages': self.config.fis_discovery_max_pages, 'read_only': True})

    def cancel(self, identifier):
        e = self.store.entity(identifier)
        if e['kind'] != 'fis_sync':
            raise Blocked('Not a catalogue job')
        if e['state'] in TERMINAL:
            return e
        return self.store.update(identifier, changes={'cancel_requested': True}, event='fis.discovery.cancel_requested')

    def _reader(self, scope):
        d = scope['data']
        account = next((a for a in accounts(self.config) if a.id == d['connection_id']), None)
        if not account or digest(account.model_dump(mode='json')) != d['configuration_sha256']:
            raise Blocked('Discovery account configuration changed; start a new sync')
        if scope['id'] not in self.clients:
            session = self.factory(account.profile)
            sts = session.client('sts', region_name=d['region'], config=self.sdk)
            raw = sts.get_caller_identity()
            body = normal(raw)
            self._capture(scope, 'sts', 'get_caller_identity', {}, body, raw.get('ResponseMetadata', {}).get('RequestId'))
            arn = body.get('Arn', '')
            if (body.get('Account') != d['account_id'] or arn.endswith(':root')
                    or not arn.startswith((f"arn:aws:iam::{d['account_id']}:", f"arn:aws:sts::{d['account_id']}:"))):
                raise Blocked('Unexpected AWS account or prohibited root identity')
            self.clients[scope['id']] = session.client('fis', region_name=d['region'], config=self.sdk)
        return self.clients[scope['id']]

    def _capture(self, scope, service, operation, params, body, request_id=None):
        if len(canonical(body).encode()) > 8_000_000:
            raise Blocked('Discovery response exceeded the capture limit')
        return self.store.put_record('fis_source', scope['id'], {
            'account_id': scope['data']['account_id'], 'region': scope['data']['region'],
            'service': service, 'operation': operation, 'parameters': {k:v for k,v in params.items() if k != 'nextToken'},
            'received_at': iso(), 'request_id': request_id,
            'response': body, 'response_sha256': digest(body)})

    def _read(self, scope, operation, **params):
        if operation not in {'list_experiment_templates', 'get_experiment_template',
                             'list_target_account_configurations', 'list_experiments'}:
            raise Blocked('Catalogue API is read-only')
        raw = getattr(self._reader(scope), operation)(**params)
        body = normal(raw)
        record = self._capture(scope, 'fis', operation, params, body, raw.get('ResponseMetadata', {}).get('RequestId'))
        return body, record['id']

    def step(self):
        jobs = [e for e in reversed(self.store.entities('fis_sync')) if e['state'] not in TERMINAL]
        if not jobs:
            return
        job = jobs[0]
        d = job['data']
        if d.get('cancel_requested'):
            for sid in d['scope_ids']:
                if self.store.entity(sid)['state'] not in TERMINAL:
                    self.store.update(sid, state='CANCELLED')
            self.store.update(job['id'], state='CANCELLED', changes={'finished_at': iso()})
            return
        # Deterministic children recover a crash between child creation and projection update.
        for i, descriptor in enumerate(d['scopes']):
            sid = job['id'] + '-scope-' + str(i)
            try:
                scope = self.store.entity(sid)
            except KeyError:
                scope = self.store.create('fis_scope', 'SCANNING', {**descriptor,
                    'sync_id': job['id'], 'stage': 'templates', 'pending': [], 'template_token': None,
                    'history_token': None, 'seen_tokens': [], 'pages': 0, 'errors': [], 'max_pages': d['max_pages']}, sid)
            if sid not in d['scope_ids']:
                d['scope_ids'].append(sid)
                self.store.update(job['id'], state='RUNNING', changes={'scope_ids': d['scope_ids']})
            if scope['state'] not in TERMINAL:
                try:
                    self._scope_step(scope)
                except Exception as exc:
                    code = error_code(exc)
                    self.store.put_record('fis_discovery_error', sid, {'at':iso(), 'stage':scope['data']['stage'], 'code':code})
                    self.store.update(sid, state='DENIED' if 'denied' in code.lower() else 'ERROR',
                                      changes={'error_code': code, 'finished_at': iso()})
                return
        states = [self.store.entity(sid)['state'] for sid in d['scope_ids']]
        self.store.update(job['id'], state='COMPLETE' if all(s == 'COMPLETE' for s in states) else 'PARTIAL',
                          changes={'finished_at': iso()})

    def _page(self, scope, operation, key, token, **params):
        d = scope['data']
        if d['pages'] >= d['max_pages']:
            self.store.update(scope['id'], state='PARTIAL', changes={'error_code':'PageBudgetReached', 'finished_at':iso()})
            return None
        if token:
            params['nextToken'] = token
        body, source = self._read(scope, operation, maxResults=100, **params)
        values = body.get(key)
        if not isinstance(values, list):
            raise Blocked('Unexpected FIS list response')
        next_token = body.get('nextToken')
        token_key = digest([operation, params.get('experimentTemplateId'), next_token]) if next_token else None
        if token_key and token_key in d['seen_tokens']:
            raise Blocked('Repeated FIS pagination token')
        d['pages'] += 1
        if token_key:
            d['seen_tokens'].append(token_key)
        return values, next_token, source

    def _save_template(self, scope, summary, template, sources, target_accounts=None, error=None):
        d = scope['data']
        data = {'sync_id': d['sync_id'], 'scope_id': scope['id'], 'connection_id':d['connection_id'],
                'account_id':d['account_id'], 'region':d['region'], 'template_id':summary['id'],
                'summary':summary, 'template':template, 'target_accounts':target_accounts or [],
                'complete': error is None, 'error_code':error, 'observed_at':iso(),
                'contract_sha256':digest(template_contract(template)) if template else None,
                'input_hashes':{rid:self.store.record(rid)['sha256'] for rid in sources}}
        rid = 'fis-template-' + digest([scope['id'], summary['id']])[:40]
        # If the prior step committed a row but not the cursor, retain that row.
        try:
            self.store.record(rid)
        except KeyError:
            self.store.put_record('fis_template', scope['id'], data, rid)

    def _scope_step(self, scope):
        d = scope['data']; stage = d['stage']
        if stage == 'templates':
            page = self._page(scope, 'list_experiment_templates', 'experimentTemplates', d['template_token'])
            if page is None: return
            values, token, source = page
            d.update(pending=values, template_token=token, summary_source=source,
                     stage='details' if values else ('templates' if token else 'history'))
        elif stage == 'details':
            summary = d['pending'][0]
            sources = [d['summary_source']]
            try:
                body, source = self._read(scope, 'get_experiment_template', id=summary['id']); sources.append(source)
                template = body['experimentTemplate']
                if template.get('id') != summary['id']:
                    raise Blocked('Template identifier mismatch')
                if template.get('experimentOptions', {}).get('accountTargeting') == 'multi-account':
                    d.update(current_summary=summary, current_template=template, current_sources=sources,
                             target_accounts=[], account_token=None, stage='target_accounts')
                else:
                    self._save_template(scope, summary, template, sources)
                    d['pending'] = d['pending'][1:]
            except Exception as exc:
                code = error_code(exc)
                self._save_template(scope, summary, None, sources, error=code)
                d['errors'].append({'template_id':summary['id'], 'code':code})
                d['pending'] = d['pending'][1:]
            if d['stage'] == 'details' and not d['pending']:
                d['stage'] = 'templates' if d['template_token'] else 'history'
        elif stage == 'target_accounts':
            try:
                page = self._page(scope, 'list_target_account_configurations', 'targetAccountConfigurations',
                                  d['account_token'], experimentTemplateId=d['current_template']['id'])
                if page is None: return
                values, token, source = page
                d['target_accounts'] += values; d['current_sources'].append(source); d['account_token'] = token
                if not token:
                    self._save_template(scope, d['current_summary'], d['current_template'], d['current_sources'], d['target_accounts'])
                    d['pending'] = d['pending'][1:]
                    d['stage'] = 'details' if d['pending'] else ('templates' if d['template_token'] else 'history')
            except Exception as exc:
                code = error_code(exc)
                self._save_template(scope, d['current_summary'], d['current_template'], d['current_sources'], d['target_accounts'], code)
                d['errors'].append({'template_id':d['current_template']['id'], 'code':code})
                d['pending'] = d['pending'][1:]
                d['stage'] = 'details' if d['pending'] else ('templates' if d['template_token'] else 'history')
        else:
            page = self._page(scope, 'list_experiments', 'experiments', d['history_token'])
            if page is None: return
            values, token, source = page
            rid = 'fis-history-' + digest([scope['id'], d['history_token']])[:40]
            try: self.store.record(rid)
            except KeyError:
                self.store.put_record('fis_history', scope['id'], {'scope_id':scope['id'], 'account_id':d['account_id'],
                    'region':d['region'], 'experiments':values, 'source_id':source}, rid)
            d['history_token'] = token
            if not token:
                self.store.update(scope['id'], state='PARTIAL' if d['errors'] else 'COMPLETE',
                                  changes={**d, 'finished_at':iso()})
                return
        self.store.update(scope['id'], changes=d)

    def view(self):
        jobs = self.store.entities('fis_sync')
        job = jobs[0] if jobs else None
        scopes = [self.store.entity(sid) for sid in job['data']['scope_ids']] if job else []
        templates = [r for scope in scopes for r in self.store.records(scope['id'], 'fis_template')]
        history = [{**e, 'account_id':scope['data']['account_id'], 'region':scope['data']['region']}
                   for scope in scopes for r in self.store.records(scope['id'], 'fis_history') for e in r['data']['experiments']]
        return {'job':job, 'scopes':scopes, 'templates':templates, 'history':history,
                'coverage':'not_collected' if not job else job['state'],
                'scope_note':'Only explicitly configured accounts and Regions; denied or partial scopes are not empty.'}
