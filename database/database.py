import sqlite3
import logging
from flask import current_app

#로깅 설정
logging.basicConfig(level=logging.DEBUG,  # 로깅 레벨 설정. DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL 순으로 레벨이 높음. 설정된 레벨 이상의 로그만 출력됨.im
                    format="%(asctime)s [%(levelname)s] %(message)s", # 로그 출력 형식을 정의(포맷팅). 로그 발생 시각, 로그 레벨 이름, 출력 메시지(사용자가 정의..?) 
                    datefmt='%Y-%m-%d %H-%M-%S') # 로그 발생 시각의 출력 형식을 정의



# 데이터베이스 연결
def get_connect():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn



def get_stores_list(count, filtering):
    offset_num = (filtering['page'] - 1) * count

    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    filter_keys = []   # ex) id LIKE ?
    filter_values = []  # ex) %김%
    for key, value in filtering.items(): 
        if key not in ['page', 'type', 'orderby']:
            filter_keys.append(f'{key} LIKE ?')
            filter_values.append(f'%{value}%')
        elif key == 'type':
            filter_keys.append(f'{key}=?')
            filter_values.append(value)
    parameter_count_tuple = tuple(filter_values)
    filter_values.extend([count, offset_num])
    parameter_tuple = tuple(filter_values)
    logging.debug(f'where 조건이 없으면 0, 있으면 1 이상 : {len(filter_keys)}')

    conn = get_connect()
    cur = conn.cursor()
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(filter_keys) == 0:
        # 쿼리문 실행 - 사용자 목록 가져오기
        logging.debug(f'order by 조건: {filtering["orderby"]}')
        sql_query = f'SELECT * FROM stores ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        stores = cur.fetchall()
        # 쿼리문 실행 - 사용자 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) FROM stores')
        count_stores = cur.fetchone()[0]
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:    
        where_keys = ' AND '.join(filter_keys)
        where = 'WHERE ' + where_keys
        sql_query = 'SELECT * FROM stores ' + where + ' ORDER BY '+ filtering['orderby']+' LIMIT ? OFFSET ?'
        sql_count_query = 'SELECT COUNT(*) FROM stores ' + where
        logging.debug(f'SQL 쿼리문:  {sql_query}')
        logging.debug(f'파라미터 튜플 :  {parameter_tuple}')
        cur.execute(sql_query, parameter_tuple)
        stores = cur.fetchall()
        logging.debug(f'사용자 목록 가져온건 맞음? {stores}')
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_stores = cur.fetchone()[0]
        logging.debug(count_stores)
    cur.close()
    conn.close()
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_stores}')
    if count_stores == 0:
        stores_dict = []
        logging.debug('검색 조건에 해당하는 사용자를 찾을 수 없습니다.')
    else:
        logging.debug(f'첫번째 스토어 정보만 가져옴. -> {stores[0]}')
        stores_dict = [dict(s) for s in stores]
        logging.debug(stores_dict)
        logging.debug(count_stores)

    return stores_dict, count_stores

def get_store_type():
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT type from stores')
    store_type = cur.fetchall()
    logging.debug(store_type)
    type_values = [dict(s)['type'] for s in store_type]
    logging.debug(type_values)
    cur.close()
    conn.close()
    return type_values

def get_store_name(type):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT id, name from stores WHERE type=?',(type,))
    store_name = cur.fetchall()
    logging.debug(store_name)
    store_values = [dict(s) for s in store_name]
    logging.debug(store_values)
    cur.close()
    conn.close()
    return store_values

