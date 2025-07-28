import logging
from database.models import *

#로깅 설정
logging.basicConfig(level=logging.DEBUG,  # 로깅 레벨 설정. DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL 순으로 레벨이 높음. 설정된 레벨 이상의 로그만 출력됨.im
                    format="%(asctime)s [%(levelname)s] %(message)s", # 로그 출력 형식을 정의(포맷팅). 로그 발생 시각, 로그 레벨 이름, 출력 메시지(사용자가 정의..?) 
                    datefmt='%Y-%m-%d %H-%M-%S') # 로그 발생 시각의 출력 형식을 정의

# 데이터베이스 연결


# 데이터 전체 조회
# stores = Store.query.all()
# orders = Order.query.all()
# items = Item.query.all()
# orderitems = Orderitem.query.all()



# 데이터베이스 연결



def get_orderitem_by_id(id):
    orderitem = Orderitem.query.get(id)
    if not orderitem:
        orderitem_dict = {}
        return orderitem
    else:
        orderitem_dict = orderitem.to_dict()
        return orderitem_dict
    

def insert_user(users):
    cur.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
                (users['id'], users['name'], users['birthdate'], users['age'], users['gender'], users['address']))
    return '회원가입 완료'

def insert_order(order):
    cur.execute('INSERT INTO orders VALUES (?, ?, ?, ?)',
                (order['id'], order['ordertime'], order['store_id'], order['user_id']))
    cur.execute('SELECT * FROM orders WHERE id=?', (order['id'],))
    new_order = dict(new_order)
    return new_order

def insert_orderitem(orderitem):
    new_orderitems = []
    for i in orderitem:
        new_orderitems.append(new)
    new_orderitems = [dict(new) for new in new_orderitems]
    return new_orderitems