#create model first becasue resource usually relies on the model (by import) in order to get data from database
from db import db

class StoreModel(db.Model): 
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10))

    items = db.relationship('ItemModel', lazy='dynamic') 
    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items' : [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return StoreModel.query.filter_by(name=name).first() 


    def save_to_db(self): 
        db.session.add(self) #adds ItemModel-object to database --> this adds OR updates data in database
        db.session.commit() #commit changes

    def delete_from_db(self):
        #delete object
        db.session.delete(self)
        db.session.commit()