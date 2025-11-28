"""
매장 API 라우터
매장 조회, 생성, 수정, 삭제 엔드포인트
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.session import get_db
from app.database.models import Store
from app.schemas import StoreCreate, StoreUpdate, StoreResponse
from . import crud
import math

router = APIRouter(prefix='/stores', tags=['Stores'])


@router.get('/')
async def list_stores(
    page: int = 1,
    id: Optional[str] = None,
    name: Optional[str] = None,
    address: Optional[str] = None,
    type: Optional[str] = None,
    orderby: str = 'name',
    db: Session = Depends(get_db)
):
    """
    모든 매장 조회 (페이지네이션)

    - **page**: 페이지 번호 (기본값: 1)
    - **id**: 매장 ID 검색 (LIKE)
    - **name**: 매장 이름 검색 (LIKE)
    - **address**: 주소 검색 (LIKE)
    - **type**: 매장 타입 필터 (정확히 일치)
    - **orderby**: 정렬 기준 (id, name, type, address)
    """
    number_per_page = 10

    # 페이지 검증
    if page < 1:
        page = 1

    # WHERE 조건 구성
    where = []
    if id:
        where.append(Store.id.like(f'%{id}%'))
    if name:
        where.append(Store.name.like(f'%{name}%'))
    if address:
        where.append(Store.address.like(f'%{address}%'))
    if type:
        where.append(Store.type == type)

    # ORDER BY 설정
    orderby_map = {
        'id': Store.id,
        'type': Store.type,
        'name': Store.name,
        'address': Store.address
    }
    orderby_column = orderby_map.get(orderby, Store.name)

    # 오프셋 계산
    offset_num = (page - 1) * number_per_page

    # 쿼리 실행
    if len(where) == 0:
        stores = db.query(Store).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_stores = db.query(Store).count()
    else:
        stores = db.query(Store).filter(and_(*where)).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_stores = db.query(Store).filter(and_(*where)).count()

    # 결과 변환
    stores_dict = [s.to_dict() for s in stores] if stores else []

    # 총 페이지 수 계산
    end_page = math.ceil(count_stores / number_per_page) if count_stores > 0 else 0

    # 페이지 범위 검증
    if end_page != 0 and page > end_page:
        raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다")

    # 매장 타입 목록 조회
    store_types = db.query(Store.type).distinct().all()
    store_types = [s[0] for s in store_types]

    return {
        'stores': stores_dict,
        'end_page': end_page,
        'store_types': store_types
    }


@router.get('/{store_id}', response_model=StoreResponse)
async def get_store(
    store_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 매장 조회

    - **store_id**: 매장 ID
    """
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="매장을 찾을 수 없습니다")
    return store


@router.post('/', response_model=StoreResponse, status_code=201)
async def create_store(
    store: StoreCreate,
    db: Session = Depends(get_db)
):
    """
    새 매장 생성

    - **id**: 매장 ID (필수)
    - **type**: 매장 타입 (필수)
    - **name**: 매장명 (필수)
    - **address**: 주소 (필수)
    """
    # 중복 확인
    existing_store = crud.get_store(db, store.id)
    if existing_store:
        raise HTTPException(status_code=400, detail="이미 존재하는 매장입니다")

    return crud.create_store(db, store)


@router.put('/{store_id}', response_model=StoreResponse)
async def update_store(
    store_id: str,
    store_update: StoreUpdate,
    db: Session = Depends(get_db)
):
    """
    매장 정보 수정

    - **store_id**: 매장 ID
    - **type**: 매장 타입 (선택사항)
    - **name**: 매장명 (선택사항)
    - **address**: 주소 (선택사항)
    """
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="매장을 찾을 수 없습니다")

    return crud.update_store(db, store_id, store_update)


@router.delete('/{store_id}', status_code=204)
async def delete_store(
    store_id: str,
    db: Session = Depends(get_db)
):
    """
    매장 삭제

    - **store_id**: 매장 ID
    """
    store = crud.get_store(db, store_id)
    if not store:
        raise HTTPException(status_code=404, detail="매장을 찾을 수 없습니다")

    crud.delete_store(db, store_id)
