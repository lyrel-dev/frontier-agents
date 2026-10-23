"""Execute AWS-owned definitions, including selectors and multi-account targets.

A preview is a real skip-all FIS operation, never a permissions test or a target
lock. Approval covers the captured definition plus an explicitly selected target
policy. AWS execution-role restrictions remain the preventive blast-radius boundary.
"""
from __future__ import annotations
from types import SimpleNamespace
from datetime import timedelta
import boto3
from botocore.config import Config
from .aws import template_contract, FIS_TERMINAL
from .broker import Broker
from .util import Blocked, UnknownRemoteState, digest, iso, dt, normal, utcnow, error_code


def account_contract(rows):
    return sorted([{'accountId':r['accountId'],'roleArn':r['roleArn']} for r in rows], key=lambda r:r['accountId'])


def target_key(row):
    info=row.get('targetInformation') or {}
    if not isinstance(info,dict) or not info or not row.get('resourceType') or not row.get('targetName'):
        raise Blocked('Resolved target lacks type, name or identity information')
    return {'targetName':row['targetName'],'resourceType':row['resourceType'],
            'targetInformation':dict(sorted(info.items()))}


def target_identity(row):
    r=target_key(row)
    return r['targetInformation'].get('arn') or 'fis-resource:'+digest(r)


def target_match(fault, rows, *, complete=False):
    actual={digest(target_key(r)) for r in rows}
    approved={digest(target_key(r)) for r in fault.resolved_targets}
    if not actual <= approved:
        raise Blocked('FIS resolved a resource outside the approved preview envelope; stop and review')
    if complete and len(actual)<fault.minimum_targets:
        raise Blocked('FIS resolved fewer targets than the approved minimum')
    names={r['targetName'] for r in rows}
    required={r['targetName'] for r in fault.resolved_targets}
    enough=len(actual)>=fault.minimum_targets and names==required
    return enough and (actual==approved if fault.target_match=='exact' else True)


class PreviewAWS:
    """Minimal real-SDK adapter for an approved skip-all operation."""
    def __init__(self, account, region, store, owner, *, factory=boto3.Session):
        self.account,self.region,self.store,self.owner=account,region,store,owner
        self.b=SimpleNamespace(workload=SimpleNamespace(account_id=account.account_id,region=region),orchestrator=None)
        self.session=factory(profile_name=account.execution_profile or account.profile)
        self.clients={};self.verified=False
    def side_account(self, side): return self.b.workload
    def client(self,side,service,write=False):
        key=(service,write)
        if key not in self.clients:
            self.clients[key]=self.session.client(service,region_name=self.region,config=Config(
                connect_timeout=3,read_timeout=8,retries={'total_max_attempts':1 if write else 2},ignore_configured_endpoint_urls=True))
        return self.clients[key]
    def call(self,side,service,operation,**params):
        raw=getattr(self.client(side,service),operation)(**params);body=normal(raw)
        record=self.store.put_record('aws',self.owner,{'side':'fault','account_id':self.account.account_id,
          'region':self.region,'service':service,'operation':operation,'parameters':{k:v for k,v in params.items() if k!='nextToken'},
          'received_at':iso(),'request_id':raw.get('ResponseMetadata',{}).get('RequestId'),
          'response':body,'response_sha256':digest(body)})
        return body,record['id']
    def identity(self,side):
        if not self.verified:
            r,_=self.call(side,'sts','get_caller_identity')
            if r.get('Account')!=self.account.account_id or not r.get('Arn','').startswith((f'arn:aws:iam::{self.account.account_id}:',f'arn:aws:sts::{self.account.account_id}:')) or r.get('Arn','').endswith(':root'):
                raise Blocked('Unexpected or root preview execution identity')
            self.verified=True
        return {'account':self.account.account_id}
    def pages(self,side,service,op,key,**params):
        rows=[];refs=[];seen=set()
        for _ in range(100):
            r,ref=self.call(side,service,op,**params);refs.append(ref)
            if not isinstance(r.get(key),list): raise Blocked('Malformed paginated response')
            rows.extend(r[key])
            if len(rows)>10000: raise Blocked('Target preview exceeds the capture budget')
            token=r.get('nextToken')
            if not token:return rows,refs
            if token in seen:raise Blocked('Repeated pagination token')
            seen.add(token);params['nextToken']=token
        raise Blocked('Preview collection incomplete')
    def write(self,side,service,op,params):
        if side!='fault' or service!='fis' or op not in {'start_experiment','stop_experiment'}:
            raise Blocked('Preview adapter permits only owned FIS preview lifecycle')
        if op=='start_experiment' and params.get('experimentOptions',{}).get('actionsMode')!='skip-all':
            raise Blocked('Preview cannot inject faults')
        return normal(getattr(self.client(side,service,True),op)(**params))
    def experiment(self,identifier):
        value,ref=self.call('fault','fis','get_experiment',id=identifier)
        if value['experiment'].get('id')!=identifier:raise Blocked('Preview identity mismatch')
        rows,refs=self.pages('fault','fis','list_experiment_resolved_targets','resolvedTargets',experimentId=identifier,maxResults=100)
        account_rows=[];account_refs=[]
        if value['experiment'].get('experimentOptions',{}).get('accountTargeting')=='multi-account':
            account_rows,account_refs=self.pages('fault','fis','list_experiment_target_account_configurations','targetAccountConfigurations',experimentId=identifier)
        return {'experiment':value['experiment'],'resolved_targets':rows,'source_record_id':ref,'target_sources':refs,
                'target_accounts':account_rows,'account_sources':account_refs}


