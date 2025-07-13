from pydantic import EmailStr
from sqlmodel import Field, SQLModel
import uuid


class UserBase(SQLModel):
    name: str = Field(max_length=100, nullable=False)
    email: EmailStr = Field(max_length=100, nullable=False)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    google_id: str = Field(max_length=100, nullable=True)
    hash_password: str = Field(max_length=60, nullable=True)
