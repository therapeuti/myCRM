"""
주문-상품(Orderitem) Pydantic 스키마
"""

from pydantic import BaseModel


class OrderitemBase(BaseModel):
    """주문상품 기본 정보"""
    order_id: str
    item_id: str


class OrderitemCreate(OrderitemBase):
    """주문상품 생성 요청"""
    id: str


class OrderitemResponse(OrderitemBase):
    """주문상품 조회/응답"""
    id: str

    class Config:
        from_attributes = True
