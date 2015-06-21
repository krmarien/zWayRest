import os
basedir = os.path.abspath(os.path.dirname(__file__))

API_VERSION='/api/v1'

CSRF_ENABLED = True
SECRET_KEY = 'ba0b875d-aa57-4574-b05e-3c9c825a2bbf'

SQLALCHEMY_DATABASE_URI = 'postgresql://zwayrest:zwayrest@localhost/zwayrest'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

OAUTH2_PROVIDER_TOKEN_EXPIRES_IN = 60*60*24*30

DISABLE_AUTH = False

ZWAY_URL = 'http://127.0.0.1:8043'

SMTP_HOST = 'localhost'
SMTP_PORT = 1025
SMTP_SENDER = 'zway@localhost'
