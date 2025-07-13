from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from server.dtos.token_dtos import Token, TokenRefresh
from server.dtos.user_dtos import UserCreate, UserPublic
from server.models.user_model import User
from server.services.auth_service import (
    AuthServiceDep,
    login_form_schema,
)
from server.services.user_service import UserServiceDep
import uuid


password_router = APIRouter(prefix="/login/password", tags=["password"])


@password_router.post("", response_model=Token)
async def login(
    form_data: login_form_schema,
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    invalid_credentials = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = await user_service.get_user_by_email(form_data.username)
    if not user:
        raise invalid_credentials
    if not user.hash_password:
        raise invalid_credentials
    if not auth_service.verify_password(form_data.password, user.hash_password):
        raise invalid_credentials
    access_token, refresh_token = auth_service.create_tokens(
        access_data={"sub": str(user.id)},
        refresh_data={"sub": str(user.id)},
    )
    response = RedirectResponse(url="/user/me", status_code=303)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        path="/",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        path="/",
    )
    return response


@password_router.post("/register", response_model=UserPublic, status_code=201)
async def register_user(
    req: UserCreate, auth_service: AuthServiceDep, user_service: UserServiceDep
):
    existing_user = await user_service.get_user_by_email(req.email)
    if not existing_user:
        hash_password = auth_service.get_password_hash(req.password)
        user = User(email=req.email, name=req.name, hash_password=hash_password)
        return await user_service.create_user(user)
    if existing_user and existing_user.hash_password:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    existing_user.hash_password = auth_service.get_password_hash(req.password)
    return await user_service.update_user(existing_user)


@password_router.post("/refresh", response_model=Token)
async def refresh(
    req: TokenRefresh,
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    payload = auth_service.decode_jwt(req.refresh_token)
    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    # Convert string UUID back to UUID object
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID format")
    user = await user_service.get_user_by_id(user_uuid)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return auth_service.create_tokens(
        access_data={"sub": str(user.id)},
        refresh_data={"sub": str(user.id)},
    )
