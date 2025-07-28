from database.database import *


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
    # 전체 아이템 목록 가져오기 (필터링 조건 없음)
    if len(filter_keys) == 0:
        # 쿼리문 실행 - 아이템 목록 가져오기
        logging.debug(f'order by 조건: {filtering["orderby"]}')
        sql_query = f'SELECT * FROM items ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        items = cur.fetchall()
        # 쿼리문 실행 - 아이템 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) from items')
        count_items = cur.fetchone()[0]
    # 필터링 조건에 따른 아이템 목록 가져오기
    else:    
        where_keys = ' AND '.join(filter_keys)
        where = 'WHERE ' + where_keys
        sql_query = 'SELECT * FROM items ' + where + ' ORDER BY '+ filtering['orderby']+' LIMIT ? OFFSET ?'
        sql_count_query = 'SELECT COUNT(*) FROM items ' + where
        logging.debug(f'SQL 쿼리문:  {sql_query}')
        logging.debug(f'파라미터 튜플 :  {parameter_tuple}')
        cur.execute(sql_query, parameter_tuple)
        items = cur.fetchall()
        logging.debug(f'아이템 목록 가져온건 맞음? {items}')
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_items = cur.fetchone()[0]
        logging.debug(count_items)
    cur.close()
    conn.close()
    # 검색된 아이템가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 아이템 수: {count_items}')
    if count_items == 0:
        items_dict = []
        logging.debug('검색 조건에 해당하는 아이템를 찾을 수 없습니다.')
    else:
        logging.debug(f'아이템 목록. -> {items}')
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
    item_sales = [dict(i) for i in item_sales]
    item_sales.reverse()
    return item_sales


def insert_item(item):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO items VALUES (?, ?, ?, ?)',
                (item['id'], item['name'], item['type'], item['price']))
    conn.commit()
    cur.execute('SELECT * FROM items WHERE id=?', (item['id'],))
    new_item = cur.fetchone()
    new_item = dict(new_item)
    cur.close()
    conn.close()
    return new_item

def update_item(item):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                UPDATE items 
                SET  type=?, name=?, price=? 
                WHERE id=?
                ''',
                (item['type'], item['name'], item['price'], item['id']))
    conn.commit()
    cur.close()
    conn.close()

def delete_item_by_id(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM items WHERE id=?', (id, ))
    conn.commit()
    cur.close()
    conn.close()
    