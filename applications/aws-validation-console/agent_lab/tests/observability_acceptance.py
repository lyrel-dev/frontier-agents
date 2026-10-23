#!/usr/bin/env python3
"""Real Docker/Prometheus/Grafana acceptance of the empty, authenticated console.

No AWS credentials, account bindings, incidents or fake measurements are used.
The servers share one isolated network namespace, with no host ports published.
HTTP assertions run inside that namespace. Tokens are sent through stdin, never
command-line arguments, committed files, or printed diagnostics.
"""
from __future__ import annotations
import base64
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
PROM_IMAGE = 'prom/prometheus:v3.15.1'
GRAFANA_IMAGE = 'grafana/grafana:13.2.4'


# Execute HTTP from inside the shared namespace. Docker internal networks need
# no host-side port mapping, and this avoids relying on daemon NAT behavior.
# Only this fixed program is passed as an argument; request credentials use stdin.
HTTP_CLIENT = r"""
import base64,json,sys,urllib.request,urllib.error
p=json.load(sys.stdin)
headers=p.get('headers',{})
body=p.get('body')
if body is not None:headers['Content-Type']='application/json'
request=urllib.request.Request('http://127.0.0.1:'+str(p['port'])+p['path'],
    data=json.dumps(body).encode() if body is not None else None,headers=headers)
try:
    with urllib.request.urlopen(request,timeout=8) as response:
        status,data=response.status,response.read()
except urllib.error.HTTPError as error:
    status,data=error.code,error.read()
except (OSError,urllib.error.URLError):
    print(json.dumps({'unavailable':True}))
    raise SystemExit(0)
print(json.dumps({'status':status,'body':base64.b64encode(data).decode()}))
"""


def namespace_http(container, port, path, body=None, headers=None, *, run=None):
    if port not in (8787,9090,3000) or not path.startswith('/') or path.startswith('//'):
        raise ValueError('Only the three local acceptance endpoints are permitted')
    run=run or subprocess.run
    payload={'port':port,'path':path,'body':body,'headers':headers or {}}
    try:
        result=run(['docker','exec','-i',container,'python','-c',HTTP_CLIENT],
                   input=json.dumps(payload),text=True,stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE,timeout=15,check=False)
    except subprocess.TimeoutExpired:
        raise OSError('Acceptance HTTP helper timed out') from None
    if result.returncode:
        # Never echo command stderr or request headers, which might include tokens.
        raise RuntimeError('Acceptance HTTP helper failed with exit '+str(result.returncode))
    try:
        response=json.loads(result.stdout)
        if not isinstance(response,dict):
            raise ValueError('Invalid response')
        if response.get('unavailable'):
            raise OSError('Local acceptance server is not ready')
        status=response['status']
        if type(status) is not int or not 100<=status<=599:
            raise ValueError('Invalid status')
        return status,base64.b64decode(response['body'],validate=True)
    except (KeyError,TypeError,ValueError):
        raise RuntimeError('Acceptance HTTP helper returned a malformed response') from None


