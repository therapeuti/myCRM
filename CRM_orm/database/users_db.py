from database.models import *
from database.database import *
import logging
from sqlalchemy import and_


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

def get_user_by_id(id):
    user = User.query.get(id)
    user_dict = user.to_dict()
    if user is None:
        user_dict = {}
    return user_dict
    
# def get_users_order(id):
#     return order_history

# def get_store_top5(id):
#     return store_top5

# def get_item_top5(id):
#     return item_top5

# def update_user(user):

# def delete_user_by_id(id):
    