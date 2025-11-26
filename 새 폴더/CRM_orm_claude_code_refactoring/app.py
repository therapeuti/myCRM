from flask import Flask
from flask import redirect, url_for, request, send_from_directory
from routes.api import api_bp
from database.models import *
from database.kiosk_db import *
from database.users_db import *
from database.stores_db import *
from database.items_db import *
from config import config
from utils.logger import setup_logging, get_logger
import uuid
import os
from datetime import datetime

def create_app(config_name=None):
    """애플리케이션 팩토리 함수"""
    app = Flask(__name__, static_folder='static')
    
    # 설정 로드
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app.config.from_object(config[config_name])
    
    # 데이터베이스 초기화
    db.init_app(app)
    
    # 로깅 설정
    setup_logging(app, app.config)
    
    # 블루프린트 등록
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

app = create_app()
logger = get_logger(__name__)

@app.errorhandler(404)
def not_found_error(error):
    logger.warning(f'404 에러: {request.url}')
    return send_from_directory(app.static_folder, 'index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f'500 에러: {str(error)}')
    return send_from_directory(app.static_folder, 'index.html'), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f'처리되지 않은 예외: {str(e)}')
    db.session.rollback()
    return send_from_directory(app.static_folder, 'index.html'), 500


@app.route('/', methods=['GET','POST'])
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    id_ = request.form.get('id')
    pw = request.form.get('pw')
    logger.info(f'로그인 시도 - 아이디: {id_}')
    
    if not id_ or not pw:
        logger.warning('로그인 실패: 아이디 또는 비밀번호 누락')
        return redirect(url_for('index', error='missing_credentials'))
    
    if id_ == app.config['ADMIN_USERNAME'] and pw == app.config['ADMIN_PASSWORD']:
        logger.info(f'관리자 로그인 성공: {id_}')
        return redirect(url_for('users'))
    else:
        logger.warning(f'로그인 실패: 잘못된 인증 정보 - {id_}')
        return redirect(url_for('index', error='invalid_credentials'))

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

@app.route('/user_login', methods=['POST'])
def user_login():
    u_id = request.form.get('id')
    logging.debug(u_id)
    login_user = get_user_by_id(u_id)
    logging.debug(login_user)
    if not login_user:
        return redirect(url_for('customer_page', message='로그인 실패'))
    else:
        login_user = get_user_by_id(u_id)
        store_type = get_store_type()
        logging.debug(store_type)
        return redirect(url_for('kiosk_page', id=u_id))
    
@app.route('/signup', methods=['POST'])
def user_signup():
    try:
        u_id = str(uuid.uuid4())
        u_name = request.form.get('name')
        birthdate_str = request.form.get('birthdate')
        gender = request.form.get('gender')
        address = request.form.get('address')
        
        if not all([u_name, birthdate_str, gender]):
            logging.warning('회원가입 필수 정보 누락')
            return redirect(url_for('customer_page', error='missing_info'))
        
        birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
        age = datetime.today().year - birthdate.year
        
        logger.info(f'새 사용자 가입 시도: {u_name}')
        
        users = {
            'id': u_id, 
            'name': u_name, 
            'birthdate': birthdate, 
            'age': age, 
            'gender': gender, 
            'address': address
        }
        
        insert_result = insert_user(users)
        logger.info(f'회원가입 완료: {u_id}')
        return redirect(url_for('kiosk_page', id=u_id))
        
    except Exception as e:
        logger.error(f'회원가입 실패: {str(e)}')
        return redirect(url_for('customer_page', error='signup_failed'))


if __name__=='__main__':
    app.run(
        debug=app.config.get('DEBUG', False),
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000)
    )