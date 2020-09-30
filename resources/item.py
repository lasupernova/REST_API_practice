from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from flask import request #request --> when someone (e.g. Postman or CLient etc) makes request to API, that request gets saved in this variable

#import needed model with supportgin helper-function
from models.item import ItemModel


#api works with ressources and every ressource needs to be a class - here: inheriting from Resource-class, e.g:
#define resources to use within on app/api
#one class per working endpoint; one function per action (e.g. GET, POST, DELETE etc.)
class Item(Resource): #note: __init__ not mandatory as it is inheriting from Redsource-class

    #parser is used multiple times within different functions 
    #--> pull out parser code and make it intrinsic part of Item-class, by putting it outside of funtions
    #--> can then be used by all Item-methods:

    #create parser to only request information of interest (here: only price NOT name, in case both should be in the payload)
    parser = reqparse.RequestParser() 

    #define whcih information to retrieve from payload AND which type it should be; 
    # use require to make this info mandatory as well as message in case this info should not be gotten from payload
    #this will ook in JSON payloads, but also other things like form pasyloads (gotten from form-fields in HTML)
    parser.add_argument('price', type = float, required = True, help = "This field cannot be left blank!") 
    parser.add_argument('store_id', type = int, required = True, help = "Every item needs a store-ID!") 

    @jwt_required() #decorator, that mandates we have to authenticate before calling the get method
    def get(self,name): #function names must co-incide with action defined in Postman
        #now: retrieving item info from database --> not as preciously from list

        #use find_by_name() to not have duplicate code
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() #convert ItemModel-instance into JSON in order to be able to return it
        return {'message' : 'Item not found'}, 404

    def post(self,name):
        #check if item already exists, and if so return error message
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists!'}, 400 # 400 is the status code for "bad request" 

        #call Item-class variable "parser" (see above)
        data = Item.parser.parse_args() 

        #create new itemModel instance for new item
        item = ItemModel(name, **data)

        #try inserting --> try/except can also be done for GET and other methods
        try: 
            #insert item using insert()-method 
            item.save_to_db()
        #in case that does not work and an error is raised --> return error message
        except:
            return {'message' : 'An error occured inserting the item!'}, 500 # 500 is the status code for "internal server error"

        #REMEMBER: for flask_restful code JSON data needs to always be returned  (not other-tyoed object)
        return item.json(), 201 #so that the application or client knows that this has happened, add 201 as status code for "created"

    def delete(self, name):
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
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #.json() because item is a Item-class object 
