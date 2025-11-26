"""
데이터베이스 모델 테스트
"""
import pytest
from datetime import datetime, date
from database.models import User, Store, Order, Item, Orderitem

class TestUserModel:
    """User 모델 테스트"""
    
    def test_user_creation(self, db_session, sample_user):
        """사용자 생성 테스트"""
        user = User(**sample_user)
        db_session.add(user)
        db_session.commit()
        
        retrieved_user = User.query.get(sample_user['id'])
        assert retrieved_user is not None
        assert retrieved_user.name == sample_user['name']
        assert retrieved_user.birthdate == sample_user['birthdate']
        assert retrieved_user.age == sample_user['age']
        assert retrieved_user.gender == sample_user['gender']
        assert retrieved_user.address == sample_user['address']
    
    def test_user_to_dict(self, db_session, sample_user):
        """사용자 딕셔너리 변환 테스트"""
        user = User(**sample_user)
        db_session.add(user)
        db_session.commit()
        
        user_dict = user.to_dict()
        assert user_dict['id'] == sample_user['id']
        assert user_dict['name'] == sample_user['name']
        assert user_dict['birthdate'] == sample_user['birthdate'].strftime('%Y-%m-%d')
        assert user_dict['age'] == sample_user['age']
        assert user_dict['gender'] == sample_user['gender']
        assert user_dict['address'] == sample_user['address']
        assert 'created_at' in user_dict
        assert 'updated_at' in user_dict
    
    def test_user_str_representation(self, db_session, sample_user):
        """사용자 문자열 표현 테스트"""
        user = User(**sample_user)
        str_repr = str(user)
        assert sample_user['name'] in str_repr
        assert sample_user['address'] in str_repr

class TestStoreModel:
    """Store 모델 테스트"""
    
    def test_store_creation(self, db_session, sample_store):
        """스토어 생성 테스트"""
        store = Store(**sample_store)
        db_session.add(store)
        db_session.commit()
        
        retrieved_store = Store.query.get(sample_store['id'])
        assert retrieved_store is not None
        assert retrieved_store.type == sample_store['type']
        assert retrieved_store.name == sample_store['name']
        assert retrieved_store.address == sample_store['address']
    
    def test_store_to_dict(self, db_session, sample_store):
        """스토어 딕셔너리 변환 테스트"""
        store = Store(**sample_store)
        db_session.add(store)
        db_session.commit()
        
        store_dict = store.to_dict()
        assert store_dict['id'] == sample_store['id']
        assert store_dict['type'] == sample_store['type']
        assert store_dict['name'] == sample_store['name']
        assert store_dict['address'] == sample_store['address']

class TestItemModel:
    """Item 모델 테스트"""
    
    def test_item_creation(self, db_session, sample_item):
        """아이템 생성 테스트"""
        item = Item(**sample_item)
        db_session.add(item)
        db_session.commit()
        
        retrieved_item = Item.query.get(sample_item['id'])
        assert retrieved_item is not None
        assert retrieved_item.type == sample_item['type']
        assert retrieved_item.name == sample_item['name']
        assert retrieved_item.price == sample_item['price']
    
    def test_item_to_dict(self, db_session, sample_item):
        """아이템 딕셔너리 변환 테스트"""
        item = Item(**sample_item)
        db_session.add(item)
        db_session.commit()
        
        item_dict = item.to_dict()
        assert item_dict['id'] == sample_item['id']
        assert item_dict['type'] == sample_item['type']
        assert item_dict['name'] == sample_item['name']
        assert item_dict['price'] == sample_item['price']

class TestOrderModel:
    """Order 모델 테스트"""
    
    def test_order_creation(self, db_session, sample_user, sample_store):
        """주문 생성 테스트"""
        # 사용자와 스토어 먼저 생성
        user = User(**sample_user)
        store = Store(**sample_store)
        db_session.add(user)
        db_session.add(store)
        db_session.commit()
        
        # 주문 생성
        order = Order(
            id='test-order-id',
            ordertime=datetime(2024, 1, 1, 12, 0, 0),
            store_id=sample_store['id'],
            user_id=sample_user['id']
        )
        db_session.add(order)
        db_session.commit()
        
        retrieved_order = Order.query.get('test-order-id')
        assert retrieved_order is not None
        assert retrieved_order.store_id == sample_store['id']
        assert retrieved_order.user_id == sample_user['id']
        
        # 관계 테스트
        assert retrieved_order.user.name == sample_user['name']
        assert retrieved_order.store.name == sample_store['name']

class TestOrderitemModel:
    """Orderitem 모델 테스트"""
    
    def test_orderitem_creation(self, db_session, sample_user, sample_store, sample_item):
        """주문 아이템 생성 테스트"""
        # 필요한 엔티티들 먼저 생성
        user = User(**sample_user)
        store = Store(**sample_store)
        item = Item(**sample_item)
        db_session.add(user)
        db_session.add(store)
        db_session.add(item)
        db_session.commit()
        
        order = Order(
            id='test-order-id',
            ordertime=datetime.now(),
            store_id=sample_store['id'],
            user_id=sample_user['id']
        )
        db_session.add(order)
        db_session.commit()
        
        # 주문 아이템 생성
        orderitem = Orderitem(
            id='test-orderitem-id',
            order_id='test-order-id',
            item_id=sample_item['id'],
            quantity=2
        )
        db_session.add(orderitem)
        db_session.commit()
        
        retrieved_orderitem = Orderitem.query.get('test-orderitem-id')
        assert retrieved_orderitem is not None
        assert retrieved_orderitem.order_id == 'test-order-id'
        assert retrieved_orderitem.item_id == sample_item['id']
        assert retrieved_orderitem.quantity == 2
        
        # 관계 테스트
        assert retrieved_orderitem.order.user.name == sample_user['name']
        assert retrieved_orderitem.item.name == sample_item['name']