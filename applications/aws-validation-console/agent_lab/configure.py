#!/usr/bin/env python3
"""Validate local configuration or fingerprint already-existing approved instruments.
This utility never creates IAM roles, FIS templates, Automation documents or tasks.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re
from pathlib import Path
import boto3
from botocore.config import Config
from lab.models import Configuration,Experiment,CampaignRequest,Diagnosis,ChangeProposal
from lab.aws import template_contract
from lab.util import digest


def read_configuration(path):
    raw=Path(path).read_text()
    # Substitute only complete JSON string placeholders; JSON encode env values.
    raw=re.sub(r'"\$\{([A-Z][A-Z0-9_]*)\}"',lambda m:json.dumps(os.environ[m[1]]) if m[1] in os.environ else m[0],raw)
    return Configuration.model_validate_json(raw)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--schema',action='store_true');g.add_argument('--check',metavar='CONFIG')
    g.add_argument('--fingerprint-fis',metavar='TEMPLATE_ID');g.add_argument('--fingerprint-runbook',metavar='DOCUMENT_ARN')
    p.add_argument('--profile');p.add_argument('--region');p.add_argument('--account');p.add_argument('--version')
    p.add_argument('--output',default='schemas')
    a=p.parse_args()
    if a.schema:
        dest=Path(a.output);dest.mkdir(parents=True,exist_ok=True)
        for name,model in [('configuration',Configuration),('experiment',Experiment),('campaign',CampaignRequest),('diagnosis',Diagnosis),('change',ChangeProposal)]:
            (dest/(name+'.schema.json')).write_text(json.dumps(model.model_json_schema(),indent=2)+'\n')
        print('Wrote five JSON schemas. No AWS access.');return
    if a.check:
        config=read_configuration(a.check)
        print(json.dumps({'bindings':len(config.bindings),'aws_writes_enabled':config.enable_aws_writes,
                          'configuration_sha256':digest(config.model_dump(mode='json')),
                          'boundary':'Syntax/reference validation only. No AWS permissions or resource behavior tested.'},indent=2));return
    if not all([a.profile,a.region,a.account]):p.error('Fingerprint reads require --profile --region and --account')
    session=boto3.Session(profile_name=a.profile)
    cfg=Config(connect_timeout=3,read_timeout=8,retries={'total_max_attempts':2},ignore_configured_endpoint_urls=True)
    identity=session.client('sts',region_name=a.region,config=cfg).get_caller_identity()
    if identity['Account']!=a.account or identity['Arn'].endswith(':root'):raise SystemExit('Unexpected or root identity; no resource read')
    if a.fingerprint_fis:
        body=session.client('fis',region_name=a.region,config=cfg).get_experiment_template(id=a.fingerprint_fis)['experimentTemplate']
        print(json.dumps({'account':a.account,'region':a.region,'template_id':a.fingerprint_fis,
                          'template_sha256':digest(template_contract(body)),'contract':template_contract(body)},indent=2,default=str))
    else:
        if not a.version or not a.version.isdigit():p.error('Runbook fingerprint requires a numeric --version')
        body=session.client('ssm',region_name=a.region,config=cfg).get_document(Name=a.fingerprint_runbook,DocumentVersion=a.version,DocumentFormat='JSON')
        print(json.dumps({'account':a.account,'document':a.fingerprint_runbook,'version':body['DocumentVersion'],
                          'content_sha256':hashlib.sha256(body['Content'].encode()).hexdigest(),
                          'boundary':'Review document parameters, effects, timeout, recovery and IAM before registering it.'},indent=2))

if __name__=='__main__':main()
