from zwayrest import db

class Action(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   name = db.Column(db.String(64), unique = True)
