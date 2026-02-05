from fastapi import FastAPI, APIRouter

router = APIRouter(prefix='/users')

@router.get('/')
def get_users():
    return {'message': 'List of users'}
