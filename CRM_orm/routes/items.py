from flask import Blueprint
from flask import request,jsonify, abort, redirect, url_for
from database.database import *
from database.items_db import *
import math
import uuid

logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s [%(levelname)s] %(message)s',
                       datefmt='%Y-%m-%d %H-%M-%S')

items_bp = Blueprint('items', __name__)

number_per_page = 10
@items_bp.route('/items/')
def get_items():
    logging.debug('----- 아이템 목록 조회 -------')
    page = request.args.get('page', default=1, type=int)
    if (page < 1) or type(page) is not int:
        page = 1
    i_id = request.args.get('id')
    i_name = request.args.get('name')
    orderby = request.args.get('orderby', default='name', type=str)
    item_type = request.args.get('type')

    filtering = {'page':page,'orderby':orderby}
    where = []
    if i_id:
        where.append(Item.id.like(f'%{i_id}%'))
    if i_name:
        where.append(Item.name.like(f'%{i_name}%'))
    if item_type:
        where.append(Item.type == item_type)
    logging.debug(f'검색조건: {where}')

    items, count_items = get_items_list(number_per_page, filtering, where)
    logging.debug(items)
    end_page = math.ceil(count_items / number_per_page)
    # item_type = get_item_type()
    item_type = []
    return jsonify({'items': items, 'end_page': end_page, 'item_types': item_type})

@items_bp.route('/item_info/<id>')
def get_item_info(id):
    logging.debug('아이템 정보 요청')
    item = get_item_by_id(id)
    item_types = get_item_type()
    return jsonify({'item': item, 'item_types':item_types})

@items_bp.route('/items/monthly_sales/<id>')
def get_items_monthly_sales(id):
    item_sales = get_item_sales(id)
    logging.debug(f'최근 1년간 월간 매출액 : {item_sales}')
    return jsonify(item_sales)

@items_bp.route('/items/update_item/<id>', methods=['PUT'])
def update_item_info(id):
    item = request.get_json()
    logging.debug(f'수정 요청한 아이템 정보: {item}')
    update_item(item)
    item_info = get_item_by_id(id)
    logging.debug(f'수정된 아이템 정보 : {item_info}')
    return jsonify(item_info)

@items_bp.route('/items/delete_item/<id>', methods=['DELETE'])
def delete_item(id):
    delete_item_by_id(id)
    deleted_item = get_item_by_id(id)
    logging.debug(f'삭제된 아이템 : {deleted_item}')
    return jsonify({'message': f'아이템ID {id}의 정보가 삭제되었습니다.'})

@items_bp.route('/add_item', methods=['POST'])
def add_item():
    i_id = str(uuid.uuid4())
    i_type = request.form.get('type', type=str)
    name = request.form.get('name', type=str)
    price = request.form.get('price', type=int)
    item = {'id': i_id, 'type': i_type, 'name': name, 'price': price}
    new_item = insert_item(item)
    logging.debug(f'추가된 아이템: {new_item}')
    return redirect(url_for('item_info', id=i_id))
