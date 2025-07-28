from database.database import *
from database.models import *
from sqlalchemy import and_



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

# def get_items():
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('SELECT * from items')
#     items = cur.fetchall()
#     items = [dict(i) for i in items]
#     cur.close()
#     conn.close()
#     return items

# def get_item_type():
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('SELECT distinct type from items')
#     item_type = cur.fetchall()
#     item_type = [dict(i)['type'] for i in item_type]
#     logging.debug(item_type)
#     cur.close()
#     conn.close()
#     return item_type


# def get_item_by_id(id):
#     conn = get_connect()
#     cur = conn.cursor()

#     cur.execute('SELECT * FROM items WHERE id=?', (id ,))
#     item = cur.fetchone()
#     cur.close()
#     conn.close()
#     if not item:
#         item = '아이템 정보가 없음'
#         return item
#     else:
#         logging.debug(dict(item))
#         item_dict = dict(item)
#         return item_dict

# def get_item_sales(id):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('''
#                 SELECT strftime('%Y-%m', o.ordertime) as month, sum(i.price) as revenue, count(*) as cnt
#                 FROM items i
#                 JOIN orderitems oi ON i.id=oi.item_id
#                 JOIN orders o ON o.id=oi.order_id
#                 WHERE i.id=?
#                 GROUP BY month
#                 ORDER BY month DESC
#                 LIMIT 12
#                 ''',(id,))
#     item_sales = cur.fetchall()
#     cur.close()
#     conn.close()
#     item_sales = [dict(i) for i in item_sales]
#     item_sales.reverse()
#     return item_sales


# def insert_item(item):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('INSERT INTO items VALUES (?, ?, ?, ?)',
#                 (item['id'], item['name'], item['type'], item['price']))
#     conn.commit()
#     cur.execute('SELECT * FROM items WHERE id=?', (item['id'],))
#     new_item = cur.fetchone()
#     new_item = dict(new_item)
#     cur.close()
#     conn.close()
#     return new_item

# def update_item(item):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('''
#                 UPDATE items 
#                 SET  type=?, name=?, price=? 
#                 WHERE id=?
#                 ''',
#                 (item['type'], item['name'], item['price'], item['id']))
#     conn.commit()
#     cur.close()
#     conn.close()

# def delete_item_by_id(id):
#     conn = get_connect()
#     cur = conn.cursor()
#     cur.execute('DELETE FROM items WHERE id=?', (id, ))
#     conn.commit()
#     cur.close()
#     conn.close()
    