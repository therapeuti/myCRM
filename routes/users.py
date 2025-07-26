from flask import Blueprint, current_app
from flask import send_from_directory, redirect, url_for, request
from database.database import *
from database.users_db import *
import uuid
from datetime import datetime

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s [%(levelname)s] %(messages)s',
                   datefmt='%Y-%m-%d %H-%M-%S')

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def users():
    logging.debug('시작!?')
    return send_from_directory(current_app.static_folder, 'users_index.html')

@users_bp.route('/add_user', methods=['POST'])
def add_user():
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
    return redirect(url_for('users.user_info', id=u_id))


@users_bp.route('/info/<id>')
def user_info(id):
    return send_from_directory(current_app.static_folder, 'user_info.html')



