"""FIS-first multi-account campaign queue over the qualified response executor.

A catalogue row is not execution authority. Every child receives fresh AWS
qualification and its own exact, expiring approval. The one worker serializes
exposure; a pause never masquerades as stopping a running FIS experiment.
"""
from __future__ import annotations
from pydantic import Field
from .aws import DURATION_ACTIONS
from .fis_catalog import Catalog
from .models import Strict, ID, Experiment, TrialRequest
from .service import Service
from .util import Blocked, digest, iso, canonical
import json

CLOSED = {'CLOSED', 'CLOSED_ABORTED', 'CLOSED_BLOCKED', 'BLOCKED'}
ACTIVE = {'QUALIFYING','BASELINING','EXPOSING','OBSERVING','ABORTING','CLEANING',
          'SETTLING','FINALIZING','UNKNOWN_REMOTE_STATE','RESTORE_REQUIRED'}


class CatalogRequest(Strict):
    account_ids: list[ID] | None = Field(default=None, min_length=1, max_length=100)


class AttachContract(Strict):
    template_record_id: str = Field(min_length=1, max_length=150)
    experiment: Experiment


class QueueEntry(Strict):
    template_record_id: str = Field(min_length=1, max_length=150)
    experiment_ref: str = Field(min_length=1, max_length=150)


class QueueRequest(Strict):
    title: str = Field(min_length=1, max_length=200)
    entries: list[QueueEntry] = Field(min_length=1, max_length=50)
    repetitions: int = Field(default=1, ge=1, le=20)
    stop_on_failure: bool = True
    comparability_tolerance: float = Field(default=.1, ge=0, le=.2)
    knowledge_history_note: str = Field(min_length=20, max_length=4000)


def execution_gaps(template):
    reasons = []
    options = template.get('experimentOptions') or {}
    if options.get('accountTargeting', 'single-account') != 'single-account':
        reasons.append('Multi-account FIS template: discovery supported; multi-target-account effect/cleanup verifiers are not qualified.')
    if options.get('emptyTargetResolutionMode', 'fail') != 'fail':
        reasons.append('Empty-target skipping is not qualified for response benchmarking.')
    if not template.get('targets'):
        reasons.append('No explicit target set.')
    for name, target in template.get('targets', {}).items():
        if (not target.get('resourceArns') or target.get('selectionMode') != 'ALL'
                or target.get('resourceTags') or target.get('filters') or target.get('parameters')):
            reasons.append('Target ' + name + ' requires a separately qualified selector resolver.')
    for action in template.get('actions', {}).values():
        if action.get('actionId') not in DURATION_ACTIONS:
            reasons.append('Action lacks a reviewed finite-duration adapter: ' + str(action.get('actionId')))
    if not template.get('actions'):
        reasons.append('Template has no actions.')
    stops = template.get('stopConditions') or []
    if not stops or any(s.get('source') != 'aws:cloudwatch:alarm' for s in stops):
        reasons.append('CloudWatch stop alarms are required.')
    return reasons


