from flask import Blueprint
from flask import request,jsonify, abort
from database.database import *
from database.stores_db import *
import uuid
import math

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

stores_bp = Blueprint('stores', __name__)


number_per_page = 10
@stores_bp.route('/stores/')
def get_stores():
    logging.debug('----- 스토어 목록 조회 -------')
    page = request.args.get('page', default=1, type=int)
    if (page < 1) or type(page) is not int:
        page = 1
    orderby = request.args.get('orderby', default='name', type=str)
    s_id = request.args.get('id', type=str)
    name = request.args.get('name', type=str)
    address = request.args.get('address', type=str)
    store_type = request.args.get('type', type=str)
    logging.debug(f'GET 파라미터 : 페이지 {page}, 아이디 {s_id}, 이름 {name}, 주소 {address}, 매장종류 {store_type}, 정렬기준 {orderby}')

    filtering = {'page': page, 'orderby': orderby}
    if s_id:
        filtering['id'] = s_id
    if name:
        filtering['name'] = name
    if address:
        filtering['address'] = address
    if store_type:
        filtering['type'] = store_type
    logging.debug(f'검색조건: {filtering}')

    stores, count_stores = get_stores_list(number_per_page, filtering)
    end_page = math.ceil(count_stores / number_per_page)
    if (end_page != 0) and (page > end_page):
        abort(404)
    store_types = get_store_type()
    return jsonify({'stores': stores, 'end_page': end_page, 'store_types': store_types})

@stores_bp.route('/store_info/<id>')
def get_store_info(id):
    logging.debug('스토어 정보 가져오기')
    # id에 맞는 해당 스토어 정보 데이터베이스에서 가져와서 전송
    store = get_store_by_id(id)
    store_types = get_store_type()
    logging.debug(store)
    return jsonify({'store': store, 'store_types': store_types})

@stores_bp.route('/store/monthly_sales/<id>')
def get_stores_monthly_sales(id):
    monthly_sales = get_monthly_sales(id)
    return jsonify(monthly_sales)

@stores_bp.route('/store/most_visited/<id>')
def get_stores_most_visited(id):
    most_visited = get_most_visited(id)
    return jsonify(most_visited)