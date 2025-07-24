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
orderitems_bp = Blueprint('orderitems', __name__)

count_per_page = 10
# @app.route('/')
@orderitems_bp.route('/')
def orderitems_index():
    page = request.args.get('page', default=1, type=int)
    id = request.args.get('id')
    order_id = request.args.get('order_id')
    item_id = request.args.get('item_id')
    orderby = request.args.get('orderby', default='id', type=str)
    filtering = {'page':page, 'orderby':orderby}
    if id:
        filtering['id'] = id
    if order_id:
        filtering['order_id'] = order_id
    if item_id:
        filtering['item_id'] = item_id
    logging.debug(filtering)
    orderitems, count_orderitems = get_orderitems_list(count_per_page, filtering)
    end_page = math.ceil(count_orderitems / count_per_page)
    return render_template('orderitems_index.html', orderitems=orderitems, end_page=end_page, current_page=page)


# if __name__=='__main__':
#     app.run(debug=True)

