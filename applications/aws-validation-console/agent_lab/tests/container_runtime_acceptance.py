#!/usr/bin/env python3
"""Docker hosting acceptance. Empty runtime configuration; no AWS credentials.

Creates only uniquely named disposable containers and a volume. A locally
created storage marker is not incident evidence. No fault/agent API is called.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import secrets
import shutil
import sqlite3
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]


def main():
    if not shutil.which('docker'):
        raise SystemExit('Docker is required; this acceptance check does not silently skip.')
    checks = []
    prefix = 'agent-lab-accept-' + uuid.uuid4().hex[:12]
    image, volume = prefix + ':test', prefix + '-data'
    first, second = prefix + '-a', prefix + '-b'
    env = dict(os.environ)
    env['LAB_OPERATOR_TOKEN'] = secrets.token_urlsafe(32)
    env['LAB_APPROVAL_TOKEN'] = secrets.token_urlsafe(32)
    started = time.monotonic()

    def docker(*args, check=True, timeout=60, input=None):
        result = subprocess.run(['docker', *args], cwd=ROOT, env=env, input=input,
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                timeout=timeout)
        if check and result.returncode:
            # Do not echo complete docker commands or environment (tokens).
            raise RuntimeError('Docker command failed: ' + args[0] + '\n' + result.stderr[-2500:])
        return result

    def passed(label, condition):
        if not condition:
            raise AssertionError(label)
        checks.append(label)
        print('PASS', label, flush=True)

    def inspect(name):
        return json.loads(docker('inspect', name).stdout)[0]

    def request(base, path, authenticated=True):
        headers = {'Authorization': 'Bearer ' + env['LAB_OPERATOR_TOKEN']} if authenticated else {}
        req = urllib.request.Request(base + path, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=4) as response:
                return response.status, response.read()
        except urllib.error.HTTPError as exc:
            return exc.code, exc.read()

    def start_container(name):
        docker('run', '-d', '--name', name, '--label', 'agent-lab-acceptance=' + prefix,
               '--read-only', '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges:true',
               '--tmpfs', '/tmp:rw,noexec,nosuid,size=32m',
               '-e', 'LAB_OPERATOR_TOKEN', '-e', 'LAB_APPROVAL_TOKEN',
               '-e', 'AWS_EC2_METADATA_DISABLED=true',
               '-p', '127.0.0.1::8787', '-v', volume + ':/data', image)
        info = inspect(name)
        port = info['NetworkSettings']['Ports']['8787/tcp'][0]['HostPort']
        base = 'http://127.0.0.1:' + port
        deadline = time.monotonic() + 35
        while time.monotonic() < deadline:
            if not inspect(name)['State']['Running']:
                raise RuntimeError('Container exited before the service and worker became ready')
            try:
                status, raw = request(base, '/api/workspace')
                body = json.loads(raw)
                if status == 200 and body.get('worker', {}).get('state') == 'running':
                    return base, info
            except (OSError, ValueError, AttributeError):
                pass
            time.sleep(.1)
        raise RuntimeError('Container API/worker startup deadline exceeded')

    try:
        docker('version', timeout=15)
        docker('build', '-t', image, '.', timeout=300)
        docker('volume', 'create', '--label', 'agent-lab-acceptance=' + prefix, volume)
        base, info = start_container(first)
        host = info['HostConfig']
        passed('image runs non-root with a read-only root filesystem',
               info['Config']['User'] == '10001:10001' and host['ReadonlyRootfs'])
        ports = info['NetworkSettings']['Ports']['8787/tcp']
        passed('HTTP is published only on loopback', all(p['HostIp'] == '127.0.0.1' for p in ports))
        passed('container drops capabilities and cannot gain privileges',
               'ALL' in host['CapDrop'] and 'no-new-privileges:true' in host['SecurityOpt'])
        passed('no credential directories or runtime sockets are mounted',
               all(m['Type'] == 'volume' and m['Name'] == volume and m['Destination'] == '/data'
                   for m in info['Mounts']))
        passed('workspace and metrics require authentication',
               request(base, '/api/workspace', False)[0] == 401
               and request(base, '/api/metrics', False)[0] == 401)
        configuration = json.loads(request(base, '/api/config')[1])
        passed('container starts with no bindings and AWS execution disabled',
               configuration['bindings'] == [] and configuration['write_enabled'] is False)
        workspace = json.loads(request(base, '/api/workspace')[1])
        passed('fresh workspace has no scenarios, trials or source observations',
               workspace['entities'] == [] and workspace['experiments'] == [] and workspace['records'] == [])
        passed('empty metrics export has no invented samples',
               all(not line or line.startswith('#') for line in request(base, '/api/metrics')[1].decode().splitlines()))
        result = docker('exec', first, 'python', '-c',
                        "from pathlib import Path; assert not Path('/app/tests').exists()")
        passed('test fixture directory is absent from the runtime image', result.returncode == 0)
        duplicate = docker('exec', '-e', 'LAB_PORT=8788', first, 'python', 'run.py',
                           '--with-worker', '--data', '/data', check=False, timeout=12)
        passed('second combined process fails before serving when the worker lock is owned',
               duplicate.returncode != 0 and 'already owns' in duplicate.stderr
               and request(base, '/healthz', False)[0] == 200)
        marker_id = 'hosting-acceptance-' + uuid.uuid4().hex
        script = ("import json\nfrom lab.store import Store\n"
                  "r=Store('/data').put_record('hosting_acceptance','container-test',"
                  + repr({'purpose': 'Ephemeral storage test; not incident evidence', 'nonce': uuid.uuid4().hex})
                  + ',' + repr(marker_id) + ")\nprint(json.dumps(r))\n")
        marker = json.loads(docker('exec', '-i', first, 'python', '-', input=script).stdout)
        _, raw_backup = request(base, '/api/backup')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'backup.sqlite3'; path.write_bytes(raw_backup)
            with sqlite3.connect(path) as db:
                valid = db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
                saved = db.execute('SELECT sha256 FROM records WHERE id=?', (marker_id,)).fetchone()[0]
            passed('backup is a consistent SQLite database containing the recorded hash', valid and saved == marker['sha256'])
        docker('kill', '--signal', 'KILL', first)
        docker('rm', first)
        base, info = start_container(second)
        record = json.loads(request(base, '/api/records/' + marker_id)[1])
        passed('record data and hash survive abrupt idle-container replacement',
               record['sha256'] == marker['sha256'] and record['data'] == marker['data'])
        workspace = json.loads(request(base, '/api/workspace')[1])
        passed('replacement worker reacquires ownership without creating a trial',
               workspace['worker']['state'] == 'running' and workspace['entities'] == [])
        docker('stop', '-t', '40', second, timeout=50)
        passed('SIGTERM drains the combined process and exits successfully', inspect(second)['State']['ExitCode'] == 0)
        # WAL readers may need a shared-memory sidecar even with mode=ro.
        # The application has stopped. Copy its DB and WAL to disposable writable
        # storage, leaving the mounted workspace read-only; never ignore the WAL.
        read_only = """import json,shutil,sqlite3,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as directory:
    for name in ('experiments.sqlite3','experiments.sqlite3-wal'):
        source=Path('/data')/name
        if source.exists(): shutil.copyfile(source,Path(directory)/name)
    with sqlite3.connect(str(Path(directory)/'experiments.sqlite3')) as db:
        assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
        print(db.execute("SELECT data FROM metadata WHERE key='worker'").fetchone()[0])
