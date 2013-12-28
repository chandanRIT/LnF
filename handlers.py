import webapp2
import login_module
import utils_module
import jinja_module

from table_classes.user import User
  
from webapp2_extras import sessions
from webapp2_extras import auth

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
            
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()
    
    def render(self, template, **kw):
        self.response.out.write(jinja_module.render_str(template, **kw))

    """
        Check if the user's logged-in, if not redirect him to the login page.
        Useful when the users try to use the direct urls without actually logging in. 
    """
    def check_loggedin(self):
        if not self.session :
            self.redirect('/login')
       
    """
        Check if the session's active, if so, redirect to the welcome page. 
        Useful if the the /login url is used when the session's active. 
    """     
    def check_session(self):
        uid = self.session.get('username')
        if uid:
            print "session present"
            self.redirect('/welcome')
    
class MainHandler(BaseHandler):
    def get(self):
        self.check_loggedin()
        self.redirect('/welcome')
    
class SignupHandler(BaseHandler):
    def get(self):
        #super(BaseHandler, self).get()
        self.check_session()
        self.render('signup-form.html')
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        vpassword = self.request.get('vpassword')  
        email = self.request.get('email')
        
        params = self.__validate_fields(username, password, vpassword, email)
        if params :
            self.render('signup-form.html', **params)
            return
        
        #department = self.request.get('department')
        print username
        print password
        
        user = utils_module.get_user(username)
        if user:
            msg = 'UserName already Exists'
        else:
            #validate email : not required for now
            new_user = User()
            new_user.userName = username
            new_user.password = login_module.make_password_hash(username, password, login_module.make_random_salt(5)) 
            new_user.email = email
            #@todo: test department
            new_user.department = 'test'
            new_user.active = 'false'
            new_user.put()
            self.session['username'] = username
            self.redirect('/welcome')
    
    """
        Returns a dictionary containing error messages and values for fields to auto-fill the form fields, if there are
        errors in filling the form, else None
    """        
    def __validate_fields(self, username, password, vpassword, email):
        field_error = False
        params = dict(username = username, email = email)

        if not utils_module.valid_username(username):
            params['error_username'] = "Invalid username."
            field_error = True

        if not utils_module.valid_password(password):
            params['error_password'] = "Invalid password."
            field_error = True
        elif password != vpassword:
            params['error_verify'] = "Passwords didn't match."
            field_error = True

        if not utils_module.valid_email(email):
            params['error_email'] = "Invalid email."
            field_error = True
        
        return params if field_error is True else None

class LoginHandler(BaseHandler):
    def get(self):
        self.check_session()
        #@askDinesh? logic needs to be added for the existing session
        self.render('login-form.html')
    
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        
        print 'username: ' + username
        print 'password: ' + password
        
        user = login_module.validate_login(username,password)
        if user:
            #needed to be verified : get key method
            self.session['username'] = username
            self.redirect('/welcome')
        else:
            msg ='Invalid user'
            self.redirect('/login');
            print msg
            
class WelcomeHandler(BaseHandler):
    def get(self):
        self.check_loggedin()
        self.render('welcome.html')

class LogoutHandler(BaseHandler):
    def get(self):
        self.check_loggedin()
        #self.auth.unset_session()
        #self.auth().unset_session()
        self.session.clear() #not sure if this is the right method
        self.render('logout_page.html')
