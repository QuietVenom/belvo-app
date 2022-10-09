from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str


class BaseLink(BaseModel):
    institution: str
    username: str
    password: str


class BaseAccount(BaseModel):
    link: str


class BaseTransaction(BaseModel):
    link: str
    date_from_YYYYMMDD: str
    date_to_YYYYMMDD: str
