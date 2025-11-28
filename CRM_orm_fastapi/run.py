# 앱 실행 진입점

import uvicorn
from app.main import app

if __name__=='__main__':
    uvicorn.run('run:app', reload=True)