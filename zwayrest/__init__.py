from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restful import Api
from flask_oauthlib.provider import OAuth2Provider

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')
db = SQLAlchemy(app)
oauth = OAuth2Provider(app)

oauth.init_app(app)

api = Api(app)
api.unauthorized = lambda a: a

from zwayrest.helper import oauth
