from database.database import *
from database.models import *
from sqlalchemy import and_



# 스토어 전체 조회
def get_stores_list(count: int, filtering: dict, where: list):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {where}')

    orderby = {'id': Store.id, 'type': Store.type, 'name': Store.name, 'address':Store.address}
    orderby_ = orderby[filtering['orderby']]
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(where) == 0:
        stores = Store.query.order_by(orderby_).limit(count).offset(offset_num).all()
        count_stores = Store.query.count()
        logging.debug(f'조회된 사용자 목록: {stores}')
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:
        stores = Store.query.filter(and_(*where)).order_by(orderby_).limit(count).offset(offset_num).all()
        count_stores = Store.query.filter(and_(*where)).count()
    # 검색결과가 있는 경우와 아닌 경우
    if stores:
        stores_dict = [u.to_dict() for u in stores]
    else:
        stores_dict = []
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_stores}')

    return stores_dict, count_stores

# #  스토어 타입 정보만 가져오기
# def get_store_type():
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('SELECT DISTINCT type from stores')
#     store_type = cur.fetchall()
#     logging.debug(store_type)
#     type_values = [dict(s)['type'] for s in store_type]
#     logging.debug(type_values)
#     cur.close()
#     conn.close()
#     return type_values

# # 특정 스토어 타입의 매장이름들만 가져오기
# def get_store_name(type):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('SELECT id, name from stores WHERE type=?',(type,))
#     store_name = cur.fetchall()
#     logging.debug(store_name)
#     store_values = [dict(s) for s in store_name]
#     logging.debug(store_values)
#     cur.close()
#     conn.close()
#     return store_values

def get_store_by_id(id_):
    store = Store.query.get(id_)
    store_dict = store.to_dict()
    if store is None:
        store_dict = {}
    return store_dict

# def get_monthly_sales(id):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('''
#                 SELECT strftime('%Y-%m', o.ordertime) as monthly, sum(i.price) as revenue, count(*) as cnt
#                 FROM stores s
#                 JOIN orders o ON s.id=o.store_id
#                 JOIN orderitems oi ON o.id=oi.order_id
#                 JOIN items i ON oi.item_id=i.id
#                 WHERE s.id=?
#                 GROUP BY monthly
#                 ORDER BY monthly DESC;
#                 ''', (id,))
#     monthly_sales = cur.fetchall()
#     cur.close()
#     conn.close()
#     monthly_sales = [dict(m) for m in monthly_sales]
#     return monthly_sales

# def get_most_visited(id):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('''
#                 SELECT o.user_id, u.name, count(*) as cnt
#                 FROM users u
#                 JOIN orders o ON u.id=o.user_id
#                 JOIN orderitems oi ON o.id=oi.order_id
#                 JOIN items i ON oi.item_id=i.id
#                 WHERE o.store_id=?
#                 GROUP BY o.user_id
#                 ORDER BY cnt DESC LIMIT 10;
#                 ''', (id,))
#     most_visited = cur.fetchall()
#     cur.close()
#     conn.close()
#     most_visited = [dict(m) for m in most_visited]
#     return most_visited




# def update_store(store):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('''
#                 UPDATE stores 
#                 SET name=?, type=?, address=? 
#                 WHERE id=?
#                 ''',
#                 (store['name'], store['type'], store['address'], store['id']))
#     conn.commit()
#     cur.close()
#     conn.close()

# def delete_store_by_id(id):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('DELETE FROM stores WHERE id=?', (id, ))
#     conn.commit()
#     cur.close()
#     conn.close()


# def insert_store(store):
#     logging.debug('스토어 정보 추가')
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('INSERT INTO stores VALUES (?, ?, ?, ?)',
#                 (store['id'], store['type'], store['name'], store['address']))
#     conn.commit()
#     cur.execute('SELECT * FROM stores WHERE id=?', (store['id'],))
#     new_store = cur.fetchone()
#     new_store = dict(new_store)
#     logging.debug('insert 함수 내', new_store)
#     cur.close()
#     conn.close()
#     return new_store
