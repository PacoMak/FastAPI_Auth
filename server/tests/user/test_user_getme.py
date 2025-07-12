import uuid
import pytest
from server.tests.user.test_user import test_user
from server.tests.user.test_user_login import login
from server.tests.user.test_user_register import create_user


async def get_me(access_token, async_client):
    if access_token is None:
        return await async_client.get("/user/me")
    return await async_client.get(
        "/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )


@pytest.mark.asyncio
async def test_get_me(setup_database, async_client):
    await create_user(async_client)
    response = await login(async_client)
    response_data = response.json()
    access_token = response_data["access_token"]

    response = await get_me(access_token, async_client)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == test_user["name"]
    assert response_data["email"] == test_user["email"]
    assert uuid.UUID(response_data["id"])


@pytest.mark.asyncio
async def test_get_me_unauthenticated(async_client):
    response = await get_me(None, async_client)
    assert response.status_code == 401
