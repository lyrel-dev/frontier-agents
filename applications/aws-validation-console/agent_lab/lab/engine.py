"""Durable response and prevention workflows, owned by one local worker.

Every transition is journaled. Work is driven by persisted state and provider IDs,
not a browser session. Local failure cannot extend a FIS action's declared finite
duration. Cleanup verification is mandatory and does not assume StopExperiment
reverses changes.
"""
from __future__ import annotations
from datetime import timedelta
import json
from .aws import AWS, FIS_TERMINAL, SSM_TERMINAL
from .broker import Broker
from .evaluation import buckets, evaluate_trial
from .models import Binding, Experiment
from .probe import permitted_addresses
from .util import Blocked, UnknownRemoteState, utcnow, iso, dt, digest

PROBING={'BASELINING','EXPOSING','OBSERVING','CLEANING','ABORTING','UNKNOWN_REMOTE_STATE'}


class Engine:
    def __init__(self,config,store,*,aws_factory=AWS,clock=utcnow):
        self.config=config; self.store=store; self.aws_factory=aws_factory; self.clock=clock

    def instruments(self,trial):
        spec=Experiment.model_validate(self.store.record(trial['data']['experiment_ref'])['data'])
        binding=Binding.model_validate(self.store.record(trial['data']['binding_record_id'])['data'])
        fault=next(f for f in binding.faults if f.id==spec.fault_id)
        probe=next(p for p in binding.probes if p.id==spec.probe_id)
        return spec,binding,fault,probe

    def current_binding(self,identifier):
        return next(b for b in self.config.bindings if b.id==identifier)

    def step(self):
        for campaign in self.store.entities('campaign'):
            if campaign['state'] in {'EVALUATION_APPROVED','EVALUATING'}:
                self._guard(campaign,self.campaign_step)
        for change in self.store.entities('change'):
            if change['state'] in {'APPROVED','RUNNING','ROLLBACK_APPROVED','ROLLING_BACK'}:
                self._guard(change,self.change_step)
        for trial in reversed(self.store.entities('trial')):
            if trial['state'] in {'QUALIFYING','BASELINING','EXPOSING','OBSERVING','CLEANING','ABORTING','SETTLING','FINALIZING','UNKNOWN_REMOTE_STATE'}:
                self._guard(trial,self.trial_step)

    def _guard(self,entity,method):
        try: method(entity)
        except UnknownRemoteState as exc:
            self.store.update(entity['id'],state='UNKNOWN_REMOTE_STATE',changes={'resume_state':entity['state'],'unknown_operation_id':str(exc)},event='remote.unknown')
        except Exception as exc:
            # No raw SDK or credential messages in state/API error strings.
            from .util import error_code
            reason=str(exc) if isinstance(exc,Blocked) else error_code(exc)
            self.store.put_record('workflow_error',entity['id'],{'phase':entity['state'],'at':iso(self.clock()),'reason':reason[:2000]})
            if entity['kind']=='trial':
                latest=self.store.entity(entity['id'])
                if latest['data'].get('fis_id'):
                    state='RESTORE_REQUIRED' if entity['state'] in {'ABORTING','CLEANING'} else 'ABORTING'
                else: state='CLOSED_BLOCKED'
            elif entity['kind']=='change': state='RESTORE_REQUIRED' if entity['state'] in {'RUNNING','ROLLING_BACK'} else 'BLOCKED'
            else: state='BLOCKED'
            self.store.update(entity['id'],state=state,changes={'blocking_reason':reason[:2000]},event='workflow.blocked')

    def _dispatch_approval(self, entity, purpose, operation_name):
        """Validate authority immediately before the FIRST remote dispatch.
        Reconciliation/cleanup of an existing intent is never a new permission.
        """
        op=self.store.operation(entity['id'],operation_name)
        if op and op['state']!='PENDING':
            return
        d=entity['data']
        binding=Binding.model_validate(self.store.record(d['binding_record_id'])['data'])
        if digest(self.current_binding(binding.id).model_dump(mode='json'))!=self.store.record(d['binding_record_id'])['sha256']:
            raise Blocked('Administrator instruments changed since approval')
        key='start_approval_id' if purpose=='start' else 'rollback_approval_id' if purpose=='rollback' else 'approval_id'
        record=self.store.record(d[key]); approval=record['data']
        if approval['purpose']!=purpose or approval['digest']!=digest(approval['subject']):
            raise Blocked('Approval purpose or subject integrity mismatch')
        if dt(approval['expires_at'])<self.clock():
            raise Blocked('Approval expired before provider dispatch; no new mutation sent')
        if not self.config.enable_aws_writes:
            raise Blocked('New AWS mutations have been disabled')

    def _settle_interventions(self, trial):
        """Do not leave a concurrently executing runbook hidden behind cleanup.
        Stopping Automation is NOT rollback; any interrupted change requires an
        explicit rollback and state verification before the environment is freed.
        """
        waiting=False
        for change in self.store.entities('change'):
            if change['data'].get('trial_id')!=trial['id']: continue
            state=change['state']; d=change['data']
            if state in {'PROPOSED','APPROVED'} and not self.store.operation(change['id'],'apply-change'):
                self.store.update(change['id'],state='CANCELLED',changes={'reason':'Trial closed its intervention window'},event='change.cancelled_before_dispatch')
            elif state in {'RUNNING','APPROVED'}:
                binding=Binding.model_validate(self.store.record(d['binding_record_id'])['data'])
                adapter=self.aws_factory(binding,self.store,change['id'])
                intent=self.store.operation(change['id'],'apply-change')
                provider=d.get('automation_id') or (intent or {}).get('provider_id')
                if not provider or (intent and intent['state'] in {'UNKNOWN','DISPATCHING'}):
                    raise Blocked('Intervention provider state is uncertain; reconcile it before restoration')
                remote=adapter.automation(provider)['execution']
                if remote.get('AutomationExecutionStatus') not in SSM_TERMINAL:
                    Broker(self.store,adapter,True).execute(change['id'],'cancel-on-close','change','ssm','stop_automation_execution',{'AutomationExecutionId':provider,'Type':'Cancel'})
                    waiting=True
                else:
                    self.store.update(change['id'],state='RESTORE_REQUIRED',changes={'blocking_reason':'Intervention interrupted by trial close; stopping is not rollback'},event='change.restore_required')
                    raise Blocked('Interrupted intervention requires approved rollback and independent verification')
            elif state in {'UNKNOWN_REMOTE_STATE','RESTORE_REQUIRED'}:
                raise Blocked('Intervention must be reconciled/restored before the environment is released')
            elif state in {'ROLLBACK_APPROVED','ROLLING_BACK'}:
                waiting=True
        return not waiting

    def _save_observation(self,trial,aws,until=None):
        d=trial['data']; start=d['started_at']; end=until or iso(self.clock())
        try:
            observation=aws.observe(start,end,d.get('exposure_at'),d.get('assisted_task_id'))
            record=self.store.put_record('observation',trial['id'],observation)
            self.store.update(trial['id'],changes={'observation_id':record['id'],'last_collection_at':iso(self.clock())})
            return record
        except Exception:
            # The source adapter has already journaled the error. Missing polls
            # cannot be interpreted as no task, no effect, or healthy service.
            self.store.put_record('observation_gap',trial['id'],{'at':iso(self.clock()),'start':start,'end':end})
            return None

    def _verify_change_for_replay(self,trial,aws):
        if trial['data']['arm'] not in {'treatment','benign'} or not trial['data'].get('campaign_id'): return None
        if trial['data']['arm']=='benign' and not self.store.entity(trial['data']['campaign_id'])['data'].get('change_id'): return None
        campaign=self.store.entity(trial['data']['campaign_id'])
        change=self.store.entity(campaign['data']['change_id'])
        if change['state']!='VERIFIED': raise Blocked('Prevention change has not been verified')
        book=next(b for b in aws.b.runbooks if b.id==change['data']['runbook_id'])
        checks=aws.checks(book.after_checks)
        if not all(c['passed'] for c in checks): raise Blocked('Prevention change no longer present')
        return change['id']

    def trial_step(self,trial):
        spec,binding,fault,probe=self.instruments(trial)
        aws=self.aws_factory(binding,self.store,trial['id'])
        broker=Broker(self.store,aws,self.config.enable_aws_writes)
        now=self.clock(); d=trial['data']; state=trial['state']; tid=trial['id']
        if state=='UNKNOWN_REMOTE_STATE':
            unresolved=[op for op in self.store.operations(tid) if op['state'] in {'UNKNOWN','DISPATCHING'}]
            if all(broker.reconcile_automatically(op) for op in unresolved):
                self.store.update(tid,state=d.get('resume_state','ABORTING'),changes={'unknown_operation_id':None},event='remote.reconciled')
            return
        if state=='QUALIFYING':
            if digest(self.current_binding(binding.id).model_dump(mode='json'))!=d['binding_sha256']:
                raise Blocked('Administrator binding changed; register a new trial')
            permitted_addresses(probe)
            qualification=aws.qualify(spec)
            self._verify_change_for_replay(trial,aws)
            record=self.store.put_record('qualification',tid,qualification)
            self.store.update(tid,state='READY',changes={'qualification_id':record['id'],'qualification_digest':record['sha256']},event='trial.qualified')
            return
        if d.get('abort_requested') and state not in {'ABORTING','CLEANING','SETTLING','FINALIZING'}:
            self.store.update(tid,state='ABORTING',changes={'aborted':True},event='trial.abort_started'); return
        if state=='BASELINING':
            if (now-dt(d['started_at'])).total_seconds()<spec.baseline_seconds: return
            rows=buckets(self.store.probes(tid),d['started_at'],iso(dt(d['started_at'])+timedelta(seconds=spec.baseline_seconds)),spec,probe.requests_per_second)
            if not rows or not all(r['healthy'] for r in rows): raise Blocked('Real baseline traffic or health did not meet the registered requirements; no fault started')
            baseline=self.store.put_record('baseline',tid,{'buckets':rows,'probe_input_sha256':digest(self.store.probes(tid))})
            # Re-read exact immutable instruments and baseline facts immediately
            # before mutation; an old approval is not permission for changed targets.
            fresh=aws.qualify(spec)
            pinned=self.store.record(d['qualification_id'])['data']
            if fresh['template']['contract']!=pinned['template']['contract']:
                raise Blocked('Qualified template changed before exposure')
            change_id=self._verify_change_for_replay(trial,aws)
            self.store.update(tid,state='EXPOSING',changes={'baseline_record_id':baseline['id'],'prevention_change_id':change_id,
                 'fault_requested_at':iso(now),'last_worker_tick':iso(now)},event='trial.baseline_passed')
            return
        if state=='EXPOSING':
            if d['arm']=='benign':
                self.store.update(tid,state='OBSERVING',changes={'exposure_at':iso(now),'observation_ends_at':iso(now+timedelta(seconds=spec.observation_seconds)),
                                   'fault_state':'not_applied','fault_confirmed':False},event='trial.benign_started'); return
            # This call rechecks the pinned template and stop-alarm states. It
            # still cannot prove future AWS efficacy or prevent concurrent admin edits.
            aws.template(fault)
            self._dispatch_approval(trial,'start','start-fault')
            op=broker.execute(tid,'start-fault','fault','fis','start_experiment',{'experimentTemplateId':fault.template_id,'experimentOptions':{'actionsMode':'run-all'}})
            eid=op['provider_id']
            self.store.update(tid,changes={'fis_id':eid},event='trial.fis_attached')
            status=aws.experiment(eid); value=status['experiment']
            if value.get('state',{}).get('status') in {'failed','stopped'}: raise Blocked('FIS did not start the approved exposure')
            start=value.get('startTime')
            if not start:
                if (now-dt(d['fault_requested_at'])).total_seconds()>120: raise Blocked('FIS start deadline exceeded')
                return
            self.store.update(tid,state='OBSERVING',changes={'exposure_at':start,'observation_ends_at':iso(dt(start)+timedelta(seconds=spec.observation_seconds)),
                                   'last_worker_tick':iso(now)},event='trial.exposure_started')
            return
        if state=='OBSERVING':
            last=d.get('last_worker_tick')
            if last and (now-dt(last)).total_seconds()>max(90,self.config.poll_seconds*5):
                self.store.put_record('worker_gap',tid,{'from':last,'to':iso(now)})
                self.store.update(tid,state='ABORTING',changes={'aborted':True,'blocking_reason':'Worker interruption exceeded the observation gap budget'},event='trial.worker_gap'); return
            self.store.update(tid,changes={'last_worker_tick':iso(now)})
            if d.get('fis_id'):
                status=aws.experiment(d['fis_id']); value=status['experiment']
                resolved=sorted({r.get('resourceArn') or r.get('targetInformation',{}).get('arn','') for r in status['resolved_targets']})
                resolved=[x for x in resolved if x]
                # AWS uses targetInformation.arn for resolved resources; retain
                # the entire source response and reject anything not exactly scoped.
                target_ok=resolved==sorted(set(fault.target_arns))
                action_states=[a.get('state',{}).get('status') for a in value.get('actions',{}).values()]
                if any(x in {'skipped','failed','stopped'} for x in action_states) or value.get('state',{}).get('status') in {'failed','stopped'}:
                    self.store.update(tid,state='ABORTING',changes={'aborted':True,'fault_state':value['state']['status'],'blocking_reason':'FIS stopped, failed or skipped a required action'},event='trial.fis_incomplete'); return
                if resolved and not target_ok: raise Blocked('Actual FIS target set differs from the approved set')
                changes={'fault_state':value.get('state',{}).get('status'),'targets_verified':target_ok,'resolved_target_arns':resolved}
                if value.get('endTime'):
                    changes['fault_end_at']=value['endTime']
                    changes['fault_duration_seconds']=(dt(value['endTime'])-dt(value['startTime'])).total_seconds()
                self.store.update(tid,changes=changes)
                if not d.get('fault_confirmed') and target_ok and any(x in {'running','completed'} for x in action_states):
                    checks=aws.checks(fault.fault_checks+spec.oracle.required_checks)
                    if all(c['passed'] for c in checks):
                        truth=self.store.put_record('ground_truth',tid,{'oracle':spec.oracle.model_dump(mode='json'),'verified_checks':checks,
                             'fis_source':status['source_record_id'],'verified_at':iso(now),'definition_sha256':digest(spec.model_dump(mode='json'))})
                        self.store.update(tid,changes={'fault_confirmed':True,'ground_truth_id':truth['id']},event='trial.fault_verified')
            if spec.mode=='assisted' and not d.get('assisted_task_id'):
                # Symptoms only. The oracle, expected mechanism and hidden rubric
                # never enter an Agent Space request.
                op=broker.execute(tid,'assisted-investigation','requester','devops-agent','create_backlog_task',{
                    'agentSpaceId':binding.agent_space_id,'taskType':'INVESTIGATION','priority':'HIGH',
                    'title':'Authorized incident investigation: '+binding.service_id+' ['+tid+']',
                    'description':'Investigate the observed service symptoms and telemetry for '+binding.service_id+'. This is an explicitly assisted validation trial.'})
                self.store.update(tid,changes={'assisted_task_id':op['provider_id']},event='trial.assisted_task_created')
                trial=self.store.entity(tid); d=trial['data']
            self._save_observation(trial,aws)
            if now>=dt(d['observation_ends_at']):
                self.store.update(tid,state='CLEANING',changes={'observation_finished_at':iso(now),'cleanup_started_at':iso(now)},event='trial.observation_closed')
            return
        if state in {'ABORTING','CLEANING'}:
            # Stopping and the originally approved cleanup remain authorized if
            # administrator configuration is changed to disable NEW mutations.
            safety=Broker(self.store,aws,True)
            if state=='ABORTING' and not d.get('aborted'):
                self.store.update(tid,changes={'aborted':True}); d=self.store.entity(tid)['data']
            if not d.get('cleanup_started_at'):
                self.store.update(tid,changes={'cleanup_started_at':iso(now)}); d=self.store.entity(tid)['data']
            if d.get('fis_id'):
                status=aws.experiment(d['fis_id']); value=status['experiment']; fis_state=value.get('state',{}).get('status')
                if fis_state not in FIS_TERMINAL:
                    safety.execute(tid,'stop-fault','fault','fis','stop_experiment',{'id':d['fis_id']})
                    if (now-dt(d['cleanup_started_at'])).total_seconds()>fault.max_fault_seconds+120:
                        raise Blocked('FIS stopping did not reach a terminal state')
                    return
                updates={'fault_state':fis_state}
                if value.get('endTime') and value.get('startTime'):
                    updates.update(fault_end_at=value['endTime'],fault_duration_seconds=(dt(value['endTime'])-dt(value['startTime'])).total_seconds())
                self.store.update(tid,changes=updates)
            if not self._settle_interventions(self.store.entity(tid)):
                if (now-dt(d['cleanup_started_at'])).total_seconds()>fault.max_fault_seconds+180:
                    raise Blocked('Intervention cancellation exceeded the cleanup budget')
                return
            if fault.cleanup_runbook_id and d.get('fis_id'):
                book=next(x for x in binding.runbooks if x.id==fault.cleanup_runbook_id)
                aws.document(book)
                op=safety.execute(tid,'cleanup-runbook','change','ssm','start_automation_execution',{
                    'DocumentName':book.document_arn,'DocumentVersion':book.document_version,'Parameters':book.parameters,'Mode':'Auto'})
                status=aws.automation(op['provider_id'])['execution']; s=status.get('AutomationExecutionStatus')
                if s not in SSM_TERMINAL:
                    if (now-dt(op['created_at'])).total_seconds()>book.timeout_seconds:
                        safety.execute(tid,'cancel-cleanup','change','ssm','stop_automation_execution',{'AutomationExecutionId':op['provider_id'],'Type':'Cancel'})
                        raise Blocked('Cleanup runbook deadline exceeded; restoration requires an operator')
                    return
                if s not in {'Success','CompletedWithSuccess'}: raise Blocked('Cleanup Automation failed')
            checks=aws.checks(fault.cleanup_checks)
            if not all(c['passed'] for c in checks):
                if (now-dt(d['cleanup_started_at'])).total_seconds()>fault.max_fault_seconds+180: raise Blocked('Cleanup state remains unverified')
                return
            change_id=self._verify_change_for_replay(self.store.entity(tid),aws)
            self.store.update(tid,state='SETTLING',changes={'cleanup_verified':True,'change_still_verified':bool(change_id),
                'settle_until':iso(now+timedelta(seconds=spec.ingestion_wait_seconds))},event='trial.cleanup_verified')
            return
        if state=='SETTLING':
            if now<dt(d['settle_until']): return
            end=d.get('observation_ends_at') or iso(now)
            observation=self._save_observation(trial,aws,until=min(end,iso(now)))
            self.store.update(tid,state='FINALIZING',changes={'final_observation_id':observation['id'] if observation else None},event='trial.evidence_closed')
            return
        if state=='FINALIZING':
            final='CLOSED_ABORTED' if d.get('aborted') else 'CLOSED'
            self.store.update(tid,state=final,changes={'closed_at':iso(now)},event='trial.closed')
            evaluate_trial(self.store,tid,binding)

    def campaign_step(self,campaign):
        d=campaign['data']; cid=campaign['id']; spec=Experiment.model_validate(self.store.record(d['experiment_ref'])['data'])
        binding=Binding.model_validate(self.store.record(d['binding_record_id'])['data'])
        aws=self.aws_factory(binding,self.store,cid); broker=Broker(self.store,aws,self.config.enable_aws_writes)
        if campaign['state']=='EVALUATION_APPROVED':
            self._dispatch_approval(campaign,'evaluation','prevention-evaluation')
            baseline=[t for t in self.store.entities('trial') if t['data'].get('campaign_id')==cid and t['data']['arm']=='baseline' and t['state']=='CLOSED']
            if not baseline: raise Blocked('No completed baseline incident')
            task_ids=[]
            for t in baseline:
                if not t['data'].get('assessment_id'): continue
                assessment=self.store.record(t['data']['assessment_id'])['data']
                if assessment['dimensions']['challenge']['outcome']!='pass' or not assessment['impact_at']: continue
                for record in self.store.records(t['id'],'observation'):
                    if record['data'].get('task'): task_ids.append(record['data']['task']['taskId'])
            if not task_ids: raise Blocked('No qualified baseline incident with correlated Agent Space investigation history')
            op=broker.execute(cid,'prevention-evaluation','requester','devops-agent','create_backlog_task',{
                'agentSpaceId':binding.agent_space_id,'taskType':'EVALUATION','priority':'MEDIUM',
                'title':'Reliability evaluation: '+binding.service_id+' ['+cid+']',
                'description':'Review incident history for '+binding.service_id+'. Relevant investigation tasks: '+', '.join(sorted(set(task_ids)))+'. Propose evidence-supported changes to reduce recurrence or impact.'})
            self.store.update(cid,state='EVALUATING',changes={'evaluation_task_id':op['provider_id'],'evaluation_requested_at':iso(self.clock())},event='campaign.evaluation_requested'); return
        response=aws.recommendations(d['evaluation_task_id'])
        snapshot=self.store.put_record('recommendation_poll',cid,response)
        changes={'recommendation_poll_id':snapshot['id'],'recommendation_ids':response['recommendation_record_ids']}
        if response['recommendation_record_ids']:
            self.store.update(cid,state='RECOMMENDATIONS',changes=changes,event='campaign.recommendations_available')
        elif response['task']['status'] in {'FAILED','TIMED_OUT','CANCELLED','SKIPPED'}:
            self.store.update(cid,state='BLOCKED',changes={**changes,'blocking_reason':'Agent evaluation ended without a recommendation'},event='campaign.no_recommendation')
        elif (self.clock()-dt(d['evaluation_requested_at'])).total_seconds()>3600:
            self.store.update(cid,state='BLOCKED',changes={**changes,'blocking_reason':'No recommendation within the one-hour evaluation observation budget'},event='campaign.no_recommendation')
        else: self.store.update(cid,changes=changes)

    def change_step(self,change):
        d=change['data']; cid=change['id']
        binding=Binding.model_validate(self.store.record(d['binding_record_id'])['data'])
        book=next(b for b in binding.runbooks if b.id==d['runbook_id'])
        rollback=change['state'] in {'ROLLBACK_APPROVED','ROLLING_BACK'}
        if rollback:
            if not book.rollback_runbook_id: raise Blocked('No registered rollback instrument')
            book=next(b for b in binding.runbooks if b.id==book.rollback_runbook_id)
        aws=self.aws_factory(binding,self.store,cid); broker=Broker(self.store,aws,self.config.enable_aws_writes)
        name='rollback' if rollback else 'apply-change'
        if change['state'] in {'APPROVED','ROLLBACK_APPROVED'}:
            if d.get('trial_id') and not rollback:
                parent=self.store.entity(d['trial_id'])
                if parent['data'].get('abort_requested') or parent['state']!='OBSERVING' or self.clock()>=dt(parent['data']['observation_ends_at']):
                    if not self.store.operation(cid,name):
                        self.store.update(cid,state='CANCELLED',event='change.cancelled_before_dispatch'); return
                    raise Blocked('Trial intervention window closed; reconcile any original operation')
            self._dispatch_approval(change,'rollback' if rollback else 'change',name)
            aws.document(book)
            before=aws.checks(book.before_checks)
            if before and not all(c['passed'] for c in before): raise Blocked('Change precondition differs from approved state')
            if d.get('trial_id'):
                trial=self.store.entity(d['trial_id'])
                if trial['state']!='OBSERVING' and not rollback: raise Blocked('Mitigation can execute only during the active observation interval')
            op=broker.execute(cid,name,'change','ssm','start_automation_execution',{
                'DocumentName':book.document_arn,'DocumentVersion':book.document_version,'Parameters':book.parameters,'Mode':'Auto'})
            self.store.update(cid,state='ROLLING_BACK' if rollback else 'RUNNING',changes={'automation_id':op['provider_id'],'execution_started_at':iso(self.clock())},event='change.executing'); return
        status=aws.automation(d['automation_id']); value=status['execution']; state=value.get('AutomationExecutionStatus')
        if state not in SSM_TERMINAL:
            if (self.clock()-dt(d['execution_started_at'])).total_seconds()>book.timeout_seconds:
                Broker(self.store,aws,True).execute(cid,'cancel-'+name,'change','ssm','stop_automation_execution',{'AutomationExecutionId':d['automation_id'],'Type':'Cancel'})
                raise Blocked('Automation exceeded its approved deadline; independent state restoration required')
            return
        if state not in {'Success','CompletedWithSuccess'}: raise Blocked('Automation did not complete successfully')
        verified=aws.checks(book.after_checks)
        if not all(x['passed'] for x in verified): raise Blocked('Execution succeeded but intended deployed state is not verified')
        record=self.store.put_record('change_verification',cid,{'checks':verified,'automation_source':status['source_record_id'],
                  'runbook_sha256':book.content_sha256,'implementation_artifact':book.implementation_artifact,
                  'implementation_diff_sha256':book.implementation_diff_sha256,'verified_at':iso(self.clock())})
        self.store.update(cid,state='ROLLED_BACK' if rollback else 'VERIFIED',changes={'verification_id':record['id'],'verified_at':iso(self.clock())},event='change.verified')
        if d.get('campaign_id'):
            self.store.update(d['campaign_id'],state='BASELINES' if rollback else 'REPLAY_READY',changes={'change_id':cid},event='campaign.change_verified')
