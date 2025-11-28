"""
매장(Store) Pydantic 스키마
"""

from pydantic import BaseModel
from typing import Optional


class StoreBase(BaseModel):
    """매장 기본 정보"""
    type: str
    name: str
    address: str


class StoreCreate(StoreBase):
    """매장 생성 요청"""
    id: str


class StoreUpdate(BaseModel):
    """매장 수정 요청"""
    type: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None


class StoreResponse(StoreBase):
    """매장 조회/응답"""
    id: str

    class Config:
        from_attributes = True
