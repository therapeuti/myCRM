"""
pytest 설정 및 테스트 픽스처
"""
import pytest
import os
import sys
from datetime import datetime, date

# 프로젝트 루트 디렉토리를 Python path에 추가
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from database.models import db, User, Store, Order, Item, Orderitem
from config import config

@pytest.fixture
def client():
    """테스트용 Flask 클라이언트"""
    app.config.from_object(config['testing'])
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def sample_user():
    """테스트용 샘플 사용자"""
    return {
        'id': 'test-user-id',
        'name': '테스트사용자',
        'birthdate': date(1990, 1, 1),
        'age': 34,
        'gender': '남성',
        'address': '서울시 테스트구'
    }

@pytest.fixture
def sample_store():
    """테스트용 샘플 스토어"""
    return {
        'id': 'test-store-id',
        'type': '테스트카페',
        'name': '테스트 스토어',
        'address': '서울시 테스트구 테스트로 123'
    }

@pytest.fixture
def sample_item():
    """테스트용 샘플 아이템"""
    return {
        'id': 'test-item-id',
        'type': '음료',
        'name': '테스트 아메리카노',
        'price': 4000
    }

@pytest.fixture
def db_session(client):
    """데이터베이스 세션"""
    with app.app_context():
        yield db.session