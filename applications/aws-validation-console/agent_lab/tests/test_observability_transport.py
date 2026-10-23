"""Acceptance-harness transport checks; real local HTTP, no Docker or AWS needed."""
import base64
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import subprocess
import sys
import threading
from types import SimpleNamespace

import pytest
from observability_acceptance import HTTP_CLIENT, namespace_http


def output(value, *, code=0, error=''):
    return SimpleNamespace(returncode=code, stdout=json.dumps(value), stderr=error)


def test_request_credentials_use_stdin_not_process_arguments():
    captured={}
    def run(command, **options):
        captured.update(command=command, **options)
        return output({'status':200,'body':base64.b64encode(b'{}').decode()})
    assert namespace_http('owned-app',8787,'/api/metrics',headers={'Authorization':'Bearer private-test-token'},run=run)==(200,b'{}')
    assert 'private-test-token' not in ' '.join(captured['command'])
    assert json.loads(captured['input'])['headers']['Authorization']=='Bearer private-test-token'
    assert captured['command']==['docker','exec','-i','owned-app','python','-c',HTTP_CLIENT]
    assert captured['timeout']==15 and captured['check'] is False


@pytest.mark.parametrize('port,path', [(80,'/'),(8787,'//outside'),(9090,'https://outside')])
def test_only_local_acceptance_endpoints_are_allowed(port,path):
    with pytest.raises(ValueError,match='endpoints'):
        namespace_http('owned-app',port,path,run=lambda *a,**k:pytest.fail('Must not run'))


@pytest.mark.parametrize('reply', [None,[],{}, {'status':True,'body':''}, {'status':200,'body':'!invalid!'}])
def test_malformed_helper_response_has_bounded_error(reply):
    with pytest.raises(RuntimeError,match='malformed'):
        namespace_http('owned-app',8787,'/',run=lambda *a,**k:output(reply))


def test_failed_helper_does_not_echo_credentials_from_stderr():
    with pytest.raises(RuntimeError) as caught:
        namespace_http('owned-app',8787,'/',run=lambda *a,**k:output({},code=1,error='private-test-token'))
    assert 'private-test-token' not in str(caught.value)


def test_unavailable_server_is_retriable_without_echoing_the_request():
    with pytest.raises(OSError,match='not ready'):
        namespace_http('owned-app',9090,'/-/ready',run=lambda *a,**k:output({'unavailable':True}))


def test_timeout_is_retriable_and_does_not_echo_subprocess_payload():
    def run(*args,**kwargs):
        raise subprocess.TimeoutExpired(args[0],15,output='private-test-token')
    with pytest.raises(OSError) as caught:
        namespace_http('owned-app',3000,'/api/health',run=run)
    assert 'private-test-token' not in str(caught.value)


def test_fixed_helper_performs_real_authenticated_http_and_preserves_http_errors():
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            self.send_response(200 if self.headers.get('Authorization')=='Bearer test-only-token' else 401)
            self.end_headers();self.wfile.write(b'actual-response')
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    try:
        for headers,expected in [({},401),({'Authorization':'Bearer test-only-token'},200)]:
            response=subprocess.run([sys.executable,'-c',HTTP_CLIENT],input=json.dumps({
                'port':server.server_port,'path':'/actual','headers':headers}),text=True,capture_output=True,timeout=10,check=True)
            result=json.loads(response.stdout)
            assert result['status']==expected
            assert base64.b64decode(result['body'])==b'actual-response'
    finally:
        server.shutdown();server.server_close();thread.join(5)
