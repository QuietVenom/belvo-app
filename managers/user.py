from fastapi import HTTPException
from passlib.context import CryptContext
from db import database
from models import user
from asyncpg import UniqueViolationError
from managers.auth import AuthManager


pwd__context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd__context.hash(user_data["password"])
        try:
            id = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "This User already exists.")
        user_do = await database.fetch_one(user.select().where(user.c.id == id))
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"])
        )
        if not user_do:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd__context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong email or password")
        return AuthManager.encode_token(user_do), user_do["role"]