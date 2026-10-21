"""Chart samples are supplemental evidence, not a new decision engine."""
from copy import deepcopy
import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from app.models import Bundle, EvidenceData
from app.store import Store, digest
from app.evaluator import evaluate
from build_metrics import examples, catalogue, dashboard, build
ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def metric_bundle():
    return examples()

@pytest.fixture
def series_data(metric_bundle):
    return deepcopy(next(r['data'] for r in metric_bundle['records'] if r['kind']=='evidence' and r['data'].get('series')))

def test_legacy_evidence_serialization_preserves_hash(examples):
    for record in examples['records']:
        if record['kind']=='evidence':
            before=digest(record)
            record['data']=EvidenceData.model_validate(record['data']).model_dump(mode='json')
            assert 'series' not in record['data']
            assert digest(record)==before

def test_series_roundtrip_with_manifest(tmp_path,metric_bundle):
    store=Store(tmp_path/'one');store.import_bundle(metric_bundle)
    export=store.export();other=Store(tmp_path/'two');other.import_bundle(export)
    assert export==other.export()
    assert any(r['data'].get('series') for r in export['records'])

@pytest.mark.parametrize('change',[
    lambda d:d['series']['points'].reverse(),
    lambda d:d['series']['points'].insert(0,d['series']['points'][0]),
    lambda d:d['series']['points'][0].update(at='2026-10-21T09:00:00Z'),
    lambda d:d['series']['points'][-1].update(at='2026-10-21T11:00:00Z'),
    lambda d:d['series']['points'][0].update(at='2026-10-21T10:00:00'),
    lambda d:d['series']['points'][0].update(value='3.5'),
    lambda d:d['series']['points'][0].update(value=float('nan')),
    lambda d:d['series']['points'][0].update(value=float('inf')),
    lambda d:d['series']['points'][0].update(value=True),
    lambda d:d['series'].update(points=[]),
    lambda d:d['series'].update(expected_interval_seconds=0),
    lambda d:d['series'].update(expected_interval_seconds='10'),
    lambda d:d['series']['events'][0].update(at='2026-10-21T11:00:00Z'),
    lambda d:d['series']['events'][0].update(kind='execute-command'),
    lambda d:d['series'].update(unknown='rejected'),
])
def test_reject_malformed_chart_samples(series_data,change):
    change(series_data)
    with pytest.raises(ValidationError):EvidenceData.model_validate(series_data)

def test_null_samples_are_not_coerced_to_zero(series_data):
    series_data['series']['points'][1]['value']=None
    data=EvidenceData.model_validate(series_data).model_dump(mode='json')
    assert data['series']['points'][1]['value'] is None

def test_boolean_chart_accepts_boolean_and_null(metric_bundle):
    d=next(r['data'] for r in metric_bundle['records'] if r['kind']=='evidence' and r['data']['metric']=='fault_active')
    assert EvidenceData.model_validate(d).series.points[0].value is False

def test_sample_limit(series_data):
    series_data['series']['points']*=300
    with pytest.raises(ValidationError):EvidenceData.model_validate(series_data)

def test_samples_cannot_change_scalar_verdict(tmp_path,metric_bundle):
    r=next(r for r in metric_bundle['records'] if r['kind']=='evidence' and r['data']['metric']=='request_error_ratio')
    r['data']['series']['points']=[{'at':r['data']['window_end'],'value':.99}]
    store=Store(tmp_path);store.import_bundle(metric_bundle)
    result=evaluate(store,'execution_run:example-metric-timeline@1')
    assert next(c for c in result['data']['checks'] if c['assertion_id']=='errors')['outcome']=='pass'
    assert result['data']['outcome']=='fail' # recovery scalar 240 > 180

def test_api_import_retains_series(api_client,metric_bundle):
    c,app=api_client
    assert c.post('/api/import/preview',json=metric_bundle).status_code==200
    assert c.post('/api/import',json=metric_bundle).status_code==200
    records=c.get('/api/export').json()['records']
    assert any(r['data'].get('series') for r in records)

def test_api_schema_exposes_optional_series(api_client):
    c,_=api_client;s=c.get('/api/schema').json()
    assert 'series' in s['$defs']['EvidenceData']['properties']
    assert 'series' not in s['$defs']['EvidenceData'].get('required',[])
    assert s['$defs']['Series']['properties']['points']['maxItems']==20000

def test_all_catalogue_metrics_have_grafana_graphs():
    metrics=catalogue();d=dashboard(metrics)
    panels=[p for p in d['panels'] if p['type']=='timeseries']
    assert len(metrics)==32 and len(panels)==33
    assert {p['targets'][0]['expr'] for p in panels[:-1]}=={m['promql'] for m in metrics}
    for p in panels:
        assert p['fieldConfig']['defaults']['noValue']=='No data'
        assert p['fieldConfig']['defaults']['custom']['spanNulls'] is False
        assert 'or vector(0)' not in p['targets'][0]['expr']
    assert len({p['id'] for p in d['panels']})==len(d['panels'])

def test_grafana_layout_does_not_overlap():
    panels=dashboard(catalogue())['panels']
    for i,p in enumerate(panels):
        a=p['gridPos'];assert 0<=a['x'] and a['x']+a['w']<=24
        for q in panels[i+1:]:
            b=q['gridPos'];assert a['x']+a['w']<=b['x'] or b['x']+b['w']<=a['x'] or a['y']+a['h']<=b['y'] or b['y']+b['h']<=a['y']

def test_grafana_provenance_defaults_to_measured():
    d=dashboard(catalogue());var=next(v for v in d['templating']['list'] if v['name']=='data_kind')
    assert var['current']['value']=='measured'
    for m in catalogue():
        for label in ['environment','service','deployment_model','scenario','run_id','data_kind']:
            assert label+'=~' in m['promql']

def test_generation_is_reproducible():
    first=build();second=build();assert first==second
    assert Bundle.model_validate(first['examples'])
