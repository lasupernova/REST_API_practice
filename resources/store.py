from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message' : 'Store not found!'}, 404  
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message' : f'A store with name {name} already exists!'}, 400

        try:
            store = StoreModel(name)
            store.save_to_db()
        except:
            return {'message' : 'An error occured creating the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message' : f'Store named {name} deleted.'}, 200 
        return {'message' : f'A store of the name {name} does now exist!'}, 400


class StoreList(Resource):
    def get(self):
        return {'store' : [store.json() for store in StoreModel.query.all()]}




