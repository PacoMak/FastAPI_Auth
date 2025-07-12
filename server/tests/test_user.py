import pytest
from server.database import get_session
from server.main import app
from server.models.user_model import User
from server.tests.conftest import get_test_session, setup_database, async_client
import uuid

app.dependency_overrides[get_session] = get_test_session

test_user = {
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "SecurePass123!",
}


@pytest.mark.asyncio
async def test_create_user(setup_database, async_client):

    response = await async_client.post("/user/register", json=test_user)

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


@pytest.mark.asyncio
async def test_login(setup_database, async_client):

    register_response = await async_client.post("/user/register", json=test_user)
    assert register_response.status_code == 201

    login_data = {
        "username": test_user["name"],
        "password": test_user["password"],
    }

    response = await async_client.post(
        "/user/login",
        data=login_data,
    )
    assert response.status_code == 200

    response_data = response.json()
    assert "access_token" in response_data
    assert "refresh_token" in response_data
    assert response_data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_get_me(setup_database, async_client):
    register_response = await async_client.post("/user/register", json=test_user)
    assert register_response.status_code == 201
    login_data = {
        "username": test_user["name"],
        "password": test_user["password"],
    }

    response = await async_client.post(
        "/user/login",
        data=login_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    access_token = response_data["access_token"]

    response = await async_client.get(
        "/user/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == test_user["name"]
    assert response_data["email"] == test_user["email"]
    assert uuid.UUID(response_data["id"])


@pytest.mark.asyncio
async def test_get_me_unauthenticated(async_client):
    response = await async_client.get("/user/me")
    assert response.status_code == 401
