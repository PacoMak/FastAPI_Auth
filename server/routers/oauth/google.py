from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuthError
from server.models.user_model import User
from server.oauth.oauth import oauth
from server.services.auth_service import AuthServiceDep
from server.services.user_service import UserServiceDep

google_router = APIRouter(prefix="/login", tags=["google"])


@google_router.get("/google")
async def login_via_google(request: Request):
    url = request.url_for("auth_via_google")
    return await oauth.google.authorize_redirect(request, url)


@google_router.get("/google/callback")
async def auth_via_google(
    request: Request, auth_service: AuthServiceDep, user_service: UserServiceDep
):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth error: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(
            status_code=400,
            detail="User information not found in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await user_service.get_user_by_email(user_info["email"])
    # new user
    if not user:
        user = User(
            name=user_info["name"],
            email=user_info["email"],
            google_id=user_info["sub"],
        )
        user = await user_service.create_user(user)
    # exist user(not google)
    elif not user.google_id:
        user.google_id = user_info["sub"]
        await user_service.update_user(user)
    access_token, refresh_token = auth_service.create_tokens(
        access_data={"sub": str(user.id)},
        refresh_data={"sub": str(user.id)},
    )
    response = RedirectResponse(url="/user/me")
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
