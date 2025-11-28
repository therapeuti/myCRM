from fastapi import APIRouter
from . import users
from . import user_info

router = APIRouter()

router.include_router(users.router)
router.include_router(user_info.router)

__all__ = ['router']