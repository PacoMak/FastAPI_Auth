from typing import Annotated
from fastapi import Cookie, Depends, HTTPException
from server.models.user_model import User
from server.services.auth_service import AuthServiceDep
from server.services.user_service import UserServiceDep
import uuid


async def get_current_user(
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
    access_token: Annotated[str, Cookie()],
):

    payload = auth_service.decode_jwt(access_token)
    id = payload.get("sub")
    if not id:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    # Convert string UUID back to UUID object
    try:
        user_uuid = uuid.UUID(id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid user ID format")
    user = await user_service.get_user_by_id(user_uuid)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
