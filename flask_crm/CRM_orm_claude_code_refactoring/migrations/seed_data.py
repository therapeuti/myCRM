"""
테스트용 샘플 데이터 생성 스크립트
"""
import os
import sys
import uuid
from datetime import datetime, date

# 프로젝트 루트 디렉토리를 Python path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import db, User, Store, Order, Item, Orderitem
from app import app

def create_sample_data():
    """샘플 데이터 생성"""
    print("샘플 데이터 생성 시작...")
    
    with app.app_context():
        # 기존 데이터 확인
        if User.query.first():
            print("이미 데이터가 존재합니다. 샘플 데이터 생성을 건너뜁니다.")
            return
        
        # 샘플 사용자 생성
        users = [
            User(
                id=str(uuid.uuid4()),
                name='김철수',
                birthdate=date(1990, 1, 15),
                age=34,
                gender='남성',
                address='서울시 강남구'
            ),
            User(
                id=str(uuid.uuid4()),
                name='이영희',
                birthdate=date(1985, 5, 20),
                age=39,
                gender='여성',
                address='서울시 서초구'
            ),
            User(
                id=str(uuid.uuid4()),
                name='박민수',
                birthdate=date(1995, 8, 10),
                age=29,
                gender='남성',
                address='부산시 해운대구'
            )
        ]
        
        for user in users:
            db.session.add(user)
        
        # 샘플 스토어 생성
        stores = [
            Store(
                id=str(uuid.uuid4()),
                type='카페',
                name='스타벅스 강남점',
                address='서울시 강남구 테헤란로 123'
            ),
            Store(
                id=str(uuid.uuid4()),
                type='패스트푸드',
                name='맥도날드 서초점',
                address='서울시 서초구 서초대로 456'
            ),
            Store(
                id=str(uuid.uuid4()),
                type='베이커리',
                name='파리바게뜨 해운대점',
                address='부산시 해운대구 해운대로 789'
            )
        ]
        
        for store in stores:
            db.session.add(store)
        
        # 샘플 아이템 생성
        items = [
            Item(
                id=str(uuid.uuid4()),
                type='음료',
                name='아메리카노',
                price=4500
            ),
            Item(
                id=str(uuid.uuid4()),
                type='음료',
                name='카페라떼',
                price=5000
            ),
            Item(
                id=str(uuid.uuid4()),
                type='음식',
                name='빅맥세트',
                price=6500
            ),
            Item(
                id=str(uuid.uuid4()),
                type='음식',
                name='크로와상',
                price=3000
            ),
            Item(
                id=str(uuid.uuid4()),
                type='디저트',
                name='치즈케이크',
                price=5500
            )
        ]
        
        for item in items:
            db.session.add(item)
        
        # 중간 커밋
        db.session.commit()
        
        # 샘플 주문 생성
        orders = [
            Order(
                id=str(uuid.uuid4()),
                ordertime=datetime(2024, 1, 15, 9, 30),
                store_id=stores[0].id,
                user_id=users[0].id
            ),
            Order(
                id=str(uuid.uuid4()),
                ordertime=datetime(2024, 1, 16, 12, 15),
                store_id=stores[1].id,
                user_id=users[1].id
            ),
            Order(
                id=str(uuid.uuid4()),
                ordertime=datetime(2024, 1, 17, 15, 45),
                store_id=stores[2].id,
                user_id=users[2].id
            )
        ]
        
        for order in orders:
            db.session.add(order)
        
        # 중간 커밋
        db.session.commit()
        
        # 샘플 주문 아이템 생성
        orderitems = [
            Orderitem(
                id=str(uuid.uuid4()),
                order_id=orders[0].id,
                item_id=items[0].id,
                quantity=2
            ),
            Orderitem(
                id=str(uuid.uuid4()),
                order_id=orders[0].id,
                item_id=items[1].id,
                quantity=1
            ),
            Orderitem(
                id=str(uuid.uuid4()),
                order_id=orders[1].id,
                item_id=items[2].id,
                quantity=1
            ),
            Orderitem(
                id=str(uuid.uuid4()),
                order_id=orders[2].id,
                item_id=items[3].id,
                quantity=2
            ),
            Orderitem(
                id=str(uuid.uuid4()),
                order_id=orders[2].id,
                item_id=items[4].id,
                quantity=1
            )
        ]
        
        for orderitem in orderitems:
            db.session.add(orderitem)
        
        # 최종 커밋
        db.session.commit()
        
        print(f"샘플 데이터 생성 완료:")
        print(f"- 사용자: {len(users)}명")
        print(f"- 스토어: {len(stores)}개")
        print(f"- 아이템: {len(items)}개")
        print(f"- 주문: {len(orders)}개")
        print(f"- 주문 아이템: {len(orderitems)}개")

if __name__ == '__main__':
    create_sample_data()