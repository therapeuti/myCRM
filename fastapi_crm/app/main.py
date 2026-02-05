# fastapi 앱 생성
from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app.api import router

app = FastAPI(debug=True)
api_router = APIRouter() # flask의 blueprint

# static 폴더 절대 경로 설정
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / 'app' / 'static'


# 페이지 라우터 없이 ~.html 경로로 페이지 서빙, CSS/JS 경로에서 static prefix 제거해야함.
# app.mount('/', StaticFiles(directory=str(STATIC_DIR), html=True), name='static')

# 
app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')

# include API routes (router has prefix='/api')
app.include_router(router)


# HTML 페이지 서빙 한꺼번에 하기
@app.get('/{path:path}') # path 타입 지정해줘야 / 들어간 중첩 경로나 index 경로도 받을 수 있음.
def user_login(path: str):

    print(f'요청 경로 : {path}')

    if path == '' or path == '/':
        file_path = 'index.html'
    
    elif 'info' in path:
        file_path = path.split('/')[0] + '_info.html' 

    else:
        file_path = path.split('/')[0] + '.html'
    
    html_file = STATIC_DIR / file_path
    print(f'파일 경로 : {html_file}')

    if html_file.exists():
        return FileResponse(html_file)