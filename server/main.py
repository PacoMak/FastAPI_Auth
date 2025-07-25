from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from server.settings.config import SettingsDep, get_settings
from server.routers.user import user_router
from server.database import create_db_and_tables, drop_db_and_tables
from server.routers.oauth.google import google_router
from server.routers.oauth.password import password_router
from starlette.middleware.sessions import SessionMiddleware

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


setting = get_settings()
app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=setting.secret_key)
app.mount("/static", StaticFiles(directory="server/static"), name="static")


@app.get("/env")
async def get_environment_variables(settings: SettingsDep):
    return settings


@app.get("/")
def index(req: Request):
    return templates.TemplateResponse("index.html", context={"request": req})


app.include_router(user_router)
app.include_router(google_router)
app.include_router(password_router)
