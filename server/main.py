from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from server.settings.config import SettingsDep
from server.routers.user import user_router
from server.database import create_db_and_tables
from server.routers.oauth.google import google_router
from starlette.middleware.sessions import SessionMiddleware

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key="some-random-string")
app.mount("/static", StaticFiles(directory="server/static"), name="static")


@app.get("/env")
async def get_environment_variables(settings: SettingsDep):
    return settings


@app.get("/")
def index(req: Request):
    user = req.session.get("user")
    if user:
        return RedirectResponse("/welcome")
    return templates.TemplateResponse("home.html", context={"request": req})


@app.get("/welcome")
async def welcome(request: Request):
    user = request.session.get("user")
    if user:
        return {"message": f"Welcome {user['name']}!"}
    return RedirectResponse("/")


app.include_router(user_router)
app.include_router(google_router)
