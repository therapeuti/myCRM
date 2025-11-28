# 앱 실행 진입점

import uvicorn

if __name__=='__main__':
    uvicorn.run('app.main:app', reload=True)