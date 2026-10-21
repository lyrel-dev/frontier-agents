from copy import deepcopy
import json, sqlite3
import pytest
from pydantic import ValidationError
from app.store import Store, strict_json, digest, ref, Conflict
from app.models import Bundle


def test_catalogue_has_six_models_and_36_drafts(api_client):
    c,_=api_client
    entries=c.get('/api/workspace').json()['records']
    scenarios=[e['record'] for e in entries if e['record']['kind']=='scenario']
    assert len(scenarios)==37
    assert sum(r['data']['status']=='draft' for r in scenarios)==36
    assert {'ec2','eks-ec2','eks-fargate','ecs-ec2','ecs-fargate','lambda'} <= {m for r in scenarios for m in r['data']['models']}


def test_dry_run_does_not_write(tmp_path,examples):
    s=Store(tmp_path)
    result=s.import_bundle(examples,dry_run=True)
    assert result['committed'] is False and result['created']==15
    assert not s.all()


def test_import_is_idempotent(store,examples):
    before=len(store.all())
    result=store.import_bundle(examples)
    assert result['created']==0 and len(store.all())==before


def test_conflicting_revision_is_rejected_atomically(store,examples):
    altered=deepcopy(examples)
    altered['records'][0]['title']='Changed without revision'
    new=deepcopy(altered['records'][0]);new['id']='new-record'
    altered['records'].insert(0,new)
    before=len(store.all())
    with pytest.raises(Conflict): store.import_bundle(altered)
    assert len(store.all())==before


def test_next_revision_is_allowed(store,examples):
    r=deepcopy(examples['records'][0]);r['revision']=2;r['title']='Revised requirement'
    result=store.import_bundle({'records':[r]})
    assert result['created']==1
    assert store.get('scenario:EXAMPLE-RECOVERY@1')['record']['title']!=r['title']


def test_missing_reference_rejects(tmp_path,examples):
    s=Store(tmp_path)
    run=next(r for r in examples['records'] if r['kind']=='execution_run')
    with pytest.raises(ValueError,match='missing dependency'):s.import_bundle({'records':[run]})


def test_reference_kind_must_match(store,examples):
    r=deepcopy(next(r for r in examples['records'] if r['kind']=='evidence'))
    r['id']='wrong-kind';r['data']['run_ref']='scenario:EXAMPLE-RECOVERY@1'
    with pytest.raises(ValueError,match='must reference'):store.import_bundle({'records':[r]})


def test_repeated_reference_in_bundle_rejected(store,examples):
    r=examples['records'][0]
    with pytest.raises(ValueError,match='repeats'):store.import_bundle({'records':[r,r]})


def test_export_manifest_roundtrip(store,tmp_path):
    exported=store.export();other=Store(tmp_path/'other')
    other.import_bundle(exported)
    assert other.export()==exported
    assert all(e['meta']['origin']=='imported' for e in other.all())


def test_manifest_tamper_rejected(store,tmp_path):
    exported=store.export();exported['records'][0]['title']='Tampered'
    with pytest.raises(ValueError,match='hash mismatch'):Store(tmp_path/'other').import_bundle(exported)


def test_manifest_must_cover_all_records(store,tmp_path):
    exported=store.export();exported['manifest'].pop(next(iter(exported['manifest'])))
    with pytest.raises(ValueError,match='cover every'):Store(tmp_path/'other').import_bundle(exported)


def test_backup_and_restart_preserve_hashes(store,tmp_path):
    target=tmp_path/'backup.sqlite3';store.backup(target)
    with sqlite3.connect(target) as con: assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
    restored_dir=tmp_path/'restored';restored_dir.mkdir();target.rename(restored_dir/'workspace.sqlite3')
    restored=Store(restored_dir)
    assert restored.export()==store.export()
    assert restored.audit_entries()==store.audit_entries()


def test_existing_directory_reopen_preserves_data(store):
    reopened=Store(store.directory)
    assert reopened.export()==store.export()


@pytest.mark.parametrize('text',['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}','{"a":-Infinity}'])
def test_json_ambiguities_rejected(text):
    with pytest.raises(ValueError):strict_json(text)


@pytest.mark.parametrize('field,value',[('revision',True),('revision',0),('id','../../bad'),('simulated','bad')])
def test_invalid_identity(examples,field,value):
    r=deepcopy(examples['records'][0]);r[field]=value
    with pytest.raises(ValidationError):Bundle.model_validate({'records':[r]})


def test_unknown_fields_rejected(examples):
    r=deepcopy(examples['records'][0]);r['aws_secret_access_key']='never-store-this'
    with pytest.raises(ValidationError):Bundle.model_validate({'records':[r]})


def test_schema_rejects_unknown_revision(examples):
    with pytest.raises(ValidationError):Bundle.model_validate({**examples,'schema_version':'2.0'})


@pytest.mark.parametrize('field,value',[('window_start','2026-10-21T09:00:00'),('sample_count',0),('sample_count',True),('value','1.0'),('value',float('nan'))])
def test_invalid_evidence_values(examples,field,value):
    r=deepcopy(next(r for r in examples['records'] if r['kind']=='evidence'));r['data'][field]=value
    with pytest.raises(ValidationError):Bundle.model_validate({'records':[r]})


def test_normalized_hash_equates_integral_floats():
    assert digest({'n':42.0,'z':-0.0})==digest({'n':42,'z':0})
