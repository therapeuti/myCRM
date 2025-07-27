from flask import Blueprint
from flask import request,jsonify, abort, redirect, url_for
from database.database import *
from database.stores_db import *
from database.items_db import *
import uuid
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

kiosk_bp = Blueprint('kiosk', __name__)

@kiosk_bp.route('/store_name/<store_type>')
def get_store_names_by_type(store_type):
    store_names = get_store_name(store_type)
    logging.debug(store_names)
    return jsonify(store_names)

@kiosk_bp.route(('/store_type'))
def get_store_types():
    store_types = get_store_type()
    return jsonify(store_types)

@kiosk_bp.route('/items')
def get_items_for_order():
    items = get_items()
    return jsonify(items)

@kiosk_bp.route('/add_order', methods=['POST'])
def add_order():
    logging.debug(request.get_json())
    user_id = request.get_json()['user_id']
    store_id = request.get_json()['store_id']
    item_ids = request.get_json()['items']
    order_id = str(uuid.uuid4())
    ordertime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    logging.debug(ordertime)
    order_data = {'id': order_id, 'ordertime': ordertime, 'store_id': store_id, 'user_id': user_id}
    new_order = insert_order(order_data)
    logging.debug(f'주문이 들어왔습니다.  {new_order}')
    orderitems = []
    for i in item_ids:
        orderitem_id = str(uuid.uuid4())
        orderitem = {'id': orderitem_id, 'order_id': order_id, 'item_id': i}
        orderitems.append(orderitem)
    new_orderitems = insert_orderitem(orderitems)
    logging.debug(f'삽입된 주문아이템 데이터: {orderitems}')
    return jsonify({'order':new_order, 'orderitems':new_orderitems})
