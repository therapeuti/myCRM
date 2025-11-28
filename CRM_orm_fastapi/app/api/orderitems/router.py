"""
주문-상품 API 라우터
주문-상품 조회, 생성, 삭제 엔드포인트
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.session import get_db
from app.database.models import Orderitem
from app.schemas import OrderitemCreate, OrderitemResponse
from . import crud
import math

router = APIRouter(prefix='/orderitems', tags=['Orderitems'])


@router.get('/')
async def list_orderitems(
    page: int = 1,
    id: Optional[str] = None,
    order_id: Optional[str] = None,
    item_id: Optional[str] = None,
    orderby: str = 'id',
    db: Session = Depends(get_db)
):
    """
    모든 주문-상품 조회 (페이지네이션)

    - **page**: 페이지 번호 (기본값: 1)
    - **id**: 주문-상품 ID 검색 (LIKE)
    - **order_id**: 주문 ID 검색 (LIKE)
    - **item_id**: 상품 ID 검색 (LIKE)
    - **orderby**: 정렬 기준 (id, order_id, item_id)
    """
    number_per_page = 10

    # 페이지 검증
    if page < 1:
        page = 1

    # WHERE 조건 구성
    where = []
    if id:
        where.append(Orderitem.id.like(f'%{id}%'))
    if order_id:
        where.append(Orderitem.order_id.like(f'%{order_id}%'))
    if item_id:
        where.append(Orderitem.item_id.like(f'%{item_id}%'))

    # ORDER BY 설정
    orderby_map = {
        'id': Orderitem.id,
        'order_id': Orderitem.order_id,
        'item_id': Orderitem.item_id
    }
    orderby_column = orderby_map.get(orderby, Orderitem.id)

    # 오프셋 계산
    offset_num = (page - 1) * number_per_page

    # 쿼리 실행
    if len(where) == 0:
        orderitems = db.query(Orderitem).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_orderitems = db.query(Orderitem).count()
    else:
        orderitems = db.query(Orderitem).filter(and_(*where)).order_by(orderby_column).limit(number_per_page).offset(offset_num).all()
        count_orderitems = db.query(Orderitem).filter(and_(*where)).count()

    # 결과 변환
    orderitems_dict = [oi.to_dict() for oi in orderitems] if orderitems else []

    # 총 페이지 수 계산
    end_page = math.ceil(count_orderitems / number_per_page) if count_orderitems > 0 else 0

    # 페이지 범위 검증
    if end_page != 0 and page > end_page:
        raise HTTPException(status_code=404, detail="페이지를 찾을 수 없습니다")

    return {
        'orderitems': orderitems_dict,
        'end_page': end_page
    }


@router.get('/{orderitem_id}', response_model=OrderitemResponse)
async def get_orderitem(
    orderitem_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 주문-상품 조회

    - **orderitem_id**: 주문-상품 ID
    """
    orderitem = crud.get_orderitem(db, orderitem_id)
    if not orderitem:
        raise HTTPException(status_code=404, detail="주문-상품을 찾을 수 없습니다")
    return orderitem


@router.get('/order/{order_id}', response_model=list[OrderitemResponse])
async def get_orderitems_by_order(
    order_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 주문의 모든 상품 조회

    - **order_id**: 주문 ID
    """
    orderitems = crud.get_orderitems_by_order(db, order_id)
    if not orderitems:
        raise HTTPException(status_code=404, detail="해당 주문의 상품이 없습니다")
    return orderitems


@router.post('/', response_model=OrderitemResponse, status_code=201)
async def create_orderitem(
    orderitem: OrderitemCreate,
    db: Session = Depends(get_db)
):
    """
    새 주문-상품 생성

    - **id**: 주문-상품 ID (필수)
    - **order_id**: 주문 ID (필수)
    - **item_id**: 상품 ID (필수)
    """
    # 중복 확인
    existing_orderitem = crud.get_orderitem(db, orderitem.id)
    if existing_orderitem:
        raise HTTPException(status_code=400, detail="이미 존재하는 주문-상품입니다")

    return crud.create_orderitem(db, orderitem)


@router.delete('/{orderitem_id}', status_code=204)
async def delete_orderitem(
    orderitem_id: str,
    db: Session = Depends(get_db)
):
    """
    주문-상품 삭제

    - **orderitem_id**: 주문-상품 ID
    """
    orderitem = crud.get_orderitem(db, orderitem_id)
    if not orderitem:
        raise HTTPException(status_code=404, detail="주문-상품을 찾을 수 없습니다")

    crud.delete_orderitem(db, orderitem_id)
