# from flask import Flask
from flask import Blueprint
from flask import render_template, request, url_for, redirect
from database.database import *
import math
import logging

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

# app = Flask(__name__)
orders_bp = Blueprint('orders', __name__)

count_per_page = 10
# @app.route('/')
@orders_bp.route('/')
def orders_index():
    page = request.args.get('page', default=1, type=int)
    id = request.args.get('id')
    ordertime = request.args.get('ordertime')
    store_id = request.args.get('store_id')
    user_id = request.args.get('user_id')
    orderby = request.args.get('orderby', default='id', type=str)
    filtering = {'page':page, 'orderby':orderby}
    if id:
        filtering['id'] = id
    if ordertime:
        filtering['ordertime'] = ordertime
    if store_id:
        filtering['store_id'] = store_id
    if user_id:
        filtering['user_id'] = user_id
    logging.debug(filtering)
    orders, count_orders = get_orders_list(count_per_page, filtering)
    end_pages = math.ceil(count_orders / count_per_page)
    return render_template('orders_index.html', orders=orders, end_page=end_pages, current_page=page)

@orders_bp.route('/info/<id>')
def order_info(id):
    order = get_order_by_id(id)
    logging.debug(order)
    items_in_order = get_items_in_order(id)
    logging.debug(items_in_order)
    return render_template('order_info.html', order=order[0], items_in_order=items_in_order)

# if __name__=='__main__':
#     app.run(debug=True)

