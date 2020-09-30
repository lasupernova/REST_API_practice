#import User-class from user.py 
from models.user import UserModel
#import this function which compares strings
from werkzeug.security import safe_str_cmp

#function to authenticate user --> compare userpassword to mappings password
def authenticate(username, password):
    user = UserModel.find_by_username(username) 
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id) 