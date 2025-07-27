from flask import Blueprint, current_app
from flask import request, jsonify, abort
from routes.stores import stores_bp
from routes.orders import orders_bp
from routes.items import items_bp
from routes.orderitems import orderitems_bp
from database.database import *
from database.users_db import *
from database.stores_db import *
from database.items_db import *
from database.orders_db import *
import logging
import math

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H-%M-%S')

api_bp = Blueprint('api', __name__)

#서브 블루프린트 등록
api_bp.register_blueprint(stores_bp)
api_bp.register_blueprint(orders_bp)
api_bp.register_blueprint(items_bp)
api_bp.register_blueprint(orderitems_bp)

number_per_page = 10
@api_bp.route('/users/')
def get_users():
    logging.debug('---------------사용자 목록 조회------------------------')
    page = request.args.get('page', default=1, type=int)
    if (page < 1) or type(page) is not int:
        page = 1
    orderby = request.args.get('orderby', default='name', type=str)
    u_id = request.args.get('id', type=str)
    name = request.args.get('name', type=str)
    address = request.args.get('address', type=str)
    gender = request.args.get('gender', type=str)
    logging.debug(f'GET 파라미터 : 페이지 {page}, 아이디 {u_id}, 이름 {name}, 주소 {address}, 성별 {gender}, 정렬기준 {orderby}')
    
    filtering = {'page': page, 'orderby': orderby}
    if u_id:
        filtering['id'] = u_id
    if name:
        filtering['name'] = name
    if address:
        filtering['address'] = address
    if gender:
        filtering['gender'] = gender
    logging.debug(f'검색조건: {filtering}')

    users, count_users = get_users_list(number_per_page, filtering)
    end_page = math.ceil(count_users / number_per_page)
    if (end_page != 0) and (page > end_page):
        abort(404)
    logging.debug(f'send_user() : {users}')
    logging.debug(f'전체 사용자 데이터 개수: {count_users}, 전체 페이지 수: {end_page}')
    return jsonify({'users':users, 'end_page':end_page})

@api_bp.route('/user_info/<id>')
def get_user_info(id):
    user = get_user_by_id(id)
    logging.debug(f'ID로 조회한 사용자: {user}')
    return jsonify(user)

@api_bp.route('/update_user/<id>', methods=['PUT'])
def update_user_info(id):
    user = request.get_json()
    logging.debug(user)
    update_user(user)
    user_info = get_user_by_id(id)
    logging.debug(user_info)
    return jsonify(user_info)

@api_bp.route('/delete_user/<id>', methods=['DELETE'])
def delete_user_info(id):
    delete_user_by_id(id)
    user = get_user_by_id(id)
    logging.debug(user)
    return jsonify({'message': f'사용자ID {id}의 정보가 삭제되었습니다.'})

@api_bp.route('/order_history/<id>')
def get_users_order_history(id):
    order_history = get_users_order(id)
    return jsonify(order_history)

@api_bp.route('/store_top5/<id>')
def get_users_store_top5(id):
    store_top5 = get_store_top5(id)
    return jsonify(store_top5)

@api_bp.route('/item_top5/<id>')
def get_users_item_top5(id):
    item_top5 = get_item_top5(id)
    return jsonify(item_top5)

@api_bp.route('/store_name/<type>')
def get_store_name_by_type(type):
    store_names = get_store_name(type)
    logging.debug(store_names)
    return jsonify(store_names)

@api_bp.route('/items')
def get_items_for_order():
    items = get_items()
    return jsonify(items)

