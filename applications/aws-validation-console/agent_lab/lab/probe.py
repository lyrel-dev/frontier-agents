"""Bounded real HTTP GET workload. No generated responses or unrestricted URLs.

DNS is resolved and checked against administrator-approved networks, then the
socket connects to that specific address. HTTPS still validates the hostname.
Redirects, proxy environment variables, metadata/link-local targets and response
body storage are disabled. A skipped slot is recorded, never filled in.
"""
from __future__ import annotations
import hashlib
import http.client
import ipaddress
import json
import os
import socket
import ssl
import time
from urllib.parse import urlsplit
import jmespath
from .models import Probe
from .util import iso, error_code, Blocked


class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, hostname, port, address, timeout):
        super().__init__(hostname, port, timeout=timeout, context=ssl.create_default_context())
        self.address = address
    def connect(self):
        sock = socket.create_connection((self.address,self.port),self.timeout)
        self.sock = self._context.wrap_socket(sock,server_hostname=self.host)


class PinnedHTTP(http.client.HTTPConnection):
    def __init__(self, hostname, port, address, timeout):
        super().__init__(hostname,port,timeout=timeout); self.address=address
    def connect(self):
        self.sock=socket.create_connection((self.address,self.port),self.timeout)


def permitted_addresses(spec: Probe):
    u=urlsplit(spec.url); networks=[ipaddress.ip_network(n) for n in spec.allowed_networks]
    addresses=[]
    for answer in socket.getaddrinfo(u.hostname,u.port or (443 if u.scheme=='https' else 80),type=socket.SOCK_STREAM):
        address=answer[4][0]; ip=ipaddress.ip_address(address)
        if ip.is_link_local or ip.is_multicast or ip.is_unspecified or (ip.is_loopback and not spec.allow_loopback_http):
            raise Blocked('Probe resolved to a disallowed address class')
        if not any(ip in network for network in networks):
            raise Blocked('Probe DNS result is outside the approved networks')
        if address not in addresses: addresses.append(address)
    if not addresses: raise Blocked('Probe has no approved address')
    return addresses


def request(spec: Probe, scheduled_at: str):
    start=time.monotonic(); at=iso(); conn=None
    result={'scheduled_at':scheduled_at,'at':at,'attempted':True,'success':False,
            'latency_ms':None,'status':None,'error':None,'probe_id':spec.id,'response_sha256':None}
    try:
        u=urlsplit(spec.url); address=permitted_addresses(spec)[0]
        cls=PinnedHTTPS if u.scheme=='https' else PinnedHTTP
        conn=cls(u.hostname,u.port or (443 if u.scheme=='https' else 80),address,spec.timeout_seconds)
        headers={'User-Agent':'agent-validation-console/0.3','Accept':'application/json','Connection':'close'}
        for key, env in spec.header_environment.items():
            if env not in os.environ: raise Blocked('Missing probe credential environment variable')
            value=os.environ[env]
            if '\r' in value or '\n' in value: raise Blocked('Invalid header secret')
            headers[key]=value
        path=(u.path or '/')+('?' + u.query if u.query else '')
        conn.request('GET',path,headers=headers)
        response=conn.getresponse(); body=response.read(65537)
        result['status']=response.status
        if len(body)>65536: raise Blocked('Probe response exceeded 64 KiB')
        result['response_sha256']=hashlib.sha256(body).hexdigest()
        success=response.status in spec.expected_status
        if spec.json_expression:
            success=success and jmespath.search(spec.json_expression,json.loads(body))==spec.expected_json_value
        result['success']=success
    except Exception as exc:
        result['error']=error_code(exc)
    finally:
        result['latency_ms']=round((time.monotonic()-start)*1000,3)
        result['received_at']=iso()
        if conn: conn.close()
    return result
