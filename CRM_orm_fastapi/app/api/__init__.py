"""
FastAPI CRM API 라우터 통합
모든 리소스별 API 라우터를 하나로 통합합니다.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.database.session import get_db
from app.schemas import KioskOrderRequest
from .users import router as users_router
from .stores import router as stores_router
from .items import router as items_router
from .orders import router as orders_router
from .orderitems import router as orderitems_router

# 메인 API 라우터
router = APIRouter(prefix='/api/v1')

# 모든 리소스 라우터 포함
router.include_router(users_router)
router.include_router(stores_router)
router.include_router(items_router)
router.include_router(orders_router)
router.include_router(orderitems_router)


# Flask 호환 엔드포인트 (users)
@router.get('/user_info/{user_id}')
async def get_user_info(
    user_id: str,
    db: Session = Depends(get_db)
):
    """사용자 상세정보 조회"""
    from app.database.models import User
    from .users import users as crud

    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user


@router.get('/order_history/{user_id}')
async def get_user_order_history(
    user_id: str,
    db: Session = Depends(get_db)
):
    """사용자 주문 이력 조회"""
    from app.database.models import Order, Store, Item, Orderitem
    from sqlalchemy import func

    # Order를 상세정보와 함께 조회
    orders = db.query(
        Order.id.label('order_id'),
        Order.ordertime,
        Store.name.label('store'),
        func.group_concat(Item.name, ', ').label('item')
    ).outerjoin(Store, Order.store_id == Store.id).outerjoin(
        Orderitem, Order.id == Orderitem.order_id
    ).outerjoin(Item, Orderitem.item_id == Item.id).filter(
        Order.user_id == user_id
    ).group_by(Order.id).order_by(desc(Order.ordertime)).all()

    return [{
        'order_id': o.order_id,
        'ordertime': str(o.ordertime) if o.ordertime else None,
        'store': o.store or 'Unknown',
        'item': o.item or 'Unknown'
    } for o in orders]


@router.get('/store_top5/{user_id}')
async def get_user_store_top5(
    user_id: str,
    db: Session = Depends(get_db)
):
    """사용자가 가장 많이 방문한 스토어 TOP 5"""
    from app.database.models import Order, Store

    top_stores = db.query(
        Store.name.label('store'),
        func.count(Order.id).label('cnt')
    ).join(Order, Store.id == Order.store_id).filter(
        Order.user_id == user_id
    ).group_by(Store.id, Store.name).order_by(
        desc(func.count(Order.id))
    ).limit(5).all()

    return [{'store': s.store, 'cnt': s.cnt} for s in top_stores]


@router.get('/item_top5/{user_id}')
async def get_user_item_top5(
    user_id: str,
    db: Session = Depends(get_db)
):
    """사용자가 가장 많이 구매한 아이템 TOP 5"""
    from app.database.models import Order, Orderitem, Item

    top_items = db.query(
        Item.name.label('item'),
        func.count(Orderitem.id).label('cnt')
    ).join(Orderitem, Item.id == Orderitem.item_id).join(
        Order, Orderitem.order_id == Order.id
    ).filter(Order.user_id == user_id).group_by(
        Item.id, Item.name
    ).order_by(desc(func.count(Orderitem.id))).limit(5).all()

    return [{'item': i.item, 'cnt': i.cnt} for i in top_items]


# Flask 호환 엔드포인트 (stores)
@router.get('/store_info/{store_id}')
async def get_store_info(
    store_id: str,
    db: Session = Depends(get_db)
):
    """매장 상세정보 조회"""
    from app.database.models import Store

    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="매장을 찾을 수 없습니다")

    # 매장 타입 목록 조회
    store_types = db.query(Store.type).distinct().all()
    store_types = [s[0] for s in store_types]

    store_dict = store.to_dict() if hasattr(store, 'to_dict') else {
        'id': store.id,
        'name': store.name,
        'type': store.type,
        'address': store.address
    }

    return {
        'store': store_dict,
        'store_types': store_types
    }


# Flask 호환 엔드포인트 (items)
@router.get('/item_info/{item_id}')
async def get_item_info(
    item_id: str,
    db: Session = Depends(get_db)
):
    """상품 상세정보 조회"""
    from app.database.models import Item

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다")

    # 상품 타입 목록 조회
    item_types = db.query(Item.type).distinct().all()
    item_types = [i[0] for i in item_types]

    item_dict = item.to_dict() if hasattr(item, 'to_dict') else {
        'id': item.id,
        'name': item.name,
        'price': item.price,
        'type': item.type
    }

    return {
        'item': item_dict,
        'item_types': item_types
    }


# Flask 호환 엔드포인트 (orders)
@router.get('/order_info/{order_id}')
async def get_order_info(
    order_id: str,
    db: Session = Depends(get_db)
):
    """주문 상세정보 조회"""
    from app.database.models import Order, User, Store, Orderitem, Item

    order = db.query(
        Order.id.label('order_id'),
        Order.ordertime,
        User.id.label('user_id'),
        User.name.label('user'),
        Store.id.label('store_id'),
        Store.name.label('store'),
        func.group_concat(Item.name, ', ').label('items'),
        func.sum(Item.price).label('total_price')
    ).outerjoin(User, Order.user_id == User.id).outerjoin(
        Store, Order.store_id == Store.id
    ).outerjoin(Orderitem, Order.id == Orderitem.order_id).outerjoin(
        Item, Orderitem.item_id == Item.id
    ).filter(Order.id == order_id).group_by(Order.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다")

    return {
        'order_id': order.order_id,
        'ordertime': str(order.ordertime) if order.ordertime else None,
        'user_id': order.user_id or 'Unknown',
        'user': order.user or 'Unknown',
        'store_id': order.store_id or 'Unknown',
        'store': order.store or 'Unknown',
        'items': order.items or 'Unknown',
        'total_price': order.total_price or 0
    }


# 주문의 아이템 목록 조회
@router.get('/orders/items/{order_id}')
async def get_order_items(
    order_id: str,
    db: Session = Depends(get_db)
):
    """주문에 포함된 아이템 목록"""
    from app.database.models import Order, Orderitem, Item

    items = db.query(
        Item.id.label('item_id'),
        Item.name.label('item'),
        Item.price
    ).join(Orderitem, Item.id == Orderitem.item_id).join(
        Order, Orderitem.order_id == Order.id
    ).filter(Order.id == order_id).all()

    return [{'item_id': i.item_id, 'item': i.item, 'price': i.price} for i in items]


# 매장의 월간 매출액
@router.get('/store/monthly_sales/{store_id}')
async def get_store_monthly_sales(
    store_id: str,
    db: Session = Depends(get_db)
):
    """매장의 월간 매출액"""
    from app.database.models import Order, Store, Orderitem, Item
    from sqlalchemy.sql import extract

    sales = db.query(
        func.strftime('%Y-%m', Order.ordertime).label('monthly'),
        func.sum(Item.price).label('revenue'),
        func.count(Orderitem.id).label('cnt')
    ).join(Store, Order.store_id == Store.id).join(
        Orderitem, Order.id == Orderitem.order_id
    ).join(Item, Orderitem.item_id == Item.id).filter(
        Store.id == store_id
    ).group_by(func.strftime('%Y-%m', Order.ordertime)).order_by(
        desc(func.strftime('%Y-%m', Order.ordertime))
    ).limit(12).all()

    return [{'monthly': s.monthly, 'revenue': s.revenue or 0, 'cnt': s.cnt or 0} for s in sales]


# 매장을 가장 많이 방문한 사용자 TOP 5
@router.get('/store/most_visited/{store_id}')
async def get_store_most_visited_users(
    store_id: str,
    db: Session = Depends(get_db)
):
    """매장을 가장 많이 방문한 사용자 TOP 5"""
    from app.database.models import Order, Store, User

    top_users = db.query(
        User.id.label('user_id'),
        User.name.label('user'),
        func.count(Order.id).label('cnt')
    ).join(Order, User.id == Order.user_id).join(
        Store, Order.store_id == Store.id
    ).filter(Store.id == store_id).group_by(
        User.id, User.name
    ).order_by(desc(func.count(Order.id))).limit(5).all()

    return [{'user_id': u.user_id, 'user': u.user, 'cnt': u.cnt} for u in top_users]


# 아이템의 월간 매출액
@router.get('/items/monthly_sales/{item_id}')
async def get_item_monthly_sales(
    item_id: str,
    db: Session = Depends(get_db)
):
    """아이템의 월간 매출액"""
    from app.database.models import Item, Orderitem, Order

    sales = db.query(
        func.strftime('%Y-%m', Order.ordertime).label('month'),
        func.sum(Item.price).label('revenue'),
        func.count(Orderitem.id).label('cnt')
    ).join(Orderitem, Item.id == Orderitem.item_id).join(
        Order, Orderitem.order_id == Order.id
    ).filter(Item.id == item_id).group_by(
        func.strftime('%Y-%m', Order.ordertime)
    ).order_by(desc(func.strftime('%Y-%m', Order.ordertime))).limit(12).all()

    return [{'month': s.month, 'revenue': s.revenue or 0, 'cnt': s.cnt or 0} for s in sales]


# Kiosk 페이지용 엔드포인트
@router.get('/store_type')
async def get_store_types(db: Session = Depends(get_db)):
    """모든 매장 종류 조회"""
    from app.database.models import Store

    store_types = db.query(Store.type).distinct().all()
    store_types = [s[0] for s in store_types if s[0]]
    return store_types


@router.get('/store_name/{store_type}')
async def get_stores_by_type(
    store_type: str,
    db: Session = Depends(get_db)
):
    """특정 종류의 모든 매장 조회"""
    from app.database.models import Store

    stores = db.query(Store).filter(Store.type == store_type).all()
    return [{'id': s.id, 'name': s.name, 'type': s.type, 'address': s.address} for s in stores]


# Kiosk용 간단한 상품 목록 조회 (페이지네이션 없이)
@router.get('/items')
async def get_all_items(db: Session = Depends(get_db)):
    """키오스크용 모든 상품 조회 (간단한 형식)"""
    from app.database.models import Item

    items = db.query(Item).all()
    return [i.to_dict() for i in items] if items else []


# 주문 생성 엔드포인트
@router.post('/add_order')
async def add_order(
    order_data: KioskOrderRequest,
    db: Session = Depends(get_db)
):
    """주문 생성"""
    from app.database.models import Order, Orderitem
    from datetime import datetime
    import uuid

    try:
        # 요청 데이터 검증
        request_data = order_data

        user_id = request_data.user_id
        store_id = request_data.store_id
        items = request_data.items

        if not user_id or not store_id or not items:
            raise HTTPException(status_code=400, detail="필수 필드가 없습니다")

        # Order 생성
        new_order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            store_id=store_id,
            ordertime=datetime.now()
        )
        db.add(new_order)
        db.flush()

        # Orderitem 생성
        for item_id in items:
            orderitem = Orderitem(
                id=str(uuid.uuid4()),
                order_id=new_order.id,
                item_id=item_id
            )
            db.add(orderitem)

        db.commit()
        return {'message': '주문이 완료되었습니다!'}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"주문 생성 중 오류: {str(e)}")


__all__ = ['router']
