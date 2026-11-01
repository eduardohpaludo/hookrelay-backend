from fastapi.testclient import TestClient

from hookrelay_backend.main import app

client = TestClient(app)


def test_health_success():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_non_existent_route():
    response = client.get("/non-exist")
    assert response.status_code == 404
