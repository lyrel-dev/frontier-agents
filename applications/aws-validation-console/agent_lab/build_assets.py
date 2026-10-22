#!/usr/bin/env python3
"""Rebuild schemas, the empty preview and Grafana JSON without AWS or credentials."""
import json
from pathlib import Path
from build_preview import build
from lab.metrics import dashboard
from lab.models import Configuration, Experiment, CampaignRequest, Diagnosis, ChangeProposal

ROOT = Path(__file__).resolve().parent


def main():
    models = {'configuration': Configuration, 'experiment': Experiment,
              'campaign': CampaignRequest, 'diagnosis': Diagnosis, 'change': ChangeProposal}
    (ROOT / 'schemas').mkdir(exist_ok=True)
    for name, model in models.items():
        (ROOT / 'schemas' / (name + '.schema.json')).write_text(
            json.dumps(model.model_json_schema(), indent=2) + '\n', encoding='utf-8')
    (ROOT / 'grafana').mkdir(exist_ok=True)
    (ROOT / 'grafana' / 'agent-validation.json').write_text(
        json.dumps(dashboard(), indent=2) + '\n', encoding='utf-8')
    build()
    print('Built five schemas, Grafana dashboard and empty offline preview. No AWS access.')


if __name__ == '__main__':
    main()
