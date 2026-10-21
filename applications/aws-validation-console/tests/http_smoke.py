"""Actual loopback HTTP startup/restart smoke test; no external connector calls."""
from pathlib import Path
import tempfile,subprocess,sys,os,socket,time,json,urllib.request,urllib.error
ROOT=Path(__file__).resolve().parents[1]
TOKEN='http-smoke-only-token-0123456789abcdef'
results=[]
def check(name,value):
    assert value,name
    results.append({'name':name,'result':'pass'})
with tempfile.TemporaryDirectory() as td:
    with socket.socket() as s:s.bind(('127.0.0.1',0));port=s.getsockname()[1]
    base='http://127.0.0.1:'+str(port)
    env={**os.environ,'CONSOLE_DATA':str(Path(td)/'data'),'CONSOLE_CONFIG':str(ROOT/'config.json'),'CONSOLE_PORT':str(port),'CONSOLE_TOKEN':TOKEN,'CONSOLE_BIND':'127.0.0.1'}
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def req(path,body=None,auth=True):
        h={'Authorization':'Bearer '+TOKEN} if auth else {}
        if body is not None:h['Content-Type']='application/json'
        return opener.open(urllib.request.Request(base+path,data=body,headers=h),timeout=8)
    def start():
        p=subprocess.Popen([sys.executable,'run.py'],cwd=ROOT,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        for _ in range(100):
            if p.poll() is not None:raise RuntimeError('Server exited before readiness')
            try:
                with req('/healthz',auth=False) as r:
                    if r.status==200:return p
            except (OSError,urllib.error.URLError):time.sleep(.1)
        p.terminate();raise RuntimeError('Server did not become ready')
    def stop(p):
        p.terminate()
        try:p.wait(timeout=10)
        except subprocess.TimeoutExpired:p.kill();p.wait()
    p=start()
    try:
        with req('/',auth=False) as r:
            page=r.read().decode()
            check('actual HTTP serves single-file page','const APP_DATA' in page)
            check('actual HTTP sends hashed CSP',"script-src 'sha256-" in r.headers['Content-Security-Policy'])
        try:req('/api/workspace',auth=False)
        except urllib.error.HTTPError as e:check('actual HTTP rejects unauthenticated workspace',e.code==401)
        else:raise AssertionError('Expected authentication failure')
        with req('/api/workspace') as r:
            check('actual HTTP starts with catalogue',len(json.load(r)['records'])==37)
        with req('/api/import',(ROOT/'examples/synthetic-workflow.json').read_bytes()) as r:
            check('actual HTTP imports synthetic records',r.status==200)
        with req('/api/export') as r:before=json.load(r)
        check('actual HTTP exports integrity manifest',len(before['manifest'])==52)
    finally:stop(p)
    p=start()
    try:
        with req('/api/export') as r:after=json.load(r)
        check('record hashes survive real process restart',before['manifest']==after['manifest'])
        with req('/api/backup') as r:
            check('actual HTTP serves SQLite backup',r.read(16)==b'SQLite format 3\x00')
    finally:stop(p)
(ROOT/'validation/http-smoke.json').write_text(json.dumps({'checks':len(results),'passed':len(results),'scope':'Real uvicorn process and loopback HTTP; temporary local database. No AWS, engine or Kubernetes access.','results':results},indent=2))
print(f'{len(results)} HTTP smoke checks passed')
