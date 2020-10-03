import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

#import custom classes and methods from security.py, user.py and item.py
from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.item import Item, ItemList
from resources.store import Store, StoreList
# from db import db #only uncomment in localhost

#initiate app
app = Flask(__name__)

#tell SQLAlchemy where to find the database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db')

#turn off Flask-SQLAlchemy modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# allow Flask-extensions (like Flask-JWT) return their own custom errors (instead of returning generic 500-errors)
app.config['PROPAGATE_TRACK_MODIFICATIONS'] = True

#enable JWT-blacklist feature for both access and refresh tokens
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = 'holajose' # NOTE: app.config['JWT_SECRET_KEY] could be set separetely from app.secret_key for security reasons
api = Api(app) #allows to easily add ressources to app

#link JWTManageer to the app
jwt = JWTManager(app) 

#NOTE: jwt.loaders do not have to be imported, as these come with JWTManager
#create claim --> this claim can then be used in resources
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin' : True}
    return {'is_admin' : False}

#create custom message for expired tokens (instead of generic JWT-message)
@jwt.expired_token_loader
def expired_token_callback(error):
    return jsonify({
        'description' : 'The token has expired.',
        'error' : 'token_expired',
    }), 401

#called when received token is not an actual JWT (but, for example a random string)
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description' : 'Signature verification failed',
        'error' : 'invalid_token'
    }), 401

#called when no JWT was sent at all
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description' : 'Request does not contain an access token.',
        'error' : 'authorization_required'
    }), 401

#called when a non-fresh token was sent, despite requirement for fresh token
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(error):
    return jsonify({
        'description' : 'The token is not fresh.',
        'error' : 'fersh_token_required'
    }), 401

#called when revoked token was sent
@jwt.revoked_token_loader
def revoked_token_callback(error):
    return jsonify({
        'description' : 'The token has been revoked :)',
        'error' : 'revoked_token'
    }), 401

#function that returns True when user_id is in the blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    # get user_id from decrypted token --> this variable comes from JWT
    return decrypted_token['jti'] in BLACKLIST #chekc token-jti for logout purposes


#adds a created resource to api and define under which route it will run/be used
api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')

api.add_resource(UserRegister, '/register') 

#only run this if file is run, NOT if importing from this file
if __name__ == '__main__':
    db.init_app(app) #only uncomment in localhost
    #run app, NOTE: default port is already 5000, putting it in only for clarity
    app.run(port=5000, debug=True)