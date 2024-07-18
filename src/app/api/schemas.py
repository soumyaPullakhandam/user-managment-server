from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserInfoBase(BaseModel):
    email: str


class UserCreate(UserInfoBase):
    fullname: str


class SetPassword(UserInfoBase):
    password: str
    is_active: bool
    activate_on: str


class UserAuthenticate(UserInfoBase):
    password: str


class UserInfo(UserInfoBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class EmailToken(BaseModel):
    email_token: str
    password: str
