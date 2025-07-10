from typing import Annotated
from fastapi import Depends
from sqlmodel import select

from server.database import SessionDep
from server.models.user_model import User


class UserRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    async def get_user_by_id(self, id: str):
        return await self.session.get(User, id)

    async def get_user_by_username(self, username: str):
        statement = select(User).where(User.name == username)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def update_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_user(self, user: User):
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


UserRepositoryDep = Annotated[UserRepository, Depends()]
