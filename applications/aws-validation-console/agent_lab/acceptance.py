#!/usr/bin/env python3
"""Local preflight and frozen-evidence audit; no experiment execution commands."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from configure import read_configuration
from lab.models import Experiment
from lab.preflight import run_preflight
from lab.acceptance import audit
from lab.store import Store
from lab.util import Blocked, error_code


def save(path, value):
    """Never overwrite an earlier acceptance report; create it owner-readable only."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as out:
        json.dump(value, out, indent=2, ensure_ascii=False, allow_nan=False)
        out.write('\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('preflight', help='Offline plan unless --read-aws is explicitly set')
    p.add_argument('--config', default='config.json')
    p.add_argument('--experiment', help='Your actual Experiment JSON; no example records are inserted')
    p.add_argument('--data', default='data')
    p.add_argument('--output', required=True)
    p.add_argument('--read-aws', action='store_true')
    p.add_argument('--probe', action='store_true', help='Send exactly one configured GET after read qualification')
    p = sub.add_parser('audit', help='Audit a consistent snapshot of existing evidence, without AWS access')
    p.add_argument('--data', required=True)
    p.add_argument('--trial', required=True)
    p.add_argument('--campaign')
    p.add_argument('--output', required=True)
    args = parser.parse_args(argv)
    try:
        if Path(args.output).exists():
            raise Blocked('Output already exists; choose a new report filename')
        if args.command == 'preflight':
            config = read_configuration(args.config)
            spec = None
            if args.experiment:
                path = Path(args.experiment)
                if path.stat().st_size > 1048576:
                    raise Blocked('Experiment file exceeds 1 MiB')
                spec = Experiment.model_validate_json(path.read_text(encoding='utf-8'))
            record = run_preflight(config, spec, Store(args.data), read_aws=args.read_aws, probe=args.probe)
            report = record['data']
            report = {**report, 'record_id': record['id'], 'record_sha256': record['sha256']}
        else:
            path = (Path(args.data) / 'experiments.sqlite3').resolve()
            if not path.is_file():
                raise Blocked('No existing workspace database; no live trial can be audited')
            # Audit a consistent copy. Never initialize or edit the operator's database.
            with tempfile.TemporaryDirectory() as temp:
                target = Path(temp) / 'experiments.sqlite3'
                with sqlite3.connect(path.as_uri() + '?mode=ro', uri=True) as source, sqlite3.connect(target) as dest:
                    source.backup(dest)
                report = audit(Store(temp), args.trial, args.campaign)
        save(args.output, report)
        print(json.dumps({'status': report['status'], 'blocking_checks': report['blocking_checks'],
                          'report': str(args.output), 'execution_authorized': False}, indent=2))
        return 0 if report['status'] in ('read_checks_passed', 'reviewable') else 2
    except (Blocked, OSError, ValueError, KeyError, sqlite3.Error) as exc:
        # Do not print Pydantic input values, credential files or SDK exception bodies.
        detail = str(exc) if isinstance(exc, Blocked) else error_code(exc)
        print(json.dumps({'status': 'blocked', 'error': detail, 'execution_authorized': False}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