def get_store_by_id(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM stores WHERE id=?', (id ,))
    store = cur.fetchone()
    cur.close()
    conn.close()
    if not store:
        store = '스토어 정보가 없음'
        return store
    else:
        logging.debug(dict(store))
        store_dict = dict(store)
        return store_dict

def get_monthly_sales(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT strftime('%Y-%m', o.ordertime) as monthly, sum(i.price) as reevenue, count(*) as cnt
                FROM stores s
                JOIN orders o ON s.id=o.store_id
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN items i ON oi.item_id=i.id
                WHERE s.id=?
                GROUP BY monthly
                ORDER BY monthly DESC;
                ''', (id,))
    monthly_sales = cur.fetchall()
    cur.close()
    conn.close()
    if not monthly_sales:
        monthly_sales = '검색된 내용 없음'
    else:
        monthly_sales = [dict(m) for m in monthly_sales]
    return monthly_sales

def get_most_visited(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT o.user_id, u.name, count(*) as cnt
                FROM users u
                JOIN orders o ON u.id=o.user_id
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN items i ON oi.item_id=i.id
                WHERE o.store_id=?
                GROUP BY o.user_id
                ORDER BY cnt DESC LIMIT 10;
                ''', (id,))
    most_visited = cur.fetchall()
    cur.close()
    conn.close()
    if not most_visited:
        most_visited = '검색된 내용 없음'
    else:
        most_visited = [dict(m) for m in most_visited]
    return most_visited



def get_items_list(count, filtering):
    offset_num = (filtering['page'] - 1) * count
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    filter_keys = []   # ex) id LIKE ?
    filter_values = []  # ex) %김%
    for key, value in filtering.items(): 
        if key not in ['page', 'type', 'orderby']:
            filter_keys.append(f'{key} LIKE ?')
            filter_values.append(f'%{value}%')
        elif key == 'type':
            filter_keys.append(f'{key}=?')
            filter_values.append(value)
    parameter_count_tuple = tuple(filter_values)
    filter_values.extend([count, offset_num])
    parameter_tuple = tuple(filter_values)
    logging.debug(f'where 조건이 없으면 0, 있으면 1 이상 : {len(filter_keys)}')

    conn = get_connect()
    cur = conn.cursor()
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(filter_keys) == 0:
        # 쿼리문 실행 - 사용자 목록 가져오기
        logging.debug(f'order by 조건: {filtering["orderby"]}')
        sql_query = f'SELECT * FROM items ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        items = cur.fetchall()
        # 쿼리문 실행 - 사용자 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) from items')
        count_items = cur.fetchone()[0]
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:    
        where_keys = ' AND '.join(filter_keys)
        where = 'WHERE ' + where_keys
        sql_query = 'SELECT * FROM items ' + where + ' ORDER BY '+ filtering['orderby']+' LIMIT ? OFFSET ?'
        sql_count_query = 'SELECT COUNT(*) FROM items ' + where
        logging.debug(f'SQL 쿼리문:  {sql_query}')
        logging.debug(f'파라미터 튜플 :  {parameter_tuple}')
        cur.execute(sql_query, parameter_tuple)
        items = cur.fetchall()
        logging.debug(f'사용자 목록 가져온건 맞음? {items}')
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_items = cur.fetchone()[0]
        logging.debug(count_items)
    cur.close()
    conn.close()
    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_items}')
    if count_items == 0:
        items_dict = []
        logging.debug('검색 조건에 해당하는 사용자를 찾을 수 없습니다.')
    else:
        logging.debug(f'첫번째 스토어 정보만 가져옴. -> {items[0]}')
        items_dict = [dict(s) for s in items]
        logging.debug(items_dict)
        logging.debug(count_items)
    return items_dict, count_items

def get_items():
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT * from items')
    items = cur.fetchall()
    items = [dict(i) for i in items]
    cur.close()
    conn.close()
    return items

def get_item_type():
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT distinct type from items')
    item_type = cur.fetchall()
    item_type = [dict(i)['type'] for i in item_type]
    logging.debug(item_type)
    cur.close()
    conn.close()
    return item_type


def get_item_by_id(id):
    conn = get_connect()
    cur = conn.cursor()

    cur.execute('SELECT * FROM items WHERE id=?', (id ,))
    item = cur.fetchone()
    cur.close()
    conn.close()
    if not item:
        item = '아이템 정보가 없음'
        return item
    else:
        logging.debug(dict(item))
        item_dict = dict(item)
        return item_dict

