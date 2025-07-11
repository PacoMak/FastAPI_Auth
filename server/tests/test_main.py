from fastapi.testclient import TestClient
from server.main import app


client = TestClient(app)


def test_get_environment_variables():
    response = client.get("/env")
    assert response.status_code == 200
    data = response.json()
    assert data.get("database_url") is not None
    assert data.get("secret_key") is not None
    assert data.get("algorithm") is not None
