from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    birthdate = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    address = db.Column(db.String)

    def to_dict(self):
        return {'id': self.id,
                 'name': self.name,
                 'birthdate': self.birthdate,
                 'age': self.age,
                 'gender': self.gender,
                 'address': self.address}
    # 디버깅용...
    def __repr__(self):
        return f'"id":{self.id}, "name":{self.name}, "birthdate":{self.birthdate}, "age":{self.age}, "gender":{self.gender}, "address":{self.address}'
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <User {self.id}: {self.name}, {self.address}>'
    
class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    address = db.Column(db.String)

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
    id = db.Column(db.String, primary_key=True)
    ordertime = db.Column(db.String)
    store_id = db.Column(db.String, db.ForeignKey('store.id'))
    user_id = db.Column(db.String, db.ForeignKey('user.id'))

    def to_dict(self):
        return {'id': self.id,
                'ordertime': self.ordertime,
                'store_id': self.store_id,
                'user_id': self.user_id}
    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Order {self.id}: {self.ordertime}, {self.store_id}, {self.user_id}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Order {self.id}: {self.ordertime}, {self.store_id}, {self.user_id}>'
        
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.String, primary_key=True)
    type = db.Column(db.String)
    name = db.Column(db.String)
    price = db.Column(db.Integer)

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
    
    id = db.Column(db.String, primary_key=True)
    order_id = db.Column(db.String, db.ForeignKey('order.id'))
    item_id = db.Column(db.String, db.ForeignKey('item.id'))

    def to_dict(self):
        return {'id': self.id,
                'order_id': self.order_id,
                'item_id': self.item_id}
    # 디버깅용...
    def __repr__(self):
        return f'출력 : <Orderitem {self.id}: {self.order_id}, {self.item_id}>'    
    # 문자열로 출력...
    def __str__(self):
        return f'문자열 변환 : <Orderitem {self.id}: {self.order_id}, {self.item_id}>'