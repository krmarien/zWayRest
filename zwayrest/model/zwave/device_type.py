from zwayrest import db
from zwayrest.model.model_base import ModelBase

class DeviceType(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
