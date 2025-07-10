from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException

from server.dependencies import CurrentUserDep
from server.dtos.token_dtos import Token, TokenRefresh
from server.dtos.user_dtos import UserCreate, UserPublic
from server.models.user_model import User
from server.services.auth_service import (
    AuthServiceDep,
    login_form_schema,
)
from server.services.user_service import UserServiceDep


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me", response_model=UserPublic)
def get_current_user(currentUser: CurrentUserDep):
    return currentUser


@user_router.post("/register", response_model=UserPublic)
def register_user(
    req: UserCreate, auth_service: AuthServiceDep, user_service: UserServiceDep
):
    hash_password = auth_service.get_password_hash(req.password)
    user = User(email=req.email, name=req.name, hash_password=hash_password)
    return user_service.create_user(user)


@user_router.post("/login", response_model=Token)
def login(
    form_data: login_form_schema,
    auth_service: AuthServiceDep,
    user_service: UserServiceDep,
):
    user = user_service.get_user_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not auth_service.verify_password(form_data.password, user.hash_password):
        raise HTTPException(
            status_code=404,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_tokens(
        access_data={"sub": user.email},
        refresh_data={"sub": user.email},
    )


@user_router.post("/refresh", response_model=Token)
def refresh(
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
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return auth_service.create_tokens(
        access_data={"sub": user.email},
        refresh_data={"sub": user.email},
    )


@user_router.patch("/me", response_model=UserPublic)
def update_user():
    pass
