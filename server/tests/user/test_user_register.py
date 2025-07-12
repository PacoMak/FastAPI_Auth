import uuid
import pytest

from server.models.user_model import User
from server.tests.conftest import get_test_session
from server.tests.user.test_user import test_user


async def create_user(async_client):
    response = await async_client.post("/user/register", json=test_user)
    return response


@pytest.mark.asyncio
async def test_create_user(setup_database, async_client):

    response = await create_user(async_client)

    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == test_user["name"]
    assert response_data["email"] == test_user["email"]
    assert "password" not in response_data
    assert uuid.UUID(response_data["id"])

    async for session in get_test_session():
        user_id = uuid.UUID(response_data["id"])
        user = await session.get(User, user_id)
        assert user is not None
        assert user.name == test_user["name"]
        assert user.email == test_user["email"]
