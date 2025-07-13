import uuid
import pytest

from server.models.user_model import User
from server.tests.conftest import get_test_session
from server.tests.user.test_user import test_user
from server.tests.user.test_user_login import login
from server.tests.user.test_user_register import create_user


async def get_refresh_token(async_client, refresh_token):
    body = {"refresh_token": refresh_token} if refresh_token else {}
    return await async_client.post("/login/password/refresh", json=body)


@pytest.mark.asyncio
async def test_user_refresh_token(setup_database, async_client):
    await create_user(async_client)
    response = await login(async_client)
    response_data = response.json()

    response = await get_refresh_token(async_client, response_data["refresh_token"])
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_user_refresh_token_unauthenticated(async_client):
    response = await get_refresh_token(async_client, None)
    assert response.status_code == 422

    response = await get_refresh_token(async_client, "invalid_refresh_token")
    assert response.status_code == 401
