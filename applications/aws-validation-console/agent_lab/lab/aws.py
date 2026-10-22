"""AWS instruments, with separately verified observer and execution identities.

No agent journal, API request, or imported experiment can add an SDK operation.
Every write is issued by the worker through a durable operation intent. FIS and
Automation calls use the original persisted idempotency token. Unknown results
require reconciliation; there is no blind automatic retry of an uncertain write.
"""
from __future__ import annotations
import hashlib
import json
import math
import re
from datetime import datetime, timedelta, timezone
from typing import Any
import boto3
from botocore.config import Config
import jmespath
from .models import Binding, Experiment, READS
from .util import Blocked, UnknownRemoteState, normal, iso, dt, canonical, digest, error_code

# Only documented duration-bounded effects. Additional actions require an adapter
# review, not an operator checkbox. Destructive one-shot faults are excluded.
DURATION_ACTIONS = {
    'aws:ec2:stop-instances': 'startInstancesAfterDuration',
    'aws:ec2:api-insufficient-instance-capacity-error': 'duration',
    'aws:ec2:asg-insufficient-instance-capacity-error': 'duration',
    'aws:ec2:ebs-volume-io-latency': 'duration',
    'aws:ebs:pause-volume-io': 'duration',
    'aws:ecs:task-cpu-stress': 'duration',
    'aws:ecs:task-memory-stress': 'duration',
    'aws:ecs:task-network-blackhole-port': 'duration',
    'aws:ecs:task-network-latency': 'duration',
    'aws:ecs:task-network-packet-loss': 'duration',
    'aws:eks:pod-cpu-stress': 'duration',
    'aws:eks:pod-memory-stress': 'duration',
    'aws:eks:pod-network-blackhole-port': 'duration',
    'aws:eks:pod-network-latency': 'duration',
    'aws:eks:pod-network-packet-loss': 'duration',
    'aws:lambda:invocation-add-delay': 'duration',
    'aws:lambda:invocation-error': 'duration',
    'aws:lambda:invocation-http-integration-response': 'duration',
    'aws:fis:inject-api-internal-error': 'duration',
    'aws:fis:inject-api-throttle-error': 'duration',
    'aws:fis:inject-api-unavailable-error': 'duration',
    'aws:network:disrupt-connectivity': 'duration',
}
FIS_TERMINAL={'completed','stopped','failed','cancelled'}
SSM_TERMINAL={'Success','Failed','TimedOut','Cancelled','Rejected','CompletedWithSuccess','CompletedWithFailure'}


def template_contract(template):
    keys=('roleArn','targets','actions','stopConditions','experimentOptions','logConfiguration','experimentReportConfiguration')
    return {k:template.get(k) for k in keys}


