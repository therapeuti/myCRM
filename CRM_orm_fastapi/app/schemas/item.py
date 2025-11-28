"""
상품(Item) Pydantic 스키마
"""

from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    """상품 기본 정보"""
    type: str
    name: str
    price: int


class ItemCreate(ItemBase):
    """상품 생성 요청"""
    id: str


class ItemUpdate(BaseModel):
    """상품 수정 요청"""
    type: Optional[str] = None
    name: Optional[str] = None
    price: Optional[int] = None


class ItemResponse(ItemBase):
    """상품 조회/응답"""
    id: str

    class Config:
        from_attributes = True
