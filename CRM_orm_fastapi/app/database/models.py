"""
SQLAlchemy ORM 모델 정의
FastAPI와 호환되는 SQLAlchemy 2.0 스타일의 모델입니다.
"""

from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base


class User(Base):
    """사용자 모델"""
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    name = Column(String)
    birthdate = Column(String)
    age = Column(Integer)
    gender = Column(String)
    address = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'birthdate': self.birthdate,
            'age': self.age,
            'gender': self.gender,
            'address': self.address
        }

    def __repr__(self):
        return f'<User {self.id}: {self.name}>'


class Store(Base):
    """매장 모델"""
    __tablename__ = 'stores'

    id = Column(String, primary_key=True)
    type = Column(String)
    name = Column(String)
    address = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'address': self.address
        }

    def __repr__(self):
        return f'<Store {self.id}: {self.name}>'


class Order(Base):
    """주문 모델"""
    __tablename__ = 'orders'

    id = Column(String, primary_key=True)
    ordertime = Column(String)
    store_id = Column(String, ForeignKey('stores.id'))
    user_id = Column(String, ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'ordertime': self.ordertime,
            'store_id': self.store_id,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f'<Order {self.id}: {self.ordertime}>'


class Item(Base):
    """상품 모델"""
    __tablename__ = 'items'

    id = Column(String, primary_key=True)
    type = Column(String)
    name = Column(String)
    price = Column(Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'name': self.name,
            'price': self.price
        }

    def __repr__(self):
        return f'<Item {self.id}: {self.name}>'


class Orderitem(Base):
    """주문-상품 관계 모델"""
    __tablename__ = 'orderitems'

    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey('orders.id'))
    item_id = Column(String, ForeignKey('items.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'item_id': self.item_id
        }

    def __repr__(self):
        return f'<Orderitem {self.id}>'