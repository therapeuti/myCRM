"""
주문-상품 API CRUD 작업
"""

from sqlalchemy.orm import Session
from app.database.models import Orderitem
from app.schemas import OrderitemCreate


def get_orderitem(db: Session, orderitem_id: str) -> Orderitem:
    """특정 주문-상품 조회"""
    return db.query(Orderitem).filter(Orderitem.id == orderitem_id).first()


def get_orderitems(db: Session, skip: int = 0, limit: int = 10) -> list[Orderitem]:
    """모든 주문-상품 조회 (페이지네이션)"""
    return db.query(Orderitem).offset(skip).limit(limit).all()


def get_orderitems_by_order(db: Session, order_id: str) -> list[Orderitem]:
    """특정 주문의 모든 상품 조회"""
    return db.query(Orderitem).filter(Orderitem.order_id == order_id).all()


def create_orderitem(db: Session, orderitem: OrderitemCreate) -> Orderitem:
    """새 주문-상품 생성"""
    db_orderitem = Orderitem(**orderitem.dict())
    db.add(db_orderitem)
    db.commit()
    db.refresh(db_orderitem)
    return db_orderitem


def delete_orderitem(db: Session, orderitem_id: str) -> bool:
    """주문-상품 삭제"""
    db_orderitem = get_orderitem(db, orderitem_id)
    if db_orderitem:
        db.delete(db_orderitem)
        db.commit()
        return True
    return False
