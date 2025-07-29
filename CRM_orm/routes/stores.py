from flask import Blueprint
from flask import request,jsonify, abort, redirect, url_for
from database.kiosk_db import *
from database.stores_db import *
import math
import uuid

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

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
    s_name = request.args.get('name', type=str)
    s_address = request.args.get('address', type=str)
    store_type = request.args.get('type', type=str)
    logging.debug(f'GET 파라미터 : 페이지 {page}, 아이디 {s_id}, 이름 {s_name}, 주소 {s_address}, 매장종류 {store_type}, 정렬기준 {orderby}')

    filtering = {'page': page, 'orderby': orderby}
    where = []
    if s_id:
        where.append(Store.id.like(f'%{s_id}%'))
    if s_name:
        where.append(Store.name.like(f'%{s_name}%'))
    if s_address:
        where.append(Store.address.like(f'%{s_address}%'))
    if store_type:
        where.append(Store.type == store_type)
    logging.debug(f'검색조건: {where}')

    stores, count_stores = get_stores_list(number_per_page, filtering, where)
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


@stores_bp.route('/stores/update_store/<id>', methods=['PUT'])
def update_store_info(id):
    store = request.get_json()
    logging.debug(f'수정 요청한 스토어 정보: {store}')
    update_store(store)
    store_info = get_store_by_id(id)
    logging.debug(f'수정된 스토어 정보 : {store_info}')
    return jsonify(store_info)

@stores_bp.route('/stores/delete_store/<id>', methods=['DELETE'])
def delete_store_info(id):
    delete_store_by_id(id)
    deleted_store = get_store_by_id(id)
    logging.debug(f'삭제된 스토어 : {deleted_store}')
    return jsonify({'message': f'스토어ID {id}의 정보가 삭제되었습니다.'})

@stores_bp.route('/add_store', methods=['POST'])
def add_store():
    s_id = str(uuid.uuid4())
    s_type = request.form.get('type')
    s_name = request.form.get('name')
    address = request.form.get('address')
    logging.debug(f'스토어 정보 : {s_id}, {s_name}, {s_type}, {address}')
    store = {'id': s_id, 'name': s_name, 'type': s_type, 'address': address}
    insert_result = insert_store(store)
    new_store = get_store_by_id(s_id)
    logging.debug(insert_result)
    logging.debug(new_store)
    return redirect(url_for('store_info', id=s_id))
