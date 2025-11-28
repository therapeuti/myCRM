"""
주문(Order) Pydantic 스키마
"""

from pydantic import BaseModel
from typing import Optional, List


class OrderBase(BaseModel):
    """주문 기본 정보"""
    ordertime: str
    store_id: str
    user_id: str


class OrderCreate(OrderBase):
    """주문 생성 요청"""
    id: str


class OrderUpdate(BaseModel):
    """주문 수정 요청"""
    ordertime: Optional[str] = None
    store_id: Optional[str] = None
    user_id: Optional[str] = None


class OrderResponse(OrderBase):
    """주문 조회/응답"""
    id: str

    class Config:
        from_attributes = True


class KioskOrderRequest(BaseModel):
    """키오스크용 주문 요청"""
    user_id: str
    store_id: str
    items: List[str]  # item ID 목록
