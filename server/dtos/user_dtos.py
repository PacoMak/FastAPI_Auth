from typing import Optional
from pydantic import model_validator
from sqlmodel import SQLModel
from server.models.user_model import UserBase
import uuid


class UserPublic(UserBase):
    id: uuid.UUID


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    old_password: Optional[str] = None
    new_password: Optional[str] = None

    @model_validator(mode="after")
    def check_passwords(cls, values):
        old_password = values.old_password
        new_password = values.new_password
        if (old_password is None) != (new_password is None):
            raise ValueError(
                "old_password and new_password must both be provided or both be None"
            )
        return values
