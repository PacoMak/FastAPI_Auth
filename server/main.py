from contextlib import asynccontextmanager
from fastapi import FastAPI

from server.settings.config import SettingsDep
from server.routers.user import user_router
from server.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/env")
async def get_environment_variables(settings: SettingsDep):
    return settings


app.include_router(user_router)
