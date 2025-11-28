"""
사용자 API 라우터
사용자 조회, 생성, 수정, 삭제 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database.session import get_db
from app.schemas import UserCreate, UserUpdate, UserResponse
from app.database.models import User
from . import users as crud
import math

router = APIRouter(prefix='/users', tags=['Users'])

number_per_page = 10

@router.get('/')
async def list_users(
    page: int = 1,
    id: str = None,
    name: str = None,
    address: str = None,
    gender: str = None,
    orderby: str = 'name',
    db: Session = Depends(get_db)
):
    """
    사용자 목록 조회 (페이지네이션, 검색, 정렬)

    - **page**: 페이지 번호 (기본값: 1)
    - **id**: 사용자 ID로 검색
    - **name**: 이름으로 검색
    - **address**: 주소로 검색
    - **gender**: 성별로 필터 (Female/Male)
    - **orderby**: 정렬 기준 (id/name/birthdate/age/gender/address, 기본값: name)
    """
    if page < 1:
        page = 1

    # 검색 조건 구성
    where = []
    if id:
        where.append(User.id.like(f'%{id}%'))
    if name:
        where.append(User.name.like(f'%{name}%'))
    if address:
        where.append(User.address.like(f'%{address}%'))
    if gender:
        where.append(User.gender == gender)

    # 쿼리 구성
    query = db.query(User)
    if where:
        query = query.filter(and_(*where))

    # 정렬
    if orderby == 'id':
        query = query.order_by(User.id)
    elif orderby == 'birthdate':
        query = query.order_by(User.birthdate)
    elif orderby == 'age':
        query = query.order_by(User.age)
    elif orderby == 'gender':
        query = query.order_by(User.gender)
    elif orderby == 'address':
        query = query.order_by(User.address)
    else:  # name or default
        query = query.order_by(User.name)

    # 전체 카운트
    count_users = query.count()
    end_page = math.ceil(count_users / number_per_page) if count_users > 0 else 1

    # 페이지네이션
    skip = (page - 1) * number_per_page
    users = query.offset(skip).limit(number_per_page).all()

    # 응답 형식: Flask와 동일하게 {"users": [...], "end_page": 10}
    return {
        'users': [UserResponse.model_validate(u).model_dump() for u in users],
        'end_page': end_page
    }


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    특정 사용자 조회

    - **user_id**: 사용자 ID
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


@router.post('/', response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    새 사용자 생성

    - **id**: 사용자 ID (필수)
    - **name**: 이름 (필수)
    - **birthdate**: 생년월일 (필수)
    - **age**: 나이 (필수)
    - **gender**: 성별 (필수)
    - **address**: 주소 (필수)
    """
    # 중복 확인
    existing_user = crud.get_user(db, user.id)
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다")

    return crud.create_user(db, user)


@router.put('/{user_id}', response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """
    사용자 정보 수정

    - **user_id**: 사용자 ID
    - **name**: 이름 (선택사항)
    - **age**: 나이 (선택사항)
    - **address**: 주소 (선택사항)
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    return crud.update_user(db, user_id, user_update)


@router.delete('/{user_id}', status_code=204)
async def delete_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    사용자 삭제

    - **user_id**: 사용자 ID
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    crud.delete_user(db, user_id)


# Flask 호환 엔드포인트
@router.get('/user_info/{user_id}')
async def get_user_info(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    사용자 상세정보 조회 (Flask 호환)

    - **user_id**: 사용자 ID
    """
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")

    # Flask와 동일한 형식으로 반환
    return user


@router.get('/order_history/{user_id}')
async def get_user_order_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    사용자 주문 이력 조회 (Flask 호환)

    - **user_id**: 사용자 ID
    """
    from sqlalchemy import desc
    from app.database.models import Order

    orders = db.query(Order).filter(Order.user_id == user_id).order_by(desc(Order.ordertime)).all()

    return [o.to_dict() if hasattr(o, 'to_dict') else {
        'id': o.id,
        'ordertime': str(o.ordertime) if o.ordertime else None,
        'store_id': o.store_id,
        'user_id': o.user_id
    } for o in orders]


@router.get('/store_top5/{user_id}')
async def get_user_store_top5(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    사용자가 가장 많이 방문한 스토어 TOP 5 (Flask 호환)

    - **user_id**: 사용자 ID
    """
    from sqlalchemy import func, desc
    from app.database.models import Order, Store

    top_stores = db.query(
        Store.id,
        Store.name,
        func.count(Order.id).label('visit_count')
    ).join(Order, Store.id == Order.store_id).filter(
        Order.user_id == user_id
    ).group_by(Store.id, Store.name).order_by(
        desc('visit_count')
    ).limit(5).all()

    return [{'store_id': s[0], 'store_name': s[1], 'visit_count': s[2]} for s in top_stores]


@router.get('/item_top5/{user_id}')
async def get_user_item_top5(
    user_id: str,
    db: Session = Depends(get_db)
):
    """
    사용자가 가장 많이 구매한 아이템 TOP 5 (Flask 호환)

    - **user_id**: 사용자 ID
    """
    from sqlalchemy import func, desc
    from app.database.models import Order, Orderitem, Item

    top_items = db.query(
        Item.id,
        Item.name,
        func.count(Orderitem.id).label('purchase_count')
    ).join(Orderitem, Item.id == Orderitem.item_id).join(
        Order, Orderitem.order_id == Order.id
    ).filter(Order.user_id == user_id).group_by(
        Item.id, Item.name
    ).order_by(desc('purchase_count')).limit(5).all()

    return [{'item_id': i[0], 'item_name': i[1], 'purchase_count': i[2]} for i in top_items]
