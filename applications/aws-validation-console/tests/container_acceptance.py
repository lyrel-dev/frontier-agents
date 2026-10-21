"""Build and exercise the unprivileged container with an isolated synthetic workspace."""
from __future__ import annotations
import json, subprocess, time, urllib.error, urllib.request, uuid
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def main():
    suffix = uuid.uuid4().hex[:10]
    name, volume, image = 'console-review-'+suffix, 'console-review-data-'+suffix, 'validation-console:review-'+suffix
    token = 'container-test-only-token-0123456789abcdef'
    checks = []
    def docker(*args):
        return subprocess.run(['docker', *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    def call(path, payload=None, authorized=True):
        headers = {'Authorization': 'Bearer '+token} if authorized else {}
        data = None if payload is None else json.dumps(payload).encode()
        if data is not None: headers['Content-Type'] = 'application/json'
        request = urllib.request.Request(base+path, data=data, headers=headers)
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.read()
    def check(name, passed):
        assert passed, name
        checks.append(name); print('PASS', name, flush=True)
    def start():
        docker('run', '--detach', '--name', name, '--read-only', '--cap-drop=ALL', '--security-opt=no-new-privileges', '--tmpfs', '/tmp:rw,noexec,nosuid,size=64m', '--publish', '127.0.0.1::8787', '--mount', f'type=volume,source={volume},target=/data', '--env', 'CONSOLE_TOKEN='+token, image)
        binding = json.loads(docker('inspect', name))[0]['NetworkSettings']['Ports']['8787/tcp'][0]
        return 'http://127.0.0.1:'+binding['HostPort']
    def wait():
        for _ in range(90):
            try:
                if json.loads(call('/healthz', authorized=False))['status']=='ok': return
            except (OSError, ValueError): pass
            time.sleep(1)
        raise AssertionError('Container health endpoint did not become ready')
    try:
        docker('build', '--tag', image, '.')
        docker('volume', 'create', volume)
        base = start(); wait()
        details = json.loads(docker('inspect', name))[0]
        check('container is non-root with a read-only root filesystem', details['Config']['User']=='10001:10001' and details['HostConfig']['ReadonlyRootfs'])
        try:
            call('/api/workspace', authorized=False)
            raise AssertionError('Unauthenticated API call was accepted')
        except urllib.error.HTTPError as error:
            check('container API requires its token', error.code==401)
        check('container defaults to no external connections', json.loads(call('/api/config'))['connections']==[])
        bundle = json.loads((ROOT/'examples/metrics-series.json').read_text())
        check('container imports synthetic evidence', json.loads(call('/api/import', bundle))['created']==len(bundle['records']))
        before = json.loads(call('/api/export'))
        docker('stop', name); docker('rm', name)
        base = start(); wait()
        after = json.loads(call('/api/export'))
        check('records and hashes survive container replacement', before['manifest']==after['manifest'] and len(before['records'])==len(after['records']))
        check('container backup is a SQLite database', call('/api/backup').startswith(b'SQLite format 3\x00'))
    finally:
        for args in [('rm','--force',name),('volume','rm','--force',volume),('image','rm','--force',image)]:
            subprocess.run(['docker',*args], capture_output=True)
    target = ROOT/'validation/container-acceptance.json'
    target.write_text(json.dumps({'passed':len(checks),'checks':checks,'external_connectors_tested':False},indent=2)+'\n')

if __name__ == '__main__':
    main()
