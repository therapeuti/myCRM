from fastapi import FastAPI, APIRouter
from .users import users_router
from .auth import auth_router

router = APIRouter(prefix='/api')

router.include_router(users_router)
router.include_router(auth_router)

__all__ = ['router']
