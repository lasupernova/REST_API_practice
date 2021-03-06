from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required, 
    get_jwt_claims, 
    jwt_optional, 
    get_jwt_identity, 
    fresh_jwt_required
)
from flask import request

#import needed model with supportgin helper-function
from models.item import ItemModel


#define resources to use within on app/api
class Item(Resource): #note: __init__ not mandatory as it is inheriting from Redsource-class
    #create parser 
    parser = reqparse.RequestParser() 

    #define whcih information to retrieve from payload AND which type it should be; 
    parser.add_argument('price', type = float, required = True, help = "This field cannot be left blank!") 
    parser.add_argument('store_id', type = int, required = True, help = "Every item needs a store-ID!") 

    @jwt_required #this checks if a valid, logged in user is making this request
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #convert ItemModel-instance into JSON in order to be able to return it
        return {'message' : 'Item not found'}, 404

    @fresh_jwt_required
    def post(self,name):
        #check if item already exists, and if so return error message
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists!'}, 400 # 400 is the status code for "bad request" 

        #call Item-class variable "parser" (see above)
        data = Item.parser.parse_args() 

        #create new itemModel instance for new item
        item = ItemModel(name, **data)

        #try inserting 
        try: 
            #insert item using insert()-method 
            item.save_to_db()
        #in case that does not work and an error is raised --> return error message
        except:
            return {'message' : 'An error occured inserting the item!'}, 500 
        #REMEMBER: for flask_restful code JSON data needs to always be returned  (not other-typed object)
        return item.json(), 201

    @jwt_required
    def delete(self, name):
        # check for admin-rights based on claims created in app.py
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message' : 'Admin privilege required!'}

        #find item by name
        item = ItemModel.find_by_name(name)

        #if it exists, delete
        if item:
            item.delete_from_db()

        return {'message' : 'Item deleted'}

    def put(self, name):
        #get data from payload
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        #if item already exists in database (= does not default to None with this next()-funtion) --> update
        if item:
            try:
                # update item price
                item.price = data['price']
            except:
                return {'message' : 'An error occured updating the item!'}, 500
        #if item does not exist yet (--> defaulted to None), create item and add to items-list
        else:
            try:
                #create new ItemModel object
                item = ItemModel(name, **data)
            except:
                return {'message' : 'An error occured inserting the item!'}, 500

        # save ItemModel object to db
        item.save_to_db()

        return item.json(), 200


#create class for items endpoint
class ItemList(Resource):
    @jwt_optional
    def get(self):
        #get jwt identity
        user_id = get_jwt_identity()
        #get item list of all items
        items = [item.json() for item in ItemModel.find_all()]

        if user_id: #if no jwt_token passed, this will return None
            return {'items' : items}, 200

        #if user not logged in, display item names only
        return {
            'items': [item['name'] for item in items],
            'message' : 'More data available if you log in.'
            }, 200
