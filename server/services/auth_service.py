from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from server.dtos.token_dtos import Token
import jwt

from server.services.user_service import UserServiceDep
from server.settings.config import SettingsDep

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_token_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
login_form_schema = Annotated[OAuth2PasswordRequestForm, Depends()]


class AuthService:
    def __init__(self, user_service: UserServiceDep, setting: SettingsDep):
        self.user_service = user_service
        self.setting = setting

    def verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return pwd_context.hash(password)

    def encode_jwt(self, data: dict):
        return jwt.encode(
            data, self.setting.secret_key, algorithm=self.setting.algorithm
        )

    def decode_jwt(self, access_token: str):
        return jwt.decode(
            access_token,
            self.setting.secret_key,
            algorithms=[self.setting.algorithm],
        )

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=5)
        to_encode.update({"exp": expire})
        return self.encode_jwt(to_encode)

    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
        to_encode.update({"exp": expire})
        return self.encode_jwt(to_encode)

    def create_tokens(self, access_data: dict, refresh_data: dict):
        access_token = self.create_access_token(access_data)
        refresh_token = self.create_refresh_token(refresh_data)
        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="bearer"
        )


AuthServiceDep = Annotated[AuthService, Depends()]
