import sqlite3
from db import db

#create class to save security.py users-list information in this form
class UserModel(db.Model):
    #tell SQLAlchemy the tablename where these models are going to be stored 
    __tablename__ = 'users' 

    #tell SQLAlchemy what columns the table should/does contain
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password): 
        self.username = username
        self.password = password

    def json(self):
        return {
            'id' : self.id,
            'username' : self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    #function to retrieve info from db
    @classmethod 
    def find_by_username(cls, username):
        #return User-object or None
        return cls.query.filter_by(username = username).first()

    #function to retrieve info from db
    @classmethod 
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    #function to retrieve all users 
    @classmethod 
    def find_all(cls):
        return cls.query.all()