from fastapi import APIRouter
from . import users
from . import user_info

users_router = APIRouter()

users_router.include_router(users.router)
users_router.include_router(user_info.router)

__all__ = ['users_router']