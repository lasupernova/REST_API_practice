from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from db import db

#import custom classes and methods from security.py, user.py and item.py
from security import authenticate, identity
from resources.user import UserRegister # a Resource added to api ( =Api(app) )
from resources.item import Item, ItemList
from resources.store import Store, StoreList

#initiate app
app = Flask(__name__)

#tell SQLAlchemy where to find the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

#turn off Flask-SQLAlchemy modification tracker, as SQLAlchemy has its own --> only changes the extensions behavior
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.secret_key = 'estoessecreto' #needs to be  SECRET --> shoul not show in public code
api = Api(app) #allows to easily add ressources to app

#create tables using SQLAlchemy
@app.before_first_request #decorator that is influencing method after it, to only run on first request
def create_tables():
    db.create_all() #create all tables in this file, unless they exist already --> here: tables  imported from item.py and user.py resource-files (which in turn import from the item.py and user.py model-files)

###create JWT-object for authentication
#-->JWT creates new endpoint("/auth") 
# --> when we call /auth, we send it a username and a password and JWT-extension, gets username and pw and sends it over to authenticate()
# -->we are then going to find the correct User-object using that information and compare its password to the one received through /auth-endpoint
#if they match --> user is returned and becomes the identity
# --> /auth-endpoint returns a JW-token, which does not do anything in itself, but can be send to the next request we make
#so when we send a JW-token, what JWT does is, it calls the identity function 
#  --> then it uses the JWT to get the userID and thus gets correct user for the ID that the JWT represents
# -> if it can do that it means that the user was authenticated, the JWT is valid and all is good
jwt = JWT(app, authenticate, identity) #JWT-object si going to use app, authenticate() and identity() to allow for user authentication

#adds a created resource to api and define under which route it will run/be used
#go to Postman and check if this works correctly; when the defined route is used, the 'Item'-resource functions should run --> make sure app is running ("python app.py" in cmd)
api.add_resource(Item, '/item/<string:name>') #here: e.g. runs under http://127.0.0.1:5000/item/<item_name>
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register') #this means: if we go to "/register", this will call UserRegister and all its methods

#only run this if file is run, NOT if importing from this file
if __name__ == '__main__':
    db.init_app(app)
    #run app, NOTE: default port is already 5000, putting it in only for clarity
    #debug=True --> renders nice HTML error message in case something goes wrong
    app.run(port=5000, debug=True)