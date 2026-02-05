from database.models import *

def insert_order(order):
    new_order = Order(id=order['id'],
                      ordertime=order['ordertime'],
                      store_id=order['store_id'],
                      user_id=order['user_id'])
    db.session.add(new_order)
    db.session.commit()
    return new_order

def insert_orderitem(orderitem):
    new_orderitems = []
    for i in orderitem:
        new = Orderitem(id=i['id'],
                        order_id=i['order_id'],
                        item_id=i['item_id'])
        db.session.add(new)
        db.session.commit()
        new_orderitems.append(new)
    return new_orderitems
