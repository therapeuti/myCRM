"""
FastAPI CRM 실행 진입점
"""

import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        'app.main:app',
        host='127.0.0.1',
        port=8001,
        reload=True
    )
