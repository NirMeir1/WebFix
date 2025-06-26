from fastapi.testclient import TestClient
from ab_tests_backend import main

client = TestClient(main.app)


def setup_module(module):
    main.DB_PATH = ':memory:'
    main.init_db()


def test_log_and_results():
    client.post('/events', json={'experiment':'cta_test','variant':'A','goal':'view'})
    client.post('/events', json={'experiment':'cta_test','variant':'A','goal':'click'})
    res = client.get('/results/cta_test')
    assert res.status_code == 200
    data = res.json()
    assert data['A']['views'] == 1
    assert data['A']['conversions'] == 1