"""
        last = json.loads(docker('run', '--rm', '--network', 'none', '--read-only',
                                 '--tmpfs', '/tmp:rw,noexec,nosuid,size=32m',
                                 '-v', volume + ':/data:ro', '--entrypoint', 'python', image, '-c', read_only).stdout)
        passed('graceful shutdown persists a stopped worker heartbeat', last['state'] == 'stopped')
        report = {'schema': 'agent-lab.container-runtime/v1', 'passed': len(checks), 'checks': checks,
                  'image_id': info['Image'], 'duration_seconds': round(time.monotonic()-started, 2),
                  'configuration': 'empty; AWS execution disabled', 'aws_accounts_accessed': False,
                  'faults_started': 0, 'workload': 'no workload; ephemeral storage marker only',
                  'not_verified': ['Active AWS-operation crash recovery', 'Actual agent response or prevention',
                                   'Podman or Kubernetes hosting', 'External IAM and credential refresh']}
        output = ROOT / 'validation' / 'container-runtime.json'
        output.parent.mkdir(exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + '\n')
        print(json.dumps(report, indent=2), flush=True)
    finally:
        for name in (first, second):
            docker('rm', '-f', name, check=False)
        docker('volume', 'rm', volume, check=False)
        docker('image', 'rm', image, check=False)


if __name__ == '__main__':
    main()
