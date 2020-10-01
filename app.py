import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

#import custom classes and methods from security.py, user.py and item.py
from security import authenticate, identity
from resources.user import UserRegister 
from resources.item import Item, ItemList
from resources.store import Store, StoreList

#initiate app
app = Flask(__name__)

#tell SQLAlchemy where to find the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

#turn off Flask-SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = 'holajose' #needs to be  SECRET --> shoul not show in public code
api = Api(app) #allows to easily add ressources to app

#create JWT-object for authentication
jwt = JWT(app, authenticate, identity) 

#adds a created resource to api and define under which route it will run/be used
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register') 

#only run this if file is run, NOT if importing from this file
if __name__ == '__main__':
    #run app, NOTE: default port is already 5000, putting it in only for clarity
    app.run(port=5000, debug=True)