def duration_seconds(value):
    match=re.fullmatch(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?',value or '')
    if not match or not any(match.groups()): raise Blocked('Unsupported or missing bounded duration')
    h,m,s=(float(v or 0) for v in match.groups())
    return h*3600+m*60+s


def compare(actual, operation, expected):
    if operation=='eq': return actual == expected and isinstance(actual,bool)==isinstance(expected,bool)
    if operation=='contains': return isinstance(actual,(list,str)) and expected in actual
    if isinstance(actual,bool) or not isinstance(actual,(int,float)) or isinstance(expected,bool) or not isinstance(expected,(int,float)):
        return False
    return actual>=expected if operation=='gte' else actual<=expected


class AWS:
    def __init__(self, binding: Binding, store, owner, *, session_factory=None):
        self.b=binding; self.store=store; self.owner=owner
        self.factory=session_factory or (lambda p:boto3.Session(profile_name=p))
        self.sessions={}; self.clients={}; self.verified={}
        self.read_config=Config(connect_timeout=3,read_timeout=8,retries={'total_max_attempts':2,'mode':'standard'},ignore_configured_endpoint_urls=True)
        self.write_config=Config(connect_timeout=3,read_timeout=10,retries={'total_max_attempts':1,'mode':'standard'},ignore_configured_endpoint_urls=True)

    def side_account(self, side):
        return self.b.agent if side in ('agent','requester') else self.b.workload

    def profile(self, side):
        if side in ('agent','workload'): return getattr(self.b,side).profile
        value=getattr(self.b,{'requester':'requester_profile','fault':'fault_profile','change':'change_profile'}[side])
        if not value: raise Blocked('No explicitly configured '+side+' profile')
        return value

    def client(self, side, service, write=False):
        key=(side,service,write)
        if side not in self.sessions: self.sessions[side]=self.factory(self.profile(side))
        if key not in self.clients:
            self.clients[key]=self.sessions[side].client(service,region_name=self.side_account(side).region,
                                                        config=self.write_config if write else self.read_config)
        return self.clients[key]

    def call(self, side, service, operation, **params):
        allowed={
            'sts':{'get_caller_identity'},
            'devops-agent':{'get_agent_space','get_association','list_backlog_tasks','get_backlog_task','list_executions','list_journal_records','list_recommendations','get_recommendation'},
            'fis':{'get_experiment_template','get_experiment','list_experiments','list_experiment_resolved_targets'},
            'ssm':{'get_document','get_automation_execution','list_tags_for_resource','get_parameter'},
            'cloudwatch':{'describe_alarms','describe_alarm_history','get_metric_data'},
            'logs':{'filter_log_events','describe_log_groups'},
        }
        if operation not in allowed.get(service,set()) | READS.get(service,set()):
            raise Blocked('Read operation not allowlisted')
        at=iso()
        try:
            response=getattr(self.client(side,service),operation)(**params)
            body=normal(response)
            if len(canonical(body).encode())>8_000_000: raise Blocked('AWS response limit exceeded')
            record=self.store.put_record('aws',self.owner,{
                'side':side,'account_id':self.side_account(side).account_id,'region':self.side_account(side).region,
                'service':service,'operation':operation,'parameters':normal({k:v for k,v in params.items() if k not in ('NextToken','nextToken')}),
                'requested_at':at,'received_at':iso(),'request_id':response.get('ResponseMetadata',{}).get('RequestId'),
                'response':body,'response_sha256':digest(body)})
            return body,record['id']
        except Exception as exc:
            self.store.put_record('collection_error',self.owner,{'service':service,'operation':operation,'side':side,'at':at,'code':error_code(exc)})
            raise

    def pages(self, side, service, op, key, token='nextToken', **params):
        rows=[]; refs=[]; seen=set()
        for _ in range(self.b.max_pages):
            response,ref=self.call(side,service,op,**params); refs.append(ref)
            if not isinstance(response.get(key),list): raise Blocked('Unexpected '+op+' response shape')
            rows.extend(response[key])
            if len(rows)>10000 or response.get('Messages'): raise Blocked('Incomplete '+op+' response')
            next_token=response.get(token)
            if not next_token: return rows,refs
            if next_token in seen: raise Blocked('Repeated pagination token')
            seen.add(next_token); params[token]=next_token
        raise Blocked('Pagination limit exceeded')

    def identity(self, side):
        # Recheck for each adapter lifetime; SDK refresh is used, never cached keys.
        if side in self.verified: return self.verified[side]
        value,ref=self.call(side,'sts','get_caller_identity')
        expected=self.side_account(side).account_id
        arn=value.get('Arn','')
        if value.get('Account')!=expected or arn.endswith(':root') or not arn.startswith((f'arn:aws:sts::{expected}:',f'arn:aws:iam::{expected}:')):
            raise Blocked('Unexpected account or root identity: '+side)
        result={'account':expected,'principal':arn,'source':ref}; self.verified[side]=result; return result

    def checks(self, ids):
        self.identity('workload'); results=[]
        for identifier in ids:
            spec=next(c for c in self.b.checks if c.id==identifier)
            body,ref=self.call('workload',spec.service,spec.operation,**spec.parameters)
            if any(body.get(k) for k in ('NextToken','nextToken','Marker','NextMarker')):
                raise Blocked('Verifier response is paginated; narrow the explicit selector')
            if spec.service=='ssm' and body.get('Parameter',{}).get('Type')=='SecureString':
                raise Blocked('SecureString is not an admissible configuration verifier')
            actual=jmespath.search(spec.expression,body)
            results.append({'id':identifier,'passed':actual is not None and compare(actual,spec.operator,spec.expected),
                            'actual':actual,'expected':spec.expected,'operator':spec.operator,'source_record_id':ref})
        self.store.put_record('verification',self.owner,{'checks':results,'all_passed':bool(results) and all(r['passed'] for r in results),'at':iso()})
        return results

    def template(self, fault):
        self.identity('fault')
        value,ref=self.call('fault','fis','get_experiment_template',id=fault.template_id)
        template=value['experimentTemplate']
        if template.get('id')!=fault.template_id or digest(template_contract(template))!=fault.template_sha256:
            raise Blocked('FIS template changed or its pinned digest is incorrect')
        if not template.get('roleArn','').startswith(f'arn:aws:iam::{self.b.workload.account_id}:role/'):
            raise Blocked('FIS execution role outside workload account')
        options=template.get('experimentOptions',{})
        if options.get('accountTargeting','single-account')!='single-account' or options.get('emptyTargetResolutionMode','fail')!='fail':
            raise Blocked('Only single-workload-account experiments with fail-on-empty targets are accepted')
        targets=template.get('targets',{})
        actual_arns=[]
        for name,target in targets.items():
            # First release deliberately rejects random/tag discovery and k8s selector
            # targets. They need their own qualified target resolver, not a blanket claim.
            if not target.get('resourceArns') or target.get('selectionMode')!='ALL' or target.get('resourceTags') or target.get('filters'):
                raise Blocked('This executor requires explicit ARNs and ALL selection; selector-based targets are not qualified')
            if target.get('parameters'):
                raise Blocked('Target parameters require a resource-specific target resolver, which is not qualified in this executor')
            actual_arns.extend(target['resourceArns'])
        if sorted(set(actual_arns))!=sorted(set(fault.target_arns)):
            raise Blocked('FIS template targets differ from the approved exact target set')
        actions=template.get('actions',{})
        if not actions: raise Blocked('Empty FIS template')
        total=0
        for name,action in actions.items():
            action_id=action['actionId']; duration_key=DURATION_ACTIONS.get(action_id)
            if action_id not in fault.allowed_action_ids or not duration_key:
                raise Blocked('Action lacks a reviewed bounded adapter: '+action_id)
            duration=duration_seconds(action.get('parameters',{}).get(duration_key))
            if duration<=0: raise Blocked('Fault duration must be positive')
            total+=duration
            if any(n not in actions for n in action.get('startAfter',[])): raise Blocked('Invalid action dependency')
        def visit(name,path):
            if name in path: raise Blocked('FIS action dependency cycle')
            for parent in actions[name].get('startAfter',[]): visit(parent,path|{name})
        for name in actions: visit(name,set())
        if total>fault.max_fault_seconds: raise Blocked('Conservative sum of action durations exceeds the approved fault budget')
        stops=template.get('stopConditions',[])
        if any(s.get('source')!='aws:cloudwatch:alarm' for s in stops): raise Blocked('No unguarded FIS templates')
        if set(s['value'] for s in stops)!=set(fault.safety_alarm_arns): raise Blocked('Stop alarms differ from the approved set')
        alarm_names=[a.split(':alarm:',1)[1] for a in fault.safety_alarm_arns]
        alarms,_=self.call('workload','cloudwatch','describe_alarms',AlarmNames=alarm_names,AlarmTypes=['MetricAlarm'])
        actual={a['AlarmArn']:a for a in alarms.get('MetricAlarms',[])}
        if set(actual)!=set(fault.safety_alarm_arns) or any(a.get('StateValue')!='OK' for a in actual.values()):
            raise Blocked('Every stop alarm must exist and be OK before exposure')
        return {'contract':template_contract(template),'source':ref,'duration_upper_bound_seconds':total}

    def document(self, book):
        self.identity('change')
        value,ref=self.call('change','ssm','get_document',Name=book.document_arn,DocumentVersion=book.document_version,DocumentFormat='JSON')
        if value.get('DocumentVersion')!=book.document_version or value.get('DocumentType')!='Automation':
            raise Blocked('Unexpected Automation document version/type')
        if hashlib.sha256(value.get('Content','').encode()).hexdigest()!=book.content_sha256:
            raise Blocked('Automation document content hash changed')
        content=json.loads(value['Content']); steps=content.get('mainSteps',[])
        if not steps: raise Blocked('Empty Automation runbook')
        bounded=0
        for step in steps:
            if step.get('action') not in {'aws:executeAwsApi','aws:assertAwsResourceProperty','aws:waitForAwsResourceProperty','aws:sleep'}:
                raise Blocked('This executor accepts only linear AWS API/assert/wait/sleep runbooks, not scripts, nested execution or branches')
            if step.get('nextStep') or step.get('onFailure','Abort') not in {'Abort','Continue'} or step.get('onCancel','Abort')!='Abort':
                raise Blocked('Runbook jumps, loops or custom cancellation branches are not qualified')
            timeout=step.get('timeoutSeconds'); attempts=step.get('maxAttempts',1)
            if not isinstance(timeout,int) or isinstance(timeout,bool) or timeout<=0 or not isinstance(attempts,int) or not 1<=attempts<=3:
                raise Blocked('Every Automation step needs an explicit finite timeout and bounded attempts')
            bounded+=timeout*attempts
        if bounded>book.timeout_seconds: raise Blocked('Automation step budgets exceed the registered timeout')
        return {'document_arn':book.document_arn,'version':book.document_version,'sha256':book.content_sha256,'source':ref}

    def qualify(self, experiment: Experiment):
        identities={side:self.identity(side) for side in ('agent','workload','fault')}
        space,space_ref=self.call('agent','devops-agent','get_agent_space',agentSpaceId=self.b.agent_space_id)
        association,association_ref=self.call('agent','devops-agent','get_association',agentSpaceId=self.b.agent_space_id,associationId=self.b.association_id)
        a=association.get('association',{}); conf=a.get('configuration',{}).get('sourceAws',{})
        if space.get('agentSpace',{}).get('agentSpaceId')!=self.b.agent_space_id or a.get('agentSpaceId')!=self.b.agent_space_id or a.get('associationId')!=self.b.association_id:
            raise Blocked('Agent Space or association identity mismatch')
        if a.get('status')!='valid' or conf.get('accountType')!='source' or conf.get('accountId')!=self.b.workload.account_id or not conf.get('assumableRoleArn','').startswith(f'arn:aws:iam::{self.b.workload.account_id}:role/'):
            raise Blocked('Secondary-account association is not a valid binding to account B')
        fault=next(f for f in self.b.faults if f.id==experiment.fault_id)
        template=self.template(fault)
        checks=self.checks(fault.baseline_checks)
        if not all(c['passed'] for c in checks): raise Blocked('Baseline resource verification failed')
        alarm,_=self.call('workload','cloudwatch','describe_alarms',AlarmNames=[self.b.route.alarm_name],AlarmTypes=['MetricAlarm'])
        rows=alarm.get('MetricAlarms',[])
        if len(rows)!=1 or rows[0].get('StateValue')!='OK' or not rows[0].get('ActionsEnabled'):
            raise Blocked('Incident alarm must exist, be OK and have actions enabled')
        for side,group in [(self.b.route.receipt_account,self.b.route.receipt_log_group),('agent',self.b.route.lifecycle_log_group)]:
            if group:
                logs,_=self.call(side,'logs','describe_log_groups',logGroupNamePrefix=group,limit=50)
                if group not in {x['logGroupName'] for x in logs.get('logGroups',[])}: raise Blocked('Configured event log is not visible')
        books=set(experiment.intervention_runbook_ids)
        if fault.cleanup_runbook_id: books.add(fault.cleanup_runbook_id)
        documents=[]
        for identifier in books:
            book=next(x for x in self.b.runbooks if x.id==identifier)
            documents.append(self.document(book))
            if book.rollback_runbook_id: documents.append(self.document(next(x for x in self.b.runbooks if x.id==book.rollback_runbook_id)))
        return {'identities':identities,'space_source':space_ref,'association_source':association_ref,
                'template':template,'baseline_checks':checks,'documents':documents,'qualified_at':iso(),
                'alarm_arn':rows[0]['AlarmArn'],'binding_sha256':digest(self.b.model_dump(mode='json')),
                'limitations':['Read qualification does not prove fault efficacy, task delivery or all write permissions.',
                               'Native incident correlation requires the configured exact reference contract.',
                               'Delivery without a receipt adapter remains unverified.']}

    def write(self, side, service, operation, params):
        allowed={('fault','fis','start_experiment'),('fault','fis','stop_experiment'),
                 ('change','ssm','start_automation_execution'),('change','ssm','stop_automation_execution'),
                 ('requester','devops-agent','create_backlog_task')}
        if (side,service,operation) not in allowed: raise Blocked('Write operation not allowlisted')
        self.identity(side)
        return normal(getattr(self.client(side,service,True),operation)(**params))

    def experiment(self, experiment_id):
        self.identity('fault')
        body,ref=self.call('fault','fis','get_experiment',id=experiment_id)
        value=body['experiment']
        if value.get('id')!=experiment_id: raise Blocked('FIS experiment identity mismatch')
        targets,refs=self.pages('fault','fis','list_experiment_resolved_targets','resolvedTargets',experimentId=experiment_id,maxResults=100)
        return {'experiment':value,'resolved_targets':targets,'source_record_id':ref,'target_sources':refs}

    def automation(self, execution_id):
        self.identity('change')
        body,ref=self.call('change','ssm','get_automation_execution',AutomationExecutionId=execution_id)
        value=body['AutomationExecution']
        if value.get('AutomationExecutionId')!=execution_id: raise Blocked('Automation identity mismatch')
        return {'execution':value,'source_record_id':ref}

    def task(self, task_id, task_type='INVESTIGATION'):
        self.identity('agent')
        body,ref=self.call('agent','devops-agent','get_backlog_task',agentSpaceId=self.b.agent_space_id,taskId=task_id)
        task=body['task']
        if task.get('taskId')!=task_id or task.get('agentSpaceId')!=self.b.agent_space_id or task.get('taskType')!=task_type:
            raise Blocked('Task type or identity mismatch')
        return task,ref

    def summaries(self, task):
        original=task; seen=set(); task_refs=[]
        while task.get('status')=='LINKED' and task.get('primaryTaskId'):
            if task['taskId'] in seen or len(seen)>=4: raise Blocked('Linked task loop or traversal bound')
            seen.add(task['taskId']); task,ref=self.task(task['primaryTaskId']); task_refs.append(ref)
        executions,refs=self.pages('agent','devops-agent','list_executions','executions',agentSpaceId=self.b.agent_space_id,taskId=task['taskId'],limit=100)
        if len(executions)>20: raise Blocked('Execution limit reached')
        ids={x['executionId'] for x in executions}
        if task.get('executionId'): ids.add(task['executionId'])
        if any(x.get('agentSpaceId')!=self.b.agent_space_id for x in executions): raise Blocked('Execution space mismatch')
        records=[]
        for eid in sorted(ids):
            for typ in ('investigation_summary_md','mitigation_summary_md'):
                rows,_=self.pages('agent','devops-agent','list_journal_records','records',agentSpaceId=self.b.agent_space_id,executionId=eid,recordType=typ,order='ASC',limit=100)
                for row in rows:
                    if row.get('agentSpaceId')!=self.b.agent_space_id or row.get('executionId')!=eid or row.get('recordType')!=typ:
                        raise Blocked('Journal identity mismatch')
                    rec=self.store.put_record('finding',self.owner,row,record_id='finding-'+digest([self.owner,row])[:32])
                    records.append(rec['id'])
        return {'original_task':original,'effective_task':task,'finding_record_ids':sorted(set(records)),'linked_task_sources':task_refs}

    def _logs(self, side, group, start, end):
        if not group: return []
        rows,_=self.pages(side,'logs','filter_log_events','events',logGroupName=group,
                           startTime=int(dt(start).timestamp()*1000),endTime=int(dt(end).timestamp()*1000),limit=1000)
        events=[]; hashes={}
        for row in rows:
            try: event=json.loads(row.get('message',''))
            except (ValueError,TypeError): continue
            key=row.get('eventId')
            if key in hashes and hashes[key]!=digest(event): raise Blocked('Conflicting log event')
            if key in hashes: continue
            hashes[key]=digest(event)
            events.append({'event':event,'log_event_id':key,'ingestion_time':row.get('ingestionTime'),'log_timestamp':row.get('timestamp')})
        return events

    def observe(self, start, end, fault_at=None, assisted_task=None):
        """Return a complete bounded poll or raise; no partial poll is a clean absence."""
        self.identity('agent'); self.identity('workload')
        start,end=dt(start),dt(end)
        result={'at':iso(),'start':iso(start),'end':iso(end),'complete':True,'alarm':None,'receipt':None,'delivery_failure':None,
                'task':None,'findings':[],'candidate_ids':[],'lifecycle':[],'metrics':[]}
        alarms,_=self.pages('workload','cloudwatch','describe_alarm_history','AlarmHistoryItems',token='NextToken',
                             AlarmName=self.b.route.alarm_name,HistoryItemType='StateUpdate',StartDate=start,EndDate=end,MaxRecords=100,ScanBy='TimestampAscending')
        transitions=[]
        for row in alarms:
            if row.get('AlarmName')!=self.b.route.alarm_name: raise Blocked('Alarm history scope mismatch')
            body=json.loads(row['HistoryData'])
            if body.get('newState',{}).get('stateValue')=='ALARM':
                when=dt(row['Timestamp'])
                if start<=when<=end and (not fault_at or when>=dt(fault_at)):
                    transitions.append({'at':iso(when),'alarm_name':self.b.route.alarm_name,'history':row})
        if transitions: result['alarm']=min(transitions,key=lambda a:a['at'])
        alarm_arn=f'arn:aws:cloudwatch:{self.b.workload.region}:{self.b.workload.account_id}:alarm:{self.b.route.alarm_name}'
        receipts=self._logs(self.b.route.receipt_account,self.b.route.receipt_log_group,start,end)
        candidates=[]
        if result['alarm']:
            matching=[]; rejected=[]
            for item in receipts:
                event=item['event']
                if event.get('schema')!='agent-validation.delivery/v1' or event.get('alarm_arn')!=alarm_arn or event.get('agent_space_id')!=self.b.agent_space_id:
                    continue
                if event.get('agent_account_id')!=self.b.agent.account_id or event.get('workload_account_id')!=self.b.workload.account_id:
                    continue
                if not event.get('source_event_id'): continue
                if abs((dt(event['alarm_transition_at'])-dt(result['alarm']['at'])).total_seconds())>1: continue
                if event.get('accepted') is False and event.get('final') is True:
                    attempted=dt(event['attempted_at'])
                    if dt(result['alarm']['at'])<=attempted<=end and event.get('reason_code'):
                        rejected.append(event)
                    continue
                if event.get('accepted') is not True: continue
                delivered=dt(event['accepted_at'])
                if not dt(result['alarm']['at'])<=delivered<=end: continue
                matching.append(event)
            unique={digest(x):x for x in matching}
            if len(unique)>1:
                # Repeated equivalent receipts are fine; different source/reference IDs are not.
                ids={(x.get('source_event_id'),x.get('reference_system'),x.get('reference_id')) for x in unique.values()}
                if len(ids)!=1: raise Blocked('Ambiguous native delivery receipts')
            if unique: result['receipt']=min(unique.values(),key=lambda x:x['accepted_at'])
            elif rejected:
                if len({(x['source_event_id'],x.get('reference_system'),x.get('reference_id')) for x in rejected})!=1:
                    raise Blocked('Ambiguous native delivery failures')
                result['delivery_failure']=max(rejected,key=lambda x:x['attempted_at'])
        tasks,_=self.pages('agent','devops-agent','list_backlog_tasks','tasks',agentSpaceId=self.b.agent_space_id,
                            filter={'taskType':['INVESTIGATION'],'createdAfter':start,'createdBefore':end},limit=100,sortField='CREATED_AT',order='ASC')
        result['alarm_transition_count']=len(transitions)
        result['benign_scope_complete']='{source_event_id}' not in self.b.route.reference_id_format
        result['service_task_ids']=[]
        if result['benign_scope_complete']:
            static_reference=self.b.route.reference_id_format.format(alarm_arn=alarm_arn,alarm_name=self.b.route.alarm_name)
            result['service_task_ids']=sorted({t['taskId'] for t in tasks if t.get('reference',{}).get('system')==self.b.route.reference_system
                and t.get('reference',{}).get('referenceId')==static_reference and t.get('agentSpaceId')==self.b.agent_space_id})
        if assisted_task:
            task,task_ref=self.task(assisted_task); candidates=[task]
        elif result['alarm']:
            source_id=result['receipt'].get('source_event_id','') if result['receipt'] else ''
            if '{source_event_id}' not in self.b.route.reference_id_format or source_id:
                reference=self.b.route.reference_id_format.format(alarm_arn=alarm_arn,alarm_name=self.b.route.alarm_name,source_event_id=source_id)
                for task in tasks:
                    r=task.get('reference',{})
                    if r.get('system')==self.b.route.reference_system and r.get('referenceId')==reference and dt(result['alarm']['at'])<=dt(task['createdAt'])<=end:
                        if task.get('agentSpaceId')!=self.b.agent_space_id or task.get('taskType')!='INVESTIGATION': raise Blocked('Task collection scope mismatch')
                        candidates.append(task)
                if result['receipt'] and (result['receipt'].get('reference_system')!=self.b.route.reference_system or result['receipt'].get('reference_id')!=reference):
                    raise Blocked('Delivery reference contract does not match configured join')
        result['candidate_ids']=sorted({t['taskId'] for t in candidates})
        if len(result['candidate_ids'])>1: result['correlation']='ambiguous'
        elif len(result['candidate_ids'])==1:
            task,task_ref=self.task(result['candidate_ids'][0]); result['task']=task; result['task_source']=task_ref
            detail=self.summaries(task)
            result['findings']=[rid for rid in detail['finding_record_ids'] if dt(task['createdAt'])<=dt(self.store.record(rid)['data']['createdAt'])<=end]
            result['effective_task_id']=detail['effective_task']['taskId']
            ids={task['taskId'],detail['effective_task']['taskId']}
            logs=self._logs('agent',self.b.route.lifecycle_log_group,start,end)
            for row in logs:
                event=row['event']; meta=event.get('detail',{}).get('metadata',{})
                if event.get('source')=='aws.aidevops' and event.get('account')==self.b.agent.account_id and event.get('region')==self.b.agent.region and meta.get('agent_space_id')==self.b.agent_space_id and meta.get('task_id') in ids:
                    if start<=dt(event['time'])<=end: result['lifecycle'].append(event)
            result['correlation']='exact_reference' if not assisted_task else 'assisted'
        else: result['correlation']='none'
        for metric in self.b.metrics:
            period=metric.period_seconds
            left=math.ceil(start.timestamp()/period)*period
            right=math.floor(end.timestamp()/period)*period
            if right<=left: continue
            query={'Id':'m1','MetricStat':{'Metric':{'Namespace':metric.namespace,'MetricName':metric.metric_name,
                        'Dimensions':[{'Name':k,'Value':v} for k,v in sorted(metric.dimensions.items())]},'Period':period,'Stat':metric.statistic,'Unit':metric.unit},'ReturnData':True}
            chunks,_=self.pages('workload','cloudwatch','get_metric_data','MetricDataResults',token='NextToken',
                    MetricDataQueries=[query],StartTime=datetime.fromtimestamp(left,timezone.utc),EndTime=datetime.fromtimestamp(right,timezone.utc),ScanBy='TimestampAscending',MaxDatapoints=10000)
            values={}; complete=bool(chunks)
            for chunk in chunks:
                complete=complete and chunk.get('Id')=='m1' and chunk.get('StatusCode')=='Complete' and not chunk.get('Messages')
                if len(chunk.get('Timestamps',[]))!=len(chunk.get('Values',[])): complete=False
                for when,value in zip(chunk.get('Timestamps',[]),chunk.get('Values',[])):
                    stamp=dt(when).timestamp()
                    if not left<=stamp<right or stamp%period or isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value): complete=False; continue
                    if stamp in values and values[stamp]!=value: complete=False
                    values[stamp]=value
            points=[{'at':iso(datetime.fromtimestamp(t,timezone.utc)),'value':values.get(t)} for t in range(left,right,period)]
            result['metrics'].append({'id':metric.id,'title':metric.title,'unit':metric.unit,'query':query,'complete':complete,
                                       'period_seconds':period,'points':points,'missing':sum(p['value'] is None for p in points)})
        return result

    def recommendations(self, task_id):
        task,task_ref=self.task(task_id,'EVALUATION')
        rows,refs=self.pages('agent','devops-agent','list_recommendations','recommendations',agentSpaceId=self.b.agent_space_id,taskId=task_id,limit=100)
        result=[]
        for row in rows:
            rec,ref=self.call('agent','devops-agent','get_recommendation',agentSpaceId=self.b.agent_space_id,
                              recommendationId=row['recommendationId'],recommendationVersion=row['version'])
            item=rec['recommendation']
            expected=f'arn:aws:aidevops:{self.b.agent.region}:{self.b.agent.account_id}:agentspace/{self.b.agent_space_id}'
            if item.get('agentSpaceArn')!=expected or item.get('taskId')!=task_id or item.get('recommendationId')!=row['recommendationId'] or item.get('version')!=row['version']:
                raise Blocked('Recommendation lineage/version mismatch')
            record=self.store.put_record('recommendation',self.owner,{'recommendation':item,'source_record_id':ref},
                                          record_id='recommendation-'+digest([self.owner,item])[:32])
            result.append(record['id'])
        return {'task':task,'task_source':task_ref,'recommendation_record_ids':result,'complete':True,'at':iso()}
