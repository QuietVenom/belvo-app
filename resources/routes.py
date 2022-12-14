from fastapi import APIRouter
from resources import auth, belvo


api_router = APIRouter()


api_router.include_router(auth.router)
api_router.include_router(belvo.router)
