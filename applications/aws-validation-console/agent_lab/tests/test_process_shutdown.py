"""Actual loopback process shutdown; empty configuration and no AWS access."""
import time
import pytest


@pytest.mark.parametrize('signal_name', ['SIGTERM', 'SIGINT'])
def test_foreground_signal_drains_worker_before_exit(tmp_path, signal_name):
    import json
    import os
    from pathlib import Path
    import signal
    import socket
    import subprocess
    import sys
    import urllib.request
    from lab.store import Store
    root = Path(__file__).resolve().parents[1]
    cfg = tmp_path / 'config.json'; cfg.write_text('{"bindings":[]}')
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0)); port = sock.getsockname()[1]
    env = dict(os.environ, LAB_OPERATOR_TOKEN='operator-test-' + 'x'*32,
               LAB_APPROVAL_TOKEN='approval-test-' + 'y'*32,
               LAB_BIND='127.0.0.1', LAB_PORT=str(port), AWS_EC2_METADATA_DISABLED='true')
    process = subprocess.Popen([sys.executable, str(root/'run.py'), '--with-worker',
        '--config', str(cfg), '--data', str(tmp_path/'data')], cwd=root, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        ready = False
        for _ in range(100):
            assert process.poll() is None, 'Combined process exited during startup'
            try:
                req = urllib.request.Request(f'http://127.0.0.1:{port}/api/workspace',
                    headers={'Authorization': 'Bearer ' + env['LAB_OPERATOR_TOKEN']})
                with urllib.request.urlopen(req, timeout=1) as response:
                    ready = json.load(response).get('worker', {}).get('state') == 'running'
                if ready:
                    break
            except OSError:
                pass
            time.sleep(.05)
        assert ready, 'Worker/API did not become ready'
        process.send_signal(getattr(signal, signal_name))
        process.communicate(timeout=10)
        assert process.returncode == 0
        assert Store(tmp_path/'data').meta('worker')['state'] == 'stopped'
    finally:
        if process.poll() is None:
            process.kill(); process.communicate(timeout=5)


def test_shutdown_deadline_terminates_even_with_an_undrained_executor(monkeypatch, tmp_path):
    from threading import Event
    from test_runtime_guards import prepare_main
    run = prepare_main(monkeypatch, tmp_path)
    joins = []
    exits = []
    class PendingThread:
        def is_alive(self): return True
        def join(self, timeout=None): joins.append(timeout)
    class PendingWorker:
        def __init__(self, *args):
            self.finished = Event()
            self.failure = None
        def start_background(self): return PendingThread()
        def stop(self): pass
    class Server:
        def __init__(self, *args, **kwargs): self.should_exit = False
        def run(self): pass
    def terminate(status):
        exits.append(status)
        raise SystemExit(status)
    monkeypatch.setattr(run, 'Worker', PendingWorker)
    monkeypatch.setattr(run.uvicorn, 'Server', Server)
    monkeypatch.setattr(run.os, '_exit', terminate)
    with pytest.raises(SystemExit) as exc:
        run.main()
    assert exc.value.code == 1 and exits == [1] and joins == [30]
