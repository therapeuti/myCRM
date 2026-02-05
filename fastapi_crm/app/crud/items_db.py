from models.kiosk_db import *
from models.models import *
from sqlalchemy import and_, func

def get_items_list(count: int, filtering: dict, where: list):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {where}')

    orderby = {'id': Item.id, 'type': Item.type, 'name': Item.name, 'price':Item.price}
    orderby_ = orderby[filtering['orderby']]
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(where) == 0:
        items = Item.query.order_by(orderby_).limit(count).offset(offset_num).all()
        count_items = Item.query.count()
        logging.debug(f'조회된 사용자 목록: {items}')
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:
        items = Item.query.filter(and_(*where)).order_by(orderby_).limit(count).offset(offset_num).all()
        count_items = Item.query.filter(and_(*where)).count()
    # 검색결과가 있는 경우와 아닌 경우
    if items:
        items_dict = [u.to_dict() for u in items]
    else:
        items_dict = []
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_items}')
    return items_dict, count_items

def get_items():
    items = Item.query.all()
    items = [{'id': i.id, 'type': i.type, 'name': i.name, 'price': i.price} for i in items]
    return items

def get_item_type():
    types = db.session.query(Item.type).distinct().all()
    logging.debug(types)
    item_types = [i[0] for i in types]
    return item_types


def get_item_by_id(id):
    item = Item.query.get(id)
    if not item:
        item = {}
        return item
    else:
        item_dict = item.to_dict()
        return item_dict

def get_item_sales(id):
    sales = db.session.query(func.strftime('%Y-%m', Order.ordertime).label('month'),
                             func.sum(Item.price).label('revenue'),
                             func.count().label('cnt'))\
                             .join(Orderitem, Orderitem.order_id == Order.id)\
                             .join(Item, Item.id == Orderitem.item_id)\
                             .filter(Item.id == id)\
                             .group_by(func.strftime('%Y-%m', Order.ordertime))\
                             .order_by(func.strftime('%Y-%m', Order.ordertime).desc()).limit(12).all()
    logging.debug(sales)
    item_sales = [{'month': s.month, 'revenue': s.revenue, 'cnt': s.cnt} for s in sales]    
    return item_sales

def insert_item(item):
    new_item = Item(id=item['id'],
                    type=item['type'],
                    name=item['name'],
                    price=item['price'])
    db.session.add(new_item)
    db.session.commit()
    return '아이템 등록 완료'

def update_item(item):
    new_item = db.session.get(Item, item['id'])
    if new_item is None:
        return print('아이템이 존재하지 않습니다')
    new_item.type = item['type']
    new_item.name = item['name']
    new_item.price = item['price']
    db.session.commit()

def delete_item_by_id(id):
    item = db.session.get(Item, id)
    if item:
        db.session.delete(item)
        db.session.commit()
    else:
        print('아이템 없음 : ', id)