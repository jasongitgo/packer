import sys
import os

#Expand Python classes path with your app's path
#sys.path.insert(0, "/var/www/html/smilodon")

from app import create_app

#Put logging code (and imports) here ...

#Initialize WSGI app object
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
application = app