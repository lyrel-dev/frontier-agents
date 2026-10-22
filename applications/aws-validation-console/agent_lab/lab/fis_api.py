"""AWS-centric HTTP view; all routes inherit the existing token/origin boundary."""
from pathlib import Path
from fastapi.responses import HTMLResponse, Response
from .fis_catalog import accounts
from .fis_campaigns import Fleet, CatalogRequest, AttachContract, QueueRequest
from .fis_benchmark import benchmark, benchmark_csv
from .util import Blocked

ROOT = Path(__file__).resolve().parents[1]


def install(app, config, store, service):
    fleet = Fleet(config, store, service=service)

    @app.get('/aws', response_class=HTMLResponse)
    def aws_home():
        return (ROOT/'static/aws.html').read_text()

    @app.get('/api/fis/accounts')
    def configured_accounts():
        return {'accounts':[{'id':a.id,'name':a.name,'account_id':a.account_id,'regions':a.regions}
                            for a in accounts(config)],
                'agents':[{'binding_id':b.id,'label':b.name,'agent_account':b.agent.account_id,
                           'agent_region':b.agent.region,'agent_space_id':b.agent_space_id,
                           'workload_account':b.workload.account_id,'workload_region':b.workload.region,
                           'service_id':b.service_id} for b in config.bindings],
                'worker':store.meta('worker'),'write_enabled':config.enable_aws_writes,
                'credential_source':'Administrator-configured AWS SDK profiles; no browser credential storage.'}

    @app.post('/api/fis/sync')
    def discover(body:CatalogRequest):
        with store.lock:
            return fleet.catalog.request(body.account_ids)

    @app.post('/api/fis/sync/{identifier}/cancel')
    def cancel_discovery(identifier:str): return fleet.catalog.cancel(identifier)

    @app.get('/api/fis/catalog')
    def catalog(): return fleet.library()

    @app.post('/api/fis/contracts')
    def attach(body:AttachContract): return fleet.attach(body)

    @app.get('/api/fis/campaigns')
    def campaigns():
        return {'campaigns':store.entities('fis_campaign'),'benchmarks':[
            {k:v for k,v in record.items() if k!='data'} for record in store.records(kind='fis_benchmark')]}

    @app.post('/api/fis/campaigns')
    def create_campaign(body:QueueRequest): return fleet.create(body)

    @app.post('/api/fis/campaigns/{identifier}/command/{command}')
    def command(identifier:str,command:str): return fleet.command(identifier,command)

    @app.get('/api/fis/campaigns/{identifier}')
    def campaign(identifier:str):
        e=store.entity(identifier)
        if e['kind']!='fis_campaign': raise Blocked('Not a FIS campaign')
        return {'campaign':e,'plan':store.record(e['data']['plan_id']),
                'trials':[t for t in reversed(store.entities('trial')) if t['data'].get('fis_campaign_id')==identifier]}

    @app.post('/api/fis/campaigns/{identifier}/benchmark')
    def freeze_benchmark(identifier:str): return benchmark(store,identifier)

    @app.get('/api/fis/benchmarks/{identifier}/csv')
    def csv_export(identifier:str):
        record=store.record(identifier)
        if record['kind']!='fis_benchmark': raise Blocked('Not a benchmark')
        return Response(benchmark_csv(record),media_type='text/csv',headers={'Content-Disposition':'attachment; filename="fis-agent-attempts.csv"'})
