#use SQLAlchemy instead of sqlite3 to interact with database
from db import db

#let ItemModel inherit from db.Model (a SQLAlchemy model) --> to create mapping between class-objects and database
#SQLAlchemy takes care of all conenction-stuff (connecting, commiting etc) and facilitates things as filtering from table
class ItemModel(db.Model): 
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))
    price = db.Column(db.Float(precision = 2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) #"link" to stores-table --> foreign key is the id-column in stores-table
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price' : self.price}

    @classmethod
    def find_by_name(cls, name):
        #use SQLAlchemy to filter: the below line does same as: "SELECT * FROM __tablename__ WHERE name=name LIMIT 1" --> without explicitly having to connect, iterate etc.
        #the below code returns an ItemModel object automatically
        return ItemModel.query.filter_by(name=name).first() #NOTE: multiple filter_by() can be applied back-to-back


    def save_to_db(self): 
        #SQLAlchemy automatically trasnlates from object to row in database
        db.session.add(self) #adds ItemModel-object to database --> this adds OR updates data in database
        db.session.commit() #commit changes

    def delete_from_db(self):
        #delete object (=automatically translated to row) from database
        db.session.delete(self)
        db.session.commit()