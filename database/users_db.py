from database.database import *

# 사용자 전체 조회
def get_users_list(count: int, filtering: dict):
    offset_num = int((filtering['page'] - 1 ) * count)
    logging.debug(f'count: {count}, page: {filtering["page"]}, offset_num: {offset_num}')
    logging.debug(f'필터링 조건 확인: {filtering}')

    # SQL 쿼리문 작성위해 where 조건이 있는 경우와 없는 경우로 구분
    filter_keys = []   # ex) id LIKE ?
    filter_values = []  # ex) %김%
    for key, value in filtering.items(): 
        if key not in ['page', 'gender', 'orderby']:
            filter_keys.append(f'{key} LIKE ?')
            filter_values.append(f'%{value}%')
        elif key == 'gender':
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
        sql_query = f'SELECT * FROM users ORDER BY {filtering["orderby"]} LIMIT ? OFFSET ?'
        cur.execute(sql_query, (count, offset_num))
        users = cur.fetchall()
        # 쿼리문 실행 - 사용자 데이터 개수 가져오기
        cur.execute('SELECT COUNT(*) FROM users')
        count_users = cur.fetchone()[0]
    # 필터링 조건에 따른 사용자 목록 가져오기
    else:    
        where_keys = ' AND '.join(filter_keys)
        where = 'WHERE ' + where_keys
        sql_query = 'SELECT * FROM users ' + where + ' ORDER BY '+ filtering['orderby']+' LIMIT ? OFFSET ?'
        sql_count_query = 'SELECT COUNT(*) FROM users ' + where
        logging.debug(f'SQL 쿼리문:  {sql_query}')
        logging.debug(f'파라미터 튜플 :  {parameter_tuple}')
        cur.execute(sql_query, parameter_tuple)
        users = cur.fetchall()
        logging.debug(f'사용자 목록 가져온건 맞음? {users}')
        logging.debug(sql_count_query)
        logging.debug(parameter_count_tuple)
        cur.execute(sql_count_query, parameter_count_tuple)
        count_users = cur.fetchone()[0]
        logging.debug(count_users)
    cur.close()
    conn.close()

    # 검색된 사용자가 없는 경우... 한 명만 있는 경우... 여러 명인 경우...
    logging.debug(f'전체 사용자 수: {count_users}')
    if count_users == 0:
        users_dict = []
        logging.debug('검색 조건에 해당하는 사용자를 찾을 수 없습니다.')
    else:
        users_dict = [dict(u) for u in users]
        logging.debug(f'조회된 사용자 데이터 10개. -> {users_dict}')
    return users_dict, count_users

def get_users_gender():
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT DISTINCT gender from users')
    gender = cur.fetchall()
    gender_value = gender.values()
    logging.debug(gender_value)
    cur.close()
    conn.close()
    return gender_value

def get_user_by_id(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id=?', (id ,))
    user = cur.fetchone()
    logging.debug(user)
    cur.close()
    conn.close()
    if not user:
        return user
    else:
        logging.debug(dict(user))
        user_dict = dict(user)
        return user_dict
    
def get_users_order(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT o.id as order_id, o.ordertime, s.name as store, group_concat(i.name) as item 
                FROM orders o 
                JOIN users u ON o.user_id=u.id
                JOIN stores s ON o.store_id=s.id
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN items i ON oi.item_id=i.id
                WHERE u.id=?
                GROUP BY order_id
                ORDER BY ordertime DESC'''
                , (id,))
    order_history = cur.fetchall()

    order_history = [dict(h) for h in order_history]
    logging.debug(order_history)
    cur.close()
    conn.close()
    return order_history

def get_store_top5(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT s.name as store, count(*) as cnt
                FROM orders o 
                JOIN stores s ON o.store_id=s.id
                WHERE o.user_id=?
                GROUP BY store
                ORDER BY cnt DESC LIMIT 5
                ''', (id, ))
    store_top5 = cur.fetchall()
    cur.close()
    conn.close()
    # if not store_top5:
    #     store_top5 = '검색 결과 없음'
    # else:
    #     store_top5 = [dict(s) for s in store_top5]
    #     logging.debug(store_top5)
    store_top5 = [dict(s) for s in store_top5]
    logging.debug(store_top5)
    return store_top5

def get_item_top5(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                SELECT i.name as item, count(*) as cnt
                FROM orders o 
                JOIN orderitems oi ON o.id=oi.order_id
                JOIN items i ON oi.item_id=i.id
                WHERE o.user_id=?
                GROUP BY item
                ORDER BY cnt DESC LIMIT 5
                ''', (id, ))
    item_top5 = cur.fetchall()
    cur.close()
    conn.close()
    item_top5 = [dict(s) for s in item_top5]
    # if not item_top5:
    #     item_top5 = '검색 결과 없음'
    # else:
    #     item_top5 = [dict(s) for s in item_top5]
    #     logging.debug(item_top5)
    return item_top5

def update_user(user):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('''
                UPDATE users 
                SET name=?, birthdate=?, age=?, gender=?, address=? 
                WHERE id=?
                ''',
                (user['name'], user['birthdate'], user['age'], user['gender'], user['address'], user['id']))
    conn.commit()
    cur.close()
    conn.close()

def delete_user_by_id(id):
    conn = get_connect()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE id=?', (id, ))
    conn.commit()
    cur.close()
    conn.close()
    