from flask import Flask
from flask import Blueprint, current_app
from flask import render_template, request, url_for, redirect
from database.database import *
import math
import logging

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

# app = Flask(__name__)
stores_bp = Blueprint('stores', __name__)

count_per_page = 10
# @app.route('/')
@stores_bp.route('/')
def stores_index():
    page = request.args.get('page', default=1, type=int)
    id = request.args.get('id', type=str)
    name = request.args.get('name', type=str)
    type = request.args.get('type', type=str)
    address = request.args.get('address', type=str)
    orderby = request.args.get('orderby', default='name', type=str)
    filtering = {'page':page, 'orderby':orderby}
    if id:
        filtering['id'] = id
    if name:
        filtering['name'] = name
    if type:
        filtering['type'] = type
    if address:
        filtering['address'] = address
    logging.debug(f'필터링 조건들: {filtering}')    
    stores, count_stores = get_stores_list(count_per_page, filtering)
    end_page = math.ceil(count_stores / count_per_page)
    type_values = get_store_type()
    return render_template('stores_index.html', stores=stores, end_page=end_page, current_page=page, type_values=type_values)

@stores_bp.route('/info/<id>')
def store_info(id):
    logging.debug('스토어 정보 가져오기')
    # id에 맞는 해당 스토어 정보 데이터베이스에서 가져와서 전송
    store = get_store_by_id(id)
    monthly_sales = get_monthly_sales(id)
    most_visited = get_most_visited(id)

    return render_template('store_info.html', store=store, monthly_sales=monthly_sales, most_visited=most_visited)
# if __name__=='__main__':
    # app.run(debug=True)

