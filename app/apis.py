from app import application
from flask import jsonify, Response, session
from app.models import *
from app import *
import uuid
from datetime import datetime, timezone
from marshmallow import Schema, fields
from flask_restful import Resource, Api
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
import json
from sqlalchemy.sql import func

class SignUpRequest(Schema):
    username = fields.Str(default = 'username')
    password = fields.Str(default = 'password')
    address = fields.Str(default = 'address')
    phone_number = fields.Str(default = '+91 99999 55555')
    email_id = fields.Str(default = 'exmaple@abc.com')
    
class LoginRequest(Schema):
    username = fields.Str(default = 'username')
    password = fields.Str(default = 'password')
    
class APIResponse(Schema):
    message = fields.Str(dump_default = 'Success')
    
class StocksListResponse(Schema):
    stocks = fields.List(fields.Dict())
    
class StockRequest(Schema):
    stock_id = fields.Str(default="stock_id")
    units = fields.Int(default=0)

class TransactionsResponse(Schema):
    transactions = fields.List(fields.Dict())
    
class SignUpAPI(MethodResource, Resource):
    @doc(description = 'Sign up API', tags = ['SignUp API'])
    @use_kwargs(SignUpRequest, location = ('json'))
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            user = User(
                uuid.uuid4(),
                kwargs['username'],
                kwargs['password'],
                kwargs['address'],
                kwargs['phone_number'],
                kwargs['email_id'],
                1,
                func.now()
            )
            # print(datetime.now())
            # print(func.now())
            db.session.add(user)
            db.session.commit()
            return APIResponse().dump(dict(message = 'User is successfully registered')), 200
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message = f'Not able to register user : {str(e)}')), 400
        
api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)

class LoginAPI(MethodResource, Resource):
    @doc(description='Login API', tags=['Login API'])
    @use_kwargs(LoginRequest, location='json')
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            user = User.query.filter_by(username=kwargs['username'], password=kwargs['password']).first()
            
            if user:  # If user exists
                print('Logged in')
                session['user_id'] = user.user_id
                print(f'User ID: {session["user_id"]}')
                return APIResponse().dump(dict(message='User is successfully logged in')), 200
            else:
                print('Invalid credentials')
                return APIResponse().dump(dict(message='Invalid credentials')), 401  
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Unable to login user: {str(e)}')), 500
            # return jsonify({'message': f'Not able to login user : {str(e)}'}), 400
            
api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)

class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @marshal_with(APIResponse)
    def post(self, **kwargs):
        try:
            if session.get('user_id'):  # Use `session.get` to avoid potential KeyError
                session['user_id'] = None
                print('Logged out')
                return APIResponse().dump(dict(message='User is successfully logged out')), 200
            else:
                print('User not found')
                return APIResponse().dump(dict(message='User is not logged in')), 400  
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to logout user: {str(e)}')), 500
            # return jsonify({'message':f'Not able to logout user : {str(e)}'}), 400
            
api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)

class StocksListAPI(MethodResource, Resource):
    @doc(description='Stocks List API', tags=['Stocks API'])
    @marshal_with(StocksListResponse)  # marshalling
    def get(self):
        try:
            stocks = Stock.query.all()
            stocks_list = list()
            for stock in stocks:
                stock_dict = {}
                stock_dict['stock_id'] = stock.stock_id
                stock_dict['stock_name'] = stock.stock_name
                stock_dict['stock_description'] = stock.stock_description
                stock_dict['balance_units'] = stock.balance_units
                stock_dict['exercise_price'] = stock.exercise_price
                stock_dict['currency'] = stock.currency

                stocks_list.append(stock_dict)
            print(stocks_list)
            return StocksListResponse().dump(dict(stocks=stocks_list)), 200
            # return {'stocks' : dict(stocks_list)} , 200
        except Exception as e:
            return APIResponse().dump(dict(message = 'Not able to list stocks')), 400
            # return jsonify({'message':'Not able to list stocks'}), 400
            
api.add_resource(StocksListAPI, '/stocks')
docs.register(StocksListAPI)

