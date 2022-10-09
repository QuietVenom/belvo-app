from schemas.base import BaseUser


class UserRegisterIn(BaseUser):
    password: str
    first_name: str
    last_name: str


class UserLoginIn(BaseUser):
    password: str
