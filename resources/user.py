import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from blacklist import BLACKLIST

#get user-data from body
_user_parser = reqparse.RequestParser()
#add arguments to parser
_user_parser.add_argument('username', type=str, required=True, help='This field cannot be blank!')
_user_parser.add_argument('password', type=str, required=True, help='This field cannot be blank!')


#class for user registration --> inheriting from flask_restful "Resource"-class
class UserRegister(Resource):
    def post(self):
        #get data from parser
        data = _user_parser.parse_args() 

        #check if username already exist --> if so return according message (and thus disregard rest of the code --> as return was done) 
        if UserModel.find_by_username(data['username']):
            return {'message' : 'This username already exist! Choose another username.'}

        user = UserModel(**data)
        user.save_to_db()

        #return success method
        return {'message': "User created successfully"}, 201 #201 is the code for "created"

    def get(self):
        return {'users' : [user.json() for user in UserModel.find_all()]}


#class for retrieveing or deleting users
class User(Resource):
    @classmethod
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message' : 'User not found'}, 404
        return user.json(), 202

    @classmethod
    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message' : 'User not found'}
        user.delete_from_db()
        return {'message' : 'User deleted.'}, 200


#class for user authentification
class UserLogin(Resource):
    @classmethod
    def post(cls):
        #get data from parser
        data = _user_parser.parse_args() 
        username = data['username']
        password = data['password']

        #find user in database
        user = UserModel.find_by_username(data['username'])

        #check that user exist and password is correct
        if user and safe_str_cmp(user.password, data['password']):
            #create an access-token (JWT) using the flask_jwt_extended funtions --> this is possicle because JWTManager is linked to the app
            access_token = create_access_token(identity=user.id, fresh=True) 
            #create a refresh-token
            refresh_token = create_refresh_token(user.id) 
            #return the tokens
            return {
                'access_token' : access_token,
                'refresh_token' : refresh_token #this is never going to change
            }, 200

        return {'message' : 'Invalid credentials!'}, 401


#class to refresh access token
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token' : new_token}, 200


class UserLogout(Resource):
    @jwt_required #because user needs to be logged in in order to log them out
    def post(self):
        jti = get_raw_jwt()['jti'] #jti is the "JWT ID", a unique identifier for that JWT
        BLACKLIST.add(jti)
        return {'message' : 'Successfully logged out.'}