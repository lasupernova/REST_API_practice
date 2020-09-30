#create model firts becasue resource usually relies on the model (by import) in order to get data from database
from db import db

class StoreModel(db.Model): 
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))

    items = db.relationship('ItemModel', lazy='dynamic') #gets all items associated with specific store(-ID); if lazy=dynamic --> .all() needs to be addeed to sel.items.all() in json()-method below

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items' : [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        #use SQLAlchemy to filter: the below line does same as: "SELECT * FROM __tablename__ WHERE name=name LIMIT 1" --> without explicitly having to connect, iterate etc.
        #the below code returns an ItemModel object automatically
        return StoreModel.query.filter_by(name=name).first() #NOTE: multiple filter_by() can be applied back-to-back


    def save_to_db(self): 
        #SQLAlchemy automatically trasnlates from object to row in database
        db.session.add(self) #adds ItemModel-object to database --> this adds OR updates data in database
        db.session.commit() #commit changes

    def delete_from_db(self):
        #delete object (=automatically translated to row) from database
        db.session.delete(self)
        db.session.commit()