def get_item_sales(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT strftime('%Y-%m', o.ordertime) as month, sum(i.price) as revenue, count(*) as cnt
                FROM items i
                JOIN orderitems oi ON i.id=oi.item_id
                JOIN orders o ON o.id=oi.order_id
                WHERE i.id=?
                GROUP BY month
                ORDER BY month DESC
                LIMIT 12
                ''',(id,))
    item_sales = cur.fetchall()
    cur.close()
    conn.close()
    if not item_sales:
        item_sales = '검색된 내용 없음'
    else:
        item_sales = [dict(i) for i in item_sales]
        item_sales.reverse()
    return item_sales

def get_orders_list(count, filtering):
    offset_num = (filtering['page'] - 1) * count
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    filter_keys = []   # ex) id LIKE ?
    filter_values = []  # ex) %김%
    for key, value in filtering.items(): 
        if key not in ['page', 'ordertime', 'orderby']:
            filter_keys.append(f'{key} LIKE ?')
            filter_values.append(f'%{value}%')
        elif key == 'ordertime':
            filter_keys.append(f'strftime("%Y-%m-%d",{key})=?')
            filter_values.append(value)
    parameter_count_tuple = tuple(filter_values)
    filter_values.extend([count, offset_num])
    parameter_tuple = tuple(filter_values)
    logging.debug(f'where 조건이 없으면 0, 있으면 1 이상 : {len(filter_keys)}')

    conn = get_connect()
    cur = conn.cursor()
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(filter_keys) == 0:
        logging.debug(f'order by 조건: {filtering["orderby"]}')
        # 쿼리문 실행 - 사용자 목록 가져오기
        sql_query = f'SELECT * FROM orders ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        orders = cur.fetchall()
        orders_dict = [dict(s) for s in orders]
        # 쿼리문 실행 - 사용자 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) from orders')
        count_orders = cur.fetchone()[0]
        logging.debug(orders_dict)
        logging.debug(count_orders)
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:    
        where_keys = ' AND '.join(filter_keys)
        where = 'WHERE ' + where_keys
        sql_query = 'SELECT * FROM orders ' + where + ' ORDER BY '+ filtering['orderby']+' LIMIT ? OFFSET ?'
        sql_count_query = 'SELECT COUNT(*) FROM orders ' + where
        logging.debug(f'SQL 쿼리문:  {sql_query}')
        logging.debug(f'파라미터 튜플 :  {parameter_tuple}')
        # 필터링한 데이터 가져오기
        cur.execute(sql_query, parameter_tuple)
        orders = cur.fetchall()
        logging.debug(f'사용자 목록 가져온건 맞음? {orders}')
        # 데이터 개수 가져오기
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_orders = cur.fetchone()[0]
        logging.debug(count_orders)
    cur.close()
    conn.close()

    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_orders}')
    if count_orders == 0:
        orders_dict = []
        logging.debug('검색 조건에 해당하는 사용자를 찾을 수 없습니다.')
    else:
        logging.debug(f'첫번째 스토어 정보만 가져옴. -> {orders[0]}')
        orders_dict = [dict(o) for o in orders]
        logging.debug(orders_dict)
        logging.debug(count_orders)
    return orders_dict, count_orders

def get_order_by_id(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT o.id as order_id, o.ordertime, o.store_id, s.name as store, o.user_id, u.name as user
                FROM orders o
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN stores s ON o.store_id=s.id
                JOIN users u ON o.user_id=u.id 
                JOIN items i ON i.id=oi.item_id
                WHERE o.id=?
                GROUP BY order_id
                ''',(id ,))
    order = cur.fetchall()
    cur.close()
    conn.close()
    if not order:
        order = '아이템 정보가 없음'
        return order
    else:
        order_dict = [dict(o) for o in order]
        return order_dict

