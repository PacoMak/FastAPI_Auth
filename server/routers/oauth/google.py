from fastapi import APIRouter
from starlette.requests import Request
from authlib.integrations.starlette_client import OAuthError
from server.oauth.oauth import oauth

google_router = APIRouter(prefix="/login", tags=["google"])


@google_router.get("/google")
async def login_via_google(request: Request):
    url = request.url_for("auth_via_google")
    return await oauth.google.authorize_redirect(request, url)


@google_router.get("/google/callback")
async def auth_via_google(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return {"error": e.error}
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
        return {"user": user}
    return {"error": "User information not found"}
