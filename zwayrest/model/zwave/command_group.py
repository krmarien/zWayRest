from zwayrest import db
from zwayrest.model.model_base import ModelBase

class CommandGroup(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    description = db.Column(db.Text())
