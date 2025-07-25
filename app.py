from flask import Flask
from flask import render_template, redirect, url_for, request, jsonify
from flask import flash
from routes.users import users_bp
from routes.stores import stores_bp
from routes.orders import orders_bp
from routes.items import items_bp
from routes.orderitems import orderitems_bp
from routes.api import api_bp
from database.database import *
from database.users_db import *
import logging
import math
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'my_secret'
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(stores_bp, url_prefix='/stores')
app.register_blueprint(orders_bp, url_prefix='/orders')
app.register_blueprint(items_bp, url_prefix='/items')
app.register_blueprint(orderitems_bp, url_prefix='/orderitems')
app.register_blueprint(api_bp, url_prefix='/api')

app.config['DATABASE'] = 'database/mycrm.db'

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

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