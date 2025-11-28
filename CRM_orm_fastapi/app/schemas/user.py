"""
사용자(User) Pydantic 스키마
요청/응답 데이터 검증 및 직렬화
"""

from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    """사용자 기본 정보"""
    name: str
    birthdate: str
    age: int
    gender: str
    address: str


class UserCreate(UserBase):
    """사용자 생성 요청"""
    id: str


class UserUpdate(BaseModel):
    """사용자 수정 요청 (모든 필드 선택사항)"""
    name: Optional[str] = None
    birthdate: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None


class UserResponse(BaseModel):
    """사용자 조회/응답"""
    id: str
    name: Optional[str] = None
    birthdate: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True  # ORM 모델 자동 변환
