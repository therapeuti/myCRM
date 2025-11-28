from fastapi import APIRouter
from . import user_info

router = APIRouter()

router.include_router(user_info.router)

__all__ = ['router']