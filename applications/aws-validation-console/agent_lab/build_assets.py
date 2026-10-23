#!/usr/bin/env python3
"""Rebuild schemas, the empty preview and Grafana JSON without AWS or credentials."""
import json
from pathlib import Path
from build_preview import build
from build_aws_preview import build as build_aws
from lab.fis_campaigns import QueueRequest, AttachContract
from lab.metrics import dashboard
from lab.setup import AccountDraft, ConfigDraft, Compose
from lab.models import Configuration, Experiment, CampaignRequest, Diagnosis, ChangeProposal

ROOT = Path(__file__).resolve().parent


def main():
    models = {'configuration': Configuration, 'experiment': Experiment,
              'campaign': CampaignRequest, 'diagnosis': Diagnosis, 'change': ChangeProposal,
              'fis_campaign': QueueRequest, 'fis_contract': AttachContract,
              'account_draft':AccountDraft,'configuration_draft':ConfigDraft,'guided_plan':Compose}
    (ROOT / 'schemas').mkdir(exist_ok=True)
    for name, model in models.items():
        (ROOT / 'schemas' / (name + '.schema.json')).write_text(
            json.dumps(model.model_json_schema(), indent=2) + '\n', encoding='utf-8')
    (ROOT / 'grafana').mkdir(exist_ok=True)
    (ROOT / 'grafana' / 'agent-validation.json').write_text(
        json.dumps(dashboard(), indent=2) + '\n', encoding='utf-8')
    build()
    build_aws()
    from build_setup_preview import build as setup_preview
    setup_preview()
    print('Built schemas, Grafana dashboard and empty response/AWS/setup previews. No AWS access.')


if __name__ == '__main__':
    main()
