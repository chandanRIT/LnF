
from google.appengine.ext import ndb

class User(ndb.Model):
	userName = ndb.StringProperty(required=True)
	password = ndb.StringProperty(required=True)
	department = ndb.StringProperty()
	email = ndb.StringProperty(required=True)
	active = ndb.StringProperty(required=True)
	LastTimestamp = ndb.TimeProperty()

	