def main():
    if not shutil.which('docker'):
        raise SystemExit('Docker is required; no acceptance result is inferred or skipped.')
    label = 'fis-observability-' + uuid.uuid4().hex[:12]
    image, network = label + ':test', label + '-network'
    app, prom, grafana = (label + suffix for suffix in ('-app', '-prom', '-grafana'))
    token, approver, password = (secrets.token_urlsafe(32) for _ in range(3))
    environment = {**os.environ, 'LAB_OPERATOR_TOKEN':token, 'LAB_APPROVAL_TOKEN':approver,
                   'GF_SECURITY_ADMIN_PASSWORD':password}
    checks=[]
    def docker(*args, check=True, timeout=60):
        r=subprocess.run(['docker',*args],cwd=ROOT,env=environment,text=True,
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
        if check and r.returncode:
            raise RuntimeError('Docker '+args[0]+' failed: '+r.stderr[-1500:])
        return r.stdout
    def passed(name, condition):
        assert condition,name
        checks.append(name);print('PASS',name,flush=True)
    def http(base,path,body=None,headers=None):
        return namespace_http(app,base,path,body,headers)
    def document(base,path,body=None,headers=None):
        status,data=http(base,path,body,headers)
        if status>=400:raise RuntimeError('HTTP '+str(status)+' for '+path.split('?')[0]+': '+data.decode()[:1000])
        return json.loads(data)
    def wait(base,path):
        end=time.monotonic()+90
        while time.monotonic()<end:
            try:
                if http(base,path)[0]==200:return
            except OSError:pass
            time.sleep(.25)
        raise RuntimeError('Readiness deadline exceeded: '+path)
    try:
        docker('version',timeout=15)
        docker('build','-t',image,'.',timeout=300)
        for dependency in (PROM_IMAGE,GRAFANA_IMAGE):docker('pull',dependency,timeout=180)
        docker('network','create','--internal',network)
        docker('run','-d','--name',app,'--network',network,'--read-only','--cap-drop','ALL',
               '--security-opt','no-new-privileges:true','--tmpfs','/tmp:rw,noexec,nosuid,size=32m',
               '--tmpfs','/data:rw,nosuid,uid=10001,gid=10001,size=64m',
               '-e','LAB_OPERATOR_TOKEN','-e','LAB_APPROVAL_TOKEN','-e','AWS_EC2_METADATA_DISABLED=true',
               image)
        info=json.loads(docker('inspect',app))[0]
        if not info['State']['Running']:
            raise RuntimeError('Acceptance application exited during startup; exit '+str(info['State'].get('ExitCode')))
        passed('observability servers use an internal network with no published host ports',
               json.loads(docker('network','inspect',network))[0]['Internal'] is True
               and not info['HostConfig'].get('PortBindings'))
        bases={port:port for port in (8787,9090,3000)}
        wait(bases[8787],'/healthz')
        auth={'Authorization':'Bearer '+token}
        passed('metrics endpoint rejects unauthenticated scrapes',http(bases[8787],'/api/metrics')[0]==401)
        metrics=http(bases[8787],'/api/metrics',headers=auth)[1].decode()
        passed('authenticated empty exporter has no invented observations',all(not l or l.startswith('#') for l in metrics.splitlines()))
        dashboard=document(bases[8787],'/api/grafana',headers=auth)
        with tempfile.TemporaryDirectory() as temporary:
            temp=Path(temporary)
            (temp/'token').write_text(token);(temp/'token').chmod(0o600)
            (temp/'prometheus.yml').write_text('global:\n  scrape_interval: 1s\nscrape_configs:\n  - job_name: console\n    metrics_path: /api/metrics\n    authorization:\n      type: Bearer\n      credentials_file: /config/token\n    static_configs:\n      - targets: ["127.0.0.1:8787"]\n')
            uid,gid=os.getuid(),os.getgid()
            docker('run','-d','--name',prom,'--network','container:'+app,'--read-only',
                   '--user',f'{uid}:{gid}','--cap-drop','ALL','--security-opt','no-new-privileges:true',
                   '--tmpfs',f'/prometheus:rw,nosuid,uid={uid},gid={gid},size=64m',
                   '-v',str(temp)+':/config:ro',PROM_IMAGE,'--config.file=/config/prometheus.yml',
                   '--storage.tsdb.path=/prometheus','--web.listen-address=0.0.0.0:9090')
            wait(bases[9090],'/-/ready')
            deadline=time.monotonic()+30;targets=[]
            while time.monotonic()<deadline:
                targets=document(bases[9090],'/api/v1/targets')['data']['activeTargets']
                if targets and all(t['health']=='up' for t in targets):break
                time.sleep(.3)
            passed('Prometheus authenticates and successfully scrapes the real console',len(targets)==1 and targets[0]['health']=='up')
            passed('Prometheus confirms no trial measurements exist',document(bases[9090],'/api/v1/query?query=agent_validation_observed_timestamp_seconds')['data']['result']==[])
            expressions=[]
            for panel in dashboard['panels']:
                for target in panel.get('targets',[]):
                    expr=target['expr'].replace('${trial:regex}','.*')
                    answer=document(bases[9090],'/api/v1/query?'+urllib.parse.urlencode({'query':expr}))
                    assert answer['status']=='success' and answer['data']['result']==[],panel['title']
                    expressions.append(expr)
            passed('every baseline dashboard expression executes in Prometheus without false samples',len(expressions)==12)
            docker('run','-d','--name',grafana,'--network','container:'+app,'--read-only','--cap-drop','ALL',
                   '--security-opt','no-new-privileges:true','--tmpfs','/tmp:rw,nosuid,size=32m',
                   '--tmpfs','/var/lib/grafana:rw,nosuid,uid=472,gid=0,size=128m',
                   '--tmpfs','/var/log/grafana:rw,nosuid,uid=472,gid=0,size=32m',
                   '-e','GF_SECURITY_ADMIN_PASSWORD','-e','GF_AUTH_ANONYMOUS_ENABLED=false',
                   '-e','GF_ANALYTICS_REPORTING_ENABLED=false','-e','GF_ANALYTICS_CHECK_FOR_UPDATES=false',
                   '-e','GF_PLUGINS_PREINSTALL_DISABLED=true',GRAFANA_IMAGE)
            wait(bases[3000],'/api/health')
            admin={'Authorization':'Basic '+base64.b64encode(('admin:'+password).encode()).decode()}
            data_source=document(bases[3000],'/api/datasources',{'name':'Console acceptance','uid':'console-prom','type':'prometheus','access':'proxy','url':'http://127.0.0.1:9090','jsonData':{'httpMethod':'POST'}},admin)
            passed('Grafana creates the actual Prometheus datasource',data_source['datasource']['uid']=='console-prom')
            # Only select the concrete datasource for this test; retain generated queries.
            configured=json.loads(json.dumps(dashboard).replace('${DS_PROMETHEUS}','console-prom'))
            saved=document(bases[3000],'/api/dashboards/db',{'dashboard':configured,'overwrite':False},admin)
            returned=document(bases[3000],'/api/dashboards/uid/'+saved['uid'],headers=admin)['dashboard']
            before=[t['expr'] for p in configured['panels'] for t in p.get('targets',[])]
            after=[t['expr'] for p in returned['panels'] for t in p.get('targets',[])]
            passed('Grafana preserves all graph panels and original queries',before==after and len(returned['panels'])==len(configured['panels']))
            for i,expr in enumerate(expressions):
                answer=document(bases[3000],'/api/ds/query',{'from':str(int((time.time()-60)*1000)), 'to':str(int(time.time()*1000)),
                    'queries':[{'refId':'A','datasource':{'type':'prometheus','uid':'console-prom'},'expr':expr,'range':True,'instant':False,'intervalMs':1000,'maxDataPoints':100}]},admin)
                result=answer['results']['A']
                assert not result.get('error') and result.get('status',200)==200,(i,result)
            passed('Grafana executes every graph query through its datasource',len(expressions)==12)
            workspace=document(bases[8787],'/api/workspace',headers=auth)
            passed('observability acceptance leaves the application workspace empty',workspace['entities']==[] and workspace['records']==[])
            versions={'prometheus':document(bases[9090],'/api/v1/status/buildinfo')['data']['version'],
                      'grafana':document(bases[3000],'/api/health')['version']}
        report={'passed':len(checks),'checks':checks,'server_versions':versions,
                'images':{img:json.loads(docker('image','inspect',img))[0]['Id'] for img in (image,PROM_IMAGE,GRAFANA_IMAGE)},
                'query_count':len(expressions),'http_transport':'real urllib HTTP inside shared isolated container namespace; no host ports','real_scrape':True,'promql_executed':True,'grafana_queries_executed':True,
                'live_aws_tested':False,'measurement_data':'none: authentic empty runtime, not injected fixtures',
                'limits':['Host integration on isolated Docker only; no live incident, workload telemetry or agent efficacy established.']}
        (ROOT/'validation').mkdir(exist_ok=True)
        (ROOT/'validation/observability-acceptance.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
    finally:
        for name in (grafana,prom,app):docker('rm','-f',name,check=False)
        docker('network','rm',network,check=False)
        docker('rmi',image,check=False)

if __name__=='__main__':main()
