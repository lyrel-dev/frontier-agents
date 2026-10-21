"""Import and read back the generated proposal in an ephemeral Grafana server.
This checks dashboard storage, not PromQL execution or real account telemetry.
"""
from __future__ import annotations
import base64, json, subprocess, time, urllib.request, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IMAGE = 'grafana/grafana:13.2.4'


def main():
    name = 'grafana-review-'+uuid.uuid4().hex[:10]
    password = 'grafana-review-test-only-password'
    checks = []
    def docker(*args):
        return subprocess.run(['docker', *args], check=True, capture_output=True, text=True).stdout.strip()
    def call(path, payload=None):
        headers = {'Authorization':'Basic '+base64.b64encode(('admin:'+password).encode()).decode()}
        data = None if payload is None else json.dumps(payload).encode()
        if data is not None: headers['Content-Type']='application/json'
        with urllib.request.urlopen(urllib.request.Request(base+path,data=data,headers=headers),timeout=10) as response:
            return json.load(response)
    def check(name, passed):
        assert passed, name
        checks.append(name); print('PASS',name,flush=True)
    try:
        docker('run','--detach','--name',name,'--publish','127.0.0.1::3000','--env','GF_SECURITY_ADMIN_PASSWORD='+password,'--env','GF_ANALYTICS_REPORTING_ENABLED=false','--env','GF_ANALYTICS_CHECK_FOR_UPDATES=false','--env','GF_ANALYTICS_CHECK_FOR_PLUGIN_UPDATES=false','--env','GF_LOG_LEVEL=warn',IMAGE)
        binding=json.loads(docker('inspect',name))[0]['NetworkSettings']['Ports']['3000/tcp'][0]
        base='http://127.0.0.1:'+binding['HostPort']
        for _ in range(120):
            try:
                health=call('/api/health')
                if health.get('database')=='ok': break
            except (OSError,ValueError): pass
            time.sleep(1)
        else: raise AssertionError('Grafana did not become ready')
        check('Grafana database is healthy',health['database']=='ok')
        dashboard=json.loads((ROOT/'grafana/operational-readiness.json').read_text())
        result=call('/api/dashboards/db',{'dashboard':dashboard,'overwrite':True,'message':'Isolated synthetic publication check'})
        check('Grafana accepts generated dashboard JSON',result.get('status')=='success')
        saved=call('/api/dashboards/uid/'+dashboard['uid'])['dashboard']
        panels=[p for p in saved['panels'] if p['type']=='timeseries']
        check('all 33 graph panels survive import',len(panels)==33)
        check('queries survive import unchanged',[p['targets'][0]['expr'] for p in panels]==[p['targets'][0]['expr'] for p in dashboard['panels'] if p['type']=='timeseries'])
        provenance=next(v for v in saved['templating']['list'] if v['name']=='data_kind')
        check('import retains measured-data default',provenance['current']['value']=='measured')
        target=ROOT/'validation/grafana-acceptance.json'
        target.write_text(json.dumps({'image':IMAGE,'server_version':health.get('version'),'passed':len(checks),'checks':checks,'promql_executed':False,'external_telemetry_tested':False},indent=2)+'\n')
    finally:
        subprocess.run(['docker','rm','--force',name],capture_output=True)

if __name__=='__main__':
    main()
