"""Authenticated onboarding, exact approvals, preview and guided preparation."""
from pathlib import Path
from fastapi import Request
from fastapi.responses import HTMLResponse
from pydantic import Field
from .setup import Setup, ConfigDraft, AccountDraft, Compose
from .native_fis import Previews
from .models import Strict, Approval, ReadCheck, READS
from .util import Blocked, error_code, normal

class ConnectionCheck(Strict):
    region: str
    draft_id: str | None = None

class ReadTest(Strict):
    connection_id: str
    region: str
    check: ReadCheck

class RunbookRead(Strict):
    connection_id: str
    region: str
    document_arn: str
    document_version: str = Field(pattern=r'^[1-9][0-9]*$')


def install(app,config,store,service):
    from botocore.exceptions import BotoCoreError, ClientError
    from fastapi.responses import JSONResponse
    @app.exception_handler(BotoCoreError)
    @app.exception_handler(ClientError)
    async def sdk_error(request,exc):
        return JSONResponse({'error':'AWS read failed: '+error_code(exc),'guidance':'Check the selected profile, SSO session, Region and read permissions.'},424)
    setup=Setup(config,store);previews=Previews(config,store)
    @app.get('/setup',response_class=HTMLResponse)
    def page():return (Path(__file__).resolve().parents[1]/'static/setup.html').read_text()
    @app.get('/api/setup')
    def state():return setup.current()
    @app.post('/api/setup/accounts')
    def account(body:AccountDraft):return setup.account_draft(body)
    @app.post('/api/setup/drafts')
    def draft(body:ConfigDraft):return setup.draft(body)
    @app.get('/api/setup/drafts/{identifier}/subject')
    def subject(identifier:str):return setup.subject(identifier)
    @app.post('/api/setup/approve/config/{identifier}')
    def commit(identifier:str,body:Approval):return setup.commit(identifier,body)
    @app.post('/api/setup/connections/{identifier}/check')
    def check(identifier:str,body:ConnectionCheck):return setup.verify_account(identifier,body.region,draft_id=body.draft_id)
    @app.post('/api/setup/connections/{identifier}/agents')
    def agents(identifier:str,body:ConnectionCheck):return setup.agents(identifier,body.region)
    @app.post('/api/setup/compose')
    def compose(body:Compose):return setup.compose(body)
    @app.get('/api/setup/preview-subject/{identifier}')
    def preview_subject(identifier:str):return previews.subject(identifier)
    @app.post('/api/setup/approve/preview/{identifier}')
    def preview(identifier:str,body:Approval):return previews.request(identifier,body)
    @app.get('/api/setup/previews')
    def preview_list():
        return {'jobs':store.entities('fis_preview'),'results':store.records(kind='fis_preview_result')}
    @app.post('/api/setup/previews/{identifier}/cancel')
    def cancel(identifier:str):
        from .preview_control import cancel as cancel_preview
        return cancel_preview(store,identifier)
    @app.get('/api/setup/read-operations')
    def reads():return {k:sorted(v) for k,v in READS.items()}
    @app.get('/api/setup/read-shape/{svc}/{op}')
    def read_shape(svc:str,op:str):
        if op not in READS.get(svc,set()):raise Blocked('Read operation not allowlisted')
        import botocore.session
        model=botocore.session.get_session().get_service_model(svc)
        from botocore import xform_name
        api_name=next((name for name in model.operation_names if xform_name(name)==op),None)
        if not api_name:raise Blocked('Operation not in the installed SDK model')
        from .sdk_shapes import input_shape
        return input_shape(model.operation_model(api_name).input_shape)

    @app.post('/api/setup/test-read')
    def test_read(body:ReadTest):
        from .aws import compare
        import jmespath
        a=setup._account(body.connection_id)
        if body.region not in a.regions or (body.check.account_id and body.check.account_id!=a.account_id):raise Blocked('Verifier scope mismatch')
        session=setup.factory(a.profile)
        identity=session.client('sts',region_name=body.region,config=setup.sdk).get_caller_identity()
        if identity.get('Account')!=a.account_id or identity.get('Arn','').endswith(':root'):raise Blocked('Unexpected observer account')
        raw=getattr(session.client(body.check.service,region_name=body.region,config=setup.sdk),body.check.operation)(**body.check.parameters)
        response=normal(raw)
        if any(response.get(t) for t in ('NextToken','nextToken','Marker','NextMarker')):raise Blocked('Verifier read is truncated; narrow resource selectors')
        if body.check.service=='ssm' and response.get('Parameter',{}).get('Type')=='SecureString':raise Blocked('SecureString cannot be used as a verifier')
        record=setup._capture('verifier-test',a,body.region,body.check.service,body.check.operation,body.check.parameters,raw)
        value=jmespath.search(body.check.expression,response)
        return {'source_record_id':record['id'],'observed':value,'passed':value is not None and compare(value,body.check.operator,body.check.expected),'assessment':'Verifier test only, not an incident result.'}
    @app.post('/api/setup/runbook')
    def runbook(body:RunbookRead):
        import hashlib,json
        a=setup._account(body.connection_id)
        if body.region not in a.regions or not body.document_arn.startswith(f'arn:aws:ssm:{body.region}:{a.account_id}:document/'):
            raise Blocked('Runbook must be in the selected account and Region')
        session=setup.factory(a.profile);identity=session.client('sts',region_name=body.region,config=setup.sdk).get_caller_identity()
        if identity.get('Account')!=a.account_id or identity.get('Arn','').endswith(':root'):raise Blocked('Unexpected observer account')
        params={'Name':body.document_arn,'DocumentVersion':body.document_version,'DocumentFormat':'JSON'}
        value=session.client('ssm',region_name=body.region,config=setup.sdk).get_document(**params)
        if value.get('DocumentType')!='Automation' or value.get('DocumentVersion')!=body.document_version:raise Blocked('Unexpected runbook version or type')
        record=setup._capture('runbook-review',a,body.region,'ssm','get_document',params,value)
        return {'source_record_id':record['id'],'content_sha256':hashlib.sha256(value['Content'].encode()).hexdigest(),
                'document':json.loads(value['Content']),'version':value['DocumentVersion'],
                'execution_verified':False}