class BuyStockAPI(MethodResource, Resource):
    @doc(description='Buy Stock API', tags=['Buy Stock API'])
    @use_kwargs(StockRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                stock_id = kwargs['stock_id']
                units = kwargs['units']
                if units <=0:
                    return APIResponse().dump(dict(message = 'Units must be more than 0.')), 400
                    # return jsonify({'message':'Units must be more than 0.'}), 400
                stock = Stock.query.filter_by(stock_id=stock_id, is_active=1).first()
                
                if stock.balance_units < units:
                    return APIResponse().dump(dict(message = 'Not enough stocks to purchase.')), 404
                    # return jsonify({'message':'Not enough stocks to purchase'}), 404
                
                stock.balance_units = stock.balance_units - units
                
                transaction = Transactions(
                    transaction_id=uuid.uuid4(),
                    user_id = session['user_id'],
                    stock_id = stock_id,
                    transaction_type = 0,
                    units_exercised = units,
                    exercised_price = stock.exercise_price,
                    created_ts = func.now()
                )
                db.session.add(transaction)
                
                user_stock = UserStocks.query.filter_by(user_id = session['user_id'], stock_id = stock_id).first()
                if not user_stock:
                    user_stock = UserStocks(
                        id = uuid.uuid4(),
                        user_id = session['user_id'],
                        stock_id = stock_id,
                        stock_units = units,
                        is_active = 1,
                        created_ts = func.now()
                    )
                    db.session.add(user_stock)
                else:
                    user_stock.stock_units = user_stock.stock_units + units
                
                db.session.commit()
                
                return APIResponse().dump(dict(message='Buy activity is successfully completed')), 200
                # return jsonify({'message':'Buy activity is successfully completed'}), 200
            else:
                print('not logged in')
                return APIResponse().dump(dict(message = 'User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to buy required stocks : {str(e)}')), 400
            # return jsonify({'message':f'Not able to buy required stocks : {str(e)}'}), 400

api.add_resource(BuyStockAPI, '/buy')
docs.register(BuyStockAPI)


class SellStockAPI(MethodResource, Resource):
    @doc(description='Sell Stock API', tags=['Sell Stock API'])
    @use_kwargs(StockRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            if session['user_id']:
                stock_id = kwargs['stock_id']
                units = kwargs['units']
                if units <=0:
                    return APIResponse().dump(dict(message = 'Units must be more than 0.')), 400
                    # return jsonify({'message':'Units must be more than 0.'}), 400
                
                stock = Stock.query.filter_by(stock_id=stock_id, is_active=1).first()
                stock.balance_units = stock.balance_units + units
                
                user_stock = UserStocks.query.filter_by(user_id = session['user_id'], stock_id = stock_id).first()
                if not user_stock:
                    return APIResponse().dump(dict(message = 'Stock not purchased yet.')), 404
                else:
                    if user_stock.stock_units < units:
                        return APIResponse().dump(dict(message = 'Not enough stocks to sell.')), 404
                        # return jsonify({'message':'Not enough stocks to sell'}), 404
                    user_stock.stock_units = user_stock.stock_units - units

                transaction = Transactions(
                    transaction_id=uuid.uuid4(),
                    user_id = session['user_id'],
                    stock_id = stock_id,
                    transaction_type = 1,
                    units_exercised = units,
                    exercised_price = stock.exercise_price,
                    created_ts = func.now()
                )
                db.session.add(transaction)
                
                db.session.commit()
                
                return APIResponse().dump(dict(message='Sell activity is successfully completed.')), 200
                # return jsonify({'message':'Sell activity is successfully completed'}), 200
            else:
                print('not logged in')
                return APIResponse().dump(dict(message = 'User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to sell required stocks : {str(e)}')), 400
            # return jsonify({'message':f'Not able to sell required stocks : {str(e)}'}), 400

api.add_resource(SellStockAPI, '/sell')
docs.register(SellStockAPI)

class HoldingsAPI(MethodResource, Resource):
    @doc(description='Holdings API', tags=['Holdings API'])
    @marshal_with(StocksListResponse)  # marshalling
    def get(self):
        try:
            if session['user_id']:
                holdings = UserStocks.query.filter_by(user_id=session['user_id'], is_active=1)
                holdings_list = list()
                for stock in holdings:
                    stock_dict = {}
                    stock_dict['stock_id'] = stock.stock_id
                    stock_dict['stock_name'] = Stock.query.filter_by(stock_id=stock.stock_id).first().stock_name
                    stock_dict['stock_units'] = stock.stock_units

                    holdings_list.append(stock_dict)
                print(holdings_list)
                return StocksListResponse().dump(dict(stocks = holdings_list)), 200
                # return {'holdings' : dict(holdings_list)} , 200
            
            else:
                print('user not logged in')
                return APIResponse().dump(dict(message = 'User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message=f'Not able to list stocks : {str(e)}')), 400
            # return jsonify({'message':'Not able to list stocks'}), 400
            
api.add_resource(HoldingsAPI, '/holdings')
docs.register(HoldingsAPI)

class TransactionsAPI(MethodResource, Resource):
    @doc(description='Transactions API', tags=['Transactions API'])
    @marshal_with(TransactionsResponse)  # marshalling
    def get(self):
        try:
            if session['user_id']:
                trans = Transactions.query.filter_by(user_id=session['user_id'])
                trans_list = list()
                for tran in trans:
                    stock_dict = {}
                    stock_dict['stock_id'] = tran.stock_id
                    stock_dict['stock_name'] = Stock.query.filter_by(stock_id=tran.stock_id).first().stock_name
                    stock_dict['units_transacted'] = tran.units_exercised
                    stock_dict['exercised_price'] = tran.exercised_price
                    stock_dict['transaction_type'] = 'Buy' if tran.transaction_type == 0 else 'Sell'
                    stock_dict['transaction_date'] = tran.created_ts

                    trans_list.append(stock_dict)
                print(trans_list)
                return TransactionsResponse().dump(dict(transactions=trans_list)), 200
                # return {'transactions' : dict(trans_list)} , 200
            
            else:
                print('user not logged in')
                return APIResponse().dump(dict(message = 'User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message='Not able to list transactions')), 400
            # return jsonify({'message':'Not able to list transactions'}), 400
            
api.add_resource(TransactionsAPI, '/transactions')
docs.register(TransactionsAPI)

class DeRegisterAPI(MethodResource, Resource):
    @doc(description='DeRegister User API', tags=['DeRegister User API'])
    @marshal_with(APIResponse)  # marshalling
    def delete(self):
        try:
            if session['user_id']:
                user = User.query.filter_by(user_id = session['user_id']).first()
                user.is_active = 0
                db.session.commit()
                session['user_id'] = None
                print('logged out')
                return APIResponse().dump(dict(message = 'User is successfully de registered')), 200
                # return jsonify({'message':'User is successfully de registered'}), 200
            else:
                print('user not logged in')
                return APIResponse().dump(dict(message = 'User is not logged in')), 401
                # return jsonify({'message':'User is not logged in'}), 401
        except Exception as e:
            print(str(e))
            return APIResponse().dump(dict(message = f'Not able to de-register user : {str(e)}')), 400
            # return jsonify({'message':f'Not able to de-register user : {str(e)}'}), 400

api.add_resource(DeRegisterAPI, '/deregister')
docs.register(DeRegisterAPI)
       