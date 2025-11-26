from flask import Blueprint, current_app
from flask import send_from_directory
from database.database import *
from database.users_db import *

pages_bp = Blueprint('pages', __name__)
