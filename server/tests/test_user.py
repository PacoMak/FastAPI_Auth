from httpx import ASGITransport, AsyncClient
import pytest
from server.database import get_session
from server.main import app
from server.models.user_model import User
from server.tests.conftest import get_test_session, setup_database, async_client
import uuid

app.dependency_overrides[get_session] = get_test_session


@pytest.mark.asyncio
async def test_create_user(setup_database, async_client):

    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "SecurePass123!",
    }

    response = await async_client.post("/user/register", json=user_data)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]
    assert "password" not in response_data
    assert "id" in response_data

    async for session in get_test_session():
        user_id = uuid.UUID(response_data["id"])
        user = await session.get(User, user_id)
        assert user is not None
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
