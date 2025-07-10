from typing import Annotated
from fastapi import Depends
from sqlmodel import select

from server.database import SessionDep
from server.models.user_model import User


class UserRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def get_user_by_id(self, id: str):
        return self.session.get(User, id)

    def get_user_by_username(self, username: str):
        statement = select(User).where(User.name == username)
        return self.session.exec(statement).first()

    def get_user_by_email(self, email: str):
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def update_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def create_user(self, user: User):
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


UserRepositoryDep = Annotated[UserRepository, Depends()]
