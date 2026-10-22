"""Authenticated local API. The browser never supplies AWS credentials or endpoints."""
from __future__ import annotations
from contextlib import asynccontextmanager
import hashlib
import hmac
import json
from pathlib import Path
import tempfile
from urllib.parse import urlsplit
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel, ConfigDict, Field
from . import __version__
from .evaluation import evaluate_trial, compare_campaign
from .fis_campaigns import QueueRequest, AttachContract
from .models import Configuration, Experiment, TrialRequest, CampaignRequest, Approval, Diagnosis, ChangeProposal, Binding
from .service import Service
from .store import Store
from .util import Blocked, iso

ROOT=Path(__file__).resolve().parents[1]


class Pin(BaseModel):
    model_config=ConfigDict(extra='forbid')
    record_id: str=Field(min_length=1,max_length=200)


class Reconcile(BaseModel):
    model_config=ConfigDict(extra='forbid')
    operation_id: str=Field(min_length=1,max_length=100)
    provider_id: str=Field(pattern=r'^[A-Za-z0-9_.-]{1,128}$')


def create_app(config:Configuration,store:Store,operator_token:str,approval_token:str,*,service=None):
    if len(operator_token)<24 or len(approval_token)<24 or operator_token==approval_token:
        raise ValueError('Two distinct local tokens of at least 24 characters are required')
    app=FastAPI(title='DevOps Agent experiment console',version=__version__,docs_url=None,redoc_url=None,openapi_url=None)
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=['127.0.0.1','localhost','[::1]','testserver'])
    svc=service or Service(config,store)

    @app.middleware('http')
    async def boundary(request:Request,call_next):
        if request.url.path.startswith('/api/'):
            supplied=request.headers.get('authorization','').removeprefix('Bearer ')
            role='approver' if hmac.compare_digest(supplied,approval_token) else 'operator' if hmac.compare_digest(supplied,operator_token) else None
            if role is None: return JSONResponse({'error':'Unauthorized'},401)
            if '/approve/' in request.url.path and role!='approver': return JSONResponse({'error':'Approval credential required'},403)
            if request.method not in ('GET','HEAD'):
                origin=request.headers.get('origin')
                if origin and origin!=str(request.base_url).rstrip('/'):
                    return JSONResponse({'error':'Cross-origin write rejected'},403)
                declared=request.headers.get('content-length','0')
                try: size=int(declared)
                except ValueError: return JSONResponse({'error':'Invalid content length'},400)
                if size>1_048_576: return JSONResponse({'error':'Request too large'},413)
                body=await request.body()
                if len(body)>1_048_576: return JSONResponse({'error':'Request too large'},413)
            request.state.role=role
        response=await call_next(request)
        response.headers['Cache-Control']='no-store'
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['X-Frame-Options']='DENY'
        response.headers.setdefault('Content-Security-Policy',"default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")
        return response

    @app.exception_handler(Blocked)
    async def blocked(request,exc): return JSONResponse({'error':str(exc)},409)
    @app.exception_handler(KeyError)
    async def missing(request,exc): return JSONResponse({'error':'Unknown record'},404)
    @app.exception_handler(ValueError)
    async def invalid(request,exc): return JSONResponse({'error':str(exc)[:1000]},400)

    @app.get('/healthz')
    def health(): return {'status':'ok','version':__version__}

    @app.get('/',response_class=HTMLResponse)
    def index(): return (ROOT/'static/aws.html').read_text()

    @app.get('/response',response_class=HTMLResponse)
    def response_console(): return (ROOT/'static/index.html').read_text()

    @app.get('/static/{name}')
    def static(name:str):
        allowed={'app.js':'text/javascript','charts.js':'text/javascript','style.css':'text/css','aws.js':'text/javascript','aws.css':'text/css'}
        if name not in allowed: raise HTTPException(404)
        return Response((ROOT/'static'/name).read_text(),media_type=allowed[name])

    @app.get('/api/workspace')
    def workspace():
        records=store.records()
        # Source bodies are opened explicitly; keep polling payloads bounded.
        summary=[{k:v for k,v in r.items() if k!='data'} for r in records]
        return {'version':__version__,'worker':store.meta('worker'),'entities':store.entities(),
                'records':summary,'experiments':store.records(kind='experiment'),
                'write_enabled':config.enable_aws_writes,'role_mode':'single-operator with separate approval credential',
                'at':iso()}

    @app.get('/api/config')
    def public_configuration():
        return {'write_enabled':config.enable_aws_writes,'bindings':[{
            'id':b.id,'name':b.name,'agent_account':b.agent.account_id,'agent_region':b.agent.region,
            'workload_account':b.workload.account_id,'workload_region':b.workload.region,'agent_space_id':b.agent_space_id,
            'service_id':b.service_id,'deployment_model':b.deployment_model,'environment':b.environment,
            'receipt_adapter_configured':bool(b.route.receipt_log_group),
            'faults':[{'id':f.id,'title':f.title,'targets':f.target_arns,'max_seconds':f.max_fault_seconds,'fault_checks':f.fault_checks} for f in b.faults],
            'probes':[{'id':p.id,'title':p.title,'requests_per_second':p.requests_per_second} for p in b.probes],
            'checks':[{'id':c.id,'purpose':c.purpose} for c in b.checks],
            'runbooks':[{'id':r.id,'title':r.title,'version':r.document_version,'sha256':r.content_sha256,'rollback':r.rollback_runbook_id} for r in b.runbooks],
        } for b in config.bindings]}

    @app.get('/api/schema/{kind}')
    def schema(kind:str):
        models={'experiment':Experiment,'configuration':Configuration,'diagnosis':Diagnosis,'campaign':CampaignRequest,'change':ChangeProposal,'fis_campaign':QueueRequest,'fis_contract':AttachContract}
        if kind not in models: raise HTTPException(404)
        return models[kind].model_json_schema()

    @app.post('/api/experiments')
    def experiment(body:Experiment): return svc.register(body)
    @app.post('/api/trials')
    def trial(body:TrialRequest): return svc.trial(body)
    @app.post('/api/trials/{identifier}/qualify')
    def qualify(identifier:str): return svc.qualify(identifier)
    @app.post('/api/trials/{identifier}/start')
    def start(identifier:str): return svc.start(identifier)
    @app.post('/api/trials/{identifier}/abort')
    def abort(identifier:str): return svc.abort(identifier)
    @app.post('/api/trials/{identifier}/retry-cleanup')
    def retry_cleanup(identifier:str): return svc.retry_cleanup(identifier)
    @app.post('/api/trials/{identifier}/diagnosis')
    def diagnosis(identifier:str,body:Diagnosis): return svc.diagnosis(identifier,body)
    @app.post('/api/trials/{identifier}/assess')
    def assess(identifier:str):
        entity=store.entity(identifier)
        if entity['kind']!='trial': raise Blocked('Not a trial')
        binding=Binding.model_validate(store.record(entity['data']['binding_record_id'])['data'])
        return evaluate_trial(store,identifier,binding)
    @app.post('/api/campaigns')
    def campaign(body:CampaignRequest): return svc.campaign(body)
    @app.post('/api/campaigns/{identifier}/pin')
    def pin(identifier:str,body:Pin): return svc.pin_recommendation(identifier,body.record_id)
    @app.post('/api/campaigns/{identifier}/compare')
    def compare(identifier:str):
        c=store.entity(identifier)
        if c['kind']!='campaign': raise Blocked('Not a campaign')
        binding=Binding.model_validate(store.record(c['data']['binding_record_id'])['data'])
        return compare_campaign(store,identifier,binding)
    @app.post('/api/entities/{identifier}/changes')
    def change(identifier:str,body:ChangeProposal): return svc.propose_change(identifier,body)
    @app.get('/api/entities/{identifier}/approval/{purpose}')
    def approval_subject(identifier:str,purpose:str): return svc.approval_subject(identifier,purpose)
    @app.post('/api/entities/{identifier}/approve/{purpose}')
    def approve(identifier:str,purpose:str,body:Approval): return svc.approve(identifier,purpose,body)
    @app.post('/api/entities/{identifier}/reconcile')
    def reconcile(identifier:str,body:Reconcile): return svc.reconcile(identifier,body.operation_id,body.provider_id)
    @app.get('/api/entities/{identifier}')
    def details(identifier:str):
        return {'entity':store.entity(identifier),'events':store.events(identifier),'records':store.records(identifier),
                'operations':store.operations(identifier),'probes':store.probes(identifier)}
    @app.get('/api/records/{identifier}')
    def record(identifier:str): return store.record(identifier)
    @app.get('/api/entities/{identifier}/export')
    def export(identifier:str): return store.export(identifier)
    @app.get('/api/entities/{identifier}/report',response_class=HTMLResponse)
    def report(identifier:str):
        from .report import report_document
        document,csp=report_document(store,identifier)
        return HTMLResponse(document,headers={'Content-Security-Policy':csp})
    @app.get('/api/backup')
    def backup():
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/'backup.sqlite3';store.backup(p)
            return Response(p.read_bytes(),media_type='application/vnd.sqlite3',headers={'Content-Disposition':'attachment; filename="agent-validation.sqlite3"'})
    @app.get('/api/metrics',response_class=PlainTextResponse)
    def metrics():
        from .metrics import prometheus
        return prometheus(store)
    @app.get('/api/grafana')
    def grafana():
        from .metrics import dashboard
        return dashboard()
    from .fis_api import install
    install(app, config, store, svc)
    return app
