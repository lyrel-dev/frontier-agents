"""Local, versioned onboarding. Credential material never enters these contracts.

The bootstrap file is only the initial configuration. Subsequent revisions live
in SQLite, are activated with the approval credential, and are adopted by API and
worker processes. In-flight work retains its own immutable binding snapshot.
"""
from __future__ import annotations
import json
from datetime import timedelta
from typing import Any
import boto3
from botocore.config import Config
from pydantic import Field
from .models import Strict, Configuration, FISAccount, Binding, Experiment, Probe, ReadCheck, Metric, Route, Oracle, BusinessRequirement, Approval, Account, TargetAccount, Runbook
from .util import Blocked, digest, iso, normal, error_code, canonical

BUSY={'RUNNING','CANCELLING','QUALIFYING','READY','BASELINING','EXPOSING','OBSERVING','ABORTING','CLEANING',
      'SETTLING','FINALIZING','UNKNOWN_REMOTE_STATE','RESTORE_REQUIRED','QUEUED','SCANNING','APPROVED',
      'ROLLBACK_APPROVED','ROLLING_BACK','EVALUATION_APPROVED','EVALUATING','STOPPING'}


def refresh(config,store):
    current=store.meta('active_configuration')
    if current and getattr(config,'_workspace_revision',None)!=current['record_id']:
        saved=store.record(current['record_id'])
        candidate=Configuration.model_validate(saved['data']['configuration'])
        for name in Configuration.model_fields:
            setattr(config,name,getattr(candidate,name))
        config._workspace_revision=current['record_id']
    return config


class AccountDraft(Strict):
    account: FISAccount
    base_digest: str


class ConfigDraft(Strict):
    configuration: Configuration
    base_digest: str
    rationale: str = Field(min_length=10,max_length=3000)


class Compose(Strict):
    template_record_id: str
    preview_record_id: str
    binding_id: str = Field(pattern=r'^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$')
    name: str = Field(min_length=1,max_length=150)
    agent_connection_id: str
    agent_region: str
    agent_space_id: str
    workload_connection_id: str
    association_id: str
    additional_targets: dict[str,str] = Field(default_factory=dict)  # connection ID -> association ID
    service_id: str
    deployment_model: str
    target_match: str = 'exact'
    minimum_targets: int = Field(default=1,ge=1,le=1000)
    maximum_fault_seconds: int = Field(default=300,ge=1,le=86400)
    independent_recovery: str = Field(min_length=20,max_length=6000)
    action_review: str = Field(min_length=20,max_length=6000)
    safety_review: str = Field(min_length=20,max_length=4000)
    probe: Probe
    checks: list[ReadCheck] = Field(min_length=3,max_length=100)
    baseline_check_ids: list[str] = Field(min_length=1)
    fault_check_ids: list[str] = Field(min_length=1)
    cleanup_check_ids: list[str] = Field(min_length=1)
    metrics: list[Metric] = Field(default_factory=list,max_length=20)
    route: Route
    oracle: Oracle
    business_requirements: list[BusinessRequirement] = Field(default_factory=list,max_length=30)
    runbooks: list[Runbook] = Field(default_factory=list,max_length=30)
    cleanup_runbook_id: str | None = None
    requester_profile: str | None = None
    change_profile: str | None = None
    experiment_id: str
    revision: int = Field(default=1,ge=1)
    hypotheses: str = Field(min_length=20,max_length=5000)
    baseline_seconds: int = Field(default=60,ge=30,le=600)
    observation_seconds: int = Field(default=600,ge=60,le=172800)
    response_deadline_seconds: int = Field(default=300,ge=10,le=1800)
    ingestion_wait_seconds: int = Field(default=120,ge=0,le=600)
    max_error_ratio: float = Field(default=.01,ge=0,lt=1)
    max_latency_ms: float = Field(default=1000,gt=0,le=120000)
    stable_seconds: int = Field(default=30,ge=10,le=300)
    bucket_seconds: int = Field(default=10,ge=5,le=60)


