import pytest
from server.tests.user.test_user import test_user
from server.tests.user.test_user_register import create_user


async def login(async_client, user=test_user):
    login_data = {
        "username": user["name"],
        "password": user["password"],
    }

    response = await async_client.post(
        "/user/login",
        data=login_data,
    )
    return response


@pytest.mark.asyncio
async def test_login(setup_database, async_client):
    await create_user(async_client)
    response = await login(async_client)
    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(setup_database, async_client):
    login_data = {
        "name": "invalid_user",
        "password": "invalid_password",
    }
    response = await login(async_client, user=login_data)
    assert response.status_code == 401

    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Invalid credentials"
