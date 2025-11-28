"""
매장 API CRUD 작업
"""

from sqlalchemy.orm import Session
from app.database.models import Store
from app.schemas import StoreCreate, StoreUpdate


def get_store(db: Session, store_id: str) -> Store:
    """특정 매장 조회"""
    return db.query(Store).filter(Store.id == store_id).first()


def get_stores(db: Session, skip: int = 0, limit: int = 10) -> list[Store]:
    """모든 매장 조회 (페이지네이션)"""
    return db.query(Store).offset(skip).limit(limit).all()


def create_store(db: Session, store: StoreCreate) -> Store:
    """새 매장 생성"""
    db_store = Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store


def update_store(db: Session, store_id: str, store_update: StoreUpdate) -> Store:
    """매장 정보 수정"""
    db_store = get_store(db, store_id)
    if db_store:
        update_data = store_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_store, key, value)
        db.commit()
        db.refresh(db_store)
    return db_store


def delete_store(db: Session, store_id: str) -> bool:
    """매장 삭제"""
    db_store = get_store(db, store_id)
    if db_store:
        db.delete(db_store)
        db.commit()
        return True
    return False
