from app import application
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Shubham%4012@localhost/stock_app_db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(application)

class User(db.Model):
    __tablename__ = 'user'

    user_id = db.Column(db.String(100), primary_key = True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(500))
    phone_number = db.Column(db.String(100), unique = True)
    email_id = db.Column(db.String(100), unique = True)
    is_active = db.Column(db.Integer, default = 1)
    created_ts = db.Column(db.DateTime, default = func.now())
    updated_ts= db.Column(db.DateTime)
    
    def __init__(self, user_id, username, password, address, phone_number, email_id, is_active, created_ts):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.address = address
        self.phone_number = phone_number
        self.email_id = email_id
        self.is_active = is_active
        self.created_ts = created_ts
                
class Stock(db.Model):
    __tablename__ = 'stock'

    stock_id = db.Column(db.String(100), primary_key = True)
    stock_name = db.Column(db.String(100), unique = True)
    stock_description = db.Column(db.String(500))
    balance_units = db.Column(db.Integer, default = 0)
    exercise_price = db.Column(db.Integer, default= 0)
    currency = db.Column(db.String(100))
    is_active = db.Column(db.Integer, default = 0)
    created_ts = db.Column(db.DateTime, default = func.now())
    updated_ts = db.Column(db.DateTime)
    
    def __init__(self, stock_id, stock_name, stock_description, balance_units, exercise_price, currency, is_active, created_ts):
        self.stock_id = stock_id
        self.stock_name = stock_name
        self.stock_description = stock_description
        self.balance_units = balance_units
        self.exercise_price = exercise_price
        self.currency = currency
        self.is_active = is_active
        self.created_ts = created_ts

class UserStocks(db.Model):
    __tablename__ = 'userstocks'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'stock_id', name='unique_user_stock'),
    )
    
    id = db.Column(db.String(100), primary_key = True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.user_id'))
    stock_id = db.Column(db.String(100), db.ForeignKey('stock.stock_id'))
    stock_units = db.Column(db.Integer, default = 0)
    is_active = db.Column(db.Integer, default = 1)
    created_ts = db.Column(db.DateTime, default = func.now())
    updated_ts = db.Column(db.DateTime)
    
    def __init__(self, id, user_id, stock_id, stock_units, is_active, created_ts):
        self.id = id
        self.user_id = user_id
        self.stock_id = stock_id
        self.stock_units = stock_units
        self.is_active = is_active
        self.created_ts = created_ts

class Transactions(db.Model):
    __tablename__ = 'transactions'

    transaction_id = db.Column(db.String(100), primary_key = True)
    user_id = db.Column(db.String(100), db.ForeignKey('user.user_id'))
    stock_id = db.Column(db.String(100), db.ForeignKey('stock.stock_id'))
    transaction_type = db.Column(db.Integer, default = 0)
    units_exercised = db.Column(db.Integer, default = 0)
    exercised_price = db.Column(db.Integer, default = 0)
    created_ts = db.Column(db.DateTime, default = func.now())
    updated_ts = db.Column(db.DateTime)
    
    def __init__(self, transaction_id, user_id, stock_id, transaction_type, units_exercised, exercised_price, created_ts):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.stock_id = stock_id
        self.transaction_type = transaction_type
        self.units_exercised = units_exercised
        self.exercised_price = exercised_price
        self.created_ts = created_ts
        
with application.app_context():
    db.create_all()
    db.session.commit()
        
