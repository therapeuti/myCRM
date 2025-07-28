from flask import Blueprint
from flask import abort, request, jsonify
from database.orders_db import *
import math

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

orders_bp = Blueprint('orders', __name__)

number_per_page = 10
@orders_bp.route('/orders/')
def get_orders():
    logging.debug('----- 오더 목록 조회 -------')
    page = request.args.get('page', default=1, type=int)
    if (page < 1) or type(page) is not int:
        page = 1
    orderby = request.args.get('orderby', default='id', type=str)
    o_id = request.args.get('id')
    ordertime = request.args.get('ordertime')
    logging.debug(ordertime)
    store_id = request.args.get('store_id')
    user_id = request.args.get('user_id')

    filtering = {'page':page, 'orderby':orderby}
    where = []
    if o_id:
        where.append(Order.id.like(f'%{o_id}%'))
    if store_id:
        where.append(Order.store_id.like(f'%{store_id}%'))
    if user_id:
        where.append(Order.user_id.like(f'%{user_id}%'))
    if ordertime:
        where.append(Order.ordertime.like(f'%{ordertime}%'))
    logging.debug(f'검색조건: {where}')

    orders, count_orders = get_orders_list(number_per_page, filtering, where)
    end_page = math.ceil(count_orders / number_per_page)
    if (end_page != 0) and (page > end_page):
        abort(404)
    return jsonify({'orders': orders, 'end_page': end_page})

@orders_bp.route('/order_info/<id>')
def get_order_info(id):
    logging.debug('주문 정보 가져오기')
    order = get_order_by_id(id)
    logging.debug(order)
    return jsonify(order)

@orders_bp.route('/orders/items/<id>')
def get_orders_items(id):
    logging.debug('주문아이디에 해당하는 아이템들 가져오기')
    items_in_order = get_items_in_order(id)
    logging.debug(items_in_order)
    return jsonify(items_in_order)

