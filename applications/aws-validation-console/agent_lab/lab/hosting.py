"""Local hosting controls; never accepts connection authority from the browser."""
from __future__ import annotations

import ipaddress
import os
from pathlib import Path
import re

DEFAULT_HOSTS = ('127.0.0.1', 'localhost', '[::1]', 'testserver')


def allowed_hosts(values=None):
    """Require explicit hosts, not wildcards, URLs, ports or proxy header trust."""
    if values is None:
        return list(DEFAULT_HOSTS)
    if isinstance(values, str):
        values = values.split(',')
    if not values or len(values) > 20:
        raise ValueError('Configure between one and twenty exact allowed hosts')
    result = []
    for value in values:
        if not isinstance(value, str) or any(ord(c) < 32 or ord(c) == 127 for c in value):
            raise ValueError('Invalid allowed host')
        host = value.strip().lower()
        if not host or any(c in host for c in ('*', '/', '\\', '@', '?', '#')):
            raise ValueError('Allowed hosts must be exact hostnames or IP addresses')
        if host.startswith('[') and host.endswith(']'):
            ipaddress.IPv6Address(host[1:-1])
        else:
            if ':' in host or len(host) > 253:
                raise ValueError('Allowed hosts cannot contain ports or URLs')
            for label in host.split('.'):
                if not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label):
                    raise ValueError('Invalid allowed host')
        if host not in result:
            result.append(host)
    return result


def metrics_secret(env=None):
    """Read an optional scrape-only secret. Do not log or place it in SQLite."""
    env = os.environ if env is None else env
    value, filename = env.get('LAB_METRICS_TOKEN'), env.get('LAB_METRICS_TOKEN_FILE')
    if value and filename:
        raise ValueError('Configure metrics token using either an environment value or a file, not both')
    if filename:
        with Path(filename).open('r', encoding='utf-8') as stream:
            value = stream.read(514).rstrip('\n')
    if value is None or value == '':
        return None
    if not 24 <= len(value) <= 512 or any(ord(c) < 33 or ord(c) > 126 for c in value):
        raise ValueError('Metrics token must contain 24–512 non-whitespace ASCII characters')
    return value
