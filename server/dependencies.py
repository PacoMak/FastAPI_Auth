from typing import Annotated
from fastapi import Depends, HTTPException
from server.models.user_model import User
from server.services.auth_service import AuthServiceDep, oauth2_token_scheme
from server.services.user_service import UserServiceDep


def get_current_user(
    token: Annotated[str, Depends(oauth2_token_scheme)],
    user_service: UserServiceDep,
    auth_service: AuthServiceDep,
):
    payload = auth_service.decode_jwt(token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    user = user_service.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
