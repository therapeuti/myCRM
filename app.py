from flask import Flask
from flask import render_template, redirect, url_for, request, jsonify, send_from_directory
from flask import flash
from routes.users import users_bp
from routes.api import api_bp
from database.database import *
from database.users_db import *
from database.stores_db import *
from database.items_db import *
import logging
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'my_secret'
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(api_bp, url_prefix='/api')

app.config['DATABASE'] = 'database/mycrm.db'

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/stores/')
def stores():
    return send_from_directory(app.static_folder, 'stores_index.html')

@app.route('/orders/')
def orders():
    return send_from_directory(app.static_folder, 'orders_index.html')

@app.route('/items/')
def items():
    return send_from_directory(app.static_folder, 'items_index.html')

@app.route('/orderitems/')
def orderitems():
    return send_from_directory(app.static_folder, 'orderitems_index.html')

@app.route('/stores/add_store', methods=['POST'])
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

@app.route('/items/add_item', methods=['POST'])
def add_item():
    i_id = str(uuid.uuid4())
    i_type = request.form.get('type', type=str)
    name = request.form.get('name', type=str)
    price = request.form.get('price', type=int)
    item = {'id': i_id, 'type': i_type, 'name': name, 'price': price}
    new_item = insert_item(item)
    logging.debug(f'추가된 아이템: {new_item}')
    return redirect(url_for('item_info', id=i_id))

@app.route('/stores/info/<id>')
def store_info(id):
    logging.debug('스토어 상세 페이지')
    return send_from_directory(app.static_folder, 'store_info.html')

@app.route('/orders/info/<id>')
def order_info(id):
    logging.debug('오더 상세 페이지')
    return send_from_directory(app.static_folder, 'order_info.html')

@app.route('/item_info/<id>')
def item_info(id):
    return send_from_directory(app.static_folder, 'item_info.html')





@app.route('/admin_login', methods=['POST'])
def admin_login():
    id = request.form.get('id')
    pw = request.form.get('pw')
    logging.debug(f'로그인 폼 제출 : 아이디는 {id}, 비번은 {pw}')
    return redirect(url_for('users.users'))

@app.route('/customer')
def customer_page():
    
    return render_template('signup.html')

@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        u_id = request.args.get('id')
    if request.method == 'POST':
        u_id = request.form.get('id')
    logging.debug(u_id)
    login_user = get_user_by_id(u_id)
    logging.debug(login_user)
    # if u_id == 'admin':
    #     login_user = 'admin'
    #     return render_template('kiosk.html', login_user=login_user)
    if not login_user:
        flash('로그인 실패 : 사용자 정보 없음')
        return redirect(url_for('customer_page'))
    else:
        login_user = get_user_by_id(u_id)
        store_type = get_store_type()
        logging.debug(store_type)
        return render_template('kiosk.html', login_user=login_user, store_type=store_type) 
    



@app.route('/signup', methods=['POST'])
def user_signup():
    u_id = str(uuid.uuid4())
    u_name =  request.form.get('name')
    birthdate =  request.form.get('birthdate')
    birthdate =  datetime.strptime(birthdate, '%Y-%m-%d')
    age = datetime.today().year - birthdate.year
    birthdate = birthdate.strftime('%Y-%m-%d')
    gender =  request.form.get('gender')
    address =  request.form.get('address')
    logging.debug(f'사용자 정보 : {u_id}, {u_name}, {birthdate}, {gender}, {age}, {address}')
    users = {'id':u_id, 'name':u_name, 'birthdate':birthdate, 'age':age, 'gender':gender, 'address':address}
    insert_result = insert_user(users)
    logging.debug(insert_result)
    new_user = get_user_by_id(u_id)
    logging.debug(new_user)
    return redirect(url_for('user_login', id=u_id))

@app.route('/add_order', methods=['POST'])
def add_order():
    logging.debug(request.get_json())
    user_id = request.get_json()['user_id']
    store_id = request.get_json()['store_id']
    item_ids = request.get_json()['items']
    order_id = str(uuid.uuid4())
    ordertime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    logging.debug(ordertime)
    order_data = {'id': order_id, 'ordertime': ordertime, 'store_id': store_id, 'user_id': user_id}
    new_order = insert_order(order_data)
    logging.debug(f'주문이 들어왔습니다.  {new_order}')
    orderitems = []
    for i in item_ids:
        orderitem_id = str(uuid.uuid4())
        orderitem = {'id': orderitem_id, 'order_id': order_id, 'item_id': i}
        orderitems.append(orderitem)
    new_orderitems = insert_orderitem(orderitems)
    logging.debug(f'삽입된 주문아이템 데이터: {orderitems}')
    return jsonify({'order':new_order, 'orderitems':new_orderitems})

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)