from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from server.dtos.token_dtos import Token, TokenRefresh
from server.dtos.user_dtos import UserCreate, UserPublic
from server.models.user_model import User
from server.services.auth_service import (
    AuthServiceDep,
    login_form_schema,
)
from server.oauth import oauth
from server.services.user_service import UserServiceDep


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
    user = await user_service.get_user_by_username(form_data.username)
    if not user:
        raise invalid_credentials
    if not auth_service.verify_password(form_data.password, user.hash_password):
        raise invalid_credentials
    return auth_service.create_tokens(
        access_data={"sub": user.email},
        refresh_data={"sub": user.email},
    )


@password_router.post("/register", response_model=UserPublic, status_code=201)
async def register_user(
    req: UserCreate, auth_service: AuthServiceDep, user_service: UserServiceDep
):
    hash_password = auth_service.get_password_hash(req.password)
    user = User(email=req.email, name=req.name, hash_password=hash_password)
    return await user_service.create_user(user)


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
    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return auth_service.create_tokens(
        access_data={"sub": user.email},
        refresh_data={"sub": user.email},
    )
