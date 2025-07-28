from database.models import *
from database.kiosk_db import *
from sqlalchemy import and_, func
from datetime import datetime


# 사용자 전체 조회
def get_users_list(count: int, filtering: dict, where: list):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {where}')

    orderby = {'id': User.id, 'name': User.name, 'birthdate': User.birthdate, 'age': User.age, 'gender': User.gender, 'address':User.address}
    orderby_ = orderby[filtering['orderby']]
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(where) == 0:
        users = User.query.order_by(orderby_).limit(count).offset(offset_num).all()
        count_users = User.query.count()
        logging.debug(f'조회된 사용자 목록: {users}')
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:
        users = User.query.filter(and_(*where)).order_by(orderby_).limit(count).offset(offset_num).all()
        count_users = User.query.filter(and_(*where)).count()
    # 검색결과가 있는 경우와 아닌 경우
    if users:
        users_dict = [u.to_dict() for u in users]
    else:
        users_dict = []
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_users}')
    return users_dict, count_users

# def get_users_gender():
#     return gender_value

def get_user_by_id(id_):
    user = User.query.get(id_)
    logging.debug(f'ID로 조회된 사용자 : {user}')
    if user is None:
        user_dict = {}
    else:
        user_dict = user.to_dict()
    return user_dict
    
def get_users_order(id_):
    users_order = db.session.query(Order.id.label('order_id'), 
                                   Order.ordertime, 
                                   Store.name.label('store'), 
                                   func.group_concat(Item.name, ',').label('item'))\
                                   .join(Store, Order.store_id == Store.id)\
                                   .join(Orderitem, Orderitem.order_id == Order.id)\
                                   .join(Item, Item.id == Orderitem.item_id)\
                                   .filter(Order.user_id == id_)\
                                   .group_by(Order.id)\
                                   .order_by(Order.ordertime.desc()).all()
    logging.debug(users_order)
    order_history = [{'order_id': i.order_id, 
                      'ordertime': i.ordertime, 
                      'store': i.store,
                      'item': i.item} for i in users_order]         
    return order_history

def get_store_top5(id_):
    stores5 = db.session.query(Store.name.label('store'), func.count(Store.id).label('cnt'))\
        .join(Order, Order.store_id == Store.id)\
        .filter(Order.user_id == id_)\
        .group_by(Store.id)\
        .order_by(func.count(Store.id).desc()).limit(5).all()
    logging.debug(stores5)
    store_top5 = [{'store': s.store, 'cnt': s.cnt} for s in stores5]
    return store_top5

def get_item_top5(id_):
    item5 = db.session.query(Item.name.label('item'),
                             func.count(Item.id).label('cnt') )\
                             .join(Orderitem, Orderitem.item_id == Item.id)\
                             .join(Order, Order.id == Orderitem.order_id)\
                             .filter(Order.user_id == id_)\
                             .group_by(Item.id)\
                             .order_by(func.Count(Item.id).desc()).limit(5).all()
    logging.debug(item5)
    item_top5 = [{'item': i.item, 'cnt': i.cnt} for i in item5]
    return item_top5

def insert_user(user):
    new_user = User(id=user['id'], 
                    name=user['name'],
                    birthdate=user['birthdate'],
                    age=user['age'],
                    gender=user['gender'],
                    address=user['address'])
    db.session.add(new_user)
    db.session.commit()
    return '회원가입 완료'

def update_user(user):
    new_user = db.session.get(User, user['id'])
    if new_user is None:
        return print('사용자가 존재하지 않습니다.')
    new_user.name = user['name']
    new_user.birthdate = user['birthdate']
    birthdate = datetime.strptime(new_user.birthdate, '%Y-%m-%d')
    new_user.age = datetime.today().year - birthdate.year
    logging.debug(new_user.age)
    new_user.gender = user['gender']
    new_user.address = user['address']
    db.session.commit()

def delete_user_by_id(id_):
    user = db.session.get(User, id_)
    if user:
        db.session.delete(user)
        db.session.commit()
        print(f'사용자({id_}) 삭제')
    else:
        print('사용자 없음 : ', id_)