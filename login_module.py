import utils_module
import random
import string
import hashlib

def validate_login(username,password):
    user = utils_module.get_user(username)
    if user:
        if validate_password(user,password):
            return user
    return None

def validate_password(user, password):
    salt = user.password.split('|')[1]
    print 'salt: ' + salt
    
    h = make_password_hash(user.userName, password, salt)
    if h == user.password:
        return True
    return False
        #check for sessions

def make_password_hash(username, password, salt):
    #if not salt:
    #    salt=make_salt()
    h = hashlib.sha256(username + password + salt).hexdigest()
    return '%s|%s' %(h, salt)

def make_random_salt(length):
    return ''.join(random.choice(string.letters) for x in range(length))
