#!flask/bin/python
from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from zwayrest import app, db
from zwayrest.command.init import InitCommand
from zwayrest.command.user import UserCommand

import os, json, random
basedir = os.path.abspath(os.path.dirname(__file__))

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('init', InitCommand)
manager.add_command('user', UserCommand)

if __name__ == '__main__':
   app.debug = True
   # app.run(host='0.0.0.0')
   manager.run()
