"""Persist intent, dispatch once, and reconcile uncertain provider operations."""
from __future__ import annotations
from botocore.exceptions import ClientError
from .fis_safety import read_safety_lever
from .util import Blocked, UnknownRemoteState, dt, iso, error_code

DEFINITIVE_REJECTIONS={'AccessDeniedException','AccessDenied','UnauthorizedOperation','ValidationException',
    'ValidationError','InvalidParameterException','ResourceNotFoundException','InvalidDocument','InvalidDocumentVersion'}


class Broker:
    def __init__(self,store,aws,enabled):
        self.store=store; self.aws=aws; self.enabled=enabled

    def execute(self, owner, name, side, service, operation, params):
        if not self.enabled: raise Blocked('AWS mutations are disabled in administrator configuration')
        self.aws.identity(side)  # A failed identity read cannot leave an uncertain write intent.
        request={'side':side,'service':service,'operation':operation,'parameters':params}
        op=self.store.operation(owner,name)
        if op:
            # Validate the original request even when returning a previous result.
            op=self.store.intent(owner,name,request)
            if op['state']=='CONFIRMED': return op
            if op['state']=='FAILED': raise Blocked('Previously rejected provider operation: '+name)
            if op['state'] in ('DISPATCHING','UNKNOWN'):
                if self.reconcile_automatically(op): return self.store.operation(owner,name)
                raise UnknownRemoteState(op['id'])
        if service == 'fis' and operation == 'start_experiment':
            if side != 'fault':
                raise Blocked('FIS starts require the configured workload fault identity')
            # Read at first dispatch, not just in optional onboarding. A previous
            # read is not authority. Reconciliation and cleanup bypass this gate.
            try:
                lever = read_safety_lever(self.aws)
                allowed = lever.get('status') == 'disengaged'
                self.store.put_record('execution_guard', owner, {
                    'guard': 'fis_safety_lever', 'at': iso(), 'allowed': allowed,
                    'status': lever.get('status'), 'source_record_id': lever.get('source'),
                    'operation': name, 'provider_start_dispatched': False})
            except Exception as exc:
                self.store.put_record('execution_guard', owner, {
                    'guard': 'fis_safety_lever', 'at': iso(), 'allowed': False,
                    'error_code': error_code(exc), 'operation': name,
                    'provider_start_dispatched': False})
                raise Blocked('FIS safety lever could not be verified; no start dispatched') from None
            if not allowed:
                raise Blocked('FIS safety lever is not disengaged; no start dispatched')
        op=self.store.intent(owner,name,request)
        args=dict(params)
        if operation=='start_experiment':
            args['clientToken']=op['token']
            args['tags']={**args.get('tags',{}),'ValidationTrial':owner,'ValidationOperation':op['id']}
        elif operation=='start_automation_execution':
            args['ClientToken']=op['token']
            args['Tags']=[{'Key':'ValidationTrial','Value':owner},{'Key':'ValidationOperation','Value':op['id']}]
        elif operation=='create_backlog_task':
            args['clientToken']=op['token']
        self.store.operation_state(op,'DISPATCHING')
        try:
            response=self.aws.write(side,service,operation,args)
        except Exception as exc:
            code=getattr(exc,'response',{}).get('Error',{}).get('Code','')
            if code in DEFINITIVE_REJECTIONS:
                self.store.operation_state(op,'FAILED',response={'code':code})
                raise Blocked('Provider rejected '+name+': '+code) from None
            self.store.operation_state(op,'UNKNOWN')
            raise UnknownRemoteState(op['id']) from None
        try:
            if operation=='start_experiment': provider_id=response['experiment']['id']
            elif operation=='start_automation_execution': provider_id=response['AutomationExecutionId']
            elif operation=='create_backlog_task': provider_id=response['task']['taskId']
            else: provider_id=params.get('id') or params.get('AutomationExecutionId')
            if not isinstance(provider_id,str) or not provider_id: raise ValueError('Missing provider identity')
        except (KeyError,TypeError,ValueError):
            self.store.operation_state(op,'UNKNOWN')
            raise UnknownRemoteState(op['id']) from None
        return self.store.operation_state(op,'CONFIRMED',provider_id,response)

    def reconcile_automatically(self, op):
        request=op['request']; operation=request['operation']; params=request['parameters']
        if operation=='start_experiment':
            rows,_=self.aws.pages('fault','fis','list_experiments','experiments',experimentTemplateId=params['experimentTemplateId'],maxResults=100)
            candidates=[r['id'] for r in rows if r.get('tags',{}).get('ValidationTrial')==op['owner'] and r.get('tags',{}).get('ValidationOperation')==op['id']]
            if len(candidates)==1:
                self.reconcile(op,candidates[0]); return True
            if len(candidates)>1: raise Blocked('Multiple experiments match one operation intent; emergency review required')
        elif operation=='create_backlog_task':
            from .util import utcnow
            rows,_=self.aws.pages('agent','devops-agent','list_backlog_tasks','tasks',agentSpaceId=params['agentSpaceId'],
                  filter={'taskType':[params['taskType']],'createdAfter':dt(op['created_at']),'createdBefore':utcnow()},
                  limit=100,sortField='CREATED_AT',order='ASC')
            candidates=[r['taskId'] for r in rows if r.get('reference')==params.get('reference') and r.get('title')==params.get('title')]
            if len(candidates)==1:
                self.reconcile(op,candidates[0]); return True
        elif operation=='stop_experiment':
            result=self.aws.experiment(params['id'])
            if result['experiment'].get('state',{}).get('status') in ('stopping','stopped','completed','failed'):
                self.store.operation_state(op,'CONFIRMED',params['id'],result); return True
        elif operation=='stop_automation_execution':
            result=self.aws.automation(params['AutomationExecutionId'])
            if result['execution'].get('AutomationExecutionStatus') in ('Cancelled','Cancelling','Success','Failed','TimedOut'):
                self.store.operation_state(op,'CONFIRMED',params['AutomationExecutionId'],result); return True
        return False

    def reconcile(self, op, provider_id):
        request=op['request']; p=request['parameters']; operation=request['operation']
        if op['state'] not in ('UNKNOWN','DISPATCHING'): raise Blocked('Only an uncertain operation can be reconciled')
        if operation=='start_experiment':
            result=self.aws.experiment(provider_id); value=result['experiment']
            if value.get('experimentTemplateId')!=p['experimentTemplateId'] or value.get('tags',{}).get('ValidationOperation')!=op['id'] or value.get('tags',{}).get('ValidationTrial')!=op['owner']:
                raise Blocked('Experiment does not belong to this operation')
            response={'experiment':value}
        elif operation=='start_automation_execution':
            result=self.aws.automation(provider_id); value=result['execution']
            tags,_=self.aws.call('change','ssm','list_tags_for_resource',ResourceType='Automation',ResourceId=provider_id)
            tagmap={x['Key']:x['Value'] for x in tags.get('TagList',[])}
            name=p['DocumentName'].split(':document/')[-1]
            if value.get('DocumentName') not in (name,p['DocumentName']) or value.get('DocumentVersion')!=p['DocumentVersion'] or value.get('Parameters')!=p['Parameters'] or tagmap.get('ValidationOperation')!=op['id'] or tagmap.get('ValidationTrial')!=op['owner']:
                raise Blocked('Automation does not match the pinned operation')
            response={'AutomationExecutionId':provider_id}
        elif operation=='create_backlog_task':
            value,_=self.aws.task(provider_id,p['taskType'])
            if value.get('reference')!=p.get('reference') or value.get('title')!=p['title'] or dt(value['createdAt'])<dt(op['created_at']):
                raise Blocked('Task does not match the original request')
            response={'task':value}
        elif self.reconcile_automatically(op): return self.store.operation(op['owner'],op['name'])
        else: raise Blocked('No supported reconciliation for this operation')
        return self.store.operation_state(op,'CONFIRMED',provider_id,response)
