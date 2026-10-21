from __future__ import annotations
import base64, hashlib, html, json, os, re, secrets, tempfile, threading
from pathlib import Path
from typing import Literal
from uuid import uuid4
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from starlette.background import BackgroundTask
from starlette.middleware.trustedhost import TrustedHostMiddleware
from pydantic import Field, ValidationError
from . import __version__
from .models import (StrictModel, ID, InspectRequest, EvaluateRequest, ObserveRequest,
                     ReportRequest, Bundle)
from .store import Store, strict_json, now, ref, Conflict
from .evaluator import evaluate
from . import connectors

ROOT = Path(__file__).resolve().parents[1]
MAX_IMPORT = 5 * 1024 * 1024

class AWSConnection(StrictModel):
    id: ID
    name: str = Field(min_length=1, max_length=100)
    kind: Literal['aws']
    profile: str | None = Field(default=None, max_length=150)
    expected_account_id: str = Field(pattern=r'^\d{12}$')
    regions: list[str] = Field(min_length=1, max_length=3)
    services: list[Literal['ec2', 'autoscaling', 'eks', 'ecs', 'lambda', 'rds', 'elbv2', 'cloudwatch', 'fis']] = Field(default_factory=lambda: connectors.AWS_SERVICES.copy(), min_length=1, max_length=9)

class EngineConnection(StrictModel):
    id: ID
    name: str = Field(min_length=1, max_length=100)
    kind: Literal['docker', 'podman']
    socket: str = Field(pattern=r'^/', max_length=1000)

class KubeConnection(StrictModel):
    id: ID
    name: str = Field(min_length=1, max_length=100)
    kind: Literal['kubernetes']
    in_cluster: bool = False
    kubeconfig: str | None = Field(default=None, max_length=1000)
    context: str | None = Field(default=None, max_length=300)
    namespaces: list[str] = Field(min_length=1, max_length=10)

class Configuration(StrictModel):
    connections: list[AWSConnection | EngineConnection | KubeConnection] = Field(default_factory=list, max_length=20)


def load_config(path):
    if not path:
        return {'connections': []}
    config = Configuration.model_validate(strict_json(Path(path).read_text())).model_dump(mode='json')
    if len({c['id'] for c in config['connections']}) != len(config['connections']):
        raise ValueError('Connection IDs must be unique')
    for c in config['connections']:
        if c['kind'] == 'aws':
            if any(not re.fullmatch(r'[a-z]{2}(?:-[a-z]+)+-\d', r) for r in c['regions']):
                raise ValueError('Invalid AWS Region in administrator configuration')
        if c['kind'] == 'kubernetes':
            if not c['in_cluster'] and not c['context']:
                raise ValueError('Kubernetes connection requires an explicit context or in_cluster=true')
            if any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]*[a-z0-9])?', ns) for ns in c['namespaces']):
                raise ValueError('Invalid Kubernetes namespace')
    return config


def make_bundle(records):
    return {'schema_version': '1.0', 'kind': 'validation_bundle', 'records': records}


def make_observation(snapshot):
    d = snapshot['data']
    run_id = 'obs-' + uuid4().hex[:16]
    rr = 'execution_run:' + run_id + '@1'
    incomplete = sum(x['status'] not in ('complete', 'not_requested') for x in d['coverage'])
    scope_missing = sorted(set(d['requested_scope']) - {x['scope'] for x in d['coverage'] if x['status'] != 'not_requested'})
    # No requested scope is not a successful inspection.
    incomplete += len(scope_missing) + int(not d['requested_scope'])
    run = {'kind': 'execution_run', 'id': run_id, 'revision': 1, 'title': 'Inventory collection · ' + d['connection_id'], 'simulated': snapshot['simulated'], 'data': {'scenario_ref': 'scenario:INSPECTION-COVERAGE@1', 'snapshot_ref': ref(snapshot), 'execution_type': 'observation', 'execution_state': 'completed', 'scope_id': d['scope_id'], 'targets': [d['connection_id']], 'started_at': d['started_at'], 'ended_at': d['ended_at'], 'fault_confirmed': None, 'external_id': None, 'notes': 'The run records a completed collection attempt. Its validation may fail if any requested scope was incomplete. No fault or workload test was executed.'}}
    e = {'kind': 'evidence', 'id': 'ev-' + uuid4().hex[:16], 'revision': 1, 'title': 'Incomplete requested collection scopes', 'simulated': snapshot['simulated'], 'data': {'run_ref': rr, 'scope_id': d['scope_id'], 'metric': 'incomplete_scope_count', 'value': incomplete, 'unit': 'scopes', 'sample_count': max(1, len(d['requested_scope'])), 'window_start': d['started_at'], 'window_end': d['ended_at'], 'collected_at': d['ended_at'], 'source': ref(snapshot), 'notes': 'Counts denied, errored, truncated and missing requested scopes. Zero does not mean the application is healthy.'}}
    return [run, e]


