#!/usr/bin/env python3
"""Summarize this CI run only. Software acceptance is not live AWS acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    'response_browser': 'browser-review.json',
    'fis_browser': 'fis-browser-review.json',
    'setup_browser': 'setup-browser.json',
    'worker_http': 'worker-http-review.json',
    'container': 'container-runtime.json',
    'observability': 'observability-acceptance.json',
}


def main():
    marker = json.loads((ROOT/'validation/current-run.json').read_text())
    epoch = marker['started_at_epoch']
    summaries = {}
    artifacts = {}
    for name, filename in FILES.items():
        p = ROOT/'validation'/filename
        if p.stat().st_mtime < epoch:
            raise AssertionError('Stale evidence: '+filename)
        data = json.loads(p.read_text())
        if data.get('passed', 0) <= 0 or data.get('passed') != len(data.get('checks', [])):
            raise AssertionError('Incomplete test evidence: '+filename)
        if name.endswith('browser'):
            if data.get('native_navigation') is not True or data.get('browser_bridge') is not False:
                raise AssertionError('Native browser acceptance is required: '+filename)
        if name == 'observability' and data.get('promql_executed') is not True:
            raise AssertionError('Actual PromQL execution is required')
        summaries[name] = data
        artifacts[filename] = hashlib.sha256(p.read_bytes()).hexdigest()
    junit = ROOT/'validation/fis-console-pytest.xml'
    if junit.stat().st_mtime < epoch:
        raise AssertionError('Stale Python test result')
    suites = list(ET.parse(junit).getroot().iter('testsuite'))
    counts = {k:sum(int(s.get(k, '0')) for s in suites) for k in ('tests','failures','errors','skipped')}
    if counts['tests'] == 0 or any(counts[k] for k in ('failures','errors','skipped')):
        raise AssertionError('Python tests must pass without skipped acceptance')
    tracked = subprocess.check_output(['git','ls-files','-z'],cwd=ROOT).decode().split('\0')
    sources = {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in tracked if p and (ROOT/p).is_file()}
    result = {'schema':'fis-console.software-acceptance/v1',
        'checked_at':datetime.now(timezone.utc).isoformat(),
        'source_commit':os.environ.get('GITHUB_SHA'),
        'workflow_run':os.environ.get('GITHUB_RUN_ID'),
        'python_tests':counts,'suites':summaries,'evidence_sha256':artifacts,'source_sha256':sources,
        'software_acceptance':'passed','live_aws_acceptance':'not_run','definition_of_done':'open',
        'limits':['AWS responses are isolated fixtures; no real account or agent was exercised.',
                  'Docker and native HTTP browser acceptance do not establish Podman or Kubernetes acceptance.',
                  'Prometheus/Grafana checks use an actual loopback latency with test-only account/business labels.',
                  'Image IDs identify tested builds; this is not an independent security review.']}
    (ROOT/'validation/software-acceptance.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'software_acceptance':result['software_acceptance'],'python':counts,
        'suites':{k:v['passed'] for k,v in summaries.items()},'live_aws_acceptance':'not_run'},indent=2))


if __name__ == '__main__':
    main()
