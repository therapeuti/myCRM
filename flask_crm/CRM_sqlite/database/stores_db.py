from database.database import *

# 스토어 전체 조회
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

#  스토어 타입 정보만 가져오기
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

# 특정 스토어 타입의 매장이름들만 가져오기
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
    logging.debug(dict(store))
    store_dict = dict(store)
    return store_dict

def get_monthly_sales(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT strftime('%Y-%m', o.ordertime) as monthly, sum(i.price) as revenue, count(*) as cnt
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
    most_visited = [dict(m) for m in most_visited]
    return most_visited




def update_store(store):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                UPDATE stores 
                SET name=?, type=?, address=? 
                WHERE id=?
                ''',
                (store['name'], store['type'], store['address'], store['id']))
    conn.commit()
    cur.close()
    conn.close()

def delete_store_by_id(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM stores WHERE id=?', (id, ))
    conn.commit()
    cur.close()
    conn.close()


def insert_store(store):
    logging.debug('스토어 정보 추가')
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('INSERT INTO stores VALUES (?, ?, ?, ?)',
                (store['id'], store['type'], store['name'], store['address']))
    conn.commit()
    cur.execute('SELECT * FROM stores WHERE id=?', (store['id'],))
    new_store = cur.fetchone()
    new_store = dict(new_store)
    logging.debug('insert 함수 내', new_store)
    cur.close()
    conn.close()
    return new_store
