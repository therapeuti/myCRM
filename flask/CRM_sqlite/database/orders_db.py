from database.database import *

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
    # 전체 주문 목록 가져오기 (필터링 조건 없음)
    if len(filter_keys) == 0:
        logging.debug(f'order by 조건: {filtering["orderby"]}')
        # 쿼리문 실행 - 주문 목록 가져오기
        sql_query = f'SELECT * FROM orders ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        orders = cur.fetchall()
        orders_dict = [dict(s) for s in orders]
        # 쿼리문 실행 - 주문 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) from orders')
        count_orders = cur.fetchone()[0]
        logging.debug(orders_dict)
        logging.debug(count_orders)
    # 필터링 조건에 따른 주문 목록 가져오기
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
        logging.debug(f'주문 목록 : {orders}')
        # 데이터 개수 가져오기
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_orders = cur.fetchone()[0]
        logging.debug(count_orders)
    cur.close()
    conn.close()

    logging.debug(f'전체 주문 수: {count_orders}')
    if count_orders == 0:
        orders_dict = []
        logging.debug('검색 조건에 해당하는 주문정보를 찾을 수 없습니다.')
    else:
        logging.debug(f'첫번째 주문정보만 가져옴. -> {orders[0]}')
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
                WHERE o.id=?
                GROUP BY order_id
                ''',(id ,))
    order = cur.fetchone()
    cur.close()
    conn.close()
    if order:
        order = dict(order)
        logging.debug(order)
    else:
        logging.debug(f'조회된 결과가 없음 : {order}')
        order = []
    return order

def get_items_in_order(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT i.id as item_id, i.name as item, i.price
                FROM orders o
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN items i ON i.id=oi.item_id
                WHERE o.id=?
                ''',(id ,))
    items_in_order = cur.fetchall()
    cur.close()
    conn.close()
    items_in_order = [dict(i) for i in items_in_order]
    logging.debug(items_in_order)
    return items_in_order


