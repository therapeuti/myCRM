from database.database import *

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
