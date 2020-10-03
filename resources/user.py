import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

#class for user registration --> inheriting from flask_restful "Resource"-class
class UserRegister(Resource):
    #get user-data from body
    parser = reqparse.RequestParser() 
    #add arguments to aprser
    parser.add_argument('username', type = str, required = True, help = "Please, choose a username!") 
    parser.add_argument('password', type = str, required = True, help = "Please, coose a password!") 

    def post(self):

        data = UserRegister.parser.parse_args() 

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