from flask import Flask
from flask import redirect, url_for, request, send_from_directory
from flask import flash
from routes.api import api_bp
from database.models import *
from database.kiosk_db import *
from database.users_db import *
from database.stores_db import *
from database.items_db import *
import logging
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.secret_key = 'my_secret'
app.register_blueprint(api_bp, url_prefix='/api')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mycrm.db'
db.init_app(app)


@app.route('/', methods=['GET','POST'])
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    id_ = request.form.get('id')
    pw = request.form.get('pw')
    logging.debug(f'로그인 폼 제출 : 아이디는 {id_}, 비번은 {pw}')
    return redirect(url_for('users'))

@app.route('/users/')
def users():
    return send_from_directory(app.static_folder, 'users_index.html')

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

@app.route('/users/info/<id>')
def user_info(id):
    return send_from_directory(app.static_folder, 'user_info.html')

@app.route('/stores/info/<id>')
def store_info(id):
    logging.debug('스토어 상세 페이지')
    return send_from_directory(app.static_folder, 'store_info.html')

@app.route('/orders/info/<id>')
def order_info(id):
    logging.debug('오더 상세 페이지')
    return send_from_directory(app.static_folder, 'order_info.html')

@app.route('/items/info/<id>')
def item_info(id):
    return send_from_directory(app.static_folder, 'item_info.html')

@app.route('/customer')
def customer_page():
    return send_from_directory(app.static_folder, 'signup.html')
    
@app.route('/kiosk/<id>')
def kiosk_page(id):
    return send_from_directory(app.static_folder, 'kiosk.html')

@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method == 'GET':
        u_id = request.args.get('id')
    if request.method == 'POST':
        u_id = request.form.get('id')
    logging.debug(u_id)
    login_user = get_user_by_id(u_id)
    logging.debug(login_user)
    if not login_user:
        flash('로그인 실패 : 사용자 정보 없음')
        return redirect(url_for('customer_page'))
    else:
        login_user = get_user_by_id(u_id)
        store_type = get_store_type()
        logging.debug(store_type)
        return redirect(url_for('kiosk_page', id=u_id)) 
    
@app.route('/signup', methods=['POST'])
def user_signup():
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
    users = {'id':u_id, 'name':u_name, 'birthdate':birthdate, 'age':age, 'gender':gender, 'address':address}
    insert_result = insert_user(users)
    logging.debug(insert_result)
    new_user = get_user_by_id(u_id)
    logging.debug(new_user)
    return redirect(url_for('kiosk_page', id=u_id))


if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)