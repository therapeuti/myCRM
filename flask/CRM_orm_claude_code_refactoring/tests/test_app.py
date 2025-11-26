"""
Flask 애플리케이션 라우트 테스트
"""
import pytest
from urllib.parse import urlparse

class TestAppRoutes:
    """애플리케이션 라우트 테스트"""
    
    def test_index_route(self, client):
        """인덱스 페이지 테스트"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_admin_login_success(self, client):
        """관리자 로그인 성공 테스트"""
        response = client.post('/admin_login', data={
            'id': 'admin',
            'pw': 'admin123'
        })
        assert response.status_code == 302  # 리다이렉트
        
        # 리다이렉트 위치 확인
        location = response.headers.get('Location')
        assert '/users/' in location
    
    def test_admin_login_failure(self, client):
        """관리자 로그인 실패 테스트"""
        response = client.post('/admin_login', data={
            'id': 'wrong_user',
            'pw': 'wrong_password'
        })
        assert response.status_code == 302  # 리다이렉트
        
        # 에러와 함께 인덱스로 리다이렉트
        location = response.headers.get('Location')
        parsed_url = urlparse(location)
        assert parsed_url.path == '/'
        assert 'error=invalid_credentials' in parsed_url.query
    
    def test_admin_login_missing_credentials(self, client):
        """인증 정보 누락 테스트"""
        response = client.post('/admin_login', data={
            'id': '',
            'pw': ''
        })
        assert response.status_code == 302
        
        location = response.headers.get('Location')
        parsed_url = urlparse(location)
        assert parsed_url.path == '/'
        assert 'error=missing_credentials' in parsed_url.query
    
    def test_users_route(self, client):
        """사용자 페이지 라우트 테스트"""
        response = client.get('/users/')
        assert response.status_code == 200
    
    def test_stores_route(self, client):
        """스토어 페이지 라우트 테스트"""
        response = client.get('/stores/')
        assert response.status_code == 200
    
    def test_orders_route(self, client):
        """주문 페이지 라우트 테스트"""
        response = client.get('/orders/')
        assert response.status_code == 200
    
    def test_items_route(self, client):
        """아이템 페이지 라우트 테스트"""
        response = client.get('/items/')
        assert response.status_code == 200
    
    def test_user_info_route(self, client):
        """사용자 상세 페이지 라우트 테스트"""
        response = client.get('/users/info/test-id')
        assert response.status_code == 200
    
    def test_store_info_route(self, client):
        """스토어 상세 페이지 라우트 테스트"""
        response = client.get('/stores/info/test-id')
        assert response.status_code == 200
    
    def test_order_info_route(self, client):
        """주문 상세 페이지 라우트 테스트"""
        response = client.get('/orders/info/test-id')
        assert response.status_code == 200
    
    def test_item_info_route(self, client):
        """아이템 상세 페이지 라우트 테스트"""
        response = client.get('/items/info/test-id')
        assert response.status_code == 200
    
    def test_customer_page_route(self, client):
        """고객 페이지 라우트 테스트"""
        response = client.get('/customer')
        assert response.status_code == 200
    
    def test_kiosk_page_route(self, client):
        """키오스크 페이지 라우트 테스트"""
        response = client.get('/kiosk/test-id')
        assert response.status_code == 200
    
    def test_user_signup(self, client):
        """사용자 회원가입 테스트"""
        response = client.post('/signup', data={
            'name': '테스트사용자',
            'birthdate': '1990-01-01',
            'gender': '남성',
            'address': '서울시 테스트구'
        })
        assert response.status_code == 302  # 리다이렉트
        
        # 키오스크 페이지로 리다이렉트되는지 확인
        location = response.headers.get('Location')
        assert '/kiosk/' in location
    
    def test_user_signup_missing_info(self, client):
        """회원가입 정보 누락 테스트"""
        response = client.post('/signup', data={
            'name': '',  # 이름 누락
            'birthdate': '1990-01-01',
            'gender': '남성',
            'address': '서울시 테스트구'
        })
        assert response.status_code == 302
        
        location = response.headers.get('Location')
        parsed_url = urlparse(location)
        assert parsed_url.path == '/customer'
        assert 'error=missing_info' in parsed_url.query
    
    def test_404_error_handler(self, client):
        """404 에러 핸들러 테스트"""
        response = client.get('/non-existent-page')
        assert response.status_code == 404