def get_items_in_order(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT i.id as item_id, i.name as item, i.price
                FROM orders o
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN stores s ON o.store_id=s.id
                JOIN users u ON o.user_id=u.id 
                JOIN items i ON i.id=oi.item_id
                WHERE o.id=?
                ''',(id ,))
    items_in_order = cur.fetchall()
    cur.close()
    conn.close()
    if not items_in_order:
        items_in_order = '아이템 정보가 없음'
        return items_in_order
    else:
        items_in_order = [dict(i) for i in items_in_order]
    return items_in_order


def get_orderitems_list(count, filtering):
    offset_num = (filtering['page'] - 1) * count
    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    filter_keys = []   # ex) id LIKE ?
    filter_values = []  # ex) %김%
    for key, value in filtering.items(): 
        if key not in ['page', 'orderby']:
            filter_keys.append(f'{key} LIKE ?')
            filter_values.append(f'%{value}%')
    parameter_count_tuple = tuple(filter_values)
    filter_values.extend([count, offset_num])
    parameter_tuple = tuple(filter_values)
    logging.debug(f'where 조건이 없으면 0, 있으면 1 이상 : {len(filter_keys)}')


    conn = get_connect()
    cur = conn.cursor()
    # 전체 사용자 목록 가져오기 (필터링 조건 없음)
    if len(filter_keys) == 0:
        logging.debug(f'order by 조건: {filtering["orderby"]}')
        # 쿼리문 실행 - 사용자 목록 가져오기
        sql_query = f'SELECT * FROM orderitems ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        orderitems = cur.fetchall()
        # 쿼리문 실행 - 사용자 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) from orderitems')
        count_orderitems = cur.fetchone()[0]
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:    
        where_keys = ' AND '.join(filter_keys)
        where = 'WHERE ' + where_keys
        sql_query = 'SELECT * FROM orderitems ' + where + ' ORDER BY '+ filtering['orderby']+' LIMIT ? OFFSET ?'
        sql_count_query = 'SELECT COUNT(*) FROM orderitems ' + where
        logging.debug(f'SQL 쿼리문:  {sql_query}')
        logging.debug(f'파라미터 튜플 :  {parameter_tuple}')
        # 필터링한 데이터 가져오기
        cur.execute(sql_query, parameter_tuple)
        orderitems = cur.fetchall()
        logging.debug(f'사용자 목록 가져온건 맞음? {orderitems}')
        # 데이터 개수 가져오기
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_orderitems = cur.fetchone()[0]
        logging.debug(count_orderitems)

    cur.close()
    conn.close()

    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_orderitems}')
    if count_orderitems == 0:
        orderitems_dict = []
        logging.debug('검색 조건에 해당하는 사용자를 찾을 수 없습니다.')
    else:
        logging.debug(f'첫번째 스토어 정보만 가져옴. -> {orderitems[0]}')
        orderitems_dict = [dict(o) for o in orderitems]
        logging.debug(orderitems_dict)
        logging.debug(count_orderitems)
    return orderitems_dict, count_orderitems

def get_orderitem_by_id(id):
    conn = get_connect()
    cur = conn.cursor()

    cur.execute('SELECT * FROM orderitems WHERE id=?', (id ,))
    orderitem = cur.fetchone()
    cur.close()
    conn.close()
    if not orderitem:
        orderitem = '아이템 정보가 없음'
        return orderitem
    else:
        logging.debug(dict(orderitem))
        orderitem_dict = dict(orderitem)
        return orderitem_dict
    

def insert_user(users):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
                (users['id'], users['name'], users['birthdate'], users['age'], users['gender'], users['address']))
    conn.commit()
    cur.close()
    conn.close()
    return '회원가입 완료'

def insert_order(order):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO orders VALUES (?, ?, ?, ?)',
                (order['id'], order['ordertime'], order['store_id'], order['user_id']))
    conn.commit()
    cur.execute('SELECT * FROM orders WHERE id=?', (order['id'],))
    new_order = cur.fetchone()
    new_order = dict(new_order)
    cur.close()
    conn.close()
    return new_order

def insert_orderitem(orderitem):
    conn = get_connect()
    cur = conn.cursor()
    new_orderitems = []
    for i in orderitem:
        cur.execute('INSERT INTO orderitems VALUES (?, ?, ?)',
                    (i['id'], i['order_id'], i['item_id']))
        conn.commit()
        cur.execute('SELECT * FROM orderitems WHERE id=?', (i['id'],))
        new = cur.fetchone()
        new_orderitems.append(new)
    cur.close()
    conn.close()
    new_orderitems = [dict(new) for new in new_orderitems]
    return new_orderitems