class Setup:
    def __init__(self,config,store,*,session_factory=None):
        self.config,self.store=config,store
        self.factory=session_factory or (lambda profile=None:boto3.Session(profile_name=profile))
        self.sdk=Config(connect_timeout=3,read_timeout=8,retries={'total_max_attempts':2},ignore_configured_endpoint_urls=True)
    def current(self):
        refresh(self.config,self.store)
        data=self.config.model_dump(mode='json')
        return {'configuration':data,'digest':digest(data),'revision':self.store.meta('active_configuration'),
          'profiles':sorted(self.factory().available_profiles),
          'credential_boundary':'Only installed SDK profile names; no key, token, path or endpoint input.',
          'blocking_work':[{'id':e['id'],'kind':e['kind'],'state':e['state']} for e in self.store.entities() if e['state'] in BUSY]}
    def _profiles(self,candidate):
        installed=set(self.factory().available_profiles)
        names={a.profile for a in candidate.fis_accounts}|{a.execution_profile for a in candidate.fis_accounts if a.execution_profile}
        for b in candidate.bindings:
            names|={b.agent.profile,b.workload.profile}
            names|={x for x in [b.fault_profile,b.change_profile,b.requester_profile] if x}
            names|={a.profile for a in b.target_accounts}
            if b.orchestrator:names.add(b.orchestrator.profile)
        if not names<=installed:raise Blocked('Install these SDK profiles on the host first: '+', '.join(sorted(names-installed)))
    def draft(self,request:ConfigDraft):
        refresh(self.config,self.store)
        if request.base_digest!=digest(self.config.model_dump(mode='json')):raise Blocked('Configuration changed; reload before editing')
        self._profiles(request.configuration)
        return self.store.put_record('configuration_draft','setup',request.model_dump(mode='json'))
    def account_draft(self,request:AccountDraft):
        data=self.config.model_dump(mode='json')
        data['fis_accounts']=[a for a in data['fis_accounts'] if a['id']!=request.account.id]+[request.account.model_dump(mode='json')]
        return self.draft(ConfigDraft(configuration=Configuration.model_validate(data),base_digest=request.base_digest,rationale='Console account onboarding/edit; no AWS mutation.'))
    def subject(self,record_id):
        r=self.store.record(record_id)
        if r['kind'] not in {'configuration_draft','guided_plan'}:raise Blocked('Not a configuration proposal')
        return {'digest':r['sha256'],'confirmation':'CONFIGURE '+r['id'],
          'accounts':[{'id':a['id'],'account_id':a['account_id'],'regions':a['regions']} for a in r['data']['configuration']['fis_accounts']],
          'aws_writes_enabled':r['data']['configuration']['enable_aws_writes'],
          'definition':r['data']}
    def commit(self,record_id,approval):
        row=self.store.record(record_id);sub=self.subject(record_id)
        if approval.expected_digest!=sub['digest'] or approval.confirmation!=sub['confirmation']:raise Blocked('Configuration approval does not match')
        candidate=Configuration.model_validate(row['data']['configuration']);self._profiles(candidate)
        # BEGIN IMMEDIATE serializes against worker reservations and other setup clients.
        with self.store.transaction() as db:
            current=db.execute("SELECT data FROM metadata WHERE key='active_configuration'").fetchone()
            active=self.store.record(json.loads(current['data'])['record_id'])['data']['configuration'] if current else self.config.model_dump(mode='json')
            if digest(active)!=row['data']['base_digest']:raise Blocked('Proposal is stale; review a new revision')
            if any(e['state'] in BUSY for e in db.execute('SELECT kind,state FROM entities')):
                raise Blocked('Pause/finish active work and resolve restoration before changing configuration')
            if db.execute("SELECT 1 FROM operations WHERE state IN ('PENDING','DISPATCHING','UNKNOWN') LIMIT 1").fetchone():
                raise Blocked('Resolve pending or uncertain provider operations before changing configuration')
            record={'configuration':candidate.model_dump(mode='json'),'proposal_id':record_id,
              'previous_sha256':digest(active),'approved_at':iso(),'approver':approval.approver,'rationale':approval.rationale}
            rid='configuration-'+digest(record)
            db.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',(rid,'configuration','setup',iso(),digest(record),canonical(record)))
            db.execute("INSERT INTO metadata VALUES('active_configuration',?) ON CONFLICT(key) DO UPDATE SET data=excluded.data",(canonical({'record_id':rid}),))
            # Guided contract registration is part of the same local transaction.
            if row['kind']=='guided_plan':
                exp=Experiment.model_validate(row['data']['experiment']);ed=exp.model_dump(mode='json');eid=f'experiment:{exp.id}@{exp.revision}'
                old=db.execute('SELECT sha256 FROM records WHERE id=?',(eid,)).fetchone()
                if old and old['sha256']!=digest(ed):raise Blocked('Experiment revision conflict; increment the revision')
                if not old:db.execute('INSERT INTO records VALUES(?,?,?,?,?,?)',(eid,'experiment','workspace',iso(),digest(ed),canonical(ed)))
        refresh(self.config,self.store)
        return {'record_id':rid,'configuration_digest':digest(candidate.model_dump(mode='json')),'aws_operations':0}
    def _account(self,identifier,config=None):
        a=next((a for a in (config or self.config).fis_accounts if a.id==identifier),None)
        if not a:raise Blocked('Unknown configured account')
        return a
    def _capture(self,owner,account,region,service,op,params,response):
        body=normal(response)
        return self.store.put_record('setup_source',owner,{'account_id':account.account_id,'region':region,'service':service,'operation':op,
          'parameters':{k:v for k,v in params.items() if k!='nextToken'},'at':iso(),'request_id':response.get('ResponseMetadata',{}).get('RequestId'),
          'response':body,'response_sha256':digest(body)})
    def verify_account(self,identifier,region,*,draft_id=None):
        refresh(self.config,self.store)
        config=self.config
        if draft_id:config=Configuration.model_validate(self.store.record(draft_id)['data']['configuration'])
        account=self._account(identifier,config)
        if region not in account.regions:raise Blocked('Region is not in this account scope')
        owner='account-check-'+digest([identifier,iso()])[:20];checks=[]
        session=self.factory(account.profile)
        try:
            value=session.client('sts',region_name=region,config=self.sdk).get_caller_identity()
            self._capture(owner,account,region,'sts','get_caller_identity',{},value)
            if value.get('Account')!=account.account_id or value.get('Arn','').endswith(':root'):raise Blocked('Account mismatch or root identity; no service reads performed')
            checks.append({'operation':'sts:GetCallerIdentity','status':'pass','principal':value['Arn']})
        except Exception as exc:
            checks.append({'operation':'sts:GetCallerIdentity','status':'blocked','code':error_code(exc),'guidance':'Verify expected account and SDK profile; refresh SSO credentials locally.'})
            return self.store.put_record('account_check',owner,{'checks':checks,'status':'blocked','mutation_permission_verified':False})
        for service,op,params in [('fis','list_experiment_templates',{'maxResults':1}),('devops-agent','list_agent_spaces',{'maxResults':1})]:
            try:
                value=getattr(session.client(service,region_name=region,config=self.sdk),op)(**params)
                self._capture(owner,account,region,service,op,params,value)
                checks.append({'operation':('aidevops:ListAgentSpaces' if service=='devops-agent' else 'fis:ListExperimentTemplates'),'status':'pass'})
            except Exception as exc:
                checks.append({'operation':('aidevops:ListAgentSpaces' if service=='devops-agent' else 'fis:ListExperimentTemplates'),'status':'blocked','code':error_code(exc),
                  'guidance':'Verify Region availability and the listed read action in the observer policy; this does not test execution permissions.'})
        return self.store.put_record('account_check',owner,{'checks':checks,'status':'pass' if all(x['status']=='pass' for x in checks) else 'partial',
          'mutation_permission_verified':False,'at':iso()})
    def agents(self,identifier,region):
        account=self._account(identifier)
        if region not in account.regions:raise Blocked('Unconfigured Region')
        session=self.factory(account.profile);owner='agents-'+digest([identifier,iso()])[:20]
        def call(service,op,**params):
            response=getattr(session.client(service,region_name=region,config=self.sdk),op)(**params)
            self._capture(owner,account,region,service,op,params,response);return normal(response)
        identity=call('sts','get_caller_identity')
        if identity.get('Account')!=account.account_id or identity.get('Arn','').endswith(':root'):raise Blocked('Unexpected agent observer identity')
        def pages(op,key,**params):
            rows=[];seen=set()
            for _ in range(100):
                body=call('devops-agent',op,**params);rows.extend(body.get(key,[]));token=body.get('nextToken')
                if not token:return rows
                if token in seen:raise Blocked('Repeated Agent Space pagination token')
                seen.add(token);params['nextToken']=token
            raise Blocked('Agent Space enumeration incomplete')
        spaces=pages('list_agent_spaces','agentSpaces',maxResults=100)
        for space in spaces:
            associations=pages('list_associations','associations',agentSpaceId=space['agentSpaceId'],maxResults=100)
            # Expose no arbitrary external integration secrets from the API response.
            space['associations']=[{'association_id':a['associationId'],'status':a.get('status'),
              'account_id':a.get('configuration',{}).get('sourceAws',{}).get('accountId'),
              'account_type':a.get('configuration',{}).get('sourceAws',{}).get('accountType')}
              for a in associations if a.get('configuration',{}).get('sourceAws')]
            for k in list(space):
                if k not in {'agentSpaceId','name','description','associations'}:space.pop(k)
        return {'agents':spaces,'complete':True,'owner':owner}
    def compose(self,r:Compose):
        from .native_fis import target_identity
        row=self.store.record(r.template_record_id);preview=self.store.record(r.preview_record_id)
        if row['kind']!='fis_template' or preview['kind']!='fis_preview_result':raise Blocked('Template and completed preview required')
        d=row['data'];p=preview['data']
        if p['template_record_id']!=row['id'] or p['template_sha256']!=d['contract_sha256']:raise Blocked('Preview belongs to another definition revision')
        origin=next((a for a in self.config.fis_accounts if a.account_id==d['account_id'] and d['region'] in a.regions),None)
        agent=self._account(r.agent_connection_id);work=self._account(r.workload_connection_id)
        if not origin or not origin.execution_profile:raise Blocked('Select an installed executor profile on the template-owner connection')
        if r.agent_region not in agent.regions or d['region'] not in work.regions:raise Blocked('Agent/workload Region not configured')
        extra=[]
        for cid,assoc in r.additional_targets.items():
            a=self._account(cid)
            if d['region'] not in a.regions:raise Blocked('Target account Region not configured')
            extra.append({'account_id':a.account_id,'region':d['region'],'profile':a.profile,'association_id':assoc})
        if p['target_accounts']:
            if {a['accountId'] for a in p['target_accounts']}!={work.account_id,*[a['account_id'] for a in extra]}:
                raise Blocked('Select observers and associations for every target account in the preview')
        targets=[target_identity(x) for x in p['targets']]
        t=d['template'];stop=[s['value'] for s in t.get('stopConditions',[]) if s.get('source')=='aws:cloudwatch:alarm']
        if not stop:raise Blocked('Add approved stop alarms to the AWS template, then resync; the console does not rewrite it')
        binding=Binding.model_validate({'id':r.binding_id,'name':r.name,
          'agent':{'account_id':agent.account_id,'region':r.agent_region,'profile':agent.profile},
          'workload':{'account_id':work.account_id,'region':d['region'],'profile':work.profile},
          'orchestrator':{'account_id':origin.account_id,'region':d['region'],'profile':origin.execution_profile},
          'target_accounts':extra,'fault_profile':origin.execution_profile,'requester_profile':r.requester_profile,'change_profile':r.change_profile,
          'agent_space_id':r.agent_space_id,'association_id':r.association_id,'service_id':r.service_id,'deployment_model':r.deployment_model,
          'environment':'nonproduction','route':r.route,'probes':[r.probe],'checks':r.checks,'metrics':r.metrics,'runbooks':r.runbooks,
          'faults':[{'id':'aws-template','title':r.name,'native_fis':True,'template_id':d['template_id'],'template_sha256':d['contract_sha256'],
            'target_accounts_sha256':p['target_accounts_sha256'],'resolved_targets':p['targets'],'preview_record_id':preview['id'],
            'target_match':r.target_match,'minimum_targets':r.minimum_targets,'target_arns':targets,
            'allowed_action_ids':sorted({x['actionId'] for x in t['actions'].values()}),'max_fault_seconds':r.maximum_fault_seconds,
            'baseline_checks':r.baseline_check_ids,'fault_checks':r.fault_check_ids,'cleanup_checks':r.cleanup_check_ids,
            'cleanup_runbook_id':r.cleanup_runbook_id,'safety_alarm_arns':stop,'safety_review':r.safety_review,
            'independent_recovery':r.independent_recovery,'action_review':r.action_review}]})
        exp=Experiment.model_validate({'id':r.experiment_id,'revision':r.revision,'title':r.name,'binding_id':binding.id,
          'fault_id':'aws-template','probe_id':r.probe.id,'mode':'native','hypotheses':r.hypotheses,'oracle':r.oracle,
          **{k:getattr(r,k) for k in ('baseline_seconds','observation_seconds','response_deadline_seconds','ingestion_wait_seconds','max_error_ratio','max_latency_ms','stable_seconds','bucket_seconds')},
          'business_requirements':r.business_requirements,'intervention_runbook_ids':[b.id for b in r.runbooks]})
        if exp.observation_seconds<r.maximum_fault_seconds+exp.stable_seconds:raise Blocked('Observation must include fault budget and stable recovery')
        if not set(exp.oracle.affected_resource_arns)<=set(targets):raise Blocked('Oracle resources must be in the approved preview')
        if not set(exp.oracle.required_checks)<={c.id for c in r.checks}:raise Blocked('Oracle check is not configured')
        if any(a.metric_id not in {m.id for m in r.metrics} for a in r.business_requirements):raise Blocked('Business requirement metric is not configured')
        candidate=self.config.model_dump(mode='json');candidate['bindings']=[b for b in candidate['bindings'] if b['id']!=binding.id]+[binding.model_dump(mode='json')]
        config=Configuration.model_validate(candidate);self._profiles(config)
        return self.store.put_record('guided_plan','setup',{'configuration':config.model_dump(mode='json'),
           'base_digest':digest(self.config.model_dump(mode='json')),'experiment':exp.model_dump(mode='json'),
           'template_record_id':row['id'],'input_hashes':{row['id']:row['sha256'],preview['id']:preview['sha256']},
           'rationale':'Guided AWS definition-to-measurement plan; activation is local configuration, not exposure approval.'})
