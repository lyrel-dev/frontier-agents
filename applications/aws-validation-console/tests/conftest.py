import json, sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.store import Store
from app.server import create_app
from fastapi.testclient import TestClient
TOKEN = 'test-only-console-token-0123456789abcdef'

@pytest.fixture
def examples():
    return json.loads((ROOT/'examples/synthetic-workflow.json').read_text())

@pytest.fixture
def store(tmp_path, examples):
    s=Store(tmp_path/'store')
    s.import_bundle(examples, origin='example')
    return s

@pytest.fixture
def api_client(tmp_path):
    app=create_app(tmp_path/'app-data',token=TOKEN,testing=True)
    with TestClient(app,raise_server_exceptions=False) as c:
        c.headers['Authorization']='Bearer '+TOKEN
        yield c,app
