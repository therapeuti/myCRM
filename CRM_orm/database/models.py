from flask_sqlalchemy import SQLAlchemy
from datetime import datatime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    birthdate = db.Column(db.Datatime)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    address = db.Column(db.String)

    # 디버깅용...
    def __repr__(self):
        return f'출력 : <User {self.id}: {self.name}, {self.address}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <User {self.id}: {self.name}, {self.address}>'
    
class Store(db.Model):
    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Store {self.id}: {self.type}, {self.name}, {self.address}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Store {self.id}: {self.type}, {self.name}, {self.address}>'

class Order(db.Model):
    id = db.Column(db.String, primary_key=True)
    ordertime = db.Column(db.Datetime)
    store_id = db.Column(db.String, db.ForeignKey('store.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Order {self.id}: {self.ordertime}, {self.store_id}, {self.user_id}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Order {self.id}: {self.ordertime}, {self.store_id}, {self.user_id}>'
        
class Item(db.Model):
    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Item {self.id}: {self.type}, {self.name}, {self.price}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Item {self.id}: {self.type}, {self.name}, {self.price}>'

class Orderitem(db.Model):
    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String, db.ForeignKey('order.id'))
    item_id = db.Column(db.String, db.ForeignKey('item.id'))

    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Orderitem {self.id}: {self.order_id}, {self.item_id}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Orderitem {self.id}: {self.order_id}, {self.item_id}>'