def native_template(aws,fault):
    """Re-read the definition, account-role map, action availability and stop alarms."""
    aws.identity('fault')
    body,ref=aws.call('fault','fis','get_experiment_template',id=fault.template_id)
    t=body['experimentTemplate']
    if t.get('id')!=fault.template_id or digest(template_contract(t))!=fault.template_sha256:
        raise Blocked('FIS definition changed; repeat preview and approval')
    orchestrator=aws.side_account('fault')
    if not t.get('roleArn','').startswith(f'arn:aws:iam::{orchestrator.account_id}:role/'):
        raise Blocked('Unexpected orchestrator execution role')
    options=t.get('experimentOptions') or {}
    accounts=[]
    if options.get('accountTargeting','single-account')=='multi-account':
        accounts,_=aws.pages('fault','fis','list_target_account_configurations','targetAccountConfigurations',experimentTemplateId=fault.template_id,maxResults=100)
        actual={a['accountId'] for a in accounts}
        expected={aws.b.workload.account_id,*[a.account_id for a in aws.b.target_accounts]}
        if actual!=expected:raise Blocked('Every FIS target account needs a verified observer and Agent Space association')
        if any(not a.get('roleArn','').startswith(f"arn:aws:iam::{a['accountId']}:role/") for a in accounts):
            raise Blocked('Invalid target execution-role account')
    elif orchestrator.account_id!=aws.b.workload.account_id or aws.b.target_accounts:
        raise Blocked('Single-account template does not match the target observer scope')
    if digest(account_contract(accounts))!=fault.target_accounts_sha256:
        raise Blocked('Target account role configuration changed')
    preview=aws.store.record(fault.preview_record_id)
    p=preview['data']
    if (preview['kind']!='fis_preview_result' or p.get('template_sha256')!=fault.template_sha256
            or p.get('account_id')!=orchestrator.account_id or p.get('region')!=orchestrator.region
            or p.get('target_accounts_sha256')!=fault.target_accounts_sha256
            or digest(p.get('targets'))!=digest(fault.resolved_targets)):
        raise Blocked('Preview provenance does not match the execution contract')
    actions=t.get('actions') or {}
    if not actions or set(fault.allowed_action_ids)!={a['actionId'] for a in actions.values()}:
        raise Blocked('Reviewed action set does not match the template')
    for action_id in set(fault.allowed_action_ids):
        definition,_=aws.call('fault','fis','get_action',id=action_id)
        if definition.get('action',{}).get('id')!=action_id:raise Blocked('Action is not available in the selected Region')
    stops=t.get('stopConditions') or []
    if not stops or any(s.get('source')!='aws:cloudwatch:alarm' for s in stops):
        raise Blocked('Every native experiment needs CloudWatch stop conditions')
    if {s['value'] for s in stops}!=set(fault.safety_alarm_arns):raise Blocked('Stop alarm set changed')
    alarms,_=aws.call('fault','cloudwatch','describe_alarms',AlarmNames=[s.split(':alarm:',1)[1] for s in fault.safety_alarm_arns])
    found={a['AlarmArn']:a for a in alarms.get('MetricAlarms',[])+alarms.get('CompositeAlarms',[])}
    if set(found)!=set(fault.safety_alarm_arns) or any(a.get('StateValue')!='OK' for a in found.values()):
        raise Blocked('All stop alarms must exist and be OK')
    return {'contract':template_contract(t),'source':ref,'target_accounts':account_contract(accounts),
        'duration_upper_bound_seconds':fault.max_fault_seconds,'duration_basis':'operator-approved stop deadline, not a guarantee of fault reversal',
        'preview_record_id':preview['id'],'target_policy':fault.target_match,
        'limitations':['Preview is not a target lock or an action-permission test.',
          'Runtime target verification is detective; restrictive FIS execution roles are the preventive boundary.',
          'Stopping FIS does not undo completed actions. Independent recovery must remain operable.']}


