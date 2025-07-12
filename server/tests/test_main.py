import pytest


@pytest.mark.asyncio
async def test_get_environment_variables(async_client):
    response = await async_client.get("/env")
    assert response.status_code == 200
    data = response.json()
    assert data.get("database_url") is not None
    assert data.get("secret_key") is not None
    assert data.get("algorithm") is not None
    assert data.get("mode") == "test"
