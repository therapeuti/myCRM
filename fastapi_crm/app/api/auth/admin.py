from fastapi import APIRouter
from fastapi.responses import RedirectResponse


router = APIRouter(prefix='/admin')

@router.post('/')
def login_admin():
    print('관리자 로그인')
    return RedirectResponse(url='/users', status_code=303) # 상태코드를 303으로 변경해야 get으로 리다이렉트가 됨. 기본 상태코드는 307
