from fastapi import APIRouter
from . import admin

auth_router = APIRouter()

auth_router.include_router(admin.router)

__all__ = ['auth_router']