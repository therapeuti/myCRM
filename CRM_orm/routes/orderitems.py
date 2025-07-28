from flask import Blueprint
from flask import abort, request, jsonify
from database.database import *
from database.orderitems_db import *
import math

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

orderitems_bp = Blueprint('orderitems', __name__)

number_per_page = 10
@orderitems_bp.route('/orderitems/')
def get_orderitems():
    logging.debug('----- 오더아이템 목록 조회 -------')
    page = request.args.get('page', default=1, type=int)
    if (page < 1) or type(page) is not int:
        page = 1
    _id = request.args.get('id')
    order_id = request.args.get('order_id')
    item_id = request.args.get('item_id')
    orderby = request.args.get('orderby', default='id', type=str)

    filtering = {'page':page, 'orderby':orderby}
    where = []
    if _id:
        where.append(Order.id.like(f'%{_id}%'))
    if order_id:
        where.append(Order.order_id.like(f'%{order_id}%'))
    if item_id:
        where.append(Order.item_id.like(f'%{item_id}%'))
    logging.debug(f'검색조건: {where}')
    
    orderitems, count_orderitems = get_orderitems_list(number_per_page, filtering, where)
    end_page = math.ceil(count_orderitems / number_per_page)
    return jsonify({'orderitems': orderitems, 'end_page': end_page})



