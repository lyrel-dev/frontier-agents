import base64,hashlib,json,re,sqlite3
from copy import deepcopy
from pathlib import Path
import pytest
from app.server import create_app, make_observation, load_config
from app.store import ref


def test_api_requires_token(api_client):
    c,_=api_client
    r=c.get('/api/workspace',headers={'Authorization':''})
    assert r.status_code==401


def test_no_openapi_or_docs_surface(api_client):
    c,_=api_client
    for route in ['/docs','/openapi.json','/redoc']:assert c.get(route).status_code==404


def test_wrong_token_rejected(api_client):
    c,_=api_client
    assert c.get('/api/workspace',headers={'Authorization':'Bearer wrong'}).status_code==401


@pytest.mark.parametrize('origin',['https://evil.invalid','null','http://localhost:9999'])
def test_cross_origin_rejected(api_client,origin):
    c,_=api_client
    assert c.get('/api/workspace',headers={'Origin':origin}).status_code==403


def test_same_origin_allowed(api_client):
    c,_=api_client
    assert c.get('/api/workspace',headers={'Origin':'http://testserver'}).status_code==200


def test_untrusted_host_rejected(api_client):
    c,_=api_client
    assert c.get('/',headers={'Host':'evil.invalid'}).status_code==400


def test_cross_site_fetch_rejected(api_client):
    c,_=api_client
    assert c.get('/api/workspace',headers={'Sec-Fetch-Site':'cross-site'}).status_code==403


def test_oversize_content_rejected(api_client):
    c,_=api_client
    assert c.post('/api/import',content='{}',headers={'Content-Length':str(6*1024*1024)}).status_code==413


def test_duplicate_json_keys_rejected(api_client):
    c,_=api_client
    r=c.post('/api/import/preview',content='{"schema_version":"1.0","schema_version":"2.0","records":[]}')
    assert r.status_code==400 and 'Duplicate' in r.text


def test_no_fault_execution_endpoints(api_client):
    c,_=api_client
    for path in ['start-experiment','stop-experiment','execute','shell','exec']:
        assert c.post('/api/'+path,json={}).status_code==404


def test_connection_id_is_allowlisted(api_client):
    c,_=api_client
    assert c.post('/api/inspect',json={'connection_id':'not-allowed'}).status_code==400


def test_raw_credentials_rejected_without_echo(api_client):
    c,_=api_client
    secret='DO-NOT-ECHO-THIS-SECRET'
    r=c.post('/api/inspect',json={'connection_id':'not-allowed','aws_secret_access_key':secret})
    assert r.status_code==422 and secret not in r.text


def test_csp_hashes_match_served_scripts_and_styles(api_client):
    c,_=api_client;r=c.get('/')
    csp=r.headers['content-security-policy']
    for body in re.findall(r'<(?:script|style)(?:\s[^>]*)?>(.*?)</(?:script|style)>',r.text,re.S):
        hashed=base64.b64encode(hashlib.sha256(body.encode()).digest()).decode()
        assert 'sha256-'+hashed in csp
    assert "frame-ancestors 'none'" in csp and "base-uri 'none'" in csp
    assert r.headers['cache-control']=='no-store'


def test_end_to_end_import_evaluate_report_export(api_client,examples):
    c,_=api_client
    preview=c.post('/api/import/preview',json=examples)
    assert preview.status_code==200 and preview.json()['created']==15
    assert len(c.get('/api/workspace').json()['records'])==37
    assert c.post('/api/import',json=examples).status_code==200
    v=c.post('/api/evaluate',json={'run_ref':'execution_run:example-run-1@1'})
    assert v.status_code==200 and v.json()['record']['data']['outcome']=='fail'
    report=c.post('/api/reports',json={'validation_ref':v.json()['meta']['ref']})
    assert report.status_code==200
    html=c.get('/api/report-html',params={'reference':report.json()['meta']['ref']})
    assert html.status_code==200 and 'SIMULATED DATA' in html.text
    exported=c.get('/api/export').json()
    assert len(exported['records'])==54
    assert set(exported['manifest'])=={ref(r) for r in exported['records']}


def test_imported_report_html_is_escaped(api_client):
    c,_=api_client
    record={'kind':'report','id':'xss-report','revision':1,'title':'<img src=x onerror=alert(1)>','simulated':False,'data':{'validation_ref':None,'outcome':'not_assessed','body':'<script>alert(1)</script>','limitations':[],'generated_at':'2026-10-21T08:00:00Z'}}
    assert c.post('/api/import',json={'records':[record]}).status_code==200
    result=c.get('/api/report-html',params={'reference':'report:xss-report@1'})
    assert '<script>' not in result.text and '&lt;script&gt;' in result.text


def test_backup_download_is_valid_sqlite(api_client,tmp_path):
    c,app=api_client
    r=c.get('/api/backup');target=tmp_path/'download.sqlite3';target.write_bytes(r.content)
    assert r.status_code==200 and r.content.startswith(b'SQLite format 3')
    with sqlite3.connect(target) as con: assert con.execute('SELECT COUNT(*) FROM records').fetchone()[0]==37


def test_observation_run_reports_incomplete_scopes(api_client,examples):
    c,_=api_client
    snapshot=deepcopy(next(r for r in examples['records'] if r['id']=='example-aws'))
    snapshot.update(id='imported-snapshot',simulated=False)
    assert c.post('/api/import',json={'records':[snapshot]}).status_code==200
    run=c.post('/api/observe',json={'snapshot_ref':'snapshot:imported-snapshot@1'})
    assert run.status_code==200 and run.json()['meta']['origin']=='derived-from-import'
    v=c.post('/api/evaluate',json={'run_ref':run.json()['meta']['ref']})
    assert v.json()['record']['data']['outcome']=='fail'
    assert any('authenticity' in x for x in v.json()['record']['data']['limitations'])


def test_simulated_snapshot_cannot_be_used_as_real_collection(api_client,examples):
    c,_=api_client;c.post('/api/import',json=examples)
    assert c.post('/api/observe',json={'snapshot_ref':'snapshot:example-aws@1'}).status_code==400


@pytest.mark.parametrize('coverage,scopes,expected',[
 ([],[],1),
 ([],['missing'],1),
 ([{'scope':'a','status':'complete','resource_count':0}],['a'],0),
 ([{'scope':'a','status':'not_requested','resource_count':0}],['a'],1),
 ([{'scope':'a','status':'truncated','resource_count':3}],['a'],1),
])
def test_collection_metric_accounts_for_missing_scope(examples,coverage,scopes,expected):
    s=deepcopy(next(r for r in examples['records'] if r['kind']=='snapshot'))
    s['data']['coverage']=coverage;s['data']['requested_scope']=scopes
    run,evidence=make_observation(s)
    assert evidence['data']['value']==expected


def test_config_rejects_unexpected_fields(tmp_path):
    p=tmp_path/'config.json';p.write_text(json.dumps({'connections':[],'allow_shell':True}))
    with pytest.raises(ValueError):load_config(p)


def test_config_requires_explicit_kube_context(tmp_path):
    p=tmp_path/'config.json';p.write_text(json.dumps({'connections':[{'id':'k','name':'k','kind':'kubernetes','namespaces':['default']}]}))
    with pytest.raises(ValueError,match='explicit context'):load_config(p)


def test_weak_console_token_refused(tmp_path):
    with pytest.raises(ValueError,match='at least 32'):create_app(tmp_path,token='short',testing=True)
