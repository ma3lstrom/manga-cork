import os
import logging

from flask import Flask
import flask.ext.login as flask_login
from flask.ext.sqlalchemy import SQLAlchemy

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
# Loads user from an ID and directs actions for redirects etc
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
# Determine which view to direct user if logged out
login_manager.login_view = 'login'

import mangacork.views
