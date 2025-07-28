import sqlite3
import logging
from flask import current_app


from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

#로깅 설정
logging.basicConfig(level=logging.DEBUG,  # 로깅 레벨 설정. DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL 순으로 레벨이 높음. 설정된 레벨 이상의 로그만 출력됨.im
                    format="%(asctime)s [%(levelname)s] %(message)s", # 로그 출력 형식을 정의(포맷팅). 로그 발생 시각, 로그 레벨 이름, 출력 메시지(사용자가 정의..?) 
                    datefmt='%Y-%m-%d %H-%M-%S') # 로그 발생 시각의 출력 형식을 정의



# 데이터베이스 연결
def get_connect():
    conn = sqlite3.connect(current_app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


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