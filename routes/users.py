from flask import Blueprint, current_app
from flask import send_from_directory
from database.database import *

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s [%(levelname)s] %(messages)s',
                   datefmt='%Y-%m-%d %H-%M-%S')

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def users():
    logging.debug('시작!?')
    return send_from_directory(current_app.static_folder, 'users_index.html')



@users_bp.route('/info/<id>')
def user_info(id):
    return send_from_directory(current_app.static_folder, 'user_info.html')



