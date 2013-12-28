#!/usr/bin/env python

import webapp2
#import login 

import handlers

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}
   	   	
app = webapp2.WSGIApplication([
    ('/', handlers.MainHandler),
    ('/login', handlers.LoginHandler),
    ('/logout', handlers.LogoutHandler),
    ('/signup', handlers.SignupHandler),
    ('/welcome', handlers.WelcomeHandler)
], config=config)
