from fastapi import FastAPI, APIRouter
from .users import router as users_router

router = APIRouter(prefix='/api')

router.include_router(users_router)

__all__ = ['router']
