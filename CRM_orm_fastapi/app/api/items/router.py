"""
상품 API 라우터
상품 조회, 생성, 수정, 삭제 엔드포인트
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.session import get_db
from app.database.models import Item
from app.schemas import ItemCreate, ItemUpdate, ItemResponse
from . import crud
import math

router = APIRouter(prefix='/items', tags=['Items'])


@router.get('/')
async def list_items(
    page: int = 1,
    id: Optional[str] = None,
    name: Optional[str] = None,
    type: Optional[str] = None,
    orderby: str = 'name',
    db: Session = Depends(get_db)
):
    """
    모든 상품 조회 (페이지네이션)

    - **page**: 페이지 번호 (기본값: 1)
    - **id**: 상품 ID 검색 (LIKE)
    - **name**: 상품 이름 검색 (LIKE)
    - **type**: 상품 타입 필터 (정확히 일치)
    - **orderby**: 정렬 기준 (id, name, type, price)
    """
    number_per_page = 10

    # 페이지 검증
    if page < 1:
        page = 1

    # WHERE 조건 구성
    where = []
    if id:
        where.append(Item.id.like(f'%{id}%'))
    if name:
        where.append(Item.name.like(f'%{name}%'))
    if type:
        where.append(Item.type == type)

    # ORDER BY 설정
    orderby_map = {
        'id': Item.id,
        'type': Item.type,
        'name': Item.name,
        'price': Item.price
    }
    orderby_column = orderby_map.get(orderby, Item.name)

    # 오프셋 계산
    offset_num = (page - 1) * number_per_page

    # 쿼리 실행
    if len(where) == 0:
        items = db.query(Item).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_items = db.query(Item).count()
    else:
        items = db.query(Item).filter(and_(*where)).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_items = db.query(Item).filter(and_(*where)).count()

    # 결과 변환
    items_dict = [i.to_dict() for i in items] if items else []

    # 총 페이지 수 계산
    end_page = math.ceil(count_items / number_per_page) if count_items > 0 else 0

    # 페이지 범위 검증
    if end_page != 0 and page > end_page:
        raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다")

    # 상품 타입 목록 조회
    item_types = db.query(Item.type).distinct().all()
    item_types = [i[0] for i in item_types]

    return {
        'items': items_dict,
        'end_page': end_page,
        'item_types': item_types
    }


@router.get('/{item_id}', response_model=ItemResponse)
async def get_item(
    item_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 상품 조회

    - **item_id**: 상품 ID
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")
    return item


@router.post('/', response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db)
):
    """
    새 상품 생성

    - **id**: 상품 ID (필수)
    - **type**: 상품 타입 (필수)
    - **name**: 상품명 (필수)
    - **price**: 가격 (필수)
    """
    # 중복 확인
    existing_item = crud.get_item(db, item.id)
    if existing_item:
        raise HTTPException(status_code=400, detail="이미 존재하는 상품입니다")

    return crud.create_item(db, item)


@router.put('/{item_id}', response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_update: ItemUpdate,
    db: Session = Depends(get_db)
):
    """
    상품 정보 수정

    - **item_id**: 상품 ID
    - **type**: 상품 타입 (선택사항)
    - **name**: 상품명 (선택사항)
    - **price**: 가격 (선택사항)
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")

    return crud.update_item(db, item_id, item_update)


@router.delete('/{item_id}', status_code=204)
async def delete_item(
    item_id: str,
    db: Session = Depends(get_db)
):
    """
    상품 삭제

    - **item_id**: 상품 ID
    """
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")

    crud.delete_item(db, item_id)
