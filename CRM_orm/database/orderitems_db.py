from database.database import *
from database.models import *
from sqlalchemy import and_


def get_orderitems_list(count: int, filtering: dict, where: list):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {where}')

    orderby = {'id': Orderitem.id, 'order_id': Orderitem.order_id, 'item_id':Orderitem.item_id}
    orderby_ = orderby[filtering['orderby']]
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(where) == 0:
        orderitems = Orderitem.query.order_by(orderby_).limit(count).offset(offset_num).all()
        count_orderitems = Orderitem.query.count()
        logging.debug(f'조회된 사용자 목록: {orderitems}')
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:
        orderitems = Orderitem.query.filter(and_(*where)).order_by(orderby_).limit(count).offset(offset_num).all()
        count_orderitems = Orderitem.query.filter(and_(*where)).count()
    # 검색결과가 있는 경우와 아닌 경우
    if orderitems:
        orderitems_dict = [u.to_dict() for u in orderitems]
    else:
        orderitems_dict = []
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_orderitems}')    

    return orderitems_dict, count_orderitems



# def get_orderitem_by_id(id):
#     conn = get_connect()
#     cur = conn.cursor()

#     cur.execute('SELECT * FROM orderitems WHERE id=?', (id ,))
#     orderitem = cur.fetchone()
#     cur.close()
#     conn.close()
#     if not orderitem:
#         orderitem = '아이템 정보가 없음'
#         return orderitem
#     else:
#         logging.debug(dict(orderitem))
#         orderitem_dict = dict(orderitem)
#         return orderitem_dict
