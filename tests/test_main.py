from fastapi.testclient import TestClient

from hookrelay_backend.main import app, bins

client = TestClient(app)


def test_health_success():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_non_existent_route():
    response = client.get("/non-exist")
    assert response.status_code == 404


def test_create_bin_returns_201_and_url():
    response = client.post("/api/bins")
    assert response.status_code == 201
    body = response.json()
    assert body["bin_id"] in bins
    assert body["url"].endswith(f"/h/{body['bin_id']}")
