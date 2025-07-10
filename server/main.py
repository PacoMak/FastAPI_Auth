from fastapi import FastAPI

from server.database import SessionDep
from server.models.item_model import Item
from server.settings.config import SettingsDep
from server.routers.user import user_router
from server.database import create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/env")
def get_environment_variables(settings: SettingsDep):
    return settings


app.include_router(user_router)
