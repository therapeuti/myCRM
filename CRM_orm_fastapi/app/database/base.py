"""
SQLAlchemy 기본 설정
ORM 모델의 Base 클래스를 정의합니다.
"""

from sqlalchemy.orm import declarative_base

# 모든 ORM 모델이 상속받을 Base 클래스
Base = declarative_base()
