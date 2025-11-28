"""
데이터베이스 세션 관리
SQLAlchemy 엔진과 세션을 관리합니다.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from pathlib import Path

# 데이터베이스 디렉토리 생성
db_path = Path(settings.DATABASE_URL.replace("sqlite:///", ""))
db_path.parent.mkdir(parents=True, exist_ok=True)

# SQLAlchemy 엔진 생성
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 설정
    echo=False,  # SQL 쿼리 로깅 (True: 활성화)
)

# 세션 팩토리
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    의존성 주입을 위한 DB 세션 반환
    FastAPI 라우터에서 Depends(get_db)로 사용합니다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
