from zwayrest import db
from zwayrest.model.model_base import ModelBase

class Device(db.Model, ModelBase):
    id = db.Column(db.Integer, primary_key = True)
    zway_id = db.Column(db.Integer, unique = True)
    name = db.Column(db.String(50))
    device_type_id = db.Column(db.Integer, db.ForeignKey('device_type.id'))
    device_type = db.relationship('DeviceType')
    description = db.Column(db.Text())
