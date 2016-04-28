WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess' #change to something unguessable

OPENID_PROVIDERS = [
	{'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
    
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'localhost'	# Change to real email server!!!
MAIL_PORT = 2525 #listen with: "python -m smtpd -n -c DebuggingServer lochost:2525"
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['graeme.t.spence@gmail.com']

# pagination
POSTS_PER_PAGE = 3