class Fleet:
    def __init__(self, config, store, *, service=None, catalog=None):
        self.config, self.store = config, store
        self.service = service or Service(config, store)
        self.catalog = catalog or Catalog(config, store)

    def mapping(self, record_id, spec):
        row = self.store.record(record_id)
        if row['kind'] != 'fis_template':
            raise Blocked('Choose a discovered FIS template, not a historical experiment execution')
        d = row['data']; scope = self.store.entity(d['scope_id'])
        if not d['complete'] or scope['state'] != 'COMPLETE':
            raise Blocked('The account/Region catalogue is incomplete; resync before enrollment')
        reasons = execution_gaps(d['template'])
        if reasons:
            raise Blocked('; '.join(reasons))
        binding = self.service.binding(spec.binding_id)
        fault = next((f for f in binding.faults if f.id == spec.fault_id), None)
        if (binding.workload.account_id != d['account_id'] or binding.workload.region != d['region']
                or fault is None or fault.template_id != d['template_id']
                or fault.template_sha256 != d['contract_sha256']):
            raise Blocked('No matching approved account/Region/template revision in this agent binding')
        if spec.mode != 'native':
            raise Blocked('Fleet response benchmarks require native incident delivery; assisted trials remain separate')
        return row, binding

    def attach(self, request):
        self.mapping(request.template_record_id, request.experiment)
        result = self.service.register(request.experiment)
        self.store.put_record('fis_contract', 'workspace', {'template_record_id':request.template_record_id,
            'experiment_ref':result['id'], 'input_hashes':{request.template_record_id:self.store.record(request.template_record_id)['sha256'], result['id']:result['sha256']}})
        return result

    def library(self):
        view = self.catalog.view()
        definitions = self.store.records(kind='experiment')
        for row in view['templates']:
            row['contracts'] = []
            row['execution_gaps'] = execution_gaps(row['data']['template'] or {})
            for record in definitions:
                spec = Experiment.model_validate(record['data'])
                try:
                    _, binding = self.mapping(row['id'], spec)
                except Blocked:
                    continue
                row['contracts'].append({'experiment_ref':record['id'], 'title':spec.title,
                    'binding_id':binding.id, 'agent_account':binding.agent.account_id,
                    'agent_region':binding.agent.region, 'agent_space_id':binding.agent_space_id,
                    'service_id':binding.service_id, 'state':'requires_live_qualification_and_approval'})
        return view

    def create(self, request):
        if len(request.entries) * request.repetitions > 100:
            raise Blocked('A campaign is limited to 100 explicitly enumerated trials')
        signatures = [(e.template_record_id,e.experiment_ref) for e in request.entries]
        if len(set(signatures)) != len(signatures):
            raise Blocked('Use repetitions instead of duplicate plan entries')
        entries = []; hashes = {}
        for entry in request.entries:
            spec = self.service.experiment(entry.experiment_ref)
            row, binding = self.mapping(entry.template_record_id, spec)
            br = self.store.put_record('binding','workspace',binding.model_dump(mode='json'),
                                       'binding-'+digest(binding.model_dump(mode='json')))
            measured = spec.model_dump(mode='json')
            for key in ('id','revision','title','binding_id','fault_id','probe_id'):
                measured.pop(key, None)
            fault = next(f for f in binding.faults if f.id == spec.fault_id)
            probe = next(p for p in binding.probes if p.id == spec.probe_id)
            # Differences in workload, requirements, verifiers or native route
            # split cohorts rather than silently creating a global leaderboard.
            cohort = {'account_id':binding.workload.account_id,'region':binding.workload.region,
                'service_id':binding.service_id,'template_contract':row['data']['contract_sha256'],
                'requirements':measured,'fault':fault.model_dump(mode='json'),
                'probe':probe.model_dump(mode='json'),'checks':[c.model_dump(mode='json') for c in binding.checks],
                'metrics':[m.model_dump(mode='json') for m in binding.metrics],
                'route_reference':{'system':binding.route.reference_system,'format':binding.route.reference_id_format,'alarm':binding.route.alarm_name}}
            entries.append({**entry.model_dump(), 'binding_record_id':br['id'], 'binding_sha256':br['sha256'],
                'template_sha256':row['data']['contract_sha256'], 'template_id':row['data']['template_id'],
                'account_id':binding.workload.account_id,'region':binding.workload.region,
                'agent_account':binding.agent.account_id,'agent_region':binding.agent.region,
                'agent_space_id':binding.agent_space_id,'agent_label':binding.name,'cohort_id':digest(cohort),
                'service_id':binding.service_id})
            for rec in (row,br,self.store.record(entry.experiment_ref)):
                hashes[rec['id']] = rec['sha256']
        body = {**request.model_dump(), 'entries':entries, 'registered_at':iso(), 'input_hashes':hashes,
                'execution_engine':'AWS FIS', 'exposure_order':'repeat-major, entry-order; sequential replays, not simultaneous observers'}
        plan = self.store.put_record('fis_plan','workspace',body)
        return self.store.create('fis_campaign','PLANNED',{'title':request.title, 'plan_id':plan['id'],
            'next_index':0, 'active_trial_id':None, 'completed_trial_ids':[], 'total':len(entries)*request.repetitions,
            'registered_at':iso(), 'blocking_reason':None})

    def command(self, identifier, command):
        e = self.store.entity(identifier)
        if e['kind'] != 'fis_campaign': raise Blocked('Not a FIS campaign')
        if command in ('activate','resume'):
            if e['state'] not in ('PLANNED','PAUSED'): raise Blocked('Campaign cannot be activated in this state')
            if any(x['id'] != identifier and x['state'] in ('RUNNING','CANCELLING') for x in self.store.entities('fis_campaign')):
                raise Blocked('Another fleet campaign owns the dispatch queue')
            state = 'RUNNING'
        elif command == 'pause':
            if e['state'] != 'RUNNING': raise Blocked('Only an active campaign can be paused')
            state = 'PAUSED'
        elif command == 'cancel':
            if e['state'] in ('COMPLETE','CANCELLED'): return e
            state = 'CANCELLING'
        else: raise Blocked('Unknown campaign operation')
        with self.store.transaction() as db:
            current = db.execute('SELECT * FROM entities WHERE id=?', (identifier,)).fetchone()
            if current['revision'] != e['revision']:
                raise Blocked('Campaign changed; reload before issuing the command')
            if state == 'RUNNING' and db.execute(
                    "SELECT id FROM entities WHERE kind='fis_campaign' AND state IN ('RUNNING','CANCELLING') AND id!=?",
                    (identifier,)).fetchone():
                raise Blocked('Another fleet campaign owns the dispatch queue')
            data = json.loads(current['data']); data['blocking_reason'] = None
            db.execute('UPDATE entities SET state=?,revision=revision+1,updated_at=?,data=? WHERE id=?',
                       (state,iso(),canonical(data),identifier))
            self.store._event(db,identifier,'fis.campaign.'+command,{'from':current['state'],'to':state})
        return self.store.entity(identifier)

    def poll_delay(self):
        # Faster catalogue progress while idle, without changing live observation cadence.
        busy = any(e['state'] in ACTIVE for e in self.store.entities('trial'))
        pending = any(e['state'] in {'QUEUED','RUNNING'} for e in self.store.entities('fis_sync'))
        return 1 if pending and not busy else self.config.poll_seconds

    def step(self):
        for e in reversed(self.store.entities('fis_campaign')):
            if e['state'] not in ('RUNNING','CANCELLING'): continue
            try:
                self._advance(e)
            except Exception as exc:
                from .util import error_code
                if self.store.entity(e['id'])['revision'] != e['revision']:
                    return  # Concurrent pause/cancel wins; never overwrite the operator command.
                self.store.update(e['id'],state='PAUSED' if e['state']=='RUNNING' else 'CANCELLING',
                    changes={'blocking_reason':str(exc) if isinstance(exc,Blocked) else error_code(exc)},event='fis.campaign.blocked')
            break
        # Bulk discovery cannot delay stopping, observation or restoration of an active experiment.
        if (any(e['state'] in ACTIVE for e in self.store.entities('trial'))
                or any(e['state'] in {'APPROVED','RUNNING','ROLLBACK_APPROVED','ROLLING_BACK','UNKNOWN_REMOTE_STATE','RESTORE_REQUIRED'} for e in self.store.entities('change'))):
            return
        self.catalog.step()

    def _advance(self, e):
        d = e['data']; plan = self.store.record(d['plan_id'])['data']
        if any(x['state'] in {'UNKNOWN_REMOTE_STATE','RESTORE_REQUIRED'} for x in self.store.entities()):
            raise Blocked('Resolve the uncertain operation or restoration requirement before queue progression')
        current = self.store.entity(d['active_trial_id']) if d.get('active_trial_id') else None
        if e['state'] == 'CANCELLING':
            if current and current['state'] not in CLOSED:
                self.service.abort(current['id']); return
            self.store.update(e['id'],state='CANCELLED',changes={'finished_at':iso()},expected_revision=e['revision']); return
        if current:
            if current['state'] == 'DRAFT': self.service.qualify(current['id'])
            elif current['state'] == 'READY' and current['data'].get('start_approval_id'):
                self.service.start(current['id'])
            elif current['state'] in CLOSED:
                done = d['completed_trial_ids'] + [current['id']]
                aid = current['data'].get('assessment_id')
                dimensions = self.store.record(aid)['data']['dimensions'] if aid else {}
                failed = (current['state'] != 'CLOSED' or not current['data'].get('cleanup_verified')
                          or any(v.get('outcome') == 'fail' for v in dimensions.values())
                          or any(dimensions.get(k,{}).get('outcome') != 'pass' for k in ('challenge','measurement','cleanup','delivery','response')))
                state = 'PAUSED' if failed and plan['stop_on_failure'] else 'RUNNING'
                self.store.update(e['id'],state=state,expected_revision=e['revision'],changes={'completed_trial_ids':done,
                    'active_trial_id':None, 'next_index':d['next_index']+1,
                    'blocking_reason':'Previous trial failed or is unqualified; review it before resuming.' if state=='PAUSED' else None})
            return
        if d['next_index'] >= d['total']:
            self.store.update(e['id'],state='COMPLETE',changes={'finished_at':iso()},expected_revision=e['revision']); return
        # Other direct operations retain the executor's global exclusivity.
        if any(t['state'] in ACTIVE for t in self.store.entities('trial')): return
        entry = plan['entries'][d['next_index'] % len(plan['entries'])]
        spec = self.service.experiment(entry['experiment_ref'])
        binding = self.service.binding(spec.binding_id)
        if digest(binding.model_dump(mode='json')) != entry['binding_sha256']:
            raise Blocked('Campaign binding changed; create a newly reviewed plan')
        for rid, sha in plan['input_hashes'].items():
            if self.store.record(rid)['sha256'] != sha: raise Blocked('Campaign input mismatch')
        tid = e['id'] + '-trial-' + str(d['next_index'])
        trial = self.service.trial(TrialRequest(experiment_ref=entry['experiment_ref']),entity_id=tid)
        if trial['data'].get('fis_campaign_id') not in (None,e['id']): raise Blocked('Trial already belongs to another queue')
        if not trial['data'].get('fis_campaign_id'):
            self.store.update(tid,changes={'fis_campaign_id':e['id'], 'fis_slot':d['next_index']},event='fis.trial.enrolled')
        # If the worker dies before this projection update, the deterministic child is reused.
        self.store.update(e['id'],changes={'active_trial_id':tid},expected_revision=e['revision'])
        if trial['state'] == 'DRAFT': self.service.qualify(tid)
