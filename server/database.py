from typing import Annotated
from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel
from fastapi import Depends
from .models.item_model import Item
from .models.user_model import User

engine = create_engine(
    "mysql+pymysql://fastapi_user:fastapi_password@mysql:3306/fastapi_auth", echo=True
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
