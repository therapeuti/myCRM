# FastAPI 앱 생성 및 설정

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from pathlib import Path
from app.core.config import settings
from app.database.base import Base
from app.database.session import engine
from app.api import router

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.API_DESCRIPTION,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

# CORS 미들웨어
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 정적 파일 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / 'app' / 'static'

# 정적 파일 마운트 (CSS, JS, 이미지 등)
app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')

# API 라우터 등록 (HTML catch-all보다 먼저 등록되어야 API가 우선순위를 가짐)
app.include_router(router)

# 로그인 엔드포인트
@app.post('/user_login')
async def user_login(request: Request):
    """사용자 로그인 (form data)"""
    from app.database.session import SessionLocal
    from app.database.models import User

    form_data = await request.form()
    user_id = form_data.get('id')

    db = SessionLocal()
    try:
        login_user = db.query(User).filter(User.id == user_id).first()
        if not login_user:
            return RedirectResponse(url='/?message=로그인 실패', status_code=302)
        else:
            return RedirectResponse(url=f'/kiosk/{user_id}', status_code=302)
    finally:
        db.close()

# HTML 페이지 서빙 (catch-all route - 가장 나중에 등록)
@app.get('/{path:path}')
def serve_html(path: str):
    """HTML 페이지 서빙"""
    print(f'요청 경로 : {path}')

    # API 요청은 처리하지 않음
    if path.startswith('api/'):
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Not found")

    if path == '' or path == '/':
        file_path = 'index.html'
    else:
        path_parts = path.split('/')
        resource = path_parts[0]  # users, stores, items 등

        # /user/info/xxx, /store/info/xxx, /item/info/xxx, /order/info/xxx 형식
        if len(path_parts) > 1 and path_parts[1] == 'info':
            # user -> user_info.html, store -> store_info.html 등
            file_path = resource + '_info.html'
        # /items는 items_index.html
        elif resource == 'items':
            file_path = 'items_index.html'
        # /orderitems는 orderitems.html
        elif resource == 'orderitems':
            file_path = 'orderitems.html'
        # 기타: users.html, stores.html, orders.html 등
        else:
            file_path = resource + '.html'

    html_file = STATIC_DIR / file_path
    print(f'파일 경로 : {html_file}')

    if html_file.exists():
        return FileResponse(html_file)

    # 파일이 없으면 index.html
    return FileResponse(STATIC_DIR / 'index.html')