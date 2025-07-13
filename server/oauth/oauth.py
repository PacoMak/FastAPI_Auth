from authlib.integrations.starlette_client import OAuth
from server.settings.config import get_settings

setting = get_settings()
oauth = OAuth()
oauth.register(
    name="google",
    client_id=setting.google_client_id,
    client_secret=setting.google_client_secret,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        "response_type": "code",
        "redirect_uri": setting.google_redirect_uri,
    },
)

oauth.register(
    name="password",
)
