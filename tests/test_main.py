import pytest
from fastapi.testclient import TestClient

from hookrelay_backend.main import app, bins, HTTPException

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_bins():
    bins.clear()

    bins["6cadce2597d34a3eacb38f628f9712b7"] = []


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

def test_list_bin_requests():
    response = client.get("/api/bins/6cadce2597d34a3eacb38f628f9712b7/requests")
    assert response.status_code == 200

def test_list_non_existent_bin_requests():
    response = client.get("/api/bins/12345/requests")
    with pytest.raises(HTTPException):
        response = client.get("/api/bins/12345/requests")

def test_catch_all():
    bin_id = "6cadce2597d34a3eacb38f628f9712b7"

    response = client.post(f"/h/{bin_id}",json={"hello": "test"})
    assert response.status_code == 200

    assert len(bins[bin_id]) == 1
    assert bins[bin_id][0]["method"] == "POST"