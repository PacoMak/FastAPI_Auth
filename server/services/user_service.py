from typing import Annotated
from fastapi import Depends
import uuid
from server.repository.user_repository import UserRepositoryDep


class UserService:
    def __init__(self, user_repository: UserRepositoryDep):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: uuid.UUID):
        return await self.user_repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str):
        return await self.user_repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str):
        return await self.user_repository.get_user_by_email(email)

    async def update_user(self, user):
        return await self.user_repository.update_user(user)

    async def create_user(self, user):
        return await self.user_repository.create_user(user)


UserServiceDep = Annotated[UserService, Depends()]
