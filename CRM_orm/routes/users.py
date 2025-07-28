from flask import Blueprint, abort
from flask import request, jsonify, redirect, url_for
from database.database import *
from database.users_db import *
from database.stores_db import *
from database.items_db import *
from database.models import *
import math
import uuid
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s [%(levelname)s] %(messages)s',
                   datefmt='%Y-%m-%d %H-%M-%S')

users_bp = Blueprint('users', __name__)

number_per_page = 10
@users_bp.route('/users/')
def get_users():
    logging.debug('---------------사용자 목록 조회------------------------')
    page = request.args.get('page', default=1, type=int)
    if (page < 1) or type(page) is not int:
        page = 1
    orderby = request.args.get('orderby', default='name', type=str)
    u_id = request.args.get('id', type=str)
    u_name = request.args.get('name', type=str)
    u_address = request.args.get('address', type=str)
    u_gender = request.args.get('gender', type=str)
    logging.debug(f'GET 파라미터 : 페이지 {page}, 아이디 {u_id}, 이름 {u_name}, 주소 {u_address}, 성별 {u_gender}, 정렬기준 {orderby}')
    
    filtering = {'page': page, 'orderby': orderby}
    where = []
    if u_id:
        where.append(User.id.like(f'%{u_id}%'))
    if u_name:
        where.append(User.name.like(f'%{u_name}%'))
    if u_address:
        where.append(User.address.like(f'%{u_address}%'))
    if u_gender:
        where.append(User.gender == u_gender)
    logging.debug(f'검색조건: {where}')

    users, count_users = get_users_list(number_per_page, filtering, where)
    end_page = math.ceil(count_users / number_per_page)
    if (end_page != 0) and (page > end_page):
        abort(404)
    logging.debug(f'send_user() : {users}')
    logging.debug(f'전체 사용자 데이터 개수: {count_users}, 전체 페이지 수: {end_page}')
    return jsonify({'users':users, 'end_page':end_page})

@users_bp.route('/user_info/<id_>')
def get_user_info(id_):
    user = get_user_by_id(id_)
    logging.debug(f'ID로 조회한 사용자: {user}')
    return jsonify(user)

@users_bp.route('/update_user/<id_>', methods=['PUT'])
def update_user_info(id_):
    user = request.get_json()
    logging.debug(user)
    update_user(user)
    user_info = get_user_by_id(id_)
    logging.debug(user_info)
    return jsonify(user_info)

@users_bp.route('/delete_user/<id_>', methods=['DELETE'])
def delete_user_info(id_):
    delete_user_by_id(id_)
    user = get_user_by_id(id_)
    logging.debug(user)
    return jsonify({'message': f'사용자ID {id_}의 정보가 삭제되었습니다.'})

@users_bp.route('/order_history/<id_>')
def get_users_order_history(id_):
    order_history = get_users_order(id_)
    return jsonify(order_history)

@users_bp.route('/store_top5/<id_>')
def get_users_store_top5(id_):
    store_top5 = get_store_top5(id_)
    return jsonify(store_top5)

@users_bp.route('/item_top5/<id_>')
def get_users_item_top5(id_):
    item_top5 = get_item_top5(id_)
    return jsonify(item_top5)


@users_bp.route('/add_user', methods=['POST'])
def add_user():
    u_id = str(uuid.uuid4())
    u_name =  request.form.get('name')
    birthdate =  request.form.get('birthdate')
    birthdate =  datetime.strptime(birthdate, '%Y-%m-%d')
    logging.debug(birthdate)
    age = datetime.today().year - birthdate.year
    birthdate = birthdate.strftime('%Y-%m-%d')
    logging.debug(birthdate)
    gender =  request.form.get('gender')
    address =  request.form.get('address')
    logging.debug(f'사용자 정보 : {u_id}, {u_name}, {birthdate}, {gender}, {age}, {address}')
    user = {'id':u_id, 'name':u_name, 'birthdate':birthdate, 'age':age, 'gender':gender, 'address':address}
    insert_result = insert_user(user)
    logging.debug(insert_result)
    new_user = get_user_by_id(u_id)
    logging.debug(new_user)
    return redirect(url_for('user_info', id=u_id))


