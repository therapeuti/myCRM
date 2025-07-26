from flask import Blueprint
from flask import request,jsonify, abort
from database.database import *
from database.items_db import *
import uuid
import math

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
    orderby = request.args.get('orderby', default='name', type=str)
    item_type = request.args.get('type')
    name = request.args.get('name')

    filtering = {'page':page,'orderby':orderby}
    if i_id:
        filtering['id'] = i_id
    if item_type:
        filtering['type'] = item_type
    if name:
        filtering['name'] = name

    items, count_items = get_items_list(number_per_page, filtering)
    logging.debug(items)
    end_page = math.ceil(count_items / number_per_page)
    item_type = get_item_type()
    return jsonify({'items': items, 'end_page': end_page, 'item_types': item_type})



#수정
@items_bp.route('/item_info/<id>')
def get_item_info(id):
    logging.debug('아이템 정보 요청')
    item = get_item_by_id(id)
    item_sales = get_item_sales(id)
    logging.debug(item_sales)
    # 그래프 그릴 수 있게 데이터 변경..
    return jsonify('item_info.html', item=item, item_sales=item_sales)


