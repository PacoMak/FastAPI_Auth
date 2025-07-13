from fastapi import APIRouter, HTTPException
from server.dependencies import CurrentUserDep
from server.dtos.user_dtos import UserPublic, UserUpdate
from server.services.auth_service import (
    AuthServiceDep,
)
from server.services.user_service import UserServiceDep


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/me", response_model=UserPublic)
async def get_current_user(currentUser: CurrentUserDep):
    return currentUser


@user_router.patch("/me", response_model=UserPublic)
async def update_user(
    current_user: CurrentUserDep,
    req: UserUpdate,
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
):
    if req.name:
        current_user.name = req.name
    if not req.old_password and not req.new_password:
        return await user_service.update_user(current_user)
    if not auth_service.verify_password(req.old_password, current_user.hash_password):
        raise HTTPException(
            status_code=401,
            detail="Old password is incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    current_user.hash_password = auth_service.get_password_hash(req.new_password)
    await user_service.update_user(current_user)
    return current_user
