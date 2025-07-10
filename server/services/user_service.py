from typing import Annotated
from fastapi import Depends

from server.repository.user_repository import UserRepositoryDep


class UserService:
    def __init__(self, user_repository: UserRepositoryDep):
        self.user_repository = user_repository

    def get_user_by_id(self, user_id: str):
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_username(self, username: str):
        return self.user_repository.get_user_by_username(username)

    def get_user_by_email(self, email: str):
        return self.user_repository.get_user_by_email(email)

    def update_user(self, user):
        return self.user_repository.update_user(user)

    def create_user(self, user):
        return self.user_repository.create_user(user)


UserServiceDep = Annotated[UserService, Depends()]
