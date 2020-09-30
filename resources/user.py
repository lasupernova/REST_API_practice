import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

#class for user registration --> inheriting from flask_restful "Resource"-class
class UserRegister(Resource):
    #get user-data from body
    parser = reqparse.RequestParser() 

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

