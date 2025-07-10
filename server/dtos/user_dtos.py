from server.models.user_model import UserBase
import uuid


class UserPublic(UserBase):
    id: uuid.UUID


class UserCreate(UserBase):
    password: str
