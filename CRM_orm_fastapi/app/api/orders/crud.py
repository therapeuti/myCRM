"""
주문 API CRUD 작업
"""

from sqlalchemy.orm import Session
from app.database.models import Order
from app.schemas import OrderCreate, OrderUpdate


def get_order(db: Session, order_id: str) -> Order:
    """특정 주문 조회"""
    return db.query(Order).filter(Order.id == order_id).first()


def get_orders(db: Session, skip: int = 0, limit: int = 10) -> list[Order]:
    """모든 주문 조회 (페이지네이션)"""
    return db.query(Order).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate) -> Order:
    """새 주문 생성"""
    db_order = Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: str, order_update: OrderUpdate) -> Order:
    """주문 정보 수정"""
    db_order = get_order(db, order_id)
    if db_order:
        update_data = order_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_order, key, value)
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: str) -> bool:
    """주문 삭제"""
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
        return True
    return False
