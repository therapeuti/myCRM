"""
사용자 데이터베이스 함수 테스트
"""
import pytest
from datetime import date
from database.users_db import (
    get_users_list, get_user_by_id, insert_user, 
    update_user, delete_user_by_id
)
from database.models import User

class TestUsersDB:
    """사용자 데이터베이스 함수 테스트"""
    
    def test_insert_user(self, db_session, sample_user):
        """사용자 삽입 테스트"""
        result = insert_user(sample_user)
        
        assert result['success'] == True
        assert '회원가입 완료' in result['message']
        
        # 데이터베이스에서 확인
        user = User.query.get(sample_user['id'])
        assert user is not None
        assert user.name == sample_user['name']
    
    def test_get_user_by_id(self, db_session, sample_user):
        """ID로 사용자 조회 테스트"""
        # 사용자 먼저 생성
        user = User(**sample_user)
        db_session.add(user)
        db_session.commit()
        
        # 조회 테스트
        retrieved_user = get_user_by_id(sample_user['id'])
        assert retrieved_user is not None
        assert retrieved_user['name'] == sample_user['name']
        assert retrieved_user['id'] == sample_user['id']
        
        # 존재하지 않는 사용자 조회
        non_existent_user = get_user_by_id('non-existent-id')
        assert non_existent_user == {}
    
    def test_get_users_list(self, db_session, sample_user):
        """사용자 목록 조회 테스트"""
        # 테스트용 사용자들 생성
        users = []
        for i in range(3):
            user_data = sample_user.copy()
            user_data['id'] = f'test-user-{i}'
            user_data['name'] = f'테스트사용자{i}'
            user = User(**user_data)
            users.append(user)
            db_session.add(user)
        db_session.commit()
        
        # 목록 조회 테스트
        filtering = {'page': 1, 'orderby': 'name'}
        users_list, count = get_users_list(10, filtering, [])
        
        assert len(users_list) == 3
        assert count == 3
        assert all('name' in user for user in users_list)
    
    def test_update_user(self, db_session, sample_user):
        """사용자 정보 업데이트 테스트"""
        # 사용자 먼저 생성
        user = User(**sample_user)
        db_session.add(user)
        db_session.commit()
        
        # 업데이트할 데이터
        update_data = {
            'id': sample_user['id'],
            'name': '업데이트된이름',
            'birthdate': '1991-01-01',
            'gender': '여성',
            'address': '업데이트된주소'
        }
        
        result = update_user(update_data)
        assert result['success'] == True
        
        # 데이터베이스에서 확인
        updated_user = User.query.get(sample_user['id'])
        assert updated_user.name == '업데이트된이름'
        assert updated_user.birthdate == date(1991, 1, 1)
        assert updated_user.gender == '여성'
        assert updated_user.address == '업데이트된주소'
        assert updated_user.age == 33  # 1991년생이므로 33세
    
    def test_update_non_existent_user(self, db_session):
        """존재하지 않는 사용자 업데이트 테스트"""
        update_data = {
            'id': 'non-existent-id',
            'name': '존재하지않는사용자',
            'birthdate': '1990-01-01',
            'gender': '남성',
            'address': '주소'
        }
        
        result = update_user(update_data)
        assert result['success'] == False
        assert '사용자가 존재하지 않습니다' in result['message']
    
    def test_delete_user_by_id(self, db_session, sample_user):
        """사용자 삭제 테스트"""
        # 사용자 먼저 생성
        user = User(**sample_user)
        db_session.add(user)
        db_session.commit()
        
        # 삭제 테스트
        result = delete_user_by_id(sample_user['id'])
        assert result['success'] == True
        
        # 데이터베이스에서 확인
        deleted_user = User.query.get(sample_user['id'])
        assert deleted_user is None
    
    def test_delete_non_existent_user(self, db_session):
        """존재하지 않는 사용자 삭제 테스트"""
        result = delete_user_by_id('non-existent-id')
        assert result['success'] == False
        assert '사용자를 찾을 수 없습니다' in result['message']