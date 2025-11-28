"""
주문 API 라우터
주문 조회, 생성, 수정, 삭제 엔드포인트
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.session import get_db
from app.database.models import Order
from app.schemas import OrderCreate, OrderUpdate, OrderResponse
from . import crud
import math

router = APIRouter(prefix='/orders', tags=['Orders'])


@router.get('/')
async def list_orders(
    page: int = 1,
    id: Optional[str] = None,
    ordertime: Optional[str] = None,
    store_id: Optional[str] = None,
    user_id: Optional[str] = None,
    orderby: str = 'id',
    db: Session = Depends(get_db)
):
    """
    모든 주문 조회 (페이지네이션)

    - **page**: 페이지 번호 (기본값: 1)
    - **id**: 주문 ID 검색 (LIKE)
    - **ordertime**: 주문 시간 검색 (LIKE)
    - **store_id**: 매장 ID 검색 (LIKE)
    - **user_id**: 사용자 ID 검색 (LIKE)
    - **orderby**: 정렬 기준 (id, ordertime, store_id, user_id)
    """
    number_per_page = 10

    # 페이지 검증
    if page < 1:
        page = 1

    # WHERE 조건 구성
    where = []
    if id:
        where.append(Order.id.like(f'%{id}%'))
    if store_id:
        where.append(Order.store_id.like(f'%{store_id}%'))
    if user_id:
        where.append(Order.user_id.like(f'%{user_id}%'))
    if ordertime:
        where.append(Order.ordertime.like(f'%{ordertime}%'))

    # ORDER BY 설정
    orderby_map = {
        'id': Order.id,
        'ordertime': Order.ordertime,
        'store_id': Order.store_id,
        'user_id': Order.user_id
    }
    orderby_column = orderby_map.get(orderby, Order.id)

    # 오프셋 계산
    offset_num = (page - 1) * number_per_page

    # 쿼리 실행
    if len(where) == 0:
        orders = db.query(Order).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_orders = db.query(Order).count()
    else:
        orders = db.query(Order).filter(and_(*where)).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_orders = db.query(Order).filter(and_(*where)).count()

    # 결과 변환
    orders_dict = [o.to_dict() for o in orders] if orders else []

    # 총 페이지 수 계산
    end_page = math.ceil(count_orders / number_per_page) if count_orders > 0 else 0

    # 페이지 범위 검증
    if end_page != 0 and page > end_page:
        raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다")

    return {
        'orders': orders_dict,
        'end_page': end_page
    }


@router.get('/{order_id}', response_model=OrderResponse)
async def get_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 주문 조회

    - **order_id**: 주문 ID
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")
    return order


@router.post('/', response_model=OrderResponse, status_code=201)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    새 주문 생성

    - **id**: 주문 ID (필수)
    - **ordertime**: 주문 시간 (필수)
    - **store_id**: 매장 ID (필수)
    - **user_id**: 사용자 ID (필수)
    """
    # 중복 확인
    existing_order = crud.get_order(db, order.id)
    if existing_order:
        raise HTTPException(status_code=400, detail="이미 존재하는 주문입니다")

    return crud.create_order(db, order)


@router.put('/{order_id}', response_model=OrderResponse)
async def update_order(
    order_id: str,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """
    주문 정보 수정

    - **order_id**: 주문 ID
    - **ordertime**: 주문 시간 (선택사항)
    - **store_id**: 매장 ID (선택사항)
    - **user_id**: 사용자 ID (선택사항)
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")

    return crud.update_order(db, order_id, order_update)


@router.delete('/{order_id}', status_code=204)
async def delete_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    주문 삭제

    - **order_id**: 주문 ID
    """
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")

    crud.delete_order(db, order_id)
