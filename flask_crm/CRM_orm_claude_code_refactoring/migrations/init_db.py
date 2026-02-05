"""
데이터베이스 초기화 및 마이그레이션 스크립트
"""
import os
import sys
import sqlite3
from datetime import datetime

# 프로젝트 루트 디렉토리를 Python path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import db, User, Store, Order, Item, Orderitem
from app import app

def backup_existing_data():
    """기존 데이터베이스 백업"""
    db_path = 'mycrm.db'
    if os.path.exists(db_path):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'mycrm_backup_{timestamp}.db'
        
        # SQLite 데이터베이스 백업
        with sqlite3.connect(db_path) as src, sqlite3.connect(backup_path) as dst:
            src.backup(dst)
        
        print(f"기존 데이터베이스를 {backup_path}로 백업했습니다.")
        return backup_path
    return None

def migrate_data(backup_path):
    """기존 데이터를 새 스키마로 마이그레이션"""
    if not backup_path or not os.path.exists(backup_path):
        print("백업 파일이 없어 데이터 마이그레이션을 건너뜁니다.")
        return
    
    try:
        # 백업 데이터베이스 연결
        backup_conn = sqlite3.connect(backup_path)
        backup_conn.row_factory = sqlite3.Row
        cursor = backup_conn.cursor()
        
        print("기존 데이터 마이그레이션 시작...")
        
        # 사용자 데이터 마이그레이션
        try:
            cursor.execute("SELECT * FROM users")
            users_data = cursor.fetchall()
            
            for user_row in users_data:
                # 날짜 형식 변환
                birthdate = user_row['birthdate']
                if isinstance(birthdate, str):
                    try:
                        birthdate = datetime.strptime(birthdate, '%Y-%m-%d').date()
                    except:
                        print(f"사용자 {user_row['id']}의 생년월일 형식 변환 실패, 건너뜀")
                        continue
                
                user = User(
                    id=user_row['id'],
                    name=user_row['name'],
                    birthdate=birthdate,
                    age=user_row['age'],
                    gender=user_row['gender'],
                    address=user_row['address']
                )
                db.session.add(user)
            
            print(f"{len(users_data)}명의 사용자 데이터를 마이그레이션했습니다.")
        except Exception as e:
            print(f"사용자 데이터 마이그레이션 오류: {e}")
        
        # 스토어 데이터 마이그레이션
        try:
            cursor.execute("SELECT * FROM stores")
            stores_data = cursor.fetchall()
            
            for store_row in stores_data:
                store = Store(
                    id=store_row['id'],
                    type=store_row['type'],
                    name=store_row['name'],
                    address=store_row['address']
                )
                db.session.add(store)
            
            print(f"{len(stores_data)}개의 스토어 데이터를 마이그레이션했습니다.")
        except Exception as e:
            print(f"스토어 데이터 마이그레이션 오류: {e}")
        
        # 아이템 데이터 마이그레이션
        try:
            cursor.execute("SELECT * FROM items")
            items_data = cursor.fetchall()
            
            for item_row in items_data:
                item = Item(
                    id=item_row['id'],
                    type=item_row['type'],
                    name=item_row['name'],
                    price=item_row['price']
                )
                db.session.add(item)
            
            print(f"{len(items_data)}개의 아이템 데이터를 마이그레이션했습니다.")
        except Exception as e:
            print(f"아이템 데이터 마이그레이션 오류: {e}")
        
        # 주문 데이터 마이그레이션
        try:
            cursor.execute("SELECT * FROM orders")
            orders_data = cursor.fetchall()
            
            for order_row in orders_data:
                # 주문 시간 형식 변환
                ordertime = order_row['ordertime']
                if isinstance(ordertime, str):
                    try:
                        ordertime = datetime.strptime(ordertime, '%Y-%m-%d %H:%M:%S')
                    except:
                        ordertime = datetime.now()
                
                order = Order(
                    id=order_row['id'],
                    ordertime=ordertime,
                    store_id=order_row['store_id'],
                    user_id=order_row['user_id']
                )
                db.session.add(order)
            
            print(f"{len(orders_data)}개의 주문 데이터를 마이그레이션했습니다.")
        except Exception as e:
            print(f"주문 데이터 마이그레이션 오류: {e}")
        
        # 주문 아이템 데이터 마이그레이션
        try:
            cursor.execute("SELECT * FROM orderitems")
            orderitems_data = cursor.fetchall()
            
            for orderitem_row in orderitems_data:
                orderitem = Orderitem(
                    id=orderitem_row['id'],
                    order_id=orderitem_row['order_id'],
                    item_id=orderitem_row['item_id'],
                    quantity=1  # 기본값
                )
                db.session.add(orderitem)
            
            print(f"{len(orderitems_data)}개의 주문 아이템 데이터를 마이그레이션했습니다.")
        except Exception as e:
            print(f"주문 아이템 데이터 마이그레이션 오류: {e}")
        
        # 변경사항 커밋
        db.session.commit()
        print("데이터 마이그레이션이 완료되었습니다.")
        
        backup_conn.close()
        
    except Exception as e:
        db.session.rollback()
        print(f"데이터 마이그레이션 중 오류 발생: {e}")

def init_database():
    """데이터베이스 초기화"""
    print("데이터베이스 초기화 시작...")
    
    with app.app_context():
        # 기존 데이터 백업
        backup_path = backup_existing_data()
        
        # 테이블 생성
        db.create_all()
        print("새로운 데이터베이스 스키마를 생성했습니다.")
        
        # 기존 데이터 마이그레이션
        if backup_path:
            migrate_data(backup_path)
        
        print("데이터베이스 초기화가 완료되었습니다.")

if __name__ == '__main__':
    init_database()