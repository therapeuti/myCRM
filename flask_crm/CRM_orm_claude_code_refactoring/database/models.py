from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id,
                 'name': self.name,
                 'birthdate': self.birthdate.strftime('%Y-%m-%d') if self.birthdate else None,
                 'age': self.age,
                 'gender': self.gender,
                 'address': self.address,
                 'created_at': self.created_at.isoformat() if self.created_at else None,
                 'updated_at': self.updated_at.isoformat() if self.updated_at else None}
    # 디버깅용...
    def __repr__(self):
        return f'"id":{self.id}, "name":{self.name}, "birthdate":{self.birthdate}, "age":{self.age}, "gender":{self.gender}, "address":{self.address}'
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <User {self.id}: {self.name}, {self.address}>'
    
class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id,
                'type': self.type,
                'name': self.name,
                'address': self.address}
    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Store {self.id}: {self.type}, {self.name}, {self.address}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Store {self.id}: {self.type}, {self.name}, {self.address}>'

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(36), primary_key=True)
    ordertime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    store_id = db.Column(db.String(36), db.ForeignKey('stores.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('orders', lazy=True))
    store = db.relationship('Store', backref=db.backref('orders', lazy=True))

    def to_dict(self):
        return {'id': self.id,
                'ordertime': self.ordertime.isoformat() if self.ordertime else None,
                'store_id': self.store_id,
                'user_id': self.user_id,
                'created_at': self.created_at.isoformat() if self.created_at else None}
    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Order {self.id}: {self.ordertime}, {self.store_id}, {self.user_id}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Order {self.id}: {self.ordertime}, {self.store_id}, {self.user_id}>'
        
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'id': self.id,
                'type': self.type,
                'name': self.name,
                'price': self.price}
    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Item {self.id}: {self.type}, {self.name}, {self.price}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Item {self.id}: {self.type}, {self.name}, {self.price}>'

class Orderitem(db.Model):
    __tablename__ = 'orderitems'
    
    id = db.Column(db.String(36), primary_key=True)
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    item_id = db.Column(db.String(36), db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    order = db.relationship('Order', backref=db.backref('orderitems', lazy=True))
    item = db.relationship('Item', backref=db.backref('orderitems', lazy=True))

    def to_dict(self):
        return {'id': self.id,
                'order_id': self.order_id,
                'item_id': self.item_id,
                'quantity': self.quantity,
                'created_at': self.created_at.isoformat() if self.created_at else None}
    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Orderitem {self.id}: {self.order_id}, {self.item_id}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Orderitem {self.id}: {self.order_id}, {self.item_id}>'