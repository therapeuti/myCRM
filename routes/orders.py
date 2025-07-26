from flask import Blueprint
from flask import abort, request, jsonify
from database.database import *
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
    store_id = request.args.get('store_id')
    user_id = request.args.get('user_id')

    filtering = {'page':page, 'orderby':orderby}
    if o_id:
        filtering['id'] = o_id
    if ordertime:
        filtering['ordertime'] = ordertime
    if store_id:
        filtering['store_id'] = store_id
    if user_id:
        filtering['user_id'] = user_id
    logging.debug(f'검색조건: {filtering}')

    orders, count_orders = get_orders_list(number_per_page, filtering)
    end_page = math.ceil(count_orders / number_per_page)
    if (end_page != 0) and (page > end_page):
        abort(404)
    return jsonify({'orders': orders, 'end_page': end_page})



#  수정
@orders_bp.route('/info/<id>')
def order_info(id):
    logging.debug('주문 정보 가져오기')

    order = get_order_by_id(id)
    logging.debug(order)
    items_in_order = get_items_in_order(id)
    logging.debug(items_in_order)
    return jsonify('order_info.html', order=order[0], items_in_order=items_in_order)


