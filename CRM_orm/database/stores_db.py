from database.kiosk_db import *
from database.models import *
from sqlalchemy import and_, func

# 스토어 전체 조회
def get_stores_list(count: int, filtering: dict, where: list):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {where}')

    orderby = {'id': Store.id, 'type': Store.type, 'name': Store.name, 'address':Store.address}
    orderby_ = orderby[filtering['orderby']]
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    # 전체 스토어 목록 가져오기 (필터링 조건 없음)
    if len(where) == 0:
        stores = Store.query.order_by(orderby_).limit(count).offset(offset_num).all()
        count_stores = Store.query.count()
        logging.debug(f'조회된 스토어 목록: {stores}')
    # 필터링 조건에 따른 스토어 목록 가져오기
    else:
        stores = Store.query.filter(and_(*where)).order_by(orderby_).limit(count).offset(offset_num).all()
        count_stores = Store.query.filter(and_(*where)).count()
    # 검색결과가 있는 경우와 아닌 경우
    if stores:
        stores_dict = [u.to_dict() for u in stores]
    else:
        stores_dict = []
    # 검색된 스토어가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 스토어 수: {count_stores}')

    return stores_dict, count_stores

#  스토어 타입 정보만 가져오기
def get_store_type():
    store_types = db.session.query(Store.type).distinct().all()
    logging.debug(store_types)
    store_types = [s[0] for s in store_types]
    return store_types

# 특정 스토어 타입의 매장이름들만 가져오기
def get_store_name(type):
    store_names = db.session.query(Store.id, Store.name).filter(Store.type == type).all()
    logging.debug(store_names)
    store_names_dict = [{'id': i.id, 'name': i.name} for i in store_names]
    return store_names_dict

def get_store_by_id(id_):
    store = Store.query.get(id_)
    store_dict = store.to_dict()
    if store is None:
        store_dict = {}
    return store_dict

def get_monthly_sales(id):
    sales = db.session.query(func.strftime('%Y-%m', Order.ordertime).label('monthly'),
                             func.sum(Item.price).label('revenue'),
                             func.count().label('cnt'))\
                             .join(Store, Store.id == Order.store_id)\
                             .join(Orderitem, Orderitem.order_id == Order.id)\
                             .join(Item, Item.id == Orderitem.item_id)\
                             .filter(Store.id == id)\
                             .group_by(func.strftime('%Y-%m', Order.ordertime))\
                             .order_by(func.strftime('%Y-%m', Order.ordertime).desc()).all()
    monthly_sales = [{'monthly': s.monthly, 'revenue': s.revenue, 'cnt': s.cnt} for s in sales]
    return monthly_sales

def get_most_visited(id):
    visited = db.session.query(Order.user_id, 
                               User.name, 
                               func.count().label('cnt'))\
                               .join(User, User.id == Order.user_id)\
                               .join(Store, Store.id == Order.store_id)\
                               .filter(Order.store_id == id)\
                               .group_by(Order.user_id)\
                               .order_by(func.count().label('cnt').desc()).all()
    most_visited = [{'user_id': v.user_id, 'name': v.name, 'cnt': v.cnt} for v in visited]
    return most_visited




def update_store(store):
    new_store = db.session.get(Store, store['id'])
    if new_store is None:
        return print('스토어가 존재하지 않습니다.')
    new_store.id = store[id]
    new_store.type = store['type']
    new_store.name = store['name']
    new_store.address = store['address']

def delete_store_by_id(id_):
    store = db.session.get(Store, id_)
    if store:
        db.session.delete(store)
        db.session.commit()
        print(f'스토어({id_}) 삭제')
    else:
        print('스토어 없음 : ', id_)


def insert_store(store):
    new_store = Store(id=store['id'],
                      name=store['name'],
                      type=store['type'],
                      address=store['address']
                    )
    db.session.add(new_store)
    db.session.commit()
    return new_store
