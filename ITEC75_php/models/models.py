from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import Table, Column, Integer, ForeignKey, LargeBinary
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    addresses = db.relationship('Address', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)
    cart_items = db.relationship('Cart', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Address(db.Model):
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address_line = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Address {self.address_line}, {self.city}>'

from sqlalchemy import LargeBinary

class Watch(db.Model):
    __tablename__ = 'watches'
    
    id = db.Column(db.Integer, primary_key=True)
    model_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='Active')
    image = db.Column(LargeBinary, nullable=True)  # Change to LargeBinary for one image per product

    order_items = db.relationship('OrderItem', backref='watch', lazy=True)
    wishlist_items = db.relationship('Wishlist', backref='watch', lazy=True)
    cart_items = db.relationship('Cart', backref='watch', lazy=True)
    
    def __repr__(self):
        return f'<Watch {self.model_name}>'


class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='Pending')  # Added status column
    
    order_items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def __repr__(self):
        return f'<Order {self.id} - User {self.user_id}>'

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    watch_id = db.Column(db.Integer, db.ForeignKey('watches.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<OrderItem {self.id} - Order {self.order_id}>'

class Cart(db.Model):
    __tablename__ = 'cart'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    watch_id = db.Column(db.Integer, db.ForeignKey('watches.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Cart {self.id} - User {self.user_id}>'

class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    watch_id = db.Column(db.Integer, db.ForeignKey('watches.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Wishlist {self.id} - User {self.user_id}>'
