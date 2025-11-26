from database.models import *
from sqlalchemy import and_


def get_orders_list(count: int, filtering: dict, where: list):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {where}')

    orderby = {'id': Order.id, 'ordertime': Order.ordertime, 'store_id': Order.store_id, 'user_id':Order.user_id}
    orderby_ = orderby[filtering['orderby']]
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(where) == 0:
        orders = Order.query.order_by(orderby_).limit(count).offset(offset_num).all()
        count_orders = Order.query.count()
        logging.debug(f'조회된 사용자 목록: {orders}')
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:
        orders = Order.query.filter(and_(*where)).order_by(orderby_).limit(count).offset(offset_num).all()
        count_orders = Order.query.filter(and_(*where)).count()
    # 검색결과가 있는 경우와 아닌 경우
    if orders:
        orders_dict = [u.to_dict() for u in orders]
    else:
        orders_dict = []
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_orders}')
    return orders_dict, count_orders

def get_order_by_id(id_):
    order = db.session.query(Order, Store.name.label('store'), User.name.label('user'))\
        .join(Store, Order.store_id == Store.id)\
        .join(User, Order.user_id == User.id)\
        .filter(Order.id == id_)\
        .first()
    if order is None:
        order_dict = {}
    else:
        order_obj, store_name, user_name = order
        order_dict = {'order_id': order_obj.id,
                      'ordertime': order_obj.ordertime,
                      'store_id': order_obj.store_id,
                      'user_id': order_obj.user_id,
                      'store': store_name,
                      'user': user_name}
    return order_dict

def get_items_in_order(id_):
    results = db.session.query(Item.id.label('item_id'), Item.name.label('item'), Item.price)\
        .join(Orderitem, Orderitem.item_id == Item.id)\
        .join(Order, Order.id == Orderitem.order_id)\
        .filter(Order.id == id_).all()
    
    items_in_order = []
    for i in results:
        logging.debug(i)
        items_in_order.append({'item_id': i.item_id, 'item': i.item, 'price': i.price})
    return items_in_order