def create_app(data_dir=None, token=None, config_path=None, testing=False):
    app = FastAPI(title='Local Validation Console', version=__version__, docs_url=None, redoc_url=None, openapi_url=None)
    token = token or os.environ.get('CONSOLE_TOKEN', '')
    if len(token) < 32:
        raise ValueError('CONSOLE_TOKEN must contain at least 32 characters')
    config = load_config(config_path or os.environ.get('CONSOLE_CONFIG'))
    store = Store(data_dir or os.environ.get('CONSOLE_DATA', './data'))
    app.state.store = store
    app.state.config = config
    inspection_lock = threading.Lock()
    seed_path = ROOT / 'examples' / 'catalogue.json'
    if seed_path.exists() and not store.all():
        store.import_bundle(strict_json(seed_path.read_text()), origin='catalogue')
    page = (ROOT / 'static' / 'console.html').read_text() if (ROOT / 'static' / 'console.html').exists() else '<html><body>Build static/console.html first.</body></html>'
    scripts = re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>', page, flags=re.S)
    styles = re.findall(r'<style(?:\s[^>]*)?>(.*?)</style>', page, flags=re.S)
    def hashes(parts):
        return ' '.join("'sha256-" + base64.b64encode(hashlib.sha256(x.encode()).digest()).decode() + "'" for x in parts)
    csp = f"default-src 'none'; script-src {hashes(scripts)}; style-src {hashes(styles)}; connect-src 'self'; img-src data:; base-uri 'none'; object-src 'none'; frame-ancestors 'none'; form-action 'self'"
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=['localhost', '127.0.0.1', '[::1]'] + (['testserver'] if testing else []))

    @app.middleware('http')
    async def boundary(request: Request, call_next):
        if request.url.path.startswith('/api/'):
            expected = str(request.base_url).rstrip('/')
            origin = request.headers.get('origin')
            if origin and origin != expected:
                return JSONResponse({'detail': 'Cross-origin API access is disabled'}, status_code=403)
            if request.headers.get('sec-fetch-site') == 'cross-site':
                return JSONResponse({'detail': 'Cross-site API access is disabled'}, status_code=403)
            supplied = request.headers.get('authorization', '')
            if not secrets.compare_digest(supplied.encode('utf-8'), ('Bearer ' + token).encode('utf-8')):
                return JSONResponse({'detail': 'Unlock the local console with its startup token'}, status_code=401)
            length = request.headers.get('content-length', '0')
            if not length.isdigit() or int(length) > MAX_IMPORT:
                return JSONResponse({'detail': 'Request exceeds 5 MiB or has an invalid length'}, status_code=413)
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Referrer-Policy'] = 'no-referrer'
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Content-Security-Policy'] = csp
        return response

    @app.exception_handler(KeyError)
    async def missing(request, exc):
        return JSONResponse({'detail': 'A referenced record does not exist'}, status_code=404)

    @app.exception_handler(RequestValidationError)
    async def request_schema_error(request, exc):
        return JSONResponse({'detail': [{'location': list(e['loc']), 'message': e['msg'], 'type': e['type']} for e in exc.errors()]}, status_code=422)

    @app.exception_handler(ValidationError)
    async def schema_error(request, exc):
        return JSONResponse({'detail': [{'location': list(e['loc']), 'message': e['msg'], 'type': e['type']} for e in exc.errors(include_input=False, include_context=False, include_url=False)]}, status_code=422)

    @app.exception_handler(ValueError)
    async def bad_value(request, exc):
        return JSONResponse({'detail': str(exc)}, status_code=409 if isinstance(exc, Conflict) else 400)

    @app.get('/', response_class=HTMLResponse)
    def root():
        return HTMLResponse(page)

    @app.get('/healthz')
    def health():
        return {'status': 'ok'}

    @app.get('/api/workspace')
    def workspace():
        return {'version': __version__, 'records': store.all(), 'audit': store.audit_entries(), 'fault_execution': False, 'storage': 'local SQLite', 'schema_version': '1.0'}

    @app.get('/api/config')
    def public_config():
        visible = []
        for c in config['connections']:
            fields = ['id', 'name', 'kind', 'profile', 'expected_account_id', 'regions', 'services', 'context', 'namespaces', 'in_cluster']
            visible.append({k: c[k] for k in fields if k in c})
        return {'connections': visible, 'max_import_bytes': MAX_IMPORT, 'fault_execution': False}

    async def body_json(request):
        data = bytearray()
        async for chunk in request.stream():
            data.extend(chunk)
            if len(data) > MAX_IMPORT:
                raise HTTPException(413, 'Import exceeds 5 MiB')
        return strict_json(data.decode('utf-8'))

    @app.post('/api/import/preview')
    async def import_preview(request: Request):
        return store.import_bundle(await body_json(request), dry_run=True)

    @app.post('/api/import')
    async def import_commit(request: Request):
        return store.import_bundle(await body_json(request))

    @app.get('/api/export')
    def export():
        return JSONResponse(store.export(), headers={'Content-Disposition': 'attachment; filename="workspace.json"'})

    @app.get('/api/schema')
    def schema():
        return Bundle.model_json_schema()

    @app.post('/api/inspect')
    def inspect(req: InspectRequest):
        connection = next((c for c in config['connections'] if c['id'] == req.connection_id), None)
        if connection is None:
            raise HTTPException(400, 'Connection is not in the administrator allowlist')
        if not inspection_lock.acquire(blocking=False):
            raise HTTPException(409, 'An inspection is already active; this build allows one at a time')
        try:
            store.audit('inspection_started', {'connection_id': connection['id']})
            try:
                snapshot = connectors.inspect(connection)
            except connectors.InspectionError as exc:
                store.audit('inspection_rejected', {'connection_id': connection['id'], 'reason': str(exc)})
                raise HTTPException(400, str(exc))
            except Exception as exc:
                code = exc.__class__.__name__
                if hasattr(exc, 'response') and isinstance(exc.response, dict):
                    code = exc.response.get('Error', {}).get('Code', code)
                store.audit('inspection_error', {'connection_id': connection['id'], 'error_code': code})
                raise HTTPException(400, 'Connection failed: ' + code + '. Check the local profile/context and permissions; no credentials are accepted by this API.')
            store.import_bundle(make_bundle([snapshot]), origin='collected')
            return store.get(ref(snapshot))
        finally:
            inspection_lock.release()

    @app.post('/api/observe')
    def observe(req: ObserveRequest):
        snapshot_entry = store.get(req.snapshot_ref)
        snapshot = snapshot_entry['record']
        if snapshot['kind'] != 'snapshot':
            raise HTTPException(400, 'snapshot_ref must reference a snapshot')
        if snapshot['simulated']:
            raise HTTPException(400, 'Simulated snapshots cannot create collection-validation runs; use the isolated example run')
        records = make_observation(snapshot)
        # Derivation does not authenticate an imported snapshot.
        origin = 'derived-from-import' if snapshot_entry['meta']['origin'] == 'imported' else 'observed'
        store.import_bundle(make_bundle(records), origin=origin)
        return store.get(ref(records[0]))

    @app.post('/api/evaluate')
    def evaluate_run(req: EvaluateRequest):
        result = evaluate(store, req.run_ref, req.evidence_refs)
        store.import_bundle(make_bundle([result]), origin='evaluated')
        return store.get(ref(result))

    @app.post('/api/reports')
    def create_report(req: ReportRequest):
        entry = store.get(req.validation_ref)
        v = entry['record']
        if v['kind'] != 'validation_run':
            raise HTTPException(400, 'validation_ref must reference a validation_run')
        d = v['data']
        caveats = list(d['limitations'])
        if entry['meta']['origin'] != 'evaluated':
            caveats.insert(0, 'The validation result was imported and has not been recomputed by this workspace.')
        body = '\n'.join([f"Result: {d['outcome']}", f"Execution record: {d['run_ref']}", f"Scenario revision: {d['scenario_ref']}", f"Evaluator: {d['evaluator_version']}", '', *[f"{c['outcome'].upper()} | {c['title']} | {c['reason']}" for c in d['checks']], *['Gate: ' + g for g in d['gates']]])
        r = {'kind': 'report', 'id': 'report-' + uuid4().hex[:16], 'revision': 1, 'title': v['title'].replace('Validation · ', 'Report · '), 'simulated': v['simulated'], 'data': {'validation_ref': req.validation_ref, 'outcome': d['outcome'], 'body': body, 'limitations': caveats, 'generated_at': now()}}
        store.import_bundle(make_bundle([r]), origin='reported')
        return store.get(ref(r))

    @app.get('/api/report-html')
    def report_html(reference: str):
        entry = store.get(reference)
        record = entry['record']
        if record['kind'] != 'report':
            raise HTTPException(400, 'Reference is not a report')
        d = record['data']
        esc = html.escape
        watermark = 'SIMULATED DATA — NOT AN ACCOUNT ASSESSMENT' if record['simulated'] else 'Scoped evidence evaluation — not a deployment-readiness certificate'
        content = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>' + esc(record['title']) + '</title><body><h1>' + esc(record['title']) + '</h1><p><strong>' + watermark + '</strong></p><p>Report reference: ' + esc(reference) + '</p><p>Record SHA-256: ' + esc(entry['meta']['sha256']) + '</p><p>Origin: ' + esc(entry['meta']['origin']) + '</p><p>Generated: ' + esc(d['generated_at']) + '</p><pre style="white-space:pre-wrap">' + esc(d['body']) + '</pre><h2>Limits of this conclusion</h2><ul>' + ''.join('<li>' + esc(x) + '</li>' for x in d['limitations']) + '</ul></body></html>'
        return HTMLResponse(content, headers={'Content-Disposition': f'attachment; filename="{record["id"]}.html"'})

    @app.get('/api/backup')
    def backup():
        fd, name = tempfile.mkstemp(prefix='validation-backup-', suffix='.sqlite3')
        os.close(fd)
        store.backup(name)
        store.audit('backup_download', {'format': 'SQLite online backup'})
        return FileResponse(name, media_type='application/octet-stream', filename='validation-workspace.sqlite3', background=BackgroundTask(lambda: os.unlink(name)))

    return app
