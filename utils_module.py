from table_classes.user import User
 
def get_user(username):
    return User.query(User.userName == username).get() 