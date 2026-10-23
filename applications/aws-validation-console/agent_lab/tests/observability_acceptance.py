#!/usr/bin/env python3
"""Exercise actual console -> Prometheus -> Grafana servers on an internal network.

AWS is not contacted. Positive telemetry is a deliberately labelled test-only
assessment in a disposable volume. No seed route or fixture is installed in the
runtime image. All containers/volumes/network names belong to this invocation.
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
PROMETHEUS = 'prom/prometheus:v3.15.0'
GRAFANA = 'grafana/grafana:13.2.4'


def main():
    if not shutil.which('docker'):
        raise SystemExit('Docker is required; telemetry acceptance cannot silently skip.')
    name = 'fis-telemetry-' + uuid.uuid4().hex[:10]
    console, prom, grafana = name + '-console', name + '-prom', name + '-grafana'
    image, network = name + ':test', name + '-net'
    checks = []
    env = dict(os.environ)
    env.update({k: secrets.token_urlsafe(32) for k in
                ('LAB_OPERATOR_TOKEN', 'LAB_APPROVAL_TOKEN', 'LAB_METRICS_TOKEN', 'GF_SECURITY_ADMIN_PASSWORD')})
    started = time.monotonic()

    def docker(*args, check=True, timeout=90, input=None):
        result = subprocess.run(['docker', *args], cwd=ROOT, env=env, text=True, input=input,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
        if check and result.returncode:
            raise RuntimeError('Docker ' + args[0] + ' failed: ' + result.stderr[-1500:])
        return result

    def passed(label, condition):
        if not condition:
            raise AssertionError(label)
        checks.append(label)
        print('PASS', label, flush=True)

    def inspect(container):
        return json.loads(docker('inspect', container).stdout)[0]

    def base(container, port):
        mapping = inspect(container)['NetworkSettings']['Ports'][str(port) + '/tcp'][0]
        assert mapping['HostIp'] == '127.0.0.1'
        # Control requests originate on the isolated network, not through host
        # NAT rules. Host loopback publication is exercised by runtime acceptance.
        host = '127.0.0.1' if container == console else ('prometheus' if container == prom else grafana)
        return 'http://' + host + ':' + str(port)

    def http(url, *, token=None, basic=None, body=None, method=None, headers=None):
        headers = dict(headers or {})
        if token: headers['Authorization'] = 'Bearer ' + token
        if basic: headers['Authorization'] = 'Basic ' + base64.b64encode(basic.encode()).decode()
        if body is not None: headers['Content-Type'] = 'application/json'
        # Secrets travel over stdin, not a process command line. This is actual
        # HTTP against the running services, not a response bridge or API mock.
        client = r'''
import json,sys,urllib.request,urllib.error
p=json.load(sys.stdin)
b=json.dumps(p['body']).encode() if p['body'] is not None else None
request=urllib.request.Request(p['url'],data=b,headers=p['headers'],method=p['method'])
try:
    with urllib.request.urlopen(request,timeout=5) as response:
        raw=response.read().decode()
        body=json.loads(raw) if 'json' in response.headers.get('Content-Type','') else raw
        print(json.dumps({'status':response.status,'body':body}))
except urllib.error.HTTPError as exc:
    print(json.dumps({'status':exc.code,'body':exc.read().decode()}))
except (OSError,ValueError) as exc:
    print(json.dumps({'status':0,'body':type(exc).__name__}))
'''
        request = {'url':url,'headers':headers,'body':body,'method':method}
        result = docker('exec','-i',console,'python','-c',client,input=json.dumps(request),check=False)
        if result.returncode:
            raise RuntimeError('Telemetry HTTP client failed: ' + result.stderr[-1500:])
        response = json.loads(result.stdout)
        return response['status'], response['body']

    def wait(predicate, label, seconds=60):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            try:
                value = predicate()
                if value: return value
            except (OSError, ValueError, KeyError, TypeError):
                pass
            time.sleep(.25)
        raise AssertionError('Timed out: ' + label)

    containers = (console, prom, grafana)
    with tempfile.TemporaryDirectory(prefix=name) as directory:
        folder = Path(directory)
        token_file = folder / 'metrics-token'
        token_file.write_text(env['LAB_METRICS_TOKEN'])
        # Host directory is private. Only this file is mounted read-only, enabling
        # the unprivileged Prometheus process to read its own scrape credential.
        token_file.chmod(0o444)
        config_file = folder / 'prometheus.yml'
        config_file.write_text(json.dumps({'global': {'scrape_interval': '1s', 'scrape_timeout': '1s'},
            'scrape_configs': [{'job_name': 'fis-validation', 'metrics_path': '/api/metrics',
              'authorization': {'type': 'Bearer', 'credentials_file': '/run/secrets/metrics-token'},
              'static_configs': [{'targets': ['console:8787']}]}]}))
        config_file.chmod(0o444)
        try:
            docker('version', timeout=15)
            docker('pull', PROMETHEUS, timeout=300)
            docker('pull', GRAFANA, timeout=300)
            docker('build', '-t', image, '.', timeout=300)
            docker('network', 'create', '--internal', '--label', 'fis-acceptance=' + name, network)
            docker('run', '-d', '--name', console, '--network', network, '--network-alias', 'console',
                   '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
                   '--tmpfs', '/tmp:rw,nosuid,noexec,size=32m',
                   '--tmpfs', '/data:rw,nosuid,noexec,uid=10001,gid=10001,mode=700,size=64m',
                   '-p', '127.0.0.1::8787', '-e', 'AWS_EC2_METADATA_DISABLED=true',
                   '-e', 'LAB_ALLOWED_HOSTS=127.0.0.1,localhost,console',
                   '-e', 'LAB_OPERATOR_TOKEN', '-e', 'LAB_APPROVAL_TOKEN', '-e', 'LAB_METRICS_TOKEN', image)
            cb = base(console, 8787)
            wait(lambda: http(cb + '/readyz')[0] == 200, 'console worker readiness')
            passed('API and worker become ready with no AWS configuration', True)
            metrics = env['LAB_METRICS_TOKEN']; operator = env['LAB_OPERATOR_TOKEN']
            passed('scrape-only credential reads metrics but cannot read workspace or create a campaign',
                   http(cb + '/api/metrics', token=metrics)[0] == 200
                   and http(cb + '/api/workspace', token=metrics)[0] == 403
                   and http(cb + '/api/fis/campaigns', token=metrics, body={})[0] == 403)
            empty = http(cb + '/api/metrics', token=metrics)[1]
            passed('new console exports no invented performance samples',
                   all(not line or line.startswith('#') for line in empty.splitlines()))
            passed('unapproved Host is rejected', http(cb + '/healthz', headers={'Host': 'other.invalid'})[0] == 400)
            docker('run', '-d', '--name', prom, '--network', network, '--network-alias', 'prometheus',
                   '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
                   '--tmpfs', '/prometheus:rw,nosuid,noexec,uid=65534,gid=65534,size=128m',
                   '-v', str(config_file) + ':/etc/prometheus/prometheus.yml:ro',
                   '-v', str(token_file) + ':/run/secrets/metrics-token:ro',
                   '-p', '127.0.0.1::9090', PROMETHEUS, '--config.file=/etc/prometheus/prometheus.yml',
                   '--storage.tsdb.path=/prometheus', '--storage.tsdb.retention.time=1h')
            pb = base(prom, 9090)
            wait(lambda: http(pb + '/-/ready')[0] == 200, 'Prometheus readiness')

            def query(expression):
                code, data = http(pb + '/api/v1/query?' + urllib.parse.urlencode({'query': expression}))
                if code != 200 or data.get('status') != 'success':
                    raise AssertionError('PromQL did not succeed')
                return data['data']['result']

            wait(lambda: any(t.get('health') == 'up' for t in http(pb + '/api/v1/targets')[1]['data']['activeTargets']),
                 'authenticated scrape')
            passed('real Prometheus scrapes through the restricted credential', True)
            passed('PromQL preserves no data for an empty workspace', query('agent_validation_probe_latency_p95_ms') == [])
            passed('Prometheus has neither the operator nor approval secret',
                   all(env[k] not in json.dumps(inspect(prom)['Config']) for k in ('LAB_OPERATOR_TOKEN', 'LAB_APPROVAL_TOKEN')))

            # Deliberate fixture: only the measured HTTP latency below is an actual
            # measurement. Account/task/business metadata is not AWS evidence.
            fixture = r'''
import http.server,json,threading,time,urllib.request
from lab.store import Store
from lab.util import iso
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);self.end_headers();self.wfile.write(b'acceptance-probe')
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
thread=threading.Thread(target=server.serve_forever);thread.start()
latency=[]
try:
    for _ in range(5):
        start=time.perf_counter()
        with urllib.request.urlopen('http://127.0.0.1:'+str(server.server_port),timeout=3) as response:
            assert response.read()==b'acceptance-probe'
        latency.append((time.perf_counter()-start)*1000)
finally:
    server.shutdown();server.server_close();thread.join()
s=Store('/data')
b=s.put_record('binding','fixture',{'agent':{'account_id':'111111111111','region':'eu-central-1'},
'workload':{'account_id':'222222222222','region':'eu-central-1'},'service_id':'acceptance-fixture',
'agent_space_id':'test-only-space','metrics':[],
'faults':[{'id':'fixture-fault','template_id':'test-only-template','template_sha256':'0'*64}]})
e=s.put_record('experiment','fixture',{'fault_id':'fixture-fault','mode':'native'})
t=s.create('trial','CLOSED',{'arm':'baseline','binding_record_id':b['id'],'experiment_ref':e['id'],'observation_ends_at':iso()})
a=s.put_record('assessment',t['id'],{'trial_id':t['id'],'evaluated_at':iso(),
'metrics':{'probe_latency_p95_ms':max(latency),'incident_to_task_seconds':None},
'business_checks':[{'id':'test-only-check','category':'data_correctness','observed':2}],
'metric_definitions':{'business_test-only-check':{'title':'TEST FIXTURE ONLY','unit':'Count'}},
'input_hashes':{b['id']:b['sha256'],e['id']:e['sha256']},
'limitations':['TEST ONLY. HTTP latency measured; all agent/account/business metadata is a fixture. No incident was tested.']})
s.update(t['id'],changes={'assessment_id':a['id']})
print(json.dumps({'trial_id':t['id'],'assessment_id':a['id'],'latency_ms':max(latency)}))
'''
            measured = json.loads(docker('exec', '-i', console, 'python', '-', input=fixture).stdout)
            values = wait(lambda: query('agent_validation_probe_latency_p95_ms'), 'measured export')
            passed('actual HTTP measurement survives console export and Prometheus scrape',
                   len(values) == 1 and abs(float(values[0]['value'][1])-measured['latency_ms']) < .000001)
            labels = values[0]['metric']
            passed('query retains frozen agent, account, template and assessment scope',
                   labels['agent_space'] == 'test-only-space' and labels['workload_account'] == '222222222222'
                   and labels['assessment'] == measured['assessment_id'] and labels['fis_template'] == 'test-only-template')
            passed('missing investigation response is not exported as zero', query('agent_validation_incident_to_task_seconds') == [])
            business = query('agent_validation_business_value')
            passed('business series preserves declared unit and measurement account',
                   len(business) == 1 and business[0]['metric']['unit'] == 'Count'
                   and business[0]['metric']['metric_account'] == '222222222222')
            passed('observation age is queryable separately from scrape recency',
                   float(query('time() - agent_validation_observed_timestamp_seconds')[0]['value'][1]) >= 0)

            docker('run', '-d', '--name', grafana, '--network', network, '--read-only',
                   '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
                   '--tmpfs', '/tmp:rw,nosuid,noexec,size=64m',
                   '--tmpfs', '/var/lib/grafana:rw,nosuid,uid=472,gid=472,size=128m',
                   '--tmpfs', '/var/log/grafana:rw,nosuid,uid=472,gid=472,size=32m',
                   '-e', 'GF_SECURITY_ADMIN_USER=acceptance', '-e', 'GF_SECURITY_ADMIN_PASSWORD',
                   '-e', 'GF_USERS_ALLOW_SIGN_UP=false', '-e', 'GF_ANALYTICS_REPORTING_ENABLED=false',
                   '-e', 'GF_ANALYTICS_CHECK_FOR_UPDATES=false', '-e', 'GF_ANALYTICS_CHECK_FOR_PLUGIN_UPDATES=false',
                   '-p', '127.0.0.1::3000', GRAFANA)
            gb = base(grafana, 3000)
            wait(lambda: http(gb + '/api/health')[0] == 200, 'Grafana readiness')
            basic = 'acceptance:' + env['GF_SECURITY_ADMIN_PASSWORD']
            code, _ = http(gb + '/api/datasources', basic=basic, body={
                'name':'Acceptance Prometheus','uid':'acceptance-prometheus','type':'prometheus',
                'access':'proxy','url':'http://prometheus:9090','jsonData':{'httpMethod':'POST'}})
            passed('Grafana registers the isolated Prometheus datasource', code == 200)
            proposed = http(cb + '/api/grafana', token=operator)[1]
            imported = json.loads(json.dumps(proposed).replace('${DS_PROMETHEUS}', 'acceptance-prometheus'))
            code, value = http(gb + '/api/dashboards/db', basic=basic, body={'dashboard': imported, 'overwrite': False})
            passed('Grafana accepts the generated runtime dashboard with business panel', code == 200 and value.get('status') == 'success')
            stored = http(gb + '/api/dashboards/uid/' + imported['uid'], basic=basic)[1]['dashboard']
            panels = [p for p in stored['panels'] if p['type'] == 'timeseries']
            passed('all metric panels and original expressions survive readback', len(panels) == 13 and
                   [p['targets'][0]['expr'] for p in panels] == [p['targets'][0]['expr'] for p in imported['panels'] if p['type'] == 'timeseries'])
            expr = next(p['targets'][0]['expr'] for p in panels if 'probe_latency_p95_ms{' in p['targets'][0]['expr'])
            expr = expr.replace('${trial:regex}', measured['trial_id']).replace('${agent_space:regex}', 'test-only-space')
            code, result = http(gb + '/api/ds/query', basic=basic, body={
                'from':str(int((time.time()-60)*1000)), 'to':str(int(time.time()*1000)),
                'queries':[{'refId':'A','datasource':{'type':'prometheus','uid':'acceptance-prometheus'},
                'expr':expr,'instant':True,'range':False,'format':'time_series','intervalMs':1000,'maxDataPoints':1000}]})
            frames = result.get('results', {}).get('A', {}).get('frames', []) if isinstance(result, dict) else []
            returned = [v for f in frames for column in f.get('data', {}).get('values', []) for v in column if isinstance(v,(int,float))]
            passed('Grafana executes generated PromQL against measured scrape data',
                   code == 200 and any(abs(v-measured['latency_ms']) < .000001 for v in returned))
            passed('telemetry tests run on an internal-only Docker network',
                   json.loads(docker('network','inspect',network).stdout)[0]['Internal'] is True)
            report = {'schema':'fis-console.observability-acceptance/v1','passed':len(checks),'checks':checks,
                'duration_seconds':round(time.monotonic()-started,2),
                'images':{c:inspect(c)['Image'] for c in containers},
                'grafana_version':http(gb+'/api/health')[1].get('version'),
                'prometheus_version':http(pb+'/api/v1/status/buildinfo')[1]['data'].get('version'),
                'promql_executed':True,'native_aws_accessed':False,
                'http_client_origin':'Actual HTTP from the console container on the isolated Docker network; host publication is verified by the separate runtime suite.',
                'measurement':'Five actual loopback HTTP requests; account, agent and business labels are isolated test fixtures.',
                'not_verified':['AWS evidence collection','Agent response and prevention','Production TLS/credentials','Podman or Kubernetes hosting']}
            out = ROOT / 'validation' / 'observability-acceptance.json'
            out.write_text(json.dumps(report, indent=2)+'\n')
            print(json.dumps(report,indent=2))
        except Exception:
            # Retain bounded diagnostics before deleting owned test containers.
            # Never print environment values or an unredacted test credential.
            for container in containers:
                logs=docker('logs',container,check=False)
                text=(logs.stdout+'\n'+logs.stderr)[-6000:]
                for key in ('LAB_OPERATOR_TOKEN','LAB_APPROVAL_TOKEN','LAB_METRICS_TOKEN','GF_SECURITY_ADMIN_PASSWORD'):
                    text=text.replace(env[key],'[REDACTED]')
                print('DIAGNOSTIC '+container+'\n'+text,flush=True)
            raise
        finally:
            for container in containers:
                docker('rm','-f',container,check=False)
            docker('network','rm',network,check=False)
            docker('image','rm',image,check=False)


if __name__ == '__main__':
    main()
