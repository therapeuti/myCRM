"""
상품 API CRUD 작업
"""

from sqlalchemy.orm import Session
from app.database.models import Item
from app.schemas import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: str) -> Item:
    """특정 상품 조회"""
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(db: Session, skip: int = 0, limit: int = 10) -> list[Item]:
    """모든 상품 조회 (페이지네이션)"""
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: ItemCreate) -> Item:
    """새 상품 생성"""
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: str, item_update: ItemUpdate) -> Item:
    """상품 정보 수정"""
    db_item = get_item(db, item_id)
    if db_item:
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: str) -> bool:
    """상품 삭제"""
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False
