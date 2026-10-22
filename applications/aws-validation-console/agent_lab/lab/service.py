"""User commands. They register intent; the worker alone dispatches AWS writes."""
from __future__ import annotations
from datetime import timedelta
from .aws import AWS
from .broker import Broker
from .evaluation import text_content, evaluate_trial, compare_campaign
from .models import Experiment, Binding, TrialRequest, CampaignRequest, Approval, Diagnosis, ChangeProposal
from .util import Blocked, digest, iso, dt, utcnow


class Service:
    def __init__(self,config,store,*,aws_factory=AWS,clock=utcnow):
        self.config=config; self.store=store; self.aws_factory=aws_factory; self.clock=clock

    def binding(self,identifier):
        matches=[b for b in self.config.bindings if b.id==identifier]
        if len(matches)!=1: raise Blocked('Environment binding is not configured')
        return matches[0]

    def experiment(self,reference):
        record=self.store.record(reference)
        if record['kind']!='experiment': raise Blocked('Reference is not an experiment definition')
        return Experiment.model_validate(record['data'])

    def register(self,spec:Experiment):
        binding=self.binding(spec.binding_id)
        fault=next((f for f in binding.faults if f.id==spec.fault_id),None)
        if not fault or spec.probe_id not in {p.id for p in binding.probes}: raise Blocked('Unregistered fault or workload instrument')
        if spec.observation_seconds<fault.max_fault_seconds+spec.stable_seconds:
            raise Blocked('Observation must outlast the maximum fault budget plus the stable recovery interval')
        if not set(spec.oracle.affected_resource_arns)<=set(fault.target_arns): raise Blocked('Oracle resources exceed approved fault targets')
        if not set(spec.oracle.required_checks)<={c.id for c in binding.checks}: raise Blocked('Unregistered ground-truth verifier')
        if not set(spec.intervention_runbook_ids)<={r.id for r in binding.runbooks}: raise Blocked('Unregistered intervention runbook')
        if spec.mode=='assisted' and not binding.requester_profile: raise Blocked('Assisted mode needs an explicit agent requester profile')
        return self.store.put_record('experiment','workspace',spec.model_dump(mode='json'),f'experiment:{spec.id}@{spec.revision}')

    def campaign(self,request:CampaignRequest):
        spec=self.experiment(request.experiment_ref); binding=self.binding(spec.binding_id)
        br=self.store.put_record('binding','workspace',binding.model_dump(mode='json'),'binding-'+digest(binding.model_dump(mode='json')))
        return self.store.create('campaign','BASELINES',{'title':request.title,'experiment_ref':request.experiment_ref,
              'binding_record_id':br['id'],'comparison':request.comparison.model_dump(mode='json'),
              'plan_sha256':digest(request.model_dump(mode='json')),'registered_at':iso(self.clock())})

    def trial(self,request:TrialRequest):
        spec=self.experiment(request.experiment_ref); binding=self.binding(spec.binding_id)
        if request.arm=='treatment' and not request.campaign_id: raise Blocked('A treatment run requires a prevention campaign')
        if request.campaign_id:
            campaign=self.store.entity(request.campaign_id)
            if campaign['kind']!='campaign' or campaign['data']['experiment_ref']!=request.experiment_ref: raise Blocked('Campaign/experiment mismatch')
            if request.arm=='treatment' and campaign['state']!='REPLAY_READY': raise Blocked('Deploy and verify the linked recommendation before replay')
            if request.arm=='baseline' and campaign['state']!='BASELINES': raise Blocked('Untreated baselines must precede the prevention implementation')
        br=self.store.put_record('binding','workspace',binding.model_dump(mode='json'),'binding-'+digest(binding.model_dump(mode='json')))
        return self.store.create('trial','DRAFT',{'title':spec.title,'experiment_ref':request.experiment_ref,
              'binding_record_id':br['id'],'binding_sha256':br['sha256'],'campaign_id':request.campaign_id,'arm':request.arm,
              'registered_at':iso(self.clock()),'configuration_version':'0.3','fault_confirmed':False,'cleanup_verified':False})

    def qualify(self,trial_id):
        trial=self.store.entity(trial_id)
        if trial['kind']!='trial' or trial['state'] not in {'DRAFT','BLOCKED'}: raise Blocked('Only a draft trial can be qualified')
        return self.store.update(trial_id,state='QUALIFYING',changes={'blocking_reason':None},expected_revision=trial['revision'],event='trial.qualification_requested')

    def approval_subject(self,entity_id,purpose='start'):
        entity=self.store.entity(entity_id); d=entity['data']
        binding=Binding.model_validate(self.store.record(d['binding_record_id'])['data'])
        if purpose=='start':
            if entity['kind']!='trial' or entity['state']!='READY': raise Blocked('Trial is not ready for approval')
            definition=self.experiment(d['experiment_ref'])
            fault=next(f for f in binding.faults if f.id==definition.fault_id)
            workload=next(p for p in binding.probes if p.id==definition.probe_id)
            subject={'trial_id':entity_id,'experiment_sha256':self.store.record(d['experiment_ref'])['sha256'],
                     'binding_sha256':d['binding_sha256'],'qualification_sha256':self.store.record(d['qualification_id'])['sha256'],
                     'agent_account':binding.agent.account_id,'agent_space':binding.agent_space_id,
                     'workload_account':binding.workload.account_id,'workload_region':binding.workload.region,
                     'arm':d['arm'],'incident_mode':definition.mode,'fault':fault.model_dump(mode='json'),
                     'workload':{'probe_id':workload.id,'url':workload.url,'requests_per_second':workload.requests_per_second},
                     'observation_seconds':definition.observation_seconds,
                     'qualified_action_contract':self.store.record(d['qualification_id'])['data']['template']['contract']}
        elif purpose=='evaluation':
            if entity['kind']!='campaign' or entity['state']!='BASELINES': raise Blocked('Campaign is not ready for evaluation')
            trials=[t for t in self.store.entities('trial') if t['data'].get('campaign_id')==entity_id and t['data']['arm']=='baseline']
            if not trials or any(t['state'] not in {'CLOSED','CLOSED_ABORTED','CLOSED_BLOCKED'} for t in trials): raise Blocked('Close all baseline attempts first')
            subject={'campaign_id':entity_id,'plan_sha256':d['plan_sha256'],'baseline_assessments':[t['data'].get('assessment_id') for t in trials],
                     'binding_sha256':self.store.record(d['binding_record_id'])['sha256']}
        elif purpose in {'change','rollback'}:
            if entity['kind']!='change': raise Blocked('Not a change proposal')
            if purpose=='change' and entity['state']!='PROPOSED': raise Blocked('Change is not awaiting approval')
            if purpose=='rollback' and entity['state'] not in {'VERIFIED','RESTORE_REQUIRED'}: raise Blocked('Change is not eligible for rollback')
            book=next(b for b in binding.runbooks if b.id==d['runbook_id'])
            if purpose=='rollback' and not book.rollback_runbook_id: raise Blocked('No registered rollback')
            rollback=next((b for b in binding.runbooks if b.id==book.rollback_runbook_id),None)
            subject={'change_id':entity_id,'proposal_sha256':self.store.record(d['proposal_record_id'])['sha256'],
                     'runbook':book.model_dump(mode='json'),'rollback':rollback.model_dump(mode='json') if rollback else None,
                     'source_sha256':self.store.record(d['source_record_id'])['sha256'],'purpose':purpose}
        else: raise Blocked('Unsupported approval purpose')
        account=binding.agent.account_id if purpose=='evaluation' else binding.workload.account_id
        confirmation=f'{purpose.upper()} {account} {binding.agent_space_id} {entity_id}'
        return {'subject':subject,'digest':digest(subject),'confirmation':confirmation,'purpose':purpose}

    def approve(self,entity_id,purpose,approval:Approval):
        subject=self.approval_subject(entity_id,purpose)
        if approval.expected_digest!=subject['digest'] or approval.confirmation!=subject['confirmation']:
            raise Blocked('Approval does not match the exact current subject and account confirmation')
        if not self.config.enable_aws_writes: raise Blocked('Administrator has not enabled AWS execution')
        record=self.store.put_record('approval',entity_id,{**approval.model_dump(mode='json'),**subject,
              'approved_at':iso(self.clock()),'expires_at':iso(self.clock()+timedelta(seconds=self.config.approval_ttl_seconds)),
              'authority':'local approval-token holder; not AWS IAM identity'})
        if purpose=='start': self.store.update(entity_id,changes={'start_approval_id':record['id']},event='trial.approved')
        elif purpose=='evaluation': self.store.update(entity_id,state='EVALUATION_APPROVED',changes={'approval_id':record['id']},event='campaign.evaluation_approved')
        elif purpose=='change':
            self.store.reserve_change(entity_id,record,rollback=False)
        elif purpose=='rollback': self.store.reserve_change(entity_id,record,rollback=True)
        return record

    def _change_exclusivity(self,change_id):
        change=self.store.entity(change_id)
        active=[t for t in self.store.entities('trial') if t['state'] in {'BASELINING','EXPOSING','OBSERVING','ABORTING','CLEANING','UNKNOWN_REMOTE_STATE'}]
        if active and (len(active)!=1 or change['data'].get('trial_id')!=active[0]['id']): raise Blocked('Another workload trial owns the environment')
        if any(c['id']!=change_id and c['state'] in {'APPROVED','RUNNING','UNKNOWN_REMOTE_STATE','ROLLBACK_APPROVED','ROLLING_BACK'} for c in self.store.entities('change')):
            raise Blocked('Another change owns the execution slot')

    def start(self,trial_id):
        trial=self.store.entity(trial_id); d=trial['data']
        if not self.config.enable_aws_writes: raise Blocked('New AWS mutations are disabled')
        if not d.get('start_approval_id'): raise Blocked('Exact approval is required')
        approval=self.store.record(d['start_approval_id'])
        if dt(approval['data']['expires_at'])<self.clock(): raise Blocked('Approval expired')
        if approval['data']['digest']!=self.approval_subject(trial_id)['digest']: raise Blocked('Approval subject changed')
        spec=self.experiment(d['experiment_ref'])
        if digest(self.binding(spec.binding_id).model_dump(mode='json'))!=d['binding_sha256']: raise Blocked('Administrator instruments changed')
        heartbeat=self.store.meta('worker') or {}
        if heartbeat.get('state')!='running' or (self.clock()-dt(heartbeat['heartbeat_at'])).total_seconds()>90: raise Blocked('A live durable worker is required')
        return self.store.start_trial(trial_id,approval,started_at=iso(self.clock()))

    def abort(self,trial_id):
        trial=self.store.entity(trial_id)
        if trial['kind']!='trial': raise Blocked('Not a trial')
        if trial['state'] in {'CLOSED','CLOSED_ABORTED','CLOSED_BLOCKED'}: return trial
        if trial['state'] in {'DRAFT','READY','BLOCKED'}:
            return self.store.update(trial_id,state='CLOSED_ABORTED',changes={'aborted':True,'closed_at':iso(self.clock())},event='trial.cancelled_before_exposure')
        return self.store.update(trial_id,changes={'abort_requested':True,'aborted':True},event='trial.abort_requested')

    def diagnosis(self,trial_id,review:Diagnosis):
        trial=self.store.entity(trial_id); d=trial['data']
        if not d.get('ground_truth_id'): raise Blocked('A verified ground-truth capture is required')
        finding=self.store.record(review.finding_record_id)
        if finding['kind']!='finding' or finding['owner']!=trial_id or finding['data'].get('recordType')!='investigation_summary_md': raise Blocked('Select a collected investigation finding from this trial')
        if review.finding_quote not in text_content(finding['data']['content']): raise Blocked('Finding quote is not present in the pinned journal content')
        ground=self.store.record(d['ground_truth_id'])
        permitted={x['source_record_id'] for x in ground['data']['verified_checks']}
        hashes={finding['id']:finding['sha256'],ground['id']:ground['sha256']}
        for citation in review.citations:
            record=self.store.record(citation.record_id)
            if record['owner']!=trial_id or record['id'] not in permitted: raise Blocked('Ground-truth citations must reference independently captured verifier responses')
            if citation.quote not in text_content(record['data']): raise Blocked('Evidence quote is not in the captured source')
            hashes[record['id']]=record['sha256']
        record=self.store.put_record('diagnosis',trial_id,{**review.model_dump(mode='json'),'ground_truth_id':ground['id'],'input_hashes':hashes,'reviewed_at':iso(self.clock())})
        self.store.update(trial_id,changes={'diagnosis_review_id':record['id']},event='trial.diagnosis_selected')
        return record

    def pin_recommendation(self,campaign_id,record_id):
        campaign=self.store.entity(campaign_id)
        if campaign['kind']!='campaign' or campaign['state'] not in {'RECOMMENDATIONS','CHANGE_REVIEW'}: raise Blocked('No recommendation selection is open')
        record=self.store.record(record_id)
        if record_id not in campaign['data'].get('recommendation_ids',[]) or record['kind']!='recommendation' or record['owner']!=campaign_id:
            raise Blocked('Recommendation must belong to this campaign evaluation')
        return self.store.update(campaign_id,state='CHANGE_REVIEW',changes={'recommendation_record_id':record_id},event='campaign.recommendation_pinned')

    def propose_change(self,owner,request:ChangeProposal):
        entity=self.store.entity(owner); d=entity['data']
        binding=Binding.model_validate(self.store.record(d['binding_record_id'])['data'])
        book=next((b for b in binding.runbooks if b.id==request.runbook_id),None)
        if not book: raise Blocked('Runbook is not administrator registered')
        source=self.store.record(request.source_record_id)
        if entity['kind']=='trial':
            spec=self.experiment(d['experiment_ref'])
            if request.runbook_id not in spec.intervention_runbook_ids: raise Blocked('Runbook is not in the approved experiment intervention set')
            if source['owner']!=owner or source['kind']!='finding': raise Blocked('Mitigation must cite an actual collected finding')
            if source['data'].get('recordType')!='mitigation_summary_md': raise Blocked('Mitigation must cite a mitigation summary, not an arbitrary document')
        elif entity['kind']=='campaign':
            if entity['state']!='CHANGE_REVIEW' or request.source_record_id!=d.get('recommendation_record_id'): raise Blocked('Change must cite the pinned recommendation version')
        else: raise Blocked('Changes belong to a trial or prevention campaign')
        if request.source_quote not in text_content(source['data']): raise Blocked('Source quotation is not present')
        proposal=self.store.put_record('change_proposal',owner,{**request.model_dump(mode='json'),'source_sha256':source['sha256'],
                  'runbook_contract':book.model_dump(mode='json'),'registered_at':iso(self.clock()),
                  'interpretation':'Operator-mapped runbook; agent text is never directly executed.'})
        change=self.store.create('change','PROPOSED',{'title':book.title,'binding_record_id':d['binding_record_id'],
              'runbook_id':book.id,'source_record_id':source['id'],'proposal_record_id':proposal['id'],
              'trial_id':owner if entity['kind']=='trial' else None,'campaign_id':owner if entity['kind']=='campaign' else None})
        if entity['kind']=='campaign': self.store.update(owner,changes={'change_id':change['id']},event='campaign.change_proposed')
        return change

    def retry_cleanup(self,trial_id):
        trial=self.store.entity(trial_id)
        if trial['kind']!='trial' or trial['state']!='RESTORE_REQUIRED':
            raise Blocked('Only an unresolved restoration can be rechecked')
        if any(o['state'] in {'UNKNOWN','DISPATCHING'} for o in self.store.operations(trial_id)):
            raise Blocked('Reconcile uncertain provider operations first')
        return self.store.update(trial_id,state='ABORTING',changes={'cleanup_started_at':iso(self.clock()),'aborted':True},event='trial.restoration_recheck_requested')

    def reconcile(self,entity_id,operation_id,provider_id):
        entity=self.store.entity(entity_id)
        if entity['state']!='UNKNOWN_REMOTE_STATE': raise Blocked('Entity is not awaiting provider reconciliation')
        op=next((x for x in self.store.operations(entity_id) if x['id']==operation_id),None)
        if not op: raise Blocked('Operation does not belong to this entity')
        binding=Binding.model_validate(self.store.record(entity['data']['binding_record_id'])['data'])
        aws=self.aws_factory(binding,self.store,entity_id)
        result=Broker(self.store,aws,False).reconcile(op,provider_id)
        self.store.update(entity_id,state=entity['data']['resume_state'],changes={'unknown_operation_id':None},event='remote.reconciled_by_read')
        return result
