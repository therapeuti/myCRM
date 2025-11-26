from flask import Blueprint, current_app
from flask import request, jsonify, abort
from routes.users import users_bp
from routes.stores import stores_bp
from routes.orders import orders_bp
from routes.items import items_bp
from routes.kiosk import kiosk_bp
from routes.orderitems import orderitems_bp
import logging
import math

api_bp = Blueprint('api', __name__)

#서브 블루프린트 등록
api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(stores_bp)
api_bp.register_blueprint(orders_bp)
api_bp.register_blueprint(items_bp)
api_bp.register_blueprint(orderitems_bp)
api_bp.register_blueprint(kiosk_bp)


