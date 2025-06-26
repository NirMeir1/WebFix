from fastapi.testclient import TestClient
from ab_tests_backend.main import app, get_db
import os
import sqlite3

# use temporary db for tests
TEST_DB = 'test_ab_events.db'

def override_db():
    conn = sqlite3.connect(TEST_DB)
    conn.row_factory = sqlite3.Row
    return conn

app.dependency_overrides[get_db] = override_db
client = TestClient(app)


def setup_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def teardown_module(module):
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_post_event():
    resp = client.post('/events', json={'experiment':'cta_test','variant':'A','goal':'view'})
    assert resp.status_code == 200
    data = resp.json()
    assert data['status'] == 'ok'