class Previews:
    def __init__(self,config,store,*,factory=PreviewAWS,clock=utcnow):
        self.config,self.store,self.factory,self.clock=config,store,factory,clock
    def subject(self,record_id):
        row=self.store.record(record_id)
        if row['kind']!='fis_template' or not row['data'].get('complete'):raise Blocked('Choose a completely read template')
        d=row['data']
        account=next((a for a in self.config.fis_accounts if a.account_id==d['account_id'] and d['region'] in a.regions),None)
        if not account:raise Blocked('Configure this account and Region first')
        data={'template_record_id':row['id'],'template_sha256':d['contract_sha256'],
          'account_id':d['account_id'],'region':d['region'],'account_configuration_sha256':digest(account.model_dump(mode='json')),
          'actions_mode':'skip-all','target_accounts_sha256':digest(account_contract(d.get('target_accounts',[])))}
        return {'subject':data,'digest':digest(data),'confirmation':f"PREVIEW {d['account_id']} {d['template_id']}"}
    def request(self,record_id,approval):
        sub=self.subject(record_id)
        if approval.expected_digest!=sub['digest'] or approval.confirmation!=sub['confirmation']:
            raise Blocked('Exact preview approval does not match')
        if not self.config.enable_aws_writes:raise Blocked('AWS writes are disabled; preview starts an AWS skip-all experiment')
        if any(e['state'] in {'BASELINING','EXPOSING','OBSERVING','ABORTING','CLEANING','RESTORE_REQUIRED','UNKNOWN_REMOTE_STATE'} for e in self.store.entities('trial')):
            raise Blocked('Wait for the active exposure/restoration before preview')
        return self.store.create('fis_preview','QUEUED',{**sub,'approved_by':approval.approver,
          'approved_at':iso(self.clock()),'expires_at':iso(self.clock()+timedelta(seconds=self.config.approval_ttl_seconds))})
    def step(self):
        for job in reversed(self.store.entities('fis_preview')):
            if job['state'] not in {'QUEUED','RUNNING','STOPPING','UNKNOWN_REMOTE_STATE'}:continue
            try:self.advance(job)
            except UnknownRemoteState as exc:
                self.store.update(job['id'],state='UNKNOWN_REMOTE_STATE',changes={'unknown_operation_id':str(exc)})
            except Exception as exc:
                # A known remote preview must be stopped/reconciled before terminal closure.
                latest=self.store.entity(job['id'])
                intent=self.store.operation(job['id'],'target-preview')
                if intent and intent['state']=='PENDING':
                    self.store.operation_state(intent,'FAILED',response={'code':'LocalPreviewBlockedBeforeDispatch'})
                provider_id=latest['data'].get('provider_id') or (intent or {}).get('provider_id')
                if intent and intent['state'] in {'DISPATCHING','UNKNOWN'}:
                    state='UNKNOWN_REMOTE_STATE'
                else:
                    state='STOPPING' if provider_id and not latest['data'].get('remote_terminal') else 'BLOCKED'
                self.store.update(job['id'],state=state,changes={'reason':str(exc) if isinstance(exc,Blocked) else error_code(exc),
                                  **({'provider_id':provider_id,
                                      'started_at':latest['data'].get('started_at') or (intent or {}).get('created_at'),
                                      'started_at_basis':latest['data'].get('started_at_basis','operation intent when attachment is missing')} if provider_id else {})})
            return
    def advance(self,job):
        job=self.store.entity(job['id'])
        if job['state'] in {'COMPLETE','BLOCKED'}:return
        d=job['data'];sub=d['subject'];row=self.store.record(sub['template_record_id'])['data']
        account=next(a for a in self.config.fis_accounts if a.account_id==sub['account_id'] and sub['region'] in a.regions)
        if digest(account.model_dump(mode='json'))!=sub['account_configuration_sha256']:raise Blocked('Account profile changed since preview approval')
        aws=self.factory(account,sub['region'],self.store,job['id']);aws.identity('fault')
        op=self.store.operation(job['id'],'target-preview')
        recovering=bool(op and op['state'] in {'CONFIRMED','DISPATCHING','UNKNOWN'})
        broker=Broker(self.store,aws,self.config.enable_aws_writes or recovering)
        if d.get('abort_requested') and (not op or op['state']=='PENDING'):
            if op:self.store.operation_state(op,'FAILED',response={'code':'CancelledBeforeDispatch'})
            self.store.update(job['id'],state='BLOCKED',changes={'reason':'Cancelled before preview dispatch'})
            return
        if not op or op['state']=='PENDING':
            if dt(d['expires_at'])<=self.clock():raise Blocked('Preview approval expired')
            current,_=aws.call('fault','fis','get_experiment_template',id=row['template_id'])
            if digest(template_contract(current['experimentTemplate']))!=sub['template_sha256']:raise Blocked('Template changed before preview')
        from .preview_control import reserve_dispatch
        op=broker.execute(job['id'],'target-preview','fault','fis','start_experiment',{
            'experimentTemplateId':row['template_id'],'experimentOptions':{'actionsMode':'skip-all'}},
            reserve_dispatch=lambda intent:reserve_dispatch(self.store,intent,self.clock))
        if not d.get('provider_id'):
            self.store.update(job['id'],state='RUNNING',changes={'provider_id':op['provider_id'],'started_at':iso(self.clock()),'started_at_basis':'provider identity attached locally'})
            d=self.store.entity(job['id'])['data']
        result=aws.experiment(op['provider_id']);value=result['experiment'];status=value.get('state',{}).get('status')
        unexpected_mode=value.get('experimentOptions',{}).get('actionsMode')!='skip-all'
        timeout=(self.clock()-dt(d.get('started_at') or op['created_at'])).total_seconds()>180
        if status not in FIS_TERMINAL:
            if timeout or job['state']=='STOPPING' or d.get('abort_requested') or unexpected_mode:
                Broker(self.store,aws,True).execute(job['id'],'stop-preview','fault','fis','stop_experiment',{'id':op['provider_id']})
                self.store.update(job['id'],state='STOPPING')
            if unexpected_mode:raise Blocked('AWS preview actions mode mismatch; owned stop requested')
            return
        self.store.update(job['id'],changes={'remote_terminal':True,'remote_state':status})
        if unexpected_mode:raise Blocked('AWS preview actions mode mismatch')
        if status!='completed' or d.get('abort_requested') or job['state']=='STOPPING':
            self.store.update(job['id'],state='BLOCKED',changes={'reason':'Preview did not complete successfully','remote_state':status});return
        if any(a.get('state',{}).get('status')!='skipped' for a in value.get('actions',{}).values()):
            raise Blocked('Completed preview contains a non-skipped action')
        configs=result.get('target_accounts',[])
        from .execution_contract import verify_execution
        verify_execution(row['template'],value,'skip-all')
        actual=digest(account_contract(configs))
        if actual!=sub['target_accounts_sha256']:raise Blocked('Target account configuration changed during preview')
        targets=sorted([target_key(r) for r in result['resolved_targets']],key=digest)
        if not targets:raise Blocked('Preview resolved no targets; no exposure can be approved')
        from .preview_control import complete
        complete(self.store,job['id'],{**sub,'template_id':row['template_id'],
            'provider_id':op['provider_id'],'captured_at':iso(self.clock()),'targets':targets,
            'target_accounts':account_contract(configs),'input_hashes':{r['id']:r['sha256'] for r in self.store.records(job['id'])},
            'limits':['Approximate target selection only; no fault was injected and no action permission was verified.']